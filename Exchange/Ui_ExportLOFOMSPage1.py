# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportLOFOMSPage1.ui'
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

class Ui_ExportLOFOMSPage1(object):
    def setupUi(self, ExportLOFOMSPage1):
        ExportLOFOMSPage1.setObjectName(_fromUtf8("ExportLOFOMSPage1"))
        ExportLOFOMSPage1.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(ExportLOFOMSPage1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblFluorography = QtGui.QLabel(ExportLOFOMSPage1)
        self.lblFluorography.setObjectName(_fromUtf8("lblFluorography"))
        self.gridlayout.addWidget(self.lblFluorography, 0, 0, 1, 1)
        self.cmbActionTypeFluorography = CActionTypeComboBox(ExportLOFOMSPage1)
        self.cmbActionTypeFluorography.setObjectName(_fromUtf8("cmbActionTypeFluorography"))
        self.gridlayout.addWidget(self.cmbActionTypeFluorography, 1, 0, 1, 2)
        self.lblCytological = QtGui.QLabel(ExportLOFOMSPage1)
        self.lblCytological.setObjectName(_fromUtf8("lblCytological"))
        self.gridlayout.addWidget(self.lblCytological, 2, 0, 1, 1)
        self.cmbActionTypeCytological = CActionTypeComboBox(ExportLOFOMSPage1)
        self.cmbActionTypeCytological.setObjectName(_fromUtf8("cmbActionTypeCytological"))
        self.gridlayout.addWidget(self.cmbActionTypeCytological, 3, 0, 1, 2)
        self.gbAccountParams = QtGui.QGroupBox(ExportLOFOMSPage1)
        self.gbAccountParams.setObjectName(_fromUtf8("gbAccountParams"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbAccountParams)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkRFAccount = QtGui.QCheckBox(self.gbAccountParams)
        self.chkRFAccount.setObjectName(_fromUtf8("chkRFAccount"))
        self.verticalLayout.addWidget(self.chkRFAccount)
        self.lblAccountType = QtGui.QLabel(self.gbAccountParams)
        self.lblAccountType.setObjectName(_fromUtf8("lblAccountType"))
        self.verticalLayout.addWidget(self.lblAccountType)
        self.cmbAccountType = QtGui.QComboBox(self.gbAccountParams)
        self.cmbAccountType.setObjectName(_fromUtf8("cmbAccountType"))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.cmbAccountType)
        self.gridlayout.addWidget(self.gbAccountParams, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 5, 0, 1, 1)

        self.retranslateUi(ExportLOFOMSPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportLOFOMSPage1)

    def retranslateUi(self, ExportLOFOMSPage1):
        ExportLOFOMSPage1.setWindowTitle(_translate("ExportLOFOMSPage1", "Form", None))
        self.lblFluorography.setText(_translate("ExportLOFOMSPage1", "Укажите тип действия для анализа \"Флюорография\":", None))
        self.lblCytological.setText(_translate("ExportLOFOMSPage1", "Укажите тип действия для анализа \"Цитологическое исследование\"", None))
        self.gbAccountParams.setTitle(_translate("ExportLOFOMSPage1", "Свойства счета", None))
        self.chkRFAccount.setText(_translate("ExportLOFOMSPage1", "Счет по РФ", None))
        self.lblAccountType.setText(_translate("ExportLOFOMSPage1", "Категория счета:", None))
        self.cmbAccountType.setItemText(0, _translate("ExportLOFOMSPage1", "счет за застрахованных жителей Лен.области", None))
        self.cmbAccountType.setItemText(1, _translate("ExportLOFOMSPage1", "счет за иные категории граждан (условно застрахованные)", None))
        self.cmbAccountType.setItemText(2, _translate("ExportLOFOMSPage1", "счет за жителей других субъектов РФ (кроме СПб)", None))
        self.cmbAccountType.setItemText(3, _translate("ExportLOFOMSPage1", "счет за жителей Лен. обл., работающих на предприятиях РФ", None))
        self.cmbAccountType.setItemText(4, _translate("ExportLOFOMSPage1", "счет за застрахованных жителей Лен.обл. по стоматологии", None))
        self.cmbAccountType.setItemText(5, _translate("ExportLOFOMSPage1", "счет за иные категории граждан (условно застрахованные) по стоматологии", None))
        self.cmbAccountType.setItemText(6, _translate("ExportLOFOMSPage1", "счет за жителей других субъектов РФ (кроме СПб) по стоматологии", None))
        self.cmbAccountType.setItemText(7, _translate("ExportLOFOMSPage1", "счет за жителей Лен. обл., работающих на предприятиях РФ по стоматологии", None))

from Events.ActionTypeComboBox import CActionTypeComboBox
