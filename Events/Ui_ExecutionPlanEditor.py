# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\Events\ExecutionPlanEditor.ui'
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

class Ui_ExecutionPlanEditor(object):
    def setupUi(self, ExecutionPlanEditor):
        ExecutionPlanEditor.setObjectName(_fromUtf8("ExecutionPlanEditor"))
        ExecutionPlanEditor.resize(373, 272)
        self.gridLayout = QtGui.QGridLayout(ExecutionPlanEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblPlanEditor = CExecutionPlanEditorTable(ExecutionPlanEditor)
        self.tblPlanEditor.setObjectName(_fromUtf8("tblPlanEditor"))
        self.gridLayout.addWidget(self.tblPlanEditor, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ExecutionPlanEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ExecutionPlanEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExecutionPlanEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExecutionPlanEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ExecutionPlanEditor)

    def retranslateUi(self, ExecutionPlanEditor):
        ExecutionPlanEditor.setWindowTitle(_translate("ExecutionPlanEditor", "Выбранное время", None))

from ExecutionPlanEditorTable import CExecutionPlanEditorTable
