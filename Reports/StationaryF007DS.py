# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import *

from library.Utils      import *
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr
from Reports.ReportView import CPageFormat
from Orgs.Utils         import *
from Utils              import *

from Ui_StationaryF007Setup import Ui_StationaryF007SetupDialog


class CStationaryF007DSSetupDialog(QtGui.QDialog, Ui_StationaryF007SetupDialog):
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
        result = {}
        result['endDate'] = self.edtEndDate.date()
        result['endTime'] = self.edtTimeEdit.time()
        result['orgStructureId'] = self.cmbOrgStructure.value()
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
            result['begTime'] = self.edtBegTime.time()
        return result


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        endDate = date
        if endDate:
            begTime = self.edtTimeEdit.time()
            stringInfo = u'c %s до %s'%(forceString(QDateTime(endDate.addDays(-1), begTime)), forceString(QDateTime(endDate, begTime)))
        else:
            stringInfo = u'Введите дату'
        self.lblEndDate.setToolTip(stringInfo)


class CStationaryF007DS(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда дневного стационара')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.stationaryF007SetupDialog = None
        self.clientDeath = 8


    def getSetupDialog(self, parent):
        result = CStationaryF007DSSetupDialog(parent, self.currentOrgStructureId)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.cmbSchedule.setVisible(False)
        self.stationaryF007SetupDialog.lblSchedule.setVisible(False)
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params, onlyDates = False):
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
            orgStructureId = params.get('orgStructureId', None)
            hospitalBedProfileId = params.get('hospitalBedProfileId', None)
            noProfileBed = params.get('noProfileBed', True)
            isPermanentBed = params.get('isPermanentBed', False)
            if orgStructureId:
                description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
            else:
                description.append(u'подразделение: ЛПУ')
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
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getCaption(self, cursor, params, title):
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

        columns = [('50%', [], CReportBase.AlignLeft), ('50%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=7, border=0, cellPadding=2, cellSpacing=0)
        table.setText(0, 0, u'')
        table.setText(0, 1, u'Код формы по ОКУД ___________')
        table.setText(1, 0, u'')
        table.setText(1, 1, u'Код учреждения по ОКПО  %s'%(OKPO))
        table.setText(2, 0, u'')
        table.setText(2, 1, u'')
        table.setText(3, 0, u'')
        table.setText(3, 1, u'Медицинская документация')
        table.setText(4, 0, u'')
        table.setText(4, 1, u'Форма № 007/у')
        table.setText(5, 0, u'')
        table.setText(5, 1, u'Утверждена Минздравом СССР')
        table.setText(6, 0, orgName)
        table.setText(6, 1, u'04.10.80 г. № 1030')

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

        columns = [('25%', [], CReportBase.AlignLeft),
                   ('25%', [], CReportBase.AlignLeft),
                   ('25%', [], CReportBase.AlignLeft),
                   ('25%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=7, border=0, cellPadding=2, cellSpacing=0)
        table.setText(0, 0, u'')
        table.setText(0, 3, u'Код формы по ОКУД ______________')
        table.setText(1, 0, u'')
        table.setText(1, 3, u'Код учреждения по ОКПО  %s'%(OKPO))
        table.setText(2, 0, u'')
        table.setText(2, 3, u'')
        table.setText(3, 0, u'')
        table.setText(3, 3, u'Медицинская документация')
        table.setText(4, 0, u'')
        table.setText(4, 3, u'Форма № 007/у')
        table.setText(5, 0, u'')
        table.setText(5, 3, u'Утверждена Минздравом СССР')
        table.setText(6, 0, orgName)
        table.setText(6, 3, u'04.10.80 г. № 1030')
        table.mergeCells(0, 0, 1, 2)
        table.mergeCells(1, 0, 1, 2)
        table.mergeCells(2, 0, 1, 2)
        table.mergeCells(3, 0, 1, 2)

        cursor.movePosition(QtGui.QTextCursor.End)
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        columns2 = [('100%', [], CReportBase.AlignCenter)]
        table2 = createTable(cursor, columns2, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        table2.setText(0, 0, title, charFormat=boldChars)
        table2.setText(1, 0, u', '.join(underCaption for underCaption in underCaptionList if underCaption))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CStationaryF007DSMoving(CStationaryF007DS):
    def __init__(self, parent, currentOrgStructureId=None):
        CStationaryF007DS.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда дневного стационара')
        self.currentOrgStructureId = currentOrgStructureId


    def getSetupDialog(self, parent):
        result = CStationaryF007DSSetupDialog(parent, self.currentOrgStructureId)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.setBegDateVisible(True)
        self.stationaryF007SetupDialog.chkIsEventInfo.setVisible(False)
        self.stationaryF007SetupDialog.cmbSchedule.setVisible(False)
        self.stationaryF007SetupDialog.lblSchedule.setVisible(False)
        self.stationaryF007SetupDialog.chkCompactInfo.setVisible(False)
        return result


    def averageYarHospitalBed(self, orgStructureIdList, rowProfile, column, table, sumRowProfile, begDate, endDate, profile = None, row = None, isHospital = None, countMonths = None, groupOS = False):
        days = 0
        daysMonths = 0
        begDatePeriod = begDate
        endMonth = endDate.month()
        endDatePeriod = begDatePeriod.addMonths(1)
        while endDatePeriod <= endDate:
            days = self.averageDaysHospitalBed(orgStructureIdList, begDatePeriod, endDatePeriod, profile, isHospital)
            daysMonths += days / (begDatePeriod.daysInMonth())
            begDatePeriod = begDatePeriod.addMonths(1)
            endDatePeriod = endDatePeriod.addMonths(1)
        if countMonths == 12:
            daysMonths = daysMonths / 12
        elif countMonths == 6:
            daysMonths = daysMonths / 6
        if rowProfile:
           table.setText(rowProfile, column, daysMonths)
        else:
            table.setText(sumRowProfile, column, daysMonths)
            if groupOS:
                self.daysMonthsAll += daysMonths


    def averageDaysHospitalBed(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None):
        days = 0
        db = QtGui.qApp.db
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableOrg = db.table('Organisation')
        tableOS = db.table('OrgStructure')
        queryTable = tableOSHB.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        queryTable = queryTable.innerJoin(tableOrg, tableOrg['id'].eq(tableOS['organisation_id']))
        cond = [tableOSHB['master_id'].inlist(orgStructureIdList),
                tableOrg['deleted'].eq(0),
                tableOS['deleted'].eq(0),
                #tableOS['type'].eq(0)
                ]
        if isHospital is not None:
           cond.append(tableOrg['isHospital'].eq(isHospital))
        joinAnd = db.joinAnd([tableOSHB['endDate'].isNull(), db.joinOr([db.joinAnd([tableOSHB['begDate'].isNotNull(), tableOSHB['begDate'].lt(endDatePeriod)]), tableOSHB['begDate'].isNull()])])
        cond.append(db.joinOr([db.joinAnd([tableOSHB['endDate'].isNotNull(), tableOSHB['endDate'].gt(begDatePeriod), tableOSHB['begDate'].isNotNull(), tableOSHB['begDate'].lt(endDatePeriod)]), joinAnd]))
        if profile:
           cond.append(tableOSHB['profile_id'].inlist(profile))
        cond.append('''NOT EXISTS(SELECT OrgStructure_HospitalBed_Involution.id
                       FROM OrgStructure_HospitalBed_Involution
                       WHERE OrgStructure_HospitalBed_Involution.master_id = OrgStructure_HospitalBed.id
                       AND OrgStructure_HospitalBed_Involution.involutionType != 0
                       AND (OrgStructure_HospitalBed_Involution.begDate IS NULL
                       OR OrgStructure_HospitalBed_Involution. endDate IS NULL
                       OR (OrgStructure_HospitalBed_Involution.begDate >= '%s'
                       AND OrgStructure_HospitalBed_Involution. endDate <= '%s')))'''%(begDatePeriod.toString(Qt.ISODate), begDatePeriod.toString(Qt.ISODate)))
        stmt = db.selectStmt(queryTable, [tableOSHB['id'], tableOSHB['begDate'], tableOSHB['endDate']], where=cond)
        query = db.query(stmt)
        bedIdList = []
        while query.next():
            record = query.record()
            bedId = forceRef(record.value('id'))
            if bedId not in bedIdList:
                bedIdList.append(bedId)
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                if not begDate or begDate < begDatePeriod:
                    begDate = begDatePeriod
                if not endDate or endDate > endDatePeriod:
                    endDate = endDatePeriod
                if begDate and endDate:
                    if begDate == endDate:
                        days += 1
                    else:
                        days += begDate.daysTo(endDate)
        return days


    def dataMovingDays(self, orgStructureIdList, rowProfile, column, table, sumRowProfile, begDatePeriod, endDatePeriod, profile, groupOS, isHospital = None, rural = None, noProfileBed = False):
        days = getMovingDays(orgStructureIdList, begDatePeriod, endDatePeriod, profile, isHospital, rural, None, None, 0)
        if rowProfile:
           table.setText(rowProfile, column, days)
        else:
            table.setText(sumRowProfile, column, days)
            if groupOS:
                self.daysCurePassAll += days


    def dataMovingDaysOld(self, orgStructureIdList, rowProfile, column, table, sumRowProfile, begDatePeriod, endDatePeriod, profile, groupOS, isHospital = None):
        days = 0
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableOrg = db.table('Organisation')
        tableOS = db.table('OrgStructure')
        tableAPHB = db.table('ActionProperty_HospitalBed')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.leftJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
        queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
        queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
        queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        queryTable = queryTable.innerJoin(tableOrg, tableOrg['id'].eq(tableOS['organisation_id']))
        cond = [tableActionType['flatCode'].like('moving%'),
                tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableAP['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableAPT['deleted'].eq(0),
                tableOS['deleted'].eq(0),
                #tableOS['type'].eq(0),
                tableClient['deleted'].eq(0),
                tableOrg['deleted'].eq(0),
                tableAPT['typeName'].like('HospitalBed'),
                tableAP['action_id'].eq(tableAction['id'])
               ]
        if isHospital is not None:
           cond.append(tableOrg['isHospital'].eq(isHospital))
        if profile:
           cond.append(tableOSHB['profile_id'].inlist(profile))
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
        joinAnd = db.joinAnd([tableAction['endDate'].isNull(), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod)])
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].ge(begDatePeriod))
        cond.append(tableAction['begDate'].le(endDatePeriod))
        #cond.append(db.joinOr([db.joinAnd([tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDatePeriod), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod)]), joinAnd]))
        stmt = db.selectStmt(queryTable, [tableEvent['id'].alias('eventId'), tableAction['id'].alias('actionId'), tableAction['begDate'], tableAction['endDate']], cond)
        query = db.query(stmt)
        actionIdList = []
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            if actionId not in actionIdList:
                actionIdList.append(actionId)
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                if begDate < begDatePeriod.date():
                    begDate = begDatePeriod.date()
                if not endDate or endDate > endDatePeriod.date():
                    endDate = endDatePeriod.date()
                if begDate and endDate:
                    if begDate == endDate:
                        days += 1
                    else:
                        days += begDate.daysTo(endDate)

        if rowProfile:
           table.setText(rowProfile, column, days)
        else:
            table.setText(sumRowProfile, column, days)
            if groupOS:
                self.daysCurePassAll += days


    def dataPatronageOrClientRuralDays(self, orgStructureIdList, rowProfile, column, table, sumRowProfile, begDatePeriod, endDatePeriod, profile, groupOS, isHospital = None):
        days = 0
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
        cols = [tableAction['id'].alias('actionId'),
                tableAction['begDate'],
                tableAction['endDate']
                ]
        cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
                 tableEvent['deleted'].eq(0),
                 tableAction['deleted'].eq(0),
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
        #cond.append(tableOS['type'].eq(0))
        cond.append(tableOS['deleted'].eq(0))
        cond.append(tableAPT['typeName'].like('HospitalBed'))
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].ge(begDatePeriod))
        cond.append(tableAction['begDate'].le(endDatePeriod))
        if profile:
            cond.append(tableOSHB['profile_id'].eq(profile))
        cond.append(getKladrClientRural())
        stmt = db.selectStmt(queryTable, cols, where=cond)
        query = db.query(stmt)
        actionIdList = []
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            if actionId not in actionIdList:
                actionIdList.append(actionId)
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                if begDate < begDatePeriod.date():
                    begDate = begDatePeriod.date()
                if not endDate or endDate > endDatePeriod.date():
                    endDate = endDatePeriod.date()
                if begDate and endDate:
                    if begDate == endDate:
                        days += 1
                    else:
                        days += begDate.daysTo(endDate)
        if rowProfile:
           table.setText(rowProfile, column, days)
        else:
            table.setText(sumRowProfile, column, days)
            if groupOS:
                self.daysCurePassRuralAll += days


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
                column5 = ('5.5%', [u'Движение больных за истекшие сутки', u'Состояло больных на начало истекших суток', u'',u'', u'5'], CReportBase.AlignRight)
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
                column5 = ('5.5%', [u'Движение больных за истекшие сутки', u'Состояло больных на начало отчетного периода', u'',u'', u'5'], CReportBase.AlignRight)
            hospitalBedProfileId = params.get('hospitalBedProfileId', None)
            orgStructureId = params.get('orgStructureId', None)
            noProfileBed = params.get('noProfileBed', True)
            isPermanentBed = params.get('isPermanentBed', False)
            noPrintCaption = params.get('noPrintCaption', False)
            noPrintParams = params.get('noPrintFilterParameters', False)
            isGroupingOS = params.get('isGroupingOS', False)
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

            cols = [('7.0%',[u'', u'', u'', u'', u'1'], CReportBase.AlignLeft),
                    ('5.0%', [u'Код', u'', u'', u'', u'2'], CReportBase.AlignLeft),
                    ('5.5%', [u'Число мест', u'', u'', u'', u'3'], CReportBase.AlignRight),
                    ('5.5%', [u'Среднемесячных мест', u'', u'', u'', u'4'], CReportBase.AlignRight),
                    column5,
                    ('5.5%', [u'', u'поступило больных', u'Всего', u'', '6'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'в т.ч. из круглосуточных стационаров', u'', '7'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'из них: из гр.6', u'сельских жителей', '8'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'', u'0 - 17 лет', '9'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'', u'60 лет и старше', '10'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'выписано больных', u'всего', u'', '11'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'в т.ч. в круглосуточные стационары', u'', '12'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'Умерло', u'', u'', u'13'], CReportBase.AlignRight),
                    ('5.5%', [u'На начало текущего дня', u'Состоит больных', u'Всего', u'', u'14'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'', u'В т.ч. сельских жителей', u'', u'15'], CReportBase.AlignRight),
                    ('5.5%', [u'Состояло больных на конец отчетного периода', u'', u'', u'', u'16'], CReportBase.AlignRight),
                    ('5.5%', [u'Проведено больными дней лечения', u'Всего', u'', u'', u'17'], CReportBase.AlignRight),
                    ('5.5%', [u'', u'в т.ч. сельскими жителями', u'', u'', u'18'], CReportBase.AlignRight)
                   ]

            table = createTable(cursor, cols)
            table.mergeCells(0, 0, 4, 1) # 1
            table.mergeCells(0, 1, 4, 1) # код
            table.mergeCells(0, 2, 4, 1) # развернуто коек
            table.mergeCells(0, 3, 4, 1) # свернутых
            table.mergeCells(0, 4, 1, 9) # Движение больных за истекшие сутки
            table.mergeCells(1, 4, 3, 1) # Состояло больных на начало истекших суток
            table.mergeCells(1, 5, 1, 5) # Поступило больных
            table.mergeCells(2, 5, 2, 1) # - Всего
            table.mergeCells(2, 6, 2, 1) #
            table.mergeCells(2, 7, 1, 3) #
            table.mergeCells(1, 10, 1, 2) #
            table.mergeCells(1, 12, 3, 1) #
            table.mergeCells(2, 10, 2, 1) #
            table.mergeCells(2, 11, 2, 1) #
            table.mergeCells(0, 13, 1, 2) #
            table.mergeCells(1, 13, 1, 2) #
            table.mergeCells(2, 13, 2, 1) #
            table.mergeCells(2, 13, 2, 1) #
            table.mergeCells(2, 14, 2, 1) #
            table.mergeCells(0, 15, 4, 1) #
            table.mergeCells(0, 16, 1, 2) #
            table.mergeCells(1, 16, 3, 1) #
            table.mergeCells(1, 17, 3, 1) #

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
            self.presentAllSUM = 0
            self.clientRuralSUM = 0
            self.presentPatronagSUM = 0
            self.bedsAllSUM = 0
            self.bedsMenSUM = 0
            self.bedsWomenSUM = 0
            self.daysMonthsAll = 0
            self.daysPresenceAll = 0
            self.daysCurePassAll = 0
            self.daysCurePassRuralAll = 0

            def getHospitalBedId(orgStructureIdList):
                cond = []
                tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                cond.append(tableOS['deleted'].eq(0))
                #cond.append(tableOS['type'].eq(0))
                if orgStructureIdList:
                    cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
                tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                cond.append(tableHBSchedule['code'].ne(1))
                if not isPermanentBed:
                    cond.append(tableVHospitalBed['isPermanent'].eq(1))
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
    AND (APT.`typeName` LIKE 'HospitalBed') AND (APHB.`value` IN (%s)))'''%(u','.join(str(hospitalBedId) for hospitalBedId in self.hospitalBedIdList if hospitalBedId)))
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
                    cond.append(tableOS['deleted'].eq(0))
                    #cond.append(tableOS['type'].eq(0))
                    queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
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
    AND (APT.`typeName` LIKE 'HospitalBed') AND (APHB.`value` IN (%s)))'''%(u','.join(str(hospitalBedId) for hospitalBedId in hospitalBedIdList if hospitalBedId)))
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
                    tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
                    tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                    if QtGui.qApp.defaultHospitalBedProfileByMoving():
                        tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                        if self.hospitalBedIdList:
                            getBedForProfile(noProfileBed, profile, self.hospitalBedIdList, True, row, 2, groupOS)
                        else:
                            table.setText(row if row else sumRowProfile, 2, 0)
                            if groupOS:
                                table.setText(rowProfile, 2, 0)
                    else:
                        cond = []
                        cond.append(tableOS['deleted'].eq(0))
                        #cond.append(tableOS['type'].eq(0))
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
                        tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                        cond.append(tableHBSchedule['code'].ne(1))
                        cond.append(db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)]))
                        cond.append(db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(begDateTime)]))
                        self.countBeds = db.getCount(tableVHospitalBedSchedule, countCol='vHospitalBed.id', where=cond)
                        if row:
                           table.setText(row, 2, self.countBeds)
                        else:
                            table.setText(sumRowProfile, 2, self.countBeds)
                            if groupOS:
                                self.countBedsAll += self.countBeds

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
                    #cond.append(tableOS['type'].eq(0))
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
                    queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
                    cond.append(tableHBSchedule['code'].ne(1))
                    if flagCurrent:
                        cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
                        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
                        stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countPatronage, SUM(%s) AS clientRural'%(getStringProperty(u'Патронаж%', u'(APS.value LIKE \'Да\')'), getKladrClientRural()), where=cond)
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
                        table.setText(row, 12, getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1))
                    else:
                        movingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, False, orgStructureIdList, transferType=1)
                        table.setText(sumRowProfile, 12, movingTransfer)
                        if groupOS:
                            self.movingTransferAll += movingTransfer

                def receivedAll(profile = None, row = None, groupOS = False):
                    self.receivedBedsAll = 0
                    if row:
                        receivedInfo = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList)
                        receivedBedAll = receivedInfo[5]
                        childrenCount = receivedInfo[1]
                        adultCount = receivedInfo[2]
                        clientRural = receivedInfo[3]
                        isStationaryDay = receivedInfo[4]
                        orderExtren = receivedInfo[6]
                        countAll = receivedInfo[0]
                        if noProfileBed and not profile:
                            receivedInfoNoProfile = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList, False, True)
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
                        table.setText(row, 5,  countAll) #7
                        table.setText(row, 6,  isStationaryDay) #8
                        table.setText(row, 7,  clientRural) #9
                        table.setText(row, 8, childrenCount) #10
                        table.setText(row, 9, adultCount) #11
                    else:
                        receivedInfo = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList)
                        receivedBedAll = receivedInfo[5]
                        childrenCount = receivedInfo[1]
                        adultCount = receivedInfo[2]
                        clientRural = receivedInfo[3]
                        isStationaryDay = receivedInfo[4]
                        orderExtren = receivedInfo[6]
                        countAll = receivedInfo[0]
                        if noProfileBed:
                            receivedInfoNoProfile = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profile, orgStructureIdList, False, True)
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
                        table.setText(sumRowProfile, 5,  countAll) #7
                        table.setText(sumRowProfile, 6,  isStationaryDay) #8
                        table.setText(sumRowProfile, 7,  clientRural) #9
                        table.setText(sumRowProfile, 8, childrenCount) #10
                        table.setText(sumRowProfile, 9, adultCount) #11
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
                        num = getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0)
                        table.setText(row, 13, num)
                        self.daysPresenceAll += num
                    else:
                        inMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, True, orgStructureIdList, transferType=0)
                        table.setText(sumRowProfile, 13, inMovingTransfer)
                        self.daysPresenceAll += inMovingTransfer
                        if groupOS:
                            self.inMovingTransferAll += inMovingTransfer

                def leavedAll(profile = None, row = None, groupOS = False):
                    if row:
                        countLeavedAll, leavedDeath, leavedTransfer, adultCount = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed and not profile:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, adultCount = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                        table.setText(row, 10, countLeavedAll-leavedDeath) #14
                        table.setText(row, 11, leavedTransfer) #15
                        table.setText(row, 12, leavedDeath) #16
                        self.daysPresenceAll += countLeavedAll-leavedDeath
                    else:
                        countLeavedAll, leavedDeath, leavedTransfer, adultCount = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList)
                        if noProfileBed:
                            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, adultCount = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profile, orgStructureIdList, False, True)
                            countLeavedAll += countLeavedAllNoProfile
                            leavedDeath += leavedDeathNoProfile
                            leavedTransfer += leavedTransferNoProfile
                        table.setText(sumRowProfile, 10, countLeavedAll-leavedDeath) #14
                        table.setText(sumRowProfile, 11, leavedTransfer) #15
                        table.setText(sumRowProfile, 12, leavedDeath) #16
                        self.daysPresenceAll += countLeavedAll-leavedDeath
                        if groupOS:
                            self.countLeavedSUM += countLeavedAll-leavedDeath
                            self.leavedTransferSUM += leavedTransfer
                            self.leavedDeathSUM += leavedDeath

                def showDaysPresence(row):
                    table.setText(row, 16, self.daysPresenceAll) #14
                    self.daysPresenceAll = 0

                def presentEndDay(profile = None, row = None, groupOS = False):
                    self.presentAll = 0
                    if row:
                        self.presentAll, presentPatronag, clientRural = getMovingPresent(profile, True)
                        table.setText(row, 13, self.presentAll) #17
                        table.setText(row, 14, clientRural) #18
                        table.setText(row, 15, self.presentAll) #19
                        self.daysPresenceAll += self.presentAll
                    else:
                        self.presentAll, presentPatronag, clientRural = getMovingPresent(profile, True)
                        table.setText(sumRowProfile, 13, self.presentAll) #17
                        table.setText(sumRowProfile, 14, clientRural) #18
                        table.setText(sumRowProfile, 15, self.presentAll) #19
                        self.daysPresenceAll += self.presentAll
                        if groupOS:
                            self.presentAllSUM += self.presentAll
                            self.clientRuralSUM += clientRural
                            self.presentPatronagSUM += presentPatronag
                unrolledHospitalBed34(profileIdList, None, groupOS)
                self.averageYarHospitalBed(parOrgStructureIdList, None, 3, table, sumRowProfile, begDateTime.date(), endDateTime.date(), profileIdList, None, None, None, groupOS)
                presentBegDay(profileIdList, None, groupOS)
                receivedAll(profileIdList, None, groupOS)
                leavedAll(profileIdList, None, groupOS)
                presentEndDay(profileIdList, None, groupOS)
                self.dataMovingDays(parOrgStructureIdList, None, 16, table, sumRowProfile, begDateTime, endDateTime, profileIdList, groupOS, None, False, noProfileBed)
                self.dataMovingDays(parOrgStructureIdList, None, 17, table, sumRowProfile, begDateTime, endDateTime, profileIdList, groupOS, None, True, noProfileBed)
                if noProfileBed:
                    table.setText(rowProfile, 0, u'профиль койки не определен')
                    unrolledHospitalBed34([], rowProfile)
                    self.averageYarHospitalBed(parOrgStructureIdList, rowProfile, 3, table, sumRowProfile, begDateTime.date(), endDateTime.date(), [], None, None, None, groupOS)
                    presentBegDay([], rowProfile)
                    receivedAll([], rowProfile)
                    leavedAll([], rowProfile)
                    presentEndDay([], rowProfile)
                    self.dataMovingDays(parOrgStructureIdList, rowProfile, 16, table, sumRowProfile, begDateTime, endDateTime, [], groupOS, None, False, noProfileBed)
                    self.dataMovingDays(parOrgStructureIdList, rowProfile, 17, table, sumRowProfile, begDateTime, endDateTime, [], groupOS, None, True, noProfileBed)
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
                    self.averageYarHospitalBed(parOrgStructureIdList, rowProfile, 3, table, sumRowProfile, begDateTime.date(), endDateTime.date(), [profileId], rowProfile, None, None, groupOS)
                    presentBegDay([profileId], rowProfile)
                    receivedAll([profileId], rowProfile)
                    leavedAll([profileId], rowProfile)
                    presentEndDay([profileId], rowProfile)
                    self.dataMovingDays(parOrgStructureIdList, rowProfile, 16, table, sumRowProfile, begDateTime, endDateTime, [profileId], groupOS, None, False, noProfileBed)
                    self.dataMovingDays(parOrgStructureIdList, rowProfile, 17, table, sumRowProfile, begDateTime, endDateTime, [profileId], groupOS, None, True, noProfileBed)
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
                                               #tableOS['type'].eq(0),
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
                                                   [tableOS['deleted'].eq(0),
                                                    #tableOS['type'].eq(0),
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
                table.setText(nextRow, 3, self.daysMonthsAll)
                table.setText(nextRow, 4, self.movingPresentAll)
                table.setText(nextRow, 5, self.receivedInfo0)
                table.setText(nextRow, 6, self.receivedInfo4)
                table.setText(nextRow, 7, self.receivedInfo3)
                table.setText(nextRow, 8, self.receivedInfo1)
                table.setText(nextRow, 9, self.receivedInfo2)
                table.setText(nextRow, 10, self.countLeavedSUM)
                table.setText(nextRow, 11, self.leavedTransferSUM)
                table.setText(nextRow, 12, self.leavedDeathSUM)
                table.setText(nextRow, 13, self.presentAllSUM)
                table.setText(nextRow, 14, self.clientRuralSUM)
                table.setText(nextRow, 15, self.presentAllSUM)
                table.setText(nextRow, 16, self.daysCurePassAll)
                table.setText(nextRow, 17, self.daysCurePassRuralAll)
                self.daysPresenceAll = 0
            else:
                profileIdList = getHospitalBedProfile(begOrgStructureIdList)
                table.setText(nextRow, 0, u'Всего:\n\nв том числе по койкам:', boldChars)
                getDataReport(begOrgStructureIdList, table.addRow(), table, nextRow, False, profileIdList)
        return doc


class CStationaryF007DSClientList(CStationaryF007DS):
    def __init__(self, parent, currentOrgStructureId=None):
        CStationaryF007DS.__init__(self, parent)
        self.setTitle(u'Листок учета движения больных и коечного фонда стационара. Оборотная сторона')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=25, topMargin=1, rightMargin=1,  bottomMargin=1)
        self.currentOrgStructureId = currentOrgStructureId


    def getSetupDialog(self, parent):
        result = CStationaryF007DSSetupDialog(parent, self.currentOrgStructureId)
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
            if not noPrintCaption:
                self.getCaptionSV(cursor, params, u'СПИСОК БОЛЬНЫХ')
            else:
                cursor.insertText(self.title())
            cursor.insertBlock()
            self.dumpParams(cursor, params, not noPrintParams)
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            cols = [('25%',[u'ФИО поступивших'], CReportBase.AlignLeft),
                    ('25%', [u'В т.ч. из круглосуточного стационара'], CReportBase.AlignLeft),
                    ('25%', [u'ФИО выписанных'], CReportBase.AlignLeft),
                    ('25%', [u'В т. ч. в круглосуточные стационары'], CReportBase.AlignLeft)
                   ]
            table = createTable(cursor, cols)

            def setInfoClient(recordsProfile, firstRow, nextRow, columns, isEventInfo, recordsNoProfile = None, transferDirection = 0):
                def writeRecords(i, nextQuery):
                    while nextQuery.next():
                        if i <= nextRow:
                            record = nextQuery.record()
                            lastName = forceString(record.value('lastName'))
                            firstName = forceString(record.value('firstName'))
                            patrName = forceString(record.value('patrName'))
                            isStationaryDay = forceInt(record.value('isStationaryDay'))
                            if isCompactInfo:
                                if patrName:
                                    FIO = lastName + u' ' + firstName[0] + '.' + patrName[0] + '.'
                                else:
                                    FIO = lastName + u' ' + firstName[0] + '.'
                                order = [u'', u'п', u'э', u'с', u'принуд', u'вп', u'н'][forceInt(record.value('order'))]
                            else:
                                FIO = lastName + u' ' + firstName + u' ' + patrName
                                order = [u'', u'плановый', u'экстренный', u'самотёком', u'принудительный', u'внутренний перевод', u'неотложная'][forceInt(record.value('order'))]
                            for column in columns:
                                if column != 1 or (isStationaryDay and column == 1):
                                    if isEventInfo:
                                        externalId = forceString(record.value('externalId'))
                                        profileName = forceString(record.value('profileName'))
                                        orgStructureFrom = forceString(record.value('OrgStructureFrom'))
                                        orgStructureTo = forceString(record.value('OrgStructureTo'))
                                        table.setText(i, column, FIO + u', ' + externalId + u', ' + order \
                                            + ((u', ' +  profileName) if profileName else u'')\
                                            + ((u'\\Из: '+orgStructureFrom) if orgStructureFrom and transferDirection == 1 else u'')\
                                            + ((u'\\В: '+orgStructureTo) if orgStructureTo and transferDirection == 2 else u''))
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
                cond.append(tableOS['deleted'].eq(0))
                #cond.append(tableOS['type'].eq(0))
                queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
                cond.append(tableHBSchedule['code'].ne(1))
                if hospitalBedProfileId:
                    cond.append(tableRbHospitalBedProfile['id'].eq(hospitalBedProfileId))
                profileIdList = db.getDistinctIdList(queryTable, [tableRbHospitalBedProfile['id']], cond)
                return profileIdList

            def getDataReport(parOrgStructureIdList, table, firstRow, nextRow, name):
                profileIdList = getHospitalBedProfile(parOrgStructureIdList)
                if not profileIdList:
                    return firstRow, nextRow
                receivedAll = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, parOrgStructureIdList, True, False, isCompactInfo)
                receivedAllNoProfile = None
                if noProfileBed:
                    receivedAllNoProfile = getReceived(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, parOrgStructureIdList, True, True if noProfileBed else False, isCompactInfo)
                # из других отделений
                fromMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен из отделения', profileIdList, False, parOrgStructureIdList, True, isCompactInfo, transferType=1)
                # в другие отделения
                inMovingTransfer = getMovingTransfer(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, True, parOrgStructureIdList, True, isCompactInfo, transferType=0)
                leavedAll, leavedDeath, leavedTransfer = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, parOrgStructureIdList, True, False, isCompactInfo)

                leavedAllNoProfile = None
                leavedDeathNoProfile = None
                leavedTransferNoProfile = None
                if noProfileBed:
                    leavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile = getLeaved(isPermanentBed, noProfileBed, False, begDateTime, endDateTime, u'Переведен в отделение', profileIdList, parOrgStructureIdList, True, True if noProfileBed else False)

                sizeQuerys = [(receivedAll.size() + receivedAllNoProfile.size()) if noProfileBed else receivedAll.size(),
                             (leavedAll.size() + leavedAllNoProfile.size()) if noProfileBed else leavedAll.size(),
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
                setInfoClient(receivedAll, firstRow, nextRow, [0, 1], isEventInfo, receivedAllNoProfile)
                setInfoClient(leavedAll, firstRow, nextRow, [2], isEventInfo, leavedAllNoProfile)
                setInfoClient(leavedTransfer, firstRow, nextRow, [3], isEventInfo, leavedTransferNoProfile)
                return firstRow, nextRow

            boldChars = QtGui.QTextCharFormat()
            boldChars.setFontWeight(QtGui.QFont.Bold)
            def getOrgStructureParent(orgStructureIdList, rowProfile, table, firstRow, nextRow):
                for parentOrgStructureId in orgStructureIdList:
                    tableQuery = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
                    recordEx = db.getRecordEx(tableQuery,
                                              [tableOS['name'], tableOS['id']],
                                              [tableOS['deleted'].eq(0),
                                               #tableOS['type'].eq(0),
                                               tableOS['id'].eq(parentOrgStructureId)])
                    if recordEx:
                        name = forceString(recordEx.value('name'))
                        firstRow, nextRow = getDataReport([parentOrgStructureId], table, firstRow, nextRow, name)
                        records = db.getRecordList(tableQuery,
                                                   [tableOS['id'], tableOS['name']],
                                                   [tableOS['deleted'].eq(0),
                                                    #tableOS['type'].eq(0),
                                                    tableOS['parent_id'].eq(parentOrgStructureId)])
                        for record in records:
                            name = forceString(record.value('name'))
                            orgStructureId = forceRef(record.value('id'))
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
    if orgStructureIdList:
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
    cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
    cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
    cond.append(db.joinOr([tableOS['id'].isNull(), tableOS['deleted'].eq(0)]))
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
    #cond.append(tableOS['type'].eq(0))
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
    queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
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
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableClient = db.table('Client')
    tableOS = db.table('OrgStructure')
    tableAPOS = db.table('ActionProperty_OrgStructure')
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
    cond.append('''%s'''%(getOrgStructureProperty(u'Направлен в отделение', orgStructureIdList, u' = 0')))
    cond.append(u'''(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'7\')))''')
    if noPropertyProfile:
        cond.append('''%s'''%(getNoPropertyAPHBP()))
    else:
        cond.append('''%s'''%(getPropertyAPHBP(profile, noProfileBed)))
    if ageFor and ageTo and ageFor <= ageTo:
        cond.append(getAgeRangeCond(ageFor, ageTo))
    cond.append(tableAction['endDate'].isNotNull())
    cond.append(tableAction['endDate'].ge(begDateTime))
    cond.append(tableAction['endDate'].le(endDateTime))

    isStationaryDay = '''EXISTS(SELECT APS.id
    FROM ActionPropertyType AS APT
    INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
    INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
    WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id AND AP.action_id=Action.id AND APT.deleted=0
    AND APT.name LIKE '%s' AND APS.value LIKE '%s')'''%(u'Поступил из', u'КС')

    if boolFIO:
        col = 'code' if profileCode else 'name'
        stmt = db.selectDistinctStmt(queryTable, u'Client.lastName, Client.firstName, Client.patrName, Event.externalId, Event.order, %s AS isStationaryDay, %s'%(isStationaryDay, getPropertyAPHBPName(profile, noProfileBed, col)), cond)
        return db.query(stmt)
    else:
        cols = u'''COUNT(Client.id) AS countAll, SUM(IF(Event.order = 1, 1, 0)) AS orderPlan,
        SUM(IF(Event.order = 2, 1, 0)) AS orderExtren, SUM(%s) AS childrenCount, SUM(%s) AS adultCount,
        SUM(%s) AS clientRural, SUM(%s) AS isStationaryDay'''%(getChildrenCount(), getAdultCount(), getKladrClientRural(), isStationaryDay)
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


def getLeaved(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty = u'Переведен в отделение', profile = None, orgStructureIdList = [], boolFIO = False, noPropertyProfile = False, profileCode = False, additionalCond = None, ageFor = False, ageTo = False):
    db = QtGui.qApp.db
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
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
    cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
             tableAction['deleted'].eq(0),
             tableEvent['deleted'].eq(0),
             tableActionType['deleted'].eq(0),
             tableClient['deleted'].eq(0),
             tableAction['begDate'].isNotNull(),
             tableAction['endDate'].isNotNull()
           ]
    if additionalCond:
        cond.append(additionalCond)
    queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEvent['eventType_id'].eq(tableEventType['id']))
    cond.append('''%s'''%(getOrgStructureProperty(u'Отделение', orgStructureIdList, u' = 0')))
    cond.append(u'''(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'7\')))''')
    if noPropertyProfile:
        cond.append('''%s'''%(getNoPropertyAPHBP()))
    else:
        cond.append('''%s'''%(getPropertyAPHBP(profile, noProfileBed)))
    cond.append(tableAction['begDate'].ge(begDateTime))
    cond.append(tableAction['begDate'].le(endDateTime))
    if ageFor and ageTo and ageFor <= ageTo:
        cond.append(getAgeRangeCond(ageFor, ageTo))
    if boolFIO:
        col = 'code' if profileCode else 'name'
        colsFIO = u'''Client.lastName,
        Client.firstName,
        Client.patrName,
        Event.externalId,
        Event.order,
        %s'''%(getPropertyAPHBPName(profile, noProfileBed, col))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, cond)
        leavedAll = db.query(stmt)
        condTransfer = cond
        condTransfer.append(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'%стационар%\' OR APS.value LIKE \'%КС%\')'))
        stmt = db.selectDistinctStmt(queryTable, colsFIO, condTransfer)
        leavedTransfer = db.query(stmt)
        return [leavedAll, None, leavedTransfer]
    else:
        stmt = db.selectDistinctStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer, SUM(%s) AS adultCount'
                                    %(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'),
                                    getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'%стационар%\' OR APS.value LIKE \'%КС%\')'),
                                    getAdultCount()),
                                    where=cond)
        query = db.query(stmt)
        if query.first():
            record = query.record()
            return [forceInt(record.value('countAll')), forceInt(record.value('countDeath')), forceInt(record.value('countTransfer')), forceInt(record.value('adultCount'))]
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
    strIsScheduleJoin += u''' INNER JOIN rbHospitalBedShedule AS HBS ON OSHB.schedule_id = HBS.id'''
    strFilter += u''' AND HBS.code != 1'''
    return '''EXISTS(SELECT APHB.value
FROM ActionType AS AT
INNER JOIN Action AS A ON AT.id=A.actionType_id
INNER JOIN ActionPropertyType AS APT ON APT.actionType_id=AT.id
INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
INNER JOIN ActionProperty_HospitalBed AS APHB ON APHB.id=AP.id
INNER JOIN OrgStructure_HospitalBed AS OSHB ON OSHB.id=APHB.value%s%s
WHERE A.event_id=Event.id%s%s AND A.deleted=0 AND APT.actionType_id=A.actionType_id
AND AP.action_id=A.id AND AP.deleted=0 AND APT.deleted=0 AND APT.typeName LIKE 'HospitalBed'%s
AND (NOT %s)%s)'''%(strIsMedicalJoin, strIsScheduleJoin, strIsMedical, endDate, strFilter,
getTransferProperty(nameProperty),
u' AND %s'%(getDataOrgStructureStay(namePropertyStay, orgStructureIdList) if orgStructureIdList else u''))

