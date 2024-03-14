#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#############################################################################
##
## Copyright (C) 2017-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Формальный класс для формирования id подписываемых элементов
## и их actorUri.
##
#############################################################################

#CFssSignInfo

class CFssSignInfo:
    _baseUri          = 'http://eln.fss.ru/actor'

    _moElementIdFmt   = 'OGRN_%(ogrn)s'
    _moActorUriFmt    = '%(baseUri)s/mo/%(ogrn)s'

    _moLnElementIdFmt = 'ELN_%(lnCode)s'
    _moLnActorUriFmt  = '%(baseUri)s/mo/%(ogrn)s/ELN_%(lnCode)s'

    _docElementIdFmt  = 'ELN_%(lnCode)s_%(num)d_doc'
    _docActorUriFmt   = '%(baseUri)s/doc/%(lnCode)s_%(num)d_doc'

    _vkElementIdFmt   = 'ELN_%(lnCode)s_%(num)d_vk'
    _vkActorUriFmt    = '%(baseUri)s/doc/%(lnCode)s_%(num)d_vk'


    @classmethod
    def getMoElementIdAndActorUri(cls, ogrn, lnCode = None):
        args = {  'baseUri': cls._baseUri, 'ogrn': ogrn, 'lnCode': lnCode }
        if lnCode:
            return ( cls._moLnElementIdFmt % args,  cls._moLnActorUriFmt % args )
        else:
            return ( cls._moElementIdFmt % args,    cls._moActorUriFmt  % args )

    @classmethod
    def getHospitalBreachElementIdAndActorUri(cls, lnCode):
        args = {  'baseUri': cls._baseUri, 'lnCode': lnCode, 'num': 1 }
        return ( cls._docElementIdFmt % args, cls._docActorUriFmt % args )


    @classmethod
    def getLnResultElementIdAndActorUri(cls, lnCode):
        args = {  'baseUri': cls._baseUri, 'lnCode': lnCode, 'num': 2 }
        return ( cls._docElementIdFmt % args, cls._docActorUriFmt % args )


    @classmethod
    def getTreatPeriodElementIdAndActorUri(cls, lnCode, zeroBasedIndex):
        if not 0<=zeroBasedIndex<=2:
            raise Exception(u'Л.Н. не может иметь элемент %s с индексом %r' % ('THREAD_PERIOD', zeroBasedIndex))
        args = {  'baseUri': cls._baseUri, 'lnCode': lnCode, 'num': 3+zeroBasedIndex }
        return ( cls._docElementIdFmt % args, cls._docActorUriFmt % args )


    @classmethod
    def getTreatFullPeriodElementIdAndActorUri(cls, lnCode, zeroBasedIndex):
        if not 0<=zeroBasedIndex<=2:
            raise Exception(u'Л.Н. не может иметь элемент %s с индексом %r' % ('THREAD_FULL_PERIOD', zeroBasedIndex))
        args = {  'baseUri': cls._baseUri, 'lnCode': lnCode, 'num': 3+zeroBasedIndex }
        return ( cls._vkElementIdFmt % args, cls._vkActorUriFmt % args )



if __name__ == '__main__':

    print 'MO',              CFssSignInfo.getMoElementIdAndActorUri('1234567890')
    print 'MO with LN',      CFssSignInfo.getMoElementIdAndActorUri('1234567890', '777')

    print '='*40

    print 'HOSPITAL_BREACH', CFssSignInfo.getHospitalBreachElementIdAndActorUri( '777')
    print 'LN_RESULT',       CFssSignInfo.getLnResultElementIdAndActorUri('777')

    print 'TREAT_PERIOD#1',  CFssSignInfo.getTreatPeriodElementIdAndActorUri( '777', 0)
    print 'TREAT_PERIOD#2',  CFssSignInfo.getTreatPeriodElementIdAndActorUri( '777', 1)
    print 'TREAT_PERIOD#3',  CFssSignInfo.getTreatPeriodElementIdAndActorUri( '777', 2)

    print 'TREAT_FULL_PERIOD#1',  CFssSignInfo.getTreatFullPeriodElementIdAndActorUri( '777', 0)
    print 'TREAT_FULL_PERIOD#2',  CFssSignInfo.getTreatFullPeriodElementIdAndActorUri( '777', 1)
    print 'TREAT_FULL_PERIOD#3',  CFssSignInfo.getTreatFullPeriodElementIdAndActorUri( '777', 2)


