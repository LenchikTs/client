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
## Определение типа штрих-кода 
## по идентификатору символики (symbology identifier)
## по ГОСТ ISO/IEC 15424—2018
##
#############################################################################

import string

__all__ = ('hasSymbologyId',
           'getSymbologyIdLen',
           'stripSymbologyId',
           'isCode39',
           'isCode128',
           'isEan13',
           'isPdf417',
           'isPdf417DoubleBackslash',
           'isQrCode',
           'isGS1'
          )


def hasSymbologyId(data):
    u'В коде присутствует идентификатор символики'
    return len(data) >= 3 and data.startswith(']') and data[1] in string.ascii_letters and (0x20 <= ord(data[2]) <= 0x7F)


def getSymbologyIdLen(data):
    u'Получить длину идентификатора символики если есть; иначе 0'
    return 3 if hasSymbologyId(data) else 0


def stripSymbologyId(data):
    u'Удалить идентификатор символики'
    return data[getSymbologyIdLen(data):]


def isCode39(data):
    u'Это Code 39 (обычно используется для ClientId)'
    return data.startswith(']A')


def isCode128(data):
    u'Это Code 128 (обычно используется для маркировки биоматериалов)'
    return data.startswith(']C')


def isEan13(data):
    u'Это код товара (GTIN)'
    return data.startswith(']E0')


def isDataMatrix(data):
    u'Это DataMatrix'
    return data.startswith(']d')


def isPdf417(data):
    u'Это PDF417 (полис)'
    return data.startswith(']L')


def isPdf417WithDoubleBackslash(data):
    u'Этот PDF417 удваивает обратную косую: True/False/None'
    if data.startswith(']L1'):
        return True
    if data.startswith(']L2'):
        return False
    return None


def isQrCode(data):
    u'Это QR Code (на ЕКП)'
    return data.startswith(']Q')


def isGS1(data):
    u'Это код для кодирования КИЗ: sgtin & sscc'
    return data.startswith(( ']C1', # GS1-128 Standard AI element strings
                             ']e0', # GS1 DataBar; у нас не применяется
                             ']d2', # GS1 DataMatrix
                             ']Q3', # GS1 QR Code; у нас не применяется
                             ']J1', # GS1 DotCode; у нас не применяется, сканеры не поддерживают
                             ']z1', # Aztec with GS1; в GS1 General Specifications не описано, у нас не применяется, не все сканеры поддерживают
                           )
                          )

