# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_ekslp\library\ESKLP\ESKLPSmnnComboBoxPopup.ui'
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

class Ui_ESKLPSmnnComboBoxPopup(object):
    def setupUi(self, ESKLPSmnnComboBoxPopup):
        ESKLPSmnnComboBoxPopup.setObjectName(_fromUtf8("ESKLPSmnnComboBoxPopup"))
        ESKLPSmnnComboBoxPopup.resize(854, 261)
        self.gridlayout = QtGui.QGridLayout(ESKLPSmnnComboBoxPopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(ESKLPSmnnComboBoxPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabResult = QtGui.QWidget()
        self.tabResult.setObjectName(_fromUtf8("tabResult"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabResult)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tblESKLPSmnn = CTableView(self.tabResult)
        self.tblESKLPSmnn.setObjectName(_fromUtf8("tblESKLPSmnn"))
        self.vboxlayout.addWidget(self.tblESKLPSmnn)
        self.tabWidget.addTab(self.tabResult, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridlayout1 = QtGui.QGridLayout(self.tabSearch)
        self.gridlayout1.setMargin(4)
        self.gridlayout1.setSpacing(4)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.lblESKLPSmnnCode = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPSmnnCode.sizePolicy().hasHeightForWidth())
        self.lblESKLPSmnnCode.setSizePolicy(sizePolicy)
        self.lblESKLPSmnnCode.setObjectName(_fromUtf8("lblESKLPSmnnCode"))
        self.gridlayout1.addWidget(self.lblESKLPSmnnCode, 0, 0, 1, 1)
        self.edtESKLPSmnnCode = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPSmnnCode.setObjectName(_fromUtf8("edtESKLPSmnnCode"))
        self.gridlayout1.addWidget(self.edtESKLPSmnnCode, 0, 1, 1, 2)
        self.lblESKLPSmnn_mnn = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPSmnn_mnn.sizePolicy().hasHeightForWidth())
        self.lblESKLPSmnn_mnn.setSizePolicy(sizePolicy)
        self.lblESKLPSmnn_mnn.setObjectName(_fromUtf8("lblESKLPSmnn_mnn"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_mnn, 1, 0, 1, 1)
        self.edtESKLPSmnn_mnn = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPSmnn_mnn.setObjectName(_fromUtf8("edtESKLPSmnn_mnn"))
        self.gridlayout1.addWidget(self.edtESKLPSmnn_mnn, 1, 1, 1, 2)
        self.lblESKLPSmnn_form = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPSmnn_form.sizePolicy().hasHeightForWidth())
        self.lblESKLPSmnn_form.setSizePolicy(sizePolicy)
        self.lblESKLPSmnn_form.setObjectName(_fromUtf8("lblESKLPSmnn_form"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_form, 2, 0, 1, 1)
        self.lblESKLPSmnn_ftg = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblESKLPSmnn_ftg.sizePolicy().hasHeightForWidth())
        self.lblESKLPSmnn_ftg.setSizePolicy(sizePolicy)
        self.lblESKLPSmnn_ftg.setObjectName(_fromUtf8("lblESKLPSmnn_ftg"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_ftg, 3, 0, 1, 1)
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
        self.gridlayout1.addWidget(self.buttonBox, 7, 2, 1, 1)
        self.edtESKLPSmnn_form = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPSmnn_form.setObjectName(_fromUtf8("edtESKLPSmnn_form"))
        self.gridlayout1.addWidget(self.edtESKLPSmnn_form, 2, 1, 1, 2)
        self.lblESKLPSmnn_is_znvlp = QtGui.QLabel(self.tabSearch)
        self.lblESKLPSmnn_is_znvlp.setObjectName(_fromUtf8("lblESKLPSmnn_is_znvlp"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_is_znvlp, 4, 0, 1, 1)
        self.lblESKLPSmnn_is_narcotic = QtGui.QLabel(self.tabSearch)
        self.lblESKLPSmnn_is_narcotic.setObjectName(_fromUtf8("lblESKLPSmnn_is_narcotic"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_is_narcotic, 5, 0, 1, 1)
        self.edtESKLPSmnn_Dosage_grls_value = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPSmnn_Dosage_grls_value.setObjectName(_fromUtf8("edtESKLPSmnn_Dosage_grls_value"))
        self.gridlayout1.addWidget(self.edtESKLPSmnn_Dosage_grls_value, 6, 1, 1, 2)
        self.lblESKLPSmnn_Dosage_grls_value = QtGui.QLabel(self.tabSearch)
        self.lblESKLPSmnn_Dosage_grls_value.setObjectName(_fromUtf8("lblESKLPSmnn_Dosage_grls_value"))
        self.gridlayout1.addWidget(self.lblESKLPSmnn_Dosage_grls_value, 6, 0, 1, 1)
        self.edtESKLPSmnn_ftg = QtGui.QLineEdit(self.tabSearch)
        self.edtESKLPSmnn_ftg.setObjectName(_fromUtf8("edtESKLPSmnn_ftg"))
        self.gridlayout1.addWidget(self.edtESKLPSmnn_ftg, 3, 1, 1, 2)
        self.cmbESKLPSmnn_is_narcotic = QtGui.QComboBox(self.tabSearch)
        self.cmbESKLPSmnn_is_narcotic.setObjectName(_fromUtf8("cmbESKLPSmnn_is_narcotic"))
        self.cmbESKLPSmnn_is_narcotic.addItem(_fromUtf8(""))
        self.cmbESKLPSmnn_is_narcotic.addItem(_fromUtf8(""))
        self.cmbESKLPSmnn_is_narcotic.addItem(_fromUtf8(""))
        self.gridlayout1.addWidget(self.cmbESKLPSmnn_is_narcotic, 5, 1, 1, 2)
        self.cmbESKLPSmnn_is_znvlp = QtGui.QComboBox(self.tabSearch)
        self.cmbESKLPSmnn_is_znvlp.setObjectName(_fromUtf8("cmbESKLPSmnn_is_znvlp"))
        self.cmbESKLPSmnn_is_znvlp.addItem(_fromUtf8(""))
        self.cmbESKLPSmnn_is_znvlp.addItem(_fromUtf8(""))
        self.cmbESKLPSmnn_is_znvlp.addItem(_fromUtf8(""))
        self.gridlayout1.addWidget(self.cmbESKLPSmnn_is_znvlp, 4, 1, 1, 2)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.lblESKLPSmnnCode.setBuddy(self.edtESKLPSmnnCode)
        self.lblESKLPSmnn_mnn.setBuddy(self.edtESKLPSmnn_mnn)
        self.lblESKLPSmnn_form.setBuddy(self.edtESKLPSmnn_form)
        self.lblESKLPSmnn_Dosage_grls_value.setBuddy(self.edtESKLPSmnn_Dosage_grls_value)

        self.retranslateUi(ESKLPSmnnComboBoxPopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ESKLPSmnnComboBoxPopup)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.tabWidget, self.edtESKLPSmnnCode)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.edtESKLPSmnnCode, self.edtESKLPSmnn_mnn)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.edtESKLPSmnn_mnn, self.edtESKLPSmnn_form)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.edtESKLPSmnn_form, self.edtESKLPSmnn_ftg)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.edtESKLPSmnn_ftg, self.cmbESKLPSmnn_is_znvlp)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.cmbESKLPSmnn_is_znvlp, self.cmbESKLPSmnn_is_narcotic)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.cmbESKLPSmnn_is_narcotic, self.edtESKLPSmnn_Dosage_grls_value)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.edtESKLPSmnn_Dosage_grls_value, self.buttonBox)
        ESKLPSmnnComboBoxPopup.setTabOrder(self.buttonBox, self.tblESKLPSmnn)

    def retranslateUi(self, ESKLPSmnnComboBoxPopup):
        ESKLPSmnnComboBoxPopup.setWindowTitle(_translate("ESKLPSmnnComboBoxPopup", "Стандартизованное МНН", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResult), _translate("ESKLPSmnnComboBoxPopup", "Результат поиска", None))
        self.lblESKLPSmnnCode.setText(_translate("ESKLPSmnnComboBoxPopup", "Код узла СМНН", None))
        self.lblESKLPSmnn_mnn.setText(_translate("ESKLPSmnnComboBoxPopup", "Наименование МНН на русском языке (стандартизованное значение)", None))
        self.lblESKLPSmnn_form.setText(_translate("ESKLPSmnnComboBoxPopup", "Название лекарственной формы (стандартизованное значение)", None))
        self.lblESKLPSmnn_ftg.setText(_translate("ESKLPSmnnComboBoxPopup", "Название ФТГ", None))
        self.lblESKLPSmnn_is_znvlp.setText(_translate("ESKLPSmnnComboBoxPopup", "ЖНВЛП", None))
        self.lblESKLPSmnn_is_narcotic.setText(_translate("ESKLPSmnnComboBoxPopup", "Наличие в лекарственном препарате наркотических средств", None))
        self.lblESKLPSmnn_Dosage_grls_value.setText(_translate("ESKLPSmnnComboBoxPopup", "Дозировка", None))
        self.cmbESKLPSmnn_is_narcotic.setItemText(0, _translate("ESKLPSmnnComboBoxPopup", "не задано", None))
        self.cmbESKLPSmnn_is_narcotic.setItemText(1, _translate("ESKLPSmnnComboBoxPopup", "Нет", None))
        self.cmbESKLPSmnn_is_narcotic.setItemText(2, _translate("ESKLPSmnnComboBoxPopup", "Да", None))
        self.cmbESKLPSmnn_is_znvlp.setItemText(0, _translate("ESKLPSmnnComboBoxPopup", "не задано", None))
        self.cmbESKLPSmnn_is_znvlp.setItemText(1, _translate("ESKLPSmnnComboBoxPopup", "Нет", None))
        self.cmbESKLPSmnn_is_znvlp.setItemText(2, _translate("ESKLPSmnnComboBoxPopup", "Да", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("ESKLPSmnnComboBoxPopup", "&Поиск", None))

from library.TableView import CTableView