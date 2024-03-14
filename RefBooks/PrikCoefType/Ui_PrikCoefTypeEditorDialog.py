# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\PrikCoefType\PrikCoefTypeEditorDialog.ui'
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

class Ui_PrikCoefTypeEditorDialog(object):
    def setupUi(self, PrikCoefTypeEditorDialog):
        PrikCoefTypeEditorDialog.setObjectName(_fromUtf8("PrikCoefTypeEditorDialog"))
        PrikCoefTypeEditorDialog.resize(652, 396)
        PrikCoefTypeEditorDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(PrikCoefTypeEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblPeriodFrom = QtGui.QLabel(PrikCoefTypeEditorDialog)
        self.lblPeriodFrom.setObjectName(_fromUtf8("lblPeriodFrom"))
        self.horizontalLayout.addWidget(self.lblPeriodFrom)
        self.edtBegDate = CDateEdit(PrikCoefTypeEditorDialog)
        self.edtBegDate.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.lblPeriodTo = QtGui.QLabel(PrikCoefTypeEditorDialog)
        self.lblPeriodTo.setObjectName(_fromUtf8("lblPeriodTo"))
        self.horizontalLayout.addWidget(self.lblPeriodTo)
        self.edtEndDate = CDateEdit(PrikCoefTypeEditorDialog)
        self.edtEndDate.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 3)
        self.cmbInsurer = CInsurerComboBox(PrikCoefTypeEditorDialog)
        self.cmbInsurer.setEnabled(True)
        self.cmbInsurer.setObjectName(_fromUtf8("cmbInsurer"))
        self.gridLayout.addWidget(self.cmbInsurer, 2, 1, 1, 3)
        self.cmbCoefType = QtGui.QComboBox(PrikCoefTypeEditorDialog)
        self.cmbCoefType.setEnabled(True)
        self.cmbCoefType.setEditable(False)
        self.cmbCoefType.setObjectName(_fromUtf8("cmbCoefType"))
        self.cmbCoefType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbCoefType, 0, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(PrikCoefTypeEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 2, 1, 2)
        self.tblPrikCoefItem = CInDocTableView(PrikCoefTypeEditorDialog)
        self.tblPrikCoefItem.setEnabled(True)
        self.tblPrikCoefItem.setObjectName(_fromUtf8("tblPrikCoefItem"))
        self.gridLayout.addWidget(self.tblPrikCoefItem, 3, 0, 1, 4)
        self.lblInsurer = QtGui.QLabel(PrikCoefTypeEditorDialog)
        self.lblInsurer.setObjectName(_fromUtf8("lblInsurer"))
        self.gridLayout.addWidget(self.lblInsurer, 2, 0, 1, 1)
        self.lblPeriod = QtGui.QLabel(PrikCoefTypeEditorDialog)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 1, 0, 1, 1)
        self.lblCoefType = QtGui.QLabel(PrikCoefTypeEditorDialog)
        self.lblCoefType.setObjectName(_fromUtf8("lblCoefType"))
        self.gridLayout.addWidget(self.lblCoefType, 0, 0, 1, 1)
        self.lblPeriodFrom.setBuddy(self.edtBegDate)
        self.lblPeriodTo.setBuddy(self.edtEndDate)
        self.lblInsurer.setBuddy(self.cmbInsurer)
        self.lblCoefType.setBuddy(self.cmbCoefType)

        self.retranslateUi(PrikCoefTypeEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrikCoefTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrikCoefTypeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrikCoefTypeEditorDialog)

    def retranslateUi(self, PrikCoefTypeEditorDialog):
        PrikCoefTypeEditorDialog.setWindowTitle(_translate("PrikCoefTypeEditorDialog", "Поправочные коэффициенты", None))
        self.lblPeriodFrom.setText(_translate("PrikCoefTypeEditorDialog", "с", None))
        self.edtBegDate.setDisplayFormat(_translate("PrikCoefTypeEditorDialog", "dd.MM.yyyy", None))
        self.lblPeriodTo.setText(_translate("PrikCoefTypeEditorDialog", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("PrikCoefTypeEditorDialog", "dd.MM.yyyy", None))
        self.cmbCoefType.setItemText(0, _translate("PrikCoefTypeEditorDialog", "К2 | Поправочный коэффициент стоимости пролеченных больных", None))
        self.lblInsurer.setText(_translate("PrikCoefTypeEditorDialog", "Страховая компания", None))
        self.lblPeriod.setText(_translate("PrikCoefTypeEditorDialog", "Период", None))
        self.lblCoefType.setText(_translate("PrikCoefTypeEditorDialog", "Тип коэффициента", None))

from Orgs.OrgComboBox import CInsurerComboBox
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
