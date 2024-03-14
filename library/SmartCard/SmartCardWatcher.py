#! /usr/bin/env python
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
## CSmartCardWatcher - простой класс для наблюдения за смарт-картами.
## Мне не понравился подход pyscard (типа CardMonitor или ReaderMonitor )
## так как они используют потоки (которые в python умеренно полезны), 
## а в нашем приложении всегда найдётся время для idle
##
#############################################################################

#http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4_5_basic_organizations.aspx
#http://www.musclecard.com
#http://sourceforge.net/projects/pyscard

import weakref
#from sys import exc_info
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions  import CardConnectionException

from PyQt4 import QtGui

__all__ = ( 'CSmartCardWatcher',
#            'hexDump',
          )


class CSmartCardWatcher:
    def __init__(self):
        self.watchedCards = []
        self.subscribers  = []
        self.cardRequest = CardRequest(timeout=0)

# Я бы с большим удовольствием сделал регистрацию call-back-а,
# мне одновременно кажется привлекательной идея weakref
# (для исключения циркулярных ссылок) и использование callable.
# но использование weakref с bound method и тем более - с lambda
# встречает серьёзные затруднения.
# Так что будем обходиться экземплярами классов.
#
# subscriber должен предоставлять метод addSmartCardNotice
# подписчики извещаются в порядке, обратном добавлению
# если подписчик возврашает True, по другие подписчики
# более не извещаются.
# Это сделано для модальных диалогов.

    def addSubscriber(self, subscriber):
        self.subscribers = [ref for ref in self.subscribers if ref]
        self.subscribers.append(weakref.ref(subscriber))


    def removeSubscriber(self, subscriber):
        self.subscribers = [ref
                            for ref in self.subscribers
                            if ref() and ref() is not subscriber
                           ]

    def watch(self):
        try:
            currentCards = self.cardRequest.waitforcardevent()
        except:
            currentCards = []

        addedCards = [ card for card in currentCards if card not in self.watchedCards ]
#        removedCards = [ card for card in self.watchedCards if card not in currentCards ]
        self.watchedCards = currentCards
        self.processAddedCards(addedCards)


    def processAddedCards(self, addedCards):
        for card in addedCards:
            connection = card.createConnection()
            try:
                connection.connect()
                try:
                    for ref in reversed(self.subscribers):
                        subscriber = ref()
                        if subscriber and subscriber.addSmartCardNotice(connection):
                            break
                except CardConnectionException:
                    pass
                except:
                    QtGui.qApp.logCurrentException()
                finally:
                    connection.disconnect()
            except:
#                pass
                QtGui.qApp.logCurrentException()
#                print exc_info()[0], ':', exc_info()[1]



#def hexDump(bytes, separator=''):
#    return separator.join('%02.2X' % byte for byte in bytes)


if __name__ == '__main__':
    from time import sleep, clock
    from library.SmartCard import hexDump
    from Registry.IdentCard.PolicySmartCard import CPolicySmartCard
    from Registry.IdentCard.EkpContactless  import CEkpContactless

    class CPolicySmartCardSubscriber:
        def addSmartCardNotice(self, connection):
            atrHexDump = hexDump(connection.getATR(), ' ')
            identCard  = None
            print connection, connection.getReader(), CPolicySmartCard.atrIsSuitable(atrHexDump), CEkpContactless.atrIsSuitable(atrHexDump)

            if CPolicySmartCard.atrIsSuitable(atrHexDump):
                t0 = clock()
                identCard = CPolicySmartCard(connection).asIdentCard()
                t1 = clock()
            if not identCard and CEkpContactless.atrIsSuitable(atrHexDump):
                t0 = clock()
                identCard = CEkpContactless(connection).asIdentCard()
                t1 = clock()

            if identCard:
                print 'lastName'.ljust(30,'.'),     identCard.lastName
                print 'firstName'.ljust(30,'.'),    identCard.firstName
                print 'patrName'.ljust(30,'.'),     identCard.patrName
                print 'birthDate'.ljust(30,'.'),    identCard.birthDate
                print 'sex'.ljust(30,'.'),          identCard.sex
                print 'birthPlace'.ljust(30,'.'),   identCard.birthPlace
                print 'SNILS'.ljust(30,'.'),        identCard.SNILS

                if identCard.policy:
                    print 'policy.serial'.ljust(30,'.'),  identCard.policy.serial
                    print 'policy.number'.ljust(30,'.'),  identCard.policy.number
                    print 'policy.begDate'.ljust(30,'.'), identCard.policy.begDate
                    print 'policy.endDate'.ljust(30,'.'), identCard.policy.endDate
#                    print 'policy.insurerOgrn'.ljust(30,'.'),  identCard.policy.insurerOgrn
#                    print 'policy.insurerOkato'.ljust(30,'.'), identCard.policy.insurerOkato
                print 'access time =', t1-t0
                return True


    cw = CSmartCardWatcher()
    ps = CPolicySmartCardSubscriber()

    cw.addSubscriber(ps)
    for i in xrange(30):
        print 'try#',i
        cw.watch()
        sleep(3)
    cw.removeSubscriber(ps)
