# -*- coding: utf-8 -*-
#############################################################################
##
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

from library.PrintInfo          import CInfo, CTemplatableInfoMixin, CInfoList, CDateInfo, CDateTimeInfo, CRBInfo, CTimeInfo
from library.Utils              import forceDate, forceDateTime, forceInt, forceRef, forceString, forceTime, formatShortNameInt

from Orgs.PersonInfo            import CPersonInfo
from RefBooks.Speciality.Info   import CSpecialityInfo
from Orgs.Utils                 import COrgStructureInfo, CActivityInfo
from Registry.Utils             import CClientInfo


class CReasonOfAbsenceInfo(CRBInfo):
    tableName = 'rbReasonOfAbsence'


class CAppointmentPurposeInfo(CRBInfo):
    tableName = 'rbAppointmentPurpose'


class CScheduleInfo(CInfo, CTemplatableInfoMixin):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._clientId = None
        self._client = self.getInstance(CClientInfo, None)


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('Schedule', '*', self.id)
        if record:
            self._createDatetime = CDateTimeInfo(forceDateTime(record.value('createDatetime')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(record.value('modifyDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(record.value('createPerson_id')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(record.value('modifyPerson_id')))
            self._deleted = forceInt(record.value('deleted'))
            self._appointmentType = forceInt(record.value('appointmentType'))
            self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
            self._appointmentPurpose = self.getInstance(CAppointmentPurposeInfo, forceRef(record.value('appointmentPurpose_id')))
            self._office = forceString(record.value('office'))
            self._date = CDateTimeInfo(forceDate(record.value('date')))
            self._begTime = CTimeInfo(forceTime(record.value('begTime')))
            self._endTime = CTimeInfo(forceTime(record.value('endTime')))
            self._duration = CTimeInfo(forceTime(record.value('duration')))
            self._capacity = forceInt(record.value('capacity'))
            self._done = forceInt(record.value('done'))
            self._doneTime = CTimeInfo(forceTime(record.value('doneTime')))
            self._reasonOfAbsence = self.getInstance(CReasonOfAbsenceInfo, forceRef(record.value('reasonOfAbsence_id')))
            self._activity = self.getInstance(CActivityInfo, forceRef(record.value('activity_id')))
            return True
        else:
            self._createDatetime = CDateTimeInfo()
            self._modifyDatetime = CDateTimeInfo()
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._deleted = 0
            self._appointmentType = 0
            self._person = self.getInstance(CPersonInfo, None)
            self._appointmentPurpose = self.getInstance(CAppointmentPurposeInfo, None)
            self._office = ''
            self._date = CDateTimeInfo()
            self._begTime = CTimeInfo()
            self._endTime = CTimeInfo()
            self._duration = CTimeInfo()
            self._capacity = 0
            self._done = 0
            self._doneTime = CTimeInfo()
            self._reasonOfAbsence = self.getInstance(CReasonOfAbsenceInfo, None)
            self._activity = self.getInstance(CActivityInfo, None)
            return False


    def __str__(self):
        self.load()
        result = formatShortNameInt(self._person.lastName, self._person.firstName, self._person.patrName)
        if self._person.speciality:
            result += ', '+self._person.speciality.name
        return unicode(result)


    createDatetime = property(lambda self: self.load()._createDatetime)
    modifyDatetime = property(lambda self: self.load()._modifyDatetime)
    createPerson   = property(lambda self: self.load()._createPerson)
    modifyPerson   = property(lambda self: self.load()._modifyPerson)
    deleted        = property(lambda self: self.load()._deleted)
    appointmentType = property(lambda self: self.load()._appointmentType)
    person          = property(lambda self: self.load()._person)
    appointmentPurpose = property(lambda self: self.load()._appointmentPurpose)
    office             = property(lambda self: self.load()._office)
    date               = property(lambda self: self.load()._date)
    begTime            = property(lambda self: self.load()._begTime)
    endTime            = property(lambda self: self.load()._endTime)
    duration           = property(lambda self: self.load()._duration)
    capacity           = property(lambda self: self.load()._capacity)
    done               = property(lambda self: self.load()._done)
    doneTime           = property(lambda self: self.load()._doneTime)
    reasonOfAbsence    = property(lambda self: self.load()._reasonOfAbsence)
    activity           = property(lambda self: self.load()._activity)


class CScheduleItemInfo(CInfo, CTemplatableInfoMixin):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._clientId = None
        self._client = self.getInstance(CClientInfo, None)


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('Schedule_Item', '*', self.id)
        if record:
            self._createDatetime = CDateTimeInfo(forceDateTime(record.value('createDatetime')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(record.value('modifyDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(record.value('createPerson_id')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(record.value('modifyPerson_id')))
            self._schedule = self.getInstance(CScheduleInfo, forceRef(record.value('master_id')))

            self._clientId = forceRef(record.value('client_id'))
            self._client = self.getInstance(CClientInfo, forceRef(record.value('client_id')))
            self._endOfReserve = CDateTimeInfo(forceDate(record.value('endOfReserve')))
            self._time = CTimeInfo(forceTime(record.value('time')))
            self._overtime = forceInt(record.value('overtime'))
            self._recordDatetime = CDateTimeInfo(forceDate(record.value('recordDatetime')))
            self._recordPerson = self.getInstance(CPersonInfo, forceRef(record.value('recordPerson_id')))
            self._recordClass = forceInt(record.value('recordClass'))
            self._complaint = forceString(record.value('complaint'))
            self._note = forceString(record.value('note'))
            self._checked = forceInt(record.value('checked'))
            self._deleted = forceInt(record.value('deleted'))
            self._idx = forceInt(record.value('idx'))
            return True
        else:
            self._createDatetime = CDateTimeInfo()
            self._modifyDatetime = CDateTimeInfo()
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._schedule = self.getInstance(CScheduleInfo, None)
            self._clientId = None
            self._client = self.getInstance(CClientInfo, None)

            self._endOfReserve = CDateTimeInfo()
            self._time = CTimeInfo()
            self._overtime = 0
            self._recordDatetime = CDateTimeInfo()
            self._recordPerson = self.getInstance(CPersonInfo, None)
            self._recordClass = 0
            self._complaint = ''
            self._note = ''
            self._checked = 0
            self._deleted = 0
            self._idx = 0
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
    schedule       = property(lambda self: self.load()._schedule)
    endOfReserve   = property(lambda self: self.load()._endOfReserve)
    time           = property(lambda self: self.load()._time)
    overtime       = property(lambda self: self.load()._overtime)
    recordDatetime = property(lambda self: self.load()._recordDatetime)
    recordPerson   = property(lambda self: self.load()._recordPerson)
    recordClass    = property(lambda self: self.load()._recordClass)
    complaint      = property(lambda self: self.load()._complaint)
    note           = property(lambda self: self.load()._note)
    deleted        = property(lambda self: self.load()._deleted)
    idx            = property(lambda self: self.load()._idx)


class CSuspendedAppointmentInfo(CInfo, CTemplatableInfoMixin):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._clientId = None
        self._client = self.getInstance(CClientInfo, None)


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('SuspendedAppointment', '*', self.id)
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


class CSuspendedAppointmentInfoList(CInfoList):
    def __init__(self, context, idList):
        CInfoList.__init__(self, context)
        self.idList = idList


    def _load(self):
        self._items = [ self.getInstance(CSuspendedAppointmentInfo, id) for id in self.idList ]
        return True

