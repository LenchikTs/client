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
from PyQt4.QtCore import QDateTime

from library.Utils      import forceDouble, forceInt, forceRef, forceString

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.FinanceSummaryByDoctors import getCond, CFinanceSummarySetupDialog


def selectDataByEvents(params):
    db = QtGui.qApp.db
    isPeriodOnService = params.get('isPeriodOnService', False)
    cond = getCond(params)
    if isPeriodOnService:
        condDate = []
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        tableEvent = db.table('Event')
        if begDate:
            condDate.append(tableEvent['execDate'].ge(begDate))
        if endDate:
            condDate.append(tableEvent['execDate'].lt(endDate.addDays(1)))
        cond += u' AND ' + db.joinAnd(condDate) if condDate else ''
    colsClientInfo = u''
    isClientsDetail = params.get('detailClient', False)
    if isClientsDetail:
        colsClientInfo = u'''CONCAT_WS(_utf8' ', Client.lastName, Client.firstName, Client.patrName) AS clientName,'''
    stmt="""
SELECT
    Contract.payer_id,
    Organisation.id,
    Organisation.shortName,
    EventType.medicalAidKind_id,
    rbMedicalAidKind.code AS codeMAK,
    rbMedicalAidKind.name AS nameMAK,
    Event.client_id AS clientId,
    %s
    SUM(Account_Item.amount/(SELECT
                            COUNT(D.id)
                          FROM Diagnostic AS D
                          LEFT JOIN rbDiagnosisType AS DT ON DT.id = D.diagnosisType_id
                          WHERE DT.code in ('1','2') AND D.event_id = Event.id AND D.deleted = 0
                         )) AS amount,
    SUM(Account_Item.sum/(SELECT
                            COUNT(D.id)
                          FROM Diagnostic AS D
                          LEFT JOIN rbDiagnosisType AS DT ON DT.id = D.diagnosisType_id
                          WHERE DT.code in ('1','2') AND D.event_id = Event.id AND D.deleted = 0
                         )) AS sum,
    SUM(Account_Item.uet/(SELECT
                            COUNT(D.id)
                          FROM Diagnostic AS D
                          LEFT JOIN rbDiagnosisType AS DT ON DT.id = D.diagnosisType_id
                          WHERE DT.code in ('1','2') AND D.event_id = Event.id AND D.deleted = 0
                         )) AS uet
FROM Account_Item
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
INNER JOIN Client         ON Client.id = Event.client_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
LEFT JOIN rbService       ON rbService.id = IF(Account_Item.service_id IS NULL, EventType.service_id, Account_Item.service_id)
LEFT JOIN Diagnostic      ON Diagnostic.event_id = Event.id
LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnostic.diagnosisType_id
LEFT JOIN Person          ON Person.id = Diagnostic.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN Organisation    ON (Organisation.id = Contract.payer_id AND Organisation.deleted = 0)
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NULL
    AND Diagnostic.deleted = 0
    AND Event.deleted = 0
    AND EventType.deleted = 0
    AND Client.deleted = 0
    AND rbDiagnosisType.code in ('1','2')
    AND %s
GROUP BY
    Contract.payer_id, EventType.medicalAidKind_id, Organisation.id, Event.client_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % (colsClientInfo, cond))


def selectDataByVisits(params):
    db = QtGui.qApp.db
    isPeriodOnService = params.get('isPeriodOnService', False)
    cond = getCond(params)
    if isPeriodOnService:
        condDate = []
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        tableVisit = db.table('Visit')
        if begDate:
            condDate.append(tableVisit['date'].ge(begDate))
        if endDate:
            condDate.append(tableVisit['date'].lt(endDate.addDays(1)))
        cond += u' AND ' + db.joinAnd(condDate) if condDate else ''
    colsClientInfo = u''
    isClientsDetail = params.get('detailClient', False)
    if isClientsDetail:
        colsClientInfo = u'''CONCAT_WS(_utf8' ', Client.lastName, Client.firstName, Client.patrName) AS clientName,'''
    stmt="""
SELECT
    Contract.payer_id,
    Organisation.id,
    Organisation.shortName,
    EventType.medicalAidKind_id,
    rbMedicalAidKind.code AS codeMAK,
    rbMedicalAidKind.name AS nameMAK,
    Event.client_id AS clientId,
    %s
    SUM(Account_Item.amount) AS amount,
    SUM(Account_Item.sum) AS sum,
    SUM(Account_Item.uet) AS uet
