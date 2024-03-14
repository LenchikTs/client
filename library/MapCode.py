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
import re

ord0 = ord('0')
ordA = ord('A')

startChar = re.compile('^[A-Z]')
threeChar = re.compile('^[A-Z][0-9][0-9]$')
fourChar  = re.compile('^[A-Z][0-9][0-9]\.[0-9]$')
threeOrFourChar = re.compile('^[A-Z][0-9][0-9](\.[0-9])?$')
sixChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9])?$')
sevenChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9])?$')
eightChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9])?$')
nineChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9][0-9])?$')


def normalizeCode(prefix, code):
    code = code.strip().upper()
#    if re.match('^[A-Z]', code) is not None:
    if startChar.match(code):
        codeParts = code.split('.')
        prefix = codeParts[0]
    else:
        assert prefix
        code = prefix + '.' + code
#    assert  re.match('^[A-Z][0-9][0-9](\.[0-9])?$', code) is not None
    if len(code) == 6:
        assert sixChar.match(code) is not None
    elif len(code) == 7:
        assert sevenChar.match(code) is not None
    elif len(code) == 8:
        assert eightChar.match(code) is not None
    elif len(code) == 9:
        assert nineChar.match(code) is not None
    else:
        assert threeOrFourChar.match(code) is not None
    return prefix, code


def addCodesRange(rowIdx, lowCode, highCode, mapCodesToRowIdx):
    def convCodeToNumber(code):
        r = (ord(code[0])-ordA)
        r = r*10 + (ord(code[1])-ord0)
        r = r*10 + (ord(code[2])-ord0)
        r = r*10 + (ord(code[4])-ord0)
        return r

    def convNumberToCode(num):
        return '%c%c%c.%c' % (num/1000+ordA,
                              (num/100)%10+ord0,
                              (num/10)%10+ord0,
                              (num)%10+ord0)
#        return chr(num/2600+ordA)+chr((num/100)%10+ord0)+chr((num/10)%10+ord0)+'.'+chr((num)%10+ord0)


    assert  lowCode <= highCode

#    if re.match('^[A-Z][0-9][0-9]$', lowCode) is not None:
    if threeChar.match(lowCode):
        lowCode = lowCode + '.0'
#    if re.match('^[A-Z][0-9][0-9]$', highCode) is not None:
    if threeChar.match(highCode):
        highCode = highCode + '.9'

    low  = convCodeToNumber(lowCode)
    high = convCodeToNumber(highCode)
    for i in xrange(low, high+1):
        code = convNumberToCode(i)
        mapCodesToRowIdx.setdefault(code,[]).append(rowIdx)


def addCode(rowIdx, code, mapCodesToRowIdx):
#    if re.match('^[A-Z][0-9][0-9]\.[0-9]', code) is not None:
    if fourChar.match(code):
        mapCodesToRowIdx.setdefault(code,[]).append(rowIdx)
#    elif re.match('^[A-Z][0-9][0-9]$', code) is not None:
    elif threeChar.match(code):
        addCodesRange(rowIdx, code, code, mapCodesToRowIdx)


def parseRowCodes(rowIdx, codes, mapCodesToRowIdx):
    diagRanges = codes.split(',')
    for tempDiagRange in diagRanges:
        tenpDiagLimits = tempDiagRange.split('-')
        n = len(tenpDiagLimits)
        if n == 1 and tenpDiagLimits[0]:
            if 'x' in tenpDiagLimits[0]:
                for i in range(10):
                    diagRanges.append(tenpDiagLimits[0].replace('x', str(i)))
                diagRanges.remove(tenpDiagLimits[0])
    # print diagRanges
    prefix = ''
    for diagRange in diagRanges:
        diagLimits = diagRange.split('-')
        n = len(diagLimits)
        if n == 1 and diagLimits[0]:
            prefix, code = normalizeCode(prefix, diagLimits[0])
            addCode(rowIdx, code, mapCodesToRowIdx)
        elif n == 2:
            prefix, lowCode  = normalizeCode(prefix, diagLimits[0])
            prefix, highCode = normalizeCode(prefix, diagLimits[1])
            addCodesRange(rowIdx, lowCode, highCode, mapCodesToRowIdx)
        else:
            assert False, 'Wrong codes range "'+diagRange+'"';


def createMapCodeToRowIdx( codesList ):
    mapCodeToRowIdx = {}
    for rowIdx, code in enumerate(codesList):
        if u'(часть)' in code:
            code = code.replace(u'(часть)', '')
        if code:
            parseRowCodes(rowIdx, str(code), mapCodeToRowIdx)
    return mapCodeToRowIdx