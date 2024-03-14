# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/PlanningHospitalActivity/RBPlanningHospitalActivity.ui'
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

class Ui_RBPlanningHospitalActivityDialog(object):
    def setupUi(self, RBPlanningHospitalActivityDialog):
        RBPlanningHospitalActivityDialog.setObjectName(_fromUtf8("RBPlanningHospitalActivityDialog"))
        RBPlanningHospitalActivityDialog.resize(614, 606)
        self.gridLayout = QtGui.QGridLayout(RBPlanningHospitalActivityDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnFill = QtGui.QPushButton(RBPlanningHospitalActivityDialog)
        self.btnFill.setObjectName(_fromUtf8("btnFill"))
        self.gridLayout.addWidget(self.btnFill, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(351, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 4)
        self.cmbHospitalBedProfile = CRBComboBox(RBPlanningHospitalActivityDialog)
        self.cmbHospitalBedProfile.setEnabled(False)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 2, 2, 1, 5)
        self.tblItems = CInDocTableViewTabMod(RBPlanningHospitalActivityDialog)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 3, 0, 1, 7)
        self.label = QtGui.QLabel(RBPlanningHospitalActivityDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 4)
        self.chkProfilBed = QtGui.QCheckBox(RBPlanningHospitalActivityDialog)
        self.chkProfilBed.setObjectName(_fromUtf8("chkProfilBed"))
        self.gridLayout.addWidget(self.chkProfilBed, 2, 0, 1, 2)
        self.chkYear = QtGui.QCheckBox(RBPlanningHospitalActivityDialog)
        self.chkYear.setChecked(True)
        self.chkYear.setObjectName(_fromUtf8("chkYear"))
        self.gridLayout.addWidget(self.chkYear, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBPlanningHospitalActivityDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 6, 1, 1)
        self.edtYear = QtGui.QDateEdit(RBPlanningHospitalActivityDialog)
        self.edtYear.setEnabled(True)
        self.edtYear.setObjectName(_fromUtf8("edtYear"))
        self.gridLayout.addWidget(self.edtYear, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 5, 1, 1)
        self.cmbOrgStructure = COrgStructureHospitalBedsComboBox(RBPlanningHospitalActivityDialog)
        self.cmbOrgStructure.setEnabled(False)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 2, 1, 5)
        self.chkOrgStructure = QtGui.QCheckBox(RBPlanningHospitalActivityDialog)
        self.chkOrgStructure.setObjectName(_fromUtf8("chkOrgStructure"))
        self.gridLayout.addWidget(self.chkOrgStructure, 1, 0, 1, 2)

        self.retranslateUi(RBPlanningHospitalActivityDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBPlanningHospitalActivityDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBPlanningHospitalActivityDialog.reject)
        QtCore.QObject.connect(self.chkYear, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.btnFill.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(RBPlanningHospitalActivityDialog)
        RBPlanningHospitalActivityDialog.setTabOrder(self.chkYear, self.edtYear)
        RBPlanningHospitalActivityDialog.setTabOrder(self.edtYear, self.chkOrgStructure)
        RBPlanningHospitalActivityDialog.setTabOrder(self.chkOrgStructure, self.cmbOrgStructure)
        RBPlanningHospitalActivityDialog.setTabOrder(self.cmbOrgStructure, self.chkProfilBed)
        RBPlanningHospitalActivityDialog.setTabOrder(self.chkProfilBed, self.cmbHospitalBedProfile)
        RBPlanningHospitalActivityDialog.setTabOrder(self.cmbHospitalBedProfile, self.tblItems)
        RBPlanningHospitalActivityDialog.setTabOrder(self.tblItems, self.buttonBox)

    def retranslateUi(self, RBPlanningHospitalActivityDialog):
        RBPlanningHospitalActivityDialog.setWindowTitle(_translate("RBPlanningHospitalActivityDialog", "Планирование стационарной деятельности", None))
        self.btnFill.setText(_translate("RBPlanningHospitalActivityDialog", "Сгенерировать список подразделений", None))
        self.label.setText(_translate("RBPlanningHospitalActivityDialog", "Всего:", None))
        self.chkProfilBed.setText(_translate("RBPlanningHospitalActivityDialog", "Профиль койки", None))
        self.chkYear.setText(_translate("RBPlanningHospitalActivityDialog", "Год", None))
        self.edtYear.setDisplayFormat(_translate("RBPlanningHospitalActivityDialog", "yyyy", None))
        self.chkOrgStructure.setText(_translate("RBPlanningHospitalActivityDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureHospitalBedsComboBox
from RefBooks.Utils import CInDocTableViewTabMod
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBPlanningHospitalActivityDialog = QtGui.QDialog()
    ui = Ui_RBPlanningHospitalActivityDialog()
    ui.setupUi(RBPlanningHospitalActivityDialog)
    RBPlanningHospitalActivityDialog.show()
    sys.exit(app.exec_())

