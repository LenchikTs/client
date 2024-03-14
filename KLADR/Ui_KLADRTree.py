# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\KLADR\KLADRTree.ui'
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

class Ui_KLADRTreePopup(object):
    def setupUi(self, KLADRTreePopup):
        KLADRTreePopup.setObjectName(_fromUtf8("KLADRTreePopup"))
        KLADRTreePopup.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(KLADRTreePopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(KLADRTreePopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTree = QtGui.QWidget()
        self.tabTree.setObjectName(_fromUtf8("tabTree"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabTree)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.treeView = CKLADRTreeView(self.tabTree)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.vboxlayout.addWidget(self.treeView)
        self.tabWidget.addTab(self.tabTree, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridlayout1 = QtGui.QGridLayout(self.tabSearch)
        self.gridlayout1.setMargin(4)
        self.gridlayout1.setSpacing(4)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.edtWords = QtGui.QLineEdit(self.tabSearch)
        self.edtWords.setObjectName(_fromUtf8("edtWords"))
        self.gridlayout1.addWidget(self.edtWords, 0, 0, 1, 1)
        self.btnSearch = QtGui.QToolButton(self.tabSearch)
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.gridlayout1.addWidget(self.btnSearch, 0, 1, 1, 1)
        self.tblSearchResult = CKLADRSearchResult(self.tabSearch)
        self.tblSearchResult.setObjectName(_fromUtf8("tblSearchResult"))
        self.gridlayout1.addWidget(self.tblSearchResult, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(KLADRTreePopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(KLADRTreePopup)

    def retranslateUi(self, KLADRTreePopup):
        KLADRTreePopup.setWindowTitle(_translate("KLADRTreePopup", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTree), _translate("KLADRTreePopup", "&КЛАДР", None))
        self.btnSearch.setText(_translate("KLADRTreePopup", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("KLADRTreePopup", "&Поиск", None))

from KLADRViews import CKLADRSearchResult, CKLADRTreeView
