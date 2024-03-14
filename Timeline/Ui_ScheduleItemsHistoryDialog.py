# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\ScheduleItemsHistoryDialog.ui'
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

class Ui_ScheduleItemsHistoryDialog(object):
    def setupUi(self, ScheduleItemsHistoryDialog):
        ScheduleItemsHistoryDialog.setObjectName(_fromUtf8("ScheduleItemsHistoryDialog"))
        ScheduleItemsHistoryDialog.resize(593, 456)
        self.gridLayout = QtGui.QGridLayout(ScheduleItemsHistoryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblScheduleItems = CTableView(ScheduleItemsHistoryDialog)
        self.tblScheduleItems.setTabKeyNavigation(False)
        self.tblScheduleItems.setAlternatingRowColors(True)
        self.tblScheduleItems.setObjectName(_fromUtf8("tblScheduleItems"))
        self.gridLayout.addWidget(self.tblScheduleItems, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ScheduleItemsHistoryDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ScheduleItemsHistoryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ScheduleItemsHistoryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScheduleItemsHistoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScheduleItemsHistoryDialog)

    def retranslateUi(self, ScheduleItemsHistoryDialog):
        ScheduleItemsHistoryDialog.setWindowTitle(_translate("ScheduleItemsHistoryDialog", "История записи", None))
        self.tblScheduleItems.setWhatsThis(_translate("ScheduleItemsHistoryDialog", "список записей", "ура!"))

from library.TableView import CTableView
