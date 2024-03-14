# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pvtr/py-dev/samson/appendix/importNomenclature/importNomenclature.ui'
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
        MainWindow.resize(722, 679)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hlImport = QtGui.QHBoxLayout()
        self.hlImport.setObjectName(_fromUtf8("hlImport"))
        self.lblFileName = QtGui.QLabel(self.centralwidget)
        self.lblFileName.setObjectName(_fromUtf8("lblFileName"))
        self.hlImport.addWidget(self.lblFileName)
        self.edtFileName = QtGui.QLineEdit(self.centralwidget)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hlImport.addWidget(self.edtFileName)
        self.btnSelectFileName = QtGui.QToolButton(self.centralwidget)
        self.btnSelectFileName.setObjectName(_fromUtf8("btnSelectFileName"))
        self.hlImport.addWidget(self.btnSelectFileName)
        self.btnImport = QtGui.QPushButton(self.centralwidget)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hlImport.addWidget(self.btnImport)
        self.verticalLayout.addLayout(self.hlImport)
        self.hlExport = QtGui.QHBoxLayout()
        self.hlExport.setObjectName(_fromUtf8("hlExport"))
        self.lblExport = QtGui.QLabel(self.centralwidget)
        self.lblExport.setObjectName(_fromUtf8("lblExport"))
        self.hlExport.addWidget(self.lblExport)
        self.edtExportFileName = QtGui.QLineEdit(self.centralwidget)
        self.edtExportFileName.setObjectName(_fromUtf8("edtExportFileName"))
        self.hlExport.addWidget(self.edtExportFileName)
        self.btnSelectExportFileName = QtGui.QToolButton(self.centralwidget)
        self.btnSelectExportFileName.setObjectName(_fromUtf8("btnSelectExportFileName"))
        self.hlExport.addWidget(self.btnSelectExportFileName)
        self.btnExport = QtGui.QPushButton(self.centralwidget)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.hlExport.addWidget(self.btnExport)
        self.verticalLayout.addLayout(self.hlExport)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actLogin = QtGui.QAction(MainWindow)
        self.actLogin.setObjectName(_fromUtf8("actLogin"))
        self.actLogout = QtGui.QAction(MainWindow)
        self.actLogout.setEnabled(False)
        self.actLogout.setObjectName(_fromUtf8("actLogout"))
        self.actQuit = QtGui.QAction(MainWindow)
        self.actQuit.setObjectName(_fromUtf8("actQuit"))
        self.actConnection = QtGui.QAction(MainWindow)
        self.actConnection.setObjectName(_fromUtf8("actConnection"))
        self.actDecor = QtGui.QAction(MainWindow)
        self.actDecor.setObjectName(_fromUtf8("actDecor"))
        self.actAbout = QtGui.QAction(MainWindow)
        self.actAbout.setObjectName(_fromUtf8("actAbout"))
        self.actAboutQt = QtGui.QAction(MainWindow)
        self.actAboutQt.setObjectName(_fromUtf8("actAboutQt"))
        self.actDefaults = QtGui.QAction(MainWindow)
        self.actDefaults.setObjectName(_fromUtf8("actDefaults"))
        self.menuFile.addAction(self.actLogin)
        self.menuFile.addAction(self.actLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actQuit)
        self.menuPreferences.addAction(self.actConnection)
        self.menuPreferences.addAction(self.actDefaults)
        self.menuHelp.addAction(self.actAbout)
        self.menuHelp.addAction(self.actAboutQt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.lblFileName.setText(_translate("MainWindow", "Имя файла", None))
        self.btnSelectFileName.setText(_translate("MainWindow", "...", None))
        self.btnImport.setText(_translate("MainWindow", "Импорт", None))
        self.lblExport.setText(_translate("MainWindow", "Имя файла", None))
        self.btnSelectExportFileName.setText(_translate("MainWindow", "...", None))
        self.btnExport.setText(_translate("MainWindow", "Экспорт", None))
        self.menuFile.setTitle(_translate("MainWindow", "Сессия", None))
        self.menuPreferences.setTitle(_translate("MainWindow", "Настройки", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Помощь", None))
        self.actLogin.setText(_translate("MainWindow", "Подключиться к базе данных", None))
        self.actLogout.setText(_translate("MainWindow", "Отключиться от базы данных", None))
        self.actQuit.setText(_translate("MainWindow", "Закрыть программу", None))
        self.actQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actConnection.setText(_translate("MainWindow", "База данных", None))
        self.actDecor.setText(_translate("MainWindow", "Внешний вид", None))
        self.actAbout.setText(_translate("MainWindow", "О программе", None))
        self.actAboutQt.setText(_translate("MainWindow", "О Qt", None))
        self.actDefaults.setText(_translate("MainWindow", "Умолчания", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

