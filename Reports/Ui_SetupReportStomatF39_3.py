# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\SetupReportStomatF39_3.ui'
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

class Ui_SetupReportStomatF39_3Dialog(object):
    def setupUi(self, SetupReportStomatF39_3Dialog):
        SetupReportStomatF39_3Dialog.setObjectName(_fromUtf8("SetupReportStomatF39_3Dialog"))
        SetupReportStomatF39_3Dialog.resize(483, 186)
        self.gridLayout = QtGui.QGridLayout(SetupReportStomatF39_3Dialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkOrgStructure = QtGui.QCheckBox(SetupReportStomatF39_3Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkOrgStructure.sizePolicy().hasHeightForWidth())
        self.chkOrgStructure.setSizePolicy(sizePolicy)
        self.chkOrgStructure.setObjectName(_fromUtf8("chkOrgStructure"))
        self.gridLayout.addWidget(self.chkOrgStructure, 1, 0, 1, 1)
        self.chkPerson = QtGui.QCheckBox(SetupReportStomatF39_3Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPerson.sizePolicy().hasHeightForWidth())
        self.chkPerson.setSizePolicy(sizePolicy)
        self.chkPerson.setObjectName(_fromUtf8("chkPerson"))
        self.gridLayout.addWidget(self.chkPerson, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 5)
        self.edtBegDate = CDateEdit(SetupReportStomatF39_3Dialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SetupReportStomatF39_3Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 5)
        self.label = QtGui.QLabel(SetupReportStomatF39_3Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(SetupReportStomatF39_3Dialog)
        self.cmbPerson.setEnabled(False)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 4)
        self.lblDate = QtGui.QLabel(SetupReportStomatF39_3Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(SetupReportStomatF39_3Dialog)
        self.cmbOrgStructure.setEnabled(False)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 4)
        self.chkSex = QtGui.QCheckBox(SetupReportStomatF39_3Dialog)
        self.chkSex.setObjectName(_fromUtf8("chkSex"))
        self.gridLayout.addWidget(self.chkSex, 5, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(SetupReportStomatF39_3Dialog)
        self.cmbSex.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSex.sizePolicy().hasHeightForWidth())
        self.cmbSex.setSizePolicy(sizePolicy)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 5, 1, 1, 4)
        self.chkAge = QtGui.QCheckBox(SetupReportStomatF39_3Dialog)
        self.chkAge.setObjectName(_fromUtf8("chkAge"))
        self.gridLayout.addWidget(self.chkAge, 4, 0, 1, 1)
        self.frmAge = QtGui.QFrame(SetupReportStomatF39_3Dialog)
        self.frmAge.setEnabled(False)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.lblAge = QtGui.QLabel(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAge.sizePolicy().hasHeightForWidth())
        self.lblAge.setSizePolicy(sizePolicy)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.hboxlayout.addWidget(self.lblAge)
        self.edtAgeFrom = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.hboxlayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAgeTo.sizePolicy().hasHeightForWidth())
        self.lblAgeTo.setSizePolicy(sizePolicy)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.hboxlayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.hboxlayout.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAgeYears.sizePolicy().hasHeightForWidth())
        self.lblAgeYears.setSizePolicy(sizePolicy)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.hboxlayout.addWidget(self.lblAgeYears)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.frmAge, 4, 1, 1, 4)
        self.edtEndDate = CDateEdit(SetupReportStomatF39_3Dialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 3, 1, 1)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)

        self.retranslateUi(SetupReportStomatF39_3Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SetupReportStomatF39_3Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SetupReportStomatF39_3Dialog.reject)
        QtCore.QObject.connect(self.chkOrgStructure, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbOrgStructure.setEnabled)
        QtCore.QObject.connect(self.chkPerson, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbPerson.setEnabled)
        QtCore.QObject.connect(self.chkAge, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.frmAge.setEnabled)
        QtCore.QObject.connect(self.chkSex, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbSex.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(SetupReportStomatF39_3Dialog)
        SetupReportStomatF39_3Dialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        SetupReportStomatF39_3Dialog.setTabOrder(self.edtEndDate, self.chkOrgStructure)
        SetupReportStomatF39_3Dialog.setTabOrder(self.chkOrgStructure, self.cmbOrgStructure)
        SetupReportStomatF39_3Dialog.setTabOrder(self.cmbOrgStructure, self.chkPerson)
        SetupReportStomatF39_3Dialog.setTabOrder(self.chkPerson, self.cmbPerson)
        SetupReportStomatF39_3Dialog.setTabOrder(self.cmbPerson, self.chkAge)
        SetupReportStomatF39_3Dialog.setTabOrder(self.chkAge, self.edtAgeFrom)
        SetupReportStomatF39_3Dialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        SetupReportStomatF39_3Dialog.setTabOrder(self.edtAgeTo, self.chkSex)
        SetupReportStomatF39_3Dialog.setTabOrder(self.chkSex, self.cmbSex)
        SetupReportStomatF39_3Dialog.setTabOrder(self.cmbSex, self.buttonBox)

    def retranslateUi(self, SetupReportStomatF39_3Dialog):
        SetupReportStomatF39_3Dialog.setWindowTitle(_translate("SetupReportStomatF39_3Dialog", "Dialog", None))
        self.chkOrgStructure.setText(_translate("SetupReportStomatF39_3Dialog", "Подразделение", None))
        self.chkPerson.setText(_translate("SetupReportStomatF39_3Dialog", "Исполнитель", None))
        self.edtBegDate.setDisplayFormat(_translate("SetupReportStomatF39_3Dialog", "dd.MM.yyyy", None))
        self.label.setText(_translate("SetupReportStomatF39_3Dialog", "по", None))
        self.lblDate.setText(_translate("SetupReportStomatF39_3Dialog", "Период", None))
        self.chkSex.setText(_translate("SetupReportStomatF39_3Dialog", "Пол", None))
        self.cmbSex.setItemText(1, _translate("SetupReportStomatF39_3Dialog", "Мужской", None))
        self.cmbSex.setItemText(2, _translate("SetupReportStomatF39_3Dialog", "Женский", None))
        self.chkAge.setText(_translate("SetupReportStomatF39_3Dialog", "Возраст ", None))
        self.lblAge.setText(_translate("SetupReportStomatF39_3Dialog", "с", None))
        self.lblAgeTo.setText(_translate("SetupReportStomatF39_3Dialog", "по", None))
        self.lblAgeYears.setText(_translate("SetupReportStomatF39_3Dialog", "лет", None))
        self.edtEndDate.setDisplayFormat(_translate("SetupReportStomatF39_3Dialog", "dd.MM.yyyy", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit