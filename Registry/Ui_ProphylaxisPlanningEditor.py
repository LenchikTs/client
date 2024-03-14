# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_DN\Registry\ProphylaxisPlanningEditor.ui'
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

class Ui_ProphylaxisPlanningEditor(object):
    def setupUi(self, ProphylaxisPlanningEditor):
        ProphylaxisPlanningEditor.setObjectName(_fromUtf8("ProphylaxisPlanningEditor"))
        ProphylaxisPlanningEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ProphylaxisPlanningEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblProphylaxis = CInDocTableView(ProphylaxisPlanningEditor)
        self.tblProphylaxis.setObjectName(_fromUtf8("tblProphylaxis"))
        self.gridLayout.addWidget(self.tblProphylaxis, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProphylaxisPlanningEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ProphylaxisPlanningEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProphylaxisPlanningEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProphylaxisPlanningEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ProphylaxisPlanningEditor)

    def retranslateUi(self, ProphylaxisPlanningEditor):
        ProphylaxisPlanningEditor.setWindowTitle(_translate("ProphylaxisPlanningEditor", "Редактор Журнала планирования профилактического наблюдения", None))

from library.InDocTable import CInDocTableView
