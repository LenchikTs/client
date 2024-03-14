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
from PyQt4.QtCore import Qt

from Reports.Form37 import CForm37
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils import splitTitle

# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психотические расстройства, связанные с употреблением алкоголя (алкогольные психозы)', u'F10.03, F10.07, F10.4 - F10.6, F10.73, 75, 81, 91', u'', u'01'),
    (0, u'Синдром зависимости от алкоголя (алкоголизм)', u'F10.2, 3, F10.70 - 72, 74, 82, 92, 99', u'', u'02'),
    (1, u'из них со стадиями:\nначальная (I)', u'F10.2х1', u'', u'03'),
    (1, u'средняя (II)', u'F10.2х2', u'', u'04'),
    (1, u'конечная (III)', u'F10.2х3', u'', u'05'),
    (0, u'Психотические расстройства вследствие употребления:\n\tнаркотиков', u'F1x.03H, F1x.4-6H, F1x.7-9H (часть)', u'', u'06'),
    (0, u'\tненаркотических ПАВ', u'F1x.03T, F1x.4T - F1x.6T, F1x.7-9T (часть)', u'', u'073'),
    (0, u'Синдром зависимости от наркотиков (наркомания)', u'F1x.2, 3, 7-9H (часть)', u'', u'08'),
    (1, u'в том числе вследствие употребления:\nопиоидов', u'F11.2, 3, 7-9 (часть)', u'', u'09'),
    (1, u'каннабиноидов', u'F12.2, 3, 7-9 (часть)', u'', u'10'),
    (1, u'кокаина', u'F14.2, 3, 7-9 (часть)', u'', u'11'),
    (1, u'других психостимуляторов', u'F15.2, 3, 7-9Н (часть)', u'', u'12'),
    (1, u'других наркотических веществ и их сочетаний (полинаркомания)', u'F16.2, 3, 7-9H F18.2, 3, 7-9H F19.2, 3, 7-9H (часть)', u'', u'13'),
    (0, u'Синдром зависимости от ненаркотических ПАВ (токсикомания)', u'F1х.2, 3, 7-9Т (часть)', u'', u'14'),
    (0, u'Острая интоксикация и употребление с вредными последствиями:\nалкоголя', u'F10.0 (часть) F10.1', u'', u'15'),
    (0, u'наркотиков', u'F1x.0H (часть) F1x.1H', u'', u'16'),
    (0, u'ненаркотических ПАВ', u'F1x.0Т (часть) F1x.1Т', u'', u'17'),
    (0, u'ИТОГО', u'F10 - F19', u'', u'18'),
    (0, u'Из общего числа (стр. 18) - женщин с психическими и поведенческими расстройствами, связанными с употреблением:\n\tалкоголя (из стр. 01, 02, 15)', u'', u'', u'19'),
    (0, u'\tнаркотиков (из стр. 06, 08, 16)', u'', u'', u'20'),
    (0, u'\tненаркотических ПАВ (из стр. 07, 14, 17)', u'', u'', u'21'),
    (0, u'Кроме того, признанные психически здоровыми и с заболеваниями, не вошедшими в стр. 18', u'', u'', u'22'),
    (0, u'Из общего числа потребителей наркотиков (стр. 06, 08, 16) - употребляют наркотики инъекционным способом', u'', u'', u'23')
]

# наименование | диагнозы | № строки
CompRows2301 = [
    (u'Психические и поведенческие расстройства, связанные с употреблением:\n\tалкоголя  (из стр. 01, 02, 15 табл. 2300)', u'', u'01'),
    (u'\tнаркотических веществ (из стр. 06, 08, 16 табл. 2300)', u'', u'02'),
    (u'из них: употребляют наркотики инъекционным способом (из стр. 23 табл. 2300)', u'', u'03'),
    (u'ненаркотических ПАВ (из стр. 07, 14, 17 табл. 2300)', u'', u'04'),
    (u'ИТОГО', u'', u'05'),
]

class CForm37_2300_2330(CForm37):
    def __init__(self, parent):
        CForm37.__init__(self, parent)
        self.setTitle(u'Форма N 37 таблицы 2300-2330')

    def getSetupDialog(self, parent):
        result = CForm37.getSetupDialog(self, parent)
        result.setAddressTypeVisible(False)
        return result


    def build(self, params):
        rowSize = 10
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'III. Состав пациентов наркологического стационара')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2300)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('12%', [u'Наименование болезней', u'', u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ 10', u'', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'В отчетном году', u'поступило больных', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'из них:', u'сельских жителей', u'5'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'', u'детей', u'6'], CReportBase.AlignRight),
            ('6%', [u'', u'', u'', u'подростков', u'7'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'впервые в данном году', u'', u'8'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'из них впервые в жизни', u'', u'9'], CReportBase.AlignRight),
            ('7%', [u'', u'выбыло больных', u'всего', u'', u'10'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'из них - в связи со смертью', u'', u'11'], CReportBase.AlignRight),
            ('7%', [u'', u'число койко-дней, проведенных в стационаре выписанными и умершими', u'', u'', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'осталось на конец года', u'', u'', u'13'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 4, 1)
        table.mergeCells(0, 3, 1, 10)
        table.mergeCells(1, 3, 1, 6)
        table.mergeCells(2, 3, 2, 1)
        table.mergeCells(2, 4, 1, 3)
        table.mergeCells(2, 7, 2, 1)
        table.mergeCells(2, 8, 2, 1)
        table.mergeCells(1, 9, 1, 2)
        table.mergeCells(2, 9, 2, 1)
        table.mergeCells(2, 10, 2, 1)
        table.mergeCells(1, 11, 3, 1)
        table.mergeCells(1, 12, 3, 1)

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setAlignment(Qt.AlignLeft)
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # 2301
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Обследование пациентов, поступивших в стационар, на ВИЧ и другие гемоконтактные инфекции')
        splitTitle(cursor, u'(2301)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('17%', [u'Наименование', u'', u'1'], CReportBase.AlignLeft),
            ('3%', [u'№ стр.', u'', u'2'], CReportBase.AlignCenter),
            ('17%', [u'Из общего числа поступивших (из гр. 4 табл. 2300):', u'обследовано на ВИЧ - всего', u'3'], CReportBase.AlignCenter),
            ('17%', [u'', u'из них (гр. 3) выявлено ВИЧ-позитивных', u'4'], CReportBase.AlignCenter),
            ('16%', [u'', u'обследовано на гепатит C', u'5'], CReportBase.AlignCenter),
            ('16%', [u'', u'из них (гр. 5) выявлено позитивных', u'6'], CReportBase.AlignCenter),
            ('16%', [u'', u'обследовано на гепатит B', u'7'], CReportBase.AlignCenter),
            ('16%', [u'', u'из них (гр. 7) выявлено позитивных', u'8'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 6)
        rowSize = 6
        reportMainData = [[0] * rowSize for row in xrange(len(CompRows2301))]
        for row, rowDescr in enumerate(CompRows2301):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 2 + col, reportLine[col])

        return doc