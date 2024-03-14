# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ClientRelationsEditDialog.ui'
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

class Ui_ClientRelationsEditDialog(object):
    def setupUi(self, ClientRelationsEditDialog):
        ClientRelationsEditDialog.setObjectName(_fromUtf8("ClientRelationsEditDialog"))
        ClientRelationsEditDialog.resize(936, 735)
        self.gridLayout = QtGui.QGridLayout(ClientRelationsEditDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(ClientRelationsEditDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblDirectRelations = CClientRelationInDocTableView(self.splitter)
        self.tblDirectRelations.setObjectName(_fromUtf8("tblDirectRelations"))
        self.tblBackwardRelations = CClientRelationInDocTableView(self.splitter)
        self.tblBackwardRelations.setObjectName(_fromUtf8("tblBackwardRelations"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ClientRelationsEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ClientRelationsEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientRelationsEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientRelationsEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientRelationsEditDialog)
        ClientRelationsEditDialog.setTabOrder(self.tblDirectRelations, self.tblBackwardRelations)
        ClientRelationsEditDialog.setTabOrder(self.tblBackwardRelations, self.buttonBox)

    def retranslateUi(self, ClientRelationsEditDialog):
        ClientRelationsEditDialog.setWindowTitle(_translate("ClientRelationsEditDialog", "Связи", None))

from Registry.ClientRelationInDocTableView import CClientRelationInDocTableView
