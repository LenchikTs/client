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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from library.Utils      import *
from library.database   import *
from Orgs.Utils         import *
from Registry.Utils     import *
from Reports.Report     import CReport
from Reports.ReportBase import *
from Reports.ReportView    import CPageFormat, CReportViewDialog
from Accounting.AccountCheckDialog   import *

class CReportAccountCheck(CReport):
    
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=1, topMargin=1, rightMargin=1, bottomMargin=1)
        self.parent = parent
        self.params = []
        for record in parent.modelAccountItemsCheck.recordList():
            number = forceString(record.value(0))
            clientId = forceString(record.value(1))
            fio = forceString(record.value(2))
            datr = forceString(record.value(3))
            mkb = forceString(record.value(4))
            eventType_title = forceString(record.value(5))
            begDate = forceString(record.value(6))
            endDate = forceString(record.value(7))
            diagRes = forceString(record.value(8))
            eventRes = forceString(record.value(9))
            errCode = forceString(record.value(10))
            ogrn = forceString(record.value(11))
            payer = forceString(record.value(12))
            person = forceString(record.value(13))
            err = u''
            for errList in errCode.split('  '):
                err += parent.CheckTypes[trim(errList), 0][0] if (trim(errList), 0) in parent.CheckTypes else parent.CheckTypes[trim(errList), 1][0] + '; '
            self.params.append([number, clientId, fio, datr, mkb, eventType_title, begDate, endDate, diagRes, eventRes, err, ogrn, payer, person])
        self.setTitle(u'Результат проверки счетов')
        
    def build(self, params):
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Результат проверки счетов')
        cursor.insertBlock(CReportBase.AlignCenter)
        cursor.insertBlock()
        tableColumns = [
                        ('5%', [u'№ п.счета'], CReportBase.AlignCenter),
                        ('5%', [u'Код пациента'], CReportBase.AlignCenter),
                        ('10%', [u'Ф.И.О.'], CReportBase.AlignCenter),
                        ('5%', [u'Дата рож.'], CReportBase.AlignCenter),
                        ('3%', [u'МКБ'], CReportBase.AlignCenter), 
                        ('10%', [u'Тип обращения'], CReportBase.AlignCenter), 
                        ('5%', [u'Дата нач.'], CReportBase.AlignCenter), 
                        ('5%', [u'Дата окон.'], CReportBase.AlignCenter),
                        ('5%', [u'Рез.осм.'], CReportBase.AlignCenter),
                        ('5%', [u'Рез.обр.'], CReportBase.AlignCenter),
                        ('25%', [u'Ошибки'], CReportBase.AlignCenter),
                        ('5%', [u'ОГРН'], CReportBase.AlignCenter), 
                        ('12%', [u'Плательщик'], CReportBase.AlignCenter),                        
                        ('10%', [u'Ответственный'], CReportBase.AlignCenter)
                       ]
        table = createTable(cursor, tableColumns)
        for fields in self.params:
            number, clientId, fio, datr, mkb, eventType_title, begDate, endDate, diagRes, eventRes, err, ogrn, payer, person = fields
            row = table.addRow();
            table.setText(row, 0, number)
            table.setText(row, 1, clientId)
            table.setText(row, 2, fio, charFormat=boldChars)
            table.setText(row, 3, datr)
            table.setText(row, 4, mkb)
            table.setText(row, 5, eventType_title)
            table.setText(row, 6, begDate)
            table.setText(row, 7, endDate)
            table.setText(row, 8, diagRes)
            table.setText(row, 9, eventRes)
            table.setText(row, 10, err, charFormat=boldChars)
            table.setText(row, 11, ogrn)
            table.setText(row, 12, payer)
            table.setText(row, 13, person)
        return doc
        
    def reportLoop(self):
        reportResult = self.build([])
        viewDialog = CReportViewDialog(self.parent)
        viewDialog.setWindowTitle(self.title())
        viewDialog.setText(reportResult)
        viewDialog.exec_()
