# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Stock/NomenclatureExpense.ui'
#
# Created: Wed May  7 18:15:59 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_NomenclatureExpenseDialog(object):
    def setupUi(self, NomenclatureExpenseDialog):
        NomenclatureExpenseDialog.setObjectName(_fromUtf8("NomenclatureExpenseDialog"))
        NomenclatureExpenseDialog.resize(600, 500)
        self.gridLayout = QtGui.QGridLayout(NomenclatureExpenseDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblNumber = QtGui.QLabel(NomenclatureExpenseDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridLayout.addWidget(self.lblNumber, 0, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(NomenclatureExpenseDialog)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridLayout.addWidget(self.edtNumber, 0, 1, 1, 1)
        self.lblDate = QtGui.QLabel(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 2, 1, 1)
        self.edtDate = CDateEdit(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 3, 1, 1)
        self.edtTime = QtGui.QTimeEdit(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTime.sizePolicy().hasHeightForWidth())
        self.edtTime.setSizePolicy(sizePolicy)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 0, 4, 1, 1)
        self.lblReason = QtGui.QLabel(NomenclatureExpenseDialog)
        self.lblReason.setObjectName(_fromUtf8("lblReason"))
        self.gridLayout.addWidget(self.lblReason, 1, 0, 1, 1)
        self.edtReason = QtGui.QLineEdit(NomenclatureExpenseDialog)
        self.edtReason.setObjectName(_fromUtf8("edtReason"))
        self.gridLayout.addWidget(self.edtReason, 1, 1, 1, 1)
        self.lblReasonDate = QtGui.QLabel(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReasonDate.sizePolicy().hasHeightForWidth())
        self.lblReasonDate.setSizePolicy(sizePolicy)
        self.lblReasonDate.setObjectName(_fromUtf8("lblReasonDate"))
        self.gridLayout.addWidget(self.lblReasonDate, 1, 2, 1, 1)
        self.edtReasonDate = CDateEdit(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtReasonDate.sizePolicy().hasHeightForWidth())
        self.edtReasonDate.setSizePolicy(sizePolicy)
        self.edtReasonDate.setObjectName(_fromUtf8("edtReasonDate"))
        self.gridLayout.addWidget(self.edtReasonDate, 1, 3, 1, 1)
        self.lblSupplier = QtGui.QLabel(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSupplier.sizePolicy().hasHeightForWidth())
        self.lblSupplier.setSizePolicy(sizePolicy)
        self.lblSupplier.setObjectName(_fromUtf8("lblSupplier"))
        self.gridLayout.addWidget(self.lblSupplier, 2, 0, 1, 1)
        self.cmbSupplier = CStorageComboBox(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplier.sizePolicy().hasHeightForWidth())
        self.cmbSupplier.setSizePolicy(sizePolicy)
        self.cmbSupplier.setObjectName(_fromUtf8("cmbSupplier"))
        self.gridLayout.addWidget(self.cmbSupplier, 2, 1, 1, 4)
        self.lblSupplierPerson = QtGui.QLabel(NomenclatureExpenseDialog)
        self.lblSupplierPerson.setObjectName(_fromUtf8("lblSupplierPerson"))
        self.gridLayout.addWidget(self.lblSupplierPerson, 3, 0, 1, 1)
        self.cmbSupplierPerson = CPersonComboBoxEx(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSupplierPerson.sizePolicy().hasHeightForWidth())
        self.cmbSupplierPerson.setSizePolicy(sizePolicy)
        self.cmbSupplierPerson.setObjectName(_fromUtf8("cmbSupplierPerson"))
        self.gridLayout.addWidget(self.cmbSupplierPerson, 3, 1, 1, 4)
        self.lblNote = QtGui.QLabel(NomenclatureExpenseDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 4, 0, 1, 1)
        self.edtNote = QtGui.QLineEdit(NomenclatureExpenseDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 4, 1, 1, 4)
        self.tblItems = CInDocTableView(NomenclatureExpenseDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblItems.sizePolicy().hasHeightForWidth())
        self.tblItems.setSizePolicy(sizePolicy)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 5, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(NomenclatureExpenseDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 5)
        self.lblNumber.setBuddy(self.edtNumber)
        self.lblDate.setBuddy(self.edtDate)
        self.lblReason.setBuddy(self.edtReason)
        self.lblReasonDate.setBuddy(self.edtReasonDate)
        self.lblSupplier.setBuddy(self.cmbSupplier)
        self.lblSupplierPerson.setBuddy(self.cmbSupplierPerson)
        self.lblNote.setBuddy(self.edtNote)

        self.retranslateUi(NomenclatureExpenseDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NomenclatureExpenseDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NomenclatureExpenseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NomenclatureExpenseDialog)
        NomenclatureExpenseDialog.setTabOrder(self.edtNumber, self.edtDate)
        NomenclatureExpenseDialog.setTabOrder(self.edtDate, self.edtTime)
        NomenclatureExpenseDialog.setTabOrder(self.edtTime, self.edtReason)
        NomenclatureExpenseDialog.setTabOrder(self.edtReason, self.edtReasonDate)
        NomenclatureExpenseDialog.setTabOrder(self.edtReasonDate, self.cmbSupplier)
        NomenclatureExpenseDialog.setTabOrder(self.cmbSupplier, self.cmbSupplierPerson)
        NomenclatureExpenseDialog.setTabOrder(self.cmbSupplierPerson, self.edtNote)
        NomenclatureExpenseDialog.setTabOrder(self.edtNote, self.tblItems)
        NomenclatureExpenseDialog.setTabOrder(self.tblItems, self.buttonBox)

    def retranslateUi(self, NomenclatureExpenseDialog):
        NomenclatureExpenseDialog.setWindowTitle(_translate("NomenclatureExpenseDialog", "Списание ЛСиИМН", None))
        self.lblNumber.setText(_translate("NomenclatureExpenseDialog", "Номер", None))
        self.lblDate.setText(_translate("NomenclatureExpenseDialog", "Дата", None))
        self.edtTime.setDisplayFormat(_translate("NomenclatureExpenseDialog", "HH:mm", None))
        self.lblReason.setText(_translate("NomenclatureExpenseDialog", "Основание", None))
        self.lblReasonDate.setText(_translate("NomenclatureExpenseDialog", "Дата основания", None))
        self.lblSupplier.setText(_translate("NomenclatureExpenseDialog", "Подразделение", None))
        self.lblSupplierPerson.setText(_translate("NomenclatureExpenseDialog", "Ответственный", None))
        self.lblNote.setText(_translate("NomenclatureExpenseDialog", "Примечания", None))

from library.InDocTable import CInDocTableView
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import CStorageComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NomenclatureExpenseDialog = QtGui.QDialog()
    ui = Ui_NomenclatureExpenseDialog()
    ui.setupUi(NomenclatureExpenseDialog)
    NomenclatureExpenseDialog.show()
    sys.exit(app.exec_())

