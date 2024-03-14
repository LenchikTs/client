# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventJobTicketsEditorDialog.ui'
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

class Ui_EventJobTicketsEditor(object):
    def setupUi(self, EventJobTicketsEditor):
        EventJobTicketsEditor.setObjectName(_fromUtf8("EventJobTicketsEditor"))
        EventJobTicketsEditor.resize(289, 160)
        self.gridLayout = QtGui.QGridLayout(EventJobTicketsEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = CApplyResetDialogButtonBox(EventJobTicketsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.btnCloseJobTickets = QtGui.QPushButton(EventJobTicketsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCloseJobTickets.sizePolicy().hasHeightForWidth())
        self.btnCloseJobTickets.setSizePolicy(sizePolicy)
        self.btnCloseJobTickets.setObjectName(_fromUtf8("btnCloseJobTickets"))
        self.gridLayout.addWidget(self.btnCloseJobTickets, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(EventJobTicketsEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabSetJobTicket = QtGui.QWidget()
        self.tabSetJobTicket.setObjectName(_fromUtf8("tabSetJobTicket"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabSetJobTicket)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblSetEventJobTickets = CEventJobTicketsView(self.tabSetJobTicket)
        self.tblSetEventJobTickets.setObjectName(_fromUtf8("tblSetEventJobTickets"))
        self.verticalLayout_2.addWidget(self.tblSetEventJobTickets)
        self.tabWidget.addTab(self.tabSetJobTicket, _fromUtf8(""))
        self.tabChangeJobTicket = QtGui.QWidget()
        self.tabChangeJobTicket.setObjectName(_fromUtf8("tabChangeJobTicket"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabChangeJobTicket)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tblChangeEventJobTickets = CEventJobTicketsView(self.tabChangeJobTicket)
        self.tblChangeEventJobTickets.setObjectName(_fromUtf8("tblChangeEventJobTickets"))
        self.verticalLayout_3.addWidget(self.tblChangeEventJobTickets)
        self.tabWidget.addTab(self.tabChangeJobTicket, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 2)

        self.retranslateUi(EventJobTicketsEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventJobTicketsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventJobTicketsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(EventJobTicketsEditor)

    def retranslateUi(self, EventJobTicketsEditor):
        EventJobTicketsEditor.setWindowTitle(_translate("EventJobTicketsEditor", "Dialog", None))
        self.btnCloseJobTickets.setText(_translate("EventJobTicketsEditor", "Закрыть работы", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSetJobTicket), _translate("EventJobTicketsEditor", "Назначить", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabChangeJobTicket), _translate("EventJobTicketsEditor", "Изменить", None))

from Events.EventJobTicketsEditorTable import CEventJobTicketsView
from library.DialogButtonBox import CApplyResetDialogButtonBox
