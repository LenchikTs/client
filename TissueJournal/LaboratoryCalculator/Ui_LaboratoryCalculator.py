# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\TissueJournal\LaboratoryCalculator\LaboratoryCalculator.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(690, 420)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actLogin = QtGui.QAction(MainWindow)
        self.actLogin.setObjectName(_fromUtf8("actLogin"))
        self.actLogout = QtGui.QAction(MainWindow)
        self.actLogout.setObjectName(_fromUtf8("actLogout"))
        self.actExit = QtGui.QAction(MainWindow)
        self.actExit.setObjectName(_fromUtf8("actExit"))
        self.actConnection = QtGui.QAction(MainWindow)
        self.actConnection.setObjectName(_fromUtf8("actConnection"))
        self.actAboutQt = QtGui.QAction(MainWindow)
        self.actAboutQt.setObjectName(_fromUtf8("actAboutQt"))
        self.actAbout = QtGui.QAction(MainWindow)
        self.actAbout.setObjectName(_fromUtf8("actAbout"))
        self.actDecor = QtGui.QAction(MainWindow)
        self.actDecor.setObjectName(_fromUtf8("actDecor"))
        self.menu.addAction(self.actLogin)
        self.menu.addAction(self.actLogout)
        self.menu.addSeparator()
        self.menu.addAction(self.actExit)
        self.menu_2.addAction(self.actConnection)
        self.menu_2.addAction(self.actDecor)
        self.menu_3.addAction(self.actAboutQt)
        self.menu_3.addAction(self.actAbout)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menu.setTitle(_translate("MainWindow", "Меню", None))
        self.menu_2.setTitle(_translate("MainWindow", "Настройки", None))
        self.menu_3.setTitle(_translate("MainWindow", "Помощь", None))
        self.actLogin.setText(_translate("MainWindow", "Подключиться", None))
        self.actLogout.setText(_translate("MainWindow", " Отключиться", None))
        self.actExit.setText(_translate("MainWindow", " Выйти", None))
        self.actConnection.setText(_translate("MainWindow", "База данных", None))
        self.actAboutQt.setText(_translate("MainWindow", "О Qt", None))
        self.actAbout.setText(_translate("MainWindow", "О программе", None))
        self.actDecor.setText(_translate("MainWindow", "Внешний вид", None))

