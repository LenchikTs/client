# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportMovingAndBedsSetupDialog.ui'
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

class Ui_ReportMovingAndBedsSetupDialog(object):
    def setupUi(self, ReportMovingAndBedsSetupDialog):
        ReportMovingAndBedsSetupDialog.setObjectName(_fromUtf8("ReportMovingAndBedsSetupDialog"))
        ReportMovingAndBedsSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportMovingAndBedsSetupDialog.resize(587, 411)
        ReportMovingAndBedsSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportMovingAndBedsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ReportMovingAndBedsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 14, 0, 1, 4)
        self.chkIsGroupingOS = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkIsGroupingOS.setObjectName(_fromUtf8("chkIsGroupingOS"))
        self.gridLayout.addWidget(self.chkIsGroupingOS, 10, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 13, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportMovingAndBedsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportMovingAndBedsSetupDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblOrgStructureList = QtGui.QLabel(ReportMovingAndBedsSetupDialog)
        self.lblOrgStructureList.setWordWrap(True)
        self.lblOrgStructureList.setObjectName(_fromUtf8("lblOrgStructureList"))
        self.gridLayout.addWidget(self.lblOrgStructureList, 2, 1, 1, 3)
        self.chkNoProfileBed = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkNoProfileBed.setChecked(True)
        self.chkNoProfileBed.setObjectName(_fromUtf8("chkNoProfileBed"))
        self.gridLayout.addWidget(self.chkNoProfileBed, 6, 1, 1, 3)
        self.edtEndDate = CDateEdit(ReportMovingAndBedsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.chkFinance = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkFinance.setEnabled(True)
        self.chkFinance.setCheckable(True)
        self.chkFinance.setObjectName(_fromUtf8("chkFinance"))
        self.gridLayout.addWidget(self.chkFinance, 11, 0, 1, 1)
        self.edtTimeEdit = QtGui.QTimeEdit(ReportMovingAndBedsSetupDialog)
        self.edtTimeEdit.setObjectName(_fromUtf8("edtTimeEdit"))
        self.gridLayout.addWidget(self.edtTimeEdit, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.chkIsPermanentBed = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkIsPermanentBed.setObjectName(_fromUtf8("chkIsPermanentBed"))
        self.gridLayout.addWidget(self.chkIsPermanentBed, 7, 1, 1, 3)
        self.lblEndDate = QtGui.QLabel(ReportMovingAndBedsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(ReportMovingAndBedsSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 2, 1, 1)
        self.chkNoPrintCaption = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkNoPrintCaption.setChecked(True)
        self.chkNoPrintCaption.setObjectName(_fromUtf8("chkNoPrintCaption"))
        self.gridLayout.addWidget(self.chkNoPrintCaption, 8, 1, 1, 3)
        self.cmbFinance = CCheckableComboBox(ReportMovingAndBedsSetupDialog)
        self.cmbFinance.setEnabled(False)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 11, 1, 1, 3)
        self.chkNoPrintFilterParameters = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkNoPrintFilterParameters.setObjectName(_fromUtf8("chkNoPrintFilterParameters"))
        self.gridLayout.addWidget(self.chkNoPrintFilterParameters, 9, 1, 1, 3)
        self.btnOrgStructureList = QtGui.QPushButton(ReportMovingAndBedsSetupDialog)
        self.btnOrgStructureList.setObjectName(_fromUtf8("btnOrgStructureList"))
        self.gridLayout.addWidget(self.btnOrgStructureList, 2, 0, 1, 1)
        self.lblHospitalBedProfileList = QtGui.QLabel(ReportMovingAndBedsSetupDialog)
        self.lblHospitalBedProfileList.setWordWrap(True)
        self.lblHospitalBedProfileList.setObjectName(_fromUtf8("lblHospitalBedProfileList"))
        self.gridLayout.addWidget(self.lblHospitalBedProfileList, 4, 1, 1, 3)
        self.btnHospitalBedProfileList = QtGui.QPushButton(ReportMovingAndBedsSetupDialog)
        self.btnHospitalBedProfileList.setObjectName(_fromUtf8("btnHospitalBedProfileList"))
        self.gridLayout.addWidget(self.btnHospitalBedProfileList, 4, 0, 1, 1)
        self.lblSchedule = QtGui.QLabel(ReportMovingAndBedsSetupDialog)
        self.lblSchedule.setObjectName(_fromUtf8("lblSchedule"))
        self.gridLayout.addWidget(self.lblSchedule, 5, 0, 1, 1)
        self.cmbSchedule = QtGui.QComboBox(ReportMovingAndBedsSetupDialog)
        self.cmbSchedule.setObjectName(_fromUtf8("cmbSchedule"))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.cmbSchedule.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSchedule, 5, 1, 1, 3)
        self.chkTableHeaderOnlyFirstPage = QtGui.QCheckBox(ReportMovingAndBedsSetupDialog)
        self.chkTableHeaderOnlyFirstPage.setObjectName(_fromUtf8("chkTableHeaderOnlyFirstPage"))
        self.gridLayout.addWidget(self.chkTableHeaderOnlyFirstPage, 12, 0, 1, 4)

        self.retranslateUi(ReportMovingAndBedsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportMovingAndBedsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportMovingAndBedsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportMovingAndBedsSetupDialog)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.edtEndDate, self.edtTimeEdit)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.edtTimeEdit, self.btnOrgStructureList)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.btnOrgStructureList, self.btnHospitalBedProfileList)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.btnHospitalBedProfileList, self.cmbSchedule)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.cmbSchedule, self.chkNoProfileBed)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkNoProfileBed, self.chkIsPermanentBed)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkIsPermanentBed, self.chkNoPrintCaption)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkNoPrintCaption, self.chkNoPrintFilterParameters)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkNoPrintFilterParameters, self.chkIsGroupingOS)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkIsGroupingOS, self.chkFinance)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.chkFinance, self.cmbFinance)
        ReportMovingAndBedsSetupDialog.setTabOrder(self.cmbFinance, self.buttonBox)

    def retranslateUi(self, ReportMovingAndBedsSetupDialog):
        ReportMovingAndBedsSetupDialog.setWindowTitle(_translate("ReportMovingAndBedsSetupDialog", "параметры отчёта", None))
        self.chkIsGroupingOS.setText(_translate("ReportMovingAndBedsSetupDialog", "Группировка по подразделениям", None))
        self.lblBegDate.setText(_translate("ReportMovingAndBedsSetupDialog", "Дата начала", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportMovingAndBedsSetupDialog", "dd.MM.yyyy", None))
        self.lblOrgStructureList.setText(_translate("ReportMovingAndBedsSetupDialog", " ЛПУ", None))
        self.chkNoProfileBed.setText(_translate("ReportMovingAndBedsSetupDialog", "Учитывать койки без профиля", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportMovingAndBedsSetupDialog", "dd.MM.yyyy", None))
        self.chkFinance.setText(_translate("ReportMovingAndBedsSetupDialog", "Тип финансирования", None))
        self.chkIsPermanentBed.setText(_translate("ReportMovingAndBedsSetupDialog", "Добавить внештатные койки в коечный фонд", None))
        self.lblEndDate.setText(_translate("ReportMovingAndBedsSetupDialog", "Текущий день", None))
        self.chkNoPrintCaption.setText(_translate("ReportMovingAndBedsSetupDialog", "Не печатать заголовок отчета", None))
        self.chkNoPrintFilterParameters.setText(_translate("ReportMovingAndBedsSetupDialog", "Не печатать параметры фильтра", None))
        self.btnOrgStructureList.setText(_translate("ReportMovingAndBedsSetupDialog", "Подразделение", None))
        self.lblHospitalBedProfileList.setText(_translate("ReportMovingAndBedsSetupDialog", " не задано", None))
        self.btnHospitalBedProfileList.setText(_translate("ReportMovingAndBedsSetupDialog", "Профиль койки", None))
        self.lblSchedule.setText(_translate("ReportMovingAndBedsSetupDialog", "Режим койки", None))
        self.cmbSchedule.setItemText(0, _translate("ReportMovingAndBedsSetupDialog", "Не учитывать", None))
        self.cmbSchedule.setItemText(1, _translate("ReportMovingAndBedsSetupDialog", "Круглосуточные", None))
        self.cmbSchedule.setItemText(2, _translate("ReportMovingAndBedsSetupDialog", "Не круглосуточные", None))
        self.chkTableHeaderOnlyFirstPage.setText(_translate("ReportMovingAndBedsSetupDialog", "Заголовок таблицы только на первом листе", None))

from Reports.Utils import CCheckableComboBox
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportMovingAndBedsSetupDialog = QtGui.QDialog()
    ui = Ui_ReportMovingAndBedsSetupDialog()
    ui.setupUi(ReportMovingAndBedsSetupDialog)
    ReportMovingAndBedsSetupDialog.show()
    sys.exit(app.exec_())

