# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Exchange\Svod\SvodNewReportDialog.ui'
#
# Created: Wed Oct  9 09:46:53 2019
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SvodNewReportDialog(object):
    def setupUi(self, SvodNewReportDialog):
        SvodNewReportDialog.setObjectName(_fromUtf8("SvodNewReportDialog"))
        SvodNewReportDialog.resize(712, 399)
        self.gridLayout = QtGui.QGridLayout(SvodNewReportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(SvodNewReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.label_2 = QtGui.QLabel(SvodNewReportDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.edtDate = QtGui.QDateEdit(SvodNewReportDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 1, 1, 1)
        self.tblFormList = CTableView(SvodNewReportDialog)
        self.tblFormList.setObjectName(_fromUtf8("tblFormList"))
        self.gridLayout.addWidget(self.tblFormList, 2, 0, 1, 5)
        self.btnUpdateFormList = QtGui.QPushButton(SvodNewReportDialog)
        self.btnUpdateFormList.setObjectName(_fromUtf8("btnUpdateFormList"))
        self.gridLayout.addWidget(self.btnUpdateFormList, 0, 4, 1, 1)
        self.label = QtGui.QLabel(SvodNewReportDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(SvodNewReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 3, 1, 1)

        self.retranslateUi(SvodNewReportDialog)
        QtCore.QMetaObject.connectSlotsByName(SvodNewReportDialog)

    def retranslateUi(self, SvodNewReportDialog):
        SvodNewReportDialog.setWindowTitle(_translate("SvodNewReportDialog", "Новый отчет", None))
        self.label_2.setText(_translate("SvodNewReportDialog", "Дата", None))
        self.btnUpdateFormList.setText(_translate("SvodNewReportDialog", "Обновить список форм", None))
        self.label.setText(_translate("SvodNewReportDialog", "Подразделение", None))

from library.TableView import CTableView
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
