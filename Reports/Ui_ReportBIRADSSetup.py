# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportBIRADSSetup.ui'
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

class Ui_ReportBIRADSSetupDialog(object):
    def setupUi(self, ReportBIRADSSetupDialog):
        ReportBIRADSSetupDialog.setObjectName(_fromUtf8("ReportBIRADSSetupDialog"))
        ReportBIRADSSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportBIRADSSetupDialog.resize(544, 298)
        ReportBIRADSSetupDialog.setSizeGripEnabled(True)
        ReportBIRADSSetupDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ReportBIRADSSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrganisation = COrgComboBox(ReportBIRADSSetupDialog)
        self.cmbOrganisation.setObjectName(_fromUtf8("cmbOrganisation"))
        self.gridLayout.addWidget(self.cmbOrganisation, 4, 1, 1, 6)
        spacerItem = QtGui.QSpacerItem(428, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 7)
        self.frmAge = QtGui.QFrame(ReportBIRADSSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 8, 1, 1, 4)
        self.lblPerson = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 6, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportBIRADSSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 0, 1, 7)
        self.lblOrganisation = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblOrganisation.setObjectName(_fromUtf8("lblOrganisation"))
        self.gridLayout.addWidget(self.lblOrganisation, 4, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportBIRADSSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 6, 1, 1, 6)
        self.cmbOrgStructure = COrgStructureComboBox(ReportBIRADSSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 5, 1, 1, 6)
        self.lblOrgStructure = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 5, 0, 1, 1)
        self.lblActionType = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 9, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportBIRADSSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportBIRADSSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.wgtDatePeriodSpacer = QtGui.QWidget(ReportBIRADSSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wgtDatePeriodSpacer.sizePolicy().hasHeightForWidth())
        self.wgtDatePeriodSpacer.setSizePolicy(sizePolicy)
        self.wgtDatePeriodSpacer.setObjectName(_fromUtf8("wgtDatePeriodSpacer"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wgtDatePeriodSpacer)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(194, 7, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.wgtDatePeriodSpacer, 0, 3, 1, 4)
        self.chkClientDetail = QtGui.QCheckBox(ReportBIRADSSetupDialog)
        self.chkClientDetail.setObjectName(_fromUtf8("chkClientDetail"))
        self.gridLayout.addWidget(self.chkClientDetail, 11, 1, 1, 6)
        self.cmbActionType = CActionTypeComboBoxEx(ReportBIRADSSetupDialog)
        self.cmbActionType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 9, 1, 1, 6)
        self.lblEventType = QtGui.QLabel(ReportBIRADSSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 10, 0, 1, 1)
        self.cmbEventType = CRBComboBox(ReportBIRADSSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 10, 1, 1, 6)
        self.lblActionType.setBuddy(self.cmbActionType)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportBIRADSSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportBIRADSSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportBIRADSSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportBIRADSSetupDialog)
        ReportBIRADSSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportBIRADSSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrganisation)
        ReportBIRADSSetupDialog.setTabOrder(self.cmbOrganisation, self.cmbOrgStructure)
        ReportBIRADSSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        ReportBIRADSSetupDialog.setTabOrder(self.cmbPerson, self.cmbActionType)
        ReportBIRADSSetupDialog.setTabOrder(self.cmbActionType, self.cmbEventType)
        ReportBIRADSSetupDialog.setTabOrder(self.cmbEventType, self.chkClientDetail)
        ReportBIRADSSetupDialog.setTabOrder(self.chkClientDetail, self.buttonBox)

    def retranslateUi(self, ReportBIRADSSetupDialog):
        ReportBIRADSSetupDialog.setWindowTitle(_translate("ReportBIRADSSetupDialog", "параметры отчёта", None))
        self.lblPerson.setText(_translate("ReportBIRADSSetupDialog", "Врач", None))
        self.lblOrganisation.setText(_translate("ReportBIRADSSetupDialog", "ЛПУ", None))
        self.lblOrgStructure.setText(_translate("ReportBIRADSSetupDialog", "Подразделение", None))
        self.lblActionType.setText(_translate("ReportBIRADSSetupDialog", "&Мероприятие", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportBIRADSSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportBIRADSSetupDialog", "Дата &начала периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportBIRADSSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportBIRADSSetupDialog", "Дата &окончания периода", None))
        self.chkClientDetail.setText(_translate("ReportBIRADSSetupDialog", "Детализация по ФИО с кодом пациента", None))
        self.lblEventType.setText(_translate("ReportBIRADSSetupDialog", "Тип события", None))

from Events.ActionTypeComboBoxEx import CActionTypeComboBoxEx
from Orgs.OrgComboBox import COrgComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
