# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\AmbulatoryCardDialog.ui'
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

class Ui_AmbulatoryCardDialog(object):
    def setupUi(self, AmbulatoryCardDialog):
        AmbulatoryCardDialog.setObjectName(_fromUtf8("AmbulatoryCardDialog"))
        AmbulatoryCardDialog.resize(733, 556)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AmbulatoryCardDialog.sizePolicy().hasHeightForWidth())
        AmbulatoryCardDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(AmbulatoryCardDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ambulatoryCardPage = CAmbulatoryCardPage(AmbulatoryCardDialog)
        self.ambulatoryCardPage.setObjectName(_fromUtf8("ambulatoryCardPage"))
        self.gridLayout.addWidget(self.ambulatoryCardPage, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(AmbulatoryCardDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(AmbulatoryCardDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AmbulatoryCardDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AmbulatoryCardDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AmbulatoryCardDialog)

    def retranslateUi(self, AmbulatoryCardDialog):
        AmbulatoryCardDialog.setWindowTitle(_translate("AmbulatoryCardDialog", "Dialog", None))

from Events.AmbulatoryCardPage import CAmbulatoryCardPage
