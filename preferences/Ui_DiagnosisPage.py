# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_DN\preferences\DiagnosisPage.ui'
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

class Ui_DiagnosisPage(object):
    def setupUi(self, DiagnosisPage):
        DiagnosisPage.setObjectName(_fromUtf8("DiagnosisPage"))
        DiagnosisPage.resize(651, 405)
        self.gridLayout = QtGui.QGridLayout(DiagnosisPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.lblAnalyze = QtGui.QLabel(DiagnosisPage)
        self.lblAnalyze.setObjectName(_fromUtf8("lblAnalyze"))
        self.gridLayout.addWidget(self.lblAnalyze, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(400, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.chkAnalyzeSurveillance = QtGui.QCheckBox(DiagnosisPage)
        self.chkAnalyzeSurveillance.setText(_fromUtf8(""))
        self.chkAnalyzeSurveillance.setObjectName(_fromUtf8("chkAnalyzeSurveillance"))
        self.gridLayout.addWidget(self.chkAnalyzeSurveillance, 2, 1, 1, 1)
        self.lblAnalyze.setBuddy(self.chkAnalyzeSurveillance)

        self.retranslateUi(DiagnosisPage)
        QtCore.QMetaObject.connectSlotsByName(DiagnosisPage)

    def retranslateUi(self, DiagnosisPage):
        DiagnosisPage.setWindowTitle(_translate("DiagnosisPage", "Панель «ЛУД»", None))
        DiagnosisPage.setToolTip(_translate("DiagnosisPage", "Поведение панели «ЛУД»", None))
        self.lblAnalyze.setText(_translate("DiagnosisPage", "Анализ ДН", None))

