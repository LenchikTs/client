# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\TreesPage.ui'
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

class Ui_treesPage(object):
    def setupUi(self, treesPage):
        treesPage.setObjectName(_fromUtf8("treesPage"))
        treesPage.resize(402, 300)
        self.gridLayout = QtGui.QGridLayout(treesPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtActionTypeTreeExpand = QtGui.QSpinBox(treesPage)
        self.edtActionTypeTreeExpand.setMinimum(1)
        self.edtActionTypeTreeExpand.setObjectName(_fromUtf8("edtActionTypeTreeExpand"))
        self.gridLayout.addWidget(self.edtActionTypeTreeExpand, 1, 2, 1, 1)
        self.edtActionTemplateTreeExpand = QtGui.QSpinBox(treesPage)
        self.edtActionTemplateTreeExpand.setMinimum(1)
        self.edtActionTemplateTreeExpand.setObjectName(_fromUtf8("edtActionTemplateTreeExpand"))
        self.gridLayout.addWidget(self.edtActionTemplateTreeExpand, 3, 2, 1, 1)
        self.cmbActionTypeTreeExpand = QtGui.QComboBox(treesPage)
        self.cmbActionTypeTreeExpand.setObjectName(_fromUtf8("cmbActionTypeTreeExpand"))
        self.cmbActionTypeTreeExpand.addItem(_fromUtf8(""))
        self.cmbActionTypeTreeExpand.addItem(_fromUtf8(""))
        self.cmbActionTypeTreeExpand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbActionTypeTreeExpand, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(128, 217, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.cmbActionTemplateTreeExpand = QtGui.QComboBox(treesPage)
        self.cmbActionTemplateTreeExpand.setObjectName(_fromUtf8("cmbActionTemplateTreeExpand"))
        self.cmbActionTemplateTreeExpand.addItem(_fromUtf8(""))
        self.cmbActionTemplateTreeExpand.addItem(_fromUtf8(""))
        self.cmbActionTemplateTreeExpand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbActionTemplateTreeExpand, 3, 1, 1, 1)
        self.lblActionTemplateTreeExpand = QtGui.QLabel(treesPage)
        self.lblActionTemplateTreeExpand.setObjectName(_fromUtf8("lblActionTemplateTreeExpand"))
        self.gridLayout.addWidget(self.lblActionTemplateTreeExpand, 3, 0, 1, 1)
        self.lblTreeProbes = QtGui.QLabel(treesPage)
        self.lblTreeProbes.setObjectName(_fromUtf8("lblTreeProbes"))
        self.gridLayout.addWidget(self.lblTreeProbes, 2, 0, 1, 1)
        self.edtProbesTreeExpand = QtGui.QSpinBox(treesPage)
        self.edtProbesTreeExpand.setMinimum(1)
        self.edtProbesTreeExpand.setObjectName(_fromUtf8("edtProbesTreeExpand"))
        self.gridLayout.addWidget(self.edtProbesTreeExpand, 2, 2, 1, 1)
        self.cmbProbesTreeExpand = QtGui.QComboBox(treesPage)
        self.cmbProbesTreeExpand.setObjectName(_fromUtf8("cmbProbesTreeExpand"))
        self.cmbProbesTreeExpand.addItem(_fromUtf8(""))
        self.cmbProbesTreeExpand.addItem(_fromUtf8(""))
        self.cmbProbesTreeExpand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbProbesTreeExpand, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(17, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.edtTreeOrgStructureExpand = QtGui.QSpinBox(treesPage)
        self.edtTreeOrgStructureExpand.setMinimum(1)
        self.edtTreeOrgStructureExpand.setObjectName(_fromUtf8("edtTreeOrgStructureExpand"))
        self.gridLayout.addWidget(self.edtTreeOrgStructureExpand, 0, 2, 1, 1)
        self.cmbTreeOrgStructureExpand = QtGui.QComboBox(treesPage)
        self.cmbTreeOrgStructureExpand.setObjectName(_fromUtf8("cmbTreeOrgStructureExpand"))
        self.cmbTreeOrgStructureExpand.addItem(_fromUtf8(""))
        self.cmbTreeOrgStructureExpand.addItem(_fromUtf8(""))
        self.cmbTreeOrgStructureExpand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTreeOrgStructureExpand, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(17, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.lblTreeOrgStructure = QtGui.QLabel(treesPage)
        self.lblTreeOrgStructure.setObjectName(_fromUtf8("lblTreeOrgStructure"))
        self.gridLayout.addWidget(self.lblTreeOrgStructure, 0, 0, 1, 1)
        self.lblActionType = QtGui.QLabel(treesPage)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 1, 0, 1, 1)
        self.lblTreeContracts = QtGui.QLabel(treesPage)
        self.lblTreeContracts.setObjectName(_fromUtf8("lblTreeContracts"))
        self.gridLayout.addWidget(self.lblTreeContracts, 4, 0, 1, 1)
        self.cmbContractsTreeExpand = QtGui.QComboBox(treesPage)
        self.cmbContractsTreeExpand.setObjectName(_fromUtf8("cmbContractsTreeExpand"))
        self.cmbContractsTreeExpand.addItem(_fromUtf8(""))
        self.cmbContractsTreeExpand.addItem(_fromUtf8(""))
        self.cmbContractsTreeExpand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbContractsTreeExpand, 4, 1, 1, 1)
        self.edtContractsTreeExpand = QtGui.QSpinBox(treesPage)
        self.edtContractsTreeExpand.setMinimum(1)
        self.edtContractsTreeExpand.setObjectName(_fromUtf8("edtContractsTreeExpand"))
        self.gridLayout.addWidget(self.edtContractsTreeExpand, 4, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(17, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 3, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(17, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 3, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(17, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 4, 3, 1, 1)
        self.lblTreeProbes.setBuddy(self.cmbProbesTreeExpand)
        self.lblTreeOrgStructure.setBuddy(self.cmbTreeOrgStructureExpand)
        self.lblActionType.setBuddy(self.cmbActionTypeTreeExpand)

        self.retranslateUi(treesPage)
        QtCore.QMetaObject.connectSlotsByName(treesPage)
        treesPage.setTabOrder(self.cmbTreeOrgStructureExpand, self.edtTreeOrgStructureExpand)
        treesPage.setTabOrder(self.edtTreeOrgStructureExpand, self.cmbActionTypeTreeExpand)
        treesPage.setTabOrder(self.cmbActionTypeTreeExpand, self.edtActionTypeTreeExpand)
        treesPage.setTabOrder(self.edtActionTypeTreeExpand, self.cmbProbesTreeExpand)
        treesPage.setTabOrder(self.cmbProbesTreeExpand, self.edtProbesTreeExpand)

    def retranslateUi(self, treesPage):
        treesPage.setWindowTitle(_translate("treesPage", "Деревья (ui)", None))
        self.cmbActionTypeTreeExpand.setItemText(0, _translate("treesPage", "Полностью свернуто", None))
        self.cmbActionTypeTreeExpand.setItemText(1, _translate("treesPage", "Полностью развернуто", None))
        self.cmbActionTypeTreeExpand.setItemText(2, _translate("treesPage", "Развернуто на уровень", None))
        self.cmbActionTemplateTreeExpand.setItemText(0, _translate("treesPage", "Полностью свернуто", None))
        self.cmbActionTemplateTreeExpand.setItemText(1, _translate("treesPage", "Полностью развернуто", None))
        self.cmbActionTemplateTreeExpand.setItemText(2, _translate("treesPage", "Развернуто на уровень", None))
        self.lblActionTemplateTreeExpand.setText(_translate("treesPage", "Шаблоны действий", None))
        self.lblTreeProbes.setText(_translate("treesPage", "&Пробы", None))
        self.cmbProbesTreeExpand.setItemText(0, _translate("treesPage", "Полностью свернуто", None))
        self.cmbProbesTreeExpand.setItemText(1, _translate("treesPage", "Полностью развернуто", None))
        self.cmbProbesTreeExpand.setItemText(2, _translate("treesPage", "Развернуто на уровень", None))
        self.cmbTreeOrgStructureExpand.setItemText(0, _translate("treesPage", "Полностью свернуто", None))
        self.cmbTreeOrgStructureExpand.setItemText(1, _translate("treesPage", "Полностью развернуто", None))
        self.cmbTreeOrgStructureExpand.setItemText(2, _translate("treesPage", "Развернуто на уровень", None))
        self.lblTreeOrgStructure.setText(_translate("treesPage", "&Структура организации", None))
        self.lblActionType.setText(_translate("treesPage", "&Типы действий", None))
        self.lblTreeContracts.setText(_translate("treesPage", "Договоры", None))
        self.cmbContractsTreeExpand.setItemText(0, _translate("treesPage", "Полностью свернуто", None))
        self.cmbContractsTreeExpand.setItemText(1, _translate("treesPage", "Полностью развернуто", None))
        self.cmbContractsTreeExpand.setItemText(2, _translate("treesPage", "Развернуто на уровень", None))

