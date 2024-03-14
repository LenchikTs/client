# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\GroupJobTicketsManipulationsDialog.ui'
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

class Ui_GroupJobTicketsManipulationsDialog(object):
    def setupUi(self, GroupJobTicketsManipulationsDialog):
        GroupJobTicketsManipulationsDialog.setObjectName(_fromUtf8("GroupJobTicketsManipulationsDialog"))
        GroupJobTicketsManipulationsDialog.resize(465, 295)
        self.gridLayout = QtGui.QGridLayout(GroupJobTicketsManipulationsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(GroupJobTicketsManipulationsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 2)
        self.calendar = CCalendarWidget(GroupJobTicketsManipulationsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setGridVisible(False)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.gridLayout.addWidget(self.calendar, 3, 0, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(GroupJobTicketsManipulationsDialog)
        self.cmbOrgStructure.setEnabled(True)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 0, 2, 3)

        self.retranslateUi(GroupJobTicketsManipulationsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GroupJobTicketsManipulationsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GroupJobTicketsManipulationsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GroupJobTicketsManipulationsDialog)

    def retranslateUi(self, GroupJobTicketsManipulationsDialog):
        GroupJobTicketsManipulationsDialog.setWindowTitle(_translate("GroupJobTicketsManipulationsDialog", "Dialog", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.CalendarWidget import CCalendarWidget
