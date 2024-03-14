# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\PriceListComboBoxPopup.ui'
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

class Ui_PriceListComboBoxPopup(object):
    def setupUi(self, PriceListComboBoxPopup):
        PriceListComboBoxPopup.setObjectName(_fromUtf8("PriceListComboBoxPopup"))
        PriceListComboBoxPopup.resize(400, 272)
        self.gridLayout = QtGui.QGridLayout(PriceListComboBoxPopup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblPriceList = CTableView(PriceListComboBoxPopup)
        self.tblPriceList.setObjectName(_fromUtf8("tblPriceList"))
        self.gridLayout.addWidget(self.tblPriceList, 0, 0, 1, 1)

        self.retranslateUi(PriceListComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(PriceListComboBoxPopup)

    def retranslateUi(self, PriceListComboBoxPopup):
        PriceListComboBoxPopup.setWindowTitle(_translate("PriceListComboBoxPopup", "Dialog", None))

from library.TableView import CTableView
