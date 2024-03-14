# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Reports\StationaryF30KKSetup.ui'
#
# Created: Fri Jun 21 15:20:26 2019
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

class Ui_StationaryF30KKSetupDialog(object):
    def setupUi(self, StationaryF30KKSetupDialog):
        StationaryF30KKSetupDialog.setObjectName(_fromUtf8("StationaryF30KKSetupDialog"))
        StationaryF30KKSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryF30KKSetupDialog.resize(545, 244)
        StationaryF30KKSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryF30KKSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrgStructure = COrgStructureComboBox(StationaryF30KKSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 3)
        self.edtTimeEdit = QtGui.QTimeEdit(StationaryF30KKSetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 1, 2, 1, 1)
        self.lblSchedule = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblSchedule.setObjectName(_fromUtf8("lblSchedule"))
        self.gridLayout.addWidget(self.lblSchedule, 4, 0, 1, 1)
        self.cmbSchedule = QtGui.QComboBox(StationaryF30KKSetupDialog)
        self.cmbSchedule.setObjectName(_fromUtf8("cmbSchedule"))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSchedule, 4, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 11, 0, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(StationaryF30KKSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(StationaryF30KKSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.lblBegDate = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryF30KKSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(StationaryF30KKSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblFinance = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 5, 0, 1, 1)
        self.cmbFinance = CRBComboBox(StationaryF30KKSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 5, 1, 1, 3)
        self.lblStacType = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblStacType.setObjectName(_fromUtf8("lblStacType"))
        self.gridLayout.addWidget(self.lblStacType, 3, 0, 1, 1)
        self.cmbStacType = QtGui.QComboBox(StationaryF30KKSetupDialog)
        self.cmbStacType.setObjectName(_fromUtf8("cmbStacType"))
        self.cmbStacType.addItem(_fromUtf8(""))
        self.cmbStacType.addItem(_fromUtf8(""))
        self.cmbStacType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbStacType, 3, 1, 1, 3)
        self.chkPermanentBed = QtGui.QCheckBox(StationaryF30KKSetupDialog)
        self.chkPermanentBed.setObjectName(_fromUtf8("chkPermanentBed"))
        self.gridLayout.addWidget(self.chkPermanentBed, 7, 0, 1, 4)
        self.chkEventExpose = QtGui.QCheckBox(StationaryF30KKSetupDialog)
        self.chkEventExpose.setObjectName(_fromUtf8("chkEventExpose"))
        self.gridLayout.addWidget(self.chkEventExpose, 8, 0, 1, 4)
        self.lblAddressType = QtGui.QLabel(StationaryF30KKSetupDialog)
        self.lblAddressType.setObjectName(_fromUtf8("lblAddressType"))
        self.gridLayout.addWidget(self.lblAddressType, 6, 0, 1, 1)
        self.cmbAddressType = QtGui.QComboBox(StationaryF30KKSetupDialog)
        self.cmbAddressType.setObjectName(_fromUtf8("cmbAddressType"))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAddressType, 6, 1, 1, 3)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(StationaryF30KKSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryF30KKSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryF30KKSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryF30KKSetupDialog)
        StationaryF30KKSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        StationaryF30KKSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        StationaryF30KKSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, StationaryF30KKSetupDialog):
        StationaryF30KKSetupDialog.setWindowTitle(_translate("StationaryF30KKSetupDialog", "параметры отчёта", None))
        self.lblSchedule.setText(_translate("StationaryF30KKSetupDialog", "Режим койки", None))
        self.cmbSchedule.setItemText(0, _translate("StationaryF30KKSetupDialog", "Не учитывать", None))
        self.cmbSchedule.setItemText(1, _translate("StationaryF30KKSetupDialog", "Круглосуточные", None))
        self.cmbSchedule.setItemText(2, _translate("StationaryF30KKSetupDialog", "Не круглосуточные", None))
        self.lblOrgStructure.setText(_translate("StationaryF30KKSetupDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryF30KKSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("StationaryF30KKSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("StationaryF30KKSetupDialog", "Дата окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryF30KKSetupDialog", "dd.MM.yyyy", None))
        self.lblFinance.setText(_translate("StationaryF30KKSetupDialog", "Тип финансирования", None))
        self.lblStacType.setText(_translate("StationaryF30KKSetupDialog", "Тип стационара", None))
        self.cmbStacType.setItemText(0, _translate("StationaryF30KKSetupDialog", "Не учитывать", None))
        self.cmbStacType.setItemText(1, _translate("StationaryF30KKSetupDialog", "Круглосуточный", None))
        self.cmbStacType.setItemText(2, _translate("StationaryF30KKSetupDialog", "Дневной", None))
        self.chkPermanentBed.setText(_translate("StationaryF30KKSetupDialog", "Учитывать внештатные койки", None))
        self.chkEventExpose.setText(_translate("StationaryF30KKSetupDialog", "Учитывать флаг \"Выставлять в счёт\"", None))
        self.lblAddressType.setText(_translate("StationaryF30KKSetupDialog", "Адрес", None))
        self.cmbAddressType.setItemText(0, _translate("StationaryF30KKSetupDialog", "По регистрации", None))
        self.cmbAddressType.setItemText(1, _translate("StationaryF30KKSetupDialog", "По проживанию", None))

from library.crbcombobox import CRBComboBox
from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
