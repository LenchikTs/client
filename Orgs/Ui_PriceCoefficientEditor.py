# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\PriceCoefficientEditor.ui'
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

class Ui_PriceCoefficientDialog(object):
    def setupUi(self, PriceCoefficientDialog):
        PriceCoefficientDialog.setObjectName(_fromUtf8("PriceCoefficientDialog"))
        PriceCoefficientDialog.resize(314, 138)
        self.gridLayout = QtGui.QGridLayout(PriceCoefficientDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkPriceCoefficient = QtGui.QCheckBox(PriceCoefficientDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPriceCoefficient.sizePolicy().hasHeightForWidth())
        self.chkPriceCoefficient.setSizePolicy(sizePolicy)
        self.chkPriceCoefficient.setObjectName(_fromUtf8("chkPriceCoefficient"))
        self.gridLayout.addWidget(self.chkPriceCoefficient, 0, 0, 1, 1)
        self.edtPriceCoefficient = QtGui.QDoubleSpinBox(PriceCoefficientDialog)
        self.edtPriceCoefficient.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPriceCoefficient.sizePolicy().hasHeightForWidth())
        self.edtPriceCoefficient.setSizePolicy(sizePolicy)
        self.edtPriceCoefficient.setDecimals(4)
        self.edtPriceCoefficient.setMinimum(-10000.0)
        self.edtPriceCoefficient.setMaximum(10000.0)
        self.edtPriceCoefficient.setSingleStep(0.01)
        self.edtPriceCoefficient.setProperty("value", 1.0)
        self.edtPriceCoefficient.setObjectName(_fromUtf8("edtPriceCoefficient"))
        self.gridLayout.addWidget(self.edtPriceCoefficient, 0, 1, 1, 1)
        self.chkPriceExCoefficient = QtGui.QCheckBox(PriceCoefficientDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPriceExCoefficient.sizePolicy().hasHeightForWidth())
        self.chkPriceExCoefficient.setSizePolicy(sizePolicy)
        self.chkPriceExCoefficient.setObjectName(_fromUtf8("chkPriceExCoefficient"))
        self.gridLayout.addWidget(self.chkPriceExCoefficient, 1, 0, 1, 1)
        self.edtPriceExCoefficient = QtGui.QDoubleSpinBox(PriceCoefficientDialog)
        self.edtPriceExCoefficient.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPriceExCoefficient.sizePolicy().hasHeightForWidth())
        self.edtPriceExCoefficient.setSizePolicy(sizePolicy)
        self.edtPriceExCoefficient.setDecimals(4)
        self.edtPriceExCoefficient.setMinimum(-10000.0)
        self.edtPriceExCoefficient.setMaximum(10000.0)
        self.edtPriceExCoefficient.setSingleStep(0.01)
        self.edtPriceExCoefficient.setProperty("value", 1.0)
        self.edtPriceExCoefficient.setObjectName(_fromUtf8("edtPriceExCoefficient"))
        self.gridLayout.addWidget(self.edtPriceExCoefficient, 1, 1, 1, 1)
        self.chkPriceEx2Coefficient = QtGui.QCheckBox(PriceCoefficientDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPriceEx2Coefficient.sizePolicy().hasHeightForWidth())
        self.chkPriceEx2Coefficient.setSizePolicy(sizePolicy)
        self.chkPriceEx2Coefficient.setObjectName(_fromUtf8("chkPriceEx2Coefficient"))
        self.gridLayout.addWidget(self.chkPriceEx2Coefficient, 2, 0, 1, 1)
        self.edtPriceEx2Coefficient = QtGui.QDoubleSpinBox(PriceCoefficientDialog)
        self.edtPriceEx2Coefficient.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPriceEx2Coefficient.sizePolicy().hasHeightForWidth())
        self.edtPriceEx2Coefficient.setSizePolicy(sizePolicy)
        self.edtPriceEx2Coefficient.setDecimals(4)
        self.edtPriceEx2Coefficient.setMinimum(-10000.0)
        self.edtPriceEx2Coefficient.setMaximum(10000.0)
        self.edtPriceEx2Coefficient.setSingleStep(0.01)
        self.edtPriceEx2Coefficient.setProperty("value", 1.0)
        self.edtPriceEx2Coefficient.setObjectName(_fromUtf8("edtPriceEx2Coefficient"))
        self.gridLayout.addWidget(self.edtPriceEx2Coefficient, 2, 1, 1, 1)
        self.lblSelectionRows = QtGui.QLabel(PriceCoefficientDialog)
        self.lblSelectionRows.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblSelectionRows.setText(_fromUtf8(""))
        self.lblSelectionRows.setObjectName(_fromUtf8("lblSelectionRows"))
        self.gridLayout.addWidget(self.lblSelectionRows, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 23, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PriceCoefficientDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 2, 1, 1)

        self.retranslateUi(PriceCoefficientDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PriceCoefficientDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PriceCoefficientDialog.reject)
        QtCore.QObject.connect(self.chkPriceCoefficient, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtPriceCoefficient.setEnabled)
        QtCore.QObject.connect(self.chkPriceExCoefficient, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtPriceExCoefficient.setEnabled)
        QtCore.QObject.connect(self.chkPriceEx2Coefficient, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtPriceEx2Coefficient.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(PriceCoefficientDialog)
        PriceCoefficientDialog.setTabOrder(self.chkPriceCoefficient, self.edtPriceCoefficient)
        PriceCoefficientDialog.setTabOrder(self.edtPriceCoefficient, self.chkPriceExCoefficient)
        PriceCoefficientDialog.setTabOrder(self.chkPriceExCoefficient, self.edtPriceExCoefficient)
        PriceCoefficientDialog.setTabOrder(self.edtPriceExCoefficient, self.chkPriceEx2Coefficient)
        PriceCoefficientDialog.setTabOrder(self.chkPriceEx2Coefficient, self.edtPriceEx2Coefficient)
        PriceCoefficientDialog.setTabOrder(self.edtPriceEx2Coefficient, self.buttonBox)

    def retranslateUi(self, PriceCoefficientDialog):
        PriceCoefficientDialog.setWindowTitle(_translate("PriceCoefficientDialog", "Пересчет тарифов", None))
        self.chkPriceCoefficient.setText(_translate("PriceCoefficientDialog", "Коэффициент тарифа", None))
        self.chkPriceExCoefficient.setText(_translate("PriceCoefficientDialog", "Коэффициент расшир. тарифа", None))
        self.chkPriceEx2Coefficient.setText(_translate("PriceCoefficientDialog", "Коэффициент второго расшир. тарифа", None))

