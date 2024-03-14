# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\NumberInsuredPersonsSMOSetup.ui'
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

class Ui_NumberInsuredPersonsSMOSetupDialog(object):
    def setupUi(self, NumberInsuredPersonsSMOSetupDialog):
        NumberInsuredPersonsSMOSetupDialog.setObjectName(_fromUtf8("NumberInsuredPersonsSMOSetupDialog"))
        NumberInsuredPersonsSMOSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NumberInsuredPersonsSMOSetupDialog.resize(413, 230)
        NumberInsuredPersonsSMOSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(NumberInsuredPersonsSMOSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPolicyKind = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblPolicyKind.setObjectName(_fromUtf8("lblPolicyKind"))
        self.gridLayout.addWidget(self.lblPolicyKind, 3, 0, 1, 1)
        self.lblPolicyType = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblPolicyType.setObjectName(_fromUtf8("lblPolicyType"))
        self.gridLayout.addWidget(self.lblPolicyType, 2, 0, 1, 1)
        self.edtPolicyDate = CDateEdit(NumberInsuredPersonsSMOSetupDialog)
        self.edtPolicyDate.setCalendarPopup(True)
        self.edtPolicyDate.setObjectName(_fromUtf8("edtPolicyDate"))
        self.gridLayout.addWidget(self.edtPolicyDate, 0, 1, 2, 2)
        self.lblPolicyDate = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblPolicyDate.setObjectName(_fromUtf8("lblPolicyDate"))
        self.gridLayout.addWidget(self.lblPolicyDate, 0, 0, 2, 1)
        self.lblInsurer = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblInsurer.setObjectName(_fromUtf8("lblInsurer"))
        self.gridLayout.addWidget(self.lblInsurer, 4, 0, 1, 1)
        self.lblSex = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.cmbSex = QtGui.QComboBox(NumberInsuredPersonsSMOSetupDialog)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 5, 1, 1, 1)
        self.lblAge = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 6, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.cmbPolicyType = CRBComboBox(NumberInsuredPersonsSMOSetupDialog)
        self.cmbPolicyType.setObjectName(_fromUtf8("cmbPolicyType"))
        self.gridLayout.addWidget(self.cmbPolicyType, 2, 1, 1, 3)
        self.cmbPolicyKind = CRBComboBox(NumberInsuredPersonsSMOSetupDialog)
        self.cmbPolicyKind.setObjectName(_fromUtf8("cmbPolicyKind"))
        self.gridLayout.addWidget(self.cmbPolicyKind, 3, 1, 1, 3)
        self.cmbInsurer = CInsurerComboBox(NumberInsuredPersonsSMOSetupDialog)
        self.cmbInsurer.setObjectName(_fromUtf8("cmbInsurer"))
        self.gridLayout.addWidget(self.cmbInsurer, 4, 1, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.edtAgeFrom = QtGui.QSpinBox(NumberInsuredPersonsSMOSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.horizontalLayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAgeTo.sizePolicy().hasHeightForWidth())
        self.lblAgeTo.setSizePolicy(sizePolicy)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.horizontalLayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(NumberInsuredPersonsSMOSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.horizontalLayout.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(NumberInsuredPersonsSMOSetupDialog)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.horizontalLayout.addWidget(self.lblAgeYears)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(NumberInsuredPersonsSMOSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 4)
        self.lblPolicyDate.setBuddy(self.edtPolicyDate)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)

        self.retranslateUi(NumberInsuredPersonsSMOSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NumberInsuredPersonsSMOSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NumberInsuredPersonsSMOSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NumberInsuredPersonsSMOSetupDialog)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.edtPolicyDate, self.cmbPolicyType)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.cmbPolicyType, self.cmbPolicyKind)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.cmbPolicyKind, self.cmbInsurer)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.cmbInsurer, self.cmbSex)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.cmbSex, self.edtAgeFrom)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        NumberInsuredPersonsSMOSetupDialog.setTabOrder(self.edtAgeTo, self.buttonBox)

    def retranslateUi(self, NumberInsuredPersonsSMOSetupDialog):
        NumberInsuredPersonsSMOSetupDialog.setWindowTitle(_translate("NumberInsuredPersonsSMOSetupDialog", "параметры отчёта", None))
        self.lblPolicyKind.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "Вид полиса", None))
        self.lblPolicyType.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "Тип полиса", None))
        self.edtPolicyDate.setDisplayFormat(_translate("NumberInsuredPersonsSMOSetupDialog", "dd.MM.yyyy", None))
        self.lblPolicyDate.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "Дата", None))
        self.lblInsurer.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "Страховая компания", None))
        self.lblSex.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "По&л", None))
        self.cmbSex.setItemText(1, _translate("NumberInsuredPersonsSMOSetupDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("NumberInsuredPersonsSMOSetupDialog", "Ж", None))
        self.lblAge.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "Возраст с", None))
        self.lblAgeTo.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("NumberInsuredPersonsSMOSetupDialog", "лет", None))

from Orgs.OrgComboBox import CInsurerComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
