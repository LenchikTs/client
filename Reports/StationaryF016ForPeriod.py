# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate,  QDateTime, QTime

from library.Utils      import forceDate, forceInt, forceRef, forceString
from Events.Utils       import getActionTypeIdListByFlatCode
from Orgs.Utils         import getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import (dateRangeAsStr,
                                getKladrClientRural,
                                getNoPropertyAPHBP,
                                getOrgStructureProperty_HBDS,
                                getPropertyAPHBP,
                                getStringProperty,
                                isEXISTSTransfer,
                                getMovingDays)


from Ui_StationaryF016ForPeriodSetup import Ui_StationaryF016ForPeriodSetupDialog


def getPureHMTime(time):
    return QTime(time.hour(), time.minute())


class CStationaryF016ForPeriodSetupDialog(QtGui.QDialog, Ui_StationaryF016ForPeriodSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', addNone=True, order='code')
        self.edtBegTime.setTime(getPureHMTime(QTime(9, 0, 0, 0)))
        self.edtEndTime.setTime(getPureHMTime(QTime(9, 0, 0, 0)))


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtBegTime.setTime(params.get('begTime', getPureHMTime(QTime(9, 0, 0, 0))))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtEndTime.setTime(params.get('endTime', getPureHMTime(QTime(9, 0, 0, 0))))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbHospitalBedProfile.setValue(params.get('hospitalBedProfileId', None))
        self.chkIsGroupingOS.setChecked(params.get('isGroupingOS', False))
        self.cmbIsTypeOS.setCurrentIndex(params.get('isTypeOS', 0))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['begTime'] = getPureHMTime(self.edtBegTime.time())
        result['endDate'] = self.edtEndDate.date()
        result['endTime'] = getPureHMTime(self.edtEndTime.time())
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['hospitalBedProfileId'] = self.cmbHospitalBedProfile.value()
        result['isGroupingOS'] = self.chkIsGroupingOS.isChecked()
        result['isTypeOS'] = self.cmbIsTypeOS.currentIndex()
        return result


class CStationaryF016ForPeriod(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'СВОДНАЯ ВЕДОМОСТЬ учета движения больных и коечного фонда по стационару, отделению или профилю коек')
        self.stationaryF016ForPeriodSetupDialog = None
        self.clientDeath = 8
        self.begTime = getPureHMTime(QTime(0, 0, 0, 0))
        self.endTime = getPureHMTime(QTime(0, 0, 0, 0))


    def getSetupDialog(self, parent):
        result = CStationaryF016ForPeriodSetupDialog(parent)
        result.setTitle(self.title())
        self.stationaryF016SetupDialog = result
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params):
        description = []
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        endTime = params.get('endTime', getPureHMTime(QTime(9, 0, 0, 0)))
        begTime = params.get('begTime', None)
        endDateTime = QDateTime(endDate, endTime)
        begTime = begTime if begTime else endTime
        begDateTime = QDateTime(begDate, begTime)
        description.append(dateRangeAsStr(u'за период', begDateTime, endDateTime))
        orgStructureId = params.get('orgStructureId', None)
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        if hospitalBedProfileId:
            description.append(u'профиль койки: ' + forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name')))
        isTypeOs = params.get('isTypeOS', 0)
        if isTypeOs:
            description.append(u'стационар: %s'%([u'не задано', u'круглосуточный', u'дневной'][isTypeOs]))
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
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

        profile = params.get('hospitalBedProfileId', None)
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        endTime = params.get('endTime', getPureHMTime(QTime(9, 0, 0, 0)))
        begTime = params.get('begTime', getPureHMTime(QTime(9, 0, 0, 0)))
        endDateTime = QDateTime(endDate, endTime)
        begTime = begTime if begTime else endTime
        begDateTime = QDateTime(begDate, begTime)
        titlePeriod = dateRangeAsStr(u'за период', begDateTime, endDateTime)
        self.begTime = begTime
        self.endTime = endTime
        isGroupingOS = params.get('isGroupingOS', False)
        isType = params.get('isTypeOS', 0)
        begYear = begDate.year()
        endYear = endDate.year()
        yearDateIntDict = {}
        endYear += 1
        for year in range(begYear, endYear):
            if begDateTime.date().year() == year:
                begDateTimeYear = begDateTime
            else:
                begDateTimeYear = QDateTime(QDate(year, 1, 1), getPureHMTime(QTime(9, 0, 0, 0)))
            if endDateTime.date().year() == year:
                endDateTimeYear = endDateTime
            else:
                endDateTimeYear = QDateTime(QDate(year, 12, 1), getPureHMTime(QTime(9, 0, 0, 0)))
            yearDateIntDict[year] = (begDateTimeYear, endDateTimeYear)
        orgStructureIndex = self.stationaryF016SetupDialog.cmbOrgStructure._model.index(self.stationaryF016SetupDialog.cmbOrgStructure.currentIndex(), 0, self.stationaryF016SetupDialog.cmbOrgStructure.rootModelIndex())
        begOrgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'СВОДНАЯ ВЕДОМОСТЬ учета движения больных и коечного фонда по стационару, отделению или профилю коек %s' % (titlePeriod))
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('6%',[u'', u'', u'', u''], CReportBase.AlignLeft),
                ('6%', [u'Число коек в пределах сметы фактически развернутых + свернутых на ремонт на конец отчетного периода', u'', u'', u'', u'1'], CReportBase.AlignRight),
                ('6%', [u'Среднемесячных(годовых) коек', u'', u'', u'', u'2'], CReportBase.AlignRight),
                ('6%', [u'Состояло больных на начало отчетного периода', u'', u'', u'', u'3'], CReportBase.AlignRight),
                ('6%', [u'За отчетный период', u'поступило больных', u'всего', u'', u'4'], CReportBase.AlignRight),
                ('6%', [u'', u'', u'Из них', u'Сельских жителей', u'5'], CReportBase.AlignRight),
                ('6%', [u'', u'', u'', u'Детей в возрасте до 17 лет включительно', u'6'], CReportBase.AlignRight),
                ('6%', [u'', u'Переведено больных внутри больницы', u'из других отделений', u'', u'7'], CReportBase.AlignRight),
                ('6%', [u'', u'', u'в другие отделения', u'', u'8'], CReportBase.AlignRight),
                ('6%', [u'', u'Выписано больных', u'Всего', u'', u'9'], CReportBase.AlignRight),
                ('6%', [u'', u'', u'в т.ч. переведено в другие стационары', u'', u'10'], CReportBase.AlignRight),
                ('6%', [u'', u'Умерло', u'', u'', u'11'], CReportBase.AlignRight),
                ('6%', [u'Состояло больных на конец отчетного периода', u'', u'', u'', u'12'], CReportBase.AlignRight),
                ('6%', [u'Проведено всеми больными койко-дней', u'', u'', u'', u'13'], CReportBase.AlignRight),
                ('6%', [u'В т.ч. сельскими жителями', u'', u'', u'', u'14'], CReportBase.AlignRight),
                ('6%', [u'Число койко-дней закрытия', u'', u'', u'', u'15'], CReportBase.AlignRight),
                ('6%', [u'Кроме того, проведено койко-дней матерями при больных детях', u'', u'', u'', u'16'], CReportBase.AlignRight)
               ]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 4, 1) # 1
        table.mergeCells(0, 1, 4, 1) # Число коек
        table.mergeCells(0, 2, 4, 1) # Среднемесячных(годовых) коек
        table.mergeCells(0, 3, 4, 1) # Состояло больных на начало отчетного периода
        table.mergeCells(0, 4, 1, 8) # За отчетный период
        table.mergeCells(1, 4, 1, 3) # поступило больных
        table.mergeCells(2, 4, 2, 1) # Всего
        table.mergeCells(2, 5, 1, 2) # Из них
        table.mergeCells(1, 7, 1, 2) # Переведено больных внутри больницы
        table.mergeCells(2, 7, 2, 1) # из других отделений
        table.mergeCells(2, 8, 2, 1) # в другие отделения
        table.mergeCells(1, 9, 1, 2) # Выписано больных
        table.mergeCells(2, 9, 2, 1) # Всего
        table.mergeCells(2, 10, 2, 1) # в т.ч. переведено в другие стационары
        table.mergeCells(1, 11, 3, 1) # Умерло
        table.mergeCells(0, 12, 4, 1) # Состояло больных на конец отчетного периода
        table.mergeCells(0, 13, 4, 1) # Проведено всеми больными койко-дней
        table.mergeCells(0, 14, 4, 1) # В т.ч. сельскими жителями
        table.mergeCells(0, 15, 4, 1) # Число койко-дней закрытия
        table.mergeCells(0, 16, 4, 1) # Кроме того, проведено койко-дней матерями при больных детях

        def unrolledHospitalBed(endDate, orgStructureIdList, profile = None, type=0):
            countBeds = 0
            if type == 1:
                isTypeOS = u'OrgStructure.type != 0'
            elif type == 2:
                isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
            else:
                isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
            bedType = db.translate('rbHospitalBedType', 'name', u'профильная', 'id')
            cond = []
            cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
            cond.append(tableVHospitalBed['type_id'].eq(bedType))
            cond.append(tableVHospitalBed['isPermanent'].eq('1'))
            if profile:
               cond.append(tableVHospitalBed['profile_id'].eq(profile))
            joinOr1 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].le(endDate)])
            joinOr2 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(endDate)])
            table = tableVHospitalBed.innerJoin(tableOS, tableOS['id'].eq(tableVHospitalBed['master_id']))
            cond.append(db.joinAnd([joinOr1, joinOr2]))
            cond.append(isTypeOS)
            countBeds = db.getCount(table, countCol='vHospitalBed.id', where=cond)
            return countBeds

        def unrolledHospitalBedsMonth(row, monthEnd, orgStructureIdList, profile = None, type=0):
            monthEndDate = QDate(yearDateInt, monthEnd, 1)
            endDate = QDate(yearDateInt, monthEnd, monthEndDate.daysInMonth())
            countBedsMonth = unrolledHospitalBed(endDate, orgStructureIdList, profile, type=type)
            table.setText(row, 1, countBedsMonth)
            return countBedsMonth

        def getMovingPresent(begDateTime, endDateTime, orgStructureIdList, endTime, profile = None, flagCurrent = False, type=0):
            cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('moving%')),
                     tableAction['deleted'].eq(0),
                     tableEvent['deleted'].eq(0),
                     tableAP['deleted'].eq(0),
                     tableActionType['deleted'].eq(0),
                     tableClient['deleted'].eq(0),
                     tableAP['action_id'].eq(tableAction['id'])
                   ]
            if type == 1:
                isTypeOS = u'OrgStructure.type != 0'
            elif type == 2:
                isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
            else:
                isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
            queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
            queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
            queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
            queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
            queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
            queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
            cond.append(tableOS['deleted'].eq(0))
            cond.append(isTypeOS)
            cond.append(tableAPT['typeName'].like('HospitalBed'))
            if orgStructureIdList:
                cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
            #cond.append('''NOT %s'''%(getTransferPropertyIn(u'Переведен из отделения'))) #??????????
            if profile:
                cond.append(tableOSHB['profile_id'].eq(profile))
            if flagCurrent:
                #endDateTime = QDateTime(endDate, endTime)
                cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(endDateTime)]))
                cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(endDateTime)]))
                stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll', where=cond)
                query = db.query(stmt)
                if query.first():
                    record = query.record()
                    return forceInt(record.value('countAll'))
                else:
                    return 0
            else:
                #begDateTime = QDateTime(begDate.addDays(-1), endTime)
                #begDateTime = QDateTime(begDate, endTime)
                cond.append(db.joinOr([tableAction['begDate'].isNull(), tableAction['begDate'].lt(begDateTime)]))
                cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].ge(begDateTime)]))
                return db.getCount(queryTable, countCol='Client.id', where=cond)

        def getMovingTransfer(begDateTime, endDateTime, orgStructureIdList, nameProperty, profile = None, transferIn = False, type=0, transferType=0):
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
            queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
            cond.append(tableOS['deleted'].eq(0))
            if type == 1:
                isTypeOS = u'OrgStructure.type != 0'
            elif type == 2:
                isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
            else:
                isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
            cond.append(isTypeOS)
            cond.append(tableAPT['typeName'].like(u'HospitalBed'))
            if orgStructureIdList:
                cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
            cond.append('''%s'''%(isEXISTSTransfer(nameProperty, namePropertyP=u'Отделение пребывания', transferType=transferType)))
            if profile:
                cond.append(tableOSHB['profile_id'].eq(profile))
