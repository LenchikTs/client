# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\preferences\ClientPlatePage.ui'
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

class Ui_clientPlatePage(object):
    def setupUi(self, clientPlatePage):
        clientPlatePage.setObjectName(_fromUtf8("clientPlatePage"))
        clientPlatePage.resize(651, 592)
        self.gridLayout = QtGui.QGridLayout(clientPlatePage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.cmbShowingInInfoBlockSocStatus = QtGui.QComboBox(clientPlatePage)
        self.cmbShowingInInfoBlockSocStatus.setObjectName(_fromUtf8("cmbShowingInInfoBlockSocStatus"))
        self.cmbShowingInInfoBlockSocStatus.addItem(_fromUtf8(""))
        self.cmbShowingInInfoBlockSocStatus.addItem(_fromUtf8(""))
        self.cmbShowingInInfoBlockSocStatus.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbShowingInInfoBlockSocStatus, 0, 1, 1, 2)
        self.lblShowingInInfoBlockSocStatus = QtGui.QLabel(clientPlatePage)
        self.lblShowingInInfoBlockSocStatus.setObjectName(_fromUtf8("lblShowingInInfoBlockSocStatus"))
        self.gridLayout.addWidget(self.lblShowingInInfoBlockSocStatus, 0, 0, 1, 1)
        self.lblTFAccountingSystemId = QtGui.QLabel(clientPlatePage)
        self.lblTFAccountingSystemId.setObjectName(_fromUtf8("lblTFAccountingSystemId"))
        self.gridLayout.addWidget(self.lblTFAccountingSystemId, 1, 0, 1, 1)
        self.cmbTFAccountingSystemId = CRBComboBox(clientPlatePage)
        self.cmbTFAccountingSystemId.setObjectName(_fromUtf8("cmbTFAccountingSystemId"))
        self.gridLayout.addWidget(self.cmbTFAccountingSystemId, 1, 1, 1, 2)
        self.lblShowingAttach = QtGui.QLabel(clientPlatePage)
        self.lblShowingAttach.setObjectName(_fromUtf8("lblShowingAttach"))
        self.gridLayout.addWidget(self.lblShowingAttach, 2, 0, 1, 1)
        self.cmbShowingAttach = QtGui.QComboBox(clientPlatePage)
        self.cmbShowingAttach.setObjectName(_fromUtf8("cmbShowingAttach"))
        self.cmbShowingAttach.addItem(_fromUtf8(""))
        self.cmbShowingAttach.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbShowingAttach, 2, 1, 1, 2)
        self.lblShowingInInfoBlockSocStatus.setBuddy(self.cmbShowingInInfoBlockSocStatus)
        self.lblTFAccountingSystemId.setBuddy(self.cmbTFAccountingSystemId)

        self.retranslateUi(clientPlatePage)
        self.cmbShowingAttach.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(clientPlatePage)

    def retranslateUi(self, clientPlatePage):
        clientPlatePage.setWindowTitle(_translate("clientPlatePage", "Сведения о пациенте", None))
        self.cmbShowingInInfoBlockSocStatus.setItemText(0, _translate("clientPlatePage", "Код", None))
        self.cmbShowingInInfoBlockSocStatus.setItemText(1, _translate("clientPlatePage", "Наименование", None))
        self.cmbShowingInInfoBlockSocStatus.setItemText(2, _translate("clientPlatePage", "Наименование и код", None))
        self.lblShowingInInfoBlockSocStatus.setText(_translate("clientPlatePage", "Отображать &Социальный статус пациента как", None))
        self.lblTFAccountingSystemId.setText(_translate("clientPlatePage", "Отображать идентификатор &ТФОМС по справочнику", None))
        self.lblShowingAttach.setText(_translate("clientPlatePage", "Отображать закрытое прикрепление", None))
        self.cmbShowingAttach.setItemText(0, _translate("clientPlatePage", "Нет", None))
        self.cmbShowingAttach.setItemText(1, _translate("clientPlatePage", "Да", None))

from library.crbcombobox import CRBComboBox
