# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ReportF12_D_3_MSave.ui'
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

class Ui_ReportF12_D_3_MSaveDialog(object):
    def setupUi(self, ReportF12_D_3_MSaveDialog):
        ReportF12_D_3_MSaveDialog.setObjectName(_fromUtf8("ReportF12_D_3_MSaveDialog"))
        ReportF12_D_3_MSaveDialog.resize(447, 150)
        self.gridLayout = QtGui.QGridLayout(ReportF12_D_3_MSaveDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(ReportF12_D_3_MSaveDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)
        self.nameEdit = QtGui.QLineEdit(ReportF12_D_3_MSaveDialog)
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridLayout.addWidget(self.nameEdit, 0, 2, 1, 3)
        self.label = QtGui.QLabel(ReportF12_D_3_MSaveDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.edtFileDir = QtGui.QLineEdit(ReportF12_D_3_MSaveDialog)
        self.edtFileDir.setObjectName(_fromUtf8("edtFileDir"))
        self.gridLayout.addWidget(self.edtFileDir, 1, 2, 1, 2)
        self.btnSelectDir = QtGui.QToolButton(ReportF12_D_3_MSaveDialog)
        self.btnSelectDir.setObjectName(_fromUtf8("btnSelectDir"))
        self.gridLayout.addWidget(self.btnSelectDir, 1, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.saveButton = QtGui.QPushButton(ReportF12_D_3_MSaveDialog)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 3, 0, 1, 1)
        self.btnSendMail = QtGui.QPushButton(ReportF12_D_3_MSaveDialog)
        self.btnSendMail.setEnabled(False)
        self.btnSendMail.setObjectName(_fromUtf8("btnSendMail"))
        self.gridLayout.addWidget(self.btnSendMail, 3, 1, 1, 2)
        self.reportButton = QtGui.QPushButton(ReportF12_D_3_MSaveDialog)
        self.reportButton.setEnabled(False)
        self.reportButton.setObjectName(_fromUtf8("reportButton"))
        self.gridLayout.addWidget(self.reportButton, 3, 3, 1, 2)

        self.retranslateUi(ReportF12_D_3_MSaveDialog)
        QtCore.QMetaObject.connectSlotsByName(ReportF12_D_3_MSaveDialog)
        ReportF12_D_3_MSaveDialog.setTabOrder(self.nameEdit, self.edtFileDir)
        ReportF12_D_3_MSaveDialog.setTabOrder(self.edtFileDir, self.btnSelectDir)
        ReportF12_D_3_MSaveDialog.setTabOrder(self.btnSelectDir, self.saveButton)
        ReportF12_D_3_MSaveDialog.setTabOrder(self.saveButton, self.btnSendMail)
        ReportF12_D_3_MSaveDialog.setTabOrder(self.btnSendMail, self.reportButton)

    def retranslateUi(self, ReportF12_D_3_MSaveDialog):
        ReportF12_D_3_MSaveDialog.setWindowTitle(_translate("ReportF12_D_3_MSaveDialog", "Экспорт формы 12-3-М", None))
        self.label_2.setText(_translate("ReportF12_D_3_MSaveDialog", "Имя файла (без расширения)", None))
        self.label.setText(_translate("ReportF12_D_3_MSaveDialog", "Сохранить в", None))
        self.btnSelectDir.setText(_translate("ReportF12_D_3_MSaveDialog", "...", None))
        self.saveButton.setText(_translate("ReportF12_D_3_MSaveDialog", "сохранить", None))
        self.btnSendMail.setText(_translate("ReportF12_D_3_MSaveDialog", "послать по почте", None))
        self.reportButton.setText(_translate("ReportF12_D_3_MSaveDialog", "сформироать акт приёма-передачи", None))

