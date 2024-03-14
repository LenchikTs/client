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
    (u'Отделения-общежития', u'1'),
    (u'Групповые дома', u'2'),
    (u'Квартиры для независимого проживания', u'3')
]

class CForm36_2800(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2800')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        rowSize = 4
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Жилье с поддержкой для пациентов, больных психическими расстройствами')
        cursor.insertBlock()
        splitTitle(cursor, u'(2800)', u'Коды по ОКЕИ: единица - 642, человек - 792, место - 698', '60%')
        tableColumns = [
            ('15%', [u'Вид жилья', u'1'], CReportBase.AlignLeft),
            ('5%', [u'N строки', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Число учреждений, имеющих жилье для пациентов, больных психическими расстройствами', u'3'], CReportBase.AlignCenter),
            ('10%', [u'Число мест для проживания', u'4'], CReportBase.AlignCenter),
            ('10%', [u'Число пациентов, пользовавшихся жильем (проживавших) в течение отчетного года', u'5'], CReportBase.AlignCenter),
            ('10%', [u'из них число пациентов, проживающих на конец года', u'6'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                table.setText(i, 2 + col, reportLine[col])
        return doc