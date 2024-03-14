# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Samson\UP_s11\client_test\preferences\StockPage.ui'
#
# Created: Mon Jul 10 11:35:06 2023
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

class Ui_stockPage(object):
    def setupUi(self, stockPage):
        stockPage.setObjectName(_fromUtf8("stockPage"))
        stockPage.resize(651, 405)
        stockPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(stockPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkShowOnlyCurrentAndDescendantsStock = QtGui.QCheckBox(stockPage)
        self.chkShowOnlyCurrentAndDescendantsStock.setObjectName(_fromUtf8("chkShowOnlyCurrentAndDescendantsStock"))
        self.gridLayout.addWidget(self.chkShowOnlyCurrentAndDescendantsStock, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 2, 1, 1)
        self.chkPermitRequisitionsOnlyParentStock = QtGui.QCheckBox(stockPage)
        self.chkPermitRequisitionsOnlyParentStock.setObjectName(_fromUtf8("chkPermitRequisitionsOnlyParentStock"))
        self.gridLayout.addWidget(self.chkPermitRequisitionsOnlyParentStock, 1, 0, 1, 3)
        self.chkShowMainStockRemainings = QtGui.QCheckBox(stockPage)
        self.chkShowMainStockRemainings.setObjectName(_fromUtf8("chkShowMainStockRemainings"))
        self.gridLayout.addWidget(self.chkShowMainStockRemainings, 0, 0, 1, 3)
        self.cmbAccordingRequirementsType = QtGui.QComboBox(stockPage)
        self.cmbAccordingRequirementsType.setObjectName(_fromUtf8("cmbAccordingRequirementsType"))
        self.cmbAccordingRequirementsType.addItem(_fromUtf8(""))
        self.cmbAccordingRequirementsType.addItem(_fromUtf8(""))
        self.cmbAccordingRequirementsType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAccordingRequirementsType, 4, 1, 1, 2)
        self.lblAccordingRequirementsStock = QtGui.QLabel(stockPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAccordingRequirementsStock.sizePolicy().hasHeightForWidth())
        self.lblAccordingRequirementsStock.setSizePolicy(sizePolicy)
        self.lblAccordingRequirementsStock.setObjectName(_fromUtf8("lblAccordingRequirementsStock"))
        self.gridLayout.addWidget(self.lblAccordingRequirementsStock, 4, 0, 1, 1)
        self.chkShowOnlyLsInFilterNomenklature = QtGui.QCheckBox(stockPage)
        self.chkShowOnlyLsInFilterNomenklature.setObjectName(_fromUtf8("chkShowOnlyLsInFilterNomenklature"))
        self.gridLayout.addWidget(self.chkShowOnlyLsInFilterNomenklature, 5, 0, 1, 1)

        self.retranslateUi(stockPage)
        QtCore.QMetaObject.connectSlotsByName(stockPage)
        stockPage.setTabOrder(self.chkShowMainStockRemainings, self.chkPermitRequisitionsOnlyParentStock)
        stockPage.setTabOrder(self.chkPermitRequisitionsOnlyParentStock, self.chkShowOnlyCurrentAndDescendantsStock)
        stockPage.setTabOrder(self.chkShowOnlyCurrentAndDescendantsStock, self.cmbAccordingRequirementsType)

    def retranslateUi(self, stockPage):
        stockPage.setWindowTitle(_translate("stockPage", "Складской учет", None))
        self.chkShowOnlyCurrentAndDescendantsStock.setText(_translate("stockPage", "Отображать остатки только текущего и нижестоящих складов", None))
        self.chkPermitRequisitionsOnlyParentStock.setText(_translate("stockPage", "Оформлять требования только на вышестоящий склад", None))
        self.chkShowMainStockRemainings.setText(_translate("stockPage", "Отображать остатки основного склада", None))
        self.cmbAccordingRequirementsType.setItemText(0, _translate("stockPage", "Никакие", None))
        self.cmbAccordingRequirementsType.setItemText(1, _translate("stockPage", "Только на основной склад", None))
        self.cmbAccordingRequirementsType.setItemText(2, _translate("stockPage", "Все", None))
        self.lblAccordingRequirementsStock.setText(_translate("stockPage", "Согласовывать требования", None))
        self.chkShowOnlyLsInFilterNomenklature.setText(_translate("stockPage", "Отображать только ЛС в фильтре номенклатуры", None))

