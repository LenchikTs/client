# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_ELN\library\DBReconnectProgressDialog.ui'
#
# Created: Mon Jul 27 08:34:18 2020
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_DialogDBReconnect(object):
    def setupUi(self, DialogDBReconnect):
        DialogDBReconnect.setObjectName(_fromUtf8("DialogDBReconnect"))
        DialogDBReconnect.setWindowModality(QtCore.Qt.WindowModal)
        DialogDBReconnect.resize(312, 88)
        self.layoutWidget = QtGui.QWidget(DialogDBReconnect)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 291, 52))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = QtGui.QProgressBar(self.layoutWidget)
        self.progressBar.setMaximum(10)
        self.progressBar.setProperty("value", 1)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFormat(_fromUtf8(""))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(188, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.abortBtn = QtGui.QPushButton(self.layoutWidget)
        self.abortBtn.setObjectName(_fromUtf8("abortBtn"))
        self.gridLayout.addWidget(self.abortBtn, 1, 1, 1, 1)

        self.retranslateUi(DialogDBReconnect)
        QtCore.QMetaObject.connectSlotsByName(DialogDBReconnect)

    def retranslateUi(self, DialogDBReconnect):
        DialogDBReconnect.setWindowTitle(_translate("DialogDBReconnect", "Восстановление соединения с БД", None))
        self.abortBtn.setText(_translate("DialogDBReconnect", "Прервать", None))

