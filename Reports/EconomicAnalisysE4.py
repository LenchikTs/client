# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from Reports.Report import CReport, createTable
from Reports.ReportBase import CReportBase

from library.Utils import forceString, forceInt, forceDouble
from EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog
from EconomicAnalisys import getStmt, colClient, colEvent, colFinance, colPerson, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM


class CEconomicAnalisysE4(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Э-4. Анализ нагрузки на врачей по видам финансирования')

    def selectData(self, params):
        cols = [colClient, colEvent, colFinance, colPerson, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM]
        colsStmt = u"""select colFinance as fin,
        colPerson as person,
        count(distinct colEvent) as cnt,
        count(distinct colClient) as fl,
        sum(colCSG) as mes,
        sum(colPos) as pos,
        sum(colObr) as obr,
        round(sum(colUET), 2) as uet,
        sum(colKD) as kd,
        sum(colPD) as pd,
        sum(colSMP) as callambulance,
        sum(IF(colPos = 0 and colCSG = 0 and colSMP = 0 and colObr = 0, colAmount, 0)) as usl,
        round(sum(colSUM), 2) as sum
        """
        groupCols = u'colFinance, colPerson'
        orderCols = u'colFinance, colPerson'
        stmt = getStmt(colsStmt, cols, groupCols, orderCols, params)

        return QtGui.qApp.db.query(stmt)

    def build(self, description, params):
        reportRowSize = 13
        reportData = {}

        def processQuery(query):
            while query.next():
                record = query.record()
                fin = forceString(record.value('fin'))
                person = forceString(record.value('person'))
                cnt = forceInt(record.value('cnt'))
                fl = forceInt(record.value('fl'))
                mes = forceInt(record.value('mes'))
                pos = forceInt(record.value('pos'))
                obr = forceInt(record.value('obr'))
                kd = forceInt(record.value('kd'))
                pd = forceInt(record.value('pd'))
                usl = forceInt(record.value('usl'))
                callambulance = forceInt(record.value('callambulance'))
                uet = forceDouble(record.value('uet'))
                sum = forceDouble(record.value('sum'))

                key = (fin if fin else u'Без вида финансирования',
                       person)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += cnt
                reportLine[1] += fl
                reportLine[2] += mes
                reportLine[3] += kd
                reportLine[4] += pd
                reportLine[5] += pos
                reportLine[6] += obr
                reportLine[7] += uet
                reportLine[8] += usl
                reportLine[9] += callambulance
                reportLine[10] += sum

        query = self.selectData(params)
        processQuery(query)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        tableColumns = [
            ('35%', [u'Вид оплаты / Врач'], CReportBase.AlignLeft),
            ('5%', [u'Кол-во случаев'], CReportBase.AlignRight),
            ('5%', [u'Кол-во пациентов'], CReportBase.AlignRight),
            ('5%', [u'Кол-во КСГ'], CReportBase.AlignRight),
            ('5%', [u'Кол-во койко-дней'], CReportBase.AlignRight),
            ('5%', [u'Кол-во дней лечения'], CReportBase.AlignRight),
            ('5%', [u'Кол-во посещений'], CReportBase.AlignRight),
            ('5%', [u'Кол-во обращений'], CReportBase.AlignRight),
            ('5%', [u'Кол-во УЕТ'], CReportBase.AlignRight),
            ('5%', [u'Кол-во простых услуг'], CReportBase.AlignRight),
            ('5%', [u'Кол-во вызовов СМП'], CReportBase.AlignRight),
            ('15%', [u'Сумма'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        totalByFinance = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        colsShift = 1
        prevFinanceName = None
        financeName = None

        keys = reportData.keys()
        keys.sort()
        for key in keys:
            financeName = key[0]
            person = key[1]

            if prevFinanceName != financeName:
                if prevFinanceName is not None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого по %s' % financeName)
                    for col in xrange(reportRowSize-2):
                        table.setText(row, col + colsShift, totalByFinance[col])
                        totalByReport[col] = totalByReport[col] + totalByFinance[col]
                    totalByFinance = [0]*reportRowSize

                row = table.addRow()
                table.setText(row, 0, u'Вид финансирования: %s' % financeName,  CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 12)
                prevFinanceName = financeName

            row = table.addRow()
            table.setText(row, 0, person)

            reportLine = reportData[key]
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, reportLine[col])
                totalByFinance[col] = totalByFinance[col] + reportLine[col]
        if prevFinanceName != financeName:
            if prevFinanceName is not None:
                row = table.addRow()
                table.setText(row, 0, u'Итого по %s' % financeName)
                for col in xrange(reportRowSize-2):
                    table.setText(row, col + colsShift, totalByFinance[col])
                    totalByReport[col] = totalByReport[col] + totalByFinance[col]

        if prevFinanceName is not None:
            row = table.addRow()
            table.setText(row, 0, u'Итого по %s' % financeName)
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, totalByFinance[col])
                totalByReport[col] = totalByReport[col] + totalByFinance[col]

        row = table.addRow()
        table.setText(row, 0, u'Итого')
        for col in xrange(reportRowSize-2):
            table.setText(row, col + colsShift, totalByReport[col])

        return doc


class CEconomicAnalisysE4Ex(CEconomicAnalisysE4):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CEconomicAnalisysE4.exec_(self)

    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        result.shrink()
        return result

    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CEconomicAnalisysE4.build(self, '\n'.join(self.getDescription(params)), params)
