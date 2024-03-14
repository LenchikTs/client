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
## Извлечение ширин глифов из данных шрифта для указания в PDF
## описание заголовков шрифта -
## см. https://docs.microsoft.com/ru-ru/typography/opentype/spec/otff
##
#############################################################################

from struct import unpack_from, calcsize

__all__ = ( 'extractGlyphWidthsFromTTFData',
          )


def extractGlyphWidthsFromTTFData(fontData):
    fontDataHeaderFormat = '>LHHHH'
    fontDataHeaderSize   = calcsize(fontDataHeaderFormat)

    tableRecordFormat    = '>4sLlL'
    tableRecordSize      = calcsize(tableRecordFormat)

    headRecordFormat = '>HHLLLHHqqhhhhHHhhh'
    headRecordSize   = calcsize(headRecordFormat)

    hmtxRecordFormat = '>Hh'
    hmtxRecordSize   = calcsize(hmtxRecordFormat)

    unitsPerEm = 1000
    widths = []

    if len(fontData) < fontDataHeaderSize + tableRecordSize*2:
        return None
    sfntVersion, numTables, searchRange, entrySelector, rangeShift = unpack_from(fontDataHeaderFormat, fontData)
    if sfntVersion not in (0x00010000, 0x4F54544F):
        return None

    for i in xrange(numTables):
        tag, checkSum, offset, length = unpack_from(tableRecordFormat, fontData, fontDataHeaderSize + i*tableRecordSize)
        if tag == 'head':
            assert headRecordSize == length
            (majorVersion,
             minorVersion,
             fontRevision,
             checkSumAdjustment,
             magicNumber,
             flags,
             unitsPerEm,
             created,
             modified,
             xMin,
             yMin,
             xMax,
             yMax,
             macStyle,
             lowestRecPPEM,
             fontDirectionHint,
             indexToLocFormat,
             glyphDataFormat,
            ) =  unpack_from(headRecordFormat, fontData, offset)
            if magicNumber != 0x5F0F3CF5:
                return None

        elif tag == 'hmtx':
            for ig in xrange(length/hmtxRecordSize):
                advanceWidth, lsb = unpack_from(hmtxRecordFormat, fontData, offset+ig*hmtxRecordSize)
                widths.append(advanceWidth)

    return [ int((w*1000+0.5)//unitsPerEm) for w in widths ]

