# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventTypeComboBoxExPopup.ui'
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

class Ui_EventTypeComboBoxExPopup(object):
    def setupUi(self, EventTypeComboBoxExPopup):
        EventTypeComboBoxExPopup.setObjectName(_fromUtf8("EventTypeComboBoxExPopup"))
        EventTypeComboBoxExPopup.resize(404, 326)
        self.gridLayout = QtGui.QGridLayout(EventTypeComboBoxExPopup)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblEventTypeList = CTableView(EventTypeComboBoxExPopup)
        self.tblEventTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblEventTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblEventTypeList.setObjectName(_fromUtf8("tblEventTypeList"))
        self.gridLayout.addWidget(self.tblEventTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EventTypeComboBoxExPopup)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EventTypeComboBoxExPopup)
        QtCore.QMetaObject.connectSlotsByName(EventTypeComboBoxExPopup)

    def retranslateUi(self, EventTypeComboBoxExPopup):
        EventTypeComboBoxExPopup.setWindowTitle(_translate("EventTypeComboBoxExPopup", "Form", None))

from library.TableView import CTableView
