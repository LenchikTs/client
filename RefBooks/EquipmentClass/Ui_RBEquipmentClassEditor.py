# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/RefBooks/RBEquipmentClassEditor.ui'
#
# Created: Mon Sep 10 17:12:22 2018
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_RBEquipmentClassEditorDialog(object):
    def setupUi(self, RBEquipmentClassEditorDialog):
        RBEquipmentClassEditorDialog.setObjectName(_fromUtf8("RBEquipmentClassEditorDialog"))
        RBEquipmentClassEditorDialog.resize(320, 99)
        RBEquipmentClassEditorDialog.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(RBEquipmentClassEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblCode = QtGui.QLabel(RBEquipmentClassEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblName = QtGui.QLabel(RBEquipmentClassEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBEquipmentClassEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.edtName = QtGui.QLineEdit(RBEquipmentClassEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtCode = QtGui.QLineEdit(RBEquipmentClassEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBEquipmentClassEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBEquipmentClassEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBEquipmentClassEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBEquipmentClassEditorDialog)
        RBEquipmentClassEditorDialog.setTabOrder(self.edtCode, self.edtName)
        RBEquipmentClassEditorDialog.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, RBEquipmentClassEditorDialog):
        RBEquipmentClassEditorDialog.setWindowTitle(_translate("RBEquipmentClassEditorDialog", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBEquipmentClassEditorDialog", "&Код", None))
        self.lblName.setText(_translate("RBEquipmentClassEditorDialog", "&Наименование", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBEquipmentClassEditorDialog = QtGui.QDialog()
    ui = Ui_RBEquipmentClassEditorDialog()
    ui.setupUi(RBEquipmentClassEditorDialog)
    RBEquipmentClassEditorDialog.show()
    sys.exit(app.exec_())

