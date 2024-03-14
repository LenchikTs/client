# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\kmivc\Samson\UP_s11\client\Exchange\Svod\SvodEditReportDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_SvodEditReportDialog(object):
    def setupUi(self, SvodEditReportDialog):
        SvodEditReportDialog.setObjectName(_fromUtf8("SvodEditReportDialog"))
        SvodEditReportDialog.resize(520, 70)
        self.gridLayout = QtGui.QGridLayout(SvodEditReportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(SvodEditReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(SvodEditReportDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.edtDate = QtGui.QDateEdit(SvodEditReportDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 1, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(SvodEditReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 3, 1, 1)
        self.label = QtGui.QLabel(SvodEditReportDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.retranslateUi(SvodEditReportDialog)
        QtCore.QMetaObject.connectSlotsByName(SvodEditReportDialog)

    def retranslateUi(self, SvodEditReportDialog):
        SvodEditReportDialog.setWindowTitle(_translate("SvodEditReportDialog", "Новый отчет", None))
        self.label_2.setText(_translate("SvodEditReportDialog", "Дата", None))
        self.label.setText(_translate("SvodEditReportDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
