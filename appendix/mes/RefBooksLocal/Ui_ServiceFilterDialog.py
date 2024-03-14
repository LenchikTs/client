# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\mes\RefBooksLocal\ServiceFilterDialog.ui'
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

class Ui_ServiceFilterDialog(object):
    def setupUi(self, ServiceFilterDialog):
        ServiceFilterDialog.setObjectName(_fromUtf8("ServiceFilterDialog"))
        ServiceFilterDialog.resize(400, 173)
        ServiceFilterDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ServiceFilterDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbServiceGroup = CRBComboBox(ServiceFilterDialog)
        self.cmbServiceGroup.setObjectName(_fromUtf8("cmbServiceGroup"))
        self.gridLayout.addWidget(self.cmbServiceGroup, 3, 1, 1, 1)
        self.edtDoctorWTU = QtGui.QDoubleSpinBox(ServiceFilterDialog)
        self.edtDoctorWTU.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtDoctorWTU.setObjectName(_fromUtf8("edtDoctorWTU"))
        self.gridLayout.addWidget(self.edtDoctorWTU, 5, 1, 1, 1)
        self.lblParamedicalWTU = QtGui.QLabel(ServiceFilterDialog)
        self.lblParamedicalWTU.setObjectName(_fromUtf8("lblParamedicalWTU"))
        self.gridLayout.addWidget(self.lblParamedicalWTU, 7, 0, 1, 1)
        self.lblServiceGroup = QtGui.QLabel(ServiceFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblServiceGroup.sizePolicy().hasHeightForWidth())
        self.lblServiceGroup.setSizePolicy(sizePolicy)
        self.lblServiceGroup.setObjectName(_fromUtf8("lblServiceGroup"))
        self.gridLayout.addWidget(self.lblServiceGroup, 3, 0, 1, 1)
        self.lblDoctorWTU = QtGui.QLabel(ServiceFilterDialog)
        self.lblDoctorWTU.setObjectName(_fromUtf8("lblDoctorWTU"))
        self.gridLayout.addWidget(self.lblDoctorWTU, 5, 0, 1, 1)
        self.lblName = QtGui.QLabel(ServiceFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ServiceFilterDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 2)
        self.edtCode = QtGui.QLineEdit(ServiceFilterDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 1, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(ServiceFilterDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 11, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 9, 1, 1, 1)
        self.lblCode = QtGui.QLabel(ServiceFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 1, 0, 1, 1)
        self.edtParamedicalWTU = QtGui.QDoubleSpinBox(ServiceFilterDialog)
        self.edtParamedicalWTU.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtParamedicalWTU.setObjectName(_fromUtf8("edtParamedicalWTU"))
        self.gridLayout.addWidget(self.edtParamedicalWTU, 7, 1, 1, 1)
        self.lblServiceGroup.setBuddy(self.cmbServiceGroup)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(ServiceFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ServiceFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ServiceFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ServiceFilterDialog)
        ServiceFilterDialog.setTabOrder(self.edtCode, self.edtName)
        ServiceFilterDialog.setTabOrder(self.edtName, self.cmbServiceGroup)
        ServiceFilterDialog.setTabOrder(self.cmbServiceGroup, self.buttonBox)

    def retranslateUi(self, ServiceFilterDialog):
        ServiceFilterDialog.setWindowTitle(_translate("ServiceFilterDialog", "Фильтр услуг", None))
        self.lblParamedicalWTU.setText(_translate("ServiceFilterDialog", "УЕТ средний", None))
        self.lblServiceGroup.setText(_translate("ServiceFilterDialog", "&Группа", None))
        self.lblDoctorWTU.setText(_translate("ServiceFilterDialog", "УЕТ врача", None))
        self.lblName.setText(_translate("ServiceFilterDialog", "Наименование", None))
        self.lblCode.setText(_translate("ServiceFilterDialog", "Код", None))

from library.crbcombobox import CRBComboBox
