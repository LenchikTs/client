# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\PlacementEditor.ui'
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

class Ui_PlacementEditor(object):
    def setupUi(self, PlacementEditor):
        PlacementEditor.setObjectName(_fromUtf8("PlacementEditor"))
        PlacementEditor.resize(400, 88)
        self.gridLayout = QtGui.QGridLayout(PlacementEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbPlacement = CRBComboBox(PlacementEditor)
        self.cmbPlacement.setEditable(True)
        self.cmbPlacement.setObjectName(_fromUtf8("cmbPlacement"))
        self.gridLayout.addWidget(self.cmbPlacement, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(PlacementEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblHospitalBed = QtGui.QLabel(PlacementEditor)
        self.lblHospitalBed.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblHospitalBed.setObjectName(_fromUtf8("lblHospitalBed"))
        self.gridLayout.addWidget(self.lblHospitalBed, 0, 0, 1, 2)

        self.retranslateUi(PlacementEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PlacementEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PlacementEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(PlacementEditor)

    def retranslateUi(self, PlacementEditor):
        PlacementEditor.setWindowTitle(_translate("PlacementEditor", "Редактор помещения", None))
        self.lblHospitalBed.setText(_translate("PlacementEditor", "Помещение", None))

from library.crbcombobox import CRBComboBox
