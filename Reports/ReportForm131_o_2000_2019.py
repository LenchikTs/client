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
from Reports.ReportForm131_o_2000_2016 import selectData


class CReportForm131_o_2000_2019(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о первом этапе диспансеризации определенных групп взрослого населения (2019)')
        self.mapNumMesVisitCodeToRow = {
                    1:  0,
                    3:  1,
                    2:  2,
                    4:  3,
                    5:  4,
                    6:  5,
                    86: 6,
                    15: 7,
                    97: 8,
                    98: 8,
                    14: 9,
                    19: 10,
                    8:  11,
                    95: 12,
                    11: 13,
                    10: 14,
                    12: 15,
                    87: 16,
                    13: 17,
                    7:  18,
                    17: 19,
                    }

        self.rowNames = [
                     u'Опрос(анкетирование), направленный на выявление хронических неинфекционных заболеваний, факторов риска их развития, потребления наркотических средств и психотропных веществ без назначения врача',
                     u'Антропометрия (измерение роста стоя, массы тела, окружности талии), расчет индекса массы тела',
                     u'Измерение артериального давления',
                     u'Определение уровня общего холестерина в крови',
                     u'Определение уровня глюкозы в крови экспресс-методом',
                     u'Определение относительного суммарного сердечно-сосудистого риска',
                     u'Определение абсолютного суммарного сердечно-сосудистого риска',
                     u'Электрокардиография (в покое)',
                     u'Осмотр фельдшером (акушеркой), включая взятие мазка (соскоба) с поверхности шейки матки (наружного маточного зева) и цервикального канала на цитологическое исследование',
                     u'Флюорография легких',
                     u'Маммография обеих молочных желез',
                     u'Клинический анализ крови',
                     u'Клинический анализ крови развернутый',
                     u'Анализ крови биохимический общетерапевтический',
                     u'Общий анализ мочи',
                     u'Исследование кала на скрытую кровь иммунохимическим методом',
                     u'Ультразвуковое исследование (УЗИ) на предмет исключения новообразований органов брюшной полости, малого таза и аневризмы брюшной аорты',
                     u'Ультразвуковое исследование (УЗИ) в целях исключения аневризмы брюшной аорты',
                     u'Измерение внутриглазного давления',
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
        result = [ [0, 0, 0, 0] for row in self.rowNames
                 ]
        return result


    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0]
        uniqueSet = set()
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            actionMkb = forceString(record.value('actionMkb'))
            propertyDescr1 = forceString(record.value('propertyDescr1'))
            propertyDescr2 = forceString(record.value('propertyDescr2'))
            numMesVisitCode = forceInt(record.value('numMesVisitCode'))
            ageClient = forceInt(record.value('ageClient'))
            actionExecPrev = forceInt(record.value('actionExecPrev'))
            propertyEvaluation = forceInt(record.value('propertyEvaluation'))
            endDate = forceDate(record.value('endDate'))
            status = forceInt(record.value('status'))
            actionExecRefusal = (not endDate) and (status == CActionStatus.refused)
            if numMesVisitCode not in self.mapNumMesVisitCodeToRow:
                continue
            if actionId in uniqueSet:
                continue
            uniqueSet.add(actionId)
            targetRow = self.mapNumMesVisitCodeToRow.get(numMesVisitCode, None)
            if targetRow == 5 and ageClient >= 40:
                targetRow = 6
            if targetRow is not None:
                reportLine = reportData[targetRow]
                if endDate and status != CActionStatus.refused:
                    if endDate and status == CActionStatus.finished and not actionExecPrev:
                        reportLine[0] += 1
                        reportDataTotal[0] += 1
                    if actionExecPrev:
                        reportLine[1] += 1
                        reportDataTotal[1] += 1
                    if targetRow ==5 and propertyDescr1:
                        reportLine[3] += 1
                        reportDataTotal[3] += 1
                    elif targetRow ==6 and propertyDescr2:
                        reportLine[3] += 1
                        reportDataTotal[3] += 1
                    elif targetRow not in [5, 6]:
                        if ((actionMkb and 'A00'<=actionMkb<'U') or propertyEvaluation) and targetRow not in [5, 6]:
                            reportLine[3] += 1
                            reportDataTotal[3] += 1
                if actionExecRefusal:
                    reportLine[2] += 1
                    reportDataTotal[2] += 1
        return reportData, reportDataTotal


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(2000)')
        cursor.insertBlock()
        tableColumns = [
            ( '45%', [u'', u'Осмотр, исследование, иное медицинское мероприятие первого этапа диспансеризации', u'1'], CReportBase.AlignLeft),
            ( '3%',  [u'', u'№ строки', u'2'], CReportBase.AlignRight),
            ( '15%', [u'Медицинское мероприятие', u'проведено', u'3'], CReportBase.AlignRight),
            ( '15%', [u'', u'учтено, выполненных ранее (в предшествующие 12 мес.)', u'4'], CReportBase.AlignRight),
            ( '15%', [u'', u'отказы', u'5'], CReportBase.AlignRight),
            ( '15%', [u'Выявлены патологические отклонения', u'', u'6'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 2, 1)
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
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        table.setText(i, 2, total[0])
        table.setText(i, 3, total[1])
        table.setText(i, 4, total[2])
        table.setText(i, 5, total[3])
        return doc

