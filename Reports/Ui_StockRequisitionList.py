# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\StockRequisitionList.ui'
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

class Ui_StockRequisitionList(object):
    def setupUi(self, StockRequisitionList):
        StockRequisitionList.setObjectName(_fromUtf8("StockRequisitionList"))
        StockRequisitionList.resize(402, 300)
        self.gridLayout = QtGui.QGridLayout(StockRequisitionList)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(222, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.lblUnitNameMNNRussian = QtGui.QLabel(StockRequisitionList)
        self.lblUnitNameMNNRussian.setObjectName(_fromUtf8("lblUnitNameMNNRussian"))
        self.gridLayout.addWidget(self.lblUnitNameMNNRussian, 3, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 2, 1, 1)
        self.tblStockRequisitionList = CInDocTableView(StockRequisitionList)
        self.tblStockRequisitionList.setObjectName(_fromUtf8("tblStockRequisitionList"))
        self.gridLayout.addWidget(self.tblStockRequisitionList, 0, 0, 1, 3)
        self.lblUnitNameMNNLatin = QtGui.QLabel(StockRequisitionList)
        self.lblUnitNameMNNLatin.setObjectName(_fromUtf8("lblUnitNameMNNLatin"))
        self.gridLayout.addWidget(self.lblUnitNameMNNLatin, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StockRequisitionList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.edtUnitNameMNNRussian = QtGui.QSpinBox(StockRequisitionList)
        self.edtUnitNameMNNRussian.setMaximum(4)
        self.edtUnitNameMNNRussian.setProperty("value", 0)
        self.edtUnitNameMNNRussian.setObjectName(_fromUtf8("edtUnitNameMNNRussian"))
        self.gridLayout.addWidget(self.edtUnitNameMNNRussian, 3, 1, 1, 1)
        self.edtUnitNameMNNLatin = QtGui.QSpinBox(StockRequisitionList)
        self.edtUnitNameMNNLatin.setMaximum(4)
        self.edtUnitNameMNNLatin.setProperty("value", 0)
        self.edtUnitNameMNNLatin.setObjectName(_fromUtf8("edtUnitNameMNNLatin"))
        self.gridLayout.addWidget(self.edtUnitNameMNNLatin, 4, 1, 1, 1)
        self.lblUnitNameTNRussian = QtGui.QLabel(StockRequisitionList)
        self.lblUnitNameTNRussian.setObjectName(_fromUtf8("lblUnitNameTNRussian"))
        self.gridLayout.addWidget(self.lblUnitNameTNRussian, 1, 0, 1, 1)
        self.edtUnitNameTNLatin = QtGui.QSpinBox(StockRequisitionList)
        self.edtUnitNameTNLatin.setMaximum(4)
        self.edtUnitNameTNLatin.setProperty("value", 0)
        self.edtUnitNameTNLatin.setObjectName(_fromUtf8("edtUnitNameTNLatin"))
        self.gridLayout.addWidget(self.edtUnitNameTNLatin, 2, 1, 1, 1)
        self.lblUnitNameTNLatin = QtGui.QLabel(StockRequisitionList)
        self.lblUnitNameTNLatin.setObjectName(_fromUtf8("lblUnitNameTNLatin"))
        self.gridLayout.addWidget(self.lblUnitNameTNLatin, 2, 0, 1, 1)
        self.edtUnitNameTNRussian = QtGui.QSpinBox(StockRequisitionList)
        self.edtUnitNameTNRussian.setMaximum(4)
        self.edtUnitNameTNRussian.setProperty("value", 0)
        self.edtUnitNameTNRussian.setObjectName(_fromUtf8("edtUnitNameTNRussian"))
        self.gridLayout.addWidget(self.edtUnitNameTNRussian, 1, 1, 1, 1)

        self.retranslateUi(StockRequisitionList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StockRequisitionList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StockRequisitionList.reject)
        QtCore.QMetaObject.connectSlotsByName(StockRequisitionList)

    def retranslateUi(self, StockRequisitionList):
        StockRequisitionList.setWindowTitle(_translate("StockRequisitionList", "Параметры формирования", None))
        self.lblUnitNameMNNRussian.setText(_translate("StockRequisitionList", "МНН на русском", None))
        self.lblUnitNameMNNLatin.setText(_translate("StockRequisitionList", "МНН на латинском", None))
        self.lblUnitNameTNRussian.setText(_translate("StockRequisitionList", "ТН на русском", None))
        self.lblUnitNameTNLatin.setText(_translate("StockRequisitionList", "ТН на латинском", None))

from library.InDocTable import CInDocTableView
