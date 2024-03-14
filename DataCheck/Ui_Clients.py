# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\DataCheck\Clients.ui'
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

class Ui_ClientsCheckDialog(object):
    def setupUi(self, ClientsCheckDialog):
        ClientsCheckDialog.setObjectName(_fromUtf8("ClientsCheckDialog"))
        ClientsCheckDialog.resize(589, 538)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClientsCheckDialog.sizePolicy().hasHeightForWidth())
        ClientsCheckDialog.setSizePolicy(sizePolicy)
        ClientsCheckDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ClientsCheckDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = CProgressBar(ClientsCheckDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 5)
        self.btnStart = QtGui.QPushButton(ClientsCheckDialog)
        self.btnStart.setMinimumSize(QtCore.QSize(100, 0))
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(361, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.log = QtGui.QListWidget(ClientsCheckDialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 1, 0, 1, 5)
        self.label = QtGui.QLabel(ClientsCheckDialog)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(ClientsCheckDialog)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 2, 4, 1, 1)
        self.btnPrint = QtGui.QPushButton(ClientsCheckDialog)
        self.btnPrint.setMinimumSize(QtCore.QSize(100, 0))
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 2, 2, 1, 1)

        self.retranslateUi(ClientsCheckDialog)
        QtCore.QMetaObject.connectSlotsByName(ClientsCheckDialog)

    def retranslateUi(self, ClientsCheckDialog):
        ClientsCheckDialog.setWindowTitle(_translate("ClientsCheckDialog", "логический контроль клиентов", None))
        self.btnStart.setText(_translate("ClientsCheckDialog", "начать проверку", None))
        self.btnClose.setText(_translate("ClientsCheckDialog", "прервать", None))
        self.btnPrint.setText(_translate("ClientsCheckDialog", "печать", None))

from library.ProgressBar import CProgressBar
