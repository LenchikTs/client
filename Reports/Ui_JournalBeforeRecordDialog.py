# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Reports/JournalBeforeRecordDialog.ui'
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

class Ui_JournalBeforeRecordDialog(object):
    def setupUi(self, JournalBeforeRecordDialog):
        JournalBeforeRecordDialog.setObjectName(_fromUtf8("JournalBeforeRecordDialog"))
        JournalBeforeRecordDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        JournalBeforeRecordDialog.resize(637, 622)
        JournalBeforeRecordDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(JournalBeforeRecordDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtEndScheduleDate = CDateEdit(JournalBeforeRecordDialog)
        self.edtEndScheduleDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndScheduleDate.sizePolicy().hasHeightForWidth())
        self.edtEndScheduleDate.setSizePolicy(sizePolicy)
        self.edtEndScheduleDate.setCalendarPopup(True)
        self.edtEndScheduleDate.setObjectName(_fromUtf8("edtEndScheduleDate"))
        self.gridLayout.addWidget(self.edtEndScheduleDate, 1, 4, 1, 1)
        self.edtBegScheduleTime = QtGui.QTimeEdit(JournalBeforeRecordDialog)
        self.edtBegScheduleTime.setEnabled(False)
        self.edtBegScheduleTime.setObjectName(_fromUtf8("edtBegScheduleTime"))
        self.gridLayout.addWidget(self.edtBegScheduleTime, 1, 2, 1, 1)
        self.edtBegScheduleDate = CDateEdit(JournalBeforeRecordDialog)
        self.edtBegScheduleDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegScheduleDate.sizePolicy().hasHeightForWidth())
        self.edtBegScheduleDate.setSizePolicy(sizePolicy)
        self.edtBegScheduleDate.setCalendarPopup(True)
        self.edtBegScheduleDate.setObjectName(_fromUtf8("edtBegScheduleDate"))
        self.gridLayout.addWidget(self.edtBegScheduleDate, 1, 1, 1, 1)
        self.edtBegRecordTime = QtGui.QTimeEdit(JournalBeforeRecordDialog)
        self.edtBegRecordTime.setObjectName(_fromUtf8("edtBegRecordTime"))
        self.gridLayout.addWidget(self.edtBegRecordTime, 0, 2, 1, 1)
        self.chkSchedulePeriod = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkSchedulePeriod.setObjectName(_fromUtf8("chkSchedulePeriod"))
        self.gridLayout.addWidget(self.chkSchedulePeriod, 1, 0, 1, 1)
        self.chkRecordPeriod = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkRecordPeriod.setChecked(True)
        self.chkRecordPeriod.setObjectName(_fromUtf8("chkRecordPeriod"))
        self.gridLayout.addWidget(self.chkRecordPeriod, 0, 0, 1, 1)
        self.edtBegRecordDate = CDateEdit(JournalBeforeRecordDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegRecordDate.sizePolicy().hasHeightForWidth())
        self.edtBegRecordDate.setSizePolicy(sizePolicy)
        self.edtBegRecordDate.setCalendarPopup(True)
        self.edtBegRecordDate.setObjectName(_fromUtf8("edtBegRecordDate"))
        self.gridLayout.addWidget(self.edtBegRecordDate, 0, 1, 1, 1)
        self.lblEndRecordDate = QtGui.QLabel(JournalBeforeRecordDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndRecordDate.sizePolicy().hasHeightForWidth())
        self.lblEndRecordDate.setSizePolicy(sizePolicy)
        self.lblEndRecordDate.setObjectName(_fromUtf8("lblEndRecordDate"))
        self.gridLayout.addWidget(self.lblEndRecordDate, 0, 3, 1, 1)
        self.edtEndRecordDate = CDateEdit(JournalBeforeRecordDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndRecordDate.sizePolicy().hasHeightForWidth())
        self.edtEndRecordDate.setSizePolicy(sizePolicy)
        self.edtEndRecordDate.setCalendarPopup(True)
        self.edtEndRecordDate.setObjectName(_fromUtf8("edtEndRecordDate"))
        self.gridLayout.addWidget(self.edtEndRecordDate, 0, 4, 1, 1)
        self.label = QtGui.QLabel(JournalBeforeRecordDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lblAppointmentType = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblAppointmentType.setObjectName(_fromUtf8("lblAppointmentType"))
        self.gridLayout.addWidget(self.lblAppointmentType, 7, 0, 1, 1)
        self.lblSocStatusType = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblSocStatusType.setObjectName(_fromUtf8("lblSocStatusType"))
        self.gridLayout.addWidget(self.lblSocStatusType, 9, 0, 1, 1)
        self.lblRecordPerson = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblRecordPerson.setObjectName(_fromUtf8("lblRecordPerson"))
        self.gridLayout.addWidget(self.lblRecordPerson, 10, 0, 1, 1)
        self.lblActivity = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblActivity.setObjectName(_fromUtf8("lblActivity"))
        self.gridLayout.addWidget(self.lblActivity, 4, 0, 1, 1)
        self.lblRecordPersonProfile = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblRecordPersonProfile.setObjectName(_fromUtf8("lblRecordPersonProfile"))
        self.gridLayout.addWidget(self.lblRecordPersonProfile, 11, 0, 1, 1)
        self.lblEndScheduleDate = QtGui.QLabel(JournalBeforeRecordDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndScheduleDate.sizePolicy().hasHeightForWidth())
        self.lblEndScheduleDate.setSizePolicy(sizePolicy)
        self.lblEndScheduleDate.setObjectName(_fromUtf8("lblEndScheduleDate"))
        self.gridLayout.addWidget(self.lblEndScheduleDate, 1, 3, 1, 1)
        self.lblSpeciality = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 3, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 22, 1, 1, 1)
        self.lblSocStatusClass = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblSocStatusClass.setObjectName(_fromUtf8("lblSocStatusClass"))
        self.gridLayout.addWidget(self.lblSocStatusClass, 8, 0, 1, 1)
        self.lblAppointmentPurpose = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblAppointmentPurpose.setObjectName(_fromUtf8("lblAppointmentPurpose"))
        self.gridLayout.addWidget(self.lblAppointmentPurpose, 12, 0, 1, 1)
        self.lblSorted = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblSorted.setObjectName(_fromUtf8("lblSorted"))
        self.gridLayout.addWidget(self.lblSorted, 14, 0, 1, 1)
        self.lblUserParams = QtGui.QLabel(JournalBeforeRecordDialog)
        self.lblUserParams.setObjectName(_fromUtf8("lblUserParams"))
        self.gridLayout.addWidget(self.lblUserParams, 15, 0, 1, 1)
        self.edtEndRecordTime = QtGui.QTimeEdit(JournalBeforeRecordDialog)
        self.edtEndRecordTime.setObjectName(_fromUtf8("edtEndRecordTime"))
        self.gridLayout.addWidget(self.edtEndRecordTime, 0, 5, 1, 1)
        self.edtEndScheduleTime = QtGui.QTimeEdit(JournalBeforeRecordDialog)
        self.edtEndScheduleTime.setEnabled(False)
        self.edtEndScheduleTime.setObjectName(_fromUtf8("edtEndScheduleTime"))
        self.gridLayout.addWidget(self.edtEndScheduleTime, 1, 5, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(JournalBeforeRecordDialog)
        self.cmbOrgStructure.setEnabled(True)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 5)
        self.cmbSpeciality = CRBComboBox(JournalBeforeRecordDialog)
        self.cmbSpeciality.setEnabled(True)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 3, 1, 1, 5)
        self.cmbActivity = CRBComboBox(JournalBeforeRecordDialog)
        self.cmbActivity.setObjectName(_fromUtf8("cmbActivity"))
        self.gridLayout.addWidget(self.cmbActivity, 4, 1, 1, 5)
        self.cmbPerson = CPersonComboBoxEx(JournalBeforeRecordDialog)
        self.cmbPerson.setEnabled(True)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 5)
        self.cmbAppointmentType = QtGui.QComboBox(JournalBeforeRecordDialog)
        self.cmbAppointmentType.setObjectName(_fromUtf8("cmbAppointmentType"))
        self.cmbAppointmentType.addItem(_fromUtf8(""))
        self.cmbAppointmentType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAppointmentType, 7, 1, 1, 5)
        self.cmbSocStatusClass = CSocStatusComboBox(JournalBeforeRecordDialog)
        self.cmbSocStatusClass.setObjectName(_fromUtf8("cmbSocStatusClass"))
        self.gridLayout.addWidget(self.cmbSocStatusClass, 8, 1, 1, 5)
        self.cmbSocStatusType = CRBComboBox(JournalBeforeRecordDialog)
        self.cmbSocStatusType.setObjectName(_fromUtf8("cmbSocStatusType"))
        self.gridLayout.addWidget(self.cmbSocStatusType, 9, 1, 1, 5)
        self.cmbRecordPerson = CPersonComboBoxEx(JournalBeforeRecordDialog)
        self.cmbRecordPerson.setEnabled(True)
        self.cmbRecordPerson.setObjectName(_fromUtf8("cmbRecordPerson"))
        self.gridLayout.addWidget(self.cmbRecordPerson, 10, 1, 1, 5)
        self.cmbRecordPersonProfile = CRBComboBox(JournalBeforeRecordDialog)
        self.cmbRecordPersonProfile.setObjectName(_fromUtf8("cmbRecordPersonProfile"))
        self.gridLayout.addWidget(self.cmbRecordPersonProfile, 11, 1, 1, 5)
        self.cmbAppointmentPurpose = CRBComboBox(JournalBeforeRecordDialog)
        self.cmbAppointmentPurpose.setObjectName(_fromUtf8("cmbAppointmentPurpose"))
        self.gridLayout.addWidget(self.cmbAppointmentPurpose, 12, 1, 1, 5)
        self.cmbSorted = QtGui.QComboBox(JournalBeforeRecordDialog)
        self.cmbSorted.setObjectName(_fromUtf8("cmbSorted"))
        self.cmbSorted.addItem(_fromUtf8(""))
        self.cmbSorted.addItem(_fromUtf8(""))
        self.cmbSorted.addItem(_fromUtf8(""))
        self.cmbSorted.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSorted, 14, 1, 1, 5)
        self.cmbUserParams = QtGui.QComboBox(JournalBeforeRecordDialog)
        self.cmbUserParams.setObjectName(_fromUtf8("cmbUserParams"))
        self.cmbUserParams.addItem(_fromUtf8(""))
        self.cmbUserParams.addItem(_fromUtf8(""))
        self.cmbUserParams.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbUserParams, 15, 1, 1, 5)
        self.chkDetailCallCenter = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkDetailCallCenter.setEnabled(True)
        self.chkDetailCallCenter.setObjectName(_fromUtf8("chkDetailCallCenter"))
        self.gridLayout.addWidget(self.chkDetailCallCenter, 13, 1, 1, 5)
        self.chkDumpParams = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkDumpParams.setChecked(True)
        self.chkDumpParams.setObjectName(_fromUtf8("chkDumpParams"))
        self.gridLayout.addWidget(self.chkDumpParams, 16, 0, 1, 6)
        self.chkPersonInfo = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkPersonInfo.setObjectName(_fromUtf8("chkPersonInfo"))
        self.gridLayout.addWidget(self.chkPersonInfo, 17, 0, 1, 6)
        self.chkComplaint = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkComplaint.setObjectName(_fromUtf8("chkComplaint"))
        self.gridLayout.addWidget(self.chkComplaint, 18, 0, 1, 6)
        self.chkClientId = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkClientId.setChecked(True)
        self.chkClientId.setObjectName(_fromUtf8("chkClientId"))
        self.gridLayout.addWidget(self.chkClientId, 19, 0, 1, 6)
        self.chkClientPhones = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkClientPhones.setChecked(True)
        self.chkClientPhones.setObjectName(_fromUtf8("chkClientPhones"))
        self.gridLayout.addWidget(self.chkClientPhones, 20, 0, 1, 6)
        self.chkClientMail = QtGui.QCheckBox(JournalBeforeRecordDialog)
        self.chkClientMail.setChecked(True)
        self.chkClientMail.setObjectName(_fromUtf8("chkClientMail"))
        self.gridLayout.addWidget(self.chkClientMail, 21, 0, 1, 6)
        self.buttonBox = QtGui.QDialogButtonBox(JournalBeforeRecordDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 23, 0, 1, 6)
        self.lblEndRecordDate.setBuddy(self.edtEndRecordDate)
        self.label.setBuddy(self.cmbOrgStructure)
        self.lblAppointmentType.setBuddy(self.cmbAppointmentType)
        self.lblSocStatusType.setBuddy(self.cmbSocStatusType)
        self.lblRecordPerson.setBuddy(self.cmbRecordPerson)
        self.lblRecordPersonProfile.setBuddy(self.cmbRecordPersonProfile)
        self.lblEndScheduleDate.setBuddy(self.edtEndScheduleDate)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblSocStatusClass.setBuddy(self.cmbSocStatusClass)

        self.retranslateUi(JournalBeforeRecordDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), JournalBeforeRecordDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), JournalBeforeRecordDialog.reject)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegRecordDate.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndRecordDate.setEnabled)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndScheduleDate.setEnabled)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegScheduleDate.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("clicked()")), self.edtBegRecordDate.setFocus)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("clicked()")), self.edtBegScheduleDate.setFocus)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegScheduleTime.setEnabled)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndScheduleTime.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegRecordTime.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndRecordTime.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(JournalBeforeRecordDialog)
        JournalBeforeRecordDialog.setTabOrder(self.chkRecordPeriod, self.edtBegRecordDate)
        JournalBeforeRecordDialog.setTabOrder(self.edtBegRecordDate, self.edtEndRecordDate)
        JournalBeforeRecordDialog.setTabOrder(self.edtEndRecordDate, self.chkSchedulePeriod)
        JournalBeforeRecordDialog.setTabOrder(self.chkSchedulePeriod, self.edtBegScheduleDate)
        JournalBeforeRecordDialog.setTabOrder(self.edtBegScheduleDate, self.edtEndScheduleDate)
        JournalBeforeRecordDialog.setTabOrder(self.edtEndScheduleDate, self.cmbOrgStructure)
        JournalBeforeRecordDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        JournalBeforeRecordDialog.setTabOrder(self.cmbSpeciality, self.cmbActivity)
        JournalBeforeRecordDialog.setTabOrder(self.cmbActivity, self.cmbPerson)
        JournalBeforeRecordDialog.setTabOrder(self.cmbPerson, self.cmbAppointmentType)
        JournalBeforeRecordDialog.setTabOrder(self.cmbAppointmentType, self.cmbSocStatusClass)
        JournalBeforeRecordDialog.setTabOrder(self.cmbSocStatusClass, self.cmbSocStatusType)
        JournalBeforeRecordDialog.setTabOrder(self.cmbSocStatusType, self.cmbRecordPerson)
        JournalBeforeRecordDialog.setTabOrder(self.cmbRecordPerson, self.cmbRecordPersonProfile)
        JournalBeforeRecordDialog.setTabOrder(self.cmbRecordPersonProfile, self.cmbAppointmentPurpose)
        JournalBeforeRecordDialog.setTabOrder(self.cmbAppointmentPurpose, self.chkDetailCallCenter)
        JournalBeforeRecordDialog.setTabOrder(self.chkDetailCallCenter, self.cmbSorted)
        JournalBeforeRecordDialog.setTabOrder(self.cmbSorted, self.cmbUserParams)
        JournalBeforeRecordDialog.setTabOrder(self.cmbUserParams, self.chkDumpParams)
        JournalBeforeRecordDialog.setTabOrder(self.chkDumpParams, self.chkPersonInfo)
        JournalBeforeRecordDialog.setTabOrder(self.chkPersonInfo, self.chkComplaint)
        JournalBeforeRecordDialog.setTabOrder(self.chkComplaint, self.chkClientId)
        JournalBeforeRecordDialog.setTabOrder(self.chkClientId, self.chkClientPhones)
        JournalBeforeRecordDialog.setTabOrder(self.chkClientPhones, self.chkClientMail)
        JournalBeforeRecordDialog.setTabOrder(self.chkClientMail, self.buttonBox)

    def retranslateUi(self, JournalBeforeRecordDialog):
        JournalBeforeRecordDialog.setWindowTitle(_translate("JournalBeforeRecordDialog", "Журнал предварительной записи", None))
        self.edtEndScheduleDate.setDisplayFormat(_translate("JournalBeforeRecordDialog", "dd.MM.yyyy", None))
        self.edtBegScheduleDate.setDisplayFormat(_translate("JournalBeforeRecordDialog", "dd.MM.yyyy", None))
        self.chkSchedulePeriod.setText(_translate("JournalBeforeRecordDialog", "Период планируемого приёма с", None))
        self.chkRecordPeriod.setText(_translate("JournalBeforeRecordDialog", "Период постановки в очередь с", None))
        self.edtBegRecordDate.setDisplayFormat(_translate("JournalBeforeRecordDialog", "dd.MM.yyyy", None))
        self.lblEndRecordDate.setText(_translate("JournalBeforeRecordDialog", "по", None))
        self.edtEndRecordDate.setDisplayFormat(_translate("JournalBeforeRecordDialog", "dd.MM.yyyy", None))
        self.label.setText(_translate("JournalBeforeRecordDialog", "&Подразделение", None))
        self.lblAppointmentType.setText(_translate("JournalBeforeRecordDialog", "Учитывать", None))
        self.lblSocStatusType.setText(_translate("JournalBeforeRecordDialog", "Тип соц.статуса", None))
        self.lblRecordPerson.setText(_translate("JournalBeforeRecordDialog", "Пользователь", None))
        self.lblActivity.setText(_translate("JournalBeforeRecordDialog", "Вид деятельности", None))
        self.lblRecordPersonProfile.setText(_translate("JournalBeforeRecordDialog", "Профиль пользователя", None))
        self.lblEndScheduleDate.setText(_translate("JournalBeforeRecordDialog", "по", None))
        self.lblSpeciality.setText(_translate("JournalBeforeRecordDialog", "&Специальность", None))
        self.lblPerson.setText(_translate("JournalBeforeRecordDialog", "&Врач", None))
        self.lblSocStatusClass.setText(_translate("JournalBeforeRecordDialog", "Класс соц.статуса", None))
        self.lblAppointmentPurpose.setText(_translate("JournalBeforeRecordDialog", "Назначение", None))
        self.lblSorted.setText(_translate("JournalBeforeRecordDialog", "Сортировать по", None))
        self.lblUserParams.setText(_translate("JournalBeforeRecordDialog", "Учитывать пользователей", None))
        self.cmbSpeciality.setWhatsThis(_translate("JournalBeforeRecordDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.cmbAppointmentType.setItemText(0, _translate("JournalBeforeRecordDialog", "Амбулаторный прием", None))
        self.cmbAppointmentType.setItemText(1, _translate("JournalBeforeRecordDialog", "Вызов на дом", None))
        self.cmbSorted.setItemText(0, _translate("JournalBeforeRecordDialog", "Дата записи", None))
        self.cmbSorted.setItemText(1, _translate("JournalBeforeRecordDialog", "ФИО", None))
        self.cmbSorted.setItemText(2, _translate("JournalBeforeRecordDialog", "Дата рождения", None))
        self.cmbSorted.setItemText(3, _translate("JournalBeforeRecordDialog", "Назначение", None))
        self.cmbUserParams.setItemText(0, _translate("JournalBeforeRecordDialog", "Все пользователи", None))
        self.cmbUserParams.setItemText(1, _translate("JournalBeforeRecordDialog", "Call-центр", None))
        self.cmbUserParams.setItemText(2, _translate("JournalBeforeRecordDialog", "Интернет", None))
        self.chkDetailCallCenter.setText(_translate("JournalBeforeRecordDialog", "Детализировать Call-центр", None))
        self.chkDumpParams.setText(_translate("JournalBeforeRecordDialog", "Печатать параметры фильтра", None))
        self.chkPersonInfo.setText(_translate("JournalBeforeRecordDialog", "Выводить данные о враче", None))
        self.chkComplaint.setText(_translate("JournalBeforeRecordDialog", "Выводить жалобы пациента", None))
        self.chkClientId.setText(_translate("JournalBeforeRecordDialog", "Выводить код пациента", None))
        self.chkClientPhones.setText(_translate("JournalBeforeRecordDialog", "Выводить телефон", None))
        self.chkClientMail.setText(_translate("JournalBeforeRecordDialog", "Выводить электронную почту", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Registry.SocStatusComboBox import CSocStatusComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    JournalBeforeRecordDialog = QtGui.QDialog()
    ui = Ui_JournalBeforeRecordDialog()
    ui.setupUi(JournalBeforeRecordDialog)
    JournalBeforeRecordDialog.show()
    sys.exit(app.exec_())
