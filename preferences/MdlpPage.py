# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки - доступ к МДЛП
##
#############################################################################

import re

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QUrl

from library.Utils            import (
                                        exceptionToUnicode,
                                        forceBool,
                                        forceString,
                                        toVariant,
                                     )
try:
    from Exchange.MDLP import CMdlp
    mdlpErr = None
except Exception as e:
    mdlpErr = exceptionToUnicode(e)


from Ui_MdlpPage import Ui_mdlpPage


class CMdlpPage(Ui_mdlpPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.api = None
        self.userCertSha1 = None


    def setProps(self, props):
        # я забыл mdlpEnabled.
        # поэтому делаем попытку угадать по наличию каких-либо значений
        # в существенных полях -
        if 'mdlpEnabled' in props:
            mdlpEnabled = forceBool(props.get('mdlpEnabled', False))
        else:
            mdlpEnabled = bool(     forceString(props.get('mdlpUrl', ''))
                                and forceString(props.get('mdlpClientId', ''))
                                and forceString(props.get('mdlpClientSecret', ''))
                                and (   not forceBool(props.get('mdlpUseStunnel', False))
                                        or forceString(props.get('mdlpStunnelUrl',  ''))
                                    )
                              )

        self.chkMdlpEnabled.setChecked(mdlpEnabled)
        self.edtMdlpUrl.setText( forceString(props.get('mdlpUrl', '')))
        self.edtMdlpClientId.setText( forceString(props.get('mdlpClientId', '')))
        self.edtMdlpClientSecret.setText( forceString(props.get('mdlpClientSecret', '')))
        self.chkMdlpStunnel.setChecked(forceBool(props.get('mdlpUseStunnel', False)))
        self.edtMdlpStunnelUrl.setText(forceString(props.get('mdlpStunnelUrl',  '')))
        self.chkMdlpNotificationMode.setChecked(forceBool(props.get('mdlpNotificationMode', False)))


    def getProps(self, props):
        props['mdlpEnabled'] = toVariant(self.chkMdlpEnabled.isChecked())
        props['mdlpUrl'] = toVariant(self.edtMdlpUrl.text())
        props['mdlpClientId'] = toVariant(uuidOrEmpty(unicode(self.edtMdlpClientId.text())))
        props['mdlpClientSecret'] = toVariant(uuidOrEmpty(unicode(self.edtMdlpClientSecret.text())))
        props['mdlpUseStunnel'] = toVariant(self.chkMdlpStunnel.isChecked())
        props['mdlpStunnelUrl'] = toVariant(self.edtMdlpStunnelUrl.text())
        props['mdlpNotificationMode'] = toVariant(self.chkMdlpNotificationMode.isChecked())


    def setApi(self, api):
        self.api = api


    def setUserCertSha1(self,  userCertSha1):
        self.userCertSha1 = unicode(userCertSha1) or None


    def _checkParams(self, mdlpUrl, clientId, clientSecret, useStunnel, stunnelUrl):
        if not self.api:
            return False, u'Требуется настройка крипто-провайдера'
        if not self.userCertSha1:
            return False, u'Требуется настройка ключа пользователя'
        parsedMdlpUrl = QUrl(mdlpUrl, QUrl.StrictMode)
        if parsedMdlpUrl.isEmpty():
            return False, u'Требуется указание URL сервиса МДЛП'
        if (    not parsedMdlpUrl.isValid()
             or parsedMdlpUrl.scheme() not in ('http', 'https')
             or parsedMdlpUrl.host() == ''
             or parsedMdlpUrl.path() == ''
           ):
            return False, u'Требуется указание допустимого URL сервиса МДЛП'
        if not uuidOrEmpty(clientId):
            return False, u'Идентификатор клиента должен иметь вид UUID'
        if not uuidOrEmpty(clientSecret):
            return False, u'Секретный код (ключ) клиента должен иметь вид UUID'
        if useStunnel:
            parsedStunnelUrl = QUrl(stunnelUrl, QUrl.StrictMode)
            if (    parsedStunnelUrl.isEmpty()
                 or not parsedStunnelUrl.isValid()
                 or parsedStunnelUrl.scheme() not in ('http', )
                 or parsedStunnelUrl.host() == ''
                 or parsedStunnelUrl.path() != ''
               ):
                return False, u'Требуется указание URL сервиса stunnel в виде http://host[:port]'
        return True, ''


    @pyqtSignature('bool')
    def on_chkMdlpEnabled_toggled(self, value):
        for widget in ( self.lblMdlpUrl, self.edtMdlpUrl,
                        self.lblMdlpClientId, self.edtMdlpClientId,
                        self.lblMdlpClientSecret, self.edtMdlpClientSecret,
                        self.chkMdlpStunnel,
                        self.lblMdlpNotificationMode, self.chkMdlpNotificationMode,
                        self.btnMdlpTest,
                      ):
            widget.setEnabled(value)

        self.edtMdlpStunnelUrl.setEnabled(value and self.chkMdlpStunnel.isChecked())


    @pyqtSignature('bool')
    def on_chkMdlpStunnel_toggled(self, value):
        self.edtMdlpStunnelUrl.setEnabled(value and self.chkMdlpEnabled.isChecked())


    @pyqtSignature('')
    def on_btnMdlpTest_clicked(self):
        try:
            mdlpUrl  = unicode(self.edtMdlpUrl.text())
            clientId = unicode(self.edtMdlpClientId.text())
            clientSecret = unicode(self.edtMdlpClientSecret.text())
            useStunnel = self.chkMdlpStunnel.isChecked()
            stunnelUrl = unicode(self.edtMdlpStunnelUrl.text())
            ok, message = self._checkParams(mdlpUrl, clientId, clientSecret, useStunnel, stunnelUrl)
            if not ok or mdlpErr:
                QtGui.QMessageBox.information(self,
                                              u'Проверка соединения с МДЛП',
                                              message or mdlpErr,
                                              QtGui.QMessageBox.Close,
                                              QtGui.QMessageBox.Close)
                return
            mdlp = CMdlp(self.api, mdlpUrl)
            if useStunnel:
                mdlpHostUrl = unicode(QUrl(mdlpUrl).toString(QUrl.RemoveUserInfo|QUrl.RemovePath|QUrl.RemoveQuery|QUrl.RemoveFragment))
                mdlp.setStunnel(mdlpHostUrl, stunnelUrl)

            mdlp.auth( clientId     = clientId,
                       clientSecret = clientSecret,
                       certHash     = self.userCertSha1
                     )
            mdlp.getIncomingDocuments(count=1)
            mdlp.close()
            QtGui.QMessageBox.information(self,
                                          u'Проверка соединения с МДЛП',
                                          u'Завершено успешно',
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)
        except Exception as e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.information(self,
                                          u'Проверка соединения с МДЛП',
                                          exceptionToUnicode(e),
                                          QtGui.QMessageBox.Close,
                                          QtGui.QMessageBox.Close)


def uuidOrEmpty(v):
    if re.match('([0-9a-f]{8})-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{8}', v, re.IGNORECASE):
        return v
    else:
        return None
