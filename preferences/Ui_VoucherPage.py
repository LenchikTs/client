# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\VoucherPage.ui'
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

class Ui_VoucherPage(object):
    def setupUi(self, VoucherPage):
        VoucherPage.setObjectName(_fromUtf8("VoucherPage"))
        VoucherPage.resize(651, 405)
        VoucherPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(VoucherPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(168, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 2)
        self.edtVoucherDuration = QtGui.QSpinBox(VoucherPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtVoucherDuration.sizePolicy().hasHeightForWidth())
        self.edtVoucherDuration.setSizePolicy(sizePolicy)
        self.edtVoucherDuration.setObjectName(_fromUtf8("edtVoucherDuration"))
        self.gridLayout.addWidget(self.edtVoucherDuration, 0, 1, 1, 1)
        self.lblVoucherDuration = QtGui.QLabel(VoucherPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblVoucherDuration.sizePolicy().hasHeightForWidth())
        self.lblVoucherDuration.setSizePolicy(sizePolicy)
        self.lblVoucherDuration.setObjectName(_fromUtf8("lblVoucherDuration"))
        self.gridLayout.addWidget(self.lblVoucherDuration, 0, 0, 1, 1)
        self.lblVoucherDuration.setBuddy(self.edtVoucherDuration)

        self.retranslateUi(VoucherPage)
        QtCore.QMetaObject.connectSlotsByName(VoucherPage)

    def retranslateUi(self, VoucherPage):
        VoucherPage.setWindowTitle(_translate("VoucherPage", "Путевка", None))
        self.lblVoucherDuration.setText(_translate("VoucherPage", "Длительность путевки по умолчанию", None))

