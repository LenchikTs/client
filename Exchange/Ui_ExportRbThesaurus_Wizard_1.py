# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\temp1\Exchange\ExportRbThesaurus_Wizard_1.ui'
#
# Created: Wed Aug 19 12:50:34 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExportRbThesaurus_Wizard_1(object):
    def setupUi(self, ExportRbThesaurus_Wizard_1):
        ExportRbThesaurus_Wizard_1.setObjectName("ExportRbThesaurus_Wizard_1")
        ExportRbThesaurus_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportRbThesaurus_Wizard_1.resize(593, 450)
        self.gridlayout = QtGui.QGridLayout(ExportRbThesaurus_Wizard_1)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")
        self.splitterTree = QtGui.QSplitter(ExportRbThesaurus_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName("splitterTree")
        self.treeItems = CTreeView(self.splitterTree)
        self.treeItems.setObjectName("treeItems")
        self.tblItems = CTableView(self.splitterTree)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName("tblItems")
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnSelectAll = QtGui.QPushButton(ExportRbThesaurus_Wizard_1)
        self.btnSelectAll.setObjectName("btnSelectAll")
        self.hboxlayout.addWidget(self.btnSelectAll)
        self.btnClearSelection = QtGui.QPushButton(ExportRbThesaurus_Wizard_1)
        self.btnClearSelection.setObjectName("btnClearSelection")
        self.hboxlayout.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(ExportRbThesaurus_Wizard_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        self.gridlayout.addWidget(self.statusBar, 4, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.checkExportAll = QtGui.QCheckBox(ExportRbThesaurus_Wizard_1)
        self.checkExportAll.setObjectName("checkExportAll")
        self.hboxlayout1.addWidget(self.checkExportAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.chkRecursiveSelection = QtGui.QCheckBox(ExportRbThesaurus_Wizard_1)
        self.chkRecursiveSelection.setObjectName("chkRecursiveSelection")
        self.hboxlayout1.addWidget(self.chkRecursiveSelection)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)

        self.retranslateUi(ExportRbThesaurus_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportRbThesaurus_Wizard_1)
        ExportRbThesaurus_Wizard_1.setTabOrder(self.treeItems, self.tblItems)

    def retranslateUi(self, ExportRbThesaurus_Wizard_1):
        ExportRbThesaurus_Wizard_1.setWindowTitle(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "Список записей", None, QtGui.QApplication.UnicodeUTF8))
        self.tblItems.setWhatsThis(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "список записей", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectAll.setText(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "Выбрать все", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearSelection.setText(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "Очистить", None, QtGui.QApplication.UnicodeUTF8))
        self.statusBar.setToolTip(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "A status bar", None, QtGui.QApplication.UnicodeUTF8))
        self.statusBar.setWhatsThis(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "A status bar.", None, QtGui.QApplication.UnicodeUTF8))
        self.checkExportAll.setText(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "Выгружать всё", None, QtGui.QApplication.UnicodeUTF8))
        self.chkRecursiveSelection.setText(QtGui.QApplication.translate("ExportRbThesaurus_Wizard_1", "Выделять все дочерние элементы", None, QtGui.QApplication.UnicodeUTF8))

from library.TreeView import CTreeView
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExportRbThesaurus_Wizard_1 = QtGui.QDialog()
    ui = Ui_ExportRbThesaurus_Wizard_1()
    ui.setupUi(ExportRbThesaurus_Wizard_1)
    ExportRbThesaurus_Wizard_1.show()
    sys.exit(app.exec_())

