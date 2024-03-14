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
from PyQt4.QtCore import QDate, QTime, QDateTime

from Reports.Form36PL_2100_2190 import CForm36PL
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle
from library.MapCodeWithExSubClass import createMapCodeToRowIdx, normalizeMKB
from library.Utils import forceString, forceInt, forceBool

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психозы и (или) состояния слабоумия', u'F00 - F05, F06 (часть), F09, F20 - F25, F28, F29, F84.0 - 4, F30 - F39 (часть)', u'F00-F05; F06.00-F06.09; F06.10-F06.19; F06.20-F06.29; F06.30-F06.34; F06.81; F06.91; F09; F20; F21; F25; F3x.x4; F23; F24; F22; F28; F29; F84.0-F84.4; F99.1; F30.2; F31.2; F31.5; F32.2; F33.3', u'1'),
    (1, u'из них: шизофрения, шизоактивные психозы, шизотипическое расстройство, аффективные психозы с неконгруентным аффекту бредом', u'F20, F21, F25, F3x.x4', u'F20; F21; F25; F3x.x4', u'2'),
    (0, u'Психические расстройства непсихотического характера', u'F06 (часть), F07, F30 - F39 (часть), F40 - F69, F80 - F83, F84.5, F90 - F98', u'F06.350-F06.359; F06.360-F06.369; F06.370-F06.379; F06.40-F06.49; F06.50-F06.59; F06.60-F06.69; F06.70-F06.79; F06.82; F06.92; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.3; F31.4; F31.6-F31.9; F32.0; F32.1; F32.2; F32.8; F32.9; F33.0; F33.1; F33.2; F33.4; F33.8; F33.9; F34.0; F34.1; F34.8; F34.9; F38; F39; F40-F48; F50-F59; F80-F83; F84.5; F90 - F98; F99.2-F99.9; F60-F69', u'3'),
    (0, u'Умственная отсталость', u'F70 - F79', u'F70 - F79', u'4'),
    (0, u'Психические расстройства - всего', u'F00 - F09, F20 - F99', u'F00 - F09; F20 - F99', u'5'),
    (0, u'Кроме того: больные с заболеваниями, связанными с употреблением психоактивных веществ', u'F10 - F19', u'F10 - F19', u'6'),
    (1, u'из них больные алкогольными психозами и слабоумием', u'F10.4 - F10.7', u'F10.4 - F10.7', u'7'),
    (0, u'Из стр. 5 и 6: число больных, заболевших психическим расстройством после совершения преступления (п. б ч. 1 ст. 97 УК РФ)', u'F00 - F99', u'', u'8'),
    (0, u'Больные (из стр. 5 и 6), находящиеся на ПЛ в течение отчетного года в психиатрическом стационаре общего типа', u'', u'', u'9'),
    (1, u'из них число больных, заболевших психическим расстройством после совершения преступления (п. б ч. 1 ст. 97 УК РФ)', u'', u'', u'10'),
    (0, u'Больные (из стр. 5 и 6), находящиеся на ПЛ в течение отчетного года в психиатрическом стационаре специализированного типа', u'', u'', u'11'),
    (1, u'из них число больных, заболевших психическим расстройством после совершения преступления (п. б ч. 1 ст. 97 УК РФ)', u'', u'', u'12')
]


def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    if not endDate:
        endDate = QDate.currentDate()
    if endDate:
        endTime = params.get('endTime', QTime(9, 0, 0, 0))
        begTime = params.get('begTime', QTime(0, 0, 0, 0))
        endDateTime = QDateTime(endDate, endTime)
        if not begDate:
            begTime = begTime if begTime else endTime
            begDateTime = QDateTime(endDate.addDays(-1), begTime)
        else:
            begTime = begTime if begTime else endTime
            begDateTime = QDateTime(begDate, begTime)

    orgStructureIdList = params.get('orgStructureIdList', None)
    if orgStructureIdList:
        condOrgstruct = 'AND ' + db.table('Person').alias('p')['orgStructure_id'].inlist(orgStructureIdList)
    else:
        condOrgstruct = ''

    stmt = u"""
SELECT 
    IF(d.exSubclassMKB IS NOT NULL, CONCAT(d.MKB, d.exSubclassMKB), d.MKB) AS MKB,
    age(c.birthDate, e.setDate) AS age,
    age(c.birthDate, {endDate}) AS ageForEndDate,
    IF(e.setDate between {begDate} AND {endDate}, 1, 0) as isReceived,
      NOT EXISTS(SELECT NULL 
      FROM Event e2
      left JOIN EventType et2 ON e2.eventType_id = et2.id
      LEFT JOIN rbMedicalAidType mat2 ON mat2.id = et2.medicalAidType_id
      WHERE e2.client_id = c.id AND e2.setDate < e.setDate AND e2.deleted = 0 AND mat2.regionalCode IN ('11', '12')) AS isFirstInLife,
    EXISTS(SELECT NULL 
      FROM Event e2
      left JOIN EventType et2 ON e2.eventType_id = et2.id
      LEFT JOIN rbMedicalAidType mat2 ON mat2.id = et2.medicalAidType_id
      WHERE e2.client_id = c.id AND e2.execDate <= e.setDate AND e2.deleted = 0 AND et.name ='Активное диспансерное наблюдение') AS beforeAPNL,
    EXISTS(SELECT NULL 
      FROM Event e2
      left JOIN EventType et2 ON e2.eventType_id = et2.id
      LEFT JOIN rbMedicalAidType mat2 ON mat2.id = et2.medicalAidType_id
      WHERE e2.client_id = c.id AND e2.setDate >= e.execDate AND e2.deleted = 0 AND et.name ='Активное диспансерное наблюдение') AS afterAPNL,
    EXISTS(SELECT NULL 
      FROM Event e2
      left JOIN EventType et2 ON e2.eventType_id = et2.id
      LEFT JOIN rbMedicalAidType mat2 ON mat2.id = et2.medicalAidType_id
      WHERE e2.client_id = c.id AND e2.setDate >= e.execDate AND e2.deleted = 0 AND mat2.regionalCode NOT IN ('11', '12')) AS afterOther,
    IF(e.execDate is not NULL, 1, 0) as isLeaved,
    IF(e.execDate is Not null, WorkDays(e.setDate, e.execDate, et.weekProfileCode, mat.regionalCode), 0) AS bedDays
  FROM Event e
  LEFT JOIN Person p ON p.id = e.execPerson_id
  left JOIN Client c on c.id = e.client_id
  left JOIN EventType et ON e.eventType_id = et.id
  LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id
  left JOIN rbEventTypePurpose etp ON et.purpose_id = etp.id
  LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = e.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code in ('1', '2', '7')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
  WHERE e.deleted = 0
  AND c.deleted = 0
  AND d.deleted = 0
  AND mat.regionalCode IN ('11', '12')
  AND et.code NOT IN ('hospDir','egpuDisp','plng', 'anonim')
  AND et.context NOT LIKE '%relatedAction%' AND et.context NOT LIKE '%inspection%'
  AND et.form NOT IN ('000', '027', '106', '110')
  AND etp.code <> 0
  AND (e.setDate BETWEEN {begDate} AND {endDate} OR e.execDate between {begDate} AND {endDate})
  AND (c.deathDate IS NULL OR c.deathDate BETWEEN {begDate} AND {endDate})
  AND d.MKB LIKE 'F%' AND mod_id is NULL
  AND EXISTS(SELECT NULL
      FROM Action a
      LEFT JOIN ActionType at ON at.id = a.actionType_id
      LEFT JOIN ActionPropertyType apt ON apt.actionType_id = at.id AND apt.deleted = 0 AND apt.name = 'Доставлен по'
      left JOIN ActionProperty ap ON ap.type_id = apt.id AND ap.action_id = a.id AND ap.deleted = 0
      LEFT JOIN ActionProperty_String aps ON ap.id = aps.id
      WHERE a.event_id = e.id
      AND a.deleted = 0
      AND a.actionType_id 
      AND at.flatCode = 'received'
      AND at.deleted = 0
      AND aps.value LIKE 'принудительно')
  {condOrgstruct}""".format(begDate=db.formatDate(begDateTime),
            endDate=db.formatDate(endDateTime),
            condOrgstruct=condOrgstruct)

    return db.query(stmt)


