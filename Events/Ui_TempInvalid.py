# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\TempInvalid.ui'
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

class Ui_grpTempInvalid(object):
    def setupUi(self, grpTempInvalid):
        grpTempInvalid.setObjectName(_fromUtf8("grpTempInvalid"))
        grpTempInvalid.resize(884, 516)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(grpTempInvalid.sizePolicy().hasHeightForWidth())
        grpTempInvalid.setSizePolicy(sizePolicy)
        grpTempInvalid.setChecked(False)
        self.gridLayout_3 = QtGui.QGridLayout(grpTempInvalid)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.grpTempInvalidPrivate = QtGui.QGroupBox(grpTempInvalid)
        self.grpTempInvalidPrivate.setAlignment(QtCore.Qt.AlignCenter)
        self.grpTempInvalidPrivate.setObjectName(_fromUtf8("grpTempInvalidPrivate"))
        self.gridLayout = QtGui.QGridLayout(self.grpTempInvalidPrivate)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.grpTempInvalidPrivate)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblTempInvalidPrivate = CInDocTableView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblTempInvalidPrivate.sizePolicy().hasHeightForWidth())
        self.tblTempInvalidPrivate.setSizePolicy(sizePolicy)
        self.tblTempInvalidPrivate.setObjectName(_fromUtf8("tblTempInvalidPrivate"))
        self.grpTempInvalidPatronage = QtGui.QGroupBox(self.splitter)
        self.grpTempInvalidPatronage.setAlignment(QtCore.Qt.AlignCenter)
        self.grpTempInvalidPatronage.setObjectName(_fromUtf8("grpTempInvalidPatronage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpTempInvalidPatronage)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblTempInvalidPatronage = CInDocTableView(self.grpTempInvalidPatronage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblTempInvalidPatronage.sizePolicy().hasHeightForWidth())
        self.tblTempInvalidPatronage.setSizePolicy(sizePolicy)
        self.tblTempInvalidPatronage.setObjectName(_fromUtf8("tblTempInvalidPatronage"))
        self.gridLayout_2.addWidget(self.tblTempInvalidPatronage, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.grpTempInvalidPrivate, 0, 0, 1, 1)

        self.retranslateUi(grpTempInvalid)
        QtCore.QMetaObject.connectSlotsByName(grpTempInvalid)

    def retranslateUi(self, grpTempInvalid):
        self.grpTempInvalidPrivate.setTitle(_translate("grpTempInvalid", "Собственные", None))
        self.grpTempInvalidPatronage.setTitle(_translate("grpTempInvalid", "Патронаж", None))

from library.InDocTable import CInDocTableView
