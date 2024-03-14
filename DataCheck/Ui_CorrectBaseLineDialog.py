# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\CorrectBaseLineDialog.ui'
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

class Ui_CorrectBaseLineDialog(object):
    def setupUi(self, CorrectBaseLineDialog):
        CorrectBaseLineDialog.setObjectName(_fromUtf8("CorrectBaseLineDialog"))
        CorrectBaseLineDialog.resize(512, 400)
        self.gridLayout = QtGui.QGridLayout(CorrectBaseLineDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(CorrectBaseLineDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 498, 353))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblNameTitle = QtGui.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblNameTitle.setFont(font)
        self.lblNameTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblNameTitle.setWordWrap(True)
        self.lblNameTitle.setObjectName(_fromUtf8("lblNameTitle"))
        self.gridLayout_2.addWidget(self.lblNameTitle, 0, 0, 1, 1)
        self.tblSelectBaseLine = QtGui.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tblSelectBaseLine.sizePolicy().hasHeightForWidth())
        self.tblSelectBaseLine.setSizePolicy(sizePolicy)
        self.tblSelectBaseLine.setObjectName(_fromUtf8("tblSelectBaseLine"))
        self.gridLayout_2.addWidget(self.tblSelectBaseLine, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 2)
        self.btnOkCancel = QtGui.QDialogButtonBox(CorrectBaseLineDialog)
        self.btnOkCancel.setOrientation(QtCore.Qt.Horizontal)
        self.btnOkCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnOkCancel.setCenterButtons(False)
        self.btnOkCancel.setObjectName(_fromUtf8("btnOkCancel"))
        self.gridLayout.addWidget(self.btnOkCancel, 1, 0, 1, 2)

        self.retranslateUi(CorrectBaseLineDialog)
        QtCore.QObject.connect(self.btnOkCancel, QtCore.SIGNAL(_fromUtf8("accepted()")), CorrectBaseLineDialog.accept)
        QtCore.QObject.connect(self.btnOkCancel, QtCore.SIGNAL(_fromUtf8("rejected()")), CorrectBaseLineDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CorrectBaseLineDialog)

    def retranslateUi(self, CorrectBaseLineDialog):
        CorrectBaseLineDialog.setWindowTitle(_translate("CorrectBaseLineDialog", "Внимание!", None))
        self.lblNameTitle.setText(_translate("CorrectBaseLineDialog", "Выделите базовую строку", None))

