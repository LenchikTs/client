# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\InputDialog.ui'
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

class Ui_InputDialog(object):
    def setupUi(self, InputDialog):
        InputDialog.setObjectName(_fromUtf8("InputDialog"))
        InputDialog.resize(545, 115)
        self.gridLayout = QtGui.QGridLayout(InputDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPerson = QtGui.QLabel(InputDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 1, 0, 1, 1)
        self.lblDateTime = QtGui.QLabel(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDateTime.sizePolicy().hasHeightForWidth())
        self.lblDateTime.setSizePolicy(sizePolicy)
        self.lblDateTime.setObjectName(_fromUtf8("lblDateTime"))
        self.gridLayout.addWidget(self.lblDateTime, 0, 0, 1, 1)
        self.pnlDateTime = QtGui.QWidget(InputDialog)
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
        self.cmbPresetDateTime = QtGui.QComboBox(self.pnlDateTime)
        self.cmbPresetDateTime.setObjectName(_fromUtf8("cmbPresetDateTime"))
        self.horizontalLayout.addWidget(self.cmbPresetDateTime)
        self.edtDate = CDateEdit(self.pnlDateTime)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.horizontalLayout.addWidget(self.edtDate)
        self.edtTime = QtGui.QTimeEdit(self.pnlDateTime)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.horizontalLayout.addWidget(self.edtTime)
        self.gridLayout.addWidget(self.pnlDateTime, 0, 1, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(InputDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbPerson.sizePolicy().hasHeightForWidth())
        self.cmbPerson.setSizePolicy(sizePolicy)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.cmbOrgStructure = COrgStructureComboBox(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)

        self.retranslateUi(InputDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InputDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InputDialog)
        InputDialog.setTabOrder(self.cmbPresetDateTime, self.edtDate)
        InputDialog.setTabOrder(self.edtDate, self.edtTime)
        InputDialog.setTabOrder(self.edtTime, self.cmbPerson)
        InputDialog.setTabOrder(self.cmbPerson, self.cmbOrgStructure)
        InputDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, InputDialog):
        InputDialog.setWindowTitle(_translate("InputDialog", "Dialog", None))
        self.lblPerson.setText(_translate("InputDialog", "Врач", None))
        self.lblDateTime.setText(_translate("InputDialog", "Дата и время", None))
        self.lblOrgStructure.setText(_translate("InputDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
