# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\EmergencyCallListSetup.ui'
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

class Ui_EmergencyCallListSetupDialog(object):
    def setupUi(self, EmergencyCallListSetupDialog):
        EmergencyCallListSetupDialog.setObjectName(_fromUtf8("EmergencyCallListSetupDialog"))
        EmergencyCallListSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        EmergencyCallListSetupDialog.resize(467, 161)
        EmergencyCallListSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(EmergencyCallListSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrgStructure = COrgStructureComboBox(EmergencyCallListSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 3, 1, 3)
        self.lblBegDate = QtGui.QLabel(EmergencyCallListSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(EmergencyCallListSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 6)
        self.edtBegDate = CDateEdit(EmergencyCallListSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 3, 1, 2)
        self.frmAge = QtGui.QFrame(EmergencyCallListSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self._2 = QtGui.QHBoxLayout(self.frmAge)
        self._2.setMargin(0)
        self._2.setSpacing(4)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout.addWidget(self.frmAge, 4, 3, 1, 1)
        self.lblEndDate = QtGui.QLabel(EmergencyCallListSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 1)
        self.edtEndDate = CDateEdit(EmergencyCallListSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 3, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(EmergencyCallListSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 3)
        self.lblAttachType = QtGui.QLabel(EmergencyCallListSetupDialog)
        self.lblAttachType.setObjectName(_fromUtf8("lblAttachType"))
        self.gridLayout.addWidget(self.lblAttachType, 3, 0, 1, 1)
        self.cmbAttachType = CRBComboBox(EmergencyCallListSetupDialog)
        self.cmbAttachType.setObjectName(_fromUtf8("cmbAttachType"))
        self.gridLayout.addWidget(self.cmbAttachType, 3, 3, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(EmergencyCallListSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EmergencyCallListSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EmergencyCallListSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EmergencyCallListSetupDialog)
        EmergencyCallListSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        EmergencyCallListSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        EmergencyCallListSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, EmergencyCallListSetupDialog):
        EmergencyCallListSetupDialog.setWindowTitle(_translate("EmergencyCallListSetupDialog", "Список вызовов (СМП)", None))
        self.lblBegDate.setText(_translate("EmergencyCallListSetupDialog", "Дата начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("EmergencyCallListSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("EmergencyCallListSetupDialog", "Дата окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("EmergencyCallListSetupDialog", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("EmergencyCallListSetupDialog", "Зона обслуживания", None))
        self.lblAttachType.setText(_translate("EmergencyCallListSetupDialog", "Тип прикрепления", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
