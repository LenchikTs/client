# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime, QLocale

from library.Utils            import firstMonthDay, forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatName, lastMonthDay
from Events.ActionServiceType import CActionServiceType
from Events.Utils             import getWorkEventTypeFilter
from Orgs.Utils               import getOrgStructureDescendants
from Reports.Report           import CReport
from Reports.ReportView       import CPageFormat
from Reports.ReportBase       import CReportBase, createTable
from library.DialogBase       import CDialogBase
from Events.EventTypeListEditorDialog import CEventTypeListEditorDialog

from Ui_FinanceSummarySetupDialog import Ui_FinanceSummarySetupDialog


def getCond(params):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableContract = db.table('Contract')
    tableAccountItem = db.table('Account_Item')
    tablePerson = db.table('Person')
    tableClientWork   = db.table('ClientWork')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')

    cond = [tableAccountItem['reexposeItem_id'].isNull(),
            tableAccountItem['deleted'].eq(0),
            tableAccount['deleted'].eq(0),
           ]
    if params.get('accountItemIdList',  None) is not None:
        cond.append(tableAccountItem['id'].inlist(params['accountItemIdList']))
    else:
        if params.get('accountIdList', None)is not None:
            cond.append(tableAccountItem['master_id'].inlist(params['accountIdList']))
        elif params.get('accountId', None):
            cond.append(tableAccountItem['master_id'].eq(params['accountId']))
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        if not params.get('isPeriodOnService', False):
            if begDate:
                cond.append(tableAccount['date'].ge(begDate))
            if endDate:
                cond.append(tableAccount['date'].lt(endDate.addDays(1)))
        if params.get('orgInsurerId', None):
            print '''params['orgInsurerId'] = %s'''%params['orgInsurerId']
            cond.append(db.joinOr([db.joinAnd([tableContract['id'].isNotNull(),
                                               tableContract['deleted'].eq(0),
                                               tableContract['payer_id'].eq(params['orgInsurerId'])
                                               ]),
                                   db.joinAnd([tableAccount['id'].isNotNull(),
                                               tableAccount['deleted'].eq(0),
                                               tableAccount['payer_id'].eq(params['orgInsurerId']) ])
                                   ]))
    if params.get('eventTypeId', None):
        cond.append(tableEvent['eventType_id'].eq(params['eventTypeId']))
    eventTypeList = params.get('eventTypeList', [])
    if eventTypeList:
        cond.append(tableEvent['eventType_id'].inlist(eventTypeList))
    if params.get('personId', None):
        cond.append(tablePerson['id'].eq(params['personId']))
    else:
        if params.get('orgStructureId', None):
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(params['orgStructureId'])))
        else:
            cond.append(db.joinOr([tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
                                   tablePerson['org_id'].isNull()]))
        if params.get('specialityId', None):
            cond.append(tablePerson['speciality_id'].eq(params['specialityId']))

    if params.get('confirmation', None):
        if params.get('confirmationType', 0) == 1:
            cond.append(tableAccountItem['date'].isNotNull())
            cond.append(tableAccountItem['number'].ne(''))
            cond.append(tableAccountItem['refuseType_id'].isNull())
        elif params.get('confirmationType', 0) == 2:
            cond.append(tableAccountItem['date'].isNotNull())
            cond.append(tableAccountItem['number'].ne(''))
            cond.append(tableAccountItem['refuseType_id'].isNotNull())
        else:
            cond.append(tableAccountItem['number'].eq(''))
        condAIDate = []
        if params.get('confirmationBegDate', None):
            condAIDate.append(tableAccountItem['date'].ge(params['confirmationBegDate']))
        if params.get('confirmationEndDate', None):
            condAIDate.append(tableAccountItem['date'].lt(params['confirmationEndDate'].addDays(1)))
        if params.get('confirmationType', 0) in [1, 2]:
            if condAIDate:
                cond.append(db.joinAnd(condAIDate))
        else:
            if condAIDate:
                cond.append(db.joinOr([tableAccountItem['date'].isNull(), db.joinAnd(condAIDate)]))
        if params.get('refuseType', None):
            cond.append(tableAccountItem['refuseType_id'].eq(params['refuseType']))
    filterSex    = params.get('filterSex', 0)
    filterBegAge = params.get('filterBegAge', 0)
    filterEndAge = params.get('filterEndAge', 150)
    finance = params.get('finance', None)
    if finance:
        cond.append(tableContract['finance_id'].eq(finance))
    if filterSex:
        cond.append(tableClient['sex'].eq(filterSex))
    if filterEndAge and filterBegAge <= filterEndAge:
        cond.append('''age(Client.birthDate, IF(Event.execDate IS NOT NULL, DATE(Event.execDate), DATE(%s))) >= %d
                           AND age(Client.birthDate, IF(Event.execDate IS NOT NULL, DATE(Event.execDate), DATE(%s))) < %d''' % (db.formatDate(QDate.currentDate()), filterBegAge, db.formatDate(QDate.currentDate()), filterEndAge+1))
    clientOrganisationId = params.get('clientOrganisationId', None)
    freeInputWork = params.get('freeInputWork', False)
    freeInputWorkValue = params.get('freeInputWorkValue', '')
    if clientOrganisationId or (freeInputWork and freeInputWorkValue):
        workSubCond = []
        if clientOrganisationId:
            workSubCond.append(tableClientWork['org_id'].eq(clientOrganisationId))
        if (freeInputWork and freeInputWorkValue):
            workSubCond.append(tableClientWork['freeInput'].like(freeInputWorkValue))
        workCond = [db.joinOr(workSubCond),
                    'ClientWork.id = getClientWorkId(Event.client_id)'
                   ]
        cond.append(
                    '''EXISTS(
                    SELECT 1
                    FROM ClientWork
                    WHERE %s
                    )'''%db.joinAnd(workCond)
                   )

    return db.joinAnd(cond)


def selectDataByEvents(params):
    db = QtGui.qApp.db
    isPeriodOnService         = params.get('isPeriodOnService', False)
    detailClient              = params.get('detailClient', False)
    isSharingOfEventsByVisits = params.get('isSharingOfEventsByVisits', False)
    if isSharingOfEventsByVisits:
        AIEventsByVisits = u'''Account_Item.amount/IF((SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0) > 0, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0), 1) AS amount,
                               Account_Item.sum/IF((SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0) > 0, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0), 1) AS sum,
                               Account_Item.uet/IF((SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0) > 0, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0), 1) AS uet,'''
        queryEventsByVisits = u'''LEFT JOIN Visit ON Visit.event_id = Event.id
                                  LEFT JOIN Person ON Person.id = IF(Visit.id IS NULL, Event.execPerson_id, Visit.person_id)'''
    else:
        AIEventsByVisits = u'''Account_Item.amount AS amount,
                               Account_Item.sum AS sum,
                               Account_Item.uet AS uet,'''
        queryEventsByVisits = u'''LEFT JOIN Person ON Person.id = Event.execPerson_id'''
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
    detailCreatePerson = params.get('detailCreatePerson', False)
    if detailCreatePerson:
        colsCreatePerson = u''' vrbPersonWithSpeciality.id AS createPersonId, vrbPersonWithSpeciality.name AS createPersonName, '''
        joinCreatePerson = u''' LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.createPerson_id'''
    else:
        colsCreatePerson = u''
        joinCreatePerson = u''
    finance = params.get('finance', None)
    if finance:
        cond += u' AND Contract.finance_id = %s'%finance

    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    Event.MES_id,
    %s
    mes.MES.code AS mesCode,
    mes.MES.name AS mesName,
    rbMedicalAidType.code AS matCode,
    rbMedicalAidType.name AS matName,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code, Person.id AS personId,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    %s
    (Account_Item.payedSum !=0) AS exposed,
    Account_Item.price,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    (Account_Item.payedSum) AS payedSum,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    OrgStructure.id AS orgStructureId,
    OrgStructure.code AS orgStructureCode,
    OrgStructure.name AS orgStructureName,
    rbFinance.name AS financeName,
    Contract.payer_id,
    %s
    Organisation.shortName

FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN Organisation    ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
%s
%s
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN mes.MES         ON mes.MES.id = Event.MES_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
INNER JOIN Client         ON Client.id = Event.client_id

WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NULL
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '', AIEventsByVisits, colsCreatePerson, joinCreatePerson, queryEventsByVisits, cond))


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
    detailClient    = params.get('detailClient', False)
    detailCreatePerson = params.get('detailCreatePerson', False)
    if detailCreatePerson:
        colsCreatePerson = u''' vrbPersonWithSpeciality.id AS createPersonId, vrbPersonWithSpeciality.name AS createPersonName, '''
        joinCreatePerson = u''' LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.createPerson_id'''
    else:
        colsCreatePerson = u''
        joinCreatePerson = u''
    finance = params.get('finance', None)
    if finance:
        cond += u' AND Contract.finance_id = %s'%finance
    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    Event.MES_id,
    %s
    %s
    mes.MES.code AS mesCode,
    mes.MES.name AS mesName,
    rbMedicalAidType.code AS matCode,
    rbMedicalAidType.name AS matName,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code, Person.id AS personId,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet,
    Account_Item.price,
    (Account_Item.payedSum !=0) AS exposed,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    (Account_Item.payedSum) AS payedSum,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName,
    OrgStructure.id AS orgStructureId,
    OrgStructure.code AS orgStructureCode,
    OrgStructure.name AS orgStructureName,
    Contract.payer_id,
    Organisation.shortName

FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN Organisation    ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
%s
LEFT JOIN Visit           ON Visit.id = Account_Item.visit_id
LEFT JOIN Person          ON Person.id = Visit.person_id
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN mes.MES         ON mes.MES.id = Event.MES_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
INNER JOIN Client         ON Client.id = Event.client_id
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '', colsCreatePerson, joinCreatePerson, cond))


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
    detailClient    = params.get('detailClient', False)
    detailCreatePerson = params.get('detailCreatePerson', False)
    if detailCreatePerson:
        colsCreatePerson = u''' vrbPersonWithSpeciality.id AS createPersonId, vrbPersonWithSpeciality.name AS createPersonName, '''
        joinCreatePerson = u''' LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.createPerson_id'''
    else:
        colsCreatePerson = u''
        joinCreatePerson = u''
    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    Event.MES_id,
    %s
    %s
    mes.MES.code AS mesCode,
    mes.MES.name AS mesName,
    rbMedicalAidType.code AS matCode,
    rbMedicalAidType.name AS matName,
    ActionType.serviceType,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code, Person.id AS personId,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.price,
    Account_Item.uet AS uet,
    (Account_Item.payedSum !=0) AS exposed,
    IF(Account_Item.sum != Account_Item.payedSum,1,0) as refused,
    (Account_Item.payedSum) AS payedSum,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName,
    OrgStructure.id AS orgStructureId,
    OrgStructure.code AS orgStructureCode,
    OrgStructure.name AS orgStructureName,
    Contract.payer_id,
    Organisation.shortName

FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN Organisation    ON Organisation.id = Contract.payer_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
%s
LEFT JOIN Action          ON Action.id = Account_Item.action_id
LEFT JOIN Person          ON Person.id = Action.person_id
LEFT JOIN OrgStructure  ON OrgStructure.id = Person.orgStructure_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
LEFT JOIN ActionType      ON ActionType.id = Action.actionType_id
LEFT JOIN mes.MES         ON mes.MES.id = Event.MES_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
INNER JOIN Client         ON Client.id = Event.client_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NOT NULL
    AND (ActionType.id IS NULL OR ActionType.deleted = 0)
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % ('''Event.client_id,
    Client.lastName AS clientLastName,
    Client.firstName AS clientFirstName,
    Client.patrName AS clientPatrName,
    Client.id AS clientId,''' if detailClient else '', colsCreatePerson, joinCreatePerson, cond))


