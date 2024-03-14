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
    (u'Дневной стационар', u'1'),
    (u'Ночной стационар', u'2'),
    (u'Стационар на дому', u'3'),
    (u'Реабилитационное отделение психиатрического стационара', u'4')
]

class CForm36_2600(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2600')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        rowSize = 9
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Полустационарные и стационарные подразделения для пациентов, больных психическими расстройствами')
        cursor.insertBlock()
        splitTitle(cursor, u'(2600)', u'Коды по ОКЕИ: единица - 642, человек - 792, место - 698', '95%')
        tableColumns = [
            ('10%', [u'Виды подразделений', u'', u'1'], CReportBase.AlignLeft),
            ('5%', [u'N строки', u'', u'2'], CReportBase.AlignCenter),
            ('5%', [u'Число мест (коек)', u'по смете', u'3'], CReportBase.AlignCenter),
            ('5%', [u'', u'среднегодовых', u'4'], CReportBase.AlignCenter),
            ('10%', [u'Выписано пациентов', u'', u'5'], CReportBase.AlignCenter),
            ('10%', [u'Состоит пациентов на конец года', u'', u'6'], CReportBase.AlignCenter),
            ('10%', [u'Число дней, проведенных в стационаре', u'', u'7'], CReportBase.AlignCenter),
            ('10%', [u'По закрытым листкам нетрудоспособности:', u'число случаев', u'8'], CReportBase.AlignCenter),
            ('10%', [u'', u'число дней', u'9'], CReportBase.AlignCenter),
            ('10%', [u'из них у пациентов с заболеваниями, связанными с употреблением ПАВ', u'число случаев (из гр. 8)', u'10'], CReportBase.AlignCenter),
            ('10%', [u'', u'число дней (из гр. 9)', u'11'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        table.mergeCells(0, 4, 2, 1)
        table.mergeCells(0, 5, 2, 1)
        table.mergeCells(0, 6, 2, 1)
        table.mergeCells(0, 7, 1, 2)
        table.mergeCells(0, 9, 1, 2)
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                if rowDescr[1] == '3' and col in [1] or rowDescr[1] == '4' and col in [1, 5, 6, 7, 8]:
                    table.setText(i, 2 + col, 'X')
                else:
                    table.setText(i, 2 + col, reportLine[col])
        return doc