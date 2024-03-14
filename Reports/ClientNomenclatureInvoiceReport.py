# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QDate

from library.Utils      import forceDate, forceRef, forceString, forceDouble, formatNameByRecord
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr
from Orgs.Utils         import getOrgStructureFullName

from Reports.PlannedClientInvoiceNomenclaturesReport import CNomenclatureReportDialog


def getRemainingsOnMonthsFirstDays(begDate, endDate, orgStructureId):
    begDate = begDate.addMonths(-1)

    db = QtGui.qApp.db
    table = db.table('StockTrans')

    debCond = [
        # table['date'].dateGe(begDate),
        table['date'].dateLe(endDate)
    ]
    creCond = [
        # table['date'].dateGe(begDate),
        table['date'].dateLe(endDate)
    ]

    if orgStructureId:
        debCond.extend(
            [table['debOrgStructure_id'].eq(orgStructureId), table['creOrgStructure_id'].nullSafeNe(orgStructureId)]
        )
        creCond.extend(
            [table['creOrgStructure_id'].eq(orgStructureId), table['debOrgStructure_id'].nullSafeNe(orgStructureId)]
        )
    else:
        debCond.extend(
            [table['debOrgStructure_id'].isNotNull(), table['creOrgStructure_id'].isNull()]
        )
        creCond.extend(
            [table['creOrgStructure_id'].isNotNull(), table['debOrgStructure_id'].isNull()]
        )

    stmt = """
SELECT
    T.nomenclature_id, month_date, sum(T.qnt) AS `qnt`
FROM (
    SELECT
        debNomenclature_id AS nomenclature_id, sum(StockTrans.qnt) AS `qnt`,
        LAST_DAY(date) AS month_date
    FROM
        StockTrans
    LEFT JOIN StockMotion_Item ON StockMotion_Item.id = StockTrans.stockMotionItem_id
    WHERE {debCond} AND (StockMotion_Item.deleted=0)
    GROUP BY nomenclature_id, month_date
    UNION ALL
    SELECT
        creNomenclature_id AS nomenclature_id, -sum(StockTrans.qnt) AS `qnt`,
        LAST_DAY(date) AS month_date
    FROM
        StockTrans
    LEFT JOIN StockMotion_Item ON StockMotion_Item.id = StockTrans.stockMotionItem_id
    WHERE {creCond} AND (StockMotion_Item.deleted=0)
    GROUP BY nomenclature_id, month_date
) AS T
GROUP BY T.nomenclature_id, month_date
"""

    query = db.query(
        stmt.format(
            debCond=db.joinAnd(debCond), creCond=db.joinAnd(creCond)
        )
    )

    result = {}

    while query.next():
        record = query.record()
        nomenclatureId = forceRef(record.value('nomenclature_id'))
        date = forceDate(record.value('month_date')).addDays(1)
        qnt = forceDouble(record.value('qnt'))

        result.setdefault(nomenclatureId, {})[forceString(date)] = qnt

    for key, values in result.items():
        prev_qnt = 0
        for date in sorted(values.keys()):
            result[key][date] += prev_qnt
            prev_qnt = result[key][date]

    return result


def _selectData(begDate, endDate, clientId=None, **kwargs):
    nomenclatureId = kwargs.get('nomenclatureId')
    orgStructureId = kwargs.get('orgStructureId')

    remainingsByMonths = getRemainingsOnMonthsFirstDays(begDate, endDate, orgStructureId)

    db = QtGui.qApp.db

    tableSM = db.table('StockMotion')
    tableSMI = db.table('StockMotion_Item')
    tableClient = db.table('Client')
    tableNomenclature = db.table('rbNomenclature')

    cond = [ tableSM['client_id'].isNotNull(),
             tableSM['type'].eq(4), # только движения с типом "списание на пациента"
             tableSM['deleted'].eq(0),
             tableSMI['deleted'].eq(0),
             tableClient['deleted'].eq(0),
           ]

    if begDate:
        cond.append(tableSM['date'].dateGe(begDate))

    if endDate:
        cond.append(tableSM['date'].dateLt(endDate.addDays(1)))

    if nomenclatureId:
        cond.append(tableSMI['nomenclature_id'].eq(nomenclatureId))

    if clientId:
        cond.append(tableSM['client_id'].eq(clientId))

    if orgStructureId:
        cond.append(tableSM['supplier_id'].eq(orgStructureId))

    remainingAfterInvoice = 'getNomenclatureRemaining({0}, StockMotion_Item.nomenclature_id, StockMotion.date) AS remainingAfterInvoice' \
        .format(orgStructureId if orgStructureId else 'NULL')

    fields = [
        tableClient['id'].alias('clientId'), tableNomenclature['name'].alias('nomenclatureName'),
        tableNomenclature['id'].alias('nomenclatureId'), 'SUM(StockMotion_Item.qnt) as qnt',
        tableClient['firstName'], tableClient['lastName'], tableClient['patrName'],
        tableSM['date'],
        remainingAfterInvoice,
        tableSMI['nomenclature_id']
    ]

    queryTable = tableSM \
        .innerJoin(tableSMI, tableSMI['master_id'].eq(tableSM['id'])) \
        .innerJoin(tableClient, tableClient['id'].eq(tableSM['client_id'])) \
        .innerJoin(tableNomenclature, tableNomenclature['id'].eq(tableSMI['nomenclature_id']))

    group = u'StockMotion.client_id, DATE(StockMotion.`date`), rbNomenclature.`id`'

    stmt = db.selectStmtGroupBy(queryTable, fields, cond, group, order=tableSM['date'].name())

    query = db.query(stmt)

    result = {}

    while query.next():
        record = query.record()
        clientId = forceRef(record.value('clientId'))
        clientName = formatNameByRecord(record)
        remainingAfterInvoice = forceDouble(record.value('remainingAfterInvoice'))
        qnt = forceDouble(record.value('qnt'))
        date = forceDate(record.value('date'))
        nomenclatureId = forceRef(record.value('nomenclatureId'))
        nomenclatureName = forceString(record.value('nomenclatureName'))

        monthDateKey = forceString(QDate(date.year(), date.month(), 1))

        result \
            .setdefault((clientId, clientName), {}) \
            .setdefault((date.year(), date.month()), []).append({
                'qnt': qnt,
                'remainingAfterInvoice': remainingAfterInvoice,
                'day': date.day(),
                'nomenclatureName': nomenclatureName,
                'nomenclatureId': nomenclatureId,
                'remainingOnFirstMonthDay': remainingsByMonths.get(nomenclatureId, {}).get(monthDateKey, 0)
            })

    return result



class CClientNomenclatureInvoiceReport(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет выданных ЛСиИМН пациенту')

    def getSetupDialog(self, parent):
        result = CNomenclatureReportDialog(parent)
        result.setDatesVisible(True)
        result.setMonthVisible(False)
        result.setClientIdVisible(True)
        result.setOrgStructureVisible(True)
        result.setSignaVisible(False)
        result.setNomenclatureVisible(True)
        result.setSupplierVisible(False)
        result.setSupplierOrgVisible(False)
        result.setReceiverVisible(False)
        result.setReceiverPersonVisible(False)
        result.setFinanceVisible(False)
        result.setOnlyExists(False)
        result.edtBegTime.setVisible(False)
        result.edtEndTime.setVisible(False)
        return result

    def build(self, params):
        tableColumns = [
            ('40%', [u''], CReportBase.AlignLeft),
            ('20%', [u''], CReportBase.AlignRight),
            ('20%', [u''], CReportBase.AlignRight),
            ('20%', [u''], CReportBase.AlignRight),
        ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        months = [
            u'Январь',
            u'Февраль',
            u'Март',
            u'Апрель',
            u'Май',
            u'Июнь',
            u'Июль',
            u'Август',
            u'Сентябрь',
            u'Октябрь',
            u'Ноябрь',
            u'Декабрь',
        ]

        data  = _selectData(**params)
        clients = set()

        for clientId, clientName in sorted(data.keys(), key=lambda i: i[1]):

            clients.add(clientId)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.setCharFormat(CReportBase.ReportSubTitle)
            cursor.insertText(clientName)
            cursor.insertBlock()

            table = createTable(cursor, tableColumns)

            firstMonth = True
            sum = 0

            dateData = data[(clientId, clientName)]
            for year, month in sorted(dateData, key=lambda i: (i[0], i[1])):
                row = table.addRow()

                if firstMonth:
                    table.setText(row, 0, u'Наименование ЛС')
                    table.setText(row, 1, u'Дата')
                    table.setText(row, 2, u'Кол-во (в расход.ед.)')
                    table.setText(row, 3, u'Подпись')
                    for col in range(4):
                        table.mergeCells(row-1, col, 2, 1)
                    row = table.addRow()

                    firstMonth = False

                table.setText(row, 0, months[month - 1], blockFormat=CReportBase.AlignCenter)
                table.mergeCells(row, 0, 1, 4)

                monthData = dateData[(year, month)]
                for dayData in monthData:
                    row = table.addRow()
                    sum += dayData['qnt']

                    table.setText(row, 0, dayData['nomenclatureName'])
                    table.setText(row, 1, dayData['day'])
                    table.setText(row, 2, dayData['qnt'])
                    table.setText(row, 3, '')

            row = table.addRow()
            table.setText(row, 0, u'Итого (в расход.ед.)')
            table.mergeCells(row, 0, 1, 2)
            table.setText(row, 2, sum)
            table.setText(row, 3, '')

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertText(u'\n\nКоличество пациентов, получивших ЛСиИМН: %d' % len(clients))

        return doc

    def dumpParams(self, cursor, params):
        description = []
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        nomenclatureId = params.get('nomenclatureId', None)
        orgStructureId = params.get('orgStructureId', None)
        clientId = params.get('clientId', None)

        if begDate and endDate:
            description.append(dateRangeAsStr(u'За период', begDate, endDate))
        if nomenclatureId:
            description.append(u'ЛС: %s'%(forceString(db.translate('rbNomenclature', 'id', nomenclatureId, 'name'))))
        if orgStructureId:
            description.append(u'Подразделение: ' + getOrgStructureFullName(orgStructureId))
        if clientId:
            description.append(u'Код пациента: %s' %clientId)

        description.append(u'отчёт составлен: '+forceString(QtCore.QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
