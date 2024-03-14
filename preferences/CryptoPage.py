# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки крипто-провайдера и выбор ключа
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDateTime

from library.MSCAPI           import MSCApi
from library.Utils            import (
                                         exceptionToUnicode,
                                         forceBool,
                                         forceInt,
                                         forceString,
                                         formatDays,
                                         toVariant,
                                     )

from Ui_CryptoPage import Ui_cryptoPage


class CCryptoPage(Ui_cryptoPage, QtGui.QWidget):
    __pyqtSignals__ = ('apiChanged(PyQt_PyObject)',
                       'userCertChanged(QString)', # если строка пуста - нет сертификата
                      )



    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cmbCsp.addItem(u'-',              '')
        self.cmbCsp.addItem(u'Крипто-Про CSP', 'cryptopro')
        self.cmbCsp.addItem(u'ViPNet CSP',     'vipnet')
        self.cmbCsp.setCurrentIndex(0)
        self.userCertSha1 = ''
        self.orgCertSha1 = ''


    def setProps(self, props):
        self.userCertSha1 = forceString(props.get('userCertSha1', '')).lower()
        self.orgCertSha1 = forceString(props.get('orgCertSha1', '')).lower()
        if forceBool(props.get('useOwnPk', True)):
            self.rbnOwnPK.setChecked(True)
        else:
            self.rbnCustomPK.setChecked(True)
        self.cmbCsp.setCurrentIndex( max(0, self.cmbCsp.findData(toVariant(props.get('csp')),  Qt.UserRole, Qt.MatchExactly)) )
        self.chkWarnAboutCertExpiration.setChecked(forceBool(props.get('warnAboutCertExpiration', False)))
        self.edtCertExpirationWarnPeriod.setValue(forceInt(props.get('certExpirationWarnPeriod', 7)))



    def getProps(self, props):
        props['csp']          = self.cmbCsp.itemData(self.cmbCsp.currentIndex())
        props['useOwnPk']     = toVariant(self.rbnOwnPK.isChecked())
        props['userCertSha1'] = self.cmbUserCert.value()
        props['orgCertSha1']  = self.cmbOrgCert.value()
        props['warnAboutCertExpiration']  = toVariant( self.chkWarnAboutCertExpiration.isChecked())
        props['certExpirationWarnPeriod'] = toVariant( self.edtCertExpirationWarnPeriod.value())


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
        self.cmbOrgCert.setApi(self.api)
        if self.api is None:
            self.rbnOwnPK.setEnabled(False)
            self.rbnCustomPK.setEnabled(False)
            self.cmbUserCert.setEnabled(False)
            self.lblOrgCert.setEnabled(False)
            self.cmbOrgCert.setEnabled(False)
        else:
            self.rbnOwnPK.setEnabled(True)
            self.rbnCustomPK.setEnabled(True)
            self.cmbUserCert.setEnabled(self.rbnCustomPK.isChecked())
            self.cmbUserCert.setStores(self.api.SNS_OWN_CERTIFICATES)
            self.cmbUserCert.setValue(self.userCertSha1)
            self.lblOrgCert.setEnabled(True)
            self.cmbOrgCert.setEnabled(True)
            self.cmbOrgCert.setStores(self.api.SNS_OWN_CERTIFICATES)
            self.cmbOrgCert.setValue(self.orgCertSha1)
        self.emit(SIGNAL('apiChanged(PyQt_PyObject)'), self.api)
        self._emitUserCertChanged()


    def _emitUserCertChanged(self):
        if self.api:
            userCertSha1 = ''
            if self.rbnOwnPK.isChecked():
                now = QDateTime.currentDateTime().toPyDateTime()
                try:
                    snils = QtGui.qApp.getUserSnils()
                except Exception:
                    snils = None
                if snils:
                    ogrn = QtGui.qApp.getCurrentOrgOgrn()
                    cert = self.api.findCertInStores(self.api.SNS_OWN_CERTIFICATES,
                                                     snils=snils,
                                                     datetime=now,
                                                     weakOgrn=ogrn
                                                     )
                    if cert:
                        userCertSha1 = cert.sha1()
            else:
                userCertSha1 = self.cmbUserCert.value()
            self.emit(SIGNAL('userCertChanged(QString)'), userCertSha1 or '')


    @pyqtSignature('int')
    def on_cmbCsp_currentIndexChanged(self, idx):
        if idx < 0:
            self._setCsp( None )
        else:
            self._setCsp( forceString(self.cmbCsp.itemData(idx)) )


    @pyqtSignature('bool')
    def on_rbnCustomPK_toggled(self, checked):
        self._emitUserCertChanged()


    @pyqtSignature('int')
    def on_cmbUserCert_currentIndexChanged(self, index):
        self._emitUserCertChanged()


    @pyqtSignature('int')
    def on_edtCertExpirationWarnPeriod_valueChanged(self, val):
        self.lblCertExpirationWarnPeriod.setText(formatDays(val))

