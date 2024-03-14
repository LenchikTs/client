# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportFeedDataCsv_Wizard_2.ui'
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

class Ui_ExportFeedDataCsv_Wizard_2(object):
    def setupUi(self, ExportFeedDataCsv_Wizard_2):
        ExportFeedDataCsv_Wizard_2.setObjectName(_fromUtf8("ExportFeedDataCsv_Wizard_2"))
        ExportFeedDataCsv_Wizard_2.resize(400, 271)
        self.gridlayout = QtGui.QGridLayout(ExportFeedDataCsv_Wizard_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 5, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ExportFeedDataCsv_Wizard_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ExportFeedDataCsv_Wizard_2)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ExportFeedDataCsv_Wizard_2)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.btnExport = QtGui.QPushButton(ExportFeedDataCsv_Wizard_2)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.hboxlayout1.addWidget(self.btnExport)
        self.gridlayout.addLayout(self.hboxlayout1, 6, 0, 1, 1)
        self.progressBar = CProgressBar(ExportFeedDataCsv_Wizard_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 3, 0, 1, 1)
        self.stat = QtGui.QLabel(ExportFeedDataCsv_Wizard_2)
        self.stat.setText(_fromUtf8(""))
        self.stat.setObjectName(_fromUtf8("stat"))
        self.gridlayout.addWidget(self.stat, 4, 0, 1, 1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.gridlayout.addLayout(self.hboxlayout2, 1, 0, 1, 1)

        self.retranslateUi(ExportFeedDataCsv_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ExportFeedDataCsv_Wizard_2)
        ExportFeedDataCsv_Wizard_2.setTabOrder(self.edtFileName, self.btnSelectFile)
        ExportFeedDataCsv_Wizard_2.setTabOrder(self.btnSelectFile, self.btnExport)

    def retranslateUi(self, ExportFeedDataCsv_Wizard_2):
        ExportFeedDataCsv_Wizard_2.setWindowTitle(_translate("ExportFeedDataCsv_Wizard_2", "Экспорт данных о питании", None))
        self.label.setText(_translate("ExportFeedDataCsv_Wizard_2", "Экспортировать в", None))
        self.btnSelectFile.setText(_translate("ExportFeedDataCsv_Wizard_2", "...", None))
        self.btnExport.setText(_translate("ExportFeedDataCsv_Wizard_2", "Начать экспорт", None))

from library.ProgressBar import CProgressBar
