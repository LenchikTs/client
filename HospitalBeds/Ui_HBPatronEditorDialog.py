# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\HBPatronEditorDialog.ui'
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

class Ui_HBPatronEditorDialog(object):
    def setupUi(self, HBPatronEditorDialog):
        HBPatronEditorDialog.setObjectName(_fromUtf8("HBPatronEditorDialog"))
        HBPatronEditorDialog.resize(400, 99)
        self.gridLayout = QtGui.QGridLayout(HBPatronEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbPatron = CClientRelationComboBoxPatron(HBPatronEditorDialog)
        self.cmbPatron.setEditable(True)
        self.cmbPatron.setObjectName(_fromUtf8("cmbPatron"))
        self.gridLayout.addWidget(self.cmbPatron, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(HBPatronEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblHospitalBed = QtGui.QLabel(HBPatronEditorDialog)
        self.lblHospitalBed.setAlignment(QtCore.Qt.AlignCenter)
        self.lblHospitalBed.setObjectName(_fromUtf8("lblHospitalBed"))
        self.gridLayout.addWidget(self.lblHospitalBed, 0, 0, 1, 2)

        self.retranslateUi(HBPatronEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HBPatronEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HBPatronEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HBPatronEditorDialog)

    def retranslateUi(self, HBPatronEditorDialog):
        HBPatronEditorDialog.setWindowTitle(_translate("HBPatronEditorDialog", "Выбор лица по уходу", None))
        self.lblHospitalBed.setText(_translate("HBPatronEditorDialog", "Лицо по уходу", None))

from Registry.Utils import CClientRelationComboBoxPatron
