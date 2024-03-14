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

class CIdentCard:
    def __init__(self):
        self.lastName    = None
        self.firstName   = None
        self.patrName    = None
        self.sex         = None
        self.birthDate   = None
        self.birthPlace  = None
        self.SNILS       = None
        self.citizenship = None
        self.policy      = None
        self.document    = None # не заполняется и не используется
        self.regAddress  = None # не заполняется и не используется
        self.locAddress  = None # не заполняется и не используется


class CIdentCardPolicy:
    def __init__(self):
        self.serial      = None
        self.number      = None
        self.begDate     = None
        self.endDate     = None
#        self.insurerOgrn = None
#        self.insurerOkato= None
#        self.insurerCode = None
        self.insurerId   = None

        



