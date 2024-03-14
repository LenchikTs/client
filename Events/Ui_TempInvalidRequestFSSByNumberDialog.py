# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\Events\TempInvalidRequestFSSByNumberDialog.ui'
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

class Ui_TempInvalidRequestFSSByNumberDialog(object):
    def setupUi(self, TempInvalidRequestFSSByNumberDialog):
        TempInvalidRequestFSSByNumberDialog.setObjectName(_fromUtf8("TempInvalidRequestFSSByNumberDialog"))
        TempInvalidRequestFSSByNumberDialog.resize(534, 85)
        self.verticalLayout = QtGui.QVBoxLayout(TempInvalidRequestFSSByNumberDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblQuery = QtGui.QLabel(TempInvalidRequestFSSByNumberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblQuery.sizePolicy().hasHeightForWidth())
        self.lblQuery.setSizePolicy(sizePolicy)
        self.lblQuery.setObjectName(_fromUtf8("lblQuery"))
        self.horizontalLayout.addWidget(self.lblQuery)
        self.edtQuery = QtGui.QLineEdit(TempInvalidRequestFSSByNumberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtQuery.sizePolicy().hasHeightForWidth())
        self.edtQuery.setSizePolicy(sizePolicy)
        self.edtQuery.setMinimumSize(QtCore.QSize(250, 0))
        self.edtQuery.setToolTip(_fromUtf8(""))
        self.edtQuery.setObjectName(_fromUtf8("edtQuery"))
        self.horizontalLayout.addWidget(self.edtQuery)
        self.btnQuery = QtGui.QPushButton(TempInvalidRequestFSSByNumberDialog)
        self.btnQuery.setObjectName(_fromUtf8("btnQuery"))
        self.horizontalLayout.addWidget(self.btnQuery)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidRequestFSSByNumberDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TempInvalidRequestFSSByNumberDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidRequestFSSByNumberDialog.close)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidRequestFSSByNumberDialog)

    def retranslateUi(self, TempInvalidRequestFSSByNumberDialog):
        TempInvalidRequestFSSByNumberDialog.setWindowTitle(_translate("TempInvalidRequestFSSByNumberDialog", "Запрос состояния ЭЛН по номеру", None))
        self.lblQuery.setText(_translate("TempInvalidRequestFSSByNumberDialog", "Номер ЭЛН", None))
        self.edtQuery.setInputMask(_translate("TempInvalidRequestFSSByNumberDialog", "999999999999; ", None))
        self.btnQuery.setText(_translate("TempInvalidRequestFSSByNumberDialog", "Искать", None))

