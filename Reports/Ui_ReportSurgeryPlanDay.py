# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportSurgeryPlanDay.ui'
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

class Ui_ReportSurgeryPlanDay(object):
    def setupUi(self, ReportSurgeryPlanDay):
        ReportSurgeryPlanDay.setObjectName(_fromUtf8("ReportSurgeryPlanDay"))
        ReportSurgeryPlanDay.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportSurgeryPlanDay.resize(436, 133)
        ReportSurgeryPlanDay.setSizeGripEnabled(True)
        ReportSurgeryPlanDay.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ReportSurgeryPlanDay)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(31, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 6, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportSurgeryPlanDay)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.frmAge = QtGui.QFrame(ReportSurgeryPlanDay)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 4, 1, 1, 4)
        self.edtDate = CDateEdit(ReportSurgeryPlanDay)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 1, 1, 2)
        self.lblActionTypeClass = QtGui.QLabel(ReportSurgeryPlanDay)
        self.lblActionTypeClass.setObjectName(_fromUtf8("lblActionTypeClass"))
        self.gridLayout.addWidget(self.lblActionTypeClass, 5, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportSurgeryPlanDay)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 8)
        spacerItem2 = QtGui.QSpacerItem(428, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 8)
        self.cmbActionTypeClass = QtGui.QComboBox(ReportSurgeryPlanDay)
        self.cmbActionTypeClass.setObjectName(_fromUtf8("cmbActionTypeClass"))
        self.cmbActionTypeClass.addItem(_fromUtf8(""))
        self.cmbActionTypeClass.addItem(_fromUtf8(""))
        self.cmbActionTypeClass.addItem(_fromUtf8(""))
        self.cmbActionTypeClass.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbActionTypeClass, 5, 1, 1, 5)
        self.lblActionType = QtGui.QLabel(ReportSurgeryPlanDay)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 6, 0, 1, 1)
        self.cmbActionType = CActionTypeComboBoxEx(ReportSurgeryPlanDay)
        self.cmbActionType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 6, 1, 1, 5)
        spacerItem3 = QtGui.QSpacerItem(81, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 6, 1, 2)
        self.lblBegDate.setBuddy(self.edtDate)
        self.lblActionTypeClass.setBuddy(self.cmbActionTypeClass)
        self.lblActionType.setBuddy(self.cmbActionType)

        self.retranslateUi(ReportSurgeryPlanDay)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportSurgeryPlanDay.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportSurgeryPlanDay.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportSurgeryPlanDay)
        ReportSurgeryPlanDay.setTabOrder(self.edtDate, self.cmbActionTypeClass)
        ReportSurgeryPlanDay.setTabOrder(self.cmbActionTypeClass, self.cmbActionType)
        ReportSurgeryPlanDay.setTabOrder(self.cmbActionType, self.buttonBox)

    def retranslateUi(self, ReportSurgeryPlanDay):
        ReportSurgeryPlanDay.setWindowTitle(_translate("ReportSurgeryPlanDay", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportSurgeryPlanDay", "Дата ", None))
        self.edtDate.setDisplayFormat(_translate("ReportSurgeryPlanDay", "dd.MM.yyyy", None))
        self.lblActionTypeClass.setText(_translate("ReportSurgeryPlanDay", "Кла&сс", None))
        self.cmbActionTypeClass.setItemText(0, _translate("ReportSurgeryPlanDay", "Статус", None))
        self.cmbActionTypeClass.setItemText(1, _translate("ReportSurgeryPlanDay", "Диагностика", None))
        self.cmbActionTypeClass.setItemText(2, _translate("ReportSurgeryPlanDay", "Лечение", None))
        self.cmbActionTypeClass.setItemText(3, _translate("ReportSurgeryPlanDay", "Прочие мероприятия", None))
        self.lblActionType.setText(_translate("ReportSurgeryPlanDay", "&Мероприятие", None))

from Events.ActionTypeComboBoxEx import CActionTypeComboBoxEx
from library.DateEdit import CDateEdit
