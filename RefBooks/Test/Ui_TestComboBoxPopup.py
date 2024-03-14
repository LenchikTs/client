# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\Test\TestComboBoxPopup.ui'
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

class Ui_TestComboBoxPopupForm(object):
    def setupUi(self, TestComboBoxPopupForm):
        TestComboBoxPopupForm.setObjectName(_fromUtf8("TestComboBoxPopupForm"))
        TestComboBoxPopupForm.resize(491, 331)
        self.gridLayout = QtGui.QGridLayout(TestComboBoxPopupForm)
        self.gridLayout.setContentsMargins(1, 2, 1, 1)
        self.gridLayout.setHorizontalSpacing(1)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbTestGroup = CRBComboBox(TestComboBoxPopupForm)
        self.cmbTestGroup.setObjectName(_fromUtf8("cmbTestGroup"))
        self.gridLayout.addWidget(self.cmbTestGroup, 0, 1, 1, 1)
        self.tblTests = CRBPopupView(TestComboBoxPopupForm)
        self.tblTests.setObjectName(_fromUtf8("tblTests"))
        self.gridLayout.addWidget(self.tblTests, 1, 0, 1, 2)
        self.lblTestGroup = QtGui.QLabel(TestComboBoxPopupForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTestGroup.sizePolicy().hasHeightForWidth())
        self.lblTestGroup.setSizePolicy(sizePolicy)
        self.lblTestGroup.setObjectName(_fromUtf8("lblTestGroup"))
        self.gridLayout.addWidget(self.lblTestGroup, 0, 0, 1, 1)

        self.retranslateUi(TestComboBoxPopupForm)
        QtCore.QMetaObject.connectSlotsByName(TestComboBoxPopupForm)

    def retranslateUi(self, TestComboBoxPopupForm):
        TestComboBoxPopupForm.setWindowTitle(_translate("TestComboBoxPopupForm", "Form", None))
        self.lblTestGroup.setText(_translate("TestComboBoxPopupForm", "Группа", None))

from library.crbcombobox import CRBComboBox, CRBPopupView
