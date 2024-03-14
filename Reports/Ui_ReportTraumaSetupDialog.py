# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/lampa/Docs/svn/trunk/Reports/ReportTraumaSetupDialog.ui'
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

class Ui_ReportTraumaSetupDialog(object):
    def setupUi(self, ReportTraumaSetupDialog):
        ReportTraumaSetupDialog.setObjectName(_fromUtf8("ReportTraumaSetupDialog"))
        ReportTraumaSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportTraumaSetupDialog.resize(376, 148)
        ReportTraumaSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportTraumaSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblCntUser = QtGui.QLabel(ReportTraumaSetupDialog)
        self.lblCntUser.setObjectName(_fromUtf8("lblCntUser"))
        self.gridlayout.addWidget(self.lblCntUser, 3, 0, 1, 1)
        self.frmMKB = QtGui.QFrame(ReportTraumaSetupDialog)
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
        self.edtBegDate = CDateEdit(ReportTraumaSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportTraumaSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(ReportTraumaSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportTraumaSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportTraumaSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.cmbPeriodIssueDate = QtGui.QComboBox(ReportTraumaSetupDialog)
        self.cmbPeriodIssueDate.setObjectName(_fromUtf8("cmbPeriodIssueDate"))
        self.cmbPeriodIssueDate.addItem(_fromUtf8(""))
        self.cmbPeriodIssueDate.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbPeriodIssueDate, 2, 1, 1, 1)
        self.lblPeriodIssueDate = QtGui.QLabel(ReportTraumaSetupDialog)
        self.lblPeriodIssueDate.setObjectName(_fromUtf8("lblPeriodIssueDate"))
        self.gridlayout.addWidget(self.lblPeriodIssueDate, 2, 0, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportTraumaSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportTraumaSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportTraumaSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportTraumaSetupDialog)
        ReportTraumaSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportTraumaSetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ReportTraumaSetupDialog):
        ReportTraumaSetupDialog.setWindowTitle(_translate("ReportTraumaSetupDialog", "параметры отчёта", None))
        self.lblCntUser.setText(_translate("ReportTraumaSetupDialog", "Номер строки с", None))
        self.lblBegDate.setText(_translate("ReportTraumaSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("ReportTraumaSetupDialog", "Дата окончания периода", None))
        self.cmbPeriodIssueDate.setItemText(0, _translate("ReportTraumaSetupDialog", "дате обращения", None))
        self.cmbPeriodIssueDate.setItemText(1, _translate("ReportTraumaSetupDialog", "дате происшествия", None))
        self.lblPeriodIssueDate.setText(_translate("ReportTraumaSetupDialog", "Отчёт по", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportTraumaSetupDialog = QtGui.QDialog()
    ui = Ui_ReportTraumaSetupDialog()
    ui.setupUi(ReportTraumaSetupDialog)
    ReportTraumaSetupDialog.show()
    sys.exit(app.exec_())

