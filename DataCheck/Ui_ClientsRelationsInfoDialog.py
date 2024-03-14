# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\ClientsRelationsInfoDialog.ui'
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

class Ui_ClientsRelationsInfoDialog(object):
    def setupUi(self, ClientsRelationsInfoDialog):
        ClientsRelationsInfoDialog.setObjectName(_fromUtf8("ClientsRelationsInfoDialog"))
        ClientsRelationsInfoDialog.resize(643, 439)
        self.gridLayout_2 = QtGui.QGridLayout(ClientsRelationsInfoDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter = QtGui.QSplitter(ClientsRelationsInfoDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblClients = CVHTableView(self.splitter)
        self.tblClients.setObjectName(_fromUtf8("tblClients"))
        self.grpRelations = QtGui.QGroupBox(self.splitter)
        self.grpRelations.setAlignment(QtCore.Qt.AlignCenter)
        self.grpRelations.setObjectName(_fromUtf8("grpRelations"))
        self.gridLayout = QtGui.QGridLayout(self.grpRelations)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblRelations = CTableView(self.grpRelations)
        self.tblRelations.setObjectName(_fromUtf8("tblRelations"))
        self.gridLayout.addWidget(self.tblRelations, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ClientsRelationsInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ClientsRelationsInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientsRelationsInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientsRelationsInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientsRelationsInfoDialog)
        ClientsRelationsInfoDialog.setTabOrder(self.tblClients, self.tblRelations)
        ClientsRelationsInfoDialog.setTabOrder(self.tblRelations, self.buttonBox)

    def retranslateUi(self, ClientsRelationsInfoDialog):
        ClientsRelationsInfoDialog.setWindowTitle(_translate("ClientsRelationsInfoDialog", "Dialog", None))
        self.grpRelations.setTitle(_translate("ClientsRelationsInfoDialog", "Связи пациента", None))

from library.TableView import CTableView
from library.VerticalHeaderTableView import CVHTableView
