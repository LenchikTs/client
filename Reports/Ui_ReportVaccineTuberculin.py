# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Samson\UP_s11\client_test\Reports\ReportVaccineTuberculin.ui'
#
# Created: Mon May 29 14:33:50 2023
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

class Ui_ReportVaccineJournalSetup(object):
    def setupUi(self, ReportVaccineJournalSetup):
        ReportVaccineJournalSetup.setObjectName(_fromUtf8("ReportVaccineJournalSetup"))
        ReportVaccineJournalSetup.resize(485, 319)
        self.gridLayout = QtGui.QGridLayout(ReportVaccineJournalSetup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ReportVaccineJournalSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 16, 0, 1, 4)
        self.lblEndDate = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 2, 1, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(ReportVaccineJournalSetup)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 7, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 15, 0, 1, 4)
        self.lblAgeTo = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblAgeTo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 7, 2, 1, 1)
        self.lblAgeFrom = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.gridLayout.addWidget(self.lblAgeFrom, 7, 0, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(ReportVaccineJournalSetup)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setProperty("value", 0)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 7, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 1, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 1, 1, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportVaccineJournalSetup)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportVaccineJournalSetup)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 3)
        self.lblSocStatusType = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblSocStatusType.setObjectName(_fromUtf8("lblSocStatusType"))
        self.gridLayout.addWidget(self.lblSocStatusType, 9, 0, 1, 1)
        self.chkgroupfordivision = QtGui.QCheckBox(ReportVaccineJournalSetup)
        self.chkgroupfordivision.setObjectName(_fromUtf8("chkgroupfordivision"))
        self.gridLayout.addWidget(self.chkgroupfordivision, 13, 1, 1, 3)
        self.chkgroupforperson = QtGui.QCheckBox(ReportVaccineJournalSetup)
        self.chkgroupforperson.setObjectName(_fromUtf8("chkgroupforperson"))
        self.gridLayout.addWidget(self.chkgroupforperson, 14, 1, 1, 3)
        self.cmbSocStatusType = CRBComboBox(ReportVaccineJournalSetup)
        self.cmbSocStatusType.setObjectName(_fromUtf8("cmbSocStatusType"))
        self.gridLayout.addWidget(self.cmbSocStatusType, 9, 1, 1, 3)
        self.lblSocStatusClass = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblSocStatusClass.setObjectName(_fromUtf8("lblSocStatusClass"))
        self.gridLayout.addWidget(self.lblSocStatusClass, 8, 0, 1, 1)
        self.cmbSocStatusClass = CSocStatusComboBox(ReportVaccineJournalSetup)
        self.cmbSocStatusClass.setObjectName(_fromUtf8("cmbSocStatusClass"))
        self.gridLayout.addWidget(self.cmbSocStatusClass, 8, 1, 1, 3)
        self.lblOrgStructure_2 = QtGui.QLabel(ReportVaccineJournalSetup)
        self.lblOrgStructure_2.setObjectName(_fromUtf8("lblOrgStructure_2"))
        self.gridLayout.addWidget(self.lblOrgStructure_2, 10, 0, 1, 1)
        self.cmbOrgStructureRegion = CAreaComboBox(ReportVaccineJournalSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructureRegion.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructureRegion.setSizePolicy(sizePolicy)
        self.cmbOrgStructureRegion.setMinimumSize(QtCore.QSize(200, 0))
        self.cmbOrgStructureRegion.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.cmbOrgStructureRegion.setObjectName(_fromUtf8("cmbOrgStructureRegion"))
        self.gridLayout.addWidget(self.cmbOrgStructureRegion, 10, 1, 1, 3)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSocStatusType.setBuddy(self.cmbSocStatusType)
        self.lblSocStatusClass.setBuddy(self.cmbSocStatusClass)
        self.lblOrgStructure_2.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(ReportVaccineJournalSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportVaccineJournalSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportVaccineJournalSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportVaccineJournalSetup)

    def retranslateUi(self, ReportVaccineJournalSetup):
        ReportVaccineJournalSetup.setWindowTitle(_translate("ReportVaccineJournalSetup", "Параметры отчета", None))
        self.lblEndDate.setText(_translate("ReportVaccineJournalSetup", "Дата &окончания", None))
        self.lblPerson.setText(_translate("ReportVaccineJournalSetup", "&Врач", None))
        self.lblAgeTo.setText(_translate("ReportVaccineJournalSetup", "по", None))
        self.lblAgeFrom.setText(_translate("ReportVaccineJournalSetup", "Возраст с", None))
        self.lblBegDate.setText(_translate("ReportVaccineJournalSetup", "Дата &начала", None))
        self.lblOrgStructure.setText(_translate("ReportVaccineJournalSetup", "&Подразделение", None))
        self.lblSocStatusType.setText(_translate("ReportVaccineJournalSetup", "Тип соц.статуса", None))
        self.chkgroupfordivision.setText(_translate("ReportVaccineJournalSetup", "Группировать по подразделениям", None))
        self.chkgroupforperson.setText(_translate("ReportVaccineJournalSetup", "Группировать по врачам", None))
        self.lblSocStatusClass.setText(_translate("ReportVaccineJournalSetup", "Класс соц.статуса", None))
        self.lblOrgStructure_2.setText(_translate("ReportVaccineJournalSetup", "Участок прикрепления ", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.crbcombobox import CRBComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox, CAreaComboBox
from library.DateEdit import CDateEdit
from Registry.SocStatusComboBox import CSocStatusComboBox
