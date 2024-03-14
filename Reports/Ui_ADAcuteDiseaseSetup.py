# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\ADAcuteDiseaseSetup.ui'
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

class Ui_ADAcuteDiseaseSetup(object):
    def setupUi(self, ADAcuteDiseaseSetup):
        ADAcuteDiseaseSetup.setObjectName(_fromUtf8("ADAcuteDiseaseSetup"))
        ADAcuteDiseaseSetup.setWindowModality(QtCore.Qt.ApplicationModal)
        ADAcuteDiseaseSetup.resize(347, 120)
        ADAcuteDiseaseSetup.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ADAcuteDiseaseSetup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblMKB = QtGui.QLabel(ADAcuteDiseaseSetup)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 2, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(ADAcuteDiseaseSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(ADAcuteDiseaseSetup)
        self.edtMKBFrom.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBFrom.setSizePolicy(sizePolicy)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBFrom.setMaxLength(6)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ADAcuteDiseaseSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 5)
        self.edtMKBTo = CICDCodeEdit(ADAcuteDiseaseSetup)
        self.edtMKBTo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBTo.sizePolicy().hasHeightForWidth())
        self.edtMKBTo.setSizePolicy(sizePolicy)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBTo.setMaxLength(6)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 2, 3, 1, 1)
        self.edtBegDate = CDateEdit(ADAcuteDiseaseSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ADAcuteDiseaseSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.cmbMKBFilter = QtGui.QComboBox(ADAcuteDiseaseSetup)
        self.cmbMKBFilter.setObjectName(_fromUtf8("cmbMKBFilter"))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.cmbMKBFilter.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbMKBFilter, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(109, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        self.edtEndDate = CDateEdit(ADAcuteDiseaseSetup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 2)
        self.lblMKB.setBuddy(self.cmbMKBFilter)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(ADAcuteDiseaseSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ADAcuteDiseaseSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ADAcuteDiseaseSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ADAcuteDiseaseSetup)
        ADAcuteDiseaseSetup.setTabOrder(self.edtBegDate, self.edtEndDate)
        ADAcuteDiseaseSetup.setTabOrder(self.edtEndDate, self.cmbMKBFilter)
        ADAcuteDiseaseSetup.setTabOrder(self.cmbMKBFilter, self.edtMKBFrom)
        ADAcuteDiseaseSetup.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        ADAcuteDiseaseSetup.setTabOrder(self.edtMKBTo, self.buttonBox)

    def retranslateUi(self, ADAcuteDiseaseSetup):
        ADAcuteDiseaseSetup.setWindowTitle(_translate("ADAcuteDiseaseSetup", "параметры отчёта", None))
        self.lblMKB.setText(_translate("ADAcuteDiseaseSetup", "Коды диагнозов по &МКБ", None))
        self.lblBegDate.setText(_translate("ADAcuteDiseaseSetup", "Дата &начала периода", None))
        self.edtMKBFrom.setInputMask(_translate("ADAcuteDiseaseSetup", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("ADAcuteDiseaseSetup", "A.", None))
        self.edtMKBTo.setInputMask(_translate("ADAcuteDiseaseSetup", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("ADAcuteDiseaseSetup", "Z99.9", None))
        self.edtBegDate.setDisplayFormat(_translate("ADAcuteDiseaseSetup", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("ADAcuteDiseaseSetup", "Дата &окончания периода", None))
        self.cmbMKBFilter.setItemText(0, _translate("ADAcuteDiseaseSetup", "Игнор.", None))
        self.cmbMKBFilter.setItemText(1, _translate("ADAcuteDiseaseSetup", "Интервал", None))
        self.edtEndDate.setDisplayFormat(_translate("ADAcuteDiseaseSetup", "dd.MM.yyyy", None))

from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
