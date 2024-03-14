# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QDate, QDateTime, QTime

from library.Utils      import forceInt, forceRef, forceString, formatShortName, getAgeRangeCond

from Events.Utils       import getActionTypeIdListByFlatCode
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Reports.Utils      import ( dateRangeAsStr,
                                 getAdultCount,
                                 getChildrenCount,
                                 getDataOrgStructureCode,
                                 getDataOrgStructureName,
                                 getNoDeathAdultCount,
                                 getNoPropertyAPHBP,
                                 getOrgStructureProperty,
                                 getOrgStructurePropertyF30,
                                 getPropertyAPHBP,
                                 getPropertyAPHBPName,
                                 getStringProperty,
                                 isEXISTSTransfer,
                                 getOtkaz,
                                 getTransferOrganisaionName
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
        self.chkFinance.setVisible(False)
        self.cmbFinance.setVisible(False)


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
        self.chkNoPrintFilterParameters.setChecked(params.get('chkNoPrintFilterParameters', False))
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
        result['financeList'] = []
        result['financeName'] = []
        if self.chkFinance.isChecked():
            itemList = self.cmbFinance.model().takeColumn(0)
            for item in itemList:
                if item.checkState() == Qt.Checked:
                    result['financeList'].append(item.financeId)
                    result['financeName'].append(item.text())
        return result


#    @pyqtSignature('int')
#    def on_cmbOrgStructure_currentIndexChanged(self, index):
#        orgStructureId = self.cmbOrgStructure.value()


    @pyqtSignature('bool')
    def on_chkFinance_toggled(self, checked):
        self.cmbFinance.setEnabled(checked)

    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        endDate = date
        if endDate:
            begTime = self.edtTimeEdit.time()
            stringInfo = u'c %s до %s'%(forceString(QDateTime(endDate.addDays(-1), begTime)), forceString(QDateTime(endDate, begTime)))
        else:
            stringInfo = u'Введите дату'
        self.lblEndDate.setToolTip(stringInfo)


class CStationaryF007(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда стационара')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.stationaryF007SetupDialog = None
        self.clientDeath = 8


    def getSetupDialog(self, parent):
        result = CStationaryF007SetupDialog(parent)
        self.stationaryF007SetupDialog = result
        return result


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
                description.append(u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
                if begDateTime.date() or endDateTime.date():
                    description.append(dateRangeAsStr(u'за период', begDateTime, endDateTime))
        if onlyDates:
            # orgStructureId = params.get('orgStructureId', None)
            bedsSchedule = params.get('bedsSchedule', 0)
            hospitalBedProfileId = params.get('hospitalBedProfileId', None)
            noProfileBed = params.get('noProfileBed', True)
            isPermanentBed = params.get('isPermanentBed', False)
            # if orgStructureId:
            #     description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
            # else:
            #     description.append(u'подразделение: ЛПУ')
            description.append(u'режим койки: %s'%([u'Не учитывать', u'Круглосуточные', u'Не круглосуточные'][bedsSchedule]))
            if hospitalBedProfileId:
                description.append(u'профиль койки: %s'%(forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name'))))
            if noProfileBed:
                description.append(u'учитывать койки с профилем и без профиля')
            else:
                description.append(u'учитывать койки с профилем')
            if isPermanentBed:
                description.append(u'учитывать штатные и внештатные койки')
            else:
                description.append(u'учитывать штатные койки')
        financeName = params.get('financeName', [])
        financeNameString = ''
        if len(financeName):
            for item in financeName:
                financeNameString += forceString(item) + ', '
            description.append(u'тип финансирования: %s' %financeNameString)
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getCaption(self, cursor, params, title, cols = 1):
        orgId = QtGui.qApp.currentOrgId()
        orgName = u''
        OKPO = u''
        if orgId:
            record = QtGui.qApp.db.getRecordEx('Organisation', 'shortName, OKPO', 'id=%s AND deleted = 0'%(str(orgId)))
            if record:
                orgName = forceString(record.value('shortName'))
                OKPO = forceString(record.value('OKPO'))
        orgStructureId = params.get('orgStructureId', None)
        underCaptionList = []
        if orgStructureId:
            underCaptionList.append(u'подразделение: ' + forceString(getOrgStructureFullName(orgStructureId)))
        else:
            underCaptionList.append(u'подразделение: ЛПУ')
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        if hospitalBedProfileId:
            underCaptionList.append(u'профиль койки: %s'%(forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name'))))

        width = "%i%%"%(70-cols)
        columns = [(width, [], CReportBase.AlignLeft)]
        for i in range(cols-1):
            columns.append(('1%', [], CReportBase.AlignLeft))
        columns.append(('30%', [], CReportBase.AlignLeft))
        table = createTable(cursor, columns, headerRowCount=7, border=0, cellPadding=2, cellSpacing=0)
        table.mergeCells(0, 0, 1, cols)
        table.setText(0, 0, u'')
        table.setText(0, cols, u'Приложение №2')
        table.mergeCells(1, 0, 1, cols)
        table.setText(1, 0, u'')
        table.setText(1, cols, u'к приказу Минздрава России')
        table.mergeCells(2, 0, 1, cols)
        table.setText(2, 0, u'')
        table.setText(2, cols, u'от 30.12.2002 №413')
        table.mergeCells(3, 0, 1, cols)
        table.setText(3, 0, u'')
        table.setText(3, cols, u'Медицинская документация')
        table.mergeCells(4, 0, 1, cols)
        table.setText(4, 0, u'')
        table.setText(4, cols, u'Форма № 007/у-02')
        table.mergeCells(5, 0, 1, cols)
        table.setText(5, 0, u'')
        table.setText(5, cols, u'Утверждена Минздравом России')
        table.mergeCells(6, 0, 1, cols)
        table.setText(6, 0, orgName)
        table.setText(6, cols, u'от 30.12.2002 №413')

        cursor.movePosition(QtGui.QTextCursor.End)
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        columns2 = [('100%', [], CReportBase.AlignCenter)]
        for i in range(cols-1):
            columns2.append(('1%', [], CReportBase.AlignLeft))
        table2 = createTable(cursor, columns2, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        table2.mergeCells(0, 0, 1, cols)
        table2.mergeCells(1, 0, 1, cols)
        table2.setText(0, 0, title, charFormat=boldChars)
        table2.setText(1, 0, u', '.join(underCaption for underCaption in underCaptionList if underCaption))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getCaptionSV(self, cursor, params, title):
        orgId = QtGui.qApp.currentOrgId()
        orgName = u''
        OKPO = u''
        if orgId:
            record = QtGui.qApp.db.getRecordEx('Organisation', 'shortName, OKPO', 'id=%s AND deleted = 0'%(str(orgId)))
            if record:
                orgName = forceString(record.value('shortName'))
                OKPO = forceString(record.value('OKPO'))
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
        table.mergeCells(0, 0, 1, 2)
        table.mergeCells(1, 0, 1, 2)
        table.mergeCells(2, 0, 1, 2)
        table.mergeCells(3, 0, 1, 2)
        table.mergeCells(4, 0, 1, 2)
        table.mergeCells(5, 0, 1, 2)
        table.mergeCells(6, 0, 1, 2)

        cursor.movePosition(QtGui.QTextCursor.End)
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        columns2 = [('100%', [], CReportBase.AlignCenter)]
        table2 = createTable(cursor, columns2, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        table2.setText(0, 0, title, charFormat=boldChars)
        table2.setText(1, 0, u', '.join(underCaption for underCaption in underCaptionList if underCaption))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CStationaryF007Moving(CStationaryF007):
    def __init__(self, parent, currentOrgStructureId=None):
        CStationaryF007.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда стационара')
        self.currentOrgStructureId = currentOrgStructureId


    def getSetupDialog(self, parent):
        result = CStationaryF007SetupDialog(parent, self.currentOrgStructureId)
        result.setBegDateVisible(True)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.chkIsEventInfo.setVisible(False)
        self.stationaryF007SetupDialog.chkCompactInfo.setVisible(False)
        return result


    def build(self, params):
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableAPS = db.table('ActionProperty_String')
        tableAPO = db.table('ActionProperty_Organisation')
        tableOrg = db.table('Organisation')
        tableAPOS = db.table('ActionProperty_OrgStructure')
        tableOS = db.table('OrgStructure')
        tableClientAttach = db.table('ClientAttach')
        tableRBAttachType = db.table('rbAttachType')
        tableAPHB = db.table('ActionProperty_HospitalBed')
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
                self.getCaption(cursor, params, u'Листок учета движения больных и коечного фонда стационара', 23)
            else:
                cursor.insertText(self.title())
            cursor.insertBlock()
            self.dumpParams(cursor, params, not noPrintParams)
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            cols = [('5.5%',[u'', u'', u'', u'', u'1'], CReportBase.AlignLeft),
                    ('4.5%', [u'Код', u'', u'', u'', u'2'], CReportBase.AlignLeft),
                    ('4.5%', [u'Фактически развернуто коек, включая койки, свернутые', u'', u'', u'', u'3'], CReportBase.AlignRight),
                    ('4.5%', [u'В том числе коек, свернутых', u'', u'', u'', u'4'], CReportBase.AlignRight),
                    ('4.5%', [u'Движение больных за истекшие сутки', u'Состояло больных на начало истекших суток', u'',u'', u'5'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Поступило больных(без переведенных внутри больницы)', u'Всего', u'', '6'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'Плановых', u'', '7'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'Экстренных', u'', '8'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'в т.ч. из дневного стационара', u'', '9'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'Из них', u'Сельских жителей', u'10'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'', u'0 - 17 лет', u'11'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'', u'60 лет и старше', u'12'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Переведено больных внутри больницы', u'Из других отделений', u'', u'13'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'В другие отделения', u'', u'14'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Выписано больных', u'Всего', u'', u'15'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'В т.ч. переведенных в другие стационары', u'', u'16'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'В дневной стационар', u'', u'17'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Умерло', u'', u'', u'18'], CReportBase.AlignRight),
                    ('4.5%', [u'На начало текущего дня', u'Состоит больных', u'Всего', u'', u'19'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'В т.ч. сельских жителей', u'', u'20'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Состоит матерей при больных детях', u'', u'', u'21'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'Свободных мест', u'Всего', u'', u'22'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'Мужских', u'', u'23'], CReportBase.AlignRight),
                    ('4.5%', [u'', u'', u'Женских', u'', u'24'], CReportBase.AlignRight)
                   ]
            table = createTable(cursor, cols, duplicateHeaderOnNewPage=False)
            table.mergeCells(0, 0, 4, 1) # 1
            table.mergeCells(0, 1, 4, 1) # код
            table.mergeCells(0, 2, 4, 1) # развернуто коек
            table.mergeCells(0, 3, 4, 1) # свернутых
            table.mergeCells(0, 4, 1, 13) # Движение больных за истекшие сутки
            table.mergeCells(1, 4, 3, 1) # Состояло больных на начало истекших суток
            table.mergeCells(1, 5, 1, 7) # Поступило больных
            table.mergeCells(2, 5, 2, 1) # - Плановых
            table.mergeCells(2, 6, 2, 1) # - Экстренных
            table.mergeCells(2, 7, 2, 1) # - Всего
            table.mergeCells(2, 8, 2, 1) # Поступило больных - Из них-
            table.mergeCells(2, 9, 2, 1) #
            table.mergeCells(2, 10, 2, 1) #
            table.mergeCells(2, 11, 2, 1) #

            table.mergeCells(1, 12, 1, 2) # Переведено больных внутри больницы
            table.mergeCells(2, 12, 2, 1) # -Из других отделений
            table.mergeCells(2, 13, 2, 1) # Переведено больных внутри больницы-В другие отделения
            table.mergeCells(1, 14, 1, 3) # Выписано больных
            table.mergeCells(2, 14, 2, 1) # -Всего
            table.mergeCells(2, 15, 2, 1) # Выписано больных-В т.ч. переведенных в другие стационары
            table.mergeCells(2, 16, 2, 1) # Выписано больных-В т.ч. в дневной стационар
            table.mergeCells(1, 17, 3, 1) # Умерло
            table.mergeCells(0, 18, 1, 6) # На начало текущего дня
            table.mergeCells(1, 18, 1, 2) # -Состоит больных
            table.mergeCells(2, 18, 2, 1) # -Всего
            table.mergeCells(2, 19, 2, 1) # На начало текущего дня-Состоит больных-В т.ч. сельских жителей
            table.mergeCells(1, 20, 3, 1) # Состоит матерей при больных детях
            table.mergeCells(1, 21, 1, 3) # Свободных мест
            table.mergeCells(2, 21, 2, 1) # -Всего
            table.mergeCells(2, 22, 2, 1) # -Мужских
            table.mergeCells(2, 23, 2, 1) # -Женских
            cnt = 0

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
            self.bedsAllSUM = 0
            self.bedsMenSUM = 0
            self.bedsWomenSUM = 0

            def getHospitalBedId(orgStructureIdList):
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
                    cond.append(tableVHospitalBed['isPermanent'].eq(0))
                joinOr1 = db.joinAnd([tableVHospitalBed['begDate'].isNotNull(), tableVHospitalBed['endDate'].isNotNull(),
                tableVHospitalBed['begDate'].lt(endDateTime), tableVHospitalBed['endDate'].gt(begDateTime)])
                joinOr2 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)])
                joinOr3 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].le(begDateTime)])
                cond.append(db.joinOr([joinOr1, joinOr2, joinOr3]))
                return db.getDistinctIdList(tableVHospitalBedSchedule, [tableVHospitalBed['id']], cond)

            def getHospitalBedProfile(orgStructureIdList):
                cond = []
                profileIdList = []
                self.hospitalBedIdList = []
                if orgStructureIdList:
                    cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
                if QtGui.qApp.defaultHospitalBedProfileByMoving():
                    self.hospitalBedIdList = getHospitalBedId(orgStructureIdList)
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
                    profileIdList = db.getDistinctIdList(queryTable, [tableRbHospitalBedProfile['id']], cond)
                if not profileIdList:
                    return None
                if noProfileBed:
                    profileIdList.append(None)
                return profileIdList

            def getDataReport(parOrgStructureIdList, rowProfile, table, sumRowProfile, groupOS, profileIdList):
                db = QtGui.qApp.db
                tableAPT = db.table('ActionPropertyType')
                tableAP = db.table('ActionProperty')
                tableActionType = db.table('ActionType')
                tableAction = db.table('Action')
                tableEvent = db.table('Event')
                tableClient = db.table('Client')
                tableAPS = db.table('ActionProperty_String')
                tableAPO = db.table('ActionProperty_Organisation')
                tableOrg = db.table('Organisation')
                tableAPOS = db.table('ActionProperty_OrgStructure')
                tableOS = db.table('OrgStructure')
                tableClientAttach = db.table('ClientAttach')
                tableRBAttachType = db.table('rbAttachType')
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
                        condRepairs.append(tableVHospitalBed['isPermanent'].eq(0))
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
                            cond.append(tableVHospitalBed['isPermanent'].eq(0))
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
                        stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countPatronage, SUM(isClientVillager(Client.id)) AS clientRural'%(getStringProperty(u'Патронаж%', u'(APS.value = \'Да\')'), ), where=cond)
                        query = db.query(stmt)
                        if query.first():
                            record = query.record()
                            return [forceInt(record.value('countAll')), forceInt(record.value('countPatronage')), forceInt(record.value('clientRural'))]
                        else:
                            return [0, 0, 0]
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
                        table.setText(row, 12, getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1))
                    else:
                        movingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1)
                        table.setText(sumRowProfile, 12, movingTransfer)
                        if groupOS:
                            self.movingTransferAll += movingTransfer

                def receivedAll(profile = None, row = None, groupOS = False):
                    self.receivedBedsAll = 0
                    if row:
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
                        table.setText(row, 11, adultCount)
                    else:
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
                        table.setText(sumRowProfile, 11, adultCount)
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
                        table.setText(row, 13, getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0))
                    else:
                        inMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0)
                        table.setText(sumRowProfile, 13, inMovingTransfer)
                        if groupOS:
                            self.inMovingTransferAll += inMovingTransfer

                def leavedAll(profile = None, row = None, groupOS = False):
                    if row:
                        countLeavedAll, leavedDeath, leavedTransfer, countStationaryDay, adultCount, leavedotkaz = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed and not profile:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, countStationaryDayNoProfile, adultCount, leavedotkazNoProfile = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                            countStationaryDay += countStationaryDayNoProfile
                        table.setText(row, 14, countLeavedAll-leavedDeath)
                        table.setText(row, 15, leavedTransfer)
                        table.setText(row, 16, countStationaryDay)
                        table.setText(row, 17, leavedDeath)
                    else:
                        countLeavedAll, leavedDeath, leavedTransfer, countStationaryDay, adultCount, leavedotkaz = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, countStationaryDayNoProfile, adultCount, leavedotkazNoProfile = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                            countStationaryDay += countStationaryDayNoProfile
                        table.setText(sumRowProfile, 14, countLeavedAll-leavedDeath)
                        table.setText(sumRowProfile, 15, leavedTransfer)
                        table.setText(sumRowProfile, 16, countStationaryDay)
                        table.setText(sumRowProfile, 17, leavedDeath)
                        if groupOS:
                            self.countLeavedSUM += countLeavedAll-leavedDeath
                            self.leavedTransferSUM += leavedTransfer
                            self.leavedDeathSUM += leavedDeath
                            self.countStationaryDaySUM += countStationaryDay

                def presentEndDay(profile = None, row = None, groupOS = False):
                    self.presentAll = 0
                    if row:
                        self.presentAll, presentPatronag, clientRural = getMovingPresent(profile, True)
                        table.setText(row, 18, self.presentAll)
                        table.setText(row, 19, clientRural)
                        table.setText(row, 20, presentPatronag)
                    else:
                        self.presentAll, presentPatronag, clientRural = getMovingPresent(profile, True)
                        table.setText(sumRowProfile, 18, self.presentAll)
                        table.setText(sumRowProfile, 19, clientRural)
                        table.setText(sumRowProfile, 20, presentPatronag)
                        if groupOS:
                            self.presentAllSUM += self.presentAll
                            self.clientRuralSUM += clientRural
                            self.presentPatronagSUM += presentPatronag

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
                        freeBedsAll = forceInt(record.value('bedsAll'))
                        bedsAll = self.countBeds - self.presentAll
                        bedsMen = forceInt(record.value('bedsMen'))
                        bedsWomen = forceInt(record.value('bedsWomen'))
                    else:
                        bedsAll = 0 - self.presentAll
                        bedsMen = 0
                        bedsWomen = 0
                    if row:
                        table.setText(row, 21, bedsAll)
                        table.setText(row, 22, bedsMen)
                        table.setText(row, 23, bedsWomen)
                    else:
                        table.setText(sumRowProfile, 21, bedsAll)
                        table.setText(sumRowProfile, 22, bedsMen)
                        table.setText(sumRowProfile, 23, bedsWomen)
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
                return table.addRow()

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
                        rowProfile = getDataReport([parentOrgStructureId], rowProfile, table, sumRowProfile, True, profileIdList)
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
                            rowProfile = getDataReport([orgStructureId], rowProfile, table, sumRowProfile, True, profileIdList)
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
                table.setText(nextRow, 11, self.receivedInfo2)
                table.setText(nextRow, 12, self.movingTransferAll)
                table.setText(nextRow, 13, self.inMovingTransferAll)
                table.setText(nextRow, 14, self.countLeavedSUM)
                table.setText(nextRow, 15, self.leavedTransferSUM)
                table.setText(nextRow, 16, self.countStationaryDaySUM)
                table.setText(nextRow, 17, self.leavedDeathSUM)
                table.setText(nextRow, 18, self.presentAllSUM)
                table.setText(nextRow, 19, self.clientRuralSUM)
                table.setText(nextRow, 20, self.presentPatronagSUM)
                table.setText(nextRow, 21, self.bedsAllSUM)
                table.setText(nextRow, 22, self.bedsMenSUM)
                table.setText(nextRow, 23, self.bedsWomenSUM)
            else:
                profileIdList = getHospitalBedProfile(begOrgStructureIdList)
                table.setText(nextRow, 0, u'Всего:\n\nв том числе по койкам:', boldChars)
                getDataReport(begOrgStructureIdList, table.addRow(), table, nextRow, False, profileIdList)
        return doc


