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
from Reports.Utils import splitTitle, dateRangeAsStr
from library.MapCodeWithExSubClass import createMapCodeToRowIdx, normalizeMKB
from library.Utils import forceBool, forceInt, forceString
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

# титул / № строки / пол / диапазон возрастов
MainRows = [
    (u'0 - 4 года', '01', u'м', '0-4'),
    (u'', '02', u'ж', '0-4'),
    (u'5 - 9 лет', '03', u'м', '5-9'),
    (u'', '04', u'ж', '5-9'),
    (u'10 - 14 лет', '05', u'м', '10-14'),
    (u'', '06', u'ж', '10-14'),
    (u'15 - 17 лет', '07', u'м', '15-17'),
    (u'', '08', u'ж', '15-17'),
    (u'Итого (0 - 17 лет)', '09', u'м', '0-17'),
    (u'', '10', u'ж', '0-17')
]

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows2000 = [
    (0, u'Всего заболеваний', u'A00-T98', u'A00-T98', u'1.0'),
    (1, u'в том числе:\nнекоторые инфекционные и паразитарные болезни', u'A00-B99', u'A00-B99', u'2.0'),
    (2, u'из них:\nтуберкулез', u'A15-A19', u'A15-A19', u'2.1'),
    (2, u'вирусные инфекции центральной нервной системы', u'A80-A89', u'A80-A89', u'2.2'),
    (2, u'последствия инфекционных и паразитарных болезней', u'B90-B94', u'B90-B94', u'2.3'),
    (1, u'новообразования', u'C00-D48', u'C00-D48', u'3.0'),
    (2, u'из них:\nзлокачественные новообразования лимфоидной, кроветворной и родственных им тканей', u'C81-C96', u'C81-C96', u'3.1'),
    (1, u'болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм', u'D50-D89', u'D50-D89', u'4.0'),
    (2, u'нарушения свертываемости крови, пурпура и другие геморрагические состояния', u'D65-D69', u'D65-D69', u'4.1'),
    (1, u'болезни эндокринной системы, расстройства питания и нарушения обмена веществ', u'E00-E90', u'E00-E90', u'5.0'),
    (2, u'из них:\nболезни щитовидной железы', u'E00-E07', u'E00-E07', u'5.1'),
    (2, u'сахарный диабет', u'E10-E14', u'E10-E14', u'5.2'),
    (1, u'психические расстройства и расстройства поведения', u'F00-F99', u'F00-F99', u'6.0'),
    (2, u'из них:\nумственная отсталость', u'F70-F79', u'F70-F79', u'6.1'),
    (2, u'детский аутизм, атипичный аутизм, синдром Ретта, дезинтегративное расстройство детского возраста', u'F84.0-3', u'F84.0-3', u'6.2'),
    (1, u'болезни нервной системы', u'G00-G99', u'G00-G99', u'7.0'),
    (2, u'из них:\nвоспалительные болезни центральной нервной системы', u'G00-G09', u'G00-G09', u'7.1'),
    (2, u'системные атрофии, поражающие преимущественно нервную систему', u'G10-G13', u'G10-G13', u'7.2'),
    (2, u'эпизодические и пароксизмальные расстройства', u'G40-G47', u'G40-G47', u'7.3'),
    (2, u'церебральный паралич и другие паралитические синдромы', u'G80-G83', u'G80-G83', u'7.4'),
    (2, u'другие нарушения нервной системы', u'G90-G99', u'G90-G99', u'7.5'),
    (1, u'болезни глаза и его придаточного отростка', u'H00-H59', u'H00-H59', u'8.0'),
    (2, u'из них:\nслепота обоих глаз', u'H54.0', u'H54.0', u'8.1'),
    (1, u'болезни уха и сосцевидного отростка', u'H60-H95', u'H60-H95', u'9.0'),
    (2, u'из них:\nкондуктивная потеря слуха двусторонняя', u'H90.0', u'H90.0', u'9.1'),
    (2, u'нейросенсорная потеря слуха двусторонняя', u'H90.3', u'H90.3', u'9.2'),
    (1, u'болезни системы кровообращения', u'I00-I99', u'I00-I99', u'10.0'),
    (1, u'болезни органов дыхания', u'J00-J99', u'J00-J99', u'11.0'),
    (2, u'из них:\nастма, астматический статус', u'J45, J46', u'J45; J46', u'11.1'),
    (1, u'болезни органов пищеварения', u'K00-K93', u'K00-K93', u'12.0'),
    (2, u'из них:\nболезни пищевода, желудка и двенадцатиперстной кишки', u'K20-K31', u'K20-K31', u'12.1'),
    (2, u'болезни печени, желчного пузыря, желчевыводящих путей и поджелудочной железы', u'K70-K77, K80-K87', u'K70-K77; K80-K87', u'12.2'),
    (1, u'болезни кожи и подкожной клетчатки', u'L00-L99', u'L00-L99', u'13.0'),
    (2, u'из них:\nатопический дерматит', u'L20', u'L20', u'13.1'),
    (1, u'болезни костно-мышечной системы и соединительной ткани', u'M00-M99', u'M00-M99', u'14.0'),
    (2, u'из них:\nреактивные артропатии', u'M02', u'M02', u'14.1'),
    (2, u'юношеский (ювенильный) артрит', u'M08', u'M08', u'14.2'),
    (2, u'системные поражения соединительной ткани', u'M30-M36', u'M30-M36', u'14.3'),
    (2, u'остеопатии и хондропатии', u'M80-M94', u'M80-M94', u'14.4'),
    (1, u'болезни мочеполовой системы', u'N00-N99', u'N00-N99', u'15.0'),
    (2, u'из них:\nгломерулярные, тубулоинтерстициальные болезни почек, почечная недостаточность, другие болезни почки', u'N00-N19,N25-N29', u'N00-N19;N25-N29', u'15.1'),
    (1, u'беременность, роды и послеродовой период', u'O00-O99', u'O00-O99', u'16.0'),
    (1, u'отдельные состояния, возникающие в перинатальном периоде', u'P05-P96', u'P05-P96', u'17.0'),
    (1, u'врожденные аномалии', u'Q00-Q99', u'Q00-Q99', u'18.0'),
    (2, u'из них:\nаномалии нервной системы', u'Q00-Q07', u'Q00-Q07', u'18.1'),
    (2, u'аномалии системы кровообращения', u'Q20-Q28', u'Q20-Q28', u'18.2'),
    (2, u'хромосомные нарушения (не классифицированные в других рубриках)', u'Q90-Q99', u'Q90-Q99', u'18.3'),
    (1, u'травмы, отравления и некоторые другие последствия воздействия внешних причин', u'S00-T98', u'S00-T98', u'19.0'),
]

