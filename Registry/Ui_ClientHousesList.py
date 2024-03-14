# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ClientHousesList.ui'
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

class Ui_ClientHousesList(object):
    def setupUi(self, ClientHousesList):
        ClientHousesList.setObjectName(_fromUtf8("ClientHousesList"))
        ClientHousesList.resize(374, 335)
        ClientHousesList.setSizeGripEnabled(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ClientHousesList)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(ClientHousesList)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.kladrTab = QtGui.QWidget()
        self.kladrTab.setObjectName(_fromUtf8("kladrTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.kladrTab)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblHousesList = QtGui.QTableWidget(self.kladrTab)
        self.tblHousesList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblHousesList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblHousesList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblHousesList.setObjectName(_fromUtf8("tblHousesList"))
        self.tblHousesList.setColumnCount(2)
        self.tblHousesList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblHousesList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblHousesList.setHorizontalHeaderItem(1, item)
        self.tblHousesList.horizontalHeader().setStretchLastSection(True)
        self.tblHousesList.verticalHeader().setVisible(False)
        self.tblHousesList.verticalHeader().setDefaultSectionSize(20)
        self.verticalLayout.addWidget(self.tblHousesList)
        self.tabWidget.addTab(self.kladrTab, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(ClientHousesList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ClientHousesList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientHousesList.hide)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientHousesList.hide)
        QtCore.QMetaObject.connectSlotsByName(ClientHousesList)

    def retranslateUi(self, ClientHousesList):
        ClientHousesList.setWindowTitle(_translate("ClientHousesList", "Номера домов", None))
        item = self.tblHousesList.horizontalHeaderItem(0)
        item.setText(_translate("ClientHousesList", "Дом", None))
        item = self.tblHousesList.horizontalHeaderItem(1)
        item.setText(_translate("ClientHousesList", "Корпус", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.kladrTab), _translate("ClientHousesList", "КЛАДР", None))

