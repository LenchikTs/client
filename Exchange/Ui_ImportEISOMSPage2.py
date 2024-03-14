# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportEISOMSPage2.ui'
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

class Ui_ImportEISOMSPage2(object):
    def setupUi(self, ImportEISOMSPage2):
        ImportEISOMSPage2.setObjectName(_fromUtf8("ImportEISOMSPage2"))
        ImportEISOMSPage2.resize(410, 300)
        self.gridlayout = QtGui.QGridLayout(ImportEISOMSPage2)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.progressBar = CProgressBar(ImportEISOMSPage2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 0, 0, 1, 4)
        self.lblAcceptedLabel = QtGui.QLabel(ImportEISOMSPage2)
        self.lblAcceptedLabel.setObjectName(_fromUtf8("lblAcceptedLabel"))
        self.gridlayout.addWidget(self.lblAcceptedLabel, 1, 0, 1, 1)
        self.lblAccepted = QtGui.QLabel(ImportEISOMSPage2)
        self.lblAccepted.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblAccepted.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblAccepted.setTextFormat(QtCore.Qt.PlainText)
        self.lblAccepted.setScaledContents(False)
        self.lblAccepted.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblAccepted.setObjectName(_fromUtf8("lblAccepted"))
        self.gridlayout.addWidget(self.lblAccepted, 1, 1, 1, 1)
        self.lblIntegrityErrorLabel = QtGui.QLabel(ImportEISOMSPage2)
        self.lblIntegrityErrorLabel.setObjectName(_fromUtf8("lblIntegrityErrorLabel"))
        self.gridlayout.addWidget(self.lblIntegrityErrorLabel, 1, 2, 1, 1)
        self.lblIntegrityError = QtGui.QLabel(ImportEISOMSPage2)
        self.lblIntegrityError.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblIntegrityError.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblIntegrityError.setTextFormat(QtCore.Qt.PlainText)
        self.lblIntegrityError.setScaledContents(False)
        self.lblIntegrityError.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblIntegrityError.setObjectName(_fromUtf8("lblIntegrityError"))
        self.gridlayout.addWidget(self.lblIntegrityError, 1, 3, 1, 1)
        self.lblRefusedLabel = QtGui.QLabel(ImportEISOMSPage2)
        self.lblRefusedLabel.setObjectName(_fromUtf8("lblRefusedLabel"))
        self.gridlayout.addWidget(self.lblRefusedLabel, 2, 0, 1, 1)
        self.lblRefused = QtGui.QLabel(ImportEISOMSPage2)
        self.lblRefused.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblRefused.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblRefused.setTextFormat(QtCore.Qt.PlainText)
        self.lblRefused.setScaledContents(False)
        self.lblRefused.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRefused.setObjectName(_fromUtf8("lblRefused"))
        self.gridlayout.addWidget(self.lblRefused, 2, 1, 1, 1)
        self.lblChangeDisabledLabel = QtGui.QLabel(ImportEISOMSPage2)
        self.lblChangeDisabledLabel.setObjectName(_fromUtf8("lblChangeDisabledLabel"))
        self.gridlayout.addWidget(self.lblChangeDisabledLabel, 2, 2, 1, 1)
        self.lblChangeDisabled = QtGui.QLabel(ImportEISOMSPage2)
        self.lblChangeDisabled.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblChangeDisabled.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblChangeDisabled.setTextFormat(QtCore.Qt.PlainText)
        self.lblChangeDisabled.setScaledContents(False)
        self.lblChangeDisabled.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblChangeDisabled.setObjectName(_fromUtf8("lblChangeDisabled"))
        self.gridlayout.addWidget(self.lblChangeDisabled, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(151, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 2)
        self.lblUncheckedLabel = QtGui.QLabel(ImportEISOMSPage2)
        self.lblUncheckedLabel.setObjectName(_fromUtf8("lblUncheckedLabel"))
        self.gridlayout.addWidget(self.lblUncheckedLabel, 3, 2, 1, 1)
        self.lblUnchecked = QtGui.QLabel(ImportEISOMSPage2)
        self.lblUnchecked.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblUnchecked.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblUnchecked.setTextFormat(QtCore.Qt.PlainText)
        self.lblUnchecked.setScaledContents(False)
        self.lblUnchecked.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblUnchecked.setObjectName(_fromUtf8("lblUnchecked"))
        self.gridlayout.addWidget(self.lblUnchecked, 3, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(392, 111, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 4, 0, 1, 4)

        self.retranslateUi(ImportEISOMSPage2)
        QtCore.QMetaObject.connectSlotsByName(ImportEISOMSPage2)

    def retranslateUi(self, ImportEISOMSPage2):
        ImportEISOMSPage2.setWindowTitle(_translate("ImportEISOMSPage2", "Form", None))
        self.lblAcceptedLabel.setText(_translate("ImportEISOMSPage2", "принято", None))
        self.lblAccepted.setText(_translate("ImportEISOMSPage2", "0", None))
        self.lblIntegrityErrorLabel.setText(_translate("ImportEISOMSPage2", "нет в реестре", None))
        self.lblIntegrityError.setText(_translate("ImportEISOMSPage2", "0", None))
        self.lblRefusedLabel.setText(_translate("ImportEISOMSPage2", "отказано", None))
        self.lblRefused.setText(_translate("ImportEISOMSPage2", "0", None))
        self.lblChangeDisabledLabel.setText(_translate("ImportEISOMSPage2", "не подлежит изменению", None))
        self.lblChangeDisabled.setText(_translate("ImportEISOMSPage2", "0", None))
        self.lblUncheckedLabel.setText(_translate("ImportEISOMSPage2", "не обработано ЕИС-ОМС", None))
        self.lblUnchecked.setText(_translate("ImportEISOMSPage2", "0", None))

from library.ProgressBar import CProgressBar
