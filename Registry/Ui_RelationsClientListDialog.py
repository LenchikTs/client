# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\RelationsClientListDialog.ui'
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

class Ui_RelationsClientListDialog(object):
    def setupUi(self, RelationsClientListDialog):
        RelationsClientListDialog.setObjectName(_fromUtf8("RelationsClientListDialog"))
        RelationsClientListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(RelationsClientListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblRelationsClientList = CTableView(RelationsClientListDialog)
        self.tblRelationsClientList.setObjectName(_fromUtf8("tblRelationsClientList"))
        self.gridLayout.addWidget(self.tblRelationsClientList, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(RelationsClientListDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 1, 1, 1)

        self.retranslateUi(RelationsClientListDialog)
        QtCore.QMetaObject.connectSlotsByName(RelationsClientListDialog)

    def retranslateUi(self, RelationsClientListDialog):
        RelationsClientListDialog.setWindowTitle(_translate("RelationsClientListDialog", "Список связанных пациентов", None))
        self.btnClose.setText(_translate("RelationsClientListDialog", "Закрыть", None))

from library.TableView import CTableView
