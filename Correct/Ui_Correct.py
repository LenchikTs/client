# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Correct\Correct.ui'
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

class Ui_Correct(object):
    def setupUi(self, Correct):
        Correct.setObjectName(_fromUtf8("Correct"))
        Correct.resize(800, 600)
        self.centralwidget = QtGui.QWidget(Correct)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        Correct.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Correct)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        Correct.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Correct)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Correct.setStatusBar(self.statusbar)
        self.actLogin = QtGui.QAction(Correct)
        self.actLogin.setObjectName(_fromUtf8("actLogin"))
        self.actLogout = QtGui.QAction(Correct)
        self.actLogout.setObjectName(_fromUtf8("actLogout"))
        self.actConnectSettings = QtGui.QAction(Correct)
        self.actConnectSettings.setObjectName(_fromUtf8("actConnectSettings"))
        self.actAbout = QtGui.QAction(Correct)
        self.actAbout.setObjectName(_fromUtf8("actAbout"))
        self.actAboutQt = QtGui.QAction(Correct)
        self.actAboutQt.setObjectName(_fromUtf8("actAboutQt"))
        self.menu.addAction(self.actLogin)
        self.menu.addAction(self.actLogout)
        self.menu_2.addAction(self.actConnectSettings)
        self.menu_3.addAction(self.actAbout)
        self.menu_3.addAction(self.actAboutQt)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(Correct)
        QtCore.QMetaObject.connectSlotsByName(Correct)

    def retranslateUi(self, Correct):
        Correct.setWindowTitle(_translate("Correct", "MainWindow", None))
        self.menu.setTitle(_translate("Correct", "Меню", None))
        self.menu_2.setTitle(_translate("Correct", "Настройки", None))
        self.menu_3.setTitle(_translate("Correct", "Помощь", None))
        self.actLogin.setText(_translate("Correct", "Подключиться", None))
        self.actLogout.setText(_translate("Correct", "Отключиться", None))
        self.actConnectSettings.setText(_translate("Correct", "Подключение к БД", None))
        self.actAbout.setText(_translate("Correct", "О программе", None))
        self.actAboutQt.setText(_translate("Correct", "О Qt", None))

