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

from PyQt4 import QtGui

from library.PrintInfo        import CInfo, CRBInfo, CTemplatableInfoMixin, CInfoList, CDateInfo, CDateTimeInfo, CInfoProxyList
from library.Utils            import forceDate, forceDateTime, forceInt, forceRef, forceString, formatShortNameInt
from Orgs.PersonInfo          import CPersonInfo
from RefBooks.Speciality.Info import CSpecialityInfo
from Orgs.Utils               import COrgStructureInfo
from Registry.Utils           import CClientInfo
from Events.EventInfo         import CSceneInfo, CVisitInfo, CDispanserInfo
from Events.MKBInfo           import CMKBInfo
from Registry.SuspendedAppointmentInfo import CScheduleItemInfo


class CSurveillanceRemoveReasonInfo(CRBInfo):
    tableName = 'rbSurveillanceRemoveReason'


class CProphylaxisPlanningTypeInfo(CInfo, CTemplatableInfoMixin):
    def __init__(self, context, planningTypeId):
        CInfo.__init__(self, context)
        self._planningTypeId = planningTypeId


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('rbProphylaxisPlanningType', '*', self._planningTypeId)
        if record:
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._daysBefore = forceInt(record.value('daysBefore'))
            self._daysAfter = forceInt(record.value('daysAfter'))
            return True
        else:
            self._code = ''
            self._name = ''
            self._daysBefore = None
            self._daysAfter = None
            return False


    def __str__(self):
        self.load()
        return self._name


    code = property(lambda self: self.load()._code)
    name = property(lambda self: self.load()._name)
    daysBefore = property(lambda self: self.load()._daysBefore)
    daysAfter = property(lambda self: self.load()._daysAfter)



