# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVN\Samson\UP_s11\client\Reports\ReportWEBView.ui'
#
# Created: Fri Nov 15 11:05:37 2019
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ReportViewDialog(object):
    def setupUi(self, ReportViewDialog):
        ReportViewDialog.setObjectName(_fromUtf8("ReportViewDialog"))
        ReportViewDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportViewDialog.resize(929, 597)
        ReportViewDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportViewDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lineEdit = QtGui.QLineEdit(ReportViewDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridlayout.addWidget(self.lineEdit, 0, 0, 1, 5)
        self.txtReport = QtWebKit.QWebView(ReportViewDialog)
        self.txtReport.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.txtReport.setObjectName(_fromUtf8("txtReport"))
        self.gridlayout.addWidget(self.txtReport, 2, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(ReportViewDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Retry|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.btnBack = QtGui.QPushButton(ReportViewDialog)
        self.btnBack.setMaximumSize(QtCore.QSize(70, 16777215))
        self.btnBack.setObjectName(_fromUtf8("btnBack"))
        self.gridlayout.addWidget(self.btnBack, 3, 1, 1, 1)

        self.retranslateUi(ReportViewDialog)
        QtCore.QMetaObject.connectSlotsByName(ReportViewDialog)

    def retranslateUi(self, ReportViewDialog):
        ReportViewDialog.setWindowTitle(_translate("ReportViewDialog", "просмотр отчёта", None))
        self.btnBack.setText(_translate("ReportViewDialog", "Назад", None))

from PyQt4 import QtWebKit
