# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\HierarchicalItemsListDialog.ui'
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

class Ui_HierarchicalItemsListDialog(object):
    def setupUi(self, HierarchicalItemsListDialog):
        HierarchicalItemsListDialog.setObjectName(_fromUtf8("HierarchicalItemsListDialog"))
        HierarchicalItemsListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        HierarchicalItemsListDialog.resize(603, 476)
        HierarchicalItemsListDialog.setSizeGripEnabled(True)
        HierarchicalItemsListDialog.setModal(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(HierarchicalItemsListDialog)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(HierarchicalItemsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlTree = QtGui.QWidget(self.splitter)
        self.pnlTree.setObjectName(_fromUtf8("pnlTree"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlTree)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeItems = CTreeView(self.pnlTree)
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.verticalLayout.addWidget(self.treeItems)
        self.lblPadding = QtGui.QLabel(self.pnlTree)
        self.lblPadding.setText(_fromUtf8(""))
        self.lblPadding.setObjectName(_fromUtf8("lblPadding"))
        self.verticalLayout.addWidget(self.lblPadding)
        self.pnlList = QtGui.QWidget(self.splitter)
        self.pnlList.setObjectName(_fromUtf8("pnlList"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlList)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblItems = CTableView(self.pnlList)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.verticalLayout_2.addWidget(self.tblItems)
        self.lblCountRows = QtGui.QLabel(self.pnlList)
        self.lblCountRows.setText(_fromUtf8(""))
        self.lblCountRows.setObjectName(_fromUtf8("lblCountRows"))
        self.verticalLayout_2.addWidget(self.lblCountRows)
        self.verticalLayout_3.addWidget(self.splitter)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnFind = QtGui.QPushButton(HierarchicalItemsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFind.sizePolicy().hasHeightForWidth())
        self.btnFind.setSizePolicy(sizePolicy)
        self.btnFind.setObjectName(_fromUtf8("btnFind"))
        self.hboxlayout.addWidget(self.btnFind)
        self.btnSelect = QtGui.QPushButton(HierarchicalItemsListDialog)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.hboxlayout.addWidget(self.btnSelect)
        self.btnFilter = QtGui.QPushButton(HierarchicalItemsListDialog)
        self.btnFilter.setObjectName(_fromUtf8("btnFilter"))
        self.hboxlayout.addWidget(self.btnFilter)
        self.btnEdit = QtGui.QPushButton(HierarchicalItemsListDialog)
        self.btnEdit.setDefault(True)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnNew = QtGui.QPushButton(HierarchicalItemsListDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.hboxlayout.addWidget(self.btnNew)
        self.btnCancel = QtGui.QPushButton(HierarchicalItemsListDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.verticalLayout_3.addLayout(self.hboxlayout)
        self.statusBar = QtGui.QStatusBar(HierarchicalItemsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.verticalLayout_3.addWidget(self.statusBar)

        self.retranslateUi(HierarchicalItemsListDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), HierarchicalItemsListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HierarchicalItemsListDialog)
        HierarchicalItemsListDialog.setTabOrder(self.treeItems, self.tblItems)
        HierarchicalItemsListDialog.setTabOrder(self.tblItems, self.btnSelect)
        HierarchicalItemsListDialog.setTabOrder(self.btnSelect, self.btnFilter)
        HierarchicalItemsListDialog.setTabOrder(self.btnFilter, self.btnEdit)
        HierarchicalItemsListDialog.setTabOrder(self.btnEdit, self.btnNew)
        HierarchicalItemsListDialog.setTabOrder(self.btnNew, self.btnCancel)

    def retranslateUi(self, HierarchicalItemsListDialog):
        HierarchicalItemsListDialog.setWindowTitle(_translate("HierarchicalItemsListDialog", "Список записей", None))
        self.tblItems.setWhatsThis(_translate("HierarchicalItemsListDialog", "список записей", "ура!"))
        self.btnFind.setText(_translate("HierarchicalItemsListDialog", "Поиск", None))
        self.btnSelect.setWhatsThis(_translate("HierarchicalItemsListDialog", "выбрать текущую запись", None))
        self.btnSelect.setText(_translate("HierarchicalItemsListDialog", "Выбор", None))
        self.btnFilter.setWhatsThis(_translate("HierarchicalItemsListDialog", "изменить условие отбора записей для показа в списке", None))
        self.btnFilter.setText(_translate("HierarchicalItemsListDialog", "Фильтр", None))
        self.btnEdit.setWhatsThis(_translate("HierarchicalItemsListDialog", "изменить текущую запись", None))
        self.btnEdit.setText(_translate("HierarchicalItemsListDialog", "Правка F4", None))
        self.btnEdit.setShortcut(_translate("HierarchicalItemsListDialog", "F4", None))
        self.btnNew.setWhatsThis(_translate("HierarchicalItemsListDialog", "добавить новую запись", None))
        self.btnNew.setText(_translate("HierarchicalItemsListDialog", "Вставка F9", None))
        self.btnNew.setShortcut(_translate("HierarchicalItemsListDialog", "F9", None))
        self.btnCancel.setWhatsThis(_translate("HierarchicalItemsListDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("HierarchicalItemsListDialog", "Закрыть", None))
        self.statusBar.setToolTip(_translate("HierarchicalItemsListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("HierarchicalItemsListDialog", "A status bar.", None))

from library.TableView import CTableView
from library.TreeView import CTreeView