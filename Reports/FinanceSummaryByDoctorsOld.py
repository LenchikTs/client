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
from PyQt4.QtCore import *

from Reports.Report     import *
from Reports.ReportBase import CReportBase, createTable

from library.Utils      import *
from Orgs.Utils import getOrgStructureDescendants
from Ui_FinanceSummarySetupDialogOld import Ui_FinanceSummarySetupDialogOld


def getCond(params):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableContract = db.table('Contract')
    tableAccountItem = db.table('Account_Item')
    tablePerson = db.table('Person')
    tableClientWork   = db.table('ClientWork')

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

        if params.get('begDate', None):
            cond.append(tableAccount['date'].ge(params['begDate']))
        if params.get('endDate', None):
            cond.append(tableAccount['date'].lt(params['endDate'].addDays(1)))
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

        if params.get('confirmationBegDate', None):
            cond.append(tableAccountItem['date'].ge(params['confirmationBegDate']))
        if params.get('confirmationEndDate', None):
            cond.append(tableAccountItem['date'].lt(params['confirmationEndDate'].addDays(1)))

        if params.get('refuseType', None) != 0:
            cond.append(tableAccountItem['refuseType_id'].eq(params['refuseType']))

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

#    SUM(Account_Item.amount/(SELECT
#                            COUNT(D.id)
#                          FROM Diagnostic AS D
#                          LEFT JOIN rbDiagnosisType AS DT ON DT.id = D.diagnosisType_id
#                          WHERE DT.code in ('1','2') AND D.event_id = Event.id AND D.deleted=0
#                         )) AS amount,
#    SUM(Account_Item.sum/(SELECT
#                            COUNT(D.id)
#                          FROM Diagnostic AS D
#                          LEFT JOIN rbDiagnosisType AS DT ON DT.id = D.diagnosisType_id
#                          WHERE DT.code in ('1','2') AND D.event_id = Event.id AND D.deleted=0
#                         )) AS sum,



def selectDataByEvents(params):
    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    Account_Item.amount/IF(Visit.id IS NULL, 1, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0 )) AS amount,
    Account_Item.sum/IF(Visit.id IS NULL, 1, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0 )) AS sum,
    Account_Item.uet/IF(Visit.id IS NULL, 1, (SELECT COUNT(1) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted=0 )) AS uet,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NULL) AS exposed,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NOT NULL) AS refused,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName
FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN Visit           ON Visit.event_id = Event.id
LEFT JOIN Person          ON Person.id = IF(Visit.id IS NULL, Event.execPerson_id, Visit.person_id)
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NULL
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


def selectDataByVisits(params):
    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NULL) AS exposed,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NOT NULL) as refused,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName
FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN Visit           ON Visit.id = Account_Item.visit_id
LEFT JOIN Person          ON Person.id = Visit.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


