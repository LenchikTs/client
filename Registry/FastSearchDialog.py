# -*- coding: utf-8 -*-
#############################################################################
##
## Обслуживание пациентов: Быстрый поиск
##
#############################################################################
import re

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QMessageBox

from library.DialogBase import CDialogBase
from library.Utils import forceBool

from Ui_FastSearchDialog import Ui_fsDialog


class CFastSearchDialog(CDialogBase, Ui_fsDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.parsedQuery = []
        self.chkWithMask.setChecked(forceBool(QtGui.qApp.session("FS_withMask")))

    def getParsedQuery(self):
        return self.parsedQuery

    def getQuery(self):
        return self.edtQuery.text()

    def parseQuery(self):
        QtGui.qApp.session("FS_withMask", self.chkWithMask.isChecked())
        query = self.edtQuery.text()
        self.parsedQuery = []
        fio = []
        dd = ''
        mm = ''
        yy = ''
        # ФИОДДММГГГГ (РЕЕ09021995)
        # ФИДДММГГГГ (РЕ09021995)
        # ФИДДММГГ (РЕ090295)
        m = re.search(u'^([а-яА-ЯёЁ]{1,3})(\d{2})(\d{2})(\d{4}|\d{2})$', query)
        if m:
            fio = list(unicode(m.group(1)))
            dd = m.group(2)
            mm = m.group(3)
            yy = m.group(4)
        # Ф* И* (Руд Его)
        # Ф* И* О* (Руден Ег Евген)
        # Ф* И* О* ДДММГГГГ (Руденк Егор Евг 09021995)
        # Ф* И* О* ДДММГГ (Руд Ег Евг 090295)
        # Ф* И* ДДММГГГГ (Руд Егор 09021995)
        # Ф* И* ДДММГГ (Руд Его 090295)
        # Ф* ДДММГГГГ (Руден 09021995)
        # Ф* ДДММГГ (Руден 090295)
        m = re.search(u'^((?:[а-яА-ЯёЁ]+(?= |$) ?){1,3})(?:(\d{2})(\d{2})(\d{4}|\d{2}))?$', query)
        if m:
            fio = re.split(' ', unicode(m.group(1)))
            if fio[-1] == u'':  # тут может попасть пробел в конец, отсекаем
                fio = fio[:-1]
            dd = m.group(2)
            mm = m.group(3)
            yy = m.group(4)
        if len(fio) > 0:
            self.parsedQuery = [fio, dd, mm, yy, self.chkWithMask.isChecked()]
            return True
        else:
            QMessageBox.question(self, u'Внимание!', u'Ошибка шаблона', QMessageBox.Close, QMessageBox.Close)
        return False

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Close:
            self.close()

    @pyqtSignature('')
    def on_edtQuery_returnPressed(self):
        # if self.parseQuery():
        #    self.accept()
        pass

    @pyqtSignature('')
    def on_btnQuery_clicked(self):
        if self.parseQuery():
            self.accept()
