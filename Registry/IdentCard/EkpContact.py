# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Класс для декодирования данных ЕКП
## полученных через контактный интерфейс
##
#############################################################################

from ctypes import (
                      CDLL,
                      POINTER,
                      c_char_p,
                      c_int,
                      cast,
                      create_string_buffer,
                      byref,
                   )

from PyQt4 import QtGui

from IdentCardService  import findIdentCard

__all__ = ( 'CEkpContact',
          )


class CEkpContact:
    atrHexDump = '3B 68 00 00 00 73 C8 40 11 00 90 00'


    @classmethod
    def atrIsSuitable(cls, atrHexDump):
        return atrHexDump == cls.atrHexDump


    def __init__(self, connection):
        self.connection = connection


    def asIdentCard(self):
        cardId = self.getCardId()
        if cardId:
            return findIdentCard('cardId', cardId)
        return None


    def getCardId(self):
        libPath = QtGui.qApp.ekpContactLib()
        ekpLib = CDLL(libPath)

        _Authorization = ekpLib.Authorization
        _Authorization.argtypes = [c_char_p]
        _Authorization.restype = c_int

        _GetID = ekpLib.GetID
        _GetID.argtypes = [c_char_p, POINTER(c_char_p)]
        _GetID.restype = c_int

        _ReleaseData = ekpLib.ReleaseData
        _ReleaseData.argtypes = [c_char_p]
        _ReleaseData.restype = None

        password = create_string_buffer('94D5CD528592CB9E349868E5E626737F')
        retCode = _Authorization(cast(password, c_char_p))
        if retCode != 0x9000:
            return None

        pCardId = c_char_p()
        retCode = _GetID(self.connection.getReader(), byref(pCardId))
        if retCode != 0x9000:
            return None
        result = pCardId.value

        _ReleaseData(pCardId)
        return result
