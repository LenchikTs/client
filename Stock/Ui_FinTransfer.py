# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Stock\FinTransfer.ui'
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

class Ui_FinTransferDialog(object):
    def setupUi(self, FinTransferDialog):
        FinTransferDialog.setObjectName(_fromUtf8("FinTransferDialog"))
        FinTransferDialog.resize(530, 377)
        self.gridLayout = QtGui.QGridLayout(FinTransferDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtDate = CDateEdit(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 4, 1, 1)
        self.lblReason = QtGui.QLabel(FinTransferDialog)
        self.lblReason.setObjectName(_fromUtf8("lblReason"))
        self.gridLayout.addWidget(self.lblReason, 1, 0, 1, 1)
        self.lblNumber = QtGui.QLabel(FinTransferDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridLayout.addWidget(self.lblNumber, 0, 0, 1, 1)
        self.cmbSupplier = CStorageComboBox(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplier.sizePolicy().hasHeightForWidth())
        self.cmbSupplier.setSizePolicy(sizePolicy)
        self.cmbSupplier.setObjectName(_fromUtf8("cmbSupplier"))
        self.gridLayout.addWidget(self.cmbSupplier, 2, 1, 1, 5)
        self.lblNote = QtGui.QLabel(FinTransferDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 4, 0, 1, 1)
        self.lblReasonDate = QtGui.QLabel(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReasonDate.sizePolicy().hasHeightForWidth())
        self.lblReasonDate.setSizePolicy(sizePolicy)
        self.lblReasonDate.setObjectName(_fromUtf8("lblReasonDate"))
        self.gridLayout.addWidget(self.lblReasonDate, 1, 3, 1, 1)
        self.lblSupplier = QtGui.QLabel(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSupplier.sizePolicy().hasHeightForWidth())
        self.lblSupplier.setSizePolicy(sizePolicy)
        self.lblSupplier.setObjectName(_fromUtf8("lblSupplier"))
        self.gridLayout.addWidget(self.lblSupplier, 2, 0, 1, 1)
        self.lblDate = QtGui.QLabel(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 3, 1, 1)
        self.edtNote = QtGui.QLineEdit(FinTransferDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 4, 1, 1, 5)
        self.edtReasonDate = CDateEdit(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtReasonDate.sizePolicy().hasHeightForWidth())
        self.edtReasonDate.setSizePolicy(sizePolicy)
        self.edtReasonDate.setObjectName(_fromUtf8("edtReasonDate"))
        self.gridLayout.addWidget(self.edtReasonDate, 1, 4, 1, 1)
        self.edtTime = QtGui.QTimeEdit(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTime.sizePolicy().hasHeightForWidth())
        self.edtTime.setSizePolicy(sizePolicy)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 0, 5, 1, 1)
        self.lblSupplierPerson = QtGui.QLabel(FinTransferDialog)
        self.lblSupplierPerson.setObjectName(_fromUtf8("lblSupplierPerson"))
        self.gridLayout.addWidget(self.lblSupplierPerson, 3, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(FinTransferDialog)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridLayout.addWidget(self.edtNumber, 0, 1, 1, 2)
        self.edtReason = QtGui.QLineEdit(FinTransferDialog)
        self.edtReason.setObjectName(_fromUtf8("edtReason"))
        self.gridLayout.addWidget(self.edtReason, 1, 1, 1, 2)
        self.cmbSupplierPerson = CPersonComboBoxEx(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplierPerson.sizePolicy().hasHeightForWidth())
        self.cmbSupplierPerson.setSizePolicy(sizePolicy)
        self.cmbSupplierPerson.setObjectName(_fromUtf8("cmbSupplierPerson"))
        self.gridLayout.addWidget(self.cmbSupplierPerson, 3, 1, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(FinTransferDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 6)
        self.tblItems = CInDocTableView(FinTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblItems.sizePolicy().hasHeightForWidth())
        self.tblItems.setSizePolicy(sizePolicy)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 5, 0, 1, 6)
        self.lblSummaryInfo = QtGui.QLabel(FinTransferDialog)
        self.lblSummaryInfo.setText(_fromUtf8(""))
        self.lblSummaryInfo.setObjectName(_fromUtf8("lblSummaryInfo"))
        self.gridLayout.addWidget(self.lblSummaryInfo, 6, 0, 1, 6)
        self.lblReason.setBuddy(self.edtReason)
        self.lblNumber.setBuddy(self.edtNumber)
        self.lblNote.setBuddy(self.edtNote)
        self.lblReasonDate.setBuddy(self.edtReasonDate)
        self.lblSupplier.setBuddy(self.cmbSupplier)
        self.lblDate.setBuddy(self.edtDate)
        self.lblSupplierPerson.setBuddy(self.cmbSupplierPerson)

        self.retranslateUi(FinTransferDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FinTransferDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FinTransferDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FinTransferDialog)
        FinTransferDialog.setTabOrder(self.edtNumber, self.edtDate)
        FinTransferDialog.setTabOrder(self.edtDate, self.edtTime)
        FinTransferDialog.setTabOrder(self.edtTime, self.edtReason)
        FinTransferDialog.setTabOrder(self.edtReason, self.edtReasonDate)
        FinTransferDialog.setTabOrder(self.edtReasonDate, self.cmbSupplier)
        FinTransferDialog.setTabOrder(self.cmbSupplier, self.cmbSupplierPerson)
        FinTransferDialog.setTabOrder(self.cmbSupplierPerson, self.edtNote)
        FinTransferDialog.setTabOrder(self.edtNote, self.tblItems)
        FinTransferDialog.setTabOrder(self.tblItems, self.buttonBox)

    def retranslateUi(self, FinTransferDialog):
        FinTransferDialog.setWindowTitle(_translate("FinTransferDialog", "Акт изменения типа финансирования ЛСиИМН", None))
        self.lblReason.setText(_translate("FinTransferDialog", "Основание", None))
        self.lblNumber.setText(_translate("FinTransferDialog", "Номер", None))
        self.lblNote.setText(_translate("FinTransferDialog", "Примечания", None))
        self.lblReasonDate.setText(_translate("FinTransferDialog", "Дата основания", None))
        self.lblSupplier.setText(_translate("FinTransferDialog", "Подразделение", None))
        self.lblDate.setText(_translate("FinTransferDialog", "Дата", None))
        self.edtTime.setDisplayFormat(_translate("FinTransferDialog", "HH:mm", None))
        self.lblSupplierPerson.setText(_translate("FinTransferDialog", "Ответственный", None))

from Orgs.OrgStructComboBoxes import CStorageComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FinTransferDialog = QtGui.QDialog()
    ui = Ui_FinTransferDialog()
    ui.setupUi(FinTransferDialog)
    FinTransferDialog.show()
    sys.exit(app.exec_())

