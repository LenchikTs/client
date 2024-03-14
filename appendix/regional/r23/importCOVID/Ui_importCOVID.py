# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\appendix\regional\r23\importCOVID\importCOVID.ui'
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
        MainWindow.resize(915, 536)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDBF = QtGui.QLabel(self.centralwidget)
        self.lblDBF.setObjectName(_fromUtf8("lblDBF"))
        self.gridLayout.addWidget(self.lblDBF, 0, 0, 1, 1)
        self.edtDBFFileName = QtGui.QLineEdit(self.centralwidget)
        self.edtDBFFileName.setObjectName(_fromUtf8("edtDBFFileName"))
        self.gridLayout.addWidget(self.edtDBFFileName, 0, 1, 1, 1)
        self.btnSelectDBFFile = QtGui.QToolButton(self.centralwidget)
        self.btnSelectDBFFile.setObjectName(_fromUtf8("btnSelectDBFFile"))
        self.gridLayout.addWidget(self.btnSelectDBFFile, 0, 2, 1, 1)
        self.btnProcessDBF = QtGui.QPushButton(self.centralwidget)
        self.btnProcessDBF.setEnabled(False)
        self.btnProcessDBF.setObjectName(_fromUtf8("btnProcessDBF"))
        self.gridLayout.addWidget(self.btnProcessDBF, 0, 3, 1, 1)
        self.btnImport = QtGui.QPushButton(self.centralwidget)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.gridLayout.addWidget(self.btnImport, 0, 4, 1, 1)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblDBF = CInDocTableView(self.splitter)
        self.tblDBF.setObjectName(_fromUtf8("tblDBF"))
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 915, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actLogin = QtGui.QAction(MainWindow)
        self.actLogin.setObjectName(_fromUtf8("actLogin"))
        self.actLogout = QtGui.QAction(MainWindow)
        self.actLogout.setObjectName(_fromUtf8("actLogout"))
        self.actQuit = QtGui.QAction(MainWindow)
        self.actQuit.setObjectName(_fromUtf8("actQuit"))
        self.actConnection = QtGui.QAction(MainWindow)
        self.actConnection.setObjectName(_fromUtf8("actConnection"))
        self.actDecor = QtGui.QAction(MainWindow)
        self.actDecor.setObjectName(_fromUtf8("actDecor"))
        self.actPreferences = QtGui.QAction(MainWindow)
        self.actPreferences.setObjectName(_fromUtf8("actPreferences"))
        self.menuFile.addAction(self.actLogin)
        self.menuFile.addAction(self.actLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actQuit)
        self.menuPreferences.addAction(self.actConnection)
        self.menuPreferences.addAction(self.actDecor)
        self.menuPreferences.addAction(self.actPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Импорт COVID", None))
        self.lblDBF.setText(_translate("MainWindow", "Путь к файлу", None))
        self.edtDBFFileName.setToolTip(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Укажите местонахождение файла</span><span style=\" font-size:8pt; font-weight:600;\"> spr18.dbf </span><span style=\" font-size:8pt;\">в формате, определенном Положением о порядке информационного обмена в системе обязательного медицинского страхования на территории Краснодарского края Версии 8.0</span></p></body></html>", None))
        self.btnSelectDBFFile.setText(_translate("MainWindow", "...", None))
        self.btnProcessDBF.setText(_translate("MainWindow", "Открыть", None))
        self.btnImport.setText(_translate("MainWindow", "Импорт", None))
        self.menuFile.setTitle(_translate("MainWindow", "Сессия", None))
        self.menuPreferences.setTitle(_translate("MainWindow", "Настройки", None))
        self.actLogin.setText(_translate("MainWindow", "Подключиться к базе данных", None))
        self.actLogout.setText(_translate("MainWindow", "Отключиться от базы данных", None))
        self.actQuit.setText(_translate("MainWindow", "Закрыть программу", None))
        self.actConnection.setText(_translate("MainWindow", "База данных", None))
        self.actDecor.setText(_translate("MainWindow", "Внешний вид", None))
        self.actPreferences.setText(_translate("MainWindow", "Умолчания", None))

from library.InDocTable import CInDocTableView
