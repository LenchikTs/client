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
from PyQt4.QtCore import QDateTime, QLocale, QDate

from library.Utils      import forceBool, forceDouble, forceRef, forceString, forceDate, forceInt
from Reports.Report     import CReport
from Reports.ReportView import CPageFormat
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
    serviceGroup = params.get('serviceGroup', None)
    if serviceGroup:
        if serviceGroup == -1:
            cond += u' AND rbService.group_id is NULL'
        else:
            cond += u' AND rbService.group_id = %s'%serviceGroup
    finance = params.get('finance', None)
    if finance:
        cond += u' AND rbFinance.id = %s'%finance
    detailClient = params.get('detailClient', False)
    detailPerson = params.get('detailPerson', False)
    datailVAT    = params.get('datailVAT', False)
    socStatusType = params.get('socStatusType', None)
    groupByMonths = params.get('groupByMonths', False)
    detailEventCount = params.get('detailEventCount', False)
    stmt="""
SELECT
    rbService.code,
    rbService.name,
    %s
    %s
    %s
    %s
    (Account_Item.amount) AS amount,
    (Account_Item.sum) AS sum,
    (Account_Item.payedSum) AS payedSum,
    (Account_Item.uet) AS uet,
    (Account_Item.payedSum !=0) AS exposed,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    Account_Item.price,
    %s
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName,
    Contract.payer_id,
    Organisation.shortName,
    Person.id as personId,
    OrgStructure.id as orgStructureId,
    OrgStructure.name orgStructureName,
    OrgStructure.code orgStructureCode

FROM Account_Item
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN Organisation    ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbService       ON rbService.id = IF(Account_Item.service_id IS NULL, EventType.service_id, Account_Item.service_id)
LEFT JOIN Diagnostic      ON Diagnostic.event_id = Event.id
LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnostic.diagnosisType_id
LEFT JOIN Person          ON Person.id = Diagnostic.person_id
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality    ON rbSpeciality.id = Person.speciality_id
INNER JOIN Client         ON Client.id = Event.client_id
%s
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NULL
    AND Diagnostic.deleted = 0
    AND rbDiagnosisType.code in ('1','2')
    AND %s
    group by Account_Item.id %s
    """
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '',
        '''group_concat(rbSocStatusType.name SEPARATOR ',') as socName,''' if socStatusType else '',
        '''DATE(Event.execDate) as execDate,''' if groupByMonths else '',
        '''Account_Item.VAT,''' if datailVAT else '',
        '''COUNT(Event.id) AS eventCount,''' if detailEventCount else '',
        '''INNER JOIN ClientSocStatus ON ClientSocStatus.client_id=Client.id and ClientSocStatus.socStatusClass_id = %s
        LEFT JOIN rbSocStatusType on ClientSocStatus.socStatusType_id = rbSocStatusType.id''' %(socStatusType)  if socStatusType else '',
        cond,
        ''', Person.id''' if detailPerson else '',))


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
    serviceGroup = params.get('serviceGroup', None)
    if serviceGroup:
        if serviceGroup == -1:
            cond += u' AND rbService.group_id is NULL'
        else:
            cond += u' AND rbService.group_id = %s'%serviceGroup
    finance = params.get('finance', None)
    if finance:
        cond += u' AND rbFinance.id = %s'%finance
    detailClient = params.get('detailClient', False)
    detailPerson = params.get('detailPerson', False)
    datailVAT    = params.get('datailVAT', False)
    socStatusType = params.get('socStatusType', '')
    groupByMonths = params.get('groupByMonths', False)
    detailEventCount = params.get('detailEventCount', False)
    stmt="""
SELECT
    rbService.code,
    rbService.name,
    %s
    %s
    %s
    %s
    (Account_Item.amount) AS amount,
    (Account_Item.sum) AS sum,
    (Account_Item.payedSum) AS payedSum,
    (Account_Item.uet) AS uet,
    (Account_Item.payedSum !=0) AS exposed,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    Account_Item.price,
    %s
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName,
    Contract.payer_id,
    Organisation.shortName,
    Person.id as personId,
    OrgStructure.id as orgStructureId,
    OrgStructure.name orgStructureName,
    OrgStructure.code orgStructureCode

FROM Account_Item
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Contract     ON Contract.id = Account.contract_id
LEFT JOIN Organisation ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance    ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN Event        ON Event.id = Account_Item.event_id
LEFT JOIN Visit        ON Visit.id = Account_Item.visit_id
LEFT JOIN rbService    ON rbService.id = IF(Account_Item.service_id IS NULL, Visit.service_id, Account_Item.service_id)
LEFT JOIN Person       ON Person.id = Visit.person_id
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
INNER JOIN Client      ON Client.id = Event.client_id
%s
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND %s
    group by Account_Item.id %s
    """
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '',
        '''group_concat(rbSocStatusType.name SEPARATOR ',') as socName,''' if socStatusType else '',
        '''DATE(Event.execDate) as execDate,''' if groupByMonths else '',
        '''Account_Item.VAT,''' if datailVAT else '',
        '''COUNT(Event.id) AS eventCount,''' if detailEventCount else '',
        '''INNER JOIN ClientSocStatus ON ClientSocStatus.client_id=Client.id and ClientSocStatus.socStatusClass_id = %s
        LEFT JOIN rbSocStatusType on ClientSocStatus.socStatusType_id = rbSocStatusType.id''' %(socStatusType)  if socStatusType else '',
    cond,
    ''', Person.id''' if detailPerson else '',))


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
    serviceGroup = params.get('serviceGroup', None)
    if serviceGroup:
        if serviceGroup == -1:
            cond += u' AND rbService.group_id is NULL'
        else:
            cond += u' AND rbService.group_id = %s'%serviceGroup
    finance = params.get('finance', None)
    if finance:
        cond += u' AND rbFinance.id = %s'%finance
    detailClient = params.get('detailClient', False)
    detailPerson = params.get('detailPerson', False)
    datailVAT    = params.get('datailVAT', False)
    socStatusType = params.get('socStatusType', [])
    groupByMonths = params.get('groupByMonths', False)
    detailEventCount = params.get('detailEventCount', False)
    stmt="""
SELECT
    rbService.code,
    rbService.name,
    %s
    %s
    %s
    %s
    (Account_Item.amount) AS amount,
    (Account_Item.sum) AS sum,
    (Account_Item.payedSum) AS payedSum,
    (Account_Item.uet) AS uet,
    (Account_Item.payedSum !=0) AS exposed,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    Account_Item.price,
    %s
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName,
    Contract.payer_id,
    Organisation.shortName,
    Person.id as personId,
    OrgStructure.id as orgStructureId,
    OrgStructure.name orgStructureName,
    OrgStructure.code orgStructureCode

FROM Account_Item
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Contract     ON Contract.id = Account.contract_id
LEFT JOIN Organisation ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance    ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN Event        ON Event.id = Account_Item.event_id
LEFT JOIN Action       ON Action.id = Account_Item.action_id
LEFT JOIN ActionType   ON ActionType.id = Action.actionType_id
LEFT JOIN rbService    ON rbService.id = Account_Item.service_id
LEFT JOIN Person       ON Person.id = Action.person_id
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
INNER JOIN Client      ON Client.id = Event.client_id
%s
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NOT NULL
    AND %s
    group by Account_Item.id %s
    """
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '',
        '''group_concat(rbSocStatusType.name SEPARATOR ',') as socName,''' if socStatusType else '',
        '''DATE(Event.execDate) as execDate,''' if groupByMonths else '',
        '''Account_Item.VAT,''' if datailVAT else '',
        '''COUNT(Event.id) AS eventCount,''' if detailEventCount else '',
        '''INNER JOIN ClientSocStatus ON ClientSocStatus.client_id=Client.id and ClientSocStatus.socStatusClass_id = %s
        LEFT JOIN rbSocStatusType on ClientSocStatus.socStatusType_id = rbSocStatusType.id''' %(socStatusType)  if socStatusType else '',
        cond,
        ''', Person.id''' if detailPerson else '',))