class CStationaryF007ClientList(CStationaryF007):
    def __init__(self, parent, currentOrgStrucrureId=None):
        CStationaryF007.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда стационара. Оборотная сторона')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=25, topMargin=1, rightMargin=1,  bottomMargin=1)
        self.currentOrgStrucrureId = currentOrgStrucrureId


    def getSetupDialog(self, parent):
        result = CStationaryF007SetupDialog(parent, self.currentOrgStrucrureId)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.setBegDateVisible(True)
        return result


    def build(self, params):
        db = QtGui.qApp.db
        tableOS = db.table('OrgStructure')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableHBSchedule = db.table('rbHospitalBedShedule')
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
            isPermanentBed = params.get('isPermanentBed', False)
            isEventInfo = params.get('isEventInfo', False)
            noProfileBed = params.get('noProfileBed', True)
            isGroupingOS = params.get('isGroupingOS', False)
            orgStructureId = params.get('orgStructureId', None)
            noPrintCaption = params.get('noPrintCaption', False)
            noPrintParams = params.get('noPrintFilterParameters', False)
            isCompactInfo = params.get('isCompactInfo', False)
            orgStructureIndex = self.stationaryF007SetupDialog.cmbOrgStructure._model.index(self.stationaryF007SetupDialog.cmbOrgStructure.currentIndex(), 0, self.stationaryF007SetupDialog.cmbOrgStructure.rootModelIndex())
            begOrgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            #cursor.insertBlock()
            if not noPrintCaption:
                self.getCaptionSV(cursor, params, u'СПИСОК БОЛЬНЫХ')
            else:
                cursor.insertText(self.title())
            cursor.insertBlock()
            self.dumpParams(cursor, params, not noPrintParams)
            cursor.setCharFormat(CReportBase.ReportBody)
            cols = [('16.6%',[u'ФИО поступивших', u''], CReportBase.AlignLeft),
                    ('16.6%', [u'ФИО переведенных из других отделений', u''], CReportBase.AlignLeft),
                    ('16.6%', [u'ФИО выписанных', u''], CReportBase.AlignLeft),
                    ('16.6%', [u'ФИО переведенных', u'в другие отделения данной больницы'], CReportBase.AlignLeft),
                    ('16.6%', [u'', u'в другие стационары'], CReportBase.AlignLeft),
                    ('16.6%', [u'ФИО умерших', u''], CReportBase.AlignLeft)
                   ]
            table = createTable(cursor, cols)
            table.mergeCells(0, 0, 2, 1)
            table.mergeCells(0, 1, 2, 1)
            table.mergeCells(0, 2, 2, 1)
            table.mergeCells(0, 3, 1, 2)
            table.mergeCells(0, 5, 2, 1)
            table.mergeCells(0, 6, 2, 1)

            def setInfoClient(recordsProfile, firstRow, nextRow, column, isEventInfo, recordsNoProfile = None, transferDirection = 0):
                def writeRecords(i, nextQuery):
                    while nextQuery.next():
                        if i <= nextRow:
                            record = nextQuery.record()
                            lastName = forceString(record.value('lastName'))
                            firstName = forceString(record.value('firstName'))
                            patrName = forceString(record.value('patrName'))
                            if isCompactInfo:
                                FIO = formatShortName(lastName, firstName, patrName)
                                order = [u'', u'п', u'э', u'с', u'принуд', u'вп', u'н'][forceInt(record.value('order'))]
                            else:
                                FIO = lastName + u' ' + firstName + u' ' + patrName
                                order = [u'', u'плановый', u'экстренный', u'самотёком', u'принудительный', u'внутренний перевод', u'неотложная'][forceInt(record.value('order'))]
                            if isEventInfo:
                                externalId = forceString(record.value('externalId'))
                                profileName = forceString(record.value('profileName'))
                                orgStructureFrom = forceString(record.value('OrgStructureFrom'))
                                orgStructureTo = forceString(record.value('OrgStructureTo'))
                                organisationName = forceString(record.value('organisationName'))
                                table.setText(i, column, FIO + u', ' + externalId + u', ' + order \
                                    + ((u', ' +  profileName) if profileName else u'')\
                                    + ((u'\\Из: '+orgStructureFrom) if orgStructureFrom and transferDirection == 1 else u'')\
                                    + ((u'\\В: '+orgStructureTo) if orgStructureTo and transferDirection == 2 else u'')\
                                    + ((u'\\В: '+organisationName) if organisationName and column == 4 else u''))
                            else:
                                table.setText(i, column, FIO)
                            i += 1
                    return i
                i = firstRow
                if recordsProfile:
                    i = writeRecords(i, recordsProfile)
                if recordsNoProfile:
                    i = writeRecords(i, recordsNoProfile)

            def getHospitalBedProfile(orgStructureIdList):
                tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')
                cond = []
                if orgStructureIdList:
                    cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
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
                profileIdList = db.getDistinctIdList(queryTable, [tableRbHospitalBedProfile['id']], cond)
                return profileIdList

            def getDataReport(parOrgStructureIdList, table, firstRow, nextRow, name):
                profileIdList = getHospitalBedProfile(parOrgStructureIdList)
                if not profileIdList:
                    return firstRow, nextRow
                receivedAll = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, parOrgStructureIdList, True, False, isCompactInfo)
                receivedAllNoProfile = None
                if noProfileBed:
                    receivedAllNoProfile = getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, parOrgStructureIdList, True, True if noProfileBed else False, isCompactInfo)
                # из других отделений
                fromMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, False, parOrgStructureIdList, True, isCompactInfo, transferType=1)
                # в другие отделения
                inMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, True, parOrgStructureIdList, True, isCompactInfo, transferType=0)
                leavedAll, leavedDeath, leavedTransfer = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, parOrgStructureIdList, True, False, isCompactInfo)
                leavedAllNoProfile = None
                leavedDeathNoProfile = None
                leavedTransferNoProfile = None
                if noProfileBed:
                    leavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile = getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, parOrgStructureIdList, True, True if noProfileBed else False)

                sizeQuerys = [(receivedAll.size() + receivedAllNoProfile.size()) if noProfileBed else receivedAll.size(),
                             fromMovingTransfer.size(),
                             inMovingTransfer.size(),
                             (leavedAll.size() + leavedAllNoProfile.size()) if noProfileBed else leavedAll.size(),
                             (leavedDeath.size() + leavedDeathNoProfile.size()) if noProfileBed else leavedDeath.size(),
                             (leavedTransfer.size() + leavedTransferNoProfile.size()) if noProfileBed else leavedTransfer.size()
                             ]
                sizeQuerysMax = -1
                for sizeQuery in sizeQuerys:
                    if sizeQuery > sizeQuerysMax:
                        sizeQuerysMax = sizeQuery

                if sizeQuerysMax > 0 and name:
                    firstRow = table.addRow()
                    table.setText(firstRow, 0, name, boldChars)
                    table.mergeCells(firstRow, 0, 1, 5)
                    firstRow += 1

                for newRow in range(0, sizeQuerysMax):
                    i = table.addRow()
                    if firstRow > -1:
                       nextRow = i
                    else:
                        firstRow = i
                        nextRow = i
                setInfoClient(receivedAll, firstRow, nextRow, 0, isEventInfo, receivedAllNoProfile)
                setInfoClient(fromMovingTransfer, firstRow, nextRow, 1, isEventInfo, None, 1)
                setInfoClient(inMovingTransfer, firstRow, nextRow, 3, isEventInfo, None, 2)
                setInfoClient(leavedAll, firstRow, nextRow, 2, isEventInfo, leavedAllNoProfile)
                setInfoClient(leavedDeath, firstRow, nextRow, 5, isEventInfo, leavedDeathNoProfile)
                setInfoClient(leavedTransfer, firstRow, nextRow, 4, isEventInfo, leavedTransferNoProfile)
                return firstRow, nextRow

            boldChars = QtGui.QTextCharFormat()
            boldChars.setFontWeight(QtGui.QFont.Bold)

            def getOrgStructureParent(orgStructureIdList, rowProfile, table, firstRow, nextRow):
                tableQuery = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
                recordList = db.getRecordListGroupBy(tableQuery, [tableOS['name'], tableOS['id']],
                                                     [tableOS['deleted'].eq(0),
                                                      tableOS['id'].inlist(orgStructureIdList), tableOS['type'].ne(0)],
                                                     'OrgStructure.id, OrgStructure.name')

                for recordEx in recordList:
                    name = forceString(recordEx.value('name'))
                    orgStructureId = forceString(recordEx.value('id'))
                    firstRow, nextRow = getDataReport([orgStructureId], table, firstRow, nextRow, name)
            if isGroupingOS:
                getOrgStructureParent(begOrgStructureIdList, -1, table, -1, -1)
            else:
                getDataReport(begOrgStructureIdList, table, -1, -1, None)
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


def getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty, profile = None, transferIn = False, orgStructureIdList = [], boolFIO = False, getOrgStructureCode = False, ageFor = False, ageTo = False, transferType=0, financeTypeId = None, financeTypeIdList = []):
    db = QtGui.qApp.db
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')
    tableAPS = db.table('ActionProperty_String')
    tableAPO = db.table('ActionProperty_Organisation')
    tableOrg = db.table('Organisation')
    tableAPOS = db.table('ActionProperty_OrgStructure')
    tableOS = db.table('OrgStructure')
    tableClientAttach = db.table('ClientAttach')
    tableRBAttachType = db.table('rbAttachType')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    tableVHospitalBed = db.table('vHospitalBed')
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
    if financeTypeIdList:
        cond.append(tableOSHB['finance_id'].inlist(financeTypeIdList))
    if financeTypeId:
        cond.append(tableOSHB['finance_id'].eq(financeTypeId))
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

    if profile and noProfileBed:
        cond.append(db.joinOr([tableOSHB['profile_id'].inlist(profile), tableOSHB['profile_id'].isNull()]))
    elif profile:
        cond.append(tableOSHB['profile_id'].inlist(profile))
    elif not noProfileBed:
        cond.append(tableOSHB['profile_id'].isNotNull())

    if bedsSchedule:
        queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
    if bedsSchedule == 1:
        cond.append(tableHBSchedule['code'].eq(1))
    elif bedsSchedule == 2:
        cond.append(tableHBSchedule['code'].ne(1))
    if ageFor and ageTo and ageFor <= ageTo:
        cond.append(getAgeRangeCond(ageFor, ageTo))
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


