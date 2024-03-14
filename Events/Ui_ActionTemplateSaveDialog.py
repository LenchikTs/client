# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Events/ActionTemplateSaveDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ActionTemplateSaveDialog(object):
    def setupUi(self, ActionTemplateSaveDialog):
        ActionTemplateSaveDialog.setObjectName(_fromUtf8("ActionTemplateSaveDialog"))
        ActionTemplateSaveDialog.resize(718, 278)
        ActionTemplateSaveDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(ActionTemplateSaveDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_2 = QtGui.QSplitter(ActionTemplateSaveDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlTreeItems = QtGui.QWidget(self.splitter_2)
        self.pnlTreeItems.setObjectName(_fromUtf8("pnlTreeItems"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlTreeItems)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeItems = CTreeView(self.pnlTreeItems)
        self.treeItems.setAutoScroll(True)
        self.treeItems.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.verticalLayout.addWidget(self.treeItems)
        self.pnlItems = QtGui.QWidget(self.splitter_2)
        self.pnlItems.setObjectName(_fromUtf8("pnlItems"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlItems)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(self.pnlItems)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblItems = CTableView(self.splitter)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.tblProperties = CTableView(self.splitter)
        self.tblProperties.setObjectName(_fromUtf8("tblProperties"))
        self.verticalLayout_2.addWidget(self.splitter)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 2)
        self.cmbShowTypeFilter = QtGui.QComboBox(ActionTemplateSaveDialog)
        self.cmbShowTypeFilter.setObjectName(_fromUtf8("cmbShowTypeFilter"))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbShowTypeFilter, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTemplateSaveDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(ActionTemplateSaveDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTemplateSaveDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTemplateSaveDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTemplateSaveDialog)

    def retranslateUi(self, ActionTemplateSaveDialog):
        ActionTemplateSaveDialog.setWindowTitle(_translate("ActionTemplateSaveDialog", "Сохранение шаблона действия", None))
        self.tblItems.setWhatsThis(_translate("ActionTemplateSaveDialog", "список записей", "ура!"))
        self.cmbShowTypeFilter.setItemText(0, _translate("ActionTemplateSaveDialog", "Показывать все доступные шаблоны", None))
        self.cmbShowTypeFilter.setItemText(1, _translate("ActionTemplateSaveDialog", "Показывать шаблоны текущего пользователя", None))
        self.cmbShowTypeFilter.setItemText(2, _translate("ActionTemplateSaveDialog", "Показывать шаблоны со СНИЛС текущего пользователя", None))

from library.TableView import CTableView
from library.TreeView import CTreeView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActionTemplateSaveDialog = QtGui.QDialog()
    ui = Ui_ActionTemplateSaveDialog()
    ui.setupUi(ActionTemplateSaveDialog)
    ActionTemplateSaveDialog.show()
    sys.exit(app.exec_())

