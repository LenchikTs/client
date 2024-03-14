# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportINFISOMSPage1.ui'
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

class Ui_ExportINFISOMSPage1(object):
    def setupUi(self, ExportINFISOMSPage1):
        ExportINFISOMSPage1.setObjectName(_fromUtf8("ExportINFISOMSPage1"))
        ExportINFISOMSPage1.resize(556, 301)
        self.gridLayout = QtGui.QGridLayout(ExportINFISOMSPage1)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnExport = QtGui.QPushButton(ExportINFISOMSPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridLayout.addWidget(self.btnExport, 5, 3, 1, 1)
        self.btnCancel = QtGui.QPushButton(ExportINFISOMSPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout.addWidget(self.btnCancel, 5, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.progressBar = CProgressBar(ExportINFISOMSPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 5)
        self.cmbRepresentativeOutRule = QtGui.QComboBox(ExportINFISOMSPage1)
        self.cmbRepresentativeOutRule.setObjectName(_fromUtf8("cmbRepresentativeOutRule"))
        self.cmbRepresentativeOutRule.addItem(_fromUtf8(""))
        self.cmbRepresentativeOutRule.addItem(_fromUtf8(""))
        self.cmbRepresentativeOutRule.addItem(_fromUtf8(""))
        self.cmbRepresentativeOutRule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbRepresentativeOutRule, 3, 1, 1, 4)
        self.lblRepresentativeOutRule = QtGui.QLabel(ExportINFISOMSPage1)
        self.lblRepresentativeOutRule.setObjectName(_fromUtf8("lblRepresentativeOutRule"))
        self.gridLayout.addWidget(self.lblRepresentativeOutRule, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 3)
        self.cbCardflag = QtGui.QCheckBox(ExportINFISOMSPage1)
        self.cbCardflag.setObjectName(_fromUtf8("cbCardflag"))
        self.gridLayout.addWidget(self.cbCardflag, 4, 0, 1, 1)
        self.edtCardflag = QtGui.QLineEdit(ExportINFISOMSPage1)
        self.edtCardflag.setEnabled(False)
        self.edtCardflag.setObjectName(_fromUtf8("edtCardflag"))
        self.gridLayout.addWidget(self.edtCardflag, 4, 1, 1, 4)

        self.retranslateUi(ExportINFISOMSPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportINFISOMSPage1)

    def retranslateUi(self, ExportINFISOMSPage1):
        ExportINFISOMSPage1.setWindowTitle(_translate("ExportINFISOMSPage1", "Form", None))
        self.btnExport.setText(_translate("ExportINFISOMSPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportINFISOMSPage1", "прервать", None))
        self.cmbRepresentativeOutRule.setItemText(0, _translate("ExportINFISOMSPage1", "выгружать во всех случаях", None))
        self.cmbRepresentativeOutRule.setItemText(1, _translate("ExportINFISOMSPage1", "выгружать для иногородних", None))
        self.cmbRepresentativeOutRule.setItemText(2, _translate("ExportINFISOMSPage1", "выгружать для жителей СПб", None))
        self.cmbRepresentativeOutRule.setItemText(3, _translate("ExportINFISOMSPage1", "не выгружать", None))
        self.lblRepresentativeOutRule.setText(_translate("ExportINFISOMSPage1", "Данные представителя ", None))
        self.cbCardflag.setText(_translate("ExportINFISOMSPage1", "Указать cardflag", None))
        self.edtCardflag.setInputMask(_translate("ExportINFISOMSPage1", "9999; ", None))
        self.edtCardflag.setText(_translate("ExportINFISOMSPage1", "4096", None))

from library.ProgressBar import CProgressBar
