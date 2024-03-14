# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\Events\ExecuteActionParamsDialog.ui'
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

class Ui_ExecuteActionParamsDialog(object):
    def setupUi(self, ExecuteActionParamsDialog):
        ExecuteActionParamsDialog.setObjectName(_fromUtf8("ExecuteActionParamsDialog"))
        ExecuteActionParamsDialog.resize(377, 118)
        self.gridLayout = QtGui.QGridLayout(ExecuteActionParamsDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pnlDateTime = QtGui.QWidget(ExecuteActionParamsDialog)
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
        self.edtDate = CCurrentDateEditEx(self.pnlDateTime)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.horizontalLayout.addWidget(self.edtDate)
        self.gridLayout.addWidget(self.pnlDateTime, 0, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(ExecuteActionParamsDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.lblDateTime = QtGui.QLabel(ExecuteActionParamsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDateTime.sizePolicy().hasHeightForWidth())
        self.lblDateTime.setSizePolicy(sizePolicy)
        self.lblDateTime.setObjectName(_fromUtf8("lblDateTime"))
        self.gridLayout.addWidget(self.lblDateTime, 0, 0, 1, 1)
        self.cmbCourse = CCourseStatusComboBox(ExecuteActionParamsDialog)
        self.cmbCourse.setObjectName(_fromUtf8("cmbCourse"))
        self.gridLayout.addWidget(self.cmbCourse, 1, 1, 1, 3)
        self.cmbPerson = CPersonComboBoxEx(ExecuteActionParamsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbPerson.sizePolicy().hasHeightForWidth())
        self.cmbPerson.setSizePolicy(sizePolicy)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 3)
        self.lblCourse = QtGui.QLabel(ExecuteActionParamsDialog)
        self.lblCourse.setObjectName(_fromUtf8("lblCourse"))
        self.gridLayout.addWidget(self.lblCourse, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.edtTime = CTimeEdit(ExecuteActionParamsDialog)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ExecuteActionParamsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)

        self.retranslateUi(ExecuteActionParamsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExecuteActionParamsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExecuteActionParamsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExecuteActionParamsDialog)
        ExecuteActionParamsDialog.setTabOrder(self.edtDate, self.edtTime)
        ExecuteActionParamsDialog.setTabOrder(self.edtTime, self.cmbCourse)
        ExecuteActionParamsDialog.setTabOrder(self.cmbCourse, self.cmbPerson)
        ExecuteActionParamsDialog.setTabOrder(self.cmbPerson, self.buttonBox)

    def retranslateUi(self, ExecuteActionParamsDialog):
        ExecuteActionParamsDialog.setWindowTitle(_translate("ExecuteActionParamsDialog", "Параметры", None))
        self.lblPerson.setText(_translate("ExecuteActionParamsDialog", "Исполнитель", None))
        self.lblDateTime.setText(_translate("ExecuteActionParamsDialog", "Время выполнения", None))
        self.lblCourse.setText(_translate("ExecuteActionParamsDialog", "Курс", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Resources.CourseStatus import CCourseStatusComboBox
from library.DateEdit import CCurrentDateEditEx
from library.TimeEdit import CTimeEdit
