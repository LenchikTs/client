# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\Events\ExecutionPlanDialog.ui'
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

class Ui_ExecutionPlanDialog(object):
    def setupUi(self, ExecutionPlanDialog):
        ExecutionPlanDialog.setObjectName(_fromUtf8("ExecutionPlanDialog"))
        ExecutionPlanDialog.resize(795, 679)
        self.gridLayout = QtGui.QGridLayout(ExecutionPlanDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAPDirectionDate = QtGui.QLabel(ExecutionPlanDialog)
        self.lblAPDirectionDate.setObjectName(_fromUtf8("lblAPDirectionDate"))
        self.gridLayout.addWidget(self.lblAPDirectionDate, 0, 0, 1, 1)
        self.edtDirectionDate = CDateEdit(ExecutionPlanDialog)
        self.edtDirectionDate.setEnabled(False)
        self.edtDirectionDate.setCalendarPopup(True)
        self.edtDirectionDate.setObjectName(_fromUtf8("edtDirectionDate"))
        self.gridLayout.addWidget(self.edtDirectionDate, 0, 1, 1, 1)
        self.edtBegDate = CDateEdit(ExecutionPlanDialog)
        self.edtBegDate.setEnabled(False)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 4, 1, 1)
        self.lblAPEndDate = QtGui.QLabel(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAPEndDate.sizePolicy().hasHeightForWidth())
        self.lblAPEndDate.setSizePolicy(sizePolicy)
        self.lblAPEndDate.setObjectName(_fromUtf8("lblAPEndDate"))
        self.gridLayout.addWidget(self.lblAPEndDate, 0, 5, 1, 1)
        self.edtDirectionTime = QtGui.QTimeEdit(ExecutionPlanDialog)
        self.edtDirectionTime.setEnabled(False)
        self.edtDirectionTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtDirectionTime.setObjectName(_fromUtf8("edtDirectionTime"))
        self.gridLayout.addWidget(self.edtDirectionTime, 0, 2, 1, 1)
        self.lblAPBegDate = QtGui.QLabel(ExecutionPlanDialog)
        self.lblAPBegDate.setObjectName(_fromUtf8("lblAPBegDate"))
        self.gridLayout.addWidget(self.lblAPBegDate, 0, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblQuantity = QtGui.QLabel(ExecutionPlanDialog)
        self.lblQuantity.setObjectName(_fromUtf8("lblQuantity"))
        self.horizontalLayout.addWidget(self.lblQuantity)
        self.edtQuantity = QtGui.QSpinBox(ExecutionPlanDialog)
        self.edtQuantity.setObjectName(_fromUtf8("edtQuantity"))
        self.horizontalLayout.addWidget(self.edtQuantity)
        self.lblDuration = QtGui.QLabel(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDuration.sizePolicy().hasHeightForWidth())
        self.lblDuration.setSizePolicy(sizePolicy)
        self.lblDuration.setObjectName(_fromUtf8("lblDuration"))
        self.horizontalLayout.addWidget(self.lblDuration)
        self.edtDuration = QtGui.QSpinBox(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDuration.sizePolicy().hasHeightForWidth())
        self.edtDuration.setSizePolicy(sizePolicy)
        self.edtDuration.setObjectName(_fromUtf8("edtDuration"))
        self.horizontalLayout.addWidget(self.edtDuration)
        self.lblPeriodicity = QtGui.QLabel(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPeriodicity.sizePolicy().hasHeightForWidth())
        self.lblPeriodicity.setSizePolicy(sizePolicy)
        self.lblPeriodicity.setObjectName(_fromUtf8("lblPeriodicity"))
        self.horizontalLayout.addWidget(self.lblPeriodicity)
        self.edtPeriodicity = QtGui.QSpinBox(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPeriodicity.sizePolicy().hasHeightForWidth())
        self.edtPeriodicity.setSizePolicy(sizePolicy)
        self.edtPeriodicity.setObjectName(_fromUtf8("edtPeriodicity"))
        self.horizontalLayout.addWidget(self.edtPeriodicity)
        self.lblAliquoticity = QtGui.QLabel(ExecutionPlanDialog)
        self.lblAliquoticity.setObjectName(_fromUtf8("lblAliquoticity"))
        self.horizontalLayout.addWidget(self.lblAliquoticity)
        self.edtAliquoticity = QtGui.QSpinBox(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAliquoticity.sizePolicy().hasHeightForWidth())
        self.edtAliquoticity.setSizePolicy(sizePolicy)
        self.edtAliquoticity.setObjectName(_fromUtf8("edtAliquoticity"))
        self.horizontalLayout.addWidget(self.edtAliquoticity)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 8)
        self.edtEndDate = CDateEdit(ExecutionPlanDialog)
        self.edtEndDate.setEnabled(False)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(43, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 7, 1, 1)
        self.lblAPSetPerson = QtGui.QLabel(ExecutionPlanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAPSetPerson.sizePolicy().hasHeightForWidth())
        self.lblAPSetPerson.setSizePolicy(sizePolicy)
        self.lblAPSetPerson.setObjectName(_fromUtf8("lblAPSetPerson"))
        self.gridLayout.addWidget(self.lblAPSetPerson, 1, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ExecutionPlanDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.btnDeleted = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnDeleted.setObjectName(_fromUtf8("btnDeleted"))
        self.hboxlayout.addWidget(self.btnDeleted)
        self.btnSave = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.hboxlayout.addWidget(self.btnSave)
        self.btnSchedule = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnSchedule.setObjectName(_fromUtf8("btnSchedule"))
        self.hboxlayout.addWidget(self.btnSchedule)
        self.btnPlan = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnPlan.setObjectName(_fromUtf8("btnPlan"))
        self.hboxlayout.addWidget(self.btnPlan)
        self.btnEdit = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnEdit.setDefault(True)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnPrint = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.hboxlayout.addWidget(self.btnPrint)
        self.btnCancel = QtGui.QPushButton(ExecutionPlanDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.hboxlayout, 6, 0, 1, 8)
        self.tblExecutionPlan = CExecutionPlanTableView(ExecutionPlanDialog)
        self.tblExecutionPlan.setObjectName(_fromUtf8("tblExecutionPlan"))
        self.gridLayout.addWidget(self.tblExecutionPlan, 4, 0, 1, 8)
        self.cmbSetPerson = CPersonComboBoxEx(ExecutionPlanDialog)
        self.cmbSetPerson.setEnabled(False)
        self.cmbSetPerson.setObjectName(_fromUtf8("cmbSetPerson"))
        self.cmbSetPerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSetPerson, 1, 1, 1, 7)
        self.lblOrgStructure = QtGui.QLabel(ExecutionPlanDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureNodeDisableComboBox(ExecutionPlanDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 7)
        self.lblAPDirectionDate.setBuddy(self.edtDirectionDate)
        self.lblAPEndDate.setBuddy(self.edtEndDate)
        self.lblAPBegDate.setBuddy(self.edtBegDate)
        self.lblAPSetPerson.setBuddy(self.cmbSetPerson)

        self.retranslateUi(ExecutionPlanDialog)
        QtCore.QMetaObject.connectSlotsByName(ExecutionPlanDialog)
        ExecutionPlanDialog.setTabOrder(self.edtDirectionDate, self.edtDirectionTime)
        ExecutionPlanDialog.setTabOrder(self.edtDirectionTime, self.edtBegDate)
        ExecutionPlanDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ExecutionPlanDialog.setTabOrder(self.edtEndDate, self.cmbSetPerson)
        ExecutionPlanDialog.setTabOrder(self.cmbSetPerson, self.cmbOrgStructure)
        ExecutionPlanDialog.setTabOrder(self.cmbOrgStructure, self.edtQuantity)
        ExecutionPlanDialog.setTabOrder(self.edtQuantity, self.edtDuration)
        ExecutionPlanDialog.setTabOrder(self.edtDuration, self.edtPeriodicity)
        ExecutionPlanDialog.setTabOrder(self.edtPeriodicity, self.edtAliquoticity)
        ExecutionPlanDialog.setTabOrder(self.edtAliquoticity, self.tblExecutionPlan)
        ExecutionPlanDialog.setTabOrder(self.tblExecutionPlan, self.btnSchedule)
        ExecutionPlanDialog.setTabOrder(self.btnSchedule, self.btnPlan)
        ExecutionPlanDialog.setTabOrder(self.btnPlan, self.btnEdit)
        ExecutionPlanDialog.setTabOrder(self.btnEdit, self.btnDeleted)
        ExecutionPlanDialog.setTabOrder(self.btnDeleted, self.btnSave)
        ExecutionPlanDialog.setTabOrder(self.btnSave, self.btnPrint)
        ExecutionPlanDialog.setTabOrder(self.btnPrint, self.btnCancel)

    def retranslateUi(self, ExecutionPlanDialog):
        ExecutionPlanDialog.setWindowTitle(_translate("ExecutionPlanDialog", "Dialog", None))
        self.lblAPDirectionDate.setText(_translate("ExecutionPlanDialog", "Назначено", None))
        self.edtDirectionDate.setWhatsThis(_translate("ExecutionPlanDialog", "дата начала осмотра", None))
        self.edtBegDate.setWhatsThis(_translate("ExecutionPlanDialog", "дата окончания осмотра", None))
        self.lblAPEndDate.setText(_translate("ExecutionPlanDialog", "Закончить", None))
        self.edtDirectionTime.setDisplayFormat(_translate("ExecutionPlanDialog", "HH:mm", None))
        self.lblAPBegDate.setText(_translate("ExecutionPlanDialog", "Начать с", None))
        self.lblQuantity.setText(_translate("ExecutionPlanDialog", "Кол-во процедур", None))
        self.edtQuantity.setToolTip(_translate("ExecutionPlanDialog", "При изменении значений в полях \"Длительность\" или \"Кратность\" значение поля \"Кол-во процедур\" высчитывается автоматически", None))
        self.lblDuration.setToolTip(_translate("ExecutionPlanDialog", "Длительность курса лечения в днях.", None))
        self.lblDuration.setText(_translate("ExecutionPlanDialog", "Длительность", None))
        self.edtDuration.setToolTip(_translate("ExecutionPlanDialog", "Длительность курса лечения в днях.", None))
        self.lblPeriodicity.setToolTip(_translate("ExecutionPlanDialog", "0 - каждый день,\n"
"1 - через 1 день,\n"
"2 - через 2 дня,\n"
"3 - через 3 дня,\n"
"и т.д.", None))
        self.lblPeriodicity.setText(_translate("ExecutionPlanDialog", "Интервал", None))
        self.edtPeriodicity.setToolTip(_translate("ExecutionPlanDialog", "0 - каждый день,\n"
"1 - через 1 день,\n"
"2 - через 2 дня,\n"
"3 - через 3 дня,\n"
"и т.д.", None))
        self.lblAliquoticity.setToolTip(_translate("ExecutionPlanDialog", "Сколько раз в сутки.", None))
        self.lblAliquoticity.setText(_translate("ExecutionPlanDialog", "Кратность", None))
        self.edtAliquoticity.setToolTip(_translate("ExecutionPlanDialog", "Сколько раз в сутки.", None))
        self.lblAPSetPerson.setText(_translate("ExecutionPlanDialog", "Назначил", None))
        self.label.setText(_translate("ExecutionPlanDialog", "всего: ", None))
        self.btnDeleted.setText(_translate("ExecutionPlanDialog", "Удалить", None))
        self.btnSave.setText(_translate("ExecutionPlanDialog", "Сохранить", None))
        self.btnSchedule.setText(_translate("ExecutionPlanDialog", "Запл-ть по расписанию", None))
        self.btnPlan.setText(_translate("ExecutionPlanDialog", "Запланировать", None))
        self.btnEdit.setWhatsThis(_translate("ExecutionPlanDialog", "изменить текущую запись", None))
        self.btnEdit.setText(_translate("ExecutionPlanDialog", "Просмотр", None))
        self.btnEdit.setShortcut(_translate("ExecutionPlanDialog", "F4", None))
        self.btnPrint.setText(_translate("ExecutionPlanDialog", "Печать", None))
        self.btnCancel.setWhatsThis(_translate("ExecutionPlanDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("ExecutionPlanDialog", "Закрыть", None))
        self.cmbSetPerson.setItemText(0, _translate("ExecutionPlanDialog", "Врач", None))
        self.lblOrgStructure.setText(_translate("ExecutionPlanDialog", "Подразделение ", None))

from ExecutionPlanTableView import CExecutionPlanTableView
from Orgs.OrgStructComboBoxes import COrgStructureNodeDisableComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
