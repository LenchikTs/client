# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Reports/ProfileYearReportSetupDialog.ui'
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

class Ui_ProfileYearReportSetupDialog(object):
    def setupUi(self, ProfileYearReportSetupDialog):
        ProfileYearReportSetupDialog.setObjectName(_fromUtf8("ProfileYearReportSetupDialog"))
        ProfileYearReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ProfileYearReportSetupDialog.resize(491, 236)
        ProfileYearReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ProfileYearReportSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkEnableMKB = QtGui.QCheckBox(ProfileYearReportSetupDialog)
        self.chkEnableMKB.setChecked(False)
        self.chkEnableMKB.setObjectName(_fromUtf8("chkEnableMKB"))
        self.gridLayout.addWidget(self.chkEnableMKB, 5, 0, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(ProfileYearReportSetupDialog)
        self.edtMKBFrom.setEnabled(False)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 5, 1, 1, 1)
        self.lblReceivedCnd = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblReceivedCnd.setObjectName(_fromUtf8("lblReceivedCnd"))
        self.gridLayout.addWidget(self.lblReceivedCnd, 1, 0, 1, 1)
        self.cmbReceivedCnd = QtGui.QComboBox(ProfileYearReportSetupDialog)
        self.cmbReceivedCnd.setObjectName(_fromUtf8("cmbReceivedCnd"))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.setItemText(0, _fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbReceivedCnd, 1, 1, 1, 3)
        self.lblOrder = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblOrder.setObjectName(_fromUtf8("lblOrder"))
        self.gridLayout.addWidget(self.lblOrder, 2, 0, 1, 1)
        self.cmbOrder = QtGui.QComboBox(ProfileYearReportSetupDialog)
        self.cmbOrder.setObjectName(_fromUtf8("cmbOrder"))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.setItemText(0, _fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrder, 2, 1, 1, 3)
        self.lblAgeFrom = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.gridLayout.addWidget(self.lblAgeFrom, 4, 0, 1, 1)
        self.edtMKBTo = CICDCodeEdit(ProfileYearReportSetupDialog)
        self.edtMKBTo.setEnabled(False)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 5, 3, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(ProfileYearReportSetupDialog)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 4, 1, 1, 1)
        self.lblAgeTo = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 4, 2, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(ProfileYearReportSetupDialog)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 4, 3, 1, 1)
        self.lblAgeYears = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.gridLayout.addWidget(self.lblAgeYears, 4, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.lblReportYear = QtGui.QLabel(ProfileYearReportSetupDialog)
        self.lblReportYear.setObjectName(_fromUtf8("lblReportYear"))
        self.gridLayout.addWidget(self.lblReportYear, 0, 0, 1, 1)
        self.edtReportYear = QtGui.QSpinBox(ProfileYearReportSetupDialog)
        self.edtReportYear.setMinimum(2000)
        self.edtReportYear.setMaximum(2500)
        self.edtReportYear.setObjectName(_fromUtf8("edtReportYear"))
        self.gridLayout.addWidget(self.edtReportYear, 0, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ProfileYearReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 1, 1, 3)

        self.retranslateUi(ProfileYearReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProfileYearReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProfileYearReportSetupDialog.reject)
        QtCore.QObject.connect(self.chkEnableMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtMKBFrom.setEnabled)
        QtCore.QObject.connect(self.chkEnableMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtMKBTo.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ProfileYearReportSetupDialog)
        ProfileYearReportSetupDialog.setTabOrder(self.edtReportYear, self.buttonBox)

    def retranslateUi(self, ProfileYearReportSetupDialog):
        ProfileYearReportSetupDialog.setWindowTitle(_translate("ProfileYearReportSetupDialog", "Годовой отчет за ЛПУ по профилям", None))
        self.chkEnableMKB.setText(_translate("ProfileYearReportSetupDialog", "Коды диагнозов по МКБ", None))
        self.edtMKBFrom.setInputMask(_translate("ProfileYearReportSetupDialog", "A00.00; ", None))
        self.edtMKBFrom.setText(_translate("ProfileYearReportSetupDialog", "A.", None))
        self.lblReceivedCnd.setText(_translate("ProfileYearReportSetupDialog", "Состояние при поступлении", None))
        self.cmbReceivedCnd.setItemText(1, _translate("ProfileYearReportSetupDialog", "л:Лёгкая форма", None))
        self.cmbReceivedCnd.setItemText(2, _translate("ProfileYearReportSetupDialog", "с:Средне-тяжелая форма", None))
        self.cmbReceivedCnd.setItemText(3, _translate("ProfileYearReportSetupDialog", "т:Тяжелая форма", None))
        self.lblOrder.setText(_translate("ProfileYearReportSetupDialog", "Характер госпитализации", None))
        self.cmbOrder.setItemText(1, _translate("ProfileYearReportSetupDialog", "Плановые", None))
        self.cmbOrder.setItemText(2, _translate("ProfileYearReportSetupDialog", "Экстренные", None))
        self.lblAgeFrom.setText(_translate("ProfileYearReportSetupDialog", "Возраст с", None))
        self.edtMKBTo.setInputMask(_translate("ProfileYearReportSetupDialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("ProfileYearReportSetupDialog", "Z99.9", None))
        self.lblAgeTo.setText(_translate("ProfileYearReportSetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("ProfileYearReportSetupDialog", "лет", None))
        self.lblReportYear.setText(_translate("ProfileYearReportSetupDialog", "Отчётный год", None))

from library.ICDCodeEdit import CICDCodeEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProfileYearReportSetupDialog = QtGui.QDialog()
    ui = Ui_ProfileYearReportSetupDialog()
    ui.setupUi(ProfileYearReportSetupDialog)
    ProfileYearReportSetupDialog.show()
    sys.exit(app.exec_())

