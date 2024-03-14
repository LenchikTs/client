# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Exchange.AttachService as AttachService

from library.DialogBase import CConstructHelperMixin
from library.Utils import *

from Ui_ImportDispFactInfosDialog import Ui_ImportDispFactInfosDialog

class CImportDispFactInfosDialog(QtGui.QDialog, CConstructHelperMixin, Ui_ImportDispFactInfosDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        currentDate = QDate.currentDate()
        self.dateFrom.setDate(currentDate)
        self.dateTo.setDate(currentDate)
        self.dateFrom.setMaximumDate(currentDate)
        self.dateTo.setMaximumDate(currentDate)

    def disableControls(self, disabled = True):
        self.dateFrom.setDisabled(disabled)
        self.dateTo.setDisabled(disabled)
        self.btnImport.setDisabled(disabled)
        self.btnCancel.setDisabled(disabled)

    def enableControls(self):
        self.disableControls(False)

    def doImport(self):
        self.disableControls()
        try:
            dateFrom = self.dateFrom.date()
            dateTo = self.dateTo.date()
            date = dateFrom
            foundCount = 0
            notFoundCount = 0
            while date <= dateTo:
                page = 1
                nextPage = True
                while nextPage:
                    result = AttachService.getEvFactInfos(unicode(date.toString('yyyy-MM-dd')), page)
                    foundCount += result['foundCount']
                    notFoundCount += result['notFoundCount']
                    nextPage = result['nextPage']
                    page += 1
                date = date.addDays(1)
            if foundCount == 0 and notFoundCount == 0:
                if dateFrom == dateTo:
                    message = (u'Данных за %s нет' % formatDate(dateFrom))
                else:
                    message = (u'Данных c %s по %s нет' % (formatDate(dateFrom), formatDate(dateTo)))
            else:
                message = (u'Добавлено %d записей, не найдено пациентов: %d' % (foundCount, notFoundCount))
            QtGui.QMessageBox.information(self, u'Импорт завершен', message, QtGui.QMessageBox.Close)
            self.accept()
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.enableControls()

    @pyqtSignature('')
    def on_btnImport_clicked(self):
        self.doImport()
        
    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.reject()

    @pyqtSignature('QDate')
    def on_dateFrom_dateChanged(self, date):
        if self.dateTo.date() < date:
            self.dateTo.setDate(date)

    @pyqtSignature('QDate')
    def on_dateTo_dateChanged(self, date):
        if self.dateFrom.date() > date:
            self.dateFrom.setDate(date)
