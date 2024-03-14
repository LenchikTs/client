# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\CheckPeriodActions.ui'
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

class Ui_CheckPeriodActions(object):
    def setupUi(self, CheckPeriodActions):
        CheckPeriodActions.setObjectName(_fromUtf8("CheckPeriodActions"))
        CheckPeriodActions.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(CheckPeriodActions)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnPrint = QtGui.QPushButton(CheckPeriodActions)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 2, 2, 1, 1)
        self.btnClose = QtGui.QPushButton(CheckPeriodActions)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 2, 4, 1, 1)
        self.tblActionList = CInDocTableView(CheckPeriodActions)
        self.tblActionList.setObjectName(_fromUtf8("tblActionList"))
        self.gridLayout.addWidget(self.tblActionList, 1, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.txtClientInfoBrowser = CTextBrowser(CheckPeriodActions)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.gridLayout.addWidget(self.txtClientInfoBrowser, 0, 0, 1, 5)
        self.btnSave = QtGui.QPushButton(CheckPeriodActions)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout.addWidget(self.btnSave, 2, 3, 1, 1)

        self.retranslateUi(CheckPeriodActions)
        QtCore.QMetaObject.connectSlotsByName(CheckPeriodActions)

    def retranslateUi(self, CheckPeriodActions):
        CheckPeriodActions.setWindowTitle(_translate("CheckPeriodActions", "Контроль движения пациента", None))
        self.btnPrint.setText(_translate("CheckPeriodActions", "Печать", None))
        self.btnClose.setText(_translate("CheckPeriodActions", "Закрыть", None))
        self.btnSave.setText(_translate("CheckPeriodActions", "Сохранить", None))

from library.InDocTable import CInDocTableView
from library.TextBrowser import CTextBrowser
