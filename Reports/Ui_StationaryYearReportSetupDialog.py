# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Reports/StationaryYearReportSetupDialog.ui'
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

class Ui_StationaryYearReportSetupDialog(object):
    def setupUi(self, StationaryYearReportSetupDialog):
        StationaryYearReportSetupDialog.setObjectName(_fromUtf8("StationaryYearReportSetupDialog"))
        StationaryYearReportSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        StationaryYearReportSetupDialog.resize(495, 299)
        StationaryYearReportSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(StationaryYearReportSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.edtMKBTo = QtGui.QLineEdit(StationaryYearReportSetupDialog)
        self.edtMKBTo.setEnabled(False)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 5, 3, 1, 1)
        self.lblReceivedCnd = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblReceivedCnd.setObjectName(_fromUtf8("lblReceivedCnd"))
        self.gridLayout.addWidget(self.lblReceivedCnd, 2, 0, 1, 1)
        self.lblReportYear = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblReportYear.setObjectName(_fromUtf8("lblReportYear"))
        self.gridLayout.addWidget(self.lblReportYear, 0, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.lblOrder = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblOrder.setObjectName(_fromUtf8("lblOrder"))
        self.gridLayout.addWidget(self.lblOrder, 3, 0, 1, 1)
        self.lblAgeFrom = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblAgeFrom.setObjectName(_fromUtf8("lblAgeFrom"))
        self.gridLayout.addWidget(self.lblAgeFrom, 4, 0, 1, 1)
        self.chkEnableMKB = QtGui.QCheckBox(StationaryYearReportSetupDialog)
        self.chkEnableMKB.setObjectName(_fromUtf8("chkEnableMKB"))
        self.gridLayout.addWidget(self.chkEnableMKB, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 1, 1, 4)
        self.cmbOrgStructure = COrgStructureComboBox(StationaryYearReportSetupDialog)
        self.cmbOrgStructure.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 4)
        self.edtAgeFrom = QtGui.QSpinBox(StationaryYearReportSetupDialog)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 4, 1, 1, 1)
        self.lblAgeTo = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblAgeTo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 4, 2, 1, 1)
        self.lblAgeYears = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.gridLayout.addWidget(self.lblAgeYears, 4, 4, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(StationaryYearReportSetupDialog)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 4, 3, 1, 1)
        self.cmbReceivedCnd = QtGui.QComboBox(StationaryYearReportSetupDialog)
        self.cmbReceivedCnd.setObjectName(_fromUtf8("cmbReceivedCnd"))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.setItemText(0, _fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.cmbReceivedCnd.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbReceivedCnd, 2, 1, 1, 4)
        self.cmbOrder = QtGui.QComboBox(StationaryYearReportSetupDialog)
        self.cmbOrder.setObjectName(_fromUtf8("cmbOrder"))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.setItemText(0, _fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrder, 3, 1, 1, 4)
        self.edtReportYear = QtGui.QSpinBox(StationaryYearReportSetupDialog)
        self.edtReportYear.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edtReportYear.setMinimum(2000)
        self.edtReportYear.setMaximum(2500)
        self.edtReportYear.setObjectName(_fromUtf8("edtReportYear"))
        self.gridLayout.addWidget(self.edtReportYear, 0, 1, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(StationaryYearReportSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 1, 1, 4)
        self.edtMKBFrom = QtGui.QLineEdit(StationaryYearReportSetupDialog)
        self.edtMKBFrom.setEnabled(False)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 5, 1, 1, 1)
        self.lblOperations = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblOperations.setObjectName(_fromUtf8("lblOperations"))
        self.gridLayout.addWidget(self.lblOperations, 6, 0, 1, 1)
        self.cmbOperations = CRBComboBox(StationaryYearReportSetupDialog)
        self.cmbOperations.setObjectName(_fromUtf8("cmbOperations"))
        self.gridLayout.addWidget(self.cmbOperations, 6, 1, 1, 4)
        self.lblComplications = QtGui.QLabel(StationaryYearReportSetupDialog)
        self.lblComplications.setObjectName(_fromUtf8("lblComplications"))
        self.gridLayout.addWidget(self.lblComplications, 7, 0, 1, 1)
        self.cmbComplications = QtGui.QComboBox(StationaryYearReportSetupDialog)
        self.cmbComplications.setObjectName(_fromUtf8("cmbComplications"))
        self.cmbComplications.addItem(_fromUtf8(""))
        self.cmbComplications.setItemText(0, _fromUtf8(""))
        self.cmbComplications.addItem(_fromUtf8(""))
        self.cmbComplications.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbComplications, 7, 1, 1, 4)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(StationaryYearReportSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StationaryYearReportSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StationaryYearReportSetupDialog.reject)
        QtCore.QObject.connect(self.chkEnableMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtMKBFrom.setEnabled)
        QtCore.QObject.connect(self.chkEnableMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtMKBTo.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(StationaryYearReportSetupDialog)
        StationaryYearReportSetupDialog.setTabOrder(self.edtReportYear, self.cmbOrgStructure)
        StationaryYearReportSetupDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, StationaryYearReportSetupDialog):
        StationaryYearReportSetupDialog.setWindowTitle(_translate("StationaryYearReportSetupDialog", "Годовой отчет заведующего отделения", None))
        self.edtMKBTo.setInputMask(_translate("StationaryYearReportSetupDialog", "A00.00; ", None))
        self.edtMKBTo.setText(_translate("StationaryYearReportSetupDialog", "Z99.99", None))
        self.lblReceivedCnd.setText(_translate("StationaryYearReportSetupDialog", "Состояние при поступлении", None))
        self.lblReportYear.setText(_translate("StationaryYearReportSetupDialog", "Отчётный год", None))
        self.lblOrgStructure.setText(_translate("StationaryYearReportSetupDialog", "&Подразделение", None))
        self.lblOrder.setText(_translate("StationaryYearReportSetupDialog", "Характер госпитализации", None))
        self.lblAgeFrom.setText(_translate("StationaryYearReportSetupDialog", "Возраст с", None))
        self.chkEnableMKB.setText(_translate("StationaryYearReportSetupDialog", "Коды диагнозов по МКБ", None))
        self.lblAgeTo.setText(_translate("StationaryYearReportSetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("StationaryYearReportSetupDialog", "лет", None))
        self.cmbReceivedCnd.setItemText(1, _translate("StationaryYearReportSetupDialog", "л:Лёгкая форма", None))
        self.cmbReceivedCnd.setItemText(2, _translate("StationaryYearReportSetupDialog", "с:Средне-тяжелая форма", None))
        self.cmbReceivedCnd.setItemText(3, _translate("StationaryYearReportSetupDialog", "т:Тяжелая форма", None))
        self.cmbOrder.setItemText(1, _translate("StationaryYearReportSetupDialog", "Плановые", None))
        self.cmbOrder.setItemText(2, _translate("StationaryYearReportSetupDialog", "Экстренные", None))
        self.edtMKBFrom.setInputMask(_translate("StationaryYearReportSetupDialog", "A00.00; ", None))
        self.edtMKBFrom.setText(_translate("StationaryYearReportSetupDialog", "A00.00", None))
        self.lblOperations.setText(_translate("StationaryYearReportSetupDialog", "Операции", None))
        self.lblComplications.setText(_translate("StationaryYearReportSetupDialog", "Послеоперационные осложнения", None))
        self.cmbComplications.setItemText(1, _translate("StationaryYearReportSetupDialog", "Да", None))
        self.cmbComplications.setItemText(2, _translate("StationaryYearReportSetupDialog", "Нет", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StationaryYearReportSetupDialog = QtGui.QDialog()
    ui = Ui_StationaryYearReportSetupDialog()
    ui.setupUi(StationaryYearReportSetupDialog)
    StationaryYearReportSetupDialog.show()
    sys.exit(app.exec_())

