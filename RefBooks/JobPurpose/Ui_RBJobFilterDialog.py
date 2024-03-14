# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\RefBooks\JobPurpose\RBJobFilterDialog.ui'
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

class Ui_RBJobFilterDialog(object):
    def setupUi(self, RBJobFilterDialog):
        RBJobFilterDialog.setObjectName(_fromUtf8("RBJobFilterDialog"))
        RBJobFilterDialog.resize(412, 96)
        self.gridlayout = QtGui.QGridLayout(RBJobFilterDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(RBJobFilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.lbCode = QtGui.QLabel(RBJobFilterDialog)
        self.lbCode.setObjectName(_fromUtf8("lbCode"))
        self.gridlayout.addWidget(self.lbCode, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 7, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBJobFilterDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 2, 1, 1, 2)
        self.lbName = QtGui.QLabel(RBJobFilterDialog)
        self.lbName.setObjectName(_fromUtf8("lbName"))
        self.gridlayout.addWidget(self.lbName, 2, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBJobFilterDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 1, 1, 1, 2)
        self.lbCode.setBuddy(self.edtCode)
        self.lbName.setBuddy(self.edtName)

        self.retranslateUi(RBJobFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBJobFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBJobFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBJobFilterDialog)
        RBJobFilterDialog.setTabOrder(self.edtCode, self.buttonBox)

    def retranslateUi(self, RBJobFilterDialog):
        RBJobFilterDialog.setWindowTitle(_translate("RBJobFilterDialog", "Фильтр назначения работ", None))
        self.lbCode.setText(_translate("RBJobFilterDialog", "&Код", None))
        self.lbName.setText(_translate("RBJobFilterDialog", "&Наименование", None))

