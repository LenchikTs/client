# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Reports/ReportLaboratoryActionsByMedicalTypeSetupDialog.ui'
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

class Ui_ReportLaboratoryActionsByMedicalTypeSetupDialog(object):
    def setupUi(self, ReportLaboratoryActionsByMedicalTypeSetupDialog):
        ReportLaboratoryActionsByMedicalTypeSetupDialog.setObjectName(_fromUtf8("ReportLaboratoryActionsByMedicalTypeSetupDialog"))
        ReportLaboratoryActionsByMedicalTypeSetupDialog.resize(476, 208)
        self.gridLayout = QtGui.QGridLayout(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 8, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.edtEndDate = CDateEdit(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.chkDetailByMonths = QtGui.QCheckBox(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.chkDetailByMonths.setObjectName(_fromUtf8("chkDetailByMonths"))
        self.gridLayout.addWidget(self.chkDetailByMonths, 5, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 3)
        self.chkDetailByOrgStructures = QtGui.QCheckBox(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.chkDetailByOrgStructures.setObjectName(_fromUtf8("chkDetailByOrgStructures"))
        self.gridLayout.addWidget(self.chkDetailByOrgStructures, 6, 1, 1, 1)
        self.chkDetailByQuarters = QtGui.QCheckBox(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.chkDetailByQuarters.setObjectName(_fromUtf8("chkDetailByQuarters"))
        self.gridLayout.addWidget(self.chkDetailByQuarters, 4, 1, 1, 2)
        self.cmbMedicalAidType = QtGui.QComboBox(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.cmbMedicalAidType.setObjectName(_fromUtf8("cmbMedicalAidType"))
        self.cmbMedicalAidType.addItem(_fromUtf8(""))
        self.cmbMedicalAidType.addItem(_fromUtf8(""))
        self.cmbMedicalAidType.addItem(_fromUtf8(""))
        self.cmbMedicalAidType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMedicalAidType, 2, 1, 1, 1)
        self.lblMedicalAidType = QtGui.QLabel(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        self.lblMedicalAidType.setObjectName(_fromUtf8("lblMedicalAidType"))
        self.gridLayout.addWidget(self.lblMedicalAidType, 2, 0, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportLaboratoryActionsByMedicalTypeSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportLaboratoryActionsByMedicalTypeSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportLaboratoryActionsByMedicalTypeSetupDialog)
        ReportLaboratoryActionsByMedicalTypeSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportLaboratoryActionsByMedicalTypeSetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ReportLaboratoryActionsByMedicalTypeSetupDialog):
        ReportLaboratoryActionsByMedicalTypeSetupDialog.setWindowTitle(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Dialog", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Дата &окончания периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Дата &начала периода", None))
        self.chkDetailByMonths.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Детализировать по месяцам", None))
        self.chkDetailByOrgStructures.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Детализировать по подразделениям", None))
        self.chkDetailByQuarters.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Детализировать по кварталам", None))
        self.cmbMedicalAidType.setItemText(0, _translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Не задано", None))
        self.cmbMedicalAidType.setItemText(1, _translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Стационарная помощь", None))
        self.cmbMedicalAidType.setItemText(2, _translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Амбулаторная помощь", None))
        self.cmbMedicalAidType.setItemText(3, _translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Дневной стационар", None))
        self.lblMedicalAidType.setText(_translate("ReportLaboratoryActionsByMedicalTypeSetupDialog", "Тип медицинской помощи", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportLaboratoryActionsByMedicalTypeSetupDialog = QtGui.QDialog()
    ui = Ui_ReportLaboratoryActionsByMedicalTypeSetupDialog()
    ui.setupUi(ReportLaboratoryActionsByMedicalTypeSetupDialog)
    ReportLaboratoryActionsByMedicalTypeSetupDialog.show()
    sys.exit(app.exec_())

