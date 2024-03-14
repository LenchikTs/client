# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import hashlib

__all__ = [ 'calcCheckSum',
          ]

def calcCheckSum(fileName):
    sum = hashlib.md5()
    f = open(fileName, 'rb')
    while True:
        s = f.read(65536)
        if not s:
            break
        sum.update(s)
    return sum.hexdigest()