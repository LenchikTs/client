# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\PacsPage.ui'
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

class Ui_pacsPage(object):
    def setupUi(self, pacsPage):
        pacsPage.setObjectName(_fromUtf8("pacsPage"))
        pacsPage.resize(400, 300)
        pacsPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(pacsPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPacsType = QtGui.QLabel(pacsPage)
        self.lblPacsType.setObjectName(_fromUtf8("lblPacsType"))
        self.gridLayout.addWidget(self.lblPacsType, 0, 0, 1, 1)
        self.cmbPacsType = QtGui.QComboBox(pacsPage)
        self.cmbPacsType.setObjectName(_fromUtf8("cmbPacsType"))
        self.cmbPacsType.addItem(_fromUtf8(""))
        self.cmbPacsType.addItem(_fromUtf8(""))
        self.cmbPacsType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPacsType, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(164, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblPacsParams = QtGui.QLabel(pacsPage)
        self.lblPacsParams.setObjectName(_fromUtf8("lblPacsParams"))
        self.gridLayout.addWidget(self.lblPacsParams, 1, 0, 1, 1)
        self.edtPacsParams = QtGui.QLineEdit(pacsPage)
        self.edtPacsParams.setObjectName(_fromUtf8("edtPacsParams"))
        self.gridLayout.addWidget(self.edtPacsParams, 1, 1, 1, 2)
        self.lblPacsWado = QtGui.QLabel(pacsPage)
        self.lblPacsWado.setEnabled(False)
        self.lblPacsWado.setObjectName(_fromUtf8("lblPacsWado"))
        self.gridLayout.addWidget(self.lblPacsWado, 2, 0, 1, 1)
        self.edtPacsWado = QtGui.QLineEdit(pacsPage)
        self.edtPacsWado.setEnabled(False)
        self.edtPacsWado.setObjectName(_fromUtf8("edtPacsWado"))
        self.gridLayout.addWidget(self.edtPacsWado, 2, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 214, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.lblPacsType.setBuddy(self.cmbPacsType)
        self.lblPacsParams.setBuddy(self.edtPacsParams)
        self.lblPacsWado.setBuddy(self.edtPacsWado)

        self.retranslateUi(pacsPage)
        QtCore.QMetaObject.connectSlotsByName(pacsPage)
        pacsPage.setTabOrder(self.cmbPacsType, self.edtPacsParams)
        pacsPage.setTabOrder(self.edtPacsParams, self.edtPacsWado)

    def retranslateUi(self, pacsPage):
        pacsPage.setWindowTitle(_translate("pacsPage", "PACS", None))
        self.lblPacsType.setText(_translate("pacsPage", "&Тип", None))
        self.cmbPacsType.setItemText(0, _translate("pacsPage", "Выполнить команду", None))
        self.cmbPacsType.setItemText(1, _translate("pacsPage", "Weasis", None))
        self.cmbPacsType.setItemText(2, _translate("pacsPage", "Открыть браузер", None))
        self.lblPacsParams.setText(_translate("pacsPage", "&Параметры", None))
        self.lblPacsWado.setText(_translate("pacsPage", "&Wado", None))

