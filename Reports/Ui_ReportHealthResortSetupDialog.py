# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportHealthResortSetupDialog.ui'
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

class Ui_ReportHealthResortSetupDialog(object):
    def setupUi(self, ReportHealthResortSetupDialog):
        ReportHealthResortSetupDialog.setObjectName(_fromUtf8("ReportHealthResortSetupDialog"))
        ReportHealthResortSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportHealthResortSetupDialog.resize(382, 138)
        ReportHealthResortSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportHealthResortSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtEndDate = CDateEdit(ReportHealthResortSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.frmMKB = QtGui.QFrame(ReportHealthResortSetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self._2 = QtGui.QGridLayout(self.frmMKB)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout.addWidget(self.frmMKB, 2, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportHealthResortSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportHealthResortSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ReportHealthResortSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportHealthResortSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(165, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportHealthResortSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportHealthResortSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportHealthResortSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportHealthResortSetupDialog)
        ReportHealthResortSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportHealthResortSetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ReportHealthResortSetupDialog):
        ReportHealthResortSetupDialog.setWindowTitle(_translate("ReportHealthResortSetupDialog", "параметры отчёта", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportHealthResortSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportHealthResortSetupDialog", "Дата начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportHealthResortSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportHealthResortSetupDialog", "Дата окончания периода", None))

from library.DateEdit import CDateEdit
