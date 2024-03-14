# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\PriceListComboBoxPopupEx.ui'
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

class Ui_PriceListComboBoxPopupEx(object):
    def setupUi(self, PriceListComboBoxPopupEx):
        PriceListComboBoxPopupEx.setObjectName(_fromUtf8("PriceListComboBoxPopupEx"))
        PriceListComboBoxPopupEx.resize(502, 322)
        self.gridLayout_3 = QtGui.QGridLayout(PriceListComboBoxPopupEx)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tabWidget = QtGui.QTabWidget(PriceListComboBoxPopupEx)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabContractFind = QtGui.QWidget()
        self.tabContractFind.setObjectName(_fromUtf8("tabContractFind"))
        self.gridLayout = QtGui.QGridLayout(self.tabContractFind)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblPriceListFind = CTableView(self.tabContractFind)
        self.tblPriceListFind.setObjectName(_fromUtf8("tblPriceListFind"))
        self.gridLayout.addWidget(self.tblPriceListFind, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabContractFind, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabSearch)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.tabSearch)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)
        self.label = QtGui.QLabel(self.tabSearch)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.lblFinance = QtGui.QLabel(self.tabSearch)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout_2.addWidget(self.lblFinance, 0, 0, 1, 1)
        self.edtGrouping = QtGui.QLineEdit(self.tabSearch)
        self.edtGrouping.setObjectName(_fromUtf8("edtGrouping"))
        self.gridLayout_2.addWidget(self.edtGrouping, 2, 1, 1, 5)
        self.lblResolution = QtGui.QLabel(self.tabSearch)
        self.lblResolution.setObjectName(_fromUtf8("lblResolution"))
        self.gridLayout_2.addWidget(self.lblResolution, 3, 0, 1, 1)
        self.edtResolution = QtGui.QLineEdit(self.tabSearch)
        self.edtResolution.setObjectName(_fromUtf8("edtResolution"))
        self.gridLayout_2.addWidget(self.edtResolution, 3, 1, 1, 5)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 8, 4, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(231, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 8, 0, 1, 4)
        self.lblGrouping = QtGui.QLabel(self.tabSearch)
        self.lblGrouping.setObjectName(_fromUtf8("lblGrouping"))
        self.gridLayout_2.addWidget(self.lblGrouping, 2, 0, 1, 1)
        self.lblNumber = QtGui.QLabel(self.tabSearch)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridLayout_2.addWidget(self.lblNumber, 1, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(self.tabSearch)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridLayout_2.addWidget(self.edtNumber, 1, 1, 1, 5)
        self.cmbFinance = CRBComboBox(self.tabSearch)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout_2.addWidget(self.cmbFinance, 0, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(186, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 3, 1, 3)
        self.label_3 = QtGui.QLabel(self.tabSearch)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 6, 0, 1, 1)
        self.setDate = CDateEdit(self.tabSearch)
        self.setDate.setObjectName(_fromUtf8("setDate"))
        self.gridLayout_2.addWidget(self.setDate, 4, 1, 1, 1)
        self.begDate = CDateEdit(self.tabSearch)
        self.begDate.setObjectName(_fromUtf8("begDate"))
        self.gridLayout_2.addWidget(self.begDate, 5, 1, 1, 1)
        self.endDate = CDateEdit(self.tabSearch)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.gridLayout_2.addWidget(self.endDate, 6, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 4, 2, 1, 4)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 5, 2, 1, 4)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 6, 2, 1, 4)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(PriceListComboBoxPopupEx)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PriceListComboBoxPopupEx)
        PriceListComboBoxPopupEx.setTabOrder(self.tabWidget, self.cmbFinance)
        PriceListComboBoxPopupEx.setTabOrder(self.cmbFinance, self.edtNumber)
        PriceListComboBoxPopupEx.setTabOrder(self.edtNumber, self.edtGrouping)
        PriceListComboBoxPopupEx.setTabOrder(self.edtGrouping, self.edtResolution)
        PriceListComboBoxPopupEx.setTabOrder(self.edtResolution, self.setDate)
        PriceListComboBoxPopupEx.setTabOrder(self.setDate, self.begDate)
        PriceListComboBoxPopupEx.setTabOrder(self.begDate, self.endDate)
        PriceListComboBoxPopupEx.setTabOrder(self.endDate, self.buttonBox)

    def retranslateUi(self, PriceListComboBoxPopupEx):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabContractFind), _translate("PriceListComboBoxPopupEx", "Результат поиска", None))
        self.label_2.setText(_translate("PriceListComboBoxPopupEx", "Дата начала договора", None))
        self.label.setText(_translate("PriceListComboBoxPopupEx", "Дата договора", None))
        self.lblFinance.setText(_translate("PriceListComboBoxPopupEx", "Тип финансирования", None))
        self.lblResolution.setText(_translate("PriceListComboBoxPopupEx", "Основание", None))
        self.lblGrouping.setText(_translate("PriceListComboBoxPopupEx", "Группа", None))
        self.lblNumber.setText(_translate("PriceListComboBoxPopupEx", "Номер", None))
        self.label_3.setText(_translate("PriceListComboBoxPopupEx", "Дата окончания договора", None))
        self.setDate.setDisplayFormat(_translate("PriceListComboBoxPopupEx", "dd.MM.yyyy", None))
        self.begDate.setDisplayFormat(_translate("PriceListComboBoxPopupEx", "dd.MM.yyyy", None))
        self.endDate.setDisplayFormat(_translate("PriceListComboBoxPopupEx", "dd.MM.yyyy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("PriceListComboBoxPopupEx", "&Поиск", None))

from library.DateEdit import CDateEdit
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox
