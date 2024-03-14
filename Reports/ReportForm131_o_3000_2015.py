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
from PyQt4.QtCore import QDate

from library.Utils             import forceDate, forceInt, forceRef, forceString
from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from Orgs.Utils                import getOrgStructurePersonIdList


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    if not endDate:
        return None
    orgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            orgStructure = u''' AND Event.execPerson_id IN (%s)'''%(u','.join(str(personId) for personId in personIdList if personId))
    db = QtGui.qApp.db
    stmt = u'''
SELECT
    rbService.infis AS serviceCode,
    Action.status,
    Action.endDate,
    Action.MKB AS actionMkb,
    DATE(Action.endDate) BETWEEN %(begDate)s AND %(endDate)s AS actionExecNow,
    DATE(Action.endDate) BETWEEN DATE_ADD(DATE(Event.setDate), interval -1 YEAR)
        AND DATE(Event.setDate) AS actionExecPrev,
    EXISTS(SELECT 1
           FROM Diagnostic AS D
           LEFT JOIN Diagnosis ON Diagnosis.id = D.diagnosis_id
           LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id = D.result_id
           WHERE D.event_id = Event.id
             AND D.deleted = 0
             AND Diagnosis.MKB = Action.MKB
             AND Diagnosis.deleted = 0
             AND rbDiagnosticResult.code = '07'
          ) AS needToPayAttention,
    EXISTS(SELECT 1
           FROM ActionProperty
           WHERE ActionProperty.action_id = Action.id
             AND ActionProperty.deleted = 0
             AND ActionProperty.evaluation IS NOT NULL
             AND ActionProperty.evaluation != 0
          ) AS propertyEvaluation
FROM Event
left join EventType on EventType.id = Event.eventType_id
left join rbEventProfile on rbEventProfile.id = EventType.eventProfile_id
left join Action on Action.event_id = Event.id
left join ActionType on ActionType.id = Action.actionType_id
left join rbService on rbService.id = ActionType.nomenclativeService_id
WHERE Event.deleted = 0
  %(orgStructure)s
  AND Event.prevEvent_id IS NOT NULL
  AND DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s
  AND rbEventProfile.regionalCode = '8009'
  AND Action.deleted = 0
  AND ActionType.deleted = 0
''' % {  'orgStructure':orgStructure,
         'begDate': db.formatDate(begDate),
         'begDateMinusYear': db.formatDate(begDate.addYears(-1)),
         'endDate': db.formatDate(endDate),
      }
    return db.query(stmt)


