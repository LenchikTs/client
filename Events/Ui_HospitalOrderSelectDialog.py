# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\HospitalOrderSelectDialog.ui'
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

class Ui_HospitalOrderSelectDialog(object):
    def setupUi(self, HospitalOrderSelectDialog):
        HospitalOrderSelectDialog.setObjectName(_fromUtf8("HospitalOrderSelectDialog"))
        HospitalOrderSelectDialog.resize(718, 510)
        self.gridLayout = QtGui.QGridLayout(HospitalOrderSelectDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(HospitalOrderSelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.btnRefresh = QtGui.QPushButton(HospitalOrderSelectDialog)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.gridLayout.addWidget(self.btnRefresh, 4, 0, 1, 1)
        self.tblCKDInformation = QtGui.QTableView(HospitalOrderSelectDialog)
        self.tblCKDInformation.setAlternatingRowColors(True)
        self.tblCKDInformation.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblCKDInformation.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblCKDInformation.setObjectName(_fromUtf8("tblCKDInformation"))
        self.tblCKDInformation.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tblCKDInformation, 3, 0, 1, 2)
        self.label_2 = QtGui.QLabel(HospitalOrderSelectDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.cmbHospitalBedProfile = CRBComboBox(HospitalOrderSelectDialog)
        self.cmbHospitalBedProfile.setObjectName(_fromUtf8("cmbHospitalBedProfile"))
        self.gridLayout.addWidget(self.cmbHospitalBedProfile, 1, 0, 1, 2)
        self.label = QtGui.QLabel(HospitalOrderSelectDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.retranslateUi(HospitalOrderSelectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HospitalOrderSelectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HospitalOrderSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HospitalOrderSelectDialog)

    def retranslateUi(self, HospitalOrderSelectDialog):
        HospitalOrderSelectDialog.setWindowTitle(_translate("HospitalOrderSelectDialog", "Выбор ЛПУ", None))
        self.btnRefresh.setText(_translate("HospitalOrderSelectDialog", "Обновить", None))
        self.label_2.setText(_translate("HospitalOrderSelectDialog", "Выбор ЛПУ", None))
        self.label.setText(_translate("HospitalOrderSelectDialog", "Профиль койки", None))

from library.crbcombobox import CRBComboBox
