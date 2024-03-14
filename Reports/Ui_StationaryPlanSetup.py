# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StationaryPlanSetup.ui'
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

class Ui_StationaryPlanSetupDialog(object):
    def setupUi(self, StationaryPlanSetupDialog):
        StationaryPlanSetupDialog.setObjectName(_fromUtf8("StationaryPlanSetupDialog"))
        StationaryPlanSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryPlanSetupDialog.resize(459, 240)
        StationaryPlanSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryPlanSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 2)
        self.btnHospitalBedProfileList = QtGui.QPushButton(StationaryPlanSetupDialog)
        self.btnHospitalBedProfileList.setObjectName(_fromUtf8("btnHospitalBedProfileList"))
        self.gridLayout.addWidget(self.btnHospitalBedProfileList, 3, 0, 1, 1)
        self.chkIsPermanentBed = QtGui.QCheckBox(StationaryPlanSetupDialog)
        self.chkIsPermanentBed.setChecked(True)
        self.chkIsPermanentBed.setObjectName(_fromUtf8("chkIsPermanentBed"))
        self.gridLayout.addWidget(self.chkIsPermanentBed, 4, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryPlanSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 1, 1, 3)
        self.edtBegTime = QtGui.QTimeEdit(StationaryPlanSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.cmbFinance = CCheckableComboBox(StationaryPlanSetupDialog)
        self.cmbFinance.setEnabled(False)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 6, 1, 1, 3)
        self.lblEndDate = QtGui.QLabel(StationaryPlanSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(74, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.edtBegDate = CDateEdit(StationaryPlanSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(StationaryPlanSetupDialog)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 2, 1, 1)
        self.cmbBedsSchedule = QtGui.QComboBox(StationaryPlanSetupDialog)
        self.cmbBedsSchedule.setObjectName(_fromUtf8("cmbBedsSchedule"))
        self.cmbBedsSchedule.addItem(_fromUtf8(""))
        self.cmbBedsSchedule.addItem(_fromUtf8(""))
        self.cmbBedsSchedule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbBedsSchedule, 5, 1, 1, 3)
        self.lblBegDate = QtGui.QLabel(StationaryPlanSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblBedsSchedule = QtGui.QLabel(StationaryPlanSetupDialog)
        self.lblBedsSchedule.setObjectName(_fromUtf8("lblBedsSchedule"))
        self.gridLayout.addWidget(self.lblBedsSchedule, 5, 0, 1, 1)
        self.edtEndDate = CDateEdit(StationaryPlanSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)
        self.chkFinance = QtGui.QCheckBox(StationaryPlanSetupDialog)
        self.chkFinance.setEnabled(True)
        self.chkFinance.setCheckable(True)
        self.chkFinance.setObjectName(_fromUtf8("chkFinance"))
        self.gridLayout.addWidget(self.chkFinance, 6, 0, 1, 1)
        self.lblHospitalBedProfileList = QtGui.QLabel(StationaryPlanSetupDialog)
        self.lblHospitalBedProfileList.setWordWrap(True)
        self.lblHospitalBedProfileList.setObjectName(_fromUtf8("lblHospitalBedProfileList"))
        self.gridLayout.addWidget(self.lblHospitalBedProfileList, 3, 1, 1, 3)
        self.lblOrgStructureList = QtGui.QLabel(StationaryPlanSetupDialog)
        self.lblOrgStructureList.setWordWrap(True)
        self.lblOrgStructureList.setObjectName(_fromUtf8("lblOrgStructureList"))
        self.gridLayout.addWidget(self.lblOrgStructureList, 2, 1, 1, 3)
        self.btnOrgStructureList = QtGui.QPushButton(StationaryPlanSetupDialog)
        self.btnOrgStructureList.setObjectName(_fromUtf8("btnOrgStructureList"))
        self.gridLayout.addWidget(self.btnOrgStructureList, 2, 0, 1, 1)

        self.retranslateUi(StationaryPlanSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryPlanSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryPlanSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryPlanSetupDialog)
        StationaryPlanSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        StationaryPlanSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        StationaryPlanSetupDialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        StationaryPlanSetupDialog.setTabOrder(self.edtEndTime, self.btnOrgStructureList)
        StationaryPlanSetupDialog.setTabOrder(self.btnOrgStructureList, self.btnHospitalBedProfileList)
        StationaryPlanSetupDialog.setTabOrder(self.btnHospitalBedProfileList, self.chkIsPermanentBed)
        StationaryPlanSetupDialog.setTabOrder(self.chkIsPermanentBed, self.cmbBedsSchedule)
        StationaryPlanSetupDialog.setTabOrder(self.cmbBedsSchedule, self.chkFinance)
        StationaryPlanSetupDialog.setTabOrder(self.chkFinance, self.cmbFinance)
        StationaryPlanSetupDialog.setTabOrder(self.cmbFinance, self.buttonBox)

    def retranslateUi(self, StationaryPlanSetupDialog):
        StationaryPlanSetupDialog.setWindowTitle(_translate("StationaryPlanSetupDialog", "параметры отчёта", None))
        self.btnHospitalBedProfileList.setText(_translate("StationaryPlanSetupDialog", "Профиль койки", None))
        self.chkIsPermanentBed.setText(_translate("StationaryPlanSetupDialog", "Добавить внештатные койки в коечный фонд", None))
        self.lblEndDate.setText(_translate("StationaryPlanSetupDialog", "Конец периода", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryPlanSetupDialog", "dd.MM.yyyy", None))
        self.cmbBedsSchedule.setItemText(0, _translate("StationaryPlanSetupDialog", "не задано", None))
        self.cmbBedsSchedule.setItemText(1, _translate("StationaryPlanSetupDialog", "круглосуточные", None))
        self.cmbBedsSchedule.setItemText(2, _translate("StationaryPlanSetupDialog", "некруглосуточные", None))
        self.lblBegDate.setText(_translate("StationaryPlanSetupDialog", "Начало периода", None))
        self.lblBedsSchedule.setText(_translate("StationaryPlanSetupDialog", "Режим койки", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryPlanSetupDialog", "dd.MM.yyyy", None))
        self.chkFinance.setText(_translate("StationaryPlanSetupDialog", "Тип финансирования", None))
        self.lblHospitalBedProfileList.setText(_translate("StationaryPlanSetupDialog", "  не задано", None))
        self.lblOrgStructureList.setText(_translate("StationaryPlanSetupDialog", "  ЛПУ", None))
        self.btnOrgStructureList.setText(_translate("StationaryPlanSetupDialog", "Подразделение", None))

from Reports.Utils import CCheckableComboBox
from library.DateEdit import CDateEdit
