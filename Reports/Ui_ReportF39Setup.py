# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportF39Setup.ui'
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

class Ui_ReportF39SetupDialog(object):
    def setupUi(self, ReportF39SetupDialog):
        ReportF39SetupDialog.setObjectName(_fromUtf8("ReportF39SetupDialog"))
        ReportF39SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportF39SetupDialog.resize(497, 474)
        ReportF39SetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportF39SetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtBegDate = CDateEdit(ReportF39SetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.cmbRowGrouping = QtGui.QComboBox(ReportF39SetupDialog)
        self.cmbRowGrouping.setObjectName(_fromUtf8("cmbRowGrouping"))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.cmbRowGrouping.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbRowGrouping, 13, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportF39SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 19, 0, 1, 3)
        self.lblRowGrouping = QtGui.QLabel(ReportF39SetupDialog)
        self.lblRowGrouping.setObjectName(_fromUtf8("lblRowGrouping"))
        self.gridlayout.addWidget(self.lblRowGrouping, 13, 0, 1, 1)
        self.lblAge = QtGui.QLabel(ReportF39SetupDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridlayout.addWidget(self.lblAge, 12, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 18, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(ReportF39SetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridlayout.addWidget(self.lblPerson, 10, 0, 1, 1)
        self.lblSex = QtGui.QLabel(ReportF39SetupDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridlayout.addWidget(self.lblSex, 11, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportF39SetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportF39SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ReportF39SetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridlayout.addWidget(self.cmbOrgStructure, 9, 1, 1, 2)
        self.lblIsEventClosed = QtGui.QLabel(ReportF39SetupDialog)
        self.lblIsEventClosed.setObjectName(_fromUtf8("lblIsEventClosed"))
        self.gridlayout.addWidget(self.lblIsEventClosed, 16, 0, 1, 1)
        self.lblVisitPayStatus = QtGui.QLabel(ReportF39SetupDialog)
        self.lblVisitPayStatus.setObjectName(_fromUtf8("lblVisitPayStatus"))
        self.gridlayout.addWidget(self.lblVisitPayStatus, 15, 0, 1, 1)
        self.chkDetailChildren = QtGui.QCheckBox(ReportF39SetupDialog)
        self.chkDetailChildren.setObjectName(_fromUtf8("chkDetailChildren"))
        self.gridlayout.addWidget(self.chkDetailChildren, 3, 1, 1, 2)
        self.cmbEventPurpose = CRBComboBox(ReportF39SetupDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridlayout.addWidget(self.cmbEventPurpose, 5, 1, 1, 2)
        self.lblEventPurpose = QtGui.QLabel(ReportF39SetupDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridlayout.addWidget(self.lblEventPurpose, 5, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(ReportF39SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSex.sizePolicy().hasHeightForWidth())
        self.cmbSex.setSizePolicy(sizePolicy)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbSex, 11, 1, 1, 1)
        self.chkVisitHospital = QtGui.QCheckBox(ReportF39SetupDialog)
        self.chkVisitHospital.setObjectName(_fromUtf8("chkVisitHospital"))
        self.gridlayout.addWidget(self.chkVisitHospital, 4, 1, 1, 2)
        self.frmAge = QtGui.QFrame(ReportF39SetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self._2 = QtGui.QHBoxLayout(self.frmAge)
        self._2.setMargin(0)
        self._2.setSpacing(4)
        self._2.setObjectName(_fromUtf8("_2"))
        self.edtAgeFrom = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self._2.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(self.frmAge)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self._2.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self._2.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(self.frmAge)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self._2.addWidget(self.lblAgeYears)
        spacerItem3 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem3)
        self.gridlayout.addWidget(self.frmAge, 12, 1, 1, 2)
        self.cmbVisitPayStatus = QtGui.QComboBox(ReportF39SetupDialog)
        self.cmbVisitPayStatus.setObjectName(_fromUtf8("cmbVisitPayStatus"))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.cmbVisitPayStatus.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbVisitPayStatus, 15, 1, 1, 2)
        self.lblBegDate = QtGui.QLabel(ReportF39SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.cmbIsEventClosed = QtGui.QComboBox(ReportF39SetupDialog)
        self.cmbIsEventClosed.setObjectName(_fromUtf8("cmbIsEventClosed"))
        self.cmbIsEventClosed.addItem(_fromUtf8(""))
        self.cmbIsEventClosed.addItem(_fromUtf8(""))
        self.cmbIsEventClosed.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbIsEventClosed, 16, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(ReportF39SetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridlayout.addWidget(self.lblOrgStructure, 9, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportF39SetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.cmbPerson.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbPerson, 10, 1, 1, 2)
        self.lblScene = QtGui.QLabel(ReportF39SetupDialog)
        self.lblScene.setObjectName(_fromUtf8("lblScene"))
        self.gridlayout.addWidget(self.lblScene, 8, 0, 1, 1)
        self.cmbScene = CRBComboBox(ReportF39SetupDialog)
        self.cmbScene.setObjectName(_fromUtf8("cmbScene"))
        self.gridlayout.addWidget(self.cmbScene, 8, 1, 1, 2)
        self.lblFinance = QtGui.QLabel(ReportF39SetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridlayout.addWidget(self.lblFinance, 14, 0, 1, 1)
        self.cmbFinance = CRBComboBox(ReportF39SetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridlayout.addWidget(self.cmbFinance, 14, 1, 1, 2)
        self.btnEventTypeList = QtGui.QPushButton(ReportF39SetupDialog)
        self.btnEventTypeList.setObjectName(_fromUtf8("btnEventTypeList"))
        self.gridlayout.addWidget(self.btnEventTypeList, 6, 0, 1, 1)
        self.lblEventTypeList = QtGui.QLabel(ReportF39SetupDialog)
        self.lblEventTypeList.setWordWrap(True)
        self.lblEventTypeList.setObjectName(_fromUtf8("lblEventTypeList"))
        self.gridlayout.addWidget(self.lblEventTypeList, 6, 1, 1, 2)
        self.lblVisitType = QtGui.QLabel(ReportF39SetupDialog)
        self.lblVisitType.setObjectName(_fromUtf8("lblVisitType"))
        self.gridlayout.addWidget(self.lblVisitType, 2, 0, 1, 1)
        self.cmbVisitType = CRBComboBox(ReportF39SetupDialog)
        self.cmbVisitType.setObjectName(_fromUtf8("cmbVisitType"))
        self.gridlayout.addWidget(self.cmbVisitType, 2, 1, 1, 2)
        self.lblAddressType = QtGui.QLabel(ReportF39SetupDialog)
        self.lblAddressType.setObjectName(_fromUtf8("lblAddressType"))
        self.gridlayout.addWidget(self.lblAddressType, 17, 0, 1, 1)
        self.cmbAddressType = QtGui.QComboBox(ReportF39SetupDialog)
        self.cmbAddressType.setObjectName(_fromUtf8("cmbAddressType"))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.cmbAddressType.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbAddressType, 17, 1, 1, 2)
        self.lblRowGrouping.setBuddy(self.cmbRowGrouping)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventPurpose.setBuddy(self.cmbEventPurpose)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(ReportF39SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportF39SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportF39SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportF39SetupDialog)
        ReportF39SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportF39SetupDialog.setTabOrder(self.edtEndDate, self.cmbVisitType)
        ReportF39SetupDialog.setTabOrder(self.cmbVisitType, self.chkDetailChildren)
        ReportF39SetupDialog.setTabOrder(self.chkDetailChildren, self.chkVisitHospital)
        ReportF39SetupDialog.setTabOrder(self.chkVisitHospital, self.cmbEventPurpose)
        ReportF39SetupDialog.setTabOrder(self.cmbEventPurpose, self.btnEventTypeList)
        ReportF39SetupDialog.setTabOrder(self.btnEventTypeList, self.cmbScene)
        ReportF39SetupDialog.setTabOrder(self.cmbScene, self.cmbOrgStructure)
        ReportF39SetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        ReportF39SetupDialog.setTabOrder(self.cmbPerson, self.cmbSex)
        ReportF39SetupDialog.setTabOrder(self.cmbSex, self.edtAgeFrom)
        ReportF39SetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        ReportF39SetupDialog.setTabOrder(self.edtAgeTo, self.cmbRowGrouping)
        ReportF39SetupDialog.setTabOrder(self.cmbRowGrouping, self.cmbVisitPayStatus)
        ReportF39SetupDialog.setTabOrder(self.cmbVisitPayStatus, self.cmbIsEventClosed)
        ReportF39SetupDialog.setTabOrder(self.cmbIsEventClosed, self.buttonBox)
        ReportF39SetupDialog.setTabOrder(self.buttonBox, self.cmbFinance)

    def retranslateUi(self, ReportF39SetupDialog):
        ReportF39SetupDialog.setWindowTitle(_translate("ReportF39SetupDialog", "параметры отчёта", None))
        self.cmbRowGrouping.setItemText(0, _translate("ReportF39SetupDialog", "Датам", None))
        self.cmbRowGrouping.setItemText(1, _translate("ReportF39SetupDialog", "Месяцам", None))
        self.cmbRowGrouping.setItemText(2, _translate("ReportF39SetupDialog", "Врачам", None))
        self.cmbRowGrouping.setItemText(3, _translate("ReportF39SetupDialog", "Подразделениям", None))
        self.cmbRowGrouping.setItemText(4, _translate("ReportF39SetupDialog", "Специальности", None))
        self.cmbRowGrouping.setItemText(5, _translate("ReportF39SetupDialog", "Должности", None))
        self.lblRowGrouping.setText(_translate("ReportF39SetupDialog", "&Строки по", None))
        self.lblAge.setText(_translate("ReportF39SetupDialog", "Во&зраст с", None))
        self.lblPerson.setText(_translate("ReportF39SetupDialog", "&Врач", None))
        self.lblSex.setText(_translate("ReportF39SetupDialog", "По&л", None))
        self.lblEndDate.setText(_translate("ReportF39SetupDialog", "Дата &окончания периода", None))
        self.lblIsEventClosed.setText(_translate("ReportF39SetupDialog", "Закрытие события", None))
        self.lblVisitPayStatus.setText(_translate("ReportF39SetupDialog", "Флаг финансирования", None))
        self.chkDetailChildren.setText(_translate("ReportF39SetupDialog", "Детализация по подросткам", None))
        self.lblEventPurpose.setText(_translate("ReportF39SetupDialog", "&Назначение обращения", None))
        self.cmbSex.setItemText(1, _translate("ReportF39SetupDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("ReportF39SetupDialog", "Ж", None))
        self.chkVisitHospital.setText(_translate("ReportF39SetupDialog", "Учитывать посещения ДС", None))
        self.lblAgeTo.setText(_translate("ReportF39SetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("ReportF39SetupDialog", "лет", None))
        self.cmbVisitPayStatus.setItemText(0, _translate("ReportF39SetupDialog", "не задано", None))
        self.cmbVisitPayStatus.setItemText(1, _translate("ReportF39SetupDialog", "не выставлено", None))
        self.cmbVisitPayStatus.setItemText(2, _translate("ReportF39SetupDialog", "выставлено", None))
        self.cmbVisitPayStatus.setItemText(3, _translate("ReportF39SetupDialog", "отказано", None))
        self.cmbVisitPayStatus.setItemText(4, _translate("ReportF39SetupDialog", "оплачено", None))
        self.lblBegDate.setText(_translate("ReportF39SetupDialog", "Дата &начала периода", None))
        self.cmbIsEventClosed.setItemText(0, _translate("ReportF39SetupDialog", "не учитывать", None))
        self.cmbIsEventClosed.setItemText(1, _translate("ReportF39SetupDialog", "только завершённые", None))
        self.cmbIsEventClosed.setItemText(2, _translate("ReportF39SetupDialog", "только незавершённые", None))
        self.lblOrgStructure.setText(_translate("ReportF39SetupDialog", "&Подразделение", None))
        self.cmbPerson.setItemText(0, _translate("ReportF39SetupDialog", "Врач", None))
        self.lblScene.setText(_translate("ReportF39SetupDialog", "&Место посещения", None))
        self.lblFinance.setText(_translate("ReportF39SetupDialog", "Тип финансирования", None))
        self.btnEventTypeList.setText(_translate("ReportF39SetupDialog", "Тип обращения", None))
        self.lblEventTypeList.setText(_translate("ReportF39SetupDialog", "Не задано", None))
        self.lblVisitType.setText(_translate("ReportF39SetupDialog", "Тип визита", None))
        self.lblAddressType.setText(_translate("ReportF39SetupDialog", "Местность", None))
        self.cmbAddressType.setItemText(0, _translate("ReportF39SetupDialog", "не учитывать", None))
        self.cmbAddressType.setItemText(1, _translate("ReportF39SetupDialog", "городские", None))
        self.cmbAddressType.setItemText(2, _translate("ReportF39SetupDialog", "сельские", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportF39SetupDialog = QtGui.QDialog()
    ui = Ui_ReportF39SetupDialog()
    ui.setupUi(ReportF39SetupDialog)
    ReportF39SetupDialog.show()
    sys.exit(app.exec_())
