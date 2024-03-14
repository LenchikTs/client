# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_DN\Registry\ClientVaccinationEditor.ui'
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

class Ui_ClientVaccinationEditor(object):
    def setupUi(self, ClientVaccinationEditor):
        ClientVaccinationEditor.setObjectName(_fromUtf8("ClientVaccinationEditor"))
        ClientVaccinationEditor.resize(337, 325)
        self.gridLayout = QtGui.QGridLayout(ClientVaccinationEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDose = QtGui.QLabel(ClientVaccinationEditor)
        self.lblDose.setObjectName(_fromUtf8("lblDose"))
        self.gridLayout.addWidget(self.lblDose, 4, 0, 1, 1)
        self.lblDate = QtGui.QLabel(ClientVaccinationEditor)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 3, 0, 1, 1)
        self.lblVaccine = QtGui.QLabel(ClientVaccinationEditor)
        self.lblVaccine.setObjectName(_fromUtf8("lblVaccine"))
        self.gridLayout.addWidget(self.lblVaccine, 0, 0, 1, 1)
        self.lblTransitionType = QtGui.QLabel(ClientVaccinationEditor)
        self.lblTransitionType.setObjectName(_fromUtf8("lblTransitionType"))
        self.gridLayout.addWidget(self.lblTransitionType, 11, 0, 1, 1)
        self.edtDate = CDateEdit(ClientVaccinationEditor)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 3, 1, 1, 1)
        self.cmbVaccinationType = CVaccinationTypeComboBox(ClientVaccinationEditor)
        self.cmbVaccinationType.setEnabled(False)
        self.cmbVaccinationType.setObjectName(_fromUtf8("cmbVaccinationType"))
        self.gridLayout.addWidget(self.cmbVaccinationType, 2, 1, 1, 3)
        self.edtSgtin = QtGui.QLineEdit(ClientVaccinationEditor)
        self.edtSgtin.setObjectName(_fromUtf8("edtSgtin"))
        self.gridLayout.addWidget(self.edtSgtin, 7, 1, 1, 3)
        self.lblReactionDate = QtGui.QLabel(ClientVaccinationEditor)
        self.lblReactionDate.setObjectName(_fromUtf8("lblReactionDate"))
        self.gridLayout.addWidget(self.lblReactionDate, 10, 0, 1, 1)
        self.lblSgtin = QtGui.QLabel(ClientVaccinationEditor)
        self.lblSgtin.setObjectName(_fromUtf8("lblSgtin"))
        self.gridLayout.addWidget(self.lblSgtin, 7, 0, 1, 1)
        self.lblSeria = QtGui.QLabel(ClientVaccinationEditor)
        self.lblSeria.setObjectName(_fromUtf8("lblSeria"))
        self.gridLayout.addWidget(self.lblSeria, 6, 0, 1, 1)
        self.cmbVaccine = CRBComboBox(ClientVaccinationEditor)
        self.cmbVaccine.setObjectName(_fromUtf8("cmbVaccine"))
        self.gridLayout.addWidget(self.cmbVaccine, 0, 1, 1, 3)
        self.lblPerson = QtGui.QLabel(ClientVaccinationEditor)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 8, 0, 1, 1)
        self.cmbReaction = CRBComboBox(ClientVaccinationEditor)
        self.cmbReaction.setObjectName(_fromUtf8("cmbReaction"))
        self.gridLayout.addWidget(self.cmbReaction, 9, 1, 1, 3)
        self.cmbPerson = CPersonComboBoxEx(ClientVaccinationEditor)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 8, 1, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cmbRelegateOrg = CPolyclinicComboBox(ClientVaccinationEditor)
        self.cmbRelegateOrg.setObjectName(_fromUtf8("cmbRelegateOrg"))
        self.horizontalLayout.addWidget(self.cmbRelegateOrg)
        self.btnSelectRelegateOrg = QtGui.QToolButton(ClientVaccinationEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectRelegateOrg.sizePolicy().hasHeightForWidth())
        self.btnSelectRelegateOrg.setSizePolicy(sizePolicy)
        self.btnSelectRelegateOrg.setMinimumSize(QtCore.QSize(30, 0))
        self.btnSelectRelegateOrg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnSelectRelegateOrg.setObjectName(_fromUtf8("btnSelectRelegateOrg"))
        self.horizontalLayout.addWidget(self.btnSelectRelegateOrg)
        self.gridLayout.addLayout(self.horizontalLayout, 12, 1, 1, 3)
        self.edtReactionDate = CDateEdit(ClientVaccinationEditor)
        self.edtReactionDate.setObjectName(_fromUtf8("edtReactionDate"))
        self.gridLayout.addWidget(self.edtReactionDate, 10, 1, 1, 1)
        self.lblVaccinationType = QtGui.QLabel(ClientVaccinationEditor)
        self.lblVaccinationType.setObjectName(_fromUtf8("lblVaccinationType"))
        self.gridLayout.addWidget(self.lblVaccinationType, 2, 0, 1, 1)
        self.edtDose = QtGui.QDoubleSpinBox(ClientVaccinationEditor)
        self.edtDose.setDecimals(3)
        self.edtDose.setObjectName(_fromUtf8("edtDose"))
        self.gridLayout.addWidget(self.edtDose, 4, 1, 1, 1)
        self.lblRelegateOrg = QtGui.QLabel(ClientVaccinationEditor)
        self.lblRelegateOrg.setObjectName(_fromUtf8("lblRelegateOrg"))
        self.gridLayout.addWidget(self.lblRelegateOrg, 12, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 14, 1, 1, 1)
        self.lblReaction = QtGui.QLabel(ClientVaccinationEditor)
        self.lblReaction.setObjectName(_fromUtf8("lblReaction"))
        self.gridLayout.addWidget(self.lblReaction, 9, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ClientVaccinationEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 15, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 10, 3, 1, 1)
        self.cmbTransitionType = CRBComboBox(ClientVaccinationEditor)
        self.cmbTransitionType.setObjectName(_fromUtf8("cmbTransitionType"))
        self.gridLayout.addWidget(self.cmbTransitionType, 11, 1, 1, 3)
        self.edtSeria = QtGui.QLineEdit(ClientVaccinationEditor)
        self.edtSeria.setObjectName(_fromUtf8("edtSeria"))
        self.gridLayout.addWidget(self.edtSeria, 6, 1, 1, 3)
        self.lblVaccineIdentification = QtGui.QLabel(ClientVaccinationEditor)
        self.lblVaccineIdentification.setObjectName(_fromUtf8("lblVaccineIdentification"))
        self.gridLayout.addWidget(self.lblVaccineIdentification, 1, 0, 1, 1)
        self.cmbVaccineIdentification = CVaccineIdentificationComboBox(ClientVaccinationEditor)
        self.cmbVaccineIdentification.setObjectName(_fromUtf8("cmbVaccineIdentification"))
        self.gridLayout.addWidget(self.cmbVaccineIdentification, 1, 1, 1, 3)
        self.lblSgtin.setBuddy(self.edtSgtin)

        self.retranslateUi(ClientVaccinationEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientVaccinationEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientVaccinationEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientVaccinationEditor)
        ClientVaccinationEditor.setTabOrder(self.cmbVaccine, self.cmbVaccinationType)
        ClientVaccinationEditor.setTabOrder(self.cmbVaccinationType, self.edtDate)
        ClientVaccinationEditor.setTabOrder(self.edtDate, self.edtDose)
        ClientVaccinationEditor.setTabOrder(self.edtDose, self.edtSeria)
        ClientVaccinationEditor.setTabOrder(self.edtSeria, self.cmbPerson)
        ClientVaccinationEditor.setTabOrder(self.cmbPerson, self.cmbReaction)
        ClientVaccinationEditor.setTabOrder(self.cmbReaction, self.cmbTransitionType)
        ClientVaccinationEditor.setTabOrder(self.cmbTransitionType, self.buttonBox)

    def retranslateUi(self, ClientVaccinationEditor):
        ClientVaccinationEditor.setWindowTitle(_translate("ClientVaccinationEditor", "Dialog", None))
        self.lblDose.setText(_translate("ClientVaccinationEditor", "Доза", None))
        self.lblDate.setText(_translate("ClientVaccinationEditor", "Дата", None))
        self.lblVaccine.setText(_translate("ClientVaccinationEditor", "Вакцина", None))
        self.lblTransitionType.setText(_translate("ClientVaccinationEditor", "Дополнительно", None))
        self.lblReactionDate.setText(_translate("ClientVaccinationEditor", "Дата реакции", None))
        self.lblSgtin.setText(_translate("ClientVaccinationEditor", "&sgtin", None))
        self.lblSeria.setText(_translate("ClientVaccinationEditor", "Серия", None))
        self.lblPerson.setText(_translate("ClientVaccinationEditor", "Врач", None))
        self.btnSelectRelegateOrg.setText(_translate("ClientVaccinationEditor", "...", None))
        self.lblVaccinationType.setText(_translate("ClientVaccinationEditor", "Тип прививки", None))
        self.lblRelegateOrg.setText(_translate("ClientVaccinationEditor", "Направитель", None))
        self.lblReaction.setText(_translate("ClientVaccinationEditor", "Реакция", None))
        self.lblVaccineIdentification.setText(_translate("ClientVaccinationEditor", "Идентификатор МИБП", None))

from Orgs.OrgComboBox import CPolyclinicComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Orgs.VaccinationTypeComboBox import CVaccinationTypeComboBox
from Registry.VaccinationIdentificationComboBox import CVaccineIdentificationComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
