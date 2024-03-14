# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBNomenclatureTypeFilter.ui'
#
# Created: Mon Sep  7 14:11:29 2015
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

class Ui_ItemFilterDialog(object):
    def setupUi(self, ItemFilterDialog):
        ItemFilterDialog.setObjectName(_fromUtf8("ItemFilterDialog"))
        ItemFilterDialog.resize(320, 151)
        ItemFilterDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ItemFilterDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtCode = QtGui.QLineEdit(ItemFilterDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 2, 1, 1, 1)
        self.cmbClass = CRBComboBox(ItemFilterDialog)
        self.cmbClass.setObjectName(_fromUtf8("cmbClass"))
        self.gridLayout.addWidget(self.cmbClass, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 3, 0, 1, 1)
        self.cmbKind = CRBComboBox(ItemFilterDialog)
        self.cmbKind.setObjectName(_fromUtf8("cmbKind"))
        self.gridLayout.addWidget(self.cmbKind, 1, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(ItemFilterDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.lblKind = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblKind.sizePolicy().hasHeightForWidth())
        self.lblKind.setSizePolicy(sizePolicy)
        self.lblKind.setObjectName(_fromUtf8("lblKind"))
        self.gridLayout.addWidget(self.lblKind, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 2, 0, 1, 1)
        self.lblClass = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblClass.sizePolicy().hasHeightForWidth())
        self.lblClass.setSizePolicy(sizePolicy)
        self.lblClass.setObjectName(_fromUtf8("lblClass"))
        self.gridLayout.addWidget(self.lblClass, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemFilterDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblName.setBuddy(self.edtName)
        self.lblKind.setBuddy(self.cmbKind)
        self.lblCode.setBuddy(self.edtCode)
        self.lblClass.setBuddy(self.cmbClass)

        self.retranslateUi(ItemFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemFilterDialog)
        ItemFilterDialog.setTabOrder(self.cmbClass, self.cmbKind)
        ItemFilterDialog.setTabOrder(self.cmbKind, self.edtCode)
        ItemFilterDialog.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, ItemFilterDialog):
        ItemFilterDialog.setWindowTitle(_translate("ItemFilterDialog", "ChangeMe!", None))
        self.lblName.setText(_translate("ItemFilterDialog", "&Наименование", None))
        self.lblKind.setText(_translate("ItemFilterDialog", "&Вид", None))
        self.lblCode.setText(_translate("ItemFilterDialog", "&Код", None))
        self.lblClass.setText(_translate("ItemFilterDialog", "&Класс", None))

from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemFilterDialog = QtGui.QDialog()
    ui = Ui_ItemFilterDialog()
    ui.setupUi(ItemFilterDialog)
    ItemFilterDialog.show()
    sys.exit(app.exec_())

