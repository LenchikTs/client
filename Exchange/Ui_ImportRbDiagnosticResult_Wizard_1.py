# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportRbDiagnosticResult_Wizard_1.ui'
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

class Ui_ImportRbDiagnosticResult_Wizard_1(object):
    def setupUi(self, ImportRbDiagnosticResult_Wizard_1):
        ImportRbDiagnosticResult_Wizard_1.setObjectName(_fromUtf8("ImportRbDiagnosticResult_Wizard_1"))
        ImportRbDiagnosticResult_Wizard_1.resize(475, 429)
        self.gridlayout = QtGui.QGridLayout(ImportRbDiagnosticResult_Wizard_1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ImportRbDiagnosticResult_Wizard_1)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ImportRbDiagnosticResult_Wizard_1)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportRbDiagnosticResult_Wizard_1)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.progressBar = CProgressBar(ImportRbDiagnosticResult_Wizard_1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(ImportRbDiagnosticResult_Wizard_1)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridlayout.addWidget(self.statusLabel, 5, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ImportRbDiagnosticResult_Wizard_1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 4, 0, 1, 1)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(ImportRbDiagnosticResult_Wizard_1)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.rbAskUser = QtGui.QRadioButton(self.groupBox)
        self.rbAskUser.setEnabled(True)
        self.rbAskUser.setChecked(True)
        self.rbAskUser.setObjectName(_fromUtf8("rbAskUser"))
        self.vboxlayout1.addWidget(self.rbAskUser)
        self.rbUpdate = QtGui.QRadioButton(self.groupBox)
        self.rbUpdate.setChecked(False)
        self.rbUpdate.setObjectName(_fromUtf8("rbUpdate"))
        self.vboxlayout1.addWidget(self.rbUpdate)
        self.rbSkip = QtGui.QRadioButton(self.groupBox)
        self.rbSkip.setObjectName(_fromUtf8("rbSkip"))
        self.vboxlayout1.addWidget(self.rbSkip)
        self.vboxlayout.addWidget(self.groupBox)
        self.gridlayout.addLayout(self.vboxlayout, 1, 0, 1, 1)
        self.chkFullLog = QtGui.QCheckBox(ImportRbDiagnosticResult_Wizard_1)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridlayout.addWidget(self.chkFullLog, 3, 0, 1, 1)

        self.retranslateUi(ImportRbDiagnosticResult_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ImportRbDiagnosticResult_Wizard_1)

    def retranslateUi(self, ImportRbDiagnosticResult_Wizard_1):
        ImportRbDiagnosticResult_Wizard_1.setWindowTitle(_translate("ImportRbDiagnosticResult_Wizard_1", "Импорт cправочника \"Результаты Осмотра\" ", None))
        self.label.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "...", None))
        self.groupBox.setTitle(_translate("ImportRbDiagnosticResult_Wizard_1", "Совпадающие записи", None))
        self.rbAskUser.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "Спрашивать действие у пользователя", None))
        self.rbUpdate.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "Обновлять", None))
        self.rbSkip.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "Пропускать", None))
        self.chkFullLog.setText(_translate("ImportRbDiagnosticResult_Wizard_1", "Подробный отчет", None))

from library.ProgressBar import CProgressBar
