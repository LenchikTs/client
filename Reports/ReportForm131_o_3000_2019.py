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

from library.Utils                     import forceDate, forceInt, forceRef, forceString
from Events.ActionStatus               import CActionStatus
from Reports.Report                    import CReport
from Reports.ReportBase                import CReportBase, createTable
from Reports.ReportSetupDialog         import CReportSetupDialog
from Reports.ReportForm131_o_3000_2016 import selectData


class CReportForm131_o_3000_2019(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о втором этапе диспансеризации определенных групп взрослого населения (2019)')
        self.mapNumMesVisitCodeToRow = {
                55 : 0,
                44 : 1,
                96 : 2,
                50 : 3,
                49 : 3,
                45 : 4,
                46 : 4,
                57 : 5,
                53 : 6,
                90 : 7,
                48 : 8,
                54 : 9,
                91 : 10,
                20 : 11,
                47 : 12,
                52 : 13,
                59 : 14,
                17 : 15,
            }
        self.rowNames = [
                          u'Дуплексное сканирование брахицефальных артерий',
                          u'Осмотр (консультация) врачом-неврологом',
                          u'Эзофагогастродуоденоскопия ',
                          u'Осмотр (консультация) врачом-хирургом или врачом-урологом',
                          u'Осмотр (консультация) врачом-хирургом или врачом-колопроктологом',
                          u'Колоноскопия или ректороманоскопия',
                          u'Определение липидного спектра крови',
                          u'Спирометрия',
                          u'Осмотр (консультация) врачом-акушером-гинекологом',
                          u'Определение концентрации гликированного гемоглобина в крови или тест на толерантность к глюкозе',
                          u'Осмотр (консультация) врачом-оториноларингологом',
                          u'Анализ крови на уровень содержания простатспецифического антигена',
                          u'Осмотр (консультация) врачом-офтальмологом',
                          u'Индивидуальное углубленное профилактическое консультирование',
                          u'Групповое профилактическое консультирование (школа пациента)',
                          u'Прием (осмотр) врача-терапевта',
                        ]


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMesDispansListVisible(True)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result


    def _getDefault(self):
        result = [ [0, 0, 0, 0, 0]
                   for row in self.rowNames
                 ]
        return result


    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0, 0]
        uniqueSet = set()
        while query.next():
            record = query.record()
            actionId           = forceRef(record.value('actionId'))
            actionMkb          = forceString(record.value('actionMkb'))
            numMesVisitCode    = forceInt(record.value('numMesVisitCode'))
            actionExecNow      = forceInt(record.value('actionExecNow'))
            actionExecPrev     = forceInt(record.value('actionExecPrev'))
            propertyEvaluation = forceInt(record.value('propertyEvaluation'))
            endDate            = forceDate(record.value('endDate'))
            execDate           = forceDate(record.value('execDate'))
            status             = forceInt(record.value('status'))
            actionExecRefusal  = (not endDate) and (status == CActionStatus.refused)
            if numMesVisitCode not in self.mapNumMesVisitCodeToRow:
                continue
            key = actionId
            if key in uniqueSet:
                continue
            uniqueSet.add(key)
            row = self.mapNumMesVisitCodeToRow[numMesVisitCode]
            reportLine = reportData[row]
            if status != CActionStatus.canceled:  # if needToPayAttention:
                reportLine[0] += 1
                reportDataTotal[0] += 1
            if execDate and endDate and status == CActionStatus.finished: # refused:
                if actionExecNow:
                    reportLine[1] += 1
                    reportDataTotal[1] += 1
                elif actionExecPrev:
                    reportLine[2] += 1
                    reportDataTotal[2] += 1
            if actionExecRefusal:
                reportLine[3] += 1
                reportDataTotal[3] += 1
            if ('A00' <= actionMkb < 'U' or propertyEvaluation) and row not in (13, 14):
                reportLine[4] += 1
                reportDataTotal[4] += 1
        return reportData, reportDataTotal


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(3000)')
        cursor.insertBlock()
        tableColumns = [
            ( '45%', [u'Медицинское мероприятие второго этапа диспансеризации', u'', u'1'], CReportBase.AlignLeft),
            ( '3%',  [u'№ строки', u'', u'2'], CReportBase.AlignRight),
            ( '10%', [u'Выявлено показание к дополнительному обследованию', u'', u'3'], CReportBase.AlignRight),
            ( '10%', [u'Количество выполненных медицинских мероприятий', u'в рамках диспансе-ризации', u'4'], CReportBase.AlignRight),
            ( '10%', [u'', u'проведено ранее (в предшествую-щие 12 мес.)', u'5'], CReportBase.AlignRight),
            ( '10%', [u'Отказы', u'', u'6'], CReportBase.AlignRight),
            ( '10%', [u'Выявлено заболеваний', u'', u'7'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 2, 1)
        table.mergeCells(0, 6, 2, 1)
        query = selectData(params)
        if query is None:
            return doc
        reportData, total = self.getReportData(query)
        for row, name in enumerate(self.rowNames):
            reportLine = reportData[row]
            i = table.addRow()
            table.setText(i, 0, name)
            table.setText(i, 1, row+1)
            table.setText(i, 2, reportLine[0])
            table.setText(i, 3, reportLine[1])
            table.setText(i, 4, reportLine[2])
            table.setText(i, 5, reportLine[3])
            table.setText(i, 6, reportLine[4] if row not in (13, 14) else 'X')
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        table.setText(i, 2, total[0])
        table.setText(i, 3, total[1])
        table.setText(i, 4, total[2])
        table.setText(i, 5, total[3])
        table.setText(i, 6, total[4])
        return doc
