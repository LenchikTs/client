# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Объект, представляющий собой все данные идентификационной карты:
## Полиса, ЕКП и т.п.
##
#############################################################################

from PyQt4        import QtGui
from PyQt4.QtCore import Qt, QDate


from IdentCard               import CIdentCard, CIdentCardPolicy
from library.JsonRpc.client  import CJsonRpcClent
from library.Utils           import nameCase

__all__ = ( 'findIdentCard',
          )


def holderAsIdentCard(holder):
    def isoStrToQDate(s):
        return QDate.fromString(s, Qt.ISODate) if s else None

    if holder is None:
        return None
    result = CIdentCard()
    result.lastName   = nameCase(holder.get('lastName'))
    result.firstName  = nameCase(holder.get('firstName'))
    result.patrName   = nameCase(holder.get('patrName'))
    result.sex        = holder.get('sex', 0)
    result.birthDate  = isoStrToQDate(holder.get('birthDate'))
    result.birthPlace = holder.get('birthPlace')
    result.SNILS      = holder.get('SNILS')

    holderPolicy = holder.get('policy')
    if holderPolicy:
        result.policy  = policy = CIdentCardPolicy()
        policy.serial  = ''
        policy.number  = holderPolicy.get('number')
#        policy.insurerCode  = holderPolicy.get('insurerCode')
#        policy.insurerOgrn  = holderPolicy.get('insurerOgrn')
#        policy.insurerOkato = holderPolicy.get('insurerOkato')
        policy.begDate = isoStrToQDate(holderPolicy.get('begDate'))
        policy.endDate = isoStrToQDate(holderPolicy.get('endDate'))

    return result


def findIdentCard(identifierType, identifier):
    serviceUrl = QtGui.qApp.getIdentCardServiceUrl() # or 'http://serv/identCard/'
    if not serviceUrl:
        raise Exception(u'Не настроен URL сервиса')
    client = CJsonRpcClent(serviceUrl)
    result = client.call('search',
                         params={ 'identifierType': identifierType, 'identifier': identifier }
                        )
    return holderAsIdentCard(result.get('holder'))
