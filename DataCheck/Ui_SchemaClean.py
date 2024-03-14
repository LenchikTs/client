# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\SchemaClean.ui'
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

class Ui_SchemaCleanDialog(object):
    def setupUi(self, SchemaCleanDialog):
        SchemaCleanDialog.setObjectName(_fromUtf8("SchemaCleanDialog"))
        SchemaCleanDialog.resize(426, 385)
        self.gridLayout = QtGui.QGridLayout(SchemaCleanDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = CProgressBar(SchemaCleanDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 3)
        self.logBrowser = QtGui.QTextBrowser(SchemaCleanDialog)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(253, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.btnClean = QtGui.QPushButton(SchemaCleanDialog)
        self.btnClean.setObjectName(_fromUtf8("btnClean"))
        self.gridLayout.addWidget(self.btnClean, 4, 1, 1, 1)
        self.btnClose = QtGui.QPushButton(SchemaCleanDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 4, 2, 1, 1)
        self.tblTables = QtGui.QTableWidget(SchemaCleanDialog)
        self.tblTables.setObjectName(_fromUtf8("tblTables"))
        self.tblTables.setColumnCount(0)
        self.tblTables.setRowCount(0)
        self.gridLayout.addWidget(self.tblTables, 1, 0, 1, 3)
        self.chkSelectAll = QtGui.QCheckBox(SchemaCleanDialog)
        self.chkSelectAll.setObjectName(_fromUtf8("chkSelectAll"))
        self.gridLayout.addWidget(self.chkSelectAll, 0, 0, 1, 3)

        self.retranslateUi(SchemaCleanDialog)
        QtCore.QMetaObject.connectSlotsByName(SchemaCleanDialog)

    def retranslateUi(self, SchemaCleanDialog):
        SchemaCleanDialog.setWindowTitle(_translate("SchemaCleanDialog", "Очистка записей, помеченных на удаление", None))
        self.btnClean.setText(_translate("SchemaCleanDialog", "Очистка", None))
        self.btnClose.setText(_translate("SchemaCleanDialog", "Закрыть", None))
        self.chkSelectAll.setText(_translate("SchemaCleanDialog", "Выбрать всё", None))

from library.ProgressBar import CProgressBar
