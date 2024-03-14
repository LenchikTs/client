# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Reports\ReportTraumaJVSetupDialog.ui'
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

class Ui_ReportTraumaJVSetupDialog(object):
    def setupUi(self, ReportTraumaJVSetupDialog):
        ReportTraumaJVSetupDialog.setObjectName(_fromUtf8("ReportTraumaJVSetupDialog"))
        ReportTraumaJVSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportTraumaJVSetupDialog.resize(376, 148)
        ReportTraumaJVSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportTraumaJVSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblCntUser = QtGui.QLabel(ReportTraumaJVSetupDialog)
        self.lblCntUser.setObjectName(_fromUtf8("lblCntUser"))
        self.gridlayout.addWidget(self.lblCntUser, 3, 0, 1, 1)
        self.frmMKB = QtGui.QFrame(ReportTraumaJVSetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self._2 = QtGui.QGridLayout(self.frmMKB)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.edtCntUser = QtGui.QSpinBox(self.frmMKB)
        self.edtCntUser.setMinimum(1)
        self.edtCntUser.setMaximum(999999999)
        self.edtCntUser.setObjectName(_fromUtf8("edtCntUser"))
        self._2.addWidget(self.edtCntUser, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.frmMKB, 3, 1, 1, 2)
        self.edtBegDate = CDateEdit(ReportTraumaJVSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportTraumaJVSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(ReportTraumaJVSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportTraumaJVSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportTraumaJVSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.cmbPeriodIssueDate = QtGui.QComboBox(ReportTraumaJVSetupDialog)
        self.cmbPeriodIssueDate.setObjectName(_fromUtf8("cmbPeriodIssueDate"))
        self.cmbPeriodIssueDate.addItem(_fromUtf8(""))
        self.cmbPeriodIssueDate.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbPeriodIssueDate, 2, 1, 1, 1)
        self.lblPeriodIssueDate = QtGui.QLabel(ReportTraumaJVSetupDialog)
        self.lblPeriodIssueDate.setObjectName(_fromUtf8("lblPeriodIssueDate"))
        self.gridlayout.addWidget(self.lblPeriodIssueDate, 2, 0, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportTraumaJVSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportTraumaJVSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportTraumaJVSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportTraumaJVSetupDialog)
        ReportTraumaJVSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportTraumaJVSetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ReportTraumaJVSetupDialog):
        ReportTraumaJVSetupDialog.setWindowTitle(_translate("ReportTraumaJVSetupDialog", "параметры отчёта", None))
        self.lblCntUser.setText(_translate("ReportTraumaJVSetupDialog", "Номер строки с", None))
        self.lblBegDate.setText(_translate("ReportTraumaJVSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("ReportTraumaJVSetupDialog", "Дата окончания периода", None))
        self.cmbPeriodIssueDate.setItemText(0, _translate("ReportTraumaJVSetupDialog", "дате обращения", None))
        self.cmbPeriodIssueDate.setItemText(1, _translate("ReportTraumaJVSetupDialog", "дате происшествия", None))
        self.lblPeriodIssueDate.setText(_translate("ReportTraumaJVSetupDialog", "Отчёт по", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportTraumaJVSetupDialog = QtGui.QDialog()
    ui = Ui_ReportTraumaJVSetupDialog()
    ui.setupUi(ReportTraumaJVSetupDialog)
    ReportTraumaJVSetupDialog.show()
    sys.exit(app.exec_())

