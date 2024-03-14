# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ChangeMKBEditDialog.ui'
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

class Ui_ChangeMKBEditDialog(object):
    def setupUi(self, ChangeMKBEditDialog):
        ChangeMKBEditDialog.setObjectName(_fromUtf8("ChangeMKBEditDialog"))
        ChangeMKBEditDialog.resize(226, 67)
        self.gridLayout = QtGui.QGridLayout(ChangeMKBEditDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ChangeMKBEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edtMKB = CICDCodeEditEx(ChangeMKBEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKB.sizePolicy().hasHeightForWidth())
        self.edtMKB.setSizePolicy(sizePolicy)
        self.edtMKB.setObjectName(_fromUtf8("edtMKB"))
        self.gridLayout.addWidget(self.edtMKB, 0, 1, 1, 1)
        self.edtMKBEx = CICDCodeEditEx(ChangeMKBEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBEx.sizePolicy().hasHeightForWidth())
        self.edtMKBEx.setSizePolicy(sizePolicy)
        self.edtMKBEx.setObjectName(_fromUtf8("edtMKBEx"))
        self.gridLayout.addWidget(self.edtMKBEx, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 19, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeMKBEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.label.setBuddy(self.edtMKB)

        self.retranslateUi(ChangeMKBEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChangeMKBEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChangeMKBEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeMKBEditDialog)
        ChangeMKBEditDialog.setTabOrder(self.edtMKB, self.edtMKBEx)
        ChangeMKBEditDialog.setTabOrder(self.edtMKBEx, self.buttonBox)

    def retranslateUi(self, ChangeMKBEditDialog):
        ChangeMKBEditDialog.setWindowTitle(_translate("ChangeMKBEditDialog", "Dialog", None))
        self.label.setText(_translate("ChangeMKBEditDialog", "Код МКБ", None))

from library.ICDCodeEdit import CICDCodeEditEx