FROM Account_Item
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Contract     ON Contract.id = Account.contract_id
LEFT JOIN Event        ON Event.id = Account_Item.event_id
INNER JOIN Client      ON Client.id = Event.client_id
LEFT JOIN EventType    ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
LEFT JOIN Visit        ON Visit.id = Account_Item.visit_id
LEFT JOIN rbService    ON rbService.id = IF(Account_Item.service_id IS NULL, Visit.service_id, Account_Item.service_id)
LEFT JOIN Person       ON Person.id = Visit.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN Organisation ON (Organisation.id = Contract.payer_id AND Organisation.deleted = 0)
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND Event.deleted = 0
    AND EventType.deleted = 0
    AND Client.deleted = 0
    AND %s
GROUP BY
    Contract.payer_id, EventType.medicalAidKind_id, Organisation.id, Event.client_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % (colsClientInfo, cond))


def selectDataByActions(params):
    db = QtGui.qApp.db
    isPeriodOnService = params.get('isPeriodOnService', False)
    cond = getCond(params)
    if isPeriodOnService:
        condDate = []
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        tableAction = db.table('Action')
        if begDate:
            condDate.append(tableAction['endDate'].ge(begDate))
        if endDate:
            condDate.append(tableAction['endDate'].lt(endDate.addDays(1)))
        cond += u' AND ' + db.joinAnd(condDate) if condDate else ''
    colsClientInfo = u''
    isClientsDetail = params.get('detailClient', False)
    if isClientsDetail:
        colsClientInfo = u'''CONCAT_WS(_utf8' ', Client.lastName, Client.firstName, Client.patrName) AS clientName,'''
    stmt="""
SELECT
    Contract.payer_id,
    Organisation.id,
    Organisation.shortName,
    EventType.medicalAidKind_id,
    rbMedicalAidKind.code AS codeMAK,
    rbMedicalAidKind.name AS nameMAK,
    Event.client_id AS clientId,
    %s
    SUM(Account_Item.amount) AS amount,
    SUM(Account_Item.sum) AS sum,
    SUM(Account_Item.uet) AS uet
FROM Account_Item
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Contract     ON Contract.id = Account.contract_id
LEFT JOIN Event        ON Event.id = Account_Item.event_id
INNER JOIN Client      ON Client.id = Event.client_id
LEFT JOIN EventType    ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
LEFT JOIN Action       ON Action.id = Account_Item.action_id
LEFT JOIN ActionType   ON ActionType.id = Action.actionType_id
LEFT JOIN rbService    ON rbService.id = Account_Item.service_id
LEFT JOIN Person       ON Person.id = Action.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN Organisation ON (Organisation.id = Contract.payer_id AND Organisation.deleted = 0)
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NOT NULL
    AND Event.deleted = 0
    AND EventType.deleted = 0
    AND Client.deleted = 0
    AND %s
GROUP BY
    Contract.payer_id, EventType.medicalAidKind_id, Organisation.id, Event.client_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % (colsClientInfo, cond))


class CReportInsuredMedicalCare(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения об оказанной застрахованному лицу медицинской помощи')


    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialog(parent)
        result.chkDetailClient.setVisible(True)
        result.setVisiblePeriodOnService(True)
        result.setVisibleAgeFilter(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        isClientsDetail = params.get('detailClient', False)
        reportRowSize = 4
        reportData = {}
        clientIdList = []
        def processQuery(query):
            while query.next():
                record = query.record()
                clientId         = forceInt(record.value('clientId'))
                payerId          = forceRef(record.value('payer_id'))
                shortName        = forceString(record.value('shortName'))
                medicalAidKindId = forceRef(record.value('medicalAidKind_id'))
                codeNameMAK      = forceString(record.value('codeMAK')) + u'-' + forceString(record.value('nameMAK'))
                amount           = forceDouble(record.value('amount'))
                uet              = forceDouble(record.value('uet'))
                if amount == int(amount):
                   amount = int(amount)
                sum              = forceDouble(record.value('sum'))

                reportPayerLine = reportData.setdefault((shortName, payerId), {})
                if isClientsDetail:
                    clientName = forceString(record.value('clientName'))
                    reportAidKindLine = reportPayerLine.setdefault((codeNameMAK, medicalAidKindId), {})
                    reportClientAidKindLine = reportAidKindLine.setdefault((clientId, clientName), [0]*reportRowSize)
                    if clientId and (clientId, medicalAidKindId, payerId) not in clientIdList:
                        clientIdList.append((clientId, medicalAidKindId, payerId))
                        reportClientAidKindLine[0] += 1
                    reportClientAidKindLine[1] += amount
                    reportClientAidKindLine[2] += uet
                    reportClientAidKindLine[3] += sum
                else:
                    reportAidKindLine = reportPayerLine.setdefault((codeNameMAK, medicalAidKindId), [0]*reportRowSize)
                    if clientId and (clientId, medicalAidKindId, payerId) not in clientIdList:
                        clientIdList.append((clientId, medicalAidKindId, payerId))
                        reportAidKindLine[0] += 1
                    reportAidKindLine[1] += amount
                    reportAidKindLine[2] += uet
                    reportAidKindLine[3] += sum
        query = selectDataByEvents(params)
        processQuery(query)
        query = selectDataByVisits(params)
        processQuery(query)
        query = selectDataByActions(params)
        processQuery(query)
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText('\n'.join(self.getDescription(params)))
        cursor.insertBlock()
        tableColumns = [('30%',[ u'Наименование плательщика'], CReportBase.AlignLeft),
                        ('15%' if isClientsDetail else '30%',[ u'Вид медицинской помощи'  ], CReportBase.AlignLeft ),
                        ('10%', [ u'Число лиц'               ], CReportBase.AlignLeft ),
                        ('10%', [ u'Посещ./Услуг'            ], CReportBase.AlignRight ),
                        ('10%', [ u'УЕТ'                     ], CReportBase.AlignRight ),
                        ('10%', [ u'Стоимость'               ], CReportBase.AlignRight ),
                       ]
        if isClientsDetail:
            tableColumns.insert(2, ('15%',[ u'ФИО пациента'  ], CReportBase.AlignLeft ),)
        table = createTable(cursor, tableColumns)
        totalByReportAll = [0]*reportRowSize
        payerKeys = reportData.keys()
        payerKeys.sort()
        if isClientsDetail:
            for payerKey in payerKeys:
                totalByReport = [0]*reportRowSize
                i = table.addRow()
                payerRow = i
                table.setText(i, 0, payerKey[0])
                reportPayerLine = reportData.get(payerKey, {})
                aidKindKeys = reportPayerLine.keys()
                aidKindKeys.sort()
                aidKindKeyRows = len(aidKindKeys)
                for aidKindKey in aidKindKeys:
                    reportAidKindLineR = reportPayerLine.get(aidKindKey, None)
                    aidKindKeyRows += len(reportAidKindLineR.keys())-1
                aidKindClientKeyRows = 0
                for aidKindKey in aidKindKeys:
                    reportAidKindLine = reportPayerLine.get(aidKindKey, None)
                    if reportAidKindLine:
                        aidKindClientKeyRows += 1
                        aidKindRow = i
                        table.setText(i, 1, aidKindKey[0])
                        clientKeys = reportAidKindLine.keys()
                        clientKeys.sort(key=lambda item: item[1])
                        clientKeyRows = 0
                        for (clientId, clientName) in clientKeys:
                            table.setText(i, 2, clientName + u', ' + forceString(clientId))
                            clintInfo = reportAidKindLine.get((clientId, clientName), [])
                            for col, val in enumerate(clintInfo):
                                table.setText(i, col+3, val)
                                totalByReport[col] += val
                                totalByReportAll[col] += val
                            clientKeyRows += 1
                            if clientKeyRows < len(clientKeys):
                                i = table.addRow()
                        aidKindClientKeyRows += clientKeyRows-1
                        table.mergeCells(aidKindRow, 1, i-aidKindRow+1, 1)
                        if aidKindClientKeyRows < aidKindKeyRows:
                            i = table.addRow()
                table.mergeCells(payerRow, 0, i-payerRow+1, 1)
                if len(aidKindKeys) > 0:
                    i = table.addRow()
                    table.setText(i, 0, u'Итого', CReportBase.TableTotal)
                    for col, val in enumerate(totalByReport):
                        table.setText(i, col+3, val, CReportBase.TableTotal)
                    table.mergeCells(i, 0, 1, 3)
            if len(payerKeys) > 0:
                i = table.addRow()
                table.setText(i, 0, u'Всего', CReportBase.TableTotal)
                for col, val in enumerate(totalByReportAll):
                    table.setText(i, col+3, val, CReportBase.TableTotal)
                table.mergeCells(i, 0, 1, 3)
        else:
            for payerKey in payerKeys:
                totalByReport = [0]*reportRowSize
                i = table.addRow()
                payerRow = i
                table.setText(i, 0, payerKey[0])
                reportPayerLine = reportData.get(payerKey, {})
                aidKindKeys = reportPayerLine.keys()
                aidKindKeys.sort()
                for aidKindKey in aidKindKeys:
                    reportAidKindLine = reportPayerLine.get(aidKindKey, None)
                    if reportAidKindLine:
                        table.setText(i, 1, aidKindKey[0])
                        for col, val in enumerate(reportAidKindLine):
                            table.setText(i, col+2, val)
                            totalByReport[col] += val
                            totalByReportAll[col] += val
                        if (i-payerRow) < (len(aidKindKeys)-1):
                            i = table.addRow()
                table.mergeCells(payerRow, 0, i-payerRow+1, 1)
                if len(aidKindKeys) > 0:
                    i = table.addRow()
                    table.setText(i, 0, u'Итого', CReportBase.TableTotal)
                    for col, val in enumerate(totalByReport):
                        table.setText(i, col+2, val, CReportBase.TableTotal)
                    table.mergeCells(i, 0, 1, 2)
            if len(payerKeys) > 0:
                i = table.addRow()
                table.setText(i, 0, u'Всего', CReportBase.TableTotal)
                for col, val in enumerate(totalByReportAll):
                    table.setText(i, col+2, val, CReportBase.TableTotal)
                table.mergeCells(i, 0, 1, 2)
        return doc


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate             = params.get('begDate', None)
        endDate             = params.get('endDate', None)
        eventTypeId         = params.get('eventTypeId', None)
        orgStructureId      = params.get('orgStructureId', None)
        personId            = params.get('personId', None)
        specialityId        = params.get('specialityId', None)
        freeInputWork       = params.get('freeInputWork', False)
        freeInputWorkValue  = params.get('freeInputWorkValue', '')
        orgInsurerId        = params.get('orgInsurerId', None)
        confirmation        = params.get('confirmation', False)
        confirmationBegDate = params.get('confirmationBegDate', None)
        confirmationEndDate = params.get('confirmationEndDate', None)
        confirmationType    = params.get('confirmationType', 0)
        refuseType          = params.get('refuseType', None)
        filterBegAge        = params.get('filterBegAge', 0)
        filterEndAge        = params.get('filterEndAge', 150)
        isPeriodOnService   = params.get('isPeriodOnService', False)
        rows = []
        if isPeriodOnService:
            rows.append(u'учитывать период по услуге')
        if begDate:
            rows.append(u'Дата начала периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Дата окончания периода: %s'%forceString(endDate))
        if eventTypeId:
            rows.append(u'Тип события: %s'%forceString(db.translate('EventType', 'id', eventTypeId, 'CONCAT_WS(\' | \', code,name)')))
        if orgStructureId:
            rows.append(u'Подразделение исполнителя: %s'%forceString(db.translate('OrgStructure', 'id', orgStructureId, 'CONCAT_WS(\' | \', code,name)')))
        if personId:
            rows.append(u'Исполнитель: %s'%forceString(db.translate('vrbPerson', 'id', personId, 'name')))
        if specialityId:
            rows.append(u'Специальность исполнителя: %s'%forceString(db.translate('rbSpeciality', 'id', specialityId, 'CONCAT_WS(\' | \', code,name)')))
        if orgInsurerId:
            rows.append(u'Плательщик по договору: %s'%forceString(db.translate('Organisation', 'id', orgInsurerId, 'shortName')))
        if freeInputWork:
            rows.append(u'Место работы по названию: %s'%forceString(freeInputWorkValue))
        if confirmation:
            rows.append(u'Тип подтверждения: %s'%{0: u'без подтверждения',
                                                  1: u'оплаченные',
                                                  2: u'отказанные'}.get(confirmationType, u''))
            if confirmationBegDate:
                rows.append(u'Начало периода подтверждения: %s'%forceString(confirmationBegDate))
            if confirmationEndDate:
                rows.append(u'Окончание периода подтверждения: %s'%forceString(confirmationEndDate))
            if refuseType:
                rows.append(u'Причина отказа: %s'%forceString(db.translate('rbPayRefuseType', 'id', refuseType, 'CONCAT_WS(\' | \', code,name)')))
        if filterBegAge and filterEndAge:
            rows.append(u'Возраст с %s по %s'%(forceString(filterBegAge), forceString(filterEndAge)))
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows
