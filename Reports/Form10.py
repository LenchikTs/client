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

from Orgs.Utils import getOrgStructureFullName
from Reports.Form11 import CForm11SetupDialog
from Reports.StationaryF30_KK import splitTitle
from Reports.Utils import dateRangeAsStr
from library.MapCodeWithExSubClass import createMapCodeToRowIdx, normalizeMKB
from library.Utils import forceBool, forceInt, forceString

from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

# отступ | наименование | диагнозы титул | диагнозы | № строки

MainRows = [
    (0, u'Психические расстройства - всего', u'F00-F09, F20-F99', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09; F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34; F23; F24; F22; F28; F29; F80.31; F84.0-F84.4; F99.1; F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39; F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8; F40-F48; F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9; F60-F69; F70-F79', u'1'),
    (0, u'Психозы и состояния слабоумия (сумма строк 3, 7-11, 13)', u'', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09; F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34; F23; F24; F22; F28; F29; F80.31; F84.0-F84.4; F99.1; F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39', u'2'),
    (1, u'в том числе: органические психозы и (или) слабоумие', u'F00-F05, F06(часть), F09', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09', u'3'),
    (2, u'из них: сосудистая деменция', u'F01', u'F01', u'4'),
    (2, u'другие формы старческого слабоумия', u'F00, F02.0, F02.2-F02.3, F03', u'F00; F02.0; F02.2-F02.3; F03', u'5'),
    (2, u'психозы и (или) слабоумие вследствие эпилепсии', u'F02.8x2, F04.2, F05.x2, F06(часть)', u'F02.8x2; F04.2; F05.x2; F06.02; F06.12; F06.22; F06.302; F06.312; F06.322; F06.332; F06.812; F06.912', u'6'),
    (1, u'шизофрения', u'F20', u'F20', u'7'),
    (1, u'шизотипические расстройства', u'F21', u'F21', u'8'),
    (1, u'шизоаффективные психозы, аффективные психозы с неконгруентным аффекту бредом', u'F25, F3x.x4', u'F25; F30.24; F31.24; F31.54; F32.34; F33.34', u'9'),
    (1, u'острые и преходящие неорганические психозы', u'F23, F24', u'F23-F24', u'10'),
    (1, u'хронические неорганические психозы, детские психозы, неуточненные психотические расстройства', u'F22, F28, F29, F84.0-F84.4, F99.1', u'F22; F28; F29; F80.31; F84.0-F84.4; F99.1', u'11'),
    (2, u'из них: детский аутизм, атипичный аутизм', u'F84.0, F84.1', u'F84.0; F84.1', u'12'),
    (1, u'аффективные психозы', u'F30-F39(часть)', u'F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39', u'13'),
    (2, u'из них: биполярные расстройства', u'F31.23, F31.28, F31.53, F31.58', u'F31.23; F31.28; F31.53; F31.58', u'14'),
    (0, u'Психические расстройства непсихотического характера (сумма строк 16, 18, 20, 21, 23)', u'', u'F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8; F40-F48; F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9; F60-F69', u'15'),
    (1, u'в том числе: органические непсихотические расстройства', u'F06(часть), F07', u'F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07', u'16'),
    (2, u'из них обусловленные эпилепсией', u'F06(часть), F07.x2', u'F06.342; F06.352; F06.362; F06.372; F06.42; F06.52; F06.62; F06.72; F06.822; F06.922; F06.992; F07.02; F07.82; F07.92', u'17'),
    (1, u'аффективные непсихотические расстройства', u'F30-F39(часть)', u'F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8', u'18'),
    (2, u'из них биполярные расстройства', u'F31.0, F31.1, F31.3, F31.4, F31.6-F31.9', u'F31.0; F31.1; F31.3; F31.4; F31.6-F31.9', u'19'),
    (1, u'невротические, связанные со стрессом и соматоформные расстройства', u'F40-F48', u'F40-F48', u'20'),
    (1, u'другие непсихотические расстройства, поведенческие расстройства детского и подросткового возраста, неуточненные непсихотические расстройства', u'F50-F59, F80-F83, F84.5, F90 - F98, F99.2-F99.9', u'F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9', u'21'),
    (2, u'из них синдром Аспергера', u'F84.5', u'F84.5', u'22'),
    (1, u'расстройства зрелой личности и поведения у взрослых', u'F60-F69', u'F60-F69', u'23'),
    (0, u'Умственная отсталость - всего', u'F70, F71-F79', u'F70-F79', u'24'),
    (1, u'из нее легкая умственная отсталость', u'F70', u'F70', u'25'),
    (0, u'Из общего числа(стр. 1): психические расстройства (всего), за исключением расстройств, классифицированных в других рубриках МКБ-10 (код со знаком *)', u'F01,F03-F09,F20-F99', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09; F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34; F23; F24; F22; F28; F29; F80.31; F84.0-F84.4; F99.1; F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39; F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8; F40-F48; F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9; F60-F69; F70-F79', u'26'),
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

    addressType = params.get('addressType', 0)
    addressFunc = 'getClientLocAddressId' if addressType == 1 else 'getClientRegAddressId'
    orgStructureIdList = params.get('orgStructureIdList', None)
    if orgStructureIdList:
        condOrgstruct = 'AND ' + db.table('Person').alias('p')['orgStructure_id'].inlist(orgStructureIdList)
    else:
        condOrgstruct = ''

    typeDN = params.get('typeDN', -1)
    if typeDN:
        stmt = u"""SELECT 
  IF(cck.exSubclassMKB IS NOT NULL, CONCAT(cck.MKB, cck.exSubclassMKB), cck.MKB) AS MKB,
  c.sex,
  age(c.birthDate, IF(cck.begDate BETWEEN {begDate} AND {endDate}, cck.begDate, {endDate})) AS age,
  IFNULL(isAddressVillager((SELECT address_id   FROM ClientAddress  WHERE id = {addressFunc}(c.id))), 0) as isVillager,
  IF(cck.begDate BETWEEN {begDate} AND {endDate} AND c.begDate BETWEEN {begDate} AND {endDate}, 1, 0) isFirstInLife,
  IF(ck.code = 'Д-наблюдение', 1, 0)  AS DN,
  IF(ck.code = 'ПДЛР', 1, 0)  AS PDLR,
  IF(ck.code = 'Д-наблюдение' AND IFNULL(cck.endDate, {endDate} + INTERVAL 1 day) >= {endDate}, 1, 0)  AS DNforEndDate,
  IF(ck.code = 'ПДЛР' AND IFNULL(cck.endDate, {endDate} + INTERVAL 1 day) >= {endDate}, 1, 0)  AS PDLRforEndDate,m.Prim
FROM Client c
LEFT JOIN ClientContingentKind cck ON cck.client_id = c.id
LEFT JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
LEFT JOIN MKB m ON m.DiagID=cck.MKB
WHERE c.deleted = 0 
AND cck.deleted = 0
AND ck.code IN ('Д-наблюдение', 'ПДЛР')
AND (cck.endDate BETWEEN {begDate} AND {endDate} OR cck.endDate IS NULL)
AND cck.MKB LIKE 'F%' AND cck.MKB NOT LIKE 'F1%' """.format(begDate=db.formatDate(begDateTime),
                endDate=db.formatDate(endDateTime),
                addressFunc=addressFunc)
    else:
        stmt = u"""
    SELECT t.* 
      FROM (SELECT e.id, 
        IF(d.exSubclassMKB IS NOT NULL, CONCAT(d.MKB, d.exSubclassMKB), d.MKB) AS MKB,
        e.client_id, 
        e.setDate,
        c.sex,
        age(c.birthDate, e.setDate) AS age,
        IFNULL(isAddressVillager((SELECT address_id   FROM ClientAddress  WHERE id = {addressFunc}(c.id))), 0) as isVillager,
        IF(c.begDate BETWEEN {begDate} AND {endDate}, 1, 0) isFirstInLife,
        EXISTS (SELECT NULL FROM ClientContingentKind cck
          left JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
          WHERE cck.client_id = c.id AND ck.code = 'Д-наблюдение' AND cck.deleted = 0
          AND cck.begDate BETWEEN {begDate} AND {endDate}
         ) AS DN,
        EXISTS (SELECT NULL FROM ClientContingentKind cck
          left JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
          WHERE cck.client_id = c.id AND ck.code = 'ПДЛР' AND cck.deleted = 0
          AND cck.begDate BETWEEN {begDate} AND {endDate}
         ) AS PDLR,
        EXISTS (SELECT NULL FROM ClientContingentKind cck
          left JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
          WHERE cck.client_id = c.id AND ck.code = 'Д-наблюдение' AND cck.deleted = 0
          AND cck.begDate <= {endDate} AND IFNULL(cck.endDate, {endDate} + INTERVAL 1 day) >= {endDate}
         ) AS DNforEndDate,
        EXISTS (SELECT NULL FROM ClientContingentKind cck
          left JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
          WHERE cck.client_id = c.id AND ck.code = 'ПДЛР' AND cck.deleted = 0
          AND cck.begDate <= {endDate} AND IFNULL(cck.endDate, {endDate} + INTERVAL 1 day) >= {endDate}
         ) AS PDLRforEndDate,mm.Prim
      FROM Event e
      LEFT JOIN Person p ON p.id = e.execPerson_id
      left JOIN Client c on c.id = e.client_id
      left JOIN EventType et ON e.eventType_id = et.id
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
      left join MKB mm on d.MKB = mm.DiagID
      WHERE e.deleted = 0
      AND c.deleted = 0
      AND d.deleted = 0
      AND et.code NOT IN ('hospDir','egpuDisp','plng', 'anonim')
      AND et.context NOT LIKE '%relatedAction%' AND et.context NOT LIKE '%inspection%'
      AND et.form NOT IN ('000', '027', '106', '110')
      AND etp.code <> 0 
      AND e.setDate BETWEEN {begDate} AND {endDate}
      AND d.MKB LIKE 'F%' AND d.MKB NOT LIKE 'F1%' AND mod_id is NULL
      {condOrgstruct}) t
    GROUP BY t.client_id
    ORDER BY t.setDate desc
        """.format(begDate=db.formatDate(begDateTime),
                endDate=db.formatDate(endDateTime),
                addressFunc=addressFunc,
                condOrgstruct=condOrgstruct)

    return db.query(stmt)


class CForm10(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setTypeDNVisible()
        return result


    def dumpParams(self, cursor, params):
        description = []
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        if endDate:
            endTime = params.get('endTime', QTime(9, 0, 0, 0))
            begTime = params.get('begTime', None)
            endDateTime = QDateTime(endDate, endTime)
            if not begDate:
                begTime = begTime if begTime else endTime
                description.append(u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
                if begDateTime.date() or endDateTime.date():
                    description.append(dateRangeAsStr(u'за период', begDateTime, endDateTime))

        orgStructureId = params.get('orgStructureId', None)
        addressType = params.get('addressType', -1)
        typeDN = params.get('typeDN', -1)

        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')

        if addressType >= 0:
            description.append(u'адрес: ' + (u'по проживанию' if addressType else u'по регистрации'))

        if typeDN >= 0:
            description.append(u'диспансерное наблюдение по: ' + (u'контингентам в карте' if typeDN else u'событиям'))

        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CForm10_2000(CForm10):
    def __init__(self, parent):
        CForm10.__init__(self, parent)
        self.setTitle(u'Форма N 10 2000')


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 10
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        # mkbList = []
        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            Prim = forceString(record.value('Prim'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            DNforEndDate = forceBool(record.value('DNforEndDate'))
            PDLRforEndDate = forceBool(record.value('PDLRforEndDate'))
            cols = []
            cols = [0]
            if clientSex == 2:
                cols.append(1)
            if clientAge >= 0 and clientAge < 15:
                cols.append(2)
            elif clientAge >= 15 and clientAge < 18:
                cols.append(3)
            elif clientAge >= 18 and clientAge < 20:
                cols.append(4)
            elif clientAge >= 20 and clientAge < 40:
                cols.append(5)
            elif clientAge >= 40 and clientAge < 60:
                cols.append(6)
            elif clientAge >= 60:
                cols.append(7)
            if DNforEndDate:
                cols.append(8)
            elif PDLRforEndDate:
                cols.append(9)

            cols_ = []
            if Prim != '*':
                cols_ = [0]
                if clientSex == 2:
                    cols_.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols_.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols_.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols_.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols_.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols_.append(6)
                elif clientAge >= 60:
                    cols_.append(7)
                if DNforEndDate:
                    cols_.append(8)
                elif PDLRforEndDate:
                    cols_.append(9)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            # if not rows:
            #     mkbList.append(forceString(record.value('MKB')))
            for row in rows:
                reportLine = reportMainData[row]
                if row == 25:
                    if cols_:
                        for col_ in cols_:
                            reportLine[col_] += 1
                else:
                    for col in cols:
                        reportLine[col] += 1
        # tmp = ','.join(mkbList)
        # now text
        # for mk in mkbList:
        #     print mk + ','
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний психическими расстройствами, зарегистрированных учреждением')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2000)', u'Код по ОКЕИ: человек - 792')

        tableColumns = [
            ('28%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'Код по МКБ-10 (класс V, адаптированный для использования в РФ)', u'', u'', u'2'], CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Зарегистрировано пациентов в течение года', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'из них женщин', u'', u'5'], CReportBase.AlignRight),
            ('6%', [u'', u'из них(из гр. 4):', u'0 - 14 лет', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'15 - 17 лет', u'7'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'18 - 19 лет', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'20 - 39 лет', u'9'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'40 - 59 лет', u'10'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'60 лет и старше', u'11'], CReportBase.AlignRight),
            ('7%', [u'Из общего числа пациентов (гр. 4) наблюдаются и получают консультативно-лечебную помощь по состоянию на конец года', u'', u'диспансерные пациенты', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'консультативные пациенты', u'13'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 8)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 1, 6)
        table.mergeCells(0, 11, 2, 2)

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


        # продолжение
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        query.setForwardOnly(False)
        query.first()
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            Prim = forceString(record.value('Prim'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            DNforEndDate = forceBool(record.value('DNforEndDate'))
            PDLRforEndDate = forceBool(record.value('PDLRforEndDate'))
            isVillager = forceBool(record.value('isVillager'))
            cols = []
            if isVillager:
                cols.append(0)
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)
                if DNforEndDate:
                    cols.append(8)
                elif PDLRforEndDate:
                    cols.append(9)

                if Prim != '*':
                    cols_ = [0]
                    if clientSex == 2:
                        cols_.append(1)
                    if clientAge >= 0 and clientAge < 15:
                        cols_.append(2)
                    elif clientAge >= 15 and clientAge < 18:
                        cols_.append(3)
                    elif clientAge >= 18 and clientAge < 20:
                        cols_.append(4)
                    elif clientAge >= 20 and clientAge < 40:
                        cols_.append(5)
                    elif clientAge >= 40 and clientAge < 60:
                        cols_.append(6)
                    elif clientAge >= 60:
                        cols_.append(7)
                    if DNforEndDate:
                        cols_.append(8)
                    elif PDLRforEndDate:
                        cols_.append(9)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                if row == 25:
                    for col_ in cols_:
                        reportLine[col_] += 1
                else:
                    for col in cols:
                        reportLine[col] += 1

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(2000)', u'Продолжение')
        tableColumns = [
            ('28%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'Код по МКБ-10 (класс V, адаптированный для использования в РФ)', u'', u'', u'2'],
             CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Из общего числа пациентов (гр. 4) - сельских жителей', u'всего', u'', u'14'], CReportBase.AlignRight),
            ('6%', [u'', u'из них женщин', u'', u'15'], CReportBase.AlignRight),
            ('6%', [u'', u'из них(из гр. 4):', u'0 - 14 лет', u'16'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'15 - 17 лет', u'17'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'18 - 19 лет', u'18'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'20 - 39 лет', u'19'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'40 - 59 лет', u'20'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'60 лет и старше', u'21'], CReportBase.AlignRight),
            ('7%', [
                u'Из общего числа пациентов - сельских жителей (гр. 14) наблюдаются и получают консультативно-лечебную помощь по состоянию на конец года',
                u'', u'диспансерные пациенты', u'22'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'консультативные пациенты', u'23'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 8)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 1, 6)
        table.mergeCells(0, 11, 2, 2)

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

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertHtml(u'(2100) Число психических расстройств, классифицированных в других рубриках МКБ - 10, выявленных в отчетном году __________')

        return doc


class CForm10_3000(CForm10):
    def __init__(self, parent):
        CForm10.__init__(self, parent)
        self.setTitle(u'Форма N 10 3000')

    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 10
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isFirstInLife = forceBool(record.value('isFirstInLife'))
            DN = forceBool(record.value('DN'))
            PDLR = forceBool(record.value('PDLR'))
            cols = []
            if isFirstInLife:
                cols.append(0)
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)
                if DN:
                    cols.append(8)
                elif PDLR:
                    cols.append(9)

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

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний психическими расстройствами, зарегистрированных учреждением впервые в жизни')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(3000)', u'Код по ОКЕИ: человек - 792')

        tableColumns = [
            ('28%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'Код по МКБ-10 (класс V, адаптированный для использования в РФ)', u'', u'', u'2'], CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Из общего числа пациентов (гр. 4 т. 2000) - с впервые в жизни установленным диагнозом', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'из них женщин', u'', u'5'], CReportBase.AlignRight),
            ('6%', [u'', u'из них(из гр. 4):', u'0 - 14 лет', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'15 - 17 лет', u'7'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'18 - 19 лет', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'20 - 39 лет', u'9'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'40 - 59 лет', u'10'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'60 лет и старше', u'11'], CReportBase.AlignRight),
            ('7%', [u'Из общего числа пациентов с впервые в жизни установленным диагнозом (гр. 4)', u'', u'диспансерные пациенты', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'консультативные пациенты', u'13'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 8)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 1, 6)
        table.mergeCells(0, 11, 2, 2)

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


        # продолжение
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        query.setForwardOnly(False)
        query.first()
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            DN = forceBool(record.value('DN'))
            PDLR = forceBool(record.value('PDLR'))
            isVillager = forceBool(record.value('isVillager'))
            isFirstInLife = forceBool(record.value('isFirstInLife'))
            cols = []
            if isFirstInLife and isVillager:
                cols.append(0)
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)
                if DN:
                    cols.append(8)
                elif PDLR:
                    cols.append(9)

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

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'(3000)', u'Продолжение')
        tableColumns = [
            ('28%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'Код по МКБ-10 (класс V, адаптированный для использования в РФ)', u'', u'', u'2'],
             CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Из общего числа пациентов (гр. 4) - сельских жителей', u'всего', u'', u'14'], CReportBase.AlignRight),
            ('6%', [u'', u'из них женщин', u'', u'15'], CReportBase.AlignRight),
            ('6%', [u'', u'из них(из гр. 4):', u'0 - 14 лет', u'16'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'15 - 17 лет', u'17'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'18 - 19 лет', u'18'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'20 - 39 лет', u'19'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'40 - 59 лет', u'20'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'60 лет и старше', u'21'], CReportBase.AlignRight),
            ('7%', [u'Из общего числа пациентов - сельских жителей с впервые в жизни установленным диагнозом (гр. 14)', u'', u'диспансерные пациенты', u'22'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'консультативные пациенты', u'23'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 8)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 1, 6)
        table.mergeCells(0, 11, 2, 2)

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

        return doc