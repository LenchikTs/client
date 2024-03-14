# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\ClientConsentAddingDialog.ui'
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

class Ui_ClientConsentAddingDialog(object):
    def setupUi(self, ClientConsentAddingDialog):
        ClientConsentAddingDialog.setObjectName(_fromUtf8("ClientConsentAddingDialog"))
        ClientConsentAddingDialog.resize(612, 403)
        self.gridLayout = QtGui.QGridLayout(ClientConsentAddingDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbRepresenterClient = CClientRelationComboBoxForConsents(ClientConsentAddingDialog)
        self.cmbRepresenterClient.setObjectName(_fromUtf8("cmbRepresenterClient"))
        self.gridLayout.addWidget(self.cmbRepresenterClient, 0, 1, 1, 1)
        self.lblRepresenterClient = QtGui.QLabel(ClientConsentAddingDialog)
        self.lblRepresenterClient.setObjectName(_fromUtf8("lblRepresenterClient"))
        self.gridLayout.addWidget(self.lblRepresenterClient, 0, 0, 1, 1)
        self.tblClientConsents = CInDocTableView(ClientConsentAddingDialog)
        self.tblClientConsents.setObjectName(_fromUtf8("tblClientConsents"))
        self.gridLayout.addWidget(self.tblClientConsents, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ClientConsentAddingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.lblDate = QtGui.QLabel(ClientConsentAddingDialog)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 1, 0, 1, 1)
        self.edtDate = CDateEdit(ClientConsentAddingDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 1, 1, 1, 1)

        self.retranslateUi(ClientConsentAddingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientConsentAddingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientConsentAddingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientConsentAddingDialog)
        ClientConsentAddingDialog.setTabOrder(self.cmbRepresenterClient, self.edtDate)
        ClientConsentAddingDialog.setTabOrder(self.edtDate, self.tblClientConsents)
        ClientConsentAddingDialog.setTabOrder(self.tblClientConsents, self.buttonBox)

    def retranslateUi(self, ClientConsentAddingDialog):
        ClientConsentAddingDialog.setWindowTitle(_translate("ClientConsentAddingDialog", "Dialog", None))
        self.lblRepresenterClient.setText(_translate("ClientConsentAddingDialog", "Подписавший согласие", None))
        self.lblDate.setText(_translate("ClientConsentAddingDialog", "Дата регистрации согласия", None))

from Registry.Utils import CClientRelationComboBoxForConsents
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
