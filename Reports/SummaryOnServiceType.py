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
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime, QTime

from library.Utils      import forceRef, forceString, formatName

from Events.ActionServiceType import CActionServiceType
from Events.Utils             import getActionTypeIdListByFlatCode
from Orgs.Utils               import getOrgStructureFullName
from Reports.Report           import CReport
from Reports.ReportBase       import CReportBase, createTable
from Reports.ReportView       import CPageFormat
from Reports.Utils            import dateRangeAsStr, getStringProperty, updateLIKE

from Reports.Ui_SummaryOnServiceTypeSetup import Ui_SummaryOnServiceTypeSetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    if not endDate:
        return None
    begTime              = params.get('begTime', QTime())
    begDateTime          = QDateTime(begDate, begTime)
    endTime              = params.get('endTime', QTime())
    endDateTime          = QDateTime(endDate, endTime)
    actionDateType       = params.get('actionDateType', 0)
    orgStructureId       = params.get('orgStructureId', None)
    hospitalBedProfileId = params.get('hospitalBedProfileId', None)
    serviceType          = params.get('serviceType', CActionServiceType.other)
    typeNumberEvent      = params.get('typeNumberEvent', 0)
    eventNumber          = params.get('eventNumber', u'')
    order                = params.get('order', 0)
    financeId            = params.get('financeId', None)
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tableAction = db.table('Action')
    tableClient = db.table('Client')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableActionType = db.table('ActionType')
    queryTable = tableEvent.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
    queryTable = queryTable.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    queryTable = queryTable.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    cols = [tableEvent['id'].alias('numberEventId'),
            tableEvent['externalId'].alias('externalId'),
            tableClient['id'].alias('clientId'),
            tableClient['lastName'],
            tableClient['firstName'],
            tableClient['patrName'],
            tableAction['id'].alias('actionId'),
            tableActionType['code'].alias('actionTypeCode'),
            tableAction['person_id'],
            tablePerson['id'].alias('personExecId'),
            tablePerson['name'].alias('personNameExec'),
            tableAction['assistant_id']
            ]
    cols.append('''(SELECT PWS.name
    FROM vrbPersonWithSpeciality AS PWS
    WHERE PWS.id = Action.assistant_id
    LIMIT 1) AS assistantName''')
    cond = [tableEvent['deleted'].eq(0),
            tableAction['deleted'].eq(0),
            tableActionType['deleted'].eq(0),
            tableClient['deleted'].eq(0)
            ]
    if actionDateType:
        cond.append(tableAction['begDate'].isNotNull())
        cond.append(tableAction['begDate'].ge(begDateTime))
        cond.append(tableAction['begDate'].le(endDateTime))
    else:
        cond.append(tableAction['endDate'].isNotNull())
        cond.append(tableAction['endDate'].ge(begDateTime))
        cond.append(tableAction['endDate'].le(endDateTime))
    if eventNumber:
        if typeNumberEvent != 1:
            cond.append(tableEvent['id'].eq(eventNumber))
        else:
            cond.append(tableEvent['externalId'].eq(eventNumber))
    if financeId:
        cond.append(tableAction['finance_id'].eq(financeId))
    if orgStructureId:
        orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
        if orgStructureIdList:
            cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    if serviceType:
        cond.append(tableActionType['serviceType'].eq(serviceType))
    if hospitalBedProfileId:
        movingIdList = getActionTypeIdListByFlatCode('moving%')
        receivedIdList = getActionTypeIdListByFlatCode('received%')
        cond.append(db.joinOr([getPropertyProfile(u'Профиль', hospitalBedProfileId, movingIdList),
                               getPropertyProfile(u'Профиль', hospitalBedProfileId, receivedIdList)
                                ]))
    if order:
        actionOrderCond = 'APS.value like '
        actionOrderValue = ''
        actionOrderValue = actionOrderValue + ([u'Плановый', u'Экстренный', u'Самотёком', u'Принудительный', u'Внутренний перевод', u'Неотложная'][order-1])
        actionOrderCond = actionOrderCond + '"' + actionOrderValue + '"'
        cond.append(db.joinOr([getStringProperty(u'Порядок', actionOrderCond), db.joinAnd([(tableEvent['order'].eq(order)), ('NOT ' + getStringProperty(u'Порядок', 'Action.deleted=0'))])]))
    stmt = db.selectDistinctStmt(queryTable, cols, cond, [tableClient['lastName'].name(),tableClient['firstName'].name(), tableClient['patrName'].name(), tableEvent['id'].name()])
    return db.query(stmt)


def getPropertyProfile(nameProperty, profileId, actionTypeIdList):
    return '''EXISTS(SELECT APHBP.value
FROM Action AS A
INNER JOIN ActionProperty AS AP_Profile ON AP_Profile.action_id=A.id
INNER JOIN ActionPropertyType AS APT_Profile ON AP_Profile.type_id=APT_Profile.id
INNER JOIN ActionProperty_rbHospitalBedProfile AS APHBP ON APHBP.id=AP_Profile.id
INNER JOIN rbHospitalBedProfile AS RBHBP ON RBHBP.id=APHBP.value
WHERE APT_Profile.actionType_id IN (%s)
AND A.event_id = Event.id
AND A.deleted = 0
AND (
(A.begDate IS NULL AND A.endDate IS NULL)
OR
(A.begDate IS NOT NULL AND A.endDate IS NULL
AND Action.endDate >= A.begDate)
OR
(A.begDate IS NULL AND A.endDate IS NOT NULL
AND Action.begDate <= A.endDate)
OR
(A.begDate IS NOT NULL AND A.endDate IS NOT NULL
AND Action.begDate <= A.endDate AND Action.endDate >= A.begDate)
)
AND AP_Profile.deleted = 0
AND APT_Profile.deleted = 0
AND APT_Profile.name %s
AND APT_Profile.typeName = 'rbHospitalBedProfile'
AND APHBP.value = %s
ORDER BY APHBP.id
LIMIT 1
)'''%(u','.join(str(actionTypeId) for actionTypeId in actionTypeIdList), updateLIKE(nameProperty), str(profileId))


class CSummaryOnServiceTypeSetupDialog(QtGui.QDialog, Ui_SummaryOnServiceTypeSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbHospitalBedProfile.setTable('rbHospitalBedProfile', True)
        self.cmbFinance.setTable('rbFinance', addNone=True)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.cmbDateType.setCurrentIndex(params.get('actionDateType', 0))
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtBegTime.setTime(params.get('begTime', QTime()))
        self.edtEndTime.setTime(params.get('endTime', QTime()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbHospitalBedProfile.setValue(params.get('hospitalBedProfileId', None))
        self.cmbServiceType.setValue(params.get('serviceType', CActionServiceType.other))
        self.cmbTypeNumberEvent.setCurrentIndex(params.get('typeNumberEvent', 0))
        self.edtEventNumber.setText(params.get('eventNumber', u''))
        self.cmbOrder.setCurrentIndex(params.get('order', 0))
        self.cmbFinance.setValue(params.get('financeId', None))


    def params(self):
        result = {}
        result['actionDateType'] = self.cmbDateType.currentIndex()
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['begTime'] = self.edtBegTime.time()
        result['endTime'] = self.edtEndTime.time()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['hospitalBedProfileId'] = self.cmbHospitalBedProfile.value()
        result['serviceType'] = self.cmbServiceType.value()
        result['typeNumberEvent'] = self.cmbTypeNumberEvent.currentIndex()
        result['eventNumber'] = self.edtEventNumber.text()
        result['order'] = self.cmbOrder.currentIndex()
        result['financeId'] = self.cmbFinance.value()
        return result


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


class CSummaryOnServiceType(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка по видам услуг')
        self.orientation = CPageFormat.Landscape
        self.setOrientation(QtGui.QPrinter.Landscape)


    def getSetupDialog(self, parent):
        result = CSummaryOnServiceTypeSetupDialog(parent)
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
        actionDateType = params.get('actionDateType', 0)
        if actionDateType:
            dateTypeName = u'Дата начала действия'
        else:
            dateTypeName = u'Дата выполнения действия'
        description.append(dateRangeAsStr(u'%s за период'%dateTypeName,
                                          QDateTime(begDate, begTime),
                                          QDateTime(endDate, endTime)))
        orgStructureId = params.get('orgStructureId', None)
        hospitalBedProfileId = params.get('hospitalBedProfileId', None)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        if hospitalBedProfileId:
            description.append(u'профиль койки: %s'%(forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'name'))))
        actionTypeId = params.get('actionTypeId', None)
        if actionTypeId:
            record = QtGui.qApp.db.getRecordEx('ActionType', ['code', 'name'],['id = %s'%actionTypeId], 'code, name')
            actionName = (u'-'.join([forceString(record.value('code')), forceString(record.value('name'))])) if record else u''
            description.append(u'вид услуги: %s'%(actionName))
        eventNumber = params.get('eventNumber', u'')
        if eventNumber:
            typeNumberEventName = u''
            typeNumberEvent = params.get('typeNumberEvent', 0)
            if typeNumberEvent:
                typeNumberEventName = u'(' + [u'номер документа', u'код карточки'][typeNumberEvent-1] + u')'
            description.append(u'номер обращения: %s %s'%(eventNumber, typeNumberEventName))
        order = params.get('order', 0)
        if order:
            description.append(u'порядок: %s'%([u'Плановый', u'Экстренный', u'Самотёком', u'Принудительный', u'Внутренний перевод', u'Неотложная'][order-1]))
        financeId = params.get('financeId', None)
        if financeId:
            description.append(u'тип финансирования: %s'%(forceString(QtGui.qApp.db.translate('rbFinance', 'id', financeId, 'name'))))
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getTheseAndChildrens(self, idlist):
        db = QtGui.qApp.db
        table = db.table('OrgStructure')
        result = []
        childrenIdList = db.getIdList(table, 'id', [table['parent_id'].inlist(idlist), table['deleted'].eq(0), table['hasHospitalBeds'].ne(0)])
        if childrenIdList:
            result = self.getTheseAndChildrens(childrenIdList)
        result += idlist
        return result


    def getNameOrgStructure(self, idlist):
        db = QtGui.qApp.db
        tableOrgStructure = db.table('OrgStructure')
        tableVHospitalBed = db.table('vHospitalBed')
        tableRBHospitalBedProfile = db.table('rbHospitalBedProfile')
        nameOrgStructureList = {}
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


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Сводка по видам услуг')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('20%',[u'Номер документа'], CReportBase.AlignLeft),
                ('20%', [u'ФИО пациента'], CReportBase.AlignLeft),
                ('20%', [u'Код услуги'], CReportBase.AlignLeft),
                ('20%', [u'ФИО исполнителя'], CReportBase.AlignLeft),
                ('20%', [u'ФИО ассистента'], CReportBase.AlignLeft)
               ]
        table = createTable(cursor, cols)
        actionListId = []
        row = 1
        prevEventId = None
        prevEventRow = 1
        prevClientId = None
        prevClientRow = 1
        typeNumberEvent = params.get('typeNumberEvent', 0)
        if typeNumberEvent != 1:
            eventName = 'numberEventId'
        else:
            eventName = 'externalId'
        query = selectData(params)
        countActions=0
        countPatients=0
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            countActions+=1
            if actionId and actionId not in actionListId:
                actionListId.append(actionId)
                numberEventId  = forceRef(record.value('numberEventId'))
                numberEvent    = forceString(record.value(eventName))
                clientId       = forceRef(record.value('clientId'))
                lastName       = forceString(record.value('lastName'))
                firstName      = forceString(record.value('firstName'))
                patrName       = forceString(record.value('patrName'))
                actionTypeCode = forceString(record.value('actionTypeCode'))
                personNameExec = forceString(record.value('personNameExec'))
                assistantName  = forceString(record.value('assistantName'))
                row = table.addRow()
                if prevEventId != numberEventId:
                    table.setText(row, 0, numberEvent)
                    prevEventId = numberEventId
                    table.mergeCells(prevEventRow, 0, row-prevEventRow, 1)
                    prevEventRow = row
                if prevClientId != clientId:
                    table.setText(row, 1, formatName(lastName, firstName, patrName))
                    prevClientId = clientId
                    table.mergeCells(prevClientRow, 1, row-prevClientRow, 1)
                    prevClientRow = row
                    countPatients+=1
                table.setText(row, 2, actionTypeCode)
                table.setText(row, 3, personNameExec)
                table.setText(row, 4, assistantName)
        if prevEventRow != row:
            table.mergeCells(prevEventRow, 0, row-prevEventRow+1, 1)
        if prevClientRow != row:
            table.mergeCells(prevClientRow, 1, row-prevClientRow+1, 1)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"Всего пациентов: %s, Всего услуг: %s" %(countPatients,  countActions))

        return doc

