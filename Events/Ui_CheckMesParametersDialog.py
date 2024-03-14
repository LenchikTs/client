# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\CheckMesParametersDialog.ui'
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

class Ui_CheckMesParametersDialog(object):
    def setupUi(self, CheckMesParametersDialog):
        CheckMesParametersDialog.setObjectName(_fromUtf8("CheckMesParametersDialog"))
        CheckMesParametersDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        CheckMesParametersDialog.resize(528, 137)
        CheckMesParametersDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(CheckMesParametersDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.chkMedicamentsSection = QtGui.QCheckBox(CheckMesParametersDialog)
        self.chkMedicamentsSection.setObjectName(_fromUtf8("chkMedicamentsSection"))
        self.gridlayout.addWidget(self.chkMedicamentsSection, 6, 0, 1, 1)
        self.chkServiceNoMes = QtGui.QCheckBox(CheckMesParametersDialog)
        self.chkServiceNoMes.setObjectName(_fromUtf8("chkServiceNoMes"))
        self.gridlayout.addWidget(self.chkServiceNoMes, 8, 0, 1, 1)
        self.chkServiceMes = QtGui.QCheckBox(CheckMesParametersDialog)
        self.chkServiceMes.setEnabled(False)
        self.chkServiceMes.setObjectName(_fromUtf8("chkServiceMes"))
        self.gridlayout.addWidget(self.chkServiceMes, 1, 0, 1, 2)
        self.chkMandatoryServiceMes = QtGui.QCheckBox(CheckMesParametersDialog)
        self.chkMandatoryServiceMes.setObjectName(_fromUtf8("chkMandatoryServiceMes"))
        self.gridlayout.addWidget(self.chkMandatoryServiceMes, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(CheckMesParametersDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 10, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 9, 0, 1, 1)

        self.retranslateUi(CheckMesParametersDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CheckMesParametersDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CheckMesParametersDialog.reject)
        QtCore.QObject.connect(self.chkMandatoryServiceMes, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkServiceMes.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(CheckMesParametersDialog)
        CheckMesParametersDialog.setTabOrder(self.chkMandatoryServiceMes, self.chkServiceMes)
        CheckMesParametersDialog.setTabOrder(self.chkServiceMes, self.chkMedicamentsSection)
        CheckMesParametersDialog.setTabOrder(self.chkMedicamentsSection, self.chkServiceNoMes)
        CheckMesParametersDialog.setTabOrder(self.chkServiceNoMes, self.buttonBox)

    def retranslateUi(self, CheckMesParametersDialog):
        CheckMesParametersDialog.setWindowTitle(_translate("CheckMesParametersDialog", "параметры отчёта", None))
        self.chkMedicamentsSection.setText(_translate("CheckMesParametersDialog", "Выводить данные о лекарственных средствах", None))
        self.chkServiceNoMes.setText(_translate("CheckMesParametersDialog", "Учитывать все услуги не входящие в стандарт", None))
        self.chkServiceMes.setText(_translate("CheckMesParametersDialog", "Учитывать все услуги входящие в стандарт", None))
        self.chkMandatoryServiceMes.setText(_translate("CheckMesParametersDialog", "Учитывать только обязательные требования стандарта", None))

