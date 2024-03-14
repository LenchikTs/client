# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\HospitalBedEditor.ui'
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

class Ui_HospitalBedEditor(object):
    def setupUi(self, HospitalBedEditor):
        HospitalBedEditor.setObjectName(_fromUtf8("HospitalBedEditor"))
        HospitalBedEditor.resize(400, 99)
        self.gridLayout = QtGui.QGridLayout(HospitalBedEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbHospitalBed = CHospitalBedFindComboBoxEditor(HospitalBedEditor)
        self.cmbHospitalBed.setEditable(True)
        self.cmbHospitalBed.setObjectName(_fromUtf8("cmbHospitalBed"))
        self.gridLayout.addWidget(self.cmbHospitalBed, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(HospitalBedEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblHospitalBed = QtGui.QLabel(HospitalBedEditor)
        self.lblHospitalBed.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHospitalBed.setObjectName(_fromUtf8("lblHospitalBed"))
        self.gridLayout.addWidget(self.lblHospitalBed, 0, 0, 1, 2)

        self.retranslateUi(HospitalBedEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HospitalBedEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HospitalBedEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(HospitalBedEditor)

    def retranslateUi(self, HospitalBedEditor):
        HospitalBedEditor.setWindowTitle(_translate("HospitalBedEditor", "Редактор койки", None))
        self.lblHospitalBed.setText(_translate("HospitalBedEditor", "Койка", None))

from HospitalBedFindComboBox import CHospitalBedFindComboBoxEditor
