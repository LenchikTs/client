# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Blank\BlankItemsListDialog.ui'
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

class Ui_BlankItemsListDialog(object):
    def setupUi(self, BlankItemsListDialog):
        BlankItemsListDialog.setObjectName(_fromUtf8("BlankItemsListDialog"))
        BlankItemsListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        BlankItemsListDialog.resize(603, 476)
        BlankItemsListDialog.setSizeGripEnabled(True)
        BlankItemsListDialog.setModal(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(BlankItemsListDialog)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(BlankItemsListDialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTempInvalid = QtGui.QWidget()
        self.tabTempInvalid.setObjectName(_fromUtf8("tabTempInvalid"))
        self.gridLayout = QtGui.QGridLayout(self.tabTempInvalid)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.tabTempInvalid)
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
        self.treeItemsTempInvalid = CTreeView(self.pnlTree)
        self.treeItemsTempInvalid.setObjectName(_fromUtf8("treeItemsTempInvalid"))
        self.verticalLayout.addWidget(self.treeItemsTempInvalid)
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
        self.tblItemsTempInvalid = CTableView(self.pnlList)
        self.tblItemsTempInvalid.setTabKeyNavigation(False)
        self.tblItemsTempInvalid.setAlternatingRowColors(True)
        self.tblItemsTempInvalid.setObjectName(_fromUtf8("tblItemsTempInvalid"))
        self.verticalLayout_2.addWidget(self.tblItemsTempInvalid)
        self.lblCountRows = QtGui.QLabel(self.pnlList)
        self.lblCountRows.setText(_fromUtf8(""))
        self.lblCountRows.setObjectName(_fromUtf8("lblCountRows"))
        self.verticalLayout_2.addWidget(self.lblCountRows)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTempInvalid, _fromUtf8(""))
        self.tabTempOthers = QtGui.QWidget()
        self.tabTempOthers.setEnabled(True)
        self.tabTempOthers.setObjectName(_fromUtf8("tabTempOthers"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabTempOthers)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter_2 = QtGui.QSplitter(self.tabTempOthers)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlTree_2 = QtGui.QWidget(self.splitter_2)
        self.pnlTree_2.setObjectName(_fromUtf8("pnlTree_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.pnlTree_2)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.treeItemsOthers = CTreeView(self.pnlTree_2)
        self.treeItemsOthers.setObjectName(_fromUtf8("treeItemsOthers"))
        self.verticalLayout_4.addWidget(self.treeItemsOthers)
        self.lblPadding_2 = QtGui.QLabel(self.pnlTree_2)
        self.lblPadding_2.setText(_fromUtf8(""))
        self.lblPadding_2.setObjectName(_fromUtf8("lblPadding_2"))
        self.verticalLayout_4.addWidget(self.lblPadding_2)
        self.pnlList_2 = QtGui.QWidget(self.splitter_2)
        self.pnlList_2.setObjectName(_fromUtf8("pnlList_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pnlList_2)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.tblItemsOthers = CTableView(self.pnlList_2)
        self.tblItemsOthers.setTabKeyNavigation(False)
        self.tblItemsOthers.setAlternatingRowColors(True)
        self.tblItemsOthers.setObjectName(_fromUtf8("tblItemsOthers"))
        self.verticalLayout_5.addWidget(self.tblItemsOthers)
        self.lblCountRows_2 = QtGui.QLabel(self.pnlList_2)
        self.lblCountRows_2.setText(_fromUtf8(""))
        self.lblCountRows_2.setObjectName(_fromUtf8("lblCountRows_2"))
        self.verticalLayout_5.addWidget(self.lblCountRows_2)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTempOthers, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnFind = QtGui.QPushButton(BlankItemsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFind.sizePolicy().hasHeightForWidth())
        self.btnFind.setSizePolicy(sizePolicy)
        self.btnFind.setObjectName(_fromUtf8("btnFind"))
        self.hboxlayout.addWidget(self.btnFind)
        self.btnSelect = QtGui.QPushButton(BlankItemsListDialog)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.hboxlayout.addWidget(self.btnSelect)
        self.btnFilter = QtGui.QPushButton(BlankItemsListDialog)
        self.btnFilter.setObjectName(_fromUtf8("btnFilter"))
        self.hboxlayout.addWidget(self.btnFilter)
        self.btnEdit = QtGui.QPushButton(BlankItemsListDialog)
        self.btnEdit.setDefault(True)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnNew = QtGui.QPushButton(BlankItemsListDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.hboxlayout.addWidget(self.btnNew)
        self.btnCancel = QtGui.QPushButton(BlankItemsListDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.verticalLayout_3.addLayout(self.hboxlayout)
        self.statusBar = QtGui.QStatusBar(BlankItemsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.verticalLayout_3.addWidget(self.statusBar)

        self.retranslateUi(BlankItemsListDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), BlankItemsListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BlankItemsListDialog)
        BlankItemsListDialog.setTabOrder(self.treeItemsTempInvalid, self.tblItemsTempInvalid)
        BlankItemsListDialog.setTabOrder(self.tblItemsTempInvalid, self.btnSelect)
        BlankItemsListDialog.setTabOrder(self.btnSelect, self.btnFilter)
        BlankItemsListDialog.setTabOrder(self.btnFilter, self.btnEdit)
        BlankItemsListDialog.setTabOrder(self.btnEdit, self.btnNew)
        BlankItemsListDialog.setTabOrder(self.btnNew, self.btnCancel)

    def retranslateUi(self, BlankItemsListDialog):
        BlankItemsListDialog.setWindowTitle(_translate("BlankItemsListDialog", "Документы ", None))
        self.tblItemsTempInvalid.setWhatsThis(_translate("BlankItemsListDialog", "список записей", "ура!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTempInvalid), _translate("BlankItemsListDialog", "ВУТ", None))
        self.tblItemsOthers.setWhatsThis(_translate("BlankItemsListDialog", "список записей", "ура!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTempOthers), _translate("BlankItemsListDialog", "Прочие", None))
        self.btnFind.setText(_translate("BlankItemsListDialog", "Поиск", None))
        self.btnSelect.setWhatsThis(_translate("BlankItemsListDialog", "выбрать текущую запись", None))
        self.btnSelect.setText(_translate("BlankItemsListDialog", "Выбор", None))
        self.btnFilter.setWhatsThis(_translate("BlankItemsListDialog", "изменить условие отбора записей для показа в списке", None))
        self.btnFilter.setText(_translate("BlankItemsListDialog", "Фильтр", None))
        self.btnEdit.setWhatsThis(_translate("BlankItemsListDialog", "изменить текущую запись", None))
        self.btnEdit.setText(_translate("BlankItemsListDialog", "Правка F4", None))
        self.btnEdit.setShortcut(_translate("BlankItemsListDialog", "F4", None))
        self.btnNew.setWhatsThis(_translate("BlankItemsListDialog", "добавить новую запись", None))
        self.btnNew.setText(_translate("BlankItemsListDialog", "Вставка F9", None))
        self.btnNew.setShortcut(_translate("BlankItemsListDialog", "F9", None))
        self.btnCancel.setWhatsThis(_translate("BlankItemsListDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("BlankItemsListDialog", "Закрыть", None))
        self.statusBar.setToolTip(_translate("BlankItemsListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("BlankItemsListDialog", "A status bar.", None))

from library.TableView import CTableView
from library.TreeView import CTreeView