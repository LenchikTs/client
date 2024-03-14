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
    (u'Психиатры, работающие по участковому принципу: для взрослых', u'1'),
    (u'для подростков', u'2'),
    (u'детские', u'3'),
    (u'Психотерапевты', u'4')
]

MainRows2210 = [
    (u'В ПНД (диспансерных отделениях, кабинетах):', u''),
    (u'медицинские психологи', u'1'),
    (u'специалисты по социальной работе', u'2'),
    (u'социальные работники', u'3'),
    ( u'В стационарах:', u''),
    (u'медицинские психологи', u'4'),
    (u'специалисты по социальной работе', u'5'),
    (u'социальные работники', u'6')
]

class CForm36_2200_2210(CForm36):
    def __init__(self, parent):
        CForm36.__init__(self, parent)
        self.setTitle(u'Форма №36 2200-2210')

    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        result.setAddressTypeVisible(False)
        return result

    def build(self, params):
        rowSize = 5
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число занятых должностей психиатров и психотерапевтов, осуществляющих диспансерное наблюдение и консультативно-лечебную помощь')
        splitTitle(cursor, u'(2200)', u'Код по ОКЕИ: единица - 642', '90%')
        tableColumns = [
            ('28%', [u'Наименование', u'1'], CReportBase.AlignLeft),
            ('10%', [u'N строки', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Занято должностей на конец года', u'3'], CReportBase.AlignCenter),
            ('10%', [u'Число посещений к врачам, включая посещения на дому - всего', u'4'], CReportBase.AlignCenter),
            ('10%', [u'из них (из гр. 4) по поводу освидетельствования для работы с источниками повышенной опасности и по другим основаниям', u'5'], CReportBase.AlignCenter),
            ('10%', [u'Число посещений по поводу заболеваний, включая посещения на дому (из гр. 4) - всего', u'6'], CReportBase.AlignCenter),
            ('10%', [u'Кроме того, проведено осмотров в военкоматах, учебных и других учреждениях', u'7'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                table.setText(i, 2 + col, reportLine[col])

        # 2201
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        splitTitle(cursor, u'Код по ОКЕИ: человек - 792', u'')
        cursor.insertText(u'(2201) Из числа пациентов, находящихся под диспансерным наблюдением и\nполучающих консультативно-лечебную помощь, получили курс\nлечения/реабилитации бригадным методом у психиатров: для взрослых\n1 ____, для подростков 2 ____, детских 3 _____.')

        # 2210
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число должностей, занятых лицами с немедицинским образованием, в психоневрологических организациях')
        splitTitle(cursor, u'(2210)', u'Коды по ОКЕИ: единица - 642, человек - 792')
        tableColumns = [
            ('28%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('10%', [u'N строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Занято должностей на конец года', u'', u'', u'3'], CReportBase.AlignCenter),
            ('10%', [u'из них принимали участие в сопровождении профилактических и реабилитационных программ с пациентами и родственниками пациентов', u'', u'', u'4'], CReportBase.AlignCenter),
            ('10%', [u'Число пациентов, которым оказывалась помощь в течение отчетного года', u'', u'', u'5'], CReportBase.AlignCenter),
            ('10%', [u'из них число пациентов, которым оказана помощь (из гр. 5)', u'индивидуально', u'', u'6'], CReportBase.AlignCenter),
            ('10%', [u'', u'в составе бригады специалистов', u'', u'7'], CReportBase.AlignCenter),
            ('10%', [u'', u'в составе психосоциальных групп', u'', u'8'], CReportBase.AlignCenter),
            ('10%', [u'из числа пациентов (из гр. 5) трудоустроено в течение года', u'', u'', u'9'], CReportBase.AlignCenter)
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 3, 1)
        table.mergeCells(0, 4, 3, 1)
        table.mergeCells(0, 5, 1, 3)
        table.mergeCells(1, 5, 2, 1)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 7, 2, 1)
        table.mergeCells(0, 8, 3, 1)
        rowSize = 7
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows2210))]
        for row, rowDescr in enumerate(MainRows2210):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                if rowDescr[1] in ['1', '4'] and col in [6]:
                    table.setText(i, 2 + col, 'X')
                elif rowDescr[1] != '':
                    table.setText(i, 2 + col, reportLine[col])
        return doc