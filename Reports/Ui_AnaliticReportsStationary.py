# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AnaliticReportsStationary.ui'
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

class Ui_AnaliticReportsStationaryDialog(object):
    def setupUi(self, AnaliticReportsStationaryDialog):
        AnaliticReportsStationaryDialog.setObjectName(_fromUtf8("AnaliticReportsStationaryDialog"))
        AnaliticReportsStationaryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AnaliticReportsStationaryDialog.resize(461, 224)
        AnaliticReportsStationaryDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(AnaliticReportsStationaryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrgStructure = COrgStructureComboBox(AnaliticReportsStationaryDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 3)
        self.lblTypeSurgery = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblTypeSurgery.setObjectName(_fromUtf8("lblTypeSurgery"))
        self.gridLayout.addWidget(self.lblTypeSurgery, 6, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.edtBegDate = CDateEdit(AnaliticReportsStationaryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 2)
        self.edtEndDate = CDateEdit(AnaliticReportsStationaryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.cmbTypeSurgery = QtGui.QComboBox(AnaliticReportsStationaryDialog)
        self.cmbTypeSurgery.setObjectName(_fromUtf8("cmbTypeSurgery"))
        self.cmbTypeSurgery.addItem(_fromUtf8(""))
        self.cmbTypeSurgery.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypeSurgery, 6, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(AnaliticReportsStationaryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 4)
        self.lblBegDate = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 2)
        self.cmbEventType = CRBComboBox(AnaliticReportsStationaryDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 3)
        self.cmbPerson = CPersonComboBoxEx(AnaliticReportsStationaryDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 4, 1, 1, 3)
        self.lblEventType = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 4, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(AnaliticReportsStationaryDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 5, 1, 1, 3)
        self.lblSpeciality = QtGui.QLabel(AnaliticReportsStationaryDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 5, 0, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(AnaliticReportsStationaryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnaliticReportsStationaryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnaliticReportsStationaryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnaliticReportsStationaryDialog)
        AnaliticReportsStationaryDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        AnaliticReportsStationaryDialog.setTabOrder(self.edtEndDate, self.cmbEventType)
        AnaliticReportsStationaryDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        AnaliticReportsStationaryDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        AnaliticReportsStationaryDialog.setTabOrder(self.cmbPerson, self.cmbSpeciality)
        AnaliticReportsStationaryDialog.setTabOrder(self.cmbSpeciality, self.cmbTypeSurgery)
        AnaliticReportsStationaryDialog.setTabOrder(self.cmbTypeSurgery, self.buttonBox)

    def retranslateUi(self, AnaliticReportsStationaryDialog):
        AnaliticReportsStationaryDialog.setWindowTitle(_translate("AnaliticReportsStationaryDialog", "параметры отчёта", None))
        self.lblTypeSurgery.setText(_translate("AnaliticReportsStationaryDialog", "Учет операций", None))
        self.lblEndDate.setText(_translate("AnaliticReportsStationaryDialog", "Дата &окончания периода", None))
        self.lblOrgStructure.setText(_translate("AnaliticReportsStationaryDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("AnaliticReportsStationaryDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("AnaliticReportsStationaryDialog", "dd.MM.yyyy", None))
        self.cmbTypeSurgery.setItemText(0, _translate("AnaliticReportsStationaryDialog", "Номенклатурный", None))
        self.cmbTypeSurgery.setItemText(1, _translate("AnaliticReportsStationaryDialog", "Пользовательский", None))
        self.lblBegDate.setText(_translate("AnaliticReportsStationaryDialog", "Дата &начала периода", None))
        self.lblEventType.setText(_translate("AnaliticReportsStationaryDialog", "Тип события", None))
        self.lblPerson.setText(_translate("AnaliticReportsStationaryDialog", "Врач", None))
        self.lblSpeciality.setText(_translate("AnaliticReportsStationaryDialog", "Специальность", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
