# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Registry\AttachOnlineReasonReject.ui'
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

class Ui_ReasonRejectDialog(object):
    def setupUi(self, ReasonRejectDialog):
        ReasonRejectDialog.setObjectName(_fromUtf8("ReasonRejectDialog"))
        ReasonRejectDialog.resize(803, 216)
        self.gridLayout = QtGui.QGridLayout(ReasonRejectDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblReasonReject = QtGui.QLabel(ReasonRejectDialog)
        self.lblReasonReject.setObjectName(_fromUtf8("lblReasonReject"))
        self.horizontalLayout_3.addWidget(self.lblReasonReject)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.cmbReasonReject = CRBComboBox(ReasonRejectDialog)
        self.cmbReasonReject.setObjectName(_fromUtf8("cmbReasonReject"))
        self.verticalLayout.addWidget(self.cmbReasonReject)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblComment = QtGui.QLabel(ReasonRejectDialog)
        self.lblComment.setObjectName(_fromUtf8("lblComment"))
        self.horizontalLayout_2.addWidget(self.lblComment)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.edtComment = QtGui.QLineEdit(ReasonRejectDialog)
        self.edtComment.setObjectName(_fromUtf8("edtComment"))
        self.verticalLayout.addWidget(self.edtComment)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnApply = QtGui.QPushButton(ReasonRejectDialog)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.horizontalLayout.addWidget(self.btnApply)
        self.btnCancel = QtGui.QPushButton(ReasonRejectDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ReasonRejectDialog)
        QtCore.QMetaObject.connectSlotsByName(ReasonRejectDialog)

    def retranslateUi(self, ReasonRejectDialog):
        ReasonRejectDialog.setWindowTitle(_translate("ReasonRejectDialog", "Причина отказа", None))
        self.lblReasonReject.setText(_translate("ReasonRejectDialog", "Причина отказа", None))
        self.lblComment.setText(_translate("ReasonRejectDialog", "Комментарий", None))
        self.btnApply.setText(_translate("ReasonRejectDialog", "Выбрать", None))
        self.btnCancel.setText(_translate("ReasonRejectDialog", "Отменить", None))

from library.crbcombobox import CRBComboBox
