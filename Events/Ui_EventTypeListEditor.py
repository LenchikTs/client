# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventTypeListEditor.ui'
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

class Ui_EventTypeListEditor(object):
    def setupUi(self, EventTypeListEditor):
        EventTypeListEditor.setObjectName(_fromUtf8("EventTypeListEditor"))
        EventTypeListEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(EventTypeListEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblEventTypeList = CTableView(EventTypeListEditor)
        self.tblEventTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblEventTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblEventTypeList.setObjectName(_fromUtf8("tblEventTypeList"))
        self.gridLayout.addWidget(self.tblEventTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EventTypeListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EventTypeListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventTypeListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventTypeListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(EventTypeListEditor)

    def retranslateUi(self, EventTypeListEditor):
        EventTypeListEditor.setWindowTitle(_translate("EventTypeListEditor", "Типы событий", None))

from library.TableView import CTableView
