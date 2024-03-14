# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from Reports.Report import CReport, createTable
from Reports.ReportBase import CReportBase

from library.Utils import forceString, forceInt, forceDouble
from EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog
from EconomicAnalisys import getStmt, colClient, colEvent, colFinance, colOrgStructure, colPerson, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM


class CEconomicAnalisysE9(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Форма Э-9. Сводка о выполненных медицинских услугах по врачам')

    def selectData(self, params):
        cols = [colClient, colEvent, colFinance, colOrgStructure, colPerson, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM]
        colsStmt = u"""select colFinance as fin,
        colOrgStructure as osname,
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
        groupCols = u'colFinance, colOrgStructure, colPerson'
        orderCols = u'colFinance, colOrgStructure, colPerson'
        
        stmt = getStmt(colsStmt, cols, groupCols, orderCols, params)

        db = QtGui.qApp.db
        return db.query(stmt)

    def build(self, description, params):
        reportRowSize = 13
        reportData = {}

        def processQuery(query):
            while query.next():
                record = query.record()
                osname = forceString(record.value('osname'))
                person = forceString(record.value('person'))
                fin = forceString(record.value('fin'))
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

                key = (person,  fin,  osname if osname else u'Без подразделения')
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
            ('35%', [u'Подразделение'], CReportBase.AlignLeft),
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
        totalByFin = [0]*reportRowSize
        totalByPerson = [0]*reportRowSize
        totalByReport = [0]*reportRowSize

        colsShift = 1
        prevFin = None
        fin = None
        prevPerson = None
        person = None

        keys = reportData.keys()
        keys.sort()

        #очень много повторюшек, это плохо :с
        for key in keys:
            person = key[0]
            fin = key[1]
            osname = key[2]
            if prevPerson != person:
                if prevFin is not None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого по %s' % prevFin)
                    for col in xrange(reportRowSize-2):
                        table.setText(row, col + colsShift, totalByFin[col])
                    totalByFin = [0]*reportRowSize
                if prevPerson is not None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого по %s' % prevPerson)
                    for col in xrange(reportRowSize-2):
                        table.setText(row, col + colsShift, totalByPerson[col])
                        totalByReport[col] = totalByReport[col] + totalByPerson[col]
                    totalByPerson = [0]*reportRowSize
                row = table.addRow()
                table.setText(row, 0, person,  CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 12)
                prevPerson = person
                prevFin = None
            ###
            if prevFin != fin:
                if prevFin is not None:
                    row = table.addRow()
                    table.setText(row, 0, u'Итого по %s' % prevFin)
                    for col in xrange(reportRowSize-2):
                        table.setText(row, col + colsShift, totalByFin[col])
                    totalByFin = [0]*reportRowSize
                row = table.addRow()
                table.setText(row, 0, u'Вид финансирования %s' % fin,  CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 12)
                prevFin = fin
            ###
            row = table.addRow()
            table.setText(row, 0, osname)
            reportLine = reportData[key]
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, reportLine[col])
                totalByFin[col] = totalByFin[col] + reportLine[col]
                totalByPerson[col] = totalByPerson[col] + reportLine[col]
            ###
        if fin is not None:
            row = table.addRow()
            table.setText(row, 0, u'Итого по %s' % fin)
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, totalByFin[col])
        if person is not None:
            row = table.addRow()
            table.setText(row, 0, u'Итого по %s' % person)
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, totalByPerson[col])
                totalByReport[col] = totalByReport[col] + totalByPerson[col]
        row = table.addRow()
        table.setText(row, 0, u'Итого')
        for col in xrange(reportRowSize-2):
            table.setText(row, col + colsShift, totalByReport[col])

        return doc


class CEconomicAnalisysE9Ex(CEconomicAnalisysE9):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CEconomicAnalisysE9.exec_(self)

    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        result.shrink()
        return result

    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CEconomicAnalisysE9.build(self, '\n'.join(self.getDescription(params)), params)
