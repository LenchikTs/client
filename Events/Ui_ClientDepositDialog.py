# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\ClientDepositDialog.ui'
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

class Ui_ClientDepositDialog(object):
    def setupUi(self, ClientDepositDialog):
        ClientDepositDialog.setObjectName(_fromUtf8("ClientDepositDialog"))
        ClientDepositDialog.resize(400, 300)
        ClientDepositDialog.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(ClientDepositDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(189, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(ClientDepositDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 2, 1, 2)
        self.tblDeposit = CInDocTableView(ClientDepositDialog)
        self.tblDeposit.setObjectName(_fromUtf8("tblDeposit"))
        self.gridLayout.addWidget(self.tblDeposit, 0, 0, 1, 4)
        self.btnIgnore = QtGui.QPushButton(ClientDepositDialog)
        self.btnIgnore.setObjectName(_fromUtf8("btnIgnore"))
        self.gridLayout.addWidget(self.btnIgnore, 1, 1, 1, 1)

        self.retranslateUi(ClientDepositDialog)
        QtCore.QMetaObject.connectSlotsByName(ClientDepositDialog)

    def retranslateUi(self, ClientDepositDialog):
        self.btnClose.setText(_translate("ClientDepositDialog", "Закрыть", None))
        self.btnIgnore.setText(_translate("ClientDepositDialog", "Пропустить", None))

from library.InDocTable import CInDocTableView
