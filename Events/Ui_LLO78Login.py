# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/Events/LLO78Login.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_LLO78LoginDialog(object):
    def setupUi(self, LLO78LoginDialog):
        LLO78LoginDialog.setObjectName(_fromUtf8("LLO78LoginDialog"))
        LLO78LoginDialog.resize(374, 103)
        self.gridlayout = QtGui.QGridLayout(LLO78LoginDialog)
        self.gridlayout.setMargin(6)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblPassword = QtGui.QLabel(LLO78LoginDialog)
        self.lblPassword.setObjectName(_fromUtf8("lblPassword"))
        self.gridlayout.addWidget(self.lblPassword, 1, 0, 1, 1)
        self.lblLogin = QtGui.QLabel(LLO78LoginDialog)
        self.lblLogin.setObjectName(_fromUtf8("lblLogin"))
        self.gridlayout.addWidget(self.lblLogin, 0, 0, 1, 1)
        self.edtPassword = QtGui.QLineEdit(LLO78LoginDialog)
        self.edtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.edtPassword.setObjectName(_fromUtf8("edtPassword"))
        self.gridlayout.addWidget(self.edtPassword, 1, 1, 1, 1)
        self.edtLogin = QtGui.QLineEdit(LLO78LoginDialog)
        self.edtLogin.setObjectName(_fromUtf8("edtLogin"))
        self.gridlayout.addWidget(self.edtLogin, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LLO78LoginDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblPassword.setBuddy(self.edtPassword)
        self.lblLogin.setBuddy(self.edtLogin)

        self.retranslateUi(LLO78LoginDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LLO78LoginDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LLO78LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LLO78LoginDialog)
        LLO78LoginDialog.setTabOrder(self.edtLogin, self.edtPassword)
        LLO78LoginDialog.setTabOrder(self.edtPassword, self.buttonBox)

    def retranslateUi(self, LLO78LoginDialog):
        LLO78LoginDialog.setWindowTitle(_translate("LLO78LoginDialog", "Регистрация в системе ЛЛО", None))
        self.lblPassword.setText(_translate("LLO78LoginDialog", "&Пароль", None))
        self.lblLogin.setText(_translate("LLO78LoginDialog", "&Логин", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LLO78LoginDialog = QtGui.QDialog()
    ui = Ui_LLO78LoginDialog()
    ui.setupUi(LLO78LoginDialog)
    LLO78LoginDialog.show()
    sys.exit(app.exec_())

