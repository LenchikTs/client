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

from library.Utils      import forceInt, forceString, forceDouble

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
    tableContractTariff = db.table('Contract_Tariff')
    tableClient = db.table('Client')
    
    tableExpense = db.table('rbExpenseServiceItem')
    expenseItems = {}
    expenseItemList = db.getRecordList(tableExpense, ['code', 'name'], [tableExpense['isBase'].eq(1)])
    for item in expenseItemList:
        code = forceString(item.value('code'))
        name = forceString(item.value('name'))
        expenseItems[code] = name
    
    table = tableAccountItem.leftJoin(tableAccount, tableAccount['id'].eq(tableAccountItem['master_id']))
    table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAccountItem['event_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    
    cond = [
        tableAccount['id'].inlist(idList), 
        'isSexAndAgeSuitable(%s, %s, %s, %s, now())'%(tableClient['sex'], tableClient['birthDate'], tableContractTariff['sex'], tableContractTariff['age']), 
        tableContractTariff['service_id'].eq(tableAccountItem['service_id']), 
        tableContractTariff['deleted'].eq(0)
        ]
    
    cols = [
       tableAccountItem['sum'], 
       tableAccountItem['amount'], 
    ] + ['(%s) as "%s"'%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    
    return (expenseItems, db.getRecordList(table, cols, cond))


class CSummaryReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Общая сводка по статьям затрат')


    def getSetupDialog(self, parent):
        return CVoidSetupDialog(parent)


    def build(self, params):
        expenseItemList, recordList = selectData(self.accountIdList)
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            
            globalSumRow['count'] += amount
            globalSumRow['sum'] += sum
            for val in codeList:
                globalSumRow[val['c']] += val['v']
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        table = createTable(cursor, [('50%', u'Общая сводка по статьям затрат', CReportBase.AlignLeft), ('50%', u'', CReportBase.AlignLeft)])
        table.mergeCells(0, 0, 1, 2)
        i = table.addRow()
        table.setText(i, 0, u'Всего СПО')
        table.setText(i, 1, globalSumRow['count'])
        i = table.addRow()
        table.setText(i, 0, u'Стоимость рестра')
        table.setText(i, 1, globalSumRow['sum'])
        for code in sorted(globalSumRow):
            if code == u'count' or code == 'sum':
                continue
            i = table.addRow()
            table.setText(i, 0, expenseItemList[code])
            table.setText(i, 1, globalSumRow[code])
        return doc


def getEmptyDict(expenseList):
    r = {'count': 0,  'sum': 0}
    for c in expenseList.keys():
        r[c] = 0
    return r
