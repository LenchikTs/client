# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_DN\Surveillance\SurveillanceRemovedDialog.ui'
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

class Ui_SurveillanceRemovedDialog(object):
    def setupUi(self, SurveillanceRemovedDialog):
        SurveillanceRemovedDialog.setObjectName(_fromUtf8("SurveillanceRemovedDialog"))
        SurveillanceRemovedDialog.resize(377, 122)
        self.gridLayout = QtGui.QGridLayout(SurveillanceRemovedDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pnlDateTime = QtGui.QWidget(SurveillanceRemovedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlDateTime.sizePolicy().hasHeightForWidth())
        self.pnlDateTime.setSizePolicy(sizePolicy)
        self.pnlDateTime.setObjectName(_fromUtf8("pnlDateTime"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.pnlDateTime)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addWidget(self.pnlDateTime, 0, 1, 1, 1)
        self.lblRemoveReason = QtGui.QLabel(SurveillanceRemovedDialog)
        self.lblRemoveReason.setObjectName(_fromUtf8("lblRemoveReason"))
        self.gridLayout.addWidget(self.lblRemoveReason, 3, 0, 1, 1)
        self.lblDispanser = QtGui.QLabel(SurveillanceRemovedDialog)
        self.lblDispanser.setObjectName(_fromUtf8("lblDispanser"))
        self.gridLayout.addWidget(self.lblDispanser, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.edtRemoveReasonDate = CDateEdit(SurveillanceRemovedDialog)
        self.edtRemoveReasonDate.setCalendarPopup(True)
        self.edtRemoveReasonDate.setObjectName(_fromUtf8("edtRemoveReasonDate"))
        self.gridLayout.addWidget(self.edtRemoveReasonDate, 2, 1, 1, 1)
        self.lblRemoveReasonDate = QtGui.QLabel(SurveillanceRemovedDialog)
        self.lblRemoveReasonDate.setObjectName(_fromUtf8("lblRemoveReasonDate"))
        self.gridLayout.addWidget(self.lblRemoveReasonDate, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.cmbDispanser = CRBComboBox(SurveillanceRemovedDialog)
        self.cmbDispanser.setObjectName(_fromUtf8("cmbDispanser"))
        self.gridLayout.addWidget(self.cmbDispanser, 1, 1, 1, 2)
        self.cmbRemoveReason = CRBComboBox(SurveillanceRemovedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbRemoveReason.sizePolicy().hasHeightForWidth())
        self.cmbRemoveReason.setSizePolicy(sizePolicy)
        self.cmbRemoveReason.setObjectName(_fromUtf8("cmbRemoveReason"))
        self.gridLayout.addWidget(self.cmbRemoveReason, 3, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(SurveillanceRemovedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)

        self.retranslateUi(SurveillanceRemovedDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SurveillanceRemovedDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SurveillanceRemovedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SurveillanceRemovedDialog)
        SurveillanceRemovedDialog.setTabOrder(self.cmbDispanser, self.edtRemoveReasonDate)
        SurveillanceRemovedDialog.setTabOrder(self.edtRemoveReasonDate, self.cmbRemoveReason)
        SurveillanceRemovedDialog.setTabOrder(self.cmbRemoveReason, self.buttonBox)

    def retranslateUi(self, SurveillanceRemovedDialog):
        SurveillanceRemovedDialog.setWindowTitle(_translate("SurveillanceRemovedDialog", "Dialog", None))
        self.lblRemoveReason.setText(_translate("SurveillanceRemovedDialog", "Причина снятия", None))
        self.lblDispanser.setText(_translate("SurveillanceRemovedDialog", "Диспансерное наблюдение", None))
        self.lblRemoveReasonDate.setText(_translate("SurveillanceRemovedDialog", "Дата снятия", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
