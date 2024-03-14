# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\RefBooks\Unit\RBUnitEditor.ui'
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

class Ui_RBUnitEditor(object):
    def setupUi(self, RBUnitEditor):
        RBUnitEditor.setObjectName(_fromUtf8("RBUnitEditor"))
        RBUnitEditor.resize(379, 155)
        RBUnitEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBUnitEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(RBUnitEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMainInfo = QtGui.QWidget()
        self.tabMainInfo.setObjectName(_fromUtf8("tabMainInfo"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabMainInfo)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblCode = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_4.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMainInfo)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_4.addWidget(self.edtCode, 0, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(17, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 3, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabMainInfo)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_4.addWidget(self.edtName, 1, 1, 1, 2)
        self.lblName = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_4.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblLatinName = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLatinName.sizePolicy().hasHeightForWidth())
        self.lblLatinName.setSizePolicy(sizePolicy)
        self.lblLatinName.setObjectName(_fromUtf8("lblLatinName"))
        self.gridLayout_4.addWidget(self.lblLatinName, 2, 0, 1, 1)
        self.edtLatinName = QtGui.QLineEdit(self.tabMainInfo)
        self.edtLatinName.setObjectName(_fromUtf8("edtLatinName"))
        self.gridLayout_4.addWidget(self.edtLatinName, 2, 1, 1, 1)
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
        self.gridLayout.addWidget(self.tabWidget, 4, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBUnitEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblLatinName.setBuddy(self.edtLatinName)

        self.retranslateUi(RBUnitEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBUnitEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBUnitEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBUnitEditor)
        RBUnitEditor.setTabOrder(self.tabWidget, self.buttonBox)
        RBUnitEditor.setTabOrder(self.buttonBox, self.edtCode)
        RBUnitEditor.setTabOrder(self.edtCode, self.edtName)
        RBUnitEditor.setTabOrder(self.edtName, self.tblIdentification)

    def retranslateUi(self, RBUnitEditor):
        RBUnitEditor.setWindowTitle(_translate("RBUnitEditor", "Dialog", None))
        self.lblCode.setText(_translate("RBUnitEditor", "&Код", None))
        self.lblName.setText(_translate("RBUnitEditor", "&Наименование", None))
        self.lblLatinName.setText(_translate("RBUnitEditor", "&Латинское наименование", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMainInfo), _translate("RBUnitEditor", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBUnitEditor", "&Идентификация", None))

from library.InDocTable import CInDocTableView
