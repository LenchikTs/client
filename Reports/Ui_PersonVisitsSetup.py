# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\PersonVisitsSetup.ui'
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

class Ui_PersonVisitsSetupDialog(object):
    def setupUi(self, PersonVisitsSetupDialog):
        PersonVisitsSetupDialog.setObjectName(_fromUtf8("PersonVisitsSetupDialog"))
        PersonVisitsSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PersonVisitsSetupDialog.resize(591, 646)
        PersonVisitsSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(PersonVisitsSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(PersonVisitsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 27, 0, 1, 5)
        self.cmbWorkOrganisation = COrgComboBox(PersonVisitsSetupDialog)
        self.cmbWorkOrganisation.setObjectName(_fromUtf8("cmbWorkOrganisation"))
        self.gridlayout.addWidget(self.cmbWorkOrganisation, 10, 1, 1, 3)
        self.edtBegDate = CDateEdit(PersonVisitsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.cmbSex = QtGui.QComboBox(PersonVisitsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSex.sizePolicy().hasHeightForWidth())
        self.cmbSex.setSizePolicy(sizePolicy)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbSex, 11, 1, 1, 1)
        self.frmAge = QtGui.QFrame(PersonVisitsSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.edtAgeFrom = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.hboxlayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(self.frmAge)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.hboxlayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.hboxlayout.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(self.frmAge)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.hboxlayout.addWidget(self.lblAgeYears)
        spacerItem = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridlayout.addWidget(self.frmAge, 12, 1, 1, 4)
        self.lblIsPrimary = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblIsPrimary.setObjectName(_fromUtf8("lblIsPrimary"))
        self.gridlayout.addWidget(self.lblIsPrimary, 8, 0, 1, 1)
        self.cmbAccountingSystem = CRBComboBox(PersonVisitsSetupDialog)
        self.cmbAccountingSystem.setObjectName(_fromUtf8("cmbAccountingSystem"))
        self.gridlayout.addWidget(self.cmbAccountingSystem, 13, 1, 1, 4)
        self.lblEndDate = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblIdentifierType = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblIdentifierType.setObjectName(_fromUtf8("lblIdentifierType"))
        self.gridlayout.addWidget(self.lblIdentifierType, 13, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridlayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(PersonVisitsSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridlayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 4)
        self.cmbEventPurpose = CRBComboBox(PersonVisitsSetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridlayout.addWidget(self.cmbEventPurpose, 5, 1, 1, 4)
        self.cmbIsPrimary = QtGui.QComboBox(PersonVisitsSetupDialog)
        self.cmbIsPrimary.setObjectName(_fromUtf8("cmbIsPrimary"))
        self.cmbIsPrimary.addItem(_fromUtf8(""))
        self.cmbIsPrimary.addItem(_fromUtf8(""))
        self.cmbIsPrimary.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbIsPrimary, 8, 1, 1, 4)
        self.cmbScene = CRBComboBox(PersonVisitsSetupDialog)
        self.cmbScene.setObjectName(_fromUtf8("cmbScene"))
        self.gridlayout.addWidget(self.cmbScene, 9, 1, 1, 4)
        self.lblBegDate = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(111, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 24, 0, 1, 1)
        self.edtEndDate = CDateEdit(PersonVisitsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.lblEventPurpose = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridlayout.addWidget(self.lblEventPurpose, 5, 0, 1, 1)
        self.btnSelectWorkOrganisation = QtGui.QToolButton(PersonVisitsSetupDialog)
        self.btnSelectWorkOrganisation.setArrowType(QtCore.Qt.NoArrow)
        self.btnSelectWorkOrganisation.setObjectName(_fromUtf8("btnSelectWorkOrganisation"))
        self.gridlayout.addWidget(self.btnSelectWorkOrganisation, 10, 4, 1, 1)
        self.cmbPreRecord = QtGui.QComboBox(PersonVisitsSetupDialog)
        self.cmbPreRecord.setObjectName(_fromUtf8("cmbPreRecord"))
        self.gridlayout.addWidget(self.cmbPreRecord, 14, 1, 1, 4)
        self.cmbPerson = CPersonComboBoxEx(PersonVisitsSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbPerson, 4, 1, 1, 4)
        self.cmbEventType = CRBComboBox(PersonVisitsSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridlayout.addWidget(self.cmbEventType, 6, 1, 1, 4)
        self.lblFinance = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridlayout.addWidget(self.lblFinance, 7, 0, 1, 1)
        self.label = QtGui.QLabel(PersonVisitsSetupDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 14, 0, 1, 1)
        self.lblSex = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridlayout.addWidget(self.lblSex, 11, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridlayout.addWidget(self.lblPerson, 4, 0, 1, 1)
        self.lblAge = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridlayout.addWidget(self.lblAge, 12, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridlayout.addWidget(self.lblEventType, 6, 0, 1, 1)
        self.lblWorkOrganisation = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblWorkOrganisation.setObjectName(_fromUtf8("lblWorkOrganisation"))
        self.gridlayout.addWidget(self.lblWorkOrganisation, 10, 0, 1, 1)
        self.cmbFinance = CRBComboBox(PersonVisitsSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridlayout.addWidget(self.cmbFinance, 7, 1, 1, 4)
        self.lblScene = QtGui.QLabel(PersonVisitsSetupDialog)
        self.lblScene.setObjectName(_fromUtf8("lblScene"))
        self.gridlayout.addWidget(self.lblScene, 9, 0, 1, 1)
        self.chkPreliminaryDiagnostics = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkPreliminaryDiagnostics.setObjectName(_fromUtf8("chkPreliminaryDiagnostics"))
        self.gridlayout.addWidget(self.chkPreliminaryDiagnostics, 23, 0, 1, 5)
        self.chkSocStatus = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkSocStatus.setObjectName(_fromUtf8("chkSocStatus"))
        self.gridlayout.addWidget(self.chkSocStatus, 22, 0, 1, 5)
        self.chkWork = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkWork.setObjectName(_fromUtf8("chkWork"))
        self.gridlayout.addWidget(self.chkWork, 21, 0, 1, 5)
        self.chkSNILS = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkSNILS.setObjectName(_fromUtf8("chkSNILS"))
        self.gridlayout.addWidget(self.chkSNILS, 20, 0, 1, 5)
        self.chkDocument = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkDocument.setObjectName(_fromUtf8("chkDocument"))
        self.gridlayout.addWidget(self.chkDocument, 18, 0, 1, 5)
        self.chkPolicy = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkPolicy.setObjectName(_fromUtf8("chkPolicy"))
        self.gridlayout.addWidget(self.chkPolicy, 17, 0, 1, 5)
        self.chkLocAddress = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkLocAddress.setObjectName(_fromUtf8("chkLocAddress"))
        self.gridlayout.addWidget(self.chkLocAddress, 16, 0, 1, 5)
        self.chkRegAddress = QtGui.QCheckBox(PersonVisitsSetupDialog)
        self.chkRegAddress.setObjectName(_fromUtf8("chkRegAddress"))
        self.gridlayout.addWidget(self.chkRegAddress, 15, 0, 1, 5)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEventPurpose.setBuddy(self.cmbPerson)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblEventType.setBuddy(self.cmbPerson)
        self.lblWorkOrganisation.setBuddy(self.cmbWorkOrganisation)
        self.lblScene.setBuddy(self.cmbPerson)

        self.retranslateUi(PersonVisitsSetupDialog)
        self.cmbPreRecord.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PersonVisitsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PersonVisitsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PersonVisitsSetupDialog)
        PersonVisitsSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        PersonVisitsSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        PersonVisitsSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        PersonVisitsSetupDialog.setTabOrder(self.cmbPerson, self.cmbEventPurpose)
        PersonVisitsSetupDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        PersonVisitsSetupDialog.setTabOrder(self.cmbEventType, self.cmbFinance)
        PersonVisitsSetupDialog.setTabOrder(self.cmbFinance, self.cmbIsPrimary)
        PersonVisitsSetupDialog.setTabOrder(self.cmbIsPrimary, self.cmbScene)
        PersonVisitsSetupDialog.setTabOrder(self.cmbScene, self.cmbWorkOrganisation)
        PersonVisitsSetupDialog.setTabOrder(self.cmbWorkOrganisation, self.btnSelectWorkOrganisation)
        PersonVisitsSetupDialog.setTabOrder(self.btnSelectWorkOrganisation, self.cmbSex)
        PersonVisitsSetupDialog.setTabOrder(self.cmbSex, self.edtAgeFrom)
        PersonVisitsSetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        PersonVisitsSetupDialog.setTabOrder(self.edtAgeTo, self.cmbAccountingSystem)
        PersonVisitsSetupDialog.setTabOrder(self.cmbAccountingSystem, self.cmbPreRecord)
        PersonVisitsSetupDialog.setTabOrder(self.cmbPreRecord, self.chkRegAddress)
        PersonVisitsSetupDialog.setTabOrder(self.chkRegAddress, self.chkLocAddress)
        PersonVisitsSetupDialog.setTabOrder(self.chkLocAddress, self.chkPolicy)
        PersonVisitsSetupDialog.setTabOrder(self.chkPolicy, self.chkDocument)
        PersonVisitsSetupDialog.setTabOrder(self.chkDocument, self.chkSNILS)
        PersonVisitsSetupDialog.setTabOrder(self.chkSNILS, self.chkWork)
        PersonVisitsSetupDialog.setTabOrder(self.chkWork, self.chkSocStatus)
        PersonVisitsSetupDialog.setTabOrder(self.chkSocStatus, self.chkPreliminaryDiagnostics)
        PersonVisitsSetupDialog.setTabOrder(self.chkPreliminaryDiagnostics, self.buttonBox)

    def retranslateUi(self, PersonVisitsSetupDialog):
        PersonVisitsSetupDialog.setWindowTitle(_translate("PersonVisitsSetupDialog", "параметры отчёта", None))
        self.cmbSex.setItemText(1, _translate("PersonVisitsSetupDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("PersonVisitsSetupDialog", "Ж", None))
        self.lblAgeTo.setText(_translate("PersonVisitsSetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("PersonVisitsSetupDialog", "лет", None))
        self.lblIsPrimary.setText(_translate("PersonVisitsSetupDialog", "Первичность", None))
        self.lblEndDate.setText(_translate("PersonVisitsSetupDialog", "Дата окончания периода", None))
        self.lblIdentifierType.setText(_translate("PersonVisitsSetupDialog", "Тип идентификатора пациента", None))
        self.lblOrgStructure.setText(_translate("PersonVisitsSetupDialog", "&Подразделение", None))
        self.cmbIsPrimary.setItemText(0, _translate("PersonVisitsSetupDialog", "Не учитывать", None))
        self.cmbIsPrimary.setItemText(1, _translate("PersonVisitsSetupDialog", "Первичные", None))
        self.cmbIsPrimary.setItemText(2, _translate("PersonVisitsSetupDialog", "Повторные", None))
        self.lblBegDate.setText(_translate("PersonVisitsSetupDialog", "Дата начала периода", None))
        self.lblEventPurpose.setText(_translate("PersonVisitsSetupDialog", "&Назначение обращения", None))
        self.btnSelectWorkOrganisation.setText(_translate("PersonVisitsSetupDialog", "...", None))
        self.cmbPerson.setItemText(0, _translate("PersonVisitsSetupDialog", "Врач", None))
        self.lblFinance.setText(_translate("PersonVisitsSetupDialog", "Тип финансирования", None))
        self.label.setText(_translate("PersonVisitsSetupDialog", "По предварительной записи", None))
        self.lblSex.setText(_translate("PersonVisitsSetupDialog", "По&л", None))
        self.lblPerson.setText(_translate("PersonVisitsSetupDialog", "&Врач", None))
        self.lblAge.setText(_translate("PersonVisitsSetupDialog", "Во&зраст с", None))
        self.lblEventType.setText(_translate("PersonVisitsSetupDialog", "&Тип обращения", None))
        self.lblWorkOrganisation.setText(_translate("PersonVisitsSetupDialog", "Занятость", None))
        self.lblScene.setText(_translate("PersonVisitsSetupDialog", "&Место", None))
        self.chkPreliminaryDiagnostics.setText(_translate("PersonVisitsSetupDialog", "Отображать предварительные диагнозы", None))
        self.chkSocStatus.setText(_translate("PersonVisitsSetupDialog", "Соц. статус", None))
        self.chkWork.setText(_translate("PersonVisitsSetupDialog", "Занятость", None))
        self.chkSNILS.setText(_translate("PersonVisitsSetupDialog", "СНИЛС", None))
        self.chkDocument.setText(_translate("PersonVisitsSetupDialog", "Документ, удостоверяющий личность", None))
        self.chkPolicy.setText(_translate("PersonVisitsSetupDialog", "Полис", None))
        self.chkLocAddress.setText(_translate("PersonVisitsSetupDialog", "Адрес проживания", None))
        self.chkRegAddress.setText(_translate("PersonVisitsSetupDialog", "Адрес регистрации", None))

from Orgs.OrgComboBox import COrgComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox