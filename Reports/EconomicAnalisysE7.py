# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

from library.Utils import forceString, forceInt, forceDouble
from EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog
from EconomicAnalisys import getStmt, colClient, colEvent, colOrgStructure, colParentOrgStructure, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM

class CEconomicAnalisysE7(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Э-7. Анализ нагрузки на подразделения')

    def selectData(self, params):
        cols = [colClient, colEvent, colOrgStructure, colParentOrgStructure, colCSG, colPos, colObr, colSMP, colKD, colPD, colUET, colAmount, colSUM]
        colsStmt = u"""select colParentOrgStructure as nam,
        colOrgStructure as osname,
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
        groupCols = u'colParentOrgStructure, colOrgStructure'
        orderCols = u'colParentOrgStructure, colOrgStructure'
        
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
                nam = forceString(record.value('nam'))
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
                osname = osname if osname else '---'
                key = (nam if nam else u'Без отделения',
                       osname)
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
            ('35%', [u'Отделение'], CReportBase.AlignLeft),
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
        prevOrgName = None
        orgName = None
        prevnum = None
        keys = reportData.keys()
        keys.sort()

        def drawTotal(table,  total,  text):

            row = table.addRow()

            table.setText(row, 1, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 12)
        for key in keys:
            orgName = key[0]
            osName = key[1]

            if prevOrgName != orgName and prevOrgName is not None:
                row = table.addRow()
                table.setText(row, 0, u'Итого по %s' % prevOrgName,  CReportBase.TableHeader)
                for col in xrange(reportRowSize-2):
                    table.setText(row, col + colsShift, totalByFinance[col])
                    totalByReport[col] = totalByReport[col] + totalByFinance[col]
                totalByFinance = [0]*reportRowSize
                prevOrgName = orgName
            if prevnum != orgName:
                row = table.addRow()
                table.setText(row, 0, orgName, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 12)

            prevOrgName = orgName
            row = table.addRow()
            table.setText(row, 0, osName)
            prevnum = orgName

            reportLine = reportData[key]
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, reportLine[col])
                totalByFinance[col] = totalByFinance[col] + reportLine[col]
        if orgName is not None:
            row = table.addRow()
            table.setText(row, 0, u'Итого по %s' % orgName, CReportBase.TableHeader)
            for col in xrange(reportRowSize-2):
                table.setText(row, col + colsShift, totalByFinance[col])
                totalByReport[col] = totalByReport[col] + totalByFinance[col]
        row = table.addRow()
        table.setText(row, 0, u'Итого', CReportBase.TableHeader)
        for col in xrange(reportRowSize-2):
            table.setText(row, col + colsShift, totalByReport[col])

        return doc


class CEconomicAnalisysE7Ex(CEconomicAnalisysE7):
    def exec_(self, accountIdList=None):
        self.accountIdList = accountIdList
        CEconomicAnalisysE7.exec_(self)

    def getSetupDialog(self, parent):
        result = CEconomicAnalisysSetupDialog(parent)
        result.setTitle(self.title())
        result.shrink()
        return result

    def build(self, params):
        params['accountIdList'] = self.accountIdList
        return CEconomicAnalisysE7.build(self, '\n'.join(self.getDescription(params)), params)
