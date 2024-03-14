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

from Reports.Form11 import CForm11SetupDialog
from Reports.Form36_2100_2190 import CForm36
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle
from library.MapCodeWithExSubClass import createMapCodeToRowIdx, normalizeMKB
from library.Utils import forceString, forceInt, forceBool

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психические расстройства - всего', u'F00 - F09, F20 - F99', u'F00-F09; F20-F99', u'1'),
    (0, u'Психозы и состояния слабоумия (сумма строк 3, 6 - 10, 12)', u'', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.91; F09; F20; F21; F25; F3x.x4; F23; F24; F22; F28; F29; F84.0-F84.4; F99.1; F30.23; F30.28; F31.23; F31.28; F31.53; F31.58; F32.33; F32.38; F33.33; F33.38; F39', u'2'),
    (1, u'в том числе: органические психозы и (или) слабоумие', u'F00-F05, F06(часть), F09', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.91; F09', u'3'),
    (2, u'из них: сосудистая деменция', u'F01', u'F01', u'4'),
    (2, u'другие формы старческого слабоумия', u'F00, F02.0, F02.2-F02.3, F03', u'F00; F02.0; F02.2-F02.3; F03', u'5'),
    (0, u'шизофрения', u'F20', u'F20', u'6'),
    (0, u'шизотипические расстройства', u'F21', u'F21', u'7'),
    (0, u'шизоаффективные психозы, аффективные психозы с неконгруентным аффекту бредом', u'F25, F3x.x4', u'F25; F3x.x4', u'8'),
    (0, u'острые и преходящие неорганические психозы', u'F23, F24', u'F23; F24', u'9'),
    (0, u'хронические неорганические психозы, детские психозы, неуточненные психотические расстройства', u'F22, F28, F29, F84.0-F84.4, F99.1', u'F22; F28; F29; F84.0-F84.4; F99.1', u'10'),
    (1, u'из них: детский аутизм, атипичный аутизм', u'F84.0, F84.1', u'F84.0; F84.1', u'11'),
    (0, u'аффективные психозы', u'F30-F39(часть)', u'F30.23; F30.28; F31.23; F31.28; F31.53; F31.58; F32.33; F32.38; F33.33; F33.38; F39', u'12'),
    (1, u'из них: биполярные расстройства', u'F31.23, F31.28, F31.53, F31.58', u'F31.23; F31.28; F31.53; F31.58', u'13'),
    (0, u'Непсихотические психические расстройства (сумма строк 15, 16, 18, 19, 21)', u'', u'F06.34-F06.39; F06.4-F06.7; F06.82; F06.92-F06.99; F07; F30.0-F30.1; F30.8-F30.9; F31.0-F31.1; F31.3-F31.4; F31.6-F31.9; F32.0-F32.2; F32.8-F32.9; F33.0-F33.2; F33.4-F33.9; F34-F38; F40-F48; F50-F59; F80.0-F80.2; F80.32-F80.39; F80.4-F80.9;F81-F83; F84.5-F84.9; F85-F98; F99.2; F99.9; F60-F69', u'14'),
    (1, u'в том числе: органические непсихотические расстройства', u'F06(часть), F07', u'F06.34-F06.39; F06.4-F06.7; F06.82; F06.92-F06.99; F07', u'15'),
    (0, u'аффективные непсихотические расстройства', u'F30-F39(часть)', u'F30.0-F30.1; F30.8-F30.9; F31.0-F31.1; F31.3-F31.4; F31.6-F31.9; F32.0-F32.2; F32.8-F32.9; F33.0-F33.2; F33.4-F33.9; F34-F38', u'16'),
    (1, u'из них биполярные расстройства', u'F31.0, F31.1, F31.3, F31.4, F31.6-F31.9', u'F31.0-F31.1; F31.3-F31.4; F31.6-F31.9', u'17'),
    (0, u'невротические, связанные со стрессом и соматоформные расстройства', u'F40-F48', u'F40-F48', u'18'),
    (0, u'другие непсихотические расстройства, поведенческие расстройства детского и подросткового возраста, неуточненные непсихотические расстройства', u'F50-F59, F80-F83, F84.5, F90 - F98, F99.2-F99.9', u'F50-F59; F80.0-F80.2; F80.32-F80.39; F80.4-F80.9;F81-F83; F84.5-F84.9; F85-F98; F99.2; F99.9', u'19'),
    (1, u'из них синдром Аспергера', u'F84.5', u'F84.5', u'20'),
    (0, u'расстройства зрелой личности и поведения у взрослых', u'F60-F69', u'F60-F69', u'21'),
    (0, u'Умственная отсталость - всего', u'F70, F71-F79', u'F70; F71-F79', u'22'),
    (0, u'Кроме того: пациенты с заболеваниями, связанными с употреблением психоактивных веществ', u'F10 - F19', u'F10 - F19', u'23'),
    (1, u'из них: больные алкогольными психозами', u'F10.4 - F10.7', u'F10.4 - F10.7', u'24'),
    (1, u'наркоманиями, токсикоманиями', u'F11 - F19', u'F11 - F16; F18; F19', u'25'),
    (0, u'признаны психически здоровыми и с заболеваниями, не вошедшими в стр. 1 и 22', u'', u'', u'26')
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
    EXISTS(SELECT NULL
      FROM Action a
      LEFT JOIN ActionType at ON at.id = a.actionType_id
      LEFT JOIN ActionPropertyType apt ON apt.actionType_id = at.id AND apt.deleted = 0 AND apt.name = 'Госпитализирован'
      left JOIN ActionProperty ap ON ap.type_id = apt.id AND ap.action_id = a.id AND ap.deleted = 0
      LEFT JOIN ActionProperty_String aps ON ap.id = aps.id
      WHERE a.event_id = e.id
      AND a.deleted = 0
      AND a.actionType_id 
      AND at.flatCode = 'received'
      AND at.deleted = 0
      AND aps.value LIKE 'первично') AS isPrimary,
    EXISTS(SELECT NULL
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
      AND aps.value LIKE '%недобровольно ст.29%') as isForcibly,
    NOT EXISTS(SELECT NULL 
      FROM Event e2
      left JOIN EventType et2 ON e2.eventType_id = et2.id
      LEFT JOIN rbMedicalAidType mat2 ON mat2.id = et2.medicalAidType_id
      WHERE e2.client_id = c.id AND e2.setDate < e.setDate AND e2.deleted = 0 AND mat2.regionalCode IN ('11', '12')) AS isFirstInLife,
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
  {condOrgstruct}
    """.format(begDate=db.formatDate(begDateTime),
            endDate=db.formatDate(endDateTime),
            condOrgstruct=condOrgstruct)

    return db.query(stmt)


class CForm36_2300_2340(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2300-2340')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 11
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            ageForEndDate = forceInt(record.value('ageForEndDate'))
            bedDays = forceInt(record.value('bedDays'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isReceived = forceBool(record.value('isReceived'))
            isPrimary = forceBool(record.value('isPrimary'))
            isFirstInLife = forceBool(record.value('isFirstInLife'))
            isForcibly = forceBool(record.value('isForcibly'))
            isLeaved = forceBool(record.value('isLeaved'))
            cols = []
            if isReceived:
                cols.append(0)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(1)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(2)
                if isPrimary:
                    cols.append(3)
                    if isFirstInLife:
                        cols.append(4)
                if isForcibly:
                    cols.append(5)
            if isLeaved:
                cols.append(6)
            else:
                cols.append(8)
                if ageForEndDate >= 0 and ageForEndDate < 15:
                    cols.append(9)
                elif ageForEndDate >= 15 and ageForEndDate < 18:
                    cols.append(10)

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
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний психическими расстройствами, зарегистрированных учреждением')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2300)', u'Коды по ОКЕИ: человек - 792, койко-день - 9111')

        tableColumns = [
            ('14%', [u'Наименование', u'', u'', u'', u'1'], CReportBase.AlignLeft),
            ('6%', [u'Код по МКБ-10 (класс V, адаптированный для использования в РФ)', u'', u'', u'', u'2'], CReportBase.AlignCenter),
            ('3%', [u'N строки', u'', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'В отчетном году', u'поступило пациентов', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'из них детей:', u'0 - 14 лет вкл.', u'5'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'', u'15 - 17 лет', u'6'], CReportBase.AlignRight),
            ('7%', [u'', u'из них поступило (из гр. 4)', u'впервые в данном году', u'', u'7'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'из них впервые в жизни', u'', u'8'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'недобровольно соответственно ст. 29', u'', u'9'], CReportBase.AlignRight),
            ('7%', [u'', u'выбыло пациентов', u'', u'', u'10'], CReportBase.AlignRight),
            ('7%', [u'', u'число койко-дней, проведенных в стационаре выписанными и умершими', u'', u'', u'11'], CReportBase.AlignRight),
            ('7%', [u'Состоит на конец года', u'всего', u'', u'', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'из них детей:', u'0 - 14 лет включительно', u'', u'13'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'15 - 17 лет', u'', u'14'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 4, 1)
        table.mergeCells(0, 3, 1, 8)
        table.mergeCells(1, 3, 1, 3)
        table.mergeCells(2, 3, 2, 1)
        table.mergeCells(2, 4, 1, 2)
        table.mergeCells(1, 6, 1, 3)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(2, 7, 2, 1)
        table.mergeCells(2, 8, 2, 1)
        table.mergeCells(1, 9, 3, 1)
        table.mergeCells(1, 10, 3, 1)
        table.mergeCells(0, 11, 1, 3)
        table.mergeCells(1, 11, 3, 1)
        table.mergeCells(1, 12, 1, 2)
        table.mergeCells(2, 12, 2, 1)
        table.mergeCells(2, 13, 2, 1)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[2])
            table.setText(i, 2, rowDescr[4])
            for col in xrange(rowSize):
                if rowDescr[4] in ['4', '5'] and col in [10, 11]:
                    table.setText(i, 3 + col, 'X')
                else:
                    table.setText(i, 3 + col, reportLine[col])

        # 2301
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'Код по ОКЕИ: человек - 792', u'')
        cursor.insertText(u'(2301) Число поступивших пациентов с психическими расстройствами,\nклассифицированные в других рубриках МКБ-10, 1 ________,\nиз них поступило повторно 2 ______')

        # 2310
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2310)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('17%', [u'Из общего числа поступивших пациентов (стр. 1, 24, 27 гр. 4, т. 2300):', u'переведено из других психиатрических стационаров', u'', u'1'], CReportBase.AlignCenter),
            ('17%', [u'', u'поступило недобровольно', u'по скорой психиатрической помощи', u'2'], CReportBase.AlignCenter),
            ('17%', [u'', u'', u'по направлению специализированного амбулаторно-поликлинической организации', u'3'], CReportBase.AlignCenter),
            ('17%', [u'Число лиц, недобровольно освидетельствованных стационаром (кроме поступивших по скорой психиатрической помощи и освидетельствованных в специализированных амбулаторно-поликлинических организациях)', u'', u'всего', u'4'], CReportBase.AlignCenter),
            ('16%', [u'', u'', u'из них госпитализировано недобровольно по ст. 29', u'5'], CReportBase.AlignCenter),
            ('16%', [u'Число пациентов, в отношении которых получено постановление судьи о недобровольной госпитализации (по ст. 35)', u'', u'', u'6'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 3)
        table.mergeCells(1, 0, 2, 1)
        table.mergeCells(1, 1, 1, 2)
        table.mergeCells(0, 3, 2, 2)
        table.mergeCells(0, 5, 3, 1)
        i = table.addRow()
        rowSize = 6
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        # 2320
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2320)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('10%', [u'Из общего числа выбывших пациентов (стр. 1, 24, 27 гр. 10 т. 2300):', u'получили курс лечения/реабилитации бригадным методом', u'', u'', u'1'], CReportBase.AlignCenter),
            ('5%', [u'', u'переведено в другие стационары', u'всего', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'из них в психиатрические стационары', u'', u'3'], CReportBase.AlignCenter),
            ('10%', [u'', u'переведено в учреждения социального обслуживания (впервые оформленных)', u'для взрослых', u'', u'4'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'для детей', u'', u'5'], CReportBase.AlignCenter),
            ('5%', [u'', u'выбыло детей в возрасте 0 - 14 лет вкл.', u'всего', u'', u'6'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'проведено ими койко-дней', u'', u'7'], CReportBase.AlignCenter),
            ('5%', [u'', u'выбыло детей в возрасте 15 - 17 лет', u'всего', u'', u'8'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'проведено ими койко-дней', u'', u'9'], CReportBase.AlignCenter),
            ('5%', [u'', u'умерли', u'всего', u'', u'10'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'из них', u'от несчастных случаев', u'11'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'', u'от самоубийств', u'12'], CReportBase.AlignCenter),
            ('10%', [u'', u'', u'', u'непосредственно от психического заболевания (коды F00 - F99)', u'13'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 13)
        table.mergeCells(1, 0, 3, 1)
        table.mergeCells(1, 1, 1, 2)
        table.mergeCells(2, 1, 2, 1)
        table.mergeCells(2, 2, 2, 1)
        table.mergeCells(1, 3, 1, 2)
        table.mergeCells(2, 3, 2, 1)
        table.mergeCells(2, 4, 2, 1)
        table.mergeCells(1, 5, 1, 2)
        table.mergeCells(2, 5, 2, 1)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(2, 7, 2, 1)
        table.mergeCells(2, 8, 2, 1)
        table.mergeCells(1, 9, 1, 4)
        table.mergeCells(2, 9, 2, 1)
        table.mergeCells(2, 10, 1, 3)
        i = table.addRow()
        rowSize = 13
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        # 2340
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2340)', u'Коды по ОКЕИ: единица - 642, человек - 792')
        tableColumns = [
            ('17%', [u'Из общего числа состоящих на конец года (стр. 1, 24, 27 гр. 12, т. 2300) число пациентов, находящихся в стационаре больше одного года', u'всего', u'', u'1'], CReportBase.AlignCenter),
            ('17%', [u'', u'из них находящихся на принудительном лечении', u'', u'2'], CReportBase.AlignCenter),
            ('17%', [u'Число случаев и дней нетрудоспособности по закрытым листкам нетрудоспособности', u'всего', u'число случаев', u'3'], CReportBase.AlignCenter),
            ('17%', [u'', u'', u'число дней', u'4'], CReportBase.AlignCenter),
            ('16%', [u'', u'из них у пациентов с заболеваниями, связанными с употреблением ПАВ', u'число случаев (из графы 3)', u'5'], CReportBase.AlignCenter),
            ('16%', [u'', u'', u'число дней (из графы 4)', u'6'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 2)
        table.mergeCells(1, 0, 2, 1)
        table.mergeCells(1, 1, 2, 1)
        table.mergeCells(0, 2, 1, 4)
        table.mergeCells(1, 2, 1, 2)
        table.mergeCells(1, 4, 1, 2)
        i = table.addRow()
        rowSize = 6
        for col in xrange(rowSize):
            table.setText(i, col, 0)

        return doc