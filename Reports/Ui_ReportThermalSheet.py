# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Reports\ReportThermalSheet.ui'
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

class Ui_ReportThermalSheetDialog(object):
    def setupUi(self, ReportThermalSheetDialog):
        ReportThermalSheetDialog.setObjectName(_fromUtf8("ReportThermalSheetDialog"))
        ReportThermalSheetDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportThermalSheetDialog.resize(371, 120)
        ReportThermalSheetDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportThermalSheetDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtBegDate = CDateEdit(ReportThermalSheetDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 2)
        self.edtBegTime = CTimeEdit(ReportThermalSheetDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportThermalSheetDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportThermalSheetDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 3)
        self.lblBegDate = QtGui.QLabel(ReportThermalSheetDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblThermalLimit = QtGui.QLabel(ReportThermalSheetDialog)
        self.lblThermalLimit.setObjectName(_fromUtf8("lblThermalLimit"))
        self.gridLayout.addWidget(self.lblThermalLimit, 2, 0, 1, 1)
        self.edtThermalLimit = QtGui.QDoubleSpinBox(ReportThermalSheetDialog)
        self.edtThermalLimit.setObjectName(_fromUtf8("edtThermalLimit"))
        self.gridLayout.addWidget(self.edtThermalLimit, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportThermalSheetDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(ReportThermalSheetDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportThermalSheetDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportThermalSheetDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportThermalSheetDialog)
        ReportThermalSheetDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        ReportThermalSheetDialog.setTabOrder(self.edtBegTime, self.cmbOrgStructure)
        ReportThermalSheetDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, ReportThermalSheetDialog):
        ReportThermalSheetDialog.setWindowTitle(_translate("ReportThermalSheetDialog", "параметры отчёта", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportThermalSheetDialog", "dd.MM.yyyy", None))
        self.edtBegTime.setDisplayFormat(_translate("ReportThermalSheetDialog", "H:mm", None))
        self.lblOrgStructure.setText(_translate("ReportThermalSheetDialog", "&Подразделение", None))
        self.lblBegDate.setText(_translate("ReportThermalSheetDialog", "Дата", None))
        self.lblThermalLimit.setText(_translate("ReportThermalSheetDialog", "Нижний предел температуры", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.TimeEdit import CTimeEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportThermalSheetDialog = QtGui.QDialog()
    ui = Ui_ReportThermalSheetDialog()
    ui.setupUi(ReportThermalSheetDialog)
    ReportThermalSheetDialog.show()
    sys.exit(app.exec_())

