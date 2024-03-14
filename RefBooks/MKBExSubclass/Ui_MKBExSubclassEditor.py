# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/RefBooks/MKBExSubclassEditor.ui'
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

class Ui_MKBExSubclassEditor(object):
    def setupUi(self, MKBExSubclassEditor):
        MKBExSubclassEditor.setObjectName(_fromUtf8("MKBExSubclassEditor"))
        MKBExSubclassEditor.resize(320, 113)
        MKBExSubclassEditor.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(MKBExSubclassEditor)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblCode = QtGui.QLabel(MKBExSubclassEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.lblPosition = QtGui.QLabel(MKBExSubclassEditor)
        self.lblPosition.setObjectName(_fromUtf8("lblPosition"))
        self.gridlayout.addWidget(self.lblPosition, 1, 0, 1, 1)
        self.lblName = QtGui.QLabel(MKBExSubclassEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.edtPosition = QtGui.QSpinBox(MKBExSubclassEditor)
        self.edtPosition.setMinimum(6)
        self.edtPosition.setMaximum(10)
        self.edtPosition.setObjectName(_fromUtf8("edtPosition"))
        self.gridlayout.addWidget(self.edtPosition, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.edtCode = QtGui.QLineEdit(MKBExSubclassEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.edtName = QtGui.QLineEdit(MKBExSubclassEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 2, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(MKBExSubclassEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(MKBExSubclassEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MKBExSubclassEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MKBExSubclassEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(MKBExSubclassEditor)
        MKBExSubclassEditor.setTabOrder(self.edtCode, self.edtPosition)
        MKBExSubclassEditor.setTabOrder(self.edtPosition, self.edtName)
        MKBExSubclassEditor.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, MKBExSubclassEditor):
        MKBExSubclassEditor.setWindowTitle(_translate("MKBExSubclassEditor", "ChangeMe!", None))
        self.lblCode.setText(_translate("MKBExSubclassEditor", "&Код", None))
        self.lblPosition.setText(_translate("MKBExSubclassEditor", "Позиция", None))
        self.lblName.setText(_translate("MKBExSubclassEditor", "Название субклассификации", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MKBExSubclassEditor = QtGui.QDialog()
    ui = Ui_MKBExSubclassEditor()
    ui.setupUi(MKBExSubclassEditor)
    MKBExSubclassEditor.show()
    sys.exit(app.exec_())

