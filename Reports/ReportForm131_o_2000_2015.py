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
    Action.status,
    Action.endDate,
    Action.MKB AS actionMkb,
    rbService.infis AS serviceCode,
    DATE(Action.endDate) BETWEEN DATE(Event.setDate) AND DATE(Event.execDate) AS actionExecNow,
    DATE(Action.endDate) BETWEEN DATE_ADD(DATE(Event.setDate), interval -1 YEAR)
        AND DATE(Event.setDate) AS actionExecPrev,

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
left join Action ON Action.event_id = Event.id
left join ActionType ON ActionType.id = Action.actionType_id
left join rbService ON rbService.id = ActionType.nomenclativeService_id
WHERE Event.deleted = 0
  %(orgStructure)s
  AND Event.prevEvent_id IS NULL
  AND DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s
  AND rbEventProfile.regionalCode = '8008'
  AND Action.deleted = 0
  AND ActionType.deleted = 0
''' % { 'orgStructure':orgStructure,
        'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate)
               }
    return db.query(stmt)


class CReportForm131_o_2000_2015(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о первом этапе диспансеризации определенных групп взрослого населения')

        self.mapServiceCodeToRowNum = {
            'A01.30.009': [0],
            'B03.069.003': [1],
            'A02.12.002': [2],
            'A09.05.026.005': [3],
            'A09.05.026.006': [3, 4],
            'A09.05.023.002': [4],
            'A09.05.023.007': [4],
            'B04.015.008': [5],
            'B04.015.007': [6],
            'A05.10.002.003': [7],
            'B04.001.009': [8],
            'A06.09.006': [9],
            'A06.09.006.001': [9],
            'A06.20.004': [10],
            'B03.016.002': [11],
            'B03.016.003': [12],
            'B03.016.004': [13],
            'B03.016.006': [14],
            'A09.19.001': [15],
            'A09.19.001.001': [15],
            'A04.15.001': [16],
            'A04.28.002.001': [17],
            'A04.21.01': [18],
            'A04.20.001': [19],
            'A04.12.003': [20],
            'A12.26.005': [21],
            'A12.26.019': [21]
            }

        stmt = u"select distinct infis from rbService where substr(infis, 1, 7) in ('B04.047', 'B04.026')"
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            record = query.record()
            self.mapServiceCodeToRowNum[forceString(record.value('infis'))] = [22]

        self.rowNames = {
            '01': u'Опрос(анкетирование), направленный на выявление хронических неинфекционных заболеваний, факторов риска их развития, потребления наркотических средств и психотропных веществ без назначения врача',
            '02': u'Антропометрия (измерение роста стоя, массы тела, окружности талии), расчет индекса массы тела',
            '03': u'Измерение артериального давления',
            '04': u'Определение уровня общего холестерина в крови',
            '05': u'Определение уровня глюкозы в крови экспресс-методом',
            '06': u'Определение относительного суммарного сердечно-сосудистого риска',
            '07': u'Определение абсолютного суммарного сердечно-сосудистого риска',
            '08': u'Электрокардиография (в покое)',
            '09': u'Осмотр фельдшером (акушеркой), включая взятие мазка (соскоба) с поверхности шейки матки (наружного маточного зева) и цервикального канала на цитологическое исследование',
            '10': u'Флюорография легких',
            '11': u'Маммография обеих молочных желез',
            '12': u'Клинический анализ крови',
            '13': u'Клинический анализ крови развернутый',
            '14': u'Анализ крови биохимический общетерапевтический',
            '15': u'Общий анализ мочи',
            '16':  u'Исследование кала на скрытую кровь иммунохимическим методом',
            '17.1': u'Ультразвуковое исследование поджелудочной железы',
            '17.2': u'Ультразвуковое исследование почек',
            '17.3': u'Ультразвуковое исследование простаты',
            '17.4': u'Ультразвуковое исследование матки и придатков',
            '18': u'Ультразвуковое исследование в целях исключения аневризмы брюшной аорты',
            '19': u'Измерение внутриглазного давления',
            '20': u'Прием (осмотр) врача-терапевта',
            }

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result

    def _getDefault(self):
        result = [[0, 0, 0, 0] for row in self.rowNames]
        return result

    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0]
        uniqueSet = set()
        while query.next():
            record = query.record()
            actionMkb = forceString(record.value('actionMkb'))
            numMesVisitCode = forceInt(record.value('numMesVisitCode'))
            serviceCode = forceString(record.value('serviceCode'))
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
                if endDate and status != 3:
                    if actionExecNow:
                        reportLine[0] += 1
                        reportDataTotal[0] += 1
                    elif actionExecPrev:
                        reportLine[1] += 1
                        reportDataTotal[1] += 1
                if actionExecRefusal:
                    reportLine[2] += 1
                    reportDataTotal[2] += 1
                if (actionMkb and 'A00' <= actionMkb < 'U') or propertyEvaluation:
                    reportLine[3] += 1
                    reportDataTotal[3] += 1
        return reportData, reportDataTotal

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(2000)')
        cursor.insertBlock()
        tableColumns = [
            ('45%', [u'', u'Осмотр, исследование, иное медицинское мероприятие первого этапа диспансеризации',
                     u'1'], CReportBase.AlignLeft),
            ('3%',  [u'', u'№ строки', u'2'], CReportBase.AlignRight),
            ('15%', [u'Медицинское мероприятие', u'проведено', u'3'], CReportBase.AlignRight),
            ('15%', [u'', u'учтено, выполненных ранее (в предшествующие 12 мес.)', u'4'], CReportBase.AlignRight),
            ('15%', [u'', u'отказы', u'5'], CReportBase.AlignRight),
            ('15%', [u'Выявлены патологические отклонения', u'', u'6'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 2, 1)
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
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        table.setText(i, 2, total[0])
        table.setText(i, 3, total[1])
        table.setText(i, 4, total[2])
        table.setText(i, 5, total[3])
        return doc
