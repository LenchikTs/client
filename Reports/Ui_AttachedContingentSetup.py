# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AttachedContingentSetup.ui'
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

class Ui_AttachedContingentSetupDialog(object):
    def setupUi(self, AttachedContingentSetupDialog):
        AttachedContingentSetupDialog.setObjectName(_fromUtf8("AttachedContingentSetupDialog"))
        AttachedContingentSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AttachedContingentSetupDialog.resize(359, 141)
        AttachedContingentSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(AttachedContingentSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEndDate = QtGui.QLabel(AttachedContingentSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(AttachedContingentSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(AttachedContingentSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(AttachedContingentSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 2)
        self.lblAddressOrgStructureType = QtGui.QLabel(AttachedContingentSetupDialog)
        self.lblAddressOrgStructureType.setObjectName(_fromUtf8("lblAddressOrgStructureType"))
        self.gridLayout.addWidget(self.lblAddressOrgStructureType, 2, 0, 1, 1)
        self.cmbAddressOrgStructureType = QtGui.QComboBox(AttachedContingentSetupDialog)
        self.cmbAddressOrgStructureType.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAddressOrgStructureType.sizePolicy().hasHeightForWidth())
        self.cmbAddressOrgStructureType.setSizePolicy(sizePolicy)
        self.cmbAddressOrgStructureType.setObjectName(_fromUtf8("cmbAddressOrgStructureType"))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAddressOrgStructureType, 2, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(AttachedContingentSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.checkBox_all = QtGui.QCheckBox(AttachedContingentSetupDialog)
        self.checkBox_all.setObjectName(_fromUtf8("checkBox_all"))
        self.gridLayout.addWidget(self.checkBox_all, 3, 1, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblAddressOrgStructureType.setBuddy(self.cmbAddressOrgStructureType)

        self.retranslateUi(AttachedContingentSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AttachedContingentSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AttachedContingentSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AttachedContingentSetupDialog)
        AttachedContingentSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        AttachedContingentSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbAddressOrgStructureType)
        AttachedContingentSetupDialog.setTabOrder(self.cmbAddressOrgStructureType, self.buttonBox)

    def retranslateUi(self, AttachedContingentSetupDialog):
        AttachedContingentSetupDialog.setWindowTitle(_translate("AttachedContingentSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("AttachedContingentSetupDialog", "Дата", None))
        self.lblOrgStructure.setText(_translate("AttachedContingentSetupDialog", "Подразделение", None))
        self.lblAddressOrgStructureType.setText(_translate("AttachedContingentSetupDialog", "Адрес", None))
        self.cmbAddressOrgStructureType.setItemText(0, _translate("AttachedContingentSetupDialog", "Регистрация", None))
        self.cmbAddressOrgStructureType.setItemText(1, _translate("AttachedContingentSetupDialog", "Проживание", None))
        self.cmbAddressOrgStructureType.setItemText(2, _translate("AttachedContingentSetupDialog", "Регистрация или проживание", None))
        self.cmbAddressOrgStructureType.setItemText(3, _translate("AttachedContingentSetupDialog", "Прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(4, _translate("AttachedContingentSetupDialog", "Регистрация или прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(5, _translate("AttachedContingentSetupDialog", "Проживание или прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(6, _translate("AttachedContingentSetupDialog", "Регистрация, проживание или прикрепление", None))
        self.checkBox_all.setText(_translate("AttachedContingentSetupDialog", "Детализация отчета", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
