# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_ekslp\library\ESKLP\ESKLPComboBoxPopup.ui'
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

class Ui_ESKLPComboBoxPopup(object):
    def setupUi(self, ESKLPComboBoxPopup):
        ESKLPComboBoxPopup.setObjectName(_fromUtf8("ESKLPComboBoxPopup"))
        ESKLPComboBoxPopup.resize(1050, 374)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ESKLPComboBoxPopup.sizePolicy().hasHeightForWidth())
        ESKLPComboBoxPopup.setSizePolicy(sizePolicy)
        self.gridlayout = QtGui.QGridLayout(ESKLPComboBoxPopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(ESKLPComboBoxPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabResult = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabResult.sizePolicy().hasHeightForWidth())
        self.tabResult.setSizePolicy(sizePolicy)
        self.tabResult.setObjectName(_fromUtf8("tabResult"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabResult)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tblESKLP = CTableView(self.tabResult)
        self.tblESKLP.setObjectName(_fromUtf8("tblESKLP"))
        self.vboxlayout.addWidget(self.tblESKLP)
        self.tabWidget.addTab(self.tabResult, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabSearch.sizePolicy().hasHeightForWidth())
        self.tabSearch.setSizePolicy(sizePolicy)
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridLayout = QtGui.QGridLayout(self.tabSearch)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtESKLPCode = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPCode.setObjectName(_fromUtf8("edtESKLPCode"))
        self.gridLayout.addWidget(self.edtESKLPCode, 0, 2, 1, 3)
        self.edtESKLPMnn_norm_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPMnn_norm_name.setObjectName(_fromUtf8("edtESKLPMnn_norm_name"))
        self.gridLayout.addWidget(self.edtESKLPMnn_norm_name, 1, 2, 1, 3)
        self.lblESKLPMnn_norm_name = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPMnn_norm_name.sizePolicy().hasHeightForWidth())
        self.lblESKLPMnn_norm_name.setSizePolicy(sizePolicy)
        self.lblESKLPMnn_norm_name.setObjectName(_fromUtf8("lblESKLPMnn_norm_name"))
        self.gridLayout.addWidget(self.lblESKLPMnn_norm_name, 1, 0, 1, 1)
        self.lblESKLPCode = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPCode.sizePolicy().hasHeightForWidth())
        self.lblESKLPCode.setSizePolicy(sizePolicy)
        self.lblESKLPCode.setObjectName(_fromUtf8("lblESKLPCode"))
        self.gridLayout.addWidget(self.lblESKLPCode, 0, 0, 1, 1)
        self.edtESKLPLf_norm_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPLf_norm_name.setObjectName(_fromUtf8("edtESKLPLf_norm_name"))
        self.gridLayout.addWidget(self.edtESKLPLf_norm_name, 3, 2, 1, 3)
        self.lblESKLPLf_norm_name = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPLf_norm_name.sizePolicy().hasHeightForWidth())
        self.lblESKLPLf_norm_name.setSizePolicy(sizePolicy)
        self.lblESKLPLf_norm_name.setObjectName(_fromUtf8("lblESKLPLf_norm_name"))
        self.gridLayout.addWidget(self.lblESKLPLf_norm_name, 3, 0, 1, 1)
        self.edtESKLPDosage_norm_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPDosage_norm_name.setObjectName(_fromUtf8("edtESKLPDosage_norm_name"))
        self.gridLayout.addWidget(self.edtESKLPDosage_norm_name, 2, 2, 1, 3)
        self.edtESKLPTrade_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPTrade_name.setObjectName(_fromUtf8("edtESKLPTrade_name"))
        self.gridLayout.addWidget(self.edtESKLPTrade_name, 4, 2, 1, 3)
        self.lblESKLPDosage_norm_name = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPDosage_norm_name.sizePolicy().hasHeightForWidth())
        self.lblESKLPDosage_norm_name.setSizePolicy(sizePolicy)
        self.lblESKLPDosage_norm_name.setObjectName(_fromUtf8("lblESKLPDosage_norm_name"))
        self.gridLayout.addWidget(self.lblESKLPDosage_norm_name, 2, 0, 1, 1)
        self.lblESKLPTrade_name = QtGui.QLabel(self.tabSearch)
        self.lblESKLPTrade_name.setObjectName(_fromUtf8("lblESKLPTrade_name"))
        self.gridLayout.addWidget(self.lblESKLPTrade_name, 4, 0, 1, 1)
        self.lblESKLPPack1_name = QtGui.QLabel(self.tabSearch)
        self.lblESKLPPack1_name.setObjectName(_fromUtf8("lblESKLPPack1_name"))
        self.gridLayout.addWidget(self.lblESKLPPack1_name, 5, 0, 1, 1)
        self.edtESKLPPack1_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPPack1_name.setObjectName(_fromUtf8("edtESKLPPack1_name"))
        self.gridLayout.addWidget(self.edtESKLPPack1_name, 5, 2, 1, 3)
        self.lblESKLPPack2_name = QtGui.QLabel(self.tabSearch)
        self.lblESKLPPack2_name.setObjectName(_fromUtf8("lblESKLPPack2_name"))
        self.gridLayout.addWidget(self.lblESKLPPack2_name, 6, 0, 1, 1)
        self.edtESKLPPack2_name = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPPack2_name.setObjectName(_fromUtf8("edtESKLPPack2_name"))
        self.gridLayout.addWidget(self.edtESKLPPack2_name, 6, 2, 1, 3)
        self.lblESKLPNum_reg = QtGui.QLabel(self.tabSearch)
        self.lblESKLPNum_reg.setObjectName(_fromUtf8("lblESKLPNum_reg"))
        self.gridLayout.addWidget(self.lblESKLPNum_reg, 7, 0, 1, 1)
        self.edtESKLPNum_reg = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPNum_reg.setObjectName(_fromUtf8("edtESKLPNum_reg"))
        self.gridLayout.addWidget(self.edtESKLPNum_reg, 7, 2, 1, 3)
        self.edtESKLPManufacturer = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPManufacturer.setObjectName(_fromUtf8("edtESKLPManufacturer"))
        self.gridLayout.addWidget(self.edtESKLPManufacturer, 8, 2, 1, 3)
        self.lblESKLPManufacturer = QtGui.QLabel(self.tabSearch)
        self.lblESKLPManufacturer.setObjectName(_fromUtf8("lblESKLPManufacturer"))
        self.gridLayout.addWidget(self.lblESKLPManufacturer, 8, 0, 1, 1)
        self.layoutBegDate = QtGui.QHBoxLayout()
        self.layoutBegDate.setObjectName(_fromUtf8("layoutBegDate"))
        self.chkBegDateWithBeg = QtGui.QCheckBox(self.tabSearch)
        self.chkBegDateWithBeg.setObjectName(_fromUtf8("chkBegDateWithBeg"))
        self.layoutBegDate.addWidget(self.chkBegDateWithBeg)
        self.edtBegDate = CDateEdit(self.tabSearch)
        self.edtBegDate.setEnabled(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.layoutBegDate.addWidget(self.edtBegDate)
        self.chkBegDateWithEnd = QtGui.QCheckBox(self.tabSearch)
        self.chkBegDateWithEnd.setObjectName(_fromUtf8("chkBegDateWithEnd"))
        self.layoutBegDate.addWidget(self.chkBegDateWithEnd)
        self.edtBegDate_2 = CDateEdit(self.tabSearch)
        self.edtBegDate_2.setEnabled(True)
        self.edtBegDate_2.setObjectName(_fromUtf8("edtBegDate_2"))
        self.layoutBegDate.addWidget(self.edtBegDate_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layoutBegDate.addItem(spacerItem)
        self.gridLayout.addLayout(self.layoutBegDate, 9, 2, 1, 1)
        self.edtESKLP_GTIN = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLP_GTIN.setEnabled(False)
        self.edtESKLP_GTIN.setObjectName(_fromUtf8("edtESKLP_GTIN"))
        self.gridLayout.addWidget(self.edtESKLP_GTIN, 11, 2, 1, 1)
        self.layoutEndDate = QtGui.QHBoxLayout()
        self.layoutEndDate.setObjectName(_fromUtf8("layoutEndDate"))
        self.chkEndDateWithBeg = QtGui.QCheckBox(self.tabSearch)
        self.chkEndDateWithBeg.setObjectName(_fromUtf8("chkEndDateWithBeg"))
        self.layoutEndDate.addWidget(self.chkEndDateWithBeg)
        self.edtEndDate = CDateEdit(self.tabSearch)
        self.edtEndDate.setEnabled(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.layoutEndDate.addWidget(self.edtEndDate)
        self.chkEndDateWithEnd = QtGui.QCheckBox(self.tabSearch)
        self.chkEndDateWithEnd.setObjectName(_fromUtf8("chkEndDateWithEnd"))
        self.layoutEndDate.addWidget(self.chkEndDateWithEnd)
        self.edtEndDate_2 = CDateEdit(self.tabSearch)
        self.edtEndDate_2.setEnabled(True)
        self.edtEndDate_2.setObjectName(_fromUtf8("edtEndDate_2"))
        self.layoutEndDate.addWidget(self.edtEndDate_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layoutEndDate.addItem(spacerItem1)
        self.gridLayout.addLayout(self.layoutEndDate, 10, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 4, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 13, 3, 1, 1)
        self.lblBegDateRecord = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDateRecord.sizePolicy().hasHeightForWidth())
        self.lblBegDateRecord.setSizePolicy(sizePolicy)
        self.lblBegDateRecord.setObjectName(_fromUtf8("lblBegDateRecord"))
        self.gridLayout.addWidget(self.lblBegDateRecord, 9, 0, 1, 1)
        self.lblEndDateRecord = QtGui.QLabel(self.tabSearch)
        self.lblEndDateRecord.setObjectName(_fromUtf8("lblEndDateRecord"))
        self.gridLayout.addWidget(self.lblEndDateRecord, 10, 0, 1, 1)
        self.chkESKLP_GTIN = QtGui.QCheckBox(self.tabSearch)
        self.chkESKLP_GTIN.setObjectName(_fromUtf8("chkESKLP_GTIN"))
        self.gridLayout.addWidget(self.chkESKLP_GTIN, 11, 0, 1, 1)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.lblESKLPMnn_norm_name.setBuddy(self.edtESKLPMnn_norm_name)
        self.lblESKLPCode.setBuddy(self.edtESKLPCode)
        self.lblESKLPDosage_norm_name.setBuddy(self.edtESKLPDosage_norm_name)
        self.lblESKLPPack2_name.setBuddy(self.edtESKLPPack2_name)

        self.retranslateUi(ESKLPComboBoxPopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.chkESKLP_GTIN, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtESKLP_GTIN.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ESKLPComboBoxPopup)
        ESKLPComboBoxPopup.setTabOrder(self.tabWidget, self.edtESKLPCode)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPCode, self.edtESKLPMnn_norm_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPMnn_norm_name, self.edtESKLPDosage_norm_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPDosage_norm_name, self.edtESKLPLf_norm_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPLf_norm_name, self.edtESKLPTrade_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPTrade_name, self.edtESKLPPack1_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPPack1_name, self.edtESKLPPack2_name)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPPack2_name, self.edtESKLPNum_reg)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPNum_reg, self.edtESKLPManufacturer)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLPManufacturer, self.chkBegDateWithBeg)
        ESKLPComboBoxPopup.setTabOrder(self.chkBegDateWithBeg, self.chkBegDateWithEnd)
        ESKLPComboBoxPopup.setTabOrder(self.chkBegDateWithEnd, self.chkEndDateWithBeg)
        ESKLPComboBoxPopup.setTabOrder(self.chkEndDateWithBeg, self.chkEndDateWithEnd)
        ESKLPComboBoxPopup.setTabOrder(self.chkEndDateWithEnd, self.edtESKLP_GTIN)
        ESKLPComboBoxPopup.setTabOrder(self.edtESKLP_GTIN, self.buttonBox)
        ESKLPComboBoxPopup.setTabOrder(self.buttonBox, self.edtEndDate_2)
        ESKLPComboBoxPopup.setTabOrder(self.edtEndDate_2, self.edtBegDate)
        ESKLPComboBoxPopup.setTabOrder(self.edtBegDate, self.edtEndDate)
        ESKLPComboBoxPopup.setTabOrder(self.edtEndDate, self.edtBegDate_2)
        ESKLPComboBoxPopup.setTabOrder(self.edtBegDate_2, self.tblESKLP)

    def retranslateUi(self, ESKLPComboBoxPopup):
        ESKLPComboBoxPopup.setWindowTitle(_translate("ESKLPComboBoxPopup", "ЕСКЛП", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResult), _translate("ESKLPComboBoxPopup", "Результат поиска", None))
        self.lblESKLPMnn_norm_name.setText(_translate("ESKLPComboBoxPopup", "Нормализованное описание (исходное) МНН", None))
        self.lblESKLPCode.setText(_translate("ESKLPComboBoxPopup", "Код каталога для позиции КЛП", None))
        self.lblESKLPLf_norm_name.setText(_translate("ESKLPComboBoxPopup", "Нормализованное название (исходное) лекарственной формы", None))
        self.lblESKLPDosage_norm_name.setText(_translate("ESKLPComboBoxPopup", "Нормализованное описание (исходное) дозировки", None))
        self.lblESKLPTrade_name.setText(_translate("ESKLPComboBoxPopup", "Торговое наименование", None))
        self.lblESKLPPack1_name.setText(_translate("ESKLPComboBoxPopup", "Название первичной упаковки", None))
        self.lblESKLPPack2_name.setText(_translate("ESKLPComboBoxPopup", "Название потребительской упаковки", None))
        self.lblESKLPNum_reg.setText(_translate("ESKLPComboBoxPopup", "Номер регистрационного удостоверения лекарственного препарата", None))
        self.lblESKLPManufacturer.setText(_translate("ESKLPComboBoxPopup", "Название производителя лекарственного препарата", None))
        self.chkBegDateWithBeg.setText(_translate("ESKLPComboBoxPopup", "С", None))
        self.chkBegDateWithEnd.setText(_translate("ESKLPComboBoxPopup", "по", None))
        self.chkEndDateWithBeg.setText(_translate("ESKLPComboBoxPopup", "С", None))
        self.chkEndDateWithEnd.setText(_translate("ESKLPComboBoxPopup", "по", None))
        self.lblBegDateRecord.setText(_translate("ESKLPComboBoxPopup", "Дата начала действия записи", None))
        self.lblEndDateRecord.setText(_translate("ESKLPComboBoxPopup", "Дата окончания действия записи", None))
        self.chkESKLP_GTIN.setText(_translate("ESKLPComboBoxPopup", "GTIN", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("ESKLPComboBoxPopup", "&Поиск", None))

from library.DateEdit import CDateEdit
from library.TableView import CTableView
