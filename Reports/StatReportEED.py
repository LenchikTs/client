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
from PyQt4.QtCore import QDate

from library.database   import addDateInRange
from library.Calendar   import monthName
from library.Utils      import firstMonthDay, forceDouble, forceInt, forceString, lastMonthDay

from Reports.Report     import CReport, CReportEx, monthsInYear, selectMonthData, selectYearData
from Reports.ReportBase import CReportBase
from Reports.ReportMonthActions import CSetupReportMonthActions


def getDoseTypes(db, actionTypeClass, actionTypeGroup, flatCode = '-'):
    tableActionType = db.table('ActionType')
    cond = []
    if actionTypeGroup:
        groups = db.getDescendants(tableActionType, 'group_id', actionTypeGroup)
        cond.append(tableActionType['id'].inlist(groups))
    if actionTypeClass:
        cond.append(tableActionType['class'].eq(actionTypeClass))
    if flatCode != '-':
        cond.append(tableActionType['flatCode'].eq(flatCode))
    if not len(cond):
        cond.append('1')
    stmt = u"""
      SELECT id, code
      FROM ActionType
      WHERE EXISTS
        (
        SELECT *
        FROM ActionPropertyType
        WHERE actionType_id = ActionType.id
          AND typeName = 'Доза облучения'
          AND deleted=0
          AND %s
        )
       AND deleted = 0
       """
    query = db.query(stmt % (db.joinAnd(cond)))
    ids = []
    codes = []
    while query.next():
        record = query.record()
        id  = forceString(record.value('id'))
        code = forceString(record.value('code'))
        ids += [id,]
        codes += [code, ]
    return [ids, codes]


def selectDataFromTypes(db, begDate, endDate, types, orgStructureId, personId): #1
    stmt= u"""
        SELECT
            ActionType.code as `code`,
            ActionType.name as `name`,
            Action.amount as `amount`,
            ActionProperty_Double.value as `dose`
        FROM
            Action
            inner JOIN ActionType ON Action.actionType_id = ActionType.id
            inner JOIN ActionPropertyType ON ActionPropertyType.actionType_id = ActionType.id
            inner JOIN ActionProperty ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id
            inner JOIN ActionProperty_Double ON ActionProperty_Double.id = ActionProperty.id
            left JOIN Person on Person.id = Action.person_id
        WHERE
            Action.deleted=0 AND ActionType.deleted=0 AND ActionProperty.deleted=0 AND ActionPropertyType.deleted=0 AND ActionPropertyType.typeName = 'Доза облучения' AND %s
        ORDER BY code
    """
    tableAction = db.table('Action')
    tablePerson = db.table('Person')
    tableActionType = db.table('ActionType')
    cond = []

    addDateInRange(cond, tableAction['endDate'], begDate, endDate)
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].eq(orgStructureId)) ##################################################
    if personId:
        cond.append(tableAction['person_id'].eq(personId))
    cond.append(tableActionType['id'].inlist(types))
    return db.query(stmt % (db.joinAnd(cond)))

def selectSummaryDataFromTypes(db, begDate, endDate, types, orgStructureId, personId): #2
    stmt= u"""
        SELECT
            ParentType.id as `parent_id`,
            Type.class as `class`,
            '' as code,
            -- CONCAT(ParentType.code, ' - ', ParentType.name) as `name`,
            Type.name as 'name',
            SUM(Action.amount) as `amount`,
            SUM(ActionProperty_Double.value) as `dose`
        FROM
            Action
            inner JOIN ActionType Type ON Action.actionType_id = Type.id
            inner JOIN ActionType ParentType ON Type.group_id = ParentType.id
            inner JOIN ActionPropertyType ON ActionPropertyType.actionType_id = Type.id
            inner JOIN ActionProperty ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id
            inner JOIN ActionProperty_Double ON ActionProperty_Double.id = ActionProperty.id
            left JOIN Person on Person.id = Action.person_id
        WHERE
            Action.deleted=0 AND ParentType.deleted=0 and Type.deleted=0 AND ActionProperty.deleted=0 AND ActionPropertyType.deleted=0 AND ActionPropertyType.typeName = 'Доза облучения' AND %s
        GROUP BY Type.name
        ORDER BY Type.name
    """
    tableAction = db.table('Action')
    tablePerson = db.table('Person')
    tableActionType = db.table('ActionType')
    cond = []
    addDateInRange(cond, tableAction['endDate'], begDate, endDate)
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].eq(orgStructureId)) ##################################################
    if personId:
        cond.append(tableAction['person_id'].eq(personId))
    cond.append(tableActionType.alias('Type')['id'].inlist(types))
    result = db.query(stmt % (db.joinAnd(cond)))
    return result


def selectDataInt(selectFunction, begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    db = QtGui.qApp.db
    [doseTypes, codes] = getDoseTypes(db, actionTypeClass, actionTypeGroup)
    return selectFunction(db, begDate, endDate, doseTypes, orgStructureId, personId)

def selectData(begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    return selectDataInt(selectDataFromTypes, begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId)

def selectSummaryData(begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    return selectDataInt(selectSummaryDataFromTypes, begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId)


def selectMonthDataInt(selectFunction, date, doseTypes, orgStructureId, personId):
    u"""Возвращает массив результатов запросов - каждый на 1 день месяца"""
    db = QtGui.qApp.db
    daysInMonth = date.daysInMonth()
    date = firstMonthDay(date)
    result = [0] * daysInMonth
    for i in xrange(daysInMonth):
        result[i] = selectFunction(db, date.addDays(i), date.addDays(i), doseTypes, orgStructureId, personId)
    return result

def selectMonthDataEED(date, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    [doseTypes, codes] = getDoseTypes(QtGui.qApp.db, actionTypeClass, actionTypeGroup)
    return selectMonthData(selectDataFromTypes, date, doseTypes, orgStructureId, personId)

def selectMonthSummaryData(date, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    [doseTypes, codes] = getDoseTypes(QtGui.qApp.db, actionTypeClass, actionTypeGroup)
    return selectMonthData(selectSummaryDataFromTypes, date, doseTypes, orgStructureId, personId)

def selectYearDataInt(selectFunction, date, doseTypes, orgStructureId, personId):
    u"""Возвращает массив результатов запросов - каждый на 1 месяц года"""
    db = QtGui.qApp.db
    year = date.year()
    result = [0] * monthsInYear
    for i in xrange(monthsInYear):
        firstDay = QDate(year, i+1, 1)
        result[i] = selectFunction(db, doseTypes, firstDay, lastMonthDay(firstDay), orgStructureId, personId)
    return result

def selectYearDataEED(date, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    [doseTypes, codes] = getDoseTypes(QtGui.qApp.db, actionTypeClass, actionTypeGroup)
    return selectYearData(selectDataFromTypes, date, doseTypes, orgStructureId, personId)

def selectYearSummaryData(date, actionTypeClass, actionTypeGroup, orgStructureId, personId):
    [doseTypes, codes] = getDoseTypes(QtGui.qApp.db, actionTypeClass, actionTypeGroup)
    return selectYearData(selectSummaryDataFromTypes, date, doseTypes, orgStructureId, personId)



class CStatReportEED(CReportEx):
    def __init__(self, parent = None):
        CReportEx.__init__(self, parent)
        self.table_columns = [
            ('50', [u'Код', u'1'], CReportBase.AlignRight),
            ('200', [u'Наименование исследования', u'2'], CReportBase.AlignRight),
            ('50', [u'Кол.-во протоколов', u'3'], CReportBase.AlignRight),
            ('60', [u'Суммарная ЭЭД, мЗв', u'4'], CReportBase.AlignRight),
            ]

    def getPeriodName(self, params):
        return u'период'

    def getSelectFunction(self, params = None):
        return lambda x: []

    def getReportName(self):
        return u'Отчет о работе рентгеновского кабинета'

    def getSubCodes(self, record):
        flatCode = forceString(record.value('name'))
        parent_type = forceString(record.value('parent_type'))
        class_ = forceString(record.value('class'))
        [ids, codes] = getDoseTypes(QtGui.qApp.db, class_, parent_type, flatCode)
        codes.sort()
        return ', '.join(codes)


    def addSummary(self, table, sumAmount, sumDose):
        tableRow = table.addRow()
        table.setText(tableRow, 1, u'Итого:')
        table.setText(tableRow, 2, sumAmount)
        table.setText(tableRow, 3, "%.5lf"%sumDose)



class CStatReportEEDMonth(CStatReportEED):
    def __init__(self, parent):
        CStatReportEED.__init__(self, parent)
        self.setTitle(u'Учет ЭЭД: отчет за месяц', u'Учет ЭЭД: отчет за месяц')

    def getSetupDialog(self, parent):
        result = CSetupReportMonthActions(parent)
        result.setTitle(self.title())
        result.setFinanceVisible(False)
        result.setStatusVisible(False)
        result.setAssistantVisible(False)
        result.setTissueTypeVisible(False)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setUETVisible(False)
        return result

    def getPeriodName(self, params):
        #return u'месяц'
        date = params.get('date', QDate.currentDate())
        month = monthName[date.month()]
        return date.toString(u"%s yyyy г."%month) + firstMonthDay(date).toString(u" (с dd.MM.yyyy") + lastMonthDay(date).toString(u" по dd.MM.yyyy)")

    def getSelectFunction(self):
        return selectMonthDataEED

    def getReportData(self, queries, daysInMonth):
        reportRowSize = 4 + daysInMonth
        reportData = {}
        for i in xrange(daysInMonth):
            while queries[i].next():
                record = queries[i].record()
                code  = forceString(record.value('code'))
                if code == '': # возможно, это сводный отчет?
                    code = self.getSubCodes(record)
                name = forceString(record.value('name'))
                amount = forceInt(record.value('amount'))
                dose = forceDouble(record.value('dose'))
                if not code in reportData:
                    reportData[code] = [0] * reportRowSize * 2
                    reportData[code][0] = code
                    reportData[code][1] = name
                    reportData[code][2] = amount #1
                    reportData[code][3] = dose
                    for j in xrange(daysInMonth):
                        reportData[code][4 + j*2] = 0
                        reportData[code][4 + j*2+1] = 0
                else:
                    reportData[code][2] += amount #1
                    reportData[code][3] += dose
                reportData[code][4+i*2] += amount
                reportData[code][4+i*2 + 1] += dose
        return reportData


    def buildInt(self, params, cursor):
        date = params.get('date', QDate.currentDate())
        daysInMonth = date.daysInMonth()
        actionTypeClass = params.get('class', None)
        actionTypeGroup = params.get('actionTypeGroupId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)

        selectFunction = self.getSelectFunction()
        queries = selectFunction(date, actionTypeClass, actionTypeGroup, orgStructureId, personId)
        reportData = self.getReportData(queries, daysInMonth)

        for i in xrange(daysInMonth):
            self.table_columns += [('40', [(u'Дата' if i==0 else ''), '%d'%(i+1)], CReportBase.AlignRight), ]
        table = self.createTable(cursor, border=3)
        table.mergeCells(0, 4, 1, daysInMonth)

        codes = reportData.keys()
        codes.sort()
        sumAmount = 0
        sumDose = 0
        for code in codes:
            tableRow = table.addRow()
            table.setText(tableRow, 0, reportData[code][0])
            table.setText(tableRow, 1, reportData[code][1])
            table.setText(tableRow, 2, reportData[code][2])
            sumAmount += reportData[code][2]
            for i in xrange(daysInMonth):
                table.setText(tableRow, 4+i, reportData[code][4+i*2])
            tableRow = table.addRow()
            table.mergeCells(tableRow-1, 0, 2, 1)
            table.mergeCells(tableRow-1, 1, 2, 1)
            table.setText(tableRow, 3, "%.5lf"%reportData[code][3])
            sumDose += reportData[code][3]
            for i in xrange(daysInMonth):
                table.setText(tableRow, 4+i, "%.3lf"%reportData[code][4+i*2+1])
        self.addSummary(table, sumAmount, sumDose)
        return reportData



class CStatReportEEDMonthSummary(CStatReportEEDMonth):
    def getSelectFunction(self):
        return selectMonthSummaryData


class CStatReportEEDYear(CStatReportEED):
    def __init__(self, parent):
        CStatReportEED.__init__(self, parent)
        self.setTitle(u'Учет ЭЭД: отчет за год', u'Учет ЭЭД: отчет за год')

    def getSetupDialog(self, parent):
        result = CSetupReportMonthActions(parent)
        result.setTitle(self.title())
        result.lblDate.setText(u'Год')
        result.edtEndDate.setDisplayFormat('dd.MM.yyyy')
        result.setFinanceVisible(False)
        result.setStatusVisible(False)
        result.setAssistantVisible(False)
        result.setTissueTypeVisible(False)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setUETVisible(False)
        return result

    def getPeriodName(self, params):
        date = params.get('date', QDate.currentDate())
        return date.toString(u"yyyy г.")

    def getSelectFunction(self):
        return selectYearDataEED

    def getReportData(self, queries):
        reportRowSize = 4 + monthsInYear
        reportData = {}
        for i in xrange(monthsInYear):
            while queries[i].next():
                record = queries[i].record()
                code  = forceString(record.value('code'))
                if code == '': # возможно, это сводный отчет?
                    code = self.getSubCodes(record)
                name = forceString(record.value('name'))
                amount = forceInt(record.value('amount'))
                dose = forceDouble(record.value('dose'))
                if not code in reportData:
                    reportData[code] = [0] * reportRowSize * 2
                    reportData[code][0] = code
                    reportData[code][1] = name
                    reportData[code][2] = amount #1
                    reportData[code][3] = dose
                    for j in xrange(monthsInYear):
                        reportData[code][4 + j*2] = 0
                        reportData[code][4 + j*2+1] = 0
                else:
                    reportData[code][2] += amount #1
                    reportData[code][3] += dose
                reportData[code][4+i*2] += amount
                reportData[code][4+i*2 + 1] += dose
        return reportData

    def buildInt(self, params, cursor):
        date = params.get('date', QDate.currentDate())
        actionTypeClass = params.get('class', None)
        actionTypeGroup = params.get('actionTypeGroupId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)

        selectFunction = self.getSelectFunction()
        queries = selectFunction(date, actionTypeClass, actionTypeGroup, orgStructureId, personId)
        reportData = self.getReportData(queries)

        for i in xrange(monthsInYear):
            self.table_columns += [('100', [(u'Месяц' if i==0 else ''), monthName[i+1]], CReportBase.AlignRight), ]
        table = self.createTable(cursor, border=1)
        table.mergeCells(0, 4, 1, monthsInYear)

        codes = reportData.keys()
        codes.sort()
        sumAmount = 0
        sumDose = 0
        for code in codes:
            tableRow = table.addRow()
            table.setText(tableRow, 0, reportData[code][0])
            table.setText(tableRow, 1, reportData[code][1])
            table.setText(tableRow, 2, reportData[code][2])
            sumAmount += reportData[code][2]
            for i in xrange(monthsInYear):
                table.setText(tableRow, 4+i, reportData[code][4+i*2])
            tableRow = table.addRow()
            table.mergeCells(tableRow-1, 0, 2, 1)
            table.mergeCells(tableRow-1, 1, 2, 1)
            table.setText(tableRow, 3, "%.5lf"%reportData[code][3])
            sumDose += reportData[code][3]
            for i in xrange(monthsInYear):
                table.setText(tableRow, 4+i, "%.3lf"%reportData[code][4+i*2+1])
        self.addSummary(table, sumAmount, sumDose)
        return reportData


class CStatReportEEDYearSummary(CStatReportEEDYear):
    def getSelectFunction(self):
        return selectYearSummaryData




class CStatReportEEDPeriod(CStatReportEED):
    def __init__(self, parent):
        CStatReportEED.__init__(self, parent)
        self.setTitle(u'Учет ЭЭД: отчет за период', u'Учет ЭЭД: отчет за период')

    def getSelectFunction(self):
        return selectData

    def getSetupDialog(self, parent):
        result = CReport.getSetupDialog(self, parent)
        result.setOrgStructureVisible(True)
        result.setPersonVisible(True)
        result.chkDetailPerson.setVisible(False)
        result.setActionTypeVisible(True)
        result.chkOnlyPermanentAttach.setVisible(False)
        return result

    def getReportData(self, query):
        reportRowSize = 4
        reportData = {}
        while query.next():
            record = query.record()
            code  = forceString(record.value('code'))
            if code == '': # возможно, это сводный отчет?
                code = self.getSubCodes(record)
            name = forceString(record.value('name'))
            amount = forceInt(record.value('amount'))
            dose = forceDouble(record.value('dose'))
            if not code in reportData:
                reportData[code] = [0] * reportRowSize
                reportData[code][0] = code
                reportData[code][1] = name
                reportData[code][2] = amount #1
                reportData[code][3] = dose
            else:
                reportData[code][2] += amount #1
                reportData[code][3] += dose
        return reportData

    def buildInt(self, params, cursor):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        actionTypeClass = params.get('actionTypeClass', None)
        actionTypeGroup = params.get('actionTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)

        selectFunction = self.getSelectFunction()
        query = selectFunction(begDate, endDate, actionTypeClass, actionTypeGroup, orgStructureId, personId)
        reportData = self.getReportData(query)

        table = self.createTable(cursor, border=1)

        codes = reportData.keys()
        codes.sort()
        sumAmount = 0
        sumDose = 0
        for code in codes:
            tableRow = table.addRow()
            table.setText(tableRow, 0, reportData[code][0])
            table.setText(tableRow, 1, reportData[code][1])
            table.setText(tableRow, 2, reportData[code][2])
            sumAmount += reportData[code][2]
            table.setText(tableRow, 3, "%.5lf"%reportData[code][3])
            sumDose += reportData[code][3]
        self.addSummary(table, sumAmount, sumDose)
        return reportData


class CStatReportEEDPeriodSummary(CStatReportEEDPeriod):
    def getSelectFunction(self):
        return selectSummaryData
