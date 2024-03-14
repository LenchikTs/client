# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Reports/FinanceServiceSetupDialog.ui'
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

class Ui_FinanceServiceSetupDialog(object):
    def setupUi(self, FinanceServiceSetupDialog):
        FinanceServiceSetupDialog.setObjectName(_fromUtf8("FinanceServiceSetupDialog"))
        FinanceServiceSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        FinanceServiceSetupDialog.resize(495, 163)
        FinanceServiceSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(FinanceServiceSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEndDate = QtGui.QLabel(FinanceServiceSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(FinanceServiceSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 4)
        self.lblPerson = QtGui.QLabel(FinanceServiceSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 4, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(FinanceServiceSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 2)
        self.lblSpeciality = QtGui.QLabel(FinanceServiceSetupDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 3, 0, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(FinanceServiceSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 2)
        self.cmbSpeciality = CRBComboBox(FinanceServiceSetupDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 3, 2, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(FinanceServiceSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 4, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 2, 1, 1)
        self.edtEndDate = CDateEdit(FinanceServiceSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(FinanceServiceSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.edtBegDate = CDateEdit(FinanceServiceSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(FinanceServiceSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FinanceServiceSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FinanceServiceSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FinanceServiceSetupDialog)
        FinanceServiceSetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        FinanceServiceSetupDialog.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        FinanceServiceSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        FinanceServiceSetupDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        FinanceServiceSetupDialog.setTabOrder(self.cmbPerson, self.buttonBox)

    def retranslateUi(self, FinanceServiceSetupDialog):
        FinanceServiceSetupDialog.setWindowTitle(_translate("FinanceServiceSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("FinanceServiceSetupDialog", "Дата &окончания периода", None))
        self.lblPerson.setText(_translate("FinanceServiceSetupDialog", "&Врач", None))
        self.lblSpeciality.setText(_translate("FinanceServiceSetupDialog", "&Специальность", None))
        self.lblOrgStructure.setText(_translate("FinanceServiceSetupDialog", "&Подразделение", None))
        self.cmbSpeciality.setWhatsThis(_translate("FinanceServiceSetupDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.edtEndDate.setDisplayFormat(_translate("FinanceServiceSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("FinanceServiceSetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("FinanceServiceSetupDialog", "dd.MM.yyyy", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FinanceServiceSetupDialog = QtGui.QDialog()
    ui = Ui_FinanceServiceSetupDialog()
    ui.setupUi(FinanceServiceSetupDialog)
    FinanceServiceSetupDialog.show()
    sys.exit(app.exec_())

