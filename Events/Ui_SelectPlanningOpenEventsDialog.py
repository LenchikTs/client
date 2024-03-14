# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Events\SelectPlanningOpenEventsDialog.ui'
#
# Created: Thu Oct 25 15:47:48 2018
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

class Ui_SelectPlanningOpenEventsDialog(object):
    def setupUi(self, SelectPlanningOpenEventsDialog):
        SelectPlanningOpenEventsDialog.setObjectName(_fromUtf8("SelectPlanningOpenEventsDialog"))
        SelectPlanningOpenEventsDialog.resize(580, 478)
        self.gridLayout = QtGui.QGridLayout(SelectPlanningOpenEventsDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(SelectPlanningOpenEventsDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.txtClientInfoEventsBrowser = CTextBrowser(self.splitter)
        self.txtClientInfoEventsBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtClientInfoEventsBrowser.setObjectName(_fromUtf8("txtClientInfoEventsBrowser"))
        self.tblOpenActions = CTableView(self.splitter)
        self.tblOpenActions.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblOpenActions.setObjectName(_fromUtf8("tblOpenActions"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 4)
        self.btnSelect = QtGui.QPushButton(SelectPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelect.sizePolicy().hasHeightForWidth())
        self.btnSelect.setSizePolicy(sizePolicy)
        self.btnSelect.setMinimumSize(QtCore.QSize(100, 0))
        self.btnSelect.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.gridLayout.addWidget(self.btnSelect, 1, 1, 1, 1)
        self.btnClose = QtGui.QPushButton(SelectPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 3, 1, 1)
        self.btnOpen = QtGui.QPushButton(SelectPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOpen.sizePolicy().hasHeightForWidth())
        self.btnOpen.setSizePolicy(sizePolicy)
        self.btnOpen.setMinimumSize(QtCore.QSize(100, 0))
        self.btnOpen.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnOpen.setObjectName(_fromUtf8("btnOpen"))
        self.gridLayout.addWidget(self.btnOpen, 1, 2, 1, 1)

        self.retranslateUi(SelectPlanningOpenEventsDialog)
        QtCore.QMetaObject.connectSlotsByName(SelectPlanningOpenEventsDialog)
        SelectPlanningOpenEventsDialog.setTabOrder(self.btnClose, self.btnSelect)
        SelectPlanningOpenEventsDialog.setTabOrder(self.btnSelect, self.tblOpenActions)

    def retranslateUi(self, SelectPlanningOpenEventsDialog):
        SelectPlanningOpenEventsDialog.setWindowTitle(_translate("SelectPlanningOpenEventsDialog", "Открытые события", None))
        self.btnSelect.setText(_translate("SelectPlanningOpenEventsDialog", "Выбрать", None))
        self.btnClose.setText(_translate("SelectPlanningOpenEventsDialog", "Отмена", None))
        self.btnOpen.setText(_translate("SelectPlanningOpenEventsDialog", "Открыть", None))

from library.TextBrowser import CTextBrowser
from library.TableView import CTableView
