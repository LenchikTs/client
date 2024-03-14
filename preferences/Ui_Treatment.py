# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\Treatment.ui'
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

class Ui_Treatment(object):
    def setupUi(self, Treatment):
        Treatment.setObjectName(_fromUtf8("Treatment"))
        Treatment.resize(405, 35)
        Treatment.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(Treatment)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.lblShowOrgStructure = QtGui.QLabel(Treatment)
        self.lblShowOrgStructure.setObjectName(_fromUtf8("lblShowOrgStructure"))
        self.gridLayout.addWidget(self.lblShowOrgStructure, 0, 0, 1, 1)
        self.cmbShowOrgStructure = QtGui.QComboBox(Treatment)
        self.cmbShowOrgStructure.setObjectName(_fromUtf8("cmbShowOrgStructure"))
        self.cmbShowOrgStructure.addItem(_fromUtf8(""))
        self.cmbShowOrgStructure.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbShowOrgStructure, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)

        self.retranslateUi(Treatment)
        QtCore.QMetaObject.connectSlotsByName(Treatment)

    def retranslateUi(self, Treatment):
        Treatment.setWindowTitle(_translate("Treatment", "Циклы", None))
        self.lblShowOrgStructure.setText(_translate("Treatment", "Отображение подразделения", None))
        self.cmbShowOrgStructure.setItemText(0, _translate("Treatment", "по названию", None))
        self.cmbShowOrgStructure.setItemText(1, _translate("Treatment", "по коду", None))

