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
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableAccountItem = db.table('Account_Item')
    tableEvent = db.table('Event')
    tableContractTariff = db.table('Contract_Tariff')
    tableClient = db.table('Client')
    tableService = db.table('rbService')
    tableServiceGroup = db.table('rbServiceGroup')
    tablePerson = db.table('Person')
    tablePost = db.table('rbPost')
    
    table = tableAccountItem.leftJoin(tableAccount, tableAccount['id'].eq(tableAccountItem['master_id']))
    table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAccountItem['event_id']))
    table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    table = table.leftJoin(tableContractTariff, tableContractTariff['master_id'].eq(tableAccount['contract_id']))
    table = table.leftJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
    table = table.leftJoin(tableServiceGroup, tableServiceGroup['id'].eq(tableService['group_id']))
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
       tableServiceGroup['name'].alias('group'), 
       u'''IF(AGE(Client.birthDate, Event.execDate) > 18, 
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`adultUetDoctor`, rbService.`adultUetAverageMedWorker` ),
        IF(LEFT(rbPost.code, 1) in ("1", "2", "3"), rbService.`childUetDoctor`, rbService.`childUetAverageMedWorker` )) as `uet`'''
    ]
    
    return db.getRecordList(table, cols, cond)


class CMedicalCareProvidedReport(CReport):
    def __init__(self, parent, idList):
        CReport.__init__(self, parent)
        self.accountIdList = idList
        self.setTitle(u'Сведения об оказанной медицинской помощи')


    def getSetupDialog(self, parent):
        return CVoidSetupDialog(parent)


    def build(self, params):
        data = {}
        recordList = selectData(self.accountIdList)
        globalSumRow =  getEmptyDict()
        for record in recordList:
            uet = forceDouble(record.value('uet'))
            sum = forceDouble(record.value('sum'))
            amount = forceInt(record.value('amount'))
            group = forceString(record.value('group'))
            if not group:
                group = u'Иная'
            line = data.setdefault(group, getEmptyDict())
            
            line['count'] += 1
            line['visit'] += amount
            line['uet'] += uet
            line['sum'] += sum

            
            globalSumRow['count'] += 1
            globalSumRow['visit'] += amount
            globalSumRow['uet'] += uet
            globalSumRow['sum'] += sum
            
            
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        tableColumns = [
            ('28%', u'Вид медицинской помощи', CReportBase.AlignLeft), 
            ('18%', u'Число лиц', CReportBase.AlignLeft), 
            ('18%', u'Посещений/Услуг', CReportBase.AlignLeft), 
            ('18%', u'УЕТ', CReportBase.AlignLeft), 
            ('18%', u'Стоимость', CReportBase.AlignLeft)
        ]
        
        table = createTable(cursor, tableColumns)
        
        for name, line in data.items():
            i = table.addRow()
            table.setText(i, 0, name)
            table.setText(i, 1, line['count'])
            table.setText(i, 2, line['visit'])
            table.setText(i, 3, line['uet'])
            table.setText(i, 4, line['sum'])
        
        i = table.addRow()
        table.setText(i, 0, u'Итого')
        table.setText(i, 1, globalSumRow['count'])
        table.setText(i, 2, globalSumRow['visit'])
        table.setText(i, 3, globalSumRow['uet'])
        table.setText(i, 4, globalSumRow['sum'])
        return doc


def getEmptyDict():
    r = {'count': 0, 'visit': 0, 'uet':0,  'sum': 0}
    return r
