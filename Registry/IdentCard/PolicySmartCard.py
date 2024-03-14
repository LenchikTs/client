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
## Класс для декодирования данных с электронного полиса ОМС.
## Алгоритм и константы получены декомпиляцией кода библиотек чтения полиса.
##
## см. также ISO 7816 Part 4: Interindustry Commands for Interchange
## http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4_3_definitions.aspx
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from IdentCard import CIdentCard, CIdentCardPolicy
from library.SmartCard import BER
from library.Utils import nameCase

__all__ = ( 'CPolicySmartCard',
          )

class CPolicySmartCard:
    appSmoInformation   = 1
    appOwnerInfornation = 2

    fidFomsRoot  = 'foms_root'
    fidOwnerInfo = '\02\01'
    fidFomsIns   = 'FOMS_INS'
    fidFomsId    = 'FOMS_ID'

    tagSMOPolicyRoot = 2
    tagSmoRoot = 4

    atrHexDump = '3B F7 13 00 00 81 31 FE 45 46 4F 4D 53 4F 4D 53 A9'


    descrCitizenship = \
    {
        (BER.classApplication, BER.typePrivitive,   49) : ('counryCode',         BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   50) : ('coutryCyrillicName', BER.bytesToUnicode),
    }

    descrOwnerInformation = \
    {
        (BER.classApplication, BER.typePrivitive,   33) : ('lastName',     BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   34) : ('firstName',    BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   35) : ('patrName',     BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   36) : ('birthDate',    BER.bytesAsBcdDDMMYYYYToDateTuple),
        (BER.classApplication, BER.typePrivitive,   37) : ('sex',          BER.bytesToInt),
        (BER.classApplication, BER.typePrivitive,   38) : ('policyNumber', BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   39) : ('SNILS',        BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   40) : ('expireDate',   BER.bytesAsBcdDDMMYYYYToDateTuple),
        (BER.classApplication, BER.typePrivitive,   41) : ('birthPlace',   BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   42) : ('issueDate',    BER.bytesAsBcdDDMMYYYYToDateTuple),
        (BER.classApplication, BER.typeConstructed, 48) : ('citizenship',  BER.bytesToObject(descrCitizenship)),
        (BER.classApplication, BER.typeConstructed, 64) : ('ownerPhoto',   BER.bytesAsIs),
    }

    descrSMOInformationEDS = \
    {
        (BER.classApplication, BER.typePrivitive,   97) : ('signature',    BER.bytesAsIs),
        (BER.classApplication, BER.typePrivitive,   98) : ('certificate',  BER.bytesAsIs),
    }

    descrSmoInformation = \
    {
        (BER.classApplication, BER.typePrivitive,   81) : ('OGRN',         BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   82) : ('OKATO',        BER.bytesToUnicode),
        (BER.classApplication, BER.typePrivitive,   83) : ('begDate',      BER.bytesAsBcdDDMMYYYYToDateTuple),
        (BER.classApplication, BER.typePrivitive,   84) : ('endDate',      BER.bytesAsBcdDDMMYYYYToDateTuple),
        (BER.classApplication, BER.typeConstructed, 96) : ('SMOInformationEDS', BER.bytesToObject(descrSMOInformationEDS)),
    }


    @classmethod 
    def atrIsSuitable(cls, atrHexDump):
        return atrHexDump == cls.atrHexDump


    def __init__(self, connection):
        self.connection = connection


    def asIdentCard(self):
        def dateTupleToQDate(date):
            return QDate(*date) if date else None

        result = CIdentCard()
        try:
            oi = self.getOwnerInformation()
            pi = self.getCurrentSMOInformation()
            result.lastName   = nameCase(oi.get('lastName'))
            result.firstName  = nameCase(oi.get('firstName'))
            result.patrName   = nameCase(oi.get('patrName'))
            result.sex        = oi.get('sex')
            result.birthDate  = dateTupleToQDate(oi.get('birthDate'))
            result.birthPlace = oi.get('birthPlace')
            result.SNILS      = oi.get('SNILS')

            citizenship = oi.get('citizenship')
            if citizenship:
                result.citizenship = citizenship.get('counryCode')
#                print 'citizenship.counryCode'.ljust(30,'.'), citizenship.get('counryCode')
#                print 'citizenship.coutryCyrillicName'.ljust(30,'.'), citizenship.get('coutryCyrillicName')

            policy = CIdentCardPolicy()
            policy.serial  = ''
            policy.number  = oi.get('policyNumber')
            policy.begDate = dateTupleToQDate(pi.get('begDate') or oi.get('issueDate'))
            policy.endDate = dateTupleToQDate(pi.get('endDate') or oi.get('expireDate'))

            policy.insurerId = findInsurerByOGRNAndOKATO(pi.get('OGRN'), pi.get('OKATO'))
