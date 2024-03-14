# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Accounting\FormProgressDialog.ui'
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

class Ui_FormProgressDialog(object):
    def setupUi(self, FormProgressDialog):
        FormProgressDialog.setObjectName(_fromUtf8("FormProgressDialog"))
        FormProgressDialog.resize(649, 142)
        self.gridlayout = QtGui.QGridLayout(FormProgressDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblByContracts = QtGui.QLabel(FormProgressDialog)
        self.lblByContracts.setObjectName(_fromUtf8("lblByContracts"))
        self.gridlayout.addWidget(self.lblByContracts, 0, 0, 1, 1)
        self.prbContracts = QtGui.QProgressBar(FormProgressDialog)
        self.prbContracts.setProperty("value", 24)
        self.prbContracts.setObjectName(_fromUtf8("prbContracts"))
        self.gridlayout.addWidget(self.prbContracts, 1, 0, 1, 3)
        self.lblByContract = QtGui.QLabel(FormProgressDialog)
        self.lblByContract.setObjectName(_fromUtf8("lblByContract"))
        self.gridlayout.addWidget(self.lblByContract, 2, 0, 1, 1)
        self.lblContract = QtGui.QLabel(FormProgressDialog)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridlayout.addWidget(self.lblContract, 2, 1, 1, 2)
        self.prbContract = QtGui.QProgressBar(FormProgressDialog)
        self.prbContract.setProperty("value", 24)
        self.prbContract.setObjectName(_fromUtf8("prbContract"))
        self.gridlayout.addWidget(self.prbContract, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 141, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(291, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 5, 0, 1, 2)
        self.btnBreak = QtGui.QPushButton(FormProgressDialog)
        self.btnBreak.setObjectName(_fromUtf8("btnBreak"))
        self.gridlayout.addWidget(self.btnBreak, 5, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 0, 1, 1, 2)

        self.retranslateUi(FormProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(FormProgressDialog)

    def retranslateUi(self, FormProgressDialog):
        FormProgressDialog.setWindowTitle(_translate("FormProgressDialog", "Идёт формирование счёта", None))
        self.lblByContracts.setText(_translate("FormProgressDialog", "Договор", None))
        self.prbContracts.setFormat(_translate("FormProgressDialog", "%v", "2223"))
        self.lblByContract.setText(_translate("FormProgressDialog", "По договору", None))
        self.lblContract.setText(_translate("FormProgressDialog", "TextLabel", None))
        self.prbContract.setFormat(_translate("FormProgressDialog", "%v", None))
        self.btnBreak.setText(_translate("FormProgressDialog", "Прервать", None))

