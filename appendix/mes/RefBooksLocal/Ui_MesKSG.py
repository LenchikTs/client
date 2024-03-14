# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\mes\RefBooksLocal\MesKSG.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(519, 271)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.edtCode = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtCode.sizePolicy().hasHeightForWidth())
        self.edtCode.setSizePolicy(sizePolicy)
        self.edtCode.setMinimumSize(QtCore.QSize(100, 0))
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.horizontalLayout.addWidget(self.edtCode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)
        self.lblName = QtGui.QLabel(Dialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.lblType = QtGui.QLabel(Dialog)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 3, 0, 1, 1)
        self.lblVk = QtGui.QLabel(Dialog)
        self.lblVk.setObjectName(_fromUtf8("lblVk"))
        self.gridLayout.addWidget(self.lblVk, 4, 0, 1, 1)
        self.lblCode = QtGui.QLabel(Dialog)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 1, 0, 1, 1)
        self.cmbType = QtGui.QComboBox(Dialog)
        self.cmbType.setObjectName(_fromUtf8("cmbType"))
        self.gridLayout.addWidget(self.cmbType, 3, 2, 1, 1)
        self.edtName = QtGui.QLineEdit(Dialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 2, 2, 1, 1)
        self.edtVk = QtGui.QDoubleSpinBox(Dialog)
        self.edtVk.setObjectName(_fromUtf8("edtVk"))
        self.gridLayout.addWidget(self.edtVk, 4, 2, 1, 1)
        self.lblProf = QtGui.QLabel(Dialog)
        self.lblProf.setObjectName(_fromUtf8("lblProf"))
        self.gridLayout.addWidget(self.lblProf, 5, 0, 1, 1)
        self.edtProf = QtGui.QSpinBox(Dialog)
        self.edtProf.setMaximum(999999999)
        self.edtProf.setObjectName(_fromUtf8("edtProf"))
        self.gridLayout.addWidget(self.edtProf, 5, 2, 1, 1)
        self.edtManagementFactor = QtGui.QDoubleSpinBox(Dialog)
        self.edtManagementFactor.setObjectName(_fromUtf8("edtManagementFactor"))
        self.gridLayout.addWidget(self.edtManagementFactor, 6, 2, 1, 1)
        self.lblManagementFactor = QtGui.QLabel(Dialog)
        self.lblManagementFactor.setObjectName(_fromUtf8("lblManagementFactor"))
        self.gridLayout.addWidget(self.lblManagementFactor, 6, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(Dialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 7, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(Dialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 8, 0, 1, 1)
        self.edtBegDate = CDateEdit(Dialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 7, 2, 1, 1)
        self.edtEndDate = CDateEdit(Dialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 8, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtCode, self.edtName)
        Dialog.setTabOrder(self.edtName, self.cmbType)
        Dialog.setTabOrder(self.cmbType, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Препараты крови", None))
        self.lblName.setText(_translate("Dialog", "Наименование", None))
        self.lblType.setText(_translate("Dialog", "Тип", None))
        self.lblVk.setText(_translate("Dialog", "Весовой коэффициент затратоемкости", None))
        self.lblCode.setText(_translate("Dialog", "Код", None))
        self.lblProf.setText(_translate("Dialog", "Код клинико-профильной группы", None))
        self.lblManagementFactor.setText(_translate("Dialog", "Управленческий коэффициент", None))
        self.lblBegDate.setText(_translate("Dialog", "Начало действия", None))
        self.lblEndDate.setText(_translate("Dialog", "Окончание действия", None))

from library.DateEdit import CDateEdit
