# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportSetupByOrgStructure.ui'
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

class Ui_ReportSetupByOrgStructureDialog(object):
    def setupUi(self, ReportSetupByOrgStructureDialog):
        ReportSetupByOrgStructureDialog.setObjectName(_fromUtf8("ReportSetupByOrgStructureDialog"))
        ReportSetupByOrgStructureDialog.resize(762, 725)
        self.gridLayout = QtGui.QGridLayout(ReportSetupByOrgStructureDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtConfirmationBegDate = CDateEdit(ReportSetupByOrgStructureDialog)
        self.edtConfirmationBegDate.setEnabled(False)
        self.edtConfirmationBegDate.setObjectName(_fromUtf8("edtConfirmationBegDate"))
        self.gridLayout.addWidget(self.edtConfirmationBegDate, 7, 1, 1, 1)
        self.chkDetailService = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkDetailService.setEnabled(False)
        self.chkDetailService.setObjectName(_fromUtf8("chkDetailService"))
        self.gridLayout.addWidget(self.chkDetailService, 20, 1, 1, 5)
        self.chkStatus = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkStatus.setObjectName(_fromUtf8("chkStatus"))
        self.gridLayout.addWidget(self.chkStatus, 9, 0, 1, 1)
        self.chkCoefficient = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkCoefficient.setObjectName(_fromUtf8("chkCoefficient"))
        self.gridLayout.addWidget(self.chkCoefficient, 22, 1, 1, 5)
        self.chkClientAgeCategory = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkClientAgeCategory.setObjectName(_fromUtf8("chkClientAgeCategory"))
        self.gridLayout.addWidget(self.chkClientAgeCategory, 23, 0, 1, 1)
        self.cmbStatus = CActionStatusComboBox(ReportSetupByOrgStructureDialog)
        self.cmbStatus.setEnabled(False)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.gridLayout.addWidget(self.cmbStatus, 9, 1, 1, 5)
        self.cmbContract = CContractComboBox(ReportSetupByOrgStructureDialog)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.gridLayout.addWidget(self.cmbContract, 3, 1, 1, 5)
        self.cmbEventStatus = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbEventStatus.setEnabled(False)
        self.cmbEventStatus.setObjectName(_fromUtf8("cmbEventStatus"))
        self.cmbEventStatus.addItem(_fromUtf8(""))
        self.cmbEventStatus.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbEventStatus, 10, 1, 1, 5)
        spacerItem = QtGui.QSpacerItem(219, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 30, 0, 1, 6)
        self.lblContract = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.gridLayout.addWidget(self.lblContract, 3, 0, 1, 1)
        self.lblReportType = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblReportType.setObjectName(_fromUtf8("lblReportType"))
        self.gridLayout.addWidget(self.lblReportType, 14, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.chkOnlyClientAsPersonInLPU = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkOnlyClientAsPersonInLPU.setObjectName(_fromUtf8("chkOnlyClientAsPersonInLPU"))
        self.gridLayout.addWidget(self.chkOnlyClientAsPersonInLPU, 25, 0, 1, 6)
        self.lblBegDateConfirmation = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblBegDateConfirmation.setObjectName(_fromUtf8("lblBegDateConfirmation"))
        self.gridLayout.addWidget(self.lblBegDateConfirmation, 7, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportSetupByOrgStructureDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 31, 0, 1, 6)
        self.chkExecDateInfo = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkExecDateInfo.setObjectName(_fromUtf8("chkExecDateInfo"))
        self.gridLayout.addWidget(self.chkExecDateInfo, 18, 1, 1, 5)
        self.lblBegDate = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 1, 0, 1, 1)
        self.lblEventIdentifierType = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblEventIdentifierType.setObjectName(_fromUtf8("lblEventIdentifierType"))
        self.gridLayout.addWidget(self.lblEventIdentifierType, 13, 0, 1, 1)
        self.lblEndDateConfirmation = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblEndDateConfirmation.setObjectName(_fromUtf8("lblEndDateConfirmation"))
        self.gridLayout.addWidget(self.lblEndDateConfirmation, 8, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportSetupByOrgStructureDialog)
        self.cmbPerson.setEnabled(False)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 12, 1, 1, 5)
        self.chkPatientInfo = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkPatientInfo.setObjectName(_fromUtf8("chkPatientInfo"))
        self.gridLayout.addWidget(self.chkPatientInfo, 17, 1, 1, 5)
        self.cmbFinance = CRBComboBox(ReportSetupByOrgStructureDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 4, 1, 1, 5)
        self.cmbReportType = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbReportType.setObjectName(_fromUtf8("cmbReportType"))
        self.cmbReportType.addItem(_fromUtf8(""))
        self.cmbReportType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbReportType, 14, 1, 1, 5)
        self.chkEventStatus = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkEventStatus.setObjectName(_fromUtf8("chkEventStatus"))
        self.gridLayout.addWidget(self.chkEventStatus, 10, 0, 1, 1)
        self.cmbDateType = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbDateType.setObjectName(_fromUtf8("cmbDateType"))
        self.cmbDateType.addItem(_fromUtf8(""))
        self.cmbDateType.addItem(_fromUtf8(""))
        self.cmbDateType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDateType, 0, 1, 1, 5)
        self.cmbClientAgeCategory = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbClientAgeCategory.setObjectName(_fromUtf8("cmbClientAgeCategory"))
        self.cmbClientAgeCategory.addItem(_fromUtf8(""))
        self.cmbClientAgeCategory.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbClientAgeCategory, 23, 1, 1, 5)
        self.edtEndDate = CDateEdit(ReportSetupByOrgStructureDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 2, 1, 1, 2)
        self.chkGroupByPatient = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkGroupByPatient.setObjectName(_fromUtf8("chkGroupByPatient"))
        self.gridLayout.addWidget(self.chkGroupByPatient, 19, 1, 1, 5)
        self.chkOrgStructure = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkOrgStructure.setObjectName(_fromUtf8("chkOrgStructure"))
        self.gridLayout.addWidget(self.chkOrgStructure, 11, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 5, 1, 1)
        self.lblDateType = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblDateType.setObjectName(_fromUtf8("lblDateType"))
        self.gridLayout.addWidget(self.lblDateType, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportSetupByOrgStructureDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 1, 1, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(ReportSetupByOrgStructureDialog)
        self.cmbOrgStructure.setEnabled(False)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 11, 1, 1, 5)
        self.chkAllOrgStructure = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkAllOrgStructure.setEnabled(False)
        self.chkAllOrgStructure.setObjectName(_fromUtf8("chkAllOrgStructure"))
        self.gridLayout.addWidget(self.chkAllOrgStructure, 16, 1, 1, 5)
        self.chkPerson = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkPerson.setObjectName(_fromUtf8("chkPerson"))
        self.gridLayout.addWidget(self.chkPerson, 12, 0, 1, 1)
        self.lblFinance = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 4, 0, 1, 1)
        self.cmbEventIdentifierType = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbEventIdentifierType.setObjectName(_fromUtf8("cmbEventIdentifierType"))
        self.cmbEventIdentifierType.addItem(_fromUtf8(""))
        self.cmbEventIdentifierType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbEventIdentifierType, 13, 1, 1, 5)
        self.lblConfirmationType = QtGui.QLabel(ReportSetupByOrgStructureDialog)
        self.lblConfirmationType.setObjectName(_fromUtf8("lblConfirmationType"))
        self.gridLayout.addWidget(self.lblConfirmationType, 6, 0, 1, 1)
        self.cmbConfirmationType = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbConfirmationType.setEnabled(False)
        self.cmbConfirmationType.setObjectName(_fromUtf8("cmbConfirmationType"))
        self.cmbConfirmationType.addItem(_fromUtf8(""))
        self.cmbConfirmationType.addItem(_fromUtf8(""))
        self.cmbConfirmationType.addItem(_fromUtf8(""))
        self.cmbConfirmationType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbConfirmationType, 6, 1, 1, 5)
        self.edtConfirmationEndDate = CDateEdit(ReportSetupByOrgStructureDialog)
        self.edtConfirmationEndDate.setEnabled(False)
        self.edtConfirmationEndDate.setObjectName(_fromUtf8("edtConfirmationEndDate"))
        self.gridLayout.addWidget(self.edtConfirmationEndDate, 8, 1, 1, 1)
        self.cmbConfirmationPeriodType = QtGui.QComboBox(ReportSetupByOrgStructureDialog)
        self.cmbConfirmationPeriodType.setEnabled(False)
        self.cmbConfirmationPeriodType.setObjectName(_fromUtf8("cmbConfirmationPeriodType"))
        self.cmbConfirmationPeriodType.addItem(_fromUtf8(""))
        self.cmbConfirmationPeriodType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbConfirmationPeriodType, 7, 3, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 8, 3, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 7, 5, 1, 1)
        self.chkConfirmation = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkConfirmation.setObjectName(_fromUtf8("chkConfirmation"))
        self.gridLayout.addWidget(self.chkConfirmation, 5, 0, 1, 6)
        self.chkVAT = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkVAT.setObjectName(_fromUtf8("chkVAT"))
        self.gridLayout.addWidget(self.chkVAT, 15, 1, 1, 5)
        self.chkDetailExecPerson = QtGui.QCheckBox(ReportSetupByOrgStructureDialog)
        self.chkDetailExecPerson.setChecked(True)
        self.chkDetailExecPerson.setObjectName(_fromUtf8("chkDetailExecPerson"))
        self.gridLayout.addWidget(self.chkDetailExecPerson, 21, 1, 1, 5)
        self.lblContract.setBuddy(self.cmbContract)
        self.lblReportType.setBuddy(self.cmbReportType)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblFinance.setBuddy(self.cmbFinance)

        self.retranslateUi(ReportSetupByOrgStructureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportSetupByOrgStructureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportSetupByOrgStructureDialog.reject)
        QtCore.QObject.connect(self.chkStatus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbStatus.setEnabled)
        QtCore.QObject.connect(self.chkOrgStructure, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbOrgStructure.setEnabled)
        QtCore.QObject.connect(self.chkClientAgeCategory, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbClientAgeCategory.setEnabled)
        QtCore.QObject.connect(self.chkPerson, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbPerson.setEnabled)
        QtCore.QObject.connect(self.chkGroupByPatient, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkDetailService.setEnabled)
        QtCore.QObject.connect(self.chkEventStatus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbEventStatus.setEnabled)
        QtCore.QObject.connect(self.chkConfirmation, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbConfirmationType.setEnabled)
        QtCore.QObject.connect(self.chkConfirmation, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbConfirmationPeriodType.setEnabled)
        QtCore.QObject.connect(self.chkConfirmation, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtConfirmationBegDate.setEnabled)
        QtCore.QObject.connect(self.chkConfirmation, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtConfirmationEndDate.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ReportSetupByOrgStructureDialog)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbDateType, self.edtBegDate)
        ReportSetupByOrgStructureDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportSetupByOrgStructureDialog.setTabOrder(self.edtEndDate, self.cmbContract)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbContract, self.cmbFinance)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbFinance, self.chkConfirmation)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkConfirmation, self.cmbConfirmationType)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbConfirmationType, self.edtConfirmationBegDate)
        ReportSetupByOrgStructureDialog.setTabOrder(self.edtConfirmationBegDate, self.edtConfirmationEndDate)
        ReportSetupByOrgStructureDialog.setTabOrder(self.edtConfirmationEndDate, self.cmbConfirmationPeriodType)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbConfirmationPeriodType, self.chkStatus)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkStatus, self.cmbStatus)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbStatus, self.chkEventStatus)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkEventStatus, self.cmbEventStatus)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbEventStatus, self.chkOrgStructure)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkOrgStructure, self.cmbOrgStructure)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbOrgStructure, self.chkPerson)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkPerson, self.cmbPerson)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbPerson, self.cmbEventIdentifierType)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbEventIdentifierType, self.cmbReportType)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbReportType, self.chkAllOrgStructure)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkAllOrgStructure, self.chkPatientInfo)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkPatientInfo, self.chkExecDateInfo)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkExecDateInfo, self.chkGroupByPatient)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkGroupByPatient, self.chkDetailService)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkDetailService, self.chkDetailExecPerson)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkDetailExecPerson, self.chkCoefficient)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkCoefficient, self.chkClientAgeCategory)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkClientAgeCategory, self.cmbClientAgeCategory)
        ReportSetupByOrgStructureDialog.setTabOrder(self.cmbClientAgeCategory, self.chkOnlyClientAsPersonInLPU)
        ReportSetupByOrgStructureDialog.setTabOrder(self.chkOnlyClientAsPersonInLPU, self.buttonBox)
        ReportSetupByOrgStructureDialog.setTabOrder(self.buttonBox, self.chkVAT)

    def retranslateUi(self, ReportSetupByOrgStructureDialog):
        ReportSetupByOrgStructureDialog.setWindowTitle(_translate("ReportSetupByOrgStructureDialog", "Dialog", None))
        self.edtConfirmationBegDate.setDisplayFormat(_translate("ReportSetupByOrgStructureDialog", "dd.MM.yyyy", None))
        self.chkDetailService.setText(_translate("ReportSetupByOrgStructureDialog", "Детализировать услуги", None))
        self.chkStatus.setText(_translate("ReportSetupByOrgStructureDialog", "Статус действия", None))
        self.chkCoefficient.setText(_translate("ReportSetupByOrgStructureDialog", "Учитывать коэффициенты", None))
        self.chkClientAgeCategory.setText(_translate("ReportSetupByOrgStructureDialog", "Возраст пациента", None))
        self.cmbEventStatus.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "Закрытые", None))
        self.cmbEventStatus.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "Открытые", None))
        self.lblContract.setText(_translate("ReportSetupByOrgStructureDialog", "Контракт", None))
        self.lblReportType.setText(_translate("ReportSetupByOrgStructureDialog", "Формировать отчет по", None))
        self.lblEndDate.setText(_translate("ReportSetupByOrgStructureDialog", "Дата &окончания периода", None))
        self.chkOnlyClientAsPersonInLPU.setText(_translate("ReportSetupByOrgStructureDialog", "Только пациенты сотрудники учереждения", None))
        self.lblBegDateConfirmation.setText(_translate("ReportSetupByOrgStructureDialog", "Начало периода подтверждения:", None))
        self.chkExecDateInfo.setText(_translate("ReportSetupByOrgStructureDialog", "Детализировать по дате", None))
        self.lblBegDate.setText(_translate("ReportSetupByOrgStructureDialog", "Дата &начала периода", None))
        self.lblEventIdentifierType.setText(_translate("ReportSetupByOrgStructureDialog", "Номер обращения", None))
        self.lblEndDateConfirmation.setText(_translate("ReportSetupByOrgStructureDialog", "Окончание периода подтверждения:", None))
        self.chkPatientInfo.setText(_translate("ReportSetupByOrgStructureDialog", "Информация о пациенте", None))
        self.cmbReportType.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "отделениям выполнившего действие врача", None))
        self.cmbReportType.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "отделениям за которым закреплено действие", None))
        self.chkEventStatus.setText(_translate("ReportSetupByOrgStructureDialog", "Статус события", None))
        self.cmbDateType.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "дата назначения", None))
        self.cmbDateType.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "дата начала", None))
        self.cmbDateType.setItemText(2, _translate("ReportSetupByOrgStructureDialog", "дата выполнения", None))
        self.cmbClientAgeCategory.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "Дети от 0 до 17 лет", None))
        self.cmbClientAgeCategory.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "Взрослые от 18 лет", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportSetupByOrgStructureDialog", "dd.MM.yyyy", None))
        self.chkGroupByPatient.setText(_translate("ReportSetupByOrgStructureDialog", "Группировать по пациентам", None))
        self.chkOrgStructure.setText(_translate("ReportSetupByOrgStructureDialog", "Подразделение", None))
        self.lblDateType.setText(_translate("ReportSetupByOrgStructureDialog", "Тип даты", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportSetupByOrgStructureDialog", "dd.MM.yyyy", None))
        self.chkAllOrgStructure.setText(_translate("ReportSetupByOrgStructureDialog", "Учитывать все возможные подразделения", None))
        self.chkPerson.setText(_translate("ReportSetupByOrgStructureDialog", "Исполнитель", None))
        self.lblFinance.setText(_translate("ReportSetupByOrgStructureDialog", "Тип финансирования", None))
        self.cmbEventIdentifierType.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "Код обращения", None))
        self.cmbEventIdentifierType.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "Номер документа", None))
        self.lblConfirmationType.setText(_translate("ReportSetupByOrgStructureDialog", "Тип подтверждения:", None))
        self.cmbConfirmationType.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "не выставлено", None))
        self.cmbConfirmationType.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "выставлено", None))
        self.cmbConfirmationType.setItemText(2, _translate("ReportSetupByOrgStructureDialog", "оплачено", None))
        self.cmbConfirmationType.setItemText(3, _translate("ReportSetupByOrgStructureDialog", "отказано", None))
        self.edtConfirmationEndDate.setDisplayFormat(_translate("ReportSetupByOrgStructureDialog", "dd.MM.yyyy", None))
        self.cmbConfirmationPeriodType.setItemText(0, _translate("ReportSetupByOrgStructureDialog", "по дате формирования счета", None))
        self.cmbConfirmationPeriodType.setItemText(1, _translate("ReportSetupByOrgStructureDialog", "по дате подтверждения оплаты", None))
        self.chkConfirmation.setText(_translate("ReportSetupByOrgStructureDialog", "Подтверждение оплаты", None))
        self.chkVAT.setText(_translate("ReportSetupByOrgStructureDialog", "Без учёта НДС", None))
        self.chkDetailExecPerson.setText(_translate("ReportSetupByOrgStructureDialog", "Детализация по исполнителю", None))

from Accounting.ContractComboBox import CContractComboBox
from Events.ActionStatus import CActionStatusComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
