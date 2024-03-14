# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\ClientPayersList.ui'
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

class Ui_ClientPayersList(object):
    def setupUi(self, ClientPayersList):
        ClientPayersList.setObjectName(_fromUtf8("ClientPayersList"))
        ClientPayersList.resize(382, 331)
        ClientPayersList.setSizeGripEnabled(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ClientPayersList)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblPayersList = CTableView(ClientPayersList)
        self.tblPayersList.setObjectName(_fromUtf8("tblPayersList"))
        self.verticalLayout_2.addWidget(self.tblPayersList)
        self.buttonBox = QtGui.QDialogButtonBox(ClientPayersList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ClientPayersList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientPayersList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientPayersList.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientPayersList)

    def retranslateUi(self, ClientPayersList):
        ClientPayersList.setWindowTitle(_translate("ClientPayersList", "Список плательщиков", None))

from library.TableView import CTableView
