# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\DiagnosisHospitalBedsDialog.ui'
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

class Ui_DiagnosisHospitalBedsDialog(object):
    def setupUi(self, DiagnosisHospitalBedsDialog):
        DiagnosisHospitalBedsDialog.setObjectName(_fromUtf8("DiagnosisHospitalBedsDialog"))
        DiagnosisHospitalBedsDialog.resize(778, 282)
        self.gridLayout = QtGui.QGridLayout(DiagnosisHospitalBedsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbAPMKB = CICDCodeEditEx(DiagnosisHospitalBedsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAPMKB.sizePolicy().hasHeightForWidth())
        self.cmbAPMKB.setSizePolicy(sizePolicy)
        self.cmbAPMKB.setObjectName(_fromUtf8("cmbAPMKB"))
        self.gridLayout.addWidget(self.cmbAPMKB, 0, 2, 1, 1)
        self.lblAPMKBText = QtGui.QLabel(DiagnosisHospitalBedsDialog)
        self.lblAPMKBText.setText(_fromUtf8(""))
        self.lblAPMKBText.setObjectName(_fromUtf8("lblAPMKBText"))
        self.gridLayout.addWidget(self.lblAPMKBText, 0, 3, 1, 1)
        self.tblAPProps = CActionPropertiesTableView(DiagnosisHospitalBedsDialog)
        self.tblAPProps.setObjectName(_fromUtf8("tblAPProps"))
        self.gridLayout.addWidget(self.tblAPProps, 1, 1, 1, 3)
        self.lblAPMKB = QtGui.QLabel(DiagnosisHospitalBedsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAPMKB.sizePolicy().hasHeightForWidth())
        self.lblAPMKB.setSizePolicy(sizePolicy)
        self.lblAPMKB.setObjectName(_fromUtf8("lblAPMKB"))
        self.gridLayout.addWidget(self.lblAPMKB, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DiagnosisHospitalBedsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 3)

        self.retranslateUi(DiagnosisHospitalBedsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DiagnosisHospitalBedsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DiagnosisHospitalBedsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DiagnosisHospitalBedsDialog)

    def retranslateUi(self, DiagnosisHospitalBedsDialog):
        DiagnosisHospitalBedsDialog.setWindowTitle(_translate("DiagnosisHospitalBedsDialog", "Диагнозы", None))
        self.lblAPMKB.setText(_translate("DiagnosisHospitalBedsDialog", "Диагноз", None))

from Events.ActionPropertiesTable import CActionPropertiesTableView
from library.ICDCodeEdit import CICDCodeEditEx
