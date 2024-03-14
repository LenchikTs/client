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
from PyQt4.QtCore import QDate, QTime, QDateTime, Qt

from Orgs.Utils import getOrgStructureFullName
from Reports.Form11 import CForm11SetupDialog, createMapCodeToRowIdx, normalizeMKB
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle
from Reports.Utils import dateRangeAsStr
from library.Utils import forceString, forceInt, forceBool

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психотические расстройства, связанные с употреблением алкоголя (алкогольные психозы)', u'F10.03, F10.7, F10.04 - F10.6, F10.73, 75, 81, 91', u'F10.03; F10.07; F10.4 - F10.6; F10.73, 75, 81, 91', u'01'),
    (0, u'Синдром зависимости от алкоголя (алкоголизм)', u'F10.2, 3, F10.70 - 72, 74, 82, 92', u'F10.2, 3; F10.70 - 72, 74, 82, 92', u'02'),
    (1, u'из них со стадиями:\nначальная (I)', u'F10.2x1', u'F10.2x1', u'03'),
    (1, u'средняя (II)', u'F10.2x2', u'F10.2x2', u'04'),
    (1, u'конечная (III)', u'F10.2x3', u'F10.2x3', u'05'),
    (0, u'Синдром зависимости от наркотических веществ (наркомания)', u'F11.2-9 - F19.2-9H', u'F11.2-F11.9;F12.2-F12.9;F13.2H-F13.9H;F14.2-F14.9;F15.2H-F15.9H;F16.2H-F16.9H;F18.2H-F18.9H;F19.2H-F19.9H', u'06'),
    (0, u'Синдром зависимости от ненаркотических ПАВ (токсикомания)', u'F13.2-9T - F16.2-9T; F18.2-9T - F19.2-9T', u'F13.2T-F13.9T;F16.2T-F16.9T;F18.2T-F18.9T;F19.2T-F19.9T', u'07'),
    (0, u'Пагубное (с вредными последствиями) употребление алкоголя', u'F10.1', u'F10.1', u'08'),
    (0, u'Пагубное (с вредными последствиями) употребление наркотических веществ', u'F11.1 - F16.1H\nF18.1H - F19.1H', u'F11.1;F12.1;F13.1H;F14.1;F15.1H;F16.1H;F18.1H;F19.1H;', u'09'),
    (0, u'Пагубное (с вредными последствиями) употребление ненаркотических веществ', u'F13.1T, F15.1T - F16.1T, F18.1T - F19.1T', u'F13.1T;F15.1T;F16.1T;F18.1T;F19.1T', u'10'),
    (0, u'ИТОГО', u'F10 - F19', u'F10-F19', u'11'),
]

# наименование | диагнозы | № строки
CompRows2160 = [
    (u'Синдром зависимости от алкоголя (стр. 01, 02)', u'', u'01'),
    (u'Синдром зависимости от наркотических веществ (стр. 06)', u'', u'02'),
    (u'Синдром зависимости от ненаркотических ПАВ (стр. 07)', u'', u'03'),
    (u'Употребление с вредными последствиями алкоголя, наркотических и ненаркотических ПАВ (стр. 08, 09, 10)', u'', u'04'),
    (u'ИТОГО', u'', u'05'),
]

