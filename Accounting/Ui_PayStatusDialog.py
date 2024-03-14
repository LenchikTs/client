# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Accounting\PayStatusDialog.ui'
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

class Ui_PayStatusDialog(object):
    def setupUi(self, PayStatusDialog):
        PayStatusDialog.setObjectName(_fromUtf8("PayStatusDialog"))
        PayStatusDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PayStatusDialog.resize(343, 204)
        self.gridlayout = QtGui.QGridLayout(PayStatusDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblNote = QtGui.QLabel(PayStatusDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridlayout.addWidget(self.lblNote, 6, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(PayStatusDialog)
        self.edtNumber.setMaxLength(20)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridlayout.addWidget(self.edtNumber, 1, 1, 1, 2)
        self.lblPayRefuseType = QtGui.QLabel(PayStatusDialog)
        self.lblPayRefuseType.setEnabled(False)
        self.lblPayRefuseType.setObjectName(_fromUtf8("lblPayRefuseType"))
        self.gridlayout.addWidget(self.lblPayRefuseType, 5, 0, 1, 1)
        self.lblNumber = QtGui.QLabel(PayStatusDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridlayout.addWidget(self.lblNumber, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PayStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.cmbRefuseType = CRBComboBox(PayStatusDialog)
        self.cmbRefuseType.setEnabled(False)
        self.cmbRefuseType.setObjectName(_fromUtf8("cmbRefuseType"))
        self.gridlayout.addWidget(self.cmbRefuseType, 5, 1, 1, 2)
        self.rbnAccepted = QtGui.QRadioButton(PayStatusDialog)
        self.rbnAccepted.setChecked(True)
        self.rbnAccepted.setObjectName(_fromUtf8("rbnAccepted"))
        self.gridlayout.addWidget(self.rbnAccepted, 2, 1, 1, 1)
        self.rbnRefused = QtGui.QRadioButton(PayStatusDialog)
        self.rbnRefused.setObjectName(_fromUtf8("rbnRefused"))
        self.gridlayout.addWidget(self.rbnRefused, 2, 2, 1, 1)
        self.edtDate = CDateEdit(PayStatusDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridlayout.addWidget(self.edtDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(81, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblDate = QtGui.QLabel(PayStatusDialog)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridlayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.rbnFactPayed = QtGui.QRadioButton(PayStatusDialog)
        self.rbnFactPayed.setObjectName(_fromUtf8("rbnFactPayed"))
        self.gridlayout.addWidget(self.rbnFactPayed, 3, 1, 1, 2)
        self.edtNote = QtGui.QLineEdit(PayStatusDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridlayout.addWidget(self.edtNote, 6, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.edtFactPayed = QtGui.QDoubleSpinBox(PayStatusDialog)
        self.edtFactPayed.setEnabled(False)
        self.edtFactPayed.setDecimals(2)
        self.edtFactPayed.setMaximum(99999999.99)
        self.edtFactPayed.setObjectName(_fromUtf8("edtFactPayed"))
        self.gridlayout.addWidget(self.edtFactPayed, 4, 1, 1, 2)
        self.lblPayRefuseType.setBuddy(self.cmbRefuseType)
        self.lblNumber.setBuddy(self.edtNumber)
        self.lblDate.setBuddy(self.edtDate)

        self.retranslateUi(PayStatusDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PayStatusDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PayStatusDialog.reject)
        QtCore.QObject.connect(self.rbnRefused, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbRefuseType.setEnabled)
        QtCore.QObject.connect(self.rbnRefused, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblPayRefuseType.setEnabled)
        QtCore.QObject.connect(self.rbnFactPayed, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFactPayed.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(PayStatusDialog)
        PayStatusDialog.setTabOrder(self.edtDate, self.edtNumber)
        PayStatusDialog.setTabOrder(self.edtNumber, self.rbnAccepted)
        PayStatusDialog.setTabOrder(self.rbnAccepted, self.rbnRefused)
        PayStatusDialog.setTabOrder(self.rbnRefused, self.cmbRefuseType)
        PayStatusDialog.setTabOrder(self.cmbRefuseType, self.edtNote)
        PayStatusDialog.setTabOrder(self.edtNote, self.buttonBox)

    def retranslateUi(self, PayStatusDialog):
        PayStatusDialog.setWindowTitle(_translate("PayStatusDialog", "Подтверждение оплаты", None))
        self.lblNote.setText(_translate("PayStatusDialog", "Примечание", None))
        self.lblPayRefuseType.setText(_translate("PayStatusDialog", "Причина отказа", None))
        self.lblNumber.setText(_translate("PayStatusDialog", "Документ", None))
        self.rbnAccepted.setText(_translate("PayStatusDialog", "Оплачено", None))
        self.rbnRefused.setText(_translate("PayStatusDialog", "Отказано", None))
        self.lblDate.setText(_translate("PayStatusDialog", "Дата", None))
        self.rbnFactPayed.setText(_translate("PayStatusDialog", "Частично оплачено на сумму", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
