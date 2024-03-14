# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\RBTumorEditor.ui'
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

class Ui_RBTumorEditor(object):
    def setupUi(self, RBTumorEditor):
        RBTumorEditor.setObjectName(_fromUtf8("RBTumorEditor"))
        RBTumorEditor.resize(530, 184)
        RBTumorEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBTumorEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(RBTumorEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMainInfo = QtGui.QWidget()
        self.tabMainInfo.setObjectName(_fromUtf8("tabMainInfo"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabMainInfo)
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
        self.lblName = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_4.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabMainInfo)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_4.addWidget(self.edtName, 1, 1, 1, 2)
        self.lblMKB = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMKB.sizePolicy().hasHeightForWidth())
        self.lblMKB.setSizePolicy(sizePolicy)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout_4.addWidget(self.lblMKB, 2, 0, 1, 1)
        self.cmbMKB = CICDCodeEditEx(self.tabMainInfo)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.gridLayout_4.addWidget(self.cmbMKB, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(318, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(17, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tabMainInfo, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_5.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 6, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBTumorEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.frmDiagRange1 = QtGui.QFrame(RBTumorEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmDiagRange1.sizePolicy().hasHeightForWidth())
        self.frmDiagRange1.setSizePolicy(sizePolicy)
        self.frmDiagRange1.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmDiagRange1.setFrameShadow(QtGui.QFrame.Plain)
        self.frmDiagRange1.setLineWidth(0)
        self.frmDiagRange1.setObjectName(_fromUtf8("frmDiagRange1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frmDiagRange1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addWidget(self.frmDiagRange1, 3, 1, 1, 1)
        self.frmDiagRange2 = QtGui.QFrame(RBTumorEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmDiagRange2.sizePolicy().hasHeightForWidth())
        self.frmDiagRange2.setSizePolicy(sizePolicy)
        self.frmDiagRange2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmDiagRange2.setFrameShadow(QtGui.QFrame.Plain)
        self.frmDiagRange2.setLineWidth(0)
        self.frmDiagRange2.setObjectName(_fromUtf8("frmDiagRange2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frmDiagRange2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout.addWidget(self.frmDiagRange2, 5, 1, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblMKB.setBuddy(self.cmbMKB)

        self.retranslateUi(RBTumorEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBTumorEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBTumorEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBTumorEditor)

    def retranslateUi(self, RBTumorEditor):
        RBTumorEditor.setWindowTitle(_translate("RBTumorEditor", "Dialog", None))
        self.lblCode.setText(_translate("RBTumorEditor", "Код", None))
        self.lblName.setText(_translate("RBTumorEditor", "Наименование", None))
        self.lblMKB.setText(_translate("RBTumorEditor", "Диагноз", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMainInfo), _translate("RBTumorEditor", "Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBTumorEditor", "Идентификация", None))

from library.ICDCodeEdit import CICDCodeEditEx
from library.InDocTable import CInDocTableView
