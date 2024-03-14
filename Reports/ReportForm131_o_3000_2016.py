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

from Events.ActionStatus       import CActionStatus
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
    mesDispansIdList = params.get('mesDispansIdList', [])
    if mesDispansIdList:
        mesDispans = u''' AND Event.MES_id IN (%s)'''%(u','.join(forceString(mesId) for mesId in mesDispansIdList if mesId))
    else:
        mesDispans = u''
    db = QtGui.qApp.db
    stmt = u'''
SELECT
    Action.id AS actionId,
    Action.status,
    Action.endDate,
    Action.MKB AS actionMkb,
    Event.execDate,
    mes.MES_visit.additionalServiceCode AS numMesVisitCode,
    DATE(Action.endDate) BETWEEN %(begDate)s AND %(endDate)s AS actionExecNow,
    DATE(Action.endDate)>=%(begDateMinusYear)s AND DATE(Action.endDate)<%(begDate)s AS actionExecPrev,
--    EXISTS(SELECT 1
--            FROM Diagnostic AS D
--            LEFT JOIN Diagnosis ON Diagnosis.id = D.diagnosis_id
--            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id = D.result_id
--            WHERE D.event_id = Event.id
--              AND D.deleted = 0
--              AND Diagnosis.MKB = Action.MKB
--              AND Diagnosis.deleted = 0
--              AND rbDiagnosticResult.code = '07'
--           ) AS needToPayAttention,
    EXISTS(SELECT 1
           FROM ActionProperty
           WHERE ActionProperty.action_id = Action.id
             AND ActionProperty.deleted = 0
             AND ActionProperty.evaluation IS NOT NULL
             AND ActionProperty.evaluation != 0
          ) AS propertyEvaluation
FROM Event
INNER JOIN mes.MES ON mes.MES.id=Event.MES_id
INNER JOIN mes.MES_visit ON mes.MES_visit.master_id=mes.MES.id
INNER JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id=mes.MES.group_id
INNER JOIN Action ON Action.event_id=Event.id
INNER JOIN ActionType ON ActionType.id=Action.actionType_id
INNER JOIN rbService ON rbService.id=ActionType.nomenclativeService_id
WHERE Event.deleted=0
  AND Event.prevEvent_id IS NOT NULL
  %(orgStructure)s
  AND (Event.execDate IS NULL OR (DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s))
  %(mesDispans)s
  AND (mes.mrbMESGroup.code='ДиспанС')
  AND (Event.execDate IS NULL OR (mes.MES.endDate IS NULL OR mes.MES.endDate >= %(begDate)s))
  AND mes.MES_visit.deleted=0
  AND Action.deleted=0
  AND ActionType.deleted=0
  AND (     mes.MES_visit.serviceCode = SUBSTR(rbService.code,1, CHAR_LENGTH(mes.MES_visit.serviceCode))
        AND SUBSTR(rbService.code, CHAR_LENGTH(mes.MES_visit.serviceCode)+1,1) IN ('','.','*')
      )
ORDER BY Action.id, mes.MES_visit.additionalServiceCode;
''' % { 'orgStructure':orgStructure,
        'begDate': db.formatDate(begDate),
        'begDateMinusYear': db.formatDate(begDate.addYears(-1)),
        'endDate': db.formatDate(endDate),
        'mesDispans' : mesDispans,
      }
    return db.query(stmt)