#            cond.append(db.joinAnd([tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)]))
            return db.getCount(queryTable, countCol=u'Client.id', where=cond)

        def getReceived(begDateTime, endDateTime, orgStructureIdList, nameProperty = u'Переведен из отделения', profile = None, noPropertyProfile = False, type = 0):
            cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('received%')),
                     tableAction['deleted'].eq(0),
                     tableEvent['deleted'].eq(0),
#                     tableAP['deleted'].eq(0),
                     tableActionType['deleted'].eq(0),
                     tableClient['deleted'].eq(0)
#                     tableAP['action_id'].eq(tableAction['id']),
#                     #tableAction['endDate'].isNotNull(),
#                     tableAction['begDate'].isNotNull(),
#                     tableOS['type'].ne(0),
#                     tableOS['deleted'].eq(0),
#                     tableAPT['name'].like(u'Направлен в отделение')
                   ]
#            if orgStructureIdList:
#                cond.append(tableOS['id'].inlist(orgStructureIdList))
            queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
#            queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
#            queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
#            queryTable = queryTable.innerJoin(tableAPOS, tableAPOS['id'].eq(tableAP['id']))
#            queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableAPOS['value']))
            if noPropertyProfile:
                cond.append('''%s'''%(getNoPropertyAPHBP()))
            elif profile:
                cond.append('''%s'''%(getPropertyAPHBP([profile], True)))
            cond.append('''%s'''%(getOrgStructureProperty_HBDS(u'Направлен в отделение', orgStructureIdList, type)))
            #cond.append('''%s'''%(getDataAPHBnoProperty(False, nameProperty, False, [profile] if profile else [], u'', u'Отделение пребывания', orgStructureIdList)))
            cond.append(db.joinAnd([tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)]))
