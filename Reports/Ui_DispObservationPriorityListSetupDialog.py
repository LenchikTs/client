# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Reports\DispObservationPriorityListSetupDialog.ui'
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

class Ui_DispObservationPriorityListSetupDialog(object):
    def setupUi(self, DispObservationPriorityListSetupDialog):
        DispObservationPriorityListSetupDialog.setObjectName(_fromUtf8("DispObservationPriorityListSetupDialog"))
        DispObservationPriorityListSetupDialog.resize(536, 138)
        self.gridLayout = QtGui.QGridLayout(DispObservationPriorityListSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDate = QtGui.QLabel(DispObservationPriorityListSetupDialog)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.edtDate = CDateEdit(DispObservationPriorityListSetupDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(DispObservationPriorityListSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(DispObservationPriorityListSetupDialog)
        self.cmbOrgStructure.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DispObservationPriorityListSetupDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)

        self.retranslateUi(DispObservationPriorityListSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DispObservationPriorityListSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DispObservationPriorityListSetupDialog)

    def retranslateUi(self, DispObservationPriorityListSetupDialog):
        DispObservationPriorityListSetupDialog.setWindowTitle(_translate("DispObservationPriorityListSetupDialog", "Параметры", None))
        self.lblDate.setText(_translate("DispObservationPriorityListSetupDialog", "Начало периода", None))
        self.lblOrgStructure.setText(_translate("DispObservationPriorityListSetupDialog", "Прикрепление", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
