# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\NomenclatureExpense\NomenclatureExpenseLoadTemplate.ui'
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

class Ui_LoadTemplateDialog(object):
    def setupUi(self, LoadTemplateDialog):
        LoadTemplateDialog.setObjectName(_fromUtf8("LoadTemplateDialog"))
        LoadTemplateDialog.resize(949, 402)
        LoadTemplateDialog.setSizeGripEnabled(False)
        self.gridLayout_2 = QtGui.QGridLayout(LoadTemplateDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblMesInfo = QtGui.QLabel(LoadTemplateDialog)
        self.lblMesInfo.setText(_fromUtf8(""))
        self.lblMesInfo.setObjectName(_fromUtf8("lblMesInfo"))
        self.gridLayout_2.addWidget(self.lblMesInfo, 4, 0, 1, 1)
        self.line = QtGui.QFrame(LoadTemplateDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 5)
        self.pnlWidgets = QtGui.QWidget(LoadTemplateDialog)
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
        self.pnlFilter = QtGui.QWidget(LoadTemplateDialog)
        self.pnlFilter.setObjectName(_fromUtf8("pnlFilter"))
        self.gridLayout = QtGui.QGridLayout(self.pnlFilter)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbClass = QtGui.QComboBox(self.pnlFilter)
        self.cmbClass.setObjectName(_fromUtf8("cmbClass"))
        self.cmbClass.addItem(_fromUtf8(""))
        self.cmbClass.addItem(_fromUtf8(""))
        self.cmbClass.addItem(_fromUtf8(""))
        self.cmbClass.addItem(_fromUtf8(""))
        self.cmbClass.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbClass, 0, 1, 1, 1)
        self.lblClass = QtGui.QLabel(self.pnlFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblClass.sizePolicy().hasHeightForWidth())
        self.lblClass.setSizePolicy(sizePolicy)
        self.lblClass.setObjectName(_fromUtf8("lblClass"))
        self.gridLayout.addWidget(self.lblClass, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.pnlFilter, 0, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(LoadTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 4, 1, 1)
        self.edtFindFilter = QtGui.QLineEdit(LoadTemplateDialog)
        self.edtFindFilter.setEnabled(False)
        self.edtFindFilter.setObjectName(_fromUtf8("edtFindFilter"))
        self.gridLayout_2.addWidget(self.edtFindFilter, 3, 2, 1, 1)
        self.chkFindFilter = QtGui.QCheckBox(LoadTemplateDialog)
        self.chkFindFilter.setObjectName(_fromUtf8("chkFindFilter"))
        self.gridLayout_2.addWidget(self.chkFindFilter, 3, 1, 1, 1)
        self.splitter_2 = QtGui.QSplitter(LoadTemplateDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlSelectedActionTypes = QtGui.QWidget(self.splitter_2)
        self.pnlSelectedActionTypes.setObjectName(_fromUtf8("pnlSelectedActionTypes"))
        self.gridLayout_4 = QtGui.QGridLayout(self.pnlSelectedActionTypes)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pnlSelectedActionTypes_2 = QtGui.QWidget(self.pnlSelectedActionTypes)
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
        self.gridLayout_4.addWidget(self.pnlSelectedActionTypes_2, 0, 0, 1, 1)
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
        self.gridLayout_2.addWidget(self.splitter_2, 2, 0, 1, 5)
        self.btnUpdateTemplate = QtGui.QPushButton(LoadTemplateDialog)
        self.btnUpdateTemplate.setObjectName(_fromUtf8("btnUpdateTemplate"))
        self.gridLayout_2.addWidget(self.btnUpdateTemplate, 3, 3, 1, 1)
        self.chkFindFilter.raise_()
        self.buttonBox.raise_()
        self.lblMesInfo.raise_()
        self.splitter_2.raise_()
        self.pnlWidgets.raise_()
        self.line.raise_()
        self.edtFindFilter.raise_()
        self.pnlFilter.raise_()
        self.btnUpdateTemplate.raise_()

        self.retranslateUi(LoadTemplateDialog)
        self.tabWgtActionTypes.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LoadTemplateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoadTemplateDialog.reject)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindFilter.setEnabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindByCode.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(LoadTemplateDialog)
        LoadTemplateDialog.setTabOrder(self.tblSelectedActionTypes, self.tabWgtActionTypes)
        LoadTemplateDialog.setTabOrder(self.tabWgtActionTypes, self.btnFindTemplates)
        LoadTemplateDialog.setTabOrder(self.btnFindTemplates, self.edtFindTemplates)
        LoadTemplateDialog.setTabOrder(self.edtFindTemplates, self.tblTemplates)
        LoadTemplateDialog.setTabOrder(self.tblTemplates, self.tblActionTypes)
        LoadTemplateDialog.setTabOrder(self.tblActionTypes, self.edtFindByCode)
        LoadTemplateDialog.setTabOrder(self.edtFindByCode, self.chkFindFilter)
        LoadTemplateDialog.setTabOrder(self.chkFindFilter, self.edtFindFilter)
        LoadTemplateDialog.setTabOrder(self.edtFindFilter, self.btnUpdateTemplate)
        LoadTemplateDialog.setTabOrder(self.btnUpdateTemplate, self.buttonBox)
        LoadTemplateDialog.setTabOrder(self.buttonBox, self.cmbClass)

    def retranslateUi(self, LoadTemplateDialog):
        LoadTemplateDialog.setWindowTitle(_translate("LoadTemplateDialog", "Выберите шаблон", None))
        self.lblSelectedCount.setText(_translate("LoadTemplateDialog", "Количество выбранных", None))
        self.lblFindByCode.setText(_translate("LoadTemplateDialog", "| Поиск по коду или наименованию", None))
        self.cmbClass.setItemText(0, _translate("LoadTemplateDialog", "Не задано", None))
        self.cmbClass.setItemText(1, _translate("LoadTemplateDialog", "Статус", None))
        self.cmbClass.setItemText(2, _translate("LoadTemplateDialog", "Диагностика", None))
        self.cmbClass.setItemText(3, _translate("LoadTemplateDialog", "Лечение", None))
        self.cmbClass.setItemText(4, _translate("LoadTemplateDialog", "Прочие мероприятия", None))
        self.lblClass.setText(_translate("LoadTemplateDialog", "Класс", None))
        self.chkFindFilter.setText(_translate("LoadTemplateDialog", "Фильтр", None))
        self.lblSelectedActionTypes.setText(_translate("LoadTemplateDialog", "Назначить", None))
        self.btnFindTemplates.setText(_translate("LoadTemplateDialog", "Поиск", None))
        self.tabWgtActionTypes.setTabText(self.tabWgtActionTypes.indexOf(self.tabActionTypesTemplates), _translate("LoadTemplateDialog", "Шаблоны", None))
        self.btnUpdateTemplate.setText(_translate("LoadTemplateDialog", "Обновить шаблон", None))

from Events.ActionsSelectorSelectedTable import CCheckedActionsTableView
from library.TableView import CTableView
