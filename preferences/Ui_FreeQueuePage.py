# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\FreeQueuePage.ui'
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

class Ui_freeQueuePage(object):
    def setupUi(self, freeQueuePage):
        freeQueuePage.setObjectName(_fromUtf8("freeQueuePage"))
        freeQueuePage.resize(651, 405)
        freeQueuePage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(freeQueuePage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.lblDoubleClickQueueFreeOrder = QtGui.QLabel(freeQueuePage)
        self.lblDoubleClickQueueFreeOrder.setObjectName(_fromUtf8("lblDoubleClickQueueFreeOrder"))
        self.gridLayout.addWidget(self.lblDoubleClickQueueFreeOrder, 0, 0, 1, 1)
        self.cmbDoubleClickQueueFreeOrder = QtGui.QComboBox(freeQueuePage)
        self.cmbDoubleClickQueueFreeOrder.setObjectName(_fromUtf8("cmbDoubleClickQueueFreeOrder"))
        self.cmbDoubleClickQueueFreeOrder.addItem(_fromUtf8(""))
        self.cmbDoubleClickQueueFreeOrder.setItemText(0, _fromUtf8(""))
        self.cmbDoubleClickQueueFreeOrder.addItem(_fromUtf8(""))
        self.cmbDoubleClickQueueFreeOrder.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDoubleClickQueueFreeOrder, 0, 1, 1, 2)
        self.lblDoubleClickQueueFreeOrder.setBuddy(self.cmbDoubleClickQueueFreeOrder)

        self.retranslateUi(freeQueuePage)
        QtCore.QMetaObject.connectSlotsByName(freeQueuePage)

    def retranslateUi(self, freeQueuePage):
        freeQueuePage.setWindowTitle(_translate("freeQueuePage", "Панель «Номерки»", None))
        self.lblDoubleClickQueueFreeOrder.setText(_translate("freeQueuePage", "Двойной щелчок в списке свободных номерков", None))
        self.cmbDoubleClickQueueFreeOrder.setItemText(1, _translate("freeQueuePage", "Поставить в очередь", None))
        self.cmbDoubleClickQueueFreeOrder.setItemText(2, _translate("freeQueuePage", "Выполнить бронирование", None))

