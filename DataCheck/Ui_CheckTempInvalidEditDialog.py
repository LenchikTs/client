# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_vipisnoy\DataCheck\CheckTempInvalidEditDialog.ui'
#
# Created: Thu Sep 24 15:27:24 2020
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

class Ui_CheckTempInvalidEditDialog(object):
    def setupUi(self, CheckTempInvalidEditDialog):
        CheckTempInvalidEditDialog.setObjectName(_fromUtf8("CheckTempInvalidEditDialog"))
        CheckTempInvalidEditDialog.resize(589, 538)
        self.gridLayout = QtGui.QGridLayout(CheckTempInvalidEditDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(349, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 3)
        self.lblDoctype = QtGui.QLabel(CheckTempInvalidEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDoctype.sizePolicy().hasHeightForWidth())
        self.lblDoctype.setSizePolicy(sizePolicy)
        self.lblDoctype.setObjectName(_fromUtf8("lblDoctype"))
        self.gridLayout.addWidget(self.lblDoctype, 1, 0, 1, 1)
        self.cmbDoctype = QtGui.QComboBox(CheckTempInvalidEditDialog)
        self.cmbDoctype.setObjectName(_fromUtf8("cmbDoctype"))
        self.cmbDoctype.addItem(_fromUtf8(""))
        self.cmbDoctype.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDoctype, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(349, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 3)
        self.prbCheckTempInvalid = CProgressBar(CheckTempInvalidEditDialog)
        self.prbCheckTempInvalid.setProperty("value", 24)
        self.prbCheckTempInvalid.setOrientation(QtCore.Qt.Horizontal)
        self.prbCheckTempInvalid.setObjectName(_fromUtf8("prbCheckTempInvalid"))
        self.gridLayout.addWidget(self.prbCheckTempInvalid, 3, 0, 1, 5)
        self.btnStart = QtGui.QPushButton(CheckTempInvalidEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy)
        self.btnStart.setMinimumSize(QtCore.QSize(100, 0))
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 5, 3, 1, 1)
        self.btnClose = QtGui.QPushButton(CheckTempInvalidEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 5, 4, 1, 1)
        self.frmDateRange = QtGui.QWidget(CheckTempInvalidEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmDateRange.sizePolicy().hasHeightForWidth())
        self.frmDateRange.setSizePolicy(sizePolicy)
        self.frmDateRange.setObjectName(_fromUtf8("frmDateRange"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frmDateRange)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtBegDate = CDateEdit(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setDate(QtCore.QDate(2000, 1, 1))
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.label_2 = QtGui.QLabel(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.edtEndDate = CDateEdit(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setDate(QtCore.QDate(2000, 1, 1))
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        self.gridLayout.addWidget(self.frmDateRange, 0, 0, 1, 2)
        self.tblExpertTempInvalid = CTableView(CheckTempInvalidEditDialog)
        self.tblExpertTempInvalid.setObjectName(_fromUtf8("tblExpertTempInvalid"))
        self.gridLayout.addWidget(self.tblExpertTempInvalid, 4, 0, 1, 5)
        self.labelInfo = QtGui.QLabel(CheckTempInvalidEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setText(_fromUtf8(""))
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.gridLayout.addWidget(self.labelInfo, 5, 1, 1, 2)
        self.lblCountRecords = QtGui.QLabel(CheckTempInvalidEditDialog)
        self.lblCountRecords.setObjectName(_fromUtf8("lblCountRecords"))
        self.gridLayout.addWidget(self.lblCountRecords, 5, 0, 1, 1)

        self.retranslateUi(CheckTempInvalidEditDialog)
        QtCore.QMetaObject.connectSlotsByName(CheckTempInvalidEditDialog)
        CheckTempInvalidEditDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        CheckTempInvalidEditDialog.setTabOrder(self.edtEndDate, self.cmbDoctype)
        CheckTempInvalidEditDialog.setTabOrder(self.cmbDoctype, self.tblExpertTempInvalid)
        CheckTempInvalidEditDialog.setTabOrder(self.tblExpertTempInvalid, self.btnStart)
        CheckTempInvalidEditDialog.setTabOrder(self.btnStart, self.btnClose)

    def retranslateUi(self, CheckTempInvalidEditDialog):
        CheckTempInvalidEditDialog.setWindowTitle(_translate("CheckTempInvalidEditDialog", "логический контроль ВУТ", None))
        self.lblDoctype.setText(_translate("CheckTempInvalidEditDialog", "Тип документа", None))
        self.cmbDoctype.setItemText(0, _translate("CheckTempInvalidEditDialog", "Больничный лист", None))
        self.cmbDoctype.setItemText(1, _translate("CheckTempInvalidEditDialog", "Справка", None))
        self.btnStart.setText(_translate("CheckTempInvalidEditDialog", "Начать проверку", None))
        self.btnClose.setText(_translate("CheckTempInvalidEditDialog", "Закрыть", None))
        self.label.setText(_translate("CheckTempInvalidEditDialog", "с", None))
        self.edtBegDate.setDisplayFormat(_translate("CheckTempInvalidEditDialog", "dd.MM.yyyy", None))
        self.label_2.setText(_translate("CheckTempInvalidEditDialog", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("CheckTempInvalidEditDialog", "dd.MM.yyyy", None))
        self.lblCountRecords.setText(_translate("CheckTempInvalidEditDialog", "Всего записей: 0", None))

from library.ProgressBar import CProgressBar
from library.TableView import CTableView
from library.DateEdit import CDateEdit
