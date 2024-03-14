# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\ItemEditorDialogWithIdentification.ui'
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

class Ui_ItemEditorDialogWithIdentification(object):
    def setupUi(self, ItemEditorDialogWithIdentification):
        ItemEditorDialogWithIdentification.setObjectName(_fromUtf8("ItemEditorDialogWithIdentification"))
        ItemEditorDialogWithIdentification.resize(313, 278)
        ItemEditorDialogWithIdentification.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(ItemEditorDialogWithIdentification)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(ItemEditorDialogWithIdentification)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblCode = QtGui.QLabel(ItemEditorDialogWithIdentification)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialogWithIdentification)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.edtName = QtGui.QLineEdit(ItemEditorDialogWithIdentification)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName = QtGui.QLabel(ItemEditorDialogWithIdentification)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.tblIdentification = CInDocTableView(ItemEditorDialogWithIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridlayout.addWidget(self.tblIdentification, 2, 0, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(ItemEditorDialogWithIdentification)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialogWithIdentification.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialogWithIdentification.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialogWithIdentification)
        ItemEditorDialogWithIdentification.setTabOrder(self.edtCode, self.edtName)
        ItemEditorDialogWithIdentification.setTabOrder(self.edtName, self.tblIdentification)
        ItemEditorDialogWithIdentification.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, ItemEditorDialogWithIdentification):
        ItemEditorDialogWithIdentification.setWindowTitle(_translate("ItemEditorDialogWithIdentification", "ChangeMe!", None))
        self.lblCode.setText(_translate("ItemEditorDialogWithIdentification", "&Код", None))
        self.lblName.setText(_translate("ItemEditorDialogWithIdentification", "&Наименование", None))

from library.InDocTable import CInDocTableView
