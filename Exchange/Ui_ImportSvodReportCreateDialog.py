# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\kmivc\Samson\UP_s11\client\Exchange\ImportSvodReportCreateDialog.ui'
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

class Ui_SvodReportCreateDialog(object):
    def setupUi(self, SvodReportCreateDialog):
        SvodReportCreateDialog.setObjectName(_fromUtf8("SvodReportCreateDialog"))
        SvodReportCreateDialog.resize(296, 67)
        self.gridLayout = QtGui.QGridLayout(SvodReportCreateDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SvodReportCreateDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbForm = QtGui.QComboBox(SvodReportCreateDialog)
        self.cmbForm.setObjectName(_fromUtf8("cmbForm"))
        self.gridLayout.addWidget(self.cmbForm, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SvodReportCreateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(SvodReportCreateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SvodReportCreateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SvodReportCreateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SvodReportCreateDialog)

    def retranslateUi(self, SvodReportCreateDialog):
        SvodReportCreateDialog.setWindowTitle(_translate("SvodReportCreateDialog", "Новый отчет", None))
        self.label.setText(_translate("SvodReportCreateDialog", "Форма", None))

