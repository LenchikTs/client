# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\DialogListWidgets.ui'
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

class Ui_DialogListWidgets(object):
    def setupUi(self, DialogListWidgets):
        DialogListWidgets.setObjectName(_fromUtf8("DialogListWidgets"))
        DialogListWidgets.resize(400, 300)

        self.retranslateUi(DialogListWidgets)
        QtCore.QMetaObject.connectSlotsByName(DialogListWidgets)

    def retranslateUi(self, DialogListWidgets):
        DialogListWidgets.setWindowTitle(_translate("DialogListWidgets", "Form", None))