# наименование | диагнозы | № строки
CompRows2170 = [
    (u'Синдром зависимости от алкоголя (стр. 01, 02)', u'', u'01'),
    (u'Синдром зависимости от наркотических веществ (стр. 06)', u'', u'02'),
    (u'Синдром зависимости от ненаркотических ПАВ (стр. 07)', u'', u'03'),
    (u'ИТОГО', u'', u'04'),
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

    stmt = u"""
SELECT t.* 
  FROM (SELECT e.id, 
    IF(d.exSubclassMKB IS NOT NULL, CONCAT(d.MKB, d.exSubclassMKB), d.MKB) AS MKB,
    e.client_id, 
    e.setDate,
    c.sex,
    age(c.birthDate, e.setDate) AS age,
    IFNULL(isAddressVillager((SELECT address_id   FROM ClientAddress  WHERE id = {addressFunc}(c.id))), 0) as isVillager,
    IF(d.setDate BETWEEN {begDate} AND {endDate}, 1, 0) isFirstInLife,
    IF(rbDispanser.code in ('2', '6'), 1, 0) AS getObserved,
    IF(rbDispanser.code in ('3', '4', '5'), 1, 0) AS removingObserved,
    IF(rbDispanser.code = '4', 1, 0) AS removingToRecoverObserved,
    IF(rbDispanser.code in ('2', '6', '1'), 1, 0) AS observed
  FROM Event e
  LEFT JOIN Person p ON p.id = e.execPerson_id
  left JOIN Client c on c.id = e.client_id
  left JOIN EventType et ON e.eventType_id = et.id
  left JOIN rbEventTypePurpose etp ON et.purpose_id = etp.id
  left join Diagnostic on Diagnostic.id = (SELECT d1.id
      FROM Diagnostic d1
      INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = d1.diagnosisType_id
      WHERE d1.event_id = e.id
      AND d1.deleted = 0
      AND rbDiagnosisType.code = '1')
  LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
  LEFT JOIN Diagnosis d on d.id = Diagnostic.diagnosis_id
  WHERE e.deleted = 0
  AND c.deleted = 0
  AND d.deleted = 0
  AND et.code NOT IN ('hospDir','egpuDisp','plng', 'anonim')
  AND et.context NOT LIKE '%relatedAction%' AND et.context NOT LIKE '%inspection%'
  AND et.form NOT IN ('000', '027', '106', '110')
  AND etp.code <> 0
  AND e.setDate BETWEEN {begDate} AND {endDate}
  AND (c.deathDate IS NULL OR c.deathDate BETWEEN {begDate} AND {endDate})
  AND d.MKB >= 'F10' and d.MKB < 'F20' and d.MKB not like 'F17%' AND mod_id is NULL
  {condOrgstruct}) t
GROUP BY t.client_id
ORDER BY t.setDate desc
    """.format(begDate=db.formatDate(begDateTime),
            endDate=db.formatDate(endDateTime),
            addressFunc=addressFunc,
            condOrgstruct=condOrgstruct)

    return db.query(stmt)


class CForm37(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
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
        forResult = params.get('forResult', -1)

        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')

        if addressType >= 0:
            description.append(u'адрес: ' + (u'по проживанию' if addressType else u'по регистрации'))
        if forResult >= 0:
            description.append(u'по результату: ' + (u'лабораторного анализа' if forResult else u'обследования в карте'))

        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CForm37_2100_2170(CForm37):
    def __init__(self, parent):
        CForm37.__init__(self, parent)
        self.setTitle(u'Форма N 37 таблицы 2100-2170')

    def getSetupDialog(self, parent):
        result = CForm37.getSetupDialog(self, parent)
        result.setAddressTypeVisible(False)
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 8
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            getObserved = forceBool(record.value('getObserved'))
            isFirstInLife = forceBool(record.value('isFirstInLife'))
            removingObserved = forceBool(record.value('removingObserved'))
            removingToRecoverObserved = forceBool(record.value('removingToRecoverObserved'))
            observed = forceBool(record.value('observed'))

            cols = []
            if getObserved:
                cols.append(0)
                if isFirstInLife:
                    cols.append(1)
            if removingObserved:
                cols.append(2)
                if removingToRecoverObserved:
                    cols.append(3)
            if observed:
                cols.append(4)

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
        cursor.insertText(u'I. Контингенты пациентов, находящихся под наблюдением психиатра-нарколога')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2100)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('32%', [u'Наименование болезней', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'Взято под наблюдение в течение года:', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('7%', [u'', u'из них: впервые в жизни', u'', u'5'], CReportBase.AlignRight),
            ('7%', [u'Снято с наблюдения в отчетном году', u'всего', u'', u'6'], CReportBase.AlignRight),
            ('7%', [u'', u'из них: в связи с выздоровлением (длительным воздержанием)', u'', u'7'], CReportBase.AlignRight),
            ('7%', [u'Состоит под наблюдением на конец отчетного года', u'всего', u'', u'8'], CReportBase.AlignRight),
            ('7%', [u'', u'из них: инвалидов', u'', u'9'], CReportBase.AlignRight),
            ('7%', [u'', u'из гр. 9:', u'детей 0 - 14 лет', u'10'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'детей 15 - 17 лет', u'11'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 3, 1)  # Код МКБ
        table.mergeCells(0, 3, 1, 2)  # Взято под наблюдение
        table.mergeCells(1, 3, 2, 1)  # Всего
        table.mergeCells(1, 4, 2, 1)  # из них
        table.mergeCells(0, 5, 1, 2)  # Снято с наблюдения
        table.mergeCells(1, 5, 2, 1)  # Всего
        table.mergeCells(1, 6, 2, 1)  # из них
        table.mergeCells(0, 7, 1, 4)  # Состоит под наблюдением
        table.mergeCells(1, 7, 2, 1)  # Всего
        table.mergeCells(1, 8, 2, 1)  # из них
        table.mergeCells(1, 9, 1, 2)  # 'из гр. 9


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
                if col == 5 and rowDescr[4] in ['08', '09', '10', '11']:
                    t.setLeftMargin(0)
                    t.setAlignment(Qt.AlignCenter)
                    table.setText(i, 3 + col, 'X', blockFormat=t)
                else:
                    table.setText(i, 3 + col, reportLine[col])

        # 2101
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Сведения о пациентах, обратившихся по поводу никотиновой зависимости, употребления табака или табакокурения (F17):')
        splitTitle(cursor, u'(2101)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('20%', [u'Число обратившихся лиц - всего', u'', u'1'], CReportBase.AlignRight),
            ('20%', [u'в том числе в отчетном году (из гр. 1):', u'закончили лечение', u'2'], CReportBase.AlignRight),
            ('20%', [u'', u'из них (из гр. 2) - находятся в ремиссии', u'3'], CReportBase.AlignRight),
            ('20%', [u'', u'отказались от лечения или прервали его', u'4'], CReportBase.AlignRight),
            ('20%', [u'', u'продолжили лечение на конец года', u'5'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 1, 4)
        table.addRow()

        # 2102
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число пациентов, снятых с наблюдения в связи со смертью (из гр. 6 табл. 2100):')
        splitTitle(cursor, u'(2102)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('12.5%', [u'психотические расстройства, связанные с употреблением алкоголя (из ст. 1)', u'', u'1'], CReportBase.AlignRight),
            ('12.5%', [u'синдром зависимости от алкоголя (алкоголизм) (из стр. 2)', u'', u'2'], CReportBase.AlignRight),
            ('12.5%', [u'в том числе со стадией:', u'начальная (из стр. 3)', u'3'], CReportBase.AlignRight),
            ('12.5%', [u'', u'средняя (из стр. 4)', u'4'], CReportBase.AlignRight),
            ('12.5%', [u'', u'конечная(из стр. 5)', u'5'], CReportBase.AlignRight),
            ('12.5%', [u'синдром зависимости от наркотических веществ (наркомания) (из стр. 6)', u'', u'6'], CReportBase.AlignRight),
            ('12.5%', [u'синдром зависимости от ненаркотических ПАВ (токсикомания) (из стр. 7)', u'', u'7'], CReportBase.AlignRight),
            ('12.5%', [u'Итого', u'', u'8'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 2, 1)
        table.mergeCells(0, 6, 2, 1)
        table.mergeCells(0, 7, 2, 1)
        table.addRow()

        # 2110
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Из числа пациентов, больных наркоманией, снятых с наблюдения в связи со смертью (гр. 6 табл. 2102), умерло по причинам:')
        splitTitle(cursor, u'(2110)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('15%', [u'психическое заболевание', u'1'], CReportBase.AlignRight),
            ('15%', [u'острое отравление (передозировка) наркотиков', u'2'], CReportBase.AlignRight),
            ('14%', [u'соматическое заболевание', u'3'], CReportBase.AlignRight),
            ('14%', [u'самоубийство', u'4'], CReportBase.AlignRight),
            ('14%', [u'несчастный случай', u'5'], CReportBase.AlignRight),
            ('14%', [u'другие причины', u'6'], CReportBase.AlignRight),
            ('14%', [u'не известно', u'7'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.addRow()

        # 2130
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Из числа пациентов, состоящих под наблюдением на конец года (гр. 8 табл. 2100), находятся в ремиссии, из них с диагнозом:')
        splitTitle(cursor, u'(2130)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('11%', [u'синдром зависимости от алкоголя (стр. 01 и 02)', u'от 6 мес. до 1 года', u'1'], CReportBase.AlignRight),
            ('11%', [u'', u'от 1 до 2 лет', u'2'], CReportBase.AlignRight),
            ('11%', [u'', u'свыше 2 лет', u'3'], CReportBase.AlignRight),
            ('11%', [u'синдром зависимости от наркотиков (стр. 06)', u'от 6 мес. до 1 года', u'4'], CReportBase.AlignRight),
            ('11%', [u'', u'от 1 до 2 лет', u'5'], CReportBase.AlignRight),
            ('11%', [u'', u'свыше 2 лет', u'6'], CReportBase.AlignRight),
            ('11%', [u'синдром зависимости от ненаркотических ПАВ (стр. 07)', u'от 6 мес. до 1 года', u'7'], CReportBase.AlignRight),
            ('11%', [u'', u'от 1 до 2 лет', u'8'], CReportBase.AlignRight),
            ('12%', [u'', u'свыше 2 лет', u'9'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 3)
        table.mergeCells(0, 3, 1, 3)
        table.mergeCells(0, 6, 1, 3)
        table.addRow()

        # 2140
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Из числа пациентов, находящихся под наблюдением в течение отчетного года, перенесли интоксикационные психозы (гр. 6 и 8 табл. 2100), из них с диагнозом:')
        splitTitle(cursor, u'(2140)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('25%', [u'синдром зависимости от наркотиков (из стр. 06)', u'1'], CReportBase.AlignRight),
            ('25%', [u'синдром зависимости от ненаркотических ПАВ (из стр. 07)', u'2'], CReportBase.AlignRight),
            ('25%', [u'употребление наркотиков с вредными последствиями (из стр. 09)', u'3'], CReportBase.AlignRight),
            ('25%', [u'употребление ненаркотических ПАВ с вредными последствиями (из стр. 10)', u'4'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.addRow()

        # 2150
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число пациентов, проходивших в течение отчетного года амбулаторное анонимное лечение и (или) реабилитацию:')
        splitTitle(cursor, u'(2150)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('17%', [u'Ведомственная принадлежность медицинской организации', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Всего больных', u'', u'3'], CReportBase.AlignRight),
            ('10%', [u'синдром зависимости от алкоголя:', u'алкоголизм', u'4'], CReportBase.AlignRight),
            ('10%', [u'', u'алкогольные психозы', u'5'], CReportBase.AlignRight),
            ('10%', [u'синдром зависимости от наркотиков и ненаркотических ПАВ:', u'наркомания', u'6'], CReportBase.AlignRight),
            ('10%', [u'', u'токсикомания', u'7'], CReportBase.AlignRight),
            ('10%', [u'острая интоксикация и употребление с вредными последствиями:', u'алкоголя', u'8'], CReportBase.AlignRight),
            ('10%', [u'', u'наркотиков', u'9'], CReportBase.AlignRight),
            ('10%', [u'', u'ненаркотичес-ких ПАВ', u'10'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(0, 7, 1, 3)
        i = table.addRow()
        t.setAlignment(Qt.AlignCenter)
        table.setText(i, 0, u'В организациях Минздрава России')
        table.setText(i, 1, '01')
        table.setText(i, 4, 'X', blockFormat=t)

        # 2160
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Сведения об амбулаторной реабилитации')
        splitTitle(cursor, u'(2160)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('22%', [u'Наименование болезней', u'', u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'', u'', u'2'], CReportBase.AlignCenter),
            ('15%', [u'Из общего числа пациентов (табл. 2100 стр. 11 гр. 6 и гр. 8) в течение отчетного года проходили амбулаторную реабилитацию:', u'всего', u'', u'', u'3'], CReportBase.AlignRight),
            ('12%', [u'', u'в том числе (из гр. 3):', u'успешно завершили реабилита-ционную программу', u'', u'4'], CReportBase.AlignRight),
            ('12%', [u'', u'', u'прервали реабилитацию', u'отказ от реабилитации', u'5'], CReportBase.AlignRight),
            ('12%', [u'', u'', u'', u'по другим причинам (умерли, осуждены и т.п.)', u'6'], CReportBase.AlignRight),
            ('12%', [u'', u'', u'на конец года продолжили реабилитацию', u'', u'7'], CReportBase.AlignRight),
            ('12%', [u'Из общего числа  (гр.3) - после прохождения стационарной реабилитации', u'', u'', u'', u'8'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 1, 5)
        table.mergeCells(1, 2, 3, 1)
        table.mergeCells(1, 3, 1, 4)
        table.mergeCells(2, 3, 2, 1)
        table.mergeCells(2, 4, 1, 2)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(0, 7, 4, 1)

        for row, rowDescr in enumerate(CompRows2160):
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[2])

        # 2170
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Контингенты пациентов, проходивших обязательное или альтернативное амбулаторное лечение')
        splitTitle(cursor, u'(2170)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('19%', [u'Наименование болезней', u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Обратились в течение года в связи с решением суда о назначении лечения - всего', u'', u'', u'3'], CReportBase.AlignRight),
            ('8%', [u'из них по поводу:', u'', u'обязательного лечения', u'4'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'альтернативного лечения', u'5'], CReportBase.AlignRight),
            ('10%', [u'Прекратили лечение:', u'всего', u'', u'6'], CReportBase.AlignRight),
            ('8%', [u'', u'в том числе по причинам:', u'окончание лечения', u'7'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'из них (гр. 6) - находятся в ремиссии свыше 1 года', u'8'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'отказ от лечения и самовольное прекращение лечения', u'9'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'иное (умер, осужден и т.п.)', u'10'], CReportBase.AlignRight),
            ('8%', [u'На конец отчетного года - продолжили лечение', u'', u'', u'11'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 2, 2)
        table.mergeCells(0, 5, 1, 5)
        table.mergeCells(1, 5, 2, 1)
        table.mergeCells(1, 6, 1, 4)
        table.mergeCells(0, 10, 3, 1)

        for row, rowDescr in enumerate(CompRows2170):
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[2])

        return doc