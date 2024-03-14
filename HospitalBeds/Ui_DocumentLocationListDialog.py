# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\DocumentLocationListDialog.ui'
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

class Ui_DocumentLocationListDialog(object):
    def setupUi(self, DocumentLocationListDialog):
        DocumentLocationListDialog.setObjectName(_fromUtf8("DocumentLocationListDialog"))
        DocumentLocationListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(DocumentLocationListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblDocumentLocationList = CTableView(DocumentLocationListDialog)
        self.tblDocumentLocationList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblDocumentLocationList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblDocumentLocationList.setObjectName(_fromUtf8("tblDocumentLocationList"))
        self.gridLayout.addWidget(self.tblDocumentLocationList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DocumentLocationListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DocumentLocationListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DocumentLocationListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DocumentLocationListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DocumentLocationListDialog)

    def retranslateUi(self, DocumentLocationListDialog):
        DocumentLocationListDialog.setWindowTitle(_translate("DocumentLocationListDialog", "Места нахождения учетных документов", None))

from library.TableView import CTableView
