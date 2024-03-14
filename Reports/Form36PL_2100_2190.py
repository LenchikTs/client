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
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle
from Reports.Utils import dateRangeAsStr
from library.MapCodeWithExSubClass import createMapCodeToRowIdx, normalizeMKB
from library.Utils import forceDateTime, forceString, forceInt, forceBool, forceDate

MainRows = [
    (0, u'Психозы и (или) состояния слабоумия', u'F00 - F05, F06 (часть), F09, F20 - F25, F28, F29, F84.0 - 4, F30 - F39 (часть)', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09; F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34; F23; F24; F22; F28; F29; F80.31; F84.0-F84.4; F99.1; F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39', u'1'),
    (1, u'из них: шизофрения, шизоактивные психозы, шизотипическое расстройство, аффективные психозы с неконгруентным аффекту бредом', u'F20, F21, F25, F3x.x4', u'F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34', u'2'),
    (0, u'Психические расстройства непсихотического характера', u'F06 (часть), F07, F30 - F39 (часть), F40 - F69, F80 - F83, F84.5, F90 - F98', u'F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8; F40-F48; F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9; F60-F69', u'3'),
    (0, u'Умственная отсталость', u'F70 - F79', u'F70-F79', u'4'),
    (0, u'Итого', u'F00 - F09, F20 - F99', u'F00-F05; F06.0-F06.2; F06.30-F06.33; F06.81; F06.910-F06.918; F09; F20; F21; F25; F30.24; F31.24; F31.54; F32.34; F33.34; F23; F24; F22; F28; F29; F80.31; F84.0-F84.4; F99.1; F30.23-F30.28; F31.23-F31.28; F31.53-F31.58; F32.33-F32.38; F33.33-F33.38; F39; F06.34-F06.39; F06.4-F06.7; F06.82; F06.920-F06.989; F06.99; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.30; F31.31; F31.3; F31.4; F31.6-F31.9; F32.0-F32.2; F32.8; F32.9; F33.0-F33.2; F33.4-F38.8; F40-F48; F50-F59; F80-F83; F84.5; F90-F98; F99.2-F99.9; F60-F69; F70-F79', u'5'),
    (0, u'Кроме того: больные с заболеваниями, связанными с употреблением психоактивных веществ', u'F10 - F19', u'F10-F19', u'6')
]

MainRows2140 = [
    (0, u'Психозы и (или) состояния слабоумия', u'F00 - F05, F06 (часть), F09, F20 - F25, F28, F29, F84.0 - 4, F30 - F39 (часть)', u'F00-F05; F06.00-F06.09; F06.10-F06.19; F06.20-F06.29; F06.30-F06.34; F06.81; F06.91; F09; F20; F21; F25; F3x.x4; F23; F24; F22; F28; F29; F84.0-F84.4; F99.1; F30.2; F31.2; F31.5; F32.2; F33.3', u'1'),
    (1, u'из них: шизофрения, шизоактивные психозы, шизотипическое расстройство, аффективные психозы с неконгруентным аффекту бредом', u'F20, F21, F25, F3x.x4', u'F20; F21; F25; F3x.x4', u'2'),
    (0, u'Психические расстройства непсихотического характера', u'F06 (часть), F07, F30 - F39 (часть), F40 - F69, F80 - F83, F84.5, F90 - F98', u'F06.350-F06.359; F06.360-F06.369; F06.370-F06.379; F06.40-F06.49; F06.50-F06.59; F06.60-F06.69; F06.70-F06.79; F06.82; F06.92; F07; F30.0; F30.1; F30.8; F30.9; F31.0; F31.1; F31.3; F31.4; F31.6-F31.9; F32.0; F32.1; F32.2; F32.8; F32.9; F33.0; F33.1; F33.2; F33.4; F33.8; F33.9; F34.0; F34.1; F34.8; F34.9; F38; F39; F40-F48; F50-F59; F80-F83; F84.5; F90 - F98; F99.2-F99.9; F60-F69', u'3'),
    (0, u'Умственная отсталость', u'F70 - F79', u'F70 - F79', u'4'),
    (0, u'Итого', u'F00 - F09, F20 - F99', u'F00 - F09; F20 - F99', u'5'),
    (0, u'Из стр. 5 и 6: число больных, заболевших психическими расстройствами после совершения преступления (пункт "б" части 1 статьи 97 УК РФ)', u'F00 - F99', '', u'7')
]

def selectGetObserved(params):
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

    stmt = u"""SELECT 
  IF(cck.exSubclassMKB IS NOT NULL, CONCAT(cck.MKB, cck.exSubclassMKB), cck.MKB) AS MKB,
  age(c.birthDate, {endDate}) AS age
FROM Client c
LEFT JOIN ClientContingentKind cck ON cck.client_id = c.id
LEFT JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
inner JOIN ClientActiveDispensary cft ON c.id = cft.client_id
WHERE c.deleted = 0 and cft.deleted = 0
AND cck.deleted = 0
AND ck.code = 'Д-наблюдение'
AND cft.begDate BETWEEN {begDate} AND {endDate}
AND ((cft.begDate >= cck.begDate AND cck.endDate is Null) or (cft.begDate >= cck.begDate and cft.endDate <= cck.endDate))
AND cck.MKB LIKE 'F%' AND cck.MKB NOT LIKE 'F1%';""".format(begDate=db.formatDate(begDateTime),
                                                            endDate=db.formatDate(endDateTime)
                                                            )
    return db.query(stmt)

def selectGetRemovingObserved(params):
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


    stmt = u"""SELECT 
  IF(cck.exSubclassMKB IS NOT NULL, CONCAT(cck.MKB, cck.exSubclassMKB), cck.MKB) AS MKB,
  IF(cft.endReason = 2, 1, 0) removedToRecover,c.id
FROM Client c
LEFT JOIN ClientContingentKind cck ON cck.client_id = c.id
LEFT JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
inner JOIN ClientActiveDispensary cft ON c.id = cft.client_id
WHERE c.deleted = 0
AND cck.deleted = 0
AND ck.code = 'Д-наблюдение'
AND cft.endDate between {begDate} and {endDate}
AND ((cft.endDate >= cck.begDate AND cck.endDate is Null) or (cft.endDate <= cck.endDate))
AND cck.MKB LIKE 'F%' AND cck.MKB NOT LIKE 'F1%';""".format(begDate=db.formatDate(begDateTime),
                                                            endDate=db.formatDate(endDateTime))
    return db.query(stmt)

def selectObserved(params):
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

    stmt = u"""SELECT 
  IF(cck.exSubclassMKB IS NOT NULL, CONCAT(cck.MKB, cck.exSubclassMKB), cck.MKB) AS MKB,
  age(c.birthDate, {endDate}) AS age, 
  IF((SELECT 1 FROM ClientDangerous cd  WHERE c.id = cd.client_id AND cd.deleted=0 limit 1)=1,1,0) AS dangerLive,
  IF((SELECT 1 FROM ClientDangerous cd  WHERE c.id = cd.client_id AND cd.deleted=0 AND cd.date BETWEEN {begDate} AND {endDate} limit 1)=1,1,0) AS dangerYear,
  IF((SELECT 1 FROM ClientActiveDispensary ca  WHERE c.id = ca.client_id AND ca.deleted=0 AND ca.begDate < {begDate} limit 1)=1,0,1) AS notADN
FROM Client c
LEFT JOIN ClientContingentKind cck ON cck.client_id = c.id
LEFT JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
inner JOIN ClientActiveDispensary cft ON c.id = cft.client_id
WHERE c.deleted = 0
AND cck.deleted = 0
AND ck.code = 'Д-наблюдение'
  AND cck.endDate IS NULL
  AND cft.endDate IS NULL
AND cck.MKB LIKE 'F%' AND cck.MKB NOT LIKE 'F1%'  GROUP BY c.id,MKB;""".format(begDate=db.formatDate(begDateTime),
                                                            endDate=db.formatDate(endDateTime)
                )

    return db.query(stmt)


def selectGetForcedObserved(params):
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

    stmt = u"""SELECT 
  IF(cck.exSubclassMKB IS NOT NULL, CONCAT(cck.MKB, cck.exSubclassMKB), cck.MKB) AS MKB,
  age(c.birthDate, {endDate}) AS age,
  cft.dispDate,
  IFNULL(cft.dispEndDate,cft.endDate) AS dispEndDate,
  cft.statEndDate,
  cft.statBegDate,
  c.forcedTreatmentBegDate,
  cft.endReason
FROM Client c
LEFT JOIN ClientContingentKind cck ON cck.client_id = c.id
LEFT JOIN rbContingentKind ck ON cck.contingentKind_id = ck.id
inner JOIN ClientForcedTreatment cft ON c.id = cft.client_id
WHERE c.deleted = 0 and cft.deleted = 0
AND cck.deleted = 0
AND ck.code = 'Д-наблюдение'
AND (cck.endDate >= NOW() OR cck.endDate IS NULL)
AND ((cft.dispDate BETWEEN {begDate} AND {endDate}) or (cft.dispEndDate BETWEEN {begDate} AND {endDate}) or cft.dispEndDate is null)
AND cck.MKB LIKE 'F%' AND cck.MKB NOT LIKE 'F1%';""".format(begDate=db.formatDate(begDateTime),
                                                            endDate=db.formatDate(endDateTime)
                                                            )
    return db.query(stmt)


class CForm36PL(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        result.setOrgStructureVisible(False)
        # result.setTypeDNVisible(True)
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

        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')

        if addressType >= 0:
            description.append(u'адрес: ' + (u'по проживанию' if addressType else u'по регистрации'))

        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

class CForm36PL_2100_2190(CForm36PL):
    def __init__(self, parent):
        CForm36PL.__init__(self, parent)
        self.setTitle(u'Форма №36-ПЛ 2100-2190')


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 9
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        
        query = selectGetObserved(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            #   isFirstInLife = forceBool(record.value('isFirstInLife'))
            cols = [0]
            if clientAge >= 0 and clientAge < 18:
                cols.append(1)

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

        query = selectGetRemovingObserved(params)
        while query.next():
            record = query.record()
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            removedToRecover = forceBool(record.value('removedToRecover'))
            cols = [2]
            if removedToRecover:
                cols.append(3)

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

        query = selectObserved(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            dangerLive = forceInt(record.value('dangerLive'))
            dangerYear = forceInt(record.value('dangerYear'))
            notADN = forceInt(record.value('notADN'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))

            cols = [4]
            if clientAge >= 0 and clientAge < 18:
                cols.append(5)
            if dangerLive:
                cols.append(6)
            if dangerYear:
                cols.append(7)
            if notADN:
                cols.append(8)

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
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Контингенты больных, находящихся под активным диспансерным наблюдением (АДН)')
        splitTitle(cursor, u'(2100)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('28%', [u'Наименование болезней', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'N строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('5%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Взято под АДН в отчетном году', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'', u'5'], CReportBase.AlignRight),
            ('6%', [u'Снято с АДН в отчетном году', u'всего', u'', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'из них в связи со снижением общественной опасности', u'', u'7'], CReportBase.AlignRight),
            ('6%', [u'Состоит под АДН на конец отчетного года', u'всего', u'', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'', u'9'], CReportBase.AlignRight),
            ('6%', [u'', u'совершили ООД (и/или преступление) в течение жизни (из гр. 8)', u'всего', u'10'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'из них совершили ООД в отчетном году', u'11'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'из них до этого не находились под АДН', u'12'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(1, 5, 2, 1)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(0, 7, 1, 5)
        table.mergeCells(1, 7, 2, 1)
        table.mergeCells(1, 8, 2, 1)
        table.mergeCells(1, 9, 1, 3)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # 2110
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'2110) Снято с АДН в отчетном году (сумма строк 5 и  6,  графа  6  таблицы 2100)\nв связи: с переменой места жительства  1. ______, со\nсмертью 2. _______, с отсутствием сведений в течение года 3. ______,\nс другими причинами 4. ______.')

        # 2120
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'(2120) Из числа поставленных под активное диспансерное наблюдение (АДН)\nв отчетном году (сумма строк 5 и 6, графа 4 таблицы 2100):\nсовершили ООД в отчетном году  1. ________, из них не находились на\nдиспансерном наблюдении 2. _______, после назначения ПЛ 3. ________,\nиз них после изменения АПНЛ на ПЛ в стационаре 4. _______.')

        # 2130
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'(2130) Из числа состоящих под активным диспансерным наблюдением (АДН) на\nконец отчетного года (сумма строк 5 и 6, графа 8 таблицы 2100):\nнаходится в психиатрическом стационаре 1. __________, из них на ПЛ\n       2. _________.')

        # 2140
        mapMainRows2140 = createMapCodeToRowIdx([row[3] for row in MainRows2140])
        rowSize = 8
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows2140))]
        year2180 = [0,0,0,0]
        days2160 = [0,0]
        reason = [0,0,0]
        query = selectGetForcedObserved(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            begDate = params.get('begDate', QDate())
            endDate = params.get('endDate', QDate())
            cols = []
            if not endDate:
                endDate = QDate.currentDate()
            dispDate = forceDate(record.value('dispDate'))
            dispEndDate = forceDate(record.value('dispEndDate'))
            forcedTretmentBegDate = forceDate(record.value('forcedTreatmentBegDate'))
            if dispDate >= begDate and dispDate <= endDate:
                cols.append(0)
                if clientAge >= 0 and clientAge < 18:
                    cols.append(1)
                if forcedTretmentBegDate < dispDate:
                    cols.append(2)
            if dispEndDate >= begDate and dispEndDate <= endDate:
                cols.append(3)
                if forceInt(record.value('endReason')): reason[forceInt(record.value('endReason'))-1] += 1
                statEndDate = forceDate(record.value('statEndDate'))
                statBegDate = forceDate(record.value('statBegDate'))
                if statEndDate >= begDate and statEndDate <= endDate:
                    if forcedTretmentBegDate: days2160[0] += forcedTretmentBegDate.daysTo(statEndDate)
                    if dispDate and dispEndDate: days2160[1] += dispDate.daysTo(dispEndDate)
                    cols.append(4)
                if statBegDate >= begDate and statBegDate <= endDate:
                    cols.append(5)
            if dispDate and not dispEndDate:
                yearsBetween = (QDate.fromJulianDay(endDate.toJulianDay() - forcedTretmentBegDate.toJulianDay()).year() - QDate.fromJulianDay(0).year())
                if yearsBetween <= 1: year2180[0]+=1
                elif yearsBetween > 1 and yearsBetween <= 2: year2180[1]+=1
                elif yearsBetween > 2 and yearsBetween <=5: year2180[2]+=1
                else: year2180[3]+=1
                cols.append(6)
                if clientAge >= 0 and clientAge < 18:
                    cols.append(7)  
                    
            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows2140.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows2140.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += 1

        
        
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Контингенты больных, находящихся на амбулаторном принудительном наблюдении и лечении (АПНЛ) у психиатра')
        splitTitle(cursor, u'(2140)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('28%', [u'Наименование болезней', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'N строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('5%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Принято на АПНЛ в отчетном году', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'', u'5'], CReportBase.AlignRight),
            ('6%', [u'', u'после ПЛ в стационаре (из гр. 4)', u'', u'6'], CReportBase.AlignRight),
            ('6%', [u'Прекращено (изменено) АПНЛ в отчетном году', u'всего', u'', u'7'], CReportBase.AlignRight),
            ('6%', [u'', u'из них в связи с', u'окончанием ПЛ', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'изменением вида ПЛ', u'9'], CReportBase.AlignRight),
            ('6%', [u'Находится больных на АПНЛ у психиатра на конец года', u'всего', u'', u'10'], CReportBase.AlignRight),
            ('6%', [u'', u'из них детей до 17 лет включительно', u'', u'11'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 3)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 2, 1)
        table.mergeCells(0, 6, 1, 3)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(0, 9, 1, 2)
        table.mergeCells(1, 9, 2, 1)
        table.mergeCells(1, 10, 2, 1)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows2140):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[2])
            table.setText(i, 2, rowDescr[4])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # 2150
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"""(2150) Из числа прекративших АПНЛ в отчетном году (таблица 2140)
прекратило АПНЛ (сумма строк 5 и 6, графа 7) в связи:
со смертью 1.  {}, с переменой места жительства 2. {}, с
привлечением  к  уголовной ответственности по новому уголовному делу 3. {}.""".format(reason[0],reason[1],reason[2]))

        # 2160
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"""(2160) Число дней, проведенных на ПЛ (от начала до окончания, включая
принудительное лечение в стационаре) больными (сумма строк 5 и 6,
графа 8 таблицы  2140), прекратившими АПНЛ по решению суда:  всего
1. {} д., в том числе дней на АПНЛ 2. {} д.""".format(days2160[0],days2160[1]))

        # 2170
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"""(2170) Из общего числа больных, находящихся на конец года на АПНЛ
(сумма строк 5 и 6, графа 10 таблицы 2140), находится в
психиатрическом стационаре  1. _______, пропало без вести 2. ______,
находится на АПНЛ в соответствии со ст. 22 УК РФ 3. _______.""")

        # 2180
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"""(2180) Из общего числа больных, находящихся на конец года на АПНЛ
(сумма строк 5 и 6, графа 10 таблицы 2140), число больных,
длительность ПЛ которых (включая пребывание в стационаре)
составляет:
до 1 года 1: {} , от 1 до 2 лет 2: {}, от 2 до 5 лет: {}, более 5 лет: {}.""".format(year2180[0],year2180[1],year2180[2],year2180[3]))

        # 2190
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u"""(2190) Из числа находившихся на АПНЛ в течение года (сумма строк 5 и 6,
графы 7 и 10 таблицы 2140), совершили в отчетном году новое ООД
1. __,  из них назначено ПЛ (АПНЛ) по новому уголовному делу 2. ___.""")

        return doc