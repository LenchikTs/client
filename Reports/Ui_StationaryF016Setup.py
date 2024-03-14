# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Reports\StationaryF016Setup.ui'
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

class Ui_StationaryF016SetupDialog(object):
    def setupUi(self, StationaryF016SetupDialog):
        StationaryF016SetupDialog.setObjectName(_fromUtf8("StationaryF016SetupDialog"))
        StationaryF016SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryF016SetupDialog.resize(490, 211)
        StationaryF016SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryF016SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblYear = QtGui.QLabel(StationaryF016SetupDialog)
        self.lblYear.setObjectName(_fromUtf8("lblYear"))
        self.gridLayout.addWidget(self.lblYear, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 2)
        self.lblHospitalBedProfile = QtGui.QLabel(StationaryF016SetupDialog)
        self.lblHospitalBedProfile.setObjectName(_fromUtf8("lblHospitalBedProfile"))
        self.gridLayout.addWidget(self.lblHospitalBedProfile, 3, 0, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(StationaryF016SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(169, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.edtTimeEdit = QtGui.QTimeEdit(StationaryF016SetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 0, 3, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryF016SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 3)
        self.cmbHospitalBedProfile = CRBComboBox(StationaryF016SetupDialog)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 3, 2, 1, 3)
        self.chkIsGroupingOS = QtGui.QCheckBox(StationaryF016SetupDialog)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 5, 2, 1, 3)
        self.cmbIsTypeOS = QtGui.QComboBox(StationaryF016SetupDialog)
        self.cmbIsTypeOS.setObjectName(_fromUtf8("cmbIsTypeOS"))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbIsTypeOS, 6, 2, 1, 3)
        self.lblISTypeOS = QtGui.QLabel(StationaryF016SetupDialog)
        self.lblISTypeOS.setObjectName(_fromUtf8("lblISTypeOS"))
        self.gridLayout.addWidget(self.lblISTypeOS, 6, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryF016SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 4, 1, 1)
        self.edtYear = QtGui.QLineEdit(StationaryF016SetupDialog)
        self.edtYear.setObjectName(_fromUtf8("edtYear"))
        self.gridLayout.addWidget(self.edtYear, 0, 2, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(StationaryF016SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryF016SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryF016SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryF016SetupDialog)
        StationaryF016SetupDialog.setTabOrder(self.edtYear, self.edtTimeEdit)
        StationaryF016SetupDialog.setTabOrder(self.edtTimeEdit, self.cmbOrgStructure)
        StationaryF016SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbHospitalBedProfile)
        StationaryF016SetupDialog.setTabOrder(self.cmbHospitalBedProfile, self.chkIsGroupingOS)
        StationaryF016SetupDialog.setTabOrder(self.chkIsGroupingOS, self.cmbIsTypeOS)
        StationaryF016SetupDialog.setTabOrder(self.cmbIsTypeOS, self.buttonBox)

    def retranslateUi(self, StationaryF016SetupDialog):
        StationaryF016SetupDialog.setWindowTitle(_translate("StationaryF016SetupDialog", "параметры отчёта", None))
        self.lblYear.setText(_translate("StationaryF016SetupDialog", "Год", None))
        self.lblHospitalBedProfile.setText(_translate("StationaryF016SetupDialog", "Профиль койки", None))
        self.lblOrgStructure.setText(_translate("StationaryF016SetupDialog", "&Подразделение", None))
        self.chkIsGroupingOS.setText(_translate("StationaryF016SetupDialog", "Группировка по подразделениям", None))
        self.cmbIsTypeOS.setItemText(0, _translate("StationaryF016SetupDialog", "не задано", None))
        self.cmbIsTypeOS.setItemText(1, _translate("StationaryF016SetupDialog", "круглосуточный", None))
        self.cmbIsTypeOS.setItemText(2, _translate("StationaryF016SetupDialog", "дневной", None))
        self.lblISTypeOS.setText(_translate("StationaryF016SetupDialog", "Стационар", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.crbcombobox import CRBComboBox
