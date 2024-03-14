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

from Reports.ReportBase import CReportBase, createTable, CReportTableBase
from library.Utils      import forceDouble, forceString, forceBool, forceInt



def selectData(accountItemIdList, orgInsurerId = None):
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    tableEventType = db.table('EventType')
    cond = db.joinAnd([tableAccountItem['id'].inlist(accountItemIdList), tableEventType['medicalAidType_id'].inlist([1, 2, 3, 7])])
    stmt="""
SELECT 
    (SELECT 
            OrgStructure.name
        FROM
            Action
                LEFT JOIN
            ActionType ON ActionType.id = Action.actionType_id
                LEFT JOIN
            ActionPropertyType ON ActionPropertyType.actionType_id = ActionType.id
                LEFT JOIN
            ActionProperty ON ActionProperty.action_id = Action.id
                LEFT JOIN
            ActionProperty_OrgStructure ON ActionProperty_OrgStructure.id = ActionProperty.id
                LEFT JOIN
            OrgStructure ON OrgStructure.id = ActionProperty_OrgStructure.value
        WHERE
            Action.event_id = Account_Item.event_id
                AND ActionType.flatCode = 'leaved'
                AND ActionPropertyType.typeName = 'OrgStructure'
                AND ActionProperty_OrgStructure.value IS NOT NULL
                AND ActionProperty.deleted = 0
                AND Action.deleted = 0
        LIMIT 1) AS orgStructureName,
    IF(Contract_Tariff.tariffType = 9,
        mes.MES_ksg.code,
        rbService.code) AS rbServiceCode,
    IF(Contract_Tariff.tariffType = 9 OR EventType.medicalAidType_id = 2,
        1,
        IF(Contract_Tariff.tariffType = 2,
            0,
            NULL)) isKSG,
    COUNT(DISTINCT Account_Item.event_id) AS eventCount,
    SUM((SELECT 
            SUM(Action.amount)
        FROM
            Action
                LEFT JOIN
            ActionType ON ActionType.id = Action.actionType_id
        WHERE
            Action.event_id = Account_Item.event_id
                AND ActionType.flatCode = 'moving'
                AND Action.deleted = 0
                AND DATE(Action.begDate)!=DATE(Action.endDate))) AS movingDays,
    SUM(Account_Item.amount) AS amount,
    SUM(Account_Item.sum) AS sum
FROM
    Account_Item
        LEFT JOIN
    Event ON Event.id = Account_Item.event_id
        LEFT JOIN
    EventType ON EventType.id = Event.eventType_id
        LEFT JOIN
    Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
        LEFT JOIN
    rbService ON rbService.id = Account_Item.service_id
        LEFT JOIN
    mes.MES ON mes.MES.id = Event.MES_id
        LEFT JOIN
    mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
WHERE
    %(cond)s"""    % {
        'cond' : cond
        }
    stmt += """
GROUP BY orgStructureName , rbServiceCode , isKSG
ORDER BY orgStructureName , rbServiceCode , isKSG
    """
    query = db.query(stmt)
    return query


def getAccountItemsList(accountsIdList):
    accountItemsList = []
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    cond = [tableAccountItem['master_id'].inlist(accountsIdList)]
    recordList = db.getRecordList(tableAccountItem, 'id', cond)
    for record in recordList:
        accountItemsList.append(forceInt(record.value('id')))
    return accountItemsList


def getAccountNumbersList(accountsIdList):
    numbersList = []
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account')
    cond = [tableAccountItem['id'].inlist(accountsIdList)]
    recordList = db.getRecordList(tableAccountItem, 'number', cond)
    for record in recordList:
        numbersList.append(forceString(record.value('number')))
    return numbersList


