# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\preferences\SurgeryPage.ui'
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

class Ui_SurgeryPage(object):
    def setupUi(self, SurgeryPage):
        SurgeryPage.setObjectName(_fromUtf8("SurgeryPage"))
        SurgeryPage.resize(604, 96)
        self.gridLayout = QtGui.QGridLayout(SurgeryPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.cmbRestrictFormationSurgeryPage = QtGui.QComboBox(SurgeryPage)
        self.cmbRestrictFormationSurgeryPage.setObjectName(_fromUtf8("cmbRestrictFormationSurgeryPage"))
        self.cmbRestrictFormationSurgeryPage.addItem(_fromUtf8(""))
        self.cmbRestrictFormationSurgeryPage.addItem(_fromUtf8(""))
        self.cmbRestrictFormationSurgeryPage.addItem(_fromUtf8(""))
        self.cmbRestrictFormationSurgeryPage.addItem(_fromUtf8(""))
        self.cmbRestrictFormationSurgeryPage.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbRestrictFormationSurgeryPage, 0, 1, 1, 1)
        self.lblRestrictFormationSurgeryPage = QtGui.QLabel(SurgeryPage)
        self.lblRestrictFormationSurgeryPage.setObjectName(_fromUtf8("lblRestrictFormationSurgeryPage"))
        self.gridLayout.addWidget(self.lblRestrictFormationSurgeryPage, 0, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(SurgeryPage)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(SurgeryPage)
        self.cmbOrgStructure.setEnabled(False)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 1)

        self.retranslateUi(SurgeryPage)
        QtCore.QMetaObject.connectSlotsByName(SurgeryPage)

    def retranslateUi(self, SurgeryPage):
        SurgeryPage.setWindowTitle(_translate("SurgeryPage", "Операции", None))
        self.cmbRestrictFormationSurgeryPage.setItemText(0, _translate("SurgeryPage", "Не выполнять", None))
        self.cmbRestrictFormationSurgeryPage.setItemText(1, _translate("SurgeryPage", "по пользователю", None))
        self.cmbRestrictFormationSurgeryPage.setItemText(2, _translate("SurgeryPage", "по подразделению пользователя", None))
        self.cmbRestrictFormationSurgeryPage.setItemText(3, _translate("SurgeryPage", "по подразделению из основных настроек", None))
        self.cmbRestrictFormationSurgeryPage.setItemText(4, _translate("SurgeryPage", "по фиксированному подразделению", None))
        self.lblRestrictFormationSurgeryPage.setText(_translate("SurgeryPage", "Ограничить формирование журнала операций", None))
        self.lblOrgStructure.setText(_translate("SurgeryPage", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
