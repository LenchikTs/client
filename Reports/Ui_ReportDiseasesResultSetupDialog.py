# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kirill/s11/Reports/ReportDiseasesResultSetupDialog.ui'
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

class Ui_ReportDiseasesResultSetupDialog(object):
    def setupUi(self, ReportDiseasesResultSetupDialog):
        ReportDiseasesResultSetupDialog.setObjectName(_fromUtf8("ReportDiseasesResultSetupDialog"))
        ReportDiseasesResultSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportDiseasesResultSetupDialog.resize(469, 211)
        ReportDiseasesResultSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportDiseasesResultSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(ReportDiseasesResultSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportDiseasesResultSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.edtBegDate = CDateEdit(ReportDiseasesResultSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(ReportDiseasesResultSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportDiseasesResultSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportDiseasesResultSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(ReportDiseasesResultSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 2)
        self.chkShowPercentages = QtGui.QCheckBox(ReportDiseasesResultSetupDialog)
        self.chkShowPercentages.setChecked(True)
        self.chkShowPercentages.setObjectName(_fromUtf8("chkShowPercentages"))
        self.gridLayout.addWidget(self.chkShowPercentages, 5, 2, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportDiseasesResultSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportDiseasesResultSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportDiseasesResultSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportDiseasesResultSetupDialog)
        ReportDiseasesResultSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportDiseasesResultSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        ReportDiseasesResultSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, ReportDiseasesResultSetupDialog):
        ReportDiseasesResultSetupDialog.setWindowTitle(_translate("ReportDiseasesResultSetupDialog", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("ReportDiseasesResultSetupDialog", "&Подразделение", None))
        self.lblEndDate.setText(_translate("ReportDiseasesResultSetupDialog", "Дата &окончания периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportDiseasesResultSetupDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportDiseasesResultSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportDiseasesResultSetupDialog", "Дата &начала периода", None))
        self.chkShowPercentages.setText(_translate("ReportDiseasesResultSetupDialog", "Показать % пролеченных", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