def createMapSexAgeToRowIdx(codesList):
    mapCodeToRowIdx = {}
    for rowIdx, (sex, ages) in enumerate(codesList):
        ageRanges = ages.split('-')
        for age in xrange(forceInt(ageRanges[0]), forceInt(ageRanges[1]) + 1):
            mapCodeToRowIdx.setdefault((1 if sex == u'м' else 2, age), []).append(rowIdx)
    return mapCodeToRowIdx

def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    isPsychiatry = params.get('isPsychiatry', False)
    isOnlyContingent = params.get('isOnlyContingent', False)
    if isPsychiatry:
        psyCols = u', cck.MKB'
        psyJoins = u"""left JOIN ClientContingentKind cck ON cck.id = (SELECT k.id FROM ClientContingentKind k
left JOIN rbContingentKind ck ON k.contingentKind_id = ck.id
WHERE k.client_id = c.id AND k.deleted = 0 {0}
AND k.endDate IS NULL
ORDER BY k.begDate DESC
LIMIT 1)""".format(u"AND ck.code IN ('Д-наблюдение', 'ПДЛР')" if isOnlyContingent else u'')
        psyCond = u" AND css.note like '%4с%'"
        if isOnlyContingent:
            psyCond += u' AND cck.id IS not NULL'
        firstInvCol = u"""IF((SELECT COUNT(DISTINCT ClientSocStatus.id) FROM ClientSocStatus
  LEFT JOIN rbSocStatusType sstold ON sstold.id = ClientSocStatus.socStatusType_id
  WHERE ClientSocStatus.client_id=css.client_id AND ClientSocStatus.begDate BETWEEN {begDate} AND {endDate} AND code IN ('081', '082', '083', '084') AND note IN ('1с', '2с', '3с', '4с') )=1, 1, 0) AS isFirstDisability""".format(begDate=db.formatDate(begDate),
            endDate=db.formatDate(endDate))
    else:
        firstInvCol = u"IF((SELECT COUNT(DISTINCT ClientSocStatus.id) FROM ClientSocStatus  LEFT JOIN rbSocStatusType sstold ON sstold.id = ClientSocStatus.socStatusType_id  WHERE ClientSocStatus.client_id=css.client_id AND ClientSocStatus.begDate BETWEEN {begDate} AND {endDate} AND code IN ('081', '082', '083', '084') AND note IN ('1с', '2с', '3с', '4с') )=1, 1, 0) AS isFirstDisability".format(begDate=db.formatDate(begDate),
            endDate=db.formatDate(endDate))
        psyCols = ''
        psyJoins = ''
        psyCond = ''

    stmt = u'''
SELECT COUNT(distinct c.id) AS cnt, c.sex, age(c.birthDate, {endDate}) AS age,
  {firstInvCol},
  EXISTS(SELECT NULL 
          FROM ClientSocStatus css_2
          left JOIN rbSocStatusClass ssc_2 ON ssc_2.id = css_2.socStatusClass_id
          left JOIN rbSocStatusType sst_2 ON sst_2.id = css_2.socStatusType_id
          WHERE css_2.client_id = css.client_id AND css_2.deleted = 0 AND IFNULL(css_2.endDate, {endDate} + INTERVAL 1 DAY) > {endDate}
          AND sst_2.code = 'с12' AND ssc_2.code = '9') AS isOrphan
  {psyCols}  
  FROM ClientSocStatus css
left JOIN rbSocStatusClass ssc ON ssc.id = css.socStatusClass_id
left JOIN rbSocStatusClass ssc2 ON ssc2.id = ssc.group_id
left JOIN rbSocStatusType sst ON sst.id = css.socStatusType_id
left JOIN Client c on c.id = css.client_id
{psyJoins}
WHERE css.deleted = 0 AND c.deleted = 0 AND sst.code = '084'
  {psyCond}  
  AND age(c.birthDate, {endDate}) < 18 AND ssc2.code = '1' AND ssc.code = '1'
 -- AND IFNULL(css.endDate, {endDate} + INTERVAL 1 DAY) > {endDate}
  AND IFNULL(css.endDate, {endDate}) >= {endDate}
  AND IFNULL(c.deathDate, {endDate} + INTERVAL 1 DAY) > {endDate}
GROUP BY c.sex, age, isFirstDisability, isOrphan {psyCols};
    '''.format(begDate=db.formatDate(begDate),
            endDate=db.formatDate(endDate),
            psyCols=psyCols,
            firstInvCol=firstInvCol,
            psyJoins=psyJoins,
            psyCond=psyCond)
    return db.query(stmt)


class CStatReportF19(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setOrgStructureVisible(False)
        result.setAddressTypeVisible(False)
        result.setForResultVisible(False)
        result.setTypeDNVisible(False)
        result.setChkOnliContingentVisible(False)
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
        isOnlyContingent = params.get('isOnlyContingent', False)
        if isOnlyContingent:
            description.append(u'только по контингентам')

        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CStatReportF19_1000(CStatReportF19):
    def __init__(self, parent):
        CStatReportF19.__init__(self, parent)
        self.setTitle(u'Форма № 19 Таблица 1000')

    def build(self, params):
        mapMainRows = createMapSexAgeToRowIdx([(row[2], row[3]) for row in MainRows])
        rowSize = 15
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        query = selectData(params)
        while query.next():
            record = query.record()
            age = forceInt(record.value('age'))
            sex = forceInt(record.value('sex'))
            cnt = forceInt(record.value('cnt'))
            isFirstDisability = forceBool(record.value('isFirstDisability'))
            isOrphan = forceBool(record.value('isOrphan'))
            cols = [0]
            if isFirstDisability:
                cols.append(1)
            if isOrphan:
                cols.append(2)

            rows = mapMainRows.get((sex, age), [])
            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'1. Контингенты детей-инвалидов')
        splitTitle(cursor, u'(1000)', u'Код по ОКЕИ: человек - 792', '90%')
        tableColumns = [
            ('5%', [u'Возраст ребенка', u'', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'', u'2'], CReportBase.AlignCenter),
            ('5%', [u'Пол ребенка', u'', u'', u'', u'3'], CReportBase.AlignCenter),
            ('5%', [u'Число детей-инвалидов', u'всего', u'', u'', u'4'], CReportBase.AlignRight),
            ('5%', [u'', u'из них', u'с впервые установленной инвалидностью', u'', u'5'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'детей-сирот', u'', u'6'], CReportBase.AlignRight),
            ('5%', [u'из них проживают в интернатных учреждениях системы:', u'Минздрава России', u'всего', u'', u'7'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'с впервые установленной инвалидностью (из гр. 7)', u'', u'8'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'получили медицинскую реабилитацию', u'всего (из гр. 7)', u'9'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'', u'с впервые установленной инвалидностью (из гр. 8)', u'10'], CReportBase.AlignRight),
            ('5%', [u'', u'Минобразования России', u'всего', u'', u'11'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'с впервые установленной инвалидностью (из гр. 11)', u'', u'12'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'получили медицинскую реабилитацию', u'всего (из гр. 11)', u'13'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'', u'с впервые установленной инвалидностью (из гр. 12)', u'14'], CReportBase.AlignRight),
            ('5%', [u'', u'Минтруда России', u'всего', u'', u'15'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'с впервые установленной инвалидностью (из гр. 15)', u'', u'16'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'получили медицинскую реабилитацию', u'всего (из гр. 15)', u'17'], CReportBase.AlignRight),
            ('5%', [u'', u'', u'', u'с впервые установленной инвалидностью (из гр. 16)', u'18'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 4, 1)
        table.mergeCells(0, 3, 1, 3)
        table.mergeCells(1, 3, 3, 1)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(2, 4, 2, 1)
        table.mergeCells(2, 5, 2, 1)
        table.mergeCells(0, 6, 1, 12)
        table.mergeCells(1, 6, 1, 4)
        table.mergeCells(1, 10, 1, 4)
        table.mergeCells(1, 14, 1, 4)
        table.mergeCells(2, 6, 2, 1)
        table.mergeCells(2, 7, 2, 1)
        table.mergeCells(2, 8, 1, 2)
        table.mergeCells(2, 10, 2, 1)
        table.mergeCells(2, 11, 2, 1)
        table.mergeCells(2, 12, 1, 2)
        table.mergeCells(2, 14, 2, 1)
        table.mergeCells(2, 15, 2, 1)
        table.mergeCells(2, 16, 1, 2)

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            if rowDescr[0] == '':
                table.mergeCells(i-1, 0, 2, 1)
            table.setText(i, 1, rowDescr[1])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        return doc

class CStatReportF19_1000_Psychiatry(CStatReportF19_1000):
    def build(self, params):
        params['isPsychiatry'] = True
        doc = CStatReportF19_1000.build(self, params)
        return doc

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setOrgStructureVisible(False)
        result.setAddressTypeVisible(False)
        result.setForResultVisible(False)
        result.setTypeDNVisible(False)
        result.setChkOnliContingentVisible()
        return result


class CStatReportF19_2000(CStatReportF19):
    def __init__(self, parent):
        CStatReportF19.__init__(self, parent)
        self.setTitle(u'Форма № 19 Таблица 2000')

    def build(self, params):
        rowSize = 10
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows2000))]
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows2000])

        query = selectData(params)
        while query.next():
            record = query.record()
            age = forceInt(record.value('age'))
            sex = forceInt(record.value('sex'))
            cnt = forceInt(record.value('cnt'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            addCols = forceInt(sex == 2)
            cols = [0 + addCols]
            if age >= 0 and age <= 4:
                cols.append(2 + addCols)
            elif age >= 5 and age <= 9:
                cols.append(4 + addCols)
            elif age >= 10 and age <= 14:
                cols.append(6 + addCols)
            elif age >= 15 and age <= 17:
                cols.append(8 + addCols)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += cnt

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'2. Распределение детей-инвалидов по заболеванию, обусловившему возникновение инвалидности')
        splitTitle(cursor, u'(2000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('28%', [u'Наименование классов и отдельных болезней', u'', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('5%', [u'Код по МКБ-10 пересмотра', u'', u'', u'3'], CReportBase.AlignCenter),
            ('6%', [u'Всего детей-инвалидов (0 - 17 лет)', u'', u'М', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'Ж', u'5'], CReportBase.AlignRight),
            ('6%', [u'в том числе в возрасте (лет):', u'0-4', u'М', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'Ж', u'7'], CReportBase.AlignRight),
            ('6%', [u'', u'5-9', u'М', u'8'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'Ж', u'9'], CReportBase.AlignRight),
            ('6%', [u'', u'10-14', u'М', u'10'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'Ж', u'11'], CReportBase.AlignRight),
            ('7%', [u'', u'15-17', u'М', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'Ж', u'13'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(1, 5, 1, 2)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(1, 9, 1, 2)
        table.mergeCells(1, 11, 1, 2)
        table.mergeCells(0, 5, 1, 8)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows2000):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[2])
            table.setText(i, 2, rowDescr[4])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        return doc


class CStatReportF19_2000_Psychiatry(CStatReportF19_2000):
    def build(self, params):
        params['isPsychiatry'] = True
        doc = CStatReportF19_2000.build(self, params)
        return doc

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setOrgStructureVisible(False)
        result.setAddressTypeVisible(False)
        result.setForResultVisible(False)
        result.setTypeDNVisible(False)
        result.setChkOnliContingentVisible()
        return result