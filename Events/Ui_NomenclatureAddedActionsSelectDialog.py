# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\Events\NomenclatureAddedActionsSelectDialog.ui'
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

class Ui_NomenclatureAddedActionsSelectDialog(object):
    def setupUi(self, NomenclatureAddedActionsSelectDialog):
        NomenclatureAddedActionsSelectDialog.setObjectName(_fromUtf8("NomenclatureAddedActionsSelectDialog"))
        NomenclatureAddedActionsSelectDialog.resize(562, 300)
        self.gridLayout = QtGui.QGridLayout(NomenclatureAddedActionsSelectDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(7)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(NomenclatureAddedActionsSelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.btnAPNomenclatureExpense = QtGui.QPushButton(NomenclatureAddedActionsSelectDialog)
        self.btnAPNomenclatureExpense.setObjectName(_fromUtf8("btnAPNomenclatureExpense"))
        self.gridLayout.addWidget(self.btnAPNomenclatureExpense, 2, 0, 1, 1)
        self.splitter = QtGui.QSplitter(NomenclatureAddedActionsSelectDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblActionsExpense = CTableView(self.splitter)
        self.tblActionsExpense.setObjectName(_fromUtf8("tblActionsExpense"))
        self.tblNomenclatureExpense = CInDocTableView(self.splitter)
        self.tblNomenclatureExpense.setObjectName(_fromUtf8("tblNomenclatureExpense"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)

        self.retranslateUi(NomenclatureAddedActionsSelectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NomenclatureAddedActionsSelectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NomenclatureAddedActionsSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NomenclatureAddedActionsSelectDialog)
        NomenclatureAddedActionsSelectDialog.setTabOrder(self.tblActionsExpense, self.tblNomenclatureExpense)
        NomenclatureAddedActionsSelectDialog.setTabOrder(self.tblNomenclatureExpense, self.btnAPNomenclatureExpense)
        NomenclatureAddedActionsSelectDialog.setTabOrder(self.btnAPNomenclatureExpense, self.buttonBox)

    def retranslateUi(self, NomenclatureAddedActionsSelectDialog):
        NomenclatureAddedActionsSelectDialog.setWindowTitle(_translate("NomenclatureAddedActionsSelectDialog", "Dialog", None))
        self.btnAPNomenclatureExpense.setText(_translate("NomenclatureAddedActionsSelectDialog", "Списание ЛСиИМН", None))

from library.InDocTable import CInDocTableView
from library.TableView import CTableView
