# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.Utils import calcAgeInYears, forceDate, forceInt, forceString
from library.MapCode import createMapCodeToRowIdx
from library.database import addDateInRange
from Orgs.Utils import getOrgStructureDescendants

from RefBooks.TempInvalidState import CTempInvalidState

from Reports.Report import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable
from Reports.TempInvalidList import CTempInvalidSetupDialog


MainRows = [
    (u'Некоторые инфекционные и паразитарные болезни', u'A00-B99', (2, 1)),
    ( u'из них: туберкулез', u'A15-A19', (4, 3)),
    (u'Новообразования', u'C00-D48', (6, 5)),
    (u'из них злокачественные новообразования', u'C00-C97', (8, 7)),
    (u'Болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм', u'D50-D89', (10, 9)),
    (u'Болезни эндокринной системы, расстройства питания и нарушения обмена веществ', u'E00-E89,E90', (12, 11)),
    ( u'из них: сахарный диабет', u'E10-E14', (14, 13)),
    ( u'Психические расстройства и расстройства поведения', u'F00-F99', (16, 15)),
    (u'Болезни нервной системы', u'G00-G98,G99', (18, 17)),
    (u'Болезни глаза и его придаточного аппарата', u'H00-H59', (20, 19)),
    (u'Болезни уха и сосцевидного отростка', u'H60-H95', (22, 21)),
    (u'Болезни системы кровообращения', u'I00-I99', (24, 23)),
    ( u'из них: ишемические болезни сердца', u'I20-I25', (26, 25)),
    (u'цереброваскулярные болезни', u'I60-I69', (28, 27)),
    (u'Болезни органов дыхания', u'J00-J98,J99', (30, 29)),
    ( u'из них: острые распираторные инфекции верхних дыхательных путей', u'J00, J01, J04, J05, J06', (32, 31)),
    (u'грипп', u'J10, J11', (34, 33)),
    (u'пневмония', u'J12-J18', (36, 35)),
    (u'Болезни органов пищеварения', u'K00-K92,K93', (38, 37)),
    (u'Болезни кожи и подкожной клетчатки', u'L00-L99', (40, 39)),
    (u'Болезни костномышечной и соединительной ткани', u'M00-M99', (42, 41)),
    (u'Болезни мочеполовой системы', u'N00-N99', (44, 43)),
    (u'Беременность, роды и послеродовой период', u'O00-O99', (45, -1)),
    (u'Врожденные аномалии (пороки развития), деформации и хромосомные нарушения', u'Q00-Q99', (47, 46)),
    (u'Травмы, отравления и некоторые другие последствия воздействия внешних причин', u'S00-T98', (49, 48)),
    (u'Всего по заболеваниям', u'A00-T98, U07', (51, 50)),
    (u'из них: аборты (из стр. 45)', u'O03-O08', (52, -1)),
    (u'Уход за больным', u'', (54, 53)),
    (u'Отпуск в связи с санаторно-курортным лечением (без туберкулеза и долечивания инфаркта миокарда)', u'', (56, 55)),
    (u'Освобождение от работы в связи с карантином и бактерионосительством', u'', (58, 57)),
    (u'ИТОГО ПО ВСЕМ ПРИЧИНАМ', u'', (60, 59)),
    (u'Отпуск по беременности и родам (неосложненным)', u'', (61, -1)),
    (u'COVID 19', u'U07.1', (63, 62)),
    (u'', u'U07.2', (65, 64))
    ]


MainCOVID19Rows = [
    ( u'Некоторые инфекционные и паразитарные болезни', u'A00-B99', (2, 1)),
    ( u'из них: туберкулез', u'A15-A19', (4, 3)),
    ( u'Новообразования', u'C00-D48', (6, 5)),
    ( u'из них злокачественные новообразования', u'C00-C97', (8, 7)),
    ( u'Болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм', u'D50-D89', (10, 9)),
    ( u'Болезни эндокринной системы, расстройства питания и нарушения обмена веществ', u'E00-E89,E90', (12, 11)),
    ( u'из них: сахарный диабет', u'E10-E14', (14, 13)),
    ( u'Психические расстройства и расстройства поведения', u'F00-F99', (16, 15)),
    ( u'Болезни нервной системы', u'G00-G98,G99', (18, 17)),
    ( u'Болезни глаза и его придаточного аппарата', u'H00-H59', (20, 19)),
    ( u'Болезни уха и сосцевидного отростка', u'H60-H95', (22, 21)),
    ( u'Болезни системы кровообращения', u'I00-I99', (24, 23)),
    ( u'из них: ишемические болезни сердца', u'I20-I25', (26, 25)),
    ( u'цереброваскулярные болезни', u'I60-I69', (28, 27)),
    ( u'Болезни органов дыхания', u'J00-J98,J99', (30, 29)),
    ( u'из них: острые распираторные инфекции верхних дыхательных путей', u'J00, J01, J04, J05, J06', (32, 31)),
    ( u'грипп', u'J09, J11', (34, 33)),
    ( u'пневмония', u'J12-J18', (36, 35)),
    ( u'Болезни органов пищеварения', u'K00-K92,K93', (38, 37)),
    ( u'Болезни кожи и подкожной клетчатки', u'L00-L99', (40, 39)),
    ( u'Болезни костномышечной и соединительной ткани', u'M00-M99', (42, 41)),
    ( u'Болезни мочеполовой системы', u'N00-N99', (44, 43)),
    ( u'Беременность, роды и послеродовой период', u'O00-O99', (45, -1)),
    ( u'Врожденные аномалии (пороки развития), деформации и хромосомные нарушения', u'Q00-Q99', (47, 46)),
    ( u'Травмы, отравления и некоторые другие последствия воздействия внешних причин', u'S00-T98', (49, 48)),
    ( u'Всего по заболеваниям', u'A00-T98', (51, 50)),
    ( u'из них: аборты (из стр. 45)', u'O03-O08', (52, -1)),
    ( u'COVID-19', u'U07.1', (54, 53)),
    ( u'Контакт по COVID-19', u'Z20.8', (56, 55)),
    ( u'Уход за больным', u'', (58, 57)),
    ( u'Отпуск в связи с санаторно-курортным лечением (без туберкулеза и долечивания инфаркта миокарда)', u'', (60, 59)),
    ( u'Освобождение от работы в связи с карантином и бактерионосительством', u'', (62, 61)),
    ( u'ИТОГО ПО ВСЕМ ПРИЧИНАМ', u'', (64, 63)),
    ( u'Отпуск по беременности и родам (неосложненным)', u'', (65, -1)),
    ]


def selectData(begDate, endDate, byPeriod, doctype, tempInvalidReasonIdList, onlyClosed, orgStructureId, personId, insuranceOfficeMark):
    stmt = """
SELECT
   Client.birthDate,
   Client.sex,
   TempInvalid.caseBegDate,
   TempInvalid.endDate,
   TempInvalid.sex AS tsex,
   TempInvalid.age AS tage,
   DATEDIFF(TempInvalid.endDate, TempInvalid.caseBegDate)+1 AS duration,
   Diagnosis.MKB,
   rbTempInvalidReason.code AS reasonCode,
   rbTempInvalidReason.grouping AS reasonGroup
   FROM TempInvalid
   LEFT JOIN TempInvalid AS NextTempInvalid ON TempInvalid.id = NextTempInvalid.prev_id
   LEFT JOIN Diagnosis ON Diagnosis.id = TempInvalid.diagnosis_id
   LEFT JOIN Person    ON Person.id = TempInvalid.person_id
   LEFT JOIN rbTempInvalidReason ON rbTempInvalidReason.id = TempInvalid.tempInvalidReason_id
   LEFT JOIN Client    ON Client.id = TempInvalid.client_id
WHERE
   NextTempInvalid.id IS NULL AND
   %s
    """
    db = QtGui.qApp.db
    table = db.table('TempInvalid')
    cond = []
    if doctype:
        cond.append(table['doctype_id'].eq(doctype))
    else:
        cond.append(table['type'].eq(0))
    cond.append(table['deleted'].eq(0))
    if tempInvalidReasonIdList:
        cond.append(table['tempInvalidReason_id'].inlist(tempInvalidReasonIdList))
    if byPeriod:
        cond.append(table['caseBegDate'].le(endDate))
        cond.append(table['endDate'].ge(begDate))
    else:
        addDateInRange(cond, table['endDate'], begDate, endDate)
    if onlyClosed:
        cond.append(table['state'].eq(CTempInvalidState.closed))
    if orgStructureId:
        tablePerson = db.table('Person')
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    if personId:
        cond.append(table['person_id'].eq(personId))
    if insuranceOfficeMark in (1, 2):
        cond.append(table['insuranceOfficeMark'].eq(insuranceOfficeMark-1))
    return db.query(stmt % (db.joinAnd(cond)))


class CTempInvalidF16(CReport):
    name = u'Сведения о причинах временной нетрудоспособности (Ф.16ВН)'

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(self.name)


    def getSetupDialog(self, parent):
        result = CTempInvalidSetupDialog(parent)
        result.setTempInvalidCOVID19Visible(False)
        result.setTitle(self.title())
        result.resize(400, 10)
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        byPeriod = params.get('byPeriod', False)
        doctype = params.get('doctype', 0)
        tempInvalidReasonIdList = params.get('tempInvalidReasonIdList', None)
        onlyClosed = params.get('onlyClosed', True)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        insuranceOfficeMark = params.get('insuranceOfficeMark', 0)
        averageDuration = params.get('averageDuration', False)
        resultsForGroups = params.get('resultsForGroups', False)
        isTempInvalidCOVID19 = params.get('isTempInvalidCOVID19', False)
        if isTempInvalidCOVID19:
            titleMainRows = MainCOVID19Rows
        else:
            titleMainRows = MainRows
        mapMainRows = createMapCodeToRowIdx( [row[1] for row in titleMainRows if row[1]] )  # выстраивает словарь {'код МКБ': [строки для записи]}
        rowSize = 12                                                                        # НО у нас часть строк в списке без МКБ, поэтому дальше в коде будет подмена нумерации
        reportMainData = [ [0]*rowSize for row in xrange(len(titleMainRows)*2) ]
        if resultsForGroups:
            reportMainDataTotal = [ [0]*rowSize for row in xrange(len(titleMainRows)) ]
        if averageDuration:
            avgDurationTotal = [[0]*2 for row in xrange(len(MainRows))]
        pregnancyRowIndex = len(MainRows)-3  # -2 строки в конце таблицы для COVID 19
        totalRowIndex = pregnancyRowIndex-1
        quarantineRowIndex = totalRowIndex-1
        sanatoriumRowIndex = quarantineRowIndex-1
        careRowIndex = sanatoriumRowIndex-1

        query = selectData(begDate, endDate, byPeriod, doctype, tempInvalidReasonIdList, onlyClosed, orgStructureId, personId, insuranceOfficeMark)
        while query.next():
            record = query.record()
            reasonGroup = forceInt(record.value('reasonGroup'))
            reasonCode = forceString(record.value('reasonCode'))
            duration = forceInt(record.value('duration'))
            if reasonGroup == 1:  # уход
#                sex = forceInt(record.value('sex'))
#                age = calcAgeInYears(forceDate(record.value('birthDate')), forceDate(record.value('begDate')))
                sex = forceInt(record.value('tsex'))
                age = forceInt(record.value('tage'))
            else:
                sex = forceInt(record.value('sex'))
                age = calcAgeInYears(forceDate(record.value('birthDate')), forceDate(record.value('caseBegDate')))

            rows = []
            if reasonGroup == 0:  # заболевание
                MKB = forceString(record.value('MKB'))
                if MKB[:2] == 'N7':
                    pass

                rows.extend(mapMainRows.get(normalizeMKB(MKB), []))
                if 27 in rows:
                    rows.remove(27)  # Изначально mapMainRows выдает строки 25 и 27
                    rows.append(32)  # COVID 19 U07.1
                if 28 in rows:
                    rows.remove(28)  # Изначально mapMainRows выдает строки 25 и 28
                    rows.append(33)  # COVID 19 U07.2
                if rows:  # or MKB[:1] == 'Z':
                    rows.append(totalRowIndex)
            elif reasonGroup == 1:  # уход
                if reasonCode in (u'09', u'12', u'13', u'15'):  # уход за больным
                    rows = [careRowIndex, totalRowIndex]
                elif reasonCode == u'03':  # карантин
                    rows = [quarantineRowIndex, totalRowIndex]
                elif reasonCode == u'14':  # поствакцинальное осложнение
                    rows = [quarantineRowIndex, totalRowIndex]
                elif reasonCode == u'08':  # санкурлечение
                    rows = [sanatoriumRowIndex, totalRowIndex]
            elif reasonGroup == 2:
                rows = [pregnancyRowIndex]
            if age < 15:
                continue
            if sex not in (1, 2):
                continue
            ageCol = min(max(age, 15), 60)/5-1
            for row in rows:
                reportLine = reportMainData[row*2+(1 if sex == 1 else 0)]
                reportLine[0] += duration
                reportLine[1] += 1
                reportLine[ageCol] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.name)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Причина нетрудоспособности',    u'',            u'1' ], CReportBase.AlignLeft),
            ('10%', [u'Код по МКБ X',                  u'',            u'2' ], CReportBase.AlignLeft),
            ( '5%', [u'Пол',                           u'',            u'3' ], CReportBase.AlignCenter),
            ( '5%', [u'№ строки',                      u'',            u'4' ], CReportBase.AlignRight),
            ('10%', [u'число дней',                    u'',            u'5' ], CReportBase.AlignRight),
            ( '5%', [u'число случаев',                 u'',            u'6' ], CReportBase.AlignRight),
            ( '5%', [u'в т.ч. по возрастам',           u'15-19',       u'7' ], CReportBase.AlignRight),
            ( '5%', [u'',                              u'20-24',       u'8' ], CReportBase.AlignRight),
            ( '5%', [u'',                              u'25-29',       u'9' ], CReportBase.AlignRight),
            ( '5%', [u'',                              u'30-34',       u'10'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'35-39',       u'11'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'40-44',       u'12'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'45-49',       u'13'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'50-54',       u'14'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'55-59',       u'15'], CReportBase.AlignRight),
            ( '5%', [u'',                              u'60 и старше', u'16'], CReportBase.AlignRight),
            ]
        if averageDuration:
            tableColumns.insert(16, ('5%', [u'Средняя длительность', u'', u'17'], CReportBase.AlignRight))
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)  # п.н.
        table.mergeCells(0, 1, 2, 1)  # мкб
        table.mergeCells(0, 2, 2, 1)  # пол
        table.mergeCells(0, 3, 2, 1)  # N
        table.mergeCells(0, 4, 2, 1)  # дней
        table.mergeCells(0, 5, 2, 1)  # случаев
        table.mergeCells(0, 6, 1,10)  # по возрастам
        if averageDuration:
            table.mergeCells(0, 16, 2, 1)
        for row, rowDescr in enumerate(titleMainRows):
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            rowSep = rowDescr[2]
            tTableRow = -1
            if rowSep[0] > 0 and rowSep[1] > 0:
                i1 = table.addRow()
                mTableRow = i
                wTableRow = i1
                if resultsForGroups:
                    tTableRow = table.addRow()
                    table.mergeCells(i, 0, 3, 1)  # п.н.
                    table.mergeCells(i, 1, 3, 1)  # мкб
                else:
                    table.mergeCells(i, 0, 2, 1)  # п.н.
                    table.mergeCells(i, 1, 2, 1)  # мкб
            elif rowSep[0] > 0:
                mTableRow = -1
                wTableRow = i
            else:
                mTableRow = i
                wTableRow = -1
            if wTableRow >= 0:
                table.setText(wTableRow, 2, u'ж')
                table.setText(wTableRow, 3, rowSep[0])
                reportLine = reportMainData[row*2]
                for col in xrange(rowSize):
                    table.setText(wTableRow, 4+col, reportLine[col])
                if averageDuration:
                    avgDuration = round((float(reportLine[0]) / reportLine[1]) if reportLine[1] else 0.0, 2)
                    table.setText(wTableRow, 16, '%.1f' % (avgDuration))
                if resultsForGroups:
                    for col in xrange(rowSize):
                        reportMainDataTotal[row][col] += reportLine[col]
                    if averageDuration:
                        avgDurationTotal[row][0] += reportLine[0]
                        avgDurationTotal[row][1] += reportLine[1]
            if mTableRow >= 0:
                table.setText(mTableRow, 2, u'м')
                table.setText(mTableRow, 3, rowSep[1])
                reportLine = reportMainData[row*2+1]
                for col in xrange(rowSize):
                    table.setText(mTableRow, 4+col, reportLine[col])
                if averageDuration:
                    avgDuration = round((float(reportLine[0]) / reportLine[1]) if reportLine[1] else 0.0, 2)
                    table.setText(mTableRow, 16, '%.1f' % (avgDuration))
                if resultsForGroups:
                    for col in xrange(rowSize):
                        reportMainDataTotal[row][col] += reportLine[col]
                    if averageDuration:
                        avgDurationTotal[row][0] += reportLine[0]
                        avgDurationTotal[row][1] += reportLine[1]
            if resultsForGroups and tTableRow > 0:
                table.setText(tTableRow, 2, u'итого')
                for col in xrange(rowSize):
                    table.setText(tTableRow, 4+col, reportMainDataTotal[row][col])
                if averageDuration:
                    avgDuration = round((float(avgDurationTotal[row][0]) / avgDurationTotal[row][1]) if avgDurationTotal[row][1] else 0.0, 2)
                    table.setText(tTableRow, 16, '%.1f' % (avgDuration))
        return doc
