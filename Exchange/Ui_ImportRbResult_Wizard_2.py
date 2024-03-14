# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\samson\Exchange\ImportRbResult_Wizard_2.ui'
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

class Ui_ImportRbResult_Wizard_2(object):
    def setupUi(self, ImportRbResult_Wizard_2):
        ImportRbResult_Wizard_2.setObjectName(_fromUtf8("ImportRbResult_Wizard_2"))
        ImportRbResult_Wizard_2.setWindowModality(QtCore.Qt.NonModal)
        ImportRbResult_Wizard_2.resize(593, 450)
        self.gridLayout = QtGui.QGridLayout(ImportRbResult_Wizard_2)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnClearSelection = QtGui.QPushButton(ImportRbResult_Wizard_2)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.gridLayout.addWidget(self.btnClearSelection, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.tblEvents = QtGui.QTableWidget(ImportRbResult_Wizard_2)
        self.tblEvents.setObjectName(_fromUtf8("tblEvents"))
        self.tblEvents.setColumnCount(0)
        self.tblEvents.setRowCount(0)
        self.gridLayout.addWidget(self.tblEvents, 1, 0, 1, 2)
        self.chkImportAll = QtGui.QCheckBox(ImportRbResult_Wizard_2)
        self.chkImportAll.setObjectName(_fromUtf8("chkImportAll"))
        self.gridLayout.addWidget(self.chkImportAll, 0, 0, 1, 2)
        self.statusLabel = QtGui.QLabel(ImportRbResult_Wizard_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 3, 0, 1, 2)

        self.retranslateUi(ImportRbResult_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ImportRbResult_Wizard_2)

    def retranslateUi(self, ImportRbResult_Wizard_2):
        ImportRbResult_Wizard_2.setWindowTitle(_translate("ImportRbResult_Wizard_2", "Список записей", None))
        self.btnClearSelection.setText(_translate("ImportRbResult_Wizard_2", "Очистить", None))
        self.chkImportAll.setText(_translate("ImportRbResult_Wizard_2", "Загружать всё", None))

