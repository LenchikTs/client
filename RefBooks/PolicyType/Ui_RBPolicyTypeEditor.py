# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBPolicyTypeEditor.ui'
#
# Created: Wed Feb 19 22:56:11 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBPolicyTypeEditorDialog(object):
    def setupUi(self, RBPolicyTypeEditorDialog):
        RBPolicyTypeEditorDialog.setObjectName(_fromUtf8("RBPolicyTypeEditorDialog"))
        RBPolicyTypeEditorDialog.resize(320, 115)
        RBPolicyTypeEditorDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(RBPolicyTypeEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(RBPolicyTypeEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.edtCode = QtGui.QLineEdit(RBPolicyTypeEditorDialog)
        self.edtCode.setMaxLength(8)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBPolicyTypeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(RBPolicyTypeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(307, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 3)
        self.edtName = QtGui.QLineEdit(RBPolicyTypeEditorDialog)
        self.edtName.setMaxLength(64)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(131, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.chkIsCompulsory = QtGui.QCheckBox(RBPolicyTypeEditorDialog)
        self.chkIsCompulsory.setObjectName(_fromUtf8("chkIsCompulsory"))
        self.gridlayout.addWidget(self.chkIsCompulsory, 2, 1, 1, 2)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBPolicyTypeEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBPolicyTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBPolicyTypeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBPolicyTypeEditorDialog)
        RBPolicyTypeEditorDialog.setTabOrder(self.edtCode, self.edtName)
        RBPolicyTypeEditorDialog.setTabOrder(self.edtName, self.chkIsCompulsory)
        RBPolicyTypeEditorDialog.setTabOrder(self.chkIsCompulsory, self.buttonBox)

    def retranslateUi(self, RBPolicyTypeEditorDialog):
        RBPolicyTypeEditorDialog.setWindowTitle(QtGui.QApplication.translate("RBPolicyTypeEditorDialog", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBPolicyTypeEditorDialog", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBPolicyTypeEditorDialog", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.chkIsCompulsory.setText(QtGui.QApplication.translate("RBPolicyTypeEditorDialog", "полис ОМС", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBPolicyTypeEditorDialog = QtGui.QDialog()
    ui = Ui_RBPolicyTypeEditorDialog()
    ui.setupUi(RBPolicyTypeEditorDialog)
    RBPolicyTypeEditorDialog.show()
    sys.exit(app.exec_())

