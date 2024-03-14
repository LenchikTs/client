# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from Reports.Form37 import CForm37
from Reports.Form11 import createMapCodeToRowIdx
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психиатры-наркологи, ведущие амбулаторный прием, в том числе:\n\tвзрослых', u'', u'', u'01'),
    (0, u'\tдетей (0 - 17 лет вкл.)', u'', u'', u'02'),
    (0, u'Психотерапевты', u'', u'', u'03'),
    (0, u'Кроме того: психиатры-наркологи, осуществляющие анонимное лечение', u'', u'', u'04')
]

# наименование | диагнозы | № строки
CompRows2210 = [
    (u'В амбулаторных подразделениях:\nПсихологи', u'', u'01'),
    (u'Специалисты по социальной работе', u'', u'02'),
    (u'Социальные работники', u'', u'03'),
    (u'В стационарных отделениях:\nПсихологи', u'', u'04'),
    (u'Специалисты по социальной работе', u'', u'05'),
    (u'Социальные работники', u'', u'06'),
]

# def selectData(params):
#     db = QtGui.qApp.db
#     begDate = params.get('begDate', QDate())
#     endDate = params.get('endDate', QDate())
#     if not endDate:
#         endDate = QDate.currentDate()
#     if endDate:
#         endTime = params.get('endTime', QTime(9, 0, 0, 0))
#         begTime = params.get('begTime', QTime(0, 0, 0, 0))
#         endDateTime = QDateTime(endDate, endTime)
#         if not begDate:
#             begTime = begTime if begTime else endTime
#             begDateTime = QDateTime(endDate.addDays(-1), begTime)
#         else:
#             begTime = begTime if begTime else endTime
#             begDateTime = QDateTime(begDate, begTime)
#
#     addressType = params.get('addressType', 0)
#     addressFunc = 'getClientLocAddressId' if addressType == 1 else 'getClientRegAddressId'
#     orgStructureIdList = params.get('orgStructureIdList', None)
#     if orgStructureIdList:
#         condOrgstruct = 'AND ' + db.table('Person').alias('p')['orgStructure_id'].inlist(orgStructureIdList)
#     else:
#         condOrgstruct = ''
#
#     stmt = u"""
# SELECT t.*
#   FROM (SELECT e.id,
#     IF(d.exSubclassMKB IS NOT NULL, CONCAT(d.MKB, d.exSubclassMKB), d.MKB) AS MKB,
#     e.client_id,
#     e.setDate,
#     c.sex,
#     age(c.birthDate, e.setDate) AS age,
#     IFNULL(isAddressVillager({addressFunc}(c.id)), 0) as isVillager,
#     IF(d.setDate BETWEEN {begDate} AND {endDate}, 1, 0) isFirstInLife,
#     IF(rbDispanser.code in ('2', '6'), 1, 0) AS getObserved,
#     IF(rbDispanser.code in ('3', '4', '5'), 1, 0) AS removingObserved,
#     IF(rbDispanser.code = '4', 1, 0) AS removingToRecoverObserved,
#     IF(rbDispanser.code in ('2', '6', '1'), 1, 0) AS observed
#   FROM Event e
#   LEFT JOIN Person p ON p.id = e.execPerson_id
#   left JOIN Client c on c.id = e.client_id
#   left JOIN EventType et ON e.eventType_id = et.id
#   left JOIN rbEventTypePurpose etp ON et.purpose_id = etp.id
#   left join Diagnostic on Diagnostic.id = (SELECT d1.id
#       FROM Diagnostic d1
#       INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = d1.diagnosisType_id
#       WHERE d1.event_id = e.id
#       AND d1.deleted = 0
#       AND rbDiagnosisType.code = '1')
#   LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
#   LEFT JOIN Diagnosis d on d.id = Diagnostic.diagnosis_id
#   WHERE e.deleted = 0
#   AND c.deleted = 0
#   AND d.deleted = 0
#   AND et.code NOT IN ('hospDir','egpuDisp','plng', 'anonim')
#   AND et.context NOT LIKE '%relatedAction%' AND et.context NOT LIKE '%inspection%'
#   AND et.form NOT IN ('000', '027', '106', '110')
#   AND etp.code <> 0
#   AND e.setDate BETWEEN {begDate} AND {endDate}
#   AND (c.deathDate IS NULL OR c.deathDate BETWEEN {begDate} AND {endDate})
#   AND d.MKB >= 'F10' and d.MKB < 'F20' and d.MKB not like 'F17%' AND mod_id is NULL
#   {condOrgstruct}) t
# GROUP BY t.client_id
# ORDER BY t.setDate desc
#     """.format(begDate=db.formatDate(begDateTime),
#             endDate=db.formatDate(endDateTime),
#             addressFunc=addressFunc,
#             condOrgstruct=condOrgstruct)
#
#     return db.query(stmt)


