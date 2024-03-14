# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Notifications\NotifyDialog.ui'
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

class Ui_NotifyDialog(object):
    def setupUi(self, NotifyDialog):
        NotifyDialog.setObjectName(_fromUtf8("NotifyDialog"))
        NotifyDialog.resize(478, 220)
        NotifyDialog.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(NotifyDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.bbxNotify = QtGui.QDialogButtonBox(NotifyDialog)
        self.bbxNotify.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbxNotify.setObjectName(_fromUtf8("bbxNotify"))
        self.gridlayout.addWidget(self.bbxNotify, 8, 0, 1, 2)
        self.lblNotificationRule = QtGui.QLabel(NotifyDialog)
        self.lblNotificationRule.setObjectName(_fromUtf8("lblNotificationRule"))
        self.gridlayout.addWidget(self.lblNotificationRule, 0, 0, 1, 1)
        self.cmbNotificationRule = CNotificationRuleComboBox(NotifyDialog)
        self.cmbNotificationRule.setObjectName(_fromUtf8("cmbNotificationRule"))
        self.cmbNotificationRule.addItem(_fromUtf8(""))
        self.cmbNotificationRule.addItem(_fromUtf8(""))
        self.cmbNotificationRule.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbNotificationRule, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 5, 0, 1, 1)
        self.edtMessage = QtGui.QPlainTextEdit(NotifyDialog)
        self.edtMessage.setObjectName(_fromUtf8("edtMessage"))
        self.gridlayout.addWidget(self.edtMessage, 4, 0, 1, 2)
        self.lblMessage = QtGui.QLabel(NotifyDialog)
        self.lblMessage.setObjectName(_fromUtf8("lblMessage"))
        self.gridlayout.addWidget(self.lblMessage, 1, 0, 1, 1)
        self.label = QtGui.QLabel(NotifyDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 6, 0, 1, 1)
        self.edtMsgExample = QtGui.QPlainTextEdit(NotifyDialog)
        self.edtMsgExample.setReadOnly(True)
        self.edtMsgExample.setObjectName(_fromUtf8("edtMsgExample"))
        self.gridlayout.addWidget(self.edtMsgExample, 7, 0, 1, 2)

        self.retranslateUi(NotifyDialog)
        QtCore.QObject.connect(self.bbxNotify, QtCore.SIGNAL(_fromUtf8("accepted()")), NotifyDialog.accept)
        QtCore.QObject.connect(self.bbxNotify, QtCore.SIGNAL(_fromUtf8("rejected()")), NotifyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NotifyDialog)

    def retranslateUi(self, NotifyDialog):
        NotifyDialog.setWindowTitle(_translate("NotifyDialog", "Правило оповещения", None))
        self.lblNotificationRule.setText(_translate("NotifyDialog", "Правило", None))
        self.cmbNotificationRule.setItemText(0, _translate("NotifyDialog", "подтверждение записи", None))
        self.cmbNotificationRule.setItemText(1, _translate("NotifyDialog", "напоминание", None))
        self.cmbNotificationRule.setItemText(2, _translate("NotifyDialog", "отмена записи", None))
        self.lblMessage.setToolTip(_translate("NotifyDialog", "Будет подставлено в шаблон как {message}", None))
        self.lblMessage.setText(_translate("NotifyDialog", "Сообщение", None))
        self.label.setText(_translate("NotifyDialog", "Пример", None))

from Notifications.Utils import CNotificationRuleComboBox
