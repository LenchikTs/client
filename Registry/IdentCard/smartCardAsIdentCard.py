#! /usr/bin/env python
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
## Унирерсальный доступ к данным сматр-карты как данным IdentCard
##
#############################################################################

from PyQt4 import QtGui

from library.SmartCard import hexDump
from PolicySmartCard   import CPolicySmartCard
from EkpContactless    import CEkpContactless
from EkpContact        import CEkpContact


__all__ = ( 'smartCardAsIdentCard',
          )

def isReaderOk(readers, reader):
    readers = readers.strip()
    if not readers:
        return True
    return reader.strip() in (tmp.strip() for tmp in reader.split('\n'))


def smartCardAsIdentCard(connection):
    atrHexDump = hexDump(connection.getATR(), ' ')
    identCard  = None

    if QtGui.qApp.getIdentCardServiceUrl():
        qApp = QtGui.qApp
        if (     not identCard
             and qApp.ekpContactlessEnabled()
             and (   not qApp.ekpContactlessCheckATR()
                  or CEkpContactless.atrIsSuitable(atrHexDump)
                 )
             and isReaderOk( qApp.ekpContactlessReaders(), connection.getReader() )
           ):
            identCard = CEkpContactless(connection).asIdentCard()

        if (     not identCard
             and qApp.ekpContactEnabled()
             and (   not qApp.ekpContactCheckATR()
                  or CEkpContact.atrIsSuitable(atrHexDump)
                 )
             and isReaderOk( qApp.ekpContactReaders(), connection.getReader() )
             and qApp.ekpContactLib()
           ):
            identCard = CEkpContact(connection).asIdentCard()

#    if CPolicySmartCard.atrIsSuitable(atrHexDump):
    if not identCard:
        identCard = CPolicySmartCard(connection).asIdentCard()


    return identCard
