# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\PreRecordSpecialityDialog.ui'
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

class Ui_PreRecordSpecialityDialog(object):
    def setupUi(self, PreRecordSpecialityDialog):
        PreRecordSpecialityDialog.setObjectName(_fromUtf8("PreRecordSpecialityDialog"))
        PreRecordSpecialityDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PreRecordSpecialityDialog.resize(447, 222)
        PreRecordSpecialityDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(PreRecordSpecialityDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkRecordPeriod = QtGui.QCheckBox(PreRecordSpecialityDialog)
        self.chkRecordPeriod.setChecked(False)
        self.chkRecordPeriod.setObjectName(_fromUtf8("chkRecordPeriod"))
        self.gridLayout.addWidget(self.chkRecordPeriod, 0, 0, 1, 2)
        self.edtBegRecordDate = CDateEdit(PreRecordSpecialityDialog)
        self.edtBegRecordDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegRecordDate.sizePolicy().hasHeightForWidth())
        self.edtBegRecordDate.setSizePolicy(sizePolicy)
        self.edtBegRecordDate.setCalendarPopup(True)
        self.edtBegRecordDate.setObjectName(_fromUtf8("edtBegRecordDate"))
        self.gridLayout.addWidget(self.edtBegRecordDate, 0, 2, 1, 1)
        self.lblEndRecordDate = QtGui.QLabel(PreRecordSpecialityDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndRecordDate.sizePolicy().hasHeightForWidth())
        self.lblEndRecordDate.setSizePolicy(sizePolicy)
        self.lblEndRecordDate.setObjectName(_fromUtf8("lblEndRecordDate"))
        self.gridLayout.addWidget(self.lblEndRecordDate, 0, 3, 1, 1)
        self.chkSchedulePeriod = QtGui.QCheckBox(PreRecordSpecialityDialog)
        self.chkSchedulePeriod.setChecked(True)
        self.chkSchedulePeriod.setObjectName(_fromUtf8("chkSchedulePeriod"))
        self.gridLayout.addWidget(self.chkSchedulePeriod, 1, 0, 1, 2)
        self.edtBegScheduleDate = CDateEdit(PreRecordSpecialityDialog)
        self.edtBegScheduleDate.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegScheduleDate.sizePolicy().hasHeightForWidth())
        self.edtBegScheduleDate.setSizePolicy(sizePolicy)
        self.edtBegScheduleDate.setCalendarPopup(True)
        self.edtBegScheduleDate.setObjectName(_fromUtf8("edtBegScheduleDate"))
        self.gridLayout.addWidget(self.edtBegScheduleDate, 1, 2, 1, 1)
        self.lblEndScheduleDate = QtGui.QLabel(PreRecordSpecialityDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndScheduleDate.sizePolicy().hasHeightForWidth())
        self.lblEndScheduleDate.setSizePolicy(sizePolicy)
        self.lblEndScheduleDate.setObjectName(_fromUtf8("lblEndScheduleDate"))
        self.gridLayout.addWidget(self.lblEndScheduleDate, 1, 3, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(PreRecordSpecialityDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.lblSpeciality = QtGui.QLabel(PreRecordSpecialityDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 3, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(PreRecordSpecialityDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 4, 0, 1, 1)
        self.lblDetail = QtGui.QLabel(PreRecordSpecialityDialog)
        self.lblDetail.setObjectName(_fromUtf8("lblDetail"))
        self.gridLayout.addWidget(self.lblDetail, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.edtEndScheduleDate = CDateEdit(PreRecordSpecialityDialog)
        self.edtEndScheduleDate.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndScheduleDate.sizePolicy().hasHeightForWidth())
        self.edtEndScheduleDate.setSizePolicy(sizePolicy)
        self.edtEndScheduleDate.setCalendarPopup(True)
        self.edtEndScheduleDate.setObjectName(_fromUtf8("edtEndScheduleDate"))
        self.gridLayout.addWidget(self.edtEndScheduleDate, 1, 4, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(PreRecordSpecialityDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 6)
        self.chkDetailOnPerson = QtGui.QCheckBox(PreRecordSpecialityDialog)
        self.chkDetailOnPerson.setObjectName(_fromUtf8("chkDetailOnPerson"))
        self.gridLayout.addWidget(self.chkDetailOnPerson, 6, 2, 1, 4)
        self.chkDetailOnOrgStructure = QtGui.QCheckBox(PreRecordSpecialityDialog)
        self.chkDetailOnOrgStructure.setObjectName(_fromUtf8("chkDetailOnOrgStructure"))
        self.gridLayout.addWidget(self.chkDetailOnOrgStructure, 5, 2, 1, 4)
        self.cmbPerson = CPersonComboBoxEx(PreRecordSpecialityDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 4, 2, 1, 4)
        self.cmbSpeciality = CRBComboBox(PreRecordSpecialityDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 3, 2, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(PreRecordSpecialityDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 4)
        self.edtEndRecordDate = CDateEdit(PreRecordSpecialityDialog)
        self.edtEndRecordDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndRecordDate.sizePolicy().hasHeightForWidth())
        self.edtEndRecordDate.setSizePolicy(sizePolicy)
        self.edtEndRecordDate.setCalendarPopup(True)
        self.edtEndRecordDate.setObjectName(_fromUtf8("edtEndRecordDate"))
        self.gridLayout.addWidget(self.edtEndRecordDate, 0, 4, 1, 2)
        self.chkShowDeleted = QtGui.QCheckBox(PreRecordSpecialityDialog)
        self.chkShowDeleted.setObjectName(_fromUtf8("chkShowDeleted"))
        self.gridLayout.addWidget(self.chkShowDeleted, 7, 2, 1, 4)
        self.lblEndRecordDate.setBuddy(self.edtEndRecordDate)
        self.lblEndScheduleDate.setBuddy(self.edtEndScheduleDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblDetail.setBuddy(self.chkDetailOnOrgStructure)

        self.retranslateUi(PreRecordSpecialityDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PreRecordSpecialityDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PreRecordSpecialityDialog.reject)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegRecordDate.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndRecordDate.setEnabled)
        QtCore.QObject.connect(self.chkRecordPeriod, QtCore.SIGNAL(_fromUtf8("clicked()")), self.edtBegRecordDate.setFocus)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegScheduleDate.setEnabled)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndScheduleDate.setEnabled)
        QtCore.QObject.connect(self.chkSchedulePeriod, QtCore.SIGNAL(_fromUtf8("clicked()")), self.edtBegScheduleDate.setFocus)
        QtCore.QMetaObject.connectSlotsByName(PreRecordSpecialityDialog)
        PreRecordSpecialityDialog.setTabOrder(self.chkRecordPeriod, self.edtBegRecordDate)
        PreRecordSpecialityDialog.setTabOrder(self.edtBegRecordDate, self.edtEndRecordDate)
        PreRecordSpecialityDialog.setTabOrder(self.edtEndRecordDate, self.chkSchedulePeriod)
        PreRecordSpecialityDialog.setTabOrder(self.chkSchedulePeriod, self.edtBegScheduleDate)
        PreRecordSpecialityDialog.setTabOrder(self.edtBegScheduleDate, self.edtEndScheduleDate)
        PreRecordSpecialityDialog.setTabOrder(self.edtEndScheduleDate, self.cmbOrgStructure)
        PreRecordSpecialityDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        PreRecordSpecialityDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        PreRecordSpecialityDialog.setTabOrder(self.cmbPerson, self.chkDetailOnOrgStructure)
        PreRecordSpecialityDialog.setTabOrder(self.chkDetailOnOrgStructure, self.chkDetailOnPerson)
        PreRecordSpecialityDialog.setTabOrder(self.chkDetailOnPerson, self.buttonBox)

    def retranslateUi(self, PreRecordSpecialityDialog):
        PreRecordSpecialityDialog.setWindowTitle(_translate("PreRecordSpecialityDialog", "параметры отчёта", None))
        self.chkRecordPeriod.setText(_translate("PreRecordSpecialityDialog", "Период постановки в очередь с", None))
        self.edtBegRecordDate.setDisplayFormat(_translate("PreRecordSpecialityDialog", "dd.MM.yyyy", None))
        self.lblEndRecordDate.setText(_translate("PreRecordSpecialityDialog", "по", None))
        self.chkSchedulePeriod.setText(_translate("PreRecordSpecialityDialog", "Период планируемого приёма с", None))
        self.edtBegScheduleDate.setDisplayFormat(_translate("PreRecordSpecialityDialog", "dd.MM.yyyy", None))
        self.lblEndScheduleDate.setText(_translate("PreRecordSpecialityDialog", "по", None))
        self.lblOrgStructure.setText(_translate("PreRecordSpecialityDialog", "&Подразделение", None))
        self.lblSpeciality.setText(_translate("PreRecordSpecialityDialog", "&Специальность", None))
        self.lblPerson.setText(_translate("PreRecordSpecialityDialog", "&Врач", None))
        self.lblDetail.setText(_translate("PreRecordSpecialityDialog", "&Детализировать", None))
        self.edtEndScheduleDate.setDisplayFormat(_translate("PreRecordSpecialityDialog", "dd.MM.yyyy", None))
        self.chkDetailOnPerson.setText(_translate("PreRecordSpecialityDialog", "по врачам", None))
        self.chkDetailOnOrgStructure.setText(_translate("PreRecordSpecialityDialog", "по подразделениям", None))
        self.cmbSpeciality.setWhatsThis(_translate("PreRecordSpecialityDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.edtEndRecordDate.setDisplayFormat(_translate("PreRecordSpecialityDialog", "dd.MM.yyyy", None))
        self.chkShowDeleted.setText(_translate("PreRecordSpecialityDialog", "Учитывать удаленные записи", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
