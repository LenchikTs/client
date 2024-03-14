# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_stock\RefBooks\AnatomicalLocalizations\EditDialog.ui'
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

class Ui_EditDialog(object):
    def setupUi(self, EditDialog):
        EditDialog.setObjectName(_fromUtf8("EditDialog"))
        EditDialog.resize(631, 381)
        self.verticalLayout = QtGui.QVBoxLayout(EditDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(EditDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName(_fromUtf8("tabGeneral"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabGeneral)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblCode = QtGui.QLabel(self.tabGeneral)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_2.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabGeneral)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_2.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(self.tabGeneral)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 1, 0, 1, 1)
        self.chkLaterality = QtGui.QCheckBox(self.tabGeneral)
        self.chkLaterality.setObjectName(_fromUtf8("chkLaterality"))
        self.gridLayout_2.addWidget(self.chkLaterality, 6, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabGeneral)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_2.addWidget(self.edtName, 1, 1, 1, 1)
        self.edtLatinName = QtGui.QLineEdit(self.tabGeneral)
        self.edtLatinName.setObjectName(_fromUtf8("edtLatinName"))
        self.gridLayout_2.addWidget(self.edtLatinName, 2, 1, 1, 1)
        self.lblLatinName = QtGui.QLabel(self.tabGeneral)
        self.lblLatinName.setObjectName(_fromUtf8("lblLatinName"))
        self.gridLayout_2.addWidget(self.lblLatinName, 2, 0, 1, 1)
        self.lblGroup = QtGui.QLabel(self.tabGeneral)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.gridLayout_2.addWidget(self.lblGroup, 3, 0, 1, 1)
        self.lblArea = QtGui.QLabel(self.tabGeneral)
        self.lblArea.setObjectName(_fromUtf8("lblArea"))
        self.gridLayout_2.addWidget(self.lblArea, 4, 0, 1, 1)
        self.cmbGroup = CRBComboBox(self.tabGeneral)
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.gridLayout_2.addWidget(self.cmbGroup, 3, 1, 1, 1)
        self.lblSynonyms = QtGui.QLabel(self.tabGeneral)
        self.lblSynonyms.setObjectName(_fromUtf8("lblSynonyms"))
        self.gridLayout_2.addWidget(self.lblSynonyms, 5, 0, 1, 1)
        self.edtArea = QtGui.QLineEdit(self.tabGeneral)
        self.edtArea.setObjectName(_fromUtf8("edtArea"))
        self.gridLayout_2.addWidget(self.edtArea, 4, 1, 1, 1)
        self.edtSynonyms = QtGui.QLineEdit(self.tabGeneral)
        self.edtSynonyms.setObjectName(_fromUtf8("edtSynonyms"))
        self.gridLayout_2.addWidget(self.edtSynonyms, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 2)
        self.tabWidget.addTab(self.tabGeneral, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tabIdentification)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.horizontalLayout.addWidget(self.tblIdentification)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(EditDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditDialog)

    def retranslateUi(self, EditDialog):
        self.lblCode.setText(_translate("EditDialog", "Код", None))
        self.lblName.setText(_translate("EditDialog", "Наименование", None))
        self.chkLaterality.setText(_translate("EditDialog", "Латеральность", None))
        self.lblLatinName.setText(_translate("EditDialog", "Английское наименование", None))
        self.lblGroup.setText(_translate("EditDialog", "Группа", None))
        self.lblArea.setText(_translate("EditDialog", "Анатомическая область", None))
        self.lblSynonyms.setText(_translate("EditDialog", "Синонимы", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), _translate("EditDialog", "Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("EditDialog", "Идентификация", None))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
