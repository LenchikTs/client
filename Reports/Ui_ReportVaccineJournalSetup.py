# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportVaccineJournalSetup.ui'
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

class Ui_ReportVaccineJournalSetup(object):
    def setupUi(self, ReportVaccineJournalSetup):
        ReportVaccineJournalSetup.setObjectName(_fromUtf8("ReportVaccineJournalSetup"))
        ReportVaccineJournalSetup.resize(485, 319)
        self.gridLayout = QtGui.QGridLayout(ReportVaccineJournalSetup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 5, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportVaccineJournalSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 4)
        self.lblEndDate = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportVaccineJournalSetup)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 5, 1, 1, 3)
        self.lblSex = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 3, 0, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(ReportVaccineJournalSetup)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 4, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 4)
        self.edtEndDate = CDateEdit(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 2, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 1, 0, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(ReportVaccineJournalSetup)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setProperty("value", 0)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 4, 1, 1, 1)
        self.lblAgeFrom = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.gridLayout.addWidget(self.lblAgeFrom, 4, 0, 1, 1)
        self.lblAgeTo = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblAgeTo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 4, 2, 1, 1)
        self.edtBegDate = CDateEdit(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 1, 1, 1, 1)
        self.cmbVaccineType = QtGui.QComboBox(ReportVaccineJournalSetup)
        self.cmbVaccineType.setObjectName(_fromUtf8("cmbVaccineType"))
        self.gridLayout.addWidget(self.cmbVaccineType, 7, 1, 1, 3)
        self.lblInfection = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblInfection.setObjectName(_fromUtf8("lblInfection"))
        self.gridLayout.addWidget(self.lblInfection, 9, 0, 1, 1)
        self.cmbInfection = CRBComboBox(ReportVaccineJournalSetup)
        self.cmbInfection.setObjectName(_fromUtf8("cmbInfection"))
        self.gridLayout.addWidget(self.cmbInfection, 9, 1, 1, 3)
        self.lblVaccineType = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblVaccineType.setObjectName(_fromUtf8("lblVaccineType"))
        self.gridLayout.addWidget(self.lblVaccineType, 7, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(ReportVaccineJournalSetup)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 3, 1, 1, 1)
        self.lblVaccine = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblVaccine.setObjectName(_fromUtf8("lblVaccine"))
        self.gridLayout.addWidget(self.lblVaccine, 6, 0, 1, 1)
        self.cmbVaccine = CRBComboBox(ReportVaccineJournalSetup)
        self.cmbVaccine.setObjectName(_fromUtf8("cmbVaccine"))
        self.gridLayout.addWidget(self.cmbVaccine, 6, 1, 1, 3)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportVaccineJournalSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportVaccineJournalSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportVaccineJournalSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportVaccineJournalSetup)

    def retranslateUi(self, ReportVaccineJournalSetup):
        ReportVaccineJournalSetup.setWindowTitle(_translate("ReportVaccineJournalSetup", "Параметры отчета", None))
        self.lblOrgStructure.setText(_translate("ReportVaccineJournalSetup", "&Подразделение", None))
        self.lblEndDate.setText(_translate("ReportVaccineJournalSetup", "Дата &окончания периода", None))
        self.lblSex.setText(_translate("ReportVaccineJournalSetup", "Пол", None))
        self.lblBegDate.setText(_translate("ReportVaccineJournalSetup", "Дата &начала периода", None))
        self.lblAgeFrom.setText(_translate("ReportVaccineJournalSetup", "Возраст с", None))
        self.lblAgeTo.setText(_translate("ReportVaccineJournalSetup", "по", None))
        self.lblInfection.setText(_translate("ReportVaccineJournalSetup", "Инфекция", None))
        self.lblVaccineType.setText(_translate("ReportVaccineJournalSetup", "Тип прививки", None))
        self.cmbSex.setItemText(1, _translate("ReportVaccineJournalSetup", "М", None))
        self.cmbSex.setItemText(2, _translate("ReportVaccineJournalSetup", "Ж", None))
        self.lblVaccine.setText(_translate("ReportVaccineJournalSetup", "Вакцина", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportVaccineJournalSetup = QtGui.QDialog()
    ui = Ui_ReportVaccineJournalSetup()
    ui.setupUi(ReportVaccineJournalSetup)
    ReportVaccineJournalSetup.show()
    sys.exit(app.exec_())

