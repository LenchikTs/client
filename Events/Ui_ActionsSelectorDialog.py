# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Events/ActionsSelectorDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ActionTypesSelectorDialog(object):
    def setupUi(self, ActionTypesSelectorDialog):
        ActionTypesSelectorDialog.setObjectName(_fromUtf8("ActionTypesSelectorDialog"))
        ActionTypesSelectorDialog.resize(971, 407)
        ActionTypesSelectorDialog.setSizeGripEnabled(False)
        self.gridLayout_2 = QtGui.QGridLayout(ActionTypesSelectorDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.chkFindFilter = QtGui.QCheckBox(ActionTypesSelectorDialog)
        self.chkFindFilter.setObjectName(_fromUtf8("chkFindFilter"))
        self.gridLayout_2.addWidget(self.chkFindFilter, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTypesSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 3, 1, 1)
        self.pnlFilter = QtGui.QWidget(ActionTypesSelectorDialog)
        self.pnlFilter.setObjectName(_fromUtf8("pnlFilter"))
        self.gridLayout = QtGui.QGridLayout(self.pnlFilter)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkOrgStructure = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkOrgStructure.sizePolicy().hasHeightForWidth())
        self.chkOrgStructure.setSizePolicy(sizePolicy)
        self.chkOrgStructure.setChecked(False)
        self.chkOrgStructure.setObjectName(_fromUtf8("chkOrgStructure"))
        self.gridLayout.addWidget(self.chkOrgStructure, 0, 10, 1, 1)
        self.chkMes = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkMes.sizePolicy().hasHeightForWidth())
        self.chkMes.setSizePolicy(sizePolicy)
        self.chkMes.setObjectName(_fromUtf8("chkMes"))
        self.gridLayout.addWidget(self.chkMes, 1, 1, 1, 1)
        self.chkNomenclative = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkNomenclative.sizePolicy().hasHeightForWidth())
        self.chkNomenclative.setSizePolicy(sizePolicy)
        self.chkNomenclative.setObjectName(_fromUtf8("chkNomenclative"))
        self.gridLayout.addWidget(self.chkNomenclative, 1, 0, 1, 1)
        self.chkContract = QtGui.QCheckBox(self.pnlFilter)
        self.chkContract.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkContract.sizePolicy().hasHeightForWidth())
        self.chkContract.setSizePolicy(sizePolicy)
        self.chkContract.setObjectName(_fromUtf8("chkContract"))
        self.gridLayout.addWidget(self.chkContract, 0, 1, 1, 1)
        self.chkContractTariffLimitations = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkContractTariffLimitations.sizePolicy().hasHeightForWidth())
        self.chkContractTariffLimitations.setSizePolicy(sizePolicy)
        self.chkContractTariffLimitations.setObjectName(_fromUtf8("chkContractTariffLimitations"))
        self.gridLayout.addWidget(self.chkContractTariffLimitations, 0, 9, 1, 1)
        self.chkSexAndAge = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSexAndAge.sizePolicy().hasHeightForWidth())
        self.chkSexAndAge.setSizePolicy(sizePolicy)
        self.chkSexAndAge.setChecked(True)
        self.chkSexAndAge.setObjectName(_fromUtf8("chkSexAndAge"))
        self.gridLayout.addWidget(self.chkSexAndAge, 0, 5, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(self.pnlFilter)
        self.cmbOrgStructure.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 11, 1, 1)
        self.chkPriceList = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPriceList.sizePolicy().hasHeightForWidth())
        self.chkPriceList.setSizePolicy(sizePolicy)
        self.chkPriceList.setObjectName(_fromUtf8("chkPriceList"))
        self.gridLayout.addWidget(self.chkPriceList, 0, 6, 1, 1)
        self.chkCSG = QtGui.QCheckBox(self.pnlFilter)
        self.chkCSG.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkCSG.sizePolicy().hasHeightForWidth())
        self.chkCSG.setSizePolicy(sizePolicy)
        self.chkCSG.setObjectName(_fromUtf8("chkCSG"))
        self.gridLayout.addWidget(self.chkCSG, 1, 2, 1, 2)
        self.chkPreferable = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPreferable.sizePolicy().hasHeightForWidth())
        self.chkPreferable.setSizePolicy(sizePolicy)
        self.chkPreferable.setChecked(True)
        self.chkPreferable.setObjectName(_fromUtf8("chkPreferable"))
        self.gridLayout.addWidget(self.chkPreferable, 0, 2, 1, 3)
        self.chkOnlyNotExists = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkOnlyNotExists.sizePolicy().hasHeightForWidth())
        self.chkOnlyNotExists.setSizePolicy(sizePolicy)
        self.chkOnlyNotExists.setChecked(True)
        self.chkOnlyNotExists.setObjectName(_fromUtf8("chkOnlyNotExists"))
        self.gridLayout.addWidget(self.chkOnlyNotExists, 0, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(self.pnlFilter)
        self.cmbSpeciality.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSpeciality.sizePolicy().hasHeightForWidth())
        self.cmbSpeciality.setSizePolicy(sizePolicy)
        self.cmbSpeciality.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 1, 11, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chkIsNecessary = QtGui.QCheckBox(self.pnlFilter)
        self.chkIsNecessary.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkIsNecessary.sizePolicy().hasHeightForWidth())
        self.chkIsNecessary.setSizePolicy(sizePolicy)
        self.chkIsNecessary.setObjectName(_fromUtf8("chkIsNecessary"))
        self.horizontalLayout.addWidget(self.chkIsNecessary)
        self.chkAmountFromMES = QtGui.QCheckBox(self.pnlFilter)
        self.chkAmountFromMES.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAmountFromMES.sizePolicy().hasHeightForWidth())
        self.chkAmountFromMES.setSizePolicy(sizePolicy)
        self.chkAmountFromMES.setObjectName(_fromUtf8("chkAmountFromMES"))
        self.horizontalLayout.addWidget(self.chkAmountFromMES)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 7, 1, 3)
        self.cmbPriceListContract = CIndependentContractComboBox(self.pnlFilter)
        self.cmbPriceListContract.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbPriceListContract.sizePolicy().hasHeightForWidth())
        self.cmbPriceListContract.setSizePolicy(sizePolicy)
        self.cmbPriceListContract.setObjectName(_fromUtf8("cmbPriceListContract"))
        self.gridLayout.addWidget(self.cmbPriceListContract, 0, 7, 1, 2)
        self.chkPlanner = QtGui.QCheckBox(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPlanner.sizePolicy().hasHeightForWidth())
        self.chkPlanner.setSizePolicy(sizePolicy)
        self.chkPlanner.setObjectName(_fromUtf8("chkPlanner"))
        self.gridLayout.addWidget(self.chkPlanner, 1, 10, 1, 1)
        self.cmbCSG = CActionCSGComboBox(self.pnlFilter)
        self.cmbCSG.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbCSG.sizePolicy().hasHeightForWidth())
        self.cmbCSG.setSizePolicy(sizePolicy)
        self.cmbCSG.setObjectName(_fromUtf8("cmbCSG"))
        self.gridLayout.addWidget(self.cmbCSG, 1, 4, 1, 3)
        self.gridLayout_2.addWidget(self.pnlFilter, 0, 0, 1, 4)
        self.lblMesInfo = QtGui.QLabel(ActionTypesSelectorDialog)
        self.lblMesInfo.setText(_fromUtf8(""))
        self.lblMesInfo.setObjectName(_fromUtf8("lblMesInfo"))
        self.gridLayout_2.addWidget(self.lblMesInfo, 4, 0, 1, 1)
        self.splitter_2 = QtGui.QSplitter(ActionTypesSelectorDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlSelectedActionTypes = QtGui.QWidget(self.splitter_2)
        self.pnlSelectedActionTypes.setObjectName(_fromUtf8("pnlSelectedActionTypes"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.pnlSelectedActionTypes)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.splSelectedActionTypes = QtGui.QSplitter(self.pnlSelectedActionTypes)
        self.splSelectedActionTypes.setOrientation(QtCore.Qt.Horizontal)
        self.splSelectedActionTypes.setObjectName(_fromUtf8("splSelectedActionTypes"))
        self.pnlSelectedActionTypes_2 = QtGui.QWidget(self.splSelectedActionTypes)
        self.pnlSelectedActionTypes_2.setObjectName(_fromUtf8("pnlSelectedActionTypes_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pnlSelectedActionTypes_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lblSelectedActionTypes = QtGui.QLabel(self.pnlSelectedActionTypes_2)
        self.lblSelectedActionTypes.setObjectName(_fromUtf8("lblSelectedActionTypes"))
        self.verticalLayout_3.addWidget(self.lblSelectedActionTypes)
        self.tblSelectedActionTypes = CCheckedActionsTableView(self.pnlSelectedActionTypes_2)
        self.tblSelectedActionTypes.setObjectName(_fromUtf8("tblSelectedActionTypes"))
        self.verticalLayout_3.addWidget(self.tblSelectedActionTypes)
        self.tblSelectedActionTypes.raise_()
        self.lblSelectedActionTypes.raise_()
        self.pnlExistsClientActions = QtGui.QWidget(self.splSelectedActionTypes)
        self.pnlExistsClientActions.setObjectName(_fromUtf8("pnlExistsClientActions"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlExistsClientActions)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lblExistsClientActions = QtGui.QLabel(self.pnlExistsClientActions)
        self.lblExistsClientActions.setObjectName(_fromUtf8("lblExistsClientActions"))
        self.verticalLayout_2.addWidget(self.lblExistsClientActions)
        self.tblExistsClientActions = CTableView(self.pnlExistsClientActions)
        self.tblExistsClientActions.setObjectName(_fromUtf8("tblExistsClientActions"))
        self.verticalLayout_2.addWidget(self.tblExistsClientActions)
        self.verticalLayout_4.addWidget(self.splSelectedActionTypes)
        self.pnlActionTypes = QtGui.QWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlActionTypes.sizePolicy().hasHeightForWidth())
        self.pnlActionTypes.setSizePolicy(sizePolicy)
        self.pnlActionTypes.setObjectName(_fromUtf8("pnlActionTypes"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pnlActionTypes)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.splitter = QtGui.QSplitter(self.pnlActionTypes)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tabWgtActionTypes = QtGui.QTabWidget(self.splitter)
        self.tabWgtActionTypes.setObjectName(_fromUtf8("tabWgtActionTypes"))
        self.tabActionTypes = QtGui.QWidget()
        self.tabActionTypes.setObjectName(_fromUtf8("tabActionTypes"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabActionTypes)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeActionTypeGroups = QtGui.QTreeView(self.tabActionTypes)
        self.treeActionTypeGroups.setObjectName(_fromUtf8("treeActionTypeGroups"))
        self.verticalLayout.addWidget(self.treeActionTypeGroups)
        self.tabWgtActionTypes.addTab(self.tabActionTypes, _fromUtf8(""))
        self.tabActionTypesTemplates = QtGui.QWidget()
        self.tabActionTypesTemplates.setObjectName(_fromUtf8("tabActionTypesTemplates"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabActionTypesTemplates)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.edtFindTemplates = QtGui.QLineEdit(self.tabActionTypesTemplates)
        self.edtFindTemplates.setObjectName(_fromUtf8("edtFindTemplates"))
        self.gridLayout_3.addWidget(self.edtFindTemplates, 0, 3, 1, 1)
        self.tblTemplates = CTableView(self.tabActionTypesTemplates)
        self.tblTemplates.setObjectName(_fromUtf8("tblTemplates"))
        self.gridLayout_3.addWidget(self.tblTemplates, 1, 1, 1, 3)
        self.btnFindTemplates = QtGui.QPushButton(self.tabActionTypesTemplates)
        self.btnFindTemplates.setObjectName(_fromUtf8("btnFindTemplates"))
        self.gridLayout_3.addWidget(self.btnFindTemplates, 0, 1, 1, 2)
        self.tabWgtActionTypes.addTab(self.tabActionTypesTemplates, _fromUtf8(""))
        self.tblActionTypes = CTableView(self.splitter)
        self.tblActionTypes.setObjectName(_fromUtf8("tblActionTypes"))
        self.verticalLayout_5.addWidget(self.splitter)
        self.gridLayout_2.addWidget(self.splitter_2, 2, 0, 1, 4)
        self.pnlWidgets = QtGui.QWidget(ActionTypesSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlWidgets.sizePolicy().hasHeightForWidth())
        self.pnlWidgets.setSizePolicy(sizePolicy)
        self.pnlWidgets.setObjectName(_fromUtf8("pnlWidgets"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.pnlWidgets)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblDeposit = QtGui.QLabel(self.pnlWidgets)
        self.lblDeposit.setText(_fromUtf8(""))
        self.lblDeposit.setObjectName(_fromUtf8("lblDeposit"))
        self.horizontalLayout_2.addWidget(self.lblDeposit)
        self.lblSelectedCount = QtGui.QLabel(self.pnlWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSelectedCount.sizePolicy().hasHeightForWidth())
        self.lblSelectedCount.setSizePolicy(sizePolicy)
        self.lblSelectedCount.setObjectName(_fromUtf8("lblSelectedCount"))
        self.horizontalLayout_2.addWidget(self.lblSelectedCount)
        self.lblFindByCode = QtGui.QLabel(self.pnlWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFindByCode.sizePolicy().hasHeightForWidth())
        self.lblFindByCode.setSizePolicy(sizePolicy)
        self.lblFindByCode.setObjectName(_fromUtf8("lblFindByCode"))
        self.horizontalLayout_2.addWidget(self.lblFindByCode)
        self.edtFindByCode = QtGui.QLineEdit(self.pnlWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFindByCode.sizePolicy().hasHeightForWidth())
        self.edtFindByCode.setSizePolicy(sizePolicy)
        self.edtFindByCode.setObjectName(_fromUtf8("edtFindByCode"))
        self.horizontalLayout_2.addWidget(self.edtFindByCode)
        self.gridLayout_2.addWidget(self.pnlWidgets, 3, 0, 1, 1)
        self.line = QtGui.QFrame(ActionTypesSelectorDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 4)
        self.edtFindFilter = QtGui.QLineEdit(ActionTypesSelectorDialog)
        self.edtFindFilter.setEnabled(False)
        self.edtFindFilter.setObjectName(_fromUtf8("edtFindFilter"))
        self.gridLayout_2.addWidget(self.edtFindFilter, 3, 2, 1, 1)

        self.retranslateUi(ActionTypesSelectorDialog)
        self.tabWgtActionTypes.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTypesSelectorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTypesSelectorDialog.reject)
        QtCore.QObject.connect(self.chkMes, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkIsNecessary.setEnabled)
        QtCore.QObject.connect(self.chkPlanner, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbSpeciality.setEnabled)
        QtCore.QObject.connect(self.chkOrgStructure, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbOrgStructure.setEnabled)
        QtCore.QObject.connect(self.chkPriceList, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbPriceListContract.setEnabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindFilter.setEnabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindByCode.setDisabled)
        QtCore.QObject.connect(self.chkCSG, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbCSG.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ActionTypesSelectorDialog)
        ActionTypesSelectorDialog.setTabOrder(self.chkOnlyNotExists, self.chkContract)
        ActionTypesSelectorDialog.setTabOrder(self.chkContract, self.chkPreferable)
        ActionTypesSelectorDialog.setTabOrder(self.chkPreferable, self.chkSexAndAge)
        ActionTypesSelectorDialog.setTabOrder(self.chkSexAndAge, self.chkPriceList)
        ActionTypesSelectorDialog.setTabOrder(self.chkPriceList, self.cmbPriceListContract)
        ActionTypesSelectorDialog.setTabOrder(self.cmbPriceListContract, self.chkContractTariffLimitations)
        ActionTypesSelectorDialog.setTabOrder(self.chkContractTariffLimitations, self.chkOrgStructure)
        ActionTypesSelectorDialog.setTabOrder(self.chkOrgStructure, self.cmbOrgStructure)
        ActionTypesSelectorDialog.setTabOrder(self.cmbOrgStructure, self.chkNomenclative)
        ActionTypesSelectorDialog.setTabOrder(self.chkNomenclative, self.chkMes)
        ActionTypesSelectorDialog.setTabOrder(self.chkMes, self.chkCSG)
        ActionTypesSelectorDialog.setTabOrder(self.chkCSG, self.cmbCSG)
        ActionTypesSelectorDialog.setTabOrder(self.cmbCSG, self.chkIsNecessary)
        ActionTypesSelectorDialog.setTabOrder(self.chkIsNecessary, self.chkAmountFromMES)
        ActionTypesSelectorDialog.setTabOrder(self.chkAmountFromMES, self.chkPlanner)
        ActionTypesSelectorDialog.setTabOrder(self.chkPlanner, self.cmbSpeciality)
        ActionTypesSelectorDialog.setTabOrder(self.cmbSpeciality, self.tblSelectedActionTypes)
        ActionTypesSelectorDialog.setTabOrder(self.tblSelectedActionTypes, self.tblExistsClientActions)
        ActionTypesSelectorDialog.setTabOrder(self.tblExistsClientActions, self.tabWgtActionTypes)
        ActionTypesSelectorDialog.setTabOrder(self.tabWgtActionTypes, self.treeActionTypeGroups)
        ActionTypesSelectorDialog.setTabOrder(self.treeActionTypeGroups, self.btnFindTemplates)
        ActionTypesSelectorDialog.setTabOrder(self.btnFindTemplates, self.edtFindTemplates)
        ActionTypesSelectorDialog.setTabOrder(self.edtFindTemplates, self.tblTemplates)
        ActionTypesSelectorDialog.setTabOrder(self.tblTemplates, self.tblActionTypes)
        ActionTypesSelectorDialog.setTabOrder(self.tblActionTypes, self.edtFindByCode)
        ActionTypesSelectorDialog.setTabOrder(self.edtFindByCode, self.chkFindFilter)
        ActionTypesSelectorDialog.setTabOrder(self.chkFindFilter, self.edtFindFilter)
        ActionTypesSelectorDialog.setTabOrder(self.edtFindFilter, self.buttonBox)

    def retranslateUi(self, ActionTypesSelectorDialog):
        ActionTypesSelectorDialog.setWindowTitle(_translate("ActionTypesSelectorDialog", "Выберите действия", None))
        self.chkFindFilter.setText(_translate("ActionTypesSelectorDialog", "Фильтр", None))
        self.chkOrgStructure.setText(_translate("ActionTypesSelectorDialog", "П&одразделение", None))
        self.chkMes.setText(_translate("ActionTypesSelectorDialog", "&МЭС", None))
        self.chkNomenclative.setText(_translate("ActionTypesSelectorDialog", "&Номенклатура", None))
        self.chkContract.setText(_translate("ActionTypesSelectorDialog", "&Договор", None))
        self.chkContractTariffLimitations.setText(_translate("ActionTypesSelectorDialog", "Ограничения", None))
        self.chkSexAndAge.setText(_translate("ActionTypesSelectorDialog", "&Пол и возраст", None))
        self.chkPriceList.setText(_translate("ActionTypesSelectorDialog", "Прайс-лист", None))
        self.chkCSG.setText(_translate("ActionTypesSelectorDialog", "КСГ", None))
        self.chkPreferable.setText(_translate("ActionTypesSelectorDialog", "П&редпочтение", None))
        self.chkOnlyNotExists.setText(_translate("ActionTypesSelectorDialog", "Отсутствующие", None))
        self.chkIsNecessary.setText(_translate("ActionTypesSelectorDialog", "Необходимо", None))
        self.chkAmountFromMES.setText(_translate("ActionTypesSelectorDialog", "Количество из МЭС", None))
        self.chkPlanner.setText(_translate("ActionTypesSelectorDialog", "П&ланировщик", None))
        self.lblSelectedActionTypes.setText(_translate("ActionTypesSelectorDialog", "Назначить", None))
        self.lblExistsClientActions.setText(_translate("ActionTypesSelectorDialog", "Назначено", None))
        self.tblExistsClientActions.setToolTip(_translate("ActionTypesSelectorDialog", "Список ранее назначенных мероприятий", None))
        self.tabWgtActionTypes.setTabText(self.tabWgtActionTypes.indexOf(self.tabActionTypes), _translate("ActionTypesSelectorDialog", "Типы мероприятий", None))
        self.btnFindTemplates.setText(_translate("ActionTypesSelectorDialog", "Поиск", None))
        self.tabWgtActionTypes.setTabText(self.tabWgtActionTypes.indexOf(self.tabActionTypesTemplates), _translate("ActionTypesSelectorDialog", "Шаблоны", None))
        self.lblSelectedCount.setText(_translate("ActionTypesSelectorDialog", "Количество выбранных", None))
        self.lblFindByCode.setText(_translate("ActionTypesSelectorDialog", "| Поиск по коду или наименованию", None))

from Events.ActionsSelectorSelectedTable import CCheckedActionsTableView
from Events.Utils import CActionCSGComboBox
from Orgs.OrgComboBox import CIndependentContractComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActionTypesSelectorDialog = QtGui.QDialog()
    ui = Ui_ActionTypesSelectorDialog()
    ui.setupUi(ActionTypesSelectorDialog)
    ActionTypesSelectorDialog.show()
    sys.exit(app.exec_())

