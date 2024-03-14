# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\DiagnosisConfirmationDialog.ui'
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

class Ui_DiagnosisConfirmationDialog(object):
    def setupUi(self, DiagnosisConfirmationDialog):
        DiagnosisConfirmationDialog.setObjectName(_fromUtf8("DiagnosisConfirmationDialog"))
        DiagnosisConfirmationDialog.resize(654, 97)
        self.gridLayout = QtGui.QGridLayout(DiagnosisConfirmationDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblMessage = QtGui.QLabel(DiagnosisConfirmationDialog)
        self.lblMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblMessage.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblMessage.setObjectName(_fromUtf8("lblMessage"))
        self.gridLayout.addWidget(self.lblMessage, 0, 0, 1, 3)
        self.btnAcceptOld = QtGui.QPushButton(DiagnosisConfirmationDialog)
        self.btnAcceptOld.setDefault(True)
        self.btnAcceptOld.setObjectName(_fromUtf8("btnAcceptOld"))
        self.gridLayout.addWidget(self.btnAcceptOld, 1, 0, 1, 1)
        self.btnAcceptNew = QtGui.QPushButton(DiagnosisConfirmationDialog)
        self.btnAcceptNew.setObjectName(_fromUtf8("btnAcceptNew"))
        self.gridLayout.addWidget(self.btnAcceptNew, 1, 1, 1, 1)
        self.btnAcceptNewAndModifyOld = QtGui.QPushButton(DiagnosisConfirmationDialog)
        self.btnAcceptNewAndModifyOld.setObjectName(_fromUtf8("btnAcceptNewAndModifyOld"))
        self.gridLayout.addWidget(self.btnAcceptNewAndModifyOld, 1, 2, 1, 1)

        self.retranslateUi(DiagnosisConfirmationDialog)
        QtCore.QMetaObject.connectSlotsByName(DiagnosisConfirmationDialog)

    def retranslateUi(self, DiagnosisConfirmationDialog):
        DiagnosisConfirmationDialog.setWindowTitle(_translate("DiagnosisConfirmationDialog", "Внимание", None))
        self.lblMessage.setText(_translate("DiagnosisConfirmationDialog", "Ведён код J06.0 (Острый ларингофарингит)\n"
"Ранее для этого пациента был указан код J06.9 (Острая инфекция верхних дыхательных путей неуточненная)\n"
"Изменить на этот код?", None))
        self.btnAcceptOld.setText(_translate("DiagnosisConfirmationDialog", "Изменить на J06.9", None))
        self.btnAcceptNew.setText(_translate("DiagnosisConfirmationDialog", "Принять J06.0", None))
        self.btnAcceptNewAndModifyOld.setText(_translate("DiagnosisConfirmationDialog", "Принять J06.0 и отметить J06.9 как изменённый", None))

