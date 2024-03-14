# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from library.PrintInfo     import CInfoList, CRBInfoWithIdentification
from RefBooks.Service.Info import CServiceInfo

from library.Utils         import forceRef,  forceString


class CSpecialityInfo(CRBInfoWithIdentification):
    tableName = 'rbSpeciality'

    def _initByRecord(self, record):
        self._OKSOName = forceString(record.value('OKSOName'))
        self._OKSOCode = forceString(record.value('OKSOCode'))
        self._regionalCode = forceString(record.value('regionalCode'))
        self._federalCode = forceString(record.value('federalCode'))
        self._usishCode = forceString(record.value('usishCode'))
        self._service = self.getInstance(CServiceInfo, forceRef(record.value('service_id')))


    def _initByNull(self):
        self._OKSOName = ''
        self._OKSOCode = ''
        self._regionalCode = ''
        self._federalCode = ''
        self._usishCode = ''
        self._service = self.getInstance(CServiceInfo, None)


    OKSOName     = property(lambda self: self.load()._OKSOName)
    OKSOCode     = property(lambda self: self.load()._OKSOCode)
    regionalCode = property(lambda self: self.load()._regionalCode)
    federalCode  = property(lambda self: self.load()._federalCode)
    usishCode    = property(lambda self: self.load()._usishCode)
    service      = property(lambda self: self.load()._service)


class CSpecialityInfoList(CInfoList):
    def __init__(self, context, specialityIdList):
        CInfoList.__init__(self, context)
        self.idList = specialityIdList


    def _load(self):
        self._items = [ self.getInstance(CSpecialityInfo, id) for id in self.idList ]
        return True
