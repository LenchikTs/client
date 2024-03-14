# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\LengthOfStayReportSetupDialog.ui'
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

class Ui_CLengthOfStayReportSetup(object):
    def setupUi(self, CLengthOfStayReportSetup):
        CLengthOfStayReportSetup.setObjectName(_fromUtf8("CLengthOfStayReportSetup"))
        CLengthOfStayReportSetup.setWindowModality(QtCore.Qt.ApplicationModal)
        CLengthOfStayReportSetup.resize(345, 142)
        CLengthOfStayReportSetup.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(CLengthOfStayReportSetup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(CLengthOfStayReportSetup)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(CLengthOfStayReportSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(CLengthOfStayReportSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.edtBegDate = CDateEdit(CLengthOfStayReportSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(CLengthOfStayReportSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(CLengthOfStayReportSetup)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(CLengthOfStayReportSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.chkClientMoving = QtGui.QCheckBox(CLengthOfStayReportSetup)
        self.chkClientMoving.setObjectName(_fromUtf8("chkClientMoving"))
        self.gridLayout.addWidget(self.chkClientMoving, 3, 0, 1, 4)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(CLengthOfStayReportSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CLengthOfStayReportSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CLengthOfStayReportSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(CLengthOfStayReportSetup)
        CLengthOfStayReportSetup.setTabOrder(self.edtBegDate, self.edtEndDate)
        CLengthOfStayReportSetup.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        CLengthOfStayReportSetup.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, CLengthOfStayReportSetup):
        CLengthOfStayReportSetup.setWindowTitle(_translate("CLengthOfStayReportSetup", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("CLengthOfStayReportSetup", "&Подразделение", None))
        self.lblEndDate.setText(_translate("CLengthOfStayReportSetup", "Дата &окончания периода", None))
        self.lblBegDate.setText(_translate("CLengthOfStayReportSetup", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("CLengthOfStayReportSetup", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("CLengthOfStayReportSetup", "dd.MM.yyyy", None))
        self.chkClientMoving.setText(_translate("CLengthOfStayReportSetup", "учитывать переводы пациента", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
