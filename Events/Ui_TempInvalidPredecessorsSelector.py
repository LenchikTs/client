# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Events\TempInvalidPredecessorsSelector.ui'
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

class Ui_TempInvalidPredecessorsSelector(object):
    def setupUi(self, TempInvalidPredecessorsSelector):
        TempInvalidPredecessorsSelector.setObjectName(_fromUtf8("TempInvalidPredecessorsSelector"))
        TempInvalidPredecessorsSelector.resize(532, 305)
        TempInvalidPredecessorsSelector.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(TempInvalidPredecessorsSelector)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtBegExternalPeriod = CDateEdit(TempInvalidPredecessorsSelector)
        self.edtBegExternalPeriod.setEnabled(False)
        self.edtBegExternalPeriod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.edtBegExternalPeriod.setObjectName(_fromUtf8("edtBegExternalPeriod"))
        self.gridLayout.addWidget(self.edtBegExternalPeriod, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.tblPredecessors = CInDocTableView(TempInvalidPredecessorsSelector)
        self.tblPredecessors.setObjectName(_fromUtf8("tblPredecessors"))
        self.gridLayout.addWidget(self.tblPredecessors, 0, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidPredecessorsSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 5)
        self.chkExternalPeriod = QtGui.QCheckBox(TempInvalidPredecessorsSelector)
        self.chkExternalPeriod.setObjectName(_fromUtf8("chkExternalPeriod"))
        self.gridLayout.addWidget(self.chkExternalPeriod, 1, 0, 1, 1)
        self.edtEndExternalPeriod = CDateEdit(TempInvalidPredecessorsSelector)
        self.edtEndExternalPeriod.setEnabled(False)
        self.edtEndExternalPeriod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.edtEndExternalPeriod.setObjectName(_fromUtf8("edtEndExternalPeriod"))
        self.gridLayout.addWidget(self.edtEndExternalPeriod, 1, 3, 1, 1)
        self.lblEndExternalPeriod = QtGui.QLabel(TempInvalidPredecessorsSelector)
        self.lblEndExternalPeriod.setEnabled(False)
        self.lblEndExternalPeriod.setObjectName(_fromUtf8("lblEndExternalPeriod"))
        self.gridLayout.addWidget(self.lblEndExternalPeriod, 1, 2, 1, 1)

        self.retranslateUi(TempInvalidPredecessorsSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidPredecessorsSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidPredecessorsSelector.reject)
        QtCore.QObject.connect(self.chkExternalPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtBegExternalPeriod.setEnabled)
        QtCore.QObject.connect(self.chkExternalPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblEndExternalPeriod.setEnabled)
        QtCore.QObject.connect(self.chkExternalPeriod, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtEndExternalPeriod.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidPredecessorsSelector)
        TempInvalidPredecessorsSelector.setTabOrder(self.tblPredecessors, self.chkExternalPeriod)
        TempInvalidPredecessorsSelector.setTabOrder(self.chkExternalPeriod, self.buttonBox)

    def retranslateUi(self, TempInvalidPredecessorsSelector):
        TempInvalidPredecessorsSelector.setWindowTitle(_translate("TempInvalidPredecessorsSelector", "Действующие ЭЛН по данным СФР", None))
        self.chkExternalPeriod.setText(_translate("TempInvalidPredecessorsSelector", "Внешний период нетрудоспособности с", None))
        self.lblEndExternalPeriod.setText(_translate("TempInvalidPredecessorsSelector", "по", None))

from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
