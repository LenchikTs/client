# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ClientRelationSimpleComboBoxPopup.ui'
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

class Ui_ClientRelationSimpleComboBoxPopup(object):
    def setupUi(self, ClientRelationSimpleComboBoxPopup):
        ClientRelationSimpleComboBoxPopup.setObjectName(_fromUtf8("ClientRelationSimpleComboBoxPopup"))
        ClientRelationSimpleComboBoxPopup.resize(455, 344)
        self.gridLayout = QtGui.QGridLayout(ClientRelationSimpleComboBoxPopup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblClientRelation = CTableView(ClientRelationSimpleComboBoxPopup)
        self.tblClientRelation.setObjectName(_fromUtf8("tblClientRelation"))
        self.gridLayout.addWidget(self.tblClientRelation, 0, 0, 1, 1)

        self.retranslateUi(ClientRelationSimpleComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(ClientRelationSimpleComboBoxPopup)

    def retranslateUi(self, ClientRelationSimpleComboBoxPopup):
        ClientRelationSimpleComboBoxPopup.setWindowTitle(_translate("ClientRelationSimpleComboBoxPopup", "Form", None))

from library.TableView import CTableView
