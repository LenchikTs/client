# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Exchange\ExportDispPlanDiagnosisDialog.ui'
#
# Created: Tue Feb 19 09:47:10 2019
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

class Ui_ExportDispPlanDiagnosisDialog(object):
    def setupUi(self, ExportDispPlanDiagnosisDialog):
        ExportDispPlanDiagnosisDialog.setObjectName(_fromUtf8("ExportDispPlanDiagnosisDialog"))
        ExportDispPlanDiagnosisDialog.resize(914, 681)
        self.gridLayout_2 = QtGui.QGridLayout(ExportDispPlanDiagnosisDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnExport = QtGui.QPushButton(ExportDispPlanDiagnosisDialog)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout.addWidget(self.btnExport)
        self.btnClose = QtGui.QPushButton(ExportDispPlanDiagnosisDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.gridLayout_2.addLayout(self.horizontalLayout, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.sbYear = QtGui.QSpinBox(ExportDispPlanDiagnosisDialog)
        self.sbYear.setMinimum(2017)
        self.sbYear.setMaximum(9999)
        self.sbYear.setObjectName(_fromUtf8("sbYear"))
        self.horizontalLayout_2.addWidget(self.sbYear)
        self.label_2 = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cmbMonthFrom = QtGui.QComboBox(ExportDispPlanDiagnosisDialog)
        self.cmbMonthFrom.setObjectName(_fromUtf8("cmbMonthFrom"))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.cmbMonthFrom.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cmbMonthFrom)
        self.label_3 = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cmbMonthTo = QtGui.QComboBox(ExportDispPlanDiagnosisDialog)
        self.cmbMonthTo.setObjectName(_fromUtf8("cmbMonthTo"))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.cmbMonthTo.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cmbMonthTo)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.pbExportProgress = QtGui.QProgressBar(ExportDispPlanDiagnosisDialog)
        self.pbExportProgress.setObjectName(_fromUtf8("pbExportProgress"))
        self.gridLayout_2.addWidget(self.pbExportProgress, 6, 0, 1, 1)
        self.lblPlanCount = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.lblPlanCount.setObjectName(_fromUtf8("lblPlanCount"))
        self.gridLayout_2.addWidget(self.lblPlanCount, 1, 0, 1, 1)
        self.tblDispPlan = CTableView(ExportDispPlanDiagnosisDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tblDispPlan.sizePolicy().hasHeightForWidth())
        self.tblDispPlan.setSizePolicy(sizePolicy)
        self.tblDispPlan.setObjectName(_fromUtf8("tblDispPlan"))
        self.gridLayout_2.addWidget(self.tblDispPlan, 2, 0, 1, 1)
        self.lblExportStatus = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.lblExportStatus.setObjectName(_fromUtf8("lblExportStatus"))
        self.gridLayout_2.addWidget(self.lblExportStatus, 5, 0, 1, 1)
        self.tblDispPlanErrors = CTableView(ExportDispPlanDiagnosisDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tblDispPlanErrors.sizePolicy().hasHeightForWidth())
        self.tblDispPlanErrors.setSizePolicy(sizePolicy)
        self.tblDispPlanErrors.setObjectName(_fromUtf8("tblDispPlanErrors"))
        self.gridLayout_2.addWidget(self.tblDispPlanErrors, 4, 0, 1, 1)
        self.label_4 = QtGui.QLabel(ExportDispPlanDiagnosisDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.retranslateUi(ExportDispPlanDiagnosisDialog)
        self.cmbMonthFrom.setCurrentIndex(0)
        self.cmbMonthTo.setCurrentIndex(11)
        QtCore.QMetaObject.connectSlotsByName(ExportDispPlanDiagnosisDialog)

    def retranslateUi(self, ExportDispPlanDiagnosisDialog):
        ExportDispPlanDiagnosisDialog.setWindowTitle(_translate("ExportDispPlanDiagnosisDialog", "Экспорт списка лиц, для которых запланированы диспансерные осмотры по заболеванию", None))
        self.btnExport.setText(_translate("ExportDispPlanDiagnosisDialog", "Экспорт", None))
        self.btnClose.setText(_translate("ExportDispPlanDiagnosisDialog", "Закрыть", None))
        self.label.setText(_translate("ExportDispPlanDiagnosisDialog", "Год", None))
        self.label_2.setText(_translate("ExportDispPlanDiagnosisDialog", "Месяцы: с", None))
        self.cmbMonthFrom.setItemText(0, _translate("ExportDispPlanDiagnosisDialog", "января", None))
        self.cmbMonthFrom.setItemText(1, _translate("ExportDispPlanDiagnosisDialog", "февраля", None))
        self.cmbMonthFrom.setItemText(2, _translate("ExportDispPlanDiagnosisDialog", "марта", None))
        self.cmbMonthFrom.setItemText(3, _translate("ExportDispPlanDiagnosisDialog", "апреля", None))
        self.cmbMonthFrom.setItemText(4, _translate("ExportDispPlanDiagnosisDialog", "мая", None))
        self.cmbMonthFrom.setItemText(5, _translate("ExportDispPlanDiagnosisDialog", "июня", None))
        self.cmbMonthFrom.setItemText(6, _translate("ExportDispPlanDiagnosisDialog", "июля", None))
        self.cmbMonthFrom.setItemText(7, _translate("ExportDispPlanDiagnosisDialog", "августа", None))
        self.cmbMonthFrom.setItemText(8, _translate("ExportDispPlanDiagnosisDialog", "сентября", None))
        self.cmbMonthFrom.setItemText(9, _translate("ExportDispPlanDiagnosisDialog", "октября", None))
        self.cmbMonthFrom.setItemText(10, _translate("ExportDispPlanDiagnosisDialog", "ноября", None))
        self.cmbMonthFrom.setItemText(11, _translate("ExportDispPlanDiagnosisDialog", "декабря", None))
        self.label_3.setText(_translate("ExportDispPlanDiagnosisDialog", "по", None))
        self.cmbMonthTo.setItemText(0, _translate("ExportDispPlanDiagnosisDialog", "январь", None))
        self.cmbMonthTo.setItemText(1, _translate("ExportDispPlanDiagnosisDialog", "февраль", None))
        self.cmbMonthTo.setItemText(2, _translate("ExportDispPlanDiagnosisDialog", "март", None))
        self.cmbMonthTo.setItemText(3, _translate("ExportDispPlanDiagnosisDialog", "апрель", None))
        self.cmbMonthTo.setItemText(4, _translate("ExportDispPlanDiagnosisDialog", "май", None))
        self.cmbMonthTo.setItemText(5, _translate("ExportDispPlanDiagnosisDialog", "июнь", None))
        self.cmbMonthTo.setItemText(6, _translate("ExportDispPlanDiagnosisDialog", "июль", None))
        self.cmbMonthTo.setItemText(7, _translate("ExportDispPlanDiagnosisDialog", "август", None))
        self.cmbMonthTo.setItemText(8, _translate("ExportDispPlanDiagnosisDialog", "сентябрь", None))
        self.cmbMonthTo.setItemText(9, _translate("ExportDispPlanDiagnosisDialog", "октябрь", None))
        self.cmbMonthTo.setItemText(10, _translate("ExportDispPlanDiagnosisDialog", "ноябрь", None))
        self.cmbMonthTo.setItemText(11, _translate("ExportDispPlanDiagnosisDialog", "декабрь", None))
        self.pbExportProgress.setFormat(_translate("ExportDispPlanDiagnosisDialog", "%v из %m", None))
        self.lblPlanCount.setText(_translate("ExportDispPlanDiagnosisDialog", "Запланировано: 0", None))
        self.lblExportStatus.setText(_translate("ExportDispPlanDiagnosisDialog", "Отправка пакетов...", None))
        self.label_4.setText(_translate("ExportDispPlanDiagnosisDialog", "Ошибки:", None))

from library.TableView import CTableView
