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
    db = QtGui.qApp.db
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
    stmt = u'''
SELECT DISTINCT
    Action.id AS actionId,
    Action.status,
    Action.endDate,
    Action.MKB AS actionMkb,
    age(Client.birthDate, Action.endDate) AS ageClient,
    mes.MES_visit.additionalServiceCode AS numMesVisitCode,
    DATE(Action.endDate) BETWEEN DATE(Event.setDate) AND DATE(Event.execDate) AS actionExecNow,
    DATE(Action.endDate) < DATE(Event.setDate) AS actionExecPrev,

    IF(rbService.code = 'А25.12.004*', (SELECT APT.descr
    FROM Action AS A
    INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
    INNER JOIN ActionProperty AS AP  ON (APT.id = AP.type_id AND AP.action_id = A.id)
    INNER JOIN ActionType AS AT      ON AT.id = A.actionType_id
    INNER JOIN rbService AS rbS      ON rbS.id = AT.nomenclativeService_id
    INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
    WHERE Action.id IS NOT NULL AND APT.deleted=0 AND A.id = Action.id AND A.deleted = 0
    AND AP.deleted=0
    AND AT.name = '(2016)Определение риска развития инсульта или инфаркта миокарда'
    AND APT.name LIKE '(18-39 лет) Относительный риск сердечно сосудистых за%%'
    AND APS.value IN ('Средний', 'Высокий', 'Очень высокий')
    AND APT.descr = '1' AND AP.action_id = Action.id
    ORDER BY APS.id DESC
    LIMIT 1), 0) AS propertyDescr1,

    IF(rbService.code = 'А25.12.004*', (SELECT APT.descr
    FROM Action AS A
    INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = A.actionType_id
    INNER JOIN ActionProperty AS AP  ON (APT.id = AP.type_id AND AP.action_id = A.id)
    INNER JOIN ActionType AS AT      ON AT.id = A.actionType_id
    INNER JOIN rbService AS rbS      ON rbS.id = AT.nomenclativeService_id
    INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
    WHERE Action.id IS NOT NULL AND APT.deleted=0 AND A.id = Action.id AND A.deleted = 0
    AND AP.deleted=0
    AND AT.name = '(2016)Определение риска развития инсульта или инфаркта миокарда'
    AND APT.name LIKE '(40-65 лет) Абсолютный риск сердечно-сосудистых за%%'
    AND APS.value IN ('Высокий', 'Очень высокий')
    AND APT.descr = '2' AND AP.action_id = Action.id
    ORDER BY APS.id DESC
    LIMIT 1), 0) AS propertyDescr2,

    EXISTS(SELECT ActionProperty.id
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
INNER JOIN Person ON Person.id=Action.person_id
INNER JOIN rbSpeciality ON rbSpeciality.id=Person.speciality_id
INNER JOIN mes.mrbSpeciality ON mes.mrbSpeciality.id=mes.MES_visit.speciality_id
INNER JOIN Client ON Client.id=Event.client_id

WHERE Event.deleted=0
  AND Event.prevEvent_id IS NULL
  %(orgStructure)s
  AND DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s
  %(mesDispans)s
  AND mes.mrbMESGroup.code='ДиспанС'
  AND (Event.execDate IS NULL OR (mes.MES.endDate IS NULL OR mes.MES.endDate >= %(begDate)s))
  AND mes.MES_visit.deleted = 0
  AND Action.deleted = 0
  AND ActionType.deleted = 0
  AND Client.deleted = 0
  AND ( mes.MES_visit.serviceCode = SUBSTR(rbService.code,1, CHAR_LENGTH(mes.MES_visit.serviceCode))
        AND SUBSTR(rbService.code, CHAR_LENGTH(mes.MES_visit.serviceCode)+1,1) IN ('','.','*')
      )
ORDER BY Action.id, mes.MES_visit.additionalServiceCode
''' % { 'orgStructure':orgStructure,
        'begDate': db.formatDate(begDate),
        'endDate': db.formatDate(endDate),
        'mesDispans' : mesDispans
      }
    return db.query(stmt)


