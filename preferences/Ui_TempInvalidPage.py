# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\preferences\TempInvalidPage.ui'
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

class Ui_tempInvalidPage(object):
    def setupUi(self, tempInvalidPage):
        tempInvalidPage.setObjectName(_fromUtf8("tempInvalidPage"))
        tempInvalidPage.resize(695, 137)
        tempInvalidPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(tempInvalidPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbTempInvalidRegime = CRBComboBox(tempInvalidPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTempInvalidRegime.sizePolicy().hasHeightForWidth())
        self.cmbTempInvalidRegime.setSizePolicy(sizePolicy)
        self.cmbTempInvalidRegime.setObjectName(_fromUtf8("cmbTempInvalidRegime"))
        self.gridLayout.addWidget(self.cmbTempInvalidRegime, 2, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.lblTempInvalidRegime = QtGui.QLabel(tempInvalidPage)
        self.lblTempInvalidRegime.setObjectName(_fromUtf8("lblTempInvalidRegime"))
        self.gridLayout.addWidget(self.lblTempInvalidRegime, 2, 0, 1, 1)
        self.lblTempInvalidReason = QtGui.QLabel(tempInvalidPage)
        self.lblTempInvalidReason.setObjectName(_fromUtf8("lblTempInvalidReason"))
        self.gridLayout.addWidget(self.lblTempInvalidReason, 1, 0, 1, 1)
        self.cmbTempInvalidReason = CRBComboBox(tempInvalidPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTempInvalidReason.sizePolicy().hasHeightForWidth())
        self.cmbTempInvalidReason.setSizePolicy(sizePolicy)
        self.cmbTempInvalidReason.setObjectName(_fromUtf8("cmbTempInvalidReason"))
        self.gridLayout.addWidget(self.cmbTempInvalidReason, 1, 1, 1, 2)
        self.lblTempInvalidDoctype = QtGui.QLabel(tempInvalidPage)
        self.lblTempInvalidDoctype.setObjectName(_fromUtf8("lblTempInvalidDoctype"))
        self.gridLayout.addWidget(self.lblTempInvalidDoctype, 0, 0, 1, 1)
        self.cmbTempInvalidDoctype = CRBComboBox(tempInvalidPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTempInvalidDoctype.sizePolicy().hasHeightForWidth())
        self.cmbTempInvalidDoctype.setSizePolicy(sizePolicy)
        self.cmbTempInvalidDoctype.setObjectName(_fromUtf8("cmbTempInvalidDoctype"))
        self.gridLayout.addWidget(self.cmbTempInvalidDoctype, 0, 1, 1, 2)
        self.lblTempInvalidRequestFss = QtGui.QLabel(tempInvalidPage)
        self.lblTempInvalidRequestFss.setObjectName(_fromUtf8("lblTempInvalidRequestFss"))
        self.gridLayout.addWidget(self.lblTempInvalidRequestFss, 3, 0, 1, 1)
        self.chkTempInvalidRequestFss = QtGui.QCheckBox(tempInvalidPage)
        self.chkTempInvalidRequestFss.setText(_fromUtf8(""))
        self.chkTempInvalidRequestFss.setChecked(True)
        self.chkTempInvalidRequestFss.setObjectName(_fromUtf8("chkTempInvalidRequestFss"))
        self.gridLayout.addWidget(self.chkTempInvalidRequestFss, 3, 1, 1, 1)
        self.lblTempInvalidRegime.setBuddy(self.cmbTempInvalidRegime)
        self.lblTempInvalidReason.setBuddy(self.cmbTempInvalidReason)
        self.lblTempInvalidDoctype.setBuddy(self.cmbTempInvalidDoctype)

        self.retranslateUi(tempInvalidPage)
        QtCore.QMetaObject.connectSlotsByName(tempInvalidPage)
        tempInvalidPage.setTabOrder(self.cmbTempInvalidDoctype, self.cmbTempInvalidReason)

    def retranslateUi(self, tempInvalidPage):
        tempInvalidPage.setWindowTitle(_translate("tempInvalidPage", "ВУТ", None))
        self.lblTempInvalidRegime.setText(_translate("tempInvalidPage", "Режим ВУТ по умолчанию", None))
        self.lblTempInvalidReason.setText(_translate("tempInvalidPage", "Причина ВУТ по умолчанию", None))
        self.lblTempInvalidDoctype.setText(_translate("tempInvalidPage", "Документ ВУТ по умолчанию", None))
        self.lblTempInvalidRequestFss.setText(_translate("tempInvalidPage", "Запрашивать СФР на наличие открытых ЭЛН при создании нового эпизода ВУТ", None))

from library.crbcombobox import CRBComboBox
