# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ImportTariffsR61.ui'
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
        Dialog.resize(627, 693)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabFKSG = QtGui.QWidget()
        self.tabFKSG.setObjectName(_fromUtf8("tabFKSG"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabFKSG)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.tabFKSG)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbFKSGUnit = CRBComboBox(self.groupBox)
        self.cmbFKSGUnit.setObjectName(_fromUtf8("cmbFKSGUnit"))
        self.gridLayout.addWidget(self.cmbFKSGUnit, 2, 1, 1, 2)
        self.edtFKSGDATE_IN = CDateEdit(self.groupBox)
        self.edtFKSGDATE_IN.setObjectName(_fromUtf8("edtFKSGDATE_IN"))
        self.gridLayout.addWidget(self.edtFKSGDATE_IN, 3, 1, 1, 2)
        self.cmbFKSGEventType = CRBComboBox(self.groupBox)
        self.cmbFKSGEventType.setObjectName(_fromUtf8("cmbFKSGEventType"))
        self.gridLayout.addWidget(self.cmbFKSGEventType, 4, 1, 1, 2)
        self.cmbFKSGTariffType = QtGui.QComboBox(self.groupBox)
        self.cmbFKSGTariffType.setObjectName(_fromUtf8("cmbFKSGTariffType"))
        self.gridLayout.addWidget(self.cmbFKSGTariffType, 5, 1, 1, 2)
        self.btnFKSGImport = QtGui.QPushButton(self.groupBox)
        self.btnFKSGImport.setObjectName(_fromUtf8("btnFKSGImport"))
        self.gridLayout.addWidget(self.btnFKSGImport, 7, 0, 1, 3)
        self.edtFKSGTARIF = QtGui.QLineEdit(self.groupBox)
        self.edtFKSGTARIF.setObjectName(_fromUtf8("edtFKSGTARIF"))
        self.gridLayout.addWidget(self.edtFKSGTARIF, 0, 1, 1, 1)
        self.lblFKSGDATE_IN = QtGui.QLabel(self.groupBox)
        self.lblFKSGDATE_IN.setObjectName(_fromUtf8("lblFKSGDATE_IN"))
        self.gridLayout.addWidget(self.lblFKSGDATE_IN, 3, 0, 1, 1)
        self.lblFKSGTARIF = QtGui.QLabel(self.groupBox)
        self.lblFKSGTARIF.setObjectName(_fromUtf8("lblFKSGTARIF"))
        self.gridLayout.addWidget(self.lblFKSGTARIF, 0, 0, 1, 1)
        self.lblFKSGEventType = QtGui.QLabel(self.groupBox)
        self.lblFKSGEventType.setObjectName(_fromUtf8("lblFKSGEventType"))
        self.gridLayout.addWidget(self.lblFKSGEventType, 4, 0, 1, 1)
        self.lblFKSGUnit = QtGui.QLabel(self.groupBox)
        self.lblFKSGUnit.setObjectName(_fromUtf8("lblFKSGUnit"))
        self.gridLayout.addWidget(self.lblFKSGUnit, 2, 0, 1, 1)
        self.lblFKSGTariffType = QtGui.QLabel(self.groupBox)
        self.lblFKSGTariffType.setObjectName(_fromUtf8("lblFKSGTariffType"))
        self.gridLayout.addWidget(self.lblFKSGTariffType, 5, 0, 1, 1)
        self.btnFKSGSelectDBF = QtGui.QPushButton(self.groupBox)
        self.btnFKSGSelectDBF.setObjectName(_fromUtf8("btnFKSGSelectDBF"))
        self.gridLayout.addWidget(self.btnFKSGSelectDBF, 0, 2, 1, 1)
        self.lblFKSGXml = QtGui.QLabel(self.groupBox)
        self.lblFKSGXml.setObjectName(_fromUtf8("lblFKSGXml"))
        self.gridLayout.addWidget(self.lblFKSGXml, 1, 0, 1, 1)
        self.edtFKSGXml = QtGui.QLineEdit(self.groupBox)
        self.edtFKSGXml.setObjectName(_fromUtf8("edtFKSGXml"))
        self.gridLayout.addWidget(self.edtFKSGXml, 1, 1, 1, 1)
        self.btnFKSGSelectXml = QtGui.QPushButton(self.groupBox)
        self.btnFKSGSelectXml.setObjectName(_fromUtf8("btnFKSGSelectXml"))
        self.gridLayout.addWidget(self.btnFKSGSelectXml, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tabFKSG)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cmbFKSGTariffTypeClose = QtGui.QComboBox(self.groupBox_2)
        self.cmbFKSGTariffTypeClose.setObjectName(_fromUtf8("cmbFKSGTariffTypeClose"))
        self.gridLayout_2.addWidget(self.cmbFKSGTariffTypeClose, 3, 1, 1, 1)
        self.lblFKSGCloseEventType = QtGui.QLabel(self.groupBox_2)
        self.lblFKSGCloseEventType.setObjectName(_fromUtf8("lblFKSGCloseEventType"))
        self.gridLayout_2.addWidget(self.lblFKSGCloseEventType, 2, 0, 1, 1)
        self.lblFKSGTariffTypeClose = QtGui.QLabel(self.groupBox_2)
        self.lblFKSGTariffTypeClose.setObjectName(_fromUtf8("lblFKSGTariffTypeClose"))
        self.gridLayout_2.addWidget(self.lblFKSGTariffTypeClose, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblFKSGPeriodBeg = QtGui.QLabel(self.groupBox_2)
        self.lblFKSGPeriodBeg.setObjectName(_fromUtf8("lblFKSGPeriodBeg"))
        self.horizontalLayout.addWidget(self.lblFKSGPeriodBeg)
        self.edtFKSGPeriodBeg = CDateEdit(self.groupBox_2)
        self.edtFKSGPeriodBeg.setObjectName(_fromUtf8("edtFKSGPeriodBeg"))
        self.horizontalLayout.addWidget(self.edtFKSGPeriodBeg)
        self.lblFKSGPeriodEnd = QtGui.QLabel(self.groupBox_2)
        self.lblFKSGPeriodEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFKSGPeriodEnd.setObjectName(_fromUtf8("lblFKSGPeriodEnd"))
        self.horizontalLayout.addWidget(self.lblFKSGPeriodEnd)
        self.edtFKSGPeriodEnd = CDateEdit(self.groupBox_2)
        self.edtFKSGPeriodEnd.setObjectName(_fromUtf8("edtFKSGPeriodEnd"))
        self.horizontalLayout.addWidget(self.edtFKSGPeriodEnd)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.cmbFKSGEventTypeClose = CRBComboBox(self.groupBox_2)
        self.cmbFKSGEventTypeClose.setObjectName(_fromUtf8("cmbFKSGEventTypeClose"))
        self.gridLayout_2.addWidget(self.cmbFKSGEventTypeClose, 2, 1, 1, 1)
        self.lblFKSGEndDate = QtGui.QLabel(self.groupBox_2)
        self.lblFKSGEndDate.setObjectName(_fromUtf8("lblFKSGEndDate"))
        self.gridLayout_2.addWidget(self.lblFKSGEndDate, 0, 0, 1, 1)
        self.edtFKSGEndDate = CDateEdit(self.groupBox_2)
        self.edtFKSGEndDate.setObjectName(_fromUtf8("edtFKSGEndDate"))
        self.gridLayout_2.addWidget(self.edtFKSGEndDate, 0, 1, 1, 1)
        self.btnFKSGClose = QtGui.QPushButton(self.groupBox_2)
        self.btnFKSGClose.setObjectName(_fromUtf8("btnFKSGClose"))
        self.gridLayout_2.addWidget(self.btnFKSGClose, 5, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tabFKSG, _fromUtf8(""))
        self.tabVMP = QtGui.QWidget()
        self.tabVMP.setObjectName(_fromUtf8("tabVMP"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabVMP)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_3 = QtGui.QGroupBox(self.tabVMP)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lblVMPTariffType = QtGui.QLabel(self.groupBox_3)
        self.lblVMPTariffType.setObjectName(_fromUtf8("lblVMPTariffType"))
        self.gridLayout_3.addWidget(self.lblVMPTariffType, 3, 0, 1, 1)
        self.btnVMPSelectDBF = QtGui.QPushButton(self.groupBox_3)
        self.btnVMPSelectDBF.setObjectName(_fromUtf8("btnVMPSelectDBF"))
        self.gridLayout_3.addWidget(self.btnVMPSelectDBF, 0, 2, 1, 1)
        self.edtVMPSTACTAR = QtGui.QLineEdit(self.groupBox_3)
        self.edtVMPSTACTAR.setObjectName(_fromUtf8("edtVMPSTACTAR"))
        self.gridLayout_3.addWidget(self.edtVMPSTACTAR, 0, 1, 1, 1)
        self.lblVMPSTACTAR = QtGui.QLabel(self.groupBox_3)
        self.lblVMPSTACTAR.setObjectName(_fromUtf8("lblVMPSTACTAR"))
        self.gridLayout_3.addWidget(self.lblVMPSTACTAR, 0, 0, 1, 1)
        self.lblVMPUnit = QtGui.QLabel(self.groupBox_3)
        self.lblVMPUnit.setObjectName(_fromUtf8("lblVMPUnit"))
        self.gridLayout_3.addWidget(self.lblVMPUnit, 1, 0, 1, 1)
        self.cmbVMPUnit = CRBComboBox(self.groupBox_3)
        self.cmbVMPUnit.setObjectName(_fromUtf8("cmbVMPUnit"))
        self.gridLayout_3.addWidget(self.cmbVMPUnit, 1, 1, 1, 2)
        self.cmbVMPEventType = CRBComboBox(self.groupBox_3)
        self.cmbVMPEventType.setObjectName(_fromUtf8("cmbVMPEventType"))
        self.gridLayout_3.addWidget(self.cmbVMPEventType, 2, 1, 1, 2)
        self.btnVMPImport = QtGui.QPushButton(self.groupBox_3)
        self.btnVMPImport.setObjectName(_fromUtf8("btnVMPImport"))
        self.gridLayout_3.addWidget(self.btnVMPImport, 5, 0, 1, 3)
        self.cmbVMPTariffType = QtGui.QComboBox(self.groupBox_3)
        self.cmbVMPTariffType.setObjectName(_fromUtf8("cmbVMPTariffType"))
        self.gridLayout_3.addWidget(self.cmbVMPTariffType, 3, 1, 1, 2)
        self.lblVMPEventType = QtGui.QLabel(self.groupBox_3)
        self.lblVMPEventType.setObjectName(_fromUtf8("lblVMPEventType"))
        self.gridLayout_3.addWidget(self.lblVMPEventType, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 4, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.tabVMP)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblVMPTariffTypeClose = QtGui.QLabel(self.groupBox_4)
        self.lblVMPTariffTypeClose.setObjectName(_fromUtf8("lblVMPTariffTypeClose"))
        self.gridLayout_4.addWidget(self.lblVMPTariffTypeClose, 3, 0, 1, 1)
        self.lblVMPEventTypeClose = QtGui.QLabel(self.groupBox_4)
        self.lblVMPEventTypeClose.setObjectName(_fromUtf8("lblVMPEventTypeClose"))
        self.gridLayout_4.addWidget(self.lblVMPEventTypeClose, 2, 0, 1, 1)
        self.cmbVMPTariffTypeClose = QtGui.QComboBox(self.groupBox_4)
        self.cmbVMPTariffTypeClose.setObjectName(_fromUtf8("cmbVMPTariffTypeClose"))
        self.gridLayout_4.addWidget(self.cmbVMPTariffTypeClose, 3, 1, 1, 1)
        self.lblVMPEndDate = QtGui.QLabel(self.groupBox_4)
        self.lblVMPEndDate.setObjectName(_fromUtf8("lblVMPEndDate"))
        self.gridLayout_4.addWidget(self.lblVMPEndDate, 0, 0, 1, 1)
        self.edtVMPEndDate = CDateEdit(self.groupBox_4)
        self.edtVMPEndDate.setObjectName(_fromUtf8("edtVMPEndDate"))
        self.gridLayout_4.addWidget(self.edtVMPEndDate, 0, 1, 1, 1)
        self.cmbVMPEventTypeClose = CRBComboBox(self.groupBox_4)
        self.cmbVMPEventTypeClose.setObjectName(_fromUtf8("cmbVMPEventTypeClose"))
        self.gridLayout_4.addWidget(self.cmbVMPEventTypeClose, 2, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblVMPPeriodBeg = QtGui.QLabel(self.groupBox_4)
        self.lblVMPPeriodBeg.setObjectName(_fromUtf8("lblVMPPeriodBeg"))
        self.horizontalLayout_2.addWidget(self.lblVMPPeriodBeg)
        self.edtVMPPerionBeg = CDateEdit(self.groupBox_4)
        self.edtVMPPerionBeg.setObjectName(_fromUtf8("edtVMPPerionBeg"))
        self.horizontalLayout_2.addWidget(self.edtVMPPerionBeg)
        self.lblVMPPerionEnd = QtGui.QLabel(self.groupBox_4)
        self.lblVMPPerionEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.lblVMPPerionEnd.setObjectName(_fromUtf8("lblVMPPerionEnd"))
        self.horizontalLayout_2.addWidget(self.lblVMPPerionEnd)
        self.edtVMPPerionEnd = CDateEdit(self.groupBox_4)
        self.edtVMPPerionEnd.setObjectName(_fromUtf8("edtVMPPerionEnd"))
        self.horizontalLayout_2.addWidget(self.edtVMPPerionEnd)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.btnVMPClose = QtGui.QPushButton(self.groupBox_4)
        self.btnVMPClose.setObjectName(_fromUtf8("btnVMPClose"))
        self.gridLayout_4.addWidget(self.btnVMPClose, 5, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 4, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tabVMP, _fromUtf8(""))
        self.tabAPP = QtGui.QWidget()
        self.tabAPP.setObjectName(_fromUtf8("tabAPP"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabAPP)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox_5 = QtGui.QGroupBox(self.tabAPP)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.cmbAppTariffType = QtGui.QComboBox(self.groupBox_5)
        self.cmbAppTariffType.setObjectName(_fromUtf8("cmbAppTariffType"))
        self.gridLayout_5.addWidget(self.cmbAppTariffType, 3, 1, 1, 2)
        self.lblAppEventType = QtGui.QLabel(self.groupBox_5)
        self.lblAppEventType.setObjectName(_fromUtf8("lblAppEventType"))
        self.gridLayout_5.addWidget(self.lblAppEventType, 2, 0, 1, 1)
        self.lblAPPPOLIKTAR = QtGui.QLabel(self.groupBox_5)
        self.lblAPPPOLIKTAR.setObjectName(_fromUtf8("lblAPPPOLIKTAR"))
        self.gridLayout_5.addWidget(self.lblAPPPOLIKTAR, 0, 0, 1, 1)
        self.lblAppUnit = QtGui.QLabel(self.groupBox_5)
        self.lblAppUnit.setObjectName(_fromUtf8("lblAppUnit"))
        self.gridLayout_5.addWidget(self.lblAppUnit, 1, 0, 1, 1)
        self.cmbAppUnit = CRBComboBox(self.groupBox_5)
        self.cmbAppUnit.setObjectName(_fromUtf8("cmbAppUnit"))
        self.gridLayout_5.addWidget(self.cmbAppUnit, 1, 1, 1, 2)
        self.btnAppSelectPOLIKTAR = QtGui.QPushButton(self.groupBox_5)
        self.btnAppSelectPOLIKTAR.setObjectName(_fromUtf8("btnAppSelectPOLIKTAR"))
        self.gridLayout_5.addWidget(self.btnAppSelectPOLIKTAR, 0, 2, 1, 1)
        self.btnAppImport = QtGui.QPushButton(self.groupBox_5)
        self.btnAppImport.setObjectName(_fromUtf8("btnAppImport"))
        self.gridLayout_5.addWidget(self.btnAppImport, 5, 0, 1, 3)
        self.cmbAppEventType = CRBComboBox(self.groupBox_5)
        self.cmbAppEventType.setObjectName(_fromUtf8("cmbAppEventType"))
        self.gridLayout_5.addWidget(self.cmbAppEventType, 2, 1, 1, 2)
        self.lblAppTariffType = QtGui.QLabel(self.groupBox_5)
        self.lblAppTariffType.setObjectName(_fromUtf8("lblAppTariffType"))
        self.gridLayout_5.addWidget(self.lblAppTariffType, 3, 0, 1, 1)
        self.edtAPPPOLIKTAR = QtGui.QLineEdit(self.groupBox_5)
        self.edtAPPPOLIKTAR.setObjectName(_fromUtf8("edtAPPPOLIKTAR"))
        self.gridLayout_5.addWidget(self.edtAPPPOLIKTAR, 0, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 4, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox_6 = QtGui.QGroupBox(self.tabAPP)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.cmbAppEventTypeClose = CRBComboBox(self.groupBox_6)
        self.cmbAppEventTypeClose.setObjectName(_fromUtf8("cmbAppEventTypeClose"))
        self.gridLayout_6.addWidget(self.cmbAppEventTypeClose, 2, 1, 1, 1)
        self.lblAppEndDate = QtGui.QLabel(self.groupBox_6)
        self.lblAppEndDate.setObjectName(_fromUtf8("lblAppEndDate"))
        self.gridLayout_6.addWidget(self.lblAppEndDate, 0, 0, 1, 1)
        self.edtAppEndDate = CDateEdit(self.groupBox_6)
        self.edtAppEndDate.setObjectName(_fromUtf8("edtAppEndDate"))
        self.gridLayout_6.addWidget(self.edtAppEndDate, 0, 1, 1, 1)
        self.cmbAppTariffTypeClose = QtGui.QComboBox(self.groupBox_6)
        self.cmbAppTariffTypeClose.setObjectName(_fromUtf8("cmbAppTariffTypeClose"))
        self.gridLayout_6.addWidget(self.cmbAppTariffTypeClose, 3, 1, 1, 1)
        self.lblAppEventTypeClose = QtGui.QLabel(self.groupBox_6)
        self.lblAppEventTypeClose.setObjectName(_fromUtf8("lblAppEventTypeClose"))
        self.gridLayout_6.addWidget(self.lblAppEventTypeClose, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblAppPeriodBeg = QtGui.QLabel(self.groupBox_6)
        self.lblAppPeriodBeg.setObjectName(_fromUtf8("lblAppPeriodBeg"))
        self.horizontalLayout_3.addWidget(self.lblAppPeriodBeg)
        self.edtAppPeriodBeg = CDateEdit(self.groupBox_6)
        self.edtAppPeriodBeg.setObjectName(_fromUtf8("edtAppPeriodBeg"))
        self.horizontalLayout_3.addWidget(self.edtAppPeriodBeg)
        self.lblAppPeriodEnd = QtGui.QLabel(self.groupBox_6)
        self.lblAppPeriodEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAppPeriodEnd.setObjectName(_fromUtf8("lblAppPeriodEnd"))
        self.horizontalLayout_3.addWidget(self.lblAppPeriodEnd)
        self.edtAppPeriodEnd = CDateEdit(self.groupBox_6)
        self.edtAppPeriodEnd.setObjectName(_fromUtf8("edtAppPeriodEnd"))
        self.horizontalLayout_3.addWidget(self.edtAppPeriodEnd)
        self.gridLayout_6.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)
        self.btnAppClose = QtGui.QPushButton(self.groupBox_6)
        self.btnAppClose.setObjectName(_fromUtf8("btnAppClose"))
        self.gridLayout_6.addWidget(self.btnAppClose, 5, 0, 1, 2)
        self.lblAppTariffTypeClose = QtGui.QLabel(self.groupBox_6)
        self.lblAppTariffTypeClose.setObjectName(_fromUtf8("lblAppTariffTypeClose"))
        self.gridLayout_6.addWidget(self.lblAppTariffTypeClose, 3, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem5, 4, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.groupBox_6)
        self.tabWidget.addTab(self.tabAPP, _fromUtf8(""))
        self.log = QtGui.QTextBrowser(self.splitter)
        self.log.setObjectName(_fromUtf8("log"))
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка тарифов для Ростовской области", None))
        self.groupBox.setTitle(_translate("Dialog", "Импорт тарифов", None))
        self.btnFKSGImport.setText(_translate("Dialog", "Импорт", None))
        self.lblFKSGDATE_IN.setText(_translate("Dialog", "DATE_IN", None))
        self.lblFKSGTARIF.setText(_translate("Dialog", "Выбор файла KSGTARIF.dbf", None))
        self.lblFKSGEventType.setText(_translate("Dialog", "Тип события", None))
        self.lblFKSGUnit.setText(_translate("Dialog", "Единица уч. мед. помощи", None))
        self.lblFKSGTariffType.setText(_translate("Dialog", "Тарифицируется", None))
        self.btnFKSGSelectDBF.setText(_translate("Dialog", "...", None))
        self.lblFKSGXml.setText(_translate("Dialog", "Выбор файла FKSG.xml", None))
        self.btnFKSGSelectXml.setText(_translate("Dialog", "...", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Закрыть тарифы", None))
        self.lblFKSGCloseEventType.setText(_translate("Dialog", "Тип события", None))
        self.lblFKSGTariffTypeClose.setText(_translate("Dialog", "Тарифицируется", None))
        self.lblFKSGPeriodBeg.setText(_translate("Dialog", "Период с", None))
        self.lblFKSGPeriodEnd.setText(_translate("Dialog", "по", None))
        self.lblFKSGEndDate.setText(_translate("Dialog", "Установить дату закрытия", None))
        self.btnFKSGClose.setText(_translate("Dialog", "Закрыть тарифы", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFKSG), _translate("Dialog", "Тарифы ФКСГ", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Импорт тарифов", None))
        self.lblVMPTariffType.setText(_translate("Dialog", "Тарифицируется", None))
        self.btnVMPSelectDBF.setText(_translate("Dialog", "...", None))
        self.lblVMPSTACTAR.setText(_translate("Dialog", "Выбор файла STACTAR.dbf", None))
        self.lblVMPUnit.setText(_translate("Dialog", "Единица уч. мед. помощи", None))
        self.btnVMPImport.setText(_translate("Dialog", "Импорт", None))
        self.lblVMPEventType.setText(_translate("Dialog", "Тип события", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Закрыть недействующие тарифы", None))
        self.lblVMPTariffTypeClose.setText(_translate("Dialog", "Тарифицируется", None))
        self.lblVMPEventTypeClose.setText(_translate("Dialog", "Тип события", None))
        self.lblVMPEndDate.setText(_translate("Dialog", "Установить дату закрытия", None))
        self.lblVMPPeriodBeg.setText(_translate("Dialog", "Период с", None))
        self.lblVMPPerionEnd.setText(_translate("Dialog", "по", None))
        self.btnVMPClose.setText(_translate("Dialog", "Закрыть тарифы", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVMP), _translate("Dialog", "Тарифы ВМП", None))
        self.groupBox_5.setTitle(_translate("Dialog", "Импорт тарифов", None))
        self.lblAppEventType.setText(_translate("Dialog", "Тип события", None))
        self.lblAPPPOLIKTAR.setText(_translate("Dialog", "Выбор файла POLIKTAR.dbf", None))
        self.lblAppUnit.setText(_translate("Dialog", "Единица уч. мед. помощи", None))
        self.btnAppSelectPOLIKTAR.setText(_translate("Dialog", "...", None))
        self.btnAppImport.setText(_translate("Dialog", "Импорт", None))
        self.lblAppTariffType.setText(_translate("Dialog", "Тарифицируется", None))
        self.groupBox_6.setTitle(_translate("Dialog", "Закрыть недействующие тарифы", None))
        self.lblAppEndDate.setText(_translate("Dialog", "Установить дату закрытия", None))
        self.lblAppEventTypeClose.setText(_translate("Dialog", "Тип события", None))
        self.lblAppPeriodBeg.setText(_translate("Dialog", "Период с", None))
        self.lblAppPeriodEnd.setText(_translate("Dialog", "по", None))
        self.btnAppClose.setText(_translate("Dialog", "Закрыть тарифы", None))
        self.lblAppTariffTypeClose.setText(_translate("Dialog", "Тарифицируется", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAPP), _translate("Dialog", "Тарифы АПП", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox