# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_DN\Surveillance\ChangeDispanserPerson.ui'
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

class Ui_ChangeDispanserPerson(object):
    def setupUi(self, ChangeDispanserPerson):
        ChangeDispanserPerson.setObjectName(_fromUtf8("ChangeDispanserPerson"))
        ChangeDispanserPerson.resize(395, 88)
        self.gridLayout = QtGui.QGridLayout(ChangeDispanserPerson)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPerson = QtGui.QLabel(ChangeDispanserPerson)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 0, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ChangeDispanserPerson)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeDispanserPerson)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 2)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(ChangeDispanserPerson)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChangeDispanserPerson.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChangeDispanserPerson.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeDispanserPerson)

    def retranslateUi(self, ChangeDispanserPerson):
        ChangeDispanserPerson.setWindowTitle(_translate("ChangeDispanserPerson", "Изменение врача по ДН", None))
        self.lblPerson.setText(_translate("ChangeDispanserPerson", "Врач по ДН", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
