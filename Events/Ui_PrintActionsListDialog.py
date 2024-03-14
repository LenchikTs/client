# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\PrintActionsListDialog.ui'
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

class Ui_PrintActionsListDialog(object):
    def setupUi(self, PrintActionsListDialog):
        PrintActionsListDialog.setObjectName(_fromUtf8("PrintActionsListDialog"))
        PrintActionsListDialog.setWindowModality(QtCore.Qt.WindowModal)
        PrintActionsListDialog.resize(726, 513)
        self.gridLayout = QtGui.QGridLayout(PrintActionsListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(PrintActionsListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.btnSelectStatus = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectStatus.setObjectName(_fromUtf8("btnSelectStatus"))
        self.gridLayout.addWidget(self.btnSelectStatus, 2, 2, 1, 1)
        self.btnSelectAll = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.gridLayout.addWidget(self.btnSelectAll, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PrintActionsListDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.btnSelectDiagnostic = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectDiagnostic.setObjectName(_fromUtf8("btnSelectDiagnostic"))
        self.gridLayout.addWidget(self.btnSelectDiagnostic, 2, 3, 1, 1)
        self.btnSelectCure = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectCure.setObjectName(_fromUtf8("btnSelectCure"))
        self.gridLayout.addWidget(self.btnSelectCure, 2, 4, 1, 1)
        self.btnSelectMisc = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectMisc.setObjectName(_fromUtf8("btnSelectMisc"))
        self.gridLayout.addWidget(self.btnSelectMisc, 2, 5, 1, 1)
        self.btnSelectNone = QtGui.QPushButton(PrintActionsListDialog)
        self.btnSelectNone.setObjectName(_fromUtf8("btnSelectNone"))
        self.gridLayout.addWidget(self.btnSelectNone, 2, 6, 1, 1)
        self.rbSortByBegDate = QtGui.QRadioButton(PrintActionsListDialog)
        self.rbSortByBegDate.setChecked(True)
        self.rbSortByBegDate.setObjectName(_fromUtf8("rbSortByBegDate"))
        self.gridLayout.addWidget(self.rbSortByBegDate, 1, 1, 1, 2)
        self.tblActions = QtGui.QTableView(PrintActionsListDialog)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout.addWidget(self.tblActions, 0, 0, 1, 7)
        self.buttonBox = QtGui.QDialogButtonBox(PrintActionsListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 7)
        self.rbSortByEndDate = QtGui.QRadioButton(PrintActionsListDialog)
        self.rbSortByEndDate.setObjectName(_fromUtf8("rbSortByEndDate"))
        self.gridLayout.addWidget(self.rbSortByEndDate, 1, 3, 1, 2)
        self.chbAddPageBreaks = QtGui.QCheckBox(PrintActionsListDialog)
        self.chbAddPageBreaks.setObjectName(_fromUtf8("chbAddPageBreaks"))
        self.gridLayout.addWidget(self.chbAddPageBreaks, 1, 5, 1, 2)

        self.retranslateUi(PrintActionsListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrintActionsListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrintActionsListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrintActionsListDialog)

    def retranslateUi(self, PrintActionsListDialog):
        PrintActionsListDialog.setWindowTitle(_translate("PrintActionsListDialog", "Печать списка действий по отдельным шаблонам", None))
        self.label.setText(_translate("PrintActionsListDialog", "Порядок печати:", None))
        self.btnSelectStatus.setText(_translate("PrintActionsListDialog", "Статус", None))
        self.btnSelectAll.setText(_translate("PrintActionsListDialog", "Все", None))
        self.label_2.setText(_translate("PrintActionsListDialog", "Выбрать:", None))
        self.btnSelectDiagnostic.setText(_translate("PrintActionsListDialog", "Диагностика", None))
        self.btnSelectCure.setText(_translate("PrintActionsListDialog", "Лечение", None))
        self.btnSelectMisc.setText(_translate("PrintActionsListDialog", "Мероприятия", None))
        self.btnSelectNone.setText(_translate("PrintActionsListDialog", "Очистить все", None))
        self.rbSortByBegDate.setText(_translate("PrintActionsListDialog", "По дате начала", None))
        self.rbSortByEndDate.setText(_translate("PrintActionsListDialog", "По дате окончания", None))
        self.chbAddPageBreaks.setText(_translate("PrintActionsListDialog", "Каждый шаблон с новой страницы", None))

