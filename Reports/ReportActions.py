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

from library.database          import addDateInRange
from library.Utils             import forceDouble, forceInt, forceString
from Events.Utils              import getActionTypeDescendants
from Reports.Report            import CReport
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportView        import CPageFormat
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.StatReport1NPUtil import havePermanentAttach


def selectData(begDate, endDate, eventTypeId, sex, ageFrom, ageTo, actionTypeClass, actionTypeId, onlyPermanentAttach, MKBFilter, MKBFrom, MKBTo, onlyPayedEvents, begPayDate, endPayDate):
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tableClient = db.table('Client')
    tableActionType = db.table('ActionType')
    cond = []
    if begDate:
        cond.append(db.joinOr([
            tableEvent['execDate'].ge(begDate), tableEvent['execDate'].isNull()]))
    if endDate:
        cond.append(tableEvent['setDate'].le(endDate))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Event.execDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if actionTypeId:
        cond.append(tableActionType['id'].inlist(getActionTypeDescendants(actionTypeId, actionTypeClass)))
    elif actionTypeClass is not None:
        cond.append(tableActionType['class'].eq(actionTypeClass))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if MKBFilter:
        tableDiagnostic = db.table('Diagnostic')
        tableDiagnosis = db.table('Diagnosis')
        subQueryTable = tableDiagnosis.leftJoin(tableDiagnostic, tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        subCond = [ tableDiagnostic['event_id'].eq(tableEvent['id']),
                    tableDiagnosis['MKB'].between(MKBFrom, MKBTo)
                  ]
        cond.append(db.existsStmt(subQueryTable, subCond))
    if onlyPayedEvents:
        cond.append('isEventPayed(Event.id)')
        tableAccountItem = db.table('Account_Item')
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
        AIJoin = '''LEFT  JOIN Account_Item      ON ( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL)
                                    )'''
    else:
        AIJoin = ''
    condStr = db.joinAnd(cond)
    stmt = """
SELECT
    SUM(Action.amount) AS amount,
    SUM(IF(Event.execDate IS NULL,0, Action.amount)) AS done,
    COUNT(*) AS cnt,
    ActionType.name
FROM
    Action
    LEFT JOIN Event on Action.event_id=Event.id
    LEFT JOIN Client on Client.id=Event.client_id
    LEFT JOIN ActionType on ActionType.id=Action.actionType_id
    %s
WHERE Action.deleted=0 AND Event.deleted=0 AND %s
GROUP BY ActionType.class, ActionType.group_id, ActionType.id
    """ % (AIJoin, condStr)
#    print stmt
    return db.query(stmt)


class CReportActions(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет об обслуживании')
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setPayPeriodVisible(True)
        result.setWorkOrganisationVisible(True)
        result.setSexVisible(True)
        result.setAgeVisible(True)
        result.setActionTypeVisible(True)
        result.setMKBFilterVisible(True)
        result.setTitle(self.title())
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventTypeId = params.get('eventTypeId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        actionTypeClass = params.get('actionTypeClass', None)
        actionTypeId = params.get('actionTypeId', None)
        onlyPermanentAttach = params.get('onlyPermanentAttach', None)
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom   = params.get('MKBFrom', '')
        MKBTo     = params.get('MKBTo', '')
        onlyPayedEvents = params.get('onlyPayedEvents', False)
        begPayDate = params.get('begPayDate', QDate())
        endPayDate = params.get('endPayDate', QDate())

        query = selectData(begDate, endDate, eventTypeId, sex, ageFrom, ageTo, actionTypeClass, actionTypeId, onlyPermanentAttach, MKBFilter, MKBFrom, MKBTo, onlyPayedEvents, begPayDate, endPayDate)

#        db = QtGui.qApp.db
        reportData = []
        resultTotal = [0, 0, 0]
        while query.next():
            record = query.record()
            name = forceString(record.value('name'))
            amount = forceDouble(record.value('amount'))
            done = forceDouble(record.value('done'))
            cnt = forceInt(record.value('cnt'))
            reportData.append([name, cnt, amount, done])
            resultTotal[0] += cnt
            resultTotal[1] += amount
            resultTotal[2] += done

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ( '6%', [u'№ п/п'], CReportBase.AlignRight),
            ( '30%', [u'Наименование'], CReportBase.AlignLeft),
            ( '10%', [u'Случаев'], CReportBase.AlignRight),
            ( '20%', [u'Назначено'], CReportBase.AlignRight),
            ( '20%', [u'Выполнено'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)

        for row in reportData:
            i = table.addRow()
            table.setText(i, 0, i)
            for j in xrange(len(row)):
                table.setText(i, j+1, row[j])
        i = table.addRow()
        table.setText(i, 0, u'Итого', blockFormat=CReportBase.AlignLeft)
        table.mergeCells(i, 0, 1, 2)
        for j, val in enumerate(resultTotal):
            table.setText(i, j+2, val)
        return doc
