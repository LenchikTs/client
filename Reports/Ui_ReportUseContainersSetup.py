# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportUseContainersSetup.ui'
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

class Ui_ReportUseContainersSetupDialog(object):
    def setupUi(self, ReportUseContainersSetupDialog):
        ReportUseContainersSetupDialog.setObjectName(_fromUtf8("ReportUseContainersSetupDialog"))
        ReportUseContainersSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportUseContainersSetupDialog.resize(465, 164)
        ReportUseContainersSetupDialog.setSizeGripEnabled(True)
        ReportUseContainersSetupDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ReportUseContainersSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 3)
        self.lblBegDate = QtGui.QLabel(ReportUseContainersSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportUseContainersSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportUseContainersSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(ReportUseContainersSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.frmAge = QtGui.QFrame(ReportUseContainersSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 6, 1, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(ReportUseContainersSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(ReportUseContainersSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 6)
        spacerItem2 = QtGui.QSpacerItem(428, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 6)
        self.edtEndDate = CDateEdit(ReportUseContainersSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.btnContainerType = QtGui.QPushButton(ReportUseContainersSetupDialog)
        self.btnContainerType.setObjectName(_fromUtf8("btnContainerType"))
        self.gridLayout.addWidget(self.btnContainerType, 5, 0, 1, 1)
        self.lblContainerType = QtGui.QLabel(ReportUseContainersSetupDialog)
        self.lblContainerType.setWordWrap(True)
        self.lblContainerType.setObjectName(_fromUtf8("lblContainerType"))
        self.gridLayout.addWidget(self.lblContainerType, 5, 1, 1, 5)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportUseContainersSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportUseContainersSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportUseContainersSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportUseContainersSetupDialog)
        ReportUseContainersSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportUseContainersSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        ReportUseContainersSetupDialog.setTabOrder(self.cmbOrgStructure, self.btnContainerType)
        ReportUseContainersSetupDialog.setTabOrder(self.btnContainerType, self.buttonBox)

    def retranslateUi(self, ReportUseContainersSetupDialog):
        ReportUseContainersSetupDialog.setWindowTitle(_translate("ReportUseContainersSetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportUseContainersSetupDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("ReportUseContainersSetupDialog", "Дата &окончания периода", None))
        self.lblOrgStructure.setText(_translate("ReportUseContainersSetupDialog", "Подразделение", None))
        self.btnContainerType.setText(_translate("ReportUseContainersSetupDialog", "Тип контейнера", None))
        self.lblContainerType.setText(_translate("ReportUseContainersSetupDialog", "не задано", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
