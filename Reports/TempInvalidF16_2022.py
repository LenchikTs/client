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

from PyQt4                  import QtGui
from PyQt4.QtCore import QDate

from Orgs.Utils import getOrgStructureDescendants
from RefBooks.TempInvalidState import CTempInvalidState
from library.Utils          import calcAgeInYears, forceDate, forceInt, forceString
from library.MapCode        import createMapCodeToRowIdx
from Reports.Report         import normalizeMKB
from Reports.ReportBase     import CReportBase, createTable
from Reports.TempInvalidF16 import CTempInvalidF16, selectData
from library.database import addDateInRange

MainRows = [
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
    ( u'COVID-19', u'U07.1, U07.2', (51, 50)),
    ( u'Всего по заболеваниям', u'A00-T98, U07.1, U07.2', (53, 52)),
    ( u'из них: аборты (из стр. 45)', u'O03-O08', (54, -1)),
    ( u'Уход за больным', u'', (56, 55)),
    ( u'Отпуск в связи с санаторно-курортным лечением (без туберкулеза и долечивания инфаркта миокарда)', u'', (58, 57)),
    ( u'Освобождение от работы в связи с карантином и бактерионосительством', u'', (60, 59)),
    ( u'из них: в связи с карантином по COVID-19 (из стр. 59–60)', u'Z20.8, Z22.8, Z29.0', (62, 61)),
    ( u'ИТОГО ПО ВСЕМ ПРИЧИНАМ', u'', (64, 63)),
    ( u'Отпуск по беременности и родам (неосложненным)', u'', (65, -1)),
]


