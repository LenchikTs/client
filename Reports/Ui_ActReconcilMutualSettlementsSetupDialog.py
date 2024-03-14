# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ActReconcilMutualSettlementsSetupDialog.ui'
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

class Ui_ActReconcilMutualSettlementsSetupDialog(object):
    def setupUi(self, ActReconcilMutualSettlementsSetupDialog):
        ActReconcilMutualSettlementsSetupDialog.setObjectName(_fromUtf8("ActReconcilMutualSettlementsSetupDialog"))
        ActReconcilMutualSettlementsSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ActReconcilMutualSettlementsSetupDialog.resize(539, 131)
        ActReconcilMutualSettlementsSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ActReconcilMutualSettlementsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 2, 1, 1)
        self.edtBegDate = CDateEdit(ActReconcilMutualSettlementsSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.lblEndDate = QtGui.QLabel(ActReconcilMutualSettlementsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(ActReconcilMutualSettlementsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ActReconcilMutualSettlementsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 4)
        self.edtEndDate = CDateEdit(ActReconcilMutualSettlementsSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.lblContract = QtGui.QLabel(ActReconcilMutualSettlementsSetupDialog)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridLayout.addWidget(self.lblContract, 2, 0, 1, 2)
        self.cmbContract = CARMSContractTreeFindComboBox(ActReconcilMutualSettlementsSetupDialog)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.gridLayout.addWidget(self.cmbContract, 2, 2, 1, 2)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ActReconcilMutualSettlementsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActReconcilMutualSettlementsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActReconcilMutualSettlementsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActReconcilMutualSettlementsSetupDialog)
        ActReconcilMutualSettlementsSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ActReconcilMutualSettlementsSetupDialog.setTabOrder(self.edtEndDate, self.cmbContract)
        ActReconcilMutualSettlementsSetupDialog.setTabOrder(self.cmbContract, self.buttonBox)

    def retranslateUi(self, ActReconcilMutualSettlementsSetupDialog):
        ActReconcilMutualSettlementsSetupDialog.setWindowTitle(_translate("ActReconcilMutualSettlementsSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("ActReconcilMutualSettlementsSetupDialog", "Дата &окончания периода", None))
        self.lblBegDate.setText(_translate("ActReconcilMutualSettlementsSetupDialog", "Дата &начала периода", None))
        self.lblContract.setText(_translate("ActReconcilMutualSettlementsSetupDialog", "Договор", None))

from Orgs.ContractFindComboBox import CARMSContractTreeFindComboBox
from library.DateEdit import CDateEdit
