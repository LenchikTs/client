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

startChar = re.compile('^[A-Z]')
threeChar = re.compile('^[A-Z][0-9][0-9]$')
fourChar = re.compile('^[A-Z][0-9][0-9]\.[0-9]$')
threeOrFourChar = re.compile('^[A-Z][0-9][0-9](\.[0-9])?$')
sixChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9])?$')
sevenChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9])?$')
eightChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9])?$')
nineChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9][0-9])?$')

ord0 = ord('0')
ordA = ord('A')


def addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx):
    def convCodeToNumberSub(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        r = r * 10 + (ord(code[5]) - ord0)
        return r

    def convNumberToCodeSub(num):
        return '%c%c%c.%c%c' % (num / 10000 + ordA,
                                (num / 1000) % 10 + ord0,
                                (num / 100) % 10 + ord0,
                                (num / 10) % 10 + ord0,
                                (num) % 10 + ord0)

    def convCodeToNumberSub7(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        r = r * 10 + (ord(code[5]) - ord0)
        r = r * 10 + (ord(code[6]) - ord0)
        return r

    def convNumberToCodeSub7(num):
        return '%c%c%c.%c%c%c' % (num / 100000 + ordA,
                                (num / 10000) % 10 + ord0,
                                (num / 1000) % 10 + ord0,
                                (num / 100) % 10 + ord0,
                                (num / 10) % 10 + ord0,
                                (num) % 10 + ord0)

    def convCodeToNumber(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        return r

    def convNumberToCode(num):
        return '%c%c%c.%c' % (num / 1000 + ordA,
                              (num / 100) % 10 + ord0,
                              (num / 10) % 10 + ord0,
                              (num) % 10 + ord0)

    #        return chr(num/2600+ordA)+chr((num/100)%10+ord0)+chr((num/10)%10+ord0)+'.'+chr((num)%10+ord0)

    assert lowCode <= highCode

    #    if re.match('^[A-Z][0-9][0-9]$', lowCode) is not None:
    if threeChar.match(lowCode):
        lowCode = lowCode + '.0'
    #    if re.match('^[A-Z][0-9][0-9]$', highCode) is not None:
    if threeChar.match(highCode):
        highCode = highCode + '.9'

    if len(lowCode) == 6:
        low = convCodeToNumberSub(lowCode)
        high = convCodeToNumberSub(highCode)
    elif len(lowCode) == 7:
        low = convCodeToNumberSub7(lowCode)
        high = convCodeToNumberSub7(highCode)
    else:
        low = convCodeToNumber(lowCode)
        high = convCodeToNumber(highCode)
    for i in xrange(low, high + 1):
        if len(lowCode) == 6:
            code = convNumberToCodeSub(i)
        elif len(lowCode) == 7:
            code = convNumberToCodeSub7(i)
        else:
            code = convNumberToCode(i)
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)


def parseRowCodes(rowIdx, codes, mapCodesToRowIdx):
    diagRanges = codes.split(';')
    removeList = []
    for tempDiagRange in diagRanges:
        tempDiagLimits = tempDiagRange.split('-')
        n = len(tempDiagLimits)
        if n == 1 and tempDiagLimits[0] and 'x' in tempDiagLimits[0]:
            pos = tempDiagLimits[0].find('x')
            xRanges = tempDiagLimits[:]
            while pos > -1:
                for item in xRanges:
                    pos = item.find('x')
                    if pos > -1:
                        for i in range(10):
                            xRanges.append(item.replace('x', str(i), 1))
                        xRanges.remove(item)
                pos = xRanges[0].find('x')
            removeList.append(tempDiagLimits[0])
            diagRanges.extend(xRanges)

    for item in removeList:
        diagRanges.remove(item)

    prefix = ''
    for diagRange in diagRanges:
        diagSets = diagRange.split(',')
        if len(diagSets) > 1:
            for i, d in enumerate(diagSets):
                diagLimits = d.split('-')
                n = len(diagLimits)
                if i == 0:
                    tmp = diagLimits[0].split('.')[0]
                if n == 1 and diagLimits[0]:
                    tmpCode = diagLimits[0] if i==0 else '.'.join([tmp.strip(), diagLimits[0].strip()])
                    prefix, code, postfix = normalizeCode(prefix, tmpCode)
                    addCode(rowIdx, code, postfix, mapCodesToRowIdx)
                elif n == 2:
                    tmpCode = diagLimits[0] if i == 0 else '.'.join([tmp.strip(), diagLimits[0].strip()])
                    tmpCode2 = diagLimits[1] if i == 0 else '.'.join([tmp.strip(), diagLimits[1].strip()])
                    prefix, lowCode, postfix = normalizeCode(prefix, tmpCode)
                    prefix, highCode, postfix = normalizeCode(prefix, tmpCode2)
                    addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx)
                else:
                    assert False, 'Wrong codes range "' + diagRange + '"'
        else:
            diagLimits = diagRange.split('-')
            n = len(diagLimits)
            if n == 1 and diagLimits[0]:
                prefix, code, postfix = normalizeCode(prefix, diagLimits[0])
                addCode(rowIdx, code, postfix, mapCodesToRowIdx)
            elif n == 2:
                prefix, lowCode, postfix = normalizeCode(prefix, diagLimits[0])
                prefix, highCode, highPostfix = normalizeCode(prefix, diagLimits[1])
                addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx)
            else:
                # assert False, 'Wrong codes range "' + diagRange + '"'
                pass


def normalizeCode(prefix, code):
    code = code.strip().upper()
    postfix = ''
    if code[-1] in ['H', 'T']:
        postfix = code[-1]
        code = code[:-1]

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
    return prefix, code, postfix


def addCode(rowIdx, code, postfix, mapCodesToRowIdx):
    #    if re.match('^[A-Z][0-9][0-9]\.[0-9]', code) is not None:
    if fourChar.match(code):
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)
    #    elif re.match('^[A-Z][0-9][0-9]$', code) is not None:
    elif threeChar.match(code):
        addCodesRange(rowIdx, code, code, postfix, mapCodesToRowIdx)
    else:
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)


def createMapCodeToRowIdx(codesList):
    mapCodeToRowIdx = {}
    for rowIdx, code in enumerate(codesList):
        if code:
            parseRowCodes(rowIdx, str(code), mapCodeToRowIdx)
    return mapCodeToRowIdx


def normalizeMKB(mkb):
    postfixs = ['']
    if mkb and mkb[-1] in [u'Н', u'Т']:
        postfixs.append(mkb[-1].replace(u'Н', 'H').replace(u'Т', 'T'))
        mkb = mkb[:-1]
    if len(mkb) == 3:
        mkb = mkb + '.0'

    return mkb, postfixs