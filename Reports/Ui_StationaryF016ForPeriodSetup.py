# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Reports\StationaryF016ForPeriodSetup.ui'
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

class Ui_StationaryF016ForPeriodSetupDialog(object):
    def setupUi(self, StationaryF016ForPeriodSetupDialog):
        StationaryF016ForPeriodSetupDialog.setObjectName(_fromUtf8("StationaryF016ForPeriodSetupDialog"))
        StationaryF016ForPeriodSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryF016ForPeriodSetupDialog.resize(490, 211)
        StationaryF016ForPeriodSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryF016ForPeriodSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEndDate = QtGui.QLabel(StationaryF016ForPeriodSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.edtEndDate = CDateEdit(StationaryF016ForPeriodSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(StationaryF016ForPeriodSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.lblHospitalBedProfile = QtGui.QLabel(StationaryF016ForPeriodSetupDialog)
        self.lblHospitalBedProfile.setObjectName(_fromUtf8("lblHospitalBedProfile"))
        self.gridLayout.addWidget(self.lblHospitalBedProfile, 4, 0, 1, 2)
        self.edtBegDate = CDateEdit(StationaryF016ForPeriodSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(StationaryF016ForPeriodSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 2)
        self.edtBegTime = QtGui.QTimeEdit(StationaryF016ForPeriodSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(169, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(StationaryF016ForPeriodSetupDialog)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryF016ForPeriodSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 2, 1, 3)
        self.cmbHospitalBedProfile = CRBComboBox(StationaryF016ForPeriodSetupDialog)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 4, 2, 1, 3)
        self.chkIsGroupingOS = QtGui.QCheckBox(StationaryF016ForPeriodSetupDialog)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 6, 2, 1, 3)
        self.cmbIsTypeOS = QtGui.QComboBox(StationaryF016ForPeriodSetupDialog)
        self.cmbIsTypeOS.setObjectName(_fromUtf8("cmbIsTypeOS"))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.cmbIsTypeOS.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbIsTypeOS, 7, 2, 1, 3)
        self.lblISTypeOS = QtGui.QLabel(StationaryF016ForPeriodSetupDialog)
        self.lblISTypeOS.setObjectName(_fromUtf8("lblISTypeOS"))
        self.gridLayout.addWidget(self.lblISTypeOS, 7, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryF016ForPeriodSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 4, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(StationaryF016ForPeriodSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryF016ForPeriodSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryF016ForPeriodSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryF016ForPeriodSetupDialog)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.edtEndTime, self.cmbOrgStructure)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbHospitalBedProfile)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.cmbHospitalBedProfile, self.chkIsGroupingOS)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.chkIsGroupingOS, self.cmbIsTypeOS)
        StationaryF016ForPeriodSetupDialog.setTabOrder(self.cmbIsTypeOS, self.buttonBox)

    def retranslateUi(self, StationaryF016ForPeriodSetupDialog):
        StationaryF016ForPeriodSetupDialog.setWindowTitle(_translate("StationaryF016ForPeriodSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("StationaryF016ForPeriodSetupDialog", "Текущий день", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryF016ForPeriodSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("StationaryF016ForPeriodSetupDialog", "Дата начала", None))
        self.lblHospitalBedProfile.setText(_translate("StationaryF016ForPeriodSetupDialog", "Профиль койки", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryF016ForPeriodSetupDialog", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("StationaryF016ForPeriodSetupDialog", "&Подразделение", None))
        self.chkIsGroupingOS.setText(_translate("StationaryF016ForPeriodSetupDialog", "Группировка по подразделениям", None))
        self.cmbIsTypeOS.setItemText(0, _translate("StationaryF016ForPeriodSetupDialog", "не задано", None))
        self.cmbIsTypeOS.setItemText(1, _translate("StationaryF016ForPeriodSetupDialog", "круглосуточный", None))
        self.cmbIsTypeOS.setItemText(2, _translate("StationaryF016ForPeriodSetupDialog", "дневной", None))
        self.lblISTypeOS.setText(_translate("StationaryF016ForPeriodSetupDialog", "Стационар", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
