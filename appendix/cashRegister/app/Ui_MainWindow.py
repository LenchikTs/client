# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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
        self.centralwidget = CMdiArea(CMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.menubar = QtGui.QMenuBar(CMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        self.menuReports = QtGui.QMenu(self.menubar)
        self.menuReports.setObjectName(_fromUtf8("menuReports"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        CMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(CMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        CMainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(CMainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(CMainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action1 = QtGui.QAction(CMainWindow)
        self.action1.setObjectName(_fromUtf8("action1"))
        self.action_4 = QtGui.QAction(CMainWindow)
        self.action_4.setObjectName(_fromUtf8("action_4"))
        self.action_5 = QtGui.QAction(CMainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))
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
        self.actReportX = QtGui.QAction(CMainWindow)
        self.actReportX.setObjectName(_fromUtf8("actReportX"))
        self.actReportOfdExchangeStatus = QtGui.QAction(CMainWindow)
        self.actReportOfdExchangeStatus.setObjectName(_fromUtf8("actReportOfdExchangeStatus"))
        self.actReportLastDocument = QtGui.QAction(CMainWindow)
        self.actReportLastDocument.setObjectName(_fromUtf8("actReportLastDocument"))
        self.actReportCashRegisterInfo = QtGui.QAction(CMainWindow)
        self.actReportCashRegisterInfo.setObjectName(_fromUtf8("actReportCashRegisterInfo"))
        self.actReportOfdTest = QtGui.QAction(CMainWindow)
        self.actReportOfdTest.setObjectName(_fromUtf8("actReportOfdTest"))
        self.actReportQuantity = QtGui.QAction(CMainWindow)
        self.actReportQuantity.setObjectName(_fromUtf8("actReportQuantity"))
        self.actReportOperators = QtGui.QAction(CMainWindow)
        self.actReportOperators.setObjectName(_fromUtf8("actReportOperators"))
        self.actReportHours = QtGui.QAction(CMainWindow)
        self.actReportHours.setObjectName(_fromUtf8("actReportHours"))
        self.actReportRegistration = QtGui.QAction(CMainWindow)
        self.actReportRegistration.setObjectName(_fromUtf8("actReportRegistration"))
        self.actReportShiftTotalCounters = QtGui.QAction(CMainWindow)
        self.actReportShiftTotalCounters.setObjectName(_fromUtf8("actReportShiftTotalCounters"))
        self.actReportFnTotalCounters = QtGui.QAction(CMainWindow)
        self.actReportFnTotalCounters.setObjectName(_fromUtf8("actReportFnTotalCounters"))
        self.menuPreferences.addAction(self.actConnection)
        self.menuPreferences.addSeparator()
        self.menuPreferences.addAction(self.actAppPreferences)
        self.menuPreferences.addAction(self.actDecor)
        self.menuReports.addAction(self.actReportX)
        self.menuReports.addAction(self.actReportLastDocument)
        self.menuReports.addAction(self.actReportOfdExchangeStatus)
        self.menuReports.addAction(self.actReportQuantity)
        self.menuReports.addAction(self.actReportOperators)
        self.menuReports.addAction(self.actReportHours)
        self.menuReports.addAction(self.actReportShiftTotalCounters)
        self.menuReports.addAction(self.actReportFnTotalCounters)
        self.menuReports.addSeparator()
        self.menuReports.addAction(self.actReportOfdTest)
        self.menuReports.addAction(self.actReportCashRegisterInfo)
        self.menuReports.addAction(self.actReportRegistration)
        self.menuFile.addAction(self.actLogin)
        self.menuFile.addAction(self.actLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actQuit)
        self.menuFile.addSeparator()
        self.menu.addAction(self.actAbout)
        self.menu.addAction(self.actAboutQt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuReports.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(CMainWindow)
        QtCore.QMetaObject.connectSlotsByName(CMainWindow)

    def retranslateUi(self, CMainWindow):
        CMainWindow.setWindowTitle(_translate("CMainWindow", "Самсон-Касса", None))
        self.menuPreferences.setTitle(_translate("CMainWindow", "Настройки", None))
        self.menuReports.setTitle(_translate("CMainWindow", "Отчёты", None))
        self.menuFile.setTitle(_translate("CMainWindow", "Сессия", None))
        self.menu.setTitle(_translate("CMainWindow", "Справка", None))
        self.action.setText(_translate("CMainWindow", "Соединение с ККМ", None))
        self.action_2.setText(_translate("CMainWindow", "Выход", None))
        self.action1.setText(_translate("CMainWindow", "1", None))
        self.action_4.setText(_translate("CMainWindow", "Настройки ККМ", None))
        self.action_5.setText(_translate("CMainWindow", "Настройки соединения с САМСОН", None))
        self.actLogin.setText(_translate("CMainWindow", "Подключиться к базе данных", None))
        self.actQuit.setText(_translate("CMainWindow", "Закрыть программу", None))
        self.actLogout.setText(_translate("CMainWindow", "Отключиться от базы данных", None))
        self.actConnection.setText(_translate("CMainWindow", "База данных", None))
        self.actDecor.setText(_translate("CMainWindow", "Внешний вид", None))
        self.actAppPreferences.setText(_translate("CMainWindow", "Умолчания", None))
        self.actAbout.setText(_translate("CMainWindow", "О програме", None))
        self.actAboutQt.setText(_translate("CMainWindow", "O Qt", None))
        self.actReportX.setText(_translate("CMainWindow", "X-отчет", None))
        self.actReportOfdExchangeStatus.setText(_translate("CMainWindow", "Отчет о состоянии расчетов", None))
        self.actReportLastDocument.setText(_translate("CMainWindow", "Копия последнего документа", None))
        self.actReportCashRegisterInfo.setText(_translate("CMainWindow", "Печать информации о ККТ", None))
        self.actReportOfdTest.setText(_translate("CMainWindow", "Диагностика соединения с ОФД", None))
        self.actReportQuantity.setText(_translate("CMainWindow", "Отчет количеств", None))
        self.actReportOperators.setText(_translate("CMainWindow", "Отчет по кассирам", None))
        self.actReportHours.setText(_translate("CMainWindow", "Отчет по часам", None))
        self.actReportRegistration.setText(_translate("CMainWindow", "Печать итогов регистрации / перерегистрации", None))
        self.actReportShiftTotalCounters.setText(_translate("CMainWindow", "Счетчики итогов смены", None))
        self.actReportFnTotalCounters.setText(_translate("CMainWindow", "Счетчики итогов ФН", None))

from library.MdiArea import CMdiArea

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CMainWindow = QtGui.QMainWindow()
    ui = Ui_CMainWindow()
    ui.setupUi(CMainWindow)
    CMainWindow.show()
    sys.exit(app.exec_())