class CForm37_2200_2210(CForm37):
    def __init__(self, parent):
        CForm37.__init__(self, parent)
        self.setTitle(u'Форма N 37 таблицы 2200-2210')

    def getSetupDialog(self, parent):
        result = CForm37.getSetupDialog(self, parent)
        result.setAddressTypeVisible(False)
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 7
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        # query = selectData(params)
        # while query.next():
        #     record = query.record()
        #     clientAge = forceInt(record.value('age'))
        #     MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
        #     getObserved = forceBool(record.value('getObserved'))
        #     isFirstInLife = forceBool(record.value('isFirstInLife'))
        #     removingObserved = forceBool(record.value('removingObserved'))
        #     removingToRecoverObserved = forceBool(record.value('removingToRecoverObserved'))
        #     observed = forceBool(record.value('observed'))
        #
        #     cols = []
        #     if getObserved:
        #         cols.append(0)
        #         if isFirstInLife:
        #             cols.append(1)
        #     if removingObserved:
        #         cols.append(2)
        #         if removingToRecoverObserved:
        #             cols.append(3)
        #     if observed:
        #         cols.append(4)
        #
        #     rows = []
        #     for postfix in postfixs:
        #         rows.extend(mapMainRows.get((MKB, postfix), []))
        #         while len(MKB[:-1]) > 4:
        #             MKB = MKB[:-1]
        #             rows.extend(mapMainRows.get((MKB, postfix), []))
        #
        #     for row in rows:
        #         reportLine = reportMainData[row]
        #         for col in cols:
        #             reportLine[col] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'II. Показатели деятельности специалистов амбулаторных наркологических организаций (подразделений)\nДеятельность врачей, осуществляющих амбулаторную помощь пациентам наркологического профиля')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2200)', u'Коды по ОКЕИ: человек - 792, единица - 642, посещение в смену - 545')
        tableColumns = [
            ('20%', [u'Наименование должностей', u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'', u'2'], CReportBase.AlignCenter),
            ('11%', [u'Занято должностей на конец года', u'', u'', u'3'], CReportBase.AlignCenter),
            ('11%', [u'Число посещений к врачам', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('11%', [u'', u'сделано по поводу (из гр. 4):', u'освидетельствования для работы и иных целей', u'5'], CReportBase.AlignRight),
            ('11%', [u'', u'', u'реабилитации (Z50.2, 50.3, 50.8) ', u'6'], CReportBase.AlignRight),
            ('11%', [u'', u'', u'детьми в возрасте 0 - 17 лет включительно', u'7'], CReportBase.AlignRight),
            ('11%', [u'Число посещений  по поводу заболевания (из гр. 4)', u'всего', u'', u'8'], CReportBase.AlignRight),
            ('11%', [u'', u'из них - детьми в возрасте 0 - 17 лет вкл.', u'', u'9'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 1, 3)
        table.mergeCells(0, 7, 1, 2)
        table.mergeCells(1, 7, 2, 1)
        table.mergeCells(1, 8, 2, 1)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setAlignment(Qt.AlignLeft)
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
               table.setText(i, 2 + col, reportLine[col])


        # продолжение
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        rowSize = 4
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        splitTitle(cursor, u'(2200)', u'Продолжение')
        tableColumns = [
            ('17%', [u'Наименование должностей', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'2'], CReportBase.AlignCenter),
            ('20%', [u'Распределение посещений по видам оплаты (из гр. 4):', u'ОМС', u'10'], CReportBase.AlignRight),
            ('20%', [u'', u'бюджет', u'11'], CReportBase.AlignRight),
            ('20%', [u'', u'платные', u'12'], CReportBase.AlignRight),
            ('20%', [u'', u'ДМС', u'13'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 4)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setAlignment(Qt.AlignLeft)
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                if col == 0 and rowDescr[4] == '04':
                    t.setLeftMargin(0)
                    t.setAlignment(Qt.AlignCenter)
                    table.setText(i, 2 + col, 'X', blockFormat=t)
                else:
                    table.setText(i, 2 + col, reportLine[col])

        # 2210
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        # mapMainRows = createMapCodeToRowIdx([row[2] for row in CompRows2210])
        rowSize = 9
        reportMainData = [[0] * rowSize for row in xrange(len(CompRows2210))]
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Деятельность психологов, специалистов по социальной работе, социальных работников')
        cursor.insertBlock()
        splitTitle(cursor, u'(2210)', u'Коды по ОКЕИ: человек - 792, единица - 642')
        tableColumns = [
            ('25%', [u'Наименование должностей', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'2'], CReportBase.AlignCenter),
            ('8%', [u'Занято должностей на конец года', u'', u'3'], CReportBase.AlignRight),
            ('8%', [u'Число пациентов, которым оказывалась помощь в течение отчетного года (вкл. созависимых)', u'', u'4'], CReportBase.AlignRight),
            ('8%', [u'Число посещений (консульта-ций и иных контактов) - всего', u'', u'5'], CReportBase.AlignRight),
            ('8%', [u'Из них по поводу (из гр. 5):', u'психодиагностики', u'6'], CReportBase.AlignRight),
            ('8%', [u'', u'психокоррекционных сеансов (бесед)', u'7'], CReportBase.AlignRight),
            ('8%', [u'', u'из них (из гр. 7) - групповых', u'8'], CReportBase.AlignRight),
            ('8%', [u'', u'трудоустройстваи иным вопросам', u'9'], CReportBase.AlignRight),
            ('8%', [u'', u'созависимости', u'10'], CReportBase.AlignRight),
            ('8%', [u'Число тренингов, проведенных в рамках реализации профилактич. программ среди учащихся и иного населения', u'', u'11'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 2, 1)
        table.mergeCells(0, 4, 2, 1)
        table.mergeCells(0, 5, 1, 5)
        table.mergeCells(0, 10, 2, 1)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(CompRows2210):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 2 + col, reportLine[col])

        return doc