# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportSMOClientsSetup.ui'
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

class Ui_ReportSMOClientsSetupDialog(object):
    def setupUi(self, ReportSMOClientsSetupDialog):
        ReportSMOClientsSetupDialog.setObjectName(_fromUtf8("ReportSMOClientsSetupDialog"))
        ReportSMOClientsSetupDialog.resize(387, 323)
        self.gridLayout = QtGui.QGridLayout(ReportSMOClientsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPurpose = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblPurpose.setObjectName(_fromUtf8("lblPurpose"))
        self.gridLayout.addWidget(self.lblPurpose, 6, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.lblSpeciality = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 4, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportSMOClientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 8, 0, 1, 1)
        self.lblPolicyType = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblPolicyType.setObjectName(_fromUtf8("lblPolicyType"))
        self.gridLayout.addWidget(self.lblPolicyType, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportSMOClientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 3)
        self.lblBegDate = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblPaying = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblPaying.setObjectName(_fromUtf8("lblPaying"))
        self.gridLayout.addWidget(self.lblPaying, 9, 0, 1, 1)
        self.lblMedicalAidKind = QtGui.QLabel(ReportSMOClientsSetupDialog)
        self.lblMedicalAidKind.setObjectName(_fromUtf8("lblMedicalAidKind"))
        self.gridLayout.addWidget(self.lblMedicalAidKind, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.cmbPolicyType = CRBComboBox(ReportSMOClientsSetupDialog)
        self.cmbPolicyType.setObjectName(_fromUtf8("cmbPolicyType"))
        self.gridLayout.addWidget(self.cmbPolicyType, 2, 1, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(ReportSMOClientsSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 4)
        self.cmbSpeciality = CRBComboBox(ReportSMOClientsSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 4, 1, 1, 4)
        self.cmbPerson = CPersonComboBoxEx(ReportSMOClientsSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 4)
        self.cmbPurpose = CRBComboBox(ReportSMOClientsSetupDialog)
        self.cmbPurpose.setObjectName(_fromUtf8("cmbPurpose"))
        self.gridLayout.addWidget(self.cmbPurpose, 6, 1, 1, 4)
        self.cmbMedicalAidKind = CRBComboBox(ReportSMOClientsSetupDialog)
        self.cmbMedicalAidKind.setObjectName(_fromUtf8("cmbMedicalAidKind"))
        self.gridLayout.addWidget(self.cmbMedicalAidKind, 7, 1, 1, 4)
        self.cmbEventType = CRBComboBox(ReportSMOClientsSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 8, 1, 1, 4)
        self.cmbPaying = QtGui.QComboBox(ReportSMOClientsSetupDialog)
        self.cmbPaying.setObjectName(_fromUtf8("cmbPaying"))
        self.cmbPaying.addItem(_fromUtf8(""))
        self.cmbPaying.addItem(_fromUtf8(""))
        self.cmbPaying.addItem(_fromUtf8(""))
        self.cmbPaying.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPaying, 9, 1, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(ReportSMOClientsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 1)
        self.lblPurpose.setBuddy(self.cmbPurpose)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportSMOClientsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportSMOClientsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportSMOClientsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportSMOClientsSetupDialog)
        ReportSMOClientsSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportSMOClientsSetupDialog.setTabOrder(self.edtEndDate, self.cmbPolicyType)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbPolicyType, self.cmbOrgStructure)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbPerson, self.cmbPurpose)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbPurpose, self.cmbMedicalAidKind)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbMedicalAidKind, self.cmbEventType)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbEventType, self.cmbPaying)
        ReportSMOClientsSetupDialog.setTabOrder(self.cmbPaying, self.buttonBox)

    def retranslateUi(self, ReportSMOClientsSetupDialog):
        ReportSMOClientsSetupDialog.setWindowTitle(_translate("ReportSMOClientsSetupDialog", "Dialog", None))
        self.lblPurpose.setText(_translate("ReportSMOClientsSetupDialog", "Назначение события", None))
        self.lblPerson.setText(_translate("ReportSMOClientsSetupDialog", "Врач", None))
        self.lblSpeciality.setText(_translate("ReportSMOClientsSetupDialog", "Специальность", None))
        self.lblEndDate.setText(_translate("ReportSMOClientsSetupDialog", "Дата &окончания периода", None))
        self.lblOrgStructure.setText(_translate("ReportSMOClientsSetupDialog", "Подразделение", None))
        self.lblEventType.setText(_translate("ReportSMOClientsSetupDialog", "&Тип события", None))
        self.lblPolicyType.setText(_translate("ReportSMOClientsSetupDialog", "Тип полиса", None))
        self.lblBegDate.setText(_translate("ReportSMOClientsSetupDialog", "Дата &начала периода", None))
        self.lblPaying.setText(_translate("ReportSMOClientsSetupDialog", "Оплата", None))
        self.lblMedicalAidKind.setText(_translate("ReportSMOClientsSetupDialog", "Вид медицинской помощи", None))
        self.cmbPaying.setItemText(0, _translate("ReportSMOClientsSetupDialog", "Не учитывать", None))
        self.cmbPaying.setItemText(1, _translate("ReportSMOClientsSetupDialog", "Выставленные", None))
        self.cmbPaying.setItemText(2, _translate("ReportSMOClientsSetupDialog", "Оплаченные", None))
        self.cmbPaying.setItemText(3, _translate("ReportSMOClientsSetupDialog", "Отказанные", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
