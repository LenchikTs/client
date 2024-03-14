# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVN\Samson\UP_s11\client\Registry\TMKSuspended.ui'
#
# Created: Mon Mar 22 10:50:38 2021
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

class Ui_TMKWindow(object):
    def setupUi(self, TMKWindow):
        TMKWindow.setObjectName(_fromUtf8("TMKWindow"))
        TMKWindow.resize(1511, 1025)
        self.horizontalLayout = QtGui.QHBoxLayout(TMKWindow)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(TMKWindow)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabSuspended = CSuspenedAppointmentWindow()
        self.tabSuspended.setObjectName(_fromUtf8("tabSuspended"))
        self.tabWidget.addTab(self.tabSuspended, _fromUtf8(""))
        self.tabTMK = CTMKWindow()
        self.tabTMK.setObjectName(_fromUtf8("tabTMK"))
        self.tabWidget.addTab(self.tabTMK, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(TMKWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TMKWindow)

    def retranslateUi(self, TMKWindow):
        TMKWindow.setWindowTitle(_translate("TMKWindow", "Журнал отложенной записи и сервис Телемедицины", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSuspended), _translate("TMKWindow", "Журнал отложенной записи", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTMK), _translate("TMKWindow", "Сервис телемедицины", None))

from Registry.TMKWindow import CTMKWindow
from Registry.SuspendedAppointment import CSuspenedAppointmentWindow
