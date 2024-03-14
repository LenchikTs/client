# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Stock\Inventory.ui'
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

class Ui_InventoryDialog(object):
    def setupUi(self, InventoryDialog):
        InventoryDialog.setObjectName(_fromUtf8("InventoryDialog"))
        InventoryDialog.resize(600, 500)
        self.gridLayout = QtGui.QGridLayout(InventoryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblSupplierPerson = QtGui.QLabel(InventoryDialog)
        self.lblSupplierPerson.setObjectName(_fromUtf8("lblSupplierPerson"))
        self.gridLayout.addWidget(self.lblSupplierPerson, 5, 0, 1, 1)
        self.edtNote = QtGui.QLineEdit(InventoryDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 6, 1, 1, 4)
        self.cmbSupplier = CStorageComboBox(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplier.sizePolicy().hasHeightForWidth())
        self.cmbSupplier.setSizePolicy(sizePolicy)
        self.cmbSupplier.setObjectName(_fromUtf8("cmbSupplier"))
        self.gridLayout.addWidget(self.cmbSupplier, 4, 1, 1, 4)
        self.lblReasonDate = QtGui.QLabel(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReasonDate.sizePolicy().hasHeightForWidth())
        self.lblReasonDate.setSizePolicy(sizePolicy)
        self.lblReasonDate.setObjectName(_fromUtf8("lblReasonDate"))
        self.gridLayout.addWidget(self.lblReasonDate, 2, 2, 1, 1)
        self.edtTime = QtGui.QTimeEdit(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTime.sizePolicy().hasHeightForWidth())
        self.edtTime.setSizePolicy(sizePolicy)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 1, 4, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InventoryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 5)
        self.tblItems = CInventoryInDocTableView(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblItems.sizePolicy().hasHeightForWidth())
        self.tblItems.setSizePolicy(sizePolicy)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 7, 0, 1, 5)
        self.edtReason = QtGui.QLineEdit(InventoryDialog)
        self.edtReason.setObjectName(_fromUtf8("edtReason"))
        self.gridLayout.addWidget(self.edtReason, 2, 1, 1, 1)
        self.lblSupplier = QtGui.QLabel(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSupplier.sizePolicy().hasHeightForWidth())
        self.lblSupplier.setSizePolicy(sizePolicy)
        self.lblSupplier.setObjectName(_fromUtf8("lblSupplier"))
        self.gridLayout.addWidget(self.lblSupplier, 4, 0, 1, 1)
        self.cmbSupplierPerson = CPersonComboBoxEx(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplierPerson.sizePolicy().hasHeightForWidth())
        self.cmbSupplierPerson.setSizePolicy(sizePolicy)
        self.cmbSupplierPerson.setObjectName(_fromUtf8("cmbSupplierPerson"))
        self.gridLayout.addWidget(self.cmbSupplierPerson, 5, 1, 1, 4)
        self.lblDate = QtGui.QLabel(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 1, 2, 1, 1)
        self.lblNote = QtGui.QLabel(InventoryDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 6, 0, 1, 1)
        self.lblReason = QtGui.QLabel(InventoryDialog)
        self.lblReason.setObjectName(_fromUtf8("lblReason"))
        self.gridLayout.addWidget(self.lblReason, 2, 0, 1, 1)
        self.edtDate = CDateEdit(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 1, 3, 1, 1)
        self.edtReasonDate = CDateEdit(InventoryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtReasonDate.sizePolicy().hasHeightForWidth())
        self.edtReasonDate.setSizePolicy(sizePolicy)
        self.edtReasonDate.setObjectName(_fromUtf8("edtReasonDate"))
        self.gridLayout.addWidget(self.edtReasonDate, 2, 3, 1, 1)
        self.edtNumber = QtGui.QLineEdit(InventoryDialog)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridLayout.addWidget(self.edtNumber, 1, 1, 1, 1)
        self.lblNumber = QtGui.QLabel(InventoryDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridLayout.addWidget(self.lblNumber, 1, 0, 1, 1)
        self.lblSummaryInfo = QtGui.QLabel(InventoryDialog)
        self.lblSummaryInfo.setText(_fromUtf8(""))
        self.lblSummaryInfo.setObjectName(_fromUtf8("lblSummaryInfo"))
        self.gridLayout.addWidget(self.lblSummaryInfo, 8, 0, 1, 5)
        self.lblSupplierPerson.setBuddy(self.cmbSupplierPerson)
        self.lblReasonDate.setBuddy(self.edtReasonDate)
        self.lblSupplier.setBuddy(self.cmbSupplier)
        self.lblDate.setBuddy(self.edtDate)
        self.lblNote.setBuddy(self.edtNote)
        self.lblReason.setBuddy(self.edtReason)
        self.lblNumber.setBuddy(self.edtNumber)

        self.retranslateUi(InventoryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InventoryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InventoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InventoryDialog)
        InventoryDialog.setTabOrder(self.edtNumber, self.edtDate)
        InventoryDialog.setTabOrder(self.edtDate, self.edtTime)
        InventoryDialog.setTabOrder(self.edtTime, self.edtReason)
        InventoryDialog.setTabOrder(self.edtReason, self.edtReasonDate)
        InventoryDialog.setTabOrder(self.edtReasonDate, self.cmbSupplier)
        InventoryDialog.setTabOrder(self.cmbSupplier, self.cmbSupplierPerson)
        InventoryDialog.setTabOrder(self.cmbSupplierPerson, self.edtNote)
        InventoryDialog.setTabOrder(self.edtNote, self.tblItems)
        InventoryDialog.setTabOrder(self.tblItems, self.buttonBox)

    def retranslateUi(self, InventoryDialog):
        InventoryDialog.setWindowTitle(_translate("InventoryDialog", "Акт инвентаризации ЛСиИМН", None))
        self.lblSupplierPerson.setText(_translate("InventoryDialog", "Ответственный", None))
        self.lblReasonDate.setText(_translate("InventoryDialog", "Дата основания", None))
        self.edtTime.setDisplayFormat(_translate("InventoryDialog", "HH:mm", None))
        self.lblSupplier.setText(_translate("InventoryDialog", "Подразделение", None))
        self.lblDate.setText(_translate("InventoryDialog", "Дата", None))
        self.lblNote.setText(_translate("InventoryDialog", "Примечания", None))
        self.lblReason.setText(_translate("InventoryDialog", "Основание", None))
        self.lblNumber.setText(_translate("InventoryDialog", "Номер", None))

from Orgs.OrgStructComboBoxes import CStorageComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Stock.InventoryInDocTableView import CInventoryInDocTableView
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InventoryDialog = QtGui.QDialog()
    ui = Ui_InventoryDialog()
    ui.setupUi(InventoryDialog)
    InventoryDialog.show()
    sys.exit(app.exec_())

