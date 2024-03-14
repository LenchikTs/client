# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Registry/RegistrySuspenedAppointment.ui'
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

class Ui_RegistrySuspenedAppointmentDialog(object):
    def setupUi(self, RegistrySuspenedAppointmentDialog):
        RegistrySuspenedAppointmentDialog.setObjectName(_fromUtf8("RegistrySuspenedAppointmentDialog"))
        RegistrySuspenedAppointmentDialog.resize(468, 300)
        self.gridLayout = QtGui.QGridLayout(RegistrySuspenedAppointmentDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 0, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(RegistrySuspenedAppointmentDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 1, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(RegistrySuspenedAppointmentDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 3, 0, 1, 1)
        self.edtBegDate = CDateEdit(RegistrySuspenedAppointmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 3, 1, 1, 1)
        self.lblNote = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(215, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 4, 0, 1, 1)
        self.edtEndDate = CDateEdit(RegistrySuspenedAppointmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(215, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RegistrySuspenedAppointmentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.lblSpeciality = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 1, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(RegistrySuspenedAppointmentDialog)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 1, 1, 1, 2)
        self.lblPerson = QtGui.QLabel(RegistrySuspenedAppointmentDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 1)
        self.edtNote = QtGui.QTextEdit(RegistrySuspenedAppointmentDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 5, 1, 2, 2)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblNote.setBuddy(self.edtNote)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(RegistrySuspenedAppointmentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RegistrySuspenedAppointmentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RegistrySuspenedAppointmentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegistrySuspenedAppointmentDialog)

    def retranslateUi(self, RegistrySuspenedAppointmentDialog):
        RegistrySuspenedAppointmentDialog.setWindowTitle(_translate("RegistrySuspenedAppointmentDialog", "Запись в Журнал отложенной записи", None))
        self.lblOrgStructure.setText(_translate("RegistrySuspenedAppointmentDialog", "&Подразделение", None))
        self.lblBegDate.setText(_translate("RegistrySuspenedAppointmentDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("RegistrySuspenedAppointmentDialog", "dd.MM.yyyy", None))
        self.lblNote.setText(_translate("RegistrySuspenedAppointmentDialog", "Приме&чание", None))
        self.lblEndDate.setText(_translate("RegistrySuspenedAppointmentDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("RegistrySuspenedAppointmentDialog", "dd.MM.yyyy", None))
        self.lblSpeciality.setText(_translate("RegistrySuspenedAppointmentDialog", "&Специальность", None))
        self.lblPerson.setText(_translate("RegistrySuspenedAppointmentDialog", "&Врач", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RegistrySuspenedAppointmentDialog = QtGui.QDialog()
    ui = Ui_RegistrySuspenedAppointmentDialog()
    ui.setupUi(RegistrySuspenedAppointmentDialog)
    RegistrySuspenedAppointmentDialog.show()
    sys.exit(app.exec_())

