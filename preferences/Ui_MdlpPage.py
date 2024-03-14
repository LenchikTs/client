# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MdlpPage.ui'
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

class Ui_mdlpPage(object):
    def setupUi(self, mdlpPage):
        mdlpPage.setObjectName(_fromUtf8("mdlpPage"))
        mdlpPage.resize(651, 592)
        self.gridLayout = QtGui.QGridLayout(mdlpPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkMdlpEnabled = QtGui.QCheckBox(mdlpPage)
        self.chkMdlpEnabled.setText(_fromUtf8(""))
        self.chkMdlpEnabled.setChecked(True)
        self.chkMdlpEnabled.setObjectName(_fromUtf8("chkMdlpEnabled"))
        self.gridLayout.addWidget(self.chkMdlpEnabled, 1, 1, 1, 1)
        self.edtMdlpUrl = QtGui.QLineEdit(mdlpPage)
        self.edtMdlpUrl.setMaxLength(128)
        self.edtMdlpUrl.setObjectName(_fromUtf8("edtMdlpUrl"))
        self.gridLayout.addWidget(self.edtMdlpUrl, 2, 1, 1, 1)
        self.chkMdlpStunnel = QtGui.QCheckBox(mdlpPage)
        self.chkMdlpStunnel.setObjectName(_fromUtf8("chkMdlpStunnel"))
        self.gridLayout.addWidget(self.chkMdlpStunnel, 5, 0, 1, 1)
        self.edtMdlpStunnelUrl = QtGui.QLineEdit(mdlpPage)
        self.edtMdlpStunnelUrl.setEnabled(True)
        self.edtMdlpStunnelUrl.setMaxLength(64)
        self.edtMdlpStunnelUrl.setObjectName(_fromUtf8("edtMdlpStunnelUrl"))
        self.gridLayout.addWidget(self.edtMdlpStunnelUrl, 5, 1, 1, 2)
        self.chkMdlpNotificationMode = QtGui.QCheckBox(mdlpPage)
        self.chkMdlpNotificationMode.setText(_fromUtf8(""))
        self.chkMdlpNotificationMode.setObjectName(_fromUtf8("chkMdlpNotificationMode"))
        self.gridLayout.addWidget(self.chkMdlpNotificationMode, 7, 1, 1, 2)
        self.edtMdlpClientId = QtGui.QLineEdit(mdlpPage)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.edtMdlpClientId.setFont(font)
        self.edtMdlpClientId.setObjectName(_fromUtf8("edtMdlpClientId"))
        self.gridLayout.addWidget(self.edtMdlpClientId, 3, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 8, 2, 1, 1)
        self.btnMdlpTest = QtGui.QPushButton(mdlpPage)
        self.btnMdlpTest.setObjectName(_fromUtf8("btnMdlpTest"))
        self.gridLayout.addWidget(self.btnMdlpTest, 8, 1, 1, 1)
        self.lblMdlpClientId = QtGui.QLabel(mdlpPage)
        self.lblMdlpClientId.setObjectName(_fromUtf8("lblMdlpClientId"))
        self.gridLayout.addWidget(self.lblMdlpClientId, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 9, 0, 1, 3)
        self.lblMdlpClientSecret = QtGui.QLabel(mdlpPage)
        self.lblMdlpClientSecret.setObjectName(_fromUtf8("lblMdlpClientSecret"))
        self.gridLayout.addWidget(self.lblMdlpClientSecret, 4, 0, 1, 1)
        self.edtMdlpClientSecret = QtGui.QLineEdit(mdlpPage)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.edtMdlpClientSecret.setFont(font)
        self.edtMdlpClientSecret.setObjectName(_fromUtf8("edtMdlpClientSecret"))
        self.gridLayout.addWidget(self.edtMdlpClientSecret, 4, 1, 1, 2)
        self.lblMdlpUrl = QtGui.QLabel(mdlpPage)
        self.lblMdlpUrl.setObjectName(_fromUtf8("lblMdlpUrl"))
        self.gridLayout.addWidget(self.lblMdlpUrl, 2, 0, 1, 1)
        self.lblMdlpEnabled = QtGui.QLabel(mdlpPage)
        self.lblMdlpEnabled.setObjectName(_fromUtf8("lblMdlpEnabled"))
        self.gridLayout.addWidget(self.lblMdlpEnabled, 1, 0, 1, 1)
        self.lblMdlpNotificationMode = QtGui.QLabel(mdlpPage)
        self.lblMdlpNotificationMode.setObjectName(_fromUtf8("lblMdlpNotificationMode"))
        self.gridLayout.addWidget(self.lblMdlpNotificationMode, 7, 0, 1, 1)
        self.lblMdlpClientId.setBuddy(self.edtMdlpClientId)
        self.lblMdlpClientSecret.setBuddy(self.edtMdlpClientSecret)
        self.lblMdlpUrl.setBuddy(self.edtMdlpUrl)
        self.lblMdlpEnabled.setBuddy(self.chkMdlpEnabled)
        self.lblMdlpNotificationMode.setBuddy(self.chkMdlpNotificationMode)

        self.retranslateUi(mdlpPage)
        QtCore.QMetaObject.connectSlotsByName(mdlpPage)
        mdlpPage.setTabOrder(self.chkMdlpEnabled, self.edtMdlpUrl)
        mdlpPage.setTabOrder(self.edtMdlpUrl, self.edtMdlpClientId)
        mdlpPage.setTabOrder(self.edtMdlpClientId, self.edtMdlpClientSecret)
        mdlpPage.setTabOrder(self.edtMdlpClientSecret, self.chkMdlpStunnel)
        mdlpPage.setTabOrder(self.chkMdlpStunnel, self.edtMdlpStunnelUrl)
        mdlpPage.setTabOrder(self.edtMdlpStunnelUrl, self.chkMdlpNotificationMode)
        mdlpPage.setTabOrder(self.chkMdlpNotificationMode, self.btnMdlpTest)

    def retranslateUi(self, mdlpPage):
        mdlpPage.setWindowTitle(_translate("mdlpPage", "Интеграция с МДЛП", None))
        self.edtMdlpUrl.setToolTip(_translate("mdlpPage", "<html><head/><body><p>в терминах МДЛП это <span style=\" font-family:\'monospace\';\">&lt;endpoint&gt;/&lt;version&gt;/</span></p><p><span style=\" font-family:\'monospace\';\">«Песочница»    https://api.sb.mdlp.crpt.ru</span><span style=\" font-family:\'monospace\';\">/api/v1/</span></p><p><span style=\" font-family:\'monospace\';\">«Промышленный» https://api.mdlp.crpt.ru</span><span style=\" font-family:\'monospace\';\">/api/v1/</span></p><p><br/></p></body></html>", None))
        self.edtMdlpUrl.setText(_translate("mdlpPage", "https://api.sb.mdlp.crpt.ru/api/v1/", None))
        self.chkMdlpStunnel.setText(_translate("mdlpPage", "Использовать stunnel", None))
        self.edtMdlpStunnelUrl.setToolTip(_translate("mdlpPage", "<html><head/><body><p>Для случая, когда ОС не позволяет напрямую использовать https c ГОСТ-овской криптографией</p></body></html>", None))
        self.edtMdlpStunnelUrl.setText(_translate("mdlpPage", "http://localhost", None))
        self.edtMdlpClientId.setToolTip(_translate("mdlpPage", "<html><head/><body><p>Для получения идентификатора и секретного кода (ключа) нужно зарегистрировать учётную систему в личном кабинете участника МДЛП (Администрирование&nbsp;→&nbsp;Учётные&nbsp;системы, см.Руководство пользователя личного кабинета, п.&nbsp;4.11.3 «Добавление, удаление учетной системы»)</p></body></html>", None))
        self.edtMdlpClientId.setInputMask(_translate("mdlpPage", "HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH; ", None))
        self.edtMdlpClientId.setText(_translate("mdlpPage", "----", None))
        self.btnMdlpTest.setText(_translate("mdlpPage", "Проверить соединение", None))
        self.lblMdlpClientId.setText(_translate("mdlpPage", "Идентификатор клиента", None))
        self.lblMdlpClientSecret.setText(_translate("mdlpPage", "Секретный код (ключ)", None))
        self.edtMdlpClientSecret.setToolTip(_translate("mdlpPage", "<html><head/><body><p>Для получения идентификатора и секретного кода (ключа) нужно зарегистрировать учётную систему в личном кабинете участника МДЛП (Администрирование&nbsp;→&nbsp;Учётные&nbsp;системы, см.Руководство пользователя личного кабинета, п.&nbsp;4.11.3 «Добавление, удаление учетной системы»)</p></body></html>", None))
        self.edtMdlpClientSecret.setInputMask(_translate("mdlpPage", "HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH; ", None))
        self.lblMdlpUrl.setText(_translate("mdlpPage", "URL сервиса МДЛП", None))
        self.lblMdlpEnabled.setText(_translate("mdlpPage", "Использование МДЛП разрешено", None))
        self.lblMdlpNotificationMode.setText(_translate("mdlpPage", "Уведомительный режим", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mdlpPage = QtGui.QWidget()
    ui = Ui_mdlpPage()
    ui.setupUi(mdlpPage)
    mdlpPage.show()
    sys.exit(app.exec_())

