# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\_SVN\client_test\Exchange\ExportActions_Wizard_1.ui'
#
# Created: Thu Apr 20 10:12:50 2023
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ExportActions_Wizard_1(object):
    def setupUi(self, ExportActions_Wizard_1):
        ExportActions_Wizard_1.setObjectName(_fromUtf8("ExportActions_Wizard_1"))
        ExportActions_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportActions_Wizard_1.resize(847, 416)
        self.gridlayout = QtGui.QGridLayout(ExportActions_Wizard_1)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setMargin(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.splitterTree = QtGui.QSplitter(ExportActions_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.treeItems = CTreeView(self.splitterTree)
        self.treeItems.setMinimumSize(QtCore.QSize(0, 450))
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.tblItems = CTableView(self.splitterTree)
        self.tblItems.setMinimumSize(QtCore.QSize(0, 450))
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnSelectAll = QtGui.QPushButton(ExportActions_Wizard_1)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.hboxlayout.addWidget(self.btnSelectAll)
        self.btnClearSelection = QtGui.QPushButton(ExportActions_Wizard_1)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.hboxlayout.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(ExportActions_Wizard_1)
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
        self.checkExportAll = QtGui.QCheckBox(ExportActions_Wizard_1)
        self.checkExportAll.setObjectName(_fromUtf8("checkExportAll"))
        self.hboxlayout1.addWidget(self.checkExportAll)
        self.checkBoxAllowedSelectFormsEvent = QtGui.QCheckBox(ExportActions_Wizard_1)
        self.checkBoxAllowedSelectFormsEvent.setObjectName(_fromUtf8("checkBoxAllowedSelectFormsEvent"))
        self.hboxlayout1.addWidget(self.checkBoxAllowedSelectFormsEvent)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.chkRecursiveSelection = QtGui.QCheckBox(ExportActions_Wizard_1)
        self.chkRecursiveSelection.setObjectName(_fromUtf8("chkRecursiveSelection"))
        self.hboxlayout1.addWidget(self.chkRecursiveSelection)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)

        self.retranslateUi(ExportActions_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportActions_Wizard_1)
        ExportActions_Wizard_1.setTabOrder(self.treeItems, self.tblItems)

    def retranslateUi(self, ExportActions_Wizard_1):
        ExportActions_Wizard_1.setWindowTitle(_translate("ExportActions_Wizard_1", "Список записей", None))
        self.tblItems.setWhatsThis(_translate("ExportActions_Wizard_1", "список записей", "ура!"))
        self.btnSelectAll.setText(_translate("ExportActions_Wizard_1", "Выбрать все", None))
        self.btnClearSelection.setText(_translate("ExportActions_Wizard_1", "Очистить", None))
        self.statusBar.setToolTip(_translate("ExportActions_Wizard_1", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ExportActions_Wizard_1", "A status bar.", None))
        self.checkExportAll.setText(_translate("ExportActions_Wizard_1", "Выгружать всё", None))
        self.checkBoxAllowedSelectFormsEvent.setText(_translate("ExportActions_Wizard_1", "Разрешается выбор в формах ввода события", None))
        self.chkRecursiveSelection.setText(_translate("ExportActions_Wizard_1", "Выделять все дочерние элементы", None))

from library.TreeView import CTreeView
from library.TableView import CTableView
