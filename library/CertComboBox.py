# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Комбо-бокс для выбора сертификата
## используется MS CAPI,
## в качестве значения используется sha1 сертификата
##
#############################################################################

from PyQt4         import QtGui
from PyQt4.QtCore  import Qt, SIGNAL, QDateTime

from library.Utils import (
                            forceString,
                            formatSNILS,
                          )

from library.PrintTemplates import escape

__all__ = ('CCertComboBox',
           'extractCertInfo',
          )


class CCertComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self.api = None
        self.stores = []
#        self.connect(self, SIGNAL('currentIndexChanged(int)'), self.updateTooltipAccordingIndex)
        # «New style connect»
        self.currentIndexChanged.connect(self.updateTooltipAccordingIndex)


    def setApi(self, api):
        self.api = api
        self.updateCertsList()


    def setStores(self, stores):
        if type(stores) is list:
            tuple_of_tuples = tuple()
            for x in stores:
                tuple_of_tuples += tuple(x)
            self.stores = tuple_of_tuples
        else:
            self.stores = stores
        self.updateCertsList()


    def updateCertsList(self):
        self.clear()
        if self.api and self.stores:
            items = set([])
            for storeName in self.stores:
                with self.api.systemStore(storeName) as store:
                    for cert in store.listCerts():
                        with cert:
                            key, text, tooltip = extractCertInfo(cert)
                            items.add((text, key, tooltip))

            self.addItem(u'не задано', None)
            self.setItemData(0, u'Сертификат не выбран', Qt.ToolTipRole)

            for text, key, tooltip in sorted(items):
                self.addItem(text, key)
                self.setItemData(self.count()-1, tooltip, Qt.ToolTipRole)
        self.updateTooltipAccordingIndex(self.currentIndex())


#    def setValue(self, certSha1):
#        self.setCurrentIndex( self.findData(certSha1, Qt.UserRole, Qt.MatchExactly) )

    def setValue(self, certSha1):
        idx = self.findData(certSha1 or None, Qt.UserRole, Qt.MatchExactly)
        if idx<0:
            idx = self.count()
            self.addItem(u'{%s}'%certSha1, certSha1)
            self.setItemData(idx, u'Значение установлено, но сертификат не доступен, подпись будет невозможна', Qt.ToolTipRole)
        self.setCurrentIndex(idx)


    def value(self):
        currentIndex = self.currentIndex()
        if currentIndex>=0:
            return forceString(self.itemData(currentIndex)) or None
        else:
            return None


    def updateTooltipAccordingIndex(self, idx):
        if 0<=idx<self.count():
            self.setToolTip(self.itemData(idx, Qt.ToolTipRole).toString())
        else:
            self.setToolTip('')


def extractCertInfo(cert):
    commonName      = cert.commonName()
    country         = cert.country()
    stateOrProvince = cert.state()
    locality        = cert.locality()
    address         = cert.streetAddress()
    org             = cert.org()
    orgUnit         = cert.orgUnit()
    title           = cert.title()
    surName         = cert.surName()
    givenName       = cert.givenName()
    email           = cert.email()
    ogrn            = cert.ogrn()
    inn             = cert.inn()
    snils           = cert.snils()
    if snils:
        snils = formatSNILS(snils)

    keyOid          = cert.keyOid()
    keyOidName      = cert.keyOidName()

    issuerName      = cert.issuerName()
    serialNumber    = cert.serialNumber()
    notBefore       = forceString(QDateTime(cert.notBefore()))
    notAfter        = forceString(QDateTime(cert.notAfter()))

    if surName and givenName:
        name = u'%s %s' % (surName, givenName)
    else:
        name = commonName or org or ''

    text = u'%s, действ. с %s по %s [%s]' % (
                                              name,
                                              notBefore,
                                              notAfter,
                                              keyOidName
                                            )
    key = cert.sha1().encode('hex').lower()
    items = (
                (u'Общее название',     commonName),
                (u'Страна',             country),
                (u'Штат или провинция', stateOrProvince),
                (u'Местность (город)',  locality),
                (u'Адрес',              address),
                (u'Организация',        org),
                (u'Подразделение',      orgUnit),
                (u'Должность',          title),
                (u'Фамилия',            surName),
                (u'Имя, Отчество',      givenName),
                (u'Email',              email),
                (u'ИНН',                inn),
                (u'ОГРН',               ogrn),
                (u'СНИЛС',              snils),
                (u'Ключ',               '%s (%s)' % (keyOidName, keyOid)),
                (u'Издатель',           issuerName),
                (u'Cерийный номер',     serialNumber),
                (u'Действителен с',     notBefore),
                (u'Действителен по',    notAfter),
                (u'Хэш SHA1',           key),
            )
    tooltip = (    '<html><body><table>'
                 + ''.join('<tr><td>%s:</td><td>%s</td></tr>' % (title, escape(value or u'⌧')) for title, value in items)
                 + '</table></body></html>'
              )
    return key, text, tooltip
