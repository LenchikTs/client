# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\DiseasesAnalysisReportSetup.ui'
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

class Ui_DiseasesAnalysisReportSetupDialog(object):
    def setupUi(self, DiseasesAnalysisReportSetupDialog):
        DiseasesAnalysisReportSetupDialog.setObjectName(_fromUtf8("DiseasesAnalysisReportSetupDialog"))
        DiseasesAnalysisReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DiseasesAnalysisReportSetupDialog.resize(439, 149)
        DiseasesAnalysisReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DiseasesAnalysisReportSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(DiseasesAnalysisReportSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.edtBegDate = CDateEdit(DiseasesAnalysisReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(DiseasesAnalysisReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.cmbMKBFilter = QtGui.QComboBox(DiseasesAnalysisReportSetupDialog)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMKBFilter, 3, 2, 1, 1)
        self.lblMKB = QtGui.QLabel(DiseasesAnalysisReportSetupDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 3, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(DiseasesAnalysisReportSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(DiseasesAnalysisReportSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.edtMKBFrom = CICDCodeEdit(DiseasesAnalysisReportSetupDialog)
        self.edtMKBFrom.setEnabled(False)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 3, 3, 1, 1)
        self.edtMKBTo = CICDCodeEdit(DiseasesAnalysisReportSetupDialog)
        self.edtMKBTo.setEnabled(False)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 3, 4, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(DiseasesAnalysisReportSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(DiseasesAnalysisReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 5)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblMKB.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(DiseasesAnalysisReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DiseasesAnalysisReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DiseasesAnalysisReportSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DiseasesAnalysisReportSetupDialog)
        DiseasesAnalysisReportSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        DiseasesAnalysisReportSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        DiseasesAnalysisReportSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, DiseasesAnalysisReportSetupDialog):
        DiseasesAnalysisReportSetupDialog.setWindowTitle(_translate("DiseasesAnalysisReportSetupDialog", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("DiseasesAnalysisReportSetupDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("DiseasesAnalysisReportSetupDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("DiseasesAnalysisReportSetupDialog", "dd.MM.yyyy", None))
        self.cmbMKBFilter.setItemText(0, _translate("DiseasesAnalysisReportSetupDialog", "Игнорировать", None))
        self.cmbMKBFilter.setItemText(1, _translate("DiseasesAnalysisReportSetupDialog", "Диапазон", None))
        self.lblMKB.setText(_translate("DiseasesAnalysisReportSetupDialog", "Коды диагнозов по МКБ", None))
        self.lblEndDate.setText(_translate("DiseasesAnalysisReportSetupDialog", "Дата &окончания периода", None))
        self.lblBegDate.setText(_translate("DiseasesAnalysisReportSetupDialog", "Дата &начала периода", None))
        self.edtMKBFrom.setInputMask(_translate("DiseasesAnalysisReportSetupDialog", "A00.00; ", None))
        self.edtMKBFrom.setText(_translate("DiseasesAnalysisReportSetupDialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("DiseasesAnalysisReportSetupDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("DiseasesAnalysisReportSetupDialog", "Z99.9", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
