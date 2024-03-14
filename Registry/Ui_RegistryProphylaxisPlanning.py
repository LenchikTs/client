# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Registry/RegistryProphylaxisPlanning.ui'
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

class Ui_RegistryProphylaxisPlanningDialog(object):
    def setupUi(self, RegistryProphylaxisPlanningDialog):
        RegistryProphylaxisPlanningDialog.setObjectName(_fromUtf8("RegistryProphylaxisPlanningDialog"))
        RegistryProphylaxisPlanningDialog.resize(459, 507)
        self.gridLayout_2 = QtGui.QGridLayout(RegistryProphylaxisPlanningDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblOrgStructure = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout_2.addWidget(self.lblOrgStructure, 0, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout_2.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(RegistryProphylaxisPlanningDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout_2.addWidget(self.cmbOrgStructure, 0, 1, 1, 2)
        self.lblNote = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout_2.addWidget(self.lblNote, 7, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(RegistryProphylaxisPlanningDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout_2.addWidget(self.cmbSpeciality, 1, 1, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(RegistryProphylaxisPlanningDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout_2.addWidget(self.cmbPerson, 2, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 9, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(RegistryProphylaxisPlanningDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(1, 0, 1, 1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblVisitPeriods = CTableView(self.groupBox)
        self.tblVisitPeriods.setObjectName(_fromUtf8("tblVisitPeriods"))
        self.gridLayout.addWidget(self.tblVisitPeriods, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(RegistryProphylaxisPlanningDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 10, 0, 1, 3)
        self.lblScene = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblScene.setObjectName(_fromUtf8("lblScene"))
        self.gridLayout_2.addWidget(self.lblScene, 5, 0, 1, 1)
        self.cmbScene = CRBComboBox(RegistryProphylaxisPlanningDialog)
        self.cmbScene.setObjectName(_fromUtf8("cmbScene"))
        self.gridLayout_2.addWidget(self.cmbScene, 5, 1, 1, 2)
        self.lblSpeciality = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout_2.addWidget(self.lblSpeciality, 1, 0, 1, 1)
        self.lblProphylaxisPlanningType = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblProphylaxisPlanningType.setObjectName(_fromUtf8("lblProphylaxisPlanningType"))
        self.gridLayout_2.addWidget(self.lblProphylaxisPlanningType, 4, 0, 1, 1)
        self.edtMKB = CICDCodeEditEx(RegistryProphylaxisPlanningDialog)
        self.edtMKB.setObjectName(_fromUtf8("edtMKB"))
        self.gridLayout_2.addWidget(self.edtMKB, 6, 1, 1, 1)
        self.lblDiagnosis = QtGui.QLabel(RegistryProphylaxisPlanningDialog)
        self.lblDiagnosis.setObjectName(_fromUtf8("lblDiagnosis"))
        self.gridLayout_2.addWidget(self.lblDiagnosis, 6, 0, 1, 1)
        self.cmbProphylaxisPlanningType = CRBComboBox(RegistryProphylaxisPlanningDialog)
        self.cmbProphylaxisPlanningType.setObjectName(_fromUtf8("cmbProphylaxisPlanningType"))
        self.gridLayout_2.addWidget(self.cmbProphylaxisPlanningType, 4, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 8, 0, 1, 1)
        self.edtNote = QtGui.QTextEdit(RegistryProphylaxisPlanningDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout_2.addWidget(self.edtNote, 7, 1, 2, 2)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblNote.setBuddy(self.edtNote)
        self.lblScene.setBuddy(self.cmbScene)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblProphylaxisPlanningType.setBuddy(self.cmbProphylaxisPlanningType)
        self.lblDiagnosis.setBuddy(self.edtMKB)

        self.retranslateUi(RegistryProphylaxisPlanningDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RegistryProphylaxisPlanningDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RegistryProphylaxisPlanningDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegistryProphylaxisPlanningDialog)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.cmbPerson, self.tblVisitPeriods)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.tblVisitPeriods, self.cmbProphylaxisPlanningType)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.cmbProphylaxisPlanningType, self.cmbScene)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.cmbScene, self.edtMKB)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.edtMKB, self.edtNote)
        RegistryProphylaxisPlanningDialog.setTabOrder(self.edtNote, self.buttonBox)

    def retranslateUi(self, RegistryProphylaxisPlanningDialog):
        RegistryProphylaxisPlanningDialog.setWindowTitle(_translate("RegistryProphylaxisPlanningDialog", "Запись в Журнал планирования профилактического наблюдения", None))
        self.lblOrgStructure.setText(_translate("RegistryProphylaxisPlanningDialog", "&Подразделение", None))
        self.lblPerson.setText(_translate("RegistryProphylaxisPlanningDialog", "&Врач", None))
        self.lblNote.setText(_translate("RegistryProphylaxisPlanningDialog", "Приме&чание", None))
        self.groupBox.setTitle(_translate("RegistryProphylaxisPlanningDialog", "Планируемые периоды визитов", None))
        self.lblScene.setText(_translate("RegistryProphylaxisPlanningDialog", "&Место", None))
        self.lblSpeciality.setText(_translate("RegistryProphylaxisPlanningDialog", "&Специальность", None))
        self.lblProphylaxisPlanningType.setText(_translate("RegistryProphylaxisPlanningDialog", "&Тип планирования профилактики", None))
        self.lblDiagnosis.setText(_translate("RegistryProphylaxisPlanningDialog", "&Диагноз", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.ICDCodeEdit import CICDCodeEditEx
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RegistryProphylaxisPlanningDialog = QtGui.QDialog()
    ui = Ui_RegistryProphylaxisPlanningDialog()
    ui.setupUi(RegistryProphylaxisPlanningDialog)
    RegistryProphylaxisPlanningDialog.show()
    sys.exit(app.exec_())

