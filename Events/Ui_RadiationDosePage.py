# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_ELN\Events\RadiationDosePage.ui'
#
# Created: Wed May 13 10:30:04 2020
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_RadiationDosePage(object):
    def setupUi(self, RadiationDosePage):
        RadiationDosePage.setObjectName(_fromUtf8("RadiationDosePage"))
        RadiationDosePage.resize(687, 300)
        self.gridLayout = QtGui.QGridLayout(RadiationDosePage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblRadiationDose = CTableView(RadiationDosePage)
        self.tblRadiationDose.setObjectName(_fromUtf8("tblRadiationDose"))
        self.gridLayout.addWidget(self.tblRadiationDose, 0, 0, 1, 4)
        self.lblRecordCount = QtGui.QLabel(RadiationDosePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRecordCount.sizePolicy().hasHeightForWidth())
        self.lblRecordCount.setSizePolicy(sizePolicy)
        self.lblRecordCount.setObjectName(_fromUtf8("lblRecordCount"))
        self.gridLayout.addWidget(self.lblRecordCount, 1, 0, 1, 1)
        self.lblDoseSum = CRadiationDoseSumLabel(RadiationDosePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDoseSum.sizePolicy().hasHeightForWidth())
        self.lblDoseSum.setSizePolicy(sizePolicy)
        self.lblDoseSum.setObjectName(_fromUtf8("lblDoseSum"))
        self.gridLayout.addWidget(self.lblDoseSum, 1, 3, 1, 1)
        self.btnRadiationDosePrint = CPrintButton(RadiationDosePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRadiationDosePrint.sizePolicy().hasHeightForWidth())
        self.btnRadiationDosePrint.setSizePolicy(sizePolicy)
        self.btnRadiationDosePrint.setObjectName(_fromUtf8("btnRadiationDosePrint"))
        self.gridLayout.addWidget(self.btnRadiationDosePrint, 2, 0, 1, 1)
        self.lblActionSum = QtGui.QLabel(RadiationDosePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblActionSum.sizePolicy().hasHeightForWidth())
        self.lblActionSum.setSizePolicy(sizePolicy)
        self.lblActionSum.setObjectName(_fromUtf8("lblActionSum"))
        self.gridLayout.addWidget(self.lblActionSum, 1, 1, 1, 1)
        self.lblPhotosSum = QtGui.QLabel(RadiationDosePage)
        self.lblPhotosSum.setObjectName(_fromUtf8("lblPhotosSum"))
        self.gridLayout.addWidget(self.lblPhotosSum, 1, 2, 1, 1)

        self.retranslateUi(RadiationDosePage)
        QtCore.QMetaObject.connectSlotsByName(RadiationDosePage)

    def retranslateUi(self, RadiationDosePage):
        RadiationDosePage.setWindowTitle(_translate("RadiationDosePage", "Form", None))
        self.lblRecordCount.setText(_translate("RadiationDosePage", "Количество записей   ", None))
        self.lblDoseSum.setText(_translate("RadiationDosePage", "Сумма доз", None))
        self.btnRadiationDosePrint.setText(_translate("RadiationDosePage", "Печать", None))
        self.lblActionSum.setText(_translate("RadiationDosePage", "Сумма количества действий   ", None))
        self.lblPhotosSum.setText(_translate("RadiationDosePage", "Сумма количества снимков    ", None))

from library.TableView import CTableView
from Events.Utils import CRadiationDoseSumLabel
from library.PrintTemplates import CPrintButton
