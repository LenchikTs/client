# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_ELN\Registry\UnlockAppLockDialog.ui'
#
# Created: Mon Sep 14 09:13:46 2020
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

class Ui_UnlockAppLockDialog(object):
    def setupUi(self, UnlockAppLockDialog):
        UnlockAppLockDialog.setObjectName(_fromUtf8("UnlockAppLockDialog"))
        UnlockAppLockDialog.resize(319, 194)
        self.gridLayout = QtGui.QGridLayout(UnlockAppLockDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblLockedCardList = QtGui.QLabel(UnlockAppLockDialog)
        self.lblLockedCardList.setObjectName(_fromUtf8("lblLockedCardList"))
        self.verticalLayout.addWidget(self.lblLockedCardList)
        self.lvCode = QtGui.QListView(UnlockAppLockDialog)
        self.lvCode.setObjectName(_fromUtf8("lvCode"))
        self.verticalLayout.addWidget(self.lvCode)
        self.lblInfo = QtGui.QLabel(UnlockAppLockDialog)
        self.lblInfo.setObjectName(_fromUtf8("lblInfo"))
        self.verticalLayout.addWidget(self.lblInfo)
        self.edtCode = QtGui.QLineEdit(UnlockAppLockDialog)
        self.edtCode.setMaxLength(11)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.verticalLayout.addWidget(self.edtCode)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnUnlock = QtGui.QPushButton(UnlockAppLockDialog)
        self.btnUnlock.setObjectName(_fromUtf8("btnUnlock"))
        self.horizontalLayout.addWidget(self.btnUnlock)
        self.btnUnlockAll = QtGui.QPushButton(UnlockAppLockDialog)
        self.btnUnlockAll.setEnabled(True)
        self.btnUnlockAll.setObjectName(_fromUtf8("btnUnlockAll"))
        self.horizontalLayout.addWidget(self.btnUnlockAll)
        self.btnCancel = QtGui.QPushButton(UnlockAppLockDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(UnlockAppLockDialog)
        QtCore.QMetaObject.connectSlotsByName(UnlockAppLockDialog)

    def retranslateUi(self, UnlockAppLockDialog):
        UnlockAppLockDialog.setWindowTitle(_translate("UnlockAppLockDialog", "Разблокировать регистрационную карту", None))
        self.lblLockedCardList.setText(_translate("UnlockAppLockDialog", "Заблокированы вашим пользователем:", None))
        self.lblInfo.setText(_translate("UnlockAppLockDialog", "Введите код пациента:", None))
        self.btnUnlock.setText(_translate("UnlockAppLockDialog", "Разблокировать", None))
        self.btnUnlockAll.setText(_translate("UnlockAppLockDialog", "Разблокировать всё", None))
        self.btnCancel.setText(_translate("UnlockAppLockDialog", "Закрыть", None))

