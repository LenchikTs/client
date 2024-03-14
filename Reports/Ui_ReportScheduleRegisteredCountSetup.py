# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\Reports\ReportScheduleRegisteredCountSetup.ui'
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

class Ui_ReportScheduleRegisteredCountSetup(object):
    def setupUi(self, ReportScheduleRegisteredCountSetup):
        ReportScheduleRegisteredCountSetup.setObjectName(_fromUtf8("ReportScheduleRegisteredCountSetup"))
        ReportScheduleRegisteredCountSetup.resize(519, 333)
        self.gridLayout = QtGui.QGridLayout(ReportScheduleRegisteredCountSetup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 2)
        self.edtBegDate = CDateEdit(ReportScheduleRegisteredCountSetup)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportScheduleRegisteredCountSetup)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 1)
        self.lblSpeciality = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 3, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(ReportScheduleRegisteredCountSetup)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 3, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 6, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportScheduleRegisteredCountSetup)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 6, 1, 1, 1)
        self.lblAppointmentType = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblAppointmentType.setObjectName(_fromUtf8("lblAppointmentType"))
        self.gridLayout.addWidget(self.lblAppointmentType, 7, 0, 1, 1)
        self.cmbAppointmentType = QtGui.QComboBox(ReportScheduleRegisteredCountSetup)
        self.cmbAppointmentType.setObjectName(_fromUtf8("cmbAppointmentType"))
        self.cmbAppointmentType.addItem(_fromUtf8(""))
        self.cmbAppointmentType.addItem(_fromUtf8(""))
        self.cmbAppointmentType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAppointmentType, 7, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportScheduleRegisteredCountSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportScheduleRegisteredCountSetup)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblAppointmentPurpose = QtGui.QLabel(ReportScheduleRegisteredCountSetup)
        self.lblAppointmentPurpose.setObjectName(_fromUtf8("lblAppointmentPurpose"))
        self.gridLayout.addWidget(self.lblAppointmentPurpose, 8, 1, 1, 1)
        self.btnAppointmentPurpose = QtGui.QPushButton(ReportScheduleRegisteredCountSetup)
        self.btnAppointmentPurpose.setObjectName(_fromUtf8("btnAppointmentPurpose"))
        self.gridLayout.addWidget(self.btnAppointmentPurpose, 8, 0, 1, 1)
        self.chkDetailPerson = QtGui.QCheckBox(ReportScheduleRegisteredCountSetup)
        self.chkDetailPerson.setObjectName(_fromUtf8("chkDetailPerson"))
        self.gridLayout.addWidget(self.chkDetailPerson, 4, 0, 1, 2)

        self.retranslateUi(ReportScheduleRegisteredCountSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportScheduleRegisteredCountSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportScheduleRegisteredCountSetup.reject)
        QtCore.QObject.connect(self.chkDetailPerson, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.cmbPerson.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(ReportScheduleRegisteredCountSetup)

    def retranslateUi(self, ReportScheduleRegisteredCountSetup):
        ReportScheduleRegisteredCountSetup.setWindowTitle(_translate("ReportScheduleRegisteredCountSetup", "Dialog", None))
        self.lblBegDate.setText(_translate("ReportScheduleRegisteredCountSetup", "Дата начала периода", None))
        self.lblOrgStructure.setText(_translate("ReportScheduleRegisteredCountSetup", "Подразделение", None))
        self.lblSpeciality.setText(_translate("ReportScheduleRegisteredCountSetup", "Специальность", None))
        self.lblPerson.setText(_translate("ReportScheduleRegisteredCountSetup", "Врач", None))
        self.lblAppointmentType.setText(_translate("ReportScheduleRegisteredCountSetup", "Тип приема", None))
        self.cmbAppointmentType.setItemText(0, _translate("ReportScheduleRegisteredCountSetup", "не задано", None))
        self.cmbAppointmentType.setItemText(1, _translate("ReportScheduleRegisteredCountSetup", "амбулаторный", None))
        self.cmbAppointmentType.setItemText(2, _translate("ReportScheduleRegisteredCountSetup", "на дому", None))
        self.lblEndDate.setText(_translate("ReportScheduleRegisteredCountSetup", "Дата окончания периода", None))
        self.lblAppointmentPurpose.setText(_translate("ReportScheduleRegisteredCountSetup", "не задано", None))
        self.btnAppointmentPurpose.setText(_translate("ReportScheduleRegisteredCountSetup", "Назначение приема", None))
        self.chkDetailPerson.setText(_translate("ReportScheduleRegisteredCountSetup", " Детализировать по врачам", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
