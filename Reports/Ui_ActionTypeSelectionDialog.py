# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ActionTypeSelectionDialog.ui'
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

class Ui_ActionTypeSelectionDialog(object):
    def setupUi(self, ActionTypeSelectionDialog):
        ActionTypeSelectionDialog.setObjectName(_fromUtf8("ActionTypeSelectionDialog"))
        ActionTypeSelectionDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ActionTypeSelectionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ActionTypeSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tblActionTypeList = CMultiSelectionTreeView(ActionTypeSelectionDialog)
        self.tblActionTypeList.setObjectName(_fromUtf8("tblActionTypeList"))
        self.gridLayout.addWidget(self.tblActionTypeList, 0, 0, 1, 1)

        self.retranslateUi(ActionTypeSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTypeSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTypeSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTypeSelectionDialog)

    def retranslateUi(self, ActionTypeSelectionDialog):
        ActionTypeSelectionDialog.setWindowTitle(_translate("ActionTypeSelectionDialog", "Типы работ", None))

from library.TreeView import CMultiSelectionTreeView
