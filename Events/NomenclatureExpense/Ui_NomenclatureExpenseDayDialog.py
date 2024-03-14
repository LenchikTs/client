# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\NomenclatureExpense\NomenclatureExpenseDayDialog.ui'
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

class Ui_NomenclatureExpenseDayDialog(object):
    def setupUi(self, NomenclatureExpenseDayDialog):
        NomenclatureExpenseDayDialog.setObjectName(_fromUtf8("NomenclatureExpenseDayDialog"))
        NomenclatureExpenseDayDialog.resize(473, 300)
        self.gridLayout = QtGui.QGridLayout(NomenclatureExpenseDayDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDayStatistics = QtGui.QLabel(NomenclatureExpenseDayDialog)
        self.lblDayStatistics.setObjectName(_fromUtf8("lblDayStatistics"))
        self.gridLayout.addWidget(self.lblDayStatistics, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NomenclatureExpenseDayDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.tblNomenlcatureExpense = CInDocTableView(NomenclatureExpenseDayDialog)
        self.tblNomenlcatureExpense.setObjectName(_fromUtf8("tblNomenlcatureExpense"))
        self.gridLayout.addWidget(self.tblNomenlcatureExpense, 0, 0, 1, 2)
        self.chkApplyChangesCourseNextDays = QtGui.QCheckBox(NomenclatureExpenseDayDialog)
        self.chkApplyChangesCourseNextDays.setObjectName(_fromUtf8("chkApplyChangesCourseNextDays"))
        self.gridLayout.addWidget(self.chkApplyChangesCourseNextDays, 1, 0, 1, 2)

        self.retranslateUi(NomenclatureExpenseDayDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NomenclatureExpenseDayDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NomenclatureExpenseDayDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NomenclatureExpenseDayDialog)
        NomenclatureExpenseDayDialog.setTabOrder(self.tblNomenlcatureExpense, self.chkApplyChangesCourseNextDays)
        NomenclatureExpenseDayDialog.setTabOrder(self.chkApplyChangesCourseNextDays, self.buttonBox)

    def retranslateUi(self, NomenclatureExpenseDayDialog):
        NomenclatureExpenseDayDialog.setWindowTitle(_translate("NomenclatureExpenseDayDialog", "Dialog", None))
        self.lblDayStatistics.setText(_translate("NomenclatureExpenseDayDialog", "Назначено: 0. Выполнено: 0. Осталось: 0.", None))
        self.chkApplyChangesCourseNextDays.setText(_translate("NomenclatureExpenseDayDialog", "Применить изменения к следующим дням курса", None))

from library.InDocTable import CInDocTableView
