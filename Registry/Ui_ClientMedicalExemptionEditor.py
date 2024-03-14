# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Registry\ClientMedicalExemptionEditor.ui'
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

class Ui_ClientMedicalExemptionEditor(object):
    def setupUi(self, ClientMedicalExemptionEditor):
        ClientMedicalExemptionEditor.setObjectName(_fromUtf8("ClientMedicalExemptionEditor"))
        ClientMedicalExemptionEditor.resize(441, 400)
        self.gridLayout = QtGui.QGridLayout(ClientMedicalExemptionEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblMedicalExemptionReason = QtGui.QLabel(ClientMedicalExemptionEditor)
        self.lblMedicalExemptionReason.setObjectName(_fromUtf8("lblMedicalExemptionReason"))
        self.gridLayout.addWidget(self.lblMedicalExemptionReason, 6, 0, 1, 2)
        self.cmbMedicalExemptionReason = CRBComboBox(ClientMedicalExemptionEditor)
        self.cmbMedicalExemptionReason.setObjectName(_fromUtf8("cmbMedicalExemptionReason"))
        self.gridLayout.addWidget(self.cmbMedicalExemptionReason, 6, 2, 1, 2)
        self.tblMedicalExemptionInfections = CInDocTableView(ClientMedicalExemptionEditor)
        self.tblMedicalExemptionInfections.setObjectName(_fromUtf8("tblMedicalExemptionInfections"))
        self.gridLayout.addWidget(self.tblMedicalExemptionInfections, 7, 0, 1, 4)
        self.lblDate = QtGui.QLabel(ClientMedicalExemptionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.cmbMedicalExemptionType = CRBComboBox(ClientMedicalExemptionEditor)
        self.cmbMedicalExemptionType.setObjectName(_fromUtf8("cmbMedicalExemptionType"))
        self.gridLayout.addWidget(self.cmbMedicalExemptionType, 5, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(236, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.lblMKB = QtGui.QLabel(ClientMedicalExemptionEditor)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 1, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(ClientMedicalExemptionEditor)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.lblMedicalExemptionType = QtGui.QLabel(ClientMedicalExemptionEditor)
        self.lblMedicalExemptionType.setObjectName(_fromUtf8("lblMedicalExemptionType"))
        self.gridLayout.addWidget(self.lblMedicalExemptionType, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(236, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.edtEndDate = CDateEdit(ClientMedicalExemptionEditor)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 3, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(ClientMedicalExemptionEditor)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 3, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ClientMedicalExemptionEditor)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 2, 1, 2)
        self.cmbMKB = CICDCodeEditEx(ClientMedicalExemptionEditor)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.gridLayout.addWidget(self.cmbMKB, 1, 2, 1, 2)
        self.edtDate = CDateEdit(ClientMedicalExemptionEditor)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ClientMedicalExemptionEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 4)
        self.lblMedicalExemptionReason.setBuddy(self.cmbMedicalExemptionType)
        self.lblDate.setBuddy(self.edtDate)
        self.lblMKB.setBuddy(self.cmbMKB)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblMedicalExemptionType.setBuddy(self.cmbMedicalExemptionType)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ClientMedicalExemptionEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientMedicalExemptionEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientMedicalExemptionEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientMedicalExemptionEditor)
        ClientMedicalExemptionEditor.setTabOrder(self.edtDate, self.cmbMKB)
        ClientMedicalExemptionEditor.setTabOrder(self.cmbMKB, self.cmbPerson)
        ClientMedicalExemptionEditor.setTabOrder(self.cmbPerson, self.tblMedicalExemptionInfections)
        ClientMedicalExemptionEditor.setTabOrder(self.tblMedicalExemptionInfections, self.buttonBox)

    def retranslateUi(self, ClientMedicalExemptionEditor):
        ClientMedicalExemptionEditor.setWindowTitle(_translate("ClientMedicalExemptionEditor", "Dialog", None))
        self.lblMedicalExemptionReason.setText(_translate("ClientMedicalExemptionEditor", "Причина медотвода", None))
        self.lblDate.setText(_translate("ClientMedicalExemptionEditor", "Дата начала", None))
        self.lblMKB.setText(_translate("ClientMedicalExemptionEditor", "Диагноз", None))
        self.lblPerson.setText(_translate("ClientMedicalExemptionEditor", "Врач", None))
        self.lblMedicalExemptionType.setText(_translate("ClientMedicalExemptionEditor", "Тип медотвода", None))
        self.lblEndDate.setText(_translate("ClientMedicalExemptionEditor", "Дата окончания", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEditEx
from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
