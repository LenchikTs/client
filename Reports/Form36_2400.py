# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui

from Reports.Form11 import CForm11SetupDialog
from Reports.Form36_2100_2190 import CForm36
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle

MainRows = [
    (u'Число пациентов, прекративших в течение года работу', u'1'),
    (u'\tиз них трудоустроено', u'2'),
    (u'Работает на конец года', u'3'),
    (u'Число мест в мастерских на конец года', u'4')
]

class CForm36_2400(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2400')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        rowSize = 2
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Лечебно-трудовые мастерские для пациентов, больных психическими расстройствами')
        cursor.insertBlock()
        splitTitle(cursor, u'(2400)', u'Код по ОКЕИ: человек - 792', '50%')
        tableColumns = [
            ('25%', [u'Наименование', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'N строки', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Для пациентов', u'стационарных', u'3'], CReportBase.AlignCenter),
            ('10%', [u'', u'амбулаторных', u'4'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                if rowDescr[1] == '2' and col == 0:
                    table.setText(i, 2 + col, 'X')
                else:
                    table.setText(i, 2 + col, reportLine[col])

        return doc