# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportCostSetup.ui'
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

class Ui_ReportCostSetupDialog(object):
    def setupUi(self, ReportCostSetupDialog):
        ReportCostSetupDialog.setObjectName(_fromUtf8("ReportCostSetupDialog"))
        ReportCostSetupDialog.resize(378, 187)
        ReportCostSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportCostSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbOrgStructure = COrgStructureComboBox(ReportCostSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 3, 1, 4)
        self.label_2 = QtGui.QLabel(ReportCostSetupDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.begDate = QtGui.QDateEdit(ReportCostSetupDialog)
        self.begDate.setObjectName(_fromUtf8("begDate"))
        self.gridLayout.addWidget(self.begDate, 0, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(106, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 6, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportCostSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 3)
        self.lblSpeciality = QtGui.QLabel(ReportCostSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 2, 0, 1, 3)
        self.endDate = QtGui.QDateEdit(ReportCostSetupDialog)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.gridLayout.addWidget(self.endDate, 0, 5, 1, 1)
        self.label_3 = QtGui.QLabel(ReportCostSetupDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.label = QtGui.QLabel(ReportCostSetupDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(ReportCostSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 2, 3, 1, 4)
        self.lblPerson = QtGui.QLabel(ReportCostSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 3, 0, 1, 1)
        self.lblVidPom = QtGui.QLabel(ReportCostSetupDialog)
        self.lblVidPom.setObjectName(_fromUtf8("lblVidPom"))
        self.gridLayout.addWidget(self.lblVidPom, 4, 0, 1, 3)
        self.cmbPerson = CPersonComboBoxEx(ReportCostSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 3, 3, 1, 4)
        self.cmbVidPom = CRBComboBox(ReportCostSetupDialog)
        self.cmbVidPom.setObjectName(_fromUtf8("cmbVidPom"))
        self.gridLayout.addWidget(self.cmbVidPom, 4, 3, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(ReportCostSetupDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 7)
        spacerItem1 = QtGui.QSpacerItem(20, 27, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.label_3.raise_()
        self.endDate.raise_()
        self.label.raise_()
        self.buttonBox.raise_()
        self.label_2.raise_()
        self.cmbVidPom.raise_()
        self.lblSpeciality.raise_()
        self.lblOrgStructure.raise_()
        self.lblVidPom.raise_()
        self.cmbPerson.raise_()
        self.lblPerson.raise_()
        self.cmbSpeciality.raise_()
        self.cmbOrgStructure.raise_()
        self.begDate.raise_()
        self.cmbSpeciality.raise_()
        self.lblSpeciality.raise_()
        self.label_2.setBuddy(self.begDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.label_3.setBuddy(self.endDate)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblVidPom.setBuddy(self.cmbVidPom)

        self.retranslateUi(ReportCostSetupDialog)
        QtCore.QMetaObject.connectSlotsByName(ReportCostSetupDialog)

    def retranslateUi(self, ReportCostSetupDialog):
        ReportCostSetupDialog.setWindowTitle(_translate("ReportCostSetupDialog", "Dialog", None))
        self.label_2.setText(_translate("ReportCostSetupDialog", "с", None))
        self.lblOrgStructure.setText(_translate("ReportCostSetupDialog", "&Подразделение", None))
        self.lblSpeciality.setText(_translate("ReportCostSetupDialog", "&Специальность", None))
        self.label_3.setText(_translate("ReportCostSetupDialog", "по", None))
        self.label.setText(_translate("ReportCostSetupDialog", "Период", None))
        self.cmbSpeciality.setWhatsThis(_translate("ReportCostSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblPerson.setText(_translate("ReportCostSetupDialog", "&Врач", None))
        self.lblVidPom.setText(_translate("ReportCostSetupDialog", "Вид помощи", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.crbcombobox import CRBComboBox
