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

from library.database   import addDateInRange
from library.Utils      import calcAgeInYears, forceDate, forceInt, forceString

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.StatReport1NPUtil  import ageSexRows, dispatchAgeSex, havePermanentAttach


def selectData(begDate, endDate,  eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate):
    stmt="""
        SELECT
            Event.execDate as date,
            Client.birthDate as birthDate,
            Client.sex as sex,
            rbHealthGroup.code as `group`
        FROM
            Event
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN Diagnostic    ON (     Diagnostic.event_id = Event.id
                                         AND Diagnostic.diagnosisType_id = (SELECT id FROM rbDiagnosisType WHERE code = '1')
                                       )
            LEFT JOIN rbHealthGroup ON rbHealthGroup.id = Diagnostic.healthGroup_id
            LEFT JOIN Account_Item ON ( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL)
                                      )
        WHERE
            Event.deleted=0 AND Diagnostic.deleted=0 AND %s
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


class CStatReport1NP3000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(True)
        self.setTitle(u'Итоги дополнительной диспансеризации граждан (3000)', u'Итоги дополнительной диспансеризации')


    def getSetupDialog(self, parent):
        result = CReport.getSetupDialog(self, parent)
        result.resize(0,0)
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventTypeId = params.get('eventTypeId', None)
        onlyPermanentAttach =  params.get('onlyPermanentAttach', False)
        onlyPayedEvents = params.get('onlyPayedEvents', False)
        begPayDate = params.get('begPayDate', QDate())
        endPayDate = params.get('endPayDate', QDate())

        reportRowSize = 5
        reportData = [ [0] * reportRowSize for row in ageSexRows ]
        query = selectData(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate)

        while query.next():
            record = query.record()
            age    = calcAgeInYears(forceDate(record.value('birthDate')), forceDate(record.value('date')))
            sex    = forceInt(record.value('sex'))
            group  = forceString(record.value('group'))

            if group == '1':
                column = 0
            elif group == '2':
                column = 1
            elif group == '3':
                column = 2
            elif group == '4':
                column = 3
            elif group == '5':
                column = 4
            else:
                column = -1

            if column >= 0:
                for row in dispatchAgeSex(age, sex):
                    reportData[row][column] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Итоги дополнительной диспансеризации граждан')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertText(u'(3000)')
        cursor.insertBlock()

        tableColumns = [
            ('30%', [u'Возрастной диапазон работающих граждан, прошедших диспансеризацию', u'', u'1'], CReportBase.AlignLeft),
            ('10%', [u'№ строки', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Распределение прошедших дополнительную диспансеризацию граждан по группам состояния здоровья', u'I гр.', u'3'], CReportBase.AlignRight),
            ('10%', [u'', u'II гр.',   u'4'], CReportBase.AlignRight),
            ('10%', [u'', u'III гр.',  u'5'], CReportBase.AlignRight),
            ('10%', [u'', u'IV гр.',   u'6'], CReportBase.AlignRight),
            ('10%', [u'', u'V гр.',    u'7'], CReportBase.AlignRight),
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 5)

        for iRow, row in enumerate(ageSexRows):
            i = table.addRow()
            for j in xrange(2):
                table.setText(i, j, row[j])
            for j in xrange(5):
                table.setText(i, 2+j, reportData[iRow][j])

        return doc
