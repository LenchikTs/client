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

from PyQt4 import QtGui, QtCore

from Reports.ReportBase import CReportBase, createTable, CReportTableBase
from Reports.StationaryAccountSummary import getAccountItemsList, getAccountNumbersList
from library.Utils      import forceDouble, forceString, forceBool, forceInt, forceDate



def selectData(accountItemIdList, detailed = None):
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    tableEventType = db.table('EventType')
    tableVisit = db.table('Visit')
    cond = db.joinAnd([tableAccountItem['id'].inlist(accountItemIdList), tableEventType['medicalAidType_id'].inlist([6, 9]), db.joinOr([tableVisit['deleted'].eq(0), tableVisit['deleted'].isNull()])])
    stmt="""
SELECT 
    IF(Account_Item.visit_id,
        VisitSpeciality.name,
        ActionSpeciality.name) AS specialityName,
    %(execPerson)s,
    rbMedicalAidUnit.id as unitId,
    rbService.code,
    rbService.name,
    SUM(Account_Item.amount) AS amount,
    IF(Account_Item.visit_id, 1, 0) AS visitFlag,
    COUNT(DISTINCT Event.id) AS eventAmount,
    SUM(Account_Item.sum) AS itemsSum,
    SUM(Account_Item.uet) AS actionUet,
    COUNT((SELECT 
            GROUP_CONCAT(distinct id)
        FROM
            Visit AS V
        WHERE
            V.event_id = Account_Item.event_id
                AND V.service_id = Visit.service_id
                AND V.deleted = 0)) AS sameVisitsInEvent
FROM
    Account_Item
        LEFT JOIN
    rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
        LEFT JOIN
    rbService ON rbService.id = Account_Item.service_id
        LEFT JOIN
    Event ON Event.id = Account_Item.event_id
    %(execPersonJoin)s
        LEFT JOIN
    EventType ON EventType.id = Event.eventType_id
        LEFT JOIN
    Visit ON Visit.id = Account_Item.visit_id
        LEFT JOIN
    Person AS VisitPerson ON VisitPerson.id = Visit.person_id
        LEFT JOIN
    rbSpeciality AS VisitSpeciality ON VisitSpeciality.id = VisitPerson.speciality_id
        LEFT JOIN
    Action ON Action.id = Account_Item.action_id
        LEFT JOIN
    Person AS ActionPerson ON ActionPerson.id = Action.person_id
        LEFT JOIN
    rbSpeciality AS ActionSpeciality ON ActionSpeciality.id = ActionPerson.speciality_id
    WHERE
    %(cond)s"""    % {
        'cond' : cond, 
        'execPerson': '''	vrbPersonWithSpeciality.name as personName''' if detailed else u'1', 
        'execPersonJoin': ''' LEFT JOIN
    vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.execPerson_id''' if detailed else u''
        }
    if detailed:
        stmt += """
GROUP BY specialityName , personName, rbService.code , rbService.name , visitFlag
ORDER BY specialityName , personName, rbService.code , rbService.name , visitFlag
    """
    else:
        stmt += """
GROUP BY specialityName , rbService.code , rbService.name , visitFlag
ORDER BY specialityName , rbService.code , rbService.name , visitFlag
    """
    query = db.query(stmt)
    return query


def getUnitDict(accountItemIdList):
    unitDict = {}
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    tableRbMedicalAidUnit = db.table('rbMedicalAidUnit')
    queryTable = tableRbMedicalAidUnit
    queryTable = queryTable.leftJoin(tableAccountItem, tableRbMedicalAidUnit['id'].eq(tableAccountItem['unit_id']))
    cols = [tableRbMedicalAidUnit['id'], tableRbMedicalAidUnit['descr']]
    cond = [tableAccountItem['id'].inlist(accountItemIdList), ]
    records = db.getRecordListGroupBy(queryTable, cols, cond, u'rbMedicalAidUnit.id')
    for record in records:
        key = forceInt(record.value('id'))
        value = forceString(record.value('descr'))
        unitDict[key] = value
    return unitDict


def getSettleDate(accountItemIdList):
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    tableAccount = db.table('Account')
    queryTable = tableAccountItem
    queryTable = queryTable.leftJoin(tableAccount, tableAccountItem['master_id'].eq(tableAccount['id']))
    col = [u'MAX(Account.settleDate) as settleDate']
    cond = [tableAccountItem['id'].inlist(accountItemIdList), ]
    record = db.getRecordEx(queryTable, col,  cond)
    return forceString(QtCore.QDate.longMonthName(forceDate(record.value('settleDate')).month())).lower(), forceDate(record.value('settleDate')).year() 


