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
## минимальная поддержка Basic Encoding Rules
## см. ISO 7816-4: Annex D: Use of Basic Encoding Rules ASN.1
## http://en.wikipedia.org/wiki/Basic_Encoding_Rules#BER_encoding
## http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4_annex-d.aspx
##
#############################################################################


classUniversal       = 0b00000000
classApplication     = 0b01000000
classContextSpecific = 0b10000000
classPrivate         = 0b11000000
classMask            = 0b11000000

typePrivitive        = 0b00000000
typeConstructed      = 0b00100000
typeMask             = 0b00100000

tagLongForm          = 0b00011111
tagMask              = 0b00011111


def getTag(byteIterator):
    try:
        tagByte = byteIterator.next()
    except StopIteration:
        return None
    dataClass       = tagByte & classMask
    dataConstructed = tagByte & typeMask
    if (tagByte & tagMask) == tagLongForm:
        tag = 0
        while True:
            tagByte = byteIterator.next()
            tag = tag*0x80+(tagByte&0x7F)
            if not (tagByte&0x80):
                break
    else:
        tag = tagByte & tagLongForm
    return (dataClass, dataConstructed, tag)


def getLength(byteIterator):
    length = byteIterator.next()
#        print 'getLength:','length=',length
    if length & 0x80:
        lengthOfLength = length - 0x80
#            print 'getLength:','lengthOfLength=',lengthOfLength
        length = 0
        for i in xrange(lengthOfLength):
            lengthByte = byteIterator.next()
#                print 'getLength:','lengthByte=',lengthByte
            length = length*256+lengthByte
#        print 'getLength:','result.length=',length
    return length


def decodeObject(byteIterator, objectDescr):
# objectDescr: словарь тег -> (имя поля, функция декодирования)
    tag = getTag(byteIterator)
    if tag:
        result = {}
        while tag:
            length = getLength(byteIterator)
            if length != 0:
                data = [byteIterator.next() for i in xrange(length)]
                fieldDescr = objectDescr.get(tag)
                if fieldDescr:
                    fieldName, fieldDecode = fieldDescr
                    result[fieldName] = fieldDecode(data)
                else:
                    print 'found tag', tag, objectDescr.keys()
            tag = getTag(byteIterator)
        return result
    return None


# утилиты для декодирования контента.
# они не являются частью BER,
# но заводить отдельный модуль не хочется

def bytesAsIs(data):
    return data


def bytesToUnicode(data):
    s = ''.join(chr(byte) for byte in data)
    return s.decode('utf8')


def bytesToInt(data):
    return reduce(lambda s, a: s*256+a, data, 0)


def bcdToInt(byte):
    return (((byte>>4)&0x0F)%10)*10 + ((byte&0x0F)%10)


def bytesAsBcdDDMMYYYYToDateTuple(data):
    day = bcdToInt(data[0])
    month = bcdToInt(data[1])
    year  = bcdToInt(data[2])*100+bcdToInt(data[3])
    return (year, month, day)


def bytesAsBcdDDMMYYYYToDateString(data):
    day, month, year  = bytesAsBcdDDMMYYYYToDateTuple(data)
    return '%d-%d-%d' % (year, month, day)


def bytesToObject(descr):
    return lambda data: decodeObject(iter(data), descr)

