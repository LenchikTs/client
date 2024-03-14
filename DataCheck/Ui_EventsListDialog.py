# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\DataCheck\EventsListDialog.ui'
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

class Ui_eventsListDialog(object):
    def setupUi(self, eventsListDialog):
        eventsListDialog.setObjectName(_fromUtf8("eventsListDialog"))
        eventsListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(eventsListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblSelectInfo = QtGui.QLabel(eventsListDialog)
        self.lblSelectInfo.setText(_fromUtf8(""))
        self.lblSelectInfo.setObjectName(_fromUtf8("lblSelectInfo"))
        self.gridLayout.addWidget(self.lblSelectInfo, 1, 0, 1, 4)
        self.lblClientInfo = QtGui.QLabel(eventsListDialog)
        self.lblClientInfo.setText(_fromUtf8(""))
        self.lblClientInfo.setObjectName(_fromUtf8("lblClientInfo"))
        self.gridLayout.addWidget(self.lblClientInfo, 0, 0, 1, 4)
        self.tblListWidget = CTableView(eventsListDialog)
        self.tblListWidget.setObjectName(_fromUtf8("tblListWidget"))
        self.gridLayout.addWidget(self.tblListWidget, 2, 0, 1, 4)
        self.btnClose = QtGui.QPushButton(eventsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 3, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(294, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.btnCloseCorrect = QtGui.QPushButton(eventsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCloseCorrect.sizePolicy().hasHeightForWidth())
        self.btnCloseCorrect.setSizePolicy(sizePolicy)
        self.btnCloseCorrect.setMinimumSize(QtCore.QSize(100, 0))
        self.btnCloseCorrect.setObjectName(_fromUtf8("btnCloseCorrect"))
        self.gridLayout.addWidget(self.btnCloseCorrect, 3, 3, 1, 1)
        self.btnPrint = QtGui.QPushButton(eventsListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPrint.sizePolicy().hasHeightForWidth())
        self.btnPrint.setSizePolicy(sizePolicy)
        self.btnPrint.setMinimumSize(QtCore.QSize(100, 0))
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 3, 1, 1, 1)

        self.retranslateUi(eventsListDialog)
        QtCore.QMetaObject.connectSlotsByName(eventsListDialog)

    def retranslateUi(self, eventsListDialog):
        eventsListDialog.setWindowTitle(_translate("eventsListDialog", "Dialog", None))
        self.btnClose.setText(_translate("eventsListDialog", "Закрыть", None))
        self.btnCloseCorrect.setText(_translate("eventsListDialog", "Прервать", None))
        self.btnPrint.setText(_translate("eventsListDialog", "Печать", None))

from library.TableView import CTableView