def selectData(params):
    stmt="""
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
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    byPeriod = params.get('byPeriod', False)
    doctype = params.get('doctype', 0)
    tempInvalidReasonId = params.get('tempInvalidReason', None)
    onlyClosed = params.get('onlyClosed', True)
    orgStructureId = params.get('orgStructureId', None)
    personId = params.get('personId', None)
    insuranceOfficeMark = params.get('insuranceOfficeMark', 0)
    hasBeginPerson = params.get('hasBeginPerson', False)
    hasEndPerson = params.get('hasEndPerson', False)
    db = QtGui.qApp.db
    table = db.table('TempInvalid')
    cond = []
    if doctype:
        cond.append(table['doctype_id'].eq(doctype))
    else:
        cond.append(table['type'].eq(0))
    cond.append(table['deleted'].eq(0))
    if tempInvalidReasonId:
        cond.append(table['tempInvalidReason_id'].eq(tempInvalidReasonId))
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
    if hasBeginPerson:
        cond.append(u'EXISTS(SELECT NULL '
                    u'FROM Person P '
                    u'JOIN TempInvalidDocument TID ON TID.person_id = P.id '
                    u'WHERE P.deleted = 0 AND TID.deleted = 0 AND TID.master_id = TempInvalid.id)')
    if hasEndPerson:
        cond.append(u'EXISTS(SELECT NULL '
                    u'FROM Person P '
                    u'JOIN TempInvalidDocument TID ON TID.execPerson_id = P.id '
                    u'WHERE P.deleted = 0 AND TID.deleted = 0 AND TID.master_id = TempInvalid.id)')
    if insuranceOfficeMark in (1, 2):
        cond.append(table['insuranceOfficeMark'].eq(insuranceOfficeMark-1))
    query = db.query(stmt % (db.joinAnd(cond)))
    recordList = []
    while query.next():
        recordList.append(query.record())
    return recordList


class CTempInvalidF16_2022(CTempInvalidF16):
    def build(self, params):
        averageDuration = params.get('averageDuration', False)
        resultsForGroups = params.get('resultsForGroups', False)
        detailMKB = params.get('detailMKB', False)

        recordList = selectData(params)

        rowSize = 12
        if detailMKB:
            mapMainRows = {}
            rowsCount = 0
            for record in recordList:
                MKB = normalizeMKB(forceString(record.value('MKB')))
                rowList = mapMainRows.setdefault(MKB, [])
                if not rowList:
                    rowList.append(rowsCount)
                    rowsCount += 1
            reportMainData = [ [0]*rowSize for row in xrange(rowsCount*2+6) ]
            pregnancyRowIndex = -1 # не отображаются
        else:
            mapMainRows = createMapCodeToRowIdx( [row[1] for row in MainRows if row[1]] )
            reportMainData = [ [0]*rowSize for row in xrange(len(MainRows)*2) ]
            if resultsForGroups:
                reportMainDataTotal = [ [0]*rowSize for row in xrange(len(MainRows)) ]
            if averageDuration:
                avgDurationTotal = [ [0]*2 for row in xrange(len(MainRows)) ]
            pregnancyRowIndex  = len(MainRows) - 1

        totalDiseases  = [ [0]*rowSize for row in xrange(2) ]
        reportTotal    = [ [0]*rowSize for row in xrange(2) ]
        totalRowIndex      = pregnancyRowIndex - 1
        quarantineRowIndex = totalRowIndex - 2
        sanatoriumRowIndex = quarantineRowIndex - 1
        careRowIndex       = sanatoriumRowIndex - 1

        for record in recordList:
            reasonGroup = forceInt(record.value('reasonGroup'))
            reasonCode = forceString(record.value('reasonCode'))
            duration = forceInt(record.value('duration'))
            if reasonGroup == 1: # уход
                sex = forceInt(record.value('tsex'))
                age = forceInt(record.value('tage'))
            else:
                sex = forceInt(record.value('sex'))
                age = calcAgeInYears(forceDate(record.value('birthDate')), forceDate(record.value('caseBegDate')))
            if age < 15:
                continue
            if sex not in (1, 2):
                continue

            rows = []
            MKB = normalizeMKB(forceString(record.value('MKB')))
            if reasonGroup == 0: # заболевание
                rows.extend(mapMainRows.get(MKB, []))
                if rows:
                    rows.append(totalRowIndex)
            elif reasonGroup == 1: # уход
                if reasonCode in (u'09', u'12', u'13', u'15'): # уход за больным
                    rows = [careRowIndex, totalRowIndex]
                elif reasonCode == u'03': # карантин
                    rows = [quarantineRowIndex, totalRowIndex]
                elif reasonCode == u'14': # поствакцинальное осложнение
                    rows = [quarantineRowIndex, totalRowIndex]
                elif reasonCode == u'08': # санкурлечение
                    rows = [sanatoriumRowIndex, totalRowIndex]
            elif reasonGroup == 2:
                rows = [pregnancyRowIndex]

            ageCol = min(max(age, 15), 60)/5-1
            for row in rows:
                if row < 0:
                    continue
                reportLine = reportMainData[row*2+(1 if sex == 1 else 0)]
                reportLine[0] += duration
                reportLine[1] += 1
                reportLine[ageCol] += 1

        if detailMKB:
            pass
        else:
            # всего по заболеваниям
            for row in (0, 2, 4, 5, 7, 8, 9, 10, 11, 14, 18, 19, 20, 21, 22, 23, 24, 25):
                for i, value in enumerate(reportMainData[row*2]):
                    totalDiseases[0][i] += value
            for row in (0, 2, 4, 5, 7, 8, 9, 10, 11, 14, 18, 19, 20, 21, 23, 24, 25):
                for i, value in enumerate(reportMainData[row*2+1]):
                    totalDiseases[1][i] += value

            # итого по всем причинам
            for sex in xrange(2):
                for row in (28, 29, 30):
                    for i, value in enumerate(reportMainData[row*2+sex]):
                        reportTotal[sex][i] += value
                for i, value in enumerate(totalDiseases[sex]):
                    reportTotal[sex][i] += value

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
        table.mergeCells(0, 0, 2, 1) # п.н.
        table.mergeCells(0, 1, 2, 1) # мкб
        table.mergeCells(0, 2, 2, 1) # пол
        table.mergeCells(0, 3, 2, 1) # N
        table.mergeCells(0, 4, 2, 1) # дней
        table.mergeCells(0, 5, 2, 1) # случаев
        table.mergeCells(0, 6, 1,10) # по возрастам
        if averageDuration:
            table.mergeCells(0, 16, 2, 1)

        if detailMKB:
            reportRows = []
            rowNum = 1
            for i, item in enumerate(mapMainRows.items()):
                MKB, rowList = item
                if i in rowList:
                    block = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'BlockName'))
                    rowSep = (rowNum+1, rowNum)
                    rowNum += 2
                    reportRows.append((block, MKB, rowSep))
        else:
            reportRows = MainRows
        for row, rowDescr in enumerate(reportRows):
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
                    table.mergeCells(i, 0, 3, 1) # п.н.
                    table.mergeCells(i, 1, 3, 1) # мкб
                else:
                    table.mergeCells(i, 0, 2, 1) # п.н.
                    table.mergeCells(i, 1, 2, 1) # мкб
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
                if rowDescr[0] == u'ИТОГО ПО ВСЕМ ПРИЧИНАМ':
                    reportLine = reportTotal[0]
                elif rowDescr[0] == u'Всего по заболеваниям':
                    reportLine = totalDiseases[0]
                for col in xrange(rowSize):
                    table.setText(wTableRow, 4+col, reportLine[col])
                if averageDuration:
                    avgDuration = round((float(reportLine[0]) / reportLine[1]) if reportLine[1] else 0.0, 2)
                    table.setText(wTableRow, 16, '%.1f'%(avgDuration))
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
                if rowDescr[0] == u'ИТОГО ПО ВСЕМ ПРИЧИНАМ':
                    reportLine = reportTotal[1]
                elif rowDescr[0] == u'Всего по заболеваниям':
                    reportLine = totalDiseases[1]
                for col in xrange(rowSize):
                    table.setText(mTableRow, 4+col, reportLine[col])
                if averageDuration:
                    avgDuration = round((float(reportLine[0]) / reportLine[1]) if reportLine[1] else 0.0, 2)
                    table.setText(mTableRow, 16, '%.1f'%(avgDuration))
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
                    table.setText(tTableRow, 16, '%.1f'%(avgDuration))

        return doc
