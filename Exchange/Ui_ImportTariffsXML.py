# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ImportTariffsXML.ui'
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

class Ui_ImportTariffsXML(object):
    def setupUi(self, ImportTariffsXML):
        ImportTariffsXML.setObjectName(_fromUtf8("ImportTariffsXML"))
        ImportTariffsXML.resize(485, 414)
        self.gridLayout = QtGui.QGridLayout(ImportTariffsXML)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkOnlyCodes = QtGui.QCheckBox(ImportTariffsXML)
        self.chkOnlyCodes.setObjectName(_fromUtf8("chkOnlyCodes"))
        self.gridLayout.addWidget(self.chkOnlyCodes, 4, 0, 1, 2)
        self.label = QtGui.QLabel(ImportTariffsXML)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.chkFullLog = QtGui.QCheckBox(ImportTariffsXML)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridLayout.addWidget(self.chkFullLog, 1, 0, 1, 2)
        self.chkUpdateTariff = QtGui.QCheckBox(ImportTariffsXML)
        self.chkUpdateTariff.setObjectName(_fromUtf8("chkUpdateTariff"))
        self.gridLayout.addWidget(self.chkUpdateTariff, 2, 0, 1, 2)
        self.lblStatus = QtGui.QLabel(ImportTariffsXML)
        self.lblStatus.setText(_fromUtf8(""))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 7, 0, 1, 3)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(ImportTariffsXML)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnAbort = QtGui.QPushButton(ImportTariffsXML)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout.addWidget(self.btnAbort)
        self.btnClose = QtGui.QPushButton(ImportTariffsXML)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout, 8, 0, 1, 3)
        self.progressBar = CProgressBar(ImportTariffsXML)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 3)
        self.logBrowser = QtGui.QTextBrowser(ImportTariffsXML)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 6, 0, 1, 3)
        self.edtFileName = QtGui.QLineEdit(ImportTariffsXML)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.gridLayout.addWidget(self.edtFileName, 0, 1, 1, 1)
        self.btnSelectFile = QtGui.QToolButton(ImportTariffsXML)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectFile.sizePolicy().hasHeightForWidth())
        self.btnSelectFile.setSizePolicy(sizePolicy)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.gridLayout.addWidget(self.btnSelectFile, 0, 2, 1, 1)

        self.retranslateUi(ImportTariffsXML)
        QtCore.QMetaObject.connectSlotsByName(ImportTariffsXML)
        ImportTariffsXML.setTabOrder(self.edtFileName, self.btnSelectFile)
        ImportTariffsXML.setTabOrder(self.btnSelectFile, self.chkFullLog)
        ImportTariffsXML.setTabOrder(self.chkFullLog, self.chkUpdateTariff)
        ImportTariffsXML.setTabOrder(self.chkUpdateTariff, self.chkOnlyCodes)
        ImportTariffsXML.setTabOrder(self.chkOnlyCodes, self.logBrowser)
        ImportTariffsXML.setTabOrder(self.logBrowser, self.btnImport)
        ImportTariffsXML.setTabOrder(self.btnImport, self.btnAbort)
        ImportTariffsXML.setTabOrder(self.btnAbort, self.btnClose)

    def retranslateUi(self, ImportTariffsXML):
        ImportTariffsXML.setWindowTitle(_translate("ImportTariffsXML", "Импорт тарифов для договора", None))
        self.chkOnlyCodes.setToolTip(_translate("ImportTariffsXML", "Не учитывать различия в наименовании", None))
        self.chkOnlyCodes.setText(_translate("ImportTariffsXML", "Учитывать только код услуги", None))
        self.label.setText(_translate("ImportTariffsXML", "Загрузить из", None))
        self.chkFullLog.setText(_translate("ImportTariffsXML", "Подробный отчет", None))
        self.chkUpdateTariff.setText(_translate("ImportTariffsXML", "Обновлять совпадающие тарифы", None))
        self.btnImport.setText(_translate("ImportTariffsXML", "Начать импорт", None))
        self.btnAbort.setText(_translate("ImportTariffsXML", "Прервать", None))
        self.btnClose.setText(_translate("ImportTariffsXML", "Закрыть", None))
        self.btnSelectFile.setText(_translate("ImportTariffsXML", "...", None))

from library.ProgressBar import CProgressBar
