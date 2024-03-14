# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportDispFactInvcsDialog.ui'
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

class Ui_ImportDispFactInvcsDialog(object):
    def setupUi(self, ImportDispFactInvcsDialog):
        ImportDispFactInvcsDialog.setObjectName(_fromUtf8("ImportDispFactInvcsDialog"))
        ImportDispFactInvcsDialog.resize(198, 99)
        self.verticalLayout = QtGui.QVBoxLayout(ImportDispFactInvcsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(ImportDispFactInvcsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.sbYear = QtGui.QSpinBox(ImportDispFactInvcsDialog)
        self.sbYear.setMinimum(2017)
        self.sbYear.setMaximum(9999)
        self.sbYear.setObjectName(_fromUtf8("sbYear"))
        self.horizontalLayout_2.addWidget(self.sbYear)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(ImportDispFactInvcsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cmbMonth = QtGui.QComboBox(ImportDispFactInvcsDialog)
        self.cmbMonth.setObjectName(_fromUtf8("cmbMonth"))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.cmbMonth.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.cmbMonth)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnImport = QtGui.QPushButton(ImportDispFactInvcsDialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.horizontalLayout_3.addWidget(self.btnImport)
        self.btnCancel = QtGui.QPushButton(ImportDispFactInvcsDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(ImportDispFactInvcsDialog)
        self.cmbMonth.setCurrentIndex(11)
        QtCore.QMetaObject.connectSlotsByName(ImportDispFactInvcsDialog)

    def retranslateUi(self, ImportDispFactInvcsDialog):
        ImportDispFactInvcsDialog.setWindowTitle(_translate("ImportDispFactInvcsDialog", "Параметры", None))
        self.label.setText(_translate("ImportDispFactInvcsDialog", "Год", None))
        self.label_2.setText(_translate("ImportDispFactInvcsDialog", "Месяц", None))
        self.cmbMonth.setItemText(0, _translate("ImportDispFactInvcsDialog", "январь", None))
        self.cmbMonth.setItemText(1, _translate("ImportDispFactInvcsDialog", "февраль", None))
        self.cmbMonth.setItemText(2, _translate("ImportDispFactInvcsDialog", "март", None))
        self.cmbMonth.setItemText(3, _translate("ImportDispFactInvcsDialog", "апрель", None))
        self.cmbMonth.setItemText(4, _translate("ImportDispFactInvcsDialog", "май", None))
        self.cmbMonth.setItemText(5, _translate("ImportDispFactInvcsDialog", "июнь", None))
        self.cmbMonth.setItemText(6, _translate("ImportDispFactInvcsDialog", "июль", None))
        self.cmbMonth.setItemText(7, _translate("ImportDispFactInvcsDialog", "август", None))
        self.cmbMonth.setItemText(8, _translate("ImportDispFactInvcsDialog", "сентябрь", None))
        self.cmbMonth.setItemText(9, _translate("ImportDispFactInvcsDialog", "октябрь", None))
        self.cmbMonth.setItemText(10, _translate("ImportDispFactInvcsDialog", "ноябрь", None))
        self.cmbMonth.setItemText(11, _translate("ImportDispFactInvcsDialog", "декабрь", None))
        self.btnImport.setText(_translate("ImportDispFactInvcsDialog", "Импорт", None))
        self.btnCancel.setText(_translate("ImportDispFactInvcsDialog", "Закрыть", None))

