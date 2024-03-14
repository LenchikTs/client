# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DiagnosticYearReportSetupDialog.ui'
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

class Ui_DiagnosticYearReportSetupDialog(object):
    def setupUi(self, DiagnosticYearReportSetupDialog):
        DiagnosticYearReportSetupDialog.setObjectName(_fromUtf8("DiagnosticYearReportSetupDialog"))
        DiagnosticYearReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DiagnosticYearReportSetupDialog.resize(398, 221)
        DiagnosticYearReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DiagnosticYearReportSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkUrgent = QtGui.QCheckBox(DiagnosticYearReportSetupDialog)
        self.chkUrgent.setObjectName(_fromUtf8("chkUrgent"))
        self.gridLayout.addWidget(self.chkUrgent, 4, 0, 1, 1)
        self.lblAgeFrom = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.gridLayout.addWidget(self.lblAgeFrom, 3, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(DiagnosticYearReportSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 5)
        self.lblAgeYears = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.gridLayout.addWidget(self.lblAgeYears, 3, 5, 1, 1)
        self.lblReportYear = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblReportYear.setObjectName(_fromUtf8("lblReportYear"))
        self.gridLayout.addWidget(self.lblReportYear, 0, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.edtReportYear = QtGui.QSpinBox(DiagnosticYearReportSetupDialog)
        self.edtReportYear.setMinimum(2000)
        self.edtReportYear.setMaximum(2500)
        self.edtReportYear.setObjectName(_fromUtf8("edtReportYear"))
        self.gridLayout.addWidget(self.edtReportYear, 0, 1, 1, 5)
        self.lblOrgStructure = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(DiagnosticYearReportSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(DiagnosticYearReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 2, 1, 5)
        self.edtAgeTo = QtGui.QSpinBox(DiagnosticYearReportSetupDialog)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 3, 4, 1, 1)
        self.lblAgeTo = QtGui.QLabel(DiagnosticYearReportSetupDialog)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 3, 3, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(DiagnosticYearReportSetupDialog)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 3, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(DiagnosticYearReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DiagnosticYearReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DiagnosticYearReportSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DiagnosticYearReportSetupDialog)
        DiagnosticYearReportSetupDialog.setTabOrder(self.edtReportYear, self.buttonBox)

    def retranslateUi(self, DiagnosticYearReportSetupDialog):
        DiagnosticYearReportSetupDialog.setWindowTitle(_translate("DiagnosticYearReportSetupDialog", "Годовой отчет по диагностическим отделениям", None))
        self.chkUrgent.setText(_translate("DiagnosticYearReportSetupDialog", "Срочные", None))
        self.lblAgeFrom.setText(_translate("DiagnosticYearReportSetupDialog", "Возраст с", None))
        self.lblAgeYears.setText(_translate("DiagnosticYearReportSetupDialog", "лет", None))
        self.lblReportYear.setText(_translate("DiagnosticYearReportSetupDialog", "Отчётный год", None))
        self.lblPerson.setText(_translate("DiagnosticYearReportSetupDialog", "Исполнитель", None))
        self.lblOrgStructure.setText(_translate("DiagnosticYearReportSetupDialog", "Назначившее отделение", None))
        self.lblAgeTo.setText(_translate("DiagnosticYearReportSetupDialog", "по", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
