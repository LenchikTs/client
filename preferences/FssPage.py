# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2022-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки взаимодействия с сервисом СФР
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.Utils import forceBool, forceInt, forceString, toVariant
from Users.Rights import urAdmin, urAccessSetupDefault
from Ui_FssPage import Ui_fssPage


class CFssPage(Ui_fssPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.fssCertSha1 = ''
        if not QtGui.qApp.userHasAnyRight([urAdmin, urAccessSetupDefault]):
            self.chkUseEncryption.setEnabled(False)
            self.cmbFssCert.setEnabled(False)
            self.chkUseProxy.setEnabled(False)
            self.edtProxyAddress.setEnabled(False)
            self.edtProxyPort.setEnabled(False)
            self.chkProxyUseAuth.setEnabled(False)
            self.edtProxyLogin.setEnabled(False)
            self.edtProxyPassword.setEnabled(False)

    def setProps(self, props):
        self.fssCertSha1 = forceString(props.get('fssCertSha1', '')).lower()

        self.edtServiceUrl.setText(forceString(props.get('fssServiceUrl', '')))
        # self.edtServiceERSUrl.setText(forceString(props.get('fssServiceERSUrl', '')))
        self.chkUseEncryption.setChecked(forceBool(props.get('fssUseEncryption', True)))
        if self.cmbFssCert.isEnabled() and self.fssCertSha1:
            self.cmbFssCert.setValue(self.fssCertSha1)

        self.chkUseProxy.setChecked(forceBool(props.get('fssUseProxy', False)))
        self.edtProxyAddress.setText(forceString(props.get('fssProxyAddress', '')))
        self.edtProxyPort.setValue(forceInt(props.get('fssProxyPort', 0)))

        self.chkProxyUseAuth.setChecked(forceBool(props.get('fssProxyUseAuth', False)))
        self.edtProxyLogin.setText(forceString(props.get('fssProxyLogin', '')))
        self.edtProxyPassword.setText(forceString(props.get('fssProxyPassword', '')))

    def getProps(self, props):
        props['fssServiceUrl']    = toVariant(self.edtServiceUrl.text())
        # props['fssServiceERSUrl'] = toVariant(self.edtServiceERSUrl.text())
        props['fssUseEncryption'] = toVariant(self.chkUseEncryption.isChecked())
        props['fssCertSha1']      = toVariant(self.cmbFssCert.value())

        props['fssUseProxy']     = toVariant(self.chkUseProxy.isChecked())
        props['fssProxyAddress'] = toVariant(self.edtProxyAddress.text())
        props['fssProxyPort']    = toVariant(self.edtProxyPort.value())

        props['fssProxyUseAuth']  = toVariant(self.chkProxyUseAuth.isChecked())
        props['fssProxyLogin']    = toVariant(self.edtProxyLogin.text())
        props['fssProxyPassword'] = toVariant(self.edtProxyPassword.text())

    def setApi(self, api):
        self.cmbFssCert.setApi(api)
        if api is None:
            self.cmbFssCert.setEnabled(False)
        else:
            if QtGui.qApp.userHasAnyRight([urAdmin, urAccessSetupDefault]):
                self.cmbFssCert.setEnabled(self.chkUseEncryption.isChecked())
            self.cmbFssCert.setStores([api.SNS_OTHER_CERTIFICATES, api.SNS_OWN_CERTIFICATES])
            self.cmbFssCert.setValue(self.fssCertSha1)

    def _tuneProxyWidgets(self):
        useProxy = self.chkUseProxy.isChecked()
        proxyUseAuth = self.chkProxyUseAuth.isChecked()
        self.lblProxyAddress.setEnabled(useProxy)
        self.edtProxyAddress.setEnabled(useProxy)
        self.lblProxyPort.setEnabled(useProxy)
        self.edtProxyPort.setEnabled(useProxy)
        self.chkProxyUseAuth.setEnabled(useProxy)
        self.lblProxyLogin.setEnabled(useProxy and proxyUseAuth)
        self.edtProxyLogin.setEnabled(useProxy and proxyUseAuth)
        self.lblProxyPassword.setEnabled(useProxy and proxyUseAuth)
        self.edtProxyPassword.setEnabled(useProxy and proxyUseAuth)

    @pyqtSignature('bool')
    def on_chkUseProxy_toggled(self, checked):
        self._tuneProxyWidgets()

    @pyqtSignature('bool')
    def on_chkProxyUseAuth_toggled(self, checked):
        self._tuneProxyWidgets()
