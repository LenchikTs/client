# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\OperatingAssistentsDialog.ui'
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

class Ui_OperatingAssistentsDialog(object):
    def setupUi(self, OperatingAssistentsDialog):
        OperatingAssistentsDialog.setObjectName(_fromUtf8("OperatingAssistentsDialog"))
        OperatingAssistentsDialog.resize(778, 282)
        self.gridLayout = QtGui.QGridLayout(OperatingAssistentsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblAPProps = CActionPropertiesTableView(OperatingAssistentsDialog)
        self.tblAPProps.setObjectName(_fromUtf8("tblAPProps"))
        self.gridLayout.addWidget(self.tblAPProps, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(OperatingAssistentsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(OperatingAssistentsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OperatingAssistentsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OperatingAssistentsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OperatingAssistentsDialog)

    def retranslateUi(self, OperatingAssistentsDialog):
        OperatingAssistentsDialog.setWindowTitle(_translate("OperatingAssistentsDialog", "Dialog", None))

from Events.ActionPropertiesTable import CActionPropertiesTableView
