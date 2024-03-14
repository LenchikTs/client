# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\MES\MESComboBoxPopupEx.ui'
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

class Ui_MESComboBoxPopupEx(object):
    def setupUi(self, MESComboBoxPopupEx):
        MESComboBoxPopupEx.setObjectName(_fromUtf8("MESComboBoxPopupEx"))
        MESComboBoxPopupEx.resize(306, 246)
        self.gridlayout = QtGui.QGridLayout(MESComboBoxPopupEx)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(MESComboBoxPopupEx)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMES = QtGui.QWidget()
        self.tabMES.setObjectName(_fromUtf8("tabMES"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabMES)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tblMES = CTableView(self.tabMES)
        self.tblMES.setObjectName(_fromUtf8("tblMES"))
        self.vboxlayout.addWidget(self.tblMES)
        self.tabWidget.addTab(self.tabMES, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(MESComboBoxPopupEx)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MESComboBoxPopupEx)
        MESComboBoxPopupEx.setTabOrder(self.tabWidget, self.tblMES)

    def retranslateUi(self, MESComboBoxPopupEx):
        MESComboBoxPopupEx.setWindowTitle(_translate("MESComboBoxPopupEx", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMES), _translate("MESComboBoxPopupEx", "&Номенклатура", None))

from library.TableView import CTableView
