# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ADAcuteDiseaseEditor.ui'
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

class Ui_ADAcuteDiseaseEditor(object):
    def setupUi(self, ADAcuteDiseaseEditor):
        ADAcuteDiseaseEditor.setObjectName(_fromUtf8("ADAcuteDiseaseEditor"))
        ADAcuteDiseaseEditor.resize(403, 371)
        self.gridLayout = QtGui.QGridLayout(ADAcuteDiseaseEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnRetry = QtGui.QPushButton(ADAcuteDiseaseEditor)
        self.btnRetry.setObjectName(_fromUtf8("btnRetry"))
        self.gridLayout.addWidget(self.btnRetry, 1, 2, 1, 1)
        self.tblAcuteDisease = CInDocTableView(ADAcuteDiseaseEditor)
        self.tblAcuteDisease.setObjectName(_fromUtf8("tblAcuteDisease"))
        self.gridLayout.addWidget(self.tblAcuteDisease, 0, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(201, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnPrint = QtGui.QPushButton(ADAcuteDiseaseEditor)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 1, 1, 1, 1)
        self.btnSave = QtGui.QPushButton(ADAcuteDiseaseEditor)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout.addWidget(self.btnSave, 1, 3, 1, 1)
        self.btnClose = QtGui.QPushButton(ADAcuteDiseaseEditor)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 4, 1, 1)

        self.retranslateUi(ADAcuteDiseaseEditor)
        QtCore.QMetaObject.connectSlotsByName(ADAcuteDiseaseEditor)
        ADAcuteDiseaseEditor.setTabOrder(self.tblAcuteDisease, self.btnPrint)
        ADAcuteDiseaseEditor.setTabOrder(self.btnPrint, self.btnRetry)
        ADAcuteDiseaseEditor.setTabOrder(self.btnRetry, self.btnSave)
        ADAcuteDiseaseEditor.setTabOrder(self.btnSave, self.btnClose)

    def retranslateUi(self, ADAcuteDiseaseEditor):
        ADAcuteDiseaseEditor.setWindowTitle(_translate("ADAcuteDiseaseEditor", "Расчет средней длительности острых заболеваний", None))
        self.btnRetry.setText(_translate("ADAcuteDiseaseEditor", "Повторить", None))
        self.btnPrint.setText(_translate("ADAcuteDiseaseEditor", "Печать", None))
        self.btnSave.setText(_translate("ADAcuteDiseaseEditor", "Сохранить", None))
        self.btnClose.setText(_translate("ADAcuteDiseaseEditor", "Отмена", None))

from library.InDocTable import CInDocTableView
