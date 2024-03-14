# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StatReportF12SetupDialog.ui'
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

class Ui_StatReportF12SetupDialog(object):
    def setupUi(self, StatReportF12SetupDialog):
        StatReportF12SetupDialog.setObjectName(_fromUtf8("StatReportF12SetupDialog"))
        StatReportF12SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StatReportF12SetupDialog.resize(412, 197)
        StatReportF12SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StatReportF12SetupDialog)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtBegDate = CDateEdit(StatReportF12SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.frmMKBEx = QtGui.QFrame(StatReportF12SetupDialog)
        self.frmMKBEx.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKBEx.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKBEx.setObjectName(_fromUtf8("frmMKBEx"))
        self._2 = QtGui.QGridLayout(self.frmMKBEx)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout.addWidget(self.frmMKBEx, 10, 1, 1, 3)
        self.frmMKB = QtGui.QFrame(StatReportF12SetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self.gridlayout = QtGui.QGridLayout(self.frmMKB)
        self.gridlayout.setMargin(0)
        self.gridlayout.setHorizontalSpacing(4)
        self.gridlayout.setVerticalSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.gridLayout.addWidget(self.frmMKB, 9, 1, 1, 3)
        self.frmAge = QtGui.QFrame(StatReportF12SetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 8, 1, 1, 3)
        self.lblFinance = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 131, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 17, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 7, 0, 1, 1)
        self.edtEndDate = CDateEdit(StatReportF12SetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StatReportF12SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 18, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 2)
        self.lblEventPurpose = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 3, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 6, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 5, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(StatReportF12SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.cmbFinance = CRBComboBox(StatReportF12SetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 2, 1, 1, 3)
        self.cmbEventPurpose = CRBComboBox(StatReportF12SetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 3, 1, 1, 3)
        self.cmbEventType = CRBComboBox(StatReportF12SetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 5, 1, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(StatReportF12SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 6, 1, 1, 3)
        self.cmbPerson = CPersonComboBoxEx(StatReportF12SetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPerson, 7, 1, 1, 3)
        self.lblFinance.setBuddy(self.cmbEventType)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(StatReportF12SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StatReportF12SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StatReportF12SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StatReportF12SetupDialog)
        StatReportF12SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        StatReportF12SetupDialog.setTabOrder(self.edtEndDate, self.cmbEventPurpose)
        StatReportF12SetupDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        StatReportF12SetupDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        StatReportF12SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        StatReportF12SetupDialog.setTabOrder(self.cmbPerson, self.buttonBox)

    def retranslateUi(self, StatReportF12SetupDialog):
        StatReportF12SetupDialog.setWindowTitle(_translate("StatReportF12SetupDialog", "параметры отчёта", None))
        self.lblFinance.setText(_translate("StatReportF12SetupDialog", "Тип финансирования", None))
        self.lblPerson.setText(_translate("StatReportF12SetupDialog", "&Врач", None))
        self.lblEventPurpose.setText(_translate("StatReportF12SetupDialog", "&Назначение обращения", None))
        self.lblOrgStructure.setText(_translate("StatReportF12SetupDialog", "&Подразделение", None))
        self.lblEventType.setText(_translate("StatReportF12SetupDialog", "&Тип обращения", None))
        self.lblEndDate.setText(_translate("StatReportF12SetupDialog", "Дата &окончания периода", None))
        self.lblBegDate.setText(_translate("StatReportF12SetupDialog", "Дата &начала периода", None))
        self.cmbPerson.setItemText(0, _translate("StatReportF12SetupDialog", "Врач", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
