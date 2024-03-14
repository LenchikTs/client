# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from library.DialogBase import CConstructHelperMixin
from library.Utils import *

from Ui_SvodEditReportDialog import Ui_SvodEditReportDialog

class CSvodEditReportDialog(QtGui.QDialog, CConstructHelperMixin, Ui_SvodEditReportDialog):
    def __init__(self, parent, reportId):
        QtGui.QDialog.__init__(self, parent)
        db = QtGui.qApp.db
        self.record = db.getRecord('SvodReport', 'id, date, orgStructure_id', reportId)
        if self.record is None:
            raise Exception(u'Не найдена запись')
        self.setupUi(self)
        self.edtDate.setDate(forceDate(self.record.value('date')))
        self.cmbOrgStructure.setValue(forceRef(self.record.value('orgStructure_id')))

    def disableControls(self, disabled = True):
        self.edtDate.setDisabled(disabled)
        self.buttonBox.setDisabled(disabled)
        QtGui.qApp.processEvents()

    def enableControls(self):
        self.disableControls(False)
    
    def editReport(self):
        date = self.edtDate.date()
        if not date.isValid():
            QtGui.QMessageBox.warning(self, u'Внимание!', u'Необходимо выбрать дату!', QtGui.QMessageBox.Close)
            return
        orgStructureId = forceRef(self.cmbOrgStructure.value())
        if not orgStructureId:
            QtGui.QMessageBox.warning(self, u'Внимание!', u'Необходимо выбрать подразделение!', QtGui.QMessageBox.Close)
            return
        self.disableControls()
        try:
            db = QtGui.qApp.db
            self.record.setValue('date', date)
            self.record.setValue('orgStructure_id', orgStructureId)
            db.updateRecord('SvodReport', self.record)
            self.accept()
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.enableControls()

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            QtGui.qApp.callWithWaitCursor(self, self.editReport)
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.reject()