class CReportForm131_o_3000_2016(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о втором этапе диспансеризации определенных групп взрослого населения (2016)')
        self.mapNumMesVisitCodeToRow = {55 : 0,
                                        44 : 1,
                                        56 : 2,
                                        50 : 3,
                                        45 : 4,
                                        46 : 4,
                                        58 : 5,
                                        53 : 6,
                                        90 : 7,
                                        48 : 8,
                                        54 : 9,
                                        91 : 10,
                                        92 : 11,
                                        47 : 12,
                                        52 : 13,
                                        59 : 14,
                                        17 : 15,
                                        51 : 15
                                      }
        self.rowNames = [
                          u'Дуплексное сканирование брахицефальных артерий',
                          u'Осмотр (консультация) врачом-неврологом',
                          u'Эзофагогастродуоденоскопия ',
                          u'Осмотр (консультация) врачом-хирургом или врачом-урологом',
                          u'Осмотр (консультация) врачом-хирургом или врачом-колопроктологом',
                          u'Колоноскопия или ректороманоскопия',
                          u'Определение липидного спектра крови',
                          u'Спирометрия',
                          u'Осмотр (консультация) врачом-акушером-гинекологом',
                          u'Определение концентрации гликированного гемоглобина в крови или тест на толерантность к глюкозе',
                          u'Осмотр (консультация) врачом-оториноларингологом',
                          u'Анализ крови на уровень содержания простатспецифического антигена',
                          u'Осмотр (консультация) врачом-офтальмологом',
                          u'Индивидуальное углубленное профилактическое консультирование',
                          u'Групповое профилактическое консультирование (школа пациента)',
                          u'Прием (осмотр) врача-терапевта',
                        ]


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMesDispansListVisible(True)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result


    def _getDefault(self):
        result = [ [0, 0, 0, 0, 0]
                   for row in self.rowNames
                 ]
        return result


    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0, 0]
        uniqueSet = set()
        while query.next():
            record = query.record()
#            eventId            = forceRef(record.value('eventId'))
            actionId           = forceRef(record.value('actionId'))
#            actionTypeName     = forceString(record.value('actionTypeName'))
            actionMkb          = forceString(record.value('actionMkb'))
#            serviceName        = forceString(record.value('serviceName'))
#            clientId           = forceRef(record.value('clientId'))
            numMesVisitCode    = forceInt(record.value('numMesVisitCode'))
#            needToPayAttention = forceInt(record.value('needToPayAttention'))
            actionExecNow      = forceInt(record.value('actionExecNow'))
            actionExecPrev     = forceInt(record.value('actionExecPrev'))
            propertyEvaluation = forceInt(record.value('propertyEvaluation'))
            endDate            = forceDate(record.value('endDate'))
            execDate           = forceDate(record.value('execDate'))
            status             = forceInt(record.value('status'))
            actionExecRefusal  = (not endDate) and (status == CActionStatus.refused)
            if numMesVisitCode not in self.mapNumMesVisitCodeToRow:
                continue
            key = actionId
            if key in uniqueSet:
                continue
            uniqueSet.add(key)
            row = self.mapNumMesVisitCodeToRow[numMesVisitCode]
            reportLine = reportData[row]
            if status != CActionStatus.canceled:#if needToPayAttention:
                reportLine[0] += 1
                reportDataTotal[0] += 1
            if execDate and endDate and status == CActionStatus.finished:#refused:
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
            ( '45%', [u'Медицинское мероприятие второго этапа диспансеризации', u'', u'1'], CReportBase.AlignLeft),
            ( '3%', [u'№ строки', u'', u'2'], CReportBase.AlignRight),
            ( '10%', [u'Выявлено показание к дополнительному обследованию', u'', u'3'], CReportBase.AlignRight),
            ( '10%', [u'Количество выполненных медицинских мероприятий', u'в рамках диспансе-ризации', u'4'], CReportBase.AlignRight),
            ( '10%', [u'', u'проведено ранее (в предшествую-щие 12 мес.)', u'5'], CReportBase.AlignRight),
            ( '10%', [u'Отказы', u'', u'6'], CReportBase.AlignRight),
            ( '10%', [u'Выявлено заболеваний', u'', u'7'], CReportBase.AlignRight)
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
        for row, name in enumerate(self.rowNames):
            reportLine = reportData[row]
            i = table.addRow()
            table.setText(i, 0, name)
            table.setText(i, 1, row+1)
            table.setText(i, 2, reportLine[0])
            table.setText(i, 3, reportLine[1])
            table.setText(i, 4, reportLine[2])
            table.setText(i, 5, reportLine[3])
            table.setText(i, 6, reportLine[4] if row not in (13, 14) else 'X')
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        table.setText(i, 2, total[0])
        table.setText(i, 3, total[1])
        table.setText(i, 4, total[2])
        table.setText(i, 5, total[3])
        table.setText(i, 6, total[4])
        return doc
