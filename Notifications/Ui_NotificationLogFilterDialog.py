# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Notifications/NotificationLogFilterDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ItemFilterDialog(object):
    def setupUi(self, ItemFilterDialog):
        ItemFilterDialog.setObjectName(_fromUtf8("ItemFilterDialog"))
        ItemFilterDialog.resize(549, 335)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ItemFilterDialog.sizePolicy().hasHeightForWidth())
        ItemFilterDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(ItemFilterDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbCreatePerson = CPersonComboBox(ItemFilterDialog)
        self.cmbCreatePerson.setObjectName(_fromUtf8("cmbCreatePerson"))
        self.gridLayout.addWidget(self.cmbCreatePerson, 2, 1, 1, 4)
        self.edtConfirmBegDate = CDateEdit(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtConfirmBegDate.sizePolicy().hasHeightForWidth())
        self.edtConfirmBegDate.setSizePolicy(sizePolicy)
        self.edtConfirmBegDate.setObjectName(_fromUtf8("edtConfirmBegDate"))
        self.gridLayout.addWidget(self.edtConfirmBegDate, 10, 1, 1, 1)
        self.lblCreatePerson = QtGui.QLabel(ItemFilterDialog)
        self.lblCreatePerson.setObjectName(_fromUtf8("lblCreatePerson"))
        self.gridLayout.addWidget(self.lblCreatePerson, 2, 0, 1, 1)
        self.edtSendBegDate = CDateEdit(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtSendBegDate.sizePolicy().hasHeightForWidth())
        self.edtSendBegDate.setSizePolicy(sizePolicy)
        self.edtSendBegDate.setObjectName(_fromUtf8("edtSendBegDate"))
        self.gridLayout.addWidget(self.edtSendBegDate, 8, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 14, 6, 1, 2)
        self.lblType = QtGui.QLabel(ItemFilterDialog)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 6, 0, 1, 1)
        self.chkWithoutSendDate = QtGui.QCheckBox(ItemFilterDialog)
        self.chkWithoutSendDate.setObjectName(_fromUtf8("chkWithoutSendDate"))
        self.gridLayout.addWidget(self.chkWithoutSendDate, 8, 7, 1, 2)
        self.lblStatus = QtGui.QLabel(ItemFilterDialog)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 3, 0, 1, 1)
        self.lblConfirmFrom = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblConfirmFrom.sizePolicy().hasHeightForWidth())
        self.lblConfirmFrom.setSizePolicy(sizePolicy)
        self.lblConfirmFrom.setObjectName(_fromUtf8("lblConfirmFrom"))
        self.gridLayout.addWidget(self.lblConfirmFrom, 10, 0, 1, 1)
        self.lblAddressTemplate = QtGui.QLabel(ItemFilterDialog)
        self.lblAddressTemplate.setObjectName(_fromUtf8("lblAddressTemplate"))
        self.gridLayout.addWidget(self.lblAddressTemplate, 1, 0, 1, 1)
        self.chkRule = QtGui.QCheckBox(ItemFilterDialog)
        self.chkRule.setObjectName(_fromUtf8("chkRule"))
        self.gridLayout.addWidget(self.chkRule, 5, 7, 1, 2)
        self.cmbKind = CRBComboBox(ItemFilterDialog)
        self.cmbKind.setObjectName(_fromUtf8("cmbKind"))
        self.gridLayout.addWidget(self.cmbKind, 4, 1, 1, 4)
        self.lblRule = QtGui.QLabel(ItemFilterDialog)
        self.lblRule.setObjectName(_fromUtf8("lblRule"))
        self.gridLayout.addWidget(self.lblRule, 5, 0, 1, 1)
        self.edtAddressTemplate = QtGui.QLineEdit(ItemFilterDialog)
        self.edtAddressTemplate.setObjectName(_fromUtf8("edtAddressTemplate"))
        self.gridLayout.addWidget(self.edtAddressTemplate, 1, 1, 1, 4)
        self.lblKind = QtGui.QLabel(ItemFilterDialog)
        self.lblKind.setObjectName(_fromUtf8("lblKind"))
        self.gridLayout.addWidget(self.lblKind, 4, 0, 1, 1)
        self.lblRecipientTemplate = QtGui.QLabel(ItemFilterDialog)
        self.lblRecipientTemplate.setObjectName(_fromUtf8("lblRecipientTemplate"))
        self.gridLayout.addWidget(self.lblRecipientTemplate, 0, 0, 1, 1)
        self.cmbStatus = QtGui.QComboBox(ItemFilterDialog)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.gridLayout.addWidget(self.cmbStatus, 3, 1, 1, 4)
        self.chkAddressTemplate = QtGui.QCheckBox(ItemFilterDialog)
        self.chkAddressTemplate.setObjectName(_fromUtf8("chkAddressTemplate"))
        self.gridLayout.addWidget(self.chkAddressTemplate, 1, 7, 1, 2)
        self.lblSendFrom = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSendFrom.sizePolicy().hasHeightForWidth())
        self.lblSendFrom.setSizePolicy(sizePolicy)
        self.lblSendFrom.setObjectName(_fromUtf8("lblSendFrom"))
        self.gridLayout.addWidget(self.lblSendFrom, 8, 0, 1, 1)
        self.chkCreatePerson = QtGui.QCheckBox(ItemFilterDialog)
        self.chkCreatePerson.setObjectName(_fromUtf8("chkCreatePerson"))
        self.gridLayout.addWidget(self.chkCreatePerson, 2, 7, 1, 2)
        self.cmbRule = CNotificationRuleComboBox(ItemFilterDialog)
        self.cmbRule.setObjectName(_fromUtf8("cmbRule"))
        self.gridLayout.addWidget(self.cmbRule, 5, 1, 1, 4)
        self.chkWithoutConfirmDate = QtGui.QCheckBox(ItemFilterDialog)
        self.chkWithoutConfirmDate.setObjectName(_fromUtf8("chkWithoutConfirmDate"))
        self.gridLayout.addWidget(self.chkWithoutConfirmDate, 10, 7, 1, 2)
        self.chkStatus = QtGui.QCheckBox(ItemFilterDialog)
        self.chkStatus.setObjectName(_fromUtf8("chkStatus"))
        self.gridLayout.addWidget(self.chkStatus, 3, 7, 1, 2)
        self.chkRecipientTemplate = QtGui.QCheckBox(ItemFilterDialog)
        self.chkRecipientTemplate.setObjectName(_fromUtf8("chkRecipientTemplate"))
        self.gridLayout.addWidget(self.chkRecipientTemplate, 0, 7, 1, 2)
        self.chkType = QtGui.QCheckBox(ItemFilterDialog)
        self.chkType.setObjectName(_fromUtf8("chkType"))
        self.gridLayout.addWidget(self.chkType, 6, 7, 1, 1)
        self.chkKind = QtGui.QCheckBox(ItemFilterDialog)
        self.chkKind.setObjectName(_fromUtf8("chkKind"))
        self.gridLayout.addWidget(self.chkKind, 4, 7, 1, 2)
        self.edtRecipientTemplate = QtGui.QLineEdit(ItemFilterDialog)
        self.edtRecipientTemplate.setObjectName(_fromUtf8("edtRecipientTemplate"))
        self.gridLayout.addWidget(self.edtRecipientTemplate, 0, 1, 1, 4)
        self.cmbType = QtGui.QComboBox(ItemFilterDialog)
        self.cmbType.setObjectName(_fromUtf8("cmbType"))
        self.cmbType.addItem(_fromUtf8(""))
        self.cmbType.setItemText(0, _fromUtf8(""))
        self.cmbType.addItem(_fromUtf8(""))
        self.cmbType.addItem(_fromUtf8(""))
        self.cmbType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbType, 6, 1, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 7, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 11, 7, 1, 1)
        self.lblSendTo = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSendTo.sizePolicy().hasHeightForWidth())
        self.lblSendTo.setSizePolicy(sizePolicy)
        self.lblSendTo.setObjectName(_fromUtf8("lblSendTo"))
        self.gridLayout.addWidget(self.lblSendTo, 8, 2, 1, 1)
        self.edtSendEndDate = CDateEdit(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtSendEndDate.sizePolicy().hasHeightForWidth())
        self.edtSendEndDate.setSizePolicy(sizePolicy)
        self.edtSendEndDate.setObjectName(_fromUtf8("edtSendEndDate"))
        self.gridLayout.addWidget(self.edtSendEndDate, 8, 3, 1, 1)
        self.lblConfirmTo = QtGui.QLabel(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblConfirmTo.sizePolicy().hasHeightForWidth())
        self.lblConfirmTo.setSizePolicy(sizePolicy)
        self.lblConfirmTo.setObjectName(_fromUtf8("lblConfirmTo"))
        self.gridLayout.addWidget(self.lblConfirmTo, 10, 2, 1, 1)
        self.edtConfirmEndDate = CDateEdit(ItemFilterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtConfirmEndDate.sizePolicy().hasHeightForWidth())
        self.edtConfirmEndDate.setSizePolicy(sizePolicy)
        self.edtConfirmEndDate.setObjectName(_fromUtf8("edtConfirmEndDate"))
        self.gridLayout.addWidget(self.edtConfirmEndDate, 10, 3, 1, 1)

        self.retranslateUi(ItemFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemFilterDialog)

    def retranslateUi(self, ItemFilterDialog):
        ItemFilterDialog.setWindowTitle(_translate("ItemFilterDialog", "Dialog", None))
        self.lblCreatePerson.setText(_translate("ItemFilterDialog", "Инициатор", None))
        self.lblType.setText(_translate("ItemFilterDialog", "Тип", None))
        self.chkWithoutSendDate.setText(_translate("ItemFilterDialog", "Без даты отправки", None))
        self.lblStatus.setText(_translate("ItemFilterDialog", "Статус", None))
        self.lblConfirmFrom.setText(_translate("ItemFilterDialog", "Подтверждение с", None))
        self.lblAddressTemplate.setText(_translate("ItemFilterDialog", "Адрес", None))
        self.chkRule.setText(_translate("ItemFilterDialog", "Без правила", None))
        self.lblRule.setText(_translate("ItemFilterDialog", "Правило", None))
        self.lblKind.setText(_translate("ItemFilterDialog", "Вид", None))
        self.lblRecipientTemplate.setText(_translate("ItemFilterDialog", "Адресат", None))
        self.chkAddressTemplate.setText(_translate("ItemFilterDialog", "Без адреса", None))
        self.lblSendFrom.setText(_translate("ItemFilterDialog", "Отправка с", None))
        self.chkCreatePerson.setText(_translate("ItemFilterDialog", "Без инициатора", None))
        self.chkWithoutConfirmDate.setText(_translate("ItemFilterDialog", "Без подтверждения", None))
        self.chkStatus.setText(_translate("ItemFilterDialog", "Без статуса", None))
        self.chkRecipientTemplate.setText(_translate("ItemFilterDialog", "Без адресата", None))
        self.chkType.setText(_translate("ItemFilterDialog", "Без типа", None))
        self.chkKind.setText(_translate("ItemFilterDialog", "Без вида", None))
        self.cmbType.setItemText(1, _translate("ItemFilterDialog", "Расписание", None))
        self.cmbType.setItemText(2, _translate("ItemFilterDialog", "Картотека", None))
        self.cmbType.setItemText(3, _translate("ItemFilterDialog", "Действие", None))
        self.lblSendTo.setText(_translate("ItemFilterDialog", "по", None))
        self.lblConfirmTo.setText(_translate("ItemFilterDialog", "по", None))

from Orgs.PersonComboBox import CPersonComboBox
from Utils import CNotificationRuleComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemFilterDialog = QtGui.QDialog()
    ui = Ui_ItemFilterDialog()
    ui.setupUi(ItemFilterDialog)
    ItemFilterDialog.show()
    sys.exit(app.exec_())

