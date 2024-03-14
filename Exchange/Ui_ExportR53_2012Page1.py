# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportR53_2012Page1.ui'
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

class Ui_ExportPage1(object):
    def setupUi(self, ExportPage1):
        ExportPage1.setObjectName(_fromUtf8("ExportPage1"))
        ExportPage1.resize(508, 415)
        self.verticalLayout = QtGui.QVBoxLayout(ExportPage1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblServiceInfoFileName = QtGui.QLabel(ExportPage1)
        self.lblServiceInfoFileName.setObjectName(_fromUtf8("lblServiceInfoFileName"))
        self.verticalLayout.addWidget(self.lblServiceInfoFileName)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.edtServiceInfoFileName = QtGui.QLineEdit(ExportPage1)
        self.edtServiceInfoFileName.setObjectName(_fromUtf8("edtServiceInfoFileName"))
        self.horizontalLayout.addWidget(self.edtServiceInfoFileName)
        self.btnSelectServiceInfoFileName = QtGui.QToolButton(ExportPage1)
        self.btnSelectServiceInfoFileName.setObjectName(_fromUtf8("btnSelectServiceInfoFileName"))
        self.horizontalLayout.addWidget(self.btnSelectServiceInfoFileName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lblRegistryNumber = QtGui.QLabel(ExportPage1)
        self.lblRegistryNumber.setObjectName(_fromUtf8("lblRegistryNumber"))
        self.horizontalLayout_5.addWidget(self.lblRegistryNumber)
        self.edtRegistryNumber = QtGui.QSpinBox(ExportPage1)
        self.edtRegistryNumber.setObjectName(_fromUtf8("edtRegistryNumber"))
        self.horizontalLayout_5.addWidget(self.edtRegistryNumber)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblExportType = QtGui.QLabel(ExportPage1)
        self.lblExportType.setEnabled(True)
        self.lblExportType.setObjectName(_fromUtf8("lblExportType"))
        self.horizontalLayout_3.addWidget(self.lblExportType)
        self.cmbExportType = QtGui.QComboBox(ExportPage1)
        self.cmbExportType.setEnabled(True)
        self.cmbExportType.setObjectName(_fromUtf8("cmbExportType"))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.cmbExportType)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lblPeriod = QtGui.QLabel(ExportPage1)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.horizontalLayout_4.addWidget(self.lblPeriod)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.lblFrom = QtGui.QLabel(ExportPage1)
        self.lblFrom.setObjectName(_fromUtf8("lblFrom"))
        self.horizontalLayout_4.addWidget(self.lblFrom)
        self.edtBegDate = CDateEdit(ExportPage1)
        self.edtBegDate.setEnabled(False)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout_4.addWidget(self.edtBegDate)
        self.lblTo = QtGui.QLabel(ExportPage1)
        self.lblTo.setObjectName(_fromUtf8("lblTo"))
        self.horizontalLayout_4.addWidget(self.lblTo)
        self.edtEndDate = CDateEdit(ExportPage1)
        self.edtEndDate.setEnabled(False)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout_4.addWidget(self.edtEndDate)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.chkGroupByService = QtGui.QCheckBox(ExportPage1)
        self.chkGroupByService.setObjectName(_fromUtf8("chkGroupByService"))
        self.verticalLayout.addWidget(self.chkGroupByService)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.verticalLayout.addWidget(self.chkVerboseLog)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportPage1)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.verticalLayout.addWidget(self.chkIgnoreErrors)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.verticalLayout.addWidget(self.logBrowser)
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout_2.addWidget(self.btnExport)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ExportPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(_translate("ExportPage1", "Form", None))
        self.lblServiceInfoFileName.setText(_translate("ExportPage1", "Имя файла с информацией о предварительном реестре", None))
        self.btnSelectServiceInfoFileName.setText(_translate("ExportPage1", "...", None))
        self.lblRegistryNumber.setText(_translate("ExportPage1", "Порядковый номер реестра", None))
        self.lblExportType.setText(_translate("ExportPage1", "Тип экспорта", None))
        self.cmbExportType.setItemText(0, _translate("ExportPage1", "2012", None))
        self.cmbExportType.setItemText(1, _translate("ExportPage1", "2013 ТФОМС", None))
        self.cmbExportType.setItemText(2, _translate("ExportPage1", "Предварительный реестр - служебная информация", None))
        self.lblPeriod.setText(_translate("ExportPage1", "Период", None))
        self.lblFrom.setText(_translate("ExportPage1", "c", None))
        self.lblTo.setText(_translate("ExportPage1", "по", None))
        self.chkGroupByService.setText(_translate("ExportPage1", "Группировать по профилям оплаты", None))
        self.chkVerboseLog.setText(_translate("ExportPage1", "Подробный отчет", None))
        self.chkIgnoreErrors.setText(_translate("ExportPage1", "Игнорировать ошибки", None))
        self.btnExport.setText(_translate("ExportPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportPage1", "прервать", None))

from library.DateEdit import CDateEdit
from library.ProgressBar import CProgressBar
