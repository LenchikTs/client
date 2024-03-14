# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\JobTicketsDialog.ui'
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

class Ui_JobTicketsDialog(object):
    def setupUi(self, JobTicketsDialog):
        JobTicketsDialog.setObjectName(_fromUtf8("JobTicketsDialog"))
        JobTicketsDialog.resize(608, 470)
        self.verticalLayout_3 = QtGui.QVBoxLayout(JobTicketsDialog)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(JobTicketsDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grplJobTickets = QtGui.QGroupBox(self.splitter)
        self.grplJobTickets.setObjectName(_fromUtf8("grplJobTickets"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grplJobTickets)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblJobTickets = CTableView(self.grplJobTickets)
        self.tblJobTickets.setObjectName(_fromUtf8("tblJobTickets"))
        self.verticalLayout.addWidget(self.tblJobTickets)
        self.grpGaps = QtGui.QGroupBox(self.splitter)
        self.grpGaps.setObjectName(_fromUtf8("grpGaps"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grpGaps)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblGaps = CTableView(self.grpGaps)
        self.tblGaps.setObjectName(_fromUtf8("tblGaps"))
        self.verticalLayout_2.addWidget(self.tblGaps)
        self.verticalLayout_3.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(JobTicketsDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(JobTicketsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), JobTicketsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), JobTicketsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(JobTicketsDialog)
        JobTicketsDialog.setTabOrder(self.tblJobTickets, self.tblGaps)
        JobTicketsDialog.setTabOrder(self.tblGaps, self.buttonBox)

    def retranslateUi(self, JobTicketsDialog):
        JobTicketsDialog.setWindowTitle(_translate("JobTicketsDialog", "Номерки", None))
        self.grplJobTickets.setTitle(_translate("JobTicketsDialog", "Номерки", None))
        self.grpGaps.setTitle(_translate("JobTicketsDialog", "Перерывы подразделения", None))

from library.TableView import CTableView
