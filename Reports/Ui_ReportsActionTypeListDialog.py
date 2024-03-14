# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportsActionTypeListDialog.ui'
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

class Ui_ReportsActionTypeListDialog(object):
    def setupUi(self, ReportsActionTypeListDialog):
        ReportsActionTypeListDialog.setObjectName(_fromUtf8("ReportsActionTypeListDialog"))
        ReportsActionTypeListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ReportsActionTypeListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionTypeList = CMultiSelectionTreeView(ReportsActionTypeListDialog)
        self.tblActionTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblActionTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblActionTypeList.setObjectName(_fromUtf8("tblActionTypeList"))
        self.gridLayout.addWidget(self.tblActionTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportsActionTypeListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ReportsActionTypeListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportsActionTypeListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportsActionTypeListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportsActionTypeListDialog)

    def retranslateUi(self, ReportsActionTypeListDialog):
        ReportsActionTypeListDialog.setWindowTitle(_translate("ReportsActionTypeListDialog", "Подразделения", None))

from library.TreeView import CMultiSelectionTreeView
