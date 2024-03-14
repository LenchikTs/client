# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Reports/ReportSanatoriumSetupDialog.ui'
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

class Ui_ReportSanatoriumSetupDialog(object):
    def setupUi(self, ReportSanatoriumSetupDialog):
        ReportSanatoriumSetupDialog.setObjectName(_fromUtf8("ReportSanatoriumSetupDialog"))
        ReportSanatoriumSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportSanatoriumSetupDialog.resize(408, 184)
        ReportSanatoriumSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportSanatoriumSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ReportSanatoriumSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.lblBegDate = QtGui.QLabel(ReportSanatoriumSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportSanatoriumSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.frmMKB = QtGui.QFrame(ReportSanatoriumSetupDialog)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self._2 = QtGui.QGridLayout(self.frmMKB)
        self._2.setMargin(0)
        self._2.setHorizontalSpacing(4)
        self._2.setVerticalSpacing(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.chkPatronage = QtGui.QCheckBox(self.frmMKB)
        self.chkPatronage.setEnabled(True)
        self.chkPatronage.setChecked(False)
        self.chkPatronage.setObjectName(_fromUtf8("chkPatronage"))
        self._2.addWidget(self.chkPatronage, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.frmMKB, 3, 1, 1, 2)
        self.edtBegDate = CDateEdit(ReportSanatoriumSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 6, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportSanatoriumSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblShowAddress = QtGui.QLabel(ReportSanatoriumSetupDialog)
        self.lblShowAddress.setObjectName(_fromUtf8("lblShowAddress"))
        self.gridlayout.addWidget(self.lblShowAddress, 2, 0, 1, 1)
        self.cmbShowAddress = QtGui.QComboBox(ReportSanatoriumSetupDialog)
        self.cmbShowAddress.setObjectName(_fromUtf8("cmbShowAddress"))
        self.cmbShowAddress.addItem(_fromUtf8(""))
        self.cmbShowAddress.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbShowAddress, 2, 1, 1, 2)
        self.chkShowBirthDate = QtGui.QCheckBox(ReportSanatoriumSetupDialog)
        self.chkShowBirthDate.setEnabled(True)
        self.chkShowBirthDate.setChecked(False)
        self.chkShowBirthDate.setObjectName(_fromUtf8("chkShowBirthDate"))
        self.gridlayout.addWidget(self.chkShowBirthDate, 4, 1, 1, 2)
        self.lblBuildBy = QtGui.QLabel(ReportSanatoriumSetupDialog)
        self.lblBuildBy.setObjectName(_fromUtf8("lblBuildBy"))
        self.gridlayout.addWidget(self.lblBuildBy, 5, 0, 1, 1)
        self.cmbBuildBy = QtGui.QComboBox(ReportSanatoriumSetupDialog)
        self.cmbBuildBy.setObjectName(_fromUtf8("cmbBuildBy"))
        self.cmbBuildBy.addItem(_fromUtf8(""))
        self.cmbBuildBy.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbBuildBy, 5, 1, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportSanatoriumSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportSanatoriumSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportSanatoriumSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportSanatoriumSetupDialog)
        ReportSanatoriumSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportSanatoriumSetupDialog.setTabOrder(self.edtEndDate, self.cmbShowAddress)
        ReportSanatoriumSetupDialog.setTabOrder(self.cmbShowAddress, self.chkPatronage)
        ReportSanatoriumSetupDialog.setTabOrder(self.chkPatronage, self.chkShowBirthDate)
        ReportSanatoriumSetupDialog.setTabOrder(self.chkShowBirthDate, self.cmbBuildBy)
        ReportSanatoriumSetupDialog.setTabOrder(self.cmbBuildBy, self.buttonBox)

    def retranslateUi(self, ReportSanatoriumSetupDialog):
        ReportSanatoriumSetupDialog.setWindowTitle(_translate("ReportSanatoriumSetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportSanatoriumSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("ReportSanatoriumSetupDialog", "Дата окончания периода", None))
        self.chkPatronage.setText(_translate("ReportSanatoriumSetupDialog", "Учитывать лицо по уходу", None))
        self.lblShowAddress.setText(_translate("ReportSanatoriumSetupDialog", "Показывать адрес", None))
        self.cmbShowAddress.setItemText(0, _translate("ReportSanatoriumSetupDialog", "по месту регистрации", None))
        self.cmbShowAddress.setItemText(1, _translate("ReportSanatoriumSetupDialog", "по месту жительства", None))
        self.chkShowBirthDate.setText(_translate("ReportSanatoriumSetupDialog", "Показывать дату рождения", None))
        self.lblBuildBy.setText(_translate("ReportSanatoriumSetupDialog", "Формировать по", None))
        self.cmbBuildBy.setItemText(0, _translate("ReportSanatoriumSetupDialog", "пациентам", None))
        self.cmbBuildBy.setItemText(1, _translate("ReportSanatoriumSetupDialog", "лицам по уходу", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportSanatoriumSetupDialog = QtGui.QDialog()
    ui = Ui_ReportSanatoriumSetupDialog()
    ui.setupUi(ReportSanatoriumSetupDialog)
    ReportSanatoriumSetupDialog.show()
    sys.exit(app.exec_())

