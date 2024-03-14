# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportUniversalEventListSetupDialog.ui'
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

class Ui_ReportUniversalEventListSetupDialog(object):
    def setupUi(self, ReportUniversalEventListSetupDialog):
        ReportUniversalEventListSetupDialog.setObjectName(_fromUtf8("ReportUniversalEventListSetupDialog"))
        ReportUniversalEventListSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportUniversalEventListSetupDialog.resize(694, 484)
        ReportUniversalEventListSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportUniversalEventListSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportUniversalEventListSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportUniversalEventListSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.lblEventPurpose = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 2, 0, 1, 1)
        self.cmbEventPurpose = CRBComboBox(ReportUniversalEventListSetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 2, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportUniversalEventListSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 2)
        self.lblSpeciality = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 4, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(ReportUniversalEventListSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 4, 1, 1, 2)
        self.lblPerson = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportUniversalEventListSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 2)
        self.lblFinance = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 6, 0, 1, 1)
        self.cmbFinance = CRBComboBox(ReportUniversalEventListSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 6, 1, 1, 2)
        self.lblVisitPayStatus = QtGui.QLabel(ReportUniversalEventListSetupDialog)
        self.lblVisitPayStatus.setObjectName(_fromUtf8("lblVisitPayStatus"))
        self.gridLayout.addWidget(self.lblVisitPayStatus, 7, 0, 1, 1)
        self.cmbVisitPayStatus = QtGui.QComboBox(ReportUniversalEventListSetupDialog)
        self.cmbVisitPayStatus.setObjectName(_fromUtf8("cmbVisitPayStatus"))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbVisitPayStatus, 7, 1, 1, 2)
        self.tblEventType = CTableView(ReportUniversalEventListSetupDialog)
        self.tblEventType.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblEventType.setObjectName(_fromUtf8("tblEventType"))
        self.gridLayout.addWidget(self.tblEventType, 8, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ReportUniversalEventListSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(ReportUniversalEventListSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportUniversalEventListSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportUniversalEventListSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportUniversalEventListSetupDialog)
        ReportUniversalEventListSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportUniversalEventListSetupDialog.setTabOrder(self.edtEndDate, self.cmbEventPurpose)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbEventPurpose, self.cmbOrgStructure)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbPerson, self.cmbFinance)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbFinance, self.cmbVisitPayStatus)
        ReportUniversalEventListSetupDialog.setTabOrder(self.cmbVisitPayStatus, self.tblEventType)
        ReportUniversalEventListSetupDialog.setTabOrder(self.tblEventType, self.buttonBox)

    def retranslateUi(self, ReportUniversalEventListSetupDialog):
        ReportUniversalEventListSetupDialog.setWindowTitle(_translate("ReportUniversalEventListSetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportUniversalEventListSetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportUniversalEventListSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportUniversalEventListSetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportUniversalEventListSetupDialog", "dd.MM.yyyy", None))
        self.lblEventPurpose.setText(_translate("ReportUniversalEventListSetupDialog", "&Назначение обращения", None))
        self.cmbEventPurpose.setWhatsThis(_translate("ReportUniversalEventListSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblOrgStructure.setText(_translate("ReportUniversalEventListSetupDialog", "&Подразделение", None))
        self.lblSpeciality.setText(_translate("ReportUniversalEventListSetupDialog", "&Специальность", None))
        self.cmbSpeciality.setWhatsThis(_translate("ReportUniversalEventListSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblPerson.setText(_translate("ReportUniversalEventListSetupDialog", "&Врач", None))
        self.cmbPerson.setWhatsThis(_translate("ReportUniversalEventListSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.cmbPerson.setItemText(0, _translate("ReportUniversalEventListSetupDialog", "Врач", None))
        self.lblFinance.setText(_translate("ReportUniversalEventListSetupDialog", "Тип финансирования", None))
        self.lblVisitPayStatus.setText(_translate("ReportUniversalEventListSetupDialog", "Флаг финансирования", None))
        self.cmbVisitPayStatus.setItemText(0, _translate("ReportUniversalEventListSetupDialog", "не задано", None))
        self.cmbVisitPayStatus.setItemText(1, _translate("ReportUniversalEventListSetupDialog", "не выставлено", None))
        self.cmbVisitPayStatus.setItemText(2, _translate("ReportUniversalEventListSetupDialog", "выставлено", None))
        self.cmbVisitPayStatus.setItemText(3, _translate("ReportUniversalEventListSetupDialog", "отказано", None))
        self.cmbVisitPayStatus.setItemText(4, _translate("ReportUniversalEventListSetupDialog", "оплачено", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox
