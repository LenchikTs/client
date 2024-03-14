# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\JobTicketProbesDialog.ui'
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

class Ui_JobTicketProbesDialog(object):
    def setupUi(self, JobTicketProbesDialog):
        JobTicketProbesDialog.setObjectName(_fromUtf8("JobTicketProbesDialog"))
        JobTicketProbesDialog.resize(362, 189)
        self.verticalLayout = QtGui.QVBoxLayout(JobTicketProbesDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblTreeProbe = CJobTicketProbeTreeView(JobTicketProbesDialog)
        self.tblTreeProbe.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tblTreeProbe.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblTreeProbe.setObjectName(_fromUtf8("tblTreeProbe"))
        self.verticalLayout.addWidget(self.tblTreeProbe)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(JobTicketProbesDialog)
        self.btnClose.setAutoDefault(False)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(JobTicketProbesDialog)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), JobTicketProbesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(JobTicketProbesDialog)

    def retranslateUi(self, JobTicketProbesDialog):
        JobTicketProbesDialog.setWindowTitle(_translate("JobTicketProbesDialog", "Dialog", None))
        self.btnClose.setText(_translate("JobTicketProbesDialog", "Закрыть", None))

from Resources.JobTicketProbeModel import CJobTicketProbeTreeView
