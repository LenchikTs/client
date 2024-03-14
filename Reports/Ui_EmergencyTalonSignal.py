# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\EmergencyTalonSignal.ui'
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

class Ui_EmergencyTalonSignalDialog(object):
    def setupUi(self, EmergencyTalonSignalDialog):
        EmergencyTalonSignalDialog.setObjectName(_fromUtf8("EmergencyTalonSignalDialog"))
        EmergencyTalonSignalDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        EmergencyTalonSignalDialog.resize(323, 146)
        EmergencyTalonSignalDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(EmergencyTalonSignalDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblBegDate = QtGui.QLabel(EmergencyTalonSignalDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(EmergencyTalonSignalDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(EmergencyTalonSignalDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EmergencyTalonSignalDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.lblTypeOrder = QtGui.QLabel(EmergencyTalonSignalDialog)
        self.lblTypeOrder.setObjectName(_fromUtf8("lblTypeOrder"))
        self.gridlayout.addWidget(self.lblTypeOrder, 2, 0, 1, 1)
        self.cmbTypeOrder = QtGui.QComboBox(EmergencyTalonSignalDialog)
        self.cmbTypeOrder.setObjectName(_fromUtf8("cmbTypeOrder"))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.cmbTypeOrder.setItemText(0, _fromUtf8(""))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.cmbTypeOrder.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbTypeOrder, 2, 1, 1, 2)
        self.edtBegTime = QtGui.QTimeEdit(EmergencyTalonSignalDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridlayout.addWidget(self.edtBegTime, 1, 1, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(EmergencyTalonSignalDialog)
        self.edtEndTime.setTime(QtCore.QTime(23, 59, 0))
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridlayout.addWidget(self.edtEndTime, 1, 2, 1, 1)
        self.chkWriteMKB = QtGui.QCheckBox(EmergencyTalonSignalDialog)
        self.chkWriteMKB.setCheckable(True)
        self.chkWriteMKB.setObjectName(_fromUtf8("chkWriteMKB"))
        self.gridlayout.addWidget(self.chkWriteMKB, 5, 0, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(EmergencyTalonSignalDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EmergencyTalonSignalDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EmergencyTalonSignalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EmergencyTalonSignalDialog)
        EmergencyTalonSignalDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        EmergencyTalonSignalDialog.setTabOrder(self.edtBegTime, self.edtEndTime)
        EmergencyTalonSignalDialog.setTabOrder(self.edtEndTime, self.cmbTypeOrder)
        EmergencyTalonSignalDialog.setTabOrder(self.cmbTypeOrder, self.chkWriteMKB)
        EmergencyTalonSignalDialog.setTabOrder(self.chkWriteMKB, self.buttonBox)

    def retranslateUi(self, EmergencyTalonSignalDialog):
        EmergencyTalonSignalDialog.setWindowTitle(_translate("EmergencyTalonSignalDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("EmergencyTalonSignalDialog", "Дата", None))
        self.edtBegDate.setDisplayFormat(_translate("EmergencyTalonSignalDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("EmergencyTalonSignalDialog", "Время", None))
        self.lblTypeOrder.setText(_translate("EmergencyTalonSignalDialog", "Тип вызова", None))
        self.cmbTypeOrder.setItemText(1, _translate("EmergencyTalonSignalDialog", "Первичный", None))
        self.cmbTypeOrder.setItemText(2, _translate("EmergencyTalonSignalDialog", "Повторный", None))
        self.cmbTypeOrder.setItemText(3, _translate("EmergencyTalonSignalDialog", "Активное посещение", None))
        self.cmbTypeOrder.setItemText(4, _translate("EmergencyTalonSignalDialog", "Перевозка", None))
        self.cmbTypeOrder.setItemText(5, _translate("EmergencyTalonSignalDialog", "Амбулаторно", None))
        self.edtBegTime.setDisplayFormat(_translate("EmergencyTalonSignalDialog", "HH:mm", None))
        self.edtEndTime.setDisplayFormat(_translate("EmergencyTalonSignalDialog", "HH:mm", None))
        self.chkWriteMKB.setText(_translate("EmergencyTalonSignalDialog", "Выводить шифры МКБ", None))

from library.DateEdit import CDateEdit
