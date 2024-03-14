# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore       import Qt, pyqtSignature, QDate, QDateTime, QTime

from library.Utils      import forceInt, forceRef, forceString

from Events.Utils       import getActionTypeIdListByFlatCode
from Orgs.Utils         import getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Reports.Utils      import ( dateRangeAsStr,
                                 getDataOrgStructureCode,
                                 getDataOrgStructureName,
                                 getDataOrgStructureStay,
                                 getNoPropertyAPHBP,
                                 getOrgStructureProperty,
                                 getPropertyAPHBP,
                                 getPropertyAPHBPName,
                                 getPropertyAPHBPNoProfile,
                                 getStringProperty,
                                 getTransferProperty,
                                 isEXISTSTransfer,
                               )

from Reports.Ui_StationaryF007Setup import Ui_StationaryF007SetupDialog


class CStationaryF007SetupDialog(QtGui.QDialog, Ui_StationaryF007SetupDialog):
    def __init__(self, parent=None, currentOrgStructureId=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.currentOrgStructureId = currentOrgStructureId
        if not self.currentOrgStructureId:
            self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
            self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        else:
            self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
            self.cmbOrgStructure.setValue(self.currentOrgStructureId)
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', True)
        self.edtTimeEdit.setTime(QTime(9, 0, 0, 0))
        self._begDateVisible = False
        self.setBegDateVisible(self._begDateVisible)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setBegDateVisible(self, value):
        self._begDateVisible = value
        self.lblBegDate.setVisible(value)
        self.edtBegDate.setVisible(value)
        self.edtBegTime.setVisible(value)
        if value:
            self.lblEndDate.setText(u'Дата окончания')
        else:
            self.lblEndDate.setText(u'Текущий день')


    def setParams(self, params):
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtTimeEdit.setTime(params.get('endTime', QTime(9, 0, 0, 0)))
        if self.currentOrgStructureId:
            self.cmbOrgStructure.setValue(self.currentOrgStructureId)
        else:
            self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSchedule.setCurrentIndex(params.get('bedsSchedule', 0))
        self.cmbHospitalBedProfile.setValue(params.get('hospitalBedProfileId', None))
        self.chkNoProfileBed.setChecked(params.get('noProfileBed', True))
        self.chkIsPermanentBed.setChecked(params.get('isPermanentBed', False))
        self.chkIsGroupingOS.setChecked(params.get('isGroupingOS', False))
        self.chkNoPrintCaption.setChecked(params.get('noPrintCaption', True))
        self.chkIsEventInfo.setChecked(params.get('isEventInfo', False))
        self.chkCompactInfo.setChecked(params.get('isCompactInfo', False))
        self.chkNoPrintFilterParameters.setChecked(params.get('noPrintFilterParameters', False))
        if self._begDateVisible:
            self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
            self.edtBegTime.setTime(params.get('begTime', QTime(9, 0, 0, 0)))


    def params(self):
        def getPureHMTime(time):
            return QTime(time.hour(), time.minute())

        result = {}
        result['endDate'] = self.edtEndDate.date()
        result['endTime'] = getPureHMTime(self.edtTimeEdit.time())
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['bedsSchedule'] = self.cmbSchedule.currentIndex()
        result['hospitalBedProfileId'] = self.cmbHospitalBedProfile.value()
        result['noProfileBed'] = self.chkNoProfileBed.isChecked()
        result['isPermanentBed'] = self.chkIsPermanentBed.isChecked()
        result['isGroupingOS'] = self.chkIsGroupingOS.isChecked()
        result['isEventInfo'] = self.chkIsEventInfo.isChecked()
        result['isCompactInfo'] = self.chkCompactInfo.isChecked()
        result['noPrintCaption'] = self.chkNoPrintCaption.isChecked()
        result['noPrintFilterParameters'] = self.chkNoPrintFilterParameters.isChecked()
        if self._begDateVisible:
            result['begDate'] = self.edtBegDate.date()
            result['begTime'] = getPureHMTime(self.edtBegTime.time())
        return result


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        endDate = date
        if endDate:
            begTime = self.edtTimeEdit.time()
            stringInfo = u'c %s до %s'%(forceString(QDateTime(endDate.addDays(-1), begTime)), forceString(QDateTime(endDate, begTime)))
        else:
            stringInfo = u'Введите дату'
        self.lblEndDate.setToolTip(stringInfo)


class CStationaryTallySheetMoving(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.orientation = CPageFormat.Landscape
        self.stationaryF007SetupDialog = None
        self.clientDeath = 8
        self.currentOrgStructureId = None


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params, onlyDates):
        description = []
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        if endDate:
            endTime = params.get('endTime', QTime(9, 0, 0, 0))
            begTime = params.get('begTime', None)
            endDateTime = QDateTime(endDate, endTime)
            if not begDate:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(endDate.addDays(-1), begTime)
#                description.append(u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
#                if begDateTime.date() or endDateTime.date():
#                    description.append(dateRangeAsStr(u'за период', begDateTime, endDateTime))
        if onlyDates:
            orgStructureId = params.get('orgStructureId', None)
            bedsSchedule = params.get('bedsSchedule', 0)
            hospitalBedProfileId = params.get('hospitalBedProfileId', None)
            noProfileBed = params.get('noProfileBed', True)
            isPermanentBed = params.get('isPermanentBed', False)
            if orgStructureId:
                description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
            else:
                description.append(u'подразделение: ЛПУ')
            description.append(u'режим койки: %s'%([u'Не учитывать', u'Круглосуточные', u'Не круглосуточные'][bedsSchedule]))
            if hospitalBedProfileId:
                description.append(u'профиль койки: %s'%(forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name'))))
            if noProfileBed:
                description.append(u'учитывать койки с профилем и без профиля')
            else:
                description.append(u'учитывать койки с профилем')
            if isPermanentBed:
                description.append(u'учитывать внештатные койки')
            else:
                description.append(u'учитывать штатные койки')
        #description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignCenter) ]
        tableTop = createTable(cursor, columns, headerRowCount=1, border=0, cellPadding=2, cellSpacing=0)
        if not begDate:
            tableTop.setText(0, 0, u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
        else:
            if begDateTime.date() or endDateTime.date():
                tableTop.setText(0, 0, dateRangeAsStr(u'за период', begDateTime, endDateTime))
        cursor.movePosition(QtGui.QTextCursor.End)

        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)


    def getCaption(self, cursor, params, title):
        orgId = QtGui.qApp.currentOrgId()
        orgName = u''
        if orgId:
            record = QtGui.qApp.db.getRecordEx('Organisation', 'shortName, OKPO', 'id=%s AND deleted = 0'%(str(orgId)))
            if record:
                orgName = forceString(record.value('shortName'))
        orgStructureId = params.get('orgStructureId', None)
        underCaptionList = []
        if orgStructureId:
            underCaptionList.append(u'подразделение: ' + forceString(getOrgStructureFullName(orgStructureId)))
        else:
            underCaptionList.append(u'подразделение: ЛПУ')
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        if hospitalBedProfileId:
            underCaptionList.append(u'профиль койки: %s'%(forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name'))))

        columns = [('70%', [], CReportBase.AlignLeft), ('30%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=7, border=0, cellPadding=2, cellSpacing=0)
        table.setText(0, 0, u'')
        table.setText(0, 1, u'Приложение №2')
        table.setText(1, 0, u'')
        table.setText(1, 1, u'к приказу Минздрава России')
        table.setText(2, 0, u'')
        table.setText(2, 1, u'от 30.12.2002 №413')
        table.setText(3, 0, u'')
        table.setText(3, 1, u'Медицинская документация')
        table.setText(4, 0, u'')
        table.setText(4, 1, u'Форма № 007/у-02')
        table.setText(5, 0, u'')
        table.setText(5, 1, u'Утверждена Минздравом России')
        table.setText(6, 0, orgName)
        table.setText(6, 1, u'от 30.12.2002 №413')

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        columns2 = [('100%', [], CReportBase.AlignCenter)]
        table2 = createTable(cursor, columns2, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        table2.setText(0, 0, title, charFormat=boldChars)
        table2.setText(1, 0, u', '.join(underCaption for underCaption in underCaptionList if underCaption))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getSetupDialog(self, parent):
        result = CStationaryF007SetupDialog(parent, self.currentOrgStructureId)
        result.setBegDateVisible(True)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.chkIsEventInfo.setVisible(False)
        self.stationaryF007SetupDialog.chkCompactInfo.setVisible(False)
        return result


    def build(self, params):
        db = QtGui.qApp.db
        tableOS = db.table('OrgStructure')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableVHospitalBed = db.table('vHospitalBed')
        tableHBSchedule = db.table('rbHospitalBedShedule')
        tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        if endDate:
            endTime = params.get('endTime', QTime(9, 0, 0, 0))
            begTime = params.get('begTime', None)
            endDateTime = QDateTime(endDate, endTime)
            if not begDate:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(endDate.addDays(-1), begTime)
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
            bedsSchedule = params.get('bedsSchedule', 0)
            hospitalBedProfileId = params.get('hospitalBedProfileId', None)
            orgStructureId = params.get('orgStructureId', None)
            noProfileBed = params.get('noProfileBed', True)
            isPermanentBed = params.get('isPermanentBed', False)
            noPrintCaption = params.get('noPrintCaption', False)
            isGroupingOS = params.get('isGroupingOS', False)
            noPrintParams = params.get('noPrintFilterParameters', False)
            orgStructureIndex = self.stationaryF007SetupDialog.cmbOrgStructure._model.index(self.stationaryF007SetupDialog.cmbOrgStructure.currentIndex(), 0, self.stationaryF007SetupDialog.cmbOrgStructure.rootModelIndex())
            begOrgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)

            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertBlock()
            if not noPrintCaption:
                self.getCaption(cursor, params, u'Листок учета движения больных и коечного фонда стационара')
            else:
                cursor.insertText(self.title())
            cursor.insertBlock()
            self.dumpParams(cursor, params, not noPrintParams)
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            cols = [('14%',[u'', u'', u'', u'', u'1'], CReportBase.AlignLeft),
                    ('4.5%', [u'Код', u'', u'', u'', u'2'], CReportBase.AlignLeft),
                    ('4.5%', [u'Факт. разв. коек, в т.ч. койки, свернутые', u'', u'', u'', u'3'], CReportBase.AlignRight),
                    ('3.5%', [u'В том числе коек, свернутых', u'', u'', u'', u'4'], CReportBase.AlignRight),
                    ('3.5%', [u'Движение больных за истекшие сутки', u'Сост. больных на начало истекших суток', u'',u'', u'5'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Поступило больных(без переведенных внутри больницы)', u'Всего', u'', '6'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'Плановых', u'', '7'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'Экстренных', u'', '8'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'в т.ч. из ДС', u'', '9'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'Из них', u'С.ж.', u'10'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'', u'0 - 17', u'11'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Переведено больных внутри больницы', u'Из др. отделений', u'', u'12'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'В др. отделения', u'', u'13'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Выписано больных', u'Всего', u'', u'14'], CReportBase.AlignRight),
                    ('3.9%', [u'', u'', u'В т.ч. перев. в др. стац', u'', u'15'], CReportBase.AlignRight),
                    ('3.1%', [u'', u'', u'В ДС', u'', u'16'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Умерло', u'', u'', u'17'], CReportBase.AlignRight),
                    ('3.5%', [u'На начало текущего дня', u'Состоит больных', u'Всего', u'', u'18'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'В т.ч. с.ж.', u'', u'19'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Состоит матерей при больных детях', u'Всего', u'', u'20'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'с питанием', u'', u'21'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'без питания', u'', u'22'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'отказ от питания', u'', u'23'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'Свободных мест', u'Всего', u'', u'24'], CReportBase.AlignRight),
                    ('3.5%', [u'', u'', u'Иностранцы', u'', u'25'], CReportBase.AlignRight)
                   ]
            table = createTable(cursor, cols)
            table.mergeCells(0, 0, 4, 1) # 1
            table.mergeCells(0, 1, 4, 1) # код
            table.mergeCells(0, 2, 4, 1) # развернуто коек
            table.mergeCells(0, 3, 4, 1) # свернутых
            table.mergeCells(0, 4, 1, 13) # Движение больных за истекшие сутки
            table.mergeCells(1, 4, 3, 1) # Состояло больных на начало истекших суток
            table.mergeCells(1, 5, 1, 6) # Поступило больных
            table.mergeCells(2, 5, 2, 1) # - Плановых
            table.mergeCells(2, 6, 2, 1) # - Экстренных
            table.mergeCells(2, 7, 2, 1) # - Всего
            table.mergeCells(2, 8, 2, 1) # Поступило больных - Из них-
            table.mergeCells(2, 9, 1, 2) #
            table.mergeCells(1, 11, 1, 2) # Переведено больных внутри больницы
            table.mergeCells(2, 11, 2, 1) # -Из других отделений
            table.mergeCells(2, 12, 2, 1) # Переведено больных внутри больницы-В другие отделения
            table.mergeCells(1, 13, 1, 3) # Выписано больных
            table.mergeCells(2, 13, 2, 1) # -Всего
            table.mergeCells(2, 14, 2, 1) # Выписано больных-В т.ч. переведенных в другие стационары
            table.mergeCells(2, 15, 2, 1) # Выписано больных-В т.ч. в дневной стационар
            table.mergeCells(1, 16, 3, 1) # Умерло
            table.mergeCells(0, 17, 1, 8) # На начало текущего дня
            table.mergeCells(1, 17, 1, 2) # -Состоит больных
            table.mergeCells(2, 17, 2, 1) # -Всего
            table.mergeCells(2, 18, 2, 1) # На начало текущего дня-Состоит больных-В т.ч. сельских жителей
            table.mergeCells(1, 19, 1, 4) # Состоит матерей при больных детях
            table.mergeCells(2, 19, 2, 1) # Состоит матерей при больных детях
            table.mergeCells(2, 20, 2, 1) # Состоит матерей с питанием
            table.mergeCells(2, 21, 2, 1) # Состоит матерей без питания
            table.mergeCells(2, 22, 2, 1) # Состоит матерей отказ от питания
            table.mergeCells(2, 23, 2, 1) # Свободных мест
            table.mergeCells(1, 24, 3, 1) # -Иностранцы

            self.countBedsRepairsAll = 0
            self.movingPresentAll = 0
            self.movingTransferAll = 0
            self.receivedBedsAllSUM = 0
            self.receivedInfo0 = 0
            self.receivedInfo6 = 0
            self.receivedInfo4 = 0
            self.receivedInfo3 = 0
            self.receivedInfo1 = 0
            self.receivedInfo2 = 0
            self.countBedsAll = 0
            self.inMovingTransferAll = 0
            self.leavedTransferSUM = 0
            self.countLeavedSUM = 0
            self.leavedDeathSUM = 0
            self.countStationaryDaySUM = 0
            self.presentAllSUM = 0
            self.clientRuralSUM = 0
            self.presentPatronagSUM = 0
            self.feedPatronagSUM = 0
            self.nofeedPatronagSUM = 0
            self.refusalToEatPatronage = 0
            self.foreignSubjectSUM = 0
            self.bedsAllSUM = 0
            self.bedsMenSUM = 0
            self.bedsWomenSUM = 0

            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            cursor.insertBlock()
            currentPersonId = QtGui.qApp.userId
            currentPerson = forceString(db.translate('vrbPerson', 'id', currentPersonId, 'name'))
            headNurseId = forceRef(db.translate(tableOS, 'id', orgStructureId, 'headNurse_id'))

            columns = [('70%', [], CReportBase.AlignLeft), ('30%', [], CReportBase.AlignLeft)]
            tableBot = createTable(cursor, columns, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
            tableBot.setText(0, 0, u'Дежурная медсестра ___________________ /%s/' %currentPerson)
            tableBot.setText(0, 1, u'')
            if orgStructureId and headNurseId:
                headNurse = forceString(db.translate('vrbPerson', 'id', headNurseId, 'name'))
                tableBot.setText(1, 0, u'Старшая медсестра ____________________ /%s/' %headNurse)
            else:
                tableBot.setText(1, 0, u'Старшая медсестра ____________________________________________')
            tableBot.setText(1, 1, u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()


            def getHospitalBedProfile(orgStructureIdList):
                def getHospitalBedId():
                    cond = []
                    tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                    cond.append(tableOS['type'].ne(0))
                    cond.append(tableOS['deleted'].eq(0))
                    if orgStructureIdList:
                        cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                    if bedsSchedule:
                        tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                    if bedsSchedule == 1:
                        cond.append(tableHBSchedule['code'].eq(1))
                    elif bedsSchedule == 2:
                        cond.append(tableHBSchedule['code'].ne(1))
                    if not isPermanentBed:
                        cond.append(tableVHospitalBed['isPermanent'].eq(1))
                    joinOr1 = db.joinAnd([tableVHospitalBed['begDate'].isNotNull(), tableVHospitalBed['endDate'].isNotNull(),
                    tableVHospitalBed['begDate'].lt(endDateTime), tableVHospitalBed['endDate'].gt(begDateTime)])
                    joinOr2 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)])
                    joinOr3 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].le(begDateTime)])
                    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3]))
                    return db.getDistinctIdList(tableVHospitalBedSchedule, [tableVHospitalBed['id']], cond)
                cond = []
                profileIdList = []
                self.hospitalBedIdList = []
                if orgStructureIdList:
                    cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
                if QtGui.qApp.defaultHospitalBedProfileByMoving():
                    self.hospitalBedIdList = getHospitalBedId()
                    tableRbAPHBP = db.table('ActionProperty_rbHospitalBedProfile')
                    tableAP = db.table('ActionProperty')
                    tableAction = db.table('Action')
                    tableAPT = db.table('ActionPropertyType')
                    queryTable = tableRbAPHBP.innerJoin(tableAP, tableRbAPHBP['id'].eq(tableAP['id']))
                    queryTable = queryTable.innerJoin(tableRbHospitalBedProfile, tableRbHospitalBedProfile['id'].eq(tableRbAPHBP['value']))
                    queryTable = queryTable.innerJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
                    queryTable = queryTable.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                    cond = [tableAP['action_id'].isNotNull(),
                            tableAP['deleted'].eq(0),
                            tableAction['deleted'].eq(0),
                            tableAPT['deleted'].eq(0),
                            tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
                            tableAPT['typeName'].like('rbHospitalBedProfile')
                            ]
                    joinOr1 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNull()])
                    joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
                    joinOr3 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDateTime)])
                    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3]))
                    cond.append(u'''EXISTS(SELECT APHB.value
    FROM ActionProperty AS AP
    INNER JOIN ActionProperty_HospitalBed AS APHB ON APHB.`id`=AP.`id`
    INNER JOIN Action AS A ON A.`id`=AP.`action_id`
    INNER JOIN ActionPropertyType AS APT ON APT.`id`=AP.`type_id`
    WHERE (AP.`action_id` IS NOT NULL AND AP.`action_id` = Action.id) AND (AP.`deleted`=0) AND (APT.`deleted`=0)
    AND (APT.`typeName` = 'HospitalBed') AND (APHB.`value` IN (%s)))'''%(u','.join(str(hospitalBedId) for hospitalBedId in self.hospitalBedIdList if hospitalBedId)))
                    records = db.getRecordList(queryTable, [tableRbHospitalBedProfile['id'], tableRbHospitalBedProfile['code'], tableRbHospitalBedProfile['name']], cond)
                    for record in records:
                        profileId = forceRef(record.value('id'))
                        if profileId not in profileIdList:
                            profileIdList.append(profileId)
                else:
                    if not noProfileBed:
                        cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
                    queryTable = tableOSHB.innerJoin(tableRbHospitalBedProfile, tableOSHB['profile_id'].eq(tableRbHospitalBedProfile['id']))
                    queryTable = queryTable.innerJoin(tableOS,  tableOSHB['master_id'].eq(tableOS['id']))
                    cond.append(tableOS['type'].ne(0))
                    cond.append(tableOS['deleted'].eq(0))
                    if bedsSchedule:
                        queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
                        if bedsSchedule == 1:
                            cond.append(tableHBSchedule['code'].eq(1))
                        elif bedsSchedule == 2:
                            cond.append(tableHBSchedule['code'].ne(1))
                    if hospitalBedProfileId:
                        cond.append(tableRbHospitalBedProfile['id'].eq(hospitalBedProfileId))
                    joinOr1 = db.joinAnd([tableOSHB['begDate'].isNull(), tableOSHB['endDate'].isNull()])
                    joinOr2 = db.joinAnd([tableOSHB['begDate'].isNotNull(), tableOSHB['endDate'].isNotNull(),
                    tableOSHB['begDate'].le(endDateTime), tableOSHB['endDate'].ge(begDateTime)])
                    joinOr3 = db.joinAnd([tableOSHB['begDate'].isNull(), tableOSHB['endDate'].ge(begDateTime)])
                    joinOr4 = db.joinAnd([tableOSHB['endDate'].isNull(), tableOSHB['begDate'].le(endDateTime)])
                    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3, joinOr4]))
                    profileIdList = db.getDistinctIdList(queryTable, [tableRbHospitalBedProfile['id']], cond)
                if not profileIdList:
                    return None
                if noProfileBed:
                    profileIdList.append(None)
                return profileIdList

            def getDataReport(parOrgStructureIdList, rowProfile, table, sumRowProfile, groupOS, profileIdList, isGroupingOS=False):
                db = QtGui.qApp.db
                tableAPT = db.table('ActionPropertyType')
                tableAP = db.table('ActionProperty')
                tableActionType = db.table('ActionType')
                tableAction = db.table('Action')
                tableEvent = db.table('Event')
                tableClient = db.table('Client')
                tableOS = db.table('OrgStructure')
                tableAPHB = db.table('ActionProperty_HospitalBed')
                tableOSHB = db.table('OrgStructure_HospitalBed')
                tableVHospitalBed = db.table('vHospitalBed')
                tableHBSchedule = db.table('rbHospitalBedShedule')

                orgStructureIdList = parOrgStructureIdList
                self.receivedBedsAll = 0
                self.countBeds = 0
                self.presentAll = 0

                def getBedForProfile(noProfileBed, profile = None, hospitalBedIdList = None, countSetText = True, row = None, column = None, groupOS = False):
                    tableRbAPHBP = db.table('ActionProperty_rbHospitalBedProfile')
                    tableAP = db.table('ActionProperty')
                    tableAction = db.table('Action')
                    tableAPT = db.table('ActionPropertyType')
                    tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')
                    queryTable = tableRbAPHBP.innerJoin(tableAP, tableRbAPHBP['id'].eq(tableAP['id']))
                    queryTable = queryTable.innerJoin(tableRbHospitalBedProfile, tableRbHospitalBedProfile['id'].eq(tableRbAPHBP['value']))
                    queryTable = queryTable.innerJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
                    queryTable = queryTable.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
                    cond = [tableAP['action_id'].isNotNull(),
                            tableAP['deleted'].eq(0),
                            tableAction['deleted'].eq(0),
                            tableAPT['deleted'].eq(0),
                            tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
                            tableAPT['typeName'].like('rbHospitalBedProfile')
                            ]
                    if profile:
                        if noProfileBed and len(profile) > 1:
                            cond.append(db.joinOr([tableRbHospitalBedProfile['profile_id'].inlist(profile), tableRbHospitalBedProfile['profile_id'].isNull()]))
                        else:
                            cond.append(tableRbHospitalBedProfile['id'].inlist(profile))
                    else:
                        cond.append(tableRbHospitalBedProfile['id'].isNull())
                    joinOr1 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNull()])
                    joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
                    joinOr3 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDateTime)])
                    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3]))
                    cond.append(u'''EXISTS(SELECT APHB.value
    FROM ActionProperty AS AP
    INNER JOIN ActionProperty_HospitalBed AS APHB ON APHB.`id`=AP.`id`
    INNER JOIN Action AS A ON A.`id`=AP.`action_id`
    INNER JOIN ActionPropertyType AS APT ON APT.`id`=AP.`type_id`
    WHERE (AP.`action_id` IS NOT NULL AND AP.`action_id` = Action.id) AND (AP.`deleted`=0) AND (APT.`deleted`=0)
    AND (APT.`typeName` = 'HospitalBed') AND (APHB.`value` IN (%s)))'''%(u','.join(str(hospitalBedId) for hospitalBedId in hospitalBedIdList if hospitalBedId)))
                    if countSetText:
                        self.countBeds = db.getCount(queryTable, countCol='rbHospitalBedProfile.id', where=cond)
                        if row:
                           table.setText(row, column, self.countBeds)
                        else:
                            table.setText(sumRowProfile, column, self.countBeds)
                            if groupOS:
                                self.countBedsAll += self.countBeds
                                table.setText(rowProfile, column, self.countBedsAll)
                        return None
                    else:
                        return db.getDistinctIdList(queryTable, [tableRbHospitalBedProfile['id']], cond)

                def unrolledHospitalBed34(profile = None, row = None, groupOS = False):
                    condRepairs = ['''OrgStructure_HospitalBed_Involution.involutionType != 0
                                           AND (OrgStructure_HospitalBed_Involution.begDate IS NULL
                                           OR OrgStructure_HospitalBed_Involution. endDate IS NULL
                                           OR (OrgStructure_HospitalBed_Involution.begDate >= '%s'
                                           AND OrgStructure_HospitalBed_Involution. endDate <= '%s'))'''%(begDateTime.toString(Qt.ISODate), begDateTime.toString(Qt.ISODate))]
                    tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
                    tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                    if not noProfileBed:
                        condRepairs.append('vHospitalBed.profile_id IS NOT NULL')
                    if not isPermanentBed:
                        condRepairs.append(tableVHospitalBed['isPermanent'].eq(1))
                    if QtGui.qApp.defaultHospitalBedProfileByMoving():
                        condRepairs.append(tableOS['type'].ne(0))
                        condRepairs.append(tableOS['deleted'].eq(0))
                        if bedsSchedule:
                            tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                        if bedsSchedule == 1:
                            condRepairs.append(tableHBSchedule['code'].eq(1))
                        elif bedsSchedule == 2:
                            condRepairs.append(tableHBSchedule['code'].ne(1))
                        if orgStructureIdList:
                            condRepairs.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                        bedRepairIdList = db.getDistinctIdList(tableVHospitalBedSchedule.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id'])), [tableVHospitalBed['id']], condRepairs)
                        if self.hospitalBedIdList:
                            getBedForProfile(noProfileBed, profile, self.hospitalBedIdList, True, row, 2, groupOS)
                        else:
                            table.setText(row if row else sumRowProfile, 2, 0)
                            if groupOS:
                                table.setText(rowProfile, 2, 0)
                        if bedRepairIdList:
                            getBedForProfile(noProfileBed, profile, bedRepairIdList, True, row, 3, groupOS)
                        else:
                            table.setText(row if row else sumRowProfile, 3, 0)
                            if groupOS:
                                table.setText(rowProfile, 3, 0)
                    else:
                        cond = []
                        cond.append(tableOS['type'].ne(0))
                        cond.append(tableOS['deleted'].eq(0))
                        if orgStructureIdList:
                            cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                        if not isPermanentBed:
                            cond.append(tableVHospitalBed['isPermanent'].eq(1))
                        if profile:
                            if noProfileBed and len(profile) > 1:
                                cond.append(db.joinOr([tableVHospitalBed['profile_id'].inlist(profile), tableVHospitalBed['profile_id'].isNull()]))
                            else:
                                cond.append(tableVHospitalBed['profile_id'].inlist(profile))
                        else:
                            cond.append(tableVHospitalBed['profile_id'].isNull())
                        if bedsSchedule:
                            tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                        if bedsSchedule == 1:
                            cond.append(tableHBSchedule['code'].eq(1))
                            condRepairs.append(tableHBSchedule['code'].eq(1))
                        elif bedsSchedule == 2:
                            cond.append(tableHBSchedule['code'].ne(1))
                            condRepairs.append(tableVHospitalBed['code'].ne(1))

                        cond.append(db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)]))
                        cond.append(db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(begDateTime)]))
                        condRepairs.append(tableOS['type'].ne(0))

                        if orgStructureIdList:
                            condRepairs.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                        if profile:
                            if noProfileBed and len(profile) > 1:
                                condRepairs.append(db.joinOr([tableVHospitalBed['profile_id'].inlist(profile), tableVHospitalBed['profile_id'].isNull()]))
                            else:
                                condRepairs.append(tableVHospitalBed['profile_id'].inlist(profile))
                        else:
                            condRepairs.append(tableVHospitalBed['profile_id'].isNull())
                        self.countBeds = db.getCount(tableVHospitalBedSchedule, countCol='vHospitalBed.id', where=cond)
                        countBedsRepairs = db.getCount(tableVHospitalBedSchedule.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id'])), countCol='vHospitalBed.id', where=condRepairs)
                        if row:
                           table.setText(row, 2, self.countBeds)
                           table.setText(row, 3, countBedsRepairs)
                        else:
                            table.setText(sumRowProfile, 2, self.countBeds)
                            table.setText(sumRowProfile, 3, countBedsRepairs)
                            if groupOS:
                                self.countBedsAll += self.countBeds
                                self.countBedsRepairsAll += countBedsRepairs

                def getMovingPresent(profile = None, flagCurrent = False):
                    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
                             tableAction['deleted'].eq(0),
                             tableEvent['deleted'].eq(0),
                             tableAP['deleted'].eq(0),
                             tableActionType['deleted'].eq(0),
                             tableClient['deleted'].eq(0),
                             tableAP['action_id'].eq(tableAction['id'])
                           ]
                    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
                    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
                    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
                    queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
                    queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
                    queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
                    queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
                    queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
                    cond.append(tableOS['deleted'].eq(0))
                    cond.append(tableOS['type'].ne(0))
                    cond.append(tableAPT['typeName'].like('HospitalBed'))
                    if orgStructureIdList:
                        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
                    if not noProfileBed:
                        cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
                    if profile:
                        if QtGui.qApp.defaultHospitalBedProfileByMoving():
                            cond.append(getPropertyAPHBP(profile, noProfileBed))
                        else:
                            if noProfileBed and len(profile) > 1:
                                cond.append(db.joinOr([tableOSHB['profile_id'].inlist(profile), tableOSHB['profile_id'].isNull()]))
                            else:
                                cond.append(tableOSHB['profile_id'].inlist(profile))
                    else:
                        if QtGui.qApp.defaultHospitalBedProfileByMoving():
                            cond.append(getPropertyAPHBP([], noProfileBed))
                        else:
                            cond.append(tableOSHB['profile_id'].isNull())
                    if bedsSchedule:
                        queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
                    if bedsSchedule == 1:
                        cond.append(tableHBSchedule['code'].eq(1))
                    elif bedsSchedule == 2:
                        cond.append(tableHBSchedule['code'].ne(1))
                    if flagCurrent:
                        cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
                        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
                        stmtPatronageFeed = u'''EXISTS(SELECT Event.relative_id
                        FROM Event_Feed
                        WHERE Event_Feed.event_id = Event.id AND Event_Feed.typeFeed = 1
                        AND Event_Feed.deleted = 0 AND Event.relative_id IS NOT NULL
                        AND Event_Feed.refusalToEat = 0
                        AND DATE(Event_Feed.date) = DATE(%s)
                        GROUP BY Event.id
                        ORDER BY Event_Feed.refusalToEat DESC LIMIT 1)'''%(db.formatDate(endDateTime))
                        stmtPatronageNoFeed = u'''IF(EXISTS( SELECT
                        APS.id
                        FROM
                        ActionProperty AS AP
                            INNER JOIN
                        ActionPropertyType AS APT ON AP.type_id = APT.id
                            INNER JOIN
                        ActionProperty_String AS APS ON APS.id = AP.id
                        WHERE
                        AP.action_id = Action.id
                            AND APT.actionType_id = Action.actionType_id
                            AND Action.id IS NOT NULL
                            AND APT.deleted = 0
                            AND AP.deleted = 0
                            AND APT.name = 'Патронаж'
                            AND (APS.value = 'Да'))
                        AND NOT EXISTS(SELECT Event.relative_id
                        FROM Event_Feed
                        WHERE Event_Feed.event_id = Event.id AND Event_Feed.typeFeed = 1
                        AND Event_Feed.deleted = 0 AND Event.relative_id IS NOT NULL
                        AND Event_Feed.refusalToEat = 0
                        AND DATE(Event_Feed.date) = DATE(%s)
                        GROUP BY Event.id
                        ORDER BY Event_Feed.refusalToEat DESC LIMIT 1), 1, 0)'''%(db.formatDate(endDateTime))
                        stmtPatronageRefusalToEat = u'''EXISTS(SELECT Event.relative_id
                        FROM Event_Feed
                        WHERE Event_Feed.event_id = Event.id AND Event_Feed.typeFeed = 1
                        AND Event_Feed.deleted = 0 AND Event.relative_id IS NOT NULL
                        AND Event_Feed.refusalToEat = 1
                        AND DATE(Event_Feed.date) = DATE(%s)
                        GROUP BY Event.id
                        ORDER BY Event_Feed.refusalToEat DESC LIMIT 1)'''%(db.formatDate(endDateTime))
                        stmtForeignSubject = u'''EXISTS(SELECT rbSocStatusType.id
                        FROM rbSocStatusType
                        WHERE rbSocStatusType.code = getClientCitizenship(Event.client_id, Action.begDate))'''
                        countAll = 0
                        countPatronage = 0
                        feedPatronage = 0
                        nofeedPatronage = 0
                        refusalToEatPatronage = 0
                        clientRural = 0
                        foreignSubject = 0
                        stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countPatronage, SUM(isClientVillager(Client.id)) AS clientRural, SUM(%s) AS foreignSubject'
                                            %(getStringProperty(u'Патронаж%', u'(APS.value = \'Да\')'), stmtForeignSubject), where=cond)
                        query = db.query(stmt)
                        if query.first():
                            record = query.record()
                            countAll = forceInt(record.value('countAll'))
                            countPatronage = forceInt(record.value('countPatronage'))
                            clientRural = forceInt(record.value('clientRural'))
                            foreignSubject = forceInt(record.value('foreignSubject'))
                        stmt = db.selectStmtGroupBy(queryTable, u'SUM(%s) AS feedPatronage, SUM(%s) AS nofeedPatronage, SUM(%s) AS refusalToEatPatronage'
                                            %(stmtPatronageFeed, stmtPatronageNoFeed, stmtPatronageRefusalToEat), where=cond, group=u'Event.id')
                        query = db.query(stmt)
                        while query.next():
                            record = query.record()
                            feedPatronage += forceInt(record.value('feedPatronage'))
                            nofeedPatronage += forceInt(record.value('nofeedPatronage'))
                            refusalToEatPatronage += forceInt(record.value('refusalToEatPatronage'))
                        return [countAll, countPatronage, feedPatronage, nofeedPatronage, clientRural, foreignSubject, refusalToEatPatronage]
                    else:
                        cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(begDateTime)]))
                        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(begDateTime)]))
                        return db.getCount(queryTable, countCol='Client.id', where=cond)

                def presentBegDay(profile = None, row = None, groupOS = False):
                    if row:
                        table.setText(row, 4, getMovingPresent(profile))
                    else:
                        movingPresent = getMovingPresent(profile)
                        table.setText(sumRowProfile, 4, movingPresent)
                        if groupOS:
                            self.movingPresentAll += movingPresent
                # из других отделений
                def fromMovingTransfer(profile = None, row = None, groupOS = False):
                    if row:
                        table.setText(row, 11, getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1))
                    else:
                        movingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1)
                        table.setText(sumRowProfile, 11, movingTransfer)
                        if groupOS:
                            self.movingTransferAll += movingTransfer

                def receivedAll(profile = None, row = None, groupOS = False):
                    self.receivedBedsAll = 0
                    if row:
                        #all, children, adultCount, clientRural, isStationaryDay, orderPlan, orderExtren
                        receivedInfo = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList)
                        receivedBedAll = receivedInfo[5]
                        childrenCount = receivedInfo[1]
                        adultCount = receivedInfo[2]
                        clientRural = receivedInfo[3]
                        isStationaryDay = receivedInfo[4]
                        orderExtren = receivedInfo[6]
                        countAll = receivedInfo[0]
                        if noProfileBed and not profile:
                            receivedInfoNoProfile = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList, False, True)
                            receivedBedAllNoProfile = receivedInfoNoProfile[5]
                            receivedBedAll += receivedBedAllNoProfile
                            childrenCountNoProfile = receivedInfoNoProfile[1]
                            childrenCount += childrenCountNoProfile
                            adultCountNoProfile = receivedInfoNoProfile[2]
                            adultCount += adultCountNoProfile
                            clientRuralNoProfile = receivedInfoNoProfile[3]
                            clientRural += clientRuralNoProfile
                            isStationaryDayNoProfile = receivedInfoNoProfile[4]
                            isStationaryDay += isStationaryDayNoProfile
                            orderExtrenNoProfile = receivedInfoNoProfile[6]
                            orderExtren += orderExtrenNoProfile
                            countAllNoProfile = receivedInfoNoProfile[0]
                            countAll += countAllNoProfile
                        self.receivedBedsAll = receivedBedAll
                        table.setText(row, 5,  countAll)
                        table.setText(row, 6,  self.receivedBedsAll)
                        table.setText(row, 7,  orderExtren)
                        table.setText(row, 8,  isStationaryDay)
                        table.setText(row, 9,  clientRural)
                        table.setText(row, 10, childrenCount)
                    else:
                        #all, children, adultCount, clientRural, isStationaryDay, orderPlan, orderExtren
                        receivedInfo = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList)
                        receivedBedAll = receivedInfo[5]
                        childrenCount = receivedInfo[1]
                        adultCount = receivedInfo[2]
                        clientRural = receivedInfo[3]
                        isStationaryDay = receivedInfo[4]
                        orderExtren = receivedInfo[6]
                        countAll = receivedInfo[0]
                        if noProfileBed:
                            receivedInfoNoProfile = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList, False, True)
                            receivedBedAllNoProfile = receivedInfoNoProfile[5]
                            receivedBedAll += receivedBedAllNoProfile
                            childrenCountNoProfile = receivedInfoNoProfile[1]
                            childrenCount += childrenCountNoProfile
                            adultCountNoProfile = receivedInfoNoProfile[2]
                            adultCount += adultCountNoProfile
                            clientRuralNoProfile = receivedInfoNoProfile[3]
                            clientRural += clientRuralNoProfile
                            isStationaryDayNoProfile = receivedInfoNoProfile[4]
                            isStationaryDay += isStationaryDayNoProfile
                            orderExtrenNoProfile = receivedInfoNoProfile[6]
                            orderExtren += orderExtrenNoProfile
                            countAllNoProfile = receivedInfoNoProfile[0]
                            countAll += countAllNoProfile
                        self.receivedBedsAll = receivedBedAll
                        table.setText(sumRowProfile, 5,  countAll)
                        table.setText(sumRowProfile, 6,  self.receivedBedsAll)
                        table.setText(sumRowProfile, 7,  orderExtren)
                        table.setText(sumRowProfile, 8,  isStationaryDay)
                        table.setText(sumRowProfile, 9,  clientRural)
                        table.setText(sumRowProfile, 10, childrenCount)
                        if groupOS:
                            self.receivedBedsAllSUM += self.receivedBedsAll
                            self.receivedInfo6 += orderExtren
                            self.receivedInfo0 += countAll
                            self.receivedInfo4 += isStationaryDay
                            self.receivedInfo3 += clientRural
                            self.receivedInfo1 += childrenCount
                            self.receivedInfo2 += adultCount

                # в другие отделения
                def inMovingTransfer(profile = None, row = None, groupOS = False):
                    if row:
                        table.setText(row, 12, getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0))
                    else:
                        inMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0)
                        table.setText(sumRowProfile, 12, inMovingTransfer)
                        if groupOS:
                            self.inMovingTransferAll += inMovingTransfer

                def leavedAll(profile = None, row = None, groupOS = False):
                    if row:
                        countLeavedAll, leavedDeath, leavedTransfer, countStationaryDay = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed and not profile:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, countStationaryDayNoProfile = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                            countStationaryDay += countStationaryDayNoProfile
                        table.setText(row, 13, countLeavedAll-leavedDeath)
                        table.setText(row, 14, leavedTransfer)
                        table.setText(row, 15, countStationaryDay)
                        table.setText(row, 16, leavedDeath)
                    else:
                        countLeavedAll, leavedDeath, leavedTransfer, countStationaryDay = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, countStationaryDayNoProfile = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                            countStationaryDay += countStationaryDayNoProfile
                        table.setText(sumRowProfile, 13, countLeavedAll-leavedDeath)
                        table.setText(sumRowProfile, 14, leavedTransfer)
                        table.setText(sumRowProfile, 15, countStationaryDay)
                        table.setText(sumRowProfile, 16, leavedDeath)
                        if groupOS:
                            self.countLeavedSUM += countLeavedAll-leavedDeath
                            self.leavedTransferSUM += leavedTransfer
                            self.leavedDeathSUM += leavedDeath
                            self.countStationaryDaySUM += countStationaryDay

                def presentEndDay(profile = None, row = None, groupOS = False):
                    self.presentAll = 0
                    if row:
                        self.presentAll, presentPatronag, feedPatronag, nofeedPatronag, clientRural, foreignSubject, refusalToEatPatronage = getMovingPresent(profile, True)
                        table.setText(row, 17, self.presentAll)
                        table.setText(row, 18, clientRural)
                        table.setText(row, 19, presentPatronag)
                        table.setText(row, 20, feedPatronag)
                        table.setText(row, 21, nofeedPatronag)
                        table.setText(row, 22, refusalToEatPatronage)
                        table.setText(row, 24, foreignSubject)
                    else:
                        self.presentAll, presentPatronag, feedPatronag, nofeedPatronag, clientRural, foreignSubject, refusalToEatPatronage = getMovingPresent(profile, True)
                        table.setText(sumRowProfile, 17, self.presentAll)
                        table.setText(sumRowProfile, 18, clientRural)
                        table.setText(sumRowProfile, 19, presentPatronag)
                        table.setText(sumRowProfile, 20, feedPatronag)
                        table.setText(sumRowProfile, 21, nofeedPatronag)
                        table.setText(sumRowProfile, 22, refusalToEatPatronage)
                        table.setText(sumRowProfile, 24, foreignSubject)
                        if groupOS:
                            self.presentAllSUM += self.presentAll
                            self.clientRuralSUM += clientRural
                            self.presentPatronagSUM += presentPatronag
                            self.feedPatronagSUM += feedPatronag
                            self.nofeedPatronagSUM += nofeedPatronag
                            self.refusalToEatPatronage += refusalToEatPatronage
                            self.foreignSubjectSUM += foreignSubject

                #Всего коек пустых
                def freelyHospitalBedAll(profile = None, row = None, groupOS = False):
                    bedIdList = getHospitalBedIdList(isPermanentBed, begDateTime, endDateTime, orgStructureIdList)
                    tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                    cond = []
                    cond.append(tableOS['type'].ne(0))
                    cond.append(tableOS['deleted'].eq(0))
                    if bedIdList:
                        cond.append(tableVHospitalBed['id'].notInlist(bedIdList))
                    if orgStructureIdList:
                        cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                    if not noProfileBed:
                        cond.append('vHospitalBed.profile_id IS NOT NULL')
                    if profile:
                        if QtGui.qApp.defaultHospitalBedProfileByMoving():
                            profileIdListNoBusi = getBedForProfile(noProfileBed, profile, self.hospitalBedIdList, False, None, None, groupOS)
                            cond.append(tableVHospitalBed['profile_id'].inlist(profileIdListNoBusi))
                        else:
                            if noProfileBed and len(profile) > 1:
                                cond.append(db.joinOr([tableVHospitalBed['profile_id'].inlist(profile), tableVHospitalBed['profile_id'].isNull()]))
                            else:
                                cond.append(tableVHospitalBed['profile_id'].inlist(profile))
                    else:
                        if QtGui.qApp.defaultHospitalBedProfileByMoving():
                            profileIdListNoBusi = getBedForProfile(noProfileBed, [], self.hospitalBedIdList, False, None, None, groupOS)
                            cond.append(tableVHospitalBed['profile_id'].inlist(profileIdListNoBusi))
                        else:
                            cond.append(tableVHospitalBed['profile_id'].isNull())
                    if bedsSchedule:
                        tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                    if bedsSchedule == 1:
                        cond.append(tableHBSchedule['code'].eq(1))
                    elif bedsSchedule == 2:
                        cond.append(tableHBSchedule['code'].ne(1))
                    stmt = db.selectStmt(tableVHospitalBedSchedule, u'COUNT(vHospitalBed.id) AS bedsAll, SUM(IF(vHospitalBed.sex = 1, 1, 0)) AS bedsMen, SUM(IF(vHospitalBed.sex = 2, 1, 0)) AS bedsWomen', where=cond)
                    query = db.query(stmt)
                    if query.first():
                        record = query.record()
                        bedsAll = self.countBeds - self.presentAll
                        bedsMen = forceInt(record.value('bedsMen'))
                        bedsWomen = forceInt(record.value('bedsWomen'))
                    else:
                        bedsAll = 0 - self.presentAll
                        bedsMen = 0
                        bedsWomen = 0
                    if row:
                        table.setText(row, 23, bedsAll)
                    else:
                        table.setText(sumRowProfile, 23, bedsAll)
                        if groupOS:
                            self.bedsAllSUM += bedsAll
                            self.bedsMenSUM += bedsMen
                            self.bedsWomenSUM += bedsWomen

                unrolledHospitalBed34(profileIdList, None, groupOS)
                presentBegDay(profileIdList, None, groupOS)
                receivedAll(profileIdList, None, groupOS)
                fromMovingTransfer(profileIdList, None, groupOS)
                inMovingTransfer(profileIdList, None, groupOS)
                leavedAll(profileIdList, None, groupOS)
                presentEndDay(profileIdList, None, groupOS)
                freelyHospitalBedAll(profileIdList, None, groupOS)
                if noProfileBed:
                    table.setText(rowProfile, 0, u'профиль койки не определен')
                    unrolledHospitalBed34([], rowProfile)
                    presentBegDay([], rowProfile)
                    receivedAll([], rowProfile)
                    fromMovingTransfer([], rowProfile)
                    inMovingTransfer([], rowProfile)
                    leavedAll([], rowProfile)
                    presentEndDay([], rowProfile)
                    freelyHospitalBedAll([], rowProfile)
                cond = []
                queryTable = tableRbHospitalBedProfile
                if QtGui.qApp.defaultHospitalBedProfileByMoving():
                    if hospitalBedProfileId and (hospitalBedProfileId in profileIdList):
                        cond.append(tableRbHospitalBedProfile['id'].eq(hospitalBedProfileId))
                    elif not hospitalBedProfileId and profileIdList:
                        cond.append(tableRbHospitalBedProfile['id'].inlist(profileIdList))
                elif hospitalBedProfileId:
                    cond.append(tableRbHospitalBedProfile['id'].eq(hospitalBedProfileId))
                else:
                    cond.append(tableRbHospitalBedProfile['id'].inlist(profileIdList))
                stmt = db.selectDistinctStmt(queryTable, [tableRbHospitalBedProfile['id'], tableRbHospitalBedProfile['code'], tableRbHospitalBedProfile['name']], cond, u'rbHospitalBedProfile.code')
                query = db.query(stmt)
                sizeQuery = query.size()
                if noProfileBed:
                    if sizeQuery > 0:
                        rowProfile = table.addRow()
                sizeQuery -= 1
                while query.next():
                    record = query.record()
                    profileId = forceRef(record.value('id'))
                    profileCode = forceString(record.value('code'))
                    profileName = forceString(record.value('name'))
                    table.setText(rowProfile, 0, profileName)
                    table.setText(rowProfile, 1, profileCode)
                    unrolledHospitalBed34([profileId], rowProfile)
                    presentBegDay([profileId], rowProfile)
                    receivedAll([profileId], rowProfile)
                    fromMovingTransfer([profileId], rowProfile)
                    inMovingTransfer([profileId], rowProfile)
                    leavedAll([profileId], rowProfile)
                    presentEndDay([profileId], rowProfile)
                    freelyHospitalBedAll([profileId], rowProfile)
                    if sizeQuery > 0:
                        rowProfile = table.addRow()
                        sizeQuery -= 1
                return rowProfile

            boldChars = QtGui.QTextCharFormat()
            boldChars.setFontWeight(QtGui.QFont.Bold)
            def getOrgStructureParent(orgStructureIdList, rowProfile, table):
                for parentOrgStructureId in orgStructureIdList:
                    tableQuery = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
                    recordEx = db.getRecordEx(tableQuery,
                                              [tableOS['name'], tableOS['id']],
                                              [tableOS['deleted'].eq(0),
                                               tableOS['type'].ne(0),
                                               tableOS['id'].eq(parentOrgStructureId)])
                    if recordEx:
                        name = forceString(recordEx.value('name'))
                        table.setText(rowProfile, 0, name, boldChars)
                        sumRowProfile = rowProfile
                        rowProfile = table.addRow()
                        profileIdList = getHospitalBedProfile([parentOrgStructureId])
                        rowProfile = getDataReport([parentOrgStructureId], rowProfile, table, sumRowProfile, True, profileIdList, isGroupingOS)
                        rowProfile = table.addRow()
                        records = db.getRecordList(tableQuery,
                                                   [tableOS['id'], tableOS['name']],
                                                   [tableOS['deleted'].eq(0), tableOS['type'].ne(0),
                                                    tableOS['parent_id'].eq(parentOrgStructureId)])
                        for record in records:
                            name = forceString(record.value('name'))
                            orgStructureId = forceRef(record.value('id'))
                            table.setText(rowProfile, 0, name, boldChars)
                            sumRowProfile = rowProfile
                            rowProfile = table.addRow()
                            profileIdList = getHospitalBedProfile([orgStructureId])
                            rowProfile = getDataReport([orgStructureId], rowProfile, table, sumRowProfile, True, profileIdList, isGroupingOS)
                            rowProfile = table.addRow()
            nextRow = table.addRow()
            if isGroupingOS:
                getOrgStructureParent(begOrgStructureIdList, table.addRow(), table)
                table.setText(nextRow, 0, u'Всего:\n\nв том числе по койкам:', boldChars)
                table.setText(nextRow, 2, self.countBedsAll)
                table.setText(nextRow, 3, self.countBedsRepairsAll)
                table.setText(nextRow, 4, self.movingPresentAll)
                table.setText(nextRow, 5, self.receivedInfo0)
                table.setText(nextRow, 6, self.receivedBedsAllSUM)
                table.setText(nextRow, 7, self.receivedInfo6)
                table.setText(nextRow, 8, self.receivedInfo4)
                table.setText(nextRow, 9, self.receivedInfo3)
                table.setText(nextRow, 10, self.receivedInfo1)
                table.setText(nextRow, 11, self.movingTransferAll)
                table.setText(nextRow, 12, self.inMovingTransferAll)
                table.setText(nextRow, 13, self.countLeavedSUM)
                table.setText(nextRow, 14, self.leavedTransferSUM)
                table.setText(nextRow, 15, self.countStationaryDaySUM)
                table.setText(nextRow, 16, self.leavedDeathSUM)
                table.setText(nextRow, 17, self.presentAllSUM)
                table.setText(nextRow, 18, self.clientRuralSUM)
                table.setText(nextRow, 19, self.presentPatronagSUM)
                table.setText(nextRow, 20, self.feedPatronagSUM) # feed
                table.setText(nextRow, 21, self.nofeedPatronagSUM) # not feed
                table.setText(nextRow, 22, self.refusalToEatPatronage)
                table.setText(nextRow, 23, self.bedsAllSUM)
                table.setText(nextRow, 24, self.foreignSubjectSUM)
                table.delRow(table.rowCount()-1, 1)
            else:
                profileIdList = getHospitalBedProfile(begOrgStructureIdList)
                table.setText(nextRow, 0, u'Всего:\n\nв том числе по койкам:', boldChars)
                getDataReport(begOrgStructureIdList, table.addRow(), table, nextRow, False, profileIdList)
        return doc


