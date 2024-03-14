# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ChangePeriodDiagnosisLUD.ui'
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

class Ui_ChangePeriodDiagnosisLUD(object):
    def setupUi(self, ChangePeriodDiagnosisLUD):
        ChangePeriodDiagnosisLUD.setObjectName(_fromUtf8("ChangePeriodDiagnosisLUD"))
        ChangePeriodDiagnosisLUD.resize(564, 71)
        self.gridLayout = QtGui.QGridLayout(ChangePeriodDiagnosisLUD)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPeriod = QtGui.QLabel(ChangePeriodDiagnosisLUD)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ChangePeriodDiagnosisLUD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.edtEndDate = CDateEdit(ChangePeriodDiagnosisLUD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChangePeriodDiagnosisLUD)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(ChangePeriodDiagnosisLUD)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChangePeriodDiagnosisLUD.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChangePeriodDiagnosisLUD.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangePeriodDiagnosisLUD)

    def retranslateUi(self, ChangePeriodDiagnosisLUD):
        ChangePeriodDiagnosisLUD.setWindowTitle(_translate("ChangePeriodDiagnosisLUD", "Изменение пероида заболевания", None))
        self.lblPeriod.setText(_translate("ChangePeriodDiagnosisLUD", "Период заболевания", None))
        self.edtBegDate.setDisplayFormat(_translate("ChangePeriodDiagnosisLUD", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("ChangePeriodDiagnosisLUD", "dd.MM.yyyy", None))

from library.DateEdit import CDateEdit
