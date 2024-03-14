# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Exchange\ExportDispContactsDialog.ui'
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

class Ui_ExportDispContactsDialog(object):
    def setupUi(self, ExportDispContactsDialog):
        ExportDispContactsDialog.setObjectName(_fromUtf8("ExportDispContactsDialog"))
        ExportDispContactsDialog.resize(838, 600)
        self.verticalLayout = QtGui.QVBoxLayout(ExportDispContactsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(ExportDispContactsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cmbOrgStructure = CDbComboBox(ExportDispContactsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.horizontalLayout.addWidget(self.cmbOrgStructure)
        self.btnExport = QtGui.QPushButton(ExportDispContactsDialog)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout.addWidget(self.btnExport)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblContacts = CInDocTableView(ExportDispContactsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tblContacts.sizePolicy().hasHeightForWidth())
        self.tblContacts.setSizePolicy(sizePolicy)
        self.tblContacts.setObjectName(_fromUtf8("tblContacts"))
        self.verticalLayout.addWidget(self.tblContacts)
        self.label = QtGui.QLabel(ExportDispContactsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tblContactErrors = CTableView(ExportDispContactsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tblContactErrors.sizePolicy().hasHeightForWidth())
        self.tblContactErrors.setSizePolicy(sizePolicy)
        self.tblContactErrors.setObjectName(_fromUtf8("tblContactErrors"))
        self.verticalLayout.addWidget(self.tblContactErrors)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnOK = QtGui.QPushButton(ExportDispContactsDialog)
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.horizontalLayout_2.addWidget(self.btnOK)
        self.btnCancel = QtGui.QPushButton(ExportDispContactsDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.btnApply = QtGui.QPushButton(ExportDispContactsDialog)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.horizontalLayout_2.addWidget(self.btnApply)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ExportDispContactsDialog)
        QtCore.QMetaObject.connectSlotsByName(ExportDispContactsDialog)

    def retranslateUi(self, ExportDispContactsDialog):
        ExportDispContactsDialog.setWindowTitle(_translate("ExportDispContactsDialog", "Список контактных телефонов", None))
        self.label_2.setText(_translate("ExportDispContactsDialog", "Подразделение:", None))
        self.btnExport.setText(_translate("ExportDispContactsDialog", "Отправить", None))
        self.label.setText(_translate("ExportDispContactsDialog", "Ошибки при экспорте:", None))
        self.btnOK.setText(_translate("ExportDispContactsDialog", "OK", None))
        self.btnCancel.setText(_translate("ExportDispContactsDialog", "Отмена", None))
        self.btnApply.setText(_translate("ExportDispContactsDialog", "Применить", None))

from library.DbComboBox import CDbComboBox
from library.InDocTable import CInDocTableView
from library.TableView import CTableView
