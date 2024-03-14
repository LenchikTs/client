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

from library.Utils      import forceInt, forceString, forceDouble, formatShortName

from Reports.Report     import CReport, CVoidSetupDialog
from Reports.ReportBase import CReportBase, createTable


def selectData(idList):
    def getExpenceSelect(code):
        db = QtGui.qApp.db
        tableCCE = db.table('Contract_CompositionExpense')
        tableESI = db.table('rbExpenseServiceItem')
        tableContractTariff = db.table('Contract_Tariff')
        table = tableCCE.leftJoin(tableESI, tableESI['id'].eq(tableCCE['rbTable_id']))
        cond = [
            tableESI['code'].eq(code), 
            tableCCE['master_id'].eq(tableContractTariff['id'])
        ]
        return db.selectStmt(table, [tableCCE['percent']], cond)
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableAccountItem = db.table('Account_Item')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableContractTariff = db.table('Contract_Tariff')
    tableClient = db.table('Client')
    tableService = db.table('rbService')
    tablePerson = db.table('Person')
    tablePost = db.table('rbPost')
    
    tableExpense = db.table('rbExpenseServiceItem')
    expenseItems = {}
    expenseItemList = db.getRecordList(tableExpense, ['code', 'name'], [tableExpense['isBase'].eq(1)])
    for item in expenseItemList:
        code = forceString(item.value('code'))
        name = forceString(item.value('name'))
        expenseItems[code] = name
    
    table = tableAccountItem.leftJoin(tableAccount, tableAccount['id'].eq(tableAccountItem['master_id']))
    table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAccountItem['event_id']))
    table = table.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    table = table.leftJoin(tablePost, tablePost['id'].eq(tablePerson['post_id']))
    
    cond = [
        tableAccount['id'].inlist(idList), 
        'isSexAndAgeSuitable(%s, %s, %s, %s, now())'%(tableClient['sex'], tableClient['birthDate'], tableContractTariff['sex'], tableContractTariff['age']), 
        tableContractTariff['service_id'].eq(tableAccountItem['service_id']), 
        tableContractTariff['deleted'].eq(0)
        ]
    
    cols = [
       tableAccountItem['sum'], 
       tableAccountItem['amount'], 
       tablePerson['lastName'], 
       tablePerson['firstName'],
       tablePerson['patrName'],
       tableEventType['name'].alias('eventTypeCode'), 
       tableService['code'].alias('serviceCode'),
       u'''IF(AGE(Client.birthDate, Event.execDate) > 18, 
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`adultUetDoctor`, rbService.`adultUetAverageMedWorker` ),
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`childUetDoctor`, rbService.`childUetAverageMedWorker` )) as `uet`'''
    ] + ['(%s) as "%s"'%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    
    return (expenseItems, db.getRecordList(table, cols, cond))


class CStructureByServiceReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Структура реестра по мероприятиям')


    def getSetupDialog(self, parent):
        return CVoidSetupDialog(parent)


    def build(self, params):
        data = {}
        expenseItemList, recordList = selectData(self.accountIdList)
        for record in recordList:
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            personName = formatShortName(lastName, firstName, patrName)
            serviceCode = forceString(record.value('serviceCode'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            
            pBlock = data.setdefault(personName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
            line = pBlock['lines'].setdefault(serviceCode, getEmptyDict(expenseItemList))
            sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            
            line['count'] += amount
            line['uet'] += uet
            line['sum'] += sum
            for val in codeList:
                line[val['c']] += val['v']
            
            sumRow['count'] += 1
            sumRow['uet'] += uet
            sumRow['sum'] += sum
            for val in codeList:
                sumRow[val['c']] += val['v']

            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Структура реестра по мероприятиям')
        cursor.insertBlock()
        self.dumpParams(cursor, {})
        cursor.insertBlock()
        
        tableColumns = [
            ('15%', u'Специалист, услуга', CReportBase.AlignLeft), 
            ('10%', u'Услуг', CReportBase.AlignLeft), 
            ('10%', u'Кол-во УЕТ', CReportBase.AlignLeft), 
            ('10%', u'Стоимость', CReportBase.AlignLeft)
        ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)]
        
        table = createTable(cursor, tableColumns)
        
        for name, inner in data.items():
            i = table.addRow()
            fillLine(table, i, name, inner['sum'], expenseItemList.keys(), bold = True)
            for innerName, innerLine in inner['lines'].items():
                j = table.addRow()
                fillLine(table, j, innerName, innerLine, expenseItemList.keys())
        
        return doc


class CStructureByEventReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Структура реестра по профилактическим осмотрам по типам событий')


    def getSetupDialog(self, parent):
        return CVoidSetupDialog(parent)


    def build(self, params):
        data = {}
        expenseItemList, recordList = selectData(self.accountIdList)
        for record in recordList:
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            personName = formatShortName(lastName, firstName, patrName)
            eventTypeCode = forceString(record.value('eventTypeCode'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            
            pBlock = data.setdefault(eventTypeCode, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
            line = pBlock['lines'].setdefault(personName, getEmptyDict(expenseItemList))
            sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            
            line['count'] += amount
            line['uet'] += uet
            line['sum'] += sum
            for val in codeList:
                line[val['c']] += val['v']
            
            sumRow['count'] += 1
            sumRow['uet'] += uet
            sumRow['sum'] += sum
            for val in codeList:
                sumRow[val['c']] += val['v']

            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Структура реестра по мероприятиям')
        cursor.insertBlock()
        self.dumpParams(cursor, {})
        cursor.insertBlock()
        
        tableColumns = [
            ('15%', u'Специалист, услуга', CReportBase.AlignLeft), 
            ('10%', u'Дисп', CReportBase.AlignLeft), 
            ('10%', u'Кол-во УЕТ', CReportBase.AlignLeft), 
            ('10%', u'Стоимость', CReportBase.AlignLeft)
        ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)]
        
        table = createTable(cursor, tableColumns)
        
        for name, inner in data.items():
            i = table.addRow()
            fillLine(table, i, name, inner['sum'], expenseItemList.keys(), bold = True)
            for innerName, innerLine in inner['lines'].items():
                j = table.addRow()
                fillLine(table, j, innerName, innerLine, expenseItemList.keys())
        
        return doc


def getEmptyDict(expenseList):
    r = {'count': 0,  'uet': 0, 'sum': 0}
    for c in expenseList.keys():
        r[c] = 0
    return r


def fillLine(table, i,  name, line, codeList, bold = False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, 0, name, charFormat=format)
    table.setText(i, 1, line['count'],  charFormat=format)
    table.setText(i, 2, line['uet'],  charFormat=format)
    table.setText(i, 3, line['sum'],  charFormat=format)
    for j, code in enumerate(sorted(codeList)):
        table.setText(i, j+4, line[code],  charFormat=format)
