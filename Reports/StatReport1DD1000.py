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

from Reports.Utils import _getChiefName
from library.database   import addDateInRange
from library.Utils      import forceInt, forceString

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.StatReport1NPUtil  import havePermanentAttach


def selectData(begDate, endDate,  eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate):
    stmt="""
        SELECT
            rbHealthGroup.code as `group`,
            COUNT(Event.id) as cnt,
            SUM(EXISTS(SELECT Visit.scene_id FROM Visit INNER JOIN rbScene ON rbScene.id = Visit.scene_id
            WHERE Visit.event_id = Event.id AND rbScene.code = 4 AND Visit.deleted = 0
            LIMIT 1)) AS departure
        FROM
            Event
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN Diagnostic AS D5 ON (     D5.event_id = Event.id
                                          AND D5.diagnosisType_id = (SELECT id FROM rbDiagnosisType WHERE code = '1')
                                          AND D5.deleted = 0
                                        )
            LEFT JOIN rbHealthGroup  ON rbHealthGroup.id  = D5.healthGroup_id
            LEFT JOIN Account_Item ON ( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL)
                                      )
        WHERE
            Event.deleted=0 AND %s
        GROUP BY
            `group`
    """
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    cond = []
    addDateInRange(cond, tableEvent['execDate'], begDate, endDate)
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if onlyPayedEvents:
        cond.append('isEventPayed(Event.id)')
        tableAccountItem = db.table('Account_Item')
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
    return db.query(stmt % (db.joinAnd(cond)))


class CStatReport1DD1000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(True)
        self.setTitle(u'Итоги дополнительной диспансеризации граждан (1000)', u'Итоги дополнительной диспансеризации')


    def getSetupDialog(self, parent):
        result = CReport.getSetupDialog(self, parent)
        result.resize(0,0)
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Итоги дополнительной диспансеризации граждан')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        self.buildInt(params, cursor)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText('\n\n\n')
        cursor.insertBlock()
        rows = []
        orgId = QtGui.qApp.currentOrgId()
        chief = _getChiefName(orgId)
        text0 = u'Руководитель ЛПУ                                   %s'%(chief)
        rows.append([text0])
        rows.append([u'\n'])
        rows.append([u'_____________________________'])
        rows.append([u'                    (подпись)'])
        rows.append([u'\n                                                                                       М.П.\n'])
        rows.append([u'"_____"________________201__г.'])
        columnDescrs = [('100%', [], CReportBase.AlignLeft)]
        table1 = createTable (
            cursor, columnDescrs, headerRowCount=len(rows), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(rows):
            table1.setText(i, 0, row[0])
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        return doc


    def buildInt(self, params, cursor):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventTypeId = params.get('eventTypeId', None)
        onlyPermanentAttach =  params.get('onlyPermanentAttach', False)
        onlyPayedEvents = params.get('onlyPayedEvents', False)
        begPayDate = params.get('begPayDate', QDate())
        endPayDate = params.get('endPayDate', QDate())

        reportRowSize = 7
        reportData = [0] * reportRowSize
        query = selectData(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate)

        while query.next():
            record = query.record()
            group  = forceString(record.value('group'))
            cnt = forceInt(record.value('cnt'))
            departure = forceInt(record.value('departure'))
            reportData[0] += cnt
            reportData[1] += departure
            if group in ('1', '2', '3', '4', '5'):
                reportData[int(group)+1] += cnt

        # now text
        cursor.insertText(u'(1000)')
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Численность работающих граждан, прошедших дополнительную диспансеризацию (законченные случаи), чел.', u'Всего', u'1'], CReportBase.AlignRight),
            ('15%', [u'', u'в том числе осмотренные специалистами выездных бригад', u'2'], CReportBase.AlignRight),
            ('15%', [u'Распределение прошедших дополнительную диспансеризацию граждан по группам состояния здоровья', u'I гр. - практически здоровые', u'3'], CReportBase.AlignRight),
            ('15%', [u'', u'II гр. - риск развития заболевания', u'4'], CReportBase.AlignRight),
            ('15%', [u'', u'III гр. - нуждаются в доп.обследовании, лечении в амбулаторно-поликлинических условиях',  u'5'], CReportBase.AlignRight),
            ('15%', [u'', u'IV гр. - нуждаются в доп.обследовании, лечении стационарах субъекта РФ', u'6'], CReportBase.AlignRight),
            ('15%', [u'', u'V гр. - нуждаются в ВМП',  u'7'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns, headerRowCount=1, border=3, cellPadding=2, cellSpacing=0)
        table.mergeCells(0, 0, 1, 2)
        table.mergeCells(0, 2, 1, 5)

        tableRow = table.addRow()
        for i in xrange(reportRowSize):
            table.setText(tableRow, i, reportData[i])

        return reportData
