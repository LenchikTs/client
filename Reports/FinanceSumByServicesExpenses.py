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
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime, QLocale, QVariant

from library.Utils      import firstMonthDay, forceDouble, forceRef, forceString, lastMonthDay
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureFullName, getPersonInfo
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr

from Ui_FinanceExpensesSetupDialog import Ui_FinanceExpensesSetupDialog


def getCond(params):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableAccountItem = db.table('Account_Item')
    tablePerson = db.table('vrbPersonWithSpeciality')
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
            cond.append(tableAccount['payer_id'].eq(params['orgInsurerId']))

    if params.get('personId', None):
        cond.append(tablePerson['id'].eq(params['personId']))
    else:
        if params.get('orgStructureId', None):
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(params['orgStructureId'])))
        else:
            cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
        if params.get('specialityId', None):
            cond.append(tablePerson['speciality_id'].eq(params['specialityId']))
    analysisAccountItems = params.get('analysisAccountItems', 0)
    if analysisAccountItems == 1:
        cond.append(db.joinOr([tableAccountItem['date'].isNull(), tableAccountItem['number'].eq('')]))
    elif analysisAccountItems == 2:
        cond.append(tableAccountItem['date'].isNotNull())
        cond.append(tableAccountItem['number'].ne(''))
    elif analysisAccountItems == 3:
        cond.append('(Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NULL)')
    elif analysisAccountItems == 4:
        cond.append('(Account_Item.date IS NOT NULL AND Account_Item.number != '' AND Account_Item.refuseType_id IS NOT NULL)')
    return db.joinAnd(cond)


def selectDataByEvents(params):
    stmt="""
SELECT
    rbService.id,
    rbService.code,
    rbService.name,
    Organisation.shortName as insurerName,
    Organisation.id as insurerId,
    vrbPersonWithSpeciality.name as person,
    vrbPersonWithSpeciality.id as personId,
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
                         )) AS uet,
    Account_Item.tariff_id

FROM Account_Item
/*INNER JOIN Contract_CompositionExpense ON Contract_CompositionExpense.master_id = Account_Item.tariff_id*/
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN Organisation ON Organisation.id = Account.payer_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN rbService       ON rbService.id = IF(Account_Item.service_id IS NULL, EventType.service_id, Account_Item.service_id)
LEFT JOIN Diagnostic      ON Diagnostic.event_id = Event.id
LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnostic.diagnosisType_id
LEFT JOIN vrbPersonWithSpeciality          ON vrbPersonWithSpeciality.id = Diagnostic.person_id
LEFT JOIN rbSpeciality    ON rbSpeciality.id = vrbPersonWithSpeciality.speciality_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.tariff_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND Diagnostic.deleted = 0
    AND rbDiagnosisType.code in ('1','2')
    AND exists (select * from Contract_CompositionExpense where Contract_CompositionExpense.master_id = Account_Item.tariff_id)
    AND %s
GROUP BY
    Account_Item.tariff_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


def selectDataByVisits(params):
    stmt="""
SELECT
    rbService.id,
    rbService.code,
    rbService.name,
    Organisation.shortName as insurerName,
    Organisation.id as insurerId,
    vrbPersonWithSpeciality.name as person,
    vrbPersonWithSpeciality.id as personId,
    SUM(Account_Item.amount) AS amount,
    SUM(Account_Item.sum) AS sum,
    SUM(Account_Item.uet) AS uet,
    Account_Item.tariff_id
FROM Account_Item
/*INNER JOIN Contract_CompositionExpense ON Contract_CompositionExpense.master_id = Account_Item.tariff_id*/
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Organisation ON Organisation.id = Account.payer_id
LEFT JOIN Visit        ON Visit.id = Account_Item.visit_id
LEFT JOIN rbService    ON rbService.id = IF(Account_Item.service_id IS NULL, Visit.service_id, Account_Item.service_id)
LEFT JOIN vrbPersonWithSpeciality       ON vrbPersonWithSpeciality.id = Visit.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = vrbPersonWithSpeciality.speciality_id
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.tariff_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND exists (select * from Contract_CompositionExpense where Contract_CompositionExpense.master_id = Account_Item.tariff_id)
    AND %s
GROUP BY
    Account_Item.tariff_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


def selectDataByActions(params):
    stmt="""
SELECT
    rbService.id,
    rbService.code,
    rbService.name,
    Organisation.shortName as insurerName,
    Organisation.id as insurerId,
    vrbPersonWithSpeciality.name as person,
    vrbPersonWithSpeciality.id as personId,
    SUM(Account_Item.amount) AS amount,
    SUM(Account_Item.sum) AS sum,
    SUM(Account_Item.uet) AS uet,
    Account_Item.tariff_id
FROM Account_Item
/*INNER JOIN Contract_CompositionExpense ON Contract_CompositionExpense.master_id = Account_Item.tariff_id*/
LEFT JOIN Account      ON Account.id = Account_Item.master_id
LEFT JOIN Organisation ON Organisation.id = Account.payer_id
LEFT JOIN Action       ON Action.id = Account_Item.action_id
LEFT JOIN ActionType   ON ActionType.id = Action.actionType_id
LEFT JOIN rbService    ON rbService.id = Account_Item.service_id
LEFT JOIN vrbPersonWithSpeciality       ON vrbPersonWithSpeciality.id = Action.person_id
LEFT JOIN rbSpeciality ON rbSpeciality.id = vrbPersonWithSpeciality.speciality_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.tariff_id IS NOT NULL
    AND Account_Item.action_id IS NOT NULL
    AND exists (select * from Contract_CompositionExpense where Contract_CompositionExpense.master_id = Account_Item.tariff_id)
    AND %s
GROUP BY
    Account_Item.tariff_id
    """
    db = QtGui.qApp.db
    return db.query(stmt % getCond(params))


