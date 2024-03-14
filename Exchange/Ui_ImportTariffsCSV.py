# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportTariffsCSV.ui'
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

class Ui_ImportTariffsCSV(object):
    def setupUi(self, ImportTariffsCSV):
        ImportTariffsCSV.setObjectName(_fromUtf8("ImportTariffsCSV"))
        ImportTariffsCSV.resize(509, 523)
        self.verticalLayout = QtGui.QVBoxLayout(ImportTariffsCSV)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ImportTariffsCSV)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ImportTariffsCSV)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportTariffsCSV)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.progressBar = CProgressBar(ImportTariffsCSV)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.chkFullLog = QtGui.QCheckBox(ImportTariffsCSV)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.verticalLayout.addWidget(self.chkFullLog)
        self.chkUpdateTariff = QtGui.QCheckBox(ImportTariffsCSV)
        self.chkUpdateTariff.setObjectName(_fromUtf8("chkUpdateTariff"))
        self.verticalLayout.addWidget(self.chkUpdateTariff)
        self.chkOnlyCodes = QtGui.QCheckBox(ImportTariffsCSV)
        self.chkOnlyCodes.setObjectName(_fromUtf8("chkOnlyCodes"))
        self.verticalLayout.addWidget(self.chkOnlyCodes)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chkAddServicesAndAT = QtGui.QCheckBox(ImportTariffsCSV)
        self.chkAddServicesAndAT.setObjectName(_fromUtf8("chkAddServicesAndAT"))
        self.horizontalLayout.addWidget(self.chkAddServicesAndAT)
        self.btnSettings = QtGui.QPushButton(ImportTariffsCSV)
        self.btnSettings.setEnabled(False)
        self.btnSettings.setObjectName(_fromUtf8("btnSettings"))
        self.horizontalLayout.addWidget(self.btnSettings)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.logBrowser = QtGui.QTextBrowser(ImportTariffsCSV)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.verticalLayout.addWidget(self.logBrowser)
        self.lblStatus = QtGui.QLabel(ImportTariffsCSV)
        self.lblStatus.setText(_fromUtf8(""))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.verticalLayout.addWidget(self.lblStatus)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(4)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.btnImport = QtGui.QPushButton(ImportTariffsCSV)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout1.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.btnAbort = QtGui.QPushButton(ImportTariffsCSV)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout1.addWidget(self.btnAbort)
        self.btnClose = QtGui.QPushButton(ImportTariffsCSV)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout1.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.hboxlayout1)

        self.retranslateUi(ImportTariffsCSV)
        QtCore.QObject.connect(self.chkAddServicesAndAT, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.btnSettings.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ImportTariffsCSV)
        ImportTariffsCSV.setTabOrder(self.edtFileName, self.btnSelectFile)
        ImportTariffsCSV.setTabOrder(self.btnSelectFile, self.chkFullLog)
        ImportTariffsCSV.setTabOrder(self.chkFullLog, self.chkUpdateTariff)
        ImportTariffsCSV.setTabOrder(self.chkUpdateTariff, self.logBrowser)
        ImportTariffsCSV.setTabOrder(self.logBrowser, self.btnImport)
        ImportTariffsCSV.setTabOrder(self.btnImport, self.btnAbort)
        ImportTariffsCSV.setTabOrder(self.btnAbort, self.btnClose)

    def retranslateUi(self, ImportTariffsCSV):
        ImportTariffsCSV.setWindowTitle(_translate("ImportTariffsCSV", "Импорт тарифов для договора", None))
        self.label.setText(_translate("ImportTariffsCSV", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportTariffsCSV", "...", None))
        self.chkFullLog.setText(_translate("ImportTariffsCSV", "Подробный отчет", None))
        self.chkUpdateTariff.setText(_translate("ImportTariffsCSV", "Обновлять совпадающие тарифы", None))
        self.chkOnlyCodes.setToolTip(_translate("ImportTariffsCSV", "Не учитывать различия в наименовании", None))
        self.chkOnlyCodes.setText(_translate("ImportTariffsCSV", "Учитывать только код услуги", None))
        self.chkAddServicesAndAT.setText(_translate("ImportTariffsCSV", "Добавлять отсутствующие сервисы и типы действий", None))
        self.btnSettings.setText(_translate("ImportTariffsCSV", "Настройка умолчаний", None))
        self.btnImport.setText(_translate("ImportTariffsCSV", "Начать импорт", None))
        self.btnAbort.setText(_translate("ImportTariffsCSV", "Прервать", None))
        self.btnClose.setText(_translate("ImportTariffsCSV", "Закрыть", None))

from library.ProgressBar import CProgressBar
