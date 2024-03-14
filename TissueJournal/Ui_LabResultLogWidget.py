# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\TissueJournal\LabResultLogWidget.ui'
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

class Ui_LabResultLogWidget(object):
    def setupUi(self, LabResultLogWidget):
        LabResultLogWidget.setObjectName(_fromUtf8("LabResultLogWidget"))
        LabResultLogWidget.resize(470, 314)
        self.verticalLayout = QtGui.QVBoxLayout(LabResultLogWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.edtLog = QtGui.QTextEdit(LabResultLogWidget)
        self.edtLog.setObjectName(_fromUtf8("edtLog"))
        self.verticalLayout.addWidget(self.edtLog)
        self.frmFind = QtGui.QFrame(LabResultLogWidget)
        self.frmFind.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmFind.setFrameShadow(QtGui.QFrame.Raised)
        self.frmFind.setLineWidth(0)
        self.frmFind.setObjectName(_fromUtf8("frmFind"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frmFind)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.edtFind = QtGui.QLineEdit(self.frmFind)
        self.edtFind.setObjectName(_fromUtf8("edtFind"))
        self.horizontalLayout.addWidget(self.edtFind)
        self.btnNext = QtGui.QToolButton(self.frmFind)
        self.btnNext.setArrowType(QtCore.Qt.DownArrow)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnPrevious = QtGui.QToolButton(self.frmFind)
        self.btnPrevious.setArrowType(QtCore.Qt.UpArrow)
        self.btnPrevious.setObjectName(_fromUtf8("btnPrevious"))
        self.horizontalLayout.addWidget(self.btnPrevious)
        self.verticalLayout.addWidget(self.frmFind)

        self.retranslateUi(LabResultLogWidget)
        QtCore.QMetaObject.connectSlotsByName(LabResultLogWidget)
        LabResultLogWidget.setTabOrder(self.edtLog, self.edtFind)
        LabResultLogWidget.setTabOrder(self.edtFind, self.btnNext)
        LabResultLogWidget.setTabOrder(self.btnNext, self.btnPrevious)

    def retranslateUi(self, LabResultLogWidget):
        LabResultLogWidget.setWindowTitle(_translate("LabResultLogWidget", "Form", None))
        self.btnNext.setText(_translate("LabResultLogWidget", "...", None))
        self.btnPrevious.setText(_translate("LabResultLogWidget", "...", None))

