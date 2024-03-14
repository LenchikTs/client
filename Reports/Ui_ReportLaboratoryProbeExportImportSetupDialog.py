# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportLaboratoryProbeExportImportSetupDialog.ui'
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

class Ui_ReportLaboratoryProbeExportImportSetupDialog(object):
    def setupUi(self, ReportLaboratoryProbeExportImportSetupDialog):
        ReportLaboratoryProbeExportImportSetupDialog.setObjectName(_fromUtf8("ReportLaboratoryProbeExportImportSetupDialog"))
        ReportLaboratoryProbeExportImportSetupDialog.resize(267, 149)
        self.gridLayout = QtGui.QGridLayout(ReportLaboratoryProbeExportImportSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ReportLaboratoryProbeExportImportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.cmbType = QtGui.QComboBox(ReportLaboratoryProbeExportImportSetupDialog)
        self.cmbType.setObjectName(_fromUtf8("cmbType"))
        self.cmbType.addItem(_fromUtf8(""))
        self.cmbType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbType, 2, 1, 1, 2)
        self.lblGroup = QtGui.QLabel(ReportLaboratoryProbeExportImportSetupDialog)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.gridLayout.addWidget(self.lblGroup, 3, 0, 1, 1)
        self.cmbGroup = QtGui.QComboBox(ReportLaboratoryProbeExportImportSetupDialog)
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.cmbGroup.addItem(_fromUtf8(""))
        self.cmbGroup.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbGroup, 3, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportLaboratoryProbeExportImportSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportLaboratoryProbeExportImportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportLaboratoryProbeExportImportSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportLaboratoryProbeExportImportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblType = QtGui.QLabel(ReportLaboratoryProbeExportImportSetupDialog)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportLaboratoryProbeExportImportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportLaboratoryProbeExportImportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportLaboratoryProbeExportImportSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportLaboratoryProbeExportImportSetupDialog)
        ReportLaboratoryProbeExportImportSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportLaboratoryProbeExportImportSetupDialog.setTabOrder(self.edtEndDate, self.cmbType)
        ReportLaboratoryProbeExportImportSetupDialog.setTabOrder(self.cmbType, self.cmbGroup)
        ReportLaboratoryProbeExportImportSetupDialog.setTabOrder(self.cmbGroup, self.buttonBox)

    def retranslateUi(self, ReportLaboratoryProbeExportImportSetupDialog):
        ReportLaboratoryProbeExportImportSetupDialog.setWindowTitle(_translate("ReportLaboratoryProbeExportImportSetupDialog", "Dialog", None))
        self.cmbType.setItemText(0, _translate("ReportLaboratoryProbeExportImportSetupDialog", "Экспорт", None))
        self.cmbType.setItemText(1, _translate("ReportLaboratoryProbeExportImportSetupDialog", "Импорт", None))
        self.lblGroup.setText(_translate("ReportLaboratoryProbeExportImportSetupDialog", "Группировка", None))
        self.cmbGroup.setItemText(0, _translate("ReportLaboratoryProbeExportImportSetupDialog", "По пациенту", None))
        self.cmbGroup.setItemText(1, _translate("ReportLaboratoryProbeExportImportSetupDialog", "По заказу", None))
        self.lblBegDate.setText(_translate("ReportLaboratoryProbeExportImportSetupDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("ReportLaboratoryProbeExportImportSetupDialog", "Дата &окончания периода", None))
        self.lblType.setText(_translate("ReportLaboratoryProbeExportImportSetupDialog", "Тип", None))

from library.DateEdit import CDateEdit
