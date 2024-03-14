# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\CountByOms.ui'
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

class Ui_CountByOmsSetupDialog(object):
    def setupUi(self, CountByOmsSetupDialog):
        CountByOmsSetupDialog.setObjectName(_fromUtf8("CountByOmsSetupDialog"))
        CountByOmsSetupDialog.resize(400, 131)
        self.gridLayout = QtGui.QGridLayout(CountByOmsSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(CountByOmsSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 5)
        self.cmbOrganisation = CInsurerComboBox(CountByOmsSetupDialog)
        self.cmbOrganisation.setObjectName(_fromUtf8("cmbOrganisation"))
        self.gridLayout.addWidget(self.cmbOrganisation, 0, 1, 1, 4)
        self.label = QtGui.QLabel(CountByOmsSetupDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lblSMO = QtGui.QLabel(CountByOmsSetupDialog)
        self.lblSMO.setObjectName(_fromUtf8("lblSMO"))
        self.gridLayout.addWidget(self.lblSMO, 0, 0, 1, 1)
        self.cmbAttachType = CRBComboBox(CountByOmsSetupDialog)
        self.cmbAttachType.setObjectName(_fromUtf8("cmbAttachType"))
        self.gridLayout.addWidget(self.cmbAttachType, 1, 1, 1, 4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.label.setBuddy(self.cmbAttachType)
        self.lblSMO.setBuddy(self.cmbOrganisation)

        self.retranslateUi(CountByOmsSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CountByOmsSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CountByOmsSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CountByOmsSetupDialog)

    def retranslateUi(self, CountByOmsSetupDialog):
        CountByOmsSetupDialog.setWindowTitle(_translate("CountByOmsSetupDialog", "параметры отчета", None))
        self.label.setText(_translate("CountByOmsSetupDialog", "Тип прикрепления", None))
        self.lblSMO.setText(_translate("CountByOmsSetupDialog", "Организация", None))

from Orgs.OrgComboBox import CInsurerComboBox
from library.crbcombobox import CRBComboBox
