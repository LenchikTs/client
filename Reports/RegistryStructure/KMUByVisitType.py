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
    tablePerson = db.table('vrbPerson')
    tableService = db.table('rbService')
    tableServiceGroup = db.table('rbServiceGroup')
    tableSpeciality = db.table('rbSpeciality')
    tableContractTariff = db.table('Contract_Tariff')
    tableContract = db.table('Contract')
    tableClient = db.table('Client')
    tableVisit = db.table('Visit')
    tableVisitType = db.table('rbVisitType')
    
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
    table = table.leftJoin(tableVisit, tableVisit['id'].eq(tableAccountItem['visit_id']))
    table = table.leftJoin(tableVisitType, tableVisitType['id'].eq(tableVisit['visitType_id']))
    table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableVisit['person_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tableServiceGroup, tableServiceGroup['id'].eq(tableService['group_id']))
    table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    table = table.leftJoin(tableContract, tableContract['id'].eq(tableContractTariff['master_id']))
    
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
        tableServiceGroup['name'].alias('group'),
        tablePerson['name'].alias('personName'), 
        tableSpeciality['name'].alias('specialityName'), 
        tableVisitType['name'].alias('visitName'), 
        tableVisitType['code'].alias('visitCode'),
        tableAccountItem['sum'], 
        tableAccountItem['uet'],
        tableAccountItem['amount'], 
        tableEvent['order'], 
        
    ] + ['(%s) as "%s"'%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    
    return (expenseItems, db.getRecordList(table, cols, cond))


class CKMUSetup(QtGui.QDialog, Ui_SetupDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.chkSpecialityDetail = QtGui.QCheckBox(u'Детализировать по специальности',  parent)
        self.chkPersonDetail = QtGui.QCheckBox(u'Детализировать по исполнителю',  parent)
        self.chkAidTypeDetail = QtGui.QCheckBox(u'Детализировать по форме помощи',  parent)
        self.chkGroupDetail = QtGui.QCheckBox(u'Детализировать по группе услуг',  parent)
        self.hLayout = QtGui.QHBoxLayout(parent)
        self.label = QtGui.QLabel(u'Группа')
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.cmbServiceGroup = CRBComboBox(parent)
        self.cmbServiceGroup.setTable('rbServiceGroup')
        self.cmbServiceGroup.setValue(None)
        self.cmbServiceGroup.setSizePolicy(sizePolicy)
        self.hLayout.addWidget(self.label)
        self.hLayout.addWidget(self.cmbServiceGroup)
        self.widgetLayout.addWidget(self.chkSpecialityDetail)
        self.widgetLayout.addWidget(self.chkPersonDetail)
        self.widgetLayout.addWidget(self.chkAidTypeDetail)
        self.widgetLayout.addWidget(self.chkGroupDetail)
        self.widgetLayout.addLayout(self.hLayout)

    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.chkSpecialityDetail.setChecked(params.get('specialityDetail', False))
        self.chkPersonDetail.setChecked(params.get('personDetail', False))
        self.chkAidTypeDetail.setChecked(params.get('aidTypeDetail', False))
        self.chkGroupDetail.setChecked(params.get('groupDetail', False))
        rowIndex = self.cmbServiceGroup.model().searchId(params.get('serviceGroupId', False))
        self.cmbServiceGroup.setCurrentIndex(rowIndex)


    def params(self):
        params = {}
        params['personDetail']  = self.chkPersonDetail.isChecked()
        params['specialityDetail']  = self.chkSpecialityDetail.isChecked()
        params['aidTypeDetail']  = self.chkAidTypeDetail.isChecked()
        params['groupDetail']  = self.chkGroupDetail.isChecked()
        rowIndex = self.cmbServiceGroup.currentIndex()
        params['serviceGroupId'] = self.cmbServiceGroup.model().getId(rowIndex)
        params['serviceGroupName'] = self.cmbServiceGroup.model().getName(rowIndex)
        return params


class CKMUByVisitTypeReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Структура КМУ по типам визитов')


    def getSetupDialog(self, parent):
        result = CKMUSetup(parent)
        return result


    def build(self, params):
        data = {}
        sumdata = {}
        #type = int('%i%i%i%i'%(params['aidTypeDetail'], params['groupDetail'], params['specialityDetail'], params['personDetail']), 2)
        type = int(params['aidTypeDetail']) + int(params['groupDetail']) + int(params['specialityDetail']) + int(params['personDetail'])
        expenseItemList, recordList = selectData(self.accountIdList, params['serviceGroupId'])
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            personName = forceString(record.value('personName'))
            specialityName = forceString(record.value('specialityName'))
            order = forceInt(record.value('order'))
            group = forceString(record.value('group'))
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            visitType = u' '.join([forceString(record.value('visitCode')), forceString(record.value('visitName'))])
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            if order == 1:
                aidType = u'плановый'
            elif order == 2:
                aidType = u'экстренный'
            elif order == 2:
                aidType = u'самотёком'
            elif order == 2:
                aidType = u'принудительный'
            elif order == 2:
                aidType = u'внутренний перевод'
            elif order == 2:
                aidType = u'неотложная'
            else:
                aidType = u'Не задано'
            if not group:
                group = u'Не задано'
            
            subdata = data
            if params['aidTypeDetail']:
                subdata = subdata.setdefault(aidType, {})
            if params['groupDetail']:
                subdata = subdata.setdefault(group, {})
            if params['specialityDetail']:
                subdata = subdata.setdefault(specialityName, {})
            if params['personDetail']:
                subdata = subdata.setdefault(personName, {})

            line = subdata.setdefault(visitType, getEmptyDict(expenseItemList))
            line['count'] += amount
            line['uet'] += uet
            line['sum'] += sum
            for val in codeList:
                line[val['c']] += val['v']
            
            globalSumRow['count'] += 1
            globalSumRow['uet'] += uet
            globalSumRow['sum'] += sum
            for val in codeList:
                globalSumRow[val['c']] += val['v']
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Структура КМУ по типам визитов')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                          ('10%', u'Посещ.', CReportBase.AlignLeft), 
                          ('10%', u'Кол-во УЕТ', CReportBase.AlignLeft), 
                          ('10%', u'Стоимость', CReportBase.AlignLeft)
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)]
        
        if type == 0:
            tableColumns.insert(0, ('10%', u'Вид посещения', CReportBase.AlignLeft))
        elif type == 1:
            if params['personDetail']:
                tableColumns.insert(0, ('10%', u'Врач, Вид посещения', CReportBase.AlignLeft))
            if params['specialityDetail']:
                tableColumns.insert(0, ('10%', u'Специальность, Вид посещения', CReportBase.AlignLeft))
            if params['groupDetail']:
                tableColumns.insert(0, ('10%', u'Группа, Вид посещения', CReportBase.AlignLeft))
            if params['aidTypeDetail']:
                tableColumns.insert(0, ('10%', u'Форма помощи, Вид посещения', CReportBase.AlignLeft))
        else:
            tableColumns.insert(0, ('10%', u'Вид посещения', CReportBase.AlignLeft))
            if params['personDetail']:
                tableColumns.insert(0, ('10%', u'Врач', CReportBase.AlignLeft))
            if params['specialityDetail']:
                tableColumns.insert(0, ('10%', u'Специальность', CReportBase.AlignLeft))
            if params['groupDetail']:
                tableColumns.insert(0, ('10%', u'Группа', CReportBase.AlignLeft))
            if params['aidTypeDetail']:
                tableColumns.insert(0, ('20%', u'Вид посещения', CReportBase.AlignLeft))
            tableColumns = tableColumns[1:]
        
        
        if params['serviceGroupId']:
            (fst_a, fst_b, fst_c)  = tableColumns[0]
            tableColumns = [(fst_a, [params['serviceGroupName'], fst_b], fst_c)] + [ (a, ['', b], c) for (a, b, c) in tableColumns[1:] ]
        
        table = createTable(cursor, tableColumns)
        if params['serviceGroupId']:
            table.mergeCells(0, 0, 1, 10)
        if type > 1:
            for key, innerData in data.items():
                i = table.addRow()
                table.setText(i, 0, key,  charFormat=CReportBase.TableTotal, blockFormat=CReportBase.AlignCenter)
                table.mergeCells(i, 0, i+1, len(expenseItemList)+3+type)
                (n_row, n_col, sum) = makeTable(i, 0, innerData, table, 1 if type > 1 else 0, expenseItemList.keys(), False, getEmptyDict(expenseItemList), expenseItemList)
                row = table.addRow()
                format = CReportBase.TableTotal
                table.setText(row, 0, u'Всего',  charFormat=format, blockFormat=CReportBase.AlignCenter)
                table.setText(row, type, sum['count'],  charFormat=format)
                table.setText(row, type+1, sum['uet'],  charFormat=format)
                table.setText(row, type+2, sum['sum'],  charFormat=format)
                for j, code in enumerate(sorted(expenseItemList.keys())):
                    table.setText(row, j+type+3, sum[code],  charFormat=format)
                table.mergeCells(row, 0, row, type)
        else:
            (n_row, n_col, sum) = makeTable(0, 0, data, table, 1 if type > 1 else 0, expenseItemList.keys(), False, getEmptyDict(expenseItemList), expenseItemList)
            row = table.addRow()
            format = CReportBase.TableTotal
            table.setText(row, 0, u'Всего',  charFormat=format)
            table.setText(row, 1, sum['count'],  charFormat=format)
            table.setText(row, 2, sum['uet'],  charFormat=format)
            table.setText(row, 3, sum['sum'],  charFormat=format)
            for j, code in enumerate(sorted(expenseItemList.keys())):
                table.setText(row, j+4, sum[code],  charFormat=format)
        return doc


def makeTable(row, col, data, table, t, codeList, bold, sumRow, expenseList):
    for key, d in data.items():
        if 'count' in d:
            row = table.addRow()
            format = CReportBase.TableTotal if bold else CReportBase.TableBody
            table.setText(row, col, key,  charFormat=format)
            table.setText(row, col+1, d['count'],  charFormat=format)
            table.setText(row, col+2, d['uet'],  charFormat=format)
            table.setText(row, col+3, d['sum'],  charFormat=format)
            for j, code in enumerate(sorted(codeList)):
                table.setText(row, j+col+4, d[code],  charFormat=format)
            for code in d:
                sumRow[code] += d[code]
        else:
            format = CReportBase.TableTotal
            if t == 0:
                row = table.addRow()
                (n_row, n_col, sum) = makeTable(row+1, col, d, table, t, codeList, bold, getEmptyDict(expenseList), expenseList)
                table.setText(row, col, key,  charFormat=format)
                table.setText(row, col+1, sum['count'],  charFormat=format)
                table.setText(row, col+2, sum['uet'],  charFormat=format)
                table.setText(row, col+3, sum['sum'],  charFormat=format)
                for j, code in enumerate(sorted(codeList)):
                    table.setText(row, j+col+4, sum[code],  charFormat=format)
            else:
                (n_row, n_col, sum) = makeTable(row, col+t, d, table, t, codeList, bold, getEmptyDict(expenseList), expenseList)
                table.setText(row+1, col, key)
                table.mergeCells(row+1, col, n_row - row + 1, 1)
                row = n_row
            for code in sum:
                sumRow[code] += sum[code]
    return (row, col, sumRow)


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
