# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ContainerTypeListEditor.ui'
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

class Ui_ContainerTypeListEditor(object):
    def setupUi(self, ContainerTypeListEditor):
        ContainerTypeListEditor.setObjectName(_fromUtf8("ContainerTypeListEditor"))
        ContainerTypeListEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ContainerTypeListEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblContainerTypeList = CTableView(ContainerTypeListEditor)
        self.tblContainerTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblContainerTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblContainerTypeList.setObjectName(_fromUtf8("tblContainerTypeList"))
        self.gridLayout.addWidget(self.tblContainerTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ContainerTypeListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ContainerTypeListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ContainerTypeListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ContainerTypeListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ContainerTypeListEditor)

    def retranslateUi(self, ContainerTypeListEditor):
        ContainerTypeListEditor.setWindowTitle(_translate("ContainerTypeListEditor", "Типы контейнера", None))

from library.TableView import CTableView
