# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportOnPersonSetupDialog.ui'
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

class Ui_ReportOnPersonSetupDialog(object):
    def setupUi(self, ReportOnPersonSetupDialog):
        ReportOnPersonSetupDialog.setObjectName(_fromUtf8("ReportOnPersonSetupDialog"))
        ReportOnPersonSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportOnPersonSetupDialog.resize(483, 298)
        ReportOnPersonSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportOnPersonSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEndDate = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.lblSpec = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblSpec.setObjectName(_fromUtf8("lblSpec"))
        self.gridLayout.addWidget(self.lblSpec, 4, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportOnPersonSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(111, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 9, 0, 1, 3)
        self.edtBegDate = CDateEdit(ReportOnPersonSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(ReportOnPersonSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 4, 1, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(ReportOnPersonSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ReportOnPersonSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 3)
        self.cmbIdentifierType = QtGui.QComboBox(ReportOnPersonSetupDialog)
        self.cmbIdentifierType.setObjectName(_fromUtf8("cmbIdentifierType"))
        self.cmbIdentifierType.addItem(_fromUtf8(""))
        self.cmbIdentifierType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbIdentifierType, 7, 1, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(ReportOnPersonSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.chkIncludeTime = QtGui.QCheckBox(ReportOnPersonSetupDialog)
        self.chkIncludeTime.setObjectName(_fromUtf8("chkIncludeTime"))
        self.gridLayout.addWidget(self.chkIncludeTime, 8, 1, 1, 2)
        self.lblIdentifierType = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblIdentifierType.setObjectName(_fromUtf8("lblIdentifierType"))
        self.gridLayout.addWidget(self.lblIdentifierType, 7, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        self.cmbEventType = CRBComboBox(ReportOnPersonSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 2)
        self.cmbFinance = CRBComboBox(ReportOnPersonSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 6, 1, 1, 2)
        self.lblFinance = QtGui.QLabel(ReportOnPersonSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 6, 0, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblSpec.setBuddy(self.cmbPerson)
        self.lblOrgStructure.setBuddy(self.cmbPerson)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportOnPersonSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportOnPersonSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportOnPersonSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportOnPersonSetupDialog)
        ReportOnPersonSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportOnPersonSetupDialog.setTabOrder(self.edtEndDate, self.cmbEventType)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbPerson, self.cmbFinance)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbFinance, self.cmbIdentifierType)
        ReportOnPersonSetupDialog.setTabOrder(self.cmbIdentifierType, self.chkIncludeTime)
        ReportOnPersonSetupDialog.setTabOrder(self.chkIncludeTime, self.buttonBox)

    def retranslateUi(self, ReportOnPersonSetupDialog):
        ReportOnPersonSetupDialog.setWindowTitle(_translate("ReportOnPersonSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("ReportOnPersonSetupDialog", "Дата окончания периода", None))
        self.lblPerson.setText(_translate("ReportOnPersonSetupDialog", "&Врач", None))
        self.lblSpec.setText(_translate("ReportOnPersonSetupDialog", "Специальность", None))
        self.lblOrgStructure.setText(_translate("ReportOnPersonSetupDialog", "Подразделение", None))
        self.cmbSpeciality.setWhatsThis(_translate("ReportOnPersonSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.cmbIdentifierType.setItemText(0, _translate("ReportOnPersonSetupDialog", "Идентификатор клиента", None))
        self.cmbIdentifierType.setItemText(1, _translate("ReportOnPersonSetupDialog", "Идентификатор во внешней учётной системе", None))
        self.cmbPerson.setItemText(0, _translate("ReportOnPersonSetupDialog", "Врач", None))
        self.lblBegDate.setText(_translate("ReportOnPersonSetupDialog", "Дата начала периода", None))
        self.chkIncludeTime.setText(_translate("ReportOnPersonSetupDialog", "Выводить время приема", None))
        self.lblIdentifierType.setText(_translate("ReportOnPersonSetupDialog", "Тип идентификатора", None))
        self.lblEventType.setText(_translate("ReportOnPersonSetupDialog", "Тип события", None))
        self.lblFinance.setText(_translate("ReportOnPersonSetupDialog", "Тип финансирования", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
