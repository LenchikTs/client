# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StationaryF007Setup.ui'
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

class Ui_StationaryF007SetupDialog(object):
    def setupUi(self, StationaryF007SetupDialog):
        StationaryF007SetupDialog.setObjectName(_fromUtf8("StationaryF007SetupDialog"))
        StationaryF007SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryF007SetupDialog.resize(505, 343)
        StationaryF007SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryF007SetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblHospitalBedProfile = QtGui.QLabel(StationaryF007SetupDialog)
        self.lblHospitalBedProfile.setObjectName(_fromUtf8("lblHospitalBedProfile"))
        self.gridLayout.addWidget(self.lblHospitalBedProfile, 4, 0, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(StationaryF007SetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(StationaryF007SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.chkNoPrintCaption = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkNoPrintCaption.setChecked(True)
        self.chkNoPrintCaption.setObjectName(_fromUtf8("chkNoPrintCaption"))
        self.gridLayout.addWidget(self.chkNoPrintCaption, 7, 1, 1, 3)
        self.chkCompactInfo = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkCompactInfo.setObjectName(_fromUtf8("chkCompactInfo"))
        self.gridLayout.addWidget(self.chkCompactInfo, 11, 1, 1, 3)
        self.chkIsPermanentBed = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkIsPermanentBed.setObjectName(_fromUtf8("chkIsPermanentBed"))
        self.gridLayout.addWidget(self.chkIsPermanentBed, 6, 1, 1, 3)
        self.chkNoProfileBed = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkNoProfileBed.setChecked(True)
        self.chkNoProfileBed.setObjectName(_fromUtf8("chkNoProfileBed"))
        self.gridLayout.addWidget(self.chkNoProfileBed, 5, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.edtBegDate = CDateEdit(StationaryF007SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryF007SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 14, 0, 1, 4)
        self.lblEndDate = QtGui.QLabel(StationaryF007SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(StationaryF007SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.chkIsEventInfo = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkIsEventInfo.setObjectName(_fromUtf8("chkIsEventInfo"))
        self.gridLayout.addWidget(self.chkIsEventInfo, 10, 1, 1, 3)
        self.lblSchedule = QtGui.QLabel(StationaryF007SetupDialog)
        self.lblSchedule.setObjectName(_fromUtf8("lblSchedule"))
        self.gridLayout.addWidget(self.lblSchedule, 3, 0, 1, 1)
        self.cmbHospitalBedProfile = CRBComboBox(StationaryF007SetupDialog)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 4, 1, 1, 3)
        self.chkNoPrintFilterParameters = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkNoPrintFilterParameters.setObjectName(_fromUtf8("chkNoPrintFilterParameters"))
        self.gridLayout.addWidget(self.chkNoPrintFilterParameters, 8, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(StationaryF007SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryF007SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 3)
        self.cmbSchedule = QtGui.QComboBox(StationaryF007SetupDialog)
        self.cmbSchedule.setObjectName(_fromUtf8("cmbSchedule"))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSchedule, 3, 1, 1, 3)
        self.chkIsGroupingOS = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 9, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 13, 0, 1, 1)
        self.edtTimeEdit = QtGui.QTimeEdit(StationaryF007SetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 1, 2, 1, 1)
        self.chkFinance = QtGui.QCheckBox(StationaryF007SetupDialog)
        self.chkFinance.setEnabled(True)
        self.chkFinance.setCheckable(True)
        self.chkFinance.setObjectName(_fromUtf8("chkFinance"))
        self.gridLayout.addWidget(self.chkFinance, 12, 0, 1, 1)
        self.cmbFinance = CCheckableComboBox(StationaryF007SetupDialog)
        self.cmbFinance.setEnabled(False)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 12, 1, 1, 3)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(StationaryF007SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryF007SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryF007SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryF007SetupDialog)
        StationaryF007SetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        StationaryF007SetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        StationaryF007SetupDialog.setTabOrder(self.edtEndDate, self.edtTimeEdit)
        StationaryF007SetupDialog.setTabOrder(self.edtTimeEdit, self.cmbOrgStructure)
        StationaryF007SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSchedule)
        StationaryF007SetupDialog.setTabOrder(self.cmbSchedule, self.cmbHospitalBedProfile)
        StationaryF007SetupDialog.setTabOrder(self.cmbHospitalBedProfile, self.chkNoProfileBed)
        StationaryF007SetupDialog.setTabOrder(self.chkNoProfileBed, self.chkIsPermanentBed)
        StationaryF007SetupDialog.setTabOrder(self.chkIsPermanentBed, self.chkNoPrintCaption)
        StationaryF007SetupDialog.setTabOrder(self.chkNoPrintCaption, self.chkNoPrintFilterParameters)
        StationaryF007SetupDialog.setTabOrder(self.chkNoPrintFilterParameters, self.chkIsGroupingOS)
        StationaryF007SetupDialog.setTabOrder(self.chkIsGroupingOS, self.chkIsEventInfo)
        StationaryF007SetupDialog.setTabOrder(self.chkIsEventInfo, self.chkCompactInfo)
        StationaryF007SetupDialog.setTabOrder(self.chkCompactInfo, self.buttonBox)

    def retranslateUi(self, StationaryF007SetupDialog):
        StationaryF007SetupDialog.setWindowTitle(_translate("StationaryF007SetupDialog", "параметры отчёта", None))
        self.lblHospitalBedProfile.setText(_translate("StationaryF007SetupDialog", "Профиль койки", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryF007SetupDialog", "dd.MM.yyyy", None))
        self.chkNoPrintCaption.setText(_translate("StationaryF007SetupDialog", "Не печатать заголовок отчета", None))
        self.chkCompactInfo.setText(_translate("StationaryF007SetupDialog", "Краткое представление", None))
        self.chkIsPermanentBed.setText(_translate("StationaryF007SetupDialog", "Добавить внештатные койки в коечный фонд", None))
        self.chkNoProfileBed.setText(_translate("StationaryF007SetupDialog", "Учитывать койки без профиля", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryF007SetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("StationaryF007SetupDialog", "Текущий день", None))
        self.lblBegDate.setText(_translate("StationaryF007SetupDialog", "Дата начала", None))
        self.chkIsEventInfo.setText(_translate("StationaryF007SetupDialog", "Включить данные о случае", None))
        self.lblSchedule.setText(_translate("StationaryF007SetupDialog", "Режим койки", None))
        self.chkNoPrintFilterParameters.setText(_translate("StationaryF007SetupDialog", "Не печатать параметры фильтра", None))
        self.lblOrgStructure.setText(_translate("StationaryF007SetupDialog", "&Подразделение", None))
        self.cmbSchedule.setItemText(0, _translate("StationaryF007SetupDialog", "Не учитывать", None))
        self.cmbSchedule.setItemText(1, _translate("StationaryF007SetupDialog", "Круглосуточные", None))
        self.cmbSchedule.setItemText(2, _translate("StationaryF007SetupDialog", "Не круглосуточные", None))
        self.chkIsGroupingOS.setText(_translate("StationaryF007SetupDialog", "Группировка по подразделениям", None))
        self.chkFinance.setText(_translate("StationaryF007SetupDialog", "Тип финансирования", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Reports.Utils import CCheckableComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox