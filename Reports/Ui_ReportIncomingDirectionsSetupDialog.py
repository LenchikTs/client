# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportIncomingDirectionsSetupDialog.ui'
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

class Ui_ReportIncomingDirectionsSetupDialog(object):
    def setupUi(self, ReportIncomingDirectionsSetupDialog):
        ReportIncomingDirectionsSetupDialog.setObjectName(_fromUtf8("ReportIncomingDirectionsSetupDialog"))
        ReportIncomingDirectionsSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportIncomingDirectionsSetupDialog.resize(404, 267)
        ReportIncomingDirectionsSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportIncomingDirectionsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPerson = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 4, 0, 1, 2)
        self.cmbActionType = QtGui.QComboBox(ReportIncomingDirectionsSetupDialog)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 2, 2, 1, 3)
        self.lblActionType = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 2, 0, 1, 2)
        self.cmbActionStatus = CActionStatusComboBox(ReportIncomingDirectionsSetupDialog)
        self.cmbActionStatus.setObjectName(_fromUtf8("cmbActionStatus"))
        self.gridLayout.addWidget(self.cmbActionStatus, 3, 2, 1, 3)
        self.cmbOrganisation = COrgIsMedicalComboBox(ReportIncomingDirectionsSetupDialog)
        self.cmbOrganisation.setObjectName(_fromUtf8("cmbOrganisation"))
        self.gridLayout.addWidget(self.cmbOrganisation, 5, 2, 1, 3)
        self.cmbPerson = CPersonComboBox(ReportIncomingDirectionsSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 4, 2, 1, 3)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.edtBegDate = CDateEdit(ReportIncomingDirectionsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.lblOrganisation = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblOrganisation.setObjectName(_fromUtf8("lblOrganisation"))
        self.gridLayout.addWidget(self.lblOrganisation, 5, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ReportIncomingDirectionsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.edtEndDate = CDateEdit(ReportIncomingDirectionsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(ReportIncomingDirectionsSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(ReportIncomingDirectionsSetupDialog)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        self.lblActionStatus = QtGui.QLabel(ReportIncomingDirectionsSetupDialog)
        self.lblActionStatus.setObjectName(_fromUtf8("lblActionStatus"))
        self.gridLayout.addWidget(self.lblActionStatus, 3, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 1, 1, 1)
        self.chkDetalLPU = QtGui.QCheckBox(ReportIncomingDirectionsSetupDialog)
        self.chkDetalLPU.setChecked(True)
        self.chkDetalLPU.setObjectName(_fromUtf8("chkDetalLPU"))
        self.gridLayout.addWidget(self.chkDetalLPU, 6, 2, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrganisation.setBuddy(self.cmbOrganisation)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportIncomingDirectionsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportIncomingDirectionsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportIncomingDirectionsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportIncomingDirectionsSetupDialog)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.edtEndTime, self.cmbActionType)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.cmbActionType, self.cmbActionStatus)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.cmbActionStatus, self.cmbPerson)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.cmbPerson, self.cmbOrganisation)
        ReportIncomingDirectionsSetupDialog.setTabOrder(self.cmbOrganisation, self.buttonBox)

    def retranslateUi(self, ReportIncomingDirectionsSetupDialog):
        ReportIncomingDirectionsSetupDialog.setWindowTitle(_translate("ReportIncomingDirectionsSetupDialog", "параметры отчёта", None))
        self.lblPerson.setText(_translate("ReportIncomingDirectionsSetupDialog", "Исполнитель", None))
        self.lblActionType.setText(_translate("ReportIncomingDirectionsSetupDialog", "Тип направления", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportIncomingDirectionsSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportIncomingDirectionsSetupDialog", "Дата &начала периода", None))
        self.lblOrganisation.setText(_translate("ReportIncomingDirectionsSetupDialog", "Направитель", None))
        self.lblEndDate.setText(_translate("ReportIncomingDirectionsSetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportIncomingDirectionsSetupDialog", "dd.MM.yyyy", None))
        self.lblActionStatus.setText(_translate("ReportIncomingDirectionsSetupDialog", "Состояние", None))
        self.chkDetalLPU.setText(_translate("ReportIncomingDirectionsSetupDialog", "Детализировать по Целевым ЛПУ", None))

from Events.ActionStatus import CActionStatusComboBox
from Orgs.OrgComboBox import COrgIsMedicalComboBox
from Orgs.PersonComboBox import CPersonComboBox
from library.DateEdit import CDateEdit
