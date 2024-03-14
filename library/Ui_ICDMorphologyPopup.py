# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\ICDMorphologyPopup.ui'
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

class Ui_ICDMorphologyPopup(object):
    def setupUi(self, ICDMorphologyPopup):
        ICDMorphologyPopup.setObjectName(_fromUtf8("ICDMorphologyPopup"))
        ICDMorphologyPopup.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ICDMorphologyPopup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(ICDMorphologyPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMorphology = QtGui.QWidget()
        self.tabMorphology.setObjectName(_fromUtf8("tabMorphology"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabMorphology)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblMorphology = CRBPopupView(self.tabMorphology)
        self.tblMorphology.setObjectName(_fromUtf8("tblMorphology"))
        self.gridLayout_2.addWidget(self.tblMorphology, 0, 0, 1, 1)
        self.lblCount = QtGui.QLabel(self.tabMorphology)
        self.lblCount.setObjectName(_fromUtf8("lblCount"))
        self.gridLayout_2.addWidget(self.lblCount, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabMorphology, _fromUtf8(""))
        self.tabFind = QtGui.QWidget()
        self.tabFind.setObjectName(_fromUtf8("tabFind"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabFind)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.edtSearch = QtGui.QLineEdit(self.tabFind)
        self.edtSearch.setObjectName(_fromUtf8("edtSearch"))
        self.gridLayout_3.addWidget(self.edtSearch, 1, 0, 1, 1)
        self.btnSearch = QtGui.QToolButton(self.tabFind)
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.gridLayout_3.addWidget(self.btnSearch, 1, 1, 1, 1)
        self.tblSearch = CTableView(self.tabFind)
        self.tblSearch.setObjectName(_fromUtf8("tblSearch"))
        self.gridLayout_3.addWidget(self.tblSearch, 2, 0, 1, 2)
        self.chkForCurrentMKB = QtGui.QCheckBox(self.tabFind)
        self.chkForCurrentMKB.setObjectName(_fromUtf8("chkForCurrentMKB"))
        self.gridLayout_3.addWidget(self.chkForCurrentMKB, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabFind, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(ICDMorphologyPopup)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ICDMorphologyPopup)
        ICDMorphologyPopup.setTabOrder(self.tabWidget, self.tblMorphology)
        ICDMorphologyPopup.setTabOrder(self.tblMorphology, self.chkForCurrentMKB)
        ICDMorphologyPopup.setTabOrder(self.chkForCurrentMKB, self.edtSearch)
        ICDMorphologyPopup.setTabOrder(self.edtSearch, self.btnSearch)
        ICDMorphologyPopup.setTabOrder(self.btnSearch, self.tblSearch)

    def retranslateUi(self, ICDMorphologyPopup):
        ICDMorphologyPopup.setWindowTitle(_translate("ICDMorphologyPopup", "Dialog", None))
        self.lblCount.setText(_translate("ICDMorphologyPopup", "Количеств записей: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMorphology), _translate("ICDMorphologyPopup", "&Номенклатура", None))
        self.btnSearch.setText(_translate("ICDMorphologyPopup", "...", None))
        self.chkForCurrentMKB.setText(_translate("ICDMorphologyPopup", "Определенные для текущего диагноза", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFind), _translate("ICDMorphologyPopup", "&Поиск", None))

from library.TableView import CTableView
from library.crbcombobox import CRBPopupView
