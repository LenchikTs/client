# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportDiseaseInPermilleSetup.ui'
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

class Ui_DiseaseInPermilleDialog(object):
    def setupUi(self, DiseaseInPermilleDialog):
        DiseaseInPermilleDialog.setObjectName(_fromUtf8("DiseaseInPermilleDialog"))
        DiseaseInPermilleDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DiseaseInPermilleDialog.resize(376, 294)
        DiseaseInPermilleDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DiseaseInPermilleDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAge = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 7, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 131, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(DiseaseInPermilleDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(DiseaseInPermilleDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 2, 1, 2)
        self.edtEndDate = CDateEdit(DiseaseInPermilleDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        self.lblEventPurpose = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 2, 0, 1, 1)
        self.frmMKB = QtGui.QFrame(DiseaseInPermilleDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self.gridlayout = QtGui.QGridLayout(self.frmMKB)
        self.gridlayout.setMargin(0)
        self.gridlayout.setHorizontalSpacing(4)
        self.gridlayout.setVerticalSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.gridLayout.addWidget(self.frmMKB, 8, 1, 1, 3)
        self.frmAge = QtGui.QFrame(DiseaseInPermilleDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.edtAgeFrom = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.hboxlayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(self.frmAge)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.hboxlayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.hboxlayout.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(self.frmAge)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.hboxlayout.addWidget(self.lblAgeYears)
        spacerItem4 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem4)
        self.gridLayout.addWidget(self.frmAge, 7, 1, 1, 3)
        self.frmMKBEx = QtGui.QFrame(DiseaseInPermilleDialog)
        self.frmMKBEx.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKBEx.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKBEx.setObjectName(_fromUtf8("frmMKBEx"))
        self._2 = QtGui.QGridLayout(self.frmMKBEx)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout.addWidget(self.frmMKBEx, 9, 1, 1, 3)
        self.lblBegDate = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DiseaseInPermilleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 0, 1, 4)
        self.cmbEventPurpose = CRBComboBox(DiseaseInPermilleDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 2, 1, 1, 3)
        self.cmbSex = QtGui.QComboBox(DiseaseInPermilleDialog)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 6, 1, 1, 1)
        self.cmbEventType = CRBComboBox(DiseaseInPermilleDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 3, 1, 1, 3)
        self.edtBegDate = CDateEdit(DiseaseInPermilleDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblSex = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 6, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.lblCountPermille = QtGui.QLabel(DiseaseInPermilleDialog)
        self.lblCountPermille.setObjectName(_fromUtf8("lblCountPermille"))
        self.gridLayout.addWidget(self.lblCountPermille, 11, 0, 1, 1)
        self.edtCountPermille = QtGui.QSpinBox(DiseaseInPermilleDialog)
        self.edtCountPermille.setMaximum(999999999)
        self.edtCountPermille.setProperty("value", 1000)
        self.edtCountPermille.setObjectName(_fromUtf8("edtCountPermille"))
        self.gridLayout.addWidget(self.edtCountPermille, 11, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 11, 2, 1, 2)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(DiseaseInPermilleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DiseaseInPermilleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DiseaseInPermilleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DiseaseInPermilleDialog)
        DiseaseInPermilleDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        DiseaseInPermilleDialog.setTabOrder(self.edtEndDate, self.cmbEventPurpose)
        DiseaseInPermilleDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        DiseaseInPermilleDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        DiseaseInPermilleDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        DiseaseInPermilleDialog.setTabOrder(self.cmbPerson, self.cmbSex)
        DiseaseInPermilleDialog.setTabOrder(self.cmbSex, self.edtAgeFrom)
        DiseaseInPermilleDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        DiseaseInPermilleDialog.setTabOrder(self.edtAgeTo, self.edtCountPermille)
        DiseaseInPermilleDialog.setTabOrder(self.edtCountPermille, self.buttonBox)

    def retranslateUi(self, DiseaseInPermilleDialog):
        DiseaseInPermilleDialog.setWindowTitle(_translate("DiseaseInPermilleDialog", "параметры отчёта", None))
        self.lblAge.setText(_translate("DiseaseInPermilleDialog", "Во&зраст с", None))
        self.lblPerson.setText(_translate("DiseaseInPermilleDialog", "&Врач", None))
        self.cmbPerson.setItemText(0, _translate("DiseaseInPermilleDialog", "Врач", None))
        self.lblEventPurpose.setText(_translate("DiseaseInPermilleDialog", "&Назначение обращения", None))
        self.lblAgeTo.setText(_translate("DiseaseInPermilleDialog", "по", None))
        self.lblAgeYears.setText(_translate("DiseaseInPermilleDialog", "лет", None))
        self.lblBegDate.setText(_translate("DiseaseInPermilleDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("DiseaseInPermilleDialog", "Дата &окончания периода", None))
        self.lblEventType.setText(_translate("DiseaseInPermilleDialog", "&Тип обращения", None))
        self.cmbSex.setItemText(1, _translate("DiseaseInPermilleDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("DiseaseInPermilleDialog", "Ж", None))
        self.lblSex.setText(_translate("DiseaseInPermilleDialog", "По&л", None))
        self.lblOrgStructure.setText(_translate("DiseaseInPermilleDialog", "&Подразделение", None))
        self.lblCountPermille.setText(_translate("DiseaseInPermilleDialog", "Количество населения", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox