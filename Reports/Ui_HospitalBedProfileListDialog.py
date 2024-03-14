# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\HospitalBedProfileListDialog.ui'
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

class Ui_HospitalBedProfileListDialog(object):
    def setupUi(self, HospitalBedProfileListDialog):
        HospitalBedProfileListDialog.setObjectName(_fromUtf8("HospitalBedProfileListDialog"))
        HospitalBedProfileListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(HospitalBedProfileListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblHospitalBedProfileList = CTableView(HospitalBedProfileListDialog)
        self.tblHospitalBedProfileList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblHospitalBedProfileList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblHospitalBedProfileList.setObjectName(_fromUtf8("tblHospitalBedProfileList"))
        self.gridLayout.addWidget(self.tblHospitalBedProfileList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(HospitalBedProfileListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(HospitalBedProfileListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HospitalBedProfileListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HospitalBedProfileListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HospitalBedProfileListDialog)

    def retranslateUi(self, HospitalBedProfileListDialog):
        HospitalBedProfileListDialog.setWindowTitle(_translate("HospitalBedProfileListDialog", "Профили коек", None))

from library.TableView import CTableView