class CFinanceSummaryByServices(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по услугам')
        self.datailVAT = False
        self.orientation = CPageFormat.Landscape


    def build(self, description, params):
        reportDataAll = {}
        detailClient  = params.get('detailClient', False)
        detailFinance = params.get('detailFinance', False)
        detalilPayer  = params.get('detailPayer', False)
        self.detailPerson  = params.get('detailPerson', False)
        detailOrgStructure = params.get('detailOrgStructure', False)
        self.datailVAT     = params.get('datailVAT', False)
        self.socStatusType = params.get('socStatusType', [])
        self.groupByMonths = params.get('groupByMonths', False)
        self.detailEventCount   = params.get('detailEventCount', False)
        reportRowSize = (12+self.detailPerson if self.datailVAT else 9+self.detailPerson) + self.detailEventCount*3
        def processQuery(query, reportDataGlobal):
            while query.next():
                record = query.record()
                code        = forceString(record.value('code'))
                name        = forceString(record.value('name'))
                amount      = forceDouble(record.value('amount'))
                price       = forceDouble(record.value('price'))
                personId    = forceDouble(record.value('personId'))
                personName  = forceString(QtGui.qApp.db.translate('vrbPerson', 'id', personId, 'name')) if personId else u''
                VAT         = forceDouble(record.value('VAT'))
                eventCount  = forceInt(record.value('eventCount')) if self.detailEventCount else 0
                financeId   = forceRef(record.value('financeId'))
                financeCode = forceString(record.value('financeCode'))
                financeName = forceString(record.value('financeName'))
                orgStructureId     = forceRef(record.value('orgStructureId'))
                orgStructureName   = forceString(record.value('orgStructureName'))
                orgStructureCode   = forceString(record.value('orgStructureCode'))
                uet                = forceDouble(record.value('uet'))
                if amount == int(amount):
                   amount = int(amount)
                sum         = forceDouble(record.value('sum'))
                payedSum    = forceDouble(record.value('payedSum'))
                exposed     = forceBool(record.value('exposed'))
                refused     = forceBool(record.value('refused'))
                if detailClient:
                    clientInfo = u' '.join(clName for clName in [forceString(record.value('clientLastName')),
                                                                 forceString(record.value('clientFirstName')),
                                                                 forceString(record.value('clientPatrName')),
                                                                 forceString(record.value('clientId'))])
                    if self.detailPerson:
                        key = ((name if name else u'Без указания услуги'), code, price, personName, clientInfo)
                    else:
                        key = ((name if name else u'Без указания услуги'), code, price, clientInfo)
                else:
                    if self.detailPerson:
                        key = ((name if name else u'Без указания услуги'), code, price, personName)
                    else:
                        key = ((name if name else u'Без указания услуги'), code, price)

                if self.groupByMonths:
                    month = forceString(forceDate(record.value('execDate')).toString('yyyy.MM'))
                    reportData = reportDataGlobal.setdefault(month, {})
                else:
                    reportData = reportDataGlobal

                if self.socStatusType:
                    socName = forceString(record.value('socName'))
                    socName = ', '.join(sorted(socName.split(',')))
                    reportSocData = reportData.setdefault(socName, {})
                    reportLine = reportSocData.setdefault(key, [0]*reportRowSize)
                elif detalilPayer:
                    payerId = forceRef(record.value('payer_id'))
                    payerName = forceString(record.value('shortName'))
                    if not detailFinance:
                        reportPayerData = reportData.setdefault((payerId, payerName), {})
                        reportLine = reportPayerData.setdefault(key, [0]*reportRowSize)
                    else:
                        reportPayerData = reportData.setdefault((payerId, payerName), {})
                        reportFinanceData = reportPayerData.setdefault((financeId, financeCode, financeName), {})
                        reportLine = reportFinanceData.setdefault(key, [0]*reportRowSize)
                elif detailFinance:
                    reportFinanceData = reportData.setdefault((financeId, financeCode, financeName), {})
                    reportLine = reportFinanceData.setdefault(key, [0]*reportRowSize)
                elif detailOrgStructure:
                    reportOrgStructureData = reportData.setdefault((orgStructureId, orgStructureCode, orgStructureName), {})
                    reportLine = reportOrgStructureData.setdefault(key, [0]*reportRowSize)
                else:
                    reportLine = reportData.setdefault(key, [0]*reportRowSize)

                if self.datailVAT:
                    index = 0 + self.detailPerson
                    reportLine[index+0] += amount
                    if self.detailEventCount:
                        index += 1
                        reportLine[index+0] += eventCount
                    reportLine[index+1] += uet
                    reportLine[index+2] += sum
                    reportLine[index+3] += ((price*VAT)/(100.0+VAT))*amount

                    if exposed:
                        reportLine[index+4] += amount if sum == payedSum else forceInt(amount-(sum-payedSum)/price)
                        if self.detailEventCount:
                            index += 1
                            reportLine[index+4] += eventCount
                        reportLine[index+5] += uet
                        reportLine[index+6] += payedSum
                        reportLine[index+7] += ((price*VAT)/(100.0+VAT))*amount

                    if refused:
                        index += int(self.detailEventCount and not exposed)
                        reportLine[index+8]  += amount if payedSum==0 else forceInt((sum-payedSum)/price)
                        if self.detailEventCount:
                            index += 1
                            reportLine[index+8] += eventCount
                        reportLine[index+9]  += uet
                        reportLine[index+10] += sum-payedSum
                        reportLine[index+11] += ((price*VAT)/(100.0+VAT))*amount
                else:
                    index = 0 + self.detailPerson
                    reportLine[index+0] += amount
                    if self.detailEventCount:
                        index += 1
                        reportLine[index+0] += eventCount
                    reportLine[index+1] += uet
                    reportLine[index+2] += sum

                    if exposed:
                        reportLine[index+3] += amount if sum == payedSum else forceInt(amount-(sum-payedSum)/price)
                        if self.detailEventCount:
                            index += 1
                            reportLine[index+3] += eventCount
                        reportLine[index+4] += uet
                        reportLine[index+5] += payedSum

                    if refused:
                        index += int(self.detailEventCount and not exposed)
                        reportLine[index+6] += amount if payedSum==0 else forceInt((sum-payedSum)/price)
                        if self.detailEventCount:
                            index += 1
                            reportLine[index+6] += eventCount
                        reportLine[index+7] += uet
                        reportLine[index+8] += sum-payedSum

                if self.socStatusType:
                    reportSocData[key] = reportLine
                    reportData[socName] = reportSocData
                elif detalilPayer:
                    if not detailFinance:
                        reportPayerData[key] = reportLine
                        reportData[(payerId, payerName)] = reportPayerData
                    else:
                        reportFinanceData[key] = reportLine
                        reportPayerData[(financeId, financeCode, financeName)] = reportFinanceData
                        reportData[(payerId, payerName)] = reportPayerData
                elif detailFinance:
                    reportFinanceData[key] = reportLine
                    reportData[(financeId, financeCode, financeName)] = reportFinanceData
                elif detailOrgStructure:
                    reportOrgStructureData[key] = reportLine
                    reportData[(orgStructureId, orgStructureCode, orgStructureName)] = reportOrgStructureData
                else:
                    reportData[key] = reportLine
            return reportDataGlobal

        query = selectDataByEvents(params)
        reportDataAll = processQuery(query, reportDataAll)
        query = selectDataByVisits(params)
        reportDataAll = processQuery(query, reportDataAll)
        query = selectDataByActions(params)
        reportDataAll = processQuery(query, reportDataAll)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()
        if self.datailVAT and not self.detailEventCount:
            procentCode = '10%'
            procentVal  = '5%'
        elif self.detailEventCount and not self.datailVAT:
            procentCode = '11%'
            procentVal  = '4%'
        else:
            procentCode = '5%'
            procentVal  = '7%'
        tableColumns = [
                          ('25%',      [ u'Услуга',   u'наименование'], CReportBase.AlignLeft ),
                          (procentCode,[ u'',         u'код'         ], CReportBase.AlignLeft ),
                          (procentVal, [ u'Тариф',    u''            ], CReportBase.AlignRight ),
                          (procentVal, [ u'Всего',    u'кол-во услуг'], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'УЕТ'         ], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'руб'         ], CReportBase.AlignRight ),
                          (procentVal, [ u'Оплачено', u'кол-во услуг'], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'УЕТ'         ], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'руб'         ], CReportBase.AlignRight ),
                          (procentVal, [ u'Отказано', u'кол-во услуг'], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'УЕТ'         ], CReportBase.AlignRight ),
                          (procentVal, [ u'',         u'руб'         ], CReportBase.AlignRight ),
                       ]
        if self.detailPerson:
            tableColumns.insert(2+(1 if self.socStatusType else 0), (procentVal,  [u'', u'Исполнитель'], CReportBase.AlignRight))
        if self.datailVAT:
            tableColumns.insert(6+self.detailPerson,  (procentVal, [u'', u'НДС'], CReportBase.AlignRight))
            tableColumns.insert(10+self.detailPerson, (procentVal, [u'', u'НДС'], CReportBase.AlignRight))
            tableColumns.insert(14+self.detailPerson, (procentVal, [u'', u'НДС'], CReportBase.AlignRight))
        elif self.socStatusType:
            tableColumns.insert(0, (procentVal,  [u'', u'Соц. статус'], CReportBase.AlignRight))

        if self.detailEventCount:  # Добавить после столбца 'кол-во услуг' столбец 'кол-во случаев'
            for idx in (i for i,item in enumerate(tableColumns) if item[1][1] == u'кол-во услуг'):
                tableColumns.insert(idx+1, (procentVal, [u'', u'кол-во случаев'], CReportBase.AlignRight))

        self.tableColumnsLen = len(tableColumns)
        table = createTable(cursor, tableColumns)
        if self.datailVAT:
            table.mergeCells(0, 0, 1, 2+self.detailPerson)
            table.mergeCells(0, 2+self.detailPerson, 2, 1)
            table.mergeCells(0, 3+self.detailPerson, 1, 4+self.detailEventCount)
            table.mergeCells(0, 7+self.detailPerson+self.detailEventCount, 1, 4+self.detailEventCount)
            table.mergeCells(0, 11, 1, 4)
            if self.detailEventCount:
                table.mergeCells(0, 13, 1, 5)
        elif self.socStatusType:
            table.mergeCells(0, 1, 1, 2+self.detailPerson)
            table.mergeCells(0, 3+self.detailPerson, 2, 1)
            table.mergeCells(0, 4+self.detailPerson, 1, 3+self.detailEventCount)
            table.mergeCells(0, 7+self.detailPerson+self.detailEventCount,    1, 3+self.detailEventCount)
            table.mergeCells(0, 10+self.detailPerson+self.detailEventCount*2, 1, 3+self.detailEventCount)
        else:
            table.mergeCells(0, 0, 1, 2+self.detailPerson)
            table.mergeCells(0, 2+self.detailPerson, 2, 1)
            table.mergeCells(0, 3+self.detailPerson, 1, 3+self.detailEventCount)
            table.mergeCells(0, 6+self.detailPerson+self.detailEventCount,   1, 3+self.detailEventCount)
            table.mergeCells(0, 9+self.detailPerson+self.detailEventCount*2, 1, 3+self.detailEventCount)

        locale = QLocale()
        self.groupRows = 2
        if self.groupByMonths:
            self.groupRows += 1

        def printTableData(table, reportData):
            totalByReport = [0]*reportRowSize
            totalReportPrice = 0
            if self.socStatusType:
                for status in sorted(reportData.keys()):
                    keys = reportData[status].keys()
                    keys.sort()
                    namePrev = u''
                    codePrev = u''
                    for key in keys:
                        name = key[0]
                        code = key[1]
                        price = key[2]
                        if self.detailPerson:
                            personName = key[3]
                        if detailClient:
                            if namePrev != name and codePrev != code:
                                i = table.addRow()
                                table.setText(i, 1, name)
                                table.setText(i, 2, code)
                                namePrev = name
                                codePrev = code
                                table.mergeCells(i, 3, 1, 10)
                            clientInfo  = key[3]
                            i = table.addRow()
                            table.setText(i, 1, clientInfo)
                            if self.detailPerson:
                                table.setText(i, 3, personName)
                            table.setText(i, 3+self.detailPerson, locale.toString(float(price), 'f', 2))
                        else:
                            i = table.addRow()
                            table.setText(i, 1, name)
                            table.setText(i, 2, code)
                            if self.detailPerson:
                                table.setText(i, 3, personName)
                            table.setText(i, 3+self.detailPerson, locale.toString(float(price), 'f', 2))
                        reportLine = reportData[status][key]
                        totalReportPrice += price
                        for j in xrange(0, reportRowSize):
                            if isinstance(reportLine[j], float):
                                table.setText(i, j+4, locale.toString(float(reportLine[j]), 'f', 2))
                            else:
                                table.setText(i, j+4, reportLine[j])
                        for j in xrange(reportRowSize):
                            totalByReport[j] += reportLine[j]
                    table.mergeCells(self.groupRows, 0, i,  1)
                    table.setText(i, 0, status)
                    self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice, 3)
                    self.groupRows = i + (3 if self.groupByMonths else 2)
                    totalByReport = [0]*reportRowSize
                    totalReportPrice = 0
            elif detalilPayer:
                payerKeys = reportData.keys()
                payerKeys.sort()
                prevPayerId = None
                prevPayerRow = 2
                for payerId, payerName in payerKeys:
                    if detailFinance:
                        reportPayerData = reportData.get((payerId, payerName), {})
                        if not reportPayerData:
                            continue
                    else:
                        reportPayerData = reportData.get((payerId, payerName), {})
                        if not reportPayerData:
                            continue
                    if prevPayerId != payerId:
                        i = table.addRow()
                        table.setText(i, 0, payerName, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                        prevPayerId = payerId
                        prevPayerRow = i
                        table.mergeCells(prevPayerRow, 0,  1, self.tableColumnsLen)
                    if detailFinance:
                        financeKeys = reportPayerData.keys()
                        financeKeys.sort()
                        prevFinanceId = None
                        prevFinanceRow = 2
                        for financeId, financeCode, financeName in financeKeys:
                            totalByFinance = [0]*reportRowSize
                            reportFinanceData = reportPayerData.get((financeId, financeCode, financeName), {})
                            if not reportFinanceData:
                                continue
                            if prevFinanceId != financeId:
                                i = table.addRow()
                                table.setText(i, 0, financeName, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                                prevFinanceId = financeId
                                prevFinanceRow = i
                                table.mergeCells(prevFinanceRow, 0,  1, self.tableColumnsLen)
                            keys = reportFinanceData.keys()
                            keys.sort()
                            namePrev = u''
                            codePrev = u''
                            for key in keys:
                                name = key[0]
                                code = key[1]
                                price = key[2]
                                if self.detailPerson:
                                    personName = key[3]
                                if detailClient:
                                    if namePrev != name and codePrev != code:
                                        i = table.addRow()
                                        table.setText(i, 0, name)
                                        table.setText(i, 1, code)
                                        namePrev = name
                                        codePrev = code
                                        table.mergeCells(i, 2, 1, 10)
                                    clientInfo  = key[3]
                                    i = table.addRow()
                                    table.setText(i, 0, clientInfo)
                                    if self.detailPerson:
                                        table.setText(i, 2, personName)
                                    table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                                else:
                                    i = table.addRow()
                                    table.setText(i, 0, name)
                                    table.setText(i, 1, code)
                                    if self.detailPerson:
                                        table.setText(i, 2, personName)
                                    table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                                reportLine = reportFinanceData[key]
                                totalReportPrice += price
                                for j in xrange(0, reportRowSize):
                                    if isinstance(reportLine[j], float):
                                        table.setText(i, j+3, locale.toString(float(reportLine[j]), 'f', 2))
                                    else:
                                        table.setText(i, j+3, reportLine[j])
                                for j in xrange(reportRowSize):
                                    totalByReport[j] += reportLine[j]
                                    totalByFinance[j] += reportLine[j]
                            self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, totalReportPrice)
                        self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
                        totalByReport = [0]*reportRowSize
                        totalReportPrice = 0
                    else:
                        keys = reportPayerData.keys()
                        keys.sort()
                        namePrev = u''
                        codePrev = u''
                        for key in keys:
                            name = key[0]
                            code = key[1]
                            price = key[2]
                            if self.detailPerson:
                                personName = key[3]
                            if detailClient:
                                if namePrev != name and codePrev != code:
                                    i = table.addRow()
                                    table.setText(i, 0, name)
                                    table.setText(i, 1, code)
                                    namePrev = name
                                    codePrev = code
                                    table.mergeCells(i, 2, 1, 10)
                                clientInfo  = key[3]
                                i = table.addRow()
                                table.setText(i, 0, clientInfo)
                                if self.detailPerson:
                                    table.setText(i, 2, personName)
                                table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                            else:
                                i = table.addRow()
                                table.setText(i, 0, name)
                                table.setText(i, 1, code)
                                if self.detailPerson:
                                    table.setText(i, 2, personName)
                                table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                            reportLine = reportPayerData[key]
                            totalReportPrice += price
                            for j in xrange(0, reportRowSize):
                                if isinstance(reportLine[j], float):
                                    table.setText(i, j+3, locale.toString(float(reportLine[j]), 'f', 2))
                                else:
                                    table.setText(i, j+3, reportLine[j])
                            for j in xrange(reportRowSize):
                                totalByReport[j] += reportLine[j]
                        self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
                        totalByReport = [0]*reportRowSize
                        totalReportPrice = 0
            elif detailFinance:
                financeKeys = reportData.keys()
                financeKeys.sort()
                prevFinanceId = None
                prevFinanceRow = 2
                for financeId, financeCode, financeName in financeKeys:
                    totalByFinance = [0]*reportRowSize
                    reportFinanceData = reportData.get((financeId, financeCode, financeName), {})
                    if not reportFinanceData:
                        continue
                    if prevFinanceId != financeId:
                        i = table.addRow()
                        table.setText(i, 0, financeName, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                        prevFinanceId = financeId
                        prevFinanceRow = i
                        table.mergeCells(prevFinanceRow, 0,  1, self.tableColumnsLen)
                    keys = reportFinanceData.keys()
                    keys.sort()
                    namePrev = u''
                    codePrev = u''
                    for key in keys:
                        name = key[0]
                        code = key[1]
                        price = key[2]
                        if self.detailPerson:
                            personName = key[3]
                        if detailClient:
                            if namePrev != name and codePrev != code:
                                i = table.addRow()
                                table.setText(i, 0, name)
                                table.setText(i, 1, code)
                                namePrev = name
                                codePrev = code
                                table.mergeCells(i, 2, 1, 10)
                            clientInfo  = key[3]
                            i = table.addRow()
                            table.setText(i, 0, clientInfo)
                            if self.detailPerson:
                                table.setText(i, 2, personName)
                            table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                        else:
                            i = table.addRow()
                            table.setText(i, 0, name)
                            table.setText(i, 1, code)
                            if self.detailPerson:
                                table.setText(i, 2, personName)
                            table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                        reportLine = reportFinanceData[key]
                        totalReportPrice += price
                        for j in xrange(0, reportRowSize):
                            if isinstance(reportLine[j], float):
                                table.setText(i, j+3, locale.toString(float(reportLine[j]), 'f', 2))
                            else:
                                table.setText(i, j+3, reportLine[j])
                        for j in xrange(reportRowSize):
                            totalByReport[j] += reportLine[j]
                            totalByFinance[j] += reportLine[j]
                    self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, totalReportPrice)
                self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
                totalByReport = [0]*reportRowSize
                totalReportPrice = 0
            elif detailOrgStructure:
                orgStructureKeys = reportData.keys()
                orgStructureKeys.sort()
                prevOrgStructureId = 0
                prevOrgStructureRow = 2
                for orgStructureId, orgStructureCode, orgStructureName in orgStructureKeys:
                    totalByOrgStructure = [0]*reportRowSize
                    reportOrgStructureData = reportData.get((orgStructureId, orgStructureCode, orgStructureName), {})
                    if not reportOrgStructureData:
                        continue
                    if prevOrgStructureId != orgStructureId:
                        i = table.addRow()
                        if not orgStructureId:
                            orgStructureName = u'Не указано'
                        table.setText(i, 0, orgStructureName, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                        prevOrgStructureId = orgStructureId
                        prevOrgStructureRow = i
                        table.mergeCells(prevOrgStructureRow, 0,  1, self.tableColumnsLen)
                    keys = reportOrgStructureData.keys()
                    keys.sort()
                    namePrev = u''
                    codePrev = u''
                    for key in keys:
                        name = key[0]
                        code = key[1]
                        price = key[2]
                        if self.detailPerson:
                            personName = key[3]
                        if detailClient:
                            if namePrev != name and codePrev != code:
                                i = table.addRow()
                                table.setText(i, 0, name)
                                table.setText(i, 1, code)
                                namePrev = name
                                codePrev = code
                                table.mergeCells(i, 2, 1, 10)
                            clientInfo  = key[3]
                            i = table.addRow()
                            table.setText(i, 0, clientInfo)
                            if self.detailPerson:
                                table.setText(i, 2, personName)
                            table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                        else:
                            i = table.addRow()
                            table.setText(i, 0, name)
                            table.setText(i, 1, code)
                            if self.detailPerson:
                                table.setText(i, 2, personName)
                            table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                        reportLine = reportOrgStructureData[key]
                        totalReportPrice += price
                        for j in xrange(0, reportRowSize):
                            if isinstance(reportLine[j], float):
                                table.setText(i, j+3, locale.toString(float(reportLine[j]), 'f', 2))
                            else:
                                table.setText(i, j+3, reportLine[j])
                        for j in xrange(reportRowSize):
                            totalByReport[j] += reportLine[j]
                            totalByOrgStructure[j] += reportLine[j]
                    self.addTotal(table, u'Всего по подразделению %s'%(orgStructureName), totalByOrgStructure, locale, totalReportPrice)
                self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
                totalByReport = [0]*reportRowSize
                totalReportPrice = 0
            else:
                keys = reportData.keys()
                keys.sort()
                namePrev = u''
                codePrev = u''
                for key in keys:
                    name = key[0]
                    code = key[1]
                    price = key[2]
                    if self.detailPerson:
                        personName = key[3]
                    if detailClient:
                        if namePrev != name and codePrev != code:
                            i = table.addRow()
                            table.setText(i, 0, name)
                            table.setText(i, 1, code)
                            namePrev = name
                            codePrev = code
                            table.mergeCells(i, 2, 1, 10)
                        clientInfo  = key[3]
                        i = table.addRow()
                        table.setText(i, 0, clientInfo)
                        if self.detailPerson:
                            table.setText(i, 2, personName)
                        table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                    else:
                        i = table.addRow()
                        table.setText(i, 0, name)
                        table.setText(i, 1, code)
                        if self.detailPerson:
                            table.setText(i, 2, personName)
                        table.setText(i, 2+self.detailPerson, locale.toString(float(price), 'f', 2))
                    reportLine = reportData[key]
                    totalReportPrice += price
                    for j in xrange(0, reportRowSize):
                        if isinstance(reportLine[j], float):
                            table.setText(i, j+3, locale.toString(float(reportLine[j]), 'f', 2))
                        else:
                            table.setText(i, j+3, reportLine[j])
                    for j in xrange(reportRowSize):
                        totalByReport[j] += reportLine[j]
                self.addTotal(table, u'Всего', totalByReport, locale, totalReportPrice)
                totalByReport = [0]*reportRowSize
                totalReportPrice = 0

        if self.groupByMonths:
            for date in sorted(reportDataAll.keys()):
                i = table.addRow()
                month = parseDate(date)
                table.setText(i, 0, month, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                table.mergeCells(i, 0,  1, self.tableColumnsLen)
                printTableData(table, reportDataAll[date])
        else:
            printTableData(table, reportDataAll)

        return doc


    def addTotal(self, table, title, reportLine, locale, totalPrice, width=2):
        i = table.addRow()
        table.mergeCells(i, 0, 1, width)
        table.setText(i, 0, title, CReportBase.TableTotal)
        table.setText(i, width+self.detailPerson, locale.toString(float(totalPrice), 'f', 2))
        endCol = (12+self.detailPerson if self.datailVAT else 9+self.detailPerson) + self.detailEventCount*3
        for j in xrange(0, endCol):
            if isinstance(reportLine[j], float):
                table.setText(i, j+width+1, locale.toString(float(reportLine[j]), 'f', 2))
            else:
                table.setText(i, j+width+1, reportLine[j])


class CFinanceSummaryByServicesEx(CFinanceSummaryByServices):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSummaryByServices.exec_(self)


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate              = params.get('begDate', None)
        endDate              = params.get('endDate', None)
        eventTypeId          = params.get('eventTypeId', None)
        orgStructureId       = params.get('orgStructureId', None)
        personId             = params.get('personId', None)
        specialityId         = params.get('specialityId', None)
        freeInputWork        = params.get('freeInputWork', False)
        freeInputWorkValue   = params.get('freeInputWorkValue', '')
        orgInsurerId         = params.get('orgInsurerId', None)
        confirmation         = params.get('confirmation', False)
        confirmationBegDate  = params.get('confirmationBegDate', None)
        confirmationEndDate  = params.get('confirmationEndDate', None)
        confirmationType     = params.get('confirmationType', 0)
        refuseType           = params.get('refuseType', None)
        isPeriodOnService    = params.get('isPeriodOnService', False)
        clientOrganisationId = params.get('clientOrganisationId', None)
        serviceGroup = params.get('serviceGroup', None)
        finance = params.get('finance', None)

        rows = []
        if isPeriodOnService:
            rows.append(u'учитывать период по услуге')
        if begDate:
            rows.append(u'Дата начала периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Дата окончания периода: %s'%forceString(endDate))
        if eventTypeId:
            rows.append(u'Тип события: %s'%forceString(db.translate('EventType', 'id', eventTypeId, 'CONCAT_WS(\' | \', code,name)')))
        eventTypeList = params.get('eventTypeList', None)
        if eventTypeList:
            tableET = db.table('EventType')
            records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(eventTypeList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            rows.append(u'Тип события:  %s'%(u','.join(name for name in nameList if name)))
        if serviceGroup:
            if serviceGroup!=-1:
                rows.append(u'Группа услуг: %s'%forceString(db.translate('rbServiceGroup', 'id', serviceGroup, 'name')))
            else:
                rows.append(u'Группа услуг: не указана')
        if finance:
            rows.append(u'Тип финансирования: %s'%forceString(db.translate('rbFinance', 'id', finance, 'name')))
        if orgStructureId:
            rows.append(u'Подразделение исполнителя: %s'%forceString(db.translate('OrgStructure', 'id', orgStructureId, 'CONCAT_WS(\' | \', code,name)')))
        if personId:
            rows.append(u'Врач: %s'%forceString(db.translate('vrbPerson', 'id', personId, 'name')))
        if specialityId:
            rows.append(u'Специальность: %s'%forceString(db.translate('rbSpeciality', 'id', specialityId, 'CONCAT_WS(\' | \', code,name)')))
        if orgInsurerId:
            rows.append(u'Плательщик по договору: %s'%forceString(db.translate('Organisation', 'id', orgInsurerId, 'shortName')))
        if clientOrganisationId:
            rows.append(u'Место работы: %s'%forceString(db.translate('Organisation', 'id', clientOrganisationId, 'shortName')))
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
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialog(parent)
        result.setVisiblePeriodOnService(True)
        result.setVisibleServiceGroup(True)
        result.setVisibleFinance(True)
        result.setVisibleDetailPerson(True)
        result.setVisibleDetailOrgStructure(True)
        result.setVisibleClientOrganisation(True)
        result.setVisibleSocStatusParams(False)
        result.setVisibleDetailFinance(True)
        result.setVisibleDetailPayer(True)
        result.setVisibleDetailVAT(True)
        result.setEventTypeVisible(False)
        result.setVisibleDetailMedicalAidKind(False)
        result.setVisibleDetailSpeciality(False)
        result.setVisibleDetailActionType(False)
        result.setEventTypeListVisible(True)
        result.setVisibleDetailEventCount(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinanceSummaryByServices.build(self, '\n'.join(self.getDescription(params)), params)



class CDetailedFinanceSummaryByServices(CFinanceSummaryByServicesEx):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSummaryByServices.exec_(self)

    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialog(parent)
        result.setVisiblePeriodOnService(True)
        result.setVisibleSocStatusParams(True)
        result.setVisibleDetailFinance(True)
        result.setVisibleDetailPayer(True)
        result.setVisibleDetailVAT(True)
        result.setTitle(self.title())
        return result


def parseDate(date):
    return forceString(QDate.fromString(date, 'yyyy.MM').toString('MMMM yyyy'))
