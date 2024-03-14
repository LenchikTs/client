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

from library.Utils      import forceString, forceDouble, forceDateTime, forceRef, forceInt

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import countMovingDays
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
    tableMES = db.table('mes.MES')
    tableMAT = db.table('rbMedicalAidType')
    tableMAP = db.table('rbMedicalAidProfile')
    tablePerson = db.table('vrbPerson')
    tableOS = db.table('OrgStructure')
    tableService = db.table('rbService')
    tableContractTariff = db.table('Contract_Tariff')
    tableClient = db.table('Client')
    #tableSpeciality = db.table('rbSpeciality')
    #tableSpecProf = db.table('rbSpeciality_MedicalAidProfile')
    
    tableExpense = db.table('rbExpenseServiceItem')
    expenseItems = {}
    expenseItemList = db.getRecordList(tableExpense, ['code', 'name'], [tableExpense['isBase'].eq(1)])
    for item in expenseItemList:
        code = forceString(item.value('code'))
        name = forceString(item.value('name'))
        expenseItems[code] = name
    
    tableAction = db.table('Action')
    tableActionType = db.table('ActionType')
    tableActionProperty = db.table('ActionProperty')
    tableActionPropertyType = db.table('ActionPropertyType')
    tableAPHBProfile = db.table('ActionProperty_rbHospitalBedProfile')
    tableHBProfile = db.table('rbHospitalBedProfile')
    
    tableBed = tableAction.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    tableBed = tableBed.leftJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    tableBed = tableBed.leftJoin(tableActionPropertyType, tableActionPropertyType['id'].eq(tableActionProperty['type_id']))
    tableBed = tableBed.leftJoin(tableAPHBProfile, tableAPHBProfile['id'].eq(tableActionProperty['id']))
    tableBed = tableBed.leftJoin(tableHBProfile, tableHBProfile['id'].eq(tableAPHBProfile['value']))
    bedCols = [tableHBProfile['name']]
    bedCond = [
        tableAction['event_id'].eq(tableEvent['id']), 
        tableActionType['flatCode'].eq('leaved'), 
        tableActionPropertyType['actionType_id'].eq(tableActionType['id']), 
        tableActionPropertyType['name'].eq(u'Профиль')
    ]
    bedStmt = db.selectStmt(tableBed, bedCols, bedCond)
    

    
    table = tableAccountItem.leftJoin(tableAccount, tableAccount['id'].eq(tableAccountItem['master_id']))
    table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAccountItem['event_id']))
    table = table.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    table = table.leftJoin(tableMES, tableMES['id'].eq(tableEvent['MES_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tableMAT, tableMAT['id'].eq(tableEventType['medicalAidType_id']))
    table = table.leftJoin(tableMAP, tableMAP['id'].eq(tableService['medicalAidProfile_id']))
    table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    #table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
    table = table.leftJoin(tableOS, tableOS['id'].eq(tablePerson['orgStructure_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    
    cond = [
        tableAccount['id'].inlist(idList), 
        tableMAT['code'].inlist(["1", "2", "3", "7"]), 
        'isSexAndAgeSuitable(%s, %s, %s, %s, now())'%(tableClient['sex'], tableClient['birthDate'], tableContractTariff['sex'], tableContractTariff['age']), 
        tableContractTariff['service_id'].eq(tableAccountItem['service_id']), 
        tableContractTariff['deleted'].eq(0)
        ]
    
    cols = [
        tableEvent['id'].alias('eventId'), 
        tableOS['name'], 
        tableAccountItem['sum'], 
        tableContractTariff['price'], 
        "(%s) as bedProfile"%bedStmt, 
        tableMAT['code'].alias('matCode'), 
        tablePerson['name'].alias('personName'), 
        tableMES['name'].alias('mesName'), 
        tableMES['code'].alias('mesCode'), 
        tableMAP['name'].alias('mapName')
        #"(select rbMedicalAidProfile.name from rbSpeciality_MedicalAidProfile left join rbMedicalAidProfile on rbMedicalAidProfile.id = rbSpeciality_MedicalAidProfile.medicalAidProfile_id where rbSpeciality_MedicalAidProfile.master_id = rbSpeciality.id limit 1) as mapName"
    ] + ["(%s) as '%s'"%(getExpenceSelect(c), c) for c in expenseItems.keys() ]
    return (expenseItems, db.getRecordList(table, cols, cond))


class CDistributionOfCostAndDurationSetup(QtGui.QDialog, Ui_SetupDialog):
    def __init__(self, parent, ver):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.chkPersonDetail = QtGui.QCheckBox(u'Детализировать по исполнителю',  parent)
        self.chkMedicalProfileDetail = QtGui.QCheckBox(u'Детализировать по профилю медицинской помощи',  parent)
        if ver == 1:
            self.widgetLayout.addWidget(self.chkPersonDetail)
        elif ver == 2:
            self.widgetLayout.addWidget(self.chkMedicalProfileDetail)
        self.chkBedProfileDetail = QtGui.QCheckBox(u'Детализировать по профилю коек',  parent)
        self.widgetLayout.addWidget(self.chkBedProfileDetail)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.chkPersonDetail.setChecked(params.get('personDetail', False))
        self.chkBedProfileDetail.setChecked(params.get('bedProfileDetail', False))
        self.chkMedicalProfileDetail.setChecked(params.get('medProfileDetail', False))


    def params(self):
        params = {}
        params['personDetail']  = self.chkPersonDetail.isChecked()
        params['bedProfileDetail'] = self.chkBedProfileDetail.isChecked()
        params['medProfileDetail'] = self.chkMedicalProfileDetail.isChecked()
        return params


class CDistributionOfCostAndDurationReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Распределение стоимости и длительности СБО в реестре по подразделениям')


    def getSetupDialog(self, parent):
        result = CDistributionOfCostAndDurationSetup(parent, 1)
        return result


    def build(self, params):
        data = {}
        type = int('%i%i'%(params['bedProfileDetail'], params['personDetail']), 2)
        expenseItemList, recordList = selectData(self.accountIdList)
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            eventId = forceRef(record.value('eventId'))
            name = forceString(record.value('name'))
            personName = forceString(record.value('personName'))
            bedProfile = forceString(record.value('bedProfile'))
            sum = forceDouble(record.value('sum'))
            price = forceDouble(record.value('price'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            daysStmt = """
            select sum(ActionAmount.amount) from (
                select DISTINCT Action.amount, DATE(Action.begDate) as dt from Action left join ActionType on ActionType.id = Action.actionType_id 
                where ActionType.flatCode = 'moving' and Action.event_id = %i
            ) as ActionAmount
            """ % eventId
            movingDays = 0
            query = QtGui.qApp.db.query(daysStmt)
            if query.first():
                movingDays = forceInt(query.value(0))
            
            if type == 0:
                line = data.setdefault(name, getEmptyDict(expenseItemList))
                sumRow = getEmptyDict(expenseItemList)
            elif type == 1:
                osBlock = data.setdefault(name, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = osBlock['lines'].setdefault(personName, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 2:
                osBlock = data.setdefault(name, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = osBlock['lines'].setdefault(bedProfile, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 3:
                osBlock = data.setdefault(name, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                personBlock = osBlock['lines'].setdefault(personName, {})
                line = personBlock.setdefault(bedProfile, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            line['count'] += 1
            line['sum'] += sum
            line['price'] += price
            for val in codeList:
                line[val['c']] += val['v']
            line['days'] += movingDays
            
            sumRow['count'] += 1
            sumRow['sum'] += sum
            sumRow['price'] += price
            for val in codeList:
                sumRow[val['c']] += val['v']
            sumRow['days'] += movingDays
            
            globalSumRow['count'] += 1
            globalSumRow['sum'] += sum
            globalSumRow['price'] += price
            for val in codeList:
                globalSumRow[val['c']] += val['v']
            globalSumRow['days'] += movingDays
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Распределение стоимости и длительности СБО в реестре по подразделениям')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                          ('10%', u"СБО", CReportBase.AlignLeft),
                          ('10%', u"Стоим.  КСГ", CReportBase.AlignLeft), 
                          ('10%', u"Ст. по Полож", CReportBase.AlignLeft)
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', u"К/д факт", CReportBase.AlignLeft)]
        if type == 0:
            tableColumns.insert(0, ('20%', u"Отделение", CReportBase.AlignLeft))
        elif type == 1:
            tableColumns.insert(0, ('20%', u"Отделение, врач", CReportBase.AlignLeft))
        elif type == 2:
            tableColumns.insert(0, ('20%', u"Отделение, профиль", CReportBase.AlignLeft))
        elif type == 3:
            tableColumns = [
                          ('10%', u"ФИО", CReportBase.AlignLeft), 
                          ('10%', u"Профиль", CReportBase.AlignLeft), 
                          ('10%', u"СБО", CReportBase.AlignLeft),
                          ('10%', u"Стоим.  КСГ", CReportBase.AlignLeft), 
                          ('10%', u"Ст. по Полож", CReportBase.AlignLeft), 
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', u"К/д факт", CReportBase.AlignLeft)]

        
        if type != 3:
            table = createTable(cursor, tableColumns)

        for name, inner in data.items():
            if type == 0:
                i = table.addRow()
                fillLine(table, i, 0, name, inner, expenseItemList.keys())
            elif type == 1 or type == 2:
                i = table.addRow()
                fillLine(table, i, 0, name, inner['sum'], expenseItemList.keys(), bold=True)
                for innerName, innerLine in inner['lines'].items():
                    j = table.addRow()
                    fillLine(table, j, 0, innerName, innerLine, expenseItemList.keys())
            else:
                table = createTable(cursor, getTableColumns(name, expenseItemList))
                table.mergeCells(0, 0, 1, 10)
                q = 2
                for personName, personLine in inner['lines'].items():
                    c = 0
                    for profileName, line in personLine.items():
                        j = table.addRow()
                        table.setText(j, 0, personName)
                        table.setText(j, 1, profileName)
                        table.setText(j, 2, line['count'])
                        table.setText(j, 3, line['sum'])
                        table.setText(j, 4, line['price'])
                        p = 0
                        for code in sorted(expenseItemList.keys()):
                            table.setText(j, p+5, line[code])
                            p += 1
                        table.setText(j, p+5, line['days'])
                        c += 1
                    table.mergeCells(q, 0, c, 1)
                    q = j+1
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
                
        if type != 3:
            i = table.addRow()
            table.setText(i, 0, u'Всего ЛПУ')
            table.setText(i, 1, globalSumRow['count'])
            table.setText(i, 2, globalSumRow['sum'])
            table.setText(i, 3, globalSumRow['price'])
            j = 0
            for code in sorted(expenseItemList.keys()):
                table.setText(i, j+4, globalSumRow[code])
                j += 1
            table.setText(i, j+4, globalSumRow['days'])
        return doc


class CDistributionOfCostAndDurationKSGReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Распределение стоимости и длительности СБО в реестре по КСГ')


    def getSetupDialog(self, parent):
        result = CDistributionOfCostAndDurationSetup(parent, 2)
        return result


    def build(self, params):
        data = {}
        type = int('%i%i'%(params['medProfileDetail'], params['bedProfileDetail']), 2)
        expenseItemList, recordList = selectData(self.accountIdList)
        globalSumRow =  getEmptyDict(expenseItemList)
        for record in recordList:
            eventId = forceRef(record.value('eventId'))
            matCode = forceString(record.value('matCode'))
            mapName = forceString(record.value('mapName'))
            name = forceString(record.value('name'))
            personName = forceString(record.value('personName'))
            bedProfile = forceString(record.value('bedProfile'))
            mesName = forceString(record.value('mesName'))
            mesCode = forceString(record.value('mesCode'))
            mes = u'[%s] %s'%(mesCode, mesName)
            sum = forceDouble(record.value('sum'))
            price = forceDouble(record.value('price'))
            codeList = [{'c': c,  'v': sum * forceDouble(record.value(c)) / 100} for c in expenseItemList.keys()]
            #movingDays = countMovingDays(begDate, endDate, begDate, endDate, 2 if matCode == '7' else 1)
            daysStmt = """
            select sum(ActionAmount.amount) from (
                select DISTINCT Action.amount, DATE(Action.begDate) as dt from Action left join ActionType on ActionType.id = Action.actionType_id 
                where ActionType.flatCode = 'moving' and Action.event_id = %i
            ) as ActionAmount
            """ % eventId
            movingDays = 0
            query = QtGui.qApp.db.query(daysStmt)
            if query.first():
                movingDays = forceInt(query.value(0))
            if not mapName:
                mapName = u'Не задано'
            
            if type == 0:
                line = data.setdefault(mes, getEmptyDict(expenseItemList))
                sumRow = getEmptyDict(expenseItemList)
            elif type == 1:
                osBlock = data.setdefault(bedProfile, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = osBlock['lines'].setdefault(mes, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 2:
                osBlock = data.setdefault(mapName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                line = osBlock['lines'].setdefault(mes, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            elif type == 3:
                osBlock = data.setdefault(mapName, {'lines': {}, 'sum': getEmptyDict(expenseItemList)})
                personBlock = osBlock['lines'].setdefault(bedProfile, {})
                line = personBlock.setdefault(mes, getEmptyDict(expenseItemList))
                sumRow = osBlock.setdefault('sum', getEmptyDict(expenseItemList))
            line['count'] += 1
            line['sum'] += sum
            line['price'] += price
            for val in codeList:
                line[val['c']] += val['v']
            line['days'] += movingDays
            
            sumRow['count'] += 1
            sumRow['sum'] += sum
            sumRow['price'] += price
            for val in codeList:
                sumRow[val['c']] += val['v']
            sumRow['days'] += movingDays
            
            globalSumRow['count'] += 1
            globalSumRow['sum'] += sum
            globalSumRow['price'] += price
            for val in codeList:
                globalSumRow[val['c']] += val['v']
            globalSumRow['days'] += movingDays
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Распределение стоимости и длительности СБО в реестре по подразделениям')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                          ('10%', u"КСГ", CReportBase.AlignLeft), 
                          ('10%', u"СБО", CReportBase.AlignLeft),
                          ('10%', u"Стоим.  КСГ", CReportBase.AlignLeft), 
                          ('10%', u"Ст. по Полож", CReportBase.AlignLeft)
                       ] + [('10%', expenseItemList[c], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', u"К/д факт", CReportBase.AlignLeft)]
        if type == 1:
            tableColumns.insert(0, ('10%', u"Профиль коек", CReportBase.AlignLeft))
        elif type == 2:
            tableColumns.insert(0, ('20%', u"Отделение, профиль", CReportBase.AlignLeft))

        
        if type <= 1:
            table = createTable(cursor, tableColumns)
        q = 1
        for name, inner in data.items():
            if type == 0:
                i = table.addRow()
                fillLine(table, i, 0, name, inner, expenseItemList.keys())
            elif type == 1:
                c = 0
                for innerName, innerLine in inner['lines'].items():
                    j = table.addRow()
                    c += 1
                    fillLine(table, j, 1, innerName, innerLine, expenseItemList.keys())
                table.setText(q, 0, name)
                table.mergeCells(q, 0, c, 1)
                i = table.addRow()
                fillLine(table, i, 1, u'Итого по профилю койки "%s"'%name, inner['sum'], expenseItemList.keys(), bold=True)
                table.mergeCells(i, 0, 1, 2)
                q = j+2
            elif type == 2:
                table = createTable(cursor, getTableColumnsKSG1(name, expenseItemList))
                table.mergeCells(0, 0, 1, 10)
                for innerName, innerLine in inner['lines'].items():
                    j = table.addRow()
                    fillLine(table, j, 0, innerName, innerLine, expenseItemList.keys())
                i = table.addRow()
                fillLine(table, i, 0, u'Итого по профилю медицинской помощи "%s"'%name, inner['sum'], expenseItemList.keys(), bold=True)
                #table.mergeCells(i, 0, 1, 2)
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
            else:
                table = createTable(cursor, getTableColumnsKSG2(name, expenseItemList))
                table.mergeCells(0, 0, 1, 10)
                q = 2
                for profileName, profileLine in inner['lines'].items():
                    c = 0
                    for csgName, line in profileLine.items():
                        j = table.addRow()
                        table.setText(j, 1, csgName)
                        table.setText(j, 2, line['count'])
                        table.setText(j, 3, line['sum'])
                        table.setText(j, 4, line['price'])
                        p = 0
                        for code in sorted(expenseItemList.keys()):
                            table.setText(j, p+5, line[code])
                            p += 1
                        table.setText(j, p+5, line['days'])
                        c += 1
                    table.mergeCells(q, 0, c, 1)
                    table.setText(q, 0, profileName)
                    q = j+1
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
                
        i = table.addRow()
        fillLine(table, i, 1 if type == 3 or type == 1 else 0, u'Всего ЛПУ', globalSumRow, expenseItemList.keys(), bold=True)
        if type == 3 or type == 1:
            table.mergeCells(i, 0, 1, 2)
        return doc


def fillLine(table, i, x,  name, line, codeList, bold = False):
    format = CReportBase.TableTotal if bold else CReportBase.TableBody
    table.setText(i, x, name,  charFormat=format)
    table.setText(i, x+1, line['count'],  charFormat=format)
    table.setText(i, x+2, line['sum'],  charFormat=format)
    table.setText(i, x+3, line['price'],  charFormat=format)
    j = 0
    for code in sorted(codeList):
        table.setText(i, x+j+4, line[code],  charFormat=format)
        j += 1
    table.setText(i, x+j+4, line['days'])


def getTableColumns(code, expenseItemList):
    return [
              ('10%', [code, u'ФИО'], CReportBase.AlignLeft), 
              ('10%', ['', u'Профиль'], CReportBase.AlignLeft), 
              ('10%', ['', u'СБО'], CReportBase.AlignLeft),
              ('10%', ['', u'Стоим.  КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'Ст. по Полож'], CReportBase.AlignLeft)
           ] + [('10%', ['', expenseItemList[c]], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', ['', u'К/д факт'], CReportBase.AlignLeft)]


def getTableColumnsKSG1(code, expenseItemList):
    return [
              ('10%', [code, u'КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'СБО'], CReportBase.AlignLeft),
              ('10%', ['', u'Стоим.  КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'Ст. по Полож'], CReportBase.AlignLeft)
           ] + [('10%', ['', expenseItemList[c]], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', ['', u'К/д факт'], CReportBase.AlignLeft)]


def getTableColumnsKSG2(code, expenseItemList):
    return [
              ('10%', [code, u'Профиль койки'], CReportBase.AlignLeft), 
              ('10%', ['', u'КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'СБО'], CReportBase.AlignLeft),
              ('10%', ['', u'Стоим.  КСГ'], CReportBase.AlignLeft), 
              ('10%', ['', u'Ст. по Полож'], CReportBase.AlignLeft)
           ] + [('10%', ['', expenseItemList[c]], CReportBase.AlignLeft) for c in sorted(expenseItemList)] + [('10%', ['', u'К/д факт'], CReportBase.AlignLeft)]


def getEmptyDict(expenseList):
    r = {'count': 0, 'sum': 0,  'price': 0,  'days': 0}
    for c in expenseList.keys():
        r[c] = 0
    return r
