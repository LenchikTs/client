# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\RefBooks\ToxicSubstances\RBToxicSubstancesEditor.ui'
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

class Ui_RBToxicSubstancesEditor(object):
    def setupUi(self, RBToxicSubstancesEditor):
        RBToxicSubstancesEditor.setObjectName(_fromUtf8("RBToxicSubstancesEditor"))
        RBToxicSubstancesEditor.resize(320, 180)
        RBToxicSubstancesEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBToxicSubstancesEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtName = QtGui.QLineEdit(RBToxicSubstancesEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtCode = QtGui.QLineEdit(RBToxicSubstancesEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBToxicSubstancesEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.lblMKB = QtGui.QLabel(RBToxicSubstancesEditor)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 5, 0, 1, 1)
        self.lblName = QtGui.QLabel(RBToxicSubstancesEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 2, 1, 1)
        self.lblCode = QtGui.QLabel(RBToxicSubstancesEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.cmbMKB = CICDCodeEditEx(RBToxicSubstancesEditor)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.gridLayout.addWidget(self.cmbMKB, 5, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBToxicSubstancesEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBToxicSubstancesEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBToxicSubstancesEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBToxicSubstancesEditor)
        RBToxicSubstancesEditor.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, RBToxicSubstancesEditor):
        RBToxicSubstancesEditor.setWindowTitle(_translate("RBToxicSubstancesEditor", "Dialog", None))
        self.lblMKB.setText(_translate("RBToxicSubstancesEditor", "Диагноз", None))
        self.lblName.setText(_translate("RBToxicSubstancesEditor", "Наименование", None))
        self.lblCode.setText(_translate("RBToxicSubstancesEditor", "Код", None))

from library.ICDCodeEdit import CICDCodeEditEx
