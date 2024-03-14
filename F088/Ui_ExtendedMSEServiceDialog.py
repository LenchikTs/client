# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Project\Samson\UP_s11\client\F088\ExtendedMSEServiceDialog.ui'
#
# Created: Thu Nov 18 17:15:23 2021
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ExtendedMSEServiceDialog(object):
    def setupUi(self, ExtendedMSEServiceDialog):
        ExtendedMSEServiceDialog.setObjectName(_fromUtf8("ExtendedMSEServiceDialog"))
        ExtendedMSEServiceDialog.resize(698, 458)
        self.gridLayout = QtGui.QGridLayout(ExtendedMSEServiceDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblExtendedMSEService = CTableView(ExtendedMSEServiceDialog)
        self.tblExtendedMSEService.setObjectName(_fromUtf8("tblExtendedMSEService"))
        self.verticalLayout.addWidget(self.tblExtendedMSEService)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnSaveSelected = QtGui.QPushButton(ExtendedMSEServiceDialog)
        self.btnSaveSelected.setObjectName(_fromUtf8("btnSaveSelected"))
        self.horizontalLayout.addWidget(self.btnSaveSelected)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ExtendedMSEServiceDialog)
        QtCore.QMetaObject.connectSlotsByName(ExtendedMSEServiceDialog)

    def retranslateUi(self, ExtendedMSEServiceDialog):
        ExtendedMSEServiceDialog.setWindowTitle(_translate("ExtendedMSEServiceDialog", "Данные из сервиса", None))
        self.btnSaveSelected.setText(_translate("ExtendedMSEServiceDialog", "Сохранить", None))

from library.TableView import CTableView
