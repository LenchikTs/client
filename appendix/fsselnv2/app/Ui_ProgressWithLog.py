# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\appendix\fsselnv2\app\ProgressWithLog.ui'
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

class Ui_ProgressWithLogDialog(object):
    def setupUi(self, ProgressWithLogDialog):
        ProgressWithLogDialog.setObjectName(_fromUtf8("ProgressWithLogDialog"))
        ProgressWithLogDialog.resize(640, 480)
        self.verticalLayout = QtGui.QVBoxLayout(ProgressWithLogDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtLogView = QtGui.QPlainTextEdit(ProgressWithLogDialog)
        font = QtGui.QFont()
        font.setKerning(True)
        self.txtLogView.setFont(font)
        self.txtLogView.setTabChangesFocus(False)
        self.txtLogView.setUndoRedoEnabled(False)
        self.txtLogView.setReadOnly(True)
        self.txtLogView.setPlainText(_fromUtf8(""))
        self.txtLogView.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.txtLogView.setBackgroundVisible(False)
        self.txtLogView.setObjectName(_fromUtf8("txtLogView"))
        self.verticalLayout.addWidget(self.txtLogView)
        self.progressBar = CProgressBar(ProgressWithLogDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(ProgressWithLogDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProgressWithLogDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProgressWithLogDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProgressWithLogDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProgressWithLogDialog)

    def retranslateUi(self, ProgressWithLogDialog):
        ProgressWithLogDialog.setWindowTitle(_translate("ProgressWithLogDialog", "Журнал обмена", None))

from library.ProgressBar import CProgressBar
