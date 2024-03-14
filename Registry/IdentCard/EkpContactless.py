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
## полученных через бесконтактный интерфейс
##
#############################################################################


from IdentCardService import findIdentCard
from library.SmartCard import hexDump

__all__ = ( 'CEkpContactless',
          )


class CEkpContactless:
    atrHexDump = '3B 86 80 01 C1 05 2F 2F 01 BC 7E'


    @classmethod
    def atrIsSuitable(cls, atrHexDump):
        return atrHexDump == cls.atrHexDump


    def __init__(self, connection):
        self.connection = connection


    def asIdentCard(self):
#        try:
        if 1:
            mifareUid = hexDump(self.getMifareUid(), '')
            if mifareUid:
                return findIdentCard('mifareUid', mifareUid)
#                return getIdentCard('cardId', '7869607882141218')
        return None


    def getMifareUid(self):
        data, sw1, sw2 = self.connection.transmit([0xFF, # cla
                                                   0xCA, # ins
                                                   0x00, # p1
                                                   0x00, # p2
                                                   0x00, # len
                                                  ]
                                                 )
        return data if sw1 == 0x90 and sw2 == 0x00 else None

