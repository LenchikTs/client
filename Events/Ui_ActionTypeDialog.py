# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\ActionTypeDialog.ui'
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

class Ui_ActionTypeDialog(object):
    def setupUi(self, ActionTypeDialog):
        ActionTypeDialog.setObjectName(_fromUtf8("ActionTypeDialog"))
        ActionTypeDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ActionTypeDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionType = CTableView(ActionTypeDialog)
        self.tblActionType.setObjectName(_fromUtf8("tblActionType"))
        self.gridLayout.addWidget(self.tblActionType, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTypeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ActionTypeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTypeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTypeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTypeDialog)

    def retranslateUi(self, ActionTypeDialog):
        ActionTypeDialog.setWindowTitle(_translate("ActionTypeDialog", "Типы действий", None))

from library.TableView import CTableView
