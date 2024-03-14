# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\InputDialog.ui'
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
        InputDialog.resize(377, 173)
        self.gridLayout = QtGui.QGridLayout(InputDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.edtDate = CCurrentDateEditEx(self.pnlDateTime)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.horizontalLayout.addWidget(self.edtDate)
        self.edtTime = QtGui.QTimeEdit(self.pnlDateTime)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.horizontalLayout.addWidget(self.edtTime)
        self.gridLayout.addWidget(self.pnlDateTime, 0, 1, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(InputDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 4, 1, 1, 1)
        self.cmbExecPerson = CPersonComboBoxEx(InputDialog)
        self.cmbExecPerson.setObjectName(_fromUtf8("cmbExecPerson"))
        self.gridLayout.addWidget(self.cmbExecPerson, 3, 1, 1, 1)
        self.lblExecPerson = QtGui.QLabel(InputDialog)
        self.lblExecPerson.setObjectName(_fromUtf8("lblExecPerson"))
        self.gridLayout.addWidget(self.lblExecPerson, 3, 0, 1, 1)
        self.lblDateTime = QtGui.QLabel(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDateTime.sizePolicy().hasHeightForWidth())
        self.lblDateTime.setSizePolicy(sizePolicy)
        self.lblDateTime.setObjectName(_fromUtf8("lblDateTime"))
        self.gridLayout.addWidget(self.lblDateTime, 0, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(InputDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.cmbPerson = CPersonComboBoxEx(InputDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbPerson.sizePolicy().hasHeightForWidth())
        self.cmbPerson.setSizePolicy(sizePolicy)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 1)
        self.lblCourse = QtGui.QLabel(InputDialog)
        self.lblCourse.setObjectName(_fromUtf8("lblCourse"))
        self.gridLayout.addWidget(self.lblCourse, 1, 0, 1, 1)
        self.cmbCourse = CCourseStatusComboBox(InputDialog)
        self.cmbCourse.setObjectName(_fromUtf8("cmbCourse"))
        self.gridLayout.addWidget(self.cmbCourse, 1, 1, 1, 1)

        self.retranslateUi(InputDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InputDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InputDialog)
        InputDialog.setTabOrder(self.cmbPresetDateTime, self.edtDate)
        InputDialog.setTabOrder(self.edtDate, self.edtTime)
        InputDialog.setTabOrder(self.edtTime, self.cmbCourse)
        InputDialog.setTabOrder(self.cmbCourse, self.cmbPerson)
        InputDialog.setTabOrder(self.cmbPerson, self.cmbExecPerson)
        InputDialog.setTabOrder(self.cmbExecPerson, self.cmbOrgStructure)
        InputDialog.setTabOrder(self.cmbOrgStructure, self.buttonBox)

    def retranslateUi(self, InputDialog):
        InputDialog.setWindowTitle(_translate("InputDialog", "Dialog", None))
        self.lblOrgStructure.setText(_translate("InputDialog", "Подразделение", None))
        self.lblExecPerson.setText(_translate("InputDialog", "Лечащий врач", None))
        self.lblDateTime.setText(_translate("InputDialog", "Дата и время", None))
        self.lblPerson.setText(_translate("InputDialog", "Переводящий врач", None))
        self.lblCourse.setText(_translate("InputDialog", "Курс", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Resources.CourseStatus import CCourseStatusComboBox
from library.DateEdit import CCurrentDateEditEx
