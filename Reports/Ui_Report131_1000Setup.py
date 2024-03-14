# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\Samson\UP_s11\client_merge\Reports\Report131_1000Setup.ui'
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

class Ui_Report131_1000SetupDialog(object):
    def setupUi(self, Report131_1000SetupDialog):
        Report131_1000SetupDialog.setObjectName(_fromUtf8("Report131_1000SetupDialog"))
        Report131_1000SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Report131_1000SetupDialog.resize(419, 226)
        Report131_1000SetupDialog.setSizeGripEnabled(True)
        Report131_1000SetupDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Report131_1000SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(Report131_1000SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(Report131_1000SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(Report131_1000SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(Report131_1000SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.lblFilterContingentType = QtGui.QLabel(Report131_1000SetupDialog)
        self.lblFilterContingentType.setObjectName(_fromUtf8("lblFilterContingentType"))
        self.gridLayout.addWidget(self.lblFilterContingentType, 3, 0, 1, 1)
        self.cmbFilterContingentType = CRBComboBox(Report131_1000SetupDialog)
        self.cmbFilterContingentType.setObjectName(_fromUtf8("cmbFilterContingentType"))
        self.gridLayout.addWidget(self.cmbFilterContingentType, 3, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(Report131_1000SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(Report131_1000SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 2)
        self.chkAttache = QtGui.QCheckBox(Report131_1000SetupDialog)
        self.chkAttache.setChecked(True)
        self.chkAttache.setObjectName(_fromUtf8("chkAttache"))
        self.gridLayout.addWidget(self.chkAttache, 5, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Report131_1000SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.btnMesDispansList = QtGui.QPushButton(Report131_1000SetupDialog)
        self.btnMesDispansList.setObjectName(_fromUtf8("btnMesDispansList"))
        self.gridLayout.addWidget(self.btnMesDispansList, 2, 0, 1, 1)
        self.lblMesDispansList = QtGui.QLabel(Report131_1000SetupDialog)
        self.lblMesDispansList.setObjectName(_fromUtf8("lblMesDispansList"))
        self.gridLayout.addWidget(self.lblMesDispansList, 2, 1, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(Report131_1000SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Report131_1000SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Report131_1000SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Report131_1000SetupDialog)
        Report131_1000SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        Report131_1000SetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, Report131_1000SetupDialog):
        Report131_1000SetupDialog.setWindowTitle(_translate("Report131_1000SetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("Report131_1000SetupDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("Report131_1000SetupDialog", "Дата &окончания периода", None))
        self.lblFilterContingentType.setText(_translate("Report131_1000SetupDialog", "Тип контингента", None))
        self.lblOrgStructure.setText(_translate("Report131_1000SetupDialog", "Подразделение", None))
        self.chkAttache.setText(_translate("Report131_1000SetupDialog", "Прикрепление к ЛПУ", None))
        self.btnMesDispansList.setText(_translate("Report131_1000SetupDialog", "Стандарт", None))
        self.lblMesDispansList.setText(_translate("Report131_1000SetupDialog", "не задано", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
