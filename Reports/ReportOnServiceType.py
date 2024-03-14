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

from library.Utils            import forceInt, forceRef, forceString

from Events.ActionServiceType import CActionServiceType
from Events.Utils             import getActionTypeIdListByFlatCode
from Orgs.Utils               import getOrgStructureFullName
from Reports.Report           import CReport
from Reports.ReportBase       import CReportBase, createTable
from Reports.ReportView       import CPageFormat
from Reports.Utils            import dateRangeAsStr, getStringProperty, updateLIKE


from Ui_ReportOnServiceTypeSetup import Ui_ReportOnServiceTypeSetupDialog


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
    isProfileDetail      = params.get('isProfileDetail', False)
    isServiceDetail      = params.get('isServiceDetail', False)
    isPersonDetail       = params.get('isPersonDetail', False)
    isMKBDetail          = params.get('isMKBDetail', False)
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tableAction = db.table('Action')
    tableClient = db.table('Client')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableActionType = db.table('ActionType')
    tableOrgStructure = db.table('OrgStructure')
    tableDiagnosis = db.table('Diagnosis')
    queryTable = tableEvent.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
    queryTable = queryTable.innerJoin(tableOrgStructure, tableOrgStructure['id'].eq(tablePerson['orgStructure_id']))
    queryTable = queryTable.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    queryTable = queryTable.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnosis['id'].eqEx('getEventDiagnosis(Event.id)'))
    cols = [tablePerson['orgStructure_id'],
            tableOrgStructure['code'].alias('codeOS'),
            tableOrgStructure['name'].alias('nameOS')
            ]
    groupBy = [tablePerson['orgStructure_id'].name()]
    orderBy = [tableOrgStructure['code'].name()]
    movingIdList = getActionTypeIdListByFlatCode('moving%')
    receivedIdList = getActionTypeIdListByFlatCode('received%')
    if isProfileDetail:
        cols.append(u'%s AS movingProfileName'%getPropertyProfileName(u'Профиль', movingIdList))
        cols.append(u'%s AS receivedProfileName'%getPropertyProfileName(u'Профиль', receivedIdList))
        groupBy.append(u'''IF(movingProfileName IS NOT NULL, movingProfileName, IF(receivedProfileName IS NOT NULL, receivedProfileName, codeOS))''')
        orderBy.append(u'''IF(movingProfileName IS NOT NULL, movingProfileName, IF(receivedProfileName IS NOT NULL, receivedProfileName, codeOS))''')
    if isPersonDetail:
        cols.append(tableAction['person_id'])
        cols.append(tablePerson['id'].alias('personExecId'))
        cols.append(tablePerson['name'].alias('personNameExec'))
        groupBy.append(tableAction['person_id'].name())
        orderBy.append(tableAction['person_id'].name())
    if isServiceDetail:
        cols.append(tableActionType['code'].alias('actionTypeCode'))
        groupBy.append(u'actionTypeCode')
        orderBy.append(u'actionTypeCode')
    if isMKBDetail:
        cols.append(tableAction['MKB'].alias('actionMKB'))
        cols.append(tableDiagnosis['MKB'].alias('eventMKB'))
        groupBy.append(u'actionMKB,eventMKB')
        orderBy.append(u'actionMKB,eventMKB')
    cols.append(u'COUNT(Action.amount) AS countActionAmount')
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
        cond.append(db.joinOr([getPropertyProfile(u'Профиль', hospitalBedProfileId, movingIdList),
                               getPropertyProfile(u'Профиль', hospitalBedProfileId, receivedIdList)
                                ]))
    if order:
        actionOrderCond = 'APS.value like '
        actionOrderValue = ''
        actionOrderValue = actionOrderValue + ([u'Плановый', u'Экстренный', u'Самотёком', u'Принудительный', u'Внутренний перевод', u'Неотложная'][order-1])
        actionOrderCond = actionOrderCond + '"' + actionOrderValue + '"'
        cond.append(db.joinOr([getStringProperty(u'Порядок', actionOrderCond), db.joinAnd([(tableEvent['order'].eq(order)), ('NOT ' + getStringProperty(u'Порядок', 'Action.deleted=0'))])]))

    stmt = db.selectStmtGroupBy(queryTable, cols, cond, groupBy, orderBy)
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


def getPropertyProfileName(nameProperty, actionTypeIdList):
    return '''(SELECT CONCAT_WS('-', RBHBP.code, RBHBP.name)
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
ORDER BY APHBP.id
LIMIT 1
)'''%(u','.join(str(actionTypeId) for actionTypeId in actionTypeIdList), updateLIKE(nameProperty))


class CReportOnServiceTypeSetupDialog(QtGui.QDialog, Ui_ReportOnServiceTypeSetupDialog):
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
        self.isProfileDetail.setChecked(params.get('isProfileDetail', False))
        self.isServiceDetail.setChecked(params.get('isServiceDetail', False))
        self.isPersonDetail.setChecked(params.get('isPersonDetail', False))
        self.isMKBDetail.setChecked(params.get('isMKBDetail', False))


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
        result['isProfileDetail'] = self.isProfileDetail.isChecked()
        result['isServiceDetail'] = self.isServiceDetail.isChecked()
        result['isPersonDetail'] = self.isPersonDetail.isChecked()
        result['isMKBDetail'] = self.isMKBDetail.isChecked()
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


class CReportOnServiceType(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет по видам услуг')
        self.orientation = CPageFormat.Landscape
        self.setOrientation(QtGui.QPrinter.Landscape)


    def getSetupDialog(self, parent):
        result = CReportOnServiceTypeSetupDialog(parent)
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
        description.append(dateRangeAsStr(u'%s за период'%dateTypeName, QDateTime(begDate, begTime), QDateTime(endDate, endTime)))
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
        if params.get('isProfileDetail', False):
            description.append(u'Детализация по профилям')
        if params.get('isPersonDetail', False):
            description.append(u'Детализация по исполнителям')
        if params.get('isServiceDetail', False):
            description.append(u'Детализация по услугам')
        if params.get('isMKBDetail', False):
            description.append(u'Детализация по кодам МКБ')
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
        isProfileDetail = params.get('isProfileDetail', False)
        isServiceDetail = params.get('isServiceDetail', False)
        isPersonDetail  = params.get('isPersonDetail', False)
        isMKBDetail = params.get('isMKBDetail', False)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Отчет по видам услуг')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        col = 0
        colDict = {}
        cols = [('20%',[u'Подразделение'], CReportBase.AlignLeft),
                ('20%', [u'Количество услуг'], CReportBase.AlignLeft)
                ]
        if isProfileDetail:
            col+=1
            cols.insert(col, ('20%', [u'Профиль'], CReportBase.AlignLeft))
            colDict[u'isProfileDetail']=col
        if isPersonDetail:
            col+=1
            cols.insert(col, ('20%', [u'Исполнитель'], CReportBase.AlignLeft))
            colDict[u'isPersonDetail']=col
        if isServiceDetail:
            col+=1
            cols.insert(col, ('20%', [u'Код услуги'], CReportBase.AlignLeft))
            colDict[u'isServiceDetail']=col
        if isMKBDetail:
            col+=1
            cols.insert(col, ('20%', [u'Код МКБ'], CReportBase.AlignLeft))
            colDict[u'isMKBDetail']=col
        table = createTable(cursor, cols)
        row = 1
        profilePrev = u'не заполнено'
        profileRow = 1
        personNameExecPrev = u'не заполнено'
        personNameExecRow = 1
        orgStructureIdPrev = u'не заполнено'
        orgStructureIdRow = 1
        query = selectData(params)
        while query.next():
            record = query.record()
            orgStructureId = forceRef(record.value('orgStructure_id'))
            codeOS = forceString(record.value('codeOS'))
            nameOS = forceString(record.value('nameOS'))
            row = table.addRow()
            if orgStructureIdPrev != orgStructureId:
                table.setText(row, 0, codeOS + u'-' + nameOS)
                orgStructureIdPrev = orgStructureId
                table.mergeCells(orgStructureIdRow, 0, row-orgStructureIdRow, 1)
                orgStructureIdRow = row
            if isProfileDetail:
                movingProfileName = forceString(record.value('movingProfileName'))
                receivedProfileName = forceString(record.value('receivedProfileName'))
                if movingProfileName:
                    if profilePrev != movingProfileName or orgStructureIdRow == row:
                        table.setText(row, colDict[u'isProfileDetail'], movingProfileName)
                        profilePrev = movingProfileName
                        table.mergeCells(profileRow, colDict[u'isProfileDetail'], row-profileRow, 1)
                        profileRow = row
                elif receivedProfileName:
                    if profilePrev != receivedProfileName or orgStructureIdRow == row:
                        table.setText(row, colDict[u'isProfileDetail'], receivedProfileName)
                        profilePrev = receivedProfileName
                        table.mergeCells(profileRow, colDict[u'isProfileDetail'], row-profileRow, 1)
                        profileRow = row
                else:
                    if profilePrev != receivedProfileName or orgStructureIdRow == row:
                        profilePrev = receivedProfileName
                        table.mergeCells(profileRow, colDict[u'isProfileDetail'], row-profileRow, 1)
                        profileRow = row
            if isPersonDetail:
                personNameExec = forceString(record.value('personNameExec'))
                if personNameExecPrev != personNameExec or (isProfileDetail and profileRow == row):
                    table.setText(row, colDict[u'isPersonDetail'], personNameExec)
                    personNameExecPrev = personNameExec
                    table.mergeCells(personNameExecRow, colDict[u'isPersonDetail'], row-personNameExecRow, 1)
                    personNameExecRow = row
            if isServiceDetail:
                actionTypeCode = forceString(record.value('actionTypeCode'))
                table.setText(row, colDict[u'isServiceDetail'], actionTypeCode)
            if isMKBDetail:
                actionMKB = forceString(record.value('actionMKB'))
                eventMKB = forceString(record.value('eventMKB'))
                table.setText(row, colDict[u'isMKBDetail'], actionMKB if actionMKB!=u'' else eventMKB)
            countActionAmount = forceInt(record.value('countActionAmount'))
            table.setText(row, len(cols)-1, countActionAmount)
        if orgStructureIdRow != row:
            table.mergeCells(orgStructureIdRow, 0, row-orgStructureIdRow+1, 1)
        if personNameExecRow != row and isPersonDetail:
            table.mergeCells(personNameExecRow, colDict[u'isPersonDetail'], row-personNameExecRow+1, 1)
        return doc

