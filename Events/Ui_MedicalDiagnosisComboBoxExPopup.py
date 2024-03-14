# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\MedicalDiagnosisComboBoxExPopup.ui'
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

class Ui_MedicalDiagnosisComboBoxExPopup(object):
    def setupUi(self, MedicalDiagnosisComboBoxExPopup):
        MedicalDiagnosisComboBoxExPopup.setObjectName(_fromUtf8("MedicalDiagnosisComboBoxExPopup"))
        MedicalDiagnosisComboBoxExPopup.resize(408, 326)
        self.gridlayout = QtGui.QGridLayout(MedicalDiagnosisComboBoxExPopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tblMedicalDiagnosis = CTableView(MedicalDiagnosisComboBoxExPopup)
        self.tblMedicalDiagnosis.setObjectName(_fromUtf8("tblMedicalDiagnosis"))
        self.gridlayout.addWidget(self.tblMedicalDiagnosis, 0, 0, 1, 1)

        self.retranslateUi(MedicalDiagnosisComboBoxExPopup)
        QtCore.QMetaObject.connectSlotsByName(MedicalDiagnosisComboBoxExPopup)

    def retranslateUi(self, MedicalDiagnosisComboBoxExPopup):
        MedicalDiagnosisComboBoxExPopup.setWindowTitle(_translate("MedicalDiagnosisComboBoxExPopup", "Form", None))

from library.TableView import CTableView
