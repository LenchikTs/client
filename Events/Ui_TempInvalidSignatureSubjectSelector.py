# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\TempInvalidSignatureSubjectSelector.ui'
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

class Ui_TempInvalidSignatureSubjectSelector(object):
    def setupUi(self, TempInvalidSignatureSubjectSelector):
        TempInvalidSignatureSubjectSelector.setObjectName(_fromUtf8("TempInvalidSignatureSubjectSelector"))
        TempInvalidSignatureSubjectSelector.resize(400, 300)
        TempInvalidSignatureSubjectSelector.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(TempInvalidSignatureSubjectSelector)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblDocumentSubjects = CInDocTableView(TempInvalidSignatureSubjectSelector)
        self.tblDocumentSubjects.setObjectName(_fromUtf8("tblDocumentSubjects"))
        self.gridLayout.addWidget(self.tblDocumentSubjects, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidSignatureSubjectSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(TempInvalidSignatureSubjectSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidSignatureSubjectSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidSignatureSubjectSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidSignatureSubjectSelector)
        TempInvalidSignatureSubjectSelector.setTabOrder(self.tblDocumentSubjects, self.buttonBox)

    def retranslateUi(self, TempInvalidSignatureSubjectSelector):
        TempInvalidSignatureSubjectSelector.setWindowTitle(_translate("TempInvalidSignatureSubjectSelector", "Перечень элементов ЭЛН, подлежащих подписыванию", None))

from library.InDocTable import CInDocTableView
