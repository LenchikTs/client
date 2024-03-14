# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StationaryF30Setup.ui'
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

class Ui_StationaryF30SetupDialog(object):
    def setupUi(self, StationaryF30SetupDialog):
        StationaryF30SetupDialog.setObjectName(_fromUtf8("StationaryF30SetupDialog"))
        StationaryF30SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryF30SetupDialog.resize(545, 350)
        StationaryF30SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryF30SetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.cmbSocStatusType = CRBComboBox(StationaryF30SetupDialog)
        self.cmbSocStatusType.setObjectName(_fromUtf8("cmbSocStatusType"))
        self.gridLayout.addWidget(self.cmbSocStatusType, 6, 1, 1, 3)
        self.edtBegTime = QtGui.QTimeEdit(StationaryF30SetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.cmbSchedule = QtGui.QComboBox(StationaryF30SetupDialog)
        self.cmbSchedule.setObjectName(_fromUtf8("cmbSchedule"))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSchedule, 3, 1, 1, 3)
        self.lblSchedule = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblSchedule.setObjectName(_fromUtf8("lblSchedule"))
        self.gridLayout.addWidget(self.lblSchedule, 3, 0, 1, 1)
        self.edtTimeEdit = QtGui.QTimeEdit(StationaryF30SetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 1, 2, 1, 1)
        self.edtBegDate = CDateEdit(StationaryF30SetupDialog)
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
        self.label = QtGui.QLabel(StationaryF30SetupDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryF30SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.cmbSocStatusClass = CSocStatusComboBox(StationaryF30SetupDialog)
        self.cmbSocStatusClass.setObjectName(_fromUtf8("cmbSocStatusClass"))
        self.gridLayout.addWidget(self.cmbSocStatusClass, 5, 1, 1, 3)
        self.cmbHospitalBedProfile = CRBComboBox(StationaryF30SetupDialog)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 4, 1, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryF30SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 3)
        self.lblSocStatusClass = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblSocStatusClass.setObjectName(_fromUtf8("lblSocStatusClass"))
        self.gridLayout.addWidget(self.lblSocStatusClass, 5, 0, 1, 1)
        self.lblHospitalBedProfile = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblHospitalBedProfile.setObjectName(_fromUtf8("lblHospitalBedProfile"))
        self.gridLayout.addWidget(self.lblHospitalBedProfile, 4, 0, 1, 1)
        self.edtEndDate = CDateEdit(StationaryF30SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblSocStatusType = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblSocStatusType.setObjectName(_fromUtf8("lblSocStatusType"))
        self.gridLayout.addWidget(self.lblSocStatusType, 6, 0, 1, 1)
        self.lblFinance = QtGui.QLabel(StationaryF30SetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 7, 0, 1, 1)
        self.cmbFinance = CRBComboBox(StationaryF30SetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 7, 1, 1, 3)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSocStatusClass.setBuddy(self.cmbSocStatusClass)
        self.lblSocStatusType.setBuddy(self.cmbSocStatusType)

        self.retranslateUi(StationaryF30SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryF30SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryF30SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StationaryF30SetupDialog)
        StationaryF30SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        StationaryF30SetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        StationaryF30SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbHospitalBedProfile)
        StationaryF30SetupDialog.setTabOrder(self.cmbHospitalBedProfile, self.cmbSocStatusClass)
        StationaryF30SetupDialog.setTabOrder(self.cmbSocStatusClass, self.cmbSocStatusType)
        StationaryF30SetupDialog.setTabOrder(self.cmbSocStatusType, self.buttonBox)

    def retranslateUi(self, StationaryF30SetupDialog):
        StationaryF30SetupDialog.setWindowTitle(_translate("StationaryF30SetupDialog", "параметры отчёта", None))
        self.lblOrgStructure.setText(_translate("StationaryF30SetupDialog", "&Подразделение", None))
        self.cmbSchedule.setItemText(0, _translate("StationaryF30SetupDialog", "Не учитывать", None))
        self.cmbSchedule.setItemText(1, _translate("StationaryF30SetupDialog", "Круглосуточные", None))
        self.cmbSchedule.setItemText(2, _translate("StationaryF30SetupDialog", "Не круглосуточные", None))
        self.lblSchedule.setText(_translate("StationaryF30SetupDialog", "Режим койки", None))
        self.edtBegDate.setDisplayFormat(_translate("StationaryF30SetupDialog", "dd.MM.yyyy", None))
        self.label.setText(_translate("StationaryF30SetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("StationaryF30SetupDialog", "Дата окончания периода", None))
        self.lblSocStatusClass.setText(_translate("StationaryF30SetupDialog", "Класс соц.статуса", None))
        self.lblHospitalBedProfile.setText(_translate("StationaryF30SetupDialog", "Профиль койки", None))
        self.edtEndDate.setDisplayFormat(_translate("StationaryF30SetupDialog", "dd.MM.yyyy", None))
        self.lblSocStatusType.setText(_translate("StationaryF30SetupDialog", "Тип соц.статуса", None))
        self.lblFinance.setText(_translate("StationaryF30SetupDialog", "Тип финансирования", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Registry.SocStatusComboBox import CSocStatusComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
