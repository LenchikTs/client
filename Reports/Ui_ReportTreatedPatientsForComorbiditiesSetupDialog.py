# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kirill/s11/Reports/ReportTreatedPatientsForComorbiditiesSetupDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ReportTreatedPatientsForComorbiditiesSetupDialog(object):
    def setupUi(self, ReportTreatedPatientsForComorbiditiesSetupDialog):
        ReportTreatedPatientsForComorbiditiesSetupDialog.setObjectName(_fromUtf8("ReportTreatedPatientsForComorbiditiesSetupDialog"))
        ReportTreatedPatientsForComorbiditiesSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportTreatedPatientsForComorbiditiesSetupDialog.resize(469, 211)
        ReportTreatedPatientsForComorbiditiesSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.edtBegDate = CDateEdit(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 8, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 2, 1, 2)
        self.chkShowPercentages = QtGui.QCheckBox(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.chkShowPercentages.setChecked(False)
        self.chkShowPercentages.setObjectName(_fromUtf8("chkShowPercentages"))
        self.gridLayout.addWidget(self.chkShowPercentages, 6, 2, 1, 1)
        self.cmbBuildCond = QtGui.QComboBox(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.cmbBuildCond.setObjectName(_fromUtf8("cmbBuildCond"))
        self.cmbBuildCond.addItem(_fromUtf8(""))
        self.cmbBuildCond.addItem(_fromUtf8(""))
        self.cmbBuildCond.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbBuildCond, 2, 2, 1, 1)
        self.lblBuildCond = QtGui.QLabel(ReportTreatedPatientsForComorbiditiesSetupDialog)
        self.lblBuildCond.setObjectName(_fromUtf8("lblBuildCond"))
        self.gridLayout.addWidget(self.lblBuildCond, 2, 0, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportTreatedPatientsForComorbiditiesSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportTreatedPatientsForComorbiditiesSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportTreatedPatientsForComorbiditiesSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportTreatedPatientsForComorbiditiesSetupDialog)
        ReportTreatedPatientsForComorbiditiesSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportTreatedPatientsForComorbiditiesSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        ReportTreatedPatientsForComorbiditiesSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, ReportTreatedPatientsForComorbiditiesSetupDialog):
        ReportTreatedPatientsForComorbiditiesSetupDialog.setWindowTitle(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "&Подразделение", None))
        self.lblEndDate.setText(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "Дата &окончания периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "Дата &начала периода", None))
        self.chkShowPercentages.setText(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "Показать % пролеченных", None))
        self.cmbBuildCond.setItemText(0, _translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "классам заболеваний", None))
        self.cmbBuildCond.setItemText(1, _translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "группам заболеваний", None))
        self.cmbBuildCond.setItemText(2, _translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "заболеваниям", None))
        self.lblBuildCond.setText(_translate("ReportTreatedPatientsForComorbiditiesSetupDialog", "Формировать по", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