def getHospitalBedIdList(isPermanentBed, begDateTime, endDateTime, orgStructureIdList):
    db = QtGui.qApp.db
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableOS = db.table('OrgStructure')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    cols = [tableOSHB['id'].alias('bedId')]
    queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
    queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
    queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
    queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode(u'moving%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableAP['deleted'].eq(0),
             tableAPT['typeName'].like('HospitalBed'),
             tableAP['action_id'].eq(tableAction['id'])
           ]
    cond.append(tableOS['type'].ne(0))
    if orgStructureIdList:
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
    cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
    cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
    cond.append(db.joinOr([tableOS['id'].isNull(), db.joinAnd([tableOS['deleted'].eq(0), tableOS['type'].ne(0)])]))
    return db.getDistinctIdList(queryTable, cols, cond)


def getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty, profile = None, transferIn = False, orgStructureIdList = [], boolFIO = False, getOrgStructureCode = False, transferType=0):
    db = QtGui.qApp.db
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')
    tableOS = db.table('OrgStructure')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    tableHBSchedule = db.table('rbHospitalBedShedule')
    tableHBProfile = db.table('rbHospitalBedProfile')

    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableAP['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             tableClient['deleted'].eq(0),
             tableAP['action_id'].eq(tableAction['id'])
           ]
    if transferIn:
        cond.append(tableAction['endDate'].isNotNull())
        joinOr2 = db.joinAnd([tableAction['endDate'].ge(begDateTime), tableAction['endDate'].lt(endDateTime)])
        cond.append(joinOr2)
    else:
        joinOr1 = tableAction['begDate'].isNull()
        joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
        cond.append(db.joinOr([joinOr1, joinOr2]))

    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
    queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
    queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
    queryTable = queryTable.innerJoin(tableHBProfile, tableHBProfile['id'].eq(tableOSHB['profile_id']))
    queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
    cond.append(tableOS['deleted'].eq(0))
    cond.append(tableOS['type'].ne(0))
    cond.append(tableAPT['typeName'].like(u'HospitalBed'))
    if orgStructureIdList:
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
    cond.append('''%s'''%(isEXISTSTransfer(nameProperty, namePropertyP=u'Отделение пребывания', transferType=transferType)))
    if not noProfileBed:
        cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
    if profile:
        if QtGui.qApp.defaultHospitalBedProfileByMoving():
            cond.append(getPropertyAPHBP(profile, noProfileBed))
        else:
            if noProfileBed and len(profile) > 1:
                cond.append(db.joinOr([tableOSHB['profile_id'].inlist(profile), tableOSHB['profile_id'].isNull()]))
            else:
                cond.append(tableOSHB['profile_id'].inlist(profile))
    else:
        if QtGui.qApp.defaultHospitalBedProfileByMoving():
            cond.append(getPropertyAPHBP([], noProfileBed))
        else:
            cond.append(tableOSHB['profile_id'].isNull())
    if bedsSchedule:
        queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
    if bedsSchedule == 1:
        cond.append(tableHBSchedule['code'].eq(1))
    elif bedsSchedule == 2:
        cond.append(tableHBSchedule['code'].ne(1))
    if boolFIO:
        if getOrgStructureCode:
            cols = u'''Client.lastName, Client.firstName, Client.patrName,
                Event.externalId, Event.order,
                rbHospitalBedProfile.code AS profileName,
                %s, %s'''%(getDataOrgStructureCode(u'Переведен из отделения', 'orgStructureFrom'),
                                   getDataOrgStructureCode(u'Переведен в отделение', 'orgStructureTo') )
        else:
            cols = u'''Client.lastName, Client.firstName, Client.patrName,
                    Event.externalId, Event.order,
                    rbHospitalBedProfile.name AS profileName,
                    %s, %s'''%(getDataOrgStructureName(u'Переведен из отделения', 'orgStructureFrom'),
                                       getDataOrgStructureName(u'Переведен в отделение', 'orgStructureTo') )
        stmt = db.selectDistinctStmt(queryTable, cols, cond)
        return db.query(stmt)
    else:
        return db.getCount(queryTable, countCol=u'Client.id', where=cond)


def getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty = u'Переведен из отделения', profile = None, orgStructureIdList = [], boolFIO = False, noPropertyProfile = False, profileCode = False):
    db = QtGui.qApp.db
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('received%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             tableClient['deleted'].eq(0),
             tableAction['endDate'].isNotNull()
            ]
    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEvent['eventType_id'].eq(tableEventType['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    cond.append('''%s'''%(getOrgStructureProperty(u'Направлен в отделение', orgStructureIdList)))
    cond.append(u'''(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'1\', \'2\', \'3\')))''')
    if noPropertyProfile:
        cond.append('''%s'''%(getNoPropertyAPHBP()))
    else:
        cond.append('''%s'''%(getPropertyAPHBP(profile, noProfileBed)))
    cond.append(tableAction['endDate'].isNotNull())
    cond.append(tableAction['endDate'].ge(begDateTime))
    cond.append(tableAction['endDate'].le(endDateTime))

    if boolFIO:
        col = 'code' if profileCode else 'name'
        stmt = db.selectDistinctStmt(queryTable, u'Client.lastName, Client.firstName, Client.patrName, Event.externalId, Event.order, %s'%(getPropertyAPHBPName(profile, noProfileBed, col)), cond)
        return db.query(stmt)
    else:
        ageStmtChildren = '''EXISTS(SELECT A.id
    FROM Action AS A
    INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
    INNER JOIN Event AS E ON A.event_id=E.id
    INNER JOIN Client AS C ON E.client_id=C.id
    WHERE A.deleted = 0 AND Action.id IS NOT NULL AND A.id = Action.id AND (age(C.birthDate, A.begDate)) <= 17)'''
        ageStmtAdult = '''EXISTS(SELECT A.id
    FROM Action AS A
    INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
    INNER JOIN Event AS E ON A.event_id=E.id
    INNER JOIN Client AS C ON E.client_id=C.id
    WHERE A.deleted = 0 AND Action.id IS NOT NULL AND A.id = Action.id AND (age(C.birthDate, A.begDate)) >= 60)'''
        isStationaryDay = '''EXISTS(SELECT APS.id
    FROM ActionPropertyType AS APT
    INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
    INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
    WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id AND AP.action_id=Action.id AND APT.deleted=0
    AND APT.name = '%s' AND APS.value = '%s')'''%(u'Поступил из', u'ДС')
        cols = u'''COUNT(Client.id) AS countAll, SUM(IF(Event.order = 1, 1, 0)) AS orderPlan,
        SUM(IF(Event.order = 2, 1, 0)) AS orderExtren, SUM(%s) AS childrenCount, SUM(%s) AS adultCount,
        SUM(isClientVillager(Client.id)) AS clientRural, SUM(%s) AS isStationaryDay'''%(ageStmtChildren, ageStmtAdult, isStationaryDay)
        stmt = db.selectStmt(queryTable, cols, where=cond)
        query = db.query(stmt)
        if query.first():
            record = query.record()
            return [forceInt(record.value('countAll')), forceInt(record.value('childrenCount')),
                    forceInt(record.value('adultCount')), forceInt(record.value('clientRural')),
                    forceInt(record.value('isStationaryDay')), forceInt(record.value('orderPlan')),
                    forceInt(record.value('orderExtren'))]
        else:
            return [0, 0, 0, 0, 0, 0, 0]


def getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty = u'Переведен в отделение', profile = None, orgStructureIdList = [], boolFIO = False, noPropertyProfile = False, profileCode = False):
    db = QtGui.qApp.db
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             tableClient['deleted'].eq(0),
             tableAction['begDate'].isNotNull(),
             tableAction['endDate'].isNotNull()
           ]
    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEvent['eventType_id'].eq(tableEventType['id']))
    cond.append('''%s'''%(getOrgStructureProperty(u'Отделение', orgStructureIdList)))
    cond.append(u'''(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'1\', \'2\', \'3\')))''')
    if noPropertyProfile:
        cond.append('''%s'''%(getNoPropertyAPHBP()))
    else:
        cond.append('''%s'''%(getPropertyAPHBP(profile, noProfileBed)))
    cond.append(tableAction['begDate'].ge(begDateTime))
    cond.append(tableAction['begDate'].le(endDateTime))

    if boolFIO:
        col = 'code' if profileCode else 'name'
        colsFIO = u'''Client.lastName, Client.firstName, Client.patrName, Event.externalId, Event.order, %s'''%(getPropertyAPHBPName(profile, noProfileBed, col))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, cond)
        leavedAll = db.query(stmt)
        condDeath = cond[:]
        condDeath.append(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, condDeath)
        leavedDeath = db.query(stmt)
        condTransfer = cond[:]
        condTransfer.append(getStringProperty(u'Исход госпитализации', u'(APS.value = \'переведен в другой стационар\')'))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, condTransfer)
        leavedTransfer = db.query(stmt)
        return [leavedAll, leavedDeath, leavedTransfer]
    else:
        isStationaryDay = '''EXISTS(SELECT APS.id
            FROM ActionPropertyType AS APT
            INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
            INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
            WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id AND AP.action_id=Action.id AND APT.deleted=0
            AND APT.name = '%s' AND APS.value = '%s')'''%(u'Исход госпитализации', u'переведен в ДС')
        stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer, SUM(%s) AS countStationaryDay'%(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'), getStringProperty(u'Исход госпитализации', u'(APS.value = \'переведен в другой стационар\')'), isStationaryDay), where=cond)
        query = db.query(stmt)
        if query.first():
            record = query.record()
            return [forceInt(record.value('countAll')), forceInt(record.value('countDeath')), forceInt(record.value('countTransfer')), forceInt(record.value('countStationaryDay'))]
        else:
            return [0, 0, 0, 0]


