# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Orgs/BankEditor.ui'
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

class Ui_BankEditorDialog(object):
    def setupUi(self, BankEditorDialog):
        BankEditorDialog.setObjectName(_fromUtf8("BankEditorDialog"))
        BankEditorDialog.resize(343, 184)
        BankEditorDialog.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(BankEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtSubAccount = QtGui.QLineEdit(BankEditorDialog)
        self.edtSubAccount.setMaxLength(20)
        self.edtSubAccount.setObjectName(_fromUtf8("edtSubAccount"))
        self.gridlayout.addWidget(self.edtSubAccount, 4, 1, 1, 2)
        self.edtCorrAccount = QtGui.QLineEdit(BankEditorDialog)
        self.edtCorrAccount.setMaxLength(20)
        self.edtCorrAccount.setObjectName(_fromUtf8("edtCorrAccount"))
        self.gridlayout.addWidget(self.edtCorrAccount, 3, 1, 1, 2)
        self.edtBranchName = QtGui.QLineEdit(BankEditorDialog)
        self.edtBranchName.setMaxLength(100)
        self.edtBranchName.setObjectName(_fromUtf8("edtBranchName"))
        self.gridlayout.addWidget(self.edtBranchName, 2, 1, 1, 2)
        self.edtName = QtGui.QLineEdit(BankEditorDialog)
        self.edtName.setMaxLength(256)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 0, 1, 1, 2)
        self.edtBIK = QtGui.QLineEdit(BankEditorDialog)
        self.edtBIK.setMaxLength(9)
        self.edtBIK.setObjectName(_fromUtf8("edtBIK"))
        self.gridlayout.addWidget(self.edtBIK, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(151, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 2, 1, 1)
        self.lblName = QtGui.QLabel(BankEditorDialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 0, 0, 1, 1)
        self.lblBIK = QtGui.QLabel(BankEditorDialog)
        self.lblBIK.setObjectName(_fromUtf8("lblBIK"))
        self.gridlayout.addWidget(self.lblBIK, 1, 0, 1, 1)
        self.lblBranchName = QtGui.QLabel(BankEditorDialog)
        self.lblBranchName.setObjectName(_fromUtf8("lblBranchName"))
        self.gridlayout.addWidget(self.lblBranchName, 2, 0, 1, 1)
        self.lblCorrAccount = QtGui.QLabel(BankEditorDialog)
        self.lblCorrAccount.setObjectName(_fromUtf8("lblCorrAccount"))
        self.gridlayout.addWidget(self.lblCorrAccount, 3, 0, 1, 1)
        self.lblSubAccount = QtGui.QLabel(BankEditorDialog)
        self.lblSubAccount.setObjectName(_fromUtf8("lblSubAccount"))
        self.gridlayout.addWidget(self.lblSubAccount, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(BankEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 6, 0, 1, 3)
        self.lblName.setBuddy(self.edtName)
        self.lblBIK.setBuddy(self.edtBIK)
        self.lblBranchName.setBuddy(self.edtBranchName)
        self.lblCorrAccount.setBuddy(self.edtCorrAccount)
        self.lblSubAccount.setBuddy(self.edtSubAccount)

        self.retranslateUi(BankEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), BankEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), BankEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BankEditorDialog)
        BankEditorDialog.setTabOrder(self.edtName, self.edtBIK)
        BankEditorDialog.setTabOrder(self.edtBIK, self.edtBranchName)
        BankEditorDialog.setTabOrder(self.edtBranchName, self.edtCorrAccount)
        BankEditorDialog.setTabOrder(self.edtCorrAccount, self.edtSubAccount)
        BankEditorDialog.setTabOrder(self.edtSubAccount, self.buttonBox)

    def retranslateUi(self, BankEditorDialog):
        BankEditorDialog.setWindowTitle(_translate("BankEditorDialog", "ChangeMe!", None))
        self.edtSubAccount.setInputMask(_translate("BankEditorDialog", "99999999999999999999; ", None))
        self.edtCorrAccount.setInputMask(_translate("BankEditorDialog", "99999999999999999999; ", None))
        self.edtBIK.setInputMask(_translate("BankEditorDialog", "999999999; ", None))
        self.lblName.setText(_translate("BankEditorDialog", "&Наименование", None))
        self.lblBIK.setText(_translate("BankEditorDialog", "&БИК", None))
        self.lblBranchName.setText(_translate("BankEditorDialog", "Наименование &филиала", None))
        self.lblCorrAccount.setText(_translate("BankEditorDialog", "&Корр.счет", None))
        self.lblSubAccount.setText(_translate("BankEditorDialog", "&Суб.счет", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BankEditorDialog = QtGui.QDialog()
    ui = Ui_BankEditorDialog()
    ui.setupUi(BankEditorDialog)
    BankEditorDialog.show()
    sys.exit(app.exec_())

