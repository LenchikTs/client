# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\RefBooks\AnatomicalLocalizations\ListDialog.ui'
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

class Ui_ListDialog(object):
    def setupUi(self, ListDialog):
        ListDialog.setObjectName(_fromUtf8("ListDialog"))
        ListDialog.resize(620, 323)
        self.gridLayout = QtGui.QGridLayout(ListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnNew = QtGui.QPushButton(ListDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.gridLayout.addWidget(self.btnNew, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(ListDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 4, 1, 1)
        self.btnEdit = QtGui.QPushButton(ListDialog)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.gridLayout.addWidget(self.btnEdit, 1, 2, 1, 1)
        self.splitter = QtGui.QSplitter(ListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeView = CTreeView(self.splitter)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.tableView = CTableView(self.splitter)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 5)
        self.btnFilter = QtGui.QPushButton(ListDialog)
        self.btnFilter.setObjectName(_fromUtf8("btnFilter"))
        self.gridLayout.addWidget(self.btnFilter, 1, 1, 1, 1)

        self.retranslateUi(ListDialog)
        QtCore.QMetaObject.connectSlotsByName(ListDialog)

    def retranslateUi(self, ListDialog):
        self.btnNew.setText(_translate("ListDialog", "Вставка F9", None))
        self.btnNew.setShortcut(_translate("ListDialog", "F9", None))
        self.btnClose.setText(_translate("ListDialog", "Закрыть", None))
        self.btnEdit.setText(_translate("ListDialog", "Правка F4", None))
        self.btnEdit.setShortcut(_translate("ListDialog", "F4", None))
        self.btnFilter.setText(_translate("ListDialog", "Фильтр", None))

from library.TableView import CTableView
from library.TreeView import CTreeView
