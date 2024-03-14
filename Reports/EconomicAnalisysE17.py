# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from Reports.Report import CReport, createTable
from Reports.ReportBase import CReportBase

from library.Utils import forceString, forceInt, forceDouble
from EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog
from EconomicAnalisys import getStmt, colClient, colEvent, colPerson, colServiceInfis, colServiceName, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM


class CEconomicAnalisysE17(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Э-17. Выполненные объемы услуг по врачам')


    def selectData(self, params):
        cols = [colClient, colEvent, colPerson, colServiceInfis, colServiceName, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM]
        colsStmt = u"""select colPerson as person,
        colServiceInfis as infis,
        colServiceName as name,
        count(distinct colEvent) as cnt,
        count(distinct colClient) as fl,
        sum(colAmount) as amount,
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
        groupCols = u'colPerson, colServiceInfis, colServiceName'
        orderCols = u'colPerson, colServiceInfis, colServiceName'

        stmt = getStmt(colsStmt, cols, groupCols, orderCols, params)

        return QtGui.qApp.db.query(stmt)
        

    def build(self, description, params):
        reportRowSize = 15
        reportData = {}

        def processQuery(query):
            while query.next():
                record = query.record()
                person = forceString(record.value('person'))
                infis = forceString(record.value('infis'))
                name = forceString(record.value('name'))
                amount = forceInt(record.value('amount'))
                kd = forceInt(record.value('kd'))
                pd = forceInt(record.value('pd'))
                uet = forceDouble(record.value('uet'))
                sum = forceDouble(record.value('sum'))
                mes = forceInt(record.value('mes'))
                pos = forceInt(record.value('pos'))
                obr = forceInt(record.value('obr'))
                usl = forceInt(record.value('usl'))
                callambulance = forceInt(record.value('callambulance'))

                key = (person if person else u'Не задано', infis,   name)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += amount
                reportLine[1] += kd
                reportLine[2] += pd
                reportLine[3] += uet
                reportLine[4] += sum
                reportLine[5] += mes
                reportLine[6] += pos
                reportLine[7] += obr
                reportLine[8] += usl
                reportLine[9] += callambulance
                if mes > 0:
                    reportLine[10] += sum
                if pos > 0:
                    reportLine[11] += sum
                if obr > 0:
                    reportLine[12] += sum
                if usl > 0:
                    reportLine[13] += sum
                if callambulance > 0:
                    reportLine[14] += sum

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
            ('10%',  [u'Услуга', u'Код'], CReportBase.AlignLeft),
            ('40%',  ['', u'Наименование'], CReportBase.AlignLeft),
            ('10%',  [u'Кол-во услуг'], CReportBase.AlignRight),
            ('10%',  [u'Кол-во койко-дней'], CReportBase.AlignRight),
            ('10%',  [u'Кол-во дней лечения'], CReportBase.AlignRight),
            ('10%',  [u'Кол-во УЕТ'], CReportBase.AlignRight),
            ('10%',  [u'Сумма'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 2)
        table.mergeCells(1, 2, 1, 10)
        totalByPerson = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        colsShift = 2
        prevPerson = None
        person = None

        keys = reportData.keys()
        keys.sort()

        # чтобы не повторять кусок кода, надо будет улучшить
        def drawTotal(table,  totalByPerson):

            row = table.addRow()

            table.setText(row, 1, u'кол-во КСГ', CReportBase.TableHeader,  CReportBase.AlignRight)
            table.setText(row, 2, totalByPerson[5],  CReportBase.TableHeader,  CReportBase.AlignLeft)
            table.setText(row, 6, totalByPerson[10],  CReportBase.TableHeader)
            row = table.addRow()
            table.setText(row, 1, u'кол-во посещений', CReportBase.TableHeader,  CReportBase.AlignRight)
            table.setText(row, 2, totalByPerson[6],  CReportBase.TableHeader,  CReportBase.AlignLeft)
            table.setText(row, 6, totalByPerson[11],  CReportBase.TableHeader)
            row = table.addRow()
            table.setText(row, 1, u'кол-во обращений', CReportBase.TableHeader,  CReportBase.AlignRight)
            table.setText(row, 2, totalByPerson[7],  CReportBase.TableHeader,  CReportBase.AlignLeft)
            table.setText(row, 6, totalByPerson[12],  CReportBase.TableHeader)
            row = table.addRow()
            table.setText(row, 1, u'кол-во простых услуг', CReportBase.TableHeader,  CReportBase.AlignRight)
            table.setText(row, 2, totalByPerson[8],  CReportBase.TableHeader,  CReportBase.AlignLeft)
            table.setText(row, 6, totalByPerson[13],  CReportBase.TableHeader)
            row = table.addRow()
            table.setText(row, 1, u'кол-во вызовов СМП', CReportBase.TableHeader,  CReportBase.AlignRight)
            table.setText(row, 2, totalByPerson[9],  CReportBase.TableHeader,  CReportBase.AlignLeft)
            table.setText(row, 6, totalByPerson[14],  CReportBase.TableHeader)

        for key in keys:
            person = key[0]
            uslugaKod = key[1]
            usluga = key[2]

            if prevPerson != person:
                if prevPerson is not None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого по врачу %s' % prevPerson)
                    for col in xrange(reportRowSize):
                        if col < 5:
                            table.setText(row, col + colsShift, totalByPerson[col])
                        totalByReport[col] = totalByReport[col] + totalByPerson[col]
                    drawTotal(table,  totalByPerson)
                    totalByPerson = [0]*reportRowSize

                row = table.addRow()
                table.setText(row, 0, u'Врач: %s' % person,  CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 7)
                prevPerson = person

            row = table.addRow()
            table.setText(row, 0, uslugaKod)
            table.setText(row, 1, usluga)
            reportLine = reportData[key]
            for col in xrange(reportRowSize):
                if col < 5:
                    table.setText(row, col + colsShift, reportLine[col])
                totalByPerson[col] = totalByPerson[col] + reportLine[col]
        if prevPerson != person:
            if prevPerson is not None:
                row = table.addRow()
                table.setText(row, 0, u'Итого по врачу %s' % prevPerson)
                for col in xrange(reportRowSize):
                    if col < 5:
                        table.setText(row, col + colsShift, totalByPerson[col])
                    totalByReport[col] = totalByReport[col] + totalByPerson[col]

        if prevPerson is not None:
            row = table.addRow()
            table.setText(row, 0, u'Итого по врачу %s' % prevPerson)
            for col in xrange(reportRowSize):
                if col < 5:
                    table.setText(row, col + colsShift, totalByPerson[col])
                totalByReport[col] = totalByReport[col] + totalByPerson[col]
            drawTotal(table,  totalByPerson)
        row = table.addRow()
        table.setText(row, 0, u'Итого')
        for col in xrange(reportRowSize):
            if col < 5:
                table.setText(row, col + colsShift, totalByReport[col])
        drawTotal(table, totalByReport)
        return doc


class CEconomicAnalisysE17Ex(CEconomicAnalisysE17):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CEconomicAnalisysE17.exec_(self)

    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        result.shrink()
        return result

    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CEconomicAnalisysE17.build(self, '\n'.join(self.getDescription(params)), params)
