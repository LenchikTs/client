# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportBreachSASetup.ui'
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

class Ui_ReportBreachSASetupDialog(object):
    def setupUi(self, ReportBreachSASetupDialog):
        ReportBreachSASetupDialog.setObjectName(_fromUtf8("ReportBreachSASetupDialog"))
        ReportBreachSASetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportBreachSASetupDialog.resize(376, 169)
        ReportBreachSASetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportBreachSASetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBreachName = QtGui.QLabel(ReportBreachSASetupDialog)
        self.lblBreachName.setObjectName(_fromUtf8("lblBreachName"))
        self.gridLayout.addWidget(self.lblBreachName, 5, 0, 1, 1)
        self.lblBreachDays = QtGui.QLabel(ReportBreachSASetupDialog)
        self.lblBreachDays.setObjectName(_fromUtf8("lblBreachDays"))
        self.gridLayout.addWidget(self.lblBreachDays, 5, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportBreachSASetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportBreachSASetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportBreachSASetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportBreachSASetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 4)
        self.edtBegDate = CDateEdit(ReportBreachSASetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportBreachSASetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportBreachSASetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.edtBreachDays = QtGui.QSpinBox(ReportBreachSASetupDialog)
        self.edtBreachDays.setMinimum(1)
        self.edtBreachDays.setMaximum(367)
        self.edtBreachDays.setObjectName(_fromUtf8("edtBreachDays"))
        self.gridLayout.addWidget(self.edtBreachDays, 5, 1, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportBreachSASetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportBreachSASetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportBreachSASetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportBreachSASetupDialog)
        ReportBreachSASetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportBreachSASetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        ReportBreachSASetupDialog.setTabOrder(self.cmbOrgStructure, self.edtBreachDays)
        ReportBreachSASetupDialog.setTabOrder(self.edtBreachDays, self.buttonBox)

    def retranslateUi(self, ReportBreachSASetupDialog):
        ReportBreachSASetupDialog.setWindowTitle(_translate("ReportBreachSASetupDialog", "параметры отчёта", None))
        self.lblBreachName.setText(_translate("ReportBreachSASetupDialog", "Нарушение сроков ожидания >=", None))
        self.lblBreachDays.setText(_translate("ReportBreachSASetupDialog", "дней", None))
        self.lblBegDate.setText(_translate("ReportBreachSASetupDialog", "Дата &начала периода", None))
        self.lblOrgStructure.setText(_translate("ReportBreachSASetupDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportBreachSASetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportBreachSASetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportBreachSASetupDialog", "dd.MM.yyyy", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
