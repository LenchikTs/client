# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Registry\DispExchange.ui'
#
# Created: Tue Feb 19 13:39:53 2019
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

class Ui_DispExchangeWindow(object):
    def setupUi(self, DispExchangeWindow):
        DispExchangeWindow.setObjectName(_fromUtf8("DispExchangeWindow"))
        DispExchangeWindow.resize(1511, 1025)
        self.horizontalLayout = QtGui.QHBoxLayout(DispExchangeWindow)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(DispExchangeWindow)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabProfilactic = CDispExchangeProfilacticPage()
        self.tabProfilactic.setObjectName(_fromUtf8("tabProfilactic"))
        self.tabWidget.addTab(self.tabProfilactic, _fromUtf8(""))
        self.tabDiagnosis = CDispExchangeDiagnosisPage()
        self.tabDiagnosis.setObjectName(_fromUtf8("tabDiagnosis"))
        self.tabWidget.addTab(self.tabDiagnosis, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(DispExchangeWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DispExchangeWindow)

    def retranslateUi(self, DispExchangeWindow):
        DispExchangeWindow.setWindowTitle(_translate("DispExchangeWindow", "Сервис диспансеризации", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProfilactic), _translate("DispExchangeWindow", "Проф. мероприятия", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDiagnosis), _translate("DispExchangeWindow", "Диспансерные осмотры", None))

from Registry.DispExchangeDiagnosisPage import CDispExchangeDiagnosisPage
from Registry.DispExchangeProfilacticPage import CDispExchangeProfilacticPage
