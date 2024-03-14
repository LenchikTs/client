# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Resources/NextDateExecutionPlanDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_NextDateExecutionPlanDialog(object):
    def setupUi(self, NextDateExecutionPlanDialog):
        NextDateExecutionPlanDialog.setObjectName(_fromUtf8("NextDateExecutionPlanDialog"))
        NextDateExecutionPlanDialog.resize(654, 138)
        self.gridLayout_2 = QtGui.QGridLayout(NextDateExecutionPlanDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NextDateExecutionPlanDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.stwFilter = QtGui.QStackedWidget(NextDateExecutionPlanDialog)
        self.stwFilter.setObjectName(_fromUtf8("stwFilter"))
        self.tabJobTicketFilter = QtGui.QWidget()
        self.tabJobTicketFilter.setObjectName(_fromUtf8("tabJobTicketFilter"))
        self.gridLayout = QtGui.QGridLayout(self.tabJobTicketFilter)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDateJobTicket = QtGui.QLabel(self.tabJobTicketFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDateJobTicket.sizePolicy().hasHeightForWidth())
        self.lblDateJobTicket.setSizePolicy(sizePolicy)
        self.lblDateJobTicket.setObjectName(_fromUtf8("lblDateJobTicket"))
        self.gridLayout.addWidget(self.lblDateJobTicket, 2, 0, 1, 1)
        self.cmbOrgStructureJobTicket = COrgStructureComboBox(self.tabJobTicketFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructureJobTicket.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructureJobTicket.setSizePolicy(sizePolicy)
        self.cmbOrgStructureJobTicket.setObjectName(_fromUtf8("cmbOrgStructureJobTicket"))
        self.gridLayout.addWidget(self.cmbOrgStructureJobTicket, 0, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.cmbDateJobTicket = CStrComboBox(self.tabJobTicketFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbDateJobTicket.sizePolicy().hasHeightForWidth())
        self.cmbDateJobTicket.setSizePolicy(sizePolicy)
        self.cmbDateJobTicket.setObjectName(_fromUtf8("cmbDateJobTicket"))
        self.gridLayout.addWidget(self.cmbDateJobTicket, 2, 1, 1, 1)
        self.lblOrgStructureJobTicket = QtGui.QLabel(self.tabJobTicketFilter)
        self.lblOrgStructureJobTicket.setObjectName(_fromUtf8("lblOrgStructureJobTicket"))
        self.gridLayout.addWidget(self.lblOrgStructureJobTicket, 0, 0, 1, 1)
        self.edtJobTicketDays = QtGui.QSpinBox(self.tabJobTicketFilter)
        self.edtJobTicketDays.setMaximum(99999)
        self.edtJobTicketDays.setProperty("value", 30)
        self.edtJobTicketDays.setObjectName(_fromUtf8("edtJobTicketDays"))
        self.gridLayout.addWidget(self.edtJobTicketDays, 1, 1, 1, 1)
        self.lblJobTicketDays = QtGui.QLabel(self.tabJobTicketFilter)
        self.lblJobTicketDays.setObjectName(_fromUtf8("lblJobTicketDays"))
        self.gridLayout.addWidget(self.lblJobTicketDays, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 2)
        self.stwFilter.addWidget(self.tabJobTicketFilter)
        self.tabNotJobTicketFilter = QtGui.QWidget()
        self.tabNotJobTicketFilter.setObjectName(_fromUtf8("tabNotJobTicketFilter"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabNotJobTicketFilter)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.edtDateNotJobTicket = CDateEdit(self.tabNotJobTicketFilter)
        self.edtDateNotJobTicket.setCalendarPopup(True)
        self.edtDateNotJobTicket.setObjectName(_fromUtf8("edtDateNotJobTicket"))
        self.gridLayout_3.addWidget(self.edtDateNotJobTicket, 3, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 4, 3, 1, 1)
        self.lblDateNotJobTicket = QtGui.QLabel(self.tabNotJobTicketFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDateNotJobTicket.sizePolicy().hasHeightForWidth())
        self.lblDateNotJobTicket.setSizePolicy(sizePolicy)
        self.lblDateNotJobTicket.setObjectName(_fromUtf8("lblDateNotJobTicket"))
        self.gridLayout_3.addWidget(self.lblDateNotJobTicket, 3, 0, 1, 1)
        self.cmbOrgStructureNotJobTicket = COrgStructureComboBox(self.tabNotJobTicketFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructureNotJobTicket.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructureNotJobTicket.setSizePolicy(sizePolicy)
        self.cmbOrgStructureNotJobTicket.setObjectName(_fromUtf8("cmbOrgStructureNotJobTicket"))
        self.gridLayout_3.addWidget(self.cmbOrgStructureNotJobTicket, 1, 1, 1, 3)
        self.lblOrgStructureNotJobTicket = QtGui.QLabel(self.tabNotJobTicketFilter)
        self.lblOrgStructureNotJobTicket.setObjectName(_fromUtf8("lblOrgStructureNotJobTicket"))
        self.gridLayout_3.addWidget(self.lblOrgStructureNotJobTicket, 1, 0, 1, 1)
        self.lblNotJobTicketDays = QtGui.QLabel(self.tabNotJobTicketFilter)
        self.lblNotJobTicketDays.setObjectName(_fromUtf8("lblNotJobTicketDays"))
        self.gridLayout_3.addWidget(self.lblNotJobTicketDays, 2, 0, 1, 1)
        self.edtNotJobTicketDays = QtGui.QSpinBox(self.tabNotJobTicketFilter)
        self.edtNotJobTicketDays.setMaximum(99999)
        self.edtNotJobTicketDays.setProperty("value", 30)
        self.edtNotJobTicketDays.setObjectName(_fromUtf8("edtNotJobTicketDays"))
        self.gridLayout_3.addWidget(self.edtNotJobTicketDays, 2, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 2, 2, 1, 2)
        spacerItem6 = QtGui.QSpacerItem(441, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 3, 2, 1, 2)
        self.stwFilter.addWidget(self.tabNotJobTicketFilter)
        self.gridLayout_2.addWidget(self.stwFilter, 1, 0, 1, 2)

        self.retranslateUi(NextDateExecutionPlanDialog)
        self.stwFilter.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NextDateExecutionPlanDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NextDateExecutionPlanDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NextDateExecutionPlanDialog)
        NextDateExecutionPlanDialog.setTabOrder(self.cmbOrgStructureJobTicket, self.edtJobTicketDays)
        NextDateExecutionPlanDialog.setTabOrder(self.edtJobTicketDays, self.cmbDateJobTicket)
        NextDateExecutionPlanDialog.setTabOrder(self.cmbDateJobTicket, self.buttonBox)
        NextDateExecutionPlanDialog.setTabOrder(self.buttonBox, self.cmbOrgStructureNotJobTicket)
        NextDateExecutionPlanDialog.setTabOrder(self.cmbOrgStructureNotJobTicket, self.edtNotJobTicketDays)
        NextDateExecutionPlanDialog.setTabOrder(self.edtNotJobTicketDays, self.edtDateNotJobTicket)

    def retranslateUi(self, NextDateExecutionPlanDialog):
        NextDateExecutionPlanDialog.setWindowTitle(_translate("NextDateExecutionPlanDialog", "Dialog", None))
        self.lblDateJobTicket.setText(_translate("NextDateExecutionPlanDialog", "Дата", None))
        self.lblOrgStructureJobTicket.setText(_translate("NextDateExecutionPlanDialog", "Подразделение", None))
        self.lblJobTicketDays.setText(_translate("NextDateExecutionPlanDialog", "Дней", None))
        self.lblDateNotJobTicket.setText(_translate("NextDateExecutionPlanDialog", "Дата", None))
        self.lblOrgStructureNotJobTicket.setText(_translate("NextDateExecutionPlanDialog", "Подразделение", None))
        self.lblNotJobTicketDays.setText(_translate("NextDateExecutionPlanDialog", "Дней", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.StrComboBox import CStrComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NextDateExecutionPlanDialog = QtGui.QDialog()
    ui = Ui_NextDateExecutionPlanDialog()
    ui.setupUi(NextDateExecutionPlanDialog)
    NextDateExecutionPlanDialog.show()
    sys.exit(app.exec_())

