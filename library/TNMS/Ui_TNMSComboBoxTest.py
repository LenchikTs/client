# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\TNMS\TNMSComboBoxTest.ui'
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

class Ui_TestDialog(object):
    def setupUi(self, TestDialog):
        TestDialog.setObjectName(_fromUtf8("TestDialog"))
        TestDialog.resize(400, 100)
        self.gridLayout = QtGui.QGridLayout(TestDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(TestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblString = QtGui.QLabel(TestDialog)
        self.lblString.setObjectName(_fromUtf8("lblString"))
        self.gridLayout.addWidget(self.lblString, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblTNMS = QtGui.QLabel(TestDialog)
        self.lblTNMS.setObjectName(_fromUtf8("lblTNMS"))
        self.gridLayout.addWidget(self.lblTNMS, 1, 0, 1, 1)
        self.edtString = QtGui.QLineEdit(TestDialog)
        self.edtString.setObjectName(_fromUtf8("edtString"))
        self.gridLayout.addWidget(self.edtString, 0, 1, 1, 1)
        self.cmbTNMS = CTNMSComboBox(TestDialog)
        self.cmbTNMS.setObjectName(_fromUtf8("cmbTNMS"))
        self.gridLayout.addWidget(self.cmbTNMS, 1, 1, 1, 1)
        self.lblString.setBuddy(self.edtString)
        self.lblTNMS.setBuddy(self.cmbTNMS)

        self.retranslateUi(TestDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestDialog)
        TestDialog.setTabOrder(self.edtString, self.cmbTNMS)
        TestDialog.setTabOrder(self.cmbTNMS, self.buttonBox)

    def retranslateUi(self, TestDialog):
        TestDialog.setWindowTitle(_translate("TestDialog", "Испытание TNMS", None))
        self.lblString.setText(_translate("TestDialog", "Строка, как она храниться в БД", None))
        self.lblTNMS.setText(_translate("TestDialog", "Комбо-бокс TNM+S", None))

from library.TNMS.TNMSComboBox import CTNMSComboBox
