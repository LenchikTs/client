# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Samson\UP_s11\client_test\Registry\ClientVaccinationProbeEditor.ui'
#
# Created: Tue Jul 18 14:44:10 2023
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

class Ui_ClientVaccinationProbeEditor(object):
    def setupUi(self, ClientVaccinationProbeEditor):
        ClientVaccinationProbeEditor.setObjectName(_fromUtf8("ClientVaccinationProbeEditor"))
        ClientVaccinationProbeEditor.resize(337, 359)
        self.gridLayout = QtGui.QGridLayout(ClientVaccinationProbeEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 11, 2, 1, 1)
        self.edtResultDate = CDateEdit(ClientVaccinationProbeEditor)
        self.edtResultDate.setObjectName(_fromUtf8("edtResultDate"))
        self.gridLayout.addWidget(self.edtResultDate, 11, 1, 1, 1)
        self.lbResultDate = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lbResultDate.setObjectName(_fromUtf8("lbResultDate"))
        self.gridLayout.addWidget(self.lbResultDate, 11, 0, 1, 1)
        self.cmbProbeType = QtGui.QComboBox(ClientVaccinationProbeEditor)
        self.cmbProbeType.setObjectName(_fromUtf8("cmbProbeType"))
        self.cmbProbeType.addItem(_fromUtf8(""))
        self.cmbProbeType.setItemText(0, _fromUtf8(""))
        self.cmbProbeType.addItem(_fromUtf8(""))
        self.cmbProbeType.addItem(_fromUtf8(""))
        self.cmbProbeType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbProbeType, 10, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ClientVaccinationProbeEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 0, 1, 3)
        self.lblResult = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblResult.setObjectName(_fromUtf8("lblResult"))
        self.gridLayout.addWidget(self.lblResult, 9, 0, 1, 1)
        self.edtReactionDate = CDateEdit(ClientVaccinationProbeEditor)
        self.edtReactionDate.setObjectName(_fromUtf8("edtReactionDate"))
        self.gridLayout.addWidget(self.edtReactionDate, 7, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ClientVaccinationProbeEditor)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 2)
        self.cmbResult = CRBComboBox(ClientVaccinationProbeEditor)
        self.cmbResult.setObjectName(_fromUtf8("cmbResult"))
        self.gridLayout.addWidget(self.cmbResult, 9, 1, 1, 2)
        self.edtDate = CDateEdit(ClientVaccinationProbeEditor)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 2, 1, 1, 1)
        self.lblProbe = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblProbe.setObjectName(_fromUtf8("lblProbe"))
        self.gridLayout.addWidget(self.lblProbe, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 12, 1, 1, 1)
        self.cmbReaction = CRBComboBox(ClientVaccinationProbeEditor)
        self.cmbReaction.setObjectName(_fromUtf8("cmbReaction"))
        self.gridLayout.addWidget(self.cmbReaction, 6, 1, 1, 2)
        self.lblReaction = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblReaction.setObjectName(_fromUtf8("lblReaction"))
        self.gridLayout.addWidget(self.lblReaction, 6, 0, 1, 1)
        self.lblRelegateOrg = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblRelegateOrg.setObjectName(_fromUtf8("lblRelegateOrg"))
        self.gridLayout.addWidget(self.lblRelegateOrg, 8, 0, 1, 1)
        self.cmbProbe = CRBComboBox(ClientVaccinationProbeEditor)
        self.cmbProbe.setObjectName(_fromUtf8("cmbProbe"))
        self.gridLayout.addWidget(self.cmbProbe, 0, 1, 1, 2)
        self.lblSeria = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblSeria.setObjectName(_fromUtf8("lblSeria"))
        self.gridLayout.addWidget(self.lblSeria, 4, 0, 1, 1)
        self.lblDose = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblDose.setObjectName(_fromUtf8("lblDose"))
        self.gridLayout.addWidget(self.lblDose, 3, 0, 1, 1)
        self.edtDose = QtGui.QDoubleSpinBox(ClientVaccinationProbeEditor)
        self.edtDose.setDecimals(3)
        self.edtDose.setObjectName(_fromUtf8("edtDose"))
        self.gridLayout.addWidget(self.edtDose, 3, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.lblDate = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 2, 0, 1, 1)
        self.lblReactionDate = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblReactionDate.setObjectName(_fromUtf8("lblReactionDate"))
        self.gridLayout.addWidget(self.lblReactionDate, 7, 0, 1, 1)
        self.edtSeria = QtGui.QLineEdit(ClientVaccinationProbeEditor)
        self.edtSeria.setObjectName(_fromUtf8("edtSeria"))
        self.gridLayout.addWidget(self.edtSeria, 4, 1, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 7, 2, 1, 1)
        self.lbProbeType = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lbProbeType.setObjectName(_fromUtf8("lbProbeType"))
        self.gridLayout.addWidget(self.lbProbeType, 10, 0, 1, 1)
        self.lblProbeIdentification = QtGui.QLabel(ClientVaccinationProbeEditor)
        self.lblProbeIdentification.setObjectName(_fromUtf8("lblProbeIdentification"))
        self.gridLayout.addWidget(self.lblProbeIdentification, 1, 0, 1, 1)
        self.cmbProbeIdentification = CVaccinationProbeIdentificationComboBox(ClientVaccinationProbeEditor)
        self.cmbProbeIdentification.setObjectName(_fromUtf8("cmbProbeIdentification"))
        self.gridLayout.addWidget(self.cmbProbeIdentification, 1, 1, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cmbRelegateOrg = COrgComboBox(ClientVaccinationProbeEditor)
        self.cmbRelegateOrg.setObjectName(_fromUtf8("cmbRelegateOrg"))
        self.horizontalLayout.addWidget(self.cmbRelegateOrg)
        self.btnSelectRelegateOrg = QtGui.QToolButton(ClientVaccinationProbeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectRelegateOrg.sizePolicy().hasHeightForWidth())
        self.btnSelectRelegateOrg.setSizePolicy(sizePolicy)
        self.btnSelectRelegateOrg.setMinimumSize(QtCore.QSize(30, 0))
        self.btnSelectRelegateOrg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnSelectRelegateOrg.setObjectName(_fromUtf8("btnSelectRelegateOrg"))
        self.horizontalLayout.addWidget(self.btnSelectRelegateOrg)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 1, 1, 2)

        self.retranslateUi(ClientVaccinationProbeEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientVaccinationProbeEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientVaccinationProbeEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientVaccinationProbeEditor)
        ClientVaccinationProbeEditor.setTabOrder(self.cmbProbe, self.edtDate)
        ClientVaccinationProbeEditor.setTabOrder(self.edtDate, self.cmbPerson)
        ClientVaccinationProbeEditor.setTabOrder(self.cmbPerson, self.cmbReaction)
        ClientVaccinationProbeEditor.setTabOrder(self.cmbReaction, self.cmbResult)
        ClientVaccinationProbeEditor.setTabOrder(self.cmbResult, self.buttonBox)

    def retranslateUi(self, ClientVaccinationProbeEditor):
        ClientVaccinationProbeEditor.setWindowTitle(_translate("ClientVaccinationProbeEditor", "Dialog", None))
        self.lbResultDate.setText(_translate("ClientVaccinationProbeEditor", "Дата результата", None))
        self.cmbProbeType.setItemText(1, _translate("ClientVaccinationProbeEditor", "Предвакцинальная", None))
        self.cmbProbeType.setItemText(2, _translate("ClientVaccinationProbeEditor", "Поствакцинальная", None))
        self.cmbProbeType.setItemText(3, _translate("ClientVaccinationProbeEditor", "Календарная", None))
        self.lblResult.setText(_translate("ClientVaccinationProbeEditor", "Результат", None))
        self.lblProbe.setText(_translate("ClientVaccinationProbeEditor", "Проба", None))
        self.lblReaction.setText(_translate("ClientVaccinationProbeEditor", "Реакция", None))
        self.lblRelegateOrg.setText(_translate("ClientVaccinationProbeEditor", "Направитель", None))
        self.lblSeria.setText(_translate("ClientVaccinationProbeEditor", "Серия", None))
        self.lblDose.setText(_translate("ClientVaccinationProbeEditor", "Доза", None))
        self.lblPerson.setText(_translate("ClientVaccinationProbeEditor", "Врач", None))
        self.lblDate.setText(_translate("ClientVaccinationProbeEditor", "Дата", None))
        self.lblReactionDate.setText(_translate("ClientVaccinationProbeEditor", "Дата реакции", None))
        self.lbProbeType.setText(_translate("ClientVaccinationProbeEditor", "Тип пробы", None))
        self.lblProbeIdentification.setText(_translate("ClientVaccinationProbeEditor", "Идентификатор МИБП", None))
        self.btnSelectRelegateOrg.setText(_translate("ClientVaccinationProbeEditor", "...", None))

from Orgs.OrgComboBox import COrgComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.crbcombobox import CRBComboBox
from library.DateEdit import CDateEdit
from Registry.VaccinationIdentificationComboBox import CVaccinationProbeIdentificationComboBox
