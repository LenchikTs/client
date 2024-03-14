# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_ELN\Exchange\ExportSanAviacInfoDialog.ui'
#
# Created: Mon Jul 27 08:34:18 2020
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ExportSanAviacInfoDialog(object):
    def setupUi(self, ExportSanAviacInfoDialog):
        ExportSanAviacInfoDialog.setObjectName(_fromUtf8("ExportSanAviacInfoDialog"))
        ExportSanAviacInfoDialog.resize(953, 819)
        ExportSanAviacInfoDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(ExportSanAviacInfoDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnRefresh = QtGui.QPushButton(ExportSanAviacInfoDialog)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.horizontalLayout.addWidget(self.btnRefresh)
        self.btnExport = QtGui.QPushButton(ExportSanAviacInfoDialog)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout.addWidget(self.btnExport)
        self.btnClose = QtGui.QPushButton(ExportSanAviacInfoDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 0, 1, 1)
        self.tblSanAviac = CTableView(ExportSanAviacInfoDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tblSanAviac.sizePolicy().hasHeightForWidth())
        self.tblSanAviac.setSizePolicy(sizePolicy)
        self.tblSanAviac.setObjectName(_fromUtf8("tblSanAviac"))
        self.gridLayout_2.addWidget(self.tblSanAviac, 1, 0, 1, 1)
        self.pbExportProgress = QtGui.QProgressBar(ExportSanAviacInfoDialog)
        self.pbExportProgress.setObjectName(_fromUtf8("pbExportProgress"))
        self.gridLayout_2.addWidget(self.pbExportProgress, 4, 0, 1, 1)
        self.lblSavAviacRecordCount = QtGui.QLabel(ExportSanAviacInfoDialog)
        self.lblSavAviacRecordCount.setObjectName(_fromUtf8("lblSavAviacRecordCount"))
        self.gridLayout_2.addWidget(self.lblSavAviacRecordCount, 0, 0, 1, 1)
        self.lblExportStatus = QtGui.QLabel(ExportSanAviacInfoDialog)
        self.lblExportStatus.setEnabled(True)
        self.lblExportStatus.setObjectName(_fromUtf8("lblExportStatus"))
        self.gridLayout_2.addWidget(self.lblExportStatus, 2, 0, 1, 1)
        self.edExportResults = QtGui.QPlainTextEdit(ExportSanAviacInfoDialog)
        self.edExportResults.setEnabled(True)
        self.edExportResults.setReadOnly(True)
        self.edExportResults.setObjectName(_fromUtf8("edExportResults"))
        self.gridLayout_2.addWidget(self.edExportResults, 3, 0, 1, 1)

        self.retranslateUi(ExportSanAviacInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(ExportSanAviacInfoDialog)

    def retranslateUi(self, ExportSanAviacInfoDialog):
        ExportSanAviacInfoDialog.setWindowTitle(_translate("ExportSanAviacInfoDialog", "Экспорт сведений в web-сервис \"Сан-Авиация\"", None))
        self.btnRefresh.setText(_translate("ExportSanAviacInfoDialog", "Обновить", None))
        self.btnExport.setText(_translate("ExportSanAviacInfoDialog", "Экспорт", None))
        self.btnClose.setText(_translate("ExportSanAviacInfoDialog", "Закрыть", None))
        self.pbExportProgress.setFormat(_translate("ExportSanAviacInfoDialog", "%v из %m", None))
        self.lblSavAviacRecordCount.setText(_translate("ExportSanAviacInfoDialog", "Всего записей: 0", None))
        self.lblExportStatus.setText(_translate("ExportSanAviacInfoDialog", "Отправка пакетов...", None))

from library.TableView import CTableView
