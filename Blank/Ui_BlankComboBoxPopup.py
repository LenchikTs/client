# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Blank\BlankComboBoxPopup.ui'
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

class Ui_BlankComboBoxPopup(object):
    def setupUi(self, BlankComboBoxPopup):
        BlankComboBoxPopup.setObjectName(_fromUtf8("BlankComboBoxPopup"))
        BlankComboBoxPopup.resize(282, 207)
        self.gridLayout = QtGui.QGridLayout(BlankComboBoxPopup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblBlank = CTableView(BlankComboBoxPopup)
        self.tblBlank.setObjectName(_fromUtf8("tblBlank"))
        self.gridLayout.addWidget(self.tblBlank, 0, 0, 1, 1)

        self.retranslateUi(BlankComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(BlankComboBoxPopup)

    def retranslateUi(self, BlankComboBoxPopup):
        BlankComboBoxPopup.setWindowTitle(_translate("BlankComboBoxPopup", "Form", None))

from library.TableView import CTableView
