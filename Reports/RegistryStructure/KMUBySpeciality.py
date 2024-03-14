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

from library.Utils      import forceInt, forceString, forceDouble, forceDateTime

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.RegistryStructure.Ui_SetupDialog import Ui_SetupDialog


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
    tableMAT = db.table('rbMedicalAidType')
    tablePerson = db.table('vrbPerson')
    tableService = db.table('rbService')
    tableSpeciality = db.table('rbSpeciality')
    tableContractTariff = db.table('Contract_Tariff')
    tableContract = db.table('Contract')
    tableFinance = db.table('rbFinance')
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
    table = table.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    table = table.leftJoin(tableMAT, tableMAT['id'].eq(tableEventType['medicalAidType_id']))
    table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    table = table.leftJoin(tableContract, tableContract['id'].eq(tableContractTariff['master_id']))
    table = table.leftJoin(tableFinance, tableFinance['id'].eq(tableContract['finance_id']))
    
    cond = [
        tableAccount['id'].inlist(idList), 
        tableMAT['code'].inlist(['6', '9']), 
        'isSexAndAgeSuitable(%s, %s, %s, %s, now())'%(tableClient['sex'], tableClient['birthDate'], tableContractTariff['sex'], tableContractTariff['age']), 
        tableContractTariff['service_id'].eq(tableAccountItem['service_id']), 
        tableContractTariff['deleted'].eq(0)
        ]
    
    cols = [
        tableService['code'], 
        tablePerson['name'].alias('personName'), 
        tableSpeciality['name'].alias('specialityName'), 
        tableAccountItem['sum'], 
        tableAccountItem['uet'],
        tableAccountItem['amount'], 
        tableFinance['name'].alias('finance')
    ] + ['(%s) as "%s"'%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    return (expenseItems, db.getRecordList(table, cols, cond))


class CKMUSetup(QtGui.QDialog, Ui_SetupDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.chkPersonDetail = QtGui.QCheckBox(u'Детализировать по исполнителю',  parent)
        self.chkFinanceDetail = QtGui.QCheckBox(u'Детализировать по типу финансирования',  parent)
        self.widgetLayout.addWidget(self.chkPersonDetail)
        self.widgetLayout.addWidget(self.chkFinanceDetail)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.chkPersonDetail.setChecked(params.get('personDetail', False))
        self.chkFinanceDetail.setChecked(params.get('financeDetail', False))


    def params(self):
        params = {}
        params['personDetail']  = self.chkPersonDetail.isChecked()
        params['financeDetail']  = self.chkFinanceDetail.isChecked()
        return params


class CKMUBySpecialityReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Структура КМУ по специальностям')


    def getSetupDialog(self, parent):
        result = CKMUSetup(parent)
        return result


    def build(self, params):
        data = {}
        type = int('%i%i'%(params['financeDetail'], params['personDetail']), 2)
        expenseItemList, recordList = selectData(self.accountIdList)
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            personName = forceString(record.value('personName'))
            specialityName = forceString(record.value('specialityName'))
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            finance = forceString(record.value('finance'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            
            if type == 0:
                line = data.setdefault(specialityName, getEmptyDict(expenseItemList))
                sumRow = getEmptyDict(expenseItemList)
            elif type == 1:
                pBlock = data.setdefault(specialityName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock['lines'].setdefault(personName, getEmptyDict(expenseItemList))
                sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 2:
                pBlock = data.setdefault(specialityName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock['lines'].setdefault(finance, getEmptyDict(expenseItemList))
                sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 3:
                pBlock = data.setdefault(specialityName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                pBlock2 = pBlock['lines'].setdefault(personName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock2['lines'].setdefault(finance, getEmptyDict(expenseItemList))
                sumRow = pBlock2.setdefault('sum', getEmptyDict(expenseItemList))
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
            
            globalSumRow['count'] += 1
            globalSumRow['uet'] += uet
            globalSumRow['sum'] += sum
            for val in codeList:
                globalSumRow[val['c']] += val['v']
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Структура КМУ по специальностям')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                          ('10%', u'Посещ.', CReportBase.AlignLeft), 
                          ('10%', u'Кол-во УЕТ', CReportBase.AlignLeft), 
                          ('10%', u'Стоимость', CReportBase.AlignLeft)
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)]
        if type == 0:
            tableColumns.insert(0, ('20%', u'Специальность', CReportBase.AlignLeft))
        elif type == 1:
            tableColumns.insert(0, ('20%', u'Врач, услуга', CReportBase.AlignLeft))
        elif type == 2:
            tableColumns.insert(0, ('20%', u'Специальность, Вид услуги', CReportBase.AlignLeft))
        elif type == 3:
            tableColumns.insert(0, ('10%', u'Тип финансирования', CReportBase.AlignLeft))
            tableColumns.insert(0, ('10%', u'ФИО', CReportBase.AlignLeft))
        
        table = createTable(cursor, tableColumns)
        pos1 = 1
        for name, inner in data.items():
            if type == 0:
                i = table.addRow()
                fillLine(table, i, name, inner, expenseItemList.keys())
            elif type == 1 or type == 2:
                i = table.addRow()
                fillLine(table, i, name, inner['sum'], expenseItemList.keys(), bold=True)
                for innerName, innerLine in inner['lines'].items():
                    j = table.addRow()
                    fillLine(table, j, innerName, innerLine, expenseItemList.keys())
            else:
                j = table.addRow()
                table.mergeCells(j, 0, 1, 9)
                table.setText(j, 0, name, charFormat=CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                pos1 += 1
                for name2, inner2 in inner['lines'].items():
                    c = 0
                    for innerName, innerLine in inner2['lines'].items():
                        j = table.addRow()
                        fillLine2(table, j, '', innerName, innerLine, expenseItemList.keys())
                        c += 1
                    table.mergeCells(pos1, 0, c, 1)
                    table.setText(pos1, 0, name2)
                    pos1 = pos1+c
        i = table.addRow()
        if type != 3:
            fillLine(table, i, u'Всего ЛПУ', globalSumRow, expenseItemList.keys(), bold=True)
        else:
            fillLine2(table, i, '', u'Всего ЛПУ', globalSumRow, expenseItemList.keys(), bold=True)
        return doc


def fillLine(table, i,  name, line, codeList, bold=False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, 0, name,  charFormat=format)
    table.setText(i, 1, line['count'],  charFormat=format)
    table.setText(i, 2, line['uet'],  charFormat=format)
    table.setText(i, 3, line['sum'],  charFormat=format)
    for j, code in enumerate(sorted(codeList)):
        table.setText(i, j+4, line[code],  charFormat=format)


def fillLine2(table, i,  name1, name2, line, codeList, bold=False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, 0, name1,  charFormat=format)
    table.setText(i, 1, name2,  charFormat=format)
    table.setText(i, 2, line['count'],  charFormat=format)
    table.setText(i, 3, line['uet'],  charFormat=format)
    table.setText(i, 4, line['sum'],  charFormat=format)
    for j, code in enumerate(sorted(codeList)):
        table.setText(i, j+5, line[code],  charFormat=format)


def getTableColumns(code):
    return [
              ('10%', [code, u'ФИО'], CReportBase.AlignLeft), 
              ('10%', ['', u'Профиль'], CReportBase.AlignLeft), 
              ('10%', ['', u'СБО'], CReportBase.AlignLeft),
              ('10%', ['', u'Стоим.  КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'Ст. по Полож'], CReportBase.AlignLeft), 
              ('10%', ['', u'Заработная плата и начисления'], CReportBase.AlignLeft), 
              ('10%', ['', u'ЛС, РМ и ИМН'], CReportBase.AlignLeft), 
              ('10%', ['', u'Питание'], CReportBase.AlignLeft), 
              ('10%', ['', u'Иные расходы'], CReportBase.AlignLeft), 
              ('10%', ['', u'К/д факт'], CReportBase.AlignLeft)
           ]


def getEmptyDict(expenseList):
    r = {'count': 0,  'uet': 0, 'sum': 0}
    for c in expenseList.keys():
        r[c] = 0
    return r
