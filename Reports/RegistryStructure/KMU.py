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
from library.crbcombobox import CRBComboBox

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.RegistryStructure.Ui_SetupDialog import Ui_SetupDialog


def selectData(idList, groupId):
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
    tablePerson = db.table('Person')
    tablePost = db.table('rbPost')
    tableService = db.table('rbService')
    tableSpeciality = db.table('rbSpeciality')
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
    table = table.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    table = table.leftJoin(tableMAT, tableMAT['id'].eq(tableEventType['medicalAidType_id']))
    table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    table = table.leftJoin(tablePost, tablePost['id'].eq(tablePerson['post_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    
    cond = [
        tableAccount['id'].inlist(idList), 
        tableMAT['code'].inlist(['6', '9']), 
        'isSexAndAgeSuitable(%s, %s, %s, %s, now())'%(tableClient['sex'], tableClient['birthDate'], tableContractTariff['sex'], tableContractTariff['age']), 
        tableContractTariff['service_id'].eq(tableAccountItem['service_id']), 
        tableContractTariff['deleted'].eq(0)
        ]
    if groupId:
        cond.append(tableService['group_id'].eq(groupId))
    
    cols = [
        tableService['code'], 
        tablePerson['lastName'], 
        tablePerson['firstName'],
        tablePerson['patrName'],
        tableSpeciality['name'].alias('specialityName'), 
        tableAccountItem['sum'], 
        u'''IF(AGE(Client.birthDate, Event.execDate) > 18, 
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`adultUetDoctor`, rbService.`adultUetAverageMedWorker` ),
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`childUetDoctor`, rbService.`childUetAverageMedWorker` )) as `uet`''', 
       tableAccountItem['amount'], 
    ] + ['(%s) as "%s"'%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    
    return (expenseItems, db.getRecordList(table, cols, cond))


class CKMUSetup(QtGui.QDialog, Ui_SetupDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.chkPersonDetail = QtGui.QCheckBox(u'Детализировать по исполнителю',  parent)
        self.chkSpecialityDetail = QtGui.QCheckBox(u'Детализировать по специальности',  parent)
        self.hLayout = QtGui.QHBoxLayout(parent)
        self.label = QtGui.QLabel(u'Группа')
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.cmbServiceGroup = CRBComboBox(parent)
        self.cmbServiceGroup.setTable('rbServiceGroup')
        self.cmbServiceGroup.setValue(None)
        self.cmbServiceGroup.setSizePolicy(sizePolicy)
        self.hLayout.addWidget(self.label)
        self.hLayout.addWidget(self.cmbServiceGroup)
        self.widgetLayout.addWidget(self.chkPersonDetail)
        self.widgetLayout.addWidget(self.chkSpecialityDetail)
        self.widgetLayout.addLayout(self.hLayout)

    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.chkPersonDetail.setChecked(params.get('personDetail', False))
        self.chkSpecialityDetail.setChecked(params.get('specialityDetail', False))


    def params(self):
        params = {}
        params['personDetail']  = self.chkPersonDetail.isChecked()
        params['specialityDetail']  = self.chkSpecialityDetail.isChecked()
        rowIndex = self.cmbServiceGroup.currentIndex()
        group = self.cmbServiceGroup.model().getName(rowIndex)
        params['serviceGroup'] = group if group != u'не задано' else None
        return params


class CKMUReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Структура КМУ')


    def getSetupDialog(self, parent):
        result = CKMUSetup(parent)
        return result


    def build(self, params):
        data = {}
        type = int('%i%i'%(params['specialityDetail'], params['personDetail']), 2)
        expenseItemList, recordList = selectData(self.accountIdList, params['serviceGroup'])
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            code = forceString(record.value('code'))
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            personName = formatShortName(lastName, firstName, patrName)
            specialityName = forceString(record.value('specialityName'))
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            
            if type == 0:
                line = data.setdefault(code, getEmptyDict(expenseItemList))
                sumRow = getEmptyDict(expenseItemList)
            elif type == 1:
                pBlock = data.setdefault(personName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock['lines'].setdefault(code, getEmptyDict(expenseItemList))
                sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 2:
                pBlock = data.setdefault(specialityName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock['lines'].setdefault(code, getEmptyDict(expenseItemList))
                sumRow = pBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 3:
                pBlock = data.setdefault(specialityName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                pBlock2 = pBlock['lines'].setdefault(personName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = pBlock2['lines'].setdefault(code, getEmptyDict(expenseItemList))
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
        cursor.insertText(u'Структура КМУ')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                          ('10%', u'Посещ.', CReportBase.AlignLeft), 
                          ('10%', u'Кол-во УЕТ', CReportBase.AlignLeft), 
                          ('10%', u'Стоимость', CReportBase.AlignLeft)
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)]
        if type == 0:
            tableColumns.insert(0, ('20%', u'Услуга', CReportBase.AlignLeft))
        elif type == 1:
            tableColumns.insert(0, ('20%', u'Врач, услуга', CReportBase.AlignLeft))
        elif type == 2:
            tableColumns.insert(0, ('20%', u'Отделение, профиль', CReportBase.AlignLeft))
        elif type == 3:
            tableColumns.insert(0, ('10%', u'Услуга', CReportBase.AlignLeft))
            tableColumns.insert(0, ('10%', u'ФИО', CReportBase.AlignLeft))
            tableColumns.insert(0, ('10%', u'Специальность', CReportBase.AlignLeft))
        
        if params['serviceGroup']:
            (fst_a, fst_b, fst_c)  = tableColumns[0]
            tableColumns = [(fst_a, [params['serviceGroup'], fst_b], fst_c)] + [ (a, ['', b], c) for (a, b, c) in tableColumns[1:] ]

        
        table = createTable(cursor, tableColumns)
        if params['serviceGroup']:
            table.mergeCells(0, 0, 1, 10)
        pos1 = 1
        for name, inner in data.items():
            if type == 0:
                i = table.addRow()
                fillLine(table, i, name, inner, expenseItemList.keys())
            elif type == 1 or type == 2:
                i = table.addRow()
                fillLine(table, i, name, inner['sum'], expenseItemList.keys(), bold = True)
                for innerName, innerLine in inner['lines'].items():
                    j = table.addRow()
                    fillLine(table, j, innerName, innerLine, expenseItemList.keys())
            else:
                pos2 = pos1
                for name2, inner2 in inner['lines'].items():
                    c = 0
                    for innerName, innerLine in inner2['lines'].items():
                        j = table.addRow()
                        fillLine2(table, j, '', '', innerName, innerLine, expenseItemList.keys())
                        c += 1
                    table.mergeCells(pos2, 1, c, 1)
                    table.setText(pos2, 1, name2)
                    pos2 = pos2+c
                table.mergeCells(pos1, 0, pos2, 1)
                table.setText(pos1, 0, name)
                pos1 = pos2
        i = table.addRow()
        if type != 3:
            fillLine(table, i, u'Всего ЛПУ', globalSumRow, expenseItemList.keys(), bold=True)
        else:
            fillLine2(table, i, '', '',u'Всего ЛПУ', globalSumRow, expenseItemList.keys(), bold=True)
        return doc


def fillLine(table, i,  name, line, codeList, bold = False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, 0, name, charFormat=format)
    table.setText(i, 1, line['count'],  charFormat=format)
    table.setText(i, 2, line['uet'],  charFormat=format)
    table.setText(i, 3, line['sum'],  charFormat=format)
    for j, code in enumerate(sorted(codeList)):
        table.setText(i, j+4, line[code],  charFormat=format)


def fillLine2(table, i,  name1, name2, name3, line, codeList, bold=False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, 0, name1,  charFormat=format)
    table.setText(i, 1, name2,  charFormat=format)
    table.setText(i, 2, name3,  charFormat=format)
    table.setText(i, 3, line['count'],  charFormat=format)
    table.setText(i, 4, line['uet'],  charFormat=format)
    table.setText(i, 5, line['sum'],  charFormat=format)
    for j, code in enumerate(sorted(codeList)):
        table.setText(i, j+6, line[code],  charFormat=format)


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
