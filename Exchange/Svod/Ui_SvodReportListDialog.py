# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Exchange\Svod\SvodReportListDialog.ui'
#
# Created: Wed Oct  9 09:46:53 2019
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

class Ui_SvodReportListDialog(object):
    def setupUi(self, SvodReportListDialog):
        SvodReportListDialog.setObjectName(_fromUtf8("SvodReportListDialog"))
        SvodReportListDialog.resize(1158, 795)
        self.gridLayout_3 = QtGui.QGridLayout(SvodReportListDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(SvodReportListDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpReportList = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpReportList.sizePolicy().hasHeightForWidth())
        self.grpReportList.setSizePolicy(sizePolicy)
        self.grpReportList.setObjectName(_fromUtf8("grpReportList"))
        self.gridLayout = QtGui.QGridLayout(self.grpReportList)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnNewReport = QtGui.QPushButton(self.grpReportList)
        self.btnNewReport.setObjectName(_fromUtf8("btnNewReport"))
        self.gridLayout.addWidget(self.btnNewReport, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btnDeleteReport = QtGui.QPushButton(self.grpReportList)
        self.btnDeleteReport.setEnabled(False)
        self.btnDeleteReport.setObjectName(_fromUtf8("btnDeleteReport"))
        self.gridLayout.addWidget(self.btnDeleteReport, 0, 2, 1, 1)
        self.tblReportList = CTableView(self.grpReportList)
        self.tblReportList.setObjectName(_fromUtf8("tblReportList"))
        self.gridLayout.addWidget(self.tblReportList, 1, 0, 1, 4)
        self.btnEditReport = QtGui.QPushButton(self.grpReportList)
        self.btnEditReport.setEnabled(False)
        self.btnEditReport.setObjectName(_fromUtf8("btnEditReport"))
        self.gridLayout.addWidget(self.btnEditReport, 0, 1, 1, 1)
        self.grpCurrentReport = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.grpCurrentReport.sizePolicy().hasHeightForWidth())
        self.grpCurrentReport.setSizePolicy(sizePolicy)
        self.grpCurrentReport.setObjectName(_fromUtf8("grpCurrentReport"))
        self.gridLayout_4 = QtGui.QGridLayout(self.grpCurrentReport)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.splitter_2 = QtGui.QSplitter(self.grpCurrentReport)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.splitter_2)
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.horizontalLayoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.btnCalcReportValues = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnCalcReportValues.setObjectName(_fromUtf8("btnCalcReportValues"))
        self.gridLayout_2.addWidget(self.btnCalcReportValues, 0, 0, 1, 1)
        self.btnExportReport = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnExportReport.setObjectName(_fromUtf8("btnExportReport"))
        self.gridLayout_2.addWidget(self.btnExportReport, 0, 1, 1, 1)
        self.tvReportTables = QtGui.QTreeView(self.horizontalLayoutWidget)
        self.tvReportTables.setExpandsOnDoubleClick(False)
        self.tvReportTables.setObjectName(_fromUtf8("tvReportTables"))
        self.gridLayout_2.addWidget(self.tvReportTables, 1, 0, 1, 3)
        self.tblReportTable = CReportTableView(self.splitter_2)
        self.tblReportTable.setObjectName(_fromUtf8("tblReportTable"))
        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.splitter, 3, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(SvodReportListDialog)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_3.addWidget(self.progressBar, 4, 0, 1, 1)

        self.retranslateUi(SvodReportListDialog)
        QtCore.QMetaObject.connectSlotsByName(SvodReportListDialog)

    def retranslateUi(self, SvodReportListDialog):
        SvodReportListDialog.setWindowTitle(_translate("SvodReportListDialog", "Сервис мед. статистики: список отчетов", None))
        self.grpReportList.setTitle(_translate("SvodReportListDialog", "Список отчетов", None))
        self.btnNewReport.setText(_translate("SvodReportListDialog", "Создать", None))
        self.btnDeleteReport.setText(_translate("SvodReportListDialog", "Удалить", None))
        self.btnEditReport.setText(_translate("SvodReportListDialog", "Изменить", None))
        self.grpCurrentReport.setTitle(_translate("SvodReportListDialog", "Текущий отчет", None))
        self.btnCalcReportValues.setText(_translate("SvodReportListDialog", "Заполнить автоматически", None))
        self.btnExportReport.setText(_translate("SvodReportListDialog", "Отправить", None))
        self.progressBar.setFormat(_translate("SvodReportListDialog", "Загрузка таблиц: %v / %m", None))

from Exchange.Svod.SvodReportTable import CReportTableView
from library.TableView import CTableView
