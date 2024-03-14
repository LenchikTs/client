# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Project\Samson\UP_s11\client\Registry\VisitComboBoxPopup.ui'
#
# Created: Tue May 17 14:42:55 2022
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

class Ui_VisitComboBoxPopup(object):
    def setupUi(self, VisitComboBoxPopup):
        VisitComboBoxPopup.setObjectName(_fromUtf8("VisitComboBoxPopup"))
        VisitComboBoxPopup.resize(687, 453)
        self.gridLayout = QtGui.QGridLayout(VisitComboBoxPopup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblVisit = CTableView(VisitComboBoxPopup)
        self.tblVisit.setObjectName(_fromUtf8("tblVisit"))
        self.gridLayout.addWidget(self.tblVisit, 0, 0, 1, 2)

        self.retranslateUi(VisitComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(VisitComboBoxPopup)

    def retranslateUi(self, VisitComboBoxPopup):
        VisitComboBoxPopup.setWindowTitle(_translate("VisitComboBoxPopup", "Form", None))

from library.TableView import CTableView
