# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ExportR60NativeAmbulancePage1.ui'
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

class Ui_ExportPage1(object):
    def setupUi(self, ExportPage1):
        ExportPage1.setObjectName(_fromUtf8("ExportPage1"))
        ExportPage1.resize(435, 417)
        self.gridlayout = QtGui.QGridLayout(ExportPage1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 5)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportPage1)
        self.chkIgnoreErrors.setEnabled(False)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.gridlayout.addWidget(self.chkIgnoreErrors, 2, 0, 1, 1)
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 11, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 14, 0, 1, 5)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 10, 0, 1, 5)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridlayout.addWidget(self.chkVerboseLog, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblRevision = QtGui.QLabel(ExportPage1)
        self.lblRevision.setEnabled(False)
        self.lblRevision.setText(_fromUtf8(""))
        self.lblRevision.setObjectName(_fromUtf8("lblRevision"))
        self.horizontalLayout.addWidget(self.lblRevision)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout.addWidget(self.btnExport)
        self.gridlayout.addLayout(self.horizontalLayout, 13, 0, 1, 5)
        self.lblElapsed = QtGui.QLabel(ExportPage1)
        self.lblElapsed.setText(_fromUtf8(""))
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.gridlayout.addWidget(self.lblElapsed, 12, 0, 1, 5)
        self.lblRegistryType = QtGui.QLabel(ExportPage1)
        self.lblRegistryType.setObjectName(_fromUtf8("lblRegistryType"))
        self.gridlayout.addWidget(self.lblRegistryType, 8, 0, 1, 1)
        self.cmbRegistryType = QtGui.QComboBox(ExportPage1)
        self.cmbRegistryType.setObjectName(_fromUtf8("cmbRegistryType"))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbRegistryType, 8, 1, 1, 4)
        self.lblPacketNumber = QtGui.QLabel(ExportPage1)
        self.lblPacketNumber.setObjectName(_fromUtf8("lblPacketNumber"))
        self.gridlayout.addWidget(self.lblPacketNumber, 9, 0, 1, 1)
        self.edtPacketNumber = QtGui.QSpinBox(ExportPage1)
        self.edtPacketNumber.setObjectName(_fromUtf8("edtPacketNumber"))
        self.gridlayout.addWidget(self.edtPacketNumber, 9, 1, 1, 4)
        self.chkAmbulancePlanComplete = QtGui.QCheckBox(ExportPage1)
        self.chkAmbulancePlanComplete.setObjectName(_fromUtf8("chkAmbulancePlanComplete"))
        self.gridlayout.addWidget(self.chkAmbulancePlanComplete, 3, 0, 1, 5)
        self.chkEmergencyPlanComplete = QtGui.QCheckBox(ExportPage1)
        self.chkEmergencyPlanComplete.setObjectName(_fromUtf8("chkEmergencyPlanComplete"))
        self.gridlayout.addWidget(self.chkEmergencyPlanComplete, 4, 0, 1, 5)
        self.chkReexposed = QtGui.QCheckBox(ExportPage1)
        self.chkReexposed.setObjectName(_fromUtf8("chkReexposed"))
        self.gridlayout.addWidget(self.chkReexposed, 7, 0, 1, 1)
        self.chkAdditionalSumOfPCF = QtGui.QCheckBox(ExportPage1)
        self.chkAdditionalSumOfPCF.setObjectName(_fromUtf8("chkAdditionalSumOfPCF"))
        self.gridlayout.addWidget(self.chkAdditionalSumOfPCF, 5, 0, 1, 5)
        self.edtAdditionalSumOfPCF = QtGui.QDoubleSpinBox(ExportPage1)
        self.edtAdditionalSumOfPCF.setEnabled(False)
        self.edtAdditionalSumOfPCF.setMaximum(999999999.99)
        self.edtAdditionalSumOfPCF.setObjectName(_fromUtf8("edtAdditionalSumOfPCF"))
        self.gridlayout.addWidget(self.edtAdditionalSumOfPCF, 6, 1, 1, 4)

        self.retranslateUi(ExportPage1)
        QtCore.QObject.connect(self.chkAdditionalSumOfPCF, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtAdditionalSumOfPCF.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(_translate("ExportPage1", "Form", None))
        self.chkIgnoreErrors.setText(_translate("ExportPage1", "Игнорировать ошибки", None))
        self.chkVerboseLog.setText(_translate("ExportPage1", "Подробный отчет", None))
        self.btnCancel.setText(_translate("ExportPage1", "прервать", None))
        self.btnExport.setText(_translate("ExportPage1", "экспорт", None))
        self.lblRegistryType.setText(_translate("ExportPage1", "Тип реестра", None))
        self.cmbRegistryType.setItemText(0, _translate("ExportPage1", "ИСП или ФЛК", None))
        self.cmbRegistryType.setItemText(1, _translate("ExportPage1", "оплата", None))
        self.lblPacketNumber.setText(_translate("ExportPage1", "Номер пакета", None))
        self.chkAmbulancePlanComplete.setText(_translate("ExportPage1", "План по амбулаторным посещениям выполнен", None))
        self.chkEmergencyPlanComplete.setText(_translate("ExportPage1", "План по вызовам СМП выполнен", None))
        self.chkReexposed.setText(_translate("ExportPage1", "Повторное выставление", None))
        self.chkAdditionalSumOfPCF.setText(_translate("ExportPage1", "Дополнительная сумма с учетом показателей результативности", None))

from library.ProgressBar import CProgressBar
