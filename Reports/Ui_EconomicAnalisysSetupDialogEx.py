# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\Reports\EconomicAnalisysSetupDialogEx.ui'
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

class Ui_EconomicAnalisysSetupDialogEx(object):
    def setupUi(self, EconomicAnalisysSetupDialogEx):
        EconomicAnalisysSetupDialogEx.setObjectName(_fromUtf8("EconomicAnalisysSetupDialogEx"))
        EconomicAnalisysSetupDialogEx.setWindowModality(QtCore.Qt.ApplicationModal)
        EconomicAnalisysSetupDialogEx.resize(422, 842)
        EconomicAnalisysSetupDialogEx.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(EconomicAnalisysSetupDialogEx)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(EconomicAnalisysSetupDialogEx)
        self.widget.setMinimumSize(QtCore.QSize(0, 20))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 16, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spnWomanAgeEnd = QtGui.QSpinBox(self.widget)
        self.spnWomanAgeEnd.setGeometry(QtCore.QRect(139, 0, 50, 20))
        self.spnWomanAgeEnd.setMinimumSize(QtCore.QSize(50, 0))
        self.spnWomanAgeEnd.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spnWomanAgeEnd.setMaximum(150)
        self.spnWomanAgeEnd.setProperty("value", 150)
        self.spnWomanAgeEnd.setObjectName(_fromUtf8("spnWomanAgeEnd"))
        self.lblAge2_2 = QtGui.QLabel(self.widget)
        self.lblAge2_2.setGeometry(QtCore.QRect(105, 0, 31, 20))
        self.lblAge2_2.setStyleSheet(_fromUtf8(""))
        self.lblAge2_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAge2_2.setObjectName(_fromUtf8("lblAge2_2"))
        self.cmbWomenEndAgeUnit = QtGui.QComboBox(self.widget)
        self.cmbWomenEndAgeUnit.setGeometry(QtCore.QRect(201, 0, 34, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbWomenEndAgeUnit.sizePolicy().hasHeightForWidth())
        self.cmbWomenEndAgeUnit.setSizePolicy(sizePolicy)
        self.cmbWomenEndAgeUnit.setObjectName(_fromUtf8("cmbWomenEndAgeUnit"))
        self.cmbWomenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenEndAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbWomenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenEndAgeUnit.addItem(_fromUtf8(""))
        self.spnWomanAgeBeg = QtGui.QSpinBox(self.widget)
        self.spnWomanAgeBeg.setGeometry(QtCore.QRect(10, 0, 50, 20))
        self.spnWomanAgeBeg.setMinimumSize(QtCore.QSize(50, 0))
        self.spnWomanAgeBeg.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spnWomanAgeBeg.setObjectName(_fromUtf8("spnWomanAgeBeg"))
        self.cmbWomenBegAgeUnit = QtGui.QComboBox(self.widget)
        self.cmbWomenBegAgeUnit.setGeometry(QtCore.QRect(69, 0, 34, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbWomenBegAgeUnit.sizePolicy().hasHeightForWidth())
        self.cmbWomenBegAgeUnit.setSizePolicy(sizePolicy)
        self.cmbWomenBegAgeUnit.setObjectName(_fromUtf8("cmbWomenBegAgeUnit"))
        self.cmbWomenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenBegAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbWomenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbWomenBegAgeUnit.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.widget, 20, 2, 1, 3)
        self.cmbtypePay = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbtypePay.setObjectName(_fromUtf8("cmbtypePay"))
        self.cmbtypePay.addItem(_fromUtf8(""))
        self.cmbtypePay.addItem(_fromUtf8(""))
        self.cmbtypePay.addItem(_fromUtf8(""))
        self.cmbtypePay.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbtypePay, 14, 2, 1, 3)
        self.edtEndDate = CDateEdit(EconomicAnalisysSetupDialogEx)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.cmbScheta = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbScheta.setObjectName(_fromUtf8("cmbScheta"))
        self.cmbScheta.addItem(_fromUtf8(""))
        self.cmbScheta.addItem(_fromUtf8(""))
        self.cmbScheta.addItem(_fromUtf8(""))
        self.cmbScheta.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbScheta, 4, 2, 1, 3)
        self.cmbPurpose = CRBComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbPurpose.setObjectName(_fromUtf8("cmbPurpose"))
        self.gridLayout.addWidget(self.cmbPurpose, 16, 2, 1, 3)
        self.lblBegDate = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 29, 1, 1, 1)
        self.lblPurpose = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblPurpose.setObjectName(_fromUtf8("lblPurpose"))
        self.gridLayout.addWidget(self.lblPurpose, 16, 0, 1, 1)
        self.chkDetail = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.chkDetail.setObjectName(_fromUtf8("chkDetail"))
        self.gridLayout.addWidget(self.chkDetail, 26, 2, 1, 3)
        self.lblSpeciality = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 7, 0, 1, 2)
        self.lblRazrNas = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblRazrNas.setObjectName(_fromUtf8("lblRazrNas"))
        self.gridLayout.addWidget(self.lblRazrNas, 13, 0, 1, 2)
        self.edtEndTime = QtGui.QTimeEdit(EconomicAnalisysSetupDialogEx)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        self.lblVidPom = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblVidPom.setObjectName(_fromUtf8("lblVidPom"))
        self.gridLayout.addWidget(self.lblVidPom, 12, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.ismancheckedage = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.ismancheckedage.setObjectName(_fromUtf8("ismancheckedage"))
        self.gridLayout.addWidget(self.ismancheckedage, 19, 0, 1, 1)
        self.lblFinance = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 10, 0, 1, 2)
        self.cmbProfileBed = CRBComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbProfileBed.setObjectName(_fromUtf8("cmbProfileBed"))
        self.gridLayout.addWidget(self.cmbProfileBed, 21, 2, 1, 3)
        self.chkPrintAccNumber = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.chkPrintAccNumber.setObjectName(_fromUtf8("chkPrintAccNumber"))
        self.gridLayout.addWidget(self.chkPrintAccNumber, 27, 2, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(EconomicAnalisysSetupDialogEx)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 8, 2, 1, 3)
        self.lblDetailTo = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblDetailTo.setObjectName(_fromUtf8("lblDetailTo"))
        self.gridLayout.addWidget(self.lblDetailTo, 22, 0, 1, 2)
        self.cmbDetailTo = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbDetailTo.setObjectName(_fromUtf8("cmbDetailTo"))
        self.gridLayout.addWidget(self.cmbDetailTo, 22, 2, 1, 3)
        self.cmbVidPom = CRBComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbVidPom.setObjectName(_fromUtf8("cmbVidPom"))
        self.gridLayout.addWidget(self.cmbVidPom, 12, 2, 1, 3)
        self.cbPrice = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.cbPrice.setObjectName(_fromUtf8("cbPrice"))
        self.gridLayout.addWidget(self.cbPrice, 24, 2, 1, 3)
        self.lbltypePay = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lbltypePay.setObjectName(_fromUtf8("lbltypePay"))
        self.gridLayout.addWidget(self.lbltypePay, 14, 0, 1, 2)
        self.lblPerson = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 8, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 17, 0, 1, 2)
        self.lblStepECO = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblStepECO.setObjectName(_fromUtf8("lblStepECO"))
        self.gridLayout.addWidget(self.lblStepECO, 18, 0, 1, 1)
        self.cmbPayer = COrgIsPayer23ComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbPayer.setObjectName(_fromUtf8("cmbPayer"))
        self.gridLayout.addWidget(self.cmbPayer, 15, 2, 1, 3)
        self.cmbSpeciality = CRBComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 7, 2, 1, 3)
        self.lblPayer = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblPayer.setObjectName(_fromUtf8("lblPayer"))
        self.gridLayout.addWidget(self.lblPayer, 15, 0, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 6, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 6, 2, 1, 3)
        self.iswomencheckedage = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.iswomencheckedage.setObjectName(_fromUtf8("iswomencheckedage"))
        self.gridLayout.addWidget(self.iswomencheckedage, 20, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.ageHolder = QtGui.QWidget(EconomicAnalisysSetupDialogEx)
        self.ageHolder.setMinimumSize(QtCore.QSize(0, 20))
        self.ageHolder.setObjectName(_fromUtf8("ageHolder"))
        self.spnManAgeBeg = QtGui.QSpinBox(self.ageHolder)
        self.spnManAgeBeg.setGeometry(QtCore.QRect(10, 0, 50, 20))
        self.spnManAgeBeg.setMinimumSize(QtCore.QSize(50, 0))
        self.spnManAgeBeg.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spnManAgeBeg.setObjectName(_fromUtf8("spnManAgeBeg"))
        self.spnManAgeEnd = QtGui.QSpinBox(self.ageHolder)
        self.spnManAgeEnd.setGeometry(QtCore.QRect(139, 0, 50, 20))
        self.spnManAgeEnd.setMinimumSize(QtCore.QSize(50, 0))
        self.spnManAgeEnd.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spnManAgeEnd.setMaximum(150)
        self.spnManAgeEnd.setProperty("value", 150)
        self.spnManAgeEnd.setObjectName(_fromUtf8("spnManAgeEnd"))
        self.lblAge2 = QtGui.QLabel(self.ageHolder)
        self.lblAge2.setGeometry(QtCore.QRect(105, 0, 31, 20))
        self.lblAge2.setStyleSheet(_fromUtf8(""))
        self.lblAge2.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAge2.setObjectName(_fromUtf8("lblAge2"))
        self.label = QtGui.QLabel(self.ageHolder)
        self.label.setGeometry(QtCore.QRect(1, 2, 16, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.cmbMenBegAgeUnit = QtGui.QComboBox(self.ageHolder)
        self.cmbMenBegAgeUnit.setGeometry(QtCore.QRect(69, 0, 34, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMenBegAgeUnit.sizePolicy().hasHeightForWidth())
        self.cmbMenBegAgeUnit.setSizePolicy(sizePolicy)
        self.cmbMenBegAgeUnit.setObjectName(_fromUtf8("cmbMenBegAgeUnit"))
        self.cmbMenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenBegAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbMenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenEndAgeUnit = QtGui.QComboBox(self.ageHolder)
        self.cmbMenEndAgeUnit.setGeometry(QtCore.QRect(201, 0, 34, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMenEndAgeUnit.sizePolicy().hasHeightForWidth())
        self.cmbMenEndAgeUnit.setSizePolicy(sizePolicy)
        self.cmbMenEndAgeUnit.setObjectName(_fromUtf8("cmbMenEndAgeUnit"))
        self.cmbMenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenEndAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbMenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbMenEndAgeUnit.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.ageHolder, 19, 2, 1, 3)
        self.grpdatetype = QtGui.QGroupBox(EconomicAnalisysSetupDialogEx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpdatetype.sizePolicy().hasHeightForWidth())
        self.grpdatetype.setSizePolicy(sizePolicy)
        self.grpdatetype.setFlat(False)
        self.grpdatetype.setObjectName(_fromUtf8("grpdatetype"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grpdatetype)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbDatalech = QtGui.QRadioButton(self.grpdatetype)
        self.rbDatalech.setChecked(True)
        self.rbDatalech.setObjectName(_fromUtf8("rbDatalech"))
        self.verticalLayout.addWidget(self.rbDatalech)
        self.rbSchetf = QtGui.QRadioButton(self.grpdatetype)
        self.rbSchetf.setObjectName(_fromUtf8("rbSchetf"))
        self.verticalLayout.addWidget(self.rbSchetf)
        self.rbNomer = QtGui.QRadioButton(self.grpdatetype)
        self.rbNomer.setObjectName(_fromUtf8("rbNomer"))
        self.verticalLayout.addWidget(self.rbNomer)
        self.rbNomer.raise_()
        self.rbDatalech.raise_()
        self.rbSchetf.raise_()
        self.gridLayout.addWidget(self.grpdatetype, 5, 0, 1, 5)
        self.cmbEventType = CRBMultivalueComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 17, 2, 1, 3)
        self.lblAccountType = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblAccountType.setObjectName(_fromUtf8("lblAccountType"))
        self.gridLayout.addWidget(self.lblAccountType, 3, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(EconomicAnalisysSetupDialogEx)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 30, 3, 1, 2)
        self.cmbRazrNas = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbRazrNas.setObjectName(_fromUtf8("cmbRazrNas"))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.cmbRazrNas.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbRazrNas, 13, 2, 1, 3)
        self.cmbNoscheta = CAccountComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbNoscheta.setObjectName(_fromUtf8("cmbNoscheta"))
        self.gridLayout.addWidget(self.cmbNoscheta, 2, 2, 1, 3)
        self.lblProfileBed = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblProfileBed.setObjectName(_fromUtf8("lblProfileBed"))
        self.gridLayout.addWidget(self.lblProfileBed, 21, 0, 1, 1)
        self.cmbStepECO = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbStepECO.setObjectName(_fromUtf8("cmbStepECO"))
        self.gridLayout.addWidget(self.cmbStepECO, 18, 2, 1, 3)
        self.cmbFinance = CRBComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 10, 2, 1, 3)
        self.edtBegTime = QtGui.QTimeEdit(EconomicAnalisysSetupDialogEx)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        self.cbusl = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.cbusl.setObjectName(_fromUtf8("cbusl"))
        self.gridLayout.addWidget(self.cbusl, 25, 2, 1, 1)
        self.edtFilterClientId = QtGui.QLineEdit(EconomicAnalisysSetupDialogEx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterClientId.sizePolicy().hasHeightForWidth())
        self.edtFilterClientId.setSizePolicy(sizePolicy)
        self.edtFilterClientId.setObjectName(_fromUtf8("edtFilterClientId"))
        self.gridLayout.addWidget(self.edtFilterClientId, 23, 2, 1, 2)
        self.btnFindClientInfo = QtGui.QToolButton(EconomicAnalisysSetupDialogEx)
        self.btnFindClientInfo.setObjectName(_fromUtf8("btnFindClientInfo"))
        self.gridLayout.addWidget(self.btnFindClientInfo, 23, 4, 1, 1)
        self.cmbContract = CARMSIndependentContractTreeFindComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.gridLayout.addWidget(self.cmbContract, 11, 2, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        self.edtBegDate = CDateEdit(EconomicAnalisysSetupDialogEx)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.lblNoscheta = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblNoscheta.setObjectName(_fromUtf8("lblNoscheta"))
        self.gridLayout.addWidget(self.lblNoscheta, 2, 0, 1, 2)
        self.cmbAccountType = QtGui.QComboBox(EconomicAnalisysSetupDialogEx)
        self.cmbAccountType.setObjectName(_fromUtf8("cmbAccountType"))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.cmbAccountType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAccountType, 3, 2, 1, 3)
        self.lblContract = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridLayout.addWidget(self.lblContract, 11, 0, 1, 1)
        self.lblScheta = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblScheta.setObjectName(_fromUtf8("lblScheta"))
        self.gridLayout.addWidget(self.lblScheta, 4, 0, 1, 2)
        self.lblClient = QtGui.QLabel(EconomicAnalisysSetupDialogEx)
        self.lblClient.setObjectName(_fromUtf8("lblClient"))
        self.gridLayout.addWidget(self.lblClient, 23, 0, 1, 1)
        self.cbCashPayments = QtGui.QCheckBox(EconomicAnalisysSetupDialogEx)
        self.cbCashPayments.setObjectName(_fromUtf8("cbCashPayments"))
        self.gridLayout.addWidget(self.cbCashPayments, 28, 2, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblPurpose.setBuddy(self.cmbPurpose)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblRazrNas.setBuddy(self.cmbRazrNas)
        self.lblVidPom.setBuddy(self.cmbVidPom)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblPayer.setBuddy(self.cmbPayer)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblAccountType.setBuddy(self.cmbAccountType)
        self.lblNoscheta.setBuddy(self.cmbNoscheta)
        self.lblContract.setBuddy(self.cmbOrgStructure)
        self.lblScheta.setBuddy(self.cmbScheta)

        self.retranslateUi(EconomicAnalisysSetupDialogEx)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EconomicAnalisysSetupDialogEx.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EconomicAnalisysSetupDialogEx.reject)
        QtCore.QMetaObject.connectSlotsByName(EconomicAnalisysSetupDialogEx)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.edtBegDate, self.edtBegTime)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.edtBegTime, self.edtEndDate)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.edtEndDate, self.edtEndTime)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.edtEndTime, self.cmbNoscheta)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbNoscheta, self.rbDatalech)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.rbDatalech, self.rbSchetf)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.rbSchetf, self.rbNomer)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.rbNomer, self.cmbOrgStructure)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbPerson, self.cmbFinance)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbFinance, self.cmbContract)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbContract, self.cmbVidPom)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbVidPom, self.cmbRazrNas)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbRazrNas, self.cmbPayer)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbPayer, self.cmbEventType)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbEventType, self.spnManAgeBeg)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.spnManAgeBeg, self.spnManAgeEnd)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.spnManAgeEnd, self.cmbProfileBed)
        EconomicAnalisysSetupDialogEx.setTabOrder(self.cmbProfileBed, self.buttonBox)

    def retranslateUi(self, EconomicAnalisysSetupDialogEx):
        EconomicAnalisysSetupDialogEx.setWindowTitle(_translate("EconomicAnalisysSetupDialogEx", "параметры отчёта", None))
        self.label_2.setText(_translate("EconomicAnalisysSetupDialogEx", "с", None))
        self.lblAge2_2.setText(_translate("EconomicAnalisysSetupDialogEx", "по", None))
        self.cmbWomenEndAgeUnit.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Д", None))
        self.cmbWomenEndAgeUnit.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Н", None))
        self.cmbWomenEndAgeUnit.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "М", None))
        self.cmbWomenEndAgeUnit.setItemText(4, _translate("EconomicAnalisysSetupDialogEx", "Г", None))
        self.cmbWomenBegAgeUnit.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Д", None))
        self.cmbWomenBegAgeUnit.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Н", None))
        self.cmbWomenBegAgeUnit.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "М", None))
        self.cmbWomenBegAgeUnit.setItemText(4, _translate("EconomicAnalisysSetupDialogEx", "Г", None))
        self.cmbtypePay.setItemText(0, _translate("EconomicAnalisysSetupDialogEx", "Не задано", None))
        self.cmbtypePay.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Наличная оплата", None))
        self.cmbtypePay.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Электронная оплата", None))
        self.cmbtypePay.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "Не учитывать факт оплаты", None))
        self.cmbScheta.setItemText(0, _translate("EconomicAnalisysSetupDialogEx", "Все", None))
        self.cmbScheta.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Представленные к оплате", None))
        self.cmbScheta.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Подлежащие к оплате", None))
        self.cmbScheta.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "Возвращенные из СМО", None))
        self.lblBegDate.setText(_translate("EconomicAnalisysSetupDialogEx", "Дата &начала периода", None))
        self.lblPurpose.setText(_translate("EconomicAnalisysSetupDialogEx", "Назначение", None))
        self.chkDetail.setText(_translate("EconomicAnalisysSetupDialogEx", "&Детализировать по плательщикам", None))
        self.lblSpeciality.setText(_translate("EconomicAnalisysSetupDialogEx", "&Специальность", None))
        self.lblRazrNas.setText(_translate("EconomicAnalisysSetupDialogEx", "В разрезе населения", None))
        self.lblVidPom.setText(_translate("EconomicAnalisysSetupDialogEx", "Вид помощи", None))
        self.lblEndDate.setText(_translate("EconomicAnalisysSetupDialogEx", "Дата &окончания периода", None))
        self.ismancheckedage.setText(_translate("EconomicAnalisysSetupDialogEx", "Мужчины", None))
        self.lblFinance.setText(_translate("EconomicAnalisysSetupDialogEx", "Тип финансирования", None))
        self.chkPrintAccNumber.setText(_translate("EconomicAnalisysSetupDialogEx", "&Вывод номера счета", None))
        self.lblDetailTo.setText(_translate("EconomicAnalisysSetupDialogEx", "Детализировать по", None))
        self.cbPrice.setText(_translate("EconomicAnalisysSetupDialogEx", "Не учитывать услуги с нулевой ценой", None))
        self.lbltypePay.setText(_translate("EconomicAnalisysSetupDialogEx", "Тип оплаты", None))
        self.lblPerson.setText(_translate("EconomicAnalisysSetupDialogEx", "&Врач", None))
        self.lblEventType.setText(_translate("EconomicAnalisysSetupDialogEx", "Тип события", None))
        self.lblStepECO.setText(_translate("EconomicAnalisysSetupDialogEx", "Этап ЭКО", None))
        self.cmbSpeciality.setWhatsThis(_translate("EconomicAnalisysSetupDialogEx", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblPayer.setText(_translate("EconomicAnalisysSetupDialogEx", "Плательщик", None))
        self.lblOrgStructure.setText(_translate("EconomicAnalisysSetupDialogEx", "&Подразделение", None))
        self.iswomencheckedage.setText(_translate("EconomicAnalisysSetupDialogEx", "Женщины", None))
        self.lblAge2.setText(_translate("EconomicAnalisysSetupDialogEx", "по", None))
        self.label.setText(_translate("EconomicAnalisysSetupDialogEx", "с", None))
        self.cmbMenBegAgeUnit.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Д", None))
        self.cmbMenBegAgeUnit.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Н", None))
        self.cmbMenBegAgeUnit.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "М", None))
        self.cmbMenBegAgeUnit.setItemText(4, _translate("EconomicAnalisysSetupDialogEx", "Г", None))
        self.cmbMenEndAgeUnit.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Д", None))
        self.cmbMenEndAgeUnit.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Н", None))
        self.cmbMenEndAgeUnit.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "М", None))
        self.cmbMenEndAgeUnit.setItemText(4, _translate("EconomicAnalisysSetupDialogEx", "Г", None))
        self.grpdatetype.setTitle(_translate("EconomicAnalisysSetupDialogEx", "Формировать отчет по", None))
        self.rbDatalech.setText(_translate("EconomicAnalisysSetupDialogEx", "Дате окончания лечения", None))
        self.rbSchetf.setText(_translate("EconomicAnalisysSetupDialogEx", "Дате счет-фактуры", None))
        self.rbNomer.setText(_translate("EconomicAnalisysSetupDialogEx", "Номеру счета", None))
        self.lblAccountType.setText(_translate("EconomicAnalisysSetupDialogEx", "Типы реестров", None))
        self.cmbRazrNas.setItemText(0, _translate("EconomicAnalisysSetupDialogEx", "Все", None))
        self.cmbRazrNas.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Краевые", None))
        self.cmbRazrNas.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Инокраевые", None))
        self.lblProfileBed.setText(_translate("EconomicAnalisysSetupDialogEx", "Профиль", None))
        self.cbusl.setText(_translate("EconomicAnalisysSetupDialogEx", "вывод услуг", None))
        self.btnFindClientInfo.setText(_translate("EconomicAnalisysSetupDialogEx", "...", None))
        self.lblNoscheta.setText(_translate("EconomicAnalisysSetupDialogEx", "Номер счета", None))
        self.cmbAccountType.setItemText(0, _translate("EconomicAnalisysSetupDialogEx", "не задано", None))
        self.cmbAccountType.setItemText(1, _translate("EconomicAnalisysSetupDialogEx", "Только Основные", None))
        self.cmbAccountType.setItemText(2, _translate("EconomicAnalisysSetupDialogEx", "Основные + Дополнительные", None))
        self.cmbAccountType.setItemText(3, _translate("EconomicAnalisysSetupDialogEx", "Только Повторные", None))
        self.lblContract.setText(_translate("EconomicAnalisysSetupDialogEx", "&Договор", None))
        self.lblScheta.setText(_translate("EconomicAnalisysSetupDialogEx", "Признак оплаты", None))
        self.lblClient.setText(_translate("EconomicAnalisysSetupDialogEx", "Пациент", None))
        self.cbCashPayments.setText(_translate("EconomicAnalisysSetupDialogEx", "Оплата по кассовому аппарату", None))

from Accounting.AccountComboBox import CAccountComboBox
from Orgs.ContractFindComboBox import CARMSIndependentContractTreeFindComboBox
from Orgs.OrgComboBox import COrgIsPayer23ComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.MultivalueComboBox import CRBMultivalueComboBox
from library.crbcombobox import CRBComboBox
