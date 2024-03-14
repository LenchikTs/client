# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\FinanceTypeListEditor.ui'
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

class Ui_FinanceTypeListEditor(object):
    def setupUi(self, FinanceTypeListEditor):
        FinanceTypeListEditor.setObjectName(_fromUtf8("FinanceTypeListEditor"))
        FinanceTypeListEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(FinanceTypeListEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblFinanceTypeList = CTableView(FinanceTypeListEditor)
        self.tblFinanceTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblFinanceTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblFinanceTypeList.setObjectName(_fromUtf8("tblFinanceTypeList"))
        self.gridLayout.addWidget(self.tblFinanceTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FinanceTypeListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(FinanceTypeListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FinanceTypeListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FinanceTypeListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(FinanceTypeListEditor)

    def retranslateUi(self, FinanceTypeListEditor):
        FinanceTypeListEditor.setWindowTitle(_translate("FinanceTypeListEditor", "Типы событий", None))

from library.TableView import CTableView
