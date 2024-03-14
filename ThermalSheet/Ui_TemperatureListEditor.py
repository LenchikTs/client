# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\ThermalSheet\TemperatureListEditor.ui'
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

class Ui_TemperatureListEditor(object):
    def setupUi(self, TemperatureListEditor):
        TemperatureListEditor.setObjectName(_fromUtf8("TemperatureListEditor"))
        TemperatureListEditor.resize(437, 368)
        self.gridLayout = QtGui.QGridLayout(TemperatureListEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtDate = CDateEdit(TemperatureListEditor)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 0, 1, 1)
        self.edtTime = QtGui.QTimeEdit(TemperatureListEditor)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 0, 3, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TemperatureListEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 7)
        self.tblAPProps = CActionPropertiesTableView(TemperatureListEditor)
        self.tblAPProps.setObjectName(_fromUtf8("tblAPProps"))
        self.gridLayout.addWidget(self.tblAPProps, 2, 0, 1, 7)
        self.cmbTimeEdit = QtGui.QComboBox(TemperatureListEditor)
        self.cmbTimeEdit.setObjectName(_fromUtf8("cmbTimeEdit"))
        self.cmbTimeEdit.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTimeEdit, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 3)
        self.cmbExecPerson = CPersonComboBoxEx(TemperatureListEditor)
        self.cmbExecPerson.setObjectName(_fromUtf8("cmbExecPerson"))
        self.gridLayout.addWidget(self.cmbExecPerson, 1, 1, 1, 6)
        self.lblExecPerson = QtGui.QLabel(TemperatureListEditor)
        self.lblExecPerson.setObjectName(_fromUtf8("lblExecPerson"))
        self.gridLayout.addWidget(self.lblExecPerson, 1, 0, 1, 1)
        self.lblLastTime = QtGui.QLabel(TemperatureListEditor)
        self.lblLastTime.setText(_fromUtf8(""))
        self.lblLastTime.setObjectName(_fromUtf8("lblLastTime"))
        self.gridLayout.addWidget(self.lblLastTime, 0, 1, 1, 1)

        self.retranslateUi(TemperatureListEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TemperatureListEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TemperatureListEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TemperatureListEditor)
        TemperatureListEditor.setTabOrder(self.edtDate, self.cmbTimeEdit)
        TemperatureListEditor.setTabOrder(self.cmbTimeEdit, self.edtTime)
        TemperatureListEditor.setTabOrder(self.edtTime, self.cmbExecPerson)
        TemperatureListEditor.setTabOrder(self.cmbExecPerson, self.tblAPProps)
        TemperatureListEditor.setTabOrder(self.tblAPProps, self.buttonBox)

    def retranslateUi(self, TemperatureListEditor):
        TemperatureListEditor.setWindowTitle(_translate("TemperatureListEditor", "Редактор температурного листа", None))
        self.cmbTimeEdit.setItemText(0, _translate("TemperatureListEditor", "Время", None))
        self.lblExecPerson.setText(_translate("TemperatureListEditor", "Исполнитель", None))

from Events.ActionPropertiesTable import CActionPropertiesTableView
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
