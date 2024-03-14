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
##
## integer <--> roman converse. Thanks to wikipedia!
##
#############################################################################


tab = [ ('M',  1000),
        ('CM',  900),
        ('D',   500),
        ('CD',  400),
        ('C',   100),
        ('XC',   90),
        ('L',    50),
        ('XL',   40),
        ('X',    10),
        ('IX',    9),
        ('V',     5),
        ('IV',    4),
        ('I',     1)]


def itor(n):
    result = ''
    for d, v in tab:
        while v <= n:
            result += d
            n -= v
    return result


def rtoi(r):
    ruc = unicode(r).upper()
    result = 0
    index = 0
    for d, v in tab:
        while ruc.startswith(d, index):
            result += v
            index += len(d)
    return result
