# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportPayersWithFinanceSetup.ui'
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

class Ui_ReportPayersWithFinanceSetupDialog(object):
    def setupUi(self, ReportPayersWithFinanceSetupDialog):
        ReportPayersWithFinanceSetupDialog.setObjectName(_fromUtf8("ReportPayersWithFinanceSetupDialog"))
        ReportPayersWithFinanceSetupDialog.resize(383, 222)
        ReportPayersWithFinanceSetupDialog.setMinimumSize(QtCore.QSize(383, 0))
        self.gridLayout = QtGui.QGridLayout(ReportPayersWithFinanceSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbFinance = CRBComboBox(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFinance.sizePolicy().hasHeightForWidth())
        self.cmbFinance.setSizePolicy(sizePolicy)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 2, 1, 1, 1)
        self.edtBegDate = CDateEdit(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportPayersWithFinanceSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 2)
        self.lblFinance = QtGui.QLabel(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFinance.sizePolicy().hasHeightForWidth())
        self.lblFinance.setSizePolicy(sizePolicy)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 2, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.cmbEventType = CRBComboBox(ReportPayersWithFinanceSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 5, 1, 1, 1)
        self.chkDetailContracts = QtGui.QCheckBox(ReportPayersWithFinanceSetupDialog)
        self.chkDetailContracts.setObjectName(_fromUtf8("chkDetailContracts"))
        self.gridLayout.addWidget(self.chkDetailContracts, 6, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportPayersWithFinanceSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 5, 0, 1, 1)
        self.lblContract = QtGui.QLabel(ReportPayersWithFinanceSetupDialog)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridLayout.addWidget(self.lblContract, 4, 0, 1, 1)
        self.cmbContract = CIndependentContractComboBox(ReportPayersWithFinanceSetupDialog)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.gridLayout.addWidget(self.cmbContract, 4, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(368, 96, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportPayersWithFinanceSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.chkDetailClients = QtGui.QCheckBox(ReportPayersWithFinanceSetupDialog)
        self.chkDetailClients.setObjectName(_fromUtf8("chkDetailClients"))
        self.gridLayout.addWidget(self.chkDetailClients, 7, 0, 1, 2)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportPayersWithFinanceSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportPayersWithFinanceSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportPayersWithFinanceSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportPayersWithFinanceSetupDialog)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.edtEndDate, self.cmbFinance)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.cmbFinance, self.cmbContract)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.cmbContract, self.cmbEventType)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.cmbEventType, self.chkDetailContracts)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.chkDetailContracts, self.chkDetailClients)
        ReportPayersWithFinanceSetupDialog.setTabOrder(self.chkDetailClients, self.buttonBox)

    def retranslateUi(self, ReportPayersWithFinanceSetupDialog):
        ReportPayersWithFinanceSetupDialog.setWindowTitle(_translate("ReportPayersWithFinanceSetupDialog", "Dialog", None))
        self.lblFinance.setText(_translate("ReportPayersWithFinanceSetupDialog", "Тип финансирования", None))
        self.chkDetailContracts.setText(_translate("ReportPayersWithFinanceSetupDialog", "Детализировать по договарам", None))
        self.lblEndDate.setText(_translate("ReportPayersWithFinanceSetupDialog", "Дата &окончания периода", None))
        self.lblEventType.setText(_translate("ReportPayersWithFinanceSetupDialog", "Тип события", None))
        self.lblContract.setText(_translate("ReportPayersWithFinanceSetupDialog", "Договор", None))
        self.lblBegDate.setText(_translate("ReportPayersWithFinanceSetupDialog", "Дата &начала периода", None))
        self.chkDetailClients.setText(_translate("ReportPayersWithFinanceSetupDialog", "Детализировать по пациентам", None))

from Orgs.OrgComboBox import CIndependentContractComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
