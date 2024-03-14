# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBThesaurusFilter.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_RBThesaurusFilterDialog(object):
    def setupUi(self, RBThesaurusFilterDialog):
        RBThesaurusFilterDialog.setObjectName(_fromUtf8("RBThesaurusFilterDialog"))
        RBThesaurusFilterDialog.resize(323, 140)
        RBThesaurusFilterDialog.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(RBThesaurusFilterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblName = QtGui.QLabel(RBThesaurusFilterDialog)
        self.lblName.setText(_fromUtf8("Наименование"))
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBThesaurusFilterDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblCode = QtGui.QLabel(RBThesaurusFilterDialog)
        self.lblCode.setText(_fromUtf8("Код"))
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBThesaurusFilterDialog)
        self.edtName.setText(_fromUtf8(""))
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBThesaurusFilterDialog)
        self.edtCode.setText(_fromUtf8(""))
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)

        self.retranslateUi(RBThesaurusFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBThesaurusFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBThesaurusFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RBThesaurusFilterDialog)
        RBThesaurusFilterDialog.setTabOrder(self.edtCode, self.edtName)
        RBThesaurusFilterDialog.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, RBThesaurusFilterDialog):
        pass

