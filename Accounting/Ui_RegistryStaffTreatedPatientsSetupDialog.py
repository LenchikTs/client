# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Accounting\RegistryStaffTreatedPatientsSetupDialog.ui'
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

class Ui_RegistryStaffTreatedPatientsSetupDialog(object):
    def setupUi(self, RegistryStaffTreatedPatientsSetupDialog):
        RegistryStaffTreatedPatientsSetupDialog.setObjectName(_fromUtf8("RegistryStaffTreatedPatientsSetupDialog"))
        RegistryStaffTreatedPatientsSetupDialog.resize(279, 120)
        self.gridLayout = QtGui.QGridLayout(RegistryStaffTreatedPatientsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtBegDate = QtGui.QDateEdit(RegistryStaffTreatedPatientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblContract = QtGui.QLabel(RegistryStaffTreatedPatientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblContract.sizePolicy().hasHeightForWidth())
        self.lblContract.setSizePolicy(sizePolicy)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridLayout.addWidget(self.lblContract, 2, 0, 1, 1)
        self.edtEndDate = QtGui.QDateEdit(RegistryStaffTreatedPatientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(RegistryStaffTreatedPatientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(RegistryStaffTreatedPatientsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RegistryStaffTreatedPatientsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.cmbContract = CContractComboBox(RegistryStaffTreatedPatientsSetupDialog)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.gridLayout.addWidget(self.cmbContract, 2, 1, 1, 2)

        self.retranslateUi(RegistryStaffTreatedPatientsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RegistryStaffTreatedPatientsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RegistryStaffTreatedPatientsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegistryStaffTreatedPatientsSetupDialog)
        RegistryStaffTreatedPatientsSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        RegistryStaffTreatedPatientsSetupDialog.setTabOrder(self.edtEndDate, self.cmbContract)
        RegistryStaffTreatedPatientsSetupDialog.setTabOrder(self.cmbContract, self.buttonBox)

    def retranslateUi(self, RegistryStaffTreatedPatientsSetupDialog):
        RegistryStaffTreatedPatientsSetupDialog.setWindowTitle(_translate("RegistryStaffTreatedPatientsSetupDialog", "Реестр пролеченных больных сотрудников", None))
        self.lblContract.setText(_translate("RegistryStaffTreatedPatientsSetupDialog", "Договор", None))
        self.lblBegDate.setText(_translate("RegistryStaffTreatedPatientsSetupDialog", "Дата начала", None))
        self.lblEndDate.setText(_translate("RegistryStaffTreatedPatientsSetupDialog", "Дата окончания", None))

from Accounting.ContractComboBox import CContractComboBox
