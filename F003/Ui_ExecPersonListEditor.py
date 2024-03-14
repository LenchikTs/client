# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\F003\ExecPersonListEditor.ui'
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

class Ui_ExecPersonListEditor(object):
    def setupUi(self, ExecPersonListEditor):
        ExecPersonListEditor.setObjectName(_fromUtf8("ExecPersonListEditor"))
        ExecPersonListEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ExecPersonListEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblExecPersonList = CInDocTableView(ExecPersonListEditor)
        self.tblExecPersonList.setObjectName(_fromUtf8("tblExecPersonList"))
        self.gridLayout.addWidget(self.tblExecPersonList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ExecPersonListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ExecPersonListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExecPersonListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExecPersonListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ExecPersonListEditor)

    def retranslateUi(self, ExecPersonListEditor):
        ExecPersonListEditor.setWindowTitle(_translate("ExecPersonListEditor", "Журнал назначения лечащего врача", None))

from library.InDocTable import CInDocTableView