class CFinanceSummaryByDoctors(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по врачам')
        self.orientation = CPageFormat.Landscape


    def build(self, description, params):
        reportFinanceData = {}
        reportPayerData = {}
        reportData = {}
        detailService   = params.get('detailService', False)
        detailFedTariff = params.get('detailFedTariff', False)
        detailClient    = params.get('detailClient', False)
        detailFinance   = params.get('detailFinance', False)
        detailMedicalAidKind   = params.get('detailMedicalAidKind', False)
        detailSpeciality   = params.get('detailSpeciality', False)
        detailActionType   = params.get('detailActionType', False)
        detailOrgStructure   = params.get('detailOrgStructure', False)
        detailDate      = params.get('detailDate', False)
        detalilPayer    = params.get('detailPayer', False)
        detailCreatePerson        = params.get('detailCreatePerson', False)
        isSharingOfEventsByVisits = params.get('isSharingOfEventsByVisits', False)
        dataLineStep = 4 if detailFedTariff else 3
        reportRowSize = 12 if detailFedTariff else 9

        def processQuery(query, reportData):
            while query.next():
                record = query.record()
                specialityName = forceString(record.value('specialityName'))
                serviceDate = forceDate(record.value('serviceDate'))
                financeId = forceRef(record.value('financeId'))
                financeCode = forceString(record.value('financeCode'))
                financeName = forceString(record.value('financeName'))
                orgStructureId = forceRef(record.value('orgStructureId'))
                orgStructureCode = forceString(record.value('orgStructureCode'))
                orgStructureName = forceString(record.value('orgStructureName'))
                visitId = forceRef(record.value('visit_id'))
                actionId = forceRef(record.value('action_id'))
                lastName = forceString(record.value('lastName'))
                firstName = forceString(record.value('firstName'))
                patrName = forceString(record.value('patrName'))
                personId = forceRef(record.value('personId'))
                code = forceString(record.value('code'))
                serviceId = forceRef(record.value('serviceId'))
                serviceName = forceString(record.value('serviceName'))
                serviceCode = forceString(record.value('serviceCode'))
                matCodeName = forceString(record.value('matCode')) + u'-' + forceString(record.value('matName'))
                serviceType = forceInt(record.value('serviceType'))
                clientInfo = u' '.join(clName for clName in [forceString(record.value('clientLastName')),
                                                             forceString(record.value('clientFirstName')),
                                                             forceString(record.value('clientPatrName')),
                                                             forceString(record.value('clientId'))])
                amount = forceDouble(record.value('amount'))
                if amount == int(amount):
                   amount = int(amount)
                sum = forceDouble(record.value('sum'))
                payedSum = forceDouble(record.value('payedSum'))
                uet = forceDouble(record.value('uet'))
                price       = forceDouble(record.value('price'))
                exposed = forceBool(record.value('exposed'))
                refused = forceBool(record.value('refused'))
                federalPrice = forceDouble(record.value('federalPrice'))
                federalLimitation = forceInt(record.value('federalLimitation'))
                if detailDate:
                    serviceKey = (serviceDate, serviceId, serviceCode, serviceName if serviceId else u'Услуга не указана')
                else:
                    serviceKey = (serviceId, serviceCode, serviceName if serviceId else u'Услуга не указана') if detailService else None
                name = formatName(lastName, firstName, patrName)
                if not actionId and not visitId:
                    serviceTypeName = u'МЭС'
                elif actionId:
                    serviceTypeName = CActionServiceType.text(serviceType)
                else:
                    serviceTypeName = u''
                key = (name if name else u'Без указания врача',
                       code,
                       serviceKey,
                       clientInfo,
                       personId)
                if detailSpeciality:
                    key = list(key)
                    key.insert(0, specialityName if specialityName else u'Без указания специальности')
                    key = tuple(key)
                if detailActionType:
                    key = list(key)
                    key.insert(2+detailSpeciality+detailActionType, serviceTypeName)
                    key = tuple(key)
                if detailMedicalAidKind:
                    key = list(key)
                    key.insert(2+detailSpeciality+detailActionType+detailMedicalAidKind, matCodeName)
                    key = tuple(key)
                if detailCreatePerson:
                    createPersonId = forceRef(record.value('createPersonId'))
                    createPersonName = forceString(record.value('createPersonName'))
                    keyCreatePerson = (createPersonId, createPersonName)
                    reportCreatePerson = reportData.setdefault(keyCreatePerson, {})
                    if detalilPayer:
                        payerId = forceRef(record.value('payer_id'))
                        payerName = forceString(record.value('shortName'))
                        if not detailFinance:
                            reportPayerData = reportCreatePerson.setdefault((payerId, payerName), {})
                            reportLine = reportPayerData.setdefault(key, [0]*reportRowSize)
                        else:
                            reportPayerData = reportCreatePerson.setdefault((payerId, payerName), {})
                            reportFinanceData = reportPayerData.setdefault((financeId, financeCode, financeName), {})
                            reportLine = reportFinanceData.setdefault(key, [0]*reportRowSize)
                    elif detailFinance:
                        reportFinanceData = reportCreatePerson.setdefault((financeId, financeCode, financeName), {})
                        reportLine = reportFinanceData.setdefault(key, [0]*reportRowSize)
                    elif detailOrgStructure:
                        reportOrgStructureData = reportCreatePerson.setdefault((orgStructureId, orgStructureCode, orgStructureName), {})
                        reportLine = reportOrgStructureData.setdefault(key, [0]*reportRowSize)
                    else:
                        reportLine = reportCreatePerson.setdefault(key, [0]*reportRowSize)
                else:
                    if detalilPayer:
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
                if detailFedTariff:
                    actualAmount = federalLimitation if amount > federalLimitation else amount
                    resultFederalPrice = actualAmount*federalPrice
                    reportLine[0] += amount
                    reportLine[1] += uet
                    reportLine[2] += sum
                    reportLine[3] += resultFederalPrice
                    if exposed:
                        reportLine[4] += amount if sum == payedSum else forceInt(amount-(sum-payedSum)/price)
                        reportLine[5] += uet
                        reportLine[6] += payedSum
                        reportLine[7] += resultFederalPrice
                    if refused:
                        reportLine[8]  += amount if payedSum==0 else forceInt((sum-payedSum)/price)
                        reportLine[9]  += uet
                        reportLine[10] += sum-payedSum
                        reportLine[11] += resultFederalPrice
                else:
                    reportLine[0] += amount
                    reportLine[1] += uet
                    reportLine[2] += sum
                    if exposed:
                        reportLine[3] += amount if sum == payedSum else forceInt(amount-(sum-payedSum)/price)
                        reportLine[4] += uet
                        reportLine[5] += payedSum
                    if refused:
                        reportLine[6] += amount if payedSum==0 else forceInt((sum-payedSum)/price)
                        reportLine[7] += uet
                        reportLine[8] += sum-payedSum
                if detailCreatePerson:
                    keyCreatePerson = (createPersonId, createPersonName)
                    reportCreatePerson = reportData.setdefault(keyCreatePerson, {})
                    if detalilPayer:
                        if not detailFinance:
                            reportPayerData[key] = reportLine
                            reportCreatePerson[(payerId, payerName)] = reportPayerData
                        else:
                            reportFinanceData[key] = reportLine
                            reportPayerData[(financeId, financeCode, financeName)] = reportFinanceData
                            reportCreatePerson[(payerId, payerName)] = reportPayerData
                    elif detailFinance:
                        reportFinanceData[key] = reportLine
                        reportCreatePerson[(financeId, financeCode, financeName)] = reportFinanceData
                    elif detailOrgStructure:
                        reportOrgStructureData[key] = reportLine
                        reportCreatePerson[(orgStructureId, orgStructureCode, orgStructureName)] = reportOrgStructureData
                    else:
                        reportCreatePerson[key] = reportLine
                    reportData[keyCreatePerson] = reportCreatePerson
                else:
                    if detalilPayer:
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
            return reportData

        query = selectDataByEvents(params)
        reportData = processQuery(query, reportData)
        query = selectDataByVisits(params)
        reportData = processQuery(query, reportData)
        query = selectDataByActions(params)
        reportData = processQuery(query, reportData)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        descriptionIns = (u'Делить стоимость События по визитам.' if isSharingOfEventsByVisits else u'Не делить стоимость События по визитам.') + u'\n' + description
        cursor.insertText(descriptionIns)
        cursor.insertBlock()

        personColumnWidth = '12%'
        columnWidth = '10%'
        if detailFedTariff:
            columnWidth = '6%'
            personColumnWidth = '8%'
        tableColumns = [
                          (personColumnWidth,  [ u'Врач',     u'ФИО'       ], CReportBase.AlignLeft ),
                          (columnWidth,  [ u'',         u'код'       ], CReportBase.AlignLeft ),
                          ('6%',  [ u'Всего',    u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          (columnWidth,  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'Оплачено', u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          (columnWidth,  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'Отказано', u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          (columnWidth,  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                       ]
        if detailActionType:
            tableColumns.insert(1+detailActionType,  (columnWidth,  [ u'',         u'вид услуги/МЭС'], CReportBase.AlignLeft ))
        if detailMedicalAidKind:
            tableColumns.insert(1+detailActionType+detailMedicalAidKind,  (columnWidth,  [ u'',         u'тип медицинской помощи'], CReportBase.AlignLeft ))
        if detailFedTariff:
            tableColumns.insert(3+detailMedicalAidKind+detailActionType,  ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))
            tableColumns.insert(7+detailMedicalAidKind+detailActionType,  ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))
            tableColumns.insert(11+detailMedicalAidKind+detailActionType, ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))
        if detailDate:
            tableColumns.insert(1,  ('6%', [ u'', u'Дата'], CReportBase.AlignLeft ))
        self.tableColumnsLen = len(tableColumns)
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0,  1, 3+detailMedicalAidKind+detailActionType if detailDate else 2+detailActionType+detailMedicalAidKind)
        table.mergeCells(0, 3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType,  1, dataLineStep)
        if detailDate:
            table.mergeCells(0, 7+detailMedicalAidKind+detailActionType  if detailFedTariff else 6+detailActionType+detailMedicalAidKind,  1, dataLineStep)
            table.mergeCells(0, 11+detailMedicalAidKind+detailActionType if detailFedTariff else 9+detailMedicalAidKind+detailActionType,  1, dataLineStep)
        else:
            table.mergeCells(0, 6+detailMedicalAidKind+detailActionType  if detailFedTariff else 5+detailMedicalAidKind+detailActionType,  1, dataLineStep)
            table.mergeCells(0, 10+detailMedicalAidKind+detailActionType if detailFedTariff else 8+detailMedicalAidKind+detailActionType,  1, dataLineStep)
        prevSpecialityName = None
        prevDoctor = None
        totalBySpeciality = [0]*reportRowSize
        totalByReport     = [0]*reportRowSize
        totalByDoctor     = [0]*reportRowSize
        totalByReportOperator = [0]*reportRowSize
        locale = QLocale()
        font = CReportBase.TableTotal if detailService else None
        if detailCreatePerson:
            createPersonCnt = 1
            createPersonKeys = reportData.keys()
            createPersonKeys.sort(key=lambda x: x[1])
            prevCreatePersonId = None
            prevCreatePersonRow = 2
            for createPersonId, createPersonName in createPersonKeys:
                reportCreatePerson = reportData.get((createPersonId, createPersonName), {})
                if not reportCreatePerson:
                    continue
                firstCreatePerson = True
                if prevCreatePersonId != createPersonId:
                    i = table.addRow()
                    infoCnt = u'Создано оператором №%d'%(createPersonCnt) + u' (' + forceString(createPersonId) + u'; ' + createPersonName + u')'
                    table.setText(i, 0, infoCnt, CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                    createPersonCnt += 1
                    prevCreatePersonId = createPersonId
                    prevCreatePersonRow = i
                    table.mergeCells(prevCreatePersonRow, 0,  1, self.tableColumnsLen)
                if detalilPayer:
                    payerKeys = reportCreatePerson.keys()
                    payerKeys.sort()
                    prevPayerId = None
                    prevPayerRow = 3
                    for payerId, payerName in payerKeys:
                        if detailFinance:
                            reportPayerData = reportCreatePerson.get((payerId, payerName), {})
                            if not reportPayerData:
                                continue
                        else:
                            reportPayerData = reportCreatePerson.get((payerId, payerName), {})
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
                            prevFinanceRow = 3
                            for financeId, financeCode, financeName in financeKeys:
                                firstFinance = True
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
                                doctorNamePrev = None
                                clientInfoPrev = u''
                                doctorNameRow = 4
                                clientNameRow = 5
                                for key in keys:
                                    if detailSpeciality:
                                        specialityName = key[0]
                                    doctorName  = key[0+detailSpeciality]
                                    doctorCode  = key[1+detailSpeciality]
                                    serviceTypeName = key[2+detailSpeciality]
                                    if detailActionType:
                                        serviceTypeName = key[2+detailSpeciality+detailActionType]
                                    if detailMedicalAidKind:
                                        matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    if prevDoctor and prevDoctor != personId:
                                        if not firstFinance:
                                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalByDoctor = [0]*reportRowSize
                                    if prevSpecialityName != specialityName:
                                        if prevSpecialityName is not None:
                                            if not firstFinance and not firstCreatePerson and detailSpeciality:
                                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                            totalBySpeciality = [0]*reportRowSize
                                        self.addSpecialityHeader(table, specialityName)
                                        prevSpecialityName = specialityName
                                    firstFinance = False
                                    firstCreatePerson = False
                                    if not detailService or prevDoctor != personId:
                                        i = table.addRow()
                                        nameShift = 4*' ' if detailService else ''
                                        if doctorNamePrev != personId:
                                            table.setText(i, 0, nameShift+doctorName, font)
                                            table.setText(i, 1, doctorCode, font)
                                            if not detailService:
                                                doctorNamePrev = personId
                                                doctorNameRow = i
                                        if not detailService:
                                            if detailActionType:
                                                table.setText(i, 2, serviceTypeName, font)
                                            if detailMedicalAidKind:
                                                table.setText(i, 2+detailActionType+detailMedicalAidKind, matCodeName, font)
                                        if detailService:
                                            table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                            prevDoctor = personId
                                        if not detailClient:
                                            table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                            table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                                    if detailClient:
                                        if clientInfoPrev != clientInfo:
                                            i = table.addRow()
                                            table.setText(i, 1 if detailDate else 0, clientInfo)
                                            clientInfoPrev = clientInfo
                                            clientNameRow = i
                                            table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                                    if detailService:
                                        i = table.addRow()
                                        if detailDate:
                                            serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                            table.setText(i, 2, forceString(serviceDate))
                                        else:
                                            serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                        table.setText(i, 0, 8*' '+serviceName)
                                        table.setText(i, 1, serviceCode)
                                        if detailActionType:
                                            table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                        if detailMedicalAidKind:
                                            table.setText(i, 3+detailActionType+detailMedicalAidKind if detailDate else 2+detailActionType+detailMedicalAidKind, matCodeName)
                                    if detailClient and not detailService:
                                        i = table.addRow()
                                        table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                    reportLine = reportFinanceData[key]
                                    for j in xrange(0, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(1, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(2, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    if detailFedTariff:
                                        for j in xrange(3, reportRowSize, dataLineStep):
                                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(reportRowSize):
                                        totalBySpeciality[j] += reportLine[j]
                                        totalByReport[j] += reportLine[j]
                                        totalByReportOperator[j] += reportLine[j]
                                        totalByDoctor[j] += reportLine[j]
                                        totalByFinance[j] += reportLine[j]
                                if detailService:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                if detailSpeciality:
                                    self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        else:
                            keys = reportPayerData.keys()
                            keys.sort()
                            doctorNamePrev = None
                            clientInfoPrev = u''
                            doctorNameRow = 3
                            clientNameRow = 4
                            for key in keys:
                                if detailSpeciality:
                                    specialityName = key[0]
                                doctorName  = key[0+detailSpeciality]
                                doctorCode  = key[1+detailSpeciality]
                                serviceTypeName = key[2+detailSpeciality]
                                if detailActionType:
                                    serviceTypeName = key[2+detailSpeciality+detailActionType]
                                if detailMedicalAidKind:
                                    matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                                clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                                personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                                if prevDoctor and prevDoctor != personId:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                    totalByDoctor = [0]*reportRowSize
                                if prevSpecialityName != specialityName:
                                    if prevSpecialityName is not None:
                                        if not firstCreatePerson and detailSpeciality:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                    totalBySpeciality = [0]*reportRowSize
                                    self.addSpecialityHeader(table, specialityName)
                                    prevSpecialityName = specialityName
                                firstCreatePerson = False
                                if not detailService or prevDoctor != personId:
                                    i = table.addRow()
                                    nameShift = 4*' ' if detailService else ''
                                    if doctorNamePrev != personId:
                                        table.setText(i, 0, nameShift+doctorName, font)
                                        table.setText(i, 1, doctorCode, font)
                                        if not detailService:
                                            doctorNamePrev = personId
                                            doctorNameRow = i
                                    if not detailService:
                                        if detailActionType:
                                            table.setText(i, 2+detailActionType if detailDate else 1+detailActionType, serviceTypeName)
                                        if detailMedicalAidKind:
                                            table.setText(i, 2+detailActionType+detailMedicalAidKind if detailDate else 1+detailActionType+detailMedicalAidKind, matCodeName)
                                    if detailService:
                                        table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                        prevDoctor = personId
                                    if not detailClient:
                                        table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                        table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                                if detailClient:
                                    if clientInfoPrev != clientInfo:
                                        i = table.addRow()
                                        table.setText(i, 2 if detailDate else 1 if detailDate else 0, clientInfo)
                                        clientInfoPrev = clientInfo
                                        clientNameRow = i
                                        table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                                if detailService:
                                    i = table.addRow()
                                    if detailDate:
                                        serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                        table.setText(i, 2, forceString(serviceDate))
                                    else:
                                        serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 0, 8*' '+serviceName)
                                    table.setText(i, 1, serviceCode)
                                    if detailActionType:
                                        table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                    if detailMedicalAidKind:
                                        table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                                if detailClient and not detailService:
                                    i = table.addRow()
                                    table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                reportLine = reportPayerData[key]
                                for j in xrange(0, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(1, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(2, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                if detailFedTariff:
                                    for j in xrange(3, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(reportRowSize):
                                    totalBySpeciality[j] += reportLine[j]
                                    totalByReport[j] += reportLine[j]
                                    totalByReportOperator[j] += reportLine[j]
                                    totalByDoctor[j] += reportLine[j]
                            if detailService:
                                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            if detailSpeciality:
                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            prevSpecialityName = None
                    self.addTotal(table, u'Всего создано оператором', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    totalByReport = [0]*reportRowSize
                elif detailFinance:
                        financeKeys = reportCreatePerson.keys()
                        financeKeys.sort()
                        prevFinanceId = None
                        prevFinanceRow = 3
                        for financeId, financeCode, financeName in financeKeys:
                            firstFinance = True
                            totalByFinance = [0]*reportRowSize
                            reportFinanceData = reportCreatePerson.get((financeId, financeCode, financeName), {})
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
                            doctorNamePrev = None
                            clientInfoPrev = u''
                            doctorNameRow = 4
                            clientNameRow = 5
                            for key in keys:
                                if detailSpeciality:
                                    specialityName = key[0]
                                doctorName  = key[0+detailSpeciality]
                                doctorCode  = key[1+detailSpeciality]
                                serviceTypeName = key[2+detailSpeciality]
                                if detailActionType:
                                    serviceTypeName = key[2+detailSpeciality+detailActionType]
                                if detailMedicalAidKind:
                                    matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                                clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                                personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                                if prevDoctor and prevDoctor != personId:
                                    if not firstFinance:
                                        self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                    totalByDoctor = [0]*reportRowSize
                                if detailSpeciality:
                                    if prevSpecialityName != specialityName:
                                        if prevSpecialityName is not None:
                                            if not firstFinance and not firstCreatePerson and detailSpeciality:
                                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                            totalBySpeciality = [0]*reportRowSize
                                        self.addSpecialityHeader(table, specialityName)
                                        prevSpecialityName = specialityName
                                    firstFinance = False
                                    firstCreatePerson = False
                                    if not detailService or prevDoctor != personId:
                                        i = table.addRow()
                                        nameShift = 4*' ' if detailService else ''
                                        if doctorNamePrev != personId:
                                            table.setText(i, 0, nameShift+doctorName, font)
                                            table.setText(i, 1, doctorCode, font)
                                            if not detailService:
                                                doctorNamePrev = personId
                                                doctorNameRow = i
                                        if not detailService:
                                            if detailActionType:
                                                table.setText(i, 2, serviceTypeName, font)
                                            if detailMedicalAidKind:
                                                table.setText(i, 1+detailActionType+detailMedicalAidKind, matCodeName, font)
                                        if detailService:
                                            table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                            prevDoctor = personId
                                        if not detailClient:
                                            table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                            table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                                    if detailClient:
                                        if clientInfoPrev != clientInfo:
                                            i = table.addRow()
                                            table.setText(i, 1 if detailDate else 0, clientInfo)
                                            clientInfoPrev = clientInfo
                                            clientNameRow = i
                                            table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                                    if detailService:
                                        i = table.addRow()
                                        if detailDate:
                                            serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                            table.setText(i, 2, forceString(serviceDate))
                                        else:
                                            serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                        table.setText(i, 0, 8*' '+serviceName)
                                        table.setText(i, 1, serviceCode)
                                    if detailActionType:
                                        table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                    if detailMedicalAidKind:
                                        table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                                    if detailClient and not detailService:
                                        i = table.addRow()
                                        table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                    reportLine = reportFinanceData[key]
                                    for j in xrange(0, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(1, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(2, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    if detailFedTariff:
                                        for j in xrange(3, reportRowSize, dataLineStep):
                                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(reportRowSize):
                                        totalBySpeciality[j] += reportLine[j]
                                        totalByReport[j] += reportLine[j]
                                        totalByReportOperator[j] += reportLine[j]
                                        totalByDoctor[j] += reportLine[j]
                                        totalByFinance[j] += reportLine[j]
                            if detailService:
                                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            if detailSpeciality:
                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                elif detailOrgStructure:
                    orgStructureKeys = reportCreatePerson.keys()
                    orgStructureKeys.sort()
                    prevOrgStructureId = 0
                    prevOrgStructureRow = 3
                    for orgStructureId, orgStructureCode, orgStructureName in orgStructureKeys:
                        firstOrgStructure = True
                        totalByOrgStructure = [0]*reportRowSize
                        reportOrgStructureData = reportCreatePerson.get((orgStructureId, orgStructureCode, orgStructureName), {})
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
                        doctorNamePrev = None
                        clientInfoPrev = u''
                        doctorNameRow = 4
                        clientNameRow = 5
                        for key in keys:
                            if detailSpeciality:
                                specialityName = key[0]
                            doctorName  = key[0+detailSpeciality]
                            doctorCode  = key[1+detailSpeciality]
                            serviceTypeName = key[2+detailSpeciality]
                            if detailActionType:
                                serviceTypeName = key[2+detailSpeciality+detailActionType]
                            if detailMedicalAidKind:
                                matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                            clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                            personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                            if prevDoctor and prevDoctor != personId:
                                if not firstOrgStructure:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                totalByDoctor = [0]*reportRowSize
                            if detailSpeciality:
                                if prevSpecialityName != specialityName:
                                    if prevSpecialityName is not None:
                                        if not firstOrgStructure and not firstCreatePerson and detailSpeciality:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalBySpeciality = [0]*reportRowSize
                                    self.addSpecialityHeader(table, specialityName)
                                    prevSpecialityName = specialityName
                            firstOrgStructure = False
                            firstCreatePerson = False
                            if not detailService or prevDoctor != personId:
                                i = table.addRow()
                                nameShift = 4*' ' if detailService else ''
                                if doctorNamePrev != personId:
                                    table.setText(i, 0, nameShift+doctorName, font)
                                    table.setText(i, 1, doctorCode, font)
                                    if not detailService:
                                        doctorNamePrev = personId
                                        doctorNameRow = i
                                if not detailService:
                                    if detailActionType:
                                        table.setText(i, 2, serviceTypeName, font)
                                    if detailMedicalAidKind:
                                        table.setText(i, 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                if detailService:
                                    table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                    prevDoctor = personId
                                if not detailClient:
                                    table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                    table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                            if detailClient:
                                if clientInfoPrev != clientInfo:
                                    i = table.addRow()
                                    table.setText(i, 1 if detailDate else 0, clientInfo)
                                    clientInfoPrev = clientInfo
                                    clientNameRow = i
                                    table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                            if detailService:
                                i = table.addRow()
                                if detailDate:
                                    serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 2, forceString(serviceDate))
                                else:
                                    serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                table.setText(i, 0, 8*' '+serviceName)
                                table.setText(i, 1, serviceCode)
                                if detailActionType:
                                    table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                if detailMedicalAidKind:
                                    table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                            if detailClient and not detailService:
                                i = table.addRow()
                                table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                            reportLine = reportOrgStructureData[key]
                            for j in xrange(0, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(1, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(2, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            if detailFedTariff:
                                for j in xrange(3, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(reportRowSize):
                                totalBySpeciality[j] += reportLine[j]
                                totalByReport[j] += reportLine[j]
                                totalByReportOperator[j] += reportLine[j]
                                totalByDoctor[j] += reportLine[j]
                                totalByOrgStructure[j] += reportLine[j]
                        if detailService:
                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        if detailSpeciality:
                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        self.addTotal(table, u'Всего по подразделению %s'%(orgStructureName), totalByOrgStructure, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    else:
                        keys = reportCreatePerson.keys()
                        keys.sort()
                        doctorNamePrev = None
                        clientInfoPrev = u''
                        doctorNameRow = 3
                        clientNameRow = 4
                        for key in keys:
                            if detailSpeciality:
                                specialityName = key[0]
                            doctorName  = key[0+detailSpeciality]
                            doctorCode  = key[1+detailSpeciality]
                            serviceTypeName = key[2+detailSpeciality]
                            if detailActionType:
                                serviceTypeName = key[2+detailSpeciality+detailActionType]
                            if detailMedicalAidKind:
                                matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                            clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                            personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                            if prevDoctor and prevDoctor != personId:
                                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                totalByDoctor = [0]*reportRowSize
                            if detailSpeciality:
                                if prevSpecialityName != specialityName:
                                    if prevSpecialityName is not None:
                                        if not firstCreatePerson and detailSpeciality:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalBySpeciality = [0]*reportRowSize
                                self.addSpecialityHeader(table, specialityName)
                                prevSpecialityName = specialityName
                            firstCreatePerson = False
                            if not detailService or prevDoctor != personId:
                                i = table.addRow()
                                nameShift = 4*' ' if detailService else ''
                                if doctorNamePrev != personId:
                                    table.setText(i, 0, nameShift+doctorName, font)
                                    table.setText(i, 1, doctorCode, font)
                                    if not detailService:
                                        doctorNamePrev = personId
                                        doctorNameRow = i
                                if not detailService:
                                    if detailActionType:
                                        table.setText(i, 3 if detailDate else 2, serviceTypeName, font)
                                    if detailMedicalAidKind:
                                        table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                if detailService:
                                    table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                    prevDoctor = personId
                                if not detailClient:
                                    table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                    table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                            if detailClient:
                                if clientInfoPrev != clientInfo:
                                    i = table.addRow()
                                    table.setText(i, 2 if detailDate else 1 if detailDate else 0, clientInfo)
                                    clientInfoPrev = clientInfo
                                    clientNameRow = i
                                    table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                            if detailService:
                                i = table.addRow()
                                if detailDate:
                                    serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 2, forceString(serviceDate))
                                else:
                                    serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                table.setText(i, 0, 8*' '+serviceName)
                                table.setText(i, 1, serviceCode)
                            if detailActionType:
                                table.setText(i, 3 if detailDate else 2, serviceTypeName)
                            if detailMedicalAidKind:
                                table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                            if detailClient and not detailService:
                                i = table.addRow()
                                table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                            reportLine = reportCreatePerson[key]
                            for j in xrange(0, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(1, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(2, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            if detailFedTariff:
                                for j in xrange(3, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(reportRowSize):
                                totalBySpeciality[j] += reportLine[j]
                                totalByReport[j] += reportLine[j]
                                totalByReportOperator[j] += reportLine[j]
                                totalByDoctor[j] += reportLine[j]
                        if detailService:
                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        if detailSpeciality:
                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    self.addTotal(table, u'Всего создано оператором', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    totalByReport = [0]*reportRowSize
                self.addTotal(table, u'Итого по всем операторам', totalByReportOperator, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
            else:
                if detalilPayer:
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
                                firstFinance = True
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
                                doctorNamePrev = None
                                clientInfoPrev = u''
                                doctorNameRow = 3
                                clientNameRow = 4
                                for key in keys:
                                    if detailSpeciality:
                                        specialityName = key[0]
                                    doctorName  = key[0+detailSpeciality]
                                    doctorCode  = key[1+detailSpeciality]
                                    serviceTypeName = key[2+detailSpeciality]
                                    if detailActionType:
                                        serviceTypeName = key[2+detailSpeciality+detailActionType]
                                    if detailMedicalAidKind:
                                        matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                                    if prevDoctor and prevDoctor != personId:
                                        if not firstFinance:
                                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalByDoctor = [0]*reportRowSize
                                    if detailSpeciality:
                                        if prevSpecialityName != specialityName:
                                            if prevSpecialityName is not None:
                                                if not firstFinance and detailSpeciality:
                                                    self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                                totalBySpeciality = [0]*reportRowSize
                                            self.addSpecialityHeader(table, specialityName)
                                            prevSpecialityName = specialityName
                                    firstFinance = False
                                    if not detailService or prevDoctor != personId:
                                        i = table.addRow()
                                        nameShift = 4*' ' if detailService else ''
                                        if doctorNamePrev != personId:
                                            table.setText(i, 0, nameShift+doctorName, font)
                                            table.setText(i, 1, doctorCode, font)
                                            if not detailService:
                                                doctorNamePrev = personId
                                                doctorNameRow = i
                                        if not detailService:
                                            if detailActionType:
                                                table.setText(i, 2, serviceTypeName, font)
                                            if detailMedicalAidKind:
                                                table.setText(i, 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                        if detailService:
                                            table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                        prevDoctor = personId
                                        if not detailClient:
                                            table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                            table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                                    if detailClient:
                                        if clientInfoPrev != clientInfo:
                                            i = table.addRow()
                                            table.setText(i, 1 if detailDate else 0, clientInfo)
                                            clientInfoPrev = clientInfo
                                            clientNameRow = i
                                            table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                                    if detailService:
                                        i = table.addRow()
                                        if detailDate:
                                            serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                            table.setText(i, 2, forceString(serviceDate))
                                        else:
                                            serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                        table.setText(i, 0, 8*' '+serviceName)
                                        table.setText(i, 1, serviceCode)
                                        if detailActionType:
                                            table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                        if detailMedicalAidKind:
                                            table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                                    if detailClient and not detailService:
                                        i = table.addRow()
                                        table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                    reportLine = reportFinanceData[key]
                                    for j in xrange(0, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(1, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(2, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    if detailFedTariff:
                                        for j in xrange(3, reportRowSize, dataLineStep):
                                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                    for j in xrange(reportRowSize):
                                        totalBySpeciality[j] += reportLine[j]
                                        totalByReport[j] += reportLine[j]
                                        totalByDoctor[j] += reportLine[j]
                                        totalByFinance[j] += reportLine[j]
                                if detailService:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                if detailSpeciality:
                                    self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            totalByReport = [0]*reportRowSize
                        else:
                            keys = reportPayerData.keys()
                            keys.sort()
                            doctorNamePrev = None
                            clientInfoPrev = u''
                            doctorNameRow = 2
                            clientNameRow = 3
                            for key in keys:
                                if detailSpeciality:
                                    specialityName = key[0]
                                doctorName  = key[0+detailSpeciality]
                                doctorCode  = key[1+detailSpeciality]
                                serviceTypeName = key[2+detailSpeciality]
                                if detailActionType:
                                    serviceTypeName = key[2+detailSpeciality+detailActionType]
                                if detailMedicalAidKind:
                                    matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                                clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                                personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                                if prevDoctor and prevDoctor != personId:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                    totalByDoctor = [0]*reportRowSize
                                if detailSpeciality:
                                    if prevSpecialityName != specialityName:
                                        if prevSpecialityName is not None and detailSpeciality:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalBySpeciality = [0]*reportRowSize
                                        self.addSpecialityHeader(table, specialityName)
                                        prevSpecialityName = specialityName
                                if not detailService or prevDoctor != personId:
                                    i = table.addRow()
                                    nameShift = 4*' ' if detailService else ''
                                    if doctorNamePrev != personId:
                                        table.setText(i, 0, nameShift+doctorName, font)
                                        table.setText(i, 1, doctorCode, font)
                                        if not detailService:
                                            doctorNamePrev = personId
                                            doctorNameRow = i
                                    if not detailService:
                                        if detailActionType:
                                            table.setText(i, 3 if detailDate else 2, serviceTypeName, font)
                                        if detailMedicalAidKind:
                                            table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                    if detailService:
                                        table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                        prevDoctor = personId
                                    if not detailClient:
                                        table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                        table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                                if detailClient:
                                    if clientInfoPrev != clientInfo:
                                        i = table.addRow()
                                        table.setText(i, 2 if detailDate else 1 if detailDate else 0, clientInfo)
                                        clientInfoPrev = clientInfo
                                        clientNameRow = i
                                        table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                                if detailService:
                                    i = table.addRow()
                                    if detailDate:
                                        serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                        table.setText(i, 2, forceString(serviceDate))
                                    else:
                                        serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 0, 8*' '+serviceName)
                                    table.setText(i, 1, serviceCode)
                                    if detailActionType:
                                        table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                    if detailMedicalAidKind:
                                        table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                                if detailClient and not detailService:
                                    i = table.addRow()
                                    table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                reportLine = reportPayerData[key]
                                for j in xrange(0, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(1, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(2, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                if detailFedTariff:
                                    for j in xrange(3, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(reportRowSize):
                                    totalBySpeciality[j] += reportLine[j]
                                    totalByReport[j] += reportLine[j]
                                    totalByDoctor[j] += reportLine[j]
                            if detailService:
                                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            if detailSpeciality:
                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            prevSpecialityName = None
                            totalByReport = [0]*reportRowSize
                elif detailFinance:
                    financeKeys = reportData.keys()
                    financeKeys.sort()
                    prevFinanceId = None
                    prevFinanceRow = 2
                    for financeId, financeCode, financeName in financeKeys:
                        firstFinance = True
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
                        doctorNamePrev = None
                        clientInfoPrev = u''
                        doctorNameRow = 3
                        clientNameRow = 4
                        for key in keys:
                            if detailSpeciality:
                                specialityName = key[0]
                            doctorName  = key[0+detailSpeciality]
                            doctorCode  = key[1+detailSpeciality]
                            serviceTypeName = key[2+detailSpeciality]
                            if detailActionType:
                                serviceTypeName = key[2+detailSpeciality+detailActionType]
                            if detailMedicalAidKind:
                                matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                            clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                            personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                            if prevDoctor and prevDoctor != personId:
                                if not firstFinance:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                totalByDoctor = [0]*reportRowSize
                            if detailSpeciality:
                                if prevSpecialityName != specialityName:
                                    if prevSpecialityName is not None:
                                        if not firstFinance:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalBySpeciality = [0]*reportRowSize
                                    self.addSpecialityHeader(table, specialityName)
                                    prevSpecialityName = specialityName
                            firstFinance = False
                            if not detailService or prevDoctor != personId:
                                i = table.addRow()
                                nameShift = 4*' ' if detailService else ''
                                if doctorNamePrev != personId:
                                    table.setText(i, 0, nameShift+doctorName, font)
                                    table.setText(i, 1, doctorCode, font)
                                    if not detailService:
                                        doctorNamePrev = personId
                                        doctorNameRow = i
                                if not detailService:
                                    if detailActionType:
                                        table.setText(i, 2, serviceTypeName, font)
                                    if detailMedicalAidKind:
                                        table.setText(i, 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                if detailService:
                                    table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                    prevDoctor = personId
                                if not detailClient:
                                    table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                    table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                            if detailClient:
                                if clientInfoPrev != clientInfo:
                                    i = table.addRow()
                                    table.setText(i, 1 if detailDate else 0, clientInfo)
                                    clientInfoPrev = clientInfo
                                    clientNameRow = i
                                    table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                            if detailService:
                                i = table.addRow()
                                if detailDate:
                                    serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 2, forceString(serviceDate))
                                else:
                                    serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                table.setText(i, 0, 8*' '+serviceName)
                                table.setText(i, 1, serviceCode)
                                if detailActionType:
                                    table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                if detailMedicalAidKind:
                                    table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                                if detailClient and not detailService:
                                    i = table.addRow()
                                    table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                                reportLine = reportFinanceData[key]
                                for j in xrange(0, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(1, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(2, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                if detailFedTariff:
                                    for j in xrange(3, reportRowSize, dataLineStep):
                                        table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                                for j in xrange(reportRowSize):
                                    totalBySpeciality[j] += reportLine[j]
                                    totalByReport[j] += reportLine[j]
                                    totalByDoctor[j] += reportLine[j]
                                    totalByFinance[j] += reportLine[j]
                            if detailService:
                                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            if detailSpeciality:
                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                elif detailOrgStructure:
                    orgStructureKeys = reportData.keys()
                    orgStructureKeys.sort()
                    prevOrgStructureId = 0
                    prevOrgStructureRow = 2
                    for orgStructureId, orgStructureCode, orgStructureName in orgStructureKeys:
                        firstOrgStructure = True
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
                        doctorNamePrev = None
                        clientInfoPrev = u''
                        doctorNameRow = 3
                        clientNameRow = 4
                        for key in keys:
                            if detailSpeciality:
                                specialityName = key[0]
                            doctorName  = key[0+detailSpeciality]
                            doctorCode  = key[1+detailSpeciality]
                            serviceTypeName = key[2+detailSpeciality]
                            if detailActionType:
                                serviceTypeName = key[2+detailSpeciality+detailActionType]
                            if detailMedicalAidKind:
                                matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                            clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                            personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                            if prevDoctor and prevDoctor != personId:
                                if not firstOrgStructure:
                                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                totalByDoctor = [0]*reportRowSize
                            if detailSpeciality:
                                if prevSpecialityName != specialityName:
                                    if prevSpecialityName is not None:
                                        if not firstOrgStructure:
                                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                        totalBySpeciality = [0]*reportRowSize
                                    self.addSpecialityHeader(table, specialityName)
                                    prevSpecialityName = specialityName
                            firstOrgStructure = False
                            if not detailService or prevDoctor != personId:
                                i = table.addRow()
                                nameShift = 4*' ' if detailService else ''
                                if doctorNamePrev != personId:
                                    table.setText(i, 0, nameShift+doctorName, font)
                                    table.setText(i, 1, doctorCode, font)
                                    if not detailService:
                                        doctorNamePrev = personId
                                        doctorNameRow = i
                                if not detailService:
                                    if detailActionType:
                                        table.setText(i, 2, serviceTypeName, font)
                                    if detailMedicalAidKind:
                                        table.setText(i, 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                                if detailService:
                                    table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                    prevDoctor = personId
                                if not detailClient:
                                    table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                    table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                            if detailClient:
                                if clientInfoPrev != clientInfo:
                                    i = table.addRow()
                                    table.setText(i, 1 if detailDate else 0, clientInfo)
                                    clientInfoPrev = clientInfo
                                    clientNameRow = i
                                    table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                            if detailService:
                                i = table.addRow()
                                if detailDate:
                                    serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                    table.setText(i, 2, forceString(serviceDate))
                                else:
                                    serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                table.setText(i, 0, 8*' '+serviceName)
                                table.setText(i, 1, serviceCode)
                                if detailActionType:
                                    table.setText(i, 3 if detailDate else 2, serviceTypeName)
                                if detailMedicalAidKind:
                                    table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                            if detailClient and not detailService:
                                i = table.addRow()
                                table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                            reportLine = reportOrgStructureData[key]
                            for j in xrange(0, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(1, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(2, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            if detailFedTariff:
                                for j in xrange(3, reportRowSize, dataLineStep):
                                    table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                            for j in xrange(reportRowSize):
                                totalBySpeciality[j] += reportLine[j]
                                totalByReport[j] += reportLine[j]
                                totalByDoctor[j] += reportLine[j]
                                totalByOrgStructure[j] += reportLine[j]
                        if detailService:
                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        if detailSpeciality:
                            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                        self.addTotal(table, u'Всего по подразделению %s'%(orgStructureName), totalByOrgStructure, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                else:
                    keys = reportData.keys()
                    keys.sort()
                    doctorNamePrev = None
                    clientInfoPrev = u''
                    doctorNameRow = 2
                    clientNameRow = 3
                    for key in keys:
                        if detailSpeciality:
                            specialityName = key[0]
                        doctorName  = key[0+detailSpeciality]
                        doctorCode  = key[1+detailSpeciality]
                        serviceTypeName = key[2+detailSpeciality]
                        if detailActionType:
                            serviceTypeName = key[2+detailSpeciality+detailActionType]
                        if detailMedicalAidKind:
                            matCodeName = key[2+detailMedicalAidKind+detailSpeciality+detailActionType]
                        clientInfo  = key[3+detailMedicalAidKind+detailSpeciality+detailActionType]
                        personId    = key[4+detailMedicalAidKind+detailSpeciality+detailActionType]
                        if prevDoctor and prevDoctor != personId:
                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                            totalByDoctor = [0]*reportRowSize
                        if detailSpeciality:
                            if prevSpecialityName != specialityName:
                                if prevSpecialityName is not None:
                                    self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                                    totalBySpeciality = [0]*reportRowSize
                                self.addSpecialityHeader(table, specialityName)
                                prevSpecialityName = specialityName
                        if not detailService or prevDoctor != personId:
                            i = table.addRow()
                            nameShift = 4*' ' if detailService else ''
                            if doctorNamePrev != personId:
                                table.setText(i, 0, nameShift+doctorName, font)
                                table.setText(i, 1, doctorCode, font)
                                if not detailService:
                                    doctorNamePrev = personId
                                    doctorNameRow = i
                            if not detailService:
                                if detailActionType:
                                    table.setText(i, 3 if detailDate else 2, serviceTypeName, font)
                                if detailMedicalAidKind:
                                    table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName, font)
                            if detailService:
                                table.mergeCells(i, 2, 1, self.tableColumnsLen-2)
                                prevDoctor = personId
                            if not detailClient:
                                table.mergeCells(doctorNameRow, 0,  i-doctorNameRow+1, 1)
                                table.mergeCells(doctorNameRow, 1,  i-doctorNameRow+1, 1)
                        if detailClient:
                            if clientInfoPrev != clientInfo:
                                i = table.addRow()
                                table.setText(i, 2 if detailDate else 1 if detailDate else 0, clientInfo)
                                clientInfoPrev = clientInfo
                                clientNameRow = i
                                table.mergeCells(clientNameRow, 0,  1, self.tableColumnsLen)
                        if detailService:
                            i = table.addRow()
                            if detailDate:
                                serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                                table.setText(i, 2, forceString(serviceDate))
                        if detailService:
                            if detailDate:
                                serviceDate, serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                            else:
                                serviceId, serviceCode, serviceName = key[2+detailSpeciality]
                            table.setText(i, 0, 8*' '+serviceName)
                            table.setText(i, 1, serviceCode)
                        if detailActionType:
                            table.setText(i, 3 if detailDate else 2, serviceTypeName)
                        if detailMedicalAidKind:
                            table.setText(i, 2+detailMedicalAidKind+detailActionType if detailDate else 1+detailMedicalAidKind+detailActionType, matCodeName)
                        if detailClient and not detailService:
                            i = table.addRow()
                            table.mergeCells(clientNameRow+1, 0, i-clientNameRow, 4)
                        reportLine = reportData[key]
                        for j in xrange(0, reportRowSize, dataLineStep):
                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                        for j in xrange(1, reportRowSize, dataLineStep):
                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                        for j in xrange(2, reportRowSize, dataLineStep):
                            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                        if detailFedTariff:
                            for j in xrange(3, reportRowSize, dataLineStep):
                                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
                        for j in xrange(reportRowSize):
                            totalBySpeciality[j] += reportLine[j]
                            totalByReport[j] += reportLine[j]
                            totalByDoctor[j] += reportLine[j]
                    if detailService:
                        self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    if detailSpeciality:
                        self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
                    self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind)
        return doc


    def addSpecialityHeader(self, table, specialityName):
        i = table.addRow()
        table.mergeCells(i, 0, 1, self.tableColumnsLen)
        table.setText(i, 0, specialityName, CReportBase.TableHeader)


    def addTotal(self, table, title, reportLine, locale, dataLineStep, detailClient, detailDate, detailActionType, detailMedicalAidKind):
        reportRowSize = len(reportLine)
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1 if detailDate else 0, title, CReportBase.TableTotal)
        for j in xrange(0, reportRowSize, dataLineStep):
            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
        for j in xrange(1, reportRowSize, dataLineStep):
            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
        for j in xrange(2, reportRowSize, dataLineStep):
            table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))
        if dataLineStep == 4:
            for j in xrange(3, reportRowSize, dataLineStep):
                table.setText(i, j+(3+detailMedicalAidKind+detailActionType if detailDate else 2+detailMedicalAidKind+detailActionType), locale.toString(float(reportLine[j]), 'f', 2))


class CFinanceSummaryByDoctorsEx(CFinanceSummaryByDoctors):
    def __init__(self, parent):
        CFinanceSummaryByDoctors.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по врачам за период')


    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSummaryByDoctors.exec_(self)


    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialog(parent)
        result.setVisibleDetailService(True)
        result.setVisibleClientOrganisation(True)
        result.setVisibleDetailFedTariff(True)
        result.setVisiblePeriodOnService(True)
        result.setVisibleDetailFinance(True)
        result.setVisibleDetailPayer(True)
        result.setVisibleDetailOrgStructure(True)
        result.setVisibleFinance(True)
        result.setVisibleDetailDate(True)
        result.setSharingOfEventsByVisits(True)
        result.setVisibleAgeFilter(True)
        result.setVisibleSexFilter(True)
        result.setEventTypeVisible(False)
        result.setVisibleDetailMedicalAidKind(True)
        result.setVisibleDetailSpeciality(True)
        result.setVisibleDetailActionType(True)
        result.setEventTypeListVisible(True)
        result.setDetailCreatePerson(True)
        result.setTitle(self.title())
        return result


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate              = params.get('begDate', None)
        endDate              = params.get('endDate', None)
        eventTypeId          = params.get('eventTypeId', None)
        orgStructureId       = params.get('orgStructureId', None)
        finance       = params.get('finance', None)
        personId             = params.get('personId', None)
        specialityId         = params.get('specialityId', None)
        clientOrganisationId = params.get('clientOrganisationId', None)
        freeInputWork        = params.get('freeInputWork', False)
        freeInputWorkValue   = params.get('freeInputWorkValue', '')
        orgInsurerId         = params.get('orgInsurerId', None)
        confirmation         = params.get('confirmation', False)
        confirmationBegDate  = params.get('confirmationBegDate', None)
        confirmationEndDate  = params.get('confirmationEndDate', None)
        confirmationType     = params.get('confirmationType', 0)
        refuseType           = params.get('refuseType', None)
        filterBegAge         = params.get('filterBegAge', 0)
        filterEndAge         = params.get('filterEndAge', 150)
        isPeriodOnService    = params.get('isPeriodOnService', False)
        filterSex            = params.get('filterSex', 0)
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
        if filterEndAge and filterBegAge <= filterEndAge:
            rows.append(u'Возраст с %s по %s'%(forceString(filterBegAge), forceString(filterEndAge)))
        if filterSex:
            rows.append(u'Пол %s'%([u'не задано', u'мужской', u'женский'][filterSex]))
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinanceSummaryByDoctors.build(self, '\n'.join(self.getDescription(params)), params)


class CFinanceSummarySetupDialog(CDialogBase, Ui_FinanceSummarySetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.setSpecialityVisible(True)
        self.cmbServiceGroup.setTable('rbServiceGroup', True)
        self.cmbServiceGroup.setSpecialValues([(-1, '-', u'не указано')])
        self.cmbFinance.setTable('rbFinance', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.setOrgStructureVisible(True)
        self.cmbInsurerDoctors.setAddNone(True)
        self.setInsurerDoctorsVisible(True)
        self.cmbRefuseType.setTable('rbPayRefuseType', True)
        self.cmbConfirmationType.addItem(u'без подтверждения')
        self.cmbConfirmationType.addItem(u'оплаченные')
        self.cmbConfirmationType.addItem(u'отказанные')
        self._visibleServiceGroup = False
        self.setVisibleServiceGroup(self._visibleServiceGroup)
        self._visibleFinance = False
        self.setVisibleFinance(self._visibleFinance)
        self._visibleDetailPerson = False
        self.setVisibleDetailPerson(self._visibleDetailPerson)
        self._visibleDetailOrgStructure = False
        self.setVisibleDetailOrgStructure(self._visibleDetailOrgStructure)
        self._visibleDetailService = False
        self.setVisibleDetailService(self._visibleDetailService)
        self._visibleClientOrganisation = False
        self.setVisibleClientOrganisation(self._visibleClientOrganisation)
        self._visibleDetailFedTariff = False
        self.setVisibleDetailFedTariff(self._visibleDetailFedTariff)
        self._visibleAgeFilter = False
        self.setVisibleAgeFilter(self._visibleAgeFilter)
        self._visibleSexFilter = False
        self.setVisibleSexFilter(self._visibleSexFilter)
        self._visibleDetailEventCount = False
        self.setVisibleDetailEventCount(self._visibleDetailEventCount)
        self.setVisiblePeriodOnService(False)
        self.cmbSocStatusType.setTable('rbSocStatusClass', True, filter='group_id IS NULL')
        self.setVisibleSocStatusParams(False)
        self.setVisibleDetailFinance(False)
        self.setVisibleDetailMedicalAidKind(True)
        self.setVisibleDetailSpeciality(True)
        self.setVisibleDetailActionType(True)
        self.setVisibleDetailDate(False)
        self.setVisibleDetailPayer(False)
        self.setSharingOfEventsByVisits(False)
        self.setVisibleDetailVAT(False)
        self.setEventTypeVisible(True)
        self.setEventTypeListVisible(False)
        self.setDetailCreatePerson(False)
        self.setPersonVisible(True)
        self.setDetailClientVisible(True)
        self.setFreeInputWorkVisible(True)
        self.eventTypeList = []


    def setOrgStructureVisible(self, value):
        self.orgStructureVisible = value
        self.lblOrgStructure.setVisible(value)
        self.cmbOrgStructure.setVisible(value)


    def setSpecialityVisible(self, value):
        self.specialityVisible = value
        self.lblSpeciality.setVisible(value)
        self.cmbSpeciality.setVisible(value)


    def setPersonVisible(self, value):
        self.personVisible = value
        self.lblPerson.setVisible(value)
        self.cmbPerson.setVisible(value)


    def setDetailCreatePerson(self, value):
        self.detailCreatePersonVisible = value
        self.chkDetailCreatePerson.setVisible(value)


    def setDetailClientVisible(self, value):
        self.detailClientVisible = value
        self.chkDetailClient.setVisible(value)


    def setFreeInputWorkVisible(self, value):
        self.freeInputWorkVisibleVisible = value
        self.chkFreeInputWork.setVisible(value)
        self.edtFreeInputWork.setVisible(value)


    def setInsurerDoctorsVisible(self, value):
        self.insurerDoctorsVisible = value
        self.lblInsurerDoctors.setVisible(value)
        self.cmbInsurerDoctors.setVisible(value)


    def setEventTypeVisible(self, value=True):
        self.eventTypeVisible = value
        self.cmbEventType.setVisible(value)
        self.lblEventType.setVisible(value)


    def setEventTypeListVisible(self, value=True):
        self.eventTypeListVisible = value
        self.btnEventTypeList.setVisible(value)
        self.lblEventTypeList.setVisible(value)


    def setSharingOfEventsByVisits(self, value):
        self._visibleEventsByVisits = value
        self.chkSharingOfEventsByVisits.setVisible(value)
        if not value:
            self.chkSharingOfEventsByVisits.setChecked(False)


    def setVisibleDetailVAT(self, value):
        self._visibleDetailVAT = value
        self.chkDetailVAT.setVisible(value)
        if not value:
            self.chkDetailVAT.setChecked(False)


    def setVisibleDetailEventCount(self, value):
        self._visibleDetailEventCount = value
        self.chkDetailEventCount.setVisible(value)
        if not value:
            self.chkDetailEventCount.setChecked(False)


    def setVisibleDetailDate(self, value):
        self._visibleDetailDate = value
        self.chkDetailDate.setVisible(value)
        if not value:
            self.chkDetailDate.setChecked(False)


    def setVisibleDetailFinance(self, value):
        self._visibleDetailFinance = value
        self.chkDetailFinance.setVisible(value)
        if not value:
            self.chkDetailFinance.setChecked(False)


    def setVisibleDetailMedicalAidKind(self, value):
        self._visibleDetailMedicalAidKind = value
        self.chkDetailMedicalAidKind.setVisible(value)


    def setVisibleDetailSpeciality(self, value):
        self._visibleDetailSpeciality = value
        self.chkDetailSpeciality.setVisible(value)


    def setVisibleDetailActionType(self, value):
        self._visibleDetailActionType = value
        self.chkDetailActionType.setVisible(value)


    def setVisibleDetailPayer(self, value):
        self._visibleDetailPayer = value
        self.chkDetailPayer.setVisible(value)
        if not value:
            self.chkDetailPayer.setChecked(False)


    def setVisibleDetailFedTariff(self, value):
        self._visibleDetailFedTariff = value
        self.chkDetailFedTariff.setVisible(value)


    def setVisibleServiceGroup(self, value):
        self._visibleServiceGroup = value
        self.lblServiceGroup.setVisible(value)
        self.cmbServiceGroup.setVisible(value)


    def setVisibleDetailService(self, value):
        self._visibleDetailService = value
        self.chkDetailService.setVisible(value)


    def setVisibleFinance(self, value):
        self._visibleFinance = value
        self.lblFinance.setVisible(value)
        self.cmbFinance.setVisible(value)


    def setVisibleDetailPerson(self, value):
        self._visibleDetailPerson = value
        self.chkDetailPerson.setVisible(value)


    def setVisibleDetailOrgStructure(self, value):
        self._visibleDetailOrgStructure = value
        self.chkDetailOrgStructure.setVisible(value)


    def setVisibleClientOrganisation(self, value):
        self._visibleClientOrganisation = value
        self.cmbClientOrganisation.setVisible(value)
        self.lblClientOrganisation.setVisible(value)


    def setVisibleSexFilter(self, value):
        self._visibleSexFilter = value
        self.lblFilterSexFrom.setVisible(value)
        self.cmbFilterSex.setVisible(value)


    def setVisibleAgeFilter(self, value):
        self._visibleAgeFilter = value
        self.lblFilterAgeFrom.setVisible(value)
        self.edtFilterBegAge.setVisible(value)
        self.lblFilterAgeTo.setVisible(value)
        self.edtFilterEndAge.setVisible(value)


    def setVisiblePeriodOnService(self, value):
        self._visiblePeriodOnService = value
        self.chkPeriodOnService.setVisible(value)
        self.chkPeriodOnService.setChecked(False)



    def setVisibleSocStatusParams(self, value):
        self._visibleSocStatus = value
        self.chkDetailedSocStatus.setVisible(value)
        self.chkDetailedSocStatus.setChecked(False)
        self.cmbSocStatusType.setVisible(value)
        self.chkGroupByMonths.setVisible(value)
        self.chkGroupByMonths.setChecked(False)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        if self.eventTypeVisible:
            self.cmbEventType.setValue(params.get('eventTypeId', None))
        if self.orgStructureVisible:
            self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        if self.specialityVisible:
            self.cmbSpeciality.setValue(params.get('specialityId', None))
        if self.personVisible:
            self.cmbPerson.setValue(params.get('personId', None))
        if self.insurerDoctorsVisible:
            self.cmbInsurerDoctors.setValue(params.get('orgInsurerId', None))
        self.chkConfirmation.setChecked(params.get('confirmation', False))
        self.edtConfirmationBegDate.setDate(params.get('confirmationBegDate', firstMonthDay(date)))
        self.edtConfirmationEndDate.setDate(params.get('confirmationEndDate', lastMonthDay(date)))
        self.cmbConfirmationType.setCurrentIndex(params.get('confirmationType', 0))
        self.cmbRefuseType.setValue(params.get('refuseType', None))
        self.chkDetailService.setChecked(params.get('detailService', False))
        self.chkDetailFinance.setChecked(params.get('detailFinance', False))
        self.chkDetailMedicalAidKind.setChecked(params.get('detailMedicalAidKind', False))
        self.chkDetailSpeciality.setChecked(params.get('detailSpeciality', False))
        self.chkDetailActionType.setChecked(params.get('detailActionType', False))
        self.chkDetailPayer.setChecked(params.get('detailPayer', False))
        self.chkDetailDate.setChecked(params.get('detailDate', False))
        self.cmbClientOrganisation.setValue(params.get('clientOrganisationId', None))
        if self.freeInputWorkVisibleVisible:
            self.chkFreeInputWork.setChecked(params.get('freeInputWork', False))
        self.edtFreeInputWork.setText(params.get('freeInputWorkValue', ''))
        self.chkDetailFedTariff.setChecked(params.get('detailFedTariff', False))
        if self.detailClientVisible:
            self.chkDetailClient.setChecked(params.get('detailClient', False))
        if self._visibleSexFilter:
            self.cmbFilterSex.setCurrentIndex(params.get('filterSex', 0))
        if self._visibleDetailEventCount:
            self.chkDetailEventCount.setChecked(params.get('detailEventCount', False))
        if self._visibleAgeFilter:
            self.edtFilterBegAge.setValue(params.get('filterBegAge', 0))
            self.edtFilterEndAge.setValue(params.get('filterEndAge', 150))
        if self._visiblePeriodOnService:
            self.chkPeriodOnService.setChecked(params.get('isPeriodOnService', False))
        if self._visibleEventsByVisits:
            self.chkSharingOfEventsByVisits.setChecked(params.get('isSharingOfEventsByVisits', False))
        if self._visibleDetailVAT:
            self.chkDetailVAT.setChecked(params.get('datailVAT', False))
        if self._visibleSocStatus:
            self.chkDetailedSocStatus.setChecked(params.get('detailedSocStatus', False))
            self.cmbSocStatusType.setValue(params.get('socStatusType', None))
        self.chkGroupByMonths.setChecked(params.get('groupByMonths', False))
        if self.eventTypeListVisible:
            self.eventTypeList =  params.get('eventTypeList', [])
            if self.eventTypeList:
                db = QtGui.qApp.db
                tableET = db.table('EventType')
                records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(self.eventTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblEventTypeList.setText(u','.join(name for name in nameList if name))
            else:
                self.lblEventTypeList.setText(u'не задано')
        if self.detailCreatePersonVisible:
            self.chkDetailCreatePerson.setChecked(params.get('detailCreatePerson', False))
        if self._visibleDetailPerson:
            self.chkDetailPerson.setChecked(params.get('detailPerson', False))
        if self._visibleDetailOrgStructure:
            self.chkDetailOrgStructure.setChecked(params.get('detailOrgStructure', False))
        if self._visibleServiceGroup:
            self.cmbServiceGroup.setValue(params.get('serviceGroup', None))
        if self._visibleFinance:
            self.cmbFinance.setValue(params.get('finance', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        if self.eventTypeVisible:
            result['eventTypeId'] = self.cmbEventType.value()
        if self.orgStructureVisible:
            result['orgStructureId'] = self.cmbOrgStructure.value()
        if self.specialityVisible:
            result['specialityId'] = self.cmbSpeciality.value()
        if self.personVisible:
            result['personId'] = self.cmbPerson.value()
        if self.insurerDoctorsVisible:
            result['orgInsurerId'] = self.cmbInsurerDoctors.value()
        result['confirmation'] = self.chkConfirmation.isChecked()
        result['confirmationType'] = self.cmbConfirmationType.currentIndex()
        result['confirmationBegDate'] = self.edtConfirmationBegDate.date()
        result['confirmationEndDate'] = self.edtConfirmationEndDate.date()
        result['refuseType'] = self.cmbRefuseType.value()
        if self.detailClientVisible:
            result['detailClient'] = self.chkDetailClient.isChecked()
        if self.freeInputWorkVisibleVisible:
            result['freeInputWork'] = self.chkFreeInputWork.isChecked()
            result['freeInputWorkValue'] = forceStringEx(self.edtFreeInputWork.text())
        if self._visiblePeriodOnService:
            result['isPeriodOnService'] = self.chkPeriodOnService.isChecked()

        if self._visibleDetailService:
            result['detailService'] = self.chkDetailService.isChecked()

        if self._visibleServiceGroup:
            result['serviceGroup'] = self.cmbServiceGroup.value()

        if self._visibleFinance:
            result['finance'] = self.cmbFinance.value()

        if self._visibleDetailPerson:
            result['detailPerson'] = self.chkDetailPerson.isChecked()

        if self._visibleDetailOrgStructure:
            result['detailOrgStructure'] = self.chkDetailOrgStructure.isChecked()

        if self._visibleClientOrganisation:
            result['clientOrganisationId'] = self.cmbClientOrganisation.value()

        if self._visibleDetailFedTariff:
            result['detailFedTariff'] = self.chkDetailFedTariff.isChecked()

        result['detailClientSex'] = False
        if self._visibleSexFilter:
            result['detailClientSex'] = forceBool(self.cmbFilterSex.currentIndex())
            result['filterSex'] = self.cmbFilterSex.currentIndex()

        if self._visibleDetailEventCount:
            result['detailEventCount'] = self.chkDetailEventCount.isChecked()

        result['detailClientAge'] = False
        if self._visibleAgeFilter:
            result['filterBegAge'] = self.edtFilterBegAge.value()
            result['filterEndAge'] = self.edtFilterEndAge.value()
            if self.edtFilterEndAge.value():
                result['detailClientAge'] = True

        if self._visibleDetailFinance:
            result['detailFinance'] = self.chkDetailFinance.isChecked()

        if self._visibleDetailMedicalAidKind:
            result['detailMedicalAidKind'] = self.chkDetailMedicalAidKind.isChecked()

        if self._visibleDetailSpeciality:
            result['detailSpeciality'] = self.chkDetailSpeciality.isChecked()

        if self._visibleDetailActionType:
            result['detailActionType'] = self.chkDetailActionType.isChecked()

        if self._visibleDetailPayer:
            result['detailPayer'] = self.chkDetailPayer.isChecked()

        if self._visibleDetailDate:
            result['detailDate'] = self.chkDetailDate.isChecked()

        if self._visibleEventsByVisits:
            result['isSharingOfEventsByVisits'] = self.chkSharingOfEventsByVisits.isChecked()

        if self._visibleDetailVAT:
            result['datailVAT'] = self.chkDetailVAT.isChecked()

        if self._visibleSocStatus:
            result['detailedSocStatus'] = self.chkDetailedSocStatus.isChecked()
            result['socStatusType'] = self.cmbSocStatusType.value()

        result['groupByMonths'] = self.chkGroupByMonths.isChecked()

        if self.eventTypeListVisible:
            result['eventTypeList'] = self.eventTypeList

        if self.detailCreatePersonVisible:
            result['detailCreatePerson'] = self.chkDetailCreatePerson.isChecked()

        return result


    def onStateChanged(self, state):
        self.lblConfirmationType.setEnabled(state)
        self.lblBegDateConfirmation.setEnabled(state)
        self.lblEndDateConfirmation.setEnabled(state)
        self.lblRefuseType.setEnabled(state)
        self.cmbConfirmationType.setEnabled(state)
        self.edtConfirmationBegDate.setEnabled(state)
        self.edtConfirmationEndDate.setEnabled(state)
        self.cmbRefuseType.setEnabled(state)


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)


    @pyqtSignature('bool')
    def on_chkDetailService_toggled(self, checked):
        self.chkDetailDate.setEnabled(checked and self.chkDetailClient.isChecked())


    @pyqtSignature('bool')
    def on_chkDetailClient_toggled(self, checked):
        self.chkDetailDate.setEnabled(checked and self.chkDetailService.isChecked())


    @pyqtSignature('')
    def on_btnEventTypeList_clicked(self):
        self.eventTypeList = []
        self.lblEventTypeList.setText(u'не задано')
        filter = getWorkEventTypeFilter(isApplyActive=True)
        dialog = CEventTypeListEditorDialog(self, filter)
        if dialog.exec_():
            self.eventTypeList = dialog.values()
            if self.eventTypeList:
                db = QtGui.qApp.db
                tableET = db.table('EventType')
                records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(self.eventTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblEventTypeList.setText(u','.join(name for name in nameList if name))

