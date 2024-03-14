# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\Test\TestListFilterDialog.ui'
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

class Ui_ItemFilterDialog(object):
    def setupUi(self, ItemFilterDialog):
        ItemFilterDialog.setObjectName(_fromUtf8("ItemFilterDialog"))
        ItemFilterDialog.resize(337, 201)
        self.gridLayout = QtGui.QGridLayout(ItemFilterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblNameContains = QtGui.QLabel(ItemFilterDialog)
        self.lblNameContains.setObjectName(_fromUtf8("lblNameContains"))
        self.gridLayout.addWidget(self.lblNameContains, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(ItemFilterDialog)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 2, 0, 1, 1)
        self.edtNameContains = QtGui.QLineEdit(ItemFilterDialog)
        self.edtNameContains.setObjectName(_fromUtf8("edtNameContains"))
        self.gridLayout.addWidget(self.edtNameContains, 1, 1, 1, 1)
        self.lblGroup = QtGui.QLabel(ItemFilterDialog)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.gridLayout.addWidget(self.lblGroup, 0, 0, 1, 1)
        self.cmbGroup = CRBComboBox(ItemFilterDialog)
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.gridLayout.addWidget(self.cmbGroup, 0, 1, 1, 1)
        self.lblEquipment = QtGui.QLabel(ItemFilterDialog)
        self.lblEquipment.setObjectName(_fromUtf8("lblEquipment"))
        self.gridLayout.addWidget(self.lblEquipment, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemFilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.cmbEquipment = CEquipmentComboBox(ItemFilterDialog)
        self.cmbEquipment.setObjectName(_fromUtf8("cmbEquipment"))
        self.gridLayout.addWidget(self.cmbEquipment, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(ItemFilterDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 2, 1, 1, 1)

        self.retranslateUi(ItemFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemFilterDialog)
        ItemFilterDialog.setTabOrder(self.cmbGroup, self.edtNameContains)
        ItemFilterDialog.setTabOrder(self.edtNameContains, self.edtCode)
        ItemFilterDialog.setTabOrder(self.edtCode, self.cmbEquipment)
        ItemFilterDialog.setTabOrder(self.cmbEquipment, self.buttonBox)

    def retranslateUi(self, ItemFilterDialog):
        self.lblNameContains.setText(_translate("ItemFilterDialog", "Наименование содержит", None))
        self.lblCode.setText(_translate("ItemFilterDialog", "Код теста", None))
        self.lblGroup.setText(_translate("ItemFilterDialog", "Группа", None))
        self.lblEquipment.setText(_translate("ItemFilterDialog", "Оборудование", None))

from Orgs.EquipmentComboBox import CEquipmentComboBox
from library.crbcombobox import CRBComboBox
