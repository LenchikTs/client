# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AnaliticReportsGeneralInfoSurgery.ui'
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

class Ui_AnaliticReportsGeneralInfoSurgeryDialog(object):
    def setupUi(self, AnaliticReportsGeneralInfoSurgeryDialog):
        AnaliticReportsGeneralInfoSurgeryDialog.setObjectName(_fromUtf8("AnaliticReportsGeneralInfoSurgeryDialog"))
        AnaliticReportsGeneralInfoSurgeryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AnaliticReportsGeneralInfoSurgeryDialog.resize(434, 309)
        AnaliticReportsGeneralInfoSurgeryDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(AnaliticReportsGeneralInfoSurgeryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkIsGroupingOS = QtGui.QCheckBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 9, 1, 1, 4)
        self.lblMKB = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 4, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblDiseaseCharacter = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblDiseaseCharacter.setObjectName(_fromUtf8("lblDiseaseCharacter"))
        self.gridLayout.addWidget(self.lblDiseaseCharacter, 6, 0, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(AnaliticReportsGeneralInfoSurgeryDialog)
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
        self.buttonBox = QtGui.QDialogButtonBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 5)
        self.edtMKBTo = CICDCodeEdit(AnaliticReportsGeneralInfoSurgeryDialog)
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
        self.cmbOrgStructure = COrgStructureComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 4)
        self.lblOrgStructure = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.edtBegDate = CDateEdit(AnaliticReportsGeneralInfoSurgeryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.cmbMKBFilter = QtGui.QComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMKBFilter, 4, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(109, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 4, 1, 1)
        self.edtEndDate = CDateEdit(AnaliticReportsGeneralInfoSurgeryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.cmbTimeDeliver = CStrComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbTimeDeliver.setObjectName(_fromUtf8("cmbTimeDeliver"))
        self.gridLayout.addWidget(self.cmbTimeDeliver, 8, 1, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 3)
        self.cmbEventType = CRBComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 4)
        self.cmbOrder = QtGui.QComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbOrder.setObjectName(_fromUtf8("cmbOrder"))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrder, 7, 1, 1, 4)
        self.lblEventType = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 10, 0, 1, 2)
        self.lblOrder = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblOrder.setObjectName(_fromUtf8("lblOrder"))
        self.gridLayout.addWidget(self.lblOrder, 7, 0, 1, 1)
        self.cmbDiseaseCharacter = CRBComboBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.cmbDiseaseCharacter.setObjectName(_fromUtf8("cmbDiseaseCharacter"))
        self.gridLayout.addWidget(self.cmbDiseaseCharacter, 6, 1, 1, 4)
        self.lblTimeDeliver = QtGui.QLabel(AnaliticReportsGeneralInfoSurgeryDialog)
        self.lblTimeDeliver.setObjectName(_fromUtf8("lblTimeDeliver"))
        self.gridLayout.addWidget(self.lblTimeDeliver, 8, 0, 1, 1)
        self.chkAdditionalMKB = QtGui.QCheckBox(AnaliticReportsGeneralInfoSurgeryDialog)
        self.chkAdditionalMKB.setObjectName(_fromUtf8("chkAdditionalMKB"))
        self.gridLayout.addWidget(self.chkAdditionalMKB, 5, 1, 1, 4)
        self.lblMKB.setBuddy(self.cmbMKBFilter)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(AnaliticReportsGeneralInfoSurgeryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AnaliticReportsGeneralInfoSurgeryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AnaliticReportsGeneralInfoSurgeryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnaliticReportsGeneralInfoSurgeryDialog)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.edtEndDate, self.cmbEventType)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbEventType, self.cmbOrgStructure)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbOrgStructure, self.cmbMKBFilter)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbMKBFilter, self.edtMKBFrom)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.edtMKBTo, self.chkAdditionalMKB)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.chkAdditionalMKB, self.cmbDiseaseCharacter)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbDiseaseCharacter, self.cmbOrder)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbOrder, self.cmbTimeDeliver)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.cmbTimeDeliver, self.chkIsGroupingOS)
        AnaliticReportsGeneralInfoSurgeryDialog.setTabOrder(self.chkIsGroupingOS, self.buttonBox)

    def retranslateUi(self, AnaliticReportsGeneralInfoSurgeryDialog):
        AnaliticReportsGeneralInfoSurgeryDialog.setWindowTitle(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "параметры отчёта", None))
        self.chkIsGroupingOS.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Группировка по подразделениям", None))
        self.lblMKB.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Коды диагнозов по &МКБ", None))
        self.lblBegDate.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Дата &начала периода", None))
        self.lblDiseaseCharacter.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Характер заболевания", None))
        self.edtMKBFrom.setInputMask(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Z99.9", None))
        self.lblOrgStructure.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "&Подразделение", None))
        self.edtBegDate.setDisplayFormat(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Дата &окончания периода", None))
        self.cmbMKBFilter.setItemText(0, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "Игнор.", None))
        self.cmbMKBFilter.setItemText(1, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "Интервал", None))
        self.edtEndDate.setDisplayFormat(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "dd.MM.yyyy", None))
        self.cmbOrder.setItemText(0, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "не задано", None))
        self.cmbOrder.setItemText(1, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "плановый", None))
        self.cmbOrder.setItemText(2, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "экстренный", None))
        self.cmbOrder.setItemText(3, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "самотёком", None))
        self.cmbOrder.setItemText(4, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "принудительный", None))
        self.cmbOrder.setItemText(5, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "внутренний перевод", None))
        self.cmbOrder.setItemText(6, _translate("AnaliticReportsGeneralInfoSurgeryDialog", "неотложная", None))
        self.lblEventType.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Тип события", None))
        self.lblOrder.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Порядок поступления", None))
        self.lblTimeDeliver.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "Срок доставки", None))
        self.chkAdditionalMKB.setText(_translate("AnaliticReportsGeneralInfoSurgeryDialog", "острые заболевания ЖКТ", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
from library.StrComboBox import CStrComboBox
from library.crbcombobox import CRBComboBox
