# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportAcuteInfectionsAbleSetup.ui'
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

class Ui_ReportAcuteInfectionsAbleSetupDialog(object):
    def setupUi(self, ReportAcuteInfectionsAbleSetupDialog):
        ReportAcuteInfectionsAbleSetupDialog.setObjectName(_fromUtf8("ReportAcuteInfectionsAbleSetupDialog"))
        ReportAcuteInfectionsAbleSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportAcuteInfectionsAbleSetupDialog.resize(466, 867)
        ReportAcuteInfectionsAbleSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportAcuteInfectionsAbleSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbPersonPost = QtGui.QComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbPersonPost.setObjectName(_fromUtf8("cmbPersonPost"))
        self.cmbPersonPost.addItem(_fromUtf8(""))
        self.cmbPersonPost.addItem(_fromUtf8(""))
        self.cmbPersonPost.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPersonPost, 9, 1, 1, 3)
        self.cmbEventPurpose = CRBComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 2, 1, 1, 3)
        self.frmAge = QtGui.QFrame(ReportAcuteInfectionsAbleSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 11, 1, 1, 3)
        self.lblArea = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblArea.setObjectName(_fromUtf8("lblArea"))
        self.gridLayout.addWidget(self.lblArea, 15, 0, 1, 1)
        self.cmbFilterAddressStreet = CStreetComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbFilterAddressStreet.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterAddressStreet.sizePolicy().hasHeightForWidth())
        self.cmbFilterAddressStreet.setSizePolicy(sizePolicy)
        self.cmbFilterAddressStreet.setObjectName(_fromUtf8("cmbFilterAddressStreet"))
        self.gridLayout.addWidget(self.cmbFilterAddressStreet, 25, 1, 1, 3)
        self.frmMKB = QtGui.QFrame(ReportAcuteInfectionsAbleSetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self.gridlayout = QtGui.QGridLayout(self.frmMKB)
        self.gridlayout.setMargin(0)
        self.gridlayout.setHorizontalSpacing(4)
        self.gridlayout.setVerticalSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.cmbMKBFilter = QtGui.QComboBox(self.frmMKB)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbMKBFilter, 0, 0, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(self.frmMKB)
        self.edtMKBFrom.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBFrom.setSizePolicy(sizePolicy)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBFrom.setMaxLength(6)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridlayout.addWidget(self.edtMKBFrom, 0, 1, 1, 1)
        self.edtMKBTo = CICDCodeEdit(self.frmMKB)
        self.edtMKBTo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBTo.sizePolicy().hasHeightForWidth())
        self.edtMKBTo.setSizePolicy(sizePolicy)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBTo.setMaxLength(6)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridlayout.addWidget(self.edtMKBTo, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frmMKB, 16, 1, 1, 3)
        self.cmbSpeciality = CRBComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 7, 1, 1, 3)
        self.lblEventType = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 3, 0, 1, 1)
        self.frmMKBEx = QtGui.QFrame(ReportAcuteInfectionsAbleSetupDialog)
        self.frmMKBEx.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKBEx.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKBEx.setObjectName(_fromUtf8("frmMKBEx"))
        self._2 = QtGui.QGridLayout(self.frmMKBEx)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.cmbMKBExFilter = QtGui.QComboBox(self.frmMKBEx)
        self.cmbMKBExFilter.setObjectName(_fromUtf8("cmbMKBExFilter"))
        self.cmbMKBExFilter.addItem(_fromUtf8(""))
        self.cmbMKBExFilter.addItem(_fromUtf8(""))
        self._2.addWidget(self.cmbMKBExFilter, 0, 0, 1, 1)
        self.edtMKBExFrom = CICDCodeEdit(self.frmMKBEx)
        self.edtMKBExFrom.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBExFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBExFrom.setSizePolicy(sizePolicy)
        self.edtMKBExFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBExFrom.setMaxLength(6)
        self.edtMKBExFrom.setObjectName(_fromUtf8("edtMKBExFrom"))
        self._2.addWidget(self.edtMKBExFrom, 0, 1, 1, 1)
        self.edtMKBExTo = CICDCodeEdit(self.frmMKBEx)
        self.edtMKBExTo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBExTo.sizePolicy().hasHeightForWidth())
        self.edtMKBExTo.setSizePolicy(sizePolicy)
        self.edtMKBExTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBExTo.setMaxLength(6)
        self.edtMKBExTo.setObjectName(_fromUtf8("edtMKBExTo"))
        self._2.addWidget(self.edtMKBExTo, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frmMKBEx, 17, 1, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 5, 0, 1, 1)
        self.lblEventTypeDD = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblEventTypeDD.setObjectName(_fromUtf8("lblEventTypeDD"))
        self.gridLayout.addWidget(self.lblEventTypeDD, 28, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPerson, 8, 1, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 5, 1, 1, 3)
        self.chkOnlyFirstTime = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkOnlyFirstTime.setObjectName(_fromUtf8("chkOnlyFirstTime"))
        self.gridLayout.addWidget(self.chkOnlyFirstTime, 19, 1, 1, 3)
        self.chkFilterAddress = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkFilterAddress.setObjectName(_fromUtf8("chkFilterAddress"))
        self.gridLayout.addWidget(self.chkFilterAddress, 23, 0, 1, 1)
        self.lblOrgStructureList = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblOrgStructureList.setWordWrap(True)
        self.lblOrgStructureList.setObjectName(_fromUtf8("lblOrgStructureList"))
        self.gridLayout.addWidget(self.lblOrgStructureList, 6, 1, 1, 3)
        self.chkNotNullTraumaType = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkNotNullTraumaType.setObjectName(_fromUtf8("chkNotNullTraumaType"))
        self.gridLayout.addWidget(self.chkNotNullTraumaType, 20, 1, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 10, 2, 1, 2)
        self.lblPersonPost = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblPersonPost.setObjectName(_fromUtf8("lblPersonPost"))
        self.gridLayout.addWidget(self.lblPersonPost, 9, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)
        self.edtEndDate = CDateEdit(ReportAcuteInfectionsAbleSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.lblSocStatusClass = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblSocStatusClass.setObjectName(_fromUtf8("lblSocStatusClass"))
        self.gridLayout.addWidget(self.lblSocStatusClass, 12, 0, 1, 1)
        self.lblMKBEx = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblMKBEx.setObjectName(_fromUtf8("lblMKBEx"))
        self.gridLayout.addWidget(self.lblMKBEx, 17, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportAcuteInfectionsAbleSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 32, 0, 1, 4)
        self.lblMKB = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 16, 0, 1, 1)
        self.cmbFilterAddressCity = CKLADRComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbFilterAddressCity.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterAddressCity.sizePolicy().hasHeightForWidth())
        self.cmbFilterAddressCity.setSizePolicy(sizePolicy)
        self.cmbFilterAddressCity.setObjectName(_fromUtf8("cmbFilterAddressCity"))
        self.gridLayout.addWidget(self.cmbFilterAddressCity, 24, 1, 1, 3)
        self.lblPerson = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 8, 0, 1, 1)
        self.cmbArea = COrgStructureComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbArea.setEnabled(False)
        self.cmbArea.setObjectName(_fromUtf8("cmbArea"))
        self.gridLayout.addWidget(self.cmbArea, 15, 1, 1, 3)
        self.chkRegisteredInPeriod = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkRegisteredInPeriod.setObjectName(_fromUtf8("chkRegisteredInPeriod"))
        self.gridLayout.addWidget(self.chkRegisteredInPeriod, 21, 1, 1, 3)
        self.cmbEventTypeDD = CRBComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbEventTypeDD.setObjectName(_fromUtf8("cmbEventTypeDD"))
        self.gridLayout.addWidget(self.cmbEventTypeDD, 28, 1, 1, 3)
        self.lblEndDate = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.cmbFilterAddressType = QtGui.QComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbFilterAddressType.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFilterAddressType.sizePolicy().hasHeightForWidth())
        self.cmbFilterAddressType.setSizePolicy(sizePolicy)
        self.cmbFilterAddressType.setObjectName(_fromUtf8("cmbFilterAddressType"))
        self.cmbFilterAddressType.addItem(_fromUtf8(""))
        self.cmbFilterAddressType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbFilterAddressType, 23, 1, 1, 3)
        self.edtBegDate = CDateEdit(ReportAcuteInfectionsAbleSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblSocStatusType = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblSocStatusType.setObjectName(_fromUtf8("lblSocStatusType"))
        self.gridLayout.addWidget(self.lblSocStatusType, 13, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(129, 131, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 31, 0, 1, 1)
        self.cmbEventType = CRBComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 3, 1, 1, 3)
        self.lblEventPurpose = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 2, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 10, 1, 1, 1)
        self.chkArea = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkArea.setObjectName(_fromUtf8("chkArea"))
        self.gridLayout.addWidget(self.chkArea, 14, 1, 1, 3)
        self.lblEventTypeList = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblEventTypeList.setWordWrap(True)
        self.lblEventTypeList.setObjectName(_fromUtf8("lblEventTypeList"))
        self.gridLayout.addWidget(self.lblEventTypeList, 4, 1, 1, 3)
        self.lblBegDate = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblLocality = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblLocality.setObjectName(_fromUtf8("lblLocality"))
        self.gridLayout.addWidget(self.lblLocality, 22, 0, 1, 1)
        self.btnOrgStructureList = QtGui.QPushButton(ReportAcuteInfectionsAbleSetupDialog)
        self.btnOrgStructureList.setObjectName(_fromUtf8("btnOrgStructureList"))
        self.gridLayout.addWidget(self.btnOrgStructureList, 6, 0, 1, 1)
        self.cmbSocStatusClass = CSocStatusComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbSocStatusClass.setObjectName(_fromUtf8("cmbSocStatusClass"))
        self.gridLayout.addWidget(self.cmbSocStatusClass, 12, 1, 1, 3)
        self.lblSex = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 10, 0, 1, 1)
        self.cmbLocality = QtGui.QComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbLocality.setObjectName(_fromUtf8("cmbLocality"))
        self.cmbLocality.addItem(_fromUtf8(""))
        self.cmbLocality.addItem(_fromUtf8(""))
        self.cmbLocality.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbLocality, 22, 1, 1, 3)
        self.cmbFilterAddressOrgStructureType = QtGui.QComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbFilterAddressOrgStructureType.setEnabled(False)
        self.cmbFilterAddressOrgStructureType.setObjectName(_fromUtf8("cmbFilterAddressOrgStructureType"))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbFilterAddressOrgStructureType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbFilterAddressOrgStructureType, 29, 1, 1, 3)
        self.cmbSocStatusType = CRBComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbSocStatusType.setObjectName(_fromUtf8("cmbSocStatusType"))
        self.gridLayout.addWidget(self.cmbSocStatusType, 13, 1, 1, 3)
        self.chkAccountAccomp = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkAccountAccomp.setObjectName(_fromUtf8("chkAccountAccomp"))
        self.gridLayout.addWidget(self.chkAccountAccomp, 18, 1, 1, 3)
        spacerItem5 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 3, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.lblFilterAddressHouse = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblFilterAddressHouse.setEnabled(False)
        self.lblFilterAddressHouse.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblFilterAddressHouse.setObjectName(_fromUtf8("lblFilterAddressHouse"))
        self.horizontalLayout_6.addWidget(self.lblFilterAddressHouse)
        self.edtFilterAddressHouse = QtGui.QLineEdit(ReportAcuteInfectionsAbleSetupDialog)
        self.edtFilterAddressHouse.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterAddressHouse.sizePolicy().hasHeightForWidth())
        self.edtFilterAddressHouse.setSizePolicy(sizePolicy)
        self.edtFilterAddressHouse.setObjectName(_fromUtf8("edtFilterAddressHouse"))
        self.horizontalLayout_6.addWidget(self.edtFilterAddressHouse)
        self.lblFilterAddressCorpus = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblFilterAddressCorpus.setEnabled(False)
        self.lblFilterAddressCorpus.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblFilterAddressCorpus.setObjectName(_fromUtf8("lblFilterAddressCorpus"))
        self.horizontalLayout_6.addWidget(self.lblFilterAddressCorpus)
        self.edtFilterAddressCorpus = QtGui.QLineEdit(ReportAcuteInfectionsAbleSetupDialog)
        self.edtFilterAddressCorpus.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterAddressCorpus.sizePolicy().hasHeightForWidth())
        self.edtFilterAddressCorpus.setSizePolicy(sizePolicy)
        self.edtFilterAddressCorpus.setObjectName(_fromUtf8("edtFilterAddressCorpus"))
        self.horizontalLayout_6.addWidget(self.edtFilterAddressCorpus)
        self.lblFilterAddressFlat = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblFilterAddressFlat.setEnabled(False)
        self.lblFilterAddressFlat.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblFilterAddressFlat.setObjectName(_fromUtf8("lblFilterAddressFlat"))
        self.horizontalLayout_6.addWidget(self.lblFilterAddressFlat)
        self.edtFilterAddressFlat = QtGui.QLineEdit(ReportAcuteInfectionsAbleSetupDialog)
        self.edtFilterAddressFlat.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterAddressFlat.sizePolicy().hasHeightForWidth())
        self.edtFilterAddressFlat.setSizePolicy(sizePolicy)
        self.edtFilterAddressFlat.setObjectName(_fromUtf8("edtFilterAddressFlat"))
        self.horizontalLayout_6.addWidget(self.edtFilterAddressFlat)
        self.gridLayout.addLayout(self.horizontalLayout_6, 26, 1, 1, 3)
        self.lblSpeciality = QtGui.QLabel(ReportAcuteInfectionsAbleSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 7, 0, 1, 1)
        self.btnEventTypeList = QtGui.QPushButton(ReportAcuteInfectionsAbleSetupDialog)
        self.btnEventTypeList.setObjectName(_fromUtf8("btnEventTypeList"))
        self.gridLayout.addWidget(self.btnEventTypeList, 4, 0, 1, 1)
        self.cmbFilterAddressOrgStructure = COrgStructureComboBox(ReportAcuteInfectionsAbleSetupDialog)
        self.cmbFilterAddressOrgStructure.setEnabled(False)
        self.cmbFilterAddressOrgStructure.setObjectName(_fromUtf8("cmbFilterAddressOrgStructure"))
        self.gridLayout.addWidget(self.cmbFilterAddressOrgStructure, 30, 1, 1, 3)
        self.chkFilterAddressOrgStructure = QtGui.QCheckBox(ReportAcuteInfectionsAbleSetupDialog)
        self.chkFilterAddressOrgStructure.setObjectName(_fromUtf8("chkFilterAddressOrgStructure"))
        self.gridLayout.addWidget(self.chkFilterAddressOrgStructure, 29, 0, 1, 1)
        self.lblArea.setBuddy(self.cmbArea)
        self.lblEventTypeDD.setBuddy(self.cmbEventTypeDD)
        self.lblSocStatusClass.setBuddy(self.cmbSocStatusClass)
        self.lblMKBEx.setBuddy(self.cmbMKBExFilter)
        self.lblMKB.setBuddy(self.cmbMKBFilter)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblSocStatusType.setBuddy(self.cmbSocStatusType)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblLocality.setBuddy(self.cmbLocality)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblFilterAddressHouse.setBuddy(self.edtFilterAddressHouse)
        self.lblFilterAddressCorpus.setBuddy(self.edtFilterAddressCorpus)
        self.lblFilterAddressFlat.setBuddy(self.edtFilterAddressFlat)

        self.retranslateUi(ReportAcuteInfectionsAbleSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportAcuteInfectionsAbleSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportAcuteInfectionsAbleSetupDialog.reject)
        QtCore.QObject.connect(self.chkArea, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbArea.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterAddressType.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterAddressCity.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterAddressStreet.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterAddressHouse.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterAddressCorpus.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterAddressFlat.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblFilterAddressHouse.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblFilterAddressCorpus.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddress, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblFilterAddressFlat.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddressOrgStructure, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterAddressOrgStructureType.setEnabled)
        QtCore.QObject.connect(self.chkFilterAddressOrgStructure, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterAddressOrgStructure.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ReportAcuteInfectionsAbleSetupDialog)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtEndDate, self.cmbEventPurpose)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbEventType, self.btnEventTypeList)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.btnEventTypeList, self.cmbOrgStructure)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbOrgStructure, self.btnOrgStructureList)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.btnOrgStructureList, self.cmbPerson)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbPerson, self.cmbPersonPost)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbPersonPost, self.cmbSex)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbSex, self.cmbSpeciality)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbSocStatusClass)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbSocStatusClass, self.cmbSocStatusType)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbSocStatusType, self.chkArea)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkArea, self.cmbArea)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbArea, self.cmbMKBFilter)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbMKBFilter, self.edtMKBFrom)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtMKBTo, self.cmbMKBExFilter)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbMKBExFilter, self.edtMKBExFrom)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtMKBExFrom, self.edtMKBExTo)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtMKBExTo, self.chkAccountAccomp)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkAccountAccomp, self.chkOnlyFirstTime)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkOnlyFirstTime, self.chkNotNullTraumaType)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkNotNullTraumaType, self.chkRegisteredInPeriod)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkRegisteredInPeriod, self.cmbLocality)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbLocality, self.chkFilterAddress)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.chkFilterAddress, self.cmbFilterAddressType)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbFilterAddressType, self.cmbFilterAddressCity)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbFilterAddressCity, self.cmbFilterAddressStreet)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbFilterAddressStreet, self.edtFilterAddressHouse)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtFilterAddressHouse, self.edtFilterAddressCorpus)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtFilterAddressCorpus, self.edtFilterAddressFlat)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.edtFilterAddressFlat, self.cmbEventTypeDD)
        ReportAcuteInfectionsAbleSetupDialog.setTabOrder(self.cmbEventTypeDD, self.buttonBox)

    def retranslateUi(self, ReportAcuteInfectionsAbleSetupDialog):
        ReportAcuteInfectionsAbleSetupDialog.setWindowTitle(_translate("ReportAcuteInfectionsAbleSetupDialog", "параметры отчёта", None))
        self.cmbPersonPost.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Не задано", None))
        self.cmbPersonPost.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Врачи", None))
        self.cmbPersonPost.setItemText(2, _translate("ReportAcuteInfectionsAbleSetupDialog", "Средний медицинский персонал", None))
        self.lblArea.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Те&рритория", None))
        self.cmbMKBFilter.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Игнор.", None))
        self.cmbMKBFilter.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Интервал", None))
        self.edtMKBFrom.setInputMask(_translate("ReportAcuteInfectionsAbleSetupDialog", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("ReportAcuteInfectionsAbleSetupDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Z99.9", None))
        self.lblEventType.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип обращения", None))
        self.cmbMKBExFilter.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Игнор.", None))
        self.cmbMKBExFilter.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Интервал", None))
        self.edtMKBExFrom.setInputMask(_translate("ReportAcuteInfectionsAbleSetupDialog", "a00.00; ", None))
        self.edtMKBExFrom.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "A.", None))
        self.edtMKBExTo.setInputMask(_translate("ReportAcuteInfectionsAbleSetupDialog", "a00.00; ", None))
        self.edtMKBExTo.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Z99.9", None))
        self.lblOrgStructure.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Подразделение", None))
        self.lblEventTypeDD.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип обращения для ДД", None))
        self.cmbPerson.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Врач", None))
        self.chkOnlyFirstTime.setToolTip(_translate("ReportAcuteInfectionsAbleSetupDialog", "Значение может отличаться от значения \"впервые\" ф.12", None))
        self.chkOnlyFirstTime.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Зарегистрированные в период впервые", None))
        self.chkFilterAddress.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Адрес", None))
        self.lblOrgStructureList.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Не задано", None))
        self.chkNotNullTraumaType.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип травмы указан", None))
        self.lblPersonPost.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип персонала", None))
        self.lblSocStatusClass.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Класс соц.статуса", None))
        self.lblMKBEx.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "В сочетании с", None))
        self.lblMKB.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Коды диагнозов по &МКБ", None))
        self.lblPerson.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "&Врач", None))
        self.chkRegisteredInPeriod.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Зарегистрированные в период", None))
        self.lblEndDate.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Дата &окончания периода", None))
        self.cmbFilterAddressType.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Регистрации", None))
        self.cmbFilterAddressType.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Проживания", None))
        self.lblSocStatusType.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип соц.статуса", None))
        self.lblEventPurpose.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "&Назначение обращения", None))
        self.cmbSex.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("ReportAcuteInfectionsAbleSetupDialog", "Ж", None))
        self.chkArea.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Учитывать адрес", None))
        self.lblEventTypeList.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Не задано", None))
        self.lblBegDate.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Дата &начала периода", None))
        self.lblLocality.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Местность", None))
        self.btnOrgStructureList.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Подразделение", None))
        self.lblSex.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "По&л", None))
        self.cmbLocality.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Не учитывать", None))
        self.cmbLocality.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Городские жители", None))
        self.cmbLocality.setItemText(2, _translate("ReportAcuteInfectionsAbleSetupDialog", "Сельские жители", None))
        self.cmbFilterAddressOrgStructureType.setItemText(0, _translate("ReportAcuteInfectionsAbleSetupDialog", "Регистрация", None))
        self.cmbFilterAddressOrgStructureType.setItemText(1, _translate("ReportAcuteInfectionsAbleSetupDialog", "Проживание", None))
        self.cmbFilterAddressOrgStructureType.setItemText(2, _translate("ReportAcuteInfectionsAbleSetupDialog", "Регистрация или проживание", None))
        self.cmbFilterAddressOrgStructureType.setItemText(3, _translate("ReportAcuteInfectionsAbleSetupDialog", "Прикрепление", None))
        self.cmbFilterAddressOrgStructureType.setItemText(4, _translate("ReportAcuteInfectionsAbleSetupDialog", "Регистрация или прикрепление", None))
        self.cmbFilterAddressOrgStructureType.setItemText(5, _translate("ReportAcuteInfectionsAbleSetupDialog", "Проживание или прикрепление", None))
        self.cmbFilterAddressOrgStructureType.setItemText(6, _translate("ReportAcuteInfectionsAbleSetupDialog", "Регистрация, проживание или прикрепление", None))
        self.chkAccountAccomp.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Учитывать сопутствующие", None))
        self.lblFilterAddressHouse.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Дом", None))
        self.lblFilterAddressCorpus.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Корп", None))
        self.lblFilterAddressFlat.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Кв", None))
        self.lblSpeciality.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Специальность", None))
        self.btnEventTypeList.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "Тип обращения", None))
        self.chkFilterAddressOrgStructure.setText(_translate("ReportAcuteInfectionsAbleSetupDialog", "По участку", None))

from KLADR.kladrComboxes import CKLADRComboBox, CStreetComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Registry.SocStatusComboBox import CSocStatusComboBox
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
from library.crbcombobox import CRBComboBox
