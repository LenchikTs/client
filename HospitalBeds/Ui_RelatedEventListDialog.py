# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\RelatedEventListDialog.ui'
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

class Ui_RelatedEventListDialog(object):
    def setupUi(self, RelatedEventListDialog):
        RelatedEventListDialog.setObjectName(_fromUtf8("RelatedEventListDialog"))
        RelatedEventListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(RelatedEventListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblRelatedEventList = CTableView(RelatedEventListDialog)
        self.tblRelatedEventList.setObjectName(_fromUtf8("tblRelatedEventList"))
        self.gridLayout.addWidget(self.tblRelatedEventList, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnPrint = QtGui.QPushButton(RelatedEventListDialog)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 1, 1, 1, 1)
        self.btnClose = QtGui.QPushButton(RelatedEventListDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 2, 1, 1)

        self.retranslateUi(RelatedEventListDialog)
        QtCore.QMetaObject.connectSlotsByName(RelatedEventListDialog)

    def retranslateUi(self, RelatedEventListDialog):
        RelatedEventListDialog.setWindowTitle(_translate("RelatedEventListDialog", "Связанные события", None))
        self.btnPrint.setText(_translate("RelatedEventListDialog", "Печать", None))
        self.btnClose.setText(_translate("RelatedEventListDialog", "Закрыть", None))

from library.TableView import CTableView
