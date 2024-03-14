# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\RefBooks\QuotaType\QuotaTypeEditor.ui'
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

class Ui_QuotaTypeEditorDialog(object):
    def setupUi(self, QuotaTypeEditorDialog):
        QuotaTypeEditorDialog.setObjectName(_fromUtf8("QuotaTypeEditorDialog"))
        QuotaTypeEditorDialog.resize(629, 381)
        QuotaTypeEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(QuotaTypeEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(QuotaTypeEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.tabWidget = QtGui.QTabWidget(QuotaTypeEditorDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabMain)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(251, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 7, 3, 1, 2)
        self.lblClass = QtGui.QLabel(self.tabMain)
        self.lblClass.setObjectName(_fromUtf8("lblClass"))
        self.gridLayout_2.addWidget(self.lblClass, 0, 0, 1, 1)
        self.lblGroup = QtGui.QLabel(self.tabMain)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.gridLayout_2.addWidget(self.lblGroup, 1, 0, 1, 1)
        self.edtName = QtGui.QTextEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_2.addWidget(self.edtName, 4, 2, 2, 3)
        self.lblBegDate = QtGui.QLabel(self.tabMain)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout_2.addWidget(self.lblBegDate, 6, 0, 1, 2)
        self.lblRegionalCode = QtGui.QLabel(self.tabMain)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridLayout_2.addWidget(self.lblRegionalCode, 3, 0, 1, 2)
        self.lblName = QtGui.QLabel(self.tabMain)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 4, 0, 1, 2)
        self.edtBegDate = CDateEdit(self.tabMain)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout_2.addWidget(self.edtBegDate, 6, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(251, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 6, 3, 1, 2)
        self.lblEndDate = QtGui.QLabel(self.tabMain)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout_2.addWidget(self.lblEndDate, 7, 0, 1, 2)
        self.lblCode = QtGui.QLabel(self.tabMain)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_2.addWidget(self.lblCode, 2, 0, 1, 1)
        self.edtEndDate = CDateEdit(self.tabMain)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout_2.addWidget(self.edtEndDate, 7, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 142, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 5, 1, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_2.addWidget(self.edtCode, 2, 2, 1, 3)
        self.edtRegionalCode = QtGui.QLineEdit(self.tabMain)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridLayout_2.addWidget(self.edtRegionalCode, 3, 2, 1, 3)
        self.cmbGroup = CRBComboBox(self.tabMain)
        self.cmbGroup.setEnabled(False)
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.gridLayout_2.addWidget(self.cmbGroup, 1, 2, 1, 3)
        self.cmbClass = QtGui.QComboBox(self.tabMain)
        self.cmbClass.setEnabled(False)
        self.cmbClass.setObjectName(_fromUtf8("cmbClass"))
        self.gridLayout_2.addWidget(self.cmbClass, 0, 2, 1, 3)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 3)
        self.tabWidget.addTab(self.tabMain, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_3.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.lblClass.setBuddy(self.cmbClass)
        self.lblGroup.setBuddy(self.cmbGroup)
        self.lblBegDate.setBuddy(self.edtName)
        self.lblRegionalCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblEndDate.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(QuotaTypeEditorDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuotaTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuotaTypeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QuotaTypeEditorDialog)

    def retranslateUi(self, QuotaTypeEditorDialog):
        QuotaTypeEditorDialog.setWindowTitle(_translate("QuotaTypeEditorDialog", "Dialog", None))
        self.lblClass.setText(_translate("QuotaTypeEditorDialog", "&Класс", None))
        self.lblGroup.setText(_translate("QuotaTypeEditorDialog", "&Вид", None))
        self.lblBegDate.setText(_translate("QuotaTypeEditorDialog", "Действует с", None))
        self.lblRegionalCode.setText(_translate("QuotaTypeEditorDialog", "Региональный код", None))
        self.lblName.setText(_translate("QuotaTypeEditorDialog", "&Наименование", None))
        self.edtBegDate.setDisplayFormat(_translate("QuotaTypeEditorDialog", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("QuotaTypeEditorDialog", "Действует по", None))
        self.lblCode.setText(_translate("QuotaTypeEditorDialog", "&Код", None))
        self.edtEndDate.setDisplayFormat(_translate("QuotaTypeEditorDialog", "dd.MM.yyyy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("QuotaTypeEditorDialog", "Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("QuotaTypeEditorDialog", "Идентификация", None))

from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
