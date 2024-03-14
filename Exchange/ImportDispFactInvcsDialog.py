# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Exchange.AttachService as AttachService

from library.DialogBase import CConstructHelperMixin
from library.Utils import *

from Ui_ImportDispFactInvcsDialog import Ui_ImportDispFactInvcsDialog

class CImportDispFactInvcsDialog(QtGui.QDialog, CConstructHelperMixin, Ui_ImportDispFactInvcsDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        currentDate = QDate.currentDate()
        self.sbYear.setValue(currentDate.year())
        self.cmbMonth.setCurrentIndex(currentDate.month() - 1)

    def disableControls(self, disabled = True):
        self.sbYear.setDisabled(disabled)
        self.cmbMonth.setDisabled(disabled)
        self.btnImport.setDisabled(disabled)
        self.btnCancel.setDisabled(disabled)

    def enableControls(self):
        self.disableControls(False)

    def doImport(self):
        self.disableControls()
        page = 1
        foundCount = 0
        notFoundCount = 0
        try:
            year = self.sbYear.value()
            mnth = self.cmbMonth.currentIndex() + 1
            monthText = self.cmbMonth.currentText()
            nextPage = True
            while nextPage:
                result = AttachService.getEvFactInvcs(year, mnth, page)
                foundCount += result['foundCount']
                notFoundCount += result['notFoundCount']
                nextPage = result['nextPage']
                page += 1
            if foundCount == 0 and notFoundCount == 0:
                message = (u'Данных за %s %d г. нет' % (monthText, year))
            else:
                message = (u'Добавлено %d записей, не найдено пациентов: %d' % (foundCount, notFoundCount))
            QtGui.QMessageBox.information(self, u'Импорт завершен', message, QtGui.QMessageBox.Close)
            self.accept()
        except Exception as e:
            if page > 1:
                # загрузили хотя бы одну страницу, а потом ошибка случилась
                message = (u'Добавлено %d записей, не найдено пациентов: %d\nПроизошла ошибка: %s' % (foundCount, notFoundCount, exceptionToUnicode(e)))
                QtGui.QMessageBox.warning(self, u'Импорт прерван', message, QtGui.QMessageBox.Close)
            else:
                QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.enableControls()

    @pyqtSignature('')
    def on_btnImport_clicked(self):
        self.doImport()
        
    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.reject()