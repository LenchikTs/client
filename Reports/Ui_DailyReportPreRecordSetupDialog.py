# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\DailyReportPreRecordSetupDialog.ui'
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

class Ui_DailyReportPreRecordSetupDialog(object):
    def setupUi(self, DailyReportPreRecordSetupDialog):
        DailyReportPreRecordSetupDialog.setObjectName(_fromUtf8("DailyReportPreRecordSetupDialog"))
        DailyReportPreRecordSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DailyReportPreRecordSetupDialog.resize(382, 128)
        DailyReportPreRecordSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DailyReportPreRecordSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(DailyReportPreRecordSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.edtBegDate = CDateEdit(DailyReportPreRecordSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.lblEndDate = QtGui.QLabel(DailyReportPreRecordSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.edtEndDate = CDateEdit(DailyReportPreRecordSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 1, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(DailyReportPreRecordSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(DailyReportPreRecordSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(DailyReportPreRecordSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(DailyReportPreRecordSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DailyReportPreRecordSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DailyReportPreRecordSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DailyReportPreRecordSetupDialog)
        DailyReportPreRecordSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        DailyReportPreRecordSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        DailyReportPreRecordSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, DailyReportPreRecordSetupDialog):
        DailyReportPreRecordSetupDialog.setWindowTitle(_translate("DailyReportPreRecordSetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("DailyReportPreRecordSetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("DailyReportPreRecordSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("DailyReportPreRecordSetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("DailyReportPreRecordSetupDialog", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("DailyReportPreRecordSetupDialog", "&Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
