# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\RelatedEventListPage.ui'
#
# Created: Wed Apr 17 11:30:42 2019
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

class Ui_RelatedEventListPage(object):
    def setupUi(self, RelatedEventListPage):
        RelatedEventListPage.setObjectName(_fromUtf8("RelatedEventListPage"))
        RelatedEventListPage.resize(522, 384)
        self.verticalLayout = QtGui.QVBoxLayout(RelatedEventListPage)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblRelatedEventList = CTableView(RelatedEventListPage)
        self.tblRelatedEventList.setObjectName(_fromUtf8("tblRelatedEventList"))
        self.verticalLayout.addWidget(self.tblRelatedEventList)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnPrint = QtGui.QPushButton(RelatedEventListPage)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.horizontalLayout.addWidget(self.btnPrint)
        self.btnClose = QtGui.QPushButton(RelatedEventListPage)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RelatedEventListPage)
        QtCore.QMetaObject.connectSlotsByName(RelatedEventListPage)

    def retranslateUi(self, RelatedEventListPage):
        RelatedEventListPage.setWindowTitle(_translate("RelatedEventListPage", "Form", None))
        self.btnPrint.setText(_translate("RelatedEventListPage", "Печать", None))
        self.btnClose.setText(_translate("RelatedEventListPage", "Закрыть", None))

from library.TableView import CTableView
