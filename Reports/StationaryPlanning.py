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
from PyQt4.QtCore import Qt, pyqtSignature, QDate, QDateTime, QTime


from library.Utils      import forceDate, forceDateTime, forceInt, forceRef, forceString
from Events.Utils       import getActionTypeIdListByFlatCode
from Reports.HospitalBedProfileListDialog import CHospitalBedProfileListDialog
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.SelectOrgStructureListDialog import CSelectOrgStructureListDialog
from Reports.Utils      import ( countMovingDays,
                                 dateRangeAsStr,
                                 getDataOrgStructureStay,
                                 getOrstructureHasHospitalBeds,
                                 getPropertyAPHBP,
                                 getStringProperty,
                                 getTheseAndChildrens,
                                 getTransferProperty,
                                 isEXISTSTransfer,
                               )

from Reports.Ui_StationaryPlanSetup import Ui_StationaryPlanSetupDialog


class CStationaryPlanSetupDialog(QtGui.QDialog, Ui_StationaryPlanSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.bedsScheduleList = []
        self.hospitalBedProfileList = []
        self.orgStructureList = []


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtBegTime.setTime(params.get('begTime', QTime()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtEndTime.setTime(params.get('endTime', QTime()))
        self.orgStructureList = params.get('orgStructureList', [])
        if self.orgStructureList:
            if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
                self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
            else:
                db = QtGui.qApp.db
                table = db.table('OrgStructure')
                records = db.getRecordList(table, [table['name']], [table['deleted'].eq(0), table['id'].inlist(self.orgStructureList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblOrgStructureList.setText(u', '.join(name for name in nameList if name))
        else:
            self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
        self.chkIsPermanentBed.setChecked(params.get('isPermanentBed', False))
        self.cmbBedsSchedule.setCurrentIndex(params.get('bedsSchedule', 0))
        self.hospitalBedProfileList = params.get('hospitalBedProfileList', [])
        if self.hospitalBedProfileList:
            db = QtGui.qApp.db
            table = db.table('rbHospitalBedProfile')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.hospitalBedProfileList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            self.lblHospitalBedProfileList.setText(u', '.join(name for name in nameList if name))
        else:
            self.lblHospitalBedProfileList.setText(u'не задано')


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['begTime'] = self.edtBegTime.time()
        result['endTime'] = self.edtEndTime.time()
        if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
           result['orgStructureList'] = []
        else:
            result['orgStructureList'] = self.orgStructureList
        result['isPermanentBed'] = self.chkIsPermanentBed.isChecked()
        result['bedsSchedule'] = self.cmbBedsSchedule.currentIndex()
        result['financeList'] = []
        result['financeName'] = []
        if self.chkFinance.isChecked():
            itemList = self.cmbFinance.model().takeColumn(0)
            for item in itemList:
                if item.checkState() == Qt.Checked:
                    result['financeList'].append(item.financeId)
                    result['financeName'].append(item.text())
        result['hospitalBedProfileList'] = self.hospitalBedProfileList
        return result


    @pyqtSignature('bool')
    def on_chkFinance_toggled(self, checked):
        self.cmbFinance.setEnabled(checked)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        if not date:
            stringInfo = u'Введите дату'
            self.lblEndDate.setToolTip(stringInfo)


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        if not date:
            stringInfo = u'Введите дату'
            self.lblBegDate.setToolTip(stringInfo)


    @pyqtSignature('')
    def on_btnHospitalBedProfileList_clicked(self):
        self.hospitalBedProfileList = []
        self.lblHospitalBedProfileList.setText(u'не задано')
        dialog = CHospitalBedProfileListDialog(self)
        if dialog.exec_():
            self.hospitalBedProfileList = dialog.values()
            if self.hospitalBedProfileList:
                db = QtGui.qApp.db
                table = db.table('rbHospitalBedProfile')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.hospitalBedProfileList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblHospitalBedProfileList.setText(u', '.join(name for name in nameList if name))


    @pyqtSignature('')
    def on_btnOrgStructureList_clicked(self):
        self.orgStructureList = []
        self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
        dialog = CSelectOrgStructureListDialog(self)
        if dialog.exec_():
            self.orgStructureList = dialog.values()
            if self.orgStructureList:
                if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
                    self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
                else:
                    db = QtGui.qApp.db
                    table = db.table('OrgStructure')
                    records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.orgStructureList)])
                    nameList = []
                    for record in records:
                        nameList.append(forceString(record.value('name')))
                    self.lblOrgStructureList.setText(u', '.join(name for name in nameList if name))


class CStationaryPlanning(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Анализ использования коечного фонда с учетом плановых показателей')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.stationaryF007SetupDialog = None
        self.clientDeath = 8


    def getSetupDialog(self, parent):
        result = CStationaryPlanSetupDialog(parent)
        self.stationaryF007SetupDialog = result
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params):
        description = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        begTime = params.get('begTime', QTime())
        endTime = params.get('endTime', QTime())
        description.append(dateRangeAsStr(u'за период', QDateTime(begDate, begTime), QDateTime(endDate, endTime)))
        orgStructureList = params.get('orgStructureList', None)
        if orgStructureList:
            if len(orgStructureList) == 1 and not orgStructureList[0]:
                description.append(u'подразделение: ЛПУ')
            else:
                db = QtGui.qApp.db
                table = db.table('OrgStructure')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(orgStructureList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                description.append(u'подразделение:  %s'%(u','.join(name for name in nameList if name)))
        else:
            description.append(u'подразделение: ЛПУ')
        hospitalBedProfileList = params.get('hospitalBedProfileList', None)
        if hospitalBedProfileList:
            db = QtGui.qApp.db
            table = db.table('rbHospitalBedProfile')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(hospitalBedProfileList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            description.append(u'профиль койки:  %s'%(u','.join(name for name in nameList if name)))
        else:
            description.append(u'профиль койки:  не задано')
        isPermanentBed = params.get('isPermanentBed', False)
        if isPermanentBed:
            description.append(u'учитывать внештатные койки')
        else:
            description.append(u'учитывать штатные койки')
        bedsSchedule = params.get('bedsSchedule', 0)
        if bedsSchedule:
            description.append(u'режим койки %s'%([u'круглосуточные', u'некруглосуточные'][bedsSchedule-1]))
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


    def getCaption(self, cursor, params, title):
        orgId = QtGui.qApp.currentOrgId()
        orgName = u''
        OKPO = u''
        if orgId:
            record = QtGui.qApp.db.getRecordEx('Organisation', 'shortName, OKPO', 'id=%s AND deleted = 0'%(str(orgId)))
            if record:
                orgName = forceString(record.value('shortName'))
                OKPO = forceString(record.value('OKPO'))
        underCaptionList = []
        orgStructureList = params.get('orgStructureList', None)
        if orgStructureList:
            if len(orgStructureList) == 1 and not orgStructureList[0]:
                underCaptionList.append(u'подразделение: ЛПУ')
            else:
                db = QtGui.qApp.db
                table = db.table('OrgStructure')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(orgStructureList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                underCaptionList.append(u'подразделение:  %s'%(u','.join(name for name in nameList if name)))
        else:
            underCaptionList.append(u'подразделение: ЛПУ')
        hospitalBedProfileList = params.get('hospitalBedProfileList', None)
        if hospitalBedProfileList:
            db = QtGui.qApp.db
            table = db.table('rbHospitalBedProfile')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(hospitalBedProfileList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            underCaptionList.append(u'профиль койки:  %s'%(u','.join(name for name in nameList if name)))
        else:
            underCaptionList.append(u'профиль койки:  не задано')
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


class CStationaryPlanMoving(CStationaryPlanning):
    def __init__(self, parent):
        CStationaryPlanning.__init__(self, parent)
        self.setTitle(u'Анализ использования коечного фонда с учетом плановых показателей')


    def getNameOrgStructure(self, idlist, begDateTime, endDateTime, financeList, dayStationary = False, hbProfileIdList = [], isPermanentBed=0):
        db = QtGui.qApp.db
        tableOrgStructure = db.table('OrgStructure')
        tableVHospitalBed = db.table('vHospitalBed')
        tableRBHospitalBedProfile = db.table('rbHospitalBedProfile')

        nameOrgStructureList = {}
#        cols = [tableOrgStructure['id'],
#                tableOrgStructure['code'],
#                tableOrgStructure['name'],
#                tableRBHospitalBedProfile['id'].alias('profileId'),
#                tableRBHospitalBedProfile['code'].alias('profileCode'),
#                tableRBHospitalBedProfile['name'].alias('profileName')
#                ]
        cols = []
        cols.append(u'DISTINCT OrgStructure.id AS orgStructureId')
        cols.append(tableOrgStructure['code'])
        cols.append(tableOrgStructure['name'])
        cols.append(tableRBHospitalBedProfile['id'].alias('profileId'))
        cols.append(tableRBHospitalBedProfile['code'].alias('profileCode'))
        cols.append(tableRBHospitalBedProfile['name'].alias('profileName'))

        cond = [tableOrgStructure['id'].inlist(idlist),
                tableOrgStructure['deleted'].eq(0),
                tableOrgStructure['hasHospitalBeds'].ne(0)
                ]
        if not isPermanentBed:
            cond.append(tableVHospitalBed['isPermanent'].eq(1))
        cond.append(db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)]))
        cond.append(db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(begDateTime)]))
        if hbProfileIdList:
            cond.append(tableRBHospitalBedProfile['id'].inlist(hbProfileIdList))
        if dayStationary:
            cond.append(tableOrgStructure['type'].eq(0))
        else:
            cond.append(tableOrgStructure['type'].ne(0))

        if len(financeList)>0:
            cond.append(tableVHospitalBed['finance_id'].inlist(financeList))

        table = tableOrgStructure.innerJoin(tableVHospitalBed, tableVHospitalBed['master_id'].eq(tableOrgStructure['id']))
        table = table.innerJoin(tableRBHospitalBedProfile, tableVHospitalBed['profile_id'].eq(tableRBHospitalBedProfile['id']))
        records = db.getRecordList(table, cols, cond)
        for record in records:
            orgStructureId = forceRef(record.value('orgStructureId'))
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            profileId = forceRef(record.value('profileId'))
            profileCode = forceString(record.value('profileCode'))
            profileName = forceString(record.value('profileName'))

            orgStructureList = nameOrgStructureList.get(orgStructureId, [])
            profileIdList = {}
            if orgStructureList:
                profileIdList = orgStructureList[2]
            profileIdList[profileId] = (profileCode, profileName)
            nameOrgStructureList[orgStructureId] = [code, name, profileIdList]
        return nameOrgStructureList


    def dataMovingDays(self, orgStructureIdList, begDatePeriod, endDatePeriod, financeList, profile = None, isHospital = None, dayStat=False):
        days = 0
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableContract = db.table('Contract')
        tableClient = db.table('Client')
        tableOrg = db.table('Organisation')
        tableOS = db.table('OrgStructure')
        tableAPHB = db.table('ActionProperty_HospitalBed')
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableHPS = db.table('rbHospitalBedShedule')
        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.leftJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.leftJoin(tableContract, tableEvent['contract_id'].eq(tableContract['id']))
        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
        queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
        queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
        queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        queryTable = queryTable.innerJoin(tableOrg, tableOrg['id'].eq(tableOS['organisation_id']))
        queryTable = queryTable.innerJoin(tableHPS, tableHPS['id'].eq(tableOSHB['schedule_id']))
        cols = [tableEvent['id'].alias('eventId'),
                tableAction['id'].alias('actionId'),
                tableAction['begDate'], tableAction['endDate'],
                tableHPS['code'].alias('schedCode')
                ]
        cond = [tableActionType['flatCode'].like('moving%'),
                tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableAP['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableAPT['deleted'].eq(0),
                tableOS['deleted'].eq(0),
                tableClient['deleted'].eq(0),
                tableOrg['deleted'].eq(0),
                tableAPT['typeName'].like('HospitalBed'),
                tableAP['action_id'].eq(tableAction['id'])
               ]
        if isHospital is not None:
           cond.append(tableOrg['isHospital'].eq(isHospital))
        if dayStat:
            cond.append(tableOS['type'].eq(0))
        else:
            cond.append(tableOS['type'].ne(0))
        if len(financeList):
            cond.append(tableContract['finance_id'].inlist(financeList))
        if profile:
            cond.append(tableOSHB['profile_id'].inlist([profile]))
        if orgStructureIdList:
            cond.append(tableOSHB['master_id'].inlist([orgStructureIdList]))
        joinAnd = db.joinAnd([tableAction['endDate'].isNull(),
                              tableAction['begDate'].isNotNull(),
                              tableAction['begDate'].lt(endDatePeriod)])
        cond.append(db.joinOr([db.joinAnd([tableAction['endDate'].isNotNull(),
                                           tableAction['endDate'].gt(begDatePeriod),
                                           tableAction['begDate'].isNotNull(),
                                           tableAction['begDate'].lt(endDatePeriod)]), joinAnd]))
        stmt = db.selectStmt(queryTable, cols, cond)
        query = db.query(stmt)
        actionIdList = []
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            if actionId not in actionIdList:
                actionIdList.append(actionId)
                begDate = forceDateTime(record.value('begDate'))
                endDate = forceDateTime(record.value('endDate'))
                schedule = forceInt(record.value('schedCode'))
                if begDate < begDatePeriod:
                    begDate = begDatePeriod #.addDays(-1)
                if not endDate or endDate > endDatePeriod:
                    endDate = endDatePeriod
                    if schedule != 1:
                        days -= 1
                    if endDate.date().dayOfYear() == endDate.date().daysInYear() or endDate.date().dayOfYear() == 1:
                        days += 1
                if begDate and endDate:
                    daysTo = begDate.daysTo(endDate)
                    days += daysTo
                    begTime = begDate.time()
                    endTime = endDate.time()
                    if schedule != 1:
                        days += 1
                    else:
                        dayOfYear = begDate.date().dayOfYear()
                        if daysTo:
                            if begTime < QTime(9, 0) and dayOfYear != 1:
                                days += 1
                            if endTime < QTime(9, 0):
                                days -= 1
                        else:
                            if begTime < QTime(9, 0) and dayOfYear != 1 and endTime >= QTime(9, 0):
                                days += 1
        return days


#    def getCountPatronageList(self, orgStructureIdList, begDateTime, endDateTime, noProfileBed, profile = None, bedsSchedule = False):
#        countPatronage = 0
#        if begDateTime <= endDateTime:
#            newBegDateTime = begDateTime.addDays(1)
#            if newBegDateTime >= endDateTime:
#                newBegDateTime = endDateTime
#            while newBegDateTime <= endDateTime:
#                countPatronage += self.getCountPatronage(orgStructureIdList, newBegDateTime, noProfileBed, profile, bedsSchedule)
#                newBegDateTime = newBegDateTime.addDays(1)
#        return countPatronage
#
#
#    def getCountPatronage(self, orgStructureId, endDateTime, noProfileBed, profile = None, dayStat = False):
#        countPatronage = 0
#        db = QtGui.qApp.db
#        tableAPT = db.table('ActionPropertyType')
#        tableAP = db.table('ActionProperty')
#        tableActionType = db.table('ActionType')
#        tableAction = db.table('Action')
#        tableEvent = db.table('Event')
#        tableClient = db.table('Client')
#        tableOS = db.table('OrgStructure')
#        tableAPHB = db.table('ActionProperty_HospitalBed')
#        tableOSHB = db.table('OrgStructure_HospitalBed')
#        tableHBSchedule = db.table('rbHospitalBedShedule')
#        cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
#                 tableAction['deleted'].eq(0),
#                 tableEvent['deleted'].eq(0),
#                 tableAP['deleted'].eq(0),
#                 tableActionType['deleted'].eq(0),
#                 tableClient['deleted'].eq(0),
#                 tableAP['action_id'].eq(tableAction['id'])
#               ]
#        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
#        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
#        queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
#        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
#        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
#        queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
#        queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
#        queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
#        cond.append(tableAPT['typeName'].like('HospitalBed'))
#        if orgStructureId:
#            cond.append(tableOS['deleted'].eq(0))
#            cond.append(tableOS['id'].eq(orgStructureId))
#            if dayStat:
#                cond.append(tableOS['type'].eq(0))
#            else:
#                cond.append(tableOS['type'].ne(0))
#        if not noProfileBed:
#            cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
#        if profile:
#            if QtGui.qApp.defaultHospitalBedProfileByMoving():
#                cond.append(getPropertyAPHBP(profile, noProfileBed))
#            else:
#                if noProfileBed and len([profile]) > 1:
#                    cond.append(db.joinOr([tableOSHB['profile_id'].eq(profile), tableOSHB['profile_id'].isNull()]))
#                else:
#                    cond.append(tableOSHB['profile_id'].eq(profile))
#        else:
#            if QtGui.qApp.defaultHospitalBedProfileByMoving():
#                cond.append(getPropertyAPHBP([], noProfileBed))
#            else:
#                cond.append(tableOSHB['profile_id'].isNull())
#        if self.bedsSchedule:
#            queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
#        if self.bedsSchedule == 1:
#            cond.append(tableHBSchedule['code'].eq(1))
#        elif self.bedsSchedule == 2:
#            cond.append(tableHBSchedule['code'].ne(1))
#        cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
#        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
#        cond.append(getStringProperty(u'''Патронаж%''', u'''(APS.value = 'Да')'''))
#        stmt = db.selectStmt(queryTable, u'COUNT(Action.id) AS countPatronage', where=cond)
#        query = db.query(stmt)
#        while query.next():
#            record = query.record()
#            countPatronage += forceInt(record.value('countPatronage'))
#        return countPatronage


    def getCountPatronageList(self, orgStructureId, begDateTime, endDateTime, noProfileBed, profile = None, dayStat = False):
        countPatronage = 0
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
        cond.append(tableAPT['typeName'].like('HospitalBed'))
        if orgStructureId:
            cond.append(tableOS['deleted'].eq(0))
            cond.append(tableOS['id'].eq(orgStructureId))
            if dayStat:
                cond.append(tableOS['type'].eq(0))
            else:
                cond.append(tableOS['type'].ne(0))
        if not noProfileBed:
            cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
        if profile:
            if QtGui.qApp.defaultHospitalBedProfileByMoving():
                cond.append(getPropertyAPHBP([profile], noProfileBed))
            else:
                if noProfileBed and profile:
                    cond.append(db.joinOr([tableOSHB['profile_id'].eq(profile), tableOSHB['profile_id'].isNull()]))
                else:
                    cond.append(tableOSHB['profile_id'].eq(profile))
        else:
            if QtGui.qApp.defaultHospitalBedProfileByMoving():
                cond.append(getPropertyAPHBP([], noProfileBed))
            else:
                cond.append(tableOSHB['profile_id'].isNull())
        if self.bedsSchedule:
            queryTable = queryTable.innerJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
        else:
            queryTable = queryTable.leftJoin(tableHBSchedule, tableOSHB['schedule_id'].eq(tableHBSchedule['id']))
        if self.bedsSchedule == 1:
            cond.append(tableHBSchedule['code'].eq(1))
        elif self.bedsSchedule == 2:
            cond.append(tableHBSchedule['code'].ne(1))
        cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].le(endDateTime)]))
        cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(begDateTime)]))
        cond.append(getStringProperty(u'''Патронаж%''', u'''(APS.value = 'Да')'''))
        cols = [tableAction['id'].alias('actionId'),
                tableAction['begDate'],
                tableAction['endDate'],
                tableHBSchedule['code'].alias('scheduleCode')
                ]
        stmt = db.selectStmt(queryTable, cols, where=cond)
        query = db.query(stmt)
        actionIdList = []
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            if actionId not in actionIdList:
                actionIdList.append(actionId)
                begDate = forceDateTime(record.value('begDate'))
                endDate = forceDateTime(record.value('endDate'))
                schedule = forceInt(record.value('scheduleCode'))
                countPatronage += countMovingDays(begDate, endDate, begDateTime, endDateTime, schedule)
        return countPatronage


    def getReceived(self, begDateTime, endDateTime, profileId, orgStructureId, financeList, nameProperty = u'Переведен из отделения', dayStat=False):
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableContract = db.table('Contract')
        tableOS = db.table('OrgStructure')
        tableAPOS = db.table('ActionProperty_OrgStructure')
        cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('received%')),
                 tableAction['deleted'].eq(0),
                 tableEvent['deleted'].eq(0),
                 tableAP['deleted'].eq(0),
                 tableActionType['deleted'].eq(0),
                 tableClient['deleted'].eq(0),
                 tableAP['action_id'].eq(tableAction['id']),
                 tableAction['endDate'].isNotNull(),
                 tableOS['deleted'].eq(0),
                 tableAPT['name'].like(u'Направлен в отделение')
                ]
        if orgStructureId:
            cond.append(tableOS['id'].eq(orgStructureId))
            if dayStat:
                cond.append(tableOS['type'].eq(0))
            else:
                cond.append(tableOS['type'].ne(0))
        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
        queryTable = queryTable.innerJoin(tableAPOS, tableAPOS['id'].eq(tableAP['id']))
        queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableAPOS['value']))
        if len(financeList):
            queryTable = queryTable.innerJoin(tableContract, tableEvent['contract_id'].eq(tableContract['id']))
            cond.append(tableContract['finance_id'].inlist(financeList))
        cond.append('''%s'''%(self.getDataAPHBnoProperty(nameProperty, [profileId], [orgStructureId], u'Отделение пребывания', u'', dayStat)))
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].ge(begDateTime))
        cond.append(tableAction['begDate'].le(endDateTime))

        stmt = db.selectStmt(queryTable, u'''COUNT(Client.id) AS countAll''', cond)
        query = db.query(stmt)
        if query.first():
            record = query.record()
            return forceInt(record.value('countAll'))
        else:
            return 0


    def getDataAPHBnoProperty(self, nameProperty, profileList=[], orgStructureIdList=[], namePropertyStay=u'Отделение пребывания', endDate = u'', dayStat=False):
        strFilter = u''''''
        actionTypeIdList = getActionTypeIdListByFlatCode(u'moving%')
        if profileList:
            strFilter += u''' AND (OSHB.profile_id IN (%s))'''%((','.join(forceString(profile) for profile in profileList if profile)))
        return '''EXISTS(SELECT APHB.value
    FROM ActionType AS AT
    INNER JOIN Action AS A ON AT.id=A.actionType_id
    INNER JOIN ActionPropertyType AS APT ON APT.actionType_id=AT.id
    INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
    INNER JOIN ActionProperty_HospitalBed AS APHB ON APHB.id=AP.id
    INNER JOIN OrgStructure_HospitalBed AS OSHB ON OSHB.id=APHB.value
    INNER JOIN OrgStructure AS OS ON OS.id=OSHB.master_id
    WHERE A.event_id=Event.id%s AND A.deleted=0 AND APT.actionType_id=A.actionType_id
    AND AP.action_id=A.id AND AP.deleted=0
    AND APT.deleted=0 AND APT.typeName = 'HospitalBed'%s AND (NOT %s)%s
    AND OS.deleted = 0%s %s)'''%(endDate, strFilter, getTransferProperty(nameProperty, dayStat),
    u' AND %s'%(getDataOrgStructureStay(namePropertyStay, orgStructureIdList, dayStat) if orgStructureIdList else u''),
    u' AND OS.type = 0' if dayStat else u' AND OS.type != 0',
    u''' AND (A.actionType_id IN (%s))'''%((','.join(forceString(actionTypeId) for actionTypeId in actionTypeIdList if actionTypeId)))
    )


    def dataInvolutionDays(self, orgStructureId, begDatePeriod, endDatePeriod, financeList, profileId, dayStat):
        days = 0
        condRepairs = []
        db = QtGui.qApp.db
        tableOS = db.table('OrgStructure')
        tableVHospitalBed = db.table('vHospitalBed')
        tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
        tableHBSchedule = db.table('rbHospitalBedShedule')
        queryTable = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
        queryTable = queryTable.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id']))
        condRepairs.append(tableOS['deleted'].eq(0))
        condRepairs.append(tableVHospitalBed['master_id'].eq(orgStructureId))
        if dayStat:
            condRepairs.append(tableOS['type'].eq(0))
        else:
            condRepairs.append(tableOS['type'].ne(0))
        if self.bedsSchedule > 0:
            queryTable = queryTable.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableVHospitalBed['id']))
        if self.bedsSchedule == 1:
            condRepairs.append(tableHBSchedule['code'].eq(1))
        elif self.bedsSchedule == 2:
            condRepairs.append(tableHBSchedule['code'].ne(1))
        if profileId:
           condRepairs.append(tableVHospitalBed['profile_id'].eq(profileId))
        condRepairs.append('''OrgStructure_HospitalBed_Involution.involutionType != 0
                               AND (OrgStructure_HospitalBed_Involution.begDate IS NULL
                               OR OrgStructure_HospitalBed_Involution. endDate IS NULL
                               OR (OrgStructure_HospitalBed_Involution.begDate >= '%s'
                               AND OrgStructure_HospitalBed_Involution. endDate <= '%s'))'''%(begDatePeriod.toString(Qt.ISODate), begDatePeriod.toString(Qt.ISODate)))
        stmt = db.selectStmt(queryTable, [tableVHospitalBed['id'].alias('bedId'), tableInvolution['begDate'].alias('begDateInvolute'), tableInvolution['endDate'].alias('endDateInvolute')], condRepairs)
        query = db.query(stmt)
        bedIdList = []
        while query.next():
            record = query.record()
            bedId = forceRef(record.value('bedId'))
            if bedId not in bedIdList:
                bedIdList.append(bedId)
                begDate = forceDate(record.value('begDateInvolute'))
                endDate = forceDate(record.value('endDateInvolute'))
                if not begDate or begDate < begDatePeriod.date():
                    begDate = begDatePeriod.date()
                if not endDate or endDate > endDatePeriod.date():
                    endDate = endDatePeriod.date()
                if begDate and endDate:
                    if begDate == endDate:
                        days += 1
                    else:
                        days += begDate.daysTo(endDate)
        return days


    def getLeaved(self, begDateTime, endDateTime, profileId, orgStructureId, financeList, nameProperty = u'Переведен в отделение', dayStat=False, eventList = False):
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableContract = db.table('Contract')
        tableClient = db.table('Client')
        cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
                 tableAction['deleted'].eq(0),
                 tableEvent['deleted'].eq(0),
                 tableActionType['deleted'].eq(0),
                 tableClient['deleted'].eq(0),
                 tableAction['endDate'].isNotNull()
               ]
        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        if len(financeList):
            queryTable = queryTable.innerJoin(tableContract, tableEvent['contract_id'].eq(tableContract['id']))
            cond.append(tableContract['finance_id'].inlist(financeList))
        cond.append('''%s'''%(self.getDataAPHBnoProperty(nameProperty, [profileId], [orgStructureId], u'Отделение пребывания', u' AND A.endDate IS NOT NULL', dayStat)))
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].ge(begDateTime))
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].le(endDateTime))
        if eventList:
            eventIdList = []
            stmt = db.selectStmt(queryTable, u'DISTINCT Event.id', where=cond)
            query = db.query(stmt)
            while query.next():
                record = query.record()
                eventId = forceRef(record.value('id'))
                if eventId and eventId not in eventIdList:
                    eventIdList.append(eventId)
            return eventIdList
        else:
            stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer'%(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'), getStringProperty(u'Исход госпитализации', u'(APS.value = \'переведен в другой стационар\')')), where=cond)
            query = db.query(stmt)
            if query.first():
                record = query.record()
                return [forceInt(record.value('countAll')), forceInt(record.value('countDeath')), forceInt(record.value('countTransfer'))]
            else:
                return [0, 0, 0]


    def build(self, params):
        db = QtGui.qApp.db
        tableVHospitalBed = db.table('vHospitalBed')
        tableHBSchedule = db.table('rbHospitalBedShedule')
        tableOS = db.table('OrgStructure')
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        begTime = params.get('begTime', QTime())
        endTime = params.get('endTime', QTime())
        begDateTime = QDateTime(begDate, begTime)
        endDateTime = QDateTime(endDate, endTime)
        self.bedsSchedule = params.get('bedsSchedule', 0)
        if begDate and endDate:
            self.countDaysInPeriod = begDate.daysTo(endDate)
        else:
            self.countDaysInPeriod = 0
        hospitalBedProfileList = params.get('hospitalBedProfileList', None)
        orgStructureIdListFilter =  params.get('orgStructureList', [])
        noProfileBed = params.get('noProfileBed', True)
        isPermanentBed = params.get('isPermanentBed', False)
        financeList = params.get('financeList', [])
        dayStatList =[False, True]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Анализ исполнения плановых показателей')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('8%',[u'Отделение', u''], CReportBase.AlignLeft),
                ('8%', [u'Профиль', u''], CReportBase.AlignLeft),
                ('4%', [u'Разв. коек', u''], CReportBase.AlignRight),
                ('4%', [u'Среднемесячн. коек', u''], CReportBase.AlignRight),
                ('4%', [u'Пролеченн. больные', u'План'], CReportBase.AlignRight),
                ('4%', [u'', u'Факт.'], CReportBase.AlignRight),
                ('4%', [u'', u'% вып.'], CReportBase.AlignRight),
                ('4%', [u'Проведено к/д', u'План'], CReportBase.AlignRight),
                ('4%', [u'', u'Факт.'], CReportBase.AlignRight),
                ('4%', [u'', u'% вып.'], CReportBase.AlignRight),
                ('4%', [u'Работа койки', u'План'], CReportBase.AlignRight),
                ('4%', [u'', u'Факт.'], CReportBase.AlignRight),
                ('4%', [u'Ср.длит. пребыв. на к-ке', u''], CReportBase.AlignRight),
                ('4%', [u'Оборот койки', u''], CReportBase.AlignRight),
                ('4%', [u'Леталь-ность', u''], CReportBase.AlignRight),
                ('4%', [u'Пользова-нные б-ные', u''], CReportBase.AlignRight),
                ('4%', [u'К/д закрытия', u''], CReportBase.AlignRight),
                ('4%', [u'Простой койки', u''], CReportBase.AlignRight),
                ('4%', [u'Факт. развер-нуто к/д', u''], CReportBase.AlignRight),
                ('4%', [u'% заполне-ния', u''], CReportBase.AlignRight),
                ('4%', [u'Ср. число своб. мест ежеднев-но', u''], CReportBase.AlignRight),
                ('4%', [u'Ср. число больных ежеднев-но', u''], CReportBase.AlignRight),
                ('4%', [u'Состоит матерей при больных детях', u''], CReportBase.AlignRight)
               ]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 2, 1)
        table.mergeCells(0, 4, 1, 3)
        table.mergeCells(0, 7, 1, 3)
        table.mergeCells(0, 10, 1, 2)
        table.mergeCells(0, 12, 2, 1)
        table.mergeCells(0, 13, 2, 1)
        table.mergeCells(0, 14, 2, 1)
        table.mergeCells(0, 15, 2, 1)
        table.mergeCells(0, 16, 2, 1)
        table.mergeCells(0, 17, 2, 1)
        table.mergeCells(0, 18, 2, 1)
        table.mergeCells(0, 19, 2, 1)
        table.mergeCells(0, 20, 2, 1)
        table.mergeCells(0, 21, 2, 1)
        table.mergeCells(0, 22, 2, 1)

        endDateTimeForPlanning = endDateTime.addDays(-1)

        begMonth = begDateTime.date().month()
        endMonth = endDateTimeForPlanning.date().month()
        begYear = begDateTime.date().year()
        endYear = endDateTimeForPlanning.date().year()

        def unrolledHospitalBed34(orgStructureId, profileId, row, dayStat):
            condRepairs = []
            tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
            tableVHospitalBedSchedule = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
            tableVHospitalBedSchedule = tableVHospitalBedSchedule.leftJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id']))
            countCol = u'''IF(OrgStructure_HospitalBed_Involution.id IS NULL,
            vHospitalBed.id,

            (SELECT OSHBI.`master_id`
            FROM OrgStructure_HospitalBed_Involution AS OSHBI
            WHERE OSHBI.`master_id`=vHospitalBed.`id`
            AND (OSHBI.involutionType != 0
                                   AND (OSHBI.begDate IS NULL
                                   OR OSHBI.endDate IS NULL

                                   OR IF(OSHBI.begDate > '%s'
                                   AND OSHBI.endDate < '%s', 0, 1)))
            LIMIT 1
            )
)'''%(endDateTime.toString(Qt.ISODate), begDateTime.toString(Qt.ISODate))
            if dayStat:
                condRepairs.append(tableOS['type'].eq(0))
            else:
                condRepairs.append(tableOS['type'].ne(0))
            condRepairs.append(tableVHospitalBed['master_id'].eq(orgStructureId))
            if profileId:
                if noProfileBed:
                    condRepairs.append(db.joinOr([tableVHospitalBed['profile_id'].eq(profileId), tableVHospitalBed['profile_id'].isNull()]))
                else:
                    condRepairs.append(tableVHospitalBed['profile_id'].eq(profileId))
            else:
                condRepairs.append(tableVHospitalBed['profile_id'].isNull())
            if not isPermanentBed:
                condRepairs.append(tableVHospitalBed['isPermanent'].eq(1))
            if self.bedsSchedule > 0:
                tableVHospitalBedSchedule = tableVHospitalBedSchedule.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
            if self.bedsSchedule == 1:
                condRepairs.append(tableHBSchedule['code'].eq(1))
            elif self.bedsSchedule == 2:
                condRepairs.append(tableHBSchedule['code'].ne(1))
            joinOr1 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDateTime)])
            joinOr2 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(begDateTime)])
            condRepairs.append(db.joinAnd([joinOr1, joinOr2]))
            countBedsRepairs = db.getDistinctCount(tableVHospitalBedSchedule, countCol, where=condRepairs)
            table.setText(row, 2, countBedsRepairs)
            return countBedsRepairs

        def unrolledHospitalBedsMonth(monthEnd, yearDateInt, profileId, orgStructureId, dayStat):
            monthEndDate = QDate(yearDateInt, monthEnd, 1)
            tableVHospitalBed = db.table('vHospitalBed')
            endDate = QDate(yearDateInt, monthEnd, monthEndDate.daysInMonth())
            cond = []
            cond.append(tableVHospitalBed['master_id'].eq(orgStructureId))
            if dayStat:
                cond.append(tableOS['type'].eq(0))
            else:
                cond.append(tableOS['type'].ne(0))
            if profileId:
               cond.append(tableVHospitalBed['profile_id'].eq(profileId))
            tableQuery = tableVHospitalBed.leftJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
            if self.bedsSchedule > 0:
                tableQuery = tableQuery.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
            if self.bedsSchedule == 1:
                cond.append(tableHBSchedule['code'].eq(1))
            elif self.bedsSchedule == 2:
                cond.append(tableHBSchedule['code'].ne(1))
            joinOr1 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].lt(endDate)])
            joinOr2 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(endDate)])
            cond.append(db.joinAnd([joinOr1, joinOr2]))
            cond.append(tableVHospitalBed['isPermanent'].eq('1'))
            countBeds = db.getCount(tableQuery, countCol='vHospitalBed.id', where=cond)
            return countBeds

        def getUnrolledHospitalBedsMonth(row, begMonth, begYear, endMonth, endYear, profileId, orgStructureId, typeResult, dayStat, totalResult):
            countBedsMonth = 0
            curYear = begYear
            curMonth = begMonth
            firstMonthYear = True
            while curYear <= endYear:
                if firstMonthYear:
                    firstMonthYear = False
                else:
                    curMonth = 1
                while curMonth <= endMonth:
                    countBedsMonth += unrolledHospitalBedsMonth(curMonth, curYear, profileId, orgStructureId, dayStat)
                    curMonth += 1
                curYear += 1
            if curMonth != begMonth:
                monthDivision = curMonth - begMonth
            else:
                monthDivision = 1
            countBedsMonth = countBedsMonth/monthDivision
            table.setText(row, 3, countBedsMonth)
            involutionBeds = countBedsMonth
            typeResult[1] += countBedsMonth
            totalResult[1] += countBedsMonth
            return involutionBeds

        def getPlanningHospitalActivity(row, begMonth, begYear, endMonth, endYear, profileId, orgStructureId, typeResult, dayStat, totalResult):
            tableRBPlanningHA = db.table('OrgStructure_Planning')
            plans = 0
            bedDays = 0
            curMonth = begMonth
            curYear = begYear
            firstMonthYear = True
            while curYear <= endYear:
                curMonthList = []
                if firstMonthYear:
                    firstMonthYear = False
                else:
                    curMonth = 1
                while curMonth <= endMonth:
                    curMonthList.append(curMonth)
                    curMonth += 1
                cond = []
                group = u''
                if dayStat:
                    cond.append(tableOS['type'].eq(0))
                else:
                    cond.append(tableOS['type'].ne(0))
                cond.append(tableRBPlanningHA['orgStructure_id'].eq(orgStructureId))
                tableQuery = tableRBPlanningHA.innerJoin(tableOS,  tableRBPlanningHA['orgStructure_id'].eq(tableOS['id']))
                if self.bedsSchedule > 0:
                    tableQuery = tableQuery.leftJoin(tableVHospitalBed,  tableVHospitalBed['master_id'].eq(tableOS['id']))
                    group += u'vHospitalBed.schedule_id,'
                if self.bedsSchedule > 1:
                    tableQuery = tableQuery.innerJoin(tableHBSchedule, tableVHospitalBed['schedule_id'].eq(tableHBSchedule['id']))
                if self.bedsSchedule == 2:
                    cond.append(tableHBSchedule['code'].eq(1))
                elif self.bedsSchedule == 2:
                    cond.append(tableHBSchedule['code'].ne(1))
                if profileId:
                    cond.append(tableRBPlanningHA['profile_id'].eq(profileId))
                    group += u'OrgStructure_Planning.profile_id'
                cond.append(tableRBPlanningHA['year'].eq(curYear))
                planRecords = db.getRecordListGroupBy(tableQuery, u'OrgStructure_Planning.*', cond, group)
                for planRecord in planRecords:
                    for i in curMonthList:
                        plans += forceInt(planRecord.value('plan%i'%i))
                        bedDays += forceInt(planRecord.value('bedDays%i'%i))
                curYear += 1
            table.setText(row, 4, plans)
            typeResult[2] += plans
            totalResult[2] += plans
            table.setText(row, 7, bedDays)
            typeResult[5] += bedDays
            totalResult[5] += bedDays
            return plans, bedDays
        colSize = 21
        totalPlans = 0
        totalFacts = 0
        totalMovingDays = 0
        totalBedDays = 0
        totalInvolutionBeds = 0
        totalCuredClient = 0
        totalDeathClient = 0
        for dayStat in dayStatList:
            typeResult = [0]*colSize
            totalBool = False
            orgStructureIdList = getOrstructureHasHospitalBeds(getTheseAndChildrens(orgStructureIdListFilter))
            nameOrgStructureList = self.getNameOrgStructure(orgStructureIdList, begDateTime, endDateTime, financeList, dayStat, hbProfileIdList=hospitalBedProfileList, isPermanentBed=isPermanentBed)
            for orgStructureId, orgStructureInfo in nameOrgStructureList.items():
                totalResult = [0]*colSize
                totalOrgStrPlans = 0
                totalOrgStrFacts = 0
                totalOrgStrMovingDays = 0
                totalOrgStrBedDays = 0
                totalOrgStrInvolutionBeds = 0
                totalOrgStrCuredClient = 0
                name = orgStructureInfo[1]
                profileIdList = orgStructureInfo[2]
                rowProfile = table.addRow()
                table.setText(rowProfile, 0, name)
                lenProfileIdList = len(profileIdList)
                cnt = 0
                rowProfileOld = rowProfile
                for profileId, profileInfo in profileIdList.items():
                    totalBool = True
                    table.setText(rowProfile, 1, profileInfo[1])
                    countBedsRepairs = unrolledHospitalBed34(orgStructureId, profileId, rowProfile, dayStat)
                    typeResult[0] += countBedsRepairs
                    totalResult[0] += countBedsRepairs
                    factHB = countBedsRepairs * self.countDaysInPeriod
                    table.setText(rowProfile, 18, factHB)
                    totalResult[16] += factHB
                    typeResult[16] += factHB
                    involutionBeds = getUnrolledHospitalBedsMonth(rowProfile, begMonth, begYear, endMonth, endYear, profileId, orgStructureId, typeResult, dayStat, totalResult)
                    plans, bedDays = getPlanningHospitalActivity(rowProfile, begMonth, begYear, endMonth, endYear, profileId, orgStructureId, typeResult, dayStat, totalResult)
                    receivedClient = self.getReceived(begDateTime, endDateTime, profileId, orgStructureId, financeList, u'Переведен из отделения', dayStat)
                    leavedAll, deathAll, tranfarAll = self.getLeaved(begDateTime, endDateTime, profileId, orgStructureId, financeList, u'Переведен в отделение', dayStat)
                    curedClient = round((receivedClient + leavedAll) / 2.0, 2)
                    deathPat = round((deathAll*100)/curedClient if deathAll else 0.00, 2)
                    table.setText(rowProfile, 14, deathPat)
                    receivedFact = leavedAll
                    procentReceivedFact = round(((receivedFact*100.0)/plans) if plans else 0.00, 2)
                    table.setText(rowProfile, 5, receivedFact)
                    table.setText(rowProfile, 6, procentReceivedFact)
                    totalPlans += plans
                    totalFacts += receivedFact
                    totalOrgStrPlans += plans
                    totalOrgStrFacts += receivedFact
                    typeResult[3] += receivedFact
                    totalResult[3] += receivedFact
                    totalResult[4] = round(((totalOrgStrFacts*100.0)/totalOrgStrPlans) if totalOrgStrPlans else 0.00, 2)
                    typeResult[4] = round(((totalFacts*100.0)/totalPlans) if totalPlans else 0.00, 2)
                    movingDays = self.dataMovingDays(orgStructureId, begDateTime, endDateTime, financeList, profileId, None, dayStat)
                    table.setText(rowProfile, 8, movingDays)
                    movingDaysCountBedsRepairs =  round(((movingDays / (factHB*1.0))*100.0) if factHB else 0.00, 2)
                    table.setText(rowProfile, 19, movingDaysCountBedsRepairs)
                    hbCurrentDay = round(((factHB - movingDays)/float(self.countDaysInPeriod)) if self.countDaysInPeriod else 0, 1)
                    typeResult[18] += hbCurrentDay
                    totalResult[18] += hbCurrentDay
                    table.setText(rowProfile, 20, hbCurrentDay)
                    clCurrentDay = round((movingDays / float(self.countDaysInPeriod)) if self.countDaysInPeriod else 0, 1)
                    typeResult[19] += clCurrentDay
                    totalResult[19] += clCurrentDay
                    table.setText(rowProfile, 21, clCurrentDay)
                    procentMovingDays = round(((movingDays*100.0)/bedDays) if bedDays else 0.00, 2)
                    table.setText(rowProfile, 9, procentMovingDays)
                    typeResult[6] += movingDays
                    totalResult[6] += movingDays
                    totalMovingDays = typeResult[6]
                    totalBedDays += bedDays
                    totalOrgStrMovingDays = totalResult[6]
                    totalOrgStrBedDays += bedDays
                    totalResult[7] = round(((totalOrgStrMovingDays*100.0)/totalOrgStrBedDays) if totalOrgStrBedDays else 0.00, 2)
                    typeResult[7] = round(((totalMovingDays*100.0)/totalBedDays) if totalBedDays else 0.00, 2)
                    totalResult[17] = round(((totalOrgStrMovingDays / (totalResult[16]*1.0))*100.0) if totalResult[16] else 0.00, 2)
                    typeResult[17] = round(((totalMovingDays / (typeResult[16]*1.0))*100.0) if typeResult[16] else 0.00, 2)
                    jobBedPlan = 0
                    jobBedFact = 0
                    if involutionBeds != 0:
                        jobBedPlan = round(bedDays / float(involutionBeds),  2)
                        jobBedFact = round(movingDays / float(involutionBeds), 2)
                    typeResult[8] = round(totalBedDays / float(typeResult[1] if typeResult[1] else 1), 2)
                    typeResult[9] = round(totalMovingDays / float(typeResult[1] if typeResult[1] else 1), 2)
                    totalResult[8] = round(totalOrgStrBedDays / float(totalResult[1] if totalResult[1] else 1), 2)
                    totalResult[9] = round(totalOrgStrMovingDays / float(totalResult[1] if totalResult[1] else 1), 2)
                    totalCuredClient += curedClient
                    totalDeathClient += deathAll
                    totalOrgStrCuredClient += curedClient
                    avgDurationBedDays =  round((movingDays / float(curedClient)) if curedClient else 0, 2)
                    typeResult[10] = round((totalMovingDays / float(totalCuredClient)) if totalCuredClient else 0, 2)
                    totalResult[10] = round((totalOrgStrMovingDays / float(totalOrgStrCuredClient)) if totalOrgStrCuredClient else 0, 2)
                    rotationBeds =  round((curedClient / float(involutionBeds)) if involutionBeds else 0, 2)
                    totalInvolutionBeds += involutionBeds
                    totalOrgStrInvolutionBeds += involutionBeds
                    typeResult[11] = round((totalCuredClient / float(totalInvolutionBeds)) if totalInvolutionBeds else 0, 2)
                    totalResult[11] = round((totalOrgStrCuredClient / float(totalOrgStrInvolutionBeds)) if totalOrgStrInvolutionBeds else 0, 2)
                    table.setText(rowProfile, 10, jobBedPlan)
                    table.setText(rowProfile, 11, jobBedFact)
                    table.setText(rowProfile, 12, avgDurationBedDays)
                    table.setText(rowProfile, 13, rotationBeds)
                    typeResult[12] = round((totalDeathClient*100)/totalCuredClient if totalDeathClient else 0.00, 2)
                    typeResult[13] += curedClient
                    totalResult[12] += deathPat
                    totalResult[13] += curedClient
                    table.setText(rowProfile, 15, curedClient)
                    involutionDays = self.dataInvolutionDays(orgStructureId, begDateTime, endDateTime, financeList, profileId, dayStat)
                    table.setText(rowProfile, 16, involutionDays)
                    typeResult[14] += involutionDays
                    totalResult[14] += involutionDays
                    countPeriodDays = begDateTime.daysTo(endDateTime)
                    simpleBeds = round(((countPeriodDays - jobBedFact) / rotationBeds) if rotationBeds else 0, 2)
                    typeResult[15] = round(((countPeriodDays - typeResult[9] ) / typeResult[11] ) if typeResult[11]  else 0, 2)
                    totalResult[15] = round(((countPeriodDays - totalResult[9] ) / totalResult[11] ) if totalResult[11]  else 0, 2)
                    table.setText(rowProfile, 17, simpleBeds)
                    countPatronage = self.getCountPatronageList(orgStructureId, begDateTime, endDateTime, noProfileBed, profileId, dayStat=dayStat)
                    typeResult[20] += countPatronage
                    totalResult[20] += countPatronage
                    table.setText(rowProfile, 22, countPatronage)
                    if cnt < lenProfileIdList-1:
                        rowProfile = table.addRow()
                        cnt += 1
                rowProfile = table.addRow()
                table.setText(rowProfile, 1, u'Всего по отделению')
                table.mergeCells(rowProfileOld, 0, rowProfile - rowProfileOld + 1, 1)
                for i, val in enumerate(totalResult):
                    table.setText(rowProfile, i+2, val)
            if totalBool:
                rowProfile = table.addRow()
                table.setText(rowProfile, 0, u'Дневной стационар' if dayStat else u'Стационар')
                table.setText(rowProfile, 1, u'Всего')
                for i, val in enumerate(typeResult):
                    table.setText(rowProfile, i+2, val)
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
    if not isPermanentBed:
        cond.append(tableOSHB['isPermanent'].eq(1))