#            cond.append(tableAction['begDate'].ge(begDateTime))
#            cond.append(tableAction['begDate'].le(endDateTime))
            ageStmt = '''EXISTS(SELECT A.id
FROM Action AS A
INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
INNER JOIN Event AS E ON A.event_id=E.id
INNER JOIN Client AS C ON E.client_id=C.id
WHERE A.deleted = 0 AND Action.id IS NOT NULL AND A.id = Action.id AND (age(C.birthDate, A.begDate)) <= 17)'''
            stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS childrenCount, SUM(%s) AS clientRural'%(ageStmt, getKladrClientRural()), where=cond)
            query = db.query(stmt)
            if query.first():
                record = query.record()
                return [forceInt(record.value('countAll')), forceInt(record.value('childrenCount')), forceInt(record.value('clientRural'))]
            else:
                return [0, 0, 0]


        def getLeaved(begDateTime, endDateTime, orgStructureIdList, nameProperty = u'Переведен в отделение', profile = None, noPropertyProfile = False, type = 0):
            tableEventType = db.table('EventType')
            tableMedicalAidType = db.table('rbMedicalAidType')
            cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
                     tableAction['deleted'].eq(0),
                     tableEvent['deleted'].eq(0),
                     tableActionType['deleted'].eq(0),
                     tableClient['deleted'].eq(0),
                     #tableAction['begDate'].isNotNull(),
                     tableAction['endDate'].isNotNull()
                   ]
            queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
            queryTable = queryTable.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
            queryTable = queryTable.innerJoin(tableMedicalAidType, tableEventType['medicalAidType_id'].eq(tableMedicalAidType['id']))
            cond.append(tableMedicalAidType['code'].inlist(('1', '2', '3', '7')))
            if orgStructureIdList:
                cond.append(getOrgStructureProperty_HBDS(u'Отделение', orgStructureIdList, type))
            if noPropertyProfile:
                cond.append(getNoPropertyAPHBP())
            elif profile:
                cond.append(getPropertyAPHBP([profile], True))