class CStationaryAccountSummary(CReportBase):
    def __init__(self, parent):
        CReportBase.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по стационарной помощи')


    def build(self, description, params):
        accountId = params.get('accountId', None)
        accountIdList = params.get('selectedAccountIdList', None)
        accountItemIdList = params.get('accountItemIdList', None)
        if accountIdList:
            numberList = u', '.join(getAccountNumbersList(accountIdList))
            accountItemIdList = getAccountItemsList(accountIdList)
        if accountId:
            number, infis, payer, recipient = self.getContract(accountId)
        
        query = selectData(accountItemIdList)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        if not accountIdList:
            tableColumns1 = [
                ('50%', [u'Наименование ЛПУ: %s'%recipient, u'код %s'%infis], CReportBase.AlignLeft),
                ('50%', [u'Наименование плательщика: %s'%payer,u''], CReportBase.AlignLeft)
            ]

        tableColumns2 = [
            ('5%', [u'№ п/п'], CReportBase.AlignLeft),
            ('25%', [u'Наименование отделения'], CReportBase.AlignLeft),
            ('25%', [u'КСГ, код услуги'], CReportBase.AlignLeft),
            ('15%', [u'Число выбывших больных'], CReportBase.AlignLeft),
            ('10%', [u'Число фактически проведенных койко-дней'], CReportBase.AlignRight),
            ('10%', [u'Кол-во услуг'], CReportBase.AlignRight),
            ('10%', [u'Стоимость'], CReportBase.AlignRight),
        ]

        cursor.setCharFormat(CReportBase.ReportBody)
        if not accountIdList:
            table = self.createTable(cursor, tableColumns1, border = 0, alignHeader = CReportBase.AlignLeft)
            table.mergeCells(0, 0, 1, 1) 
            table.mergeCells(0, 1, 1, 1) 
            table.mergeCells(0, 2, 1, 1) 
            table.mergeCells(0, 3, 1, 1) 
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        
        if not accountIdList:
            table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в условиях стационара по счету № %s '%number, CReportBase.AlignLeft), ], border = 0)
        else:
            table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в условиях стационара по счетам № %s '%numberList, CReportBase.AlignLeft), ], border = 0)
        table.mergeCells(0, 0, 1, 1) 
        cursor.insertBlock()
        cursor.insertBlock()
        
        table = createTable(cursor, tableColumns2)
        table.mergeCells(0, 0, 1, 1) 
        table.mergeCells(0, 1, 1, 1) 
        table.mergeCells(0, 2, 1, 1) 
        table.mergeCells(0, 3, 1, 1) 
        table.mergeCells(0, 4, 1, 1)
        table.mergeCells(0, 5, 1, 1)
        table.mergeCells(0, 6, 1, 1)
        
        i=0
        prevOrgStrName = u''
        subTotalEvents = 0
        subTotalMovingDays = 0
        subTotalAmount = 0
        subTotalSum = 0
        totalEvents = 0
        totalMovingDays = 0
        totalAmount = 0
        totalSum = 0
        while query.next():
            record = query.record()
            orgStructureName = forceString(record.value('orgStructureName'))
            rbServiceCode = forceString(record.value('rbServiceCode'))
            isKSG = forceBool(record.value('isKSG'))
            eventCount = forceInt(record.value('eventCount'))
            movingDays = forceInt(record.value('movingDays'))
            amount = forceInt(record.value('amount'))
            sum = forceDouble(record.value('sum'))

            if prevOrgStrName!=orgStructureName and prevOrgStrName != u'':
                row = table.addRow()
                i+=1
                table.setText(row, 0, i)
                table.setText(row, 1, u'Итого по отделению %s'%prevOrgStrName, charFormat=boldChars)
                table.setText(row, 2, u'')
                table.setText(row, 3, subTotalEvents, charFormat=boldChars)
                table.setText(row, 4, subTotalMovingDays, charFormat=boldChars)
                table.setText(row, 5, subTotalAmount, charFormat=boldChars)
                table.setText(row, 6, subTotalSum, charFormat=boldChars)
                subTotalEvents = 0
                subTotalMovingDays = 0
                subTotalAmount = 0
                subTotalSum = 0
            
            row = table.addRow()
            i+=1
            table.setText(row, 0, i)
            table.setText(row, 1, orgStructureName if prevOrgStrName!=orgStructureName else u'')
            table.setText(row, 2, rbServiceCode)
            table.setText(row, 3, eventCount if isKSG else u'')
            table.setText(row, 4, movingDays if isKSG else u'')
            table.setText(row, 5, amount if not isKSG else u'')
            table.setText(row, 6, sum)
            prevOrgStrName = orgStructureName
            if isKSG:
                totalEvents += eventCount
                subTotalEvents += eventCount
                totalMovingDays += movingDays
                subTotalMovingDays += movingDays
            else:
                totalAmount += amount
                subTotalAmount += amount
            totalSum += sum
            subTotalSum += sum

        row = table.addRow()
        i+=1
        table.setText(row, 0, i)
        table.setText(row, 1, u'Итого по отделению %s'%prevOrgStrName, charFormat=boldChars)
        table.setText(row, 2, u'')
        table.setText(row, 3, subTotalEvents, charFormat=boldChars)
        table.setText(row, 4, subTotalMovingDays, charFormat=boldChars)
        table.setText(row, 5, subTotalAmount, charFormat=boldChars)
        table.setText(row, 6, subTotalSum, charFormat=boldChars)
        subTotalEvents = 0
        subTotalMovingDays = 0
        subTotalAmount = 0
        subTotalSum = 0

        row = table.addRow()
        i+=1        
        table.setText(row, 0, i)
        table.setText(row, 1, u'Итого по ЛПУ', charFormat=boldChars)
        table.setText(row, 2, u'')
        table.setText(row, 3, totalEvents, charFormat=boldChars)
        table.setText(row, 4, totalMovingDays, charFormat=boldChars)
        table.setText(row, 5, totalAmount, charFormat=boldChars)
        table.setText(row, 6, totalSum, charFormat=boldChars)

        return doc


    def getContract(self, accountId):
        db = QtGui.qApp.db
        tableAccount = db.table('Account')
        tableContract = db.table('Contract')
        tableOrganisation = db.table('Organisation')
        tablePayer = tableOrganisation.alias('Payer')
        tableRecipient = tableOrganisation.alias('Recipient')
        queryTable = tableContract.leftJoin(tableAccount, tableContract['id'].eq(tableAccount['contract_id']))
        queryTable = queryTable.leftJoin(tablePayer, tableContract['payer_id'].eq(tablePayer['id']))
        queryTable = queryTable.leftJoin(tableRecipient, tableContract['recipient_id'].eq(tableRecipient['id']))
        record = db.getRecordEx(queryTable,
                                [tableContract['number'].name(), tableRecipient['infisCode'].alias('infisCode'),
                                 tablePayer['shortName'].alias('payer'), tableRecipient['shortName'].alias('recipient')
                                ],
                                tableAccount['id'].eq(accountId)
                               )
        if record:
            return (forceString(record.value('number')), forceString(record.value('infisCode')),
                    forceString(record.value('payer')),  forceString(record.value('recipient')))
        else:
            return ('', '', '', '')

    def createTable(self, testCursor, columnDescrs, headerRowCount=1, border=1, cellPadding=2, cellSpacing=0, alignHeader=None):
        def widthToTextLenght(width):
            widthSpec = QtGui.QTextLength.VariableLength
            widthVal  = 0
            try:
                if type(width) == str:
                    if len(width)>0:
                        if width[-1:] == '%':
                            widthVal  = float(width[:-1])
                            widthSpec = QtGui.QTextLength.PercentageLength
                        elif width[-1:] == '?':
                            widthVal  = float(width[:-1])
                        elif width[-1:] == '=':
                            widthVal  = float(width[:-1])
                            widthSpec = QtGui.QTextLength.FixedLength
                        else:
                            widthVal  = float(width)
                            widthSpec = QtGui.QTextLength.FixedLength
                else:
                    widthVal  = float(width)
                    widthSpec = QtGui.QTextLength.FixedLength
            except:
                pass
            return QtGui.QTextLength(widthSpec, widthVal)


        columnWidthConstraints = []
        for columnDescr in columnDescrs:
            assert type(columnDescr)==tuple
            width, headers, align = columnDescr
            columnWidthConstraints.append(widthToTextLenght(width))
            if type(headers) == list:
                headerRowCount = max(headerRowCount,  len(headers))

        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(border)
        tableFormat.setCellPadding(cellPadding)
        tableFormat.setCellSpacing(cellSpacing)
        tableFormat.setColumnWidthConstraints(columnWidthConstraints)
        tableFormat.setHeaderRowCount(headerRowCount)
    #    tableFormat.setBackground(QtGui.QBrush(Qt.red))
        table = testCursor.insertTable(max(1, headerRowCount), max(1, len(columnDescrs)), tableFormat)

        column = 0
        aligns = []
        for columnDescr in columnDescrs:
            assert type(columnDescr)==tuple
            width, headers, align = columnDescr
            if type(headers) != list:
                headers = [ headers ]
            row = 0
            for header in headers:
                if header != '':
                    cellCursor = table.cellAt(row, column).firstCursorPosition()
                    if alignHeader:
                        cellCursor.setBlockFormat(alignHeader)
                    else:
                        cellCursor.setBlockFormat(CReportBase.AlignCenter)
                    cellCursor.setCharFormat(CReportBase.TableHeader)
                    cellCursor.insertText(header)
                row += 1
            aligns.append(align)
            column += 1

        return CReportTableBase(table, aligns)
