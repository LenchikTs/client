# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import *

from Reports.Report            import *
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog

from Events.TeethEventInfo     import CTeethEventInfo

from library.Utils             import *
from library.PrintInfo         import CInfoContext


def selectData(params):
    begDate = params.get('begDate', None)
    endDate = params.get('endDate', None)

    db = QtGui.qApp.db

    tableAction = db.table('Action')
    tableActionType = db.table('ActionType')
    tableEvent = db.table('Event')

    queryTable = tableAction
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))

    cond = [tableAction['deleted'].eq(0),
            tableActionType['deleted'].eq(0),
            tableActionType['flatCode'].like('dentitionInspection%'),
            tableEvent['deleted'].eq(0),
            tableEvent['execDate'].dateGe(begDate),
            tableEvent['execDate'].dateLe(endDate)]

    fields = [tableEvent['id'].name()]

    stmt = db.selectDistinctStmt(queryTable, fields, cond)

#    print stmt

    return db.query(stmt)


class CReportF30_2700(CReport):
    def __init__(self, parent, additionalFields = False):
        CReport.__init__(self, parent)
        self.setTitle(u'Работа стоматологического (зубоврачебного) кабинета')
        self.additionalFields = additionalFields


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        return result


    def getReportData(self, query):
        result = [
                  [u'Всего', '1'] + [0]*15,
                  [u'из них:\n    дети до 14 лет (включительно)', '2'] + [0]*15,
                  [u'    дети 15-17 лет (включительно)', '3'] + [0]*15,
                  [u'    взрослые', '4'] + [0]*15
                 ]

        context = CInfoContext()

        while query.next():
            eventId = forceRef(query.value(0))
            event = context.getInstance(CTeethEventInfo, eventId)
            action = event.stomatAction
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ( '10%', [u'Контингенты',                                          u'',        u'1'],  CReportBase.AlignLeft),
            ( '5%',  [u'№ строки',                                             u'',        u'2'],  CReportBase.AlignRight),
            ( '5%',  [u'Число посещений стоматологов и зубных врачей',         u'всего',   u'3'],  CReportBase.AlignRight),
            ( '5%',  [u'', u'в том числе первичных *)',                                    u'4'],  CReportBase.AlignRight),
            ( '5%',  [u'Вылечено зубов',                                       u'',        u'5'],  CReportBase.AlignRight),
            ( '6%',  [u'из них постоянных',                                    u'',        u'6'],  CReportBase.AlignRight),
            ( '5%',  [u'по поводу осложнен-ного кариеса (из гр.5)',            u'',        u'7'],  CReportBase.AlignRight),
            ( '5%',  [u'Удалено зубов',                                        u'',        u'8'],  CReportBase.AlignRight),
            ( '6%',  [u'из них постоянных',                                    u'',        u'9'],  CReportBase.AlignRight),
            ( '6%',  [u'Всего санировано',                                     u'',        u'10'], CReportBase.AlignRight),
            ( '5%',  [u'Профилактическая работа', u'осмотрено в порядке плановой санации', u'11'], CReportBase.AlignRight),
            ( '5%',  [u'', u'из числа осмотренных нуждались в санации',                    u'12'], CReportBase.AlignRight),
            ( '5%',  [u'', u'санировано из числа нуждавшихся в санации',                   u'13'], CReportBase.AlignRight),
            ( '7%',  [u'Проведен курс профилактики',                           u'',        u'14'], CReportBase.AlignRight),
            ( '7%',  [u'Из общего числа (гр. 3) – посещений по ОМС',           u'',        u'15'], CReportBase.AlignRight),
            ( '5%',  [u'Выполнен объем работы в УЕТ(тыс.) (из гр.3)',          u'',        u'16'], CReportBase.AlignRight),
            ( '5%',  [u'Выполнен объем работы в УЕТ (тыс.) по ОМС (из гр.15)', u'',        u'17'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0,  2, 1)
        table.mergeCells(0, 1,  2, 1)
        table.mergeCells(0, 2,  1, 2)
        table.mergeCells(0, 4,  2, 1)
        table.mergeCells(0, 5,  2, 1)
        table.mergeCells(0, 6,  2, 1)
        table.mergeCells(0, 7,  2, 1)
        table.mergeCells(0, 8,  2, 1)
        table.mergeCells(0, 9,  2, 1)
        table.mergeCells(0, 10, 1, 3)
        table.mergeCells(0, 13,  2, 1)
        table.mergeCells(0, 14,  2, 1)
        table.mergeCells(0, 15,  2, 1)
        table.mergeCells(0, 16,  2, 1)

        query = selectData(params)
        reportData = self.getReportData(query)
        for rowDataList in reportData:
            row = table.addRow()
            for idx, value in enumerate(rowDataList):
                table.setText(row, idx, value)

        return doc
