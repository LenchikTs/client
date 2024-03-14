# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\DateAndOrgStructureSetupDialog.ui'
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

class Ui_DateAndOrgStructureSetupDialog(object):
    def setupUi(self, DateAndOrgStructureSetupDialog):
        DateAndOrgStructureSetupDialog.setObjectName(_fromUtf8("DateAndOrgStructureSetupDialog"))
        DateAndOrgStructureSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DateAndOrgStructureSetupDialog.resize(326, 120)
        DateAndOrgStructureSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DateAndOrgStructureSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrgStructure = COrgStructureComboBox(DateAndOrgStructureSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 3)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.edtBegDate = CDateEdit(DateAndOrgStructureSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(DateAndOrgStructureSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(DateAndOrgStructureSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(DateAndOrgStructureSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(DateAndOrgStructureSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 5)
        self.edtEndDate = CDateEdit(DateAndOrgStructureSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(DateAndOrgStructureSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(DateAndOrgStructureSetupDialog)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(DateAndOrgStructureSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DateAndOrgStructureSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DateAndOrgStructureSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DateAndOrgStructureSetupDialog)
        DateAndOrgStructureSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        DateAndOrgStructureSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        DateAndOrgStructureSetupDialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        DateAndOrgStructureSetupDialog.setTabOrder(self.edtEndTime, self.cmbOrgStructure)
        DateAndOrgStructureSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, DateAndOrgStructureSetupDialog):
        DateAndOrgStructureSetupDialog.setWindowTitle(_translate("DateAndOrgStructureSetupDialog", "параметры отчёта", None))
        self.edtBegDate.setDisplayFormat(_translate("DateAndOrgStructureSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("DateAndOrgStructureSetupDialog", "Дата &начала периода", None))
        self.lblOrgStructure.setText(_translate("DateAndOrgStructureSetupDialog", "&Подразделение", None))
        self.lblEndDate.setText(_translate("DateAndOrgStructureSetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("DateAndOrgStructureSetupDialog", "dd.MM.yyyy", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
