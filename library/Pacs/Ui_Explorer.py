# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\Pacs\Explorer.ui'
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

class Ui_ExplorerDialog(object):
    def setupUi(self, ExplorerDialog):
        ExplorerDialog.setObjectName(_fromUtf8("ExplorerDialog"))
        ExplorerDialog.resize(468, 629)
        self.verticalLayout = QtGui.QVBoxLayout(ExplorerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblTop = QtGui.QLabel(ExplorerDialog)
        self.lblTop.setText(_fromUtf8(""))
        self.lblTop.setObjectName(_fromUtf8("lblTop"))
        self.verticalLayout.addWidget(self.lblTop)
        self.listWidget = QtGui.QListWidget(ExplorerDialog)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.progressBar = QtGui.QProgressBar(ExplorerDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(ExplorerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ExplorerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExplorerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExplorerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExplorerDialog)

    def retranslateUi(self, ExplorerDialog):
        ExplorerDialog.setWindowTitle(_translate("ExplorerDialog", "Выберите снимок", None))

