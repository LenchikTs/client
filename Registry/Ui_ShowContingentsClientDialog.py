# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ShowContingentsClientDialog.ui'
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

class Ui_ShowContingentsClientDialog(object):
    def setupUi(self, ShowContingentsClientDialog):
        ShowContingentsClientDialog.setObjectName(_fromUtf8("ShowContingentsClientDialog"))
        ShowContingentsClientDialog.resize(327, 188)
        ShowContingentsClientDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(ShowContingentsClientDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txtClientContingentBrowser = CTextBrowser(ShowContingentsClientDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtClientContingentBrowser.sizePolicy().hasHeightForWidth())
        self.txtClientContingentBrowser.setSizePolicy(sizePolicy)
        self.txtClientContingentBrowser.setObjectName(_fromUtf8("txtClientContingentBrowser"))
        self.gridLayout.addWidget(self.txtClientContingentBrowser, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ShowContingentsClientDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(ShowContingentsClientDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ShowContingentsClientDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ShowContingentsClientDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ShowContingentsClientDialog)

    def retranslateUi(self, ShowContingentsClientDialog):
        ShowContingentsClientDialog.setWindowTitle(_translate("ShowContingentsClientDialog", "Наблюдаемые контингенты", None))

from library.TextBrowser import CTextBrowser