#            else:
#                cond.append('''%s'''%(getPropertyAPHBP([profile], True)))
            cond.append(tableAction['endDate'].ge(begDateTime))
            cond.append(tableAction['endDate'].le(endDateTime))
            stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer'%(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'), getStringProperty(u'Исход госпитализации', u'(APS.value = \'переведен в другой стационар\')')), where=cond)
            query = db.query(stmt)
            if query.first():
                record = query.record()
                countAll = forceInt(record.value('countAll'))
                countDeath = forceInt(record.value('countDeath'))
                countTransfer = forceInt(record.value('countTransfer'))
                return [countAll - countDeath, countDeath, countTransfer]
            else:
                return [0, 0, 0]

        def columnFill(begDate, endDate, parentOrgStructureIdList, profile, row, endTime, type=0):
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, row, type=type)
            movingPresentBeg = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, type=type)
            #self.movingsPresentBeg += movingPresentBeg
            table.setText(row, 3, movingPresentBeg)
            all, children, clientRural = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type)
            table.setText(row, 4, all)
            table.setText(row, 5, clientRural)
            table.setText(row, 6, children)
            table.setText(row, 7, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type, transferType=1))
            table.setText(row, 8, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, type=type, transferType=0))
            countLeavedAll, leavedDeath, leavedTransfer = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile, type=type)
            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile, True, type=type)
            table.setText(row, 9, countLeavedAll + countLeavedAllNoProfile)
            table.setText(row, 11, leavedDeath + leavedDeathNoProfile)
            table.setText(row, 10, leavedTransfer + leavedTransferNoProfile)
            movingPresentEnd = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True, type=type)
            #self.movingsPresentEnd += movingPresentEnd
            table.setText(row, 12, movingPresentEnd)
            table.setText(row, 13, self.dataMovingDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))
            table.setText(row, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile, type=type))
            table.setText(row, 16, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile, type=type))
            table.setText(row, 15, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))

        currentDate = QDate.currentDate()
        currentDateYear = currentDate.year()
        precedentDateMonth = currentDate.month() - 1
        def getDataReport(parentOrgStructureIdList, rowProfile, profile, type=0):
            self.movingsPresentBeg = 0
            self.movingsPresentEnd = 0
            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 1):
                table.setText(rowProfile, 0, u'Январь')
                unrolledHospitalBedsMonth(rowProfile, 1, parentOrgStructureIdList, profile, type=type)#Число коек на конец отчетного периода - Это как общее колво за весь период или наличие коек на последний день? Как за полугодие и за год?????????????????????????????????????
                begDate, endDate = self.createBegEndDate(1, 1, yearDateInt)
                self.movingsPresentBeg = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 2):
                table.setText(rowProfile, 0, u'Февраль')
                unrolledHospitalBedsMonth(rowProfile, 2, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(2, 2, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 3):
                table.setText(rowProfile, 0, u'Март')
                unrolledHospitalBedsMonth(rowProfile, 3, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(3, 3, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 4):
                table.setText(rowProfile, 0, u'Апрель')
                unrolledHospitalBedsMonth(rowProfile, 4, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(4, 4, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 5):
                table.setText(rowProfile, 0, u'Май')
                unrolledHospitalBedsMonth(rowProfile, 5, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(5, 5, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 6):
                table.setText(rowProfile, 0, u'Июнь')
                unrolledHospitalBedsMonth(rowProfile, 6, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(6, 6, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            table.setText(rowProfile, 0, u'За полугодие')
            unrolledHospitalBedsMonth(rowProfile, 6, parentOrgStructureIdList, profile, type=type)
            begDate, endDate = self.createBegEndDate(1, precedentDateMonth if (precedentDateMonth <= 6 and yearDateInt == currentDateYear) else 6, yearDateInt)
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, rowProfile, None, 6, type=type)
            table.setText(rowProfile, 3, self.movingsPresentBeg)
            all, children, clientRural = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type)
            table.setText(rowProfile, 4, all)
            table.setText(rowProfile, 5, clientRural)
            table.setText(rowProfile, 6, children)
            table.setText(rowProfile, 7, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type, transferType=1))
            table.setText(rowProfile, 8, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, type=type, transferType=0))
            countLeavedAll, leavedDeath, leavedTransfer = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile, type=type)
            table.setText(rowProfile, 9, countLeavedAll)
            table.setText(rowProfile, 11, leavedDeath)
            table.setText(rowProfile, 10, leavedTransfer)
            #table.setText(rowProfile, 12, self.movingsPresentEnd)
            table.setText(rowProfile, 12, getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True, type=type))
            table.setText(rowProfile, 13, self.dataMovingDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))
            table.setText(rowProfile, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile, type=type))
            table.setText(rowProfile, 16, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile, type=type))
            table.setText(rowProfile, 15, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))
            rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 7):
                table.setText(rowProfile, 0, u'Июль')
                unrolledHospitalBedsMonth(rowProfile, 7, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(7, 7, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 8):
                table.setText(rowProfile, 0, u'Август')
                unrolledHospitalBedsMonth(rowProfile, 8, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(8, 8, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 9):
                table.setText(rowProfile, 0, u'Сентябрь')
                unrolledHospitalBedsMonth(rowProfile, 9, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(9, 9, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 10):
                table.setText(rowProfile, 0, u'Октябрь')
                unrolledHospitalBedsMonth(rowProfile, 10, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(10, 10, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 11):
                table.setText(rowProfile, 0, u'Ноябрь')
                unrolledHospitalBedsMonth(rowProfile, 11, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(11, 11, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 12):
                table.setText(rowProfile, 0, u'Декабрь')
                unrolledHospitalBedsMonth(rowProfile, 12, parentOrgStructureIdList, profile, type=type)
                begDate, endDate = self.createBegEndDate(12, 12, yearDateInt)
                self.movingsPresentEnd = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True, type=type)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime, type=type)
                rowProfile = table.addRow()

            table.setText(rowProfile, 0, u'За год')
            unrolledHospitalBedsMonth(rowProfile, 12, parentOrgStructureIdList, profile, type=type)
            begDate, endDate = self.createBegEndDate(1, 12, yearDateInt)
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, rowProfile, None, 12, type=type)
            begDate, endDate = self.createBegEndDate(1, precedentDateMonth if (yearDateInt == currentDateYear) else 12, yearDateInt)
            table.setText(rowProfile, 3, self.movingsPresentBeg)
            all, children, clientRural = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type)
            table.setText(rowProfile, 4, all)
            table.setText(rowProfile, 5, clientRural)
            table.setText(rowProfile, 6, children)
            table.setText(rowProfile, 7, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, type=type, transferType=1))
            table.setText(rowProfile, 8, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, type=type, transferType=0))
            countLeavedAll, leavedDeath, leavedTransfer = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile, type=type)
            table.setText(rowProfile, 9, countLeavedAll)
            table.setText(rowProfile, 11, leavedDeath)
            table.setText(rowProfile, 10, leavedTransfer)
            #table.setText(rowProfile, 12, self.movingsPresentEnd)
            table.setText(rowProfile, 12, getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True, type=type))
            table.setText(rowProfile, 13, self.dataMovingDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))
            table.setText(rowProfile, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile, type=type))
            table.setText(rowProfile, 16, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile, type=type))
            table.setText(rowProfile, 15, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile, type=type))
            #rowProfile = table.addRow()
            return rowProfile

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        def getOrgStructureParent(orgStructureIdList, rowProfile, table, profile, isPrimary, type=0):
            if type == 1:
                isTypeOS = u'OrgStructure.type != 0'
            elif type == 2:
                isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
            else:
                isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
            for parentOrgStructureId in orgStructureIdList:
                tableQuery = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
                recordEx = db.getRecordEx(tableQuery,
                                          [tableOS['name'], tableOS['id']],
                                          [tableOS['deleted'].eq(0),
                                           tableOS['id'].eq(parentOrgStructureId),
                                           isTypeOS
                                           ])
                if recordEx:
                    name = forceString(recordEx.value('name'))
                    if isPrimary:
                        isPrimary = False
                    else:
                        rowProfile = table.addRow()
                    table.setText(rowProfile, 0, name, boldChars)
                    rowProfile = table.addRow()
                    rowProfile = getDataReport([parentOrgStructureId], rowProfile, profile, type)
                    records = db.getRecordList(tableQuery,
                                               [tableOS['id'], tableOS['name']],
                                               [tableOS['deleted'].eq(0), tableOS['type'].ne(0),
                                                tableOS['parent_id'].eq(parentOrgStructureId),
                                                isTypeOS])
                    for record in records:
                        name = forceString(record.value('name'))
                        orgStructureId = forceRef(record.value('id'))
                        table.setText(rowProfile, 0, name, boldChars)
                        rowProfile = table.addRow()
                        rowProfile = getDataReport([orgStructureId], rowProfile, profile, type)
            return rowProfile
        nextRow = table.addRow()
        isNextRow = False
        yearDateKeys = yearDateIntDict.keys()
        yearDateKeys.sort()
        if isGroupingOS:
            for yearDateInt in yearDateKeys:
                begDateTime, endDateTime = yearDateIntDict.get(yearDateInt, (None, None))
                if isNextRow:
                    nextRow = table.addRow()
                else:
                    isNextRow = True
                table.setText(nextRow, 0, yearDateInt, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                table.mergeCells(nextRow, 0, 1, len(cols))
                nextRow = table.addRow()
                nextRow = getOrgStructureParent(begOrgStructureIdList, nextRow, table, profile, True, isType)
        else:
            for yearDateInt in yearDateKeys:
                begDateTime, endDateTime = yearDateIntDict.get(yearDateInt, (None, None))
                if isNextRow:
                    nextRow = table.addRow()
                else:
                    isNextRow = True
                table.setText(nextRow, 0, yearDateInt, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                table.mergeCells(nextRow, 0, 1, len(cols))
                nextRow = table.addRow()
                nextRow = getDataReport(begOrgStructureIdList, nextRow, profile, isType)
        return doc


    def createBegEndDate(self, monthBeg, monthEnd, yearDateInt):
        if monthBeg > 1:
            begDate = QDateTime(QDate(yearDateInt, monthBeg, 1), self.begTime)
        else:
            begDate = QDateTime(QDate(yearDateInt, monthBeg, 1), getPureHMTime(QTime(0, 0, 0, 0)))
        if monthEnd < 12:
            endDate = QDateTime(QDate(yearDateInt, monthEnd + 1, 1), self.endTime)
        else:
            endDate = QDateTime(QDate(yearDateInt + 1, 1, 1), getPureHMTime(QTime(0, 0, 0, 0)))
        return begDate, endDate


    def averageYarHospitalBed(self, orgStructureIdList, table, begDate, endDate, profile = None, row = None, isHospital = None, countMonths = None, type=0):
        days = 0
        daysMonths = 0
        begDatePeriod = begDate.date()
        endDatePeriod = begDatePeriod.addMonths(1)
        while endDatePeriod <= endDate.date():
            days = self.averageDaysHospitalBed(orgStructureIdList, begDatePeriod, endDatePeriod, profile, isHospital, type=type)
            daysMonths += days / (begDatePeriod.daysInMonth())
            begDatePeriod = begDatePeriod.addMonths(1)
            endDatePeriod = endDatePeriod.addMonths(1)
        if countMonths == 12:
            daysMonths = forceInt(round(daysMonths / 12.0))
        elif countMonths == 6:
            daysMonths = forceInt(round(daysMonths / 6.0))
        if profile:
           table.setText(row, 2, daysMonths)
        else:
            table.setText(row, 2, daysMonths)


    def averageDaysHospitalBed(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None, type = 0):
        days = 0
        db = QtGui.qApp.db
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableOrg = db.table('Organisation')
        tableOS = db.table('OrgStructure')
        queryTable = tableOSHB.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        queryTable = queryTable.innerJoin(tableOrg, tableOrg['id'].eq(tableOS['organisation_id']))
        bedType = db.translate('rbHospitalBedType', 'name', u'профильная', 'id')
        if type == 1:
            isTypeOS = u'OrgStructure.type != 0'
        elif type == 2:
            isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
        else:
            isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
        cond = [tableOSHB['master_id'].inlist(orgStructureIdList),
                tableOrg['deleted'].eq(0),
                tableOS['deleted'].eq(0),
                isTypeOS,
                tableOSHB['type_id'].eq(bedType),
                tableOSHB['isPermanent'].eq('1')
                ]
        if isHospital is not None:
           cond.append(tableOrg['isHospital'].eq(isHospital))
        joinAnd = db.joinAnd([tableOSHB['endDate'].isNull(), db.joinOr([db.joinAnd([tableOSHB['begDate'].isNotNull(), tableOSHB['begDate'].lt(endDatePeriod)]), tableOSHB['begDate'].isNull()])])
        cond.append(db.joinOr([db.joinAnd([tableOSHB['endDate'].isNotNull(), tableOSHB['endDate'].gt(begDatePeriod), tableOSHB['begDate'].isNotNull(), tableOSHB['begDate'].lt(endDatePeriod)]), joinAnd]))
        if profile:
           cond.append(tableOSHB['profile_id'].eq(profile))
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


    def dataMovingDays(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None, type=0):
        if type == 1:
            isTypeOS = u'OrgStructure.type != 0'
        elif type == 2:
            isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
        else:
            isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
        return getMovingDays(orgStructureIdList, begDatePeriod, endDatePeriod, profile, isHospital, additionalCond=isTypeOS)


    def dataInvolutionDays(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None, type=0):
        days = 0
        db = QtGui.qApp.db
        tableVHospitalBed = db.table('vHospitalBed')
        tableOS = db.table('OrgStructure')
        tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
        queryTable = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
        queryTable = queryTable.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id']))
        if type == 1:
            isTypeOS = u'OrgStructure.type != 0'
        elif type == 2:
            isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
        else:
            isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
        condRepairs = [isTypeOS,
                       tableOS['deleted'].eq(0),
                       tableVHospitalBed['master_id'].inlist(orgStructureIdList)]
        if profile:
            condRepairs.append(tableVHospitalBed['profile_id'].eq(profile))
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


    def dataPatronageOrClientRuralDays(self, begDatePeriod, endDatePeriod, orgStructureIdList, propertyPatronage, profile = None, type=0):
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
        if type == 1:
            isTypeOS = u'OrgStructure.type != 0'
        elif type == 2:
            isTypeOS = u'(OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1)'
        else:
            isTypeOS = u'(OrgStructure.type != 0 OR (OrgStructure.type = 0 AND (SELECT getOrgStructureIsType(OrgStructure.id)) = 1))'
        queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
        queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
        queryTable = queryTable.innerJoin(tableOSHB, tableOSHB['id'].eq(tableAPHB['value']))
        queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        cond.append(isTypeOS)
        cond.append(tableOS['deleted'].eq(0))
        cond.append(tableAPT['typeName'].like('HospitalBed'))
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))

        joinAnd = db.joinAnd([tableAction['endDate'].isNull(), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod)])
        cond.append(db.joinOr([db.joinAnd([tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDatePeriod), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod)]), joinAnd]))
        if propertyPatronage:
            cond.append(getStringProperty(u'Патронаж%', u'(APS.value = \'Да\')'))
        else:
            cond.append(getKladrClientRural())
        if profile:
            cond.append(tableOSHB['profile_id'].eq(profile))
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
        return days
