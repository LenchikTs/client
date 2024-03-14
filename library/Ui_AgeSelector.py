# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\AgeSelector.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(179, 19)
        self.hboxlayout = QtGui.QHBoxLayout(Form)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(2)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.cmbBegAgeUnit = QtGui.QComboBox(Form)
        self.cmbBegAgeUnit.setObjectName(_fromUtf8("cmbBegAgeUnit"))
        self.cmbBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbBegAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbBegAgeUnit.addItem(_fromUtf8(""))
        self.cmbBegAgeUnit.addItem(_fromUtf8(""))
        self.hboxlayout.addWidget(self.cmbBegAgeUnit)
        self.edtBegAgeCount = QtGui.QLineEdit(Form)
        self.edtBegAgeCount.setMaxLength(4)
        self.edtBegAgeCount.setObjectName(_fromUtf8("edtBegAgeCount"))
        self.hboxlayout.addWidget(self.edtBegAgeCount)
        self.lblAgeSep = QtGui.QLabel(Form)
        self.lblAgeSep.setObjectName(_fromUtf8("lblAgeSep"))
        self.hboxlayout.addWidget(self.lblAgeSep)
        self.cmbEndAgeUnit = QtGui.QComboBox(Form)
        self.cmbEndAgeUnit.setObjectName(_fromUtf8("cmbEndAgeUnit"))
        self.cmbEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbEndAgeUnit.setItemText(0, _fromUtf8(""))
        self.cmbEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbEndAgeUnit.addItem(_fromUtf8(""))
        self.cmbEndAgeUnit.addItem(_fromUtf8(""))
        self.hboxlayout.addWidget(self.cmbEndAgeUnit)
        self.edtEndAgeCount = QtGui.QLineEdit(Form)
        self.edtEndAgeCount.setMaxLength(4)
        self.edtEndAgeCount.setObjectName(_fromUtf8("edtEndAgeCount"))
        self.hboxlayout.addWidget(self.edtEndAgeCount)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.cmbBegAgeUnit, self.edtBegAgeCount)
        Form.setTabOrder(self.edtBegAgeCount, self.cmbEndAgeUnit)
        Form.setTabOrder(self.cmbEndAgeUnit, self.edtEndAgeCount)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.cmbBegAgeUnit.setItemText(1, _translate("Form", "Д", None))
        self.cmbBegAgeUnit.setItemText(2, _translate("Form", "Н", None))
        self.cmbBegAgeUnit.setItemText(3, _translate("Form", "М", None))
        self.cmbBegAgeUnit.setItemText(4, _translate("Form", "Г", None))
        self.lblAgeSep.setText(_translate("Form", "по", None))
        self.cmbEndAgeUnit.setItemText(1, _translate("Form", "Д", None))
        self.cmbEndAgeUnit.setItemText(2, _translate("Form", "Н", None))
        self.cmbEndAgeUnit.setItemText(3, _translate("Form", "М", None))
        self.cmbEndAgeUnit.setItemText(4, _translate("Form", "Г", None))

