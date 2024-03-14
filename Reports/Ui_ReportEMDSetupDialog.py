# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportEMDSetupDialog.ui'
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

class Ui_ReportEMDSetupDialog(object):
    def setupUi(self, ReportEMDSetupDialog):
        ReportEMDSetupDialog.setObjectName(_fromUtf8("ReportEMDSetupDialog"))
        ReportEMDSetupDialog.resize(428, 384)
        self.gridLayout = QtGui.QGridLayout(ReportEMDSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 2)
        self.cmbFinance = CRBComboBox(ReportEMDSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 2, 1, 1, 1)
        self.lblFinance = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportEMDSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 2)
        self.edtBegDate = CDateEdit(ReportEMDSetupDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.cmbEventType = CRBComboBox(ReportEMDSetupDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 3, 1, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportEMDSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportEMDSetupDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 3, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        self.chkOnlyProtocols = QtGui.QCheckBox(ReportEMDSetupDialog)
        self.chkOnlyProtocols.setObjectName(_fromUtf8("chkOnlyProtocols"))
        self.gridLayout.addWidget(self.chkOnlyProtocols, 8, 0, 1, 2)
        self.chkOnlyInspections = QtGui.QCheckBox(ReportEMDSetupDialog)
        self.chkOnlyInspections.setObjectName(_fromUtf8("chkOnlyInspections"))
        self.gridLayout.addWidget(self.chkOnlyInspections, 7, 0, 1, 2)
        self.lblStatus = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 6, 0, 1, 1)
        self.chkDetailClients = QtGui.QCheckBox(ReportEMDSetupDialog)
        self.chkDetailClients.setObjectName(_fromUtf8("chkDetailClients"))
        self.gridLayout.addWidget(self.chkDetailClients, 9, 0, 1, 2)
        self.cmbStatus = QtGui.QComboBox(ReportEMDSetupDialog)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.cmbStatus.addItem(_fromUtf8(""))
        self.cmbStatus.addItem(_fromUtf8(""))
        self.cmbStatus.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbStatus, 6, 1, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportEMDSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportEMDSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 5, 0, 1, 1)

        self.retranslateUi(ReportEMDSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportEMDSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportEMDSetupDialog.reject)
        QtCore.QObject.connect(self.chkOnlyProtocols, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbStatus.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(ReportEMDSetupDialog)

    def retranslateUi(self, ReportEMDSetupDialog):
        ReportEMDSetupDialog.setWindowTitle(_translate("ReportEMDSetupDialog", "Dialog", None))
        self.lblFinance.setText(_translate("ReportEMDSetupDialog", "Тип финансирования", None))
        self.lblBegDate.setText(_translate("ReportEMDSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("ReportEMDSetupDialog", "Дата окончания периода", None))
        self.lblEventType.setText(_translate("ReportEMDSetupDialog", "Тип события", None))
        self.lblOrgStructure.setText(_translate("ReportEMDSetupDialog", "Подразделение", None))
        self.chkOnlyProtocols.setText(_translate("ReportEMDSetupDialog", "Только протоколы", None))
        self.chkOnlyInspections.setText(_translate("ReportEMDSetupDialog", "Только осмотры (первичные и повторные)", None))
        self.lblStatus.setText(_translate("ReportEMDSetupDialog", "Статус документа", None))
        self.chkDetailClients.setText(_translate("ReportEMDSetupDialog", "Детализировать по пациентам", None))
        self.cmbStatus.setItemText(0, _translate("ReportEMDSetupDialog", "Не задано", None))
        self.cmbStatus.setItemText(1, _translate("ReportEMDSetupDialog", "Подписан", None))
        self.cmbStatus.setItemText(2, _translate("ReportEMDSetupDialog", "Не подписан", None))
        self.lblPerson.setText(_translate("ReportEMDSetupDialog", "Исполнитель", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportEMDSetupDialog = QtGui.QDialog()
    ui = Ui_ReportEMDSetupDialog()
    ui.setupUi(ReportEMDSetupDialog)
    ReportEMDSetupDialog.show()
    sys.exit(app.exec_())

