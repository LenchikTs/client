# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ExportR60NativePage1.ui'
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
        ExportPage1.resize(471, 370)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportPage1.sizePolicy().hasHeightForWidth())
        ExportPage1.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtGui.QGridLayout(ExportPage1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportPage1)
        self.chkIgnoreErrors.setObjectName(_fromUtf8("chkIgnoreErrors"))
        self.gridLayout_2.addWidget(self.chkIgnoreErrors, 3, 0, 1, 4)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout_2.addWidget(self.btnCancel, 6, 3, 1, 1)
        self.bgPerCapita = QtGui.QGroupBox(ExportPage1)
        self.bgPerCapita.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bgPerCapita.sizePolicy().hasHeightForWidth())
        self.bgPerCapita.setSizePolicy(sizePolicy)
        self.bgPerCapita.setMinimumSize(QtCore.QSize(0, 50))
        self.bgPerCapita.setObjectName(_fromUtf8("bgPerCapita"))
        self.gridLayout = QtGui.QGridLayout(self.bgPerCapita)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAmbFunding = QtGui.QLabel(self.bgPerCapita)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAmbFunding.sizePolicy().hasHeightForWidth())
        self.lblAmbFunding.setSizePolicy(sizePolicy)
        self.lblAmbFunding.setObjectName(_fromUtf8("lblAmbFunding"))
        self.gridLayout.addWidget(self.lblAmbFunding, 0, 0, 1, 1)
        self.edtAmbFunding = QtGui.QLineEdit(self.bgPerCapita)
        self.edtAmbFunding.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAmbFunding.sizePolicy().hasHeightForWidth())
        self.edtAmbFunding.setSizePolicy(sizePolicy)
        self.edtAmbFunding.setAcceptDrops(True)
        self.edtAmbFunding.setText(_fromUtf8(""))
        self.edtAmbFunding.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edtAmbFunding.setReadOnly(True)
        self.edtAmbFunding.setObjectName(_fromUtf8("edtAmbFunding"))
        self.gridLayout.addWidget(self.edtAmbFunding, 0, 2, 1, 1)
        self.lblEmgFunding = QtGui.QLabel(self.bgPerCapita)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEmgFunding.sizePolicy().hasHeightForWidth())
        self.lblEmgFunding.setSizePolicy(sizePolicy)
        self.lblEmgFunding.setObjectName(_fromUtf8("lblEmgFunding"))
        self.gridLayout.addWidget(self.lblEmgFunding, 0, 3, 1, 1)
        self.edtEmgFunding = QtGui.QLineEdit(self.bgPerCapita)
        self.edtEmgFunding.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEmgFunding.sizePolicy().hasHeightForWidth())
        self.edtEmgFunding.setSizePolicy(sizePolicy)
        self.edtEmgFunding.setText(_fromUtf8(""))
        self.edtEmgFunding.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edtEmgFunding.setReadOnly(True)
        self.edtEmgFunding.setObjectName(_fromUtf8("edtEmgFunding"))
        self.gridLayout.addWidget(self.edtEmgFunding, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.gridLayout_2.addWidget(self.bgPerCapita, 0, 0, 1, 4)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout_2.addWidget(self.logBrowser, 4, 0, 1, 4)
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 5, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(303, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 6, 0, 1, 2)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnExport.sizePolicy().hasHeightForWidth())
        self.btnExport.setSizePolicy(sizePolicy)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridLayout_2.addWidget(self.btnExport, 6, 2, 1, 1)
        self.lblExportType = QtGui.QLabel(ExportPage1)
        self.lblExportType.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblExportType.sizePolicy().hasHeightForWidth())
        self.lblExportType.setSizePolicy(sizePolicy)
        self.lblExportType.setObjectName(_fromUtf8("lblExportType"))
        self.gridLayout_2.addWidget(self.lblExportType, 1, 0, 1, 1)
        self.cmbExportType = QtGui.QComboBox(ExportPage1)
        self.cmbExportType.setEnabled(True)
        self.cmbExportType.setObjectName(_fromUtf8("cmbExportType"))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.cmbExportType.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cmbExportType, 1, 1, 1, 3)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridLayout_2.addWidget(self.chkVerboseLog, 2, 0, 1, 4)
        self.lblAmbFunding.setBuddy(self.edtAmbFunding)
        self.lblEmgFunding.setBuddy(self.edtEmgFunding)
        self.lblExportType.setBuddy(self.cmbExportType)

        self.retranslateUi(ExportPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)
        ExportPage1.setTabOrder(self.edtAmbFunding, self.cmbExportType)
        ExportPage1.setTabOrder(self.cmbExportType, self.chkVerboseLog)
        ExportPage1.setTabOrder(self.chkVerboseLog, self.chkIgnoreErrors)
        ExportPage1.setTabOrder(self.chkIgnoreErrors, self.logBrowser)
        ExportPage1.setTabOrder(self.logBrowser, self.btnExport)
        ExportPage1.setTabOrder(self.btnExport, self.btnCancel)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(_translate("ExportPage1", "Form", None))
        self.chkIgnoreErrors.setText(_translate("ExportPage1", "Игнорировать ошибки", None))
        self.btnCancel.setText(_translate("ExportPage1", "прервать", None))
        self.bgPerCapita.setTitle(_translate("ExportPage1", "Подушевое финансирование", None))
        self.lblAmbFunding.setText(_translate("ExportPage1", "Амбулаторная помощь", None))
        self.lblEmgFunding.setText(_translate("ExportPage1", "СМП", None))
        self.btnExport.setText(_translate("ExportPage1", "экспорт", None))
        self.lblExportType.setText(_translate("ExportPage1", "Тип экспорта", None))
        self.cmbExportType.setItemText(0, _translate("ExportPage1", "Предварительный реестр", None))
        self.cmbExportType.setItemText(1, _translate("ExportPage1", "Реестр(ФОМС, СМО)", None))
        self.chkVerboseLog.setText(_translate("ExportPage1", "Подробный отчет", None))

from library.ProgressBar import CProgressBar
