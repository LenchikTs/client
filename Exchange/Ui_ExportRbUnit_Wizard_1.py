# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportRbUnit_Wizard_1.ui'
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

class Ui_ExportRbUnit_Wizard_1(object):
    def setupUi(self, ExportRbUnit_Wizard_1):
        ExportRbUnit_Wizard_1.setObjectName(_fromUtf8("ExportRbUnit_Wizard_1"))
        ExportRbUnit_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportRbUnit_Wizard_1.resize(593, 450)
        self.gridlayout = QtGui.QGridLayout(ExportRbUnit_Wizard_1)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.splitterTree = QtGui.QSplitter(ExportRbUnit_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.tblItems = CTableView(self.splitterTree)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClearSelection = QtGui.QPushButton(ExportRbUnit_Wizard_1)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.hboxlayout.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(ExportRbUnit_Wizard_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridlayout.addWidget(self.statusBar, 4, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.chkExportAll = QtGui.QCheckBox(ExportRbUnit_Wizard_1)
        self.chkExportAll.setObjectName(_fromUtf8("chkExportAll"))
        self.hboxlayout1.addWidget(self.chkExportAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)

        self.retranslateUi(ExportRbUnit_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportRbUnit_Wizard_1)

    def retranslateUi(self, ExportRbUnit_Wizard_1):
        ExportRbUnit_Wizard_1.setWindowTitle(_translate("ExportRbUnit_Wizard_1", "Список записей", None))
        self.tblItems.setWhatsThis(_translate("ExportRbUnit_Wizard_1", "список записей", "ура!"))
        self.btnClearSelection.setText(_translate("ExportRbUnit_Wizard_1", "Очистить", None))
        self.statusBar.setToolTip(_translate("ExportRbUnit_Wizard_1", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ExportRbUnit_Wizard_1", "A status bar.", None))
        self.chkExportAll.setText(_translate("ExportRbUnit_Wizard_1", "Выгружать всё", None))

from library.TableView import CTableView
