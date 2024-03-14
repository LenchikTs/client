# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\mes\RefBooksLocal\RBService.ui'
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
        Dialog.resize(519, 295)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
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
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.edtName = QtGui.QLineEdit(Dialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.edtName)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cmbType = CRBComboBox(Dialog)
        self.cmbType.setObjectName(_fromUtf8("cmbType"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmbType)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.edtDoctor = QtGui.QDoubleSpinBox(Dialog)
        self.edtDoctor.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtDoctor.setObjectName(_fromUtf8("edtDoctor"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.edtDoctor)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.edtParamedical = QtGui.QDoubleSpinBox(Dialog)
        self.edtParamedical.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtParamedical.setObjectName(_fromUtf8("edtParamedical"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.edtParamedical)
        self.tblServices = CInDocTableView(Dialog)
        self.tblServices.setObjectName(_fromUtf8("tblServices"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.tblServices)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtCode, self.edtName)
        Dialog.setTabOrder(self.edtName, self.cmbType)
        Dialog.setTabOrder(self.cmbType, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Услуги", None))
        self.label.setText(_translate("Dialog", "Код", None))
        self.label_2.setText(_translate("Dialog", "Наименование", None))
        self.label_3.setText(_translate("Dialog", "Группа услуг", None))
        self.label_4.setText(_translate("Dialog", "УЕТ врача", None))
        self.label_5.setText(_translate("Dialog", "УЕТ средний", None))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
