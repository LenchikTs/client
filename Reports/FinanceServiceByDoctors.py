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
from Reports.ReportView import CPageFormat
from Reports.ReportBase       import CReportBase, createTable

from Ui_FinanceServiceSetupDialog import Ui_FinanceServiceSetupDialog


def getCond(params):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableAccountItem = db.table('Account_Item')
    tablePerson = db.table('vrbPersonWithSpeciality')
    cond = [tableAccountItem['reexposeItem_id'].isNull(),
            tableAccountItem['deleted'].eq(0),
            tableAccount['deleted'].eq(0),
           ]
    begDate = params.get('begDate', None)
    endDate = params.get('endDate', None)
    if begDate:
        cond.append(tableAccountItem['serviceDate'].ge(begDate))
    if endDate:
        cond.append(tableAccountItem['serviceDate'].lt(endDate.addDays(1)))
    if params.get('accountItemIdList',  None) is not None:
        cond.append(tableAccountItem['id'].inlist(params['accountItemIdList']))
    else:
        if params.get('accountIdList', None)is not None:
            cond.append(tableAccountItem['master_id'].inlist(params['accountIdList']))
        elif params.get('accountId', None):
            cond.append(tableAccountItem['master_id'].eq(params['accountId']))
    personId = params.get('personId', None)
    if params.get('personId', None):
        cond.append(tablePerson['id'].eq(personId))
    else:
        if params.get('orgStructureId', None):
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(params['orgStructureId'])))
        else:
            cond.append(db.joinOr([tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
                                   tablePerson['org_id'].isNull()]))
        if params.get('specialityId', None):
            cond.append(tablePerson['speciality_id'].eq(params['specialityId']))
    return db.joinAnd(cond)


def selectDataByEvents(params):
    db = QtGui.qApp.db
    stmt="""
SELECT
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    vrbPersonWithSpeciality.name AS personName,
    Event.execPerson_id AS personId,
    rbService.id AS serviceId,
    rbService.name AS serviceName,
    rbService.code AS serviceCode,
    Account_Item.price,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet
FROM Account_Item
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.execPerson_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NULL
    AND Account_Item.serviceDate IS NOT NULL
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND %s
    """
    db = QtGui.qApp.db
    return db.query(stmt % (getCond(params)))


def selectDataByVisits(params):
    stmt="""
SELECT
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    vrbPersonWithSpeciality.name AS personName,
    Visit.person_id AS personId,
    rbService.id AS serviceId,
    rbService.name AS serviceName,
    rbService.code AS serviceCode,
    Account_Item.price,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet
FROM Account_Item
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN Visit           ON Visit.id = Account_Item.visit_id
LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Visit.person_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
WHERE
    Account_Item.visit_id IS NOT NULL
    AND Account_Item.action_id IS NULL
    AND Account_Item.serviceDate IS NOT NULL
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND %s
    """
    return QtGui.qApp.db.query(stmt % (getCond(params)))


def selectDataByActions(params):
    stmt="""
SELECT
    Account_Item.visit_id,
    Account_Item.action_id,
    Account_Item.serviceDate,
    vrbPersonWithSpeciality.name AS personName,
    Action.person_id AS personId,
    rbService.id AS serviceId,
    rbService.name AS serviceName,
    rbService.code AS serviceCode,
    Account_Item.price,
    Account_Item.amount AS amount,
    Account_Item.sum AS sum,
    Account_Item.uet AS uet
FROM Account_Item
LEFT JOIN Account         ON Account.id = Account_Item.master_id
LEFT JOIN rbService       ON rbService.id = Account_Item.service_id
LEFT JOIN Event           ON Event.id = Account_Item.event_id
LEFT JOIN Action          ON Action.id = Account_Item.action_id
LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Action.person_id
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
WHERE
    Account_Item.visit_id IS NULL
    AND Account_Item.action_id IS NOT NULL
    AND (EventType.id IS NULL OR EventType.deleted = 0)
    AND Account_Item.serviceDate IS NOT NULL
    AND %s
    """
    return QtGui.qApp.db.query(stmt % (getCond(params)))


class CFinanceServiceByDoctors(CReport):
    def __init__(self, parent, accountIdList):
        CReport.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по врачам')
        self.orientation = CPageFormat.Landscape
        self.accountIdList = accountIdList


    def getSetupDialog(self, parent):
        result = CFinanceServiceSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate              = params.get('begDate', None)
        endDate              = params.get('endDate', None)
        orgStructureId       = params.get('orgStructureId', None)
        personId             = params.get('personId', None)
        specialityId         = params.get('specialityId', None)
        isPeriodOnService    = params.get('isPeriodOnService', False)
        rows = []
        if isPeriodOnService:
            rows.append(u'учитывать период по услуге')
        if begDate:
            rows.append(u'Дата начала периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Дата окончания периода: %s'%forceString(endDate))
        if orgStructureId:
            rows.append(u'Подразделение исполнителя: %s'%forceString(db.translate('OrgStructure', 'id', orgStructureId, 'CONCAT_WS(\' | \', code,name)')))
        if personId:
            rows.append(u'Врач: %s'%forceString(db.translate('vrbPerson', 'id', personId, 'name')))
        if specialityId:
            rows.append(u'Специальность: %s'%forceString(db.translate('rbSpeciality', 'id', specialityId, 'CONCAT_WS(\' | \', code,name)')))
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        reportData = {}
        reportDataTotal = {}
        reportDataTotalAll = {}
        params['accountIdList'] = self.accountIdList
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)

        def processQuery(query, reportData, reportDataTotal, reportDataTotalAll, begDate, endDate):
            while query.next():
                record = query.record()
                personName = forceString(record.value('personName'))
                personId = forceRef(record.value('personId'))
                serviceId = forceRef(record.value('serviceId'))
                serviceName = forceString(record.value('serviceName'))
                serviceCode = forceString(record.value('serviceCode'))
                serviceDate = forceDate(record.value('serviceDate'))
                amount = forceDouble(record.value('amount'))
                sum = forceDouble(record.value('sum'))
                price = forceDouble(record.value('price'))
                serviceKey = (serviceId, serviceCode, serviceName)
                key = (personName if personId else u'Без указания врача', personId)
                reportService = reportData.setdefault(key, {})
                reportMonth = reportService.get(serviceKey, {})
                if not reportMonth:
                    date = begDate
                    while date <= endDate:
                        reportMonth[(date.month(), date.year())] = {None:[0]*3}
                        date = date.addMonths(1)
                month = serviceDate.month()
                year = serviceDate.year()
                reportLine = reportMonth.get((month, year), {})
                reportItem = reportLine.get(price, [0]*3)
                reportItem[0] += amount
                reportItem[1] = price
                reportItem[2] += sum
                reportLine[price] = reportItem
                reportMonth[(month, year)] = reportLine
                reportService[serviceKey] = reportMonth
                reportData[key] = reportService
                reportDataTotalLine = reportDataTotal.get(personId, {})
                reportDataTotalData = reportDataTotalLine.get((month, year), [0]*2)
                reportDataTotalData[0] += amount
                reportDataTotalData[1] += sum
                reportDataTotalLine[(month, year)] = reportDataTotalData
                reportDataTotal[personId] = reportDataTotalLine
                reportDataTotalAllData = reportDataTotalAll.get((month, year), [0]*2)
                reportDataTotalAllData[0] += amount
                reportDataTotalAllData[1] += sum
                reportDataTotalAll[(month, year)] = reportDataTotalAllData
            return reportData, reportDataTotal, reportDataTotalAll

        doc = QtGui.QTextDocument()
        if not begDate or not endDate:
            return doc

        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [('10%', [ u'Услуга',     u'наименование'], CReportBase.AlignLeft),
                        ('5%',  [ u'',           u'код'],          CReportBase.AlignLeft),
                       ]

        dateColumns = {}
        date = begDate
        while date <= endDate:
            dateColumns[(date.month(), date.year())] = [0]*3
            date = date.addMonths(1)
        dateKeys = dateColumns.keys()
        dateKeys.sort(key=lambda x: (x[1], x[0]))
        reportRowSize = len(dateKeys)*3
        percent = (100.0 - 15.0)/reportRowSize
        for month, year in dateKeys:
            tableColumns.append(('%s%%'%('%.2f'%(percent)), [QDate().longMonthName(month, QDate.StandaloneFormat) + u'\n' + forceString(year), u'кол-во'],     CReportBase.AlignLeft))
            tableColumns.append(('%s%%'%('%.2f'%(percent)), [u'',                              u'тариф'],      CReportBase.AlignLeft))
            tableColumns.append(('%s%%'%('%.2f'%(percent)), [u'',                              u'сумма(руб)'], CReportBase.AlignLeft))

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0,  1, 2)
        for column in range(0, reportRowSize):
            table.mergeCells(0, column+2,  1, 3)

        query = selectDataByEvents(params)
        processQuery(query, reportData, reportDataTotal, reportDataTotalAll, begDate, endDate)
        query = selectDataByVisits(params)
        processQuery(query, reportData, reportDataTotal, reportDataTotalAll, begDate, endDate)
        query = selectDataByActions(params)
        processQuery(query, reportData, reportDataTotal, reportDataTotalAll, begDate, endDate)

        for (personName, personId), reportService in reportData.items():
            i = table.addRow()
            table.setText(i, 0, personName, CReportBase.TableTotal)
            table.mergeCells(i, 0, 1, reportRowSize+2)
            for serviceKey, reportMonth in reportService.items():
                i = table.addRow()
                serviceId, serviceCode, serviceName = serviceKey
                table.setText(i, 0, serviceName if serviceId else u'Услуга не указана')
                table.setText(i, 1, serviceCode)
                isServiceFirst = i
                priceLine = {}
                for (month, year), reportLine in reportMonth.items():
                    column = dateKeys.index((month, year))*3
                    for price, reportItem in reportLine.items():
                        if price == None:
                            continue
                        row = priceLine.get((month, year, price), None)
                        if isServiceFirst != i and row is None:
                            i = table.addRow()
                            table.setText(i, 0, serviceName if serviceId else u'Услуга не указана')
                            table.setText(i, 1, serviceCode)
                            priceLine[(month, year, price)] = i
                            row = i
                        else:
                            priceLine[(month, year, price)] = i
                            row = i
                        for j, val in enumerate(reportItem):
                            table.setText(row, column+j+2, val)

            if reportDataTotal:
                reportDataTotalLine = reportDataTotal.get(personId, {})
                if reportDataTotalLine:
                    i = table.addRow()
                    table.setText(i, 0, u'Всего', CReportBase.TableTotal)
                    table.mergeCells(i, 0,  1, 2)
                    for column, (month, year) in enumerate(dateKeys):
                        reportDataTotalData = reportDataTotalLine.get((month, year), [0]*2)
                        table.setText(i, column*3+2, reportDataTotalData[0], CReportBase.TableTotal)
                        table.setText(i, column*3+4, reportDataTotalData[1], CReportBase.TableTotal)

        if reportDataTotalAll:
            i = table.addRow()
            table.setText(i, 0, u'Итого', CReportBase.TableTotal)
            table.mergeCells(i, 0,  1, 2)
            for column, (month, year) in enumerate(dateKeys):
                reportDataTotalAllData = reportDataTotalAll.get((month, year), [0]*2)
                table.setText(i, column*3+2, reportDataTotalAllData[0], CReportBase.TableTotal)
                table.setText(i, column*3+4, reportDataTotalAllData[1], CReportBase.TableTotal)
        return doc


class CFinanceServiceSetupDialog(QtGui.QDialog, Ui_FinanceServiceSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['personId'] = self.cmbPerson.value()
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

