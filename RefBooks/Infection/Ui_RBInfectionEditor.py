# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\RefBooks\Infection\RBInfectionEditor.ui'
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

class Ui_RBInfectionEditor(object):
    def setupUi(self, RBInfectionEditor):
        RBInfectionEditor.setObjectName(_fromUtf8("RBInfectionEditor"))
        RBInfectionEditor.resize(421, 408)
        self.gridLayout = QtGui.QGridLayout(RBInfectionEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblName = QtGui.QLabel(RBInfectionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBInfectionEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.lblCode = QtGui.QLabel(RBInfectionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBInfectionEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtRegionalCode = QtGui.QLineEdit(RBInfectionEditor)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridLayout.addWidget(self.edtRegionalCode, 2, 1, 1, 2)
        self.lblRegionalCode = QtGui.QLabel(RBInfectionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRegionalCode.sizePolicy().hasHeightForWidth())
        self.lblRegionalCode.setSizePolicy(sizePolicy)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridLayout.addWidget(self.lblRegionalCode, 2, 0, 1, 1)
        self.lblMinimumTerm = QtGui.QLabel(RBInfectionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMinimumTerm.sizePolicy().hasHeightForWidth())
        self.lblMinimumTerm.setSizePolicy(sizePolicy)
        self.lblMinimumTerm.setObjectName(_fromUtf8("lblMinimumTerm"))
        self.gridLayout.addWidget(self.lblMinimumTerm, 3, 0, 1, 1)
        self.cmbMinimumTermUnit = QtGui.QComboBox(RBInfectionEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMinimumTermUnit.sizePolicy().hasHeightForWidth())
        self.cmbMinimumTermUnit.setSizePolicy(sizePolicy)
        self.cmbMinimumTermUnit.setObjectName(_fromUtf8("cmbMinimumTermUnit"))
        self.cmbMinimumTermUnit.addItem(_fromUtf8(""))
        self.cmbMinimumTermUnit.setItemText(0, _fromUtf8(""))
        self.cmbMinimumTermUnit.addItem(_fromUtf8(""))
        self.cmbMinimumTermUnit.addItem(_fromUtf8(""))
        self.cmbMinimumTermUnit.addItem(_fromUtf8(""))
        self.cmbMinimumTermUnit.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMinimumTermUnit, 3, 1, 1, 1)
        self.edtMinimumTermCount = QtGui.QLineEdit(RBInfectionEditor)
        self.edtMinimumTermCount.setInputMask(_fromUtf8(""))
        self.edtMinimumTermCount.setMaxLength(32767)
        self.edtMinimumTermCount.setObjectName(_fromUtf8("edtMinimumTermCount"))
        self.gridLayout.addWidget(self.edtMinimumTermCount, 3, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBInfectionEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.splitter = QtGui.QSplitter(RBInfectionEditor)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlView = QtGui.QWidget(self.splitter)
        self.pnlView.setObjectName(_fromUtf8("pnlView"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlView)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblInfectionVaccines = CInDocTableView(self.pnlView)
        self.tblInfectionVaccines.setObjectName(_fromUtf8("tblInfectionVaccines"))
        self.verticalLayout.addWidget(self.tblInfectionVaccines)
        self.pnlInfectionMiminumTerms = QtGui.QWidget(self.splitter)
        self.pnlInfectionMiminumTerms.setObjectName(_fromUtf8("pnlInfectionMiminumTerms"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlInfectionMiminumTerms)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblInfectionMinimumTerms = CInDocTableView(self.pnlInfectionMiminumTerms)
        self.tblInfectionMinimumTerms.setObjectName(_fromUtf8("tblInfectionMinimumTerms"))
        self.verticalLayout_2.addWidget(self.tblInfectionMinimumTerms)
        self.gridLayout.addWidget(self.splitter, 7, 0, 1, 3)
        self.chkAvailable = QtGui.QCheckBox(RBInfectionEditor)
        self.chkAvailable.setObjectName(_fromUtf8("chkAvailable"))
        self.gridLayout.addWidget(self.chkAvailable, 5, 0, 1, 3)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)
        self.lblMinimumTerm.setBuddy(self.cmbMinimumTermUnit)

        self.retranslateUi(RBInfectionEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBInfectionEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBInfectionEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBInfectionEditor)
        RBInfectionEditor.setTabOrder(self.edtCode, self.edtName)
        RBInfectionEditor.setTabOrder(self.edtName, self.edtRegionalCode)
        RBInfectionEditor.setTabOrder(self.edtRegionalCode, self.cmbMinimumTermUnit)
        RBInfectionEditor.setTabOrder(self.cmbMinimumTermUnit, self.edtMinimumTermCount)
        RBInfectionEditor.setTabOrder(self.edtMinimumTermCount, self.tblInfectionVaccines)
        RBInfectionEditor.setTabOrder(self.tblInfectionVaccines, self.tblInfectionMinimumTerms)
        RBInfectionEditor.setTabOrder(self.tblInfectionMinimumTerms, self.buttonBox)

    def retranslateUi(self, RBInfectionEditor):
        RBInfectionEditor.setWindowTitle(_translate("RBInfectionEditor", "Dialog", None))
        self.lblName.setText(_translate("RBInfectionEditor", "&Наименование", None))
        self.lblCode.setText(_translate("RBInfectionEditor", "&Код", None))
        self.lblRegionalCode.setText(_translate("RBInfectionEditor", "&Региональный код", None))
        self.lblMinimumTerm.setText(_translate("RBInfectionEditor", "&Минимальный срок", None))
        self.cmbMinimumTermUnit.setItemText(1, _translate("RBInfectionEditor", "Д", None))
        self.cmbMinimumTermUnit.setItemText(2, _translate("RBInfectionEditor", "Н", None))
        self.cmbMinimumTermUnit.setItemText(3, _translate("RBInfectionEditor", "М", None))
        self.cmbMinimumTermUnit.setItemText(4, _translate("RBInfectionEditor", "Г", None))
        self.chkAvailable.setText(_translate("RBInfectionEditor", "В наличии", None))

from library.InDocTable import CInDocTableView