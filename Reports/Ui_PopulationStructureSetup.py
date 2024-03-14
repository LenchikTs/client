# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Reports/PopulationStructureSetup.ui'
#
# Created: Wed Sep 19 16:44:10 2018
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_PopulationStructureSetupDialog(object):
    def setupUi(self, PopulationStructureSetupDialog):
        PopulationStructureSetupDialog.setObjectName(_fromUtf8("PopulationStructureSetupDialog"))
        PopulationStructureSetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PopulationStructureSetupDialog.resize(409, 182)
        PopulationStructureSetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(PopulationStructureSetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblEndDate = QtGui.QLabel(PopulationStructureSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(PopulationStructureSetupDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblAge = QtGui.QLabel(PopulationStructureSetupDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridlayout.addWidget(self.lblAge, 1, 0, 1, 1)
        self.frmAge = QtGui.QFrame(PopulationStructureSetupDialog)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.edtAgeFrom = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeFrom.sizePolicy().hasHeightForWidth())
        self.edtAgeFrom.setSizePolicy(sizePolicy)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.hboxlayout.addWidget(self.edtAgeFrom)
        self.lblAgeTo = QtGui.QLabel(self.frmAge)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.hboxlayout.addWidget(self.lblAgeTo)
        self.edtAgeTo = QtGui.QSpinBox(self.frmAge)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAgeTo.sizePolicy().hasHeightForWidth())
        self.edtAgeTo.setSizePolicy(sizePolicy)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.hboxlayout.addWidget(self.edtAgeTo)
        self.lblAgeYears = QtGui.QLabel(self.frmAge)
        self.lblAgeYears.setObjectName(_fromUtf8("lblAgeYears"))
        self.hboxlayout.addWidget(self.lblAgeYears)
        spacerItem1 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridlayout.addWidget(self.frmAge, 1, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(PopulationStructureSetupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridlayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(PopulationStructureSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridlayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(80, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PopulationStructureSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 6, 0, 1, 3)
        self.lblAddressOrgStructureType = QtGui.QLabel(PopulationStructureSetupDialog)
        self.lblAddressOrgStructureType.setObjectName(_fromUtf8("lblAddressOrgStructureType"))
        self.gridlayout.addWidget(self.lblAddressOrgStructureType, 3, 0, 2, 1)
        self.cmbAddressOrgStructureType = QtGui.QComboBox(PopulationStructureSetupDialog)
        self.cmbAddressOrgStructureType.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAddressOrgStructureType.sizePolicy().hasHeightForWidth())
        self.cmbAddressOrgStructureType.setSizePolicy(sizePolicy)
        self.cmbAddressOrgStructureType.setObjectName(_fromUtf8("cmbAddressOrgStructureType"))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.cmbAddressOrgStructureType.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbAddressOrgStructureType, 3, 1, 1, 2)
        self.chkServiceAreaDetail = QtGui.QCheckBox(PopulationStructureSetupDialog)
        self.chkServiceAreaDetail.setObjectName(_fromUtf8("chkServiceAreaDetail"))
        self.gridlayout.addWidget(self.chkServiceAreaDetail, 4, 1, 1, 2)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblAge.setBuddy(self.edtAgeFrom)
        self.lblAgeTo.setBuddy(self.edtAgeTo)
        self.lblAgeYears.setBuddy(self.edtAgeTo)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblAddressOrgStructureType.setBuddy(self.cmbAddressOrgStructureType)

        self.retranslateUi(PopulationStructureSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PopulationStructureSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PopulationStructureSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PopulationStructureSetupDialog)
        PopulationStructureSetupDialog.setTabOrder(self.edtEndDate, self.edtAgeFrom)
        PopulationStructureSetupDialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        PopulationStructureSetupDialog.setTabOrder(self.edtAgeTo, self.cmbOrgStructure)
        PopulationStructureSetupDialog.setTabOrder(self.cmbOrgStructure, self.cmbAddressOrgStructureType)
        PopulationStructureSetupDialog.setTabOrder(self.cmbAddressOrgStructureType, self.buttonBox)

    def retranslateUi(self, PopulationStructureSetupDialog):
        PopulationStructureSetupDialog.setWindowTitle(_translate("PopulationStructureSetupDialog", "параметры отчёта", None))
        self.lblEndDate.setText(_translate("PopulationStructureSetupDialog", "&Дата", None))
        self.lblAge.setText(_translate("PopulationStructureSetupDialog", "Во&зраст с", None))
        self.lblAgeTo.setText(_translate("PopulationStructureSetupDialog", "по", None))
        self.lblAgeYears.setText(_translate("PopulationStructureSetupDialog", "лет", None))
        self.lblOrgStructure.setText(_translate("PopulationStructureSetupDialog", "&Подразделение", None))
        self.lblAddressOrgStructureType.setText(_translate("PopulationStructureSetupDialog", "Адрес", None))
        self.cmbAddressOrgStructureType.setItemText(0, _translate("PopulationStructureSetupDialog", "Регистрация", None))
        self.cmbAddressOrgStructureType.setItemText(1, _translate("PopulationStructureSetupDialog", "Проживание", None))
        self.cmbAddressOrgStructureType.setItemText(2, _translate("PopulationStructureSetupDialog", "Регистрация или проживание", None))
        self.cmbAddressOrgStructureType.setItemText(3, _translate("PopulationStructureSetupDialog", "Прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(4, _translate("PopulationStructureSetupDialog", "Регистрация или прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(5, _translate("PopulationStructureSetupDialog", "Проживание или прикрепление", None))
        self.cmbAddressOrgStructureType.setItemText(6, _translate("PopulationStructureSetupDialog", "Регистрация, проживание или прикрепление", None))
        self.chkServiceAreaDetail.setText(_translate("PopulationStructureSetupDialog", "Детализация по Зоне обслуживания", None))

from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import COrgStructureComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PopulationStructureSetupDialog = QtGui.QDialog()
    ui = Ui_PopulationStructureSetupDialog()
    ui.setupUi(PopulationStructureSetupDialog)
    PopulationStructureSetupDialog.show()
    sys.exit(app.exec_())

