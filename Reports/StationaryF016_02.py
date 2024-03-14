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
from PyQt4.QtCore import Qt, QDate, QDateTime, QTime

from library.Utils      import forceDate, forceInt, forceRef, forceString

from Events.Utils       import getActionTypeIdListByFlatCode
from Orgs.Utils         import getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import (getKladrClientRural,
                                getNoPropertyAPHBP,
                                getOrgStructureProperty,
                                getPropertyAPHBP,
                                getStringProperty,
                                isEXISTSTransfer,
                                getMovingDays)

from Reports.Ui_StationaryF016Setup import Ui_StationaryF016SetupDialog


class CStationaryF016_02SetupDialog(QtGui.QDialog, Ui_StationaryF016SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', addNone=True, order='code')
        self.edtTimeEdit.setTime(QTime(9, 0, 0, 0))


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtYear.setText(params.get('Year', ''))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbHospitalBedProfile.setValue(params.get('hospitalBedProfileId', None))
        self.chkIsGroupingOS.setChecked(params.get('isGroupingOS', False))
        self.edtTimeEdit.setTime(params.get('endTime', QTime(9, 0, 0, 0)))


    def params(self):
        result = {}
        result['Year'] = forceString(self.edtYear.text())
        result['endTime'] = self.edtTimeEdit.time()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['hospitalBedProfileId'] = self.cmbHospitalBedProfile.value()
        result['isGroupingOS'] = self.chkIsGroupingOS.isChecked()
        return result


class CStationaryF016_02(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'СВОДНАЯ ВЕДОМОСТЬ учета движения больных и коечного фонда по стационару, отделению или профилю коек')
        self.stationaryF016_02SetupDialog = None
        self.clientDeath = 8
        self.endTime = QTime(0, 0, 0, 0)


    def getSetupDialog(self, parent):
        result = CStationaryF016_02SetupDialog(parent)
        result.setTitle(self.title())
        self.stationaryF016_02SetupDialog = result
        return result


    def getOrgStructureIdList(self, treeIndex):
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def dumpParams(self, cursor, params):
        description = []
        orgStructureId = params.get('orgStructureId', None)
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')

        endTime = params.get('endTime', QTime(9, 0, 0, 0))
        description.append(u'Время начала периода: ' + forceString(endTime))
        if hospitalBedProfileId:
            description.append(u'профиль койки: ' + forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name')))
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
        yearDate = params.get('Year', '')
        endTime = params.get('endTime', QTime(9, 0, 0, 0))
        self.endTime = endTime
        isGroupingOS = params.get('isGroupingOS', False)
        yearDateInt = forceInt(yearDate)
        orgStructureIndex = self.stationaryF016_02SetupDialog.cmbOrgStructure._model.index(self.stationaryF016_02SetupDialog.cmbOrgStructure.currentIndex(), 0, self.stationaryF016_02SetupDialog.cmbOrgStructure.rootModelIndex())
        begOrgStructureIdList = self.getOrgStructureIdList(orgStructureIndex)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'СВОДНАЯ ВЕДОМОСТЬ учета движения больных и коечного фонда по стационару, отделению или профилю коек за %s год' % (yearDate))
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('5%',[u'', u'', u'', u''], CReportBase.AlignLeft),
                ('5%', [u'Число коек в пределах сметы', u'фактически развернутых', u'', u'', u'1'], CReportBase.AlignRight),
                ('5%', [u'', u'свернутых на ремонт на конец отчетного периода', u'', u'', u'2'], CReportBase.AlignRight),
                ('5%', [u'Среднемесячных(годовых) коек', u'', u'', u'', u'3'], CReportBase.AlignRight),
                ('5%', [u'Состояло больных на начало отчетного периода', u'', u'', u'', u'4'], CReportBase.AlignRight),
                ('5%', [u'За отчетный период', u'поступило больных', u'всего', u'', u'5'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'в т.ч. из дневных стационаров', u'', u'6'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'из них', u'Сельских жителей', u'7'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'0 - 17 лет включительно', u'8'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'60 лет и старше', u'9'], CReportBase.AlignRight),
                ('5%', [u'', u'Переведено больных внутри больницы', u'из других отделений', u'', u'10'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'в другие отделения', u'', u'11'], CReportBase.AlignRight),
                ('5%', [u'', u'Выписано больных', u'Всего', u'', u'12'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'в дневной стационар', u'', u'13'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'в круглосуточный стационар', u'', u'14'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'в т.ч. переведено в другие стационары', u'', u'15'], CReportBase.AlignRight),
                ('5%', [u'', u'Умерло', u'', u'', u'16'], CReportBase.AlignRight),
                ('5%', [u'Состояло больных на конец отчетного периода', u'', u'', u'', u'17'], CReportBase.AlignRight),
                ('5%', [u'Проведено больными койко-дней', u'', u'', u'', u'18'], CReportBase.AlignRight),
                ('5%', [u'Кроме того', u'число койко-дней закрытия', u'', u'', u'19'], CReportBase.AlignRight),
                ('5%', [u'', u'проведено койко-дней по уходу ', u'', u'', u'20'], CReportBase.AlignRight)
               ]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 4, 1) # 1
        table.mergeCells(0, 1, 1, 2)
        table.mergeCells(1, 1, 3, 1)
        table.mergeCells(1, 2, 3, 1)
        table.mergeCells(0, 3, 4, 1)
        table.mergeCells(0, 4, 4, 1)
        table.mergeCells(0, 5, 1, 12)
        table.mergeCells(1, 5, 1, 5)
        table.mergeCells(2, 5, 2, 1)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(2, 7, 1, 3)
        table.mergeCells(1, 10, 1, 2)
        table.mergeCells(2, 10, 2, 1)
        table.mergeCells(2, 11, 2, 1)
        table.mergeCells(1, 12, 1, 4)
        table.mergeCells(2, 12, 2, 1)
        table.mergeCells(2, 13, 2, 1)
        table.mergeCells(2, 14, 2, 1)
        table.mergeCells(2, 15, 2, 1)
        table.mergeCells(1, 16, 3, 1)
        table.mergeCells(0, 17, 4, 1)
        table.mergeCells(0, 18, 4, 1)
        table.mergeCells(0, 19, 1, 2)
        table.mergeCells(1, 19, 3, 1)
        table.mergeCells(1, 20, 3, 1)

        def unrolledHospitalBed(endDate, orgStructureIdList, profile = None):
            tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
            table = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
            countBeds = 0
            countBedsRepairs = 0
            condRepairs = ['''OrgStructure_HospitalBed_Involution.involutionType != 0
                                   AND (OrgStructure_HospitalBed_Involution.begDate IS NULL
                                   OR OrgStructure_HospitalBed_Involution. endDate IS NULL
                                   OR (OrgStructure_HospitalBed_Involution.begDate >= '%s'
                                   AND OrgStructure_HospitalBed_Involution. endDate <= '%s'))'''%(endDate.toString(Qt.ISODate), endDate.toString(Qt.ISODate))]
            condRepairs.append(tableOS['type'].eq(1))
            condRepairs.append(tableOS['deleted'].eq(0))
            condRepairs.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
            bedType = db.translate('rbHospitalBedType', 'name', u'профильная', 'id')
            cond = []
            cond.append(tableVHospitalBed['master_id'].inlist(orgStructureIdList))
            cond.append(tableVHospitalBed['type_id'].eq(bedType))
            cond.append(tableVHospitalBed['isPermanent'].eq('1'))
            if profile:
               cond.append(tableVHospitalBed['profile_id'].eq(profile))
            joinOr1 = db.joinOr([tableVHospitalBed['begDate'].isNull(), tableVHospitalBed['begDate'].le(endDate)])
            joinOr2 = db.joinOr([tableVHospitalBed['endDate'].isNull(), tableVHospitalBed['endDate'].ge(endDate)])
            cond.append(db.joinAnd([joinOr1, joinOr2]))
            table = tableVHospitalBed.innerJoin(tableOS, tableOS['id'].eq(tableVHospitalBed['master_id']))
            cond.append(tableOS['deleted'].eq(0))
            cond.append(tableOS['type'].eq(1))
            countBeds = db.getCount(table, countCol='vHospitalBed.id', where=cond)
            countBedsRepairs = db.getCount(table.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id'])), countCol='vHospitalBed.id', where=condRepairs)
            return countBeds, countBedsRepairs

        def unrolledHospitalBedsMonth(row, monthEnd, orgStructureIdList, profile = None):
            monthEndDate = QDate(yearDateInt, monthEnd, 1)
            endDate = QDate(yearDateInt, monthEnd, monthEndDate.daysInMonth())
            countBedsMonth, countBedsRepairs = unrolledHospitalBed(endDate, orgStructureIdList, profile)
            table.setText(row, 1, countBedsMonth) #!
            table.setText(row, 2, countBedsRepairs)#!
            return countBedsMonth

        def getMovingPresent(begDateTime, endDateTime, orgStructureIdList, endTime, profile = None, flagCurrent = False):
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

        def getMovingTransfer(begDateTime, endDateTime, orgStructureIdList, nameProperty, profile = None, transferIn = False, transferType=0):
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
            cond.append(tableOS['type'].ne(0))
            cond.append(tableAPT['typeName'].like(u'HospitalBed'))
            if orgStructureIdList:
                cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
            cond.append(isEXISTSTransfer(nameProperty, namePropertyP=u'Отделение пребывания', transferType=transferType))
            if profile:
                cond.append(tableOSHB['profile_id'].eq(profile))
            return db.getCount(queryTable, countCol=u'Client.id', where=cond)

        def getReceived(begDateTime, endDateTime, orgStructureIdList, nameProperty = u'Переведен из отделения', profile = None, noPropertyProfile = False):
            cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('received%')),
                     tableAction['deleted'].eq(0),
                     tableEvent['deleted'].eq(0),
                     tableActionType['deleted'].eq(0),
                     tableClient['deleted'].eq(0)
                   ]
            queryTable = tableActionType.innerJoin(tableAction, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
            if noPropertyProfile:
                cond.append(getNoPropertyAPHBP())
            elif profile:
                cond.append(getPropertyAPHBP([profile], True))
            cond.append(getOrgStructureProperty(u'Направлен в отделение', orgStructureIdList))
            cond.append(db.joinAnd([tableAction['begDate'].ge(begDateTime), tableAction['begDate'].lt(endDateTime)]))
            ageChildrenStmt = '''EXISTS(SELECT A.id
FROM Action AS A
INNER JOIN ActionType AS AT ON AT.id=A.actionType_id
INNER JOIN Event AS E ON A.event_id=E.id
INNER JOIN Client AS C ON E.client_id=C.id
WHERE A.deleted = 0 AND Action.id IS NOT NULL AND A.id = Action.id AND (age(C.birthDate, A.begDate)) <= 17)'''
            ageAdultStmt = '''EXISTS(SELECT A.id
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
            stmt = db.selectStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS childrenCount, SUM(%s) AS clientRural, SUM(%s) AS isStationaryDay, SUM(%s) AS ageAdultStmt'%(ageChildrenStmt, getKladrClientRural(), isStationaryDay, ageAdultStmt), where=cond)
            query = db.query(stmt)
            if query.first():
                record = query.record()
                return [forceInt(record.value('countAll')), forceInt(record.value('childrenCount')), forceInt(record.value('clientRural')), forceInt(record.value('isStationaryDay')), forceInt(record.value('ageAdultStmt'))]
            else:
                return [0, 0, 0, 0, 0]


        def getLeaved(begDateTime, endDateTime, orgStructureIdList, nameProperty = u'Переведен в отделение', profile = None, noPropertyProfile = False):
            tableEventType = db.table('EventType')
            cond = [ tableAction['actionType_id'].inlist(getActionTypeIdListByFlatCode('leaved%')),
                     tableAction['deleted'].eq(0),
                     tableEvent['deleted'].eq(0),
                     tableActionType['deleted'].eq(0),
                     tableClient['deleted'].eq(0),
                     tableAction['endDate'].isNotNull()
                   ]
            queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
            queryTable = queryTable.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
            cond.append(u'''(EventType.medicalAidType_id IN (SELECT rbMedicalAidType.id from rbMedicalAidType where rbMedicalAidType.code IN (\'1\', \'2\', \'3\')))''')
            if orgStructureIdList:
                cond.append(getOrgStructureProperty(u'Отделение', orgStructureIdList))
            if noPropertyProfile:
                cond.append(getNoPropertyAPHBP())
            elif profile:
                cond.append(getPropertyAPHBP([profile], True))
            cond.append(tableAction['endDate'].ge(begDateTime))
            cond.append(tableAction['endDate'].le(endDateTime))
            isStationaryDS = '''EXISTS(SELECT APS.id
            FROM ActionPropertyType AS APT
            INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
            INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
            WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id AND AP.action_id=Action.id AND APT.deleted=0
            AND APT.name = '%s' AND APS.value = '%s')'''%(u'Исход госпитализации', u'переведен в ДС')
            isStationaryKS = '''EXISTS(SELECT APS.id
            FROM ActionPropertyType AS APT
            INNER JOIN ActionProperty AS AP ON AP.type_id=APT.id
            INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
            WHERE  Action.id IS NOT NULL AND APT.actionType_id=Action.actionType_id AND AP.action_id=Action.id AND APT.deleted=0
            AND APT.name = '%s' AND APS.value = '%s')'''%(u'Исход госпитализации', u'переведен в КС')
            stmt = db.selectDistinctStmt(queryTable, u'COUNT(Client.id) AS countAll, SUM(%s) AS countDeath, SUM(%s) AS countTransfer, SUM(%s) AS isStationaryDS, SUM(%s) AS isStationaryKS'%(getStringProperty(u'Исход госпитализации', u'(APS.value LIKE \'умер%\' OR APS.value LIKE \'смерть%\')'), getStringProperty(u'Исход госпитализации', u'(APS.value = \'переведен в другой стационар\')'), isStationaryDS, isStationaryKS), where=cond)
            query = db.query(stmt)
            if query.first():
                record = query.record()
                countAll = forceInt(record.value('countAll'))
                countDeath = forceInt(record.value('countDeath'))
                return [countAll - countDeath, countDeath, forceInt(record.value('countTransfer')), forceInt(record.value('isStationaryDS')), forceInt(record.value('isStationaryKS'))]
            else:
                return [0, 0, 0, 0, 0]


        def columnFill(begDate, endDate, parentOrgStructureIdList, profile, row, endTime):
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, row)
            movingPresentBeg = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile)
            #self.movingsPresentBeg += movingPresentBeg
            table.setText(row, 4, movingPresentBeg)#!
            all, children, clientRural, isStationaryDay, ageAdult = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile)
            table.setText(row, 5, all)#!
            table.setText(row, 6, isStationaryDay)#!
            table.setText(row, 7, clientRural)#!
            table.setText(row, 8, children)#!
            table.setText(row, 9, ageAdult)#!
            table.setText(row, 10, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, transferType=1))#!
            table.setText(row, 11, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, transferType=0))#!
            countLeavedAll, leavedDeath, leavedTransfer, isStationaryDS, isStationaryKS = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile)
            countLeavedAllNoProfile, leavedDeathNoProfile, leavedTransferNoProfile, isStationaryDSNoProfile, isStationaryKSNoProfile = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile, True)
            table.setText(row, 12, countLeavedAll + countLeavedAllNoProfile)#!
            table.setText(row, 13, isStationaryDS + isStationaryDSNoProfile)#!
            table.setText(row, 14, isStationaryKS + isStationaryKSNoProfile)#!
            table.setText(row, 16, leavedDeath + leavedDeathNoProfile)#!
            table.setText(row, 15, leavedTransfer + leavedTransferNoProfile)#!
            movingPresentEnd = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True)
            #self.movingsPresentEnd += movingPresentEnd
            table.setText(row, 17, movingPresentEnd)#!
            table.setText(row, 18, getMovingDays(parentOrgStructureIdList, begDate, endDate, profile))#!
            #table.setText(row, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile))
            table.setText(row, 20, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile))#!
            table.setText(row, 19, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile))#!

        currentDate = QDate.currentDate()
        currentDateYear = currentDate.year()
        precedentDateMonth = currentDate.month() - 1
        def getDataReport(parentOrgStructureIdList, rowProfile, profile):
            self.movingsPresentBeg = 0
            self.movingsPresentEnd = 0
            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 1):
                table.setText(rowProfile, 0, u'Январь')
                unrolledHospitalBedsMonth(rowProfile, 1, parentOrgStructureIdList, profile)#Число коек на конец отчетного периода - Это как общее колво за весь период или наличие коек на последний день? Как за полугодие и за год?????????????????????????????????????
                begDate, endDate = self.createBegEndDate(1, 1, yearDateInt)
                self.movingsPresentBeg = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 2):
                table.setText(rowProfile, 0, u'Февраль')
                unrolledHospitalBedsMonth(rowProfile, 2, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(2, 2, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 3):
                table.setText(rowProfile, 0, u'Март')
                unrolledHospitalBedsMonth(rowProfile, 3, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(3, 3, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 4):
                table.setText(rowProfile, 0, u'Апрель')
                unrolledHospitalBedsMonth(rowProfile, 4, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(4, 4, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 5):
                table.setText(rowProfile, 0, u'Май')
                unrolledHospitalBedsMonth(rowProfile, 5, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(5, 5, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 6):
                table.setText(rowProfile, 0, u'Июнь')
                unrolledHospitalBedsMonth(rowProfile, 6, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(6, 6, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            table.setText(rowProfile, 0, u'За полугодие')
            unrolledHospitalBedsMonth(rowProfile, 6, parentOrgStructureIdList, profile)
            begDate, endDate = self.createBegEndDate(1, precedentDateMonth if precedentDateMonth <= 6 else 6, yearDateInt)
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, rowProfile, None, 6)
            table.setText(rowProfile, 4, self.movingsPresentBeg)#!
            all, children, clientRural, isStationaryDay, ageAdult = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile)
            table.setText(rowProfile, 5, all)#!
            table.setText(rowProfile, 6, isStationaryDay)#!
            table.setText(rowProfile, 7, clientRural)#!
            table.setText(rowProfile, 8, children)#!
            table.setText(rowProfile, 9, ageAdult)#!
            table.setText(rowProfile, 10, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, transferType=1))#!
            table.setText(rowProfile, 11, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, transferType=0))#!
            countLeavedAll, leavedDeath, leavedTransfer, isStationaryDS, isStationaryKS = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile)
            table.setText(rowProfile, 12, countLeavedAll)#!
            table.setText(rowProfile, 13, isStationaryDS)#!
            table.setText(rowProfile, 14, isStationaryKS)#!
            table.setText(rowProfile, 16, leavedDeath)#!
            table.setText(rowProfile, 15, leavedTransfer)#!
            table.setText(rowProfile, 17, getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True))#!
            table.setText(rowProfile, 18, getMovingDays(parentOrgStructureIdList, begDate, endDate, profile))#!
            #table.setText(rowProfile, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile))
            table.setText(rowProfile, 20, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile))#!
            table.setText(rowProfile, 19, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile))#!
            rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 7):
                table.setText(rowProfile, 0, u'Июль')
                unrolledHospitalBedsMonth(rowProfile, 7, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(7, 7, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 8):
                table.setText(rowProfile, 0, u'Август')
                unrolledHospitalBedsMonth(rowProfile, 8, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(8, 8, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 9):
                table.setText(rowProfile, 0, u'Сентябрь')
                unrolledHospitalBedsMonth(rowProfile, 9, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(9, 9, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 10):
                table.setText(rowProfile, 0, u'Октябрь')
                unrolledHospitalBedsMonth(rowProfile, 10, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(10, 10, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 11):
                table.setText(rowProfile, 0, u'Ноябрь')
                unrolledHospitalBedsMonth(rowProfile, 11, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(11, 11, yearDateInt)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            if (yearDateInt != currentDateYear) or (precedentDateMonth >= 12):
                table.setText(rowProfile, 0, u'Декабрь')
                unrolledHospitalBedsMonth(rowProfile, 12, parentOrgStructureIdList, profile)
                begDate, endDate = self.createBegEndDate(12, 12, yearDateInt)
                self.movingsPresentEnd = getMovingPresent(begDate, endDate, parentOrgStructureIdList, endTime, profile, True)
                columnFill(begDate, endDate, parentOrgStructureIdList, profile, rowProfile, endTime)
                rowProfile = table.addRow()

            table.setText(rowProfile, 0, u'За год')
            unrolledHospitalBedsMonth(rowProfile, 12, parentOrgStructureIdList, profile)
            begDate, endDate = self.createBegEndDate(1, 12, yearDateInt)
            self.averageYarHospitalBed(parentOrgStructureIdList, table, begDate, endDate, profile, rowProfile, None, 12)
            begDate, endDate = self.createBegEndDate(1, precedentDateMonth, yearDateInt)
            table.setText(rowProfile, 4, self.movingsPresentBeg)#!
            all, children, clientRural, isStationaryDay, ageAdult = getReceived(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile)
            table.setText(rowProfile, 5, all)#!
            table.setText(rowProfile, 6, isStationaryDay)#!
            table.setText(rowProfile, 7, clientRural)#!
            table.setText(rowProfile, 8, children)#!
            table.setText(rowProfile, 9, ageAdult)#!
            table.setText(rowProfile, 10, getMovingTransfer(begDate, endDate, parentOrgStructureIdList, u'Переведен из отделения', profile, transferType=1))#!
            table.setText(rowProfile, 11, getMovingTransfer(begDate, endDate, parentOrgStructureIdList,  u'Переведен в отделение', profile, True, transferType=0))#!
            countLeavedAll, leavedDeath, leavedTransfer, isStationaryDS, isStationaryKS = getLeaved(begDate, endDate, parentOrgStructureIdList,u'Переведен в отделение', profile)
            table.setText(rowProfile, 12, countLeavedAll)#!
            table.setText(rowProfile, 13, isStationaryDS)#!
            table.setText(rowProfile, 14, isStationaryKS)#!
            table.setText(rowProfile, 16, leavedDeath)#!
            table.setText(rowProfile, 15, leavedTransfer)#!
            table.setText(rowProfile, 17, self.movingsPresentEnd)#!
            table.setText(rowProfile, 18, getMovingDays(parentOrgStructureIdList, begDate, endDate, profile))#!
            #table.setText(rowProfile, 14, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, False, profile))
            table.setText(rowProfile, 20, self.dataPatronageOrClientRuralDays(begDate, endDate, parentOrgStructureIdList, True, profile))#!
            table.setText(rowProfile, 19, self.dataInvolutionDays(parentOrgStructureIdList, begDate, endDate, profile))#!
            rowProfile = table.addRow()
            return rowProfile

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        def getOrgStructureParent(orgStructureIdList, rowProfile, table, profile):
            for parentOrgStructureId in orgStructureIdList:
                tableQuery = tableOS.innerJoin(tableOSHB, tableOSHB['master_id'].eq(tableOS['id']))
                recordEx = db.getRecordEx(tableQuery,
                                          [tableOS['name'], tableOS['id']],
                                          [tableOS['deleted'].eq(0),
                                           tableOS['id'].eq(parentOrgStructureId),
                                           tableOS['type'].ne(0)])
                if recordEx:
                    name = forceString(recordEx.value('name'))
                    table.setText(rowProfile, 0, name, boldChars)
                    rowProfile = table.addRow()
                    rowProfile = getDataReport([parentOrgStructureId], rowProfile, profile)
                    records = db.getRecordList(tableQuery,
                                               [tableOS['id'], tableOS['name']],
                                               [tableOS['deleted'].eq(0), tableOS['type'].ne(0),
                                                tableOS['parent_id'].eq(parentOrgStructureId),
                                                tableOS['type'].ne(0)])
                    for record in records:
                        name = forceString(record.value('name'))
                        orgStructureId = forceRef(record.value('id'))
                        table.setText(rowProfile, 0, name, boldChars)
                        rowProfile = table.addRow()
                        rowProfile = getDataReport([orgStructureId], rowProfile, profile)

        nextRow = table.addRow()
        if isGroupingOS:
            getOrgStructureParent(begOrgStructureIdList, nextRow, table, profile)
        else:
            getDataReport(begOrgStructureIdList, nextRow, profile)
        table.delRow(table.rowCount()-1, 1)
        return doc


    def createBegEndDate(self, monthBeg, monthEnd, yearDateInt):
        if monthBeg > 1:
            begDate = QDateTime(QDate(yearDateInt, monthBeg, 1), self.endTime)
        else:
            begDate = QDateTime(QDate(yearDateInt, monthBeg, 1), QTime(0, 0, 0, 0))
        if monthEnd < 12:
            endDate = QDateTime(QDate(yearDateInt, monthEnd + 1, 1), self.endTime)
        else:
            endDate = QDateTime(QDate(yearDateInt + 1, 1, 1), QTime(0, 0, 0, 0))
        return begDate, endDate


    def averageYarHospitalBed(self, orgStructureIdList, table, begDate, endDate, profile = None, row = None, isHospital = None, countMonths = None):
        days = 0
        daysMonths = 0
        begDatePeriod = begDate.date()
        endDatePeriod = begDatePeriod.addMonths(1)
        while endDatePeriod <= endDate.date():
            days = self.averageDaysHospitalBed(orgStructureIdList, begDatePeriod, endDatePeriod, profile, isHospital)
            daysMonths += days / (begDatePeriod.daysInMonth())
            begDatePeriod = begDatePeriod.addMonths(1)
            endDatePeriod = endDatePeriod.addMonths(1)
        if countMonths == 12:
            daysMonths = daysMonths / 12
        elif countMonths == 6:
            daysMonths = daysMonths / 6
        if profile:
           table.setText(row, 3, daysMonths) #!
        else:
            table.setText(row, 3, daysMonths)


    def averageDaysHospitalBed(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None):
        days = 0
        db = QtGui.qApp.db
        tableOSHB = db.table('OrgStructure_HospitalBed')
        tableOrg = db.table('Organisation')
        tableOS = db.table('OrgStructure')
        queryTable = tableOSHB.innerJoin(tableOS, tableOS['id'].eq(tableOSHB['master_id']))
        queryTable = queryTable.innerJoin(tableOrg, tableOrg['id'].eq(tableOS['organisation_id']))
        bedType = db.translate('rbHospitalBedType', 'name', u'профильная', 'id')
        cond = [tableOSHB['master_id'].inlist(orgStructureIdList),
                tableOrg['deleted'].eq(0),
                tableOS['deleted'].eq(0),
                tableOS['type'].ne(0),
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


    def dataMovingDays(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None):
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
                tableOS['type'].ne(0),
                tableClient['deleted'].eq(0),
                tableOrg['deleted'].eq(0),
                tableAPT['typeName'].like('HospitalBed'),
                tableAP['action_id'].eq(tableAction['id'])
               ]
        if isHospital is not None:
           cond.append(tableOrg['isHospital'].eq(isHospital))
        if profile:
           cond.append(tableOSHB['profile_id'].eq(profile))
        cond.append(tableOSHB['master_id'].inlist(orgStructureIdList))
        joinAnd = db.joinAnd([tableAction['endDate'].isNull(), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod.addDays(-1))])
        cond.append(db.joinOr([db.joinAnd([tableAction['endDate'].isNotNull(), tableAction['endDate'].gt(begDatePeriod), tableAction['begDate'].isNotNull(), tableAction['begDate'].lt(endDatePeriod.addDays(-1))]), joinAnd]))
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
                    begDate = begDatePeriod.date().addDays(-1)
                if not endDate or endDate > endDatePeriod.date():
                    endDate = endDatePeriod.date()
                if begDate and endDate:
                    if begDate == endDate:
                        days += 1
                    else:
                        days += begDate.daysTo(endDate)
        return days


    def dataInvolutionDays(self, orgStructureIdList, begDatePeriod, endDatePeriod, profile = None, isHospital = None):
        days = 0
        db = QtGui.qApp.db
        tableVHospitalBed = db.table('vHospitalBed')
        tableOS = db.table('OrgStructure')
        tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
        queryTable = tableVHospitalBed.innerJoin(tableOS,  tableVHospitalBed['master_id'].eq(tableOS['id']))
        queryTable = queryTable.innerJoin(tableInvolution, tableInvolution['master_id'].eq(tableVHospitalBed['id']))
        condRepairs = [tableOS['type'].ne(0),
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


    def dataPatronageOrClientRuralDays(self, begDatePeriod, endDatePeriod, orgStructureIdList, propertyPatronage, profile = None):
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
        cond.append(tableOS['type'].ne(0))
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
