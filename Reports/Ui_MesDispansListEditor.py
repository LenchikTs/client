# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\Samson\UP_s11\client_merge\Reports\MesDispansListEditor.ui'
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

class Ui_MesDispansListEditor(object):
    def setupUi(self, MesDispansListEditor):
        MesDispansListEditor.setObjectName(_fromUtf8("MesDispansListEditor"))
        MesDispansListEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(MesDispansListEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblMesDispansList = CTableView(MesDispansListEditor)
        self.tblMesDispansList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblMesDispansList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblMesDispansList.setObjectName(_fromUtf8("tblMesDispansList"))
        self.gridLayout.addWidget(self.tblMesDispansList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MesDispansListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(MesDispansListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MesDispansListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MesDispansListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(MesDispansListEditor)

    def retranslateUi(self, MesDispansListEditor):
        MesDispansListEditor.setWindowTitle(_translate("MesDispansListEditor", "Типы событий", None))

from library.TableView import CTableView
