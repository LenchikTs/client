# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\RefBooks\ActionTypeGroup\RBActionTypeSelectorDialog.ui'
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

class Ui_ActionTypeSelectorDialog(object):
    def setupUi(self, ActionTypeSelectorDialog):
        ActionTypeSelectorDialog.setObjectName(_fromUtf8("ActionTypeSelectorDialog"))
        ActionTypeSelectorDialog.resize(1019, 450)
        ActionTypeSelectorDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ActionTypeSelectorDialog)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(ActionTypeSelectorDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeItems = CTreeView(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeItems.sizePolicy().hasHeightForWidth())
        self.treeItems.setSizePolicy(sizePolicy)
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.verticalLayout.addWidget(self.treeItems)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblService = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblService.setObjectName(_fromUtf8("lblService"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblService)
        self.cmbService = CRBComboBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbService.sizePolicy().hasHeightForWidth())
        self.cmbService.setSizePolicy(sizePolicy)
        self.cmbService.setObjectName(_fromUtf8("cmbService"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbService)
        self.lblQuotaType = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblQuotaType.setObjectName(_fromUtf8("lblQuotaType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblQuotaType)
        self.cmbQuotaType = CRBComboBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbQuotaType.sizePolicy().hasHeightForWidth())
        self.cmbQuotaType.setSizePolicy(sizePolicy)
        self.cmbQuotaType.setObjectName(_fromUtf8("cmbQuotaType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmbQuotaType)
        self.lblTissueType = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblTissueType.setObjectName(_fromUtf8("lblTissueType"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblTissueType)
        self.cmbTissueType = CRBComboBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTissueType.sizePolicy().hasHeightForWidth())
        self.cmbTissueType.setSizePolicy(sizePolicy)
        self.cmbTissueType.setObjectName(_fromUtf8("cmbTissueType"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmbTissueType)
        self.lblServiceType = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblServiceType.setObjectName(_fromUtf8("lblServiceType"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lblServiceType)
        self.cmbServiceType = CActionServiceTypeComboBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbServiceType.sizePolicy().hasHeightForWidth())
        self.cmbServiceType.setSizePolicy(sizePolicy)
        self.cmbServiceType.setObjectName(_fromUtf8("cmbServiceType"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmbServiceType)
        self.lblIsPreferable = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblIsPreferable.setObjectName(_fromUtf8("lblIsPreferable"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.lblIsPreferable)
        self.cmbIsPreferable = CComboBoxWithKeyEventHandler(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbIsPreferable.sizePolicy().hasHeightForWidth())
        self.cmbIsPreferable.setSizePolicy(sizePolicy)
        self.cmbIsPreferable.setObjectName(_fromUtf8("cmbIsPreferable"))
        self.cmbIsPreferable.addItem(_fromUtf8(""))
        self.cmbIsPreferable.addItem(_fromUtf8(""))
        self.cmbIsPreferable.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cmbIsPreferable)
        self.lblShowInForm = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblShowInForm.setObjectName(_fromUtf8("lblShowInForm"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.lblShowInForm)
        self.cmbShowInForm = CComboBoxWithKeyEventHandler(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbShowInForm.sizePolicy().hasHeightForWidth())
        self.cmbShowInForm.setSizePolicy(sizePolicy)
        self.cmbShowInForm.setObjectName(_fromUtf8("cmbShowInForm"))
        self.cmbShowInForm.addItem(_fromUtf8(""))
        self.cmbShowInForm.addItem(_fromUtf8(""))
        self.cmbShowInForm.addItem(_fromUtf8(""))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.cmbShowInForm)
        self.verticalLayout.addLayout(self.formLayout)
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblItems = CTableView(self.layoutWidget)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 3)
        self.lblCountRows = QtGui.QLabel(self.layoutWidget)
        self.lblCountRows.setText(_fromUtf8(""))
        self.lblCountRows.setObjectName(_fromUtf8("lblCountRows"))
        self.gridLayout.addWidget(self.lblCountRows, 1, 0, 1, 1)
        self.lblCountSelectedRows = QtGui.QLabel(self.layoutWidget)
        self.lblCountSelectedRows.setText(_fromUtf8(""))
        self.lblCountSelectedRows.setObjectName(_fromUtf8("lblCountSelectedRows"))
        self.gridLayout.addWidget(self.lblCountSelectedRows, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.itemSelectBox = CTableView(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemSelectBox.sizePolicy().hasHeightForWidth())
        self.itemSelectBox.setSizePolicy(sizePolicy)
        self.itemSelectBox.setObjectName(_fromUtf8("itemSelectBox"))
        self.verticalLayout_2.addWidget(self.itemSelectBox)
        self.verticalLayout_3.addWidget(self.splitter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnFind = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnFind.setObjectName(_fromUtf8("btnFind"))
        self.horizontalLayout_2.addWidget(self.btnFind)
        self.btnAddItemToSelectBox = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnAddItemToSelectBox.setObjectName(_fromUtf8("btnAddItemToSelectBox"))
        self.horizontalLayout_2.addWidget(self.btnAddItemToSelectBox)
        self.btnRemoveItemFromSelectBox = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnRemoveItemFromSelectBox.setObjectName(_fromUtf8("btnRemoveItemFromSelectBox"))
        self.horizontalLayout_2.addWidget(self.btnRemoveItemFromSelectBox)
        self.btnSelect = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.horizontalLayout_2.addWidget(self.btnSelect)
        self.btnFilter = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnFilter.setObjectName(_fromUtf8("btnFilter"))
        self.horizontalLayout_2.addWidget(self.btnFilter)
        self.btnEdit = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.horizontalLayout_2.addWidget(self.btnEdit)
        self.btnNew = QtGui.QPushButton(ActionTypeSelectorDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout_2.addWidget(self.btnNew)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.splitter.raise_()
        self.lblService.setBuddy(self.cmbService)
        self.lblQuotaType.setBuddy(self.cmbQuotaType)
        self.lblTissueType.setBuddy(self.cmbTissueType)
        self.lblServiceType.setBuddy(self.cmbServiceType)
        self.lblIsPreferable.setBuddy(self.cmbIsPreferable)
        self.lblShowInForm.setBuddy(self.cmbShowInForm)
        self.label.setBuddy(self.itemSelectBox)

        self.retranslateUi(ActionTypeSelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(ActionTypeSelectorDialog)
        ActionTypeSelectorDialog.setTabOrder(self.treeItems, self.cmbService)
        ActionTypeSelectorDialog.setTabOrder(self.cmbService, self.cmbQuotaType)
        ActionTypeSelectorDialog.setTabOrder(self.cmbQuotaType, self.cmbTissueType)
        ActionTypeSelectorDialog.setTabOrder(self.cmbTissueType, self.cmbServiceType)
        ActionTypeSelectorDialog.setTabOrder(self.cmbServiceType, self.cmbIsPreferable)
        ActionTypeSelectorDialog.setTabOrder(self.cmbIsPreferable, self.cmbShowInForm)
        ActionTypeSelectorDialog.setTabOrder(self.cmbShowInForm, self.tblItems)
        ActionTypeSelectorDialog.setTabOrder(self.tblItems, self.itemSelectBox)
        ActionTypeSelectorDialog.setTabOrder(self.itemSelectBox, self.btnAddItemToSelectBox)
        ActionTypeSelectorDialog.setTabOrder(self.btnAddItemToSelectBox, self.btnSelect)
        ActionTypeSelectorDialog.setTabOrder(self.btnSelect, self.btnFilter)
        ActionTypeSelectorDialog.setTabOrder(self.btnFilter, self.btnEdit)
        ActionTypeSelectorDialog.setTabOrder(self.btnEdit, self.btnNew)

    def retranslateUi(self, ActionTypeSelectorDialog):
        ActionTypeSelectorDialog.setWindowTitle(_translate("ActionTypeSelectorDialog", "Dialog", None))
        self.lblService.setText(_translate("ActionTypeSelectorDialog", "Профиль оплаты", None))
        self.lblQuotaType.setText(_translate("ActionTypeSelectorDialog", "Вид квоты", None))
        self.lblTissueType.setText(_translate("ActionTypeSelectorDialog", "Тип биоматериала", None))
        self.lblServiceType.setText(_translate("ActionTypeSelectorDialog", "Вид услуги", None))
        self.lblIsPreferable.setText(_translate("ActionTypeSelectorDialog", "Является предпочитаемым(-ой)", None))
        self.cmbIsPreferable.setItemText(0, _translate("ActionTypeSelectorDialog", "не определено", None))
        self.cmbIsPreferable.setItemText(1, _translate("ActionTypeSelectorDialog", "да", None))
        self.cmbIsPreferable.setItemText(2, _translate("ActionTypeSelectorDialog", "нет", None))
        self.lblShowInForm.setText(_translate("ActionTypeSelectorDialog", "Разрешается выбор в формах ввода событий", None))
        self.cmbShowInForm.setItemText(0, _translate("ActionTypeSelectorDialog", "не определено", None))
        self.cmbShowInForm.setItemText(1, _translate("ActionTypeSelectorDialog", "да", None))
        self.cmbShowInForm.setItemText(2, _translate("ActionTypeSelectorDialog", "нет", None))
        self.label.setText(_translate("ActionTypeSelectorDialog", "Выбранные:", None))
        self.btnFind.setText(_translate("ActionTypeSelectorDialog", "Поиск", None))
        self.btnAddItemToSelectBox.setText(_translate("ActionTypeSelectorDialog", "Выбрать", None))
        self.btnRemoveItemFromSelectBox.setText(_translate("ActionTypeSelectorDialog", "Удалить", None))
        self.btnSelect.setText(_translate("ActionTypeSelectorDialog", "Добавить", None))
        self.btnFilter.setText(_translate("ActionTypeSelectorDialog", "Фильтр", None))
        self.btnEdit.setText(_translate("ActionTypeSelectorDialog", "Правка F4", None))
        self.btnNew.setText(_translate("ActionTypeSelectorDialog", "Вставка F9", None))

from Events.ActionServiceType import CActionServiceTypeComboBox
from RefBooks.ActionTypeGroup.ComboBoxWithEventHandler import CComboBoxWithKeyEventHandler
from library.TableView import CTableView
from library.TreeView import CTreeView
from library.crbcombobox import CRBComboBox