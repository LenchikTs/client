# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Samson\UP_s11\client_test\RefBooks\Login\LoginListDialog.ui'
#
# Created: Thu Aug 10 13:48:30 2023
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

class Ui_LoginListDialog(object):
    def setupUi(self, LoginListDialog):
        LoginListDialog.setObjectName(_fromUtf8("LoginListDialog"))
        LoginListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        LoginListDialog.resize(678, 228)
        LoginListDialog.setSizeGripEnabled(True)
        LoginListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(LoginListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkSurname = QtGui.QCheckBox(LoginListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSurname.sizePolicy().hasHeightForWidth())
        self.chkSurname.setSizePolicy(sizePolicy)
        self.chkSurname.setObjectName(_fromUtf8("chkSurname"))
        self.gridLayout.addWidget(self.chkSurname, 4, 0, 1, 1)
        self.chkLogin = QtGui.QCheckBox(LoginListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkLogin.sizePolicy().hasHeightForWidth())
        self.chkLogin.setSizePolicy(sizePolicy)
        self.chkLogin.setObjectName(_fromUtf8("chkLogin"))
        self.gridLayout.addWidget(self.chkLogin, 0, 0, 1, 1)
        self.edtLogin = QtGui.QLineEdit(LoginListDialog)
        self.edtLogin.setObjectName(_fromUtf8("edtLogin"))
        self.gridLayout.addWidget(self.edtLogin, 0, 1, 1, 1)
        self.chkName = QtGui.QCheckBox(LoginListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkName.sizePolicy().hasHeightForWidth())
        self.chkName.setSizePolicy(sizePolicy)
        self.chkName.setObjectName(_fromUtf8("chkName"))
        self.gridLayout.addWidget(self.chkName, 3, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(LoginListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(LoginListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.hboxlayout, 8, 0, 1, 3)
        self.tblItems = CTableView(LoginListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 7, 0, 1, 3)
        self.edtLastname = QtGui.QLineEdit(LoginListDialog)
        self.edtLastname.setObjectName(_fromUtf8("edtLastname"))
        self.gridLayout.addWidget(self.edtLastname, 2, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(LoginListDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 3, 1, 1, 1)
        self.edtSurname = QtGui.QLineEdit(LoginListDialog)
        self.edtSurname.setObjectName(_fromUtf8("edtSurname"))
        self.gridLayout.addWidget(self.edtSurname, 4, 1, 1, 1)
        self.chkLastname = QtGui.QCheckBox(LoginListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkLastname.sizePolicy().hasHeightForWidth())
        self.chkLastname.setSizePolicy(sizePolicy)
        self.chkLastname.setObjectName(_fromUtf8("chkLastname"))
        self.gridLayout.addWidget(self.chkLastname, 2, 0, 1, 1)
        self.chkSnils = QtGui.QCheckBox(LoginListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSnils.sizePolicy().hasHeightForWidth())
        self.chkSnils.setSizePolicy(sizePolicy)
        self.chkSnils.setObjectName(_fromUtf8("chkSnils"))
        self.gridLayout.addWidget(self.chkSnils, 5, 0, 1, 1)
        self.edtSnils = QtGui.QLineEdit(LoginListDialog)
        self.edtSnils.setObjectName(_fromUtf8("edtSnils"))
        self.gridLayout.addWidget(self.edtSnils, 5, 1, 1, 1)

        self.retranslateUi(LoginListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoginListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LoginListDialog)
        LoginListDialog.setTabOrder(self.buttonBox, self.tblItems)
        LoginListDialog.setTabOrder(self.tblItems, self.chkLogin)
        LoginListDialog.setTabOrder(self.chkLogin, self.edtLogin)

    def retranslateUi(self, LoginListDialog):
        LoginListDialog.setWindowTitle(_translate("LoginListDialog", "Список записей", None))
        self.chkSurname.setText(_translate("LoginListDialog", "Отчество", None))
        self.chkLogin.setText(_translate("LoginListDialog", "Регистрационное имя", None))
        self.chkName.setText(_translate("LoginListDialog", "Имя", None))
        self.label.setText(_translate("LoginListDialog", "всего: ", None))
        self.tblItems.setWhatsThis(_translate("LoginListDialog", "список записей", "ура!"))
        self.chkLastname.setText(_translate("LoginListDialog", "Фамилия", None))
        self.chkSnils.setText(_translate("LoginListDialog", "СНИЛС", None))

from library.TableView import CTableView