#    joinOr1 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNull()])
#    joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
#    joinOr3 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDateTime)])
#    joinOr4 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].le(begDateTime), db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].gt(begDateTime)])])
#    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3, joinOr4]))
    cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
    cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
    cond.append(db.joinOr([tableOS['id'].isNull(), tableOS['deleted'].eq(0)]))
    return db.getDistinctIdList(queryTable, cols, cond)


def getMovingTransfer(isPermanentBed, noProfileBed, bedsSchedule, begDateTime, endDateTime, nameProperty, profile = None, transferIn = False, orgStructureIdList = [], boolFIO = False, transferType=0):
    db = QtGui.qApp.db
    tableAPT = db.table('ActionPropertyType')
    tableAP = db.table('ActionProperty')
    tableActionType = db.table('ActionType')
    tableAction = db.table('Action')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')
    tableAPHB = db.table('ActionProperty_HospitalBed')
    tableOS = db.table('OrgStructure')
    tableOSHB = db.table('OrgStructure_HospitalBed')
    tableHBSchedule = db.table('rbHospitalBedShedule')
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
    cond.append(tableAPT['typeName'].like(u'HospitalBed'))
    if orgStructureIdList:
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
    cond.append('''%s'''%(isEXISTSTransfer(nameProperty, namePropertyP=u'Отделение пребывания', transferType=transferType)))
    if not noProfileBed:
        cond.append('OrgStructure_HospitalBed.profile_id IS NOT NULL')
#    if not isPermanentBed:
#        cond.append(tableOSHB['isPermanent'].eq(1))
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
        cond.append(tableOSHB['code'].eq(1))
    elif bedsSchedule == 2:
        cond.append(tableOSHB['code'].ne(1))
#    joinOr1 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNull()])
#    joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
#    joinOr3 = db.joinAnd([tableAction['begDate'].isNull(), tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDateTime)])
#    cond.append(db.joinOr([joinOr1, joinOr2, joinOr3]))
    joinOr1 = tableAction['begDate'].isNull()
    joinOr2 = db.joinAnd([tableAction['begDate'].isNotNull(), tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)])
    cond.append(db.joinOr([joinOr1, joinOr2]))
    if boolFIO:
        stmt = db.selectDistinctStmt(queryTable, u'Client.lastName, Client.firstName, Client.patrName', cond)
        return db.query(stmt)
    else:
        return db.getCount(queryTable, countCol=u'Client.id', where=cond)

