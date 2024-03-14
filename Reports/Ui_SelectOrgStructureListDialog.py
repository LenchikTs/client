# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\SelectOrgStructureListDialog.ui'
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

class Ui_SelectOrgStructureListDialog(object):
    def setupUi(self, SelectOrgStructureListDialog):
        SelectOrgStructureListDialog.setObjectName(_fromUtf8("SelectOrgStructureListDialog"))
        SelectOrgStructureListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(SelectOrgStructureListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblSelectOrgStructureList = CMultiSelectionTreeView(SelectOrgStructureListDialog)
        self.tblSelectOrgStructureList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblSelectOrgStructureList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblSelectOrgStructureList.setObjectName(_fromUtf8("tblSelectOrgStructureList"))
        self.gridLayout.addWidget(self.tblSelectOrgStructureList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SelectOrgStructureListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SelectOrgStructureListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectOrgStructureListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectOrgStructureListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectOrgStructureListDialog)

    def retranslateUi(self, SelectOrgStructureListDialog):
        SelectOrgStructureListDialog.setWindowTitle(_translate("SelectOrgStructureListDialog", "Подразделения", None))

from library.TreeView import CMultiSelectionTreeView
