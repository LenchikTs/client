# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportImunoprophylaxisForm5SetupDialog.ui'
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

class Ui_CReportImunoprophylaxisForm5SetupDialog(object):
    def setupUi(self, CReportImunoprophylaxisForm5SetupDialog):
        CReportImunoprophylaxisForm5SetupDialog.setObjectName(_fromUtf8("CReportImunoprophylaxisForm5SetupDialog"))
        CReportImunoprophylaxisForm5SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        CReportImunoprophylaxisForm5SetupDialog.resize(435, 186)
        CReportImunoprophylaxisForm5SetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(CReportImunoprophylaxisForm5SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtEndDate = CDateEdit(CReportImunoprophylaxisForm5SetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        self.frmMKB = QtGui.QFrame(CReportImunoprophylaxisForm5SetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self._2 = QtGui.QGridLayout(self.frmMKB)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.gridLayout.addWidget(self.frmMKB, 3, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(CReportImunoprophylaxisForm5SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(CReportImunoprophylaxisForm5SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(CReportImunoprophylaxisForm5SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(CReportImunoprophylaxisForm5SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.cmbPerson = CPersonComboBox(CReportImunoprophylaxisForm5SetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 2)
        self.lblPerson = QtGui.QLabel(CReportImunoprophylaxisForm5SetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(CReportImunoprophylaxisForm5SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CReportImunoprophylaxisForm5SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CReportImunoprophylaxisForm5SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CReportImunoprophylaxisForm5SetupDialog)
        CReportImunoprophylaxisForm5SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        CReportImunoprophylaxisForm5SetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, CReportImunoprophylaxisForm5SetupDialog):
        CReportImunoprophylaxisForm5SetupDialog.setWindowTitle(_translate("CReportImunoprophylaxisForm5SetupDialog", "параметры отчёта", None))
        self.edtEndDate.setDisplayFormat(_translate("CReportImunoprophylaxisForm5SetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("CReportImunoprophylaxisForm5SetupDialog", "Дата начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("CReportImunoprophylaxisForm5SetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("CReportImunoprophylaxisForm5SetupDialog", "Дата окончания периода", None))
        self.lblPerson.setText(_translate("CReportImunoprophylaxisForm5SetupDialog", "Врач", None))

from Orgs.PersonComboBox import CPersonComboBox
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CReportImunoprophylaxisForm5SetupDialog = QtGui.QDialog()
    ui = Ui_CReportImunoprophylaxisForm5SetupDialog()
    ui.setupUi(CReportImunoprophylaxisForm5SetupDialog)
    CReportImunoprophylaxisForm5SetupDialog.show()
    sys.exit(app.exec_())

