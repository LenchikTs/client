# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\CSG\CSGComboBoxTest.ui'
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
        TestDialog.resize(400, 364)
        self.gridLayout = QtGui.QGridLayout(TestDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAge = QtGui.QLabel(TestDialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 1, 0, 1, 1)
        self.edtAge = QtGui.QSpinBox(TestDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAge.sizePolicy().hasHeightForWidth())
        self.edtAge.setSizePolicy(sizePolicy)
        self.edtAge.setMaximum(150)
        self.edtAge.setObjectName(_fromUtf8("edtAge"))
        self.gridLayout.addWidget(self.edtAge, 1, 1, 1, 1)
        self.lblMKB = QtGui.QLabel(TestDialog)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 3, 0, 1, 1)
        self.edtMKB = CICDCodeEditEx(TestDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKB.sizePolicy().hasHeightForWidth())
        self.edtMKB.setSizePolicy(sizePolicy)
        self.edtMKB.setObjectName(_fromUtf8("edtMKB"))
        self.gridLayout.addWidget(self.edtMKB, 3, 1, 1, 1)
        self.lblMES = QtGui.QLabel(TestDialog)
        self.lblMES.setObjectName(_fromUtf8("lblMES"))
        self.gridLayout.addWidget(self.lblMES, 4, 0, 1, 1)
        self.cmbCSG = CCSGComboBox(TestDialog)
        self.cmbCSG.setObjectName(_fromUtf8("cmbCSG"))
        self.gridLayout.addWidget(self.cmbCSG, 4, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 131, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(TestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.lblSex = QtGui.QLabel(TestDialog)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 0, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(TestDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSex.sizePolicy().hasHeightForWidth())
        self.cmbSex.setSizePolicy(sizePolicy)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 0, 1, 1, 1)
        self.lblAge.setBuddy(self.edtAge)
        self.lblMKB.setBuddy(self.edtMKB)
        self.lblMES.setBuddy(self.cmbCSG)
        self.lblSex.setBuddy(self.cmbSex)

        self.retranslateUi(TestDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestDialog)
        TestDialog.setTabOrder(self.cmbSex, self.edtAge)
        TestDialog.setTabOrder(self.edtAge, self.edtMKB)
        TestDialog.setTabOrder(self.edtMKB, self.cmbCSG)
        TestDialog.setTabOrder(self.cmbCSG, self.buttonBox)

    def retranslateUi(self, TestDialog):
        TestDialog.setWindowTitle(_translate("TestDialog", "Испытание КСГ", None))
        self.lblAge.setText(_translate("TestDialog", "&Возраст пациента", None))
        self.lblMKB.setText(_translate("TestDialog", "Код &диагноза", None))
        self.lblMES.setText(_translate("TestDialog", "С&тандарт", None))
        self.lblSex.setText(_translate("TestDialog", "&Пол пациента", None))
        self.cmbSex.setItemText(1, _translate("TestDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("TestDialog", "Ж", None))

from library.CSG.CSGComboBox import CCSGComboBox
from library.ICDCodeEdit import CICDCodeEditEx
