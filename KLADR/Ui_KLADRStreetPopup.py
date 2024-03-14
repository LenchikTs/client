# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\KLADR\KLADRStreetPopup.ui'
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

class Ui_KLADRStreetPopup(object):
    def setupUi(self, KLADRStreetPopup):
        KLADRStreetPopup.setObjectName(_fromUtf8("KLADRStreetPopup"))
        KLADRStreetPopup.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(KLADRStreetPopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(KLADRStreetPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabList = QtGui.QWidget()
        self.tabList.setObjectName(_fromUtf8("tabList"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabList)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.listView = CStreetListView(self.tabList)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.vboxlayout.addWidget(self.listView)
        self.tabWidget.addTab(self.tabList, _fromUtf8(""))
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
        self.tblSearchResult = CStreetSearchResult(self.tabSearch)
        self.tblSearchResult.setObjectName(_fromUtf8("tblSearchResult"))
        self.gridlayout1.addWidget(self.tblSearchResult, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(KLADRStreetPopup)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(KLADRStreetPopup)

    def retranslateUi(self, KLADRStreetPopup):
        KLADRStreetPopup.setWindowTitle(_translate("KLADRStreetPopup", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabList), _translate("KLADRStreetPopup", "&Улицы", None))
        self.btnSearch.setText(_translate("KLADRStreetPopup", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("KLADRStreetPopup", "&Поиск", None))

from KLADRViews import CStreetListView, CStreetSearchResult
