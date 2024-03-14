# -*- coding: utf-8 -*-
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# Это соединение с МДЛП, знающее про QDate и QDateTime
# и умеющее вычитывать настройки приложения


from PyQt4 import QtGui
from PyQt4.QtCore import QUrl, QDate, QDateTime

from library.exception import CException
from library.MSCAPI import MSCApi
from library.Utils import exceptionToUnicode

try:
    from Exchange.MDLP import CMdlp
    mdlpErr = None
except Exception as e:
    mdlpErr = exceptionToUnicode(e)
    CMdlp = object


class CMdlpConnection(CMdlp):
    def __init__(self):
        if mdlpErr:
            raise CException(mdlpErr)

        qApp = QtGui.qApp
        api = MSCApi(qApp.getCsp())

        mdlpUrl, clientId, secret, useStunnel, stunnelUrl, notificationMode = qApp.getMdlpPrefs()
        if (    not mdlpUrl
             or not clientId
             or not secret
             or (useStunnel and not stunnelUrl)
           ):
            raise CException(u'Соединение с МДЛП не настроено')

        CMdlp.__init__(self, api, mdlpUrl)
        if useStunnel:
            mdlpHostUrl = unicode(QUrl(mdlpUrl).toString(QUrl.RemoveUserInfo|QUrl.RemovePath|QUrl.RemoveQuery|QUrl.RemoveFragment))
            self.setStunnel(mdlpHostUrl, stunnelUrl)

        self.setAuth(clientId     = clientId,
                     clientSecret = secret,
                     certHash     = qApp.getUserCertSha1()
                    )

        self.notificationMode = notificationMode

    def __del__(self):
        self.close()


    @classmethod
    def _dateToStr(cls, dateOrDatetime):
        if isinstance(dateOrDatetime, QDateTime):
            return CMdlp._dateToStr(dateOrDatetime.toPyDateTime())
        elif isinstance(dateOrDatetime, QDate):
            return CMdlp._dateToStr(dateOrDatetime.toPyDate())
        else:
            return CMdlp._dateToStr(dateOrDatetime)


    @classmethod
    def _dateToStrUp(cls, dateOrDatetime):
        if isinstance(dateOrDatetime, QDateTime):
            return CMdlp._dateToStrUp(dateOrDatetime.toPyDateTime())
        elif isinstance(dateOrDatetime, QDate):
            return CMdlp._dateToStrUp(dateOrDatetime.toPyDate())
        else:
            return CMdlp._dateToStrUp(dateOrDatetime)



    @classmethod
    def _strToDateTime(cls, s):
        r = CMdlp._strToDateTime(s)
        if r is None:
            return None
        else:
            return QDateTime(r)


    @classmethod
    def _strToDate(cls, s):
        r = CMdlp._strToDate(s)
        if r is None:
            return None
        else:
            return QDate(r)

