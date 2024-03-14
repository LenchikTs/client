# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Events/ActionTemplateSelectDialog.ui'
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

class Ui_ActionTemplateSelectDialog(object):
    def setupUi(self, ActionTemplateSelectDialog):
        ActionTemplateSelectDialog.setObjectName(_fromUtf8("ActionTemplateSelectDialog"))
        ActionTemplateSelectDialog.resize(787, 293)
        ActionTemplateSelectDialog.setSizeGripEnabled(False)
        self.gridLayout_2 = QtGui.QGridLayout(ActionTemplateSelectDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter_2 = QtGui.QSplitter(ActionTemplateSelectDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlTreeItems = QtGui.QWidget(self.splitter_2)
        self.pnlTreeItems.setObjectName(_fromUtf8("pnlTreeItems"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.pnlTreeItems)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeItems = CTreeView(self.pnlTreeItems)
        self.treeItems.setAutoScroll(True)
        self.treeItems.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.horizontalLayout.addWidget(self.treeItems)
        self.pnlItems = QtGui.QWidget(self.splitter_2)
        self.pnlItems.setObjectName(_fromUtf8("pnlItems"))
        self.gridLayout = QtGui.QGridLayout(self.pnlItems)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkAddProperties = QtGui.QCheckBox(self.pnlItems)
        self.chkAddProperties.setObjectName(_fromUtf8("chkAddProperties"))
        self.gridLayout.addWidget(self.chkAddProperties, 1, 1, 1, 1)
        self.chkFillProperties = QtGui.QCheckBox(self.pnlItems)
        self.chkFillProperties.setChecked(True)
        self.chkFillProperties.setObjectName(_fromUtf8("chkFillProperties"))
        self.gridLayout.addWidget(self.chkFillProperties, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.splitter = QtGui.QSplitter(self.pnlItems)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblProperties = CTableView(self.splitter)
        self.tblProperties.setObjectName(_fromUtf8("tblProperties"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 3)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 2)
        self.cmbShowTypeFilter = QtGui.QComboBox(ActionTemplateSelectDialog)
        self.cmbShowTypeFilter.setObjectName(_fromUtf8("cmbShowTypeFilter"))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.cmbShowTypeFilter.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbShowTypeFilter, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTemplateSelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(ActionTemplateSelectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTemplateSelectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTemplateSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTemplateSelectDialog)

    def retranslateUi(self, ActionTemplateSelectDialog):
        ActionTemplateSelectDialog.setWindowTitle(_translate("ActionTemplateSelectDialog", "Загрузка шаблона действия", None))
        self.chkAddProperties.setText(_translate("ActionTemplateSelectDialog", "Дополнить", None))
        self.chkFillProperties.setText(_translate("ActionTemplateSelectDialog", "Заполнить", None))
        self.cmbShowTypeFilter.setItemText(0, _translate("ActionTemplateSelectDialog", "Показывать все доступные шаблоны", None))
        self.cmbShowTypeFilter.setItemText(1, _translate("ActionTemplateSelectDialog", "Показывать шаблоны текущего пользователя", None))
        self.cmbShowTypeFilter.setItemText(2, _translate("ActionTemplateSelectDialog", "Показывать шаблоны со СНИЛС текущего пользователя", None))

from library.TableView import CTableView
from library.TreeView import CTreeView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActionTemplateSelectDialog = QtGui.QDialog()
    ui = Ui_ActionTemplateSelectDialog()
    ui.setupUi(ActionTemplateSelectDialog)
    ActionTemplateSelectDialog.show()
    sys.exit(app.exec_())