def selectDataByActions(params):
    stmt="""
SELECT
    rbSpeciality.name as specialityName,
    Person.speciality_id as speciality_id,
    Person.lastName, Person.firstName, Person.patrName, Person.code,
    rbService.id AS serviceId, rbService.name AS serviceName, rbService.code AS serviceCode,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NULL) AS exposed,
    (Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NOT NULL) as refused,
    Contract_Tariff.federalPrice,
    Contract_Tariff.federalLimitation,
    rbFinance.id AS financeId,
    rbFinance.code AS financeCode,
    rbFinance.name AS financeName
FROM Account_Item
LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Contract        ON Contract.id = Account.contract_id
LEFT JOIN rbFinance       ON (rbFinance.id = Contract.finance_id AND Contract.deleted = 0)
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN Action          ON Action.id = Account_Item.action_id
LEFT JOIN Person          ON Person.id = Action.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NOT NULL
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


class CFinanceSummaryByDoctorsOld(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по врачам')


    def build(self, description, params):
        reportData = {}
        detailService = params.get('detailService', False)
        detailFedTariff = params.get('detailFedTariff', False)
        detailFinance   = params.get('detailFinance', False)

        dataLineStep = 4 if detailFedTariff else 3
        reportRowSize = 12 if detailFedTariff else 9

        def processQuery(query):
            while query.next():
                record = query.record()
                specialityName = forceString(record.value('specialityName'))
                lastName = forceString(record.value('lastName'))
                firstName = forceString(record.value('firstName'))
                patrName = forceString(record.value('patrName'))
                code = forceString(record.value('code'))
                serviceId = forceRef(record.value('serviceId'))
                serviceName = forceString(record.value('serviceName'))
                serviceCode = forceString(record.value('serviceCode'))
                amount = forceDouble(record.value('amount'))
                if amount == int(amount):
                   amount = int(amount)
                sum = forceDouble(record.value('sum'))
                uet = forceDouble(record.value('uet'))
                exposed = forceBool(record.value('exposed'))
                refused = forceBool(record.value('refused'))
                federalPrice = forceDouble(record.value('federalPrice'))
                federalLimitation = forceInt(record.value('federalLimitation'))
                financeId = forceRef(record.value('financeId'))
                financeCode = forceString(record.value('financeCode'))
                financeName = forceString(record.value('financeName'))

                serviceKey = (serviceId, serviceCode, serviceName if serviceId else u'Услуга не указана') if detailService else None
                name = formatName(lastName, firstName, patrName)
                key = (specialityName if specialityName else u'Без указания специальности',
                       name if name else u'Без указания врача',
                       code,
                       serviceKey)
                if detailFinance:
                    reportFinanceData = reportData.setdefault((financeId, financeCode, financeName), {})
                    reportLine = reportFinanceData.setdefault(key, [0]*reportRowSize)
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
                        reportLine[4] += amount
                        reportLine[5] += uet
                        reportLine[6] += sum
                        reportLine[7] += resultFederalPrice
                    if refused:
                        reportLine[8]  += amount
                        reportLine[9]  += uet
                        reportLine[10] += sum
                        reportLine[11] += resultFederalPrice
                else:
                    reportLine[0] += amount
                    reportLine[1] += uet
                    reportLine[2] += sum
                    if exposed:
                        reportLine[3] += amount
                        reportLine[4] += uet
                        reportLine[5] += sum
                    if refused:
                        reportLine[6] += amount
                        reportLine[7] += uet
                        reportLine[8] += sum

                if detailFinance:
                    reportFinanceData[key] = reportLine
                    reportData[(financeId, financeCode, financeName)] = reportFinanceData
                else:
                    reportData[key] = reportLine

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
        cursor.insertText(description)
        cursor.insertBlock()

        tableColumns = [
                          ('20%', [ u'Врач',     u'ФИО'       ], CReportBase.AlignLeft ),
                          ('6%',  [ u'',         u'код'       ], CReportBase.AlignLeft ),
                          ('6%',  [ u'Всего',    u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'Оплачено', u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'Отказано', u'кол-во'    ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'УЕТ'       ], CReportBase.AlignRight ),
                          ('6%',  [ u'',         u'руб'       ], CReportBase.AlignRight ),
                       ]

        if detailFedTariff:
            tableColumns.insert(5,  ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))
            tableColumns.insert(9,  ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))
            tableColumns.insert(13, ('6%', [ u'', u'фед.тариф'], CReportBase.AlignRight ))

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0,  1, 2)
        table.mergeCells(0, 2,  1, dataLineStep)
        table.mergeCells(0, 6  if detailFedTariff else 5,  1, dataLineStep)
        table.mergeCells(0, 10 if detailFedTariff else 8,  1, dataLineStep)

        prevSpecialityName = None
        prevDoctor = None
        totalBySpeciality = [0]*reportRowSize
        totalByReport     = [0]*reportRowSize
        totalByDoctor     = [0]*reportRowSize
        locale = QLocale()
        tableColumnsLen = len(tableColumns)
        if detailFinance:
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
                    table.mergeCells(prevFinanceRow, 0,  1, tableColumnsLen)
                keys = reportFinanceData.keys()
                keys.sort()
                for key in keys:
                    specialityName = key[0]
                    doctorName = key[1]
                    doctorCode = key[2]
                    if prevDoctor and prevDoctor != (doctorCode, doctorName):
                        if not firstFinance:
                            self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep)
                        totalByDoctor = [0]*reportRowSize
                    if prevSpecialityName != specialityName:
                        if prevSpecialityName is not None:
                            if not firstFinance:
                                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep)
                            totalBySpeciality = [0]*reportRowSize
                        self.addSpecialityHeader(table, specialityName)
                        prevSpecialityName = specialityName
                    firstFinance = False
                    if not detailService or prevDoctor != (doctorCode, doctorName):
                        i = table.addRow()
                        nameShift = 4*' ' if detailService else ''
                        font = CReportBase.TableTotal if detailService else None
                        table.setText(i, 0, nameShift+doctorName, font)
                        table.setText(i, 1, doctorCode, font)
                        if detailService:
                            table.mergeCells(i, 2, 1, reportRowSize-2)
                            prevDoctor = (doctorCode, doctorName)
                    if detailService:
                        i = table.addRow()
                        serviceId, serviceCode, serviceName = key[3]
                        table.setText(i, 0, 8*' '+serviceName)
                        table.setText(i, 1, serviceCode)
                    reportLine = reportFinanceData[key]
                    for j in xrange(0, reportRowSize, dataLineStep):
                        table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                    for j in xrange(1, reportRowSize, dataLineStep):
                        table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                    for j in xrange(2, reportRowSize, dataLineStep):
                        table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                    if detailFedTariff:
                        for j in xrange(3, reportRowSize, dataLineStep):
                            table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                    for j in xrange(reportRowSize):
                        totalBySpeciality[j] += reportLine[j]
                        totalByReport[j] += reportLine[j]
                        totalByDoctor[j] += reportLine[j]
                        totalByFinance[j] += reportLine[j]
                if detailService:
                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep)
                self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep)
                self.addTotal(table, u'Всего по типу финансирования %s'%(financeName), totalByFinance, locale, dataLineStep)
            self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep)
        else:
            keys = reportData.keys()
            keys.sort()
            for key in keys:
                specialityName = key[0]
                doctorName = key[1]
                doctorCode = key[2]
                if prevDoctor and prevDoctor != (doctorCode, doctorName):
                    self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep)
                    totalByDoctor = [0]*reportRowSize
                if prevSpecialityName != specialityName:
                    if prevSpecialityName is not None:
                        self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep)
                        totalBySpeciality = [0]*reportRowSize
                    self.addSpecialityHeader(table, specialityName)
                    prevSpecialityName = specialityName
                if not detailService or prevDoctor != (doctorCode, doctorName):
                    i = table.addRow()
                    nameShift = 4*' ' if detailService else ''
                    font = CReportBase.TableTotal if detailService else None
                    table.setText(i, 0, nameShift+doctorName, font)
                    table.setText(i, 1, doctorCode, font)
                    if detailService:
                        table.mergeCells(i, 2, 1, reportRowSize-2)
                        prevDoctor = (doctorCode, doctorName)
                if detailService:
                    i = table.addRow()
                    serviceId, serviceCode, serviceName = key[3]
                    table.setText(i, 0, 8*' '+serviceName)
                    table.setText(i, 1, serviceCode)
                reportLine = reportData[key]
                for j in xrange(0, reportRowSize, dataLineStep):
                    table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                for j in xrange(1, reportRowSize, dataLineStep):
                    table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                for j in xrange(2, reportRowSize, dataLineStep):
                    table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                if detailFedTariff:
                    for j in xrange(3, reportRowSize, dataLineStep):
                        table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
                for j in xrange(reportRowSize):
                    totalBySpeciality[j] += reportLine[j]
                    totalByReport[j] += reportLine[j]
                    totalByDoctor[j] += reportLine[j]
            if detailService:
                self.addTotal(table, 4*' '+u'По врачу', totalByDoctor, locale, dataLineStep)
            self.addTotal(table, u'всего по специальности', totalBySpeciality, locale, dataLineStep)
            self.addTotal(table, u'Всего', totalByReport, locale, dataLineStep)
        return doc


    def addSpecialityHeader(self, table, specialityName):
        i = table.addRow()
        table.mergeCells(i, 0, 1, 8)
        table.setText(i, 0, specialityName, CReportBase.TableHeader)


    def addTotal(self, table, title, reportLine, locale, dataLineStep):
        reportRowSize = len(reportLine)
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 0, title, CReportBase.TableTotal)
        for j in xrange(0, reportRowSize, dataLineStep):
            table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
        for j in xrange(1, reportRowSize, dataLineStep):
            table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
        for j in xrange(2, reportRowSize, dataLineStep):
            table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))
        if dataLineStep == 4:
            for j in xrange(3, reportRowSize, dataLineStep):
                table.setText(i, j+2, locale.toString(float(reportLine[j]), 'f', 2))



class CFinanceSummaryByDoctorsExOld(CFinanceSummaryByDoctorsOld):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSummaryByDoctorsOld.exec_(self)


    def getSetupDialog(self, parent):
        result = CFinanceSummarySetupDialogOld(parent)
        result.setVisibleDetailService(True)
        result.setVisibleClientOrganisation(True)
        result.setVisibleDetailFedTariff(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinanceSummaryByDoctorsOld.build(self, '\n'.join(self.getDescription(params)), params)


class CFinanceSummarySetupDialogOld(QtGui.QDialog, Ui_FinanceSummarySetupDialogOld):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbInsurerDoctors.setAddNone(True)
        self.cmbRefuseType.setTable('rbPayRefuseType', True)
        self.cmbConfirmationType.addItem(u'без подтверждения')
        self.cmbConfirmationType.addItem(u'оплаченные')
        self.cmbConfirmationType.addItem(u'отказанные')
        self._visibleDetailService = False
        self.setVisibleDetailService(self._visibleDetailService)
        self._visibleClientOrganisation = False
        self.setVisibleClientOrganisation(self._visibleClientOrganisation)
        self._visibleDetailFedTariff = False
        self.setVisibleDetailFedTariff(self._visibleDetailFedTariff)

    def setVisibleDetailFedTariff(self, value):
        self._visibleDetailFedTariff = value
        self.chkDetailFedTariff.setVisible(value)

    def setVisibleDetailService(self, value):
        self._visibleDetailService = value
        self.chkDetailService.setVisible(value)

    def setVisibleClientOrganisation(self, value):
        self._visibleClientOrganisation = value
        self.cmbClientOrganisation.setVisible(value)
        self.lblClientOrganisation.setVisible(value)

    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbInsurerDoctors.setValue(params.get('orgInsurerId', None))
        self.chkConfirmation.setChecked(params.get('confirmation', False))
        self.edtConfirmationBegDate.setDate(params.get('confirmationBegDate', firstMonthDay(date)))
        self.edtConfirmationEndDate.setDate(params.get('confirmationEndDate', lastMonthDay(date)))
        self.cmbConfirmationType.setCurrentIndex(params.get('confirmationType', 0))
        self.cmbRefuseType.setValue(params.get('refuseType', None))
        self.chkDetailService.setChecked(params.get('detailService', False))
        self.cmbClientOrganisation.setValue(params.get('clientOrganisationId', None))
        self.chkFreeInputWork.setChecked(params.get('freeInputWork', False))
        self.edtFreeInputWork.setText(params.get('freeInputWorkValue', ''))
        self.chkDetailFedTariff.setChecked(params.get('detailFedTariff', False))
        self.chkDetailFinance.setChecked(params.get('detailFinance', False))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['personId'] = self.cmbPerson.value()
        result['orgInsurerId'] = self.cmbInsurerDoctors.value()
        result['confirmation'] = self.chkConfirmation.isChecked()
        result['confirmationType'] = self.cmbConfirmationType.currentIndex()
        result['confirmationBegDate'] = self.edtConfirmationBegDate.date()
        result['confirmationEndDate'] = self.edtConfirmationEndDate.date()
        result['refuseType'] = self.cmbRefuseType.value()
        result['detailFinance'] = self.chkDetailFinance.isChecked()
        result['freeInputWork'] = self.chkFreeInputWork.isChecked()
        result['freeInputWorkValue'] = forceStringEx(self.edtFreeInputWork.text())

        if self._visibleDetailService:
            result['detailService'] = self.chkDetailService.isChecked()

        if self._visibleClientOrganisation:
            result['clientOrganisationId'] = self.cmbClientOrganisation.value()

        if self._visibleDetailFedTariff:
            result['detailFedTariff'] = self.chkDetailFedTariff.isChecked()

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
