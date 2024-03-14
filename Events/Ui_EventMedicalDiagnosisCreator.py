# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventMedicalDiagnosisCreator.ui'
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

class Ui_EventMedicalDiagnosisCreator(object):
    def setupUi(self, EventMedicalDiagnosisCreator):
        EventMedicalDiagnosisCreator.setObjectName(_fromUtf8("EventMedicalDiagnosisCreator"))
        EventMedicalDiagnosisCreator.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(EventMedicalDiagnosisCreator)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionTypes = CTableView(EventMedicalDiagnosisCreator)
        self.tblActionTypes.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblActionTypes.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblActionTypes.setObjectName(_fromUtf8("tblActionTypes"))
        self.gridLayout.addWidget(self.tblActionTypes, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EventMedicalDiagnosisCreator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EventMedicalDiagnosisCreator)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventMedicalDiagnosisCreator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventMedicalDiagnosisCreator.reject)
        QtCore.QMetaObject.connectSlotsByName(EventMedicalDiagnosisCreator)

    def retranslateUi(self, EventMedicalDiagnosisCreator):
        EventMedicalDiagnosisCreator.setWindowTitle(_translate("EventMedicalDiagnosisCreator", "Выберите тип действия", None))

from library.TableView import CTableView
