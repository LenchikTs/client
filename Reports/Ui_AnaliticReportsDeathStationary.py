# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AnaliticReportsDeathStationary.ui'
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

class Ui_AnaliticReportsDeathStationaryDialog(object):
    def setupUi(self, AnaliticReportsDeathStationaryDialog):
        AnaliticReportsDeathStationaryDialog.setObjectName(_fromUtf8("AnaliticReportsDeathStationaryDialog"))
        AnaliticReportsDeathStationaryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AnaliticReportsDeathStationaryDialog.resize(434, 200)
        AnaliticReportsDeathStationaryDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(AnaliticReportsDeathStationaryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(AnaliticReportsDeathStationaryDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(AnaliticReportsDeathStationaryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 3)
        self.lblEndDate = QtGui.QLabel(AnaliticReportsDeathStationaryDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(AnaliticReportsDeathStationaryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 3)
        self.lblEventType = QtGui.QLabel(AnaliticReportsDeathStationaryDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        self.cmbEventType = CRBComboBox(AnaliticReportsDeathStationaryDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 4)
        self.lblOrgStructure = QtGui.QLabel(AnaliticReportsDeathStationaryDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(AnaliticReportsDeathStationaryDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 4)
        self.lblMKB = QtGui.QLabel(AnaliticReportsDeathStationaryDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 4, 0, 1, 1)
        self.cmbMKBFilter = QtGui.QComboBox(AnaliticReportsDeathStationaryDialog)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMKBFilter, 4, 1, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(AnaliticReportsDeathStationaryDialog)
        self.edtMKBFrom.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBFrom.setSizePolicy(sizePolicy)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBFrom.setMaxLength(6)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 4, 2, 1, 1)
        self.edtMKBTo = CICDCodeEdit(AnaliticReportsDeathStationaryDialog)
        self.edtMKBTo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBTo.sizePolicy().hasHeightForWidth())
        self.edtMKBTo.setSizePolicy(sizePolicy)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBTo.setMaxLength(6)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 4, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(109, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 4, 1, 1)
        self.chkIsGroupingOS = QtGui.QCheckBox(AnaliticReportsDeathStationaryDialog)
        self.chkIsGroupingOS.setChecked(True)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 5, 1, 1, 4)
        spacerItem3 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(AnaliticReportsDeathStationaryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 5)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblMKB.setBuddy(self.cmbMKBFilter)

        self.retranslateUi(AnaliticReportsDeathStationaryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnaliticReportsDeathStationaryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnaliticReportsDeathStationaryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnaliticReportsDeathStationaryDialog)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.edtEndDate, self.cmbEventType)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.cmbOrgStructure, self.cmbMKBFilter)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.cmbMKBFilter, self.edtMKBFrom)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.edtMKBTo, self.chkIsGroupingOS)
        AnaliticReportsDeathStationaryDialog.setTabOrder(self.chkIsGroupingOS, self.buttonBox)

    def retranslateUi(self, AnaliticReportsDeathStationaryDialog):
        AnaliticReportsDeathStationaryDialog.setWindowTitle(_translate("AnaliticReportsDeathStationaryDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("AnaliticReportsDeathStationaryDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("AnaliticReportsDeathStationaryDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("AnaliticReportsDeathStationaryDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("AnaliticReportsDeathStationaryDialog", "dd.MM.yyyy", None))
        self.lblEventType.setText(_translate("AnaliticReportsDeathStationaryDialog", "Тип события", None))
        self.lblOrgStructure.setText(_translate("AnaliticReportsDeathStationaryDialog", "&Подразделение", None))
        self.lblMKB.setText(_translate("AnaliticReportsDeathStationaryDialog", "Коды диагнозов по &МКБ", None))
        self.cmbMKBFilter.setItemText(0, _translate("AnaliticReportsDeathStationaryDialog", "Игнор.", None))
        self.cmbMKBFilter.setItemText(1, _translate("AnaliticReportsDeathStationaryDialog", "Интервал", None))
        self.edtMKBFrom.setInputMask(_translate("AnaliticReportsDeathStationaryDialog", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("AnaliticReportsDeathStationaryDialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("AnaliticReportsDeathStationaryDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("AnaliticReportsDeathStationaryDialog", "Z99.9", None))
        self.chkIsGroupingOS.setText(_translate("AnaliticReportsDeathStationaryDialog", "Группировка по подразделениям", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
from library.crbcombobox import CRBComboBox
