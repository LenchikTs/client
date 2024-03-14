# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_eln\appendix\fsselnv2\app\MainWindow.ui'
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

class Ui_CMainWindow(object):
    def setupUi(self, CMainWindow):
        CMainWindow.setObjectName(_fromUtf8("CMainWindow"))
        CMainWindow.resize(551, 558)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Icon2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CMainWindow.setWindowIcon(icon)
        self.centralwidget = CMdiArea(CMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.menubar = QtGui.QMenuBar(CMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        CMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(CMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        CMainWindow.setStatusBar(self.statusbar)
        self.actLogin = QtGui.QAction(CMainWindow)
        self.actLogin.setObjectName(_fromUtf8("actLogin"))
        self.actQuit = QtGui.QAction(CMainWindow)
        self.actQuit.setObjectName(_fromUtf8("actQuit"))
        self.actLogout = QtGui.QAction(CMainWindow)
        self.actLogout.setObjectName(_fromUtf8("actLogout"))
        self.actConnection = QtGui.QAction(CMainWindow)
        self.actConnection.setObjectName(_fromUtf8("actConnection"))
        self.actDecor = QtGui.QAction(CMainWindow)
        self.actDecor.setObjectName(_fromUtf8("actDecor"))
        self.actAppPreferences = QtGui.QAction(CMainWindow)
        self.actAppPreferences.setObjectName(_fromUtf8("actAppPreferences"))
        self.actAbout = QtGui.QAction(CMainWindow)
        self.actAbout.setMenuRole(QtGui.QAction.AboutRole)
        self.actAbout.setObjectName(_fromUtf8("actAbout"))
        self.actAboutQt = QtGui.QAction(CMainWindow)
        self.actAboutQt.setMenuRole(QtGui.QAction.AboutQtRole)
        self.actAboutQt.setObjectName(_fromUtf8("actAboutQt"))
        self.menuPreferences.addAction(self.actConnection)
        self.menuPreferences.addSeparator()
        self.menuPreferences.addAction(self.actAppPreferences)
        self.menuPreferences.addAction(self.actDecor)
        self.menuFile.addAction(self.actLogin)
        self.menuFile.addAction(self.actLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actQuit)
        self.menuFile.addSeparator()
        self.menu.addAction(self.actAbout)
        self.menu.addAction(self.actAboutQt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(CMainWindow)
        QtCore.QMetaObject.connectSlotsByName(CMainWindow)

    def retranslateUi(self, CMainWindow):
        CMainWindow.setWindowTitle(_translate("CMainWindow", "Самсон-СФР-ЭЛН", None))
        self.menuPreferences.setTitle(_translate("CMainWindow", "Настройки", None))
        self.menuFile.setTitle(_translate("CMainWindow", "Сессия", None))
        self.menu.setTitle(_translate("CMainWindow", "Справка", None))
        self.actLogin.setText(_translate("CMainWindow", "Подключиться к базе данных", None))
        self.actQuit.setText(_translate("CMainWindow", "Закрыть программу", None))
        self.actLogout.setText(_translate("CMainWindow", "Отключиться от базы данных", None))
        self.actConnection.setText(_translate("CMainWindow", "База данных", None))
        self.actDecor.setText(_translate("CMainWindow", "Внешний вид", None))
        self.actAppPreferences.setText(_translate("CMainWindow", "Умолчания", None))
        self.actAbout.setText(_translate("CMainWindow", "О програме", None))
        self.actAboutQt.setText(_translate("CMainWindow", "O Qt", None))

from library.MdiArea import CMdiArea
import s11main_rc
