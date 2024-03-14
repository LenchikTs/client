# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Reports/DailyJournalBeforeRecordSetup.ui'
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

class Ui_DailyJournalBeforeRecordSetup(object):
    def setupUi(self, DailyJournalBeforeRecordSetup):
        DailyJournalBeforeRecordSetup.setObjectName(_fromUtf8("DailyJournalBeforeRecordSetup"))
        DailyJournalBeforeRecordSetup.setWindowModality(QtCore.Qt.ApplicationModal)
        DailyJournalBeforeRecordSetup.resize(508, 344)
        DailyJournalBeforeRecordSetup.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DailyJournalBeforeRecordSetup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblOrgStructure = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 2)
        self.lblUserProfile = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblUserProfile.setObjectName(_fromUtf8("lblUserProfile"))
        self.gridLayout.addWidget(self.lblUserProfile, 5, 0, 1, 2)
        self.lblRowCount = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblRowCount.setObjectName(_fromUtf8("lblRowCount"))
        self.gridLayout.addWidget(self.lblRowCount, 8, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 14, 1, 1, 1)
        self.lblOrderSorting = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblOrderSorting.setObjectName(_fromUtf8("lblOrderSorting"))
        self.gridLayout.addWidget(self.lblOrderSorting, 6, 0, 1, 2)
        self.lblBegDate = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.edtBegDate = CDateEdit(DailyJournalBeforeRecordSetup)
        self.edtBegDate.setEnabled(True)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(DailyJournalBeforeRecordSetup)
        self.cmbOrgStructure.setEnabled(True)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 2, 1, 3)
        self.lblPerson = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 4, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(DailyJournalBeforeRecordSetup)
        self.cmbPerson.setEnabled(True)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 4, 2, 1, 3)
        self.cmbOrder = QtGui.QComboBox(DailyJournalBeforeRecordSetup)
        self.cmbOrder.setObjectName(_fromUtf8("cmbOrder"))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.cmbOrder.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrder, 6, 2, 1, 3)
        self.cmbAccountingSystem = CRBComboBox(DailyJournalBeforeRecordSetup)
        self.cmbAccountingSystem.setObjectName(_fromUtf8("cmbAccountingSystem"))
        self.gridLayout.addWidget(self.cmbAccountingSystem, 5, 2, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.lblIsPrimary = QtGui.QLabel(DailyJournalBeforeRecordSetup)
        self.lblIsPrimary.setObjectName(_fromUtf8("lblIsPrimary"))
        self.gridLayout.addWidget(self.lblIsPrimary, 7, 0, 1, 2)
        self.cmbIsPrimary = QtGui.QComboBox(DailyJournalBeforeRecordSetup)
        self.cmbIsPrimary.setObjectName(_fromUtf8("cmbIsPrimary"))
        self.cmbIsPrimary.addItem(_fromUtf8(""))
        self.cmbIsPrimary.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbIsPrimary, 7, 2, 1, 3)
        self.spnRowCount = QtGui.QSpinBox(DailyJournalBeforeRecordSetup)
        self.spnRowCount.setObjectName(_fromUtf8("spnRowCount"))
        self.gridLayout.addWidget(self.spnRowCount, 8, 2, 1, 3)
        self.chkShowEmptyItems = QtGui.QCheckBox(DailyJournalBeforeRecordSetup)
        self.chkShowEmptyItems.setObjectName(_fromUtf8("chkShowEmptyItems"))
        self.gridLayout.addWidget(self.chkShowEmptyItems, 9, 2, 1, 3)
        self.chkTablePerPage = QtGui.QCheckBox(DailyJournalBeforeRecordSetup)
        self.chkTablePerPage.setChecked(True)
        self.chkTablePerPage.setObjectName(_fromUtf8("chkTablePerPage"))
        self.gridLayout.addWidget(self.chkTablePerPage, 10, 2, 1, 3)
        self.chkOutputNotScheduled = QtGui.QCheckBox(DailyJournalBeforeRecordSetup)
        self.chkOutputNotScheduled.setObjectName(_fromUtf8("chkOutputNotScheduled"))
        self.gridLayout.addWidget(self.chkOutputNotScheduled, 11, 2, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(DailyJournalBeforeRecordSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 15, 0, 1, 5)
        self.chkClientIdentifier = QtGui.QCheckBox(DailyJournalBeforeRecordSetup)
        self.chkClientIdentifier.setObjectName(_fromUtf8("chkClientIdentifier"))
        self.gridLayout.addWidget(self.chkClientIdentifier, 12, 2, 1, 2)
        self.chkFirstEntryPatient = QtGui.QCheckBox(DailyJournalBeforeRecordSetup)
        self.chkFirstEntryPatient.setObjectName(_fromUtf8("chkFirstEntryPatient"))
        self.gridLayout.addWidget(self.chkFirstEntryPatient, 13, 2, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(DailyJournalBeforeRecordSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DailyJournalBeforeRecordSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DailyJournalBeforeRecordSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(DailyJournalBeforeRecordSetup)
        DailyJournalBeforeRecordSetup.setTabOrder(self.edtBegDate, self.cmbOrgStructure)
        DailyJournalBeforeRecordSetup.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        DailyJournalBeforeRecordSetup.setTabOrder(self.cmbPerson, self.cmbAccountingSystem)
        DailyJournalBeforeRecordSetup.setTabOrder(self.cmbAccountingSystem, self.cmbOrder)
        DailyJournalBeforeRecordSetup.setTabOrder(self.cmbOrder, self.cmbIsPrimary)
        DailyJournalBeforeRecordSetup.setTabOrder(self.cmbIsPrimary, self.spnRowCount)
        DailyJournalBeforeRecordSetup.setTabOrder(self.spnRowCount, self.chkShowEmptyItems)
        DailyJournalBeforeRecordSetup.setTabOrder(self.chkShowEmptyItems, self.chkTablePerPage)
        DailyJournalBeforeRecordSetup.setTabOrder(self.chkTablePerPage, self.chkOutputNotScheduled)
        DailyJournalBeforeRecordSetup.setTabOrder(self.chkOutputNotScheduled, self.chkClientIdentifier)
        DailyJournalBeforeRecordSetup.setTabOrder(self.chkClientIdentifier, self.chkFirstEntryPatient)
        DailyJournalBeforeRecordSetup.setTabOrder(self.chkFirstEntryPatient, self.buttonBox)

    def retranslateUi(self, DailyJournalBeforeRecordSetup):
        DailyJournalBeforeRecordSetup.setWindowTitle(_translate("DailyJournalBeforeRecordSetup", "Суточный журнал предварительной записи", None))
        self.lblOrgStructure.setText(_translate("DailyJournalBeforeRecordSetup", "Подразделение", None))
        self.lblUserProfile.setText(_translate("DailyJournalBeforeRecordSetup", "Тип идентификатора пациента", None))
        self.lblRowCount.setText(_translate("DailyJournalBeforeRecordSetup", "Количество строк на лист", None))
        self.lblOrderSorting.setText(_translate("DailyJournalBeforeRecordSetup", "Порядок сортировки", None))
        self.lblBegDate.setText(_translate("DailyJournalBeforeRecordSetup", "Дата", None))
        self.lblPerson.setText(_translate("DailyJournalBeforeRecordSetup", "&Врач", None))
        self.cmbOrder.setItemText(0, _translate("DailyJournalBeforeRecordSetup", "по идентификатору", None))
        self.cmbOrder.setItemText(1, _translate("DailyJournalBeforeRecordSetup", "по времени", None))
        self.cmbOrder.setItemText(2, _translate("DailyJournalBeforeRecordSetup", "по ФИО", None))
        self.lblIsPrimary.setText(_translate("DailyJournalBeforeRecordSetup", "Первичные", None))
        self.cmbIsPrimary.setItemText(0, _translate("DailyJournalBeforeRecordSetup", "Нет", None))
        self.cmbIsPrimary.setItemText(1, _translate("DailyJournalBeforeRecordSetup", "Да", None))
        self.chkShowEmptyItems.setText(_translate("DailyJournalBeforeRecordSetup", "Выводить свободное время", None))
        self.chkTablePerPage.setText(_translate("DailyJournalBeforeRecordSetup", "Выводить с начала листа", None))
        self.chkOutputNotScheduled.setText(_translate("DailyJournalBeforeRecordSetup", "Выводить пустые графики", None))
        self.chkClientIdentifier.setText(_translate("DailyJournalBeforeRecordSetup", "Учитывать Тип идентификатора пациента", None))
        self.chkFirstEntryPatient.setText(_translate("DailyJournalBeforeRecordSetup", "Отмечать первую запись пациента", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DailyJournalBeforeRecordSetup = QtGui.QDialog()
    ui = Ui_DailyJournalBeforeRecordSetup()
    ui.setupUi(DailyJournalBeforeRecordSetup)
    DailyJournalBeforeRecordSetup.show()
    sys.exit(app.exec_())

