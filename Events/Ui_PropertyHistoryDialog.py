# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\PropertyHistoryDialog.ui'
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

class Ui_PropertyHistoryDialog(object):
    def setupUi(self, PropertyHistoryDialog):
        PropertyHistoryDialog.setObjectName(_fromUtf8("PropertyHistoryDialog"))
        PropertyHistoryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PropertyHistoryDialog.resize(651, 291)
        self.gridlayout = QtGui.QGridLayout(PropertyHistoryDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(PropertyHistoryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tblValues = CInDocTableView(PropertyHistoryDialog)
        self.tblValues.setObjectName(_fromUtf8("tblValues"))
        self.gridlayout.addWidget(self.tblValues, 0, 0, 1, 1)

        self.retranslateUi(PropertyHistoryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PropertyHistoryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PropertyHistoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PropertyHistoryDialog)

    def retranslateUi(self, PropertyHistoryDialog):
        PropertyHistoryDialog.setWindowTitle(_translate("PropertyHistoryDialog", "Dialog", None))

from library.InDocTable import CInDocTableView