class CForm36PL_2200_2240(CForm36PL):
    def __init__(self, parent):
        CForm36PL.__init__(self, parent)
        self.setTitle(u'Форма №36-ПЛ 2200-2240')


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 12
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            ageForEndDate = forceInt(record.value('ageForEndDate'))
            bedDays = forceInt(record.value('bedDays'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isReceived = forceBool(record.value('isReceived'))
            isFirstInLife = forceBool(record.value('isFirstInLife'))
            beforeAPNL = forceBool(record.value('beforeAPNL'))
            isLeaved = forceBool(record.value('isLeaved'))
            afterAPNL = forceBool(record.value('afterAPNL'))
            afterOther = forceBool(record.value('afterOther'))
            cols = []
            if isReceived:
                cols.append(0)
                if clientAge >= 0 and clientAge < 18:
                    cols.append(1)
                if isFirstInLife:
                    cols.append(2)
                    if beforeAPNL:
                        cols.append(5)
            if isLeaved:
                cols.append(6)
                if afterOther:
                    cols.append(8)
                    if afterAPNL:
                        cols.append(9)
            else:
                cols.append(10)
                if ageForEndDate >= 0 and ageForEndDate < 18:
                    cols.append(11)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += 1
                if isLeaved:
                    reportLine[7] += bedDays

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Состав больных, находящихся на принудительном лечении (ПЛ) в психиатрических стационарах')
        cursor.insertBlock()
        splitTitle(cursor, u'(2200)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('15%', [u'Наименование болезней', u'', u'1'], CReportBase.AlignLeft),
            ('7%', [u'Код по МКБ-10', u'', u'2'], CReportBase.AlignCenter),
            ('3%', [u'N строки', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'больных в отчетном году на ПЛ', u'всего', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'5'], CReportBase.AlignRight),
            ('6%', [u'', u'впервые в жизни в ПБ (из гр. 4)', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'впервые по данному УД', u'7'], CReportBase.AlignRight),
            ('6%', [u'', u'в связи с изменением вида ПЛ по данному УД', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'из них после АПНЛ', u'9'], CReportBase.AlignRight),
            ('6%', [u'Выбыло больных', u'', u'10'], CReportBase.AlignRight),
            ('10%', [u'Ими проведено койко-дней в данном стационаре', u'', u'11'], CReportBase.AlignRight),
            ('6%', [u'Из числа выбывших (гр. 10) выбыло:', u'в связи с изменением вида ПЛ', u'12'], CReportBase.AlignRight),
            ('6%', [u'', u'в том числе переводом на АПНЛ', u'13'], CReportBase.AlignRight),
            ('6%', [u'Состоит на конец года', u'всего', u'14'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'15'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 6)
        table.mergeCells(0, 9, 2, 1)
        table.mergeCells(0, 10, 2, 1)
        table.mergeCells(0, 11, 1, 2)
        table.mergeCells(0, 13, 1, 2)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[2])
            table.setText(i, 2, rowDescr[4])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # 2210
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2210)', u'')
        tableColumns = [
            ('10%', [u'Из числа больных, поступивших на стационарное принудительное лечение (ПЛ) (сумма строк 5 и 6 графа 4 таблицы 2200):', u'ранее находились на принудительном лечении', u'', u'1'], CReportBase.AlignCenter),
            ('10%', [u'', u'из них последнее ООД совершили  после прекращения предыдущего ПЛ', u'в течение до 1 года', u'2'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'через 1 - 2 года', u'3'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'через 2 - 3 года', u'4'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'через 3 - 5 лет', u'5'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'через 5 лет и более', u'6'], CReportBase.AlignCenter),
            ('10%', [u'', u'при совершения ООД (гр. 1) находились под диспансерным наблюдением', u'', u'7'],  CReportBase.AlignCenter),
            ('10%', [u'', u'поступило впервые в данном году', u'', u'8'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 8)
        table.mergeCells(1, 0, 2, 1)
        table.mergeCells(1, 1, 1, 5)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 7, 2, 1)
        i = table.addRow()
        rowSize = 8
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        # 2220
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2220)', u'')
        tableColumns = [('10%', [u'Из общего числа выбывших (сумма строк 5 и 6 графа 10 таблицы 2200):', u'умерли', u'всего', u'1'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'из них от несчастных случаев', u'2'], CReportBase.AlignCenter),
            ('10%', [u'', u'переведено в другие психиатрические стационары (сумма гр. 4 - 7)', u'', u'3'], CReportBase.AlignCenter),
            ('10%', [u'', u'из них в связи с изменением вида ПЛ (сумма стр. 5 и 6 гр. 12 таблицы 2200)', u'в стационары общего типа', u'4'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'в стационары специализированного типа', u'5'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'в стационары специализированного типа с интенсивным наблюдением', u'6'], CReportBase.AlignCenter),
            ('10%', [u'', u'кроме того из гр. 3 переведено в другие психиатрические стационары без изменения вида ПЛ', u'', u'7'], CReportBase.AlignCenter),
            ('10%', [u'', u'выбыло в связи с прекращением принудительного лечения', u'', u'8'], CReportBase.AlignCenter),
            ('10%', [u'', u'число дней, проведенное ими на ПЛ от его начала до прекращения (включая АПНЛ)', u'', u'9'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 9)
        table.mergeCells(1, 0, 1, 2)
        table.mergeCells(1, 2, 2, 1)
        table.mergeCells(1, 3, 1, 3)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 7, 2, 1)
        table.mergeCells(1, 8, 2, 1)
        i = table.addRow()
        rowSize = 9
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        # 2230
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2230)', u'')
        tableColumns = [
            ('10%', [u'Из общего числа больных, находящихся в стационаре на конец года (сумма строк 5 и 6 графа 14 таблицы 2200):', u'время их нахождения на всех видах ПЛ (АПНЛ)', u'до 1 года', u'1'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'от 1 до 2 лет', u'2'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'от 2 до 5 лет', u'3'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'от 5 до 10 лет', u'4'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'больше 10 лет', u'5'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 5)
        table.mergeCells(1, 0, 1, 5)
        i = table.addRow()
        rowSize = 5
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        # 2240
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2240)', u'')
        tableColumns = [
            ('10%', [u'Число побегов за год', u'', u'', u'1'], CReportBase.AlignCenter),
            ('10%', [u'Находится в побеге на конец года', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Из них находится в побеге более года', u'', u'', u'3'], CReportBase.AlignCenter),
            ('10%', [u'Число нападений больных', u'на персонал', u'всего', u'4'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'из них повлекшее смертельный исход или тяжкое телесное повреждение', u'5'], CReportBase.AlignCenter),
            ('10%', [u'', u'на больных', u'всего', u'6'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'из них повлекшее смертельный исход или тяжкое телесное повреждение', u'7'], CReportBase.AlignCenter),
            ('10%', [u'Число суицидальных попыток', u'', u'', u'8'], CReportBase.AlignCenter),
            ('10%', [u'Из них завершенных', u'', u'', u'9'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(1, 3, 1, 2)
        table.mergeCells(1, 5, 1, 2)
        table.mergeCells(0, 7, 3, 1)
        table.mergeCells(0, 8, 3, 1)
        i = table.addRow()
        rowSize = 9
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        return doc