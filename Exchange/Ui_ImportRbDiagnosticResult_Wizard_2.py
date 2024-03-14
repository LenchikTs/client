# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportRbDiagnosticResult_Wizard_2.ui'
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

class Ui_ImportRbDiagnosticResult_Wizard_2(object):
    def setupUi(self, ImportRbDiagnosticResult_Wizard_2):
        ImportRbDiagnosticResult_Wizard_2.setObjectName(_fromUtf8("ImportRbDiagnosticResult_Wizard_2"))
        ImportRbDiagnosticResult_Wizard_2.setWindowModality(QtCore.Qt.NonModal)
        ImportRbDiagnosticResult_Wizard_2.resize(593, 450)
        self.gridlayout = QtGui.QGridLayout(ImportRbDiagnosticResult_Wizard_2)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.splitterTree = QtGui.QSplitter(ImportRbDiagnosticResult_Wizard_2)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.tblEvents = QtGui.QTableWidget(self.splitterTree)
        self.tblEvents.setObjectName(_fromUtf8("tblEvents"))
        self.tblEvents.setColumnCount(0)
        self.tblEvents.setRowCount(0)
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClearSelection = QtGui.QPushButton(ImportRbDiagnosticResult_Wizard_2)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.hboxlayout.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.chkImportAll = QtGui.QCheckBox(ImportRbDiagnosticResult_Wizard_2)
        self.chkImportAll.setObjectName(_fromUtf8("chkImportAll"))
        self.hboxlayout1.addWidget(self.chkImportAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(ImportRbDiagnosticResult_Wizard_2)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridlayout.addWidget(self.statusLabel, 4, 0, 1, 1)

        self.retranslateUi(ImportRbDiagnosticResult_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ImportRbDiagnosticResult_Wizard_2)

    def retranslateUi(self, ImportRbDiagnosticResult_Wizard_2):
        ImportRbDiagnosticResult_Wizard_2.setWindowTitle(_translate("ImportRbDiagnosticResult_Wizard_2", "Список записей", None))
        self.btnClearSelection.setText(_translate("ImportRbDiagnosticResult_Wizard_2", "Очистить", None))
        self.chkImportAll.setText(_translate("ImportRbDiagnosticResult_Wizard_2", "Загружать всё", None))

