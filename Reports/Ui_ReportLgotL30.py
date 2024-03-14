# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportLgotL30.ui'
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

class Ui_ReportLgotL30SetupDialog(object):
    def setupUi(self, ReportLgotL30SetupDialog):
        ReportLgotL30SetupDialog.setObjectName(_fromUtf8("ReportLgotL30SetupDialog"))
        ReportLgotL30SetupDialog.resize(315, 115)
        self.gridLayout = QtGui.QGridLayout(ReportLgotL30SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ReportLgotL30SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportLgotL30SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.edtBegDate = CDateEdit(ReportLgotL30SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(ReportLgotL30SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 3, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportLgotL30SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportLgotL30SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportLgotL30SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportLgotL30SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportLgotL30SetupDialog)

    def retranslateUi(self, ReportLgotL30SetupDialog):
        ReportLgotL30SetupDialog.setWindowTitle(_translate("ReportLgotL30SetupDialog", "параметры отчета", None))
        self.lblBegDate.setText(_translate("ReportLgotL30SetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportLgotL30SetupDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportLgotL30SetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportLgotL30SetupDialog", "Дата &окончания периода", None))

from library.DateEdit import CDateEdit
