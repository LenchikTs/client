# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Accounting\AccountEditDialog.ui'
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

class Ui_AccountEditDialog(object):
    def setupUi(self, AccountEditDialog):
        AccountEditDialog.setObjectName(_fromUtf8("AccountEditDialog"))
        AccountEditDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AccountEditDialog.resize(356, 179)
        AccountEditDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(AccountEditDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtExposeDate = CDateEdit(AccountEditDialog)
        self.edtExposeDate.setObjectName(_fromUtf8("edtExposeDate"))
        self.gridlayout.addWidget(self.edtExposeDate, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AccountEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.edtDate = CDateEdit(AccountEditDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridlayout.addWidget(self.edtDate, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(71, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 2, 2, 1, 1)
        self.lblDate = QtGui.QLabel(AccountEditDialog)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridlayout.addWidget(self.lblDate, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(AccountEditDialog)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridlayout.addWidget(self.edtNumber, 0, 1, 1, 2)
        self.lblNumber = QtGui.QLabel(AccountEditDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridlayout.addWidget(self.lblNumber, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 3, 2, 1, 1)
        self.label = QtGui.QLabel(AccountEditDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 3, 0, 1, 1)
        self.lplPrivateDate = QtGui.QLabel(AccountEditDialog)
        self.lplPrivateDate.setObjectName(_fromUtf8("lplPrivateDate"))
        self.gridlayout.addWidget(self.lplPrivateDate, 4, 0, 1, 1)
        self.edtPrivateDate = CDateEdit(AccountEditDialog)
        self.edtPrivateDate.setObjectName(_fromUtf8("edtPrivateDate"))
        self.gridlayout.addWidget(self.edtPrivateDate, 4, 1, 1, 1)
        self.edtNote = QtGui.QLineEdit(AccountEditDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridlayout.addWidget(self.edtNote, 6, 1, 1, 2)
        self.lblNote = QtGui.QLabel(AccountEditDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridlayout.addWidget(self.lblNote, 6, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3, 4, 2, 1, 1)
        self.lblAccountType = QtGui.QLabel(AccountEditDialog)
        self.lblAccountType.setObjectName(_fromUtf8("lblAccountType"))
        self.gridlayout.addWidget(self.lblAccountType, 1, 0, 1, 1)
        self.cmbAccountType = CRBComboBox(AccountEditDialog)
        self.cmbAccountType.setObjectName(_fromUtf8("cmbAccountType"))
        self.gridlayout.addWidget(self.cmbAccountType, 1, 1, 1, 2)
        self.lblDate.setBuddy(self.edtDate)
        self.lblNumber.setBuddy(self.edtNumber)
        self.label.setBuddy(self.edtExposeDate)
        self.lplPrivateDate.setBuddy(self.edtPrivateDate)
        self.lblNote.setBuddy(self.edtNote)
        self.lblAccountType.setBuddy(self.edtNumber)

        self.retranslateUi(AccountEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AccountEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AccountEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AccountEditDialog)
        AccountEditDialog.setTabOrder(self.edtNumber, self.edtDate)
        AccountEditDialog.setTabOrder(self.edtDate, self.edtExposeDate)
        AccountEditDialog.setTabOrder(self.edtExposeDate, self.edtPrivateDate)
        AccountEditDialog.setTabOrder(self.edtPrivateDate, self.edtNote)
        AccountEditDialog.setTabOrder(self.edtNote, self.buttonBox)

    def retranslateUi(self, AccountEditDialog):
        AccountEditDialog.setWindowTitle(_translate("AccountEditDialog", "Счет", None))
        self.lblDate.setText(_translate("AccountEditDialog", "&Дата", None))
        self.lblNumber.setText(_translate("AccountEditDialog", "&Номер", None))
        self.label.setText(_translate("AccountEditDialog", "Дата &выставления", None))
        self.lplPrivateDate.setText(_translate("AccountEditDialog", "Дата перс. счетов", None))
        self.lblNote.setText(_translate("AccountEditDialog", "Примечание", None))
        self.lblAccountType.setText(_translate("AccountEditDialog", "&Тип реестра счетов", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
