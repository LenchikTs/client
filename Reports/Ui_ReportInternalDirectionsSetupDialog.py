# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Reports\ReportInternalDirectionsSetupDialog.ui'
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

class Ui_ReportInternalDirectionsSetupDialog(object):
    def setupUi(self, ReportInternalDirectionsSetupDialog):
        ReportInternalDirectionsSetupDialog.setObjectName(_fromUtf8("ReportInternalDirectionsSetupDialog"))
        ReportInternalDirectionsSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportInternalDirectionsSetupDialog.resize(404, 286)
        ReportInternalDirectionsSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportInternalDirectionsSetupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPerson = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 6, 0, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 5, 0, 1, 2)
        self.edtEndDate = CDateEdit(ReportInternalDirectionsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 2)
        self.cmbPerson = CPersonComboBox(ReportInternalDirectionsSetupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 6, 2, 1, 3)
        self.edtBegTime = QtGui.QTimeEdit(ReportInternalDirectionsSetupDialog)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        self.lblJobType = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblJobType.setText(_fromUtf8(""))
        self.lblJobType.setWordWrap(True)
        self.lblJobType.setObjectName(_fromUtf8("lblJobType"))
        self.gridLayout.addWidget(self.lblJobType, 3, 2, 1, 3)
        self.edtBegDate = CDateEdit(ReportInternalDirectionsSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportInternalDirectionsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 5)
        self.cmbOrgStructure = COrgStructureComboBox(ReportInternalDirectionsSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 5, 2, 1, 3)
        self.cmbActionType = QtGui.QComboBox(ReportInternalDirectionsSetupDialog)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 2, 2, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(ReportInternalDirectionsSetupDialog)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(21, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 9, 1, 1, 1)
        self.lblActionType = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblActionType.setObjectName(_fromUtf8("lblActionType"))
        self.gridLayout.addWidget(self.lblActionType, 2, 0, 1, 2)
        self.cmbActionStatus = CActionStatusComboBox(ReportInternalDirectionsSetupDialog)
        self.cmbActionStatus.setObjectName(_fromUtf8("cmbActionStatus"))
        self.gridLayout.addWidget(self.cmbActionStatus, 4, 2, 1, 3)
        self.lblActionStatus = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblActionStatus.setObjectName(_fromUtf8("lblActionStatus"))
        self.gridLayout.addWidget(self.lblActionStatus, 4, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportInternalDirectionsSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 2)
        self.btnJobType = QtGui.QPushButton(ReportInternalDirectionsSetupDialog)
        self.btnJobType.setObjectName(_fromUtf8("btnJobType"))
        self.gridLayout.addWidget(self.btnJobType, 3, 0, 1, 2)
        self.chkJobType = QtGui.QCheckBox(ReportInternalDirectionsSetupDialog)
        self.chkJobType.setObjectName(_fromUtf8("chkJobType"))
        self.gridLayout.addWidget(self.chkJobType, 7, 2, 1, 3)
        self.chkFIO = QtGui.QCheckBox(ReportInternalDirectionsSetupDialog)
        self.chkFIO.setObjectName(_fromUtf8("chkFIO"))
        self.gridLayout.addWidget(self.chkFIO, 8, 2, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportInternalDirectionsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportInternalDirectionsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportInternalDirectionsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportInternalDirectionsSetupDialog)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.edtBegDate, self.edtBegTime)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.edtBegTime, self.edtEndDate)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.edtEndDate, self.edtEndTime)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.edtEndTime, self.cmbActionType)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.cmbActionType, self.btnJobType)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.btnJobType, self.cmbActionStatus)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.cmbActionStatus, self.cmbOrgStructure)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.cmbPerson, self.chkJobType)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.chkJobType, self.chkFIO)
        ReportInternalDirectionsSetupDialog.setTabOrder(self.chkFIO, self.buttonBox)

    def retranslateUi(self, ReportInternalDirectionsSetupDialog):
        ReportInternalDirectionsSetupDialog.setWindowTitle(_translate("ReportInternalDirectionsSetupDialog", "параметры отчёта", None))
        self.lblPerson.setText(_translate("ReportInternalDirectionsSetupDialog", "Направитель", None))
        self.lblOrgStructure.setText(_translate("ReportInternalDirectionsSetupDialog", "Подразделение", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportInternalDirectionsSetupDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ReportInternalDirectionsSetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportInternalDirectionsSetupDialog", "dd.MM.yyyy", None))
        self.lblActionType.setText(_translate("ReportInternalDirectionsSetupDialog", "Тип направления", None))
        self.lblActionStatus.setText(_translate("ReportInternalDirectionsSetupDialog", "Состояние", None))
        self.lblEndDate.setText(_translate("ReportInternalDirectionsSetupDialog", "Дата &окончания периода", None))
        self.btnJobType.setText(_translate("ReportInternalDirectionsSetupDialog", "Типы работ", None))
        self.chkJobType.setText(_translate("ReportInternalDirectionsSetupDialog", "Детализация по типам работ", None))
        self.chkFIO.setText(_translate("ReportInternalDirectionsSetupDialog", "Детализация по ФИО пациентов", None))

from Events.ActionStatus import CActionStatusComboBox
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBox import CPersonComboBox
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportInternalDirectionsSetupDialog = QtGui.QDialog()
    ui = Ui_ReportInternalDirectionsSetupDialog()
    ui.setupUi(ReportInternalDirectionsSetupDialog)
    ReportInternalDirectionsSetupDialog.show()
    sys.exit(app.exec_())

