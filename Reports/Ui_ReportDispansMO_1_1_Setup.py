# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportDispansMO_1_1_Setup.ui'
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

class Ui_ReportDispansMO_1_1_SetupDialog(object):
    def setupUi(self, ReportDispansMO_1_1_SetupDialog):
        ReportDispansMO_1_1_SetupDialog.setObjectName(_fromUtf8("ReportDispansMO_1_1_SetupDialog"))
        ReportDispansMO_1_1_SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportDispansMO_1_1_SetupDialog.resize(465, 128)
        ReportDispansMO_1_1_SetupDialog.setSizeGripEnabled(True)
        ReportDispansMO_1_1_SetupDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ReportDispansMO_1_1_SetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(ReportDispansMO_1_1_SetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportDispansMO_1_1_SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportDispansMO_1_1_SetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportDispansMO_1_1_SetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.lblFilterContingentType = QtGui.QLabel(ReportDispansMO_1_1_SetupDialog)
        self.lblFilterContingentType.setObjectName(_fromUtf8("lblFilterContingentType"))
        self.gridLayout.addWidget(self.lblFilterContingentType, 2, 0, 1, 1)
        self.cmbFilterContingentType = CRBComboBox(ReportDispansMO_1_1_SetupDialog)
        self.cmbFilterContingentType.setObjectName(_fromUtf8("cmbFilterContingentType"))
        self.gridLayout.addWidget(self.cmbFilterContingentType, 2, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(428, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ReportDispansMO_1_1_SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ReportDispansMO_1_1_SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportDispansMO_1_1_SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportDispansMO_1_1_SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportDispansMO_1_1_SetupDialog)
        ReportDispansMO_1_1_SetupDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportDispansMO_1_1_SetupDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ReportDispansMO_1_1_SetupDialog):
        ReportDispansMO_1_1_SetupDialog.setWindowTitle(_translate("ReportDispansMO_1_1_SetupDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ReportDispansMO_1_1_SetupDialog", "Дата &начала периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportDispansMO_1_1_SetupDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ReportDispansMO_1_1_SetupDialog", "Дата &окончания периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportDispansMO_1_1_SetupDialog", "dd.MM.yyyy", None))
        self.lblFilterContingentType.setText(_translate("ReportDispansMO_1_1_SetupDialog", "Тип контингента", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
