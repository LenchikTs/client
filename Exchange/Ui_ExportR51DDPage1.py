# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportR51DDPage1.ui'
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

class Ui_ExportR51DDPage1(object):
    def setupUi(self, ExportR51DDPage1):
        ExportR51DDPage1.setObjectName(_fromUtf8("ExportR51DDPage1"))
        ExportR51DDPage1.resize(435, 300)
        self.gridlayout = QtGui.QGridLayout(ExportR51DDPage1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 3)
        self.progressBar = CProgressBar(ExportR51DDPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 6, 0, 1, 3)
        self.btnExport = QtGui.QPushButton(ExportR51DDPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridlayout.addWidget(self.btnExport, 7, 1, 1, 1)
        self.btnCancel = QtGui.QPushButton(ExportR51DDPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridlayout.addWidget(self.btnCancel, 7, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 7, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ExportR51DDPage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 4, 0, 1, 3)
        self.chkVerboseLog = QtGui.QCheckBox(ExportR51DDPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridlayout.addWidget(self.chkVerboseLog, 2, 0, 1, 1)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportR51DDPage1)
        self.chkIgnoreErrors.setEnabled(False)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.gridlayout.addWidget(self.chkIgnoreErrors, 3, 0, 1, 1)
        self.chkMarkFirstForMKBZ00 = QtGui.QCheckBox(ExportR51DDPage1)
        self.chkMarkFirstForMKBZ00.setChecked(True)
        self.chkMarkFirstForMKBZ00.setObjectName(_fromUtf8("chkMarkFirstForMKBZ00"))
        self.gridlayout.addWidget(self.chkMarkFirstForMKBZ00, 1, 0, 1, 3)

        self.retranslateUi(ExportR51DDPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportR51DDPage1)

    def retranslateUi(self, ExportR51DDPage1):
        ExportR51DDPage1.setWindowTitle(_translate("ExportR51DDPage1", "Form", None))
        self.btnExport.setText(_translate("ExportR51DDPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportR51DDPage1", "прервать", None))
        self.chkVerboseLog.setText(_translate("ExportR51DDPage1", "Подробный отчет", None))
        self.chkIgnoreErrors.setText(_translate("ExportR51DDPage1", "Игнорировать ошибки", None))
        self.chkMarkFirstForMKBZ00.setText(_translate("ExportR51DDPage1", "Считать характер для обстоятельств обращения как ранее известный", None))

from library.ProgressBar import CProgressBar
