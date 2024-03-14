# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\TNMPhase\RBTNMPhaseEditor.ui'
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

class Ui_RBTNMPhaseEditor(object):
    def setupUi(self, RBTNMPhaseEditor):
        RBTNMPhaseEditor.setObjectName(_fromUtf8("RBTNMPhaseEditor"))
        RBTNMPhaseEditor.resize(603, 175)
        RBTNMPhaseEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBTNMPhaseEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(RBTNMPhaseEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMainInfo = QtGui.QWidget()
        self.tabMainInfo.setObjectName(_fromUtf8("tabMainInfo"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabMainInfo)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.edtName = QtGui.QLineEdit(self.tabMainInfo)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_4.addWidget(self.edtName, 1, 2, 1, 3)
        self.lblEndDate = QtGui.QLabel(self.tabMainInfo)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout_4.addWidget(self.lblEndDate, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 4, 4, 1, 1)
        self.cmbMKB = CICDCodeEditEx(self.tabMainInfo)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.gridLayout_4.addWidget(self.cmbMKB, 2, 2, 1, 1)
        self.lblName = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_4.addWidget(self.lblName, 1, 0, 1, 2)
        self.lblMKB = QtGui.QLabel(self.tabMainInfo)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout_4.addWidget(self.lblMKB, 2, 0, 1, 2)
        self.lblCode = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_4.addWidget(self.lblCode, 0, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 2, 4, 1, 1)
        self.edtEndDate = CDateEdit(self.tabMainInfo)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout_4.addWidget(self.edtEndDate, 4, 2, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMainInfo)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_4.addWidget(self.edtCode, 0, 2, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem2, 5, 2, 1, 1)
        self.edtBegDate = CDateEdit(self.tabMainInfo)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout_4.addWidget(self.edtBegDate, 3, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(self.tabMainInfo)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout_4.addWidget(self.lblBegDate, 3, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 3, 4, 1, 1)
        self.tabWidget.addTab(self.tabMainInfo, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_5.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBTNMPhaseEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblName.setBuddy(self.edtName)
        self.lblMKB.setBuddy(self.cmbMKB)
        self.lblCode.setBuddy(self.edtCode)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(RBTNMPhaseEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBTNMPhaseEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBTNMPhaseEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBTNMPhaseEditor)
        RBTNMPhaseEditor.setTabOrder(self.tabWidget, self.edtCode)
        RBTNMPhaseEditor.setTabOrder(self.edtCode, self.edtName)
        RBTNMPhaseEditor.setTabOrder(self.edtName, self.cmbMKB)
        RBTNMPhaseEditor.setTabOrder(self.cmbMKB, self.edtEndDate)
        RBTNMPhaseEditor.setTabOrder(self.edtEndDate, self.tblIdentification)
        RBTNMPhaseEditor.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, RBTNMPhaseEditor):
        RBTNMPhaseEditor.setWindowTitle(_translate("RBTNMPhaseEditor", "Dialog", None))
        self.lblEndDate.setText(_translate("RBTNMPhaseEditor", "Д&ата окончания", None))
        self.lblName.setText(_translate("RBTNMPhaseEditor", "&Наименование", None))
        self.lblMKB.setText(_translate("RBTNMPhaseEditor", "&Диагноз", None))
        self.lblCode.setText(_translate("RBTNMPhaseEditor", "&Код", None))
        self.edtEndDate.setDisplayFormat(_translate("RBTNMPhaseEditor", "dd.MM.yyyy", None))
        self.edtBegDate.setDisplayFormat(_translate("RBTNMPhaseEditor", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("RBTNMPhaseEditor", "Д&ата окончания", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMainInfo), _translate("RBTNMPhaseEditor", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBTNMPhaseEditor", "&Идентификация", None))

from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEditEx
from library.InDocTable import CInDocTableView
