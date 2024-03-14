# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

# редактор разных умолчаний


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QVariant

from library.MSCAPI           import MSCApi

from library.Utils            import (
                                       exceptionToUnicode,
                                       forceBool,
                                       forceInt,
                                       forceRef,
                                       forceString,
                                       toVariant,
                                     )

from Orgs.Orgs                import selectOrganisation

from Ui_appPreferencesDialog  import Ui_appPreferencesDialog


class CAppPreferencesDialog(QtGui.QDialog, Ui_appPreferencesDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.userCertSha1 = ''
        self.fssCertSha1 = ''
        self.api = None

        self.setupUi(self)

        self.edtRequestedNumbersQuantity.setRange( QtGui.qApp.minRequestedNumbersQuantity,
                                                   QtGui.qApp.maxRequestedNumbersQuantity
                                                 )

        self.cmbCsp.addItem(u'-',              '')
        self.cmbCsp.addItem(u'Крипто-Про CSP', 'cryptopro')
        self.cmbCsp.addItem(u'ViPNet CSP',     'vipnet')
        self.cmbCsp.setCurrentIndex(0)


    def setProps(self, props):
        self.userCertSha1 = forceString(props.get('userCertSha1', '')).lower()
        self.fssCertSha1 = forceString(props.get('fssCertSha1', '')).lower()

        self.cmbOrganisation.setValue(forceRef(props.get('orgId', None)))
        self.cmbOrgStructure.setValue(forceRef(props.get('orgStructureId', None)))
        self.edtRequestedNumbersQuantity.setValue(forceInt(props.get('requestedNumbersQuantity', QtGui.qApp.defaultRequestedNumbersQuantity)))
        self.cmbCsp.setCurrentIndex( max(0, self.cmbCsp.findData(props.get('csp', QVariant()),  Qt.UserRole, Qt.MatchExactly)) )
        if forceBool(props.get('useOwnPk', True)):
            self.rbnOwnPK.setChecked(True)
        else:
            self.rbnCustomPK.setChecked(True)
        self.edtServiceUrl.setText(forceString(props.get('serviceUrl', '')))
        self.chkUseEncryption.setChecked(forceBool(props.get('useEncryption', True)))

        self.chkUseProxy.setChecked(forceBool(props.get('useProxy', False)))
        self.edtProxyAddress.setText(forceString(props.get('proxyAddress', '')))
        self.edtProxyPort.setValue(forceInt(props.get('proxyPort', 0)))
        self.chkProxyUseAuth.setChecked(forceBool(props.get('proxyUseAuth', False)))
        self.edtProxyLogin.setText(forceString(props.get('proxyLogin', '')))
        self.edtProxyPassword.setText(forceString(props.get('proxyPassword', '')))


    def props(self):
        result = {
            'orgId':          toVariant(self.cmbOrganisation.value()),
            'orgStructureId': toVariant(self.cmbOrgStructure.value()),
            'requestedNumbersQuantity': toVariant(self.edtRequestedNumbersQuantity.value()),
            'csp':            self.cmbCsp.itemData(self.cmbCsp.currentIndex()),
            'useOwnPk':       toVariant(self.rbnOwnPK.isChecked()),
            'userCertSha1':   toVariant(self.cmbUserCert.value()),
            'serviceUrl':     toVariant(self.edtServiceUrl.text()),
            'useEncryption':  toVariant(self.chkUseEncryption.isChecked()),
            'fssCertSha1':    toVariant(self.cmbFssCert.value()),

            'useProxy':       toVariant(self.chkUseProxy.isChecked()),
            'proxyAddress':   toVariant(self.edtProxyAddress.text()),
            'proxyPort':      toVariant(self.edtProxyPort.value()),

            'proxyUseAuth':   toVariant(self.chkProxyUseAuth.isChecked()),
            'proxyLogin':     toVariant(self.edtProxyLogin.text()),
            'proxyPassword':  toVariant(self.edtProxyPassword.text()),
        }
        return result


    def _setCsp(self, csp):
        if csp:
            try:
                self.api = MSCApi(csp)
            except Exception, e:
                QtGui.QMessageBox.critical( self,
                                            u'Произошла ошибка подключения к криптопровайдеру',
                                            exceptionToUnicode(e),
                                            QtGui.QMessageBox.Close)
                self.api = None
        else:
            self.api = None

        self.cmbUserCert.setApi(self.api)
        self.cmbFssCert.setApi(self.api)

        if self.api is None:
            self.rbnOwnPK.setEnabled(False)
            self.rbnCustomPK.setEnabled(False)
            self.cmbUserCert.setEnabled(False)
            self.cmbFssCert.setEnabled(False)
        else:
            self.rbnOwnPK.setEnabled(True)
            self.rbnCustomPK.setEnabled(True)
            self.cmbUserCert.setEnabled(self.rbnCustomPK.isChecked())
            self.cmbUserCert.setStores(self.api.SNS_OWN_CERTIFICATES)
            self.cmbUserCert.setValue(self.userCertSha1)
            self.cmbFssCert.setEnabled(self.chkUseEncryption.isChecked())
            self.cmbFssCert.setStores([self.api.SNS_OTHER_CERTIFICATES, self.api.SNS_OWN_CERTIFICATES])
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


    @pyqtSignature('int')
    def on_cmbOrganisation_currentIndexChanged(self, index):
        orgId = self.cmbOrganisation.value()
        self.cmbOrgStructure.setOrgId(orgId)


    @pyqtSignature('')
    def on_btnSelectOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbOrganisation.value(), False)
        self.cmbOrganisation.updateModel()
        if orgId:
            self.cmbOrganisation.setValue(orgId)


    @pyqtSignature('int')
    def on_cmbCsp_currentIndexChanged(self, index):
        if index < 0:
            self._setCsp( None )
        else:
            self._setCsp( forceString(self.cmbCsp.itemData(index)) )
#            if self.api is None:
#                self.cmbCsp.setCurrentIndex(-1)


    @pyqtSignature('bool')
    def on_rbnCustomPK_toggled(self, checked):
        self.cmbUserCert.setEnabled(self.api is not None and checked)


    @pyqtSignature('bool')
    def on_chkUseProxy_toggled(self, checked):
        self._tuneProxyWidgets()


    @pyqtSignature('bool')
    def on_chkProxyUseAuth_toggled(self, checked):
        self._tuneProxyWidgets()

