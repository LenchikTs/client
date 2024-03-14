# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/library/ICDTree.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ICDTreePopup(object):
    def setupUi(self, ICDTreePopup):
        ICDTreePopup.setObjectName(_fromUtf8("ICDTreePopup"))
        ICDTreePopup.resize(567, 300)
        self.gridlayout = QtGui.QGridLayout(ICDTreePopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(ICDTreePopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTree = QtGui.QWidget()
        self.tabTree.setObjectName(_fromUtf8("tabTree"))
        self.gridLayout = QtGui.QGridLayout(self.tabTree)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtFindWord = QtGui.QLineEdit(self.tabTree)
        self.edtFindWord.setObjectName(_fromUtf8("edtFindWord"))
        self.gridLayout.addWidget(self.edtFindWord, 0, 0, 1, 1)
        self.chkUseFindFilter = QtGui.QCheckBox(self.tabTree)
        self.chkUseFindFilter.setObjectName(_fromUtf8("chkUseFindFilter"))
        self.gridLayout.addWidget(self.chkUseFindFilter, 0, 1, 1, 1)
        self.treeView = CICDTreeView(self.tabTree)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 2)
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
        self.btnSearch.setAutoRaise(False)
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.gridlayout1.addWidget(self.btnSearch, 0, 2, 1, 1)
        self.tblSearchResult = CICDSearchResult(self.tabSearch)
        self.tblSearchResult.setObjectName(_fromUtf8("tblSearchResult"))
        self.gridlayout1.addWidget(self.tblSearchResult, 1, 0, 1, 3)
        self.chkLUD = QtGui.QCheckBox(self.tabSearch)
        self.chkLUD.setObjectName(_fromUtf8("chkLUD"))
        self.gridlayout1.addWidget(self.chkLUD, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(ICDTreePopup)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ICDTreePopup)
        ICDTreePopup.setTabOrder(self.tabWidget, self.edtFindWord)
        ICDTreePopup.setTabOrder(self.edtFindWord, self.chkUseFindFilter)
        ICDTreePopup.setTabOrder(self.chkUseFindFilter, self.treeView)
        ICDTreePopup.setTabOrder(self.treeView, self.edtWords)
        ICDTreePopup.setTabOrder(self.edtWords, self.chkLUD)
        ICDTreePopup.setTabOrder(self.chkLUD, self.btnSearch)
        ICDTreePopup.setTabOrder(self.btnSearch, self.tblSearchResult)

    def retranslateUi(self, ICDTreePopup):
        ICDTreePopup.setWindowTitle(_translate("ICDTreePopup", "Form", None))
        self.chkUseFindFilter.setText(_translate("ICDTreePopup", "Фильтр", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTree), _translate("ICDTreePopup", "&Номенклатура", None))
        self.btnSearch.setText(_translate("ICDTreePopup", "...", None))
        self.btnSearch.setShortcut(_translate("ICDTreePopup", "Return", None))
        self.chkLUD.setText(_translate("ICDTreePopup", "ЛУД", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("ICDTreePopup", "&Поиск", None))

from library.ICDTreeViews import CICDSearchResult, CICDTreeView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ICDTreePopup = QtGui.QWidget()
    ui = Ui_ICDTreePopup()
    ui.setupUi(ICDTreePopup)
    ICDTreePopup.show()
    sys.exit(app.exec_())

