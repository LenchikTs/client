# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Reports\Form11Setup.ui'
#
# Created: Mon Dec 16 13:48:32 2019
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Form11SetupDialog(object):
    def setupUi(self, Form11SetupDialog):
        Form11SetupDialog.setObjectName(_fromUtf8("Form11SetupDialog"))
        Form11SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Form11SetupDialog.resize(545, 237)
        Form11SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(Form11SetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbTypeDN = QtGui.QComboBox(Form11SetupDialog)
        self.cmbTypeDN.setObjectName(_fromUtf8("cmbTypeDN"))
        self.cmbTypeDN.addItem(_fromUtf8(""))
        self.cmbTypeDN.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypeDN, 7, 1, 1, 3)
        self.cmbForResult = QtGui.QComboBox(Form11SetupDialog)
        self.cmbForResult.setObjectName(_fromUtf8("cmbForResult"))
        self.cmbForResult.addItem(_fromUtf8(""))
        self.cmbForResult.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbForResult, 4, 1, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(Form11SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 3)
        self.edtTimeEdit = QtGui.QTimeEdit(Form11SetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 1, 2, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(Form11SetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(Form11SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(Form11SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.lblBegDate = QtGui.QLabel(Form11SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(Form11SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Form11SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(Form11SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblAddressType = QtGui.QLabel(Form11SetupDialog)
        self.lblAddressType.setObjectName(_fromUtf8("lblAddressType"))
        self.gridLayout.addWidget(self.lblAddressType, 3, 0, 1, 1)
        self.cmbAddressType = QtGui.QComboBox(Form11SetupDialog)
        self.cmbAddressType.setObjectName(_fromUtf8("cmbAddressType"))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAddressType, 3, 1, 1, 3)
        self.lblForResult = QtGui.QLabel(Form11SetupDialog)
        self.lblForResult.setObjectName(_fromUtf8("lblForResult"))
        self.gridLayout.addWidget(self.lblForResult, 4, 0, 1, 1)
        self.lblTypeDN = QtGui.QLabel(Form11SetupDialog)
        self.lblTypeDN.setObjectName(_fromUtf8("lblTypeDN"))
        self.gridLayout.addWidget(self.lblTypeDN, 7, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 9, 0, 1, 1)
        self.chkOnlyContingent = QtGui.QCheckBox(Form11SetupDialog)
        self.chkOnlyContingent.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chkOnlyContingent.setObjectName(_fromUtf8("chkOnlyContingent"))
        self.gridLayout.addWidget(self.chkOnlyContingent, 8, 1, 1, 3)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblForResult.setBuddy(self.cmbForResult)
        self.lblTypeDN.setBuddy(self.cmbTypeDN)

        self.retranslateUi(Form11SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Form11SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Form11SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Form11SetupDialog)
        Form11SetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        Form11SetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        Form11SetupDialog.setTabOrder(self.edtEndDate, self.edtTimeEdit)
        Form11SetupDialog.setTabOrder(self.edtTimeEdit, self.cmbOrgStructure)
        Form11SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbAddressType)
        Form11SetupDialog.setTabOrder(self.cmbAddressType, self.cmbForResult)
        Form11SetupDialog.setTabOrder(self.cmbForResult, self.cmbTypeDN)
        Form11SetupDialog.setTabOrder(self.cmbTypeDN, self.chkOnlyContingent)
        Form11SetupDialog.setTabOrder(self.chkOnlyContingent, self.buttonBox)

    def retranslateUi(self, Form11SetupDialog):
        Form11SetupDialog.setWindowTitle(_translate("Form11SetupDialog", "параметры отчёта", None))
        self.cmbTypeDN.setItemText(0, _translate("Form11SetupDialog", "событиям", None))
        self.cmbTypeDN.setItemText(1, _translate("Form11SetupDialog", "контингентам в карте", None))
        self.cmbForResult.setItemText(0, _translate("Form11SetupDialog", "лабораторного анализа", None))
        self.cmbForResult.setItemText(1, _translate("Form11SetupDialog", "обследования в карте", None))
        self.lblOrgStructure.setText(_translate("Form11SetupDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("Form11SetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("Form11SetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("Form11SetupDialog", "Дата окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("Form11SetupDialog", "dd.MM.yyyy", None))
        self.lblAddressType.setText(_translate("Form11SetupDialog", "Адрес", None))
        self.cmbAddressType.setItemText(0, _translate("Form11SetupDialog", "По регистрации", None))
        self.cmbAddressType.setItemText(1, _translate("Form11SetupDialog", "По проживанию", None))
        self.lblForResult.setText(_translate("Form11SetupDialog", "По результату", None))
        self.lblTypeDN.setText(_translate("Form11SetupDialog", "ДН по", None))
        self.chkOnlyContingent.setText(_translate("Form11SetupDialog", "только по контингентам", None))

from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
