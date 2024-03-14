# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AnaliticReportsChildrenLeaved.ui'
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

class Ui_AnaliticReportsChildrenLeavedDialog(object):
    def setupUi(self, AnaliticReportsChildrenLeavedDialog):
        AnaliticReportsChildrenLeavedDialog.setObjectName(_fromUtf8("AnaliticReportsChildrenLeavedDialog"))
        AnaliticReportsChildrenLeavedDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AnaliticReportsChildrenLeavedDialog.resize(435, 157)
        AnaliticReportsChildrenLeavedDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(AnaliticReportsChildrenLeavedDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(AnaliticReportsChildrenLeavedDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AnaliticReportsChildrenLeavedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(AnaliticReportsChildrenLeavedDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(AnaliticReportsChildrenLeavedDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(AnaliticReportsChildrenLeavedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(AnaliticReportsChildrenLeavedDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(AnaliticReportsChildrenLeavedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 2)
        self.lblProfileBed = QtGui.QLabel(AnaliticReportsChildrenLeavedDialog)
        self.lblProfileBed.setObjectName(_fromUtf8("lblProfileBed"))
        self.gridLayout.addWidget(self.lblProfileBed, 3, 0, 1, 1)
        self.cmbProfileBed = CRBComboBox(AnaliticReportsChildrenLeavedDialog)
        self.cmbProfileBed.setObjectName(_fromUtf8("cmbProfileBed"))
        self.gridLayout.addWidget(self.cmbProfileBed, 3, 1, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(AnaliticReportsChildrenLeavedDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnaliticReportsChildrenLeavedDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnaliticReportsChildrenLeavedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnaliticReportsChildrenLeavedDialog)
        AnaliticReportsChildrenLeavedDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        AnaliticReportsChildrenLeavedDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        AnaliticReportsChildrenLeavedDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, AnaliticReportsChildrenLeavedDialog):
        AnaliticReportsChildrenLeavedDialog.setWindowTitle(_translate("AnaliticReportsChildrenLeavedDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("AnaliticReportsChildrenLeavedDialog", "Дата &начала периода", None))
        self.lblOrgStructure.setText(_translate("AnaliticReportsChildrenLeavedDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("AnaliticReportsChildrenLeavedDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("AnaliticReportsChildrenLeavedDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("AnaliticReportsChildrenLeavedDialog", "dd.MM.yyyy", None))
        self.lblProfileBed.setText(_translate("AnaliticReportsChildrenLeavedDialog", "Профиль", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
