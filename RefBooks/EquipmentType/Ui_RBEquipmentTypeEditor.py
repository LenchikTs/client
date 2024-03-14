# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/RefBooks/RBEquipmentTypeEditor.ui'
#
# Created: Mon Sep 10 17:12:21 2018
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

class Ui_RBEquipmentTypeEditorDialog(object):
    def setupUi(self, RBEquipmentTypeEditorDialog):
        RBEquipmentTypeEditorDialog.setObjectName(_fromUtf8("RBEquipmentTypeEditorDialog"))
        RBEquipmentTypeEditorDialog.resize(320, 151)
        RBEquipmentTypeEditorDialog.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(RBEquipmentTypeEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(RBEquipmentTypeEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblCode = QtGui.QLabel(RBEquipmentTypeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBEquipmentTypeEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBEquipmentTypeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBEquipmentTypeEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblClass = QtGui.QLabel(RBEquipmentTypeEditorDialog)
        self.lblClass.setObjectName(_fromUtf8("lblClass"))
        self.gridlayout.addWidget(self.lblClass, 2, 0, 1, 1)
        self.cmbClass = CRBComboBox(RBEquipmentTypeEditorDialog)
        self.cmbClass.setObjectName(_fromUtf8("cmbClass"))
        self.gridlayout.addWidget(self.cmbClass, 2, 1, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBEquipmentTypeEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBEquipmentTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBEquipmentTypeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBEquipmentTypeEditorDialog)
        RBEquipmentTypeEditorDialog.setTabOrder(self.edtCode, self.edtName)
        RBEquipmentTypeEditorDialog.setTabOrder(self.edtName, self.cmbClass)
        RBEquipmentTypeEditorDialog.setTabOrder(self.cmbClass, self.buttonBox)

    def retranslateUi(self, RBEquipmentTypeEditorDialog):
        RBEquipmentTypeEditorDialog.setWindowTitle(_translate("RBEquipmentTypeEditorDialog", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBEquipmentTypeEditorDialog", "&Код", None))
        self.lblName.setText(_translate("RBEquipmentTypeEditorDialog", "&Наименование", None))
        self.lblClass.setText(_translate("RBEquipmentTypeEditorDialog", "Класс", None))

from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBEquipmentTypeEditorDialog = QtGui.QDialog()
    ui = Ui_RBEquipmentTypeEditorDialog()
    ui.setupUi(RBEquipmentTypeEditorDialog)
    RBEquipmentTypeEditorDialog.show()
    sys.exit(app.exec_())

