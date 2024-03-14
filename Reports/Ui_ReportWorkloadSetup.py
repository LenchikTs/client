# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportWorkloadSetup.ui'
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

class Ui_ReportWorkloadSetupDialog(object):
    def setupUi(self, ReportWorkloadSetupDialog):
        ReportWorkloadSetupDialog.setObjectName(_fromUtf8("ReportWorkloadSetupDialog"))
        ReportWorkloadSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportWorkloadSetupDialog.resize(436, 170)
        ReportWorkloadSetupDialog.setSizeGripEnabled(True)
        ReportWorkloadSetupDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ReportWorkloadSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frmAge = QtGui.QFrame(ReportWorkloadSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 6, 1, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(ReportWorkloadSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 6)
        spacerItem = QtGui.QSpacerItem(428, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 6)
        self.lblEventType = QtGui.QLabel(ReportWorkloadSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportWorkloadSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportWorkloadSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportWorkloadSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportWorkloadSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.wgtDatePeriodSpacer = QtGui.QWidget(ReportWorkloadSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wgtDatePeriodSpacer.sizePolicy().hasHeightForWidth())
        self.wgtDatePeriodSpacer.setSizePolicy(sizePolicy)
        self.wgtDatePeriodSpacer.setObjectName(_fromUtf8("wgtDatePeriodSpacer"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wgtDatePeriodSpacer)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(194, 7, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.wgtDatePeriodSpacer, 0, 3, 1, 3)
        self.cmbEventType = CRBComboBox(ReportWorkloadSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 5)
        self.lblOrder = QtGui.QLabel(ReportWorkloadSetupDialog)
        self.lblOrder.setObjectName(_fromUtf8("lblOrder"))
        self.gridLayout.addWidget(self.lblOrder, 7, 0, 1, 1)
        self.cmbOrderType = QtGui.QComboBox(ReportWorkloadSetupDialog)
        self.cmbOrderType.setObjectName(_fromUtf8("cmbOrderType"))
        self.cmbOrderType.addItem(_fromUtf8(""))
        self.cmbOrderType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrderType, 7, 1, 1, 5)
        self.lblEventType.setBuddy(self.cmbEventType)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportWorkloadSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportWorkloadSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportWorkloadSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportWorkloadSetupDialog)
        ReportWorkloadSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportWorkloadSetupDialog.setTabOrder(self.edtEndDate, self.cmbEventType)
        ReportWorkloadSetupDialog.setTabOrder(self.cmbEventType, self.cmbOrderType)
        ReportWorkloadSetupDialog.setTabOrder(self.cmbOrderType, self.buttonBox)

    def retranslateUi(self, ReportWorkloadSetupDialog):
        ReportWorkloadSetupDialog.setWindowTitle(_translate("ReportWorkloadSetupDialog", "параметры отчёта", None))
        self.lblEventType.setText(_translate("ReportWorkloadSetupDialog", "&Тип обращения", None))
        self.lblBegDate.setText(_translate("ReportWorkloadSetupDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("ReportWorkloadSetupDialog", "Дата &окончания периода", None))
        self.lblOrder.setText(_translate("ReportWorkloadSetupDialog", "Сортировать", None))
        self.cmbOrderType.setItemText(0, _translate("ReportWorkloadSetupDialog", "По фамилии врача", None))
        self.cmbOrderType.setItemText(1, _translate("ReportWorkloadSetupDialog", "По подразделению", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
