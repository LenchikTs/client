# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ExportR51OMSPage1.ui'
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
        ExportPage1.resize(480, 300)
        self.gridlayout = QtGui.QGridLayout(ExportPage1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 5, 0, 1, 5)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridlayout.addWidget(self.btnExport, 9, 3, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 4, 0, 1, 5)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridlayout.addWidget(self.btnCancel, 9, 4, 1, 1)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridlayout.addWidget(self.chkVerboseLog, 0, 0, 1, 1)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportPage1)
        self.chkIgnoreErrors.setEnabled(False)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.gridlayout.addWidget(self.chkIgnoreErrors, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 6, 0, 1, 5)
        self.cmbExportType = QtGui.QComboBox(ExportPage1)
        self.cmbExportType.setObjectName(_fromUtf8("cmbExportType"))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbExportType, 3, 0, 1, 5)
        self.lblExportType = QtGui.QLabel(ExportPage1)
        self.lblExportType.setObjectName(_fromUtf8("lblExportType"))
        self.gridlayout.addWidget(self.lblExportType, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 9, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2, 8, 2, 1, 1)
        self.lblRevision = QtGui.QLabel(ExportPage1)
        self.lblRevision.setEnabled(False)
        self.lblRevision.setText(_fromUtf8(""))
        self.lblRevision.setObjectName(_fromUtf8("lblRevision"))
        self.gridlayout.addWidget(self.lblRevision, 9, 0, 1, 2)
        self.lblElapsed = QtGui.QLabel(ExportPage1)
        self.lblElapsed.setText(_fromUtf8(""))
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.gridlayout.addWidget(self.lblElapsed, 7, 0, 1, 5)

        self.retranslateUi(ExportPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(_translate("ExportPage1", "Form", None))
        self.btnExport.setText(_translate("ExportPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportPage1", "прервать", None))
        self.chkVerboseLog.setText(_translate("ExportPage1", "Подробный отчет", None))
        self.chkIgnoreErrors.setText(_translate("ExportPage1", "Игнорировать ошибки", None))
        self.cmbExportType.setItemText(0, _translate("ExportPage1", "2019", None))
        self.cmbExportType.setItemText(1, _translate("ExportPage1", "2020", None))
        self.cmbExportType.setItemText(2, _translate("ExportPage1", "2021", None))
        self.lblExportType.setText(_translate("ExportPage1", "Формат экспорта:", None))

from library.ProgressBar import CProgressBar
