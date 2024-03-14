# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\CheckPlanningOpenEventsDialog.ui'
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

class Ui_CheckPlanningOpenEventsDialog(object):
    def setupUi(self, CheckPlanningOpenEventsDialog):
        CheckPlanningOpenEventsDialog.setObjectName(_fromUtf8("CheckPlanningOpenEventsDialog"))
        CheckPlanningOpenEventsDialog.resize(580, 478)
        self.gridLayout = QtGui.QGridLayout(CheckPlanningOpenEventsDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(CheckPlanningOpenEventsDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.txtClientInfoEventsBrowser = CTextBrowser(self.splitter)
        self.txtClientInfoEventsBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtClientInfoEventsBrowser.setObjectName(_fromUtf8("txtClientInfoEventsBrowser"))
        self.tblOpenActions = CTableView(self.splitter)
        self.tblOpenActions.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblOpenActions.setObjectName(_fromUtf8("tblOpenActions"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 3)
        self.btnCreate = QtGui.QPushButton(CheckPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCreate.sizePolicy().hasHeightForWidth())
        self.btnCreate.setSizePolicy(sizePolicy)
        self.btnCreate.setMinimumSize(QtCore.QSize(100, 0))
        self.btnCreate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnCreate.setObjectName(_fromUtf8("btnCreate"))
        self.gridLayout.addWidget(self.btnCreate, 1, 0, 1, 1)
        self.btnOpen = QtGui.QPushButton(CheckPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOpen.sizePolicy().hasHeightForWidth())
        self.btnOpen.setSizePolicy(sizePolicy)
        self.btnOpen.setMinimumSize(QtCore.QSize(100, 0))
        self.btnOpen.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnOpen.setObjectName(_fromUtf8("btnOpen"))
        self.gridLayout.addWidget(self.btnOpen, 1, 1, 1, 1)
        self.btnClose = QtGui.QPushButton(CheckPlanningOpenEventsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 2, 1, 1)

        self.retranslateUi(CheckPlanningOpenEventsDialog)
        QtCore.QMetaObject.connectSlotsByName(CheckPlanningOpenEventsDialog)
        CheckPlanningOpenEventsDialog.setTabOrder(self.btnClose, self.btnOpen)
        CheckPlanningOpenEventsDialog.setTabOrder(self.btnOpen, self.btnCreate)
        CheckPlanningOpenEventsDialog.setTabOrder(self.btnCreate, self.tblOpenActions)

    def retranslateUi(self, CheckPlanningOpenEventsDialog):
        CheckPlanningOpenEventsDialog.setWindowTitle(_translate("CheckPlanningOpenEventsDialog", "Открытые события", None))
        self.btnCreate.setText(_translate("CheckPlanningOpenEventsDialog", "Создать", None))
        self.btnOpen.setText(_translate("CheckPlanningOpenEventsDialog", "Открыть", None))
        self.btnClose.setText(_translate("CheckPlanningOpenEventsDialog", "Отмена", None))

from library.TableView import CTableView
from library.TextBrowser import CTextBrowser