class CFinanceSumByServicesExpenses(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по услугам с нормативным составом затрат')


    def build(self, description, params):
        detailByPersons  = params.get('detailByPersons', False)
        detailByInsurers  = params.get('detailByInsurers', False)
        reportRowSize = 6
        reportData = {}
        reportDataExpence = {}

        def processQuery(query, type=None):
            locale = QLocale()

            def forceSum2DAP(sum):
                if isinstance(sum, QVariant):
                    sum = forceDouble(sum)
                return float(locale.toString(sum, 'f', 2))

            db = QtGui.qApp.db
            table = db.table('Contract_CompositionExpense')
            while query.next():
                record = query.record()
                code = forceString(record.value('code'))
                name = forceString(record.value('name'))
                person = forceString(record.value('person'))
                personId = forceRef(record.value('personId'))
                insurer = forceString(record.value('insurerName'))
                insurerId = forceRef(record.value('insurerId'))
                amount = forceDouble(record.value('amount'))
                uet = forceDouble(record.value('uet'))
                if amount == int(amount):
                   amount = int(amount)
                sum = forceDouble(record.value('sum'))
                tariffId = forceRef(record.value('tariff_id'))
                if tariffId:
                    if detailByPersons:
                        key = (personId if personId else u'Без указания врача', person)
                    else:
                        key = (name if name else u'Без указания услуги', code)
                    if detailByInsurers:
                        insurerKey = (insurerId if insurerId else u'Без указания плательщика', insurer)
                        reportLine = reportData.setdefault((insurerKey, key), [0]*reportRowSize)
                    else:
                        reportLine = reportData.setdefault(key, [0]*reportRowSize)
                    reportLineExpence = reportDataExpence.setdefault(key, {})
                    if type == 0:
                        reportLine[0] += amount
                    elif type == 1:
                        reportLine[1] += amount
                    elif type == 2:
                        reportLine[2] += amount
                    reportLine[3] += amount
                    reportLine[4] += uet
                    reportLine[5] += sum
                    records = db.getRecordList(table, [table['rbTable_id'], table['percent']], [table['master_id'].eq(tariffId)])
                    for recordExpence in records:
                        expenceId = forceRef(recordExpence.value('rbTable_id'))
                        percent = forceDouble(recordExpence.value('percent'))
                        if expenceId and percent:
                            for keyList in rbExpenceIdList.keys():
                                if keyList[0] == expenceId:
                                    value = reportLineExpence.get(keyList, 0)
                                    value += (sum * percent)/100.0
                                    reportLineExpence[keyList] = round(value, 2)

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
                        ('5%', [     u'Событий' ], CReportBase.AlignRight ),
                        ('5%', [     u'Посещений' ], CReportBase.AlignRight ),
                        ('5%', [     u'Услуг' ], CReportBase.AlignRight ),
                        ('5%', [ u'Всего',    u'кол-во' ], CReportBase.AlignRight ),
                        ('5%', [ u'',         u'УЕТ' ], CReportBase.AlignRight ),
                          ('10%', [ u'',         u'руб'      ], CReportBase.AlignRight )
                       ]
        if detailByPersons:
            tableColumns.insert(0, ('35%', [u'Врач'], CReportBase.AlignLeft))
        else:
            tableColumns.insert(0, ('30%', [ u'Услуга',   u'наименование'], CReportBase.AlignLeft ))
            tableColumns.insert(1, ('5%',  [ u'',         u'код'], CReportBase.AlignLeft ))

        query = QtGui.qApp.db.query('SELECT DISTINCT id, name FROM rbExpenseServiceItem')
        nameExpenceList = {}
        rbExpenceIdList = {}
        while query.next():
            record = query.record()
            rbExpenceId = forceRef(record.value('id'))
            if rbExpenceId:
                nameExpenceList[rbExpenceId] = forceString(record.value('name'))
        lenNameExpenceList = len(nameExpenceList) if len(nameExpenceList) else 1
        reportRowSizeExpence = len(nameExpenceList)
        i = len(tableColumns)
        widthInPercents = str(max(1, 45/lenNameExpenceList))+'%'
        for key, nameExpence in nameExpenceList.items():
            tableColumns.insert(i, (widthInPercents, [nameExpence, u'руб'], CReportBase.AlignRight))
            rbExpenceIdList[(key, i)] = 0
            i += 1
        table = createTable(cursor, tableColumns)
        if detailByPersons:
            table.mergeCells(0, 0, 3, 1)
            table.mergeCells(0, 1, 3, 1)
            table.mergeCells(0, 2, 3, 1)
            table.mergeCells(0, 3, 3, 1)
            table.mergeCells(0, 4, 1, 3)
        else:
            table.mergeCells(0, 0, 1, 2)
            table.mergeCells(0, 2, 3, 1)
            table.mergeCells(0, 3, 3, 1)
            table.mergeCells(0, 4, 3, 1)
            table.mergeCells(0, 5, 1, 3)

        query = selectDataByEvents(params)
        processQuery(query, 0)
        query = selectDataByVisits(params)
        processQuery(query, 1)
        query = selectDataByActions(params)
        processQuery(query, 2)

        totalByReport = [0]*(reportRowSize + reportRowSizeExpence)

        prevLineInsurer = None
        keys = reportData.keys()
        keys.sort(key=lambda item: item[1])
        for key in keys:
            if detailByInsurers:
                if prevLineInsurer != key[0][0]:
                    i = table.addRow()
                    table.mergeCells(i, 0, 1, (reportRowSize + reportRowSizeExpence + detailByPersons))
                    table.setText(i, 0, key[0][1], CReportBase.TableHeader)
                    prevLineInsurer = key[0][0]
            i = table.addRow()
            if detailByPersons:
                person = key[1][1] if detailByInsurers else key[1]
                table.setText(i, 0, person)
            else:
                name = key[1][0] if detailByInsurers else key[0]
                code = key[1][1] if detailByInsurers else key[1]
                table.setText(i, 0, name)
                table.setText(i, 1, code)
            reportLine = reportData[key]
            for j in xrange(0, reportRowSize):
                table.setText(i, j + 2 - detailByPersons, reportLine[j])
                totalByReport[j] += reportLine[j]
            reportLineExpence = reportDataExpence[key[1] if detailByInsurers else key]
            for expenceKey, value in reportLineExpence.items():
                table.setText(i, expenceKey[1], value)
                totalByReport[expenceKey[1]-2+detailByPersons] += value
        self.addTotal(table, u'Всего', totalByReport, detailByPersons)
        return doc


    def addTotal(self, table, title, reportLine, detailByPersons):
        i = table.addRow()
        if not detailByPersons:
            table.mergeCells(i, 0, 1, 2)
        table.setText(i, 0, title, CReportBase.TableTotal)
        for j, value in enumerate(reportLine):
            table.setText(i, j + 2 - detailByPersons, value)


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        specialityId = params.get('specialityId', None)
        personId = params.get('personId', None)
        orgInsurerId = params.get('orgInsurerId', None)
        analysisAccountItems = params.get('analysisAccountItems', 0)
        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if specialityId:
            rows.append(u'специальность: ' + forceString(db.translate('rbSpeciality', 'id', specialityId, 'name')))
        if personId:
            personInfo = getPersonInfo(personId)
            rows.append(u'врач: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if orgInsurerId:
            rows.append(u'СМО: ' + forceString(db.translate('Organisation', 'id', orgInsurerId, 'shortName')))
        if analysisAccountItems is not None:
            rows.append(u'статус оплаты: '+ [u'все', u'без подтверждения', u'подтверждённые', u'оплаченные', u'отказанные'][analysisAccountItems])
        detailByPersons = params.get('detailByPersons', False)
        if detailByPersons:
            rows.append(u'детализировать по врачам')
        detailByInsurers = params.get('detailByInsurers', False)
        if detailByInsurers:
            rows.append(u'детализировать по плательщикам')
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


class CFinanceSumByServicesExpensesEx(CFinanceSumByServicesExpenses):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSumByServicesExpenses.exec_(self)


    def getSetupDialog(self, parent):
        result = CFinanceExpensesSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CFinanceSumByServicesExpenses.build(self, '\n'.join(self.getDescription(params)), params)


class CFinanceExpensesSetupDialog(QtGui.QDialog, Ui_FinanceExpensesSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbInsurerDoctors.setAddNone(True)


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
        self.cmbAnalysisAccountItems.setCurrentIndex(params.get('analysisAccountItems', 0))
        self.chkDetailByPersons.setChecked(params.get('detailByPersons', False))
        self.chkDetailByInsurers.setChecked(params.get('detailByInsurers', False))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['personId'] = self.cmbPerson.value()
        result['orgInsurerId'] = self.cmbInsurerDoctors.value()
        result['analysisAccountItems'] = self.cmbAnalysisAccountItems.currentIndex()
        result['detailByPersons'] = self.chkDetailByPersons.isChecked()
        result['detailByInsurers'] = self.chkDetailByInsurers.isChecked()
        return result


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


class CDetailedFinanceSumByServicesExpenses(CFinanceSumByServicesExpensesEx):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CFinanceSumByServicesExpensesEx.exec_(self)

    def getSetupDialog(self, parent):
        result = CFinanceExpensesSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, descr, params):
        return CFinanceSumByServicesExpenses.build(self, descr, params)
