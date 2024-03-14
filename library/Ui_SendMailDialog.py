# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\SendMailDialog.ui'
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

class Ui_SendMailDialog(object):
    def setupUi(self, SendMailDialog):
        SendMailDialog.setObjectName(_fromUtf8("SendMailDialog"))
        SendMailDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SendMailDialog.resize(451, 307)
        SendMailDialog.setSizeGripEnabled(True)
        SendMailDialog.setModal(True)
        self.gridlayout = QtGui.QGridLayout(SendMailDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblRecipient = QtGui.QLabel(SendMailDialog)
        self.lblRecipient.setObjectName(_fromUtf8("lblRecipient"))
        self.gridlayout.addWidget(self.lblRecipient, 0, 0, 1, 1)
        self.edtRecipient = QtGui.QLineEdit(SendMailDialog)
        self.edtRecipient.setObjectName(_fromUtf8("edtRecipient"))
        self.gridlayout.addWidget(self.edtRecipient, 0, 1, 1, 1)
        self.lblSubject = QtGui.QLabel(SendMailDialog)
        self.lblSubject.setObjectName(_fromUtf8("lblSubject"))
        self.gridlayout.addWidget(self.lblSubject, 1, 0, 1, 1)
        self.edtSubject = QtGui.QLineEdit(SendMailDialog)
        self.edtSubject.setObjectName(_fromUtf8("edtSubject"))
        self.gridlayout.addWidget(self.edtSubject, 1, 1, 1, 1)
        self.lblText = QtGui.QLabel(SendMailDialog)
        self.lblText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblText.setObjectName(_fromUtf8("lblText"))
        self.gridlayout.addWidget(self.lblText, 2, 0, 1, 1)
        self.edtText = QtGui.QTextEdit(SendMailDialog)
        self.edtText.setObjectName(_fromUtf8("edtText"))
        self.gridlayout.addWidget(self.edtText, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SendMailDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.label = QtGui.QLabel(SendMailDialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 3, 0, 1, 1)
        self.tblAttach = CTableView(SendMailDialog)
        self.tblAttach.setObjectName(_fromUtf8("tblAttach"))
        self.gridlayout.addWidget(self.tblAttach, 3, 1, 1, 1)
        self.lblRecipient.setBuddy(self.edtRecipient)
        self.lblSubject.setBuddy(self.edtSubject)
        self.lblText.setBuddy(self.edtText)

        self.retranslateUi(SendMailDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SendMailDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SendMailDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SendMailDialog)
        SendMailDialog.setTabOrder(self.edtRecipient, self.edtSubject)
        SendMailDialog.setTabOrder(self.edtSubject, self.edtText)
        SendMailDialog.setTabOrder(self.edtText, self.buttonBox)

    def retranslateUi(self, SendMailDialog):
        SendMailDialog.setWindowTitle(_translate("SendMailDialog", "подготовка к отправке e-mail", None))
        self.lblRecipient.setText(_translate("SendMailDialog", "Кому", None))
        self.lblSubject.setText(_translate("SendMailDialog", "Тема", None))
        self.lblText.setText(_translate("SendMailDialog", "Текст", None))
        self.label.setText(_translate("SendMailDialog", "Вложенные\n"
"файлы", None))

from TableView import CTableView
