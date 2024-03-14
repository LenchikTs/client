# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\Reports\Ds14kkSetupDialog.ui'
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

class Ui_ds14kkSetupDialog(object):
    def setupUi(self, ds14kkSetupDialog):
        ds14kkSetupDialog.setObjectName(_fromUtf8("ds14kkSetupDialog"))
        ds14kkSetupDialog.resize(472, 229)
        self.gridLayout = QtGui.QGridLayout(ds14kkSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblFinance = QtGui.QLabel(ds14kkSetupDialog)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 3, 0, 1, 1)
        self.cmbFinance = CRBComboBox(ds14kkSetupDialog)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 3, 2, 1, 3)
        self.cbPermanent = QtGui.QCheckBox(ds14kkSetupDialog)
        self.cbPermanent.setObjectName(_fromUtf8("cbPermanent"))
        self.gridLayout.addWidget(self.cbPermanent, 4, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(134, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ds14kkSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(134, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(ds14kkSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(ds14kkSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 2, 1, 3)
        self.lblBegDate = QtGui.QLabel(ds14kkSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ds14kkSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtBegDate = CDateTimeEdit(ds14kkSetupDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.edtEndDate = CDateTimeEdit(ds14kkSetupDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 2, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(ds14kkSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ds14kkSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ds14kkSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ds14kkSetupDialog)

    def retranslateUi(self, ds14kkSetupDialog):
        ds14kkSetupDialog.setWindowTitle(_translate("ds14kkSetupDialog", "параметры отчёта", None))
        self.lblFinance.setText(_translate("ds14kkSetupDialog", "Тип финансирования", None))
        self.cbPermanent.setText(_translate("ds14kkSetupDialog", "Учитывать внештатные койки", None))
        self.lblOrgStructure.setText(_translate("ds14kkSetupDialog", "&Подразделение", None))
        self.lblBegDate.setText(_translate("ds14kkSetupDialog", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("ds14kkSetupDialog", "Дата &окончания периода", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateTimeEdit import CDateTimeEdit
from library.crbcombobox import CRBComboBox
