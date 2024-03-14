# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/Notifications/NotificationLogEditorDialog.ui'
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

class Ui_NotificationLogEditorDialog(object):
    def setupUi(self, NotificationLogEditorDialog):
        NotificationLogEditorDialog.setObjectName(_fromUtf8("NotificationLogEditorDialog"))
        NotificationLogEditorDialog.resize(645, 517)
        NotificationLogEditorDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(NotificationLogEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 1)
        self.label = QtGui.QLabel(NotificationLogEditorDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.cmbCreatePerson = QtGui.QComboBox(NotificationLogEditorDialog)
        self.cmbCreatePerson.setObjectName(_fromUtf8("cmbCreatePerson"))
        self.gridLayout.addWidget(self.cmbCreatePerson, 2, 1, 1, 2)
        self.label_7 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 1)
        self.edtCreateDatetime = QtGui.QDateTimeEdit(NotificationLogEditorDialog)
        self.edtCreateDatetime.setObjectName(_fromUtf8("edtCreateDatetime"))
        self.gridLayout.addWidget(self.edtCreateDatetime, 1, 1, 1, 3)
        self.edtAttempt = QtGui.QSpinBox(NotificationLogEditorDialog)
        self.edtAttempt.setObjectName(_fromUtf8("edtAttempt"))
        self.gridLayout.addWidget(self.edtAttempt, 7, 1, 1, 1)
        self.lblType = QtGui.QLabel(NotificationLogEditorDialog)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 1, 0, 1, 1)
        self.edtText = QtGui.QTextEdit(NotificationLogEditorDialog)
        self.edtText.setObjectName(_fromUtf8("edtText"))
        self.gridLayout.addWidget(self.edtText, 4, 1, 1, 3)
        self.edtNotificationRule = QtGui.QLineEdit(NotificationLogEditorDialog)
        self.edtNotificationRule.setReadOnly(True)
        self.edtNotificationRule.setObjectName(_fromUtf8("edtNotificationRule"))
        self.gridLayout.addWidget(self.edtNotificationRule, 0, 1, 1, 3)
        self.edtConfirmationDatetime = QtGui.QDateTimeEdit(NotificationLogEditorDialog)
        self.edtConfirmationDatetime.setObjectName(_fromUtf8("edtConfirmationDatetime"))
        self.gridLayout.addWidget(self.edtConfirmationDatetime, 9, 1, 1, 3)
        self.edtSendDatetime = QtGui.QDateTimeEdit(NotificationLogEditorDialog)
        self.edtSendDatetime.setObjectName(_fromUtf8("edtSendDatetime"))
        self.gridLayout.addWidget(self.edtSendDatetime, 8, 1, 1, 3)
        self.label_5 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.lblClass = QtGui.QLabel(NotificationLogEditorDialog)
        self.lblClass.setObjectName(_fromUtf8("lblClass"))
        self.gridLayout.addWidget(self.lblClass, 0, 0, 1, 1)
        self.edtRecipient = QtGui.QLineEdit(NotificationLogEditorDialog)
        self.edtRecipient.setObjectName(_fromUtf8("edtRecipient"))
        self.gridLayout.addWidget(self.edtRecipient, 3, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.label_3 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.lblStatus = QtGui.QLabel(NotificationLogEditorDialog)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 10, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NotificationLogEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 2, 1, 2)
        self.label_4 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_2 = QtGui.QLabel(NotificationLogEditorDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.lblCondition = QtGui.QLabel(NotificationLogEditorDialog)
        self.lblCondition.setObjectName(_fromUtf8("lblCondition"))
        self.gridLayout.addWidget(self.lblCondition, 2, 0, 1, 1)
        self.cmbNotificationType = QtGui.QComboBox(NotificationLogEditorDialog)
        self.cmbNotificationType.setObjectName(_fromUtf8("cmbNotificationType"))
        self.gridLayout.addWidget(self.cmbNotificationType, 5, 1, 1, 2)
        self.edtStatus = QtGui.QLineEdit(NotificationLogEditorDialog)
        self.edtStatus.setObjectName(_fromUtf8("edtStatus"))
        self.gridLayout.addWidget(self.edtStatus, 10, 1, 1, 3)
        self.edtAddress = QtGui.QLineEdit(NotificationLogEditorDialog)
        self.edtAddress.setObjectName(_fromUtf8("edtAddress"))
        self.gridLayout.addWidget(self.edtAddress, 6, 1, 1, 3)

        self.retranslateUi(NotificationLogEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NotificationLogEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NotificationLogEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NotificationLogEditorDialog)

    def retranslateUi(self, NotificationLogEditorDialog):
        NotificationLogEditorDialog.setWindowTitle(_translate("NotificationLogEditorDialog", "Элемент журнала оповещений", None))
        self.label_6.setText(_translate("NotificationLogEditorDialog", "Отправка", None))
        self.label.setText(_translate("NotificationLogEditorDialog", "Адресат", None))
        self.label_7.setText(_translate("NotificationLogEditorDialog", "Подтверждение", None))
        self.lblType.setText(_translate("NotificationLogEditorDialog", "Регистрация", None))
        self.label_5.setText(_translate("NotificationLogEditorDialog", "Попытки", None))
        self.lblClass.setText(_translate("NotificationLogEditorDialog", "Правило", None))
        self.label_3.setText(_translate("NotificationLogEditorDialog", "Вид оповещения", None))
        self.lblStatus.setText(_translate("NotificationLogEditorDialog", "Статус", None))
        self.label_4.setText(_translate("NotificationLogEditorDialog", "Адрес", None))
        self.label_2.setText(_translate("NotificationLogEditorDialog", "Текст", None))
        self.lblCondition.setText(_translate("NotificationLogEditorDialog", "Инициатор", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NotificationLogEditorDialog = QtGui.QDialog()
    ui = Ui_NotificationLogEditorDialog()
    ui.setupUi(NotificationLogEditorDialog)
    NotificationLogEditorDialog.show()
    sys.exit(app.exec_())

