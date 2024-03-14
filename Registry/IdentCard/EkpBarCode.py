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

from IdentCardService import findIdentCard
from library.luhn import checkLuhn


__all__ = ( 'isEkpCardId',
            'ekpIdAsIdentCard',
            'tryCardIdAsEkpIdentCard',
          )

def isEkpCardId(data):
    return len(data) == 16 and data.isdigit() and data.startswith('78') and checkLuhn(data)


def ekpIdAsIdentCard(identifier):
#    return getIdentCard('cardId', '7869607882141218')
    return findIdentCard('cardId', identifier)


def tryCardIdAsEkpIdentCard(data):
    return ekpIdAsIdentCard(data) if isEkpCardId(data) else None
