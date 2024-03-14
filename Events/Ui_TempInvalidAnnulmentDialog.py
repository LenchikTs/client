# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_vipisnoy\Events\TempInvalidAnnulmentDialog.ui'
#
# Created: Thu Sep 24 15:27:25 2020
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

class Ui_TempInvalidAnnulmentDialog(object):
    def setupUi(self, TempInvalidAnnulmentDialog):
        TempInvalidAnnulmentDialog.setObjectName(_fromUtf8("TempInvalidAnnulmentDialog"))
        TempInvalidAnnulmentDialog.resize(400, 62)
        self.gridLayout = QtGui.QGridLayout(TempInvalidAnnulmentDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAnnulmentReason = QtGui.QLabel(TempInvalidAnnulmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAnnulmentReason.sizePolicy().hasHeightForWidth())
        self.lblAnnulmentReason.setSizePolicy(sizePolicy)
        self.lblAnnulmentReason.setObjectName(_fromUtf8("lblAnnulmentReason"))
        self.gridLayout.addWidget(self.lblAnnulmentReason, 0, 0, 1, 1)
        self.cmbAnnulmentReason = CRBComboBox(TempInvalidAnnulmentDialog)
        self.cmbAnnulmentReason.setObjectName(_fromUtf8("cmbAnnulmentReason"))
        self.gridLayout.addWidget(self.cmbAnnulmentReason, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidAnnulmentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.lblAnnulmentReason.setBuddy(self.cmbAnnulmentReason)

        self.retranslateUi(TempInvalidAnnulmentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidAnnulmentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidAnnulmentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidAnnulmentDialog)

    def retranslateUi(self, TempInvalidAnnulmentDialog):
        TempInvalidAnnulmentDialog.setWindowTitle(_translate("TempInvalidAnnulmentDialog", "Укажите причину аннулирования", None))
        self.lblAnnulmentReason.setText(_translate("TempInvalidAnnulmentDialog", "&Причина", None))

from library.crbcombobox import CRBComboBox
