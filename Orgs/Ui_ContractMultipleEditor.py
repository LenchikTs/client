# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContractMultipleEditor.ui'
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

class Ui_ContractMultipleEditorDialog(object):
    def setupUi(self, ContractMultipleEditorDialog):
        ContractMultipleEditorDialog.setObjectName(_fromUtf8("ContractMultipleEditorDialog"))
        ContractMultipleEditorDialog.resize(574, 255)
        self.gridLayout = QtGui.QGridLayout(ContractMultipleEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDate = QtGui.QLabel(ContractMultipleEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.lblPriceList = QtGui.QLabel(ContractMultipleEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPriceList.sizePolicy().hasHeightForWidth())
        self.lblPriceList.setSizePolicy(sizePolicy)
        self.lblPriceList.setObjectName(_fromUtf8("lblPriceList"))
        self.gridLayout.addWidget(self.lblPriceList, 2, 0, 1, 1)
        self.lblRecipient = QtGui.QLabel(ContractMultipleEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRecipient.sizePolicy().hasHeightForWidth())
        self.lblRecipient.setSizePolicy(sizePolicy)
        self.lblRecipient.setObjectName(_fromUtf8("lblRecipient"))
        self.gridLayout.addWidget(self.lblRecipient, 3, 0, 1, 1)
        self.lblPayer = QtGui.QLabel(ContractMultipleEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPayer.sizePolicy().hasHeightForWidth())
        self.lblPayer.setSizePolicy(sizePolicy)
        self.lblPayer.setObjectName(_fromUtf8("lblPayer"))
        self.gridLayout.addWidget(self.lblPayer, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 4)
        self.lblBegDate = QtGui.QLabel(ContractMultipleEditorDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 1, 0, 1, 1)
        self.edtBegDate = CDateEdit(ContractMultipleEditorDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ContractMultipleEditorDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 2, 1, 1)
        self.edtEndDate = CDateEdit(ContractMultipleEditorDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.cmbPriceList = CPriceListComboBoxEx(ContractMultipleEditorDialog)
        self.cmbPriceList.setObjectName(_fromUtf8("cmbPriceList"))
        self.gridLayout.addWidget(self.cmbPriceList, 2, 1, 1, 4)
        self.cmbRecipient = COrgComboBox(ContractMultipleEditorDialog)
        self.cmbRecipient.setObjectName(_fromUtf8("cmbRecipient"))
        self.gridLayout.addWidget(self.cmbRecipient, 3, 1, 1, 4)
        self.cmbPayer = COrgComboBox(ContractMultipleEditorDialog)
        self.cmbPayer.setObjectName(_fromUtf8("cmbPayer"))
        self.gridLayout.addWidget(self.cmbPayer, 4, 1, 1, 4)
        self.edtDate = CDateEdit(ContractMultipleEditorDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 0, 1, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ContractMultipleEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 5)
        self.lblRecipient.setBuddy(self.cmbRecipient)
        self.lblPayer.setBuddy(self.cmbPayer)

        self.retranslateUi(ContractMultipleEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ContractMultipleEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ContractMultipleEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ContractMultipleEditorDialog)

    def retranslateUi(self, ContractMultipleEditorDialog):
        ContractMultipleEditorDialog.setWindowTitle(_translate("ContractMultipleEditorDialog", "Dialog", None))
        self.lblDate.setText(_translate("ContractMultipleEditorDialog", "Дата", None))
        self.lblPriceList.setText(_translate("ContractMultipleEditorDialog", "Прайс-лист", None))
        self.lblRecipient.setText(_translate("ContractMultipleEditorDialog", "Получатель", None))
        self.lblPayer.setText(_translate("ContractMultipleEditorDialog", "Плательщик", None))
        self.lblBegDate.setText(_translate("ContractMultipleEditorDialog", "Период с", None))
        self.lblEndDate.setText(_translate("ContractMultipleEditorDialog", "по", None))

from OrgComboBox import COrgComboBox
from PriceListComboBox import CPriceListComboBoxEx
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ContractMultipleEditorDialog = QtGui.QDialog()
    ui = Ui_ContractMultipleEditorDialog()
    ui.setupUi(ContractMultipleEditorDialog)
    ContractMultipleEditorDialog.show()
    sys.exit(app.exec_())