class CReportForm131_o_2000_2016(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о первом этапе диспансеризации определенных групп взрослого населения (2016)')

        self.mapNumMesVisitCodeToRow = {
                    1:  0,
                    3:  1,
                    2:  2,
                    4:  3,
                    5:  4,
                    6:  5,
                    86: 6,
                    15: 7,
                    18: 8,
                    14: 9,
                    19:10,
                    8: 11,
                    9: 12,
                    11:13,
                    10:14,
                    12:15,
                    13:16,
                    87:16,
                    89:16,
                    88:17,
                    7: 18,
                    17:19,
                    51:19,
                    }

        self.rowNames = [
                     u'Опрос(анкетирование), направленный на выявление хронических неинфекционных заболеваний, факторов риска их развития, потребления наркотических средств и психотропных веществ без назначения врача',
                     u'Антропометрия (измерение роста стоя, массы тела, окружности талии), расчет индекса массы тела',
                     u'Измерение артериального давления',
                     u'Определение уровня общего холестерина в крови',
                     u'Определение уровня глюкозы в крови экспресс-методом',
                     u'Определение относительного суммарного сердечно-сосудистого риска',
                     u'Определение абсолютного суммарного сердечно-сосудистого риска',
                     u'Электрокардиография (в покое)',
                     u'Осмотр фельдшером (акушеркой), включая взятие мазка (соскоба) с поверхности шейки матки (наружного маточного зева) и цервикального канала на цитологическое исследование',
                     u'Флюорография легких',
                     u'Маммография обеих молочных желез',
                     u'Клинический анализ крови',
                     u'Клинический анализ крови развернутый',
                     u'Анализ крови биохимический общетерапевтический',
                     u'Общий анализ мочи',
                     u'Исследование кала на скрытую кровь иммунохимическим методом',
                     u'Ультразвуковое исследование (УЗИ) на предмет исключения новообразований органов брюшной полости, малого таза и аневризмы брюшной аорты',
                     u'Ультразвуковое исследование (УЗИ) в целях исключения аневризмы брюшной аорты',
                     u'Измерение внутриглазного давления',
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
        result = [ [0, 0, 0, 0] for row in self.rowNames
                 ]
        return result


    def getReportData(self, query):
        reportData = self._getDefault()
        reportDataTotal = [0, 0, 0, 0]
        uniqueSet = set()
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            actionMkb = forceString(record.value('actionMkb'))
            propertyDescr1 = forceString(record.value('propertyDescr1'))
            propertyDescr2 = forceString(record.value('propertyDescr2'))
            numMesVisitCode = forceInt(record.value('numMesVisitCode'))
            ageClient = forceInt(record.value('ageClient'))
            actionExecPrev = forceInt(record.value('actionExecPrev'))
            propertyEvaluation = forceInt(record.value('propertyEvaluation'))
            endDate = forceDate(record.value('endDate'))
            status = forceInt(record.value('status'))
            actionExecRefusal = (not endDate) and (status == CActionStatus.refused)
            if numMesVisitCode not in self.mapNumMesVisitCodeToRow:
                continue
            if actionId in uniqueSet:
                continue
            uniqueSet.add(actionId)
            targetRow = self.mapNumMesVisitCodeToRow.get(numMesVisitCode, None)
            if targetRow == 5 and ageClient >= 40:
                targetRow = 6
            if targetRow is not None:
                reportLine = reportData[targetRow]
                if endDate and status != CActionStatus.refused:
                    if endDate and status == CActionStatus.finished and not actionExecPrev:
                        reportLine[0] += 1
                        reportDataTotal[0] += 1
                    if actionExecPrev:
                        reportLine[1] += 1
                        reportDataTotal[1] += 1
                    if targetRow ==5 and propertyDescr1:
                        reportLine[3] += 1
                        reportDataTotal[3] += 1
                    elif targetRow ==6 and propertyDescr2:
                        reportLine[3] += 1
                        reportDataTotal[3] += 1
                    elif targetRow not in [5, 6]:
                        if ((actionMkb and 'A00'<=actionMkb<'U') or propertyEvaluation) and targetRow not in [5, 6]:
                            reportLine[3] += 1
                            reportDataTotal[3] += 1
                if actionExecRefusal:
                    reportLine[2] += 1
                    reportDataTotal[2] += 1
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
            ( '45%', [u'', u'Осмотр, исследование, иное медицинское мероприятие первого этапа диспансеризации', u'1'], CReportBase.AlignLeft),
            ( '3%',  [u'', u'№ строки', u'2'], CReportBase.AlignRight),
            ( '15%', [u'Медицинское мероприятие', u'проведено', u'3'], CReportBase.AlignRight),
            ( '15%', [u'', u'учтено, выполненных ранее (в предшествующие 12 мес.)', u'4'], CReportBase.AlignRight),
            ( '15%', [u'', u'отказы', u'5'], CReportBase.AlignRight),
            ( '15%', [u'Выявлены патологические отклонения', u'', u'6'], CReportBase.AlignRight),
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

        for row, name in enumerate(self.rowNames):
            reportLine = reportData[row]
            i = table.addRow()
            table.setText(i, 0, name)
            table.setText(i, 1, row+1)
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

