# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from Events.EditDispatcher import getEventFormClassByType
from Reports.ReportBase import CReportBase
from Reports.ReportView import CReportViewDialog
from library.Utils import anyToUnicode

class CCheck:
    def __init__(self):
        self.abort = False
        self.checkRun = False
        self.progressBar.setFormat('%v')
        self.progressBar.setValue(0)
        self.rows = 0
        self.err_str = u''
        self.items = {}
        self.btnClose.setText(u'закрыть')
        if hasattr(self, 'btnPrint'):
            self.btnPrint.setEnabled(False)

    @pyqtSignature('')
    def on_btnClose_clicked(self):
        if self.checkRun:
            self.abort = True
        else:
            self.close()


    @pyqtSignature('')
    def on_btnStart_clicked(self):
        self.btnStart.setEnabled(False)
        if hasattr(self, 'btnPrint'):
            self.btnPrint.setEnabled(False)
        self.btnClose.setText(u'прервать')
        if hasattr(self, 'labelInfo'):
            self.labelInfo.setText('')
        self.abort = False
        self.checkRun = True
        self.items = {}
        self.rows = 0
        self.err_str = u''
        self.log.clear()
        self.item_bad = False
        try:
            self.check()
        except IOError, e:
            QtGui.qApp.logCurrentException()
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox().critical(self, u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox().critical(self, u'Произошла ошибка', unicode(e), QtGui.QMessageBox.Close)
            self.abort = True
        self.progressBar.setText(u'прервано' if self.abort else u'готово')
        self.btnClose.setText(u'закрыть')
        self.btnStart.setText(u'повторить')
        self.btnStart.setEnabled(True)
        if hasattr(self, 'btnPrint'):
            self.btnPrint.setEnabled(True)
        self.abort = False
        self.checkRun = False


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Результат проверки')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.setBlockFormat(QtGui.QTextBlockFormat())
        for index in range(self.log.count()):
            cursor.insertBlock()
            cursor.insertText(self.log.item(index).text())
        view = CReportViewDialog(self)
        view.setWindowTitle(u'Печать результата проверки')
        view.setText(document)
        view.exec_()


    def getEventFormClass(self, eventTypeId):
        return getEventFormClassByType(eventTypeId)


    def err2log(self, e):
        self.log.addItem(self.err_str + e)
        self.items[self.rows] = self.itemId
        item = self.log.item(self.rows)
        self.log.scrollToItem(item)
        self.rows += 1
        self.item_bad = True


    @pyqtSignature('QModelIndex')
    def on_log_doubleClicked(self, index):
        row = self.log.currentRow()
        item = self.items[row]
        if item:
            dlg = self.openItem(item)
            if dlg:
                dlg.exec_()
