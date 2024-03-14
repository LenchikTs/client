# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\mes\RefBooksLocal\RBMedicament.ui'
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
        Dialog.resize(519, 274)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 7)
        self.edtName = QtGui.QLineEdit(Dialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
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
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(Dialog)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 7, 2, 1, 1)
        self.cmbForm = CRBComboBox(Dialog)
        self.cmbForm.setObjectName(_fromUtf8("cmbForm"))
        self.gridLayout.addWidget(self.cmbForm, 6, 2, 1, 1)
        self.edtPackPrice = QtGui.QLineEdit(Dialog)
        self.edtPackPrice.setObjectName(_fromUtf8("edtPackPrice"))
        self.gridLayout.addWidget(self.edtPackPrice, 8, 2, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.edtTradeName = QtGui.QLineEdit(Dialog)
        self.edtTradeName.setObjectName(_fromUtf8("edtTradeName"))
        self.gridLayout.addWidget(self.edtTradeName, 3, 2, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.edtDosage = QtGui.QLineEdit(Dialog)
        self.edtDosage.setObjectName(_fromUtf8("edtDosage"))
        self.gridLayout.addWidget(self.edtDosage, 4, 2, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)
        self.edtForm = QtGui.QLineEdit(Dialog)
        self.edtForm.setObjectName(_fromUtf8("edtForm"))
        self.gridLayout.addWidget(self.edtForm, 5, 2, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)
        self.edtUnitPrice = QtGui.QLineEdit(Dialog)
        self.edtUnitPrice.setObjectName(_fromUtf8("edtUnitPrice"))
        self.gridLayout.addWidget(self.edtUnitPrice, 9, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtCode, self.edtName)
        Dialog.setTabOrder(self.edtName, self.edtTradeName)
        Dialog.setTabOrder(self.edtTradeName, self.edtDosage)
        Dialog.setTabOrder(self.edtDosage, self.edtForm)
        Dialog.setTabOrder(self.edtForm, self.cmbForm)
        Dialog.setTabOrder(self.cmbForm, self.spinBox)
        Dialog.setTabOrder(self.spinBox, self.edtPackPrice)
        Dialog.setTabOrder(self.edtPackPrice, self.edtUnitPrice)
        Dialog.setTabOrder(self.edtUnitPrice, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Медикаменты", None))
        self.label.setText(_translate("Dialog", "Код", None))
        self.label_2.setText(_translate("Dialog", "Наименование", None))
        self.label_3.setText(_translate("Dialog", "Лекарственная форма", None))
        self.label_4.setText(_translate("Dialog", "Кол.-во единиц в упаковке", None))
        self.label_5.setText(_translate("Dialog", "Стоимость упаковки", None))
        self.label_6.setText(_translate("Dialog", "Торговое наименование", None))
        self.label_7.setText(_translate("Dialog", "Дозировка", None))
        self.label_8.setText(_translate("Dialog", "Форма выпуска", None))
        self.label_9.setText(_translate("Dialog", "Стоимость единицы", None))

from library.crbcombobox import CRBComboBox
