# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ClientDocumentTrackingEditor.ui'
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
        ItemEditorDialog.resize(452, 518)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDocumenType = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDocumenType.sizePolicy().hasHeightForWidth())
        self.lblDocumenType.setSizePolicy(sizePolicy)
        self.lblDocumenType.setObjectName(_fromUtf8("lblDocumenType"))
        self.gridLayout.addWidget(self.lblDocumenType, 0, 0, 1, 1)
        self.lblDocumentNumber = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDocumentNumber.sizePolicy().hasHeightForWidth())
        self.lblDocumentNumber.setSizePolicy(sizePolicy)
        self.lblDocumentNumber.setObjectName(_fromUtf8("lblDocumentNumber"))
        self.gridLayout.addWidget(self.lblDocumentNumber, 1, 0, 1, 1)
        self.edtDocumentNumber = QtGui.QLineEdit(ItemEditorDialog)
        self.edtDocumentNumber.setObjectName(_fromUtf8("edtDocumentNumber"))
        self.gridLayout.addWidget(self.edtDocumentNumber, 1, 1, 1, 2)
        self.lblDocumentDate = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDocumentDate.sizePolicy().hasHeightForWidth())
        self.lblDocumentDate.setSizePolicy(sizePolicy)
        self.lblDocumentDate.setObjectName(_fromUtf8("lblDocumentDate"))
        self.gridLayout.addWidget(self.lblDocumentDate, 2, 0, 1, 1)
        self.edtDocumentDate = CDateEdit(ItemEditorDialog)
        self.edtDocumentDate.setCalendarPopup(True)
        self.edtDocumentDate.setObjectName(_fromUtf8("edtDocumentDate"))
        self.gridLayout.addWidget(self.edtDocumentDate, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(173, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.lblDocumentLocationHistory = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDocumentLocationHistory.sizePolicy().hasHeightForWidth())
        self.lblDocumentLocationHistory.setSizePolicy(sizePolicy)
        self.lblDocumentLocationHistory.setObjectName(_fromUtf8("lblDocumentLocationHistory"))
        self.gridLayout.addWidget(self.lblDocumentLocationHistory, 3, 0, 1, 1)
        self.tblDocumentLocationHistory = CInDocTableView(ItemEditorDialog)
        self.tblDocumentLocationHistory.setObjectName(_fromUtf8("tblDocumentLocationHistory"))
        self.gridLayout.addWidget(self.tblDocumentLocationHistory, 4, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.cmbDocumentType = CRBComboBox(ItemEditorDialog)
        self.cmbDocumentType.setObjectName(_fromUtf8("cmbDocumentType"))
        self.gridLayout.addWidget(self.cmbDocumentType, 0, 1, 1, 2)
        self.lblDocumenType.setBuddy(self.cmbDocumentType)
        self.lblDocumentNumber.setBuddy(self.edtDocumentNumber)
        self.lblDocumentDate.setBuddy(self.edtDocumentDate)

        self.retranslateUi(ItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.cmbDocumentType, self.edtDocumentNumber)
        ItemEditorDialog.setTabOrder(self.edtDocumentNumber, self.edtDocumentDate)
        ItemEditorDialog.setTabOrder(self.edtDocumentDate, self.tblDocumentLocationHistory)
        ItemEditorDialog.setTabOrder(self.tblDocumentLocationHistory, self.buttonBox)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.lblDocumenType.setText(_translate("ItemEditorDialog", "Вид документа", None))
        self.lblDocumentNumber.setText(_translate("ItemEditorDialog", "Номер документа", None))
        self.lblDocumentDate.setText(_translate("ItemEditorDialog", "Дата документа", None))
        self.lblDocumentLocationHistory.setText(_translate("ItemEditorDialog", "История хранения документа:", None))

from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
