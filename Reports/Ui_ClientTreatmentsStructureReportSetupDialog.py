# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ClientTreatmentsStructureReportSetupDialog.ui'
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

class Ui_ClientTreatmentsStructureReportSetupDialog(object):
    def setupUi(self, ClientTreatmentsStructureReportSetupDialog):
        ClientTreatmentsStructureReportSetupDialog.setObjectName(_fromUtf8("ClientTreatmentsStructureReportSetupDialog"))
        ClientTreatmentsStructureReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ClientTreatmentsStructureReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ClientTreatmentsStructureReportSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblAgeFrom = QtGui.QLabel(ClientTreatmentsStructureReportSetupDialog)
        self.lblAgeFrom.setEnabled(False)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.horizontalLayout.addWidget(self.lblAgeFrom)
        self.edtAgeFrom = QtGui.QSpinBox(ClientTreatmentsStructureReportSetupDialog)
        self.edtAgeFrom.setEnabled(False)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.horizontalLayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(ClientTreatmentsStructureReportSetupDialog)
        self.lblAgeTo.setEnabled(False)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.horizontalLayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(ClientTreatmentsStructureReportSetupDialog)
        self.edtAgeTo.setEnabled(False)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.horizontalLayout.addWidget(self.edtAgeTo)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.edtBegDate = CDateEdit(ClientTreatmentsStructureReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.edtEndDate = CDateEdit(ClientTreatmentsStructureReportSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ClientTreatmentsStructureReportSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(ClientTreatmentsStructureReportSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.chkAge = QtGui.QCheckBox(ClientTreatmentsStructureReportSetupDialog)
        self.chkAge.setObjectName(_fromUtf8("chkAge"))
        self.gridLayout.addWidget(self.chkAge, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.tblEventType = CTableView(ClientTreatmentsStructureReportSetupDialog)
        self.tblEventType.setObjectName(_fromUtf8("tblEventType"))
        self.gridLayout.addWidget(self.tblEventType, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ClientTreatmentsStructureReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ClientTreatmentsStructureReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientTreatmentsStructureReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientTreatmentsStructureReportSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientTreatmentsStructureReportSetupDialog)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.edtEndDate, self.chkAge)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.chkAge, self.edtAgeFrom)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.edtAgeTo, self.tblEventType)
        ClientTreatmentsStructureReportSetupDialog.setTabOrder(self.tblEventType, self.buttonBox)

    def retranslateUi(self, ClientTreatmentsStructureReportSetupDialog):
        ClientTreatmentsStructureReportSetupDialog.setWindowTitle(_translate("ClientTreatmentsStructureReportSetupDialog", "параметры отчёта", None))
        self.lblAgeFrom.setText(_translate("ClientTreatmentsStructureReportSetupDialog", "с", None))
        self.lblAgeTo.setText(_translate("ClientTreatmentsStructureReportSetupDialog", "по", None))
        self.edtBegDate.setDisplayFormat(_translate("ClientTreatmentsStructureReportSetupDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("ClientTreatmentsStructureReportSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ClientTreatmentsStructureReportSetupDialog", "Дата &окончания периода", None))
        self.lblBegDate.setText(_translate("ClientTreatmentsStructureReportSetupDialog", "Дата &начала периода", None))
        self.chkAge.setText(_translate("ClientTreatmentsStructureReportSetupDialog", "Возраст", None))

from library.DateEdit import CDateEdit
from library.TableView import CTableView
