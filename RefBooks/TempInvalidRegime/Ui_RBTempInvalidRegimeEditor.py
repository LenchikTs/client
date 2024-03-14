# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_vipisnoy\RefBooks\TempInvalidRegime\RBTempInvalidRegimeEditor.ui'
#
# Created: Thu Sep 24 15:27:24 2020
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_RBTempInvalidRegimeEditorDialog(object):
    def setupUi(self, RBTempInvalidRegimeEditorDialog):
        RBTempInvalidRegimeEditorDialog.setObjectName(_fromUtf8("RBTempInvalidRegimeEditorDialog"))
        RBTempInvalidRegimeEditorDialog.resize(320, 122)
        RBTempInvalidRegimeEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBTempInvalidRegimeEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblType = QtGui.QLabel(RBTempInvalidRegimeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblType.sizePolicy().hasHeightForWidth())
        self.lblType.setSizePolicy(sizePolicy)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 0, 0, 1, 1)
        self.lblCode = QtGui.QLabel(RBTempInvalidRegimeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBTempInvalidRegimeEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 1, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(RBTempInvalidRegimeEditorDialog)
        self.edtName.setMinimumSize(QtCore.QSize(200, 0))
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 71, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.lblName = QtGui.QLabel(RBTempInvalidRegimeEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.cmbType = QtGui.QComboBox(RBTempInvalidRegimeEditorDialog)
        self.cmbType.setObjectName(_fromUtf8("cmbType"))
        self.gridLayout.addWidget(self.cmbType, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBTempInvalidRegimeEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblType.setBuddy(self.cmbType)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBTempInvalidRegimeEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBTempInvalidRegimeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBTempInvalidRegimeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBTempInvalidRegimeEditorDialog)
        RBTempInvalidRegimeEditorDialog.setTabOrder(self.cmbType, self.edtCode)
        RBTempInvalidRegimeEditorDialog.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, RBTempInvalidRegimeEditorDialog):
        RBTempInvalidRegimeEditorDialog.setWindowTitle(_translate("RBTempInvalidRegimeEditorDialog", "ChangeMe!", None))
        self.lblType.setText(_translate("RBTempInvalidRegimeEditorDialog", "Кла&сс", None))
        self.lblCode.setText(_translate("RBTempInvalidRegimeEditorDialog", "&Код", None))
        self.lblName.setText(_translate("RBTempInvalidRegimeEditorDialog", "На&именование", None))

