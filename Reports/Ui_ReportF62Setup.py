# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportF62Setup.ui'
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

class Ui_ReportF62SetupDialog(object):
    def setupUi(self, ReportF62SetupDialog):
        ReportF62SetupDialog.setObjectName(_fromUtf8("ReportF62SetupDialog"))
        ReportF62SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportF62SetupDialog.resize(420, 151)
        ReportF62SetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportF62SetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtEndDate = CDateEdit(ReportF62SetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.edtBegDate = CDateEdit(ReportF62SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportF62SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.frmAge = QtGui.QFrame(ReportF62SetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self._2 = QtGui.QHBoxLayout(self.frmAge)
        self._2.setMargin(0)
        self._2.setSpacing(4)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridlayout.addWidget(self.frmAge, 4, 1, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportF62SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportF62SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.lblSelectRegion = QtGui.QLabel(ReportF62SetupDialog)
        self.lblSelectRegion.setObjectName(_fromUtf8("lblSelectRegion"))
        self.gridlayout.addWidget(self.lblSelectRegion, 2, 0, 1, 1)
        self.cmbSelectRegion = QtGui.QComboBox(ReportF62SetupDialog)
        self.cmbSelectRegion.setObjectName(_fromUtf8("cmbSelectRegion"))
        self.cmbSelectRegion.addItem(_fromUtf8(""))
        self.cmbSelectRegion.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbSelectRegion, 2, 1, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportF62SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportF62SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportF62SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportF62SetupDialog)
        ReportF62SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportF62SetupDialog.setTabOrder(self.edtEndDate, self.cmbSelectRegion)
        ReportF62SetupDialog.setTabOrder(self.cmbSelectRegion, self.buttonBox)

    def retranslateUi(self, ReportF62SetupDialog):
        ReportF62SetupDialog.setWindowTitle(_translate("ReportF62SetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportF62SetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("ReportF62SetupDialog", "Дата окончания периода", None))
        self.lblSelectRegion.setText(_translate("ReportF62SetupDialog", "Отбор по", None))
        self.cmbSelectRegion.setItemText(0, _translate("ReportF62SetupDialog", "Адрес регистрации", None))
        self.cmbSelectRegion.setItemText(1, _translate("ReportF62SetupDialog", "Адрес проживания", None))

from library.DateEdit import CDateEdit
