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
    (u'Реабилитационное отделение стационара', u'4'),
    (u'Клиника 1-го психиатрического эпизода', u'5'),
    (u'ЛТМ (ЛПМ)', u'6')
]

class CForm36_2900(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2900')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        rowSize = 2
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Организации, имеющие полустационары и реабилитационные подразделения для пациентов, больных психическими расстройствами')
        cursor.insertBlock()
        splitTitle(cursor, u'(2900)', u'Код по ОКЕИ: единица - 642', '60%')
        tableColumns = [
            ('30%', [u'Виды подразделений', u'1'], CReportBase.AlignLeft),
            ('10%', [u'N строки', u'2'], CReportBase.AlignCenter),
            ('10%', [u'ПНД (диспансерные отделения и кабинеты)', u'3'], CReportBase.AlignCenter),
            ('10%', [u'ПБ и другие стационары', u'4'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                if rowDescr[1] == '4' and col in [0]:
                    table.setText(i, 2 + col, 'X')
                else:
                    table.setText(i, 2 + col, reportLine[col])
        return doc