# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\RefBooks\Login\LoginEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(655, 370)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridLayout_9 = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout_9.setMargin(4)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_9.addWidget(self.buttonBox, 9, 2, 1, 1)
        self.lblCreatePerson = QtGui.QLabel(ItemEditorDialog)
        self.lblCreatePerson.setObjectName(_fromUtf8("lblCreatePerson"))
        self.gridLayout_9.addWidget(self.lblCreatePerson, 8, 0, 1, 1)
        self.lblModifyPerson = QtGui.QLabel(ItemEditorDialog)
        self.lblModifyPerson.setObjectName(_fromUtf8("lblModifyPerson"))
        self.gridLayout_9.addWidget(self.lblModifyPerson, 9, 0, 1, 1)
        self.lblPersonId = QtGui.QLabel(ItemEditorDialog)
        self.lblPersonId.setObjectName(_fromUtf8("lblPersonId"))
        self.gridLayout_9.addWidget(self.lblPersonId, 7, 0, 1, 1)
        self.chkChangePassword = QtGui.QCheckBox(ItemEditorDialog)
        self.chkChangePassword.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkChangePassword.sizePolicy().hasHeightForWidth())
        self.chkChangePassword.setSizePolicy(sizePolicy)
        self.chkChangePassword.setObjectName(_fromUtf8("chkChangePassword"))
        self.gridLayout_9.addWidget(self.chkChangePassword, 1, 0, 1, 1)
        self.lblLogin = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLogin.sizePolicy().hasHeightForWidth())
        self.lblLogin.setSizePolicy(sizePolicy)
        self.lblLogin.setObjectName(_fromUtf8("lblLogin"))
        self.gridLayout_9.addWidget(self.lblLogin, 0, 0, 1, 1)
        self.lblPersonContact = QtGui.QLabel(ItemEditorDialog)
        self.lblPersonContact.setObjectName(_fromUtf8("lblPersonContact"))
        self.gridLayout_9.addWidget(self.lblPersonContact, 2, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(ItemEditorDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setMargin(2)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblPerson = CInDocTableView(self.groupBox)
        self.tblPerson.setObjectName(_fromUtf8("tblPerson"))
        self.gridLayout.addWidget(self.tblPerson, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 4, 0, 1, 3)
        self.edtPassword = QtGui.QLineEdit(ItemEditorDialog)
        self.edtPassword.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPassword.sizePolicy().hasHeightForWidth())
        self.edtPassword.setSizePolicy(sizePolicy)
        self.edtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.edtPassword.setObjectName(_fromUtf8("edtPassword"))
        self.gridLayout_9.addWidget(self.edtPassword, 1, 1, 1, 2)
        self.edtLogin = QtGui.QLineEdit(ItemEditorDialog)
        self.edtLogin.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtLogin.sizePolicy().hasHeightForWidth())
        self.edtLogin.setSizePolicy(sizePolicy)
        self.edtLogin.setObjectName(_fromUtf8("edtLogin"))
        self.gridLayout_9.addWidget(self.edtLogin, 0, 1, 1, 2)
        self.edtNote = QtGui.QTextEdit(ItemEditorDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout_9.addWidget(self.edtNote, 2, 1, 1, 2)
        self.lblLogin.setBuddy(self.edtLogin)

        self.retranslateUi(ItemEditorDialog)
        QtCore.QObject.connect(self.chkChangePassword, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtPassword.setEnabled)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.lblCreatePerson.setText(_translate("ItemEditorDialog", "Автор и дата создания записи:", None))
        self.lblModifyPerson.setText(_translate("ItemEditorDialog", "Автор и дата последнего изменения записи:", None))
        self.lblPersonId.setText(_translate("ItemEditorDialog", "id в базе данных:", None))
        self.chkChangePassword.setText(_translate("ItemEditorDialog", "Изменить пароль", None))
        self.lblLogin.setText(_translate("ItemEditorDialog", "Регистра&ционное имя", None))
        self.lblPersonContact.setText(_translate("ItemEditorDialog", "Примечание", None))
        self.groupBox.setTitle(_translate("ItemEditorDialog", "Сотрудники", None))

from library.InDocTable import CInDocTableView
