# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\AbsenceDialog.ui'
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

class Ui_AbsenceDialog(object):
    def setupUi(self, AbsenceDialog):
        AbsenceDialog.setObjectName(_fromUtf8("AbsenceDialog"))
        AbsenceDialog.resize(294, 117)
        self.gridLayout = QtGui.QGridLayout(AbsenceDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblReasonOfAbsence = QtGui.QLabel(AbsenceDialog)
        self.lblReasonOfAbsence.setAlignment(QtCore.Qt.AlignCenter)
        self.lblReasonOfAbsence.setObjectName(_fromUtf8("lblReasonOfAbsence"))
        self.gridLayout.addWidget(self.lblReasonOfAbsence, 2, 0, 1, 2)
        self.edtBegDate = CDateEdit(AbsenceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.lblEndDate = QtGui.QLabel(AbsenceDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(AbsenceDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(AbsenceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)
        self.cmbReasonOfAbsence = CRBComboBox(AbsenceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbReasonOfAbsence.sizePolicy().hasHeightForWidth())
        self.cmbReasonOfAbsence.setSizePolicy(sizePolicy)
        self.cmbReasonOfAbsence.setObjectName(_fromUtf8("cmbReasonOfAbsence"))
        self.gridLayout.addWidget(self.cmbReasonOfAbsence, 2, 2, 1, 4)
        self.chkFillRedDays = QtGui.QCheckBox(AbsenceDialog)
        self.chkFillRedDays.setChecked(True)
        self.chkFillRedDays.setObjectName(_fromUtf8("chkFillRedDays"))
        self.gridLayout.addWidget(self.chkFillRedDays, 1, 2, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(AbsenceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 6)
        self.lblReasonOfAbsence.setBuddy(self.cmbReasonOfAbsence)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(AbsenceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AbsenceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AbsenceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AbsenceDialog)
        AbsenceDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        AbsenceDialog.setTabOrder(self.edtEndDate, self.chkFillRedDays)
        AbsenceDialog.setTabOrder(self.chkFillRedDays, self.cmbReasonOfAbsence)

    def retranslateUi(self, AbsenceDialog):
        AbsenceDialog.setWindowTitle(_translate("AbsenceDialog", "Причина отсутствия", None))
        self.lblReasonOfAbsence.setText(_translate("AbsenceDialog", "Причина &отсутствия", None))
        self.lblEndDate.setText(_translate("AbsenceDialog", "&по", None))
        self.lblBegDate.setText(_translate("AbsenceDialog", "В период &с", None))
        self.chkFillRedDays.setText(_translate("AbsenceDialog", "&Заполнять выходные дни", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
