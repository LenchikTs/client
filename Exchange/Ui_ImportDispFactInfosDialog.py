# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportDispFactInfosDialog.ui'
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

class Ui_ImportDispFactInfosDialog(object):
    def setupUi(self, ImportDispFactInfosDialog):
        ImportDispFactInfosDialog.setObjectName(_fromUtf8("ImportDispFactInfosDialog"))
        ImportDispFactInfosDialog.resize(254, 71)
        self.verticalLayout = QtGui.QVBoxLayout(ImportDispFactInfosDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(ImportDispFactInfosDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.dateFrom = QtGui.QDateEdit(ImportDispFactInfosDialog)
        self.dateFrom.setObjectName(_fromUtf8("dateFrom"))
        self.horizontalLayout.addWidget(self.dateFrom)
        self.label_3 = QtGui.QLabel(ImportDispFactInfosDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.dateTo = QtGui.QDateEdit(ImportDispFactInfosDialog)
        self.dateTo.setObjectName(_fromUtf8("dateTo"))
        self.horizontalLayout.addWidget(self.dateTo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnImport = QtGui.QPushButton(ImportDispFactInfosDialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.horizontalLayout_3.addWidget(self.btnImport)
        self.btnCancel = QtGui.QPushButton(ImportDispFactInfosDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(ImportDispFactInfosDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportDispFactInfosDialog)

    def retranslateUi(self, ImportDispFactInfosDialog):
        ImportDispFactInfosDialog.setWindowTitle(_translate("ImportDispFactInfosDialog", "Параметры", None))
        self.label_2.setText(_translate("ImportDispFactInfosDialog", "Дата: с", None))
        self.label_3.setText(_translate("ImportDispFactInfosDialog", "по", None))
        self.btnImport.setText(_translate("ImportDispFactInfosDialog", "Импорт", None))
        self.btnCancel.setText(_translate("ImportDispFactInfosDialog", "Закрыть", None))