#            policy.insurerOgrn  = pi.get('OGRN')
#            policy.insurerOKATO = pi.get('OKATO')
            result.policy  = policy

            return result
        except:
#            Qt.Gui.qApp.logCurrentException()
            pass
        return None


    def getOwnerInformation(self):
        self.selectApplication(self.appOwnerInfornation)
        self.selectFile(self.fidOwnerInfo, False)
        data = self.readObjectBytes((BER.classApplication, BER.typeConstructed, self.tagSMOPolicyRoot))
        if data:
            return BER.decodeObject(iter(data), self.descrOwnerInformation)


    def getCurrentSMOInformation(self):
        self.selectApplication(self.appSmoInformation)
        fileIdBytes = self.getData(1, 176) # const?
        if fileIdBytes and len(fileIdBytes) == 2:
            self.selectFile(chr(fileIdBytes[0])+chr(fileIdBytes[1]), False)
            data = self.readObjectBytes((BER.classApplication, BER.typeConstructed, self.tagSmoRoot))
            return BER.decodeObject(iter(data), self.descrSmoInformation)
        return None


    def selectApplication(self, app):
        self.selectFile(self.fidFomsRoot, True)
        if app == self.appSmoInformation:
            self.selectFile(self.fidFomsIns, True)
        elif app == self.appOwnerInfornation:
            self.selectFile(self.fidFomsId, True)


    def selectFile(self, fileId, isDF):
        data, sw1, sw2 = self.runCommand(0,                      # cla
                                         0xA4,                   # ins
                                         4 if isDF else 2,       # p1
                                         12,                     # p2
                                         fileId,                 # data
                                         None                    # req
                                        )
#    print 'selectFile(%s, %s, %s)' % ( repr(fileId), isDF, getFCP), data, sw1, sw2
        self.TESTANS((data, sw1, sw2), 0x90, 0)
        return None


    def readObjectBytes(self, expectedTag):
        class CConnectionByteIterator:
            def __init__(self, card):
                self.card = card
                self.offset = 0

            def __iter__(self):
                return self

            def next(self):
                result = self.card.binaryRead(self.offset, 1)
                self.offset += 1
                return result[0]

        byteIterator = CConnectionByteIterator(self)
        tag = BER.getTag(byteIterator)

#    print 'readObjectBytes: expectedTag=',expectedTag,'actualTag=',tag
        if not tag or tag != expectedTag:
            return None
        length = BER.getLength(byteIterator)
        if not length:
            return None
        return self.binaryRead(byteIterator.offset, length)


    def getData(self, byte0, byte1):
      data, sw1, sw2 = self.TESTANS(self.runCommand(0, 0xCA, byte0, byte1, None, 2), 0x90, 0)
      return data


    def binaryRead(self, offset, length):
        tmpOffset, tmpLength = offset, length
        chunkSize = 220
        result = []
        while tmpLength:
            chunkLength = min(tmpLength, chunkSize)
            data, sw1, sw2 = self.TESTANS(self.runCommand(0, 0xB0, tmpOffset>>8, tmpOffset & 0xFF, None, chunkLength), 0x90, 0)
            result += data
            tmpLength -= chunkLength
            tmpOffset += chunkLength
#       print 'binaryRead(%d,%d) -> %s' % (offset, length, repr(result))
        return result


    def runCommand(self, cla, ins, p1, p2, data=None, reqLen=None):
        d = [cla, ins, p1, p2]
        if data:
            d.append(len(data))
            d.extend([ord(c) for c in data])
        if reqLen:
            d.append(reqLen & 0xFF)
        result = self.connection.transmit(d)
#    print 'runCommand(cla=%d, ins=%d, byte0=%d, byte1=%d, byte2=%d, short0=%d, data=%s)' % (cla, ins, byte0, byte1, byte2, short0, repr(data)),'->', repr(result)
        return result


    def TESTANS(self, (data, sw1, sw2), expectedSw1=0x90, expectedSw2=0):
#    print 'TESTANS:', data, sw1, sw2
        assert(sw1==expectedSw1 and sw2==expectedSw2)
        return data, sw1, sw2



def findInsurerByOGRNAndOKATO(ogrn, okato):
    db = QtGui.qApp.db
    tableOrganisation = db.table('Organisation')

    idList = db.getIdList(tableOrganisation,
                          idCol='id',
                          where=[ 'deleted=0',
                                  'isInsurer=1',
                                  tableOrganisation['OGRN'].eq(ogrn),
                                  tableOrganisation['OKATO'].eq(okato),
                                ],
                          order='id',
                          limit=1)
    print ogrn, okato, idList
    return idList[0] if idList else None