def getReceived(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty = u'Переведен из отделения', profile = None, orgStructureIdList = [], boolFIO = False, noPropertyProfile = False, profileCode = False, ageFor = False, ageTo = False, financeTypeId = None, financeTypeIdList = []):
    db = QtGui.qApp.db
    #tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    #tableOS = db.table('OrgStructure')
    #tableAPOS = db.table('ActionProperty_OrgStructure')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    tableAPTHB = db.table('ActionPropertyType').alias('apt_bed')
    tableAPVHB = db.table('ActionProperty_HospitalBed').alias('apv_bed')
    tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')
    actionTypeMovingList = getActionTypeIdListByFlatCode('moving%')
    tableMovingAction = db.table('Action').alias('MovingAction')
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
    queryTable = queryTable.innerJoin(tableMovingAction,
                                      "MovingAction.id = (SELECT min(Action.id) FROM Action WHERE Action.event_id = Event.id AND Action.deleted = 0 AND Action.actionType_id IN ({0}))".format(
                                          ','.join(
                                              [str(id) for id in actionTypeMovingList]) if actionTypeMovingList else 0))
    queryTable = queryTable.leftJoin(tableAPTHB, db.joinAnd(
        [tableAPTHB['actionType_id'].eq(tableMovingAction['actionType_id']),
         tableAPTHB['name'].eq(u'койка'),
         tableAPTHB['deleted'].eq(0)]))
    queryTable = queryTable.leftJoin(tableAP, db.joinAnd(
        [tableAP['type_id'].eq(tableAPTHB['id']),
         tableAP['action_id'].eq(tableMovingAction['id']),
         tableAP['deleted'].eq(0)]))
    queryTable = queryTable.leftJoin(tableAPVHB, tableAPVHB['id'].eq(tableAP['id']))
    queryTable = queryTable.leftJoin(tableOSHB, tableOSHB['id'].eq(tableAPVHB['value']))
    queryTable = queryTable.leftJoin(tableRbHospitalBedProfile,
                                     tableRbHospitalBedProfile['id'].eq(tableOSHB['profile_id']))
    cond.append('''%s'''%(getOrgStructureProperty(u'Направлен в отделение', orgStructureIdList)))
    cond.append(u"(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN ('1', '2', '3', '7')))")

    if noPropertyProfile:
        cond.append(tableOSHB['profile_id'].isNull())
    else:
        if profile and noProfileBed:
            cond.append(db.joinOr([tableOSHB['profile_id'].inlist(profile), tableOSHB['profile_id'].isNull()]))
        elif profile:
            cond.append(tableOSHB['profile_id'].inlist(profile))
        elif not noProfileBed:
            cond.append(tableOSHB['profile_id'].isNotNull())

    if ageFor and ageTo and ageFor <= ageTo:
        cond.append(getAgeRangeCond(ageFor, ageTo))
    # cond.append(tableAction['endDate'].isNotNull())
    cond.append(tableAction['endDate'].ge(begDateTime))
    cond.append(tableAction['endDate'].le(endDateTime))
    if boolFIO:
        col = 'code' if profileCode else 'name'
        stmt = db.selectDistinctStmt(queryTable, u'Client.lastName, Client.firstName, Client.patrName, Event.externalId, Event.order, %s'%(getPropertyAPHBPName(profile, noProfileBed, col)), cond)
        return db.query(stmt)
    else:
        isStationaryDay = '''EXISTS(SELECT APS.id
    FROM ActionPropertyType AS APT
    INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
    INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
    WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id
    AND AP.action_id=Action.id AND APT.deleted=0
    AND APT.name = '%s' AND APS.value = '%s')'''%(u'Поступил из', u'ДС')
        cols = u'''COUNT(Client.id) AS countAll, SUM(IF(Event.order = 1, 1, 0)) AS orderPlan,
        SUM(IF(Event.order = 2, 1, 0)) AS orderExtren, SUM(%s) AS childrenCount, SUM(%s) AS adultCount,
        SUM(isClientVillager(Client.id)) AS clientRural, SUM(%s) AS isStationaryDay'''%(getChildrenCount(), getAdultCount(), isStationaryDay)
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


def getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty = u'Переведен в отделение', profile = None, orgStructureIdList = [], boolFIO = False, noPropertyProfile = False, profileCode = False, additionalCond = None, ageFor = False, ageTo = False, type = None, finance = None):
    db = QtGui.qApp.db
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    tableOS = db.table('OrgStructure')
    tablePerson = db.table('Person')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    tableAPTHB = db.table('ActionPropertyType').alias('apt_bed')
    tableAPVHB = db.table('ActionProperty_HospitalBed').alias('apv_bed')
    tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')

    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             tableClient['deleted'].eq(0),
             tableAction['begDate'].isNotNull(),
             tableAction['endDate'].isNotNull()
           ]
    actionTypeMovingList = getActionTypeIdListByFlatCode('moving%')
    tableMovingAction = db.table('Action').alias('MovingAction')
    if additionalCond:
        cond.append(additionalCond)
    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEvent['eventType_id'].eq(tableEventType['id']))
    queryTable = queryTable.leftJoin('rbMedicalAidType', 'EventType.medicalAidType_id = rbMedicalAidType.id')
    queryTable = queryTable.innerJoin(tableMovingAction,
                                      "MovingAction.id = (SELECT max(Action.id) FROM Action WHERE Action.event_id = Event.id AND Action.deleted = 0 AND Action.actionType_id IN ({0}))".format(
                                          ','.join(
                                              [str(id) for id in actionTypeMovingList]) if actionTypeMovingList else 0))
    queryTable = queryTable.leftJoin(tableAPTHB, db.joinAnd(
        [tableAPTHB['actionType_id'].eq(tableMovingAction['actionType_id']),
         tableAPTHB['name'].eq(u'койка'),
         tableAPTHB['deleted'].eq(0)]))
    queryTable = queryTable.leftJoin(tableAP, db.joinAnd(
        [tableAP['type_id'].eq(tableAPTHB['id']),
         tableAP['action_id'].eq(tableMovingAction['id']),
         tableAP['deleted'].eq(0)]))
    queryTable = queryTable.leftJoin(tableAPVHB, tableAPVHB['id'].eq(tableAP['id']))
    queryTable = queryTable.leftJoin(tableOSHB, tableOSHB['id'].eq(tableAPVHB['value']))
    queryTable = queryTable.leftJoin(tableRbHospitalBedProfile,
                                     tableRbHospitalBedProfile['id'].eq(tableOSHB['profile_id']))

    queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    queryTable = queryTable.leftJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))

    if type:
        cond.append('''%s''' % (getOrgStructurePropertyF30(u'Отделение', orgStructureIdList, type)))
    else:
        cond.append('''%s''' % (getOrgStructurePropertyF30(u'Отделение', orgStructureIdList)))

    cond.append(u"(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN ('1', '2', '3', '7')))")

    if noPropertyProfile:
        cond.append(tableOSHB['profile_id'].isNull())
    else:
        if profile and noProfileBed:
            cond.append(db.joinOr([tableOSHB['profile_id'].inlist(profile), tableOSHB['profile_id'].isNull()]))
        elif profile:
            cond.append(tableOSHB['profile_id'].inlist(profile))
        elif not noProfileBed:
            cond.append(tableOSHB['profile_id'].isNotNull())

    cond.append(tableAction['begDate'].ge(begDateTime))
    cond.append(tableAction['begDate'].le(endDateTime))
    if ageFor and ageTo and ageFor <= ageTo:
        cond.append(getAgeRangeCond(ageFor, ageTo))
    if boolFIO:
        col = 'code' if profileCode else 'name'
        colsFIO = u'''Client.lastName, Client.firstName, Client.patrName, Event.externalId, Event.order, %s, %s'''%(getPropertyAPHBPName(profile, noProfileBed, col), getTransferOrganisaionName(u'Переведен в стационар', 'organisationName'))
        condLeaved=cond[:]
        condLeaved.append(getStringProperty(u'Исход госпитализации', u'(APS.value not LIKE \'умер%\' and APS.value not LIKE \'смерть%\' and APS.value NOT LIKE \'переведен в другой стационар\')'))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, condLeaved)
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
            AND NOT EXISTS(SELECT APS.id
            FROM ActionProperty AS AP
            INNER JOIN ActionPropertyType AS APT ON AP.type_id=APT.id
            INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
            WHERE AP.action_id=Action.id AND APT.actionType_id=Action.actionType_id
            AND  Action.id IS NOT NULL
            AND APT.deleted=0 AND AP.deleted=0 AND APT.name = '%s' AND (APS.value LIKE '%s' OR APS.value LIKE '%s')
            )
            AND APT.name = '%s' AND (APS.value = '%s' OR APS.value = '%s'))'''%(u'Исход госпитализации', u'умер%%', u'смерть%%', u'Исход госпитализации', u'переведен в дневной стационар', u'выписан в дневной стационар')
        stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer, SUM(%s) AS countStationaryDay, SUM(%s) AS adultCount, SUM(%s) AS Otkaz'%(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'),
        getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'%%переведен%%\')'), isStationaryDay, getNoDeathAdultCount(), getOtkaz()), where=cond)
        query = db.query(stmt)
        if query.first():
            record = query.record()
            return [forceInt(record.value('countAll')), forceInt(record.value('countDeath')), forceInt(record.value('countTransfer')), forceInt(record.value('countStationaryDay')), forceInt(record.value('adultCount')), forceInt(record.value('Otkaz'))]
        else:
            return [0, 0, 0, 0, 0, 0]


def getOrgStructureFullName(orgStructureId):
    db = QtGui.qApp.db
    table = db.table('OrgStructure')
    names = []
    ids   = set()

    while orgStructureId:
        record = db.getRecord(table, 'name, parent_id', orgStructureId)
        if record:
            names.append(forceString(record.value('name')))
            orgStructureId = forceRef(record.value('parent_id'))
        else:
            orgStructureId = None
        if orgStructureId in ids:
            orgStructureId = None
        else:
            ids.add(orgStructureId)
    return '/'.join(reversed(names))