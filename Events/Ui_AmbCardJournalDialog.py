# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\AmbCardJournalDialog.ui'
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

class Ui_AmbCardJournalDialog(object):
    def setupUi(self, AmbCardJournalDialog):
        AmbCardJournalDialog.setObjectName(_fromUtf8("AmbCardJournalDialog"))
        AmbCardJournalDialog.resize(733, 556)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AmbCardJournalDialog.sizePolicy().hasHeightForWidth())
        AmbCardJournalDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(AmbCardJournalDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ambCardPage = CAmbCardJournalPage(AmbCardJournalDialog)
        self.ambCardPage.setObjectName(_fromUtf8("ambCardPage"))
        self.gridLayout.addWidget(self.ambCardPage, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(AmbCardJournalDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.btnRowSelect = QtGui.QPushButton(AmbCardJournalDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRowSelect.sizePolicy().hasHeightForWidth())
        self.btnRowSelect.setSizePolicy(sizePolicy)
        self.btnRowSelect.setObjectName(_fromUtf8("btnRowSelect"))
        self.gridLayout.addWidget(self.btnRowSelect, 1, 0, 1, 1)

        self.retranslateUi(AmbCardJournalDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AmbCardJournalDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AmbCardJournalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AmbCardJournalDialog)

    def retranslateUi(self, AmbCardJournalDialog):
        AmbCardJournalDialog.setWindowTitle(_translate("AmbCardJournalDialog", "Dialog", None))
        self.btnRowSelect.setText(_translate("AmbCardJournalDialog", "Переключить", None))

from Events.AmbCardJournalPage import CAmbCardJournalPage