class CProphylaxisPlanningInfo(CInfo, CTemplatableInfoMixin):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._clientId = None
        self._client = self.getInstance(CClientInfo, None)


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('ProphylaxisPlanning', '*', self.id)
        if record:
            self._clientId = forceRef(record.value('client_id'))
            self._contact = forceString(record.value('contact'))
            self._client = self.getInstance(CClientInfo, forceRef(record.value('client_id')))
            self._createDatetime = CDateTimeInfo(forceDateTime(record.value('createDatetime')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(record.value('modifyDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(record.value('createPerson_id')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(record.value('modifyPerson_id')))
            self._begDate = CDateInfo(forceDate(record.value('begDate')))
            self._endDate = CDateInfo(forceDate(record.value('endDate')))
            self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
            self._speciality = self.getInstance(CSpecialityInfo, forceRef(record.value('speciality_id')))
            self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
            self._reason = forceString(record.value('reason'))
            self._notified  = forceInt(record.value('notified'))
            self._processed = forceInt(record.value('processed'))
            self._scheduleItem = self.getInstance(CScheduleItemInfo, forceRef(record.value('appointment_id')))
            self._note = forceString(record.value('note'))
            self._externalUserId = forceString(record.value('externalUserId'))
            self._externalUserRole = forceString(record.value('externalUserRole'))
            self._externalUserName = forceString(record.value('externalUserName'))
            self._deleted = forceInt(record.value('deleted'))
            self._scene = self.getInstance(CSceneInfo, forceRef(record.value('scene_id')))
            self._typeId = self.getInstance(CProphylaxisPlanningTypeInfo, forceRef(record.value('prophylaxisPlanningType_id')))
            self._diagnosis = self.getInstance(CMKBInfo, forceString(record.value('MKB')))
            self._visit = self.getInstance(CVisitInfo, forceRef(record.value('visit_id')))
            self._dispanser = self.getInstance(CDispanserInfo, forceRef(record.value('dispanser_id')))
            self._removeReason = self.getInstance(CSurveillanceRemoveReasonInfo, forceRef(record.value('removeReason_id')))
            self._plannedDate = CDateInfo(forceDate(record.value('plannedDate')))
            self._takenDate = CDateInfo(forceDate(record.value('takenDate')))
            self._removeDate = CDateInfo(forceDate(record.value('removeDate')))
            self._prophylaxisPlanning = self.getInstance(CProphylaxisPlanningInfo, forceRef(record.value('parent_id')))
            return True
        else:
            self._clientId = None
            self._contact = ''
            self._client = self.getInstance(CClientInfo, None)
            self._createDatetime = CDateTimeInfo()
            self._modifyDatetime = CDateTimeInfo()
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._begDate = CDateInfo()
            self._endDate = CDateInfo()
            self._orgStructure = self.getInstance(COrgStructureInfo, None)
            self._speciality = self.getInstance(CSpecialityInfo, None)
            self._person = self.getInstance(CPersonInfo, None)
            self._reason = ''
            self._notified  = 0
            self._processed = 0
            self._scheduleItem = self.getInstance(CScheduleItemInfo, None)
            self._note = ''
            self._externalUserId = ''
            self._externalUserRole = ''
            self._externalUserName = ''
            self._deleted = 0
            self._scene = self.getInstance(CSceneInfo, None)
            self._typeId = self.getInstance(CProphylaxisPlanningTypeInfo, None)
            self._diagnosis = self.getInstance(CMKBInfo, None)
            self._visit = self.getInstance(CVisitInfo, None)
            self._dispanser = self.getInstance(CDispanserInfo, None)
            self._removeReason = self.getInstance(CSurveillanceRemoveReasonInfo, None)
            self._plannedDate = CDateInfo()
            self._takenDate = CDateInfo()
            self._removeDate = CDateInfo()
            self._prophylaxisPlanning = self.getInstance(CProphylaxisPlanningInfo, None)
            return False


    def __str__(self):
        self.load()
        return formatShortNameInt(self._client.lastName, self._client.firstName, self._client.patrName)


    clientId       = property(lambda self: self.load()._clientId)
    contact        = property(lambda self: self.load()._contact)
    client         = property(lambda self: self.load()._client)
    createDatetime = property(lambda self: self.load()._createDatetime)
    modifyDatetime = property(lambda self: self.load()._modifyDatetime)
    createPerson   = property(lambda self: self.load()._createPerson)
    modifyPerson   = property(lambda self: self.load()._modifyPerson)
    begDate        = property(lambda self: self.load()._begDate)
    endDate        = property(lambda self: self.load()._endDate)
    orgStructure   = property(lambda self: self.load()._orgStructure)
    speciality     = property(lambda self: self.load()._speciality)
    person         = property(lambda self: self.load()._person)
    reason         = property(lambda self: self.load()._reason)
    notified       = property(lambda self: self.load()._notified)
    processed      = property(lambda self: self.load()._processed)
    scheduleItem   = property(lambda self: self.load()._scheduleItem)
    note           = property(lambda self: self.load()._note)
    externalUserId = property(lambda self: self.load()._externalUserId)
    externalUserRole = property(lambda self: self.load()._externalUserRole)
    externalUserName = property(lambda self: self.load()._externalUserName)
    deleted          = property(lambda self: self.load()._deleted)
    scene            = property(lambda self: self.load()._scene)
    typeId           = property(lambda self: self.load()._typeId)
    diagnosis        = property(lambda self: self.load()._diagnosis)
    visit          = property(lambda self: self.load()._visit)
    dispanser      = property(lambda self: self.load()._dispanser)
    removeReason   = property(lambda self: self.load()._removeReason)
    plannedDate    = property(lambda self: self.load()._plannedDate)
    takenDate      = property(lambda self: self.load()._takenDate)
    removeDate     = property(lambda self: self.load()._removeDate)
    prophylaxisPlanning = property(lambda self: self.load()._prophylaxisPlanning)


class CProphylaxisPlanningInfoList(CInfoList):
    def __init__(self, context, idList):
        CInfoList.__init__(self, context)
        self.idList = idList


    def _load(self):
        self._items = [ self.getInstance(CProphylaxisPlanningInfo, id) for id in self.idList ]
        return True


class CCookedProphylaxisPlanningInfo(CProphylaxisPlanningInfo):
    def __init__(self, context, record):
        CProphylaxisPlanningInfo.__init__(self, context, None)
        self._record = record
        self._ok = self._load()
        self._loaded = True


    def _load(self):
        record = self._record
        if record:
            self._clientId = forceRef(record.value('client_id'))
            self._contact = forceString(record.value('contact'))
            self._client = self.getInstance(CClientInfo, forceRef(record.value('client_id')))
            self._createDatetime = CDateTimeInfo(forceDateTime(record.value('createDatetime')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(record.value('modifyDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(record.value('createPerson_id')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(record.value('modifyPerson_id')))
            self._begDate = CDateInfo(forceDate(record.value('begDate')))
            self._endDate = CDateInfo(forceDate(record.value('endDate')))
            self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
            self._speciality = self.getInstance(CSpecialityInfo, forceRef(record.value('speciality_id')))
            self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
            self._reason = forceString(record.value('reason'))
            self._notified  = forceInt(record.value('notified'))
            self._processed = forceInt(record.value('processed'))
            self._scheduleItem = self.getInstance(CScheduleItemInfo, forceRef(record.value('appointment_id')))
            self._note = forceString(record.value('note'))
            self._externalUserId = forceString(record.value('externalUserId'))
            self._externalUserRole = forceString(record.value('externalUserRole'))
            self._externalUserName = forceString(record.value('externalUserName'))
            self._deleted = forceInt(record.value('deleted'))
            self._scene = self.getInstance(CSceneInfo, forceRef(record.value('scene_id')))
            self._typeId = self.getInstance(CProphylaxisPlanningTypeInfo, forceRef(record.value('prophylaxisPlanningType_id')))
            self._diagnosis = self.getInstance(CMKBInfo, forceString(record.value('MKB')))
            self._visit = self.getInstance(CVisitInfo, forceRef(record.value('visit_id')))
            self._dispanser = self.getInstance(CDispanserInfo, forceRef(record.value('dispanser_id')))
            self._removeReason = self.getInstance(CSurveillanceRemoveReasonInfo, forceRef(record.value('removeReason_id')))
            self._plannedDate = CDateInfo(forceDate(record.value('plannedDate')))
            self._takenDate = CDateInfo(forceDate(record.value('takenDate')))
            self._removeDate = CDateInfo(forceDate(record.value('removeDate')))
            self._prophylaxisPlanning = self.getInstance(CProphylaxisPlanningInfo, forceRef(record.value('parent_id')))
            return True
        else:
            self._clientId = None
            self._contact = ''
            self._client = self.getInstance(CClientInfo, None)
            self._createDatetime = CDateTimeInfo()
            self._modifyDatetime = CDateTimeInfo()
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._begDate = CDateInfo()
            self._endDate = CDateInfo()
            self._orgStructure = self.getInstance(COrgStructureInfo, None)
            self._speciality = self.getInstance(CSpecialityInfo, None)
            self._person = self.getInstance(CPersonInfo, None)
            self._reason = ''
            self._notified  = 0
            self._processed = 0
            self._scheduleItem = self.getInstance(CScheduleItemInfo, None)
            self._note = ''
            self._externalUserId = ''
            self._externalUserRole = ''
            self._externalUserName = ''
            self._deleted = 0
            self._scene = self.getInstance(CSceneInfo, None)
            self._typeId = self.getInstance(CProphylaxisPlanningTypeInfo, None)
            self._diagnosis = self.getInstance(CMKBInfo, None)
            self._visit = self.getInstance(CVisitInfo, None)
            self._dispanser = self.getInstance(CDispanserInfo, None)
            self._removeReason = self.getInstance(CSurveillanceRemoveReasonInfo, None)
            self._plannedDate = CDateInfo()
            self._takenDate = CDateInfo()
            self._removeDate = CDateInfo()
            self._prophylaxisPlanning = self.getInstance(CProphylaxisPlanningInfo, None)
            return False


class CProphylaxisPlanningInfoProxyList(CInfoProxyList):
    def __init__(self, context, models):
        CInfoProxyList.__init__(self, context)
        self._rawItems = []
        for model in models:
            self._rawItems.extend(model.items())
        self._items = [ None ]*len(self._rawItems)


    def _getItemEx(self, key):
        record = self._rawItems[key]
        v = self.getInstance(CCookedProphylaxisPlanningInfo, record)
        return v


    def __getitem__(self, key):
        if isinstance(key, slice):
            for i in range(key.start or 0, key.stop or len(self._items), key.step or 1):
                val = self._items[i]
                if val is None:
                    self._items[i] = self._getItemEx(i)
        v = self._items[key]
        if v is None:
            v = self._getItemEx(key)
            self._items[key] = v
        return v