def getDataAPHBnoProperty(isPermanentBed, nameProperty, noProfileBed, profileList=[], endDate=u'', namePropertyStay=u'Отделение пребывания', orgStructureIdList=[], isMedical = None, bedsSchedule = None):
    strIsMedical = u''''''
    strIsMedicalJoin = u''''''
    strIsScheduleJoin = u''''''
    if isMedical is not None:
        strIsMedicalJoin += u''' INNER JOIN OrgStructure AS OS ON OSHB.master_id = OS.id INNER JOIN Organisation AS ORG ON OS.organisation_id = ORG.id'''
        strIsMedical += u''' AND OS.type != 0 AND ORG.isMedical = %d'''%(isMedical)
    strFilter = u''''''
    if profileList:
        if QtGui.qApp.defaultHospitalBedProfileByMoving():
            strFilter += u''' AND (''' + getPropertyAPHBP(profileList, noProfileBed) + u''')'''
        else:
            strFilter += u''' AND (OSHB.profile_id IN (%s)%s)'''%((','.join(forceString(profile) for profile in profileList if profile)), u' OR OSHB.profile_id IS NULL' if noProfileBed and len(profileList) > 1 else u'')
    elif noProfileBed:
        if QtGui.qApp.defaultHospitalBedProfileByMoving():
            strFilter += u''' AND EXISTS(''' + getPropertyAPHBPNoProfile() + u''')'''
        else:
            strFilter += u''' AND OSHB.profile_id IS NULL'''
    if bedsSchedule:
        strIsScheduleJoin += u''' INNER JOIN rbHospitalBedShedule AS HBS ON OSHB.schedule_id = HBS.id'''
    if bedsSchedule == 1:
        strFilter += u''' AND HBS.code = 1'''
    elif bedsSchedule == 2:
        strFilter += u''' AND HBS.code != 1'''

    return '''EXISTS(SELECT APHB.value
FROM ActionType AS AT
INNER JOIN Action AS A ON AT.id=A.actionType_id
INNER JOIN ActionPropertyType AS APT ON APT.actionType_id=AT.id
INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
INNER JOIN ActionProperty_HospitalBed AS APHB ON APHB.id=AP.id
INNER JOIN OrgStructure_HospitalBed AS OSHB ON OSHB.id=APHB.value%s%s
WHERE A.event_id=Event.id%s%s AND A.deleted=0 AND APT.actionType_id=A.actionType_id
AND AP.action_id=A.id AND AP.deleted=0 AND APT.deleted=0 AND APT.typeName = 'HospitalBed'%s
AND (NOT %s)%s)'''%(strIsMedicalJoin, strIsScheduleJoin, strIsMedical, endDate, strFilter,
getTransferProperty(nameProperty),
u' AND %s'%(getDataOrgStructureStay(namePropertyStay, orgStructureIdList, dayStat=0) if orgStructureIdList else u''))

