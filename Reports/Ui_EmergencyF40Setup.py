# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\EmergencyF40Setup.ui'
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

class Ui_EmergencyF40SetupDialog(object):
    def setupUi(self, EmergencyF40SetupDialog):
        EmergencyF40SetupDialog.setObjectName(_fromUtf8("EmergencyF40SetupDialog"))
        EmergencyF40SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        EmergencyF40SetupDialog.resize(378, 214)
        EmergencyF40SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(EmergencyF40SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(EmergencyF40SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 5)
        self.lblEndDate = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 5)
        self.edtEndDate = CDateEdit(EmergencyF40SetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.lblAttachType = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblAttachType.setObjectName(_fromUtf8("lblAttachType"))
        self.gridLayout.addWidget(self.lblAttachType, 4, 0, 1, 1)
        self.lblMKB = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 5, 0, 1, 1)
        self.cmbMKBFilter = QtGui.QComboBox(EmergencyF40SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMKBFilter.sizePolicy().hasHeightForWidth())
        self.cmbMKBFilter.setSizePolicy(sizePolicy)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMKBFilter, 5, 1, 1, 3)
        self.edtMKBFrom = CICDCodeEdit(EmergencyF40SetupDialog)
        self.edtMKBFrom.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBFrom.setSizePolicy(sizePolicy)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBFrom.setMaxLength(6)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 5, 4, 1, 2)
        self.edtMKBTo = CICDCodeEdit(EmergencyF40SetupDialog)
        self.edtMKBTo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBTo.sizePolicy().hasHeightForWidth())
        self.edtMKBTo.setSizePolicy(sizePolicy)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBTo.setMaxLength(6)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 5, 6, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(39, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 8, 1, 1)
        self.cmbAttachType = CRBComboBox(EmergencyF40SetupDialog)
        self.cmbAttachType.setObjectName(_fromUtf8("cmbAttachType"))
        self.gridLayout.addWidget(self.cmbAttachType, 4, 1, 1, 8)
        spacerItem3 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 7, 0, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(EmergencyF40SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 8)
        self.buttonBox = QtGui.QDialogButtonBox(EmergencyF40SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 9)
        self.lblAge = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 2, 0, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(EmergencyF40SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 2, 1, 1, 1)
        self.lblAgeTo = QtGui.QLabel(EmergencyF40SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAgeTo.sizePolicy().hasHeightForWidth())
        self.lblAgeTo.setSizePolicy(sizePolicy)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 2, 2, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(EmergencyF40SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 2, 3, 1, 1)
        self.lblAgeYears = QtGui.QLabel(EmergencyF40SetupDialog)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.gridLayout.addWidget(self.lblAgeYears, 2, 4, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 5, 1, 4)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblMKB.setBuddy(self.cmbMKBFilter)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)

        self.retranslateUi(EmergencyF40SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EmergencyF40SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EmergencyF40SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EmergencyF40SetupDialog)
        EmergencyF40SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        EmergencyF40SetupDialog.setTabOrder(self.edtEndDate, self.edtAgeFrom)
        EmergencyF40SetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        EmergencyF40SetupDialog.setTabOrder(self.edtAgeTo, self.cmbOrgStructure)
        EmergencyF40SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbAttachType)
        EmergencyF40SetupDialog.setTabOrder(self.cmbAttachType, self.cmbMKBFilter)
        EmergencyF40SetupDialog.setTabOrder(self.cmbMKBFilter, self.edtMKBFrom)
        EmergencyF40SetupDialog.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        EmergencyF40SetupDialog.setTabOrder(self.edtMKBTo, self.buttonBox)

    def retranslateUi(self, EmergencyF40SetupDialog):
        EmergencyF40SetupDialog.setWindowTitle(_translate("EmergencyF40SetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("EmergencyF40SetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("EmergencyF40SetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("EmergencyF40SetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("EmergencyF40SetupDialog", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("EmergencyF40SetupDialog", "Зона обслуживания", None))
        self.lblAttachType.setText(_translate("EmergencyF40SetupDialog", "Тип прикрепления", None))
        self.lblMKB.setText(_translate("EmergencyF40SetupDialog", "Коды диагнозов по &МКБ", None))
        self.cmbMKBFilter.setItemText(0, _translate("EmergencyF40SetupDialog", "Игнор.", None))
        self.cmbMKBFilter.setItemText(1, _translate("EmergencyF40SetupDialog", "Интервал", None))
        self.edtMKBFrom.setInputMask(_translate("EmergencyF40SetupDialog", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("EmergencyF40SetupDialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("EmergencyF40SetupDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("EmergencyF40SetupDialog", "Z99.9", None))
        self.lblAge.setText(_translate("EmergencyF40SetupDialog", "Возраст с", None))
        self.lblAgeTo.setText(_translate("EmergencyF40SetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("EmergencyF40SetupDialog", "лет", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
from library.crbcombobox import CRBComboBox
