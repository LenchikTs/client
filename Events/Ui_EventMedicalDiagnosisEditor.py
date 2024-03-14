# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventMedicalDiagnosisEditor.ui'
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

class Ui_EventMedicalDiagnosisEditor(object):
    def setupUi(self, EventMedicalDiagnosisEditor):
        EventMedicalDiagnosisEditor.setObjectName(_fromUtf8("EventMedicalDiagnosisEditor"))
        EventMedicalDiagnosisEditor.resize(393, 261)
        self.gridLayout = QtGui.QGridLayout(EventMedicalDiagnosisEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblLastTime = QtGui.QLabel(EventMedicalDiagnosisEditor)
        self.lblLastTime.setText(_fromUtf8(""))
        self.lblLastTime.setObjectName(_fromUtf8("lblLastTime"))
        self.gridLayout.addWidget(self.lblLastTime, 0, 1, 2, 2)
        self.edtDate = CDateEdit(EventMedicalDiagnosisEditor)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 1, 0, 1, 1)
        self.edtTime = QtGui.QTimeEdit(EventMedicalDiagnosisEditor)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.lblExecPerson = QtGui.QLabel(EventMedicalDiagnosisEditor)
        self.lblExecPerson.setObjectName(_fromUtf8("lblExecPerson"))
        self.gridLayout.addWidget(self.lblExecPerson, 2, 0, 1, 1)
        self.cmbExecPerson = CPersonComboBoxEx(EventMedicalDiagnosisEditor)
        self.cmbExecPerson.setObjectName(_fromUtf8("cmbExecPerson"))
        self.gridLayout.addWidget(self.cmbExecPerson, 2, 1, 1, 3)
        self.tblAPProps = CActionPropertiesTableView(EventMedicalDiagnosisEditor)
        self.tblAPProps.setObjectName(_fromUtf8("tblAPProps"))
        self.gridLayout.addWidget(self.tblAPProps, 3, 0, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(EventMedicalDiagnosisEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)

        self.retranslateUi(EventMedicalDiagnosisEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventMedicalDiagnosisEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventMedicalDiagnosisEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(EventMedicalDiagnosisEditor)
        EventMedicalDiagnosisEditor.setTabOrder(self.edtDate, self.cmbExecPerson)
        EventMedicalDiagnosisEditor.setTabOrder(self.cmbExecPerson, self.tblAPProps)
        EventMedicalDiagnosisEditor.setTabOrder(self.tblAPProps, self.buttonBox)

    def retranslateUi(self, EventMedicalDiagnosisEditor):
        EventMedicalDiagnosisEditor.setWindowTitle(_translate("EventMedicalDiagnosisEditor", "Диагноз", None))
        self.edtDate.setDisplayFormat(_translate("EventMedicalDiagnosisEditor", "dd.MM.yyyy", None))
        self.lblExecPerson.setText(_translate("EventMedicalDiagnosisEditor", "Исполнитель", None))

from Events.ActionPropertiesTable import CActionPropertiesTableView
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
