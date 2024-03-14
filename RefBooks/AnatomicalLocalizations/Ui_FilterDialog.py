# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\RefBooks\AnatomicalLocalizations\FilterDialog.ui'
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

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName(_fromUtf8("FilterDialog"))
        FilterDialog.resize(598, 236)
        self.gridLayout = QtGui.QGridLayout(FilterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtCode = QtGui.QLineEdit(FilterDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(FilterDialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(FilterDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.cmbGroup = CRBComboBox(FilterDialog)
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.gridLayout.addWidget(self.cmbGroup, 2, 1, 1, 1)
        self.lblGroup = QtGui.QLabel(FilterDialog)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.gridLayout.addWidget(self.lblGroup, 2, 0, 1, 1)
        self.lblCode = QtGui.QLabel(FilterDialog)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.tableView = CTableView(FilterDialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnReset = QtGui.QPushButton(FilterDialog)
        self.btnReset.setObjectName(_fromUtf8("btnReset"))
        self.horizontalLayout.addWidget(self.btnReset)
        self.btnApply = QtGui.QPushButton(FilterDialog)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.horizontalLayout.addWidget(self.btnApply)
        self.btnCancel = QtGui.QPushButton(FilterDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        self.lblName.setText(_translate("FilterDialog", "Наименование", None))
        self.lblGroup.setText(_translate("FilterDialog", "Группа", None))
        self.lblCode.setText(_translate("FilterDialog", "Код", None))
        self.btnReset.setText(_translate("FilterDialog", "Сбросить", None))
        self.btnApply.setText(_translate("FilterDialog", "Применить", None))
        self.btnCancel.setText(_translate("FilterDialog", "Отмена", None))

from library.TableView import CTableView
from library.crbcombobox import CRBComboBox
