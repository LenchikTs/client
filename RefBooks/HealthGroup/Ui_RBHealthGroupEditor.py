# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\samson\RefBooks\HealthGroup\RBHealthGroupEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(371, 210)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(ItemEditorDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMainInfo = QtGui.QWidget()
        self.tabMainInfo.setObjectName(_fromUtf8("tabMainInfo"))
        self.gridLayout = QtGui.QGridLayout(self.tabMainInfo)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtAgeTo = QtGui.QSpinBox(self.tabMainInfo)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setProperty("value", 150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 4, 5, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(self.tabMainInfo)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 4, 2, 1, 1)
        self.lblAge = QtGui.QLabel(self.tabMainInfo)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.lblName = QtGui.QLabel(self.tabMainInfo)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 3, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(self.tabMainInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 2, 0, 1, 1)
        self.lblAge_3 = QtGui.QLabel(self.tabMainInfo)
        self.lblAge_3.setObjectName(_fromUtf8("lblAge_3"))
        self.gridLayout.addWidget(self.lblAge_3, 4, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 7, 1, 1)
        self.lblAge_2 = QtGui.QLabel(self.tabMainInfo)
        self.lblAge_2.setObjectName(_fromUtf8("lblAge_2"))
        self.gridLayout.addWidget(self.lblAge_2, 4, 3, 1, 2)
        self.edtName = QtGui.QLineEdit(self.tabMainInfo)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 2, 1, 6)
        self.edtCode = QtGui.QLineEdit(self.tabMainInfo)
        self.edtCode.setMaxLength(8)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 2, 1, 6)
        self.edtEndDate = CDateEdit(self.tabMainInfo)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 3, 2, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 6, 1, 2)
        self.edtBegDate = CDateEdit(self.tabMainInfo)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 2, 2, 1, 4)
        self.tabWidget.addTab(self.tabMainInfo, _fromUtf8(""))
        self.tabIdentInfo = QtGui.QWidget()
        self.tabIdentInfo.setObjectName(_fromUtf8("tabIdentInfo"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabIdentInfo)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblIdentification = CInDocTableView(self.tabIdentInfo)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_2.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentInfo, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(ItemEditorDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.lblAge.setText(_translate("ItemEditorDialog", "Возраст с", None))
        self.lblName.setText(_translate("ItemEditorDialog", "Название", None))
        self.lblCode.setText(_translate("ItemEditorDialog", "&Код", None))
        self.lblEndDate.setText(_translate("ItemEditorDialog", "Дата окончания", None))
        self.lblBegDate.setText(_translate("ItemEditorDialog", "Дата начала", None))
        self.lblAge_3.setText(_translate("ItemEditorDialog", "лет", None))
        self.lblAge_2.setText(_translate("ItemEditorDialog", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("ItemEditorDialog", "dd.MM.yyyy", None))
        self.edtBegDate.setDisplayFormat(_translate("ItemEditorDialog", "dd.MM.yyyy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMainInfo), _translate("ItemEditorDialog", "Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentInfo), _translate("ItemEditorDialog", "Идентификация", None))

from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
