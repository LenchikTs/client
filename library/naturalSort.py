# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## "сортировка в естественном поряде"
## можно сортировать номера домов или буквенно-цифровые коды
##
#############################################################################

def convertKeyForNaturalSort(key):
    result = ''
    prevIsDigit = False
    digits = ''
    for c in key:
        if c.isdigit():
            if prevIsDigit:
                if digits or c != '0':
                    digits += c
            else:
                if c != '0':
                    digits = c
                else:
                    digits = ''
            prevIsDigit = True
        else:
            if prevIsDigit:
               digits = digits or '0'
               result += '%04d%s' % ( len(digits)-1, digits)
               prevIsDigit = False
            result += c

    if prevIsDigit:
        digits = digits or '0'
        result += '%04d%s' % ( len(digits)-1, digits)

    return result


def naturalSorted(l, reverse=False):
    return sorted(l,  key=convertKeyForNaturalSort, reverse=reverse)

