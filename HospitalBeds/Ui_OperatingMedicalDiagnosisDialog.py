# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\OperatingMedicalDiagnosisDialog.ui'
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

class Ui_OperatingMedicalDiagnosisDialog(object):
    def setupUi(self, OperatingMedicalDiagnosisDialog):
        OperatingMedicalDiagnosisDialog.setObjectName(_fromUtf8("OperatingMedicalDiagnosisDialog"))
        OperatingMedicalDiagnosisDialog.resize(778, 282)
        self.gridLayout = QtGui.QGridLayout(OperatingMedicalDiagnosisDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblMedicalDiagnosis = COperatingMedicalDiagnosisView(OperatingMedicalDiagnosisDialog)
        self.tblMedicalDiagnosis.setObjectName(_fromUtf8("tblMedicalDiagnosis"))
        self.gridLayout.addWidget(self.tblMedicalDiagnosis, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(OperatingMedicalDiagnosisDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(OperatingMedicalDiagnosisDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OperatingMedicalDiagnosisDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OperatingMedicalDiagnosisDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OperatingMedicalDiagnosisDialog)

    def retranslateUi(self, OperatingMedicalDiagnosisDialog):
        OperatingMedicalDiagnosisDialog.setWindowTitle(_translate("OperatingMedicalDiagnosisDialog", "Врачебная формулировка", None))

from HospitalBeds.OperatingMedicalDiagnosisView import COperatingMedicalDiagnosisView
