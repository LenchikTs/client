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

from library.PrintInfo import (
                               CInfoList,
                               CDateInfo,
                               CRBInfo,
                               CRBInfoWithIdentification,
                              )
from library.Utils     import (
                               forceBool,
                               forceDate,
                               forceInt,
                               forceRef,
                               forceString,
                               formatSex,
                              )

from Events.EventInfo  import CEventInfo
from Orgs.Utils        import COrgStructureInfo


class CHospitalBedInfo(CRBInfo):
    tableName = 'OrgStructure_HospitalBed'


    def _initByRecord(self, record):
        self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('master_id')))
        self._isPermanent  = forceBool(record.value('isPermanent'))
        self._type         = self.getInstance(CHospitalBedTypeInfo, forceRef(record.value('type_id')))
        self._profile      = self.getInstance(CHospitalBedProfileInfo, forceRef(record.value('profile_id')))
        self._relief       = forceInt(record.value('relief'))
        self._schedule     = self.getInstance(CHospitalBedScheduleInfo, forceRef(record.value('schedule_id')))
        self._begDate      = CDateInfo(forceDate(record.value('begDate')))
        self._endDate      = CDateInfo(forceDate(record.value('endDate')))


    def _initByNull(self):
        self._orgStructure = self.getInstance(COrgStructureInfo, None)
        self._isPermanent  = None
        self._type         = self.getInstance(CHospitalBedTypeInfo, None)
        self._profile      = self.getInstance(CHospitalBedProfileInfo, None)
        self._relief       = None
        self._schedule     = self.getInstance(CHospitalBedScheduleInfo, None)
        self._begDate      = CDateInfo()
        self._endDate      = CDateInfo()


    orgStructure = property(lambda self: self.load()._orgStructure)
    isPermanent  = property(lambda self: self.load()._isPermanent)
    type         = property(lambda self: self.load()._type)
    profile      = property(lambda self: self.load()._profile)
    relief       = property(lambda self: self.load()._relief)
    schedule     = property(lambda self: self.load()._schedule)
    begDate      = property(lambda self: self.load()._begDate)
    endDate      = property(lambda self: self.load()._endDate)


class CHospitalBedTypeInfo(CRBInfo):
    tableName = 'rbHospitalBedType'


class CHospitalBedProfileInfo(CRBInfoWithIdentification):
    tableName = 'rbHospitalBedProfile'


    def _initByRecord(self, record):
        CRBInfo._initByRecord(self, record)
        self._usishCode = forceString(record.value('usishCode'))
        self._tfomsCode = forceString(record.value('tfomsCode'))


    def _initByNull(self):
        CRBInfo._initByNull(self)
        self._usishCode = ''
        self._tfomsCode = ''


    usishCode = property(lambda self: self.load()._usishCode)
    tfomsCode = property(lambda self: self.load()._tfomsCode)


class CHospitalBedScheduleInfo(CRBInfo):
    tableName = 'rbHospitalBedShedule'


class CHospitalEventInfo(CEventInfo):
    def __init__(self, context, id):
        CEventInfo.__init__(self, context, id)
        self._action = None
        self._finance = '' # код финансирования
        self._bedCode = ''
        self._hasFeed = False
        self._feed = '' # код диеты


    def _load(self):
        return CEventInfo._load(self)


    action      = property(lambda self: self.load()._action)
    finance     = property(lambda self: self.load()._finance)
    bedCode     = property(lambda self: self.load()._bedCode)
    hasFeed     = property(lambda self: self.load()._hasFeed)
    feed        = property(lambda self: self.load()._feed)


class CvHospitalBedInfo(CHospitalBedInfo):
    tableName = 'vHospitalBed'

    def __init__(self, context, id):
        CHospitalBedInfo.__init__(self, context, id)

    def _initByRecord(self, record):
        CHospitalBedInfo._initByRecord(self, record)
        self._isBusy         = forceBool(record.value('isBusy'))
        self._age   = forceString(record.value('age'))
        self._sex   = formatSex(forceInt(record.value('sex')))

    isBusy = property(lambda self: self.load()._isBusy)
    age = property(lambda self: self.load()._age)
    sex = property(lambda self: self.load()._sex)


class CHospitalBedsListInfo(CInfoList):
    def __init__(self,  context, idList):
        CInfoList.__init__(self, context)
        self._class = CvHospitalBedInfo
        self._idList = idList

    def _load(self):
        self._items = [ self.getInstance(self._class, id) for id in self._idList ]
        return True
