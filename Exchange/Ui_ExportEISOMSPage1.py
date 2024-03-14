# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ExportEISOMSPage1.ui'
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

class Ui_ExportEISOMSPage1(object):
    def setupUi(self, ExportEISOMSPage1):
        ExportEISOMSPage1.setObjectName(_fromUtf8("ExportEISOMSPage1"))
        ExportEISOMSPage1.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(ExportEISOMSPage1)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 4)
        self.progressBar = CProgressBar(ExportEISOMSPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 1, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 2, 0, 1, 4)
        self.btnExport = QtGui.QPushButton(ExportEISOMSPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridlayout.addWidget(self.btnExport, 11, 2, 1, 1)
        self.btnCancel = QtGui.QPushButton(ExportEISOMSPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridlayout.addWidget(self.btnCancel, 11, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 11, 0, 1, 2)
        self.chkIgnoreConfirmation = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkIgnoreConfirmation.setObjectName(_fromUtf8("chkIgnoreConfirmation"))
        self.gridlayout.addWidget(self.chkIgnoreConfirmation, 3, 0, 1, 4)
        self.chkIncludeEvents = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkIncludeEvents.setChecked(True)
        self.chkIncludeEvents.setObjectName(_fromUtf8("chkIncludeEvents"))
        self.gridlayout.addWidget(self.chkIncludeEvents, 5, 0, 1, 4)
        self.chkIncludeVisits = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkIncludeVisits.setChecked(True)
        self.chkIncludeVisits.setObjectName(_fromUtf8("chkIncludeVisits"))
        self.gridlayout.addWidget(self.chkIncludeVisits, 6, 0, 1, 4)
        self.chkIncludeActions = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkIncludeActions.setChecked(True)
        self.chkIncludeActions.setObjectName(_fromUtf8("chkIncludeActions"))
        self.gridlayout.addWidget(self.chkIncludeActions, 7, 0, 1, 4)
        self.lblEisLpuId = QtGui.QLabel(ExportEISOMSPage1)
        self.lblEisLpuId.setObjectName(_fromUtf8("lblEisLpuId"))
        self.gridlayout.addWidget(self.lblEisLpuId, 9, 0, 1, 1)
        self.edtEisLpuId = QtGui.QLineEdit(ExportEISOMSPage1)
        self.edtEisLpuId.setObjectName(_fromUtf8("edtEisLpuId"))
        self.gridlayout.addWidget(self.edtEisLpuId, 9, 1, 1, 1)
        self.chkExportClients = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkExportClients.setObjectName(_fromUtf8("chkExportClients"))
        self.gridlayout.addWidget(self.chkExportClients, 4, 0, 1, 4)
        self.chkGroupByProfile = QtGui.QCheckBox(ExportEISOMSPage1)
        self.chkGroupByProfile.setObjectName(_fromUtf8("chkGroupByProfile"))
        self.gridlayout.addWidget(self.chkGroupByProfile, 8, 0, 1, 4)
        self.lblEisLpuId.setBuddy(self.edtEisLpuId)

        self.retranslateUi(ExportEISOMSPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportEISOMSPage1)
        ExportEISOMSPage1.setTabOrder(self.btnExport, self.btnCancel)
        ExportEISOMSPage1.setTabOrder(self.btnCancel, self.chkIgnoreConfirmation)
        ExportEISOMSPage1.setTabOrder(self.chkIgnoreConfirmation, self.chkExportClients)
        ExportEISOMSPage1.setTabOrder(self.chkExportClients, self.chkIncludeEvents)
        ExportEISOMSPage1.setTabOrder(self.chkIncludeEvents, self.chkIncludeVisits)
        ExportEISOMSPage1.setTabOrder(self.chkIncludeVisits, self.chkIncludeActions)
        ExportEISOMSPage1.setTabOrder(self.chkIncludeActions, self.chkGroupByProfile)
        ExportEISOMSPage1.setTabOrder(self.chkGroupByProfile, self.edtEisLpuId)

    def retranslateUi(self, ExportEISOMSPage1):
        ExportEISOMSPage1.setWindowTitle(_translate("ExportEISOMSPage1", "Form", None))
        self.btnExport.setText(_translate("ExportEISOMSPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportEISOMSPage1", "прервать", None))
        self.chkIgnoreConfirmation.setText(_translate("ExportEISOMSPage1", "Игнорировать подтверждение оплаты или отказа", None))
        self.chkIncludeEvents.setText(_translate("ExportEISOMSPage1", "Включить информацию по событиям", None))
        self.chkIncludeVisits.setText(_translate("ExportEISOMSPage1", "Включить информацию по визитам", None))
        self.chkIncludeActions.setText(_translate("ExportEISOMSPage1", "Включить информацию по действиям", None))
        self.lblEisLpuId.setText(_translate("ExportEISOMSPage1", "Идентификатор ЛПУ в ЕИС ОМС", None))
        self.chkExportClients.setText(_translate("ExportEISOMSPage1", "Подготовить базу населения", None))
        self.chkGroupByProfile.setText(_translate("ExportEISOMSPage1", "Группировать мероприятия по профилю оплаты", None))

from library.ProgressBar import CProgressBar
