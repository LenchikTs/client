# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportRbDiagnosticResult_Wizard_2.ui'
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

class Ui_ExportRbDiagnosticResult_Wizard_2(object):
    def setupUi(self, ExportRbDiagnosticResult_Wizard_2):
        ExportRbDiagnosticResult_Wizard_2.setObjectName(_fromUtf8("ExportRbDiagnosticResult_Wizard_2"))
        ExportRbDiagnosticResult_Wizard_2.resize(400, 271)
        self.gridlayout = QtGui.QGridLayout(ExportRbDiagnosticResult_Wizard_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ExportRbDiagnosticResult_Wizard_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ExportRbDiagnosticResult_Wizard_2)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ExportRbDiagnosticResult_Wizard_2)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.gridlayout.addLayout(self.hboxlayout1, 2, 0, 1, 1)
        self.progressBar = CProgressBar(ExportRbDiagnosticResult_Wizard_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.stat = QtGui.QLabel(ExportRbDiagnosticResult_Wizard_2)
        self.stat.setText(_fromUtf8(""))
        self.stat.setObjectName(_fromUtf8("stat"))
        self.gridlayout.addWidget(self.stat, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 6, 0, 1, 1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)
        self.btnExport = QtGui.QPushButton(ExportRbDiagnosticResult_Wizard_2)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.hboxlayout2.addWidget(self.btnExport)
        self.gridlayout.addLayout(self.hboxlayout2, 7, 0, 1, 1)
        self.checkRAR = QtGui.QCheckBox(ExportRbDiagnosticResult_Wizard_2)
        self.checkRAR.setCheckable(True)
        self.checkRAR.setObjectName(_fromUtf8("checkRAR"))
        self.gridlayout.addWidget(self.checkRAR, 1, 0, 1, 1)

        self.retranslateUi(ExportRbDiagnosticResult_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ExportRbDiagnosticResult_Wizard_2)

    def retranslateUi(self, ExportRbDiagnosticResult_Wizard_2):
        ExportRbDiagnosticResult_Wizard_2.setWindowTitle(_translate("ExportRbDiagnosticResult_Wizard_2", "Экспорт результатов осмотра", None))
        self.label.setText(_translate("ExportRbDiagnosticResult_Wizard_2", "Экспортировать в", None))
        self.btnSelectFile.setText(_translate("ExportRbDiagnosticResult_Wizard_2", "...", None))
        self.btnExport.setText(_translate("ExportRbDiagnosticResult_Wizard_2", "Начать экспорт", None))
        self.checkRAR.setText(_translate("ExportRbDiagnosticResult_Wizard_2", "Архивировать rar", None))

from library.ProgressBar import CProgressBar
