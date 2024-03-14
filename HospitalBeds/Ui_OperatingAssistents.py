# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\OperatingAssistents.ui'
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

class Ui_OperatingAssistents(object):
    def setupUi(self, OperatingAssistents):
        OperatingAssistents.setObjectName(_fromUtf8("OperatingAssistents"))
        OperatingAssistents.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(OperatingAssistents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblPerson = CInDocTableView(OperatingAssistents)
        self.tblPerson.setObjectName(_fromUtf8("tblPerson"))
        self.gridLayout.addWidget(self.tblPerson, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(OperatingAssistents)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(OperatingAssistents)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OperatingAssistents.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OperatingAssistents.reject)
        QtCore.QMetaObject.connectSlotsByName(OperatingAssistents)

    def retranslateUi(self, OperatingAssistents):
        OperatingAssistents.setWindowTitle(_translate("OperatingAssistents", "Выбор ассистентов", None))

from library.InDocTable import CInDocTableView
