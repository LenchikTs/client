# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\Events\TempInvalidTransferSubjectSelector.ui'
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

class Ui_TempInvalidTransferSubjectSelector(object):
    def setupUi(self, TempInvalidTransferSubjectSelector):
        TempInvalidTransferSubjectSelector.setObjectName(_fromUtf8("TempInvalidTransferSubjectSelector"))
        TempInvalidTransferSubjectSelector.resize(608, 354)
        TempInvalidTransferSubjectSelector.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(TempInvalidTransferSubjectSelector)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidTransferSubjectSelector)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.tblReadyTempInvalidDocuments = CTableView(TempInvalidTransferSubjectSelector)
        self.tblReadyTempInvalidDocuments.setObjectName(_fromUtf8("tblReadyTempInvalidDocuments"))
        self.gridLayout.addWidget(self.tblReadyTempInvalidDocuments, 0, 0, 1, 3)
        self.btnTransfer = QtGui.QPushButton(TempInvalidTransferSubjectSelector)
        self.btnTransfer.setEnabled(False)
        self.btnTransfer.setObjectName(_fromUtf8("btnTransfer"))
        self.gridLayout.addWidget(self.btnTransfer, 1, 2, 1, 1)

        self.retranslateUi(TempInvalidTransferSubjectSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidTransferSubjectSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidTransferSubjectSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidTransferSubjectSelector)
        TempInvalidTransferSubjectSelector.setTabOrder(self.tblReadyTempInvalidDocuments, self.buttonBox)

    def retranslateUi(self, TempInvalidTransferSubjectSelector):
        TempInvalidTransferSubjectSelector.setWindowTitle(_translate("TempInvalidTransferSubjectSelector", "Документы для передачи", None))
        self.btnTransfer.setText(_translate("TempInvalidTransferSubjectSelector", "Передать", None))

from library.TableView import CTableView
