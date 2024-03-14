# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\StatusObservationClientEditor.ui'
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

class Ui_StatusObservationClientEditor(object):
    def setupUi(self, StatusObservationClientEditor):
        StatusObservationClientEditor.setObjectName(_fromUtf8("StatusObservationClientEditor"))
        StatusObservationClientEditor.resize(347, 70)
        StatusObservationClientEditor.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(StatusObservationClientEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(StatusObservationClientEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.label = QtGui.QLabel(StatusObservationClientEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbStatusObservationType = CRBComboBox(StatusObservationClientEditor)
        self.cmbStatusObservationType.setObjectName(_fromUtf8("cmbStatusObservationType"))
        self.gridLayout.addWidget(self.cmbStatusObservationType, 0, 1, 1, 1)

        self.retranslateUi(StatusObservationClientEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StatusObservationClientEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StatusObservationClientEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(StatusObservationClientEditor)

    def retranslateUi(self, StatusObservationClientEditor):
        StatusObservationClientEditor.setWindowTitle(_translate("StatusObservationClientEditor", "Статус наблюдения пациента", None))
        self.label.setText(_translate("StatusObservationClientEditor", "Статус наблюдения пациента", None))

from library.crbcombobox import CRBComboBox
