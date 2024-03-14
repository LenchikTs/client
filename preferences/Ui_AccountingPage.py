# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\AccountingPage.ui'
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

class Ui_accountingPage(object):
    def setupUi(self, accountingPage):
        accountingPage.setObjectName(_fromUtf8("accountingPage"))
        accountingPage.resize(651, 592)
        accountingPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(accountingPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblCachBox = QtGui.QLabel(accountingPage)
        self.lblCachBox.setObjectName(_fromUtf8("lblCachBox"))
        self.gridLayout.addWidget(self.lblCachBox, 0, 0, 1, 1)
        self.edtCachBox = QtGui.QLineEdit(accountingPage)
        self.edtCachBox.setObjectName(_fromUtf8("edtCachBox"))
        self.gridLayout.addWidget(self.edtCachBox, 0, 1, 1, 2)
        self.chkFilterPaymentByOrgStructure = QtGui.QCheckBox(accountingPage)
        self.chkFilterPaymentByOrgStructure.setObjectName(_fromUtf8("chkFilterPaymentByOrgStructure"))
        self.gridLayout.addWidget(self.chkFilterPaymentByOrgStructure, 1, 1, 1, 1)
        self.lblCachBox.setBuddy(self.edtCachBox)

        self.retranslateUi(accountingPage)
        QtCore.QMetaObject.connectSlotsByName(accountingPage)

    def retranslateUi(self, accountingPage):
        accountingPage.setWindowTitle(_translate("accountingPage", "Расчёты", None))
        self.lblCachBox.setText(_translate("accountingPage", "Касса", None))
        self.chkFilterPaymentByOrgStructure.setText(_translate("accountingPage", "При выставлении счетов &учитывать текущее подразделение", None))

