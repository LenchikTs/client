# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\Export131_Wizard_2.ui'
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

class Ui_Export131_Wizard_2(object):
    def setupUi(self, Export131_Wizard_2):
        Export131_Wizard_2.setObjectName(_fromUtf8("Export131_Wizard_2"))
        Export131_Wizard_2.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(Export131_Wizard_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_2 = QtGui.QLabel(Export131_Wizard_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout.addWidget(self.label_2)
        self.nameEdit = QtGui.QLineEdit(Export131_Wizard_2)
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.hboxlayout.addWidget(self.nameEdit)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label = QtGui.QLabel(Export131_Wizard_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout1.addWidget(self.label)
        self.edtFileDir = QtGui.QLineEdit(Export131_Wizard_2)
        self.edtFileDir.setObjectName(_fromUtf8("edtFileDir"))
        self.hboxlayout1.addWidget(self.edtFileDir)
        self.btnSelectDir = QtGui.QToolButton(Export131_Wizard_2)
        self.btnSelectDir.setObjectName(_fromUtf8("btnSelectDir"))
        self.hboxlayout1.addWidget(self.btnSelectDir)
        self.gridlayout.addLayout(self.hboxlayout1, 1, 0, 1, 1)
        self.saveButton = QtGui.QPushButton(Export131_Wizard_2)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridlayout.addWidget(self.saveButton, 3, 0, 1, 1)
        self.btnSendMail = QtGui.QPushButton(Export131_Wizard_2)
        self.btnSendMail.setObjectName(_fromUtf8("btnSendMail"))
        self.gridlayout.addWidget(self.btnSendMail, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.reportButton = QtGui.QPushButton(Export131_Wizard_2)
        self.reportButton.setObjectName(_fromUtf8("reportButton"))
        self.gridlayout.addWidget(self.reportButton, 6, 0, 1, 1)

        self.retranslateUi(Export131_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(Export131_Wizard_2)

    def retranslateUi(self, Export131_Wizard_2):
        Export131_Wizard_2.setWindowTitle(_translate("Export131_Wizard_2", "Dialog", None))
        self.label_2.setText(_translate("Export131_Wizard_2", "имя файла (без расширения)", None))
        self.label.setText(_translate("Export131_Wizard_2", "сохранить в", None))
        self.btnSelectDir.setText(_translate("Export131_Wizard_2", "...", None))
        self.saveButton.setText(_translate("Export131_Wizard_2", "сохранить", None))
        self.btnSendMail.setText(_translate("Export131_Wizard_2", "послать по почте", None))
        self.reportButton.setText(_translate("Export131_Wizard_2", "сформироать акт приёма-передачи", None))

