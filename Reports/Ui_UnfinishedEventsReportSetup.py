# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\UnfinishedEventsReportSetup.ui'
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

class Ui_UnfinishedEventsReportSetupDialog(object):
    def setupUi(self, UnfinishedEventsReportSetupDialog):
        UnfinishedEventsReportSetupDialog.setObjectName(_fromUtf8("UnfinishedEventsReportSetupDialog"))
        UnfinishedEventsReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        UnfinishedEventsReportSetupDialog.resize(376, 272)
        UnfinishedEventsReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(UnfinishedEventsReportSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(129, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(UnfinishedEventsReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.edtEndDate = CDateEdit(UnfinishedEventsReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEventPurpose = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 2, 0, 1, 1)
        self.cmbEventPurpose = CRBComboBox(UnfinishedEventsReportSetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 2, 1, 1, 2)
        self.lblEventType = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 3, 0, 1, 1)
        self.cmbEventType = CRBComboBox(UnfinishedEventsReportSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 3, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(UnfinishedEventsReportSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 2)
        self.lblSpeciality = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 5, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(UnfinishedEventsReportSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 5, 1, 1, 2)
        self.lblPerson = QtGui.QLabel(UnfinishedEventsReportSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 6, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(UnfinishedEventsReportSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 6, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(UnfinishedEventsReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 3)
        self.chkDetailEventType = QtGui.QCheckBox(UnfinishedEventsReportSetupDialog)
        self.chkDetailEventType.setChecked(True)
        self.chkDetailEventType.setObjectName(_fromUtf8("chkDetailEventType"))
        self.gridLayout.addWidget(self.chkDetailEventType, 7, 1, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(UnfinishedEventsReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UnfinishedEventsReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UnfinishedEventsReportSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UnfinishedEventsReportSetupDialog)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.edtEndDate, self.cmbEventPurpose)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.cmbPerson, self.chkDetailEventType)
        UnfinishedEventsReportSetupDialog.setTabOrder(self.chkDetailEventType, self.buttonBox)

    def retranslateUi(self, UnfinishedEventsReportSetupDialog):
        UnfinishedEventsReportSetupDialog.setWindowTitle(_translate("UnfinishedEventsReportSetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("UnfinishedEventsReportSetupDialog", "Дата начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("UnfinishedEventsReportSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("UnfinishedEventsReportSetupDialog", "Дата окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("UnfinishedEventsReportSetupDialog", "dd.MM.yyyy", None))
        self.lblEventPurpose.setText(_translate("UnfinishedEventsReportSetupDialog", "&Назначение обращения", None))
        self.lblEventType.setText(_translate("UnfinishedEventsReportSetupDialog", "&Тип обращения", None))
        self.lblOrgStructure.setText(_translate("UnfinishedEventsReportSetupDialog", "&Подразделение", None))
        self.lblSpeciality.setText(_translate("UnfinishedEventsReportSetupDialog", "&Специальность", None))
        self.cmbSpeciality.setWhatsThis(_translate("UnfinishedEventsReportSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblPerson.setText(_translate("UnfinishedEventsReportSetupDialog", "&Врач", None))
        self.chkDetailEventType.setText(_translate("UnfinishedEventsReportSetupDialog", "Детализация по Типам Событий", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
