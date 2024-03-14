# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ComplaintsEditDialog.ui'
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

class Ui_ComplaintsEditDialog(object):
    def setupUi(self, ComplaintsEditDialog):
        ComplaintsEditDialog.setObjectName(_fromUtf8("ComplaintsEditDialog"))
        ComplaintsEditDialog.resize(348, 218)
        ComplaintsEditDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ComplaintsEditDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.splitter = QtGui.QSplitter(ComplaintsEditDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeTypicalComplaints = QtGui.QTreeView(self.splitter)
        self.treeTypicalComplaints.setObjectName(_fromUtf8("treeTypicalComplaints"))
        self.edtComplaints = QtGui.QTextEdit(self.splitter)
        self.edtComplaints.setObjectName(_fromUtf8("edtComplaints"))
        self.gridlayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ComplaintsEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ComplaintsEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ComplaintsEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ComplaintsEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ComplaintsEditDialog)
        ComplaintsEditDialog.setTabOrder(self.edtComplaints, self.buttonBox)

    def retranslateUi(self, ComplaintsEditDialog):
        ComplaintsEditDialog.setWindowTitle(_translate("ComplaintsEditDialog", "Жалобы", None))

