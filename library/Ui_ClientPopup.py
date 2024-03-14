# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\ClientPopup.ui'
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

class Ui_ClientPopup(object):
    def setupUi(self, ClientPopup):
        ClientPopup.setObjectName(_fromUtf8("ClientPopup"))
        ClientPopup.resize(780, 466)
        self.gridLayout = QtGui.QGridLayout(ClientPopup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtQuery = QtGui.QLineEdit(ClientPopup)
        self.edtQuery.setObjectName(_fromUtf8("edtQuery"))
        self.gridLayout.addWidget(self.edtQuery, 0, 1, 1, 1)
        self.lblQuery = QtGui.QLabel(ClientPopup)
        self.lblQuery.setObjectName(_fromUtf8("lblQuery"))
        self.gridLayout.addWidget(self.lblQuery, 0, 0, 1, 1)
        self.btnSearch = QtGui.QPushButton(ClientPopup)
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.gridLayout.addWidget(self.btnSearch, 0, 2, 1, 1)
        self.tblClient = CTableView(ClientPopup)
        self.tblClient.setObjectName(_fromUtf8("tblClient"))
        self.gridLayout.addWidget(self.tblClient, 1, 0, 1, 3)

        self.retranslateUi(ClientPopup)
        QtCore.QMetaObject.connectSlotsByName(ClientPopup)

    def retranslateUi(self, ClientPopup):
        ClientPopup.setWindowTitle(_translate("ClientPopup", "Form", None))
        self.lblQuery.setText(_translate("ClientPopup", "ФИО/Код:", None))
        self.btnSearch.setText(_translate("ClientPopup", "Поиск", None))

from library.TableView import CTableView
