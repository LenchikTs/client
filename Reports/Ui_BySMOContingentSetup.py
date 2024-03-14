# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Samson\UP_s11\client_test\Reports\BySMOContingentSetup.ui'
#
# Created: Mon May 15 10:58:06 2023
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_BySMOContingentSetupDialog(object):
    def setupUi(self, BySMOContingentSetupDialog):
        BySMOContingentSetupDialog.setObjectName(_fromUtf8("BySMOContingentSetupDialog"))
        BySMOContingentSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        BySMOContingentSetupDialog.resize(356, 206)
        BySMOContingentSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(BySMOContingentSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPolicyDate = QtGui.QLabel(BySMOContingentSetupDialog)
        self.lblPolicyDate.setObjectName(_fromUtf8("lblPolicyDate"))
        self.gridLayout.addWidget(self.lblPolicyDate, 0, 0, 1, 1)
        self.edtPolicyDate = CDateEdit(BySMOContingentSetupDialog)
        self.edtPolicyDate.setCalendarPopup(True)
        self.edtPolicyDate.setObjectName(_fromUtf8("edtPolicyDate"))
        self.gridLayout.addWidget(self.edtPolicyDate, 0, 1, 1, 1)
        self.cmbPolicyKind = CRBComboBox(BySMOContingentSetupDialog)
        self.cmbPolicyKind.setObjectName(_fromUtf8("cmbPolicyKind"))
        self.gridLayout.addWidget(self.cmbPolicyKind, 2, 1, 1, 2)
        self.lblPolicyKind = QtGui.QLabel(BySMOContingentSetupDialog)
        self.lblPolicyKind.setObjectName(_fromUtf8("lblPolicyKind"))
        self.gridLayout.addWidget(self.lblPolicyKind, 2, 0, 1, 1)
        self.lblPolicyType = QtGui.QLabel(BySMOContingentSetupDialog)
        self.lblPolicyType.setObjectName(_fromUtf8("lblPolicyType"))
        self.gridLayout.addWidget(self.lblPolicyType, 1, 0, 1, 1)
        self.cmbPolicyType = CRBComboBox(BySMOContingentSetupDialog)
        self.cmbPolicyType.setObjectName(_fromUtf8("cmbPolicyType"))
        self.gridLayout.addWidget(self.cmbPolicyType, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(BySMOContingentSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.lblRazrNas = QtGui.QLabel(BySMOContingentSetupDialog)
        self.lblRazrNas.setObjectName(_fromUtf8("lblRazrNas"))
        self.gridLayout.addWidget(self.lblRazrNas, 3, 0, 1, 1)
        self.cmbRazrNas = QtGui.QComboBox(BySMOContingentSetupDialog)
        self.cmbRazrNas.setObjectName(_fromUtf8("cmbRazrNas"))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbRazrNas, 3, 1, 1, 2)
        self.lblPolicyDate.setBuddy(self.edtPolicyDate)
        self.lblRazrNas.setBuddy(self.cmbRazrNas)

        self.retranslateUi(BySMOContingentSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), BySMOContingentSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), BySMOContingentSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BySMOContingentSetupDialog)
        BySMOContingentSetupDialog.setTabOrder(self.edtPolicyDate, self.cmbPolicyType)
        BySMOContingentSetupDialog.setTabOrder(self.cmbPolicyType, self.cmbPolicyKind)
        BySMOContingentSetupDialog.setTabOrder(self.cmbPolicyKind, self.buttonBox)

    def retranslateUi(self, BySMOContingentSetupDialog):
        BySMOContingentSetupDialog.setWindowTitle(_translate("BySMOContingentSetupDialog", "параметры отчёта", None))
        self.lblPolicyDate.setText(_translate("BySMOContingentSetupDialog", "Дата", None))
        self.lblPolicyKind.setText(_translate("BySMOContingentSetupDialog", "Вид полиса", None))
        self.lblPolicyType.setText(_translate("BySMOContingentSetupDialog", "Тип полиса", None))
        self.lblRazrNas.setText(_translate("BySMOContingentSetupDialog", "В разрезе населения", None))
        self.cmbRazrNas.setItemText(0, _translate("BySMOContingentSetupDialog", "Все", None))
        self.cmbRazrNas.setItemText(1, _translate("BySMOContingentSetupDialog", "Краевые", None))
        self.cmbRazrNas.setItemText(2, _translate("BySMOContingentSetupDialog", "Инокраевые", None))

from library.crbcombobox import CRBComboBox
from library.DateEdit import CDateEdit
