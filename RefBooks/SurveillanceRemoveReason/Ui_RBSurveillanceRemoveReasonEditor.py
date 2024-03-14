# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Project\Samson\UP_s11\client\RefBooks\SurveillanceRemoveReason\RBSurveillanceRemoveReasonEditor.ui'
#
# Created: Wed May 18 15:17:33 2022
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

class Ui_RBSurveillanceRemoveReasonEditor(object):
    def setupUi(self, RBSurveillanceRemoveReasonEditor):
        RBSurveillanceRemoveReasonEditor.setObjectName(_fromUtf8("RBSurveillanceRemoveReasonEditor"))
        RBSurveillanceRemoveReasonEditor.resize(400, 145)
        RBSurveillanceRemoveReasonEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBSurveillanceRemoveReasonEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(RBSurveillanceRemoveReasonEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblName = QtGui.QLabel(RBSurveillanceRemoveReasonEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBSurveillanceRemoveReasonEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.label = QtGui.QLabel(RBSurveillanceRemoveReasonEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.cmbDispanser = CRBComboBox(RBSurveillanceRemoveReasonEditor)
        self.cmbDispanser.setObjectName(_fromUtf8("cmbDispanser"))
        self.gridLayout.addWidget(self.cmbDispanser, 2, 1, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBSurveillanceRemoveReasonEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBSurveillanceRemoveReasonEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBSurveillanceRemoveReasonEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBSurveillanceRemoveReasonEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBSurveillanceRemoveReasonEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBSurveillanceRemoveReasonEditor)
        RBSurveillanceRemoveReasonEditor.setTabOrder(self.edtCode, self.edtName)
        RBSurveillanceRemoveReasonEditor.setTabOrder(self.edtName, self.cmbDispanser)
        RBSurveillanceRemoveReasonEditor.setTabOrder(self.cmbDispanser, self.buttonBox)

    def retranslateUi(self, RBSurveillanceRemoveReasonEditor):
        RBSurveillanceRemoveReasonEditor.setWindowTitle(_translate("RBSurveillanceRemoveReasonEditor", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBSurveillanceRemoveReasonEditor", "&Код", None))
        self.lblName.setText(_translate("RBSurveillanceRemoveReasonEditor", "&Наименование", None))
        self.label.setText(_translate("RBSurveillanceRemoveReasonEditor", "Отметка ДН", None))

from library.crbcombobox import CRBComboBox
