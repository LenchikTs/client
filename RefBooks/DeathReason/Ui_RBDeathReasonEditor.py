# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\DeathReason\RBDeathReasonEditor.ui'
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

class Ui_RBDeathReasonEditor(object):
    def setupUi(self, RBDeathReasonEditor):
        RBDeathReasonEditor.setObjectName(_fromUtf8("RBDeathReasonEditor"))
        RBDeathReasonEditor.resize(351, 193)
        RBDeathReasonEditor.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(RBDeathReasonEditor)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(RBDeathReasonEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 9, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 6, 0, 1, 1)
        self.lblCode = QtGui.QLabel(RBDeathReasonEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblName = QtGui.QLabel(RBDeathReasonEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(RBDeathReasonEditor)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 4, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(RBDeathReasonEditor)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 5, 0, 1, 1)
        self.edtBegDate = CDateEdit(RBDeathReasonEditor)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 4, 1, 1, 1)
        self.edtEndDate = CDateEdit(RBDeathReasonEditor)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 5, 1, 1, 1)
        self.lblRegionalCode = QtGui.QLabel(RBDeathReasonEditor)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridlayout.addWidget(self.lblRegionalCode, 2, 0, 1, 1)
        self.lblFederalCode = QtGui.QLabel(RBDeathReasonEditor)
        self.lblFederalCode.setObjectName(_fromUtf8("lblFederalCode"))
        self.gridlayout.addWidget(self.lblFederalCode, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBDeathReasonEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.edtName = QtGui.QLineEdit(RBDeathReasonEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtRegionalCode = QtGui.QLineEdit(RBDeathReasonEditor)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridlayout.addWidget(self.edtRegionalCode, 2, 1, 1, 2)
        self.edtFederalCode = QtGui.QLineEdit(RBDeathReasonEditor)
        self.edtFederalCode.setObjectName(_fromUtf8("edtFederalCode"))
        self.gridlayout.addWidget(self.edtFederalCode, 3, 1, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)
        self.lblFederalCode.setBuddy(self.edtFederalCode)

        self.retranslateUi(RBDeathReasonEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBDeathReasonEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBDeathReasonEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBDeathReasonEditor)
        RBDeathReasonEditor.setTabOrder(self.edtCode, self.edtName)
        RBDeathReasonEditor.setTabOrder(self.edtName, self.edtRegionalCode)
        RBDeathReasonEditor.setTabOrder(self.edtRegionalCode, self.edtFederalCode)
        RBDeathReasonEditor.setTabOrder(self.edtFederalCode, self.edtBegDate)
        RBDeathReasonEditor.setTabOrder(self.edtBegDate, self.edtEndDate)
        RBDeathReasonEditor.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, RBDeathReasonEditor):
        RBDeathReasonEditor.setWindowTitle(_translate("RBDeathReasonEditor", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBDeathReasonEditor", "&Код", None))
        self.lblName.setText(_translate("RBDeathReasonEditor", "&Наименование", None))
        self.lblBegDate.setText(_translate("RBDeathReasonEditor", "Дата начала действия", None))
        self.lblEndDate.setText(_translate("RBDeathReasonEditor", "Дата окончания действия", None))
        self.lblRegionalCode.setText(_translate("RBDeathReasonEditor", "&Региональный код", None))
        self.lblFederalCode.setText(_translate("RBDeathReasonEditor", "&Федеральный код", None))

from library.DateEdit import CDateEdit
