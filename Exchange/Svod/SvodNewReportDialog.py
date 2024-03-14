# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Exchange.AttachService as AttachService
from library.DialogBase import CConstructHelperMixin
from library.TableModel import CTableModel, CTextCol
from library.Utils import *

from Ui_SvodNewReportDialog import Ui_SvodNewReportDialog

class CSvodNewReportDialog(QtGui.QDialog, CConstructHelperMixin, Ui_SvodNewReportDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('FormList', CFormListModel(self))
        self.setupUi(self)
        currentDate = QDate.currentDate()
        self.edtDate.setDate(currentDate)
        self.setModels(self.tblFormList, self.modelFormList, self.selectionModelFormList)
        self.loadFormList()

    def disableControls(self, disabled = True):
        self.edtDate.setDisabled(disabled)
        self.btnUpdateFormList.setDisabled(disabled)
        self.tblFormList.setDisabled(disabled)
        self.buttonBox.setDisabled(disabled)
        QtGui.qApp.processEvents()

    def enableControls(self):
        self.disableControls(False)
    
    def loadFormList(self):
        self.modelFormList.update()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
    
    def updateFormList(self):
        self.disableControls()
        try:
            AttachService.svodUpdateFormList()
            self.loadFormList()
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
        self.enableControls()

    def createReport(self):
        formRecord = self.tblFormList.currentItem()
        formCode = forceString(formRecord.value('code')) if formRecord else None
        if not formCode:
            QtGui.QMessageBox.warning(self, u'Внимание!', u'Необходимо выбрать форму!', QtGui.QMessageBox.Close)
            return
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
            result = AttachService.svodCreateReport(formCode, unicode(date.toString('yyyy-MM-dd')), orgStructureId)
            self.accept()
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.enableControls()

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelFormList_currentRowChanged(self, current, previous):
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(current.isValid())

    @pyqtSignature('')
    def on_btnUpdateFormList_clicked(self):
        QtGui.qApp.callWithWaitCursor(self, self.updateFormList)

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            QtGui.qApp.callWithWaitCursor(self, self.createReport)
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.reject()

class CFormListModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CTextCol(u'Код формы', ['code'], 20),
            CTextCol(u'Наименование', ['name'], 20),
        ], 'SvodForm')
    
    def update(self):
        db = QtGui.qApp.db
        idList = db.getIdList('SvodForm', order='name')
        self.setIdList(idList)