# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\RefBooks\ActionTemplate\ActionTemplateListDialog.ui'
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

class Ui_ActionTemplateListDialog(object):
    def setupUi(self, ActionTemplateListDialog):
        ActionTemplateListDialog.setObjectName(_fromUtf8("ActionTemplateListDialog"))
        ActionTemplateListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ActionTemplateListDialog.resize(582, 678)
        ActionTemplateListDialog.setSizeGripEnabled(True)
        ActionTemplateListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ActionTemplateListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlTree = QtGui.QWidget(self.splitter)
        self.pnlTree.setObjectName(_fromUtf8("pnlTree"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlTree)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblPadding = QtGui.QLabel(self.pnlTree)
        self.lblPadding.setText(_fromUtf8(""))
        self.lblPadding.setObjectName(_fromUtf8("lblPadding"))
        self.verticalLayout.addWidget(self.lblPadding)
        self.treeItems = CTreeView(self.pnlTree)
        self.treeItems.setObjectName(_fromUtf8("treeItems"))
        self.verticalLayout.addWidget(self.treeItems)
        self.pnlList = QtGui.QWidget(self.splitter)
        self.pnlList.setObjectName(_fromUtf8("pnlList"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlList)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblItems = CTableView(self.pnlList)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.verticalLayout_2.addWidget(self.tblItems)
        self.lblCountRows = QtGui.QLabel(self.pnlList)
        self.lblCountRows.setText(_fromUtf8(""))
        self.lblCountRows.setObjectName(_fromUtf8("lblCountRows"))
        self.verticalLayout_2.addWidget(self.lblCountRows)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 4, 1, 1)
        self.statusBar = QtGui.QStatusBar(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 9, 0, 1, 3)
        self.lblPerson = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPerson.sizePolicy().hasHeightForWidth())
        self.lblPerson.setSizePolicy(sizePolicy)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 3, 0, 1, 1)
        self.lblCreatePerson = QtGui.QLabel(ActionTemplateListDialog)
        self.lblCreatePerson.setObjectName(_fromUtf8("lblCreatePerson"))
        self.gridLayout.addWidget(self.lblCreatePerson, 5, 0, 1, 1)
        self.edtBegCreateDate = CDateEdit(ActionTemplateListDialog)
        self.edtBegCreateDate.setCalendarPopup(True)
        self.edtBegCreateDate.setObjectName(_fromUtf8("edtBegCreateDate"))
        self.gridLayout.addWidget(self.edtBegCreateDate, 6, 1, 1, 1)
        self.lblCreateDate = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCreateDate.sizePolicy().hasHeightForWidth())
        self.lblCreateDate.setSizePolicy(sizePolicy)
        self.lblCreateDate.setObjectName(_fromUtf8("lblCreateDate"))
        self.gridLayout.addWidget(self.lblCreateDate, 6, 0, 1, 1)
        self.lblForCreateDate = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblForCreateDate.sizePolicy().hasHeightForWidth())
        self.lblForCreateDate.setSizePolicy(sizePolicy)
        self.lblForCreateDate.setObjectName(_fromUtf8("lblForCreateDate"))
        self.gridLayout.addWidget(self.lblForCreateDate, 6, 2, 1, 1)
        self.edtEndCreateDate = CDateEdit(ActionTemplateListDialog)
        self.edtEndCreateDate.setCalendarPopup(True)
        self.edtEndCreateDate.setObjectName(_fromUtf8("edtEndCreateDate"))
        self.gridLayout.addWidget(self.edtEndCreateDate, 6, 3, 1, 1)
        self.lblActionType = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblActionType.sizePolicy().hasHeightForWidth())
        self.lblActionType.setSizePolicy(sizePolicy)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 1, 0, 1, 1)
        self.lblSpeciality = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSpeciality.sizePolicy().hasHeightForWidth())
        self.lblSpeciality.setSizePolicy(sizePolicy)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnFind = QtGui.QPushButton(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFind.sizePolicy().hasHeightForWidth())
        self.btnFind.setSizePolicy(sizePolicy)
        self.btnFind.setObjectName(_fromUtf8("btnFind"))
        self.hboxlayout.addWidget(self.btnFind)
        self.btnSelect = QtGui.QPushButton(ActionTemplateListDialog)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.hboxlayout.addWidget(self.btnSelect)
        self.btnFilter = QtGui.QPushButton(ActionTemplateListDialog)
        self.btnFilter.setObjectName(_fromUtf8("btnFilter"))
        self.hboxlayout.addWidget(self.btnFilter)
        self.btnEdit = QtGui.QPushButton(ActionTemplateListDialog)
        self.btnEdit.setDefault(True)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnNew = QtGui.QPushButton(ActionTemplateListDialog)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.hboxlayout.addWidget(self.btnNew)
        self.btnCancel = QtGui.QPushButton(ActionTemplateListDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.hboxlayout, 8, 0, 1, 5)
        self.cmbCreatePerson = CPersonComboBoxEx(ActionTemplateListDialog)
        self.cmbCreatePerson.setObjectName(_fromUtf8("cmbCreatePerson"))
        self.gridLayout.addWidget(self.cmbCreatePerson, 5, 1, 1, 4)
        self.cmbPerson = CPersonComboBoxEx(ActionTemplateListDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 3, 1, 1, 4)
        self.cmbSpeciality = CRBComboBox(ActionTemplateListDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 2, 1, 1, 4)
        self.cmbActionType = CActionTypeComboBoxEx(ActionTemplateListDialog)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 1, 1, 1, 4)
        self.lblSNILS = QtGui.QLabel(ActionTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSNILS.sizePolicy().hasHeightForWidth())
        self.lblSNILS.setSizePolicy(sizePolicy)
        self.lblSNILS.setObjectName(_fromUtf8("lblSNILS"))
        self.gridLayout.addWidget(self.lblSNILS, 4, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 2)
        self.edtSNILS = QtGui.QLineEdit(ActionTemplateListDialog)
        self.edtSNILS.setObjectName(_fromUtf8("edtSNILS"))
        self.gridLayout.addWidget(self.edtSNILS, 4, 1, 1, 2)

        self.retranslateUi(ActionTemplateListDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), ActionTemplateListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTemplateListDialog)
        ActionTemplateListDialog.setTabOrder(self.treeItems, self.tblItems)
        ActionTemplateListDialog.setTabOrder(self.tblItems, self.cmbActionType)
        ActionTemplateListDialog.setTabOrder(self.cmbActionType, self.cmbSpeciality)
        ActionTemplateListDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        ActionTemplateListDialog.setTabOrder(self.cmbPerson, self.cmbCreatePerson)
        ActionTemplateListDialog.setTabOrder(self.cmbCreatePerson, self.edtBegCreateDate)
        ActionTemplateListDialog.setTabOrder(self.edtBegCreateDate, self.edtEndCreateDate)
        ActionTemplateListDialog.setTabOrder(self.edtEndCreateDate, self.btnFind)
        ActionTemplateListDialog.setTabOrder(self.btnFind, self.btnSelect)
        ActionTemplateListDialog.setTabOrder(self.btnSelect, self.btnFilter)
        ActionTemplateListDialog.setTabOrder(self.btnFilter, self.btnEdit)
        ActionTemplateListDialog.setTabOrder(self.btnEdit, self.btnNew)
        ActionTemplateListDialog.setTabOrder(self.btnNew, self.btnCancel)

    def retranslateUi(self, ActionTemplateListDialog):
        ActionTemplateListDialog.setWindowTitle(_translate("ActionTemplateListDialog", "Список записей", None))
        self.tblItems.setWhatsThis(_translate("ActionTemplateListDialog", "список записей", "ура!"))
        self.statusBar.setToolTip(_translate("ActionTemplateListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ActionTemplateListDialog", "A status bar.", None))
        self.lblPerson.setText(_translate("ActionTemplateListDialog", "Врач", None))
        self.lblCreatePerson.setText(_translate("ActionTemplateListDialog", "Автор записи", None))
        self.edtBegCreateDate.setDisplayFormat(_translate("ActionTemplateListDialog", "dd.MM.yyyy", None))
        self.lblCreateDate.setText(_translate("ActionTemplateListDialog", "Дата создания с", None))
        self.lblForCreateDate.setText(_translate("ActionTemplateListDialog", "по", None))
        self.edtEndCreateDate.setDisplayFormat(_translate("ActionTemplateListDialog", "dd.MM.yyyy", None))
        self.lblActionType.setText(_translate("ActionTemplateListDialog", "Тип действия", None))
        self.lblSpeciality.setText(_translate("ActionTemplateListDialog", "Специальность", None))
        self.btnFind.setText(_translate("ActionTemplateListDialog", "Поиск", None))
        self.btnSelect.setWhatsThis(_translate("ActionTemplateListDialog", "выбрать текущую запись", None))
        self.btnSelect.setText(_translate("ActionTemplateListDialog", "Выбор", None))
        self.btnFilter.setWhatsThis(_translate("ActionTemplateListDialog", "изменить условие отбора записей для показа в списке", None))
        self.btnFilter.setText(_translate("ActionTemplateListDialog", "Фильтр", None))
        self.btnEdit.setWhatsThis(_translate("ActionTemplateListDialog", "изменить текущую запись", None))
        self.btnEdit.setText(_translate("ActionTemplateListDialog", "Правка F4", None))
        self.btnEdit.setShortcut(_translate("ActionTemplateListDialog", "F4", None))
        self.btnNew.setWhatsThis(_translate("ActionTemplateListDialog", "добавить новую запись", None))
        self.btnNew.setText(_translate("ActionTemplateListDialog", "Вставка F9", None))
        self.btnNew.setShortcut(_translate("ActionTemplateListDialog", "F9", None))
        self.btnCancel.setWhatsThis(_translate("ActionTemplateListDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("ActionTemplateListDialog", "Закрыть", None))
        self.lblSNILS.setText(_translate("ActionTemplateListDialog", "СНИЛС", None))
        self.edtSNILS.setInputMask(_translate("ActionTemplateListDialog", "999-999-999 99; ", None))

from Events.ActionTypeComboBoxEx import CActionTypeComboBoxEx
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.TableView import CTableView
from library.TreeView import CTreeView
from library.crbcombobox import CRBComboBox