# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportHL7v2_5_Wizard_2.ui'
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

class Ui_ExportHL7v2_5_Wizard_2(object):
    def setupUi(self, ExportHL7v2_5_Wizard_2):
        ExportHL7v2_5_Wizard_2.setObjectName(_fromUtf8("ExportHL7v2_5_Wizard_2"))
        ExportHL7v2_5_Wizard_2.resize(400, 271)
        self.gridlayout = QtGui.QGridLayout(ExportHL7v2_5_Wizard_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ExportHL7v2_5_Wizard_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtDirName = QtGui.QLineEdit(ExportHL7v2_5_Wizard_2)
        self.edtDirName.setObjectName(_fromUtf8("edtDirName"))
        self.hboxlayout.addWidget(self.edtDirName)
        self.btnSelectDir = QtGui.QToolButton(ExportHL7v2_5_Wizard_2)
        self.btnSelectDir.setObjectName(_fromUtf8("btnSelectDir"))
        self.hboxlayout.addWidget(self.btnSelectDir)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.gridlayout.addLayout(self.hboxlayout1, 2, 0, 1, 1)
        self.progressBar = CProgressBar(ExportHL7v2_5_Wizard_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.stat = QtGui.QLabel(ExportHL7v2_5_Wizard_2)
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
        self.btnAbort = QtGui.QPushButton(ExportHL7v2_5_Wizard_2)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout2.addWidget(self.btnAbort)
        self.btnExport = QtGui.QPushButton(ExportHL7v2_5_Wizard_2)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.hboxlayout2.addWidget(self.btnExport)
        self.gridlayout.addLayout(self.hboxlayout2, 7, 0, 1, 1)
        self.checkRAR = QtGui.QCheckBox(ExportHL7v2_5_Wizard_2)
        self.checkRAR.setCheckable(True)
        self.checkRAR.setObjectName(_fromUtf8("checkRAR"))
        self.gridlayout.addWidget(self.checkRAR, 1, 0, 1, 1)

        self.retranslateUi(ExportHL7v2_5_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ExportHL7v2_5_Wizard_2)

    def retranslateUi(self, ExportHL7v2_5_Wizard_2):
        ExportHL7v2_5_Wizard_2.setWindowTitle(_translate("ExportHL7v2_5_Wizard_2", "Экспорт данных о сотрудниках", None))
        self.label.setText(_translate("ExportHL7v2_5_Wizard_2", "Экспортировать в", None))
        self.btnSelectDir.setText(_translate("ExportHL7v2_5_Wizard_2", "...", None))
        self.btnAbort.setText(_translate("ExportHL7v2_5_Wizard_2", "Прервать", None))
        self.btnExport.setText(_translate("ExportHL7v2_5_Wizard_2", "Начать экспорт", None))
        self.checkRAR.setText(_translate("ExportHL7v2_5_Wizard_2", "Архивировать rar", None))

from library.ProgressBar import CProgressBar
