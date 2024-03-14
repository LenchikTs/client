# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StationaryPatientsCompositionByRegionSetupDialog.ui'
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

class Ui_StationaryPatientsCompositionByRegionSetupDialog(object):
    def setupUi(self, StationaryPatientsCompositionByRegionSetupDialog):
        StationaryPatientsCompositionByRegionSetupDialog.setObjectName(_fromUtf8("StationaryPatientsCompositionByRegionSetupDialog"))
        StationaryPatientsCompositionByRegionSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryPatientsCompositionByRegionSetupDialog.resize(351, 141)
        StationaryPatientsCompositionByRegionSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryPatientsCompositionByRegionSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(StationaryPatientsCompositionByRegionSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.edtBegDate = CDateEdit(StationaryPatientsCompositionByRegionSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(StationaryPatientsCompositionByRegionSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryPatientsCompositionByRegionSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 1, 1, 1)
        self.edtEndDate = CDateEdit(StationaryPatientsCompositionByRegionSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(StationaryPatientsCompositionByRegionSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryPatientsCompositionByRegionSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(StationaryPatientsCompositionByRegionSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryPatientsCompositionByRegionSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryPatientsCompositionByRegionSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryPatientsCompositionByRegionSetupDialog)
        StationaryPatientsCompositionByRegionSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        StationaryPatientsCompositionByRegionSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        StationaryPatientsCompositionByRegionSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, StationaryPatientsCompositionByRegionSetupDialog):
        StationaryPatientsCompositionByRegionSetupDialog.setWindowTitle(_translate("StationaryPatientsCompositionByRegionSetupDialog", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("StationaryPatientsCompositionByRegionSetupDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryPatientsCompositionByRegionSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("StationaryPatientsCompositionByRegionSetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryPatientsCompositionByRegionSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("StationaryPatientsCompositionByRegionSetupDialog", "Дата &начала периода", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
