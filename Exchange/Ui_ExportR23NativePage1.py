# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportR23NativePage1.ui'
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

class Ui_ExportR23NativePage1(object):
    def setupUi(self, ExportR23NativePage1):
        ExportR23NativePage1.setObjectName(_fromUtf8("ExportR23NativePage1"))
        ExportR23NativePage1.resize(682, 453)
        self.gridLayout = QtGui.QGridLayout(ExportR23NativePage1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblRegistryNumber = QtGui.QLabel(ExportR23NativePage1)
        self.lblRegistryNumber.setObjectName(_fromUtf8("lblRegistryNumber"))
        self.gridLayout.addWidget(self.lblRegistryNumber, 2, 0, 1, 2)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportR23NativePage1)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.gridLayout.addWidget(self.chkIgnoreErrors, 4, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 4, 1, 1)
        self.lblExportType = QtGui.QLabel(ExportR23NativePage1)
        self.lblExportType.setObjectName(_fromUtf8("lblExportType"))
        self.gridLayout.addWidget(self.lblExportType, 1, 0, 1, 2)
        self.lblElapsed = QtGui.QLabel(ExportR23NativePage1)
        self.lblElapsed.setText(_fromUtf8(""))
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.gridLayout.addWidget(self.lblElapsed, 9, 0, 1, 1)
        self.cmbExportType = QtGui.QComboBox(ExportR23NativePage1)
        self.cmbExportType.setObjectName(_fromUtf8("cmbExportType"))
        self.gridLayout.addWidget(self.cmbExportType, 1, 3, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblRevision = QtGui.QLabel(ExportR23NativePage1)
        self.lblRevision.setEnabled(False)
        self.lblRevision.setText(_fromUtf8(""))
        self.lblRevision.setObjectName(_fromUtf8("lblRevision"))
        self.horizontalLayout.addWidget(self.lblRevision)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnExport = QtGui.QPushButton(ExportR23NativePage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout.addWidget(self.btnExport)
        self.btnCancel = QtGui.QPushButton(ExportR23NativePage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 11, 0, 1, 6)
        self.chkVerboseLog = QtGui.QCheckBox(ExportR23NativePage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridLayout.addWidget(self.chkVerboseLog, 3, 0, 1, 2)
        self.chkMakeInvoice = QtGui.QCheckBox(ExportR23NativePage1)
        self.chkMakeInvoice.setChecked(True)
        self.chkMakeInvoice.setObjectName(_fromUtf8("chkMakeInvoice"))
        self.gridLayout.addWidget(self.chkMakeInvoice, 5, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        self.edtRegistryNumber = QtGui.QSpinBox(ExportR23NativePage1)
        self.edtRegistryNumber.setMaximum(99999)
        self.edtRegistryNumber.setObjectName(_fromUtf8("edtRegistryNumber"))
        self.gridLayout.addWidget(self.edtRegistryNumber, 2, 3, 1, 1)
        self.progressBarAccount = CProgressBar(ExportR23NativePage1)
        self.progressBarAccount.setProperty("value", 24)
        self.progressBarAccount.setObjectName(_fromUtf8("progressBarAccount"))
        self.gridLayout.addWidget(self.progressBarAccount, 7, 0, 1, 6)
        self.logBrowser = QtGui.QTextBrowser(ExportR23NativePage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 6, 0, 1, 6)
        self.progressBar = CProgressBar(ExportR23NativePage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 8, 0, 1, 6)

        self.retranslateUi(ExportR23NativePage1)
        QtCore.QMetaObject.connectSlotsByName(ExportR23NativePage1)

    def retranslateUi(self, ExportR23NativePage1):
        ExportR23NativePage1.setWindowTitle(_translate("ExportR23NativePage1", "Form", None))
        self.lblRegistryNumber.setText(_translate("ExportR23NativePage1", "Номер реестра счета", None))
        self.chkIgnoreErrors.setText(_translate("ExportR23NativePage1", "Игнорировать ошибки", None))
        self.lblExportType.setText(_translate("ExportR23NativePage1", "Формат экспорта", None))
        self.btnExport.setText(_translate("ExportR23NativePage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportR23NativePage1", "прервать", None))
        self.chkVerboseLog.setText(_translate("ExportR23NativePage1", "Подробный отчет", None))
        self.chkMakeInvoice.setText(_translate("ExportR23NativePage1", "Формировать сч. фактуру", None))

from library.ProgressBar import CProgressBar
