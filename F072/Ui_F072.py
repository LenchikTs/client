# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\F072\F072.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1191, 878)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_5 = QtGui.QGridLayout(Dialog)
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.splitter_3 = QtGui.QSplitter(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.txtClientInfoBrowser = CTextBrowser(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.txtClientInfoBrowser.sizePolicy().hasHeightForWidth())
        self.txtClientInfoBrowser.setSizePolicy(sizePolicy)
        self.txtClientInfoBrowser.setMinimumSize(QtCore.QSize(0, 0))
        self.txtClientInfoBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txtClientInfoBrowser.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.scrollArea = QtGui.QScrollArea(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1181, 723))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_4 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tabWidget = QtGui.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabToken = QtGui.QWidget()
        self.tabToken.setObjectName(_fromUtf8("tabToken"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabToken)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter_2 = QtGui.QSplitter(self.tabToken)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.frameBaseAndDiagnosises = QtGui.QFrame(self.splitter_2)
        self.frameBaseAndDiagnosises.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameBaseAndDiagnosises.setFrameShadow(QtGui.QFrame.Raised)
        self.frameBaseAndDiagnosises.setObjectName(_fromUtf8("frameBaseAndDiagnosises"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frameBaseAndDiagnosises)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.grpBase = QtGui.QGroupBox(self.frameBaseAndDiagnosises)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpBase.sizePolicy().hasHeightForWidth())
        self.grpBase.setSizePolicy(sizePolicy)
        self.grpBase.setObjectName(_fromUtf8("grpBase"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpBase)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btnExecPersonList = QtGui.QToolButton(self.grpBase)
        self.btnExecPersonList.setObjectName(_fromUtf8("btnExecPersonList"))
        self.gridLayout_2.addWidget(self.btnExecPersonList, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 15, 0, 1, 2)
        self.cmbContract = CContractComboBox(self.grpBase)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.cmbContract.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbContract, 0, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout_2.addWidget(self.lblBegDate, 1, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout_2.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.lblDuration = QtGui.QLabel(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDuration.sizePolicy().hasHeightForWidth())
        self.lblDuration.setSizePolicy(sizePolicy)
        self.lblDuration.setObjectName(_fromUtf8("lblDuration"))
        self.gridLayout_2.addWidget(self.lblDuration, 3, 0, 1, 1)
        self.lblDurationValue = QtGui.QLabel(self.grpBase)
        self.lblDurationValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblDurationValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblDurationValue.setObjectName(_fromUtf8("lblDurationValue"))
        self.gridLayout_2.addWidget(self.lblDurationValue, 3, 1, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(self.grpBase)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbPerson, 6, 0, 1, 2)
        self.chkPrimary = QtGui.QCheckBox(self.grpBase)
        self.chkPrimary.setObjectName(_fromUtf8("chkPrimary"))
        self.gridLayout_2.addWidget(self.chkPrimary, 7, 0, 1, 1)
        self.lblOrder = QtGui.QLabel(self.grpBase)
        self.lblOrder.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblOrder.setObjectName(_fromUtf8("lblOrder"))
        self.gridLayout_2.addWidget(self.lblOrder, 7, 1, 1, 1)
        self.lblResult = QtGui.QLabel(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblResult.sizePolicy().hasHeightForWidth())
        self.lblResult.setSizePolicy(sizePolicy)
        self.lblResult.setObjectName(_fromUtf8("lblResult"))
        self.gridLayout_2.addWidget(self.lblResult, 10, 0, 1, 2)
        self.cmbResult = CRBComboBox(self.grpBase)
        self.cmbResult.setObjectName(_fromUtf8("cmbResult"))
        self.cmbResult.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbResult, 11, 0, 1, 2)
        self.frame_2 = QtGui.QFrame(self.grpBase)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.edtBegDate = CDateEdit(self.frame_2)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout_2.addWidget(self.edtBegDate)
        self.edtBegTime = QtGui.QTimeEdit(self.frame_2)
        self.edtBegTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtBegTime.setCalendarPopup(False)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.horizontalLayout_2.addWidget(self.edtBegTime)
        self.gridLayout_2.addWidget(self.frame_2, 1, 1, 1, 1)
        self.frame_3 = QtGui.QFrame(self.grpBase)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.edtEndDate = CDateEdit(self.frame_3)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout_3.addWidget(self.edtEndDate)
        self.edtEndTime = QtGui.QTimeEdit(self.frame_3)
        self.edtEndTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtEndTime.setCalendarPopup(False)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.horizontalLayout_3.addWidget(self.edtEndTime)
        self.gridLayout_2.addWidget(self.frame_3, 2, 1, 1, 1)
        self.cmbOrder = CROComboBox(self.grpBase)
        self.cmbOrder.setObjectName(_fromUtf8("cmbOrder"))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbOrder, 8, 0, 1, 2)
        self.lblPregnancyWeek = QtGui.QLabel(self.grpBase)
        self.lblPregnancyWeek.setObjectName(_fromUtf8("lblPregnancyWeek"))
        self.gridLayout_2.addWidget(self.lblPregnancyWeek, 9, 0, 1, 1)
        self.edtPregnancyWeek = QtGui.QSpinBox(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPregnancyWeek.sizePolicy().hasHeightForWidth())
        self.edtPregnancyWeek.setSizePolicy(sizePolicy)
        self.edtPregnancyWeek.setMaximum(44)
        self.edtPregnancyWeek.setObjectName(_fromUtf8("edtPregnancyWeek"))
        self.gridLayout_2.addWidget(self.edtPregnancyWeek, 9, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(self.grpBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPerson.sizePolicy().hasHeightForWidth())
        self.lblPerson.setSizePolicy(sizePolicy)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout_2.addWidget(self.lblPerson, 5, 0, 1, 1)
        self.line = QtGui.QFrame(self.grpBase)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 12, 0, 1, 2)
        self.lblClientRelationConsents = QtGui.QLabel(self.grpBase)
        self.lblClientRelationConsents.setObjectName(_fromUtf8("lblClientRelationConsents"))
        self.gridLayout_2.addWidget(self.lblClientRelationConsents, 13, 0, 1, 1)
        self.cmbClientRelationConsents = CClientRelationComboBoxPatron(self.grpBase)
        self.cmbClientRelationConsents.setObjectName(_fromUtf8("cmbClientRelationConsents"))
        self.gridLayout_2.addWidget(self.cmbClientRelationConsents, 13, 1, 1, 1)
        self.lblEventExternalId = QtGui.QLabel(self.grpBase)
        self.lblEventExternalId.setObjectName(_fromUtf8("lblEventExternalId"))
        self.gridLayout_2.addWidget(self.lblEventExternalId, 14, 0, 1, 1)
        self.edtEventExternalIdValue = QtGui.QLineEdit(self.grpBase)
        self.edtEventExternalIdValue.setObjectName(_fromUtf8("edtEventExternalIdValue"))
        self.gridLayout_2.addWidget(self.edtEventExternalIdValue, 14, 1, 1, 1)
        self.horizontalLayout.addWidget(self.grpBase)
        self.splitter = QtGui.QSplitter(self.frameBaseAndDiagnosises)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtGui.QFrame.Plain)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpInspections_2 = QtGui.QGroupBox(self.splitter)
        self.grpInspections_2.setObjectName(_fromUtf8("grpInspections_2"))
        self._4 = QtGui.QVBoxLayout(self.grpInspections_2)
        self._4.setMargin(4)
        self._4.setSpacing(4)
        self._4.setObjectName(_fromUtf8("_4"))
        self.tblPreliminaryDiagnostics = CDiagnosticsInDocTableView(self.grpInspections_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblPreliminaryDiagnostics.sizePolicy().hasHeightForWidth())
        self.tblPreliminaryDiagnostics.setSizePolicy(sizePolicy)
        self.tblPreliminaryDiagnostics.setMinimumSize(QtCore.QSize(0, 100))
        self.tblPreliminaryDiagnostics.setObjectName(_fromUtf8("tblPreliminaryDiagnostics"))
        self._4.addWidget(self.tblPreliminaryDiagnostics)
        self.grpInspections = QtGui.QGroupBox(self.splitter)
        self.grpInspections.setObjectName(_fromUtf8("grpInspections"))
        self._2 = QtGui.QVBoxLayout(self.grpInspections)
        self._2.setMargin(4)
        self._2.setSpacing(4)
        self._2.setObjectName(_fromUtf8("_2"))
        self.tblFinalDiagnostics = CDiagnosticsInDocTableView(self.grpInspections)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblFinalDiagnostics.sizePolicy().hasHeightForWidth())
        self.tblFinalDiagnostics.setSizePolicy(sizePolicy)
        self.tblFinalDiagnostics.setMinimumSize(QtCore.QSize(0, 100))
        self.tblFinalDiagnostics.setObjectName(_fromUtf8("tblFinalDiagnostics"))
        self._2.addWidget(self.tblFinalDiagnostics)
        self.horizontalLayout.addWidget(self.splitter)
        self.frame = QtGui.QFrame(self.splitter_2)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grpActions = QtGui.QGroupBox(self.frame)
        self.grpActions.setObjectName(_fromUtf8("grpActions"))
        self._3 = QtGui.QGridLayout(self.grpActions)
        self._3.setMargin(4)
        self._3.setSpacing(4)
        self._3.setObjectName(_fromUtf8("_3"))
        self.tblActions = CInDocTableView(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.tblActions.sizePolicy().hasHeightForWidth())
        self.tblActions.setSizePolicy(sizePolicy)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self._3.addWidget(self.tblActions, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.grpActions)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabToken, _fromUtf8(""))
        self.tabMedicalDiagnosis = CEventMedicalDiagnosisPage()
        self.tabMedicalDiagnosis.setObjectName(_fromUtf8("tabMedicalDiagnosis"))
        self.tabWidget.addTab(self.tabMedicalDiagnosis, _fromUtf8(""))
        self.tabMes = CEventMesPage()
        self.tabMes.setObjectName(_fromUtf8("tabMes"))
        self.tabWidget.addTab(self.tabMes, _fromUtf8(""))
        self.tabStatus = CActionsPage()
        self.tabStatus.setObjectName(_fromUtf8("tabStatus"))
        self.tabWidget.addTab(self.tabStatus, _fromUtf8(""))
        self.tabDiagnostic = CActionsPage()
        self.tabDiagnostic.setObjectName(_fromUtf8("tabDiagnostic"))
        self.tabWidget.addTab(self.tabDiagnostic, _fromUtf8(""))
        self.tabCure = CActionsPage()
        self.tabCure.setObjectName(_fromUtf8("tabCure"))
        self.tabWidget.addTab(self.tabCure, _fromUtf8(""))
        self.tabMisc = CActionsPage()
        self.tabMisc.setObjectName(_fromUtf8("tabMisc"))
        self.tabWidget.addTab(self.tabMisc, _fromUtf8(""))
        self.tabAmbCard = CAmbCardPage()
        self.tabAmbCard.setObjectName(_fromUtf8("tabAmbCard"))
        self.tabWidget.addTab(self.tabAmbCard, _fromUtf8(""))
        self.tabTempInvalidEtc = QtGui.QWidget()
        self.tabTempInvalidEtc.setObjectName(_fromUtf8("tabTempInvalidEtc"))
        self.gridLayout = QtGui.QGridLayout(self.tabTempInvalidEtc)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabTempInvalidAndAegrotat = QtGui.QTabWidget(self.tabTempInvalidEtc)
        self.tabTempInvalidAndAegrotat.setObjectName(_fromUtf8("tabTempInvalidAndAegrotat"))
        self.tabTempInvalid = QtGui.QWidget()
        self.tabTempInvalid.setObjectName(_fromUtf8("tabTempInvalid"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabTempInvalid)
        self.verticalLayout_5.setMargin(4)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.grpTempInvalid = CTempInvalid(self.tabTempInvalid)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpTempInvalid.sizePolicy().hasHeightForWidth())
        self.grpTempInvalid.setSizePolicy(sizePolicy)
        self.grpTempInvalid.setChecked(False)
        self.grpTempInvalid.setObjectName(_fromUtf8("grpTempInvalid"))
        self.verticalLayout_5.addWidget(self.grpTempInvalid)
        self.tabTempInvalidAndAegrotat.addTab(self.tabTempInvalid, _fromUtf8(""))
        self.tabAegrotat = QtGui.QWidget()
        self.tabAegrotat.setObjectName(_fromUtf8("tabAegrotat"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabAegrotat)
        self.verticalLayout_4.setMargin(4)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.grpAegrotat = CTempInvalid(self.tabAegrotat)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpAegrotat.sizePolicy().hasHeightForWidth())
        self.grpAegrotat.setSizePolicy(sizePolicy)
        self.grpAegrotat.setChecked(False)
        self.grpAegrotat.setObjectName(_fromUtf8("grpAegrotat"))
        self.verticalLayout_4.addWidget(self.grpAegrotat)
        self.tabTempInvalidAndAegrotat.addTab(self.tabAegrotat, _fromUtf8(""))
        self.tabDisability = QtGui.QWidget()
        self.tabDisability.setObjectName(_fromUtf8("tabDisability"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabDisability)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.grpDisability = CTempInvalid(self.tabDisability)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpDisability.sizePolicy().hasHeightForWidth())
        self.grpDisability.setSizePolicy(sizePolicy)
        self.grpDisability.setChecked(False)
        self.grpDisability.setObjectName(_fromUtf8("grpDisability"))
        self.verticalLayout_2.addWidget(self.grpDisability)
        self.tabTempInvalidAndAegrotat.addTab(self.tabDisability, _fromUtf8(""))
        self.tabVitalRestriction = QtGui.QWidget()
        self.tabVitalRestriction.setObjectName(_fromUtf8("tabVitalRestriction"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tabVitalRestriction)
        self.verticalLayout_6.setMargin(4)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.grpVitalRestriction = CTempInvalid(self.tabVitalRestriction)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpVitalRestriction.sizePolicy().hasHeightForWidth())
        self.grpVitalRestriction.setSizePolicy(sizePolicy)
        self.grpVitalRestriction.setChecked(False)
        self.grpVitalRestriction.setObjectName(_fromUtf8("grpVitalRestriction"))
        self.verticalLayout_6.addWidget(self.grpVitalRestriction)
        self.tabTempInvalidAndAegrotat.addTab(self.tabVitalRestriction, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabTempInvalidAndAegrotat, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTempInvalidEtc, _fromUtf8(""))
        self.tabFeed = CEventFeedPage()
        self.tabFeed.setObjectName(_fromUtf8("tabFeed"))
        self.tabWidget.addTab(self.tabFeed, _fromUtf8(""))
        self.tabCash = CEventCashPage()
        self.tabCash.setObjectName(_fromUtf8("tabCash"))
        self.tabWidget.addTab(self.tabCash, _fromUtf8(""))
        self.tabNotes = CEventVoucherNotesPage()
        self.tabNotes.setObjectName(_fromUtf8("tabNotes"))
        self.tabWidget.addTab(self.tabNotes, _fromUtf8(""))
        self.tabVoucher = CEventVoucherPage()
        self.tabVoucher.setObjectName(_fromUtf8("tabVoucher"))
        self.tabWidget.addTab(self.tabVoucher, _fromUtf8(""))
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_5.addWidget(self.splitter_3, 0, 0, 1, 4)
        self.lblProlongateEvent = QtGui.QLabel(Dialog)
        self.lblProlongateEvent.setText(_fromUtf8(""))
        self.lblProlongateEvent.setObjectName(_fromUtf8("lblProlongateEvent"))
        self.gridLayout_5.addWidget(self.lblProlongateEvent, 1, 0, 1, 1)
        self.lblValueExternalId = QtGui.QLabel(Dialog)
        self.lblValueExternalId.setText(_fromUtf8(""))
        self.lblValueExternalId.setObjectName(_fromUtf8("lblValueExternalId"))
        self.gridLayout_5.addWidget(self.lblValueExternalId, 1, 1, 1, 1)
        self.lblValueMesCode = QtGui.QLabel(Dialog)
        self.lblValueMesCode.setText(_fromUtf8(""))
        self.lblValueMesCode.setObjectName(_fromUtf8("lblValueMesCode"))
        self.gridLayout_5.addWidget(self.lblValueMesCode, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_5.addWidget(self.buttonBox, 1, 3, 1, 1)
        self.statusBar = QtGui.QStatusBar(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout_5.addWidget(self.statusBar, 2, 0, 1, 4)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrder.setBuddy(self.cmbOrder)
        self.lblResult.setBuddy(self.cmbResult)
        self.lblPregnancyWeek.setBuddy(self.edtPregnancyWeek)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.tabTempInvalidAndAegrotat.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.tabWidget, self.cmbContract)
        Dialog.setTabOrder(self.cmbContract, self.edtBegDate)
        Dialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        Dialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        Dialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        Dialog.setTabOrder(self.edtEndTime, self.btnExecPersonList)
        Dialog.setTabOrder(self.btnExecPersonList, self.cmbPerson)
        Dialog.setTabOrder(self.cmbPerson, self.chkPrimary)
        Dialog.setTabOrder(self.chkPrimary, self.cmbOrder)
        Dialog.setTabOrder(self.cmbOrder, self.edtPregnancyWeek)
        Dialog.setTabOrder(self.edtPregnancyWeek, self.cmbResult)
        Dialog.setTabOrder(self.cmbResult, self.cmbClientRelationConsents)
        Dialog.setTabOrder(self.cmbClientRelationConsents, self.edtEventExternalIdValue)
        Dialog.setTabOrder(self.edtEventExternalIdValue, self.tblPreliminaryDiagnostics)
        Dialog.setTabOrder(self.tblPreliminaryDiagnostics, self.tblFinalDiagnostics)
        Dialog.setTabOrder(self.tblFinalDiagnostics, self.tblActions)
        Dialog.setTabOrder(self.tblActions, self.tabTempInvalidAndAegrotat)
        Dialog.setTabOrder(self.tabTempInvalidAndAegrotat, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.txtClientInfoBrowser.setWhatsThis(_translate("Dialog", "Описание пациента", None))
        self.txtClientInfoBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.grpBase.setTitle(_translate("Dialog", "&ф.072", None))
        self.btnExecPersonList.setText(_translate("Dialog", "...", None))
        self.cmbContract.setWhatsThis(_translate("Dialog", "номер, дата и основание договора в рамках которого производится осмотр", None))
        self.cmbContract.setItemText(0, _translate("Dialog", "Договор", None))
        self.lblBegDate.setText(_translate("Dialog", "Поступление", None))
        self.lblEndDate.setText(_translate("Dialog", "Выбытие", None))
        self.lblDuration.setText(_translate("Dialog", "Длительность", None))
        self.lblDurationValue.setText(_translate("Dialog", "-", None))
        self.cmbPerson.setWhatsThis(_translate("Dialog", "врач отвечающий за осмотр (терапевт)", None))
        self.cmbPerson.setItemText(0, _translate("Dialog", "Врач", None))
        self.chkPrimary.setText(_translate("Dialog", "Пе&рвичный", None))
        self.lblOrder.setText(_translate("Dialog", "П&орядок", None))
        self.lblResult.setText(_translate("Dialog", "Результат", None))
        self.cmbResult.setWhatsThis(_translate("Dialog", "результат осмотра", None))
        self.cmbResult.setItemText(0, _translate("Dialog", "Результат", None))
        self.edtBegDate.setWhatsThis(_translate("Dialog", "дата начала осмотра", None))
        self.edtBegTime.setDisplayFormat(_translate("Dialog", "HH:mm", None))
        self.edtEndDate.setWhatsThis(_translate("Dialog", "дата окончания осмотра", None))
        self.edtEndTime.setDisplayFormat(_translate("Dialog", "HH:mm", None))
        self.cmbOrder.setItemText(0, _translate("Dialog", "Плановый", None))
        self.cmbOrder.setItemText(1, _translate("Dialog", "Экстренный", None))
        self.cmbOrder.setItemText(2, _translate("Dialog", "Самотёком", None))
        self.cmbOrder.setItemText(3, _translate("Dialog", "Принудительный", None))
        self.cmbOrder.setItemText(4, _translate("Dialog", "Внутренний перевод", None))
        self.cmbOrder.setItemText(5, _translate("Dialog", "Неотложная", None))
        self.lblPregnancyWeek.setText(_translate("Dialog", "Неделя беременности", None))
        self.lblPerson.setText(_translate("Dialog", "Лечащий врач", None))
        self.lblClientRelationConsents.setText(_translate("Dialog", "Лицо по уходу", None))
        self.lblEventExternalId.setText(_translate("Dialog", "Номер документа", None))
        self.grpInspections_2.setTitle(_translate("Dialog", "&Предварительный диагноз", None))
        self.grpInspections.setTitle(_translate("Dialog", "&Заключительный диагноз", None))
        self.grpActions.setTitle(_translate("Dialog", "&Мероприятия", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabToken), _translate("Dialog", "Стат.&учёт", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMedicalDiagnosis), _translate("Dialog", "Диагноз", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMes), _translate("Dialog", "Стандарт", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStatus), _translate("Dialog", "&Статус", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDiagnostic), _translate("Dialog", "&Диагностика", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCure), _translate("Dialog", "&Лечение", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMisc), _translate("Dialog", "&Мероприятия", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAmbCard), _translate("Dialog", "Мед.&карта", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabTempInvalid), _translate("Dialog", "Листок &нетрудоспособности", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabAegrotat), _translate("Dialog", "С&правка", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabDisability), _translate("Dialog", "Инвалидность", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabVitalRestriction), _translate("Dialog", "&Ограничения жизнедеятельности", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTempInvalidEtc), _translate("Dialog", "Т&рудоспособность", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFeed), _translate("Dialog", "Питание", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCash), _translate("Dialog", "Оплата", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNotes), _translate("Dialog", "Приме&чания", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVoucher), _translate("Dialog", "Путевка", None))
        self.statusBar.setToolTip(_translate("Dialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("Dialog", "A status bar.", None))

from Events.ActionsPage import CActionsPage
from Events.AmbCardPage import CAmbCardPage
from Events.EventCashPage import CEventCashPage
from Events.EventDiagnosticsTable import CDiagnosticsInDocTableView
from Events.EventFeedPage import CEventFeedPage
from Events.EventMedicalDiagnosisPage import CEventMedicalDiagnosisPage
from Events.EventMesPage import CEventMesPage
from Events.EventVoucherNotesPage import CEventVoucherNotesPage
from Events.EventVoucherPage import CEventVoucherPage
from Events.TempInvalid import CTempInvalid
from Orgs.OrgComboBox import CContractComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Registry.Utils import CClientRelationComboBoxPatron
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.ROComboBox import CROComboBox
from library.TextBrowser import CTextBrowser
from library.crbcombobox import CRBComboBox
