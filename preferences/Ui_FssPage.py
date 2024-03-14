# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\preferences\FssPage.ui'
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

class Ui_fssPage(object):
    def setupUi(self, fssPage):
        fssPage.setObjectName(_fromUtf8("fssPage"))
        fssPage.resize(489, 300)
        self.gridLayout = QtGui.QGridLayout(fssPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblProxyLogin = QtGui.QLabel(fssPage)
        self.lblProxyLogin.setEnabled(False)
        self.lblProxyLogin.setObjectName(_fromUtf8("lblProxyLogin"))
        self.gridLayout.addWidget(self.lblProxyLogin, 6, 0, 1, 1)
        self.edtProxyPassword = QtGui.QLineEdit(fssPage)
        self.edtProxyPassword.setEnabled(False)
        self.edtProxyPassword.setObjectName(_fromUtf8("edtProxyPassword"))
        self.gridLayout.addWidget(self.edtProxyPassword, 6, 3, 1, 1)
        self.edtProxyAddress = QtGui.QLineEdit(fssPage)
        self.edtProxyAddress.setEnabled(False)
        self.edtProxyAddress.setObjectName(_fromUtf8("edtProxyAddress"))
        self.gridLayout.addWidget(self.edtProxyAddress, 4, 1, 1, 1)
        self.lblProxyPort = QtGui.QLabel(fssPage)
        self.lblProxyPort.setEnabled(False)
        self.lblProxyPort.setObjectName(_fromUtf8("lblProxyPort"))
        self.gridLayout.addWidget(self.lblProxyPort, 4, 2, 1, 1)
        self.edtProxyLogin = QtGui.QLineEdit(fssPage)
        self.edtProxyLogin.setEnabled(False)
        self.edtProxyLogin.setObjectName(_fromUtf8("edtProxyLogin"))
        self.gridLayout.addWidget(self.edtProxyLogin, 6, 1, 1, 1)
        self.edtProxyPort = QtGui.QSpinBox(fssPage)
        self.edtProxyPort.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtProxyPort.sizePolicy().hasHeightForWidth())
        self.edtProxyPort.setSizePolicy(sizePolicy)
        self.edtProxyPort.setMinimum(0)
        self.edtProxyPort.setMaximum(65535)
        self.edtProxyPort.setProperty("value", 3128)
        self.edtProxyPort.setObjectName(_fromUtf8("edtProxyPort"))
        self.gridLayout.addWidget(self.edtProxyPort, 4, 3, 1, 1)
        self.lblServiceUrl = QtGui.QLabel(fssPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblServiceUrl.sizePolicy().hasHeightForWidth())
        self.lblServiceUrl.setSizePolicy(sizePolicy)
        self.lblServiceUrl.setMinimumSize(QtCore.QSize(130, 0))
        self.lblServiceUrl.setObjectName(_fromUtf8("lblServiceUrl"))
        self.gridLayout.addWidget(self.lblServiceUrl, 0, 0, 1, 1)
        self.cmbFssCert = CCertComboBox(fssPage)
        self.cmbFssCert.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbFssCert.sizePolicy().hasHeightForWidth())
        self.cmbFssCert.setSizePolicy(sizePolicy)
        self.cmbFssCert.setObjectName(_fromUtf8("cmbFssCert"))
        self.gridLayout.addWidget(self.cmbFssCert, 2, 1, 1, 3)
        self.lblProxyPassword = QtGui.QLabel(fssPage)
        self.lblProxyPassword.setEnabled(False)
        self.lblProxyPassword.setObjectName(_fromUtf8("lblProxyPassword"))
        self.gridLayout.addWidget(self.lblProxyPassword, 6, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(129, 218, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.chkUseProxy = QtGui.QCheckBox(fssPage)
        self.chkUseProxy.setObjectName(_fromUtf8("chkUseProxy"))
        self.gridLayout.addWidget(self.chkUseProxy, 3, 0, 1, 4)
        self.chkUseEncryption = QtGui.QCheckBox(fssPage)
        self.chkUseEncryption.setObjectName(_fromUtf8("chkUseEncryption"))
        self.gridLayout.addWidget(self.chkUseEncryption, 1, 0, 1, 4)
        self.lblFssCert = QtGui.QLabel(fssPage)
        self.lblFssCert.setEnabled(False)
        self.lblFssCert.setObjectName(_fromUtf8("lblFssCert"))
        self.gridLayout.addWidget(self.lblFssCert, 2, 0, 1, 1)
        self.edtServiceUrl = QtGui.QLineEdit(fssPage)
        self.edtServiceUrl.setObjectName(_fromUtf8("edtServiceUrl"))
        self.gridLayout.addWidget(self.edtServiceUrl, 0, 1, 1, 3)
        self.lblProxyAddress = QtGui.QLabel(fssPage)
        self.lblProxyAddress.setEnabled(False)
        self.lblProxyAddress.setObjectName(_fromUtf8("lblProxyAddress"))
        self.gridLayout.addWidget(self.lblProxyAddress, 4, 0, 1, 1)
        self.chkProxyUseAuth = QtGui.QCheckBox(fssPage)
        self.chkProxyUseAuth.setEnabled(False)
        self.chkProxyUseAuth.setObjectName(_fromUtf8("chkProxyUseAuth"))
        self.gridLayout.addWidget(self.chkProxyUseAuth, 5, 0, 1, 4)
        self.lblProxyLogin.setBuddy(self.edtProxyLogin)
        self.lblProxyPort.setBuddy(self.edtProxyPort)
        self.lblServiceUrl.setBuddy(self.edtServiceUrl)
        self.lblProxyPassword.setBuddy(self.edtProxyPassword)
        self.lblFssCert.setBuddy(self.cmbFssCert)
        self.lblProxyAddress.setBuddy(self.edtProxyAddress)

        self.retranslateUi(fssPage)
        QtCore.QObject.connect(self.chkUseEncryption, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblFssCert.setEnabled)
        QtCore.QObject.connect(self.chkUseEncryption, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFssCert.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(fssPage)
        fssPage.setTabOrder(self.edtServiceUrl, self.chkUseEncryption)
        fssPage.setTabOrder(self.chkUseEncryption, self.cmbFssCert)
        fssPage.setTabOrder(self.cmbFssCert, self.chkUseProxy)
        fssPage.setTabOrder(self.chkUseProxy, self.edtProxyAddress)
        fssPage.setTabOrder(self.edtProxyAddress, self.edtProxyPort)
        fssPage.setTabOrder(self.edtProxyPort, self.chkProxyUseAuth)
        fssPage.setTabOrder(self.chkProxyUseAuth, self.edtProxyLogin)
        fssPage.setTabOrder(self.edtProxyLogin, self.edtProxyPassword)

    def retranslateUi(self, fssPage):
        fssPage.setWindowTitle(_translate("fssPage", "Доступ к сервису СФР", None))
        fssPage.setToolTip(_translate("fssPage", "Настройки доступа к сервисам СФР", None))
        self.lblProxyLogin.setText(_translate("fssPage", "&Сертификат СФР", None))
        self.lblProxyPort.setText(_translate("fssPage", "&порт", None))
        self.lblServiceUrl.setText(_translate("fssPage", "&URL сервиса ЭЛН", None))
        self.lblProxyPassword.setText(_translate("fssPage", "па&роль", None))
        self.chkUseProxy.setText(_translate("fssPage", "Использовать прокси-&сервер", None))
        self.chkUseEncryption.setText(_translate("fssPage", "Использовать &шифрование сообщений", None))
        self.lblFssCert.setText(_translate("fssPage", "&Сертификат СФР", None))
        self.lblProxyAddress.setText(_translate("fssPage", "&Адрес сервера", None))
        self.chkProxyUseAuth.setText(_translate("fssPage", "Прокси-сервер требует ау&тентификацию", None))

from library.CertComboBox import CCertComboBox
