# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\DeathReportByZonesSetup.ui'
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

class Ui_DeathReportByZonesSetupDialog(object):
    def setupUi(self, DeathReportByZonesSetupDialog):
        DeathReportByZonesSetupDialog.setObjectName(_fromUtf8("DeathReportByZonesSetupDialog"))
        DeathReportByZonesSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DeathReportByZonesSetupDialog.resize(347, 110)
        DeathReportByZonesSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(DeathReportByZonesSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(DeathReportByZonesSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.lblEndDate = QtGui.QLabel(DeathReportByZonesSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(DeathReportByZonesSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblorgStructure = QtGui.QLabel(DeathReportByZonesSetupDialog)
        self.lblorgStructure.setObjectName(_fromUtf8("lblorgStructure"))
        self.gridlayout.addWidget(self.lblorgStructure, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.edtBegDate = CDateEdit(DeathReportByZonesSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.edtEndDate = CDateEdit(DeathReportByZonesSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(DeathReportByZonesSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridlayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 2)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(DeathReportByZonesSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DeathReportByZonesSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DeathReportByZonesSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DeathReportByZonesSetupDialog)
        DeathReportByZonesSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        DeathReportByZonesSetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, DeathReportByZonesSetupDialog):
        DeathReportByZonesSetupDialog.setWindowTitle(_translate("DeathReportByZonesSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("DeathReportByZonesSetupDialog", "Дата окончания периода", None))
        self.lblBegDate.setText(_translate("DeathReportByZonesSetupDialog", "Дата начала периода", None))
        self.lblorgStructure.setText(_translate("DeathReportByZonesSetupDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