class CReportForm131_o_3000_2015(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о втором этапе диспансеризации определенных групп взрослого населения')
        self.mapServiceCodeToRowNum = {
            'A04.12.005.003': [0],
            'A03.16.001': [2],
            'A03.18.001.012': [5],
            'A03.19.002': [5],
            'A09.05.024': [6],
            'B03.016.005': [6],
            'A12.09.001.003': [7],
            'A09.05.083': [9],
            'A12.22.005': [9],
            'B04.028.001.01': [10],
            'A09.05.130': [11],
            'B01.069.004': [13, 14]
            }

        stmt = u"""select distinct infis, substr(infis, 1, 7) as shortCode from rbService where substr(infis, 1, 7) in
        ('B04.023', 'B04.057', 'B04.053', 'B04.018', 'B04.001', 'B04.029', 'B04.047', 'B04.026')"""
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            shortCode = forceString(record.value('shortCode'))
            rowList = []
            if shortCode == 'B04.023':
                rowList = [1]
            elif shortCode == 'B04.057':
                rowList = [3, 4]
            elif shortCode == 'B04.053':
                rowList = [3]
            elif shortCode == 'B04.018':
                rowList = [4]
            elif shortCode == 'B04.001':
                rowList = [8]
            elif shortCode == 'B04.029':
                rowList = [12]
            elif shortCode in ['B04.047', 'B04.026']:
                rowList = [15]
            self.mapServiceCodeToRowNum[forceString(record.value('infis'))] = rowList

        self.rowNames = {
            '01': u'Дуплексное сканирование брахицефальных артерий',
            '02': u'Осмотр (консультация) врачом-неврологом',
            '03': u'Эзофагогастродуоденоскопия ',
            '04': u'Осмотр (консультация) врачом-хирургом или врачом-урологом',
            '05': u'Осмотр (консультация) врачом-хирургом или врачом-колопроктологом',
            '06': u'Колоноскопия или ректороманоскопия',
            '07': u'Определение липидного спектра крови',
            '08': u'Спирометрия',
            '09': u'Осмотр (консультация) врачом-акушером-гинекологом',
            '10': u'Определение концентрации гликированного гемоглобина в крови или тест на толерантность к глюкозе',
            '11': u'Осмотр (консультация) врачом-оториноларингологом',
            '12': u'Анализ крови на уровень содержания простатспецифического антигена',
            '13': u'Осмотр (консультация) врачом-офтальмологом',
            '14': u'Индивидуальное углубленное профилактическое консультирование',
            '15': u'Групповое профилактическое консультирование (школа пациента)',
            '16': u'Прием (осмотр) врача-терапевта',
            }

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result

    def _getDefault(self):
        result = [[0, 0, 0, 0, 0] for row in self.rowNames]
        return result

    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0, 0]
        while query.next():
            record = query.record()
            actionMkb = forceString(record.value('actionMkb'))
            serviceCode = forceString(record.value('serviceCode'))
            needToPayAttention = forceInt(record.value('needToPayAttention'))
            actionExecNow = forceInt(record.value('actionExecNow'))
            actionExecPrev = forceInt(record.value('actionExecPrev'))
            propertyEvaluation = forceInt(record.value('propertyEvaluation'))
            endDate = forceDate(record.value('endDate'))
            status = forceInt(record.value('status'))
            actionExecRefusal = (not endDate) and (status == 3)

            if serviceCode not in self.mapServiceCodeToRowNum:
                continue

            rowList = self.mapServiceCodeToRowNum[serviceCode]
            for row in rowList:
                reportLine = reportData[row]
                if needToPayAttention:
                    reportLine[0] += 1
                    reportDataTotal[0] += 1
                if endDate and status != 3:
                    if actionExecNow:
                        reportLine[1] += 1
                        reportDataTotal[1] += 1
                    elif actionExecPrev:
                        reportLine[2] += 1
                        reportDataTotal[2] += 1
                if actionExecRefusal:
                    reportLine[3] += 1
                    reportDataTotal[3] += 1
                if ('A00' <= actionMkb < 'U' or propertyEvaluation) and row not in (13, 14):
                    reportLine[4] += 1
                    reportDataTotal[4] += 1
        return reportData, reportDataTotal

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(3000)')
        cursor.insertBlock()
        tableColumns = [
            ('45%', [u'Медицинское мероприятие второго этапа диспансеризации', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ строки', u'', u'2'], CReportBase.AlignRight),
            ('10%', [u'Выявлено показание к дополнительному обследованию', u'', u'3'], CReportBase.AlignRight),
            ('10%', [u'Количество выполненных медицинских мероприятий', u'в рамках диспансеризации', u'4'],
                CReportBase.AlignRight),
            ('10%', [u'', u'проведено ранее (в предшествующие 12 мес.)', u'5'], CReportBase.AlignRight),
            ('10%', [u'Отказы', u'', u'6'], CReportBase.AlignRight),
            ('10%', [u'Выявлено заболеваний', u'', u'7'], CReportBase.AlignRight)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 2, 1)
        table.mergeCells(0, 6, 2, 1)
        query = selectData(params)
        if query is None:
            return doc
        reportData, total = self.getReportData(query)
        for num, key in enumerate(sorted(self.rowNames)):
            reportLine = reportData[num]
            i = table.addRow()
            table.setText(i, 0, self.rowNames[key])
            table.setText(i, 1, key)
            table.setText(i, 2, reportLine[0])
            table.setText(i, 3, reportLine[1])
            table.setText(i, 4, reportLine[2])
            table.setText(i, 5, reportLine[3])
            table.setText(i, 6, reportLine[4] if key not in ('14', '15') else 'X')
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        table.setText(i, 2, total[0])
        table.setText(i, 3, total[1])
        table.setText(i, 4, total[2])
        table.setText(i, 5, total[3])
        table.setText(i, 6, total[4])
        return doc