class CPolyclinicAccountSummary(CReportBase):
    def __init__(self, parent):
        CReportBase.__init__(self, parent)
        self.setTitle(u'Финансовая сводка по амбулаторной помощи')


    def build(self, description, params):
        accountId = params.get('accountId', None)
        accountIdList = params.get('selectedAccountIdList', None)
        accountItemIdList = params.get('accountItemIdList', None)
        detailed = params.get('detailed', False)
        if accountIdList:
            numberList = u', '.join(getAccountNumbersList(accountIdList))
            accountItemIdList = getAccountItemsList(accountIdList)
        if accountId:
            number, infis, payer, recipient = self.getContract(accountId)
        if detailed:
            query = selectData(accountItemIdList, detailed = True)
        else:
            query = selectData(accountItemIdList)
        
        unitDict = getUnitDict(accountItemIdList)
        totalUnitsDict = {}
        for key, value in unitDict.items():
            totalUnitsDict[key] = [0, 0, 0, 0.0]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        
        if not accountIdList:
            tableColumns1 = [
                ('50%', [u'Наименование ЛПУ: %s'%recipient, u'код %s'%infis], CReportBase.AlignLeft),
                ('50%', [u'Наименование плательщика: %s'%payer,u''], CReportBase.AlignLeft)
            ]

        tableColumns2 = [
            ('5%', [u'№ п/п'], CReportBase.AlignLeft),
            ('10%' if detailed else '25%', [u'Наименование врачебной специальности'], CReportBase.AlignLeft),]
        
        if detailed:
            tableColumns2.append(('15%', [u'ФИО Врача'], CReportBase.AlignLeft),)
            
        tableColumns2.append(('15%', [u'Код услуги'], CReportBase.AlignLeft),)
        tableColumns2.append(('25%', [u'Наименование услуги'], CReportBase.AlignLeft),)
        tableColumns2.append(('10%', [u'Кол-во обращ. и посещ.'], CReportBase.AlignRight),)
        tableColumns2.append(('5%', [u'Кол-во услуг'], CReportBase.AlignRight),)
        tableColumns2.append(('5%', [u'Кол-во УЕТ'], CReportBase.AlignRight),)
        tableColumns2.append(('10%', [u'Стоимость'], CReportBase.AlignRight),)

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
            if detailed:
                month, year = getSettleDate(accountItemIdList)
                table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в амбулаторно-поликлинических условиях по врачам за %s месяц %s'%(month, year), CReportBase.AlignLeft), ], border = 0)
            else:
                table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в амбулаторно-поликлинических условиях по счету № %s '%number, CReportBase.AlignLeft), ], border = 0)
        else:
            if detailed:
                month, year = getSettleDate(accountItemIdList)
                table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в амбулаторно-поликлинических условиях по врачам за %s месяц %s'%(month, year), CReportBase.AlignLeft), ], border = 0)
            else:
                table = self.createTable(cursor, [(u'100%', u'Сводный отчет по  оказанным медицинским услугам в амбулаторно-поликлинических условиях по счетам № %s '%numberList, CReportBase.AlignLeft), ], border = 0)
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
        table.mergeCells(0, 7, 1, 1)
        if detailed:
            table.mergeCells(0, 8, 1, 1)
        
        i=0
        prevSpecialityName = u''
        prevPersonName = u''
        subTotalVisits = 0
        subTotalActions = 0
        subTotalEvents = 0
        subTotalUET = 0
        subTotalSum = 0
        personTotalVisits = 0
        personTotalActions = 0
        personTotalEvents = 0
        personTotalUET = 0
        personTotalSum = 0
        totalVisits = 0
        totalActions = 0
        totalEvents = 0
        totalSum = 0
        totalUET = 0
        totalXRay = {}
        totalXRay[u'A05'] = [0, 0, 0, 0.0] #MRT
        totalXRay[u'A06'] = [0, 0, 0, 0.0] #KT
        while query.next():
            record = query.record()
            specialityName = forceString(record.value('specialityName'))
            personName = forceString(record.value('personName'))
            unitId = forceInt(record.value('unitId'))
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            amount = forceInt(record.value('amount'))
            visitFlag = forceBool(record.value('visitFlag'))
            eventAmount = forceInt(record.value('eventAmount'))
            actionUet = forceDouble(record.value('actionUET'))
            itemsSum = forceDouble(record.value('itemsSum'))
            sameVisitsInEvent = forceInt(record.value('sameVisitsInEvent'))
            
            if detailed and prevPersonName!=personName and prevPersonName != u'':
                row = table.addRow()
                i+=1
                table.setText(row, 0, i)
                table.setText(row, 1, u'')
                table.setText(row, 2, u'Итого по %s'%prevPersonName, charFormat=boldChars)
                table.setText(row, 3, u'')
                table.setText(row, 4, u'')
                table.setText(row, 5, u'%i | %i'%(personTotalEvents, personTotalVisits), charFormat=boldChars)
                table.setText(row, 6, personTotalActions, charFormat=boldChars)
                table.setText(row, 7, u'%i'%(personTotalUET), charFormat=boldChars)
                table.setText(row, 8, personTotalSum, charFormat=boldChars)
                personTotalVisits = 0
                personTotalActions = 0
                personTotalEvents = 0
                personTotalUET = 0
                personTotalSum = 0

            if prevSpecialityName!=specialityName and prevSpecialityName != u'':
                row = table.addRow()
                i+=1
                table.setText(row, 0, i)
                table.setText(row, 1, u'Итого по %s'%prevSpecialityName, charFormat=boldChars)
                if detailed:
                    table.setText(row, 2, u'')
                table.setText(row, 3 if detailed else 2, u'')
                table.setText(row, 4 if detailed else 3, u'')
                table.setText(row, 5 if detailed else 4, u'%i | %i'%(subTotalEvents, subTotalVisits), charFormat=boldChars)
                table.setText(row, 6 if detailed else 5, subTotalActions, charFormat=boldChars)
                table.setText(row, 7 if detailed else 6, u'%i'%(subTotalUET), charFormat=boldChars)
                table.setText(row, 8 if detailed else 7, subTotalSum, charFormat=boldChars)
                subTotalVisits = 0
                subTotalActions = 0
                subTotalEvents = 0
                subTotalUET = 0
                subTotalSum = 0
            
            row = table.addRow()
            i+=1
            table.setText(row, 0, i)
            table.setText(row, 1, specialityName if prevSpecialityName!=specialityName else u'')
            table.setText(row, 2, personName)
            table.setText(row, 3 if detailed else 2, code)
            table.setText(row, 4 if detailed else 3, name)
            table.setText(row, 5 if detailed else 4, u'%i | %i'%(eventAmount, sameVisitsInEvent)  if visitFlag else u'')
            table.setText(row, 6 if detailed else 5, amount if not visitFlag else u'')
            table.setText(row, 7 if detailed else 6, u'%i'%(actionUet))
            table.setText(row, 8 if detailed else 7, itemsSum)
            prevSpecialityName = specialityName
            prevPersonName = personName
            if visitFlag:
                totalVisits += sameVisitsInEvent
                totalEvents += eventAmount
                subTotalVisits += sameVisitsInEvent
                personTotalVisits += sameVisitsInEvent
                subTotalEvents += eventAmount
                personTotalEvents += eventAmount
                totalUnitsDict[unitId][0] += eventAmount
                totalUnitsDict[unitId][1] += sameVisitsInEvent
                if name.startswith(u'A05'):
                    totalXRay[u'A05'][0] += eventAmount
                    totalXRay[u'A05'][1] += sameVisitsInEvent
                if name.startswith(u'A06'):
                    totalXRay[u'A06'][0] += eventAmount
                    totalXRay[u'A06'][1] += sameVisitsInEvent
            else:
                subTotalActions += amount
                personTotalActions += amount
                totalActions += amount
                totalUnitsDict[unitId][2] += amount
                if name.startswith(u'A05'):
                    totalXRay[u'A05'][2] += amount
                if name.startswith(u'A06'):
                    totalXRay[u'A06'][2] += amount
            totalSum += itemsSum
            subTotalSum += itemsSum
            personTotalSum += itemsSum
            totalUET += actionUet
            subTotalUET += actionUet
            personTotalUET += actionUet
            totalUnitsDict[unitId][3] += itemsSum
            if name.startswith(u'A05'):
                totalXRay[u'A05'][3] += itemsSum
            if name.startswith(u'A06'):
                totalXRay[u'A06'][3] += itemsSum

        if detailed:
            row = table.addRow()
            i+=1
            table.setText(row, 0, i)
            table.setText(row, 1, u'')
            table.setText(row, 2, u'Итого по %s'%personName, charFormat=boldChars)
            table.setText(row, 3, u'')
            table.setText(row, 4, u'')
            table.setText(row, 5, u'%i | %i'%(personTotalEvents, personTotalVisits), charFormat=boldChars)
            table.setText(row, 6, personTotalActions, charFormat=boldChars)
            table.setText(row, 7, personTotalUET, charFormat=boldChars)
            table.setText(row, 8, personTotalSum, charFormat=boldChars)
            personTotalVisits = 0
            personTotalActions = 0
            personTotalEvents = 0
            personTotalSum = 0
            personTotalUET = 0

        row = table.addRow()
        i+=1
        table.setText(row, 0, i)
        table.setText(row, 1, u'Итого по %s'%prevSpecialityName, charFormat=boldChars)
        if detailed:
            table.setText(row, 2, u'')
        table.setText(row, 3 if detailed else 2, u'')
        table.setText(row, 4 if detailed else 3, u'')
        table.setText(row, 5 if detailed else 4, u'%i | %i'%(subTotalEvents, subTotalVisits), charFormat=boldChars)
        table.setText(row, 6 if detailed else 5, subTotalActions, charFormat=boldChars)
        table.setText(row, 7 if detailed else 6, subTotalUET, charFormat=boldChars)
        table.setText(row, 8 if detailed else 7, subTotalSum, charFormat=boldChars)
        subTotalVisits = 0
        subTotalActions = 0
        subTotalEvents = 0
        subTotalSum = 0
        subTotalUET = 0
        
        for key, value in unitDict.items():
            if totalUnitsDict[key][0] !=0 or totalUnitsDict[key][1] !=0 or totalUnitsDict[key][2] !=0 or totalUnitsDict[key][3] !=0.0:
                row = table.addRow()
                i+=1        
                table.setText(row, 0, i)
                table.setText(row, 1, u'Итого %s'%value, charFormat=boldChars)
                if detailed:
                    table.setText(row, 2, u'')
                table.setText(row, 3 if detailed else 2, u'')
                table.setText(row, 4 if detailed else 3, u'')
                table.setText(row, 5 if detailed else 4, u'%i | %i'%(totalUnitsDict[key][0], totalUnitsDict[key][1]), charFormat=boldChars)
                table.setText(row, 6 if detailed else 5, totalUnitsDict[key][2], charFormat=boldChars)
                table.setText(row, 7 if detailed else 6, u'', charFormat=boldChars)
                table.setText(row, 8 if detailed else 7, totalUnitsDict[key][3], charFormat=boldChars)

        for key, value in totalXRay.items():
            if totalXRay[key][0] !=0 or totalXRay[key][1] !=0 or totalXRay[key][2] !=0 or totalXRay[key][3] !=0.0:
                row = table.addRow()
                i+=1        
                table.setText(row, 0, i)
                table.setText(row, 1, u'Итого %s'%value, charFormat=boldChars)
                if detailed:
                    table.setText(row, 2, u'')
                table.setText(row, 3 if detailed else 2, u'')
                table.setText(row, 4 if detailed else 3, u'')
                table.setText(row, 5 if detailed else 4, u'%i | %i'%(totalXRay[key][0], totalXRay[key][1]), charFormat=boldChars)
                table.setText(row, 6 if detailed else 5, totalXRay[key][2], charFormat=boldChars)
                table.setText(row, 7 if detailed else 6, u'', charFormat=boldChars)
                table.setText(row, 8 if detailed else 7, totalXRay[key][3], charFormat=boldChars)

        row = table.addRow()
        i+=1        
        table.setText(row, 0, i)
        table.setText(row, 1, u'Итого по ЛПУ', charFormat=boldChars)
        if detailed:
            table.setText(row, 2, u'')
        table.setText(row, 3 if detailed else 2, u'')
        table.setText(row, 4 if detailed else 3, u'')
        table.setText(row, 5 if detailed else 4, u'%i | %i'%(totalEvents, totalVisits), charFormat=boldChars)
        table.setText(row, 6 if detailed else 5, totalActions, charFormat=boldChars)
        table.setText(row, 7 if detailed else 6, totalUET, charFormat=boldChars)
        table.setText(row, 8 if detailed else 7, totalSum, charFormat=boldChars)

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
