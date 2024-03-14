# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\kmivc\Samson\UP_s11\client\Registry\HomeCallRequestUpdateStatusDialog.ui'
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

class Ui_HomeCallRequestUpdateStatusDialog(object):
    def setupUi(self, HomeCallRequestUpdateStatusDialog):
        HomeCallRequestUpdateStatusDialog.setObjectName(_fromUtf8("HomeCallRequestUpdateStatusDialog"))
        HomeCallRequestUpdateStatusDialog.resize(316, 267)
        self.gridLayout = QtGui.QGridLayout(HomeCallRequestUpdateStatusDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(HomeCallRequestUpdateStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.label = QtGui.QLabel(HomeCallRequestUpdateStatusDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblNote = QtGui.QLabel(HomeCallRequestUpdateStatusDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblNote.sizePolicy().hasHeightForWidth())
        self.lblNote.setSizePolicy(sizePolicy)
        self.lblNote.setMinimumSize(QtCore.QSize(0, 25))
        self.lblNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 2, 0, 2, 1)
        self.cmbStatus = QtGui.QComboBox(HomeCallRequestUpdateStatusDialog)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.gridLayout.addWidget(self.cmbStatus, 0, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.edtComment = QtGui.QPlainTextEdit(HomeCallRequestUpdateStatusDialog)
        self.edtComment.setTabChangesFocus(True)
        self.edtComment.setObjectName(_fromUtf8("edtComment"))
        self.gridLayout.addWidget(self.edtComment, 2, 1, 3, 2)
        self.label.setBuddy(self.cmbStatus)
        self.lblNote.setBuddy(self.edtComment)

        self.retranslateUi(HomeCallRequestUpdateStatusDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HomeCallRequestUpdateStatusDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HomeCallRequestUpdateStatusDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HomeCallRequestUpdateStatusDialog)
        HomeCallRequestUpdateStatusDialog.setTabOrder(self.cmbStatus, self.edtComment)
        HomeCallRequestUpdateStatusDialog.setTabOrder(self.edtComment, self.buttonBox)

    def retranslateUi(self, HomeCallRequestUpdateStatusDialog):
        HomeCallRequestUpdateStatusDialog.setWindowTitle(_translate("HomeCallRequestUpdateStatusDialog", "Dialog", None))
        self.label.setText(_translate("HomeCallRequestUpdateStatusDialog", "Статус", None))
        self.lblNote.setText(_translate("HomeCallRequestUpdateStatusDialog", "Комментарий", None))

