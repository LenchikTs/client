# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\PriceListDialog.ui'
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

class Ui_PriceListDialog(object):
    def setupUi(self, PriceListDialog):
        PriceListDialog.setObjectName(_fromUtf8("PriceListDialog"))
        PriceListDialog.resize(1148, 582)
        self.gridLayout_3 = QtGui.QGridLayout(PriceListDialog)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.cmbPriceList = CPriceListComboBox(PriceListDialog)
        self.cmbPriceList.setObjectName(_fromUtf8("cmbPriceList"))
        self.gridLayout_3.addWidget(self.cmbPriceList, 0, 2, 1, 1)
        self.tblContracts = CTableView(PriceListDialog)
        self.tblContracts.setObjectName(_fromUtf8("tblContracts"))
        self.gridLayout_3.addWidget(self.tblContracts, 1, 0, 1, 3)
        self.grbTariff = QtGui.QGroupBox(PriceListDialog)
        self.grbTariff.setObjectName(_fromUtf8("grbTariff"))
        self.gridLayout = QtGui.QGridLayout(self.grbTariff)
        self.gridLayout.setContentsMargins(2, -1, 2, 2)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkUpdate = QtGui.QCheckBox(self.grbTariff)
        self.chkUpdate.setChecked(True)
        self.chkUpdate.setObjectName(_fromUtf8("chkUpdate"))
        self.gridLayout.addWidget(self.chkUpdate, 0, 0, 1, 1)
        self.chkInsert = QtGui.QCheckBox(self.grbTariff)
        self.chkInsert.setChecked(True)
        self.chkInsert.setObjectName(_fromUtf8("chkInsert"))
        self.gridLayout.addWidget(self.chkInsert, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.grbTariff, 2, 0, 1, 1)
        self.grbContract = QtGui.QGroupBox(PriceListDialog)
        self.grbContract.setObjectName(_fromUtf8("grbContract"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grbContract)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btnSelectedAll = QtGui.QPushButton(self.grbContract)
        self.btnSelectedAll.setObjectName(_fromUtf8("btnSelectedAll"))
        self.gridLayout_2.addWidget(self.btnSelectedAll, 0, 0, 1, 1)
        self.btnClearAll = QtGui.QPushButton(self.grbContract)
        self.btnClearAll.setObjectName(_fromUtf8("btnClearAll"))
        self.gridLayout_2.addWidget(self.btnClearAll, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(72, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.btnEstablish = QtGui.QPushButton(self.grbContract)
        self.btnEstablish.setEnabled(False)
        self.btnEstablish.setObjectName(_fromUtf8("btnEstablish"))
        self.gridLayout_2.addWidget(self.btnEstablish, 0, 4, 1, 1)
        self.btnSynchronization = QtGui.QPushButton(self.grbContract)
        self.btnSynchronization.setEnabled(False)
        self.btnSynchronization.setObjectName(_fromUtf8("btnSynchronization"))
        self.gridLayout_2.addWidget(self.btnSynchronization, 0, 6, 1, 1)
        self.btnRegistration = QtGui.QPushButton(self.grbContract)
        self.btnRegistration.setEnabled(False)
        self.btnRegistration.setObjectName(_fromUtf8("btnRegistration"))
        self.gridLayout_2.addWidget(self.btnRegistration, 0, 7, 1, 1)
        self.btnPeriodOnPriceList = QtGui.QPushButton(self.grbContract)
        self.btnPeriodOnPriceList.setEnabled(False)
        self.btnPeriodOnPriceList.setObjectName(_fromUtf8("btnPeriodOnPriceList"))
        self.gridLayout_2.addWidget(self.btnPeriodOnPriceList, 0, 5, 1, 1)
        self.gridLayout_3.addWidget(self.grbContract, 2, 2, 1, 1)
        self.lblSelectedCount = QtGui.QLabel(PriceListDialog)
        self.lblSelectedCount.setText(_fromUtf8(""))
        self.lblSelectedCount.setObjectName(_fromUtf8("lblSelectedCount"))
        self.gridLayout_3.addWidget(self.lblSelectedCount, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PriceListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.lblInfo = QtGui.QLabel(PriceListDialog)
        self.lblInfo.setObjectName(_fromUtf8("lblInfo"))
        self.gridLayout_3.addWidget(self.lblInfo, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(PriceListDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.chkInsertExpense = QtGui.QCheckBox(self.groupBox)
        self.chkInsertExpense.setChecked(True)
        self.chkInsertExpense.setObjectName(_fromUtf8("chkInsertExpense"))
        self.gridLayout_4.addWidget(self.chkInsertExpense, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 2, 1, 1, 1)

        self.retranslateUi(PriceListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PriceListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PriceListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PriceListDialog)
        PriceListDialog.setTabOrder(self.cmbPriceList, self.tblContracts)
        PriceListDialog.setTabOrder(self.tblContracts, self.chkUpdate)
        PriceListDialog.setTabOrder(self.chkUpdate, self.chkInsert)
        PriceListDialog.setTabOrder(self.chkInsert, self.btnSelectedAll)
        PriceListDialog.setTabOrder(self.btnSelectedAll, self.btnClearAll)
        PriceListDialog.setTabOrder(self.btnClearAll, self.btnEstablish)
        PriceListDialog.setTabOrder(self.btnEstablish, self.btnPeriodOnPriceList)
        PriceListDialog.setTabOrder(self.btnPeriodOnPriceList, self.btnSynchronization)
        PriceListDialog.setTabOrder(self.btnSynchronization, self.btnRegistration)
        PriceListDialog.setTabOrder(self.btnRegistration, self.buttonBox)

    def retranslateUi(self, PriceListDialog):
        PriceListDialog.setWindowTitle(_translate("PriceListDialog", "Синхронизация договоров с прайс-листом", None))
        self.grbTariff.setTitle(_translate("PriceListDialog", "Тарифы", None))
        self.chkUpdate.setText(_translate("PriceListDialog", "Обновлять", None))
        self.chkInsert.setText(_translate("PriceListDialog", "Добавлять", None))
        self.grbContract.setTitle(_translate("PriceListDialog", "Договора", None))
        self.btnSelectedAll.setText(_translate("PriceListDialog", "Выбрать все", None))
        self.btnClearAll.setText(_translate("PriceListDialog", "Очистить выбор", None))
        self.btnEstablish.setText(_translate("PriceListDialog", "Установить", None))
        self.btnSynchronization.setText(_translate("PriceListDialog", "Синхронизация", None))
        self.btnRegistration.setText(_translate("PriceListDialog", "Регистрация", None))
        self.btnPeriodOnPriceList.setText(_translate("PriceListDialog", "Период по текущему прайс-листу", None))
        self.lblInfo.setText(_translate("PriceListDialog", "Выбрать договора из Прайс-листа:", None))
        self.groupBox.setTitle(_translate("PriceListDialog", "Статьи затрат", None))
        self.chkInsertExpense.setText(_translate("PriceListDialog", "Добавлять при регистрации", None))

from PriceListComboBox import CPriceListComboBox
from library.TableView import CTableView
