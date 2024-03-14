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

u"""
Объект печати Job_Ticket
"""
from PyQt4 import QtGui
from PyQt4.QtCore import QString

from library.PrintInfo          import CInfo, CInfoList, CDateTimeInfo, CRBInfo, CTimeInfo, CDateInfo
from library.exception          import CException
from library.Utils              import forceBool, forceDateTime, forceInt, forceRef, forceString, forceTime

from Events.ActionInfo          import CActionInfo, CPropertyInfo, CCookedActionInfo
from Events.Action              import CAction
from Orgs.Utils                 import COrgStructureInfo
from Resources.JobTicketChooser import getJobTicketRecord
from Resources.JobTicketStatus  import CJobTicketStatus


class CJobTypeInfo(CRBInfo):
    tableName = 'rbJobType'


    def _initByRecord(self, record):
        self._duration = forceInt(record.value('ticketDuration'))
        self._note     = forceString(record.value('notes'))


    def _initByNull(self):
        self._duration = 0
        self._note     = ''
        self._code     = ''

    duration     = property(lambda self: self.load()._duration)
    note         = property(lambda self: self.load()._note)


class CJobPurposeInfo(CRBInfo):
    tableName = 'rbJobPurpose'


    def _initByRecord(self, record):
        self._sex = forceInt(record.value('sex'))
        self._age     = forceString(record.value('age'))


    def _initByNull(self):
        self._sex = 0
        self._age     = ''


    sex = property(lambda self: self.load()._sex)
    age = property(lambda self: self.load()._age)

# ###########################################################################
# сокращённый вариант используется при печати action

class CJobTicketInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id


    def _load(self):
        record = getJobTicketRecord(self.id) if self.id else None
        if record:
            self._initByRecord(record)
            return True
        else:
            self._initByNull()
            return False


    def _initByRecord(self, record):
        self._jobType      = self.getInstance(CJobTypeInfo, forceRef(record.value('jobType_id')))
        self._jobPurpose      = self.getInstance(CJobPurposeInfo, forceRef(record.value('jobPurpose_id')))
        self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
        self._jobTicketOrgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('jobTicketOrgStructure_id')))
        self._datetime     = CDateTimeInfo(forceDateTime(record.value('datetime')))
        self._isExceeed    = forceBool(record.value('isExceedQuantity'))
        self._idx          = forceInt(record.value('idx'))
        self._status       = forceInt(record.value('status'))
        self._label        = forceString(record.value('label'))
        self._note         = forceString(record.value('note'))
        self._numberid         = forceString(record.value('id'))
        self._jobDate  = CDateInfo(forceDateTime(record.value('date')))
        self._begJobTime  = CTimeInfo(forceTime(record.value('begTime')))
        self._endJobTime  = CTimeInfo(forceTime(record.value('endTime')))
        self._begDateTime  = CDateTimeInfo(forceDateTime(record.value('begDateTime')))
        self._endDateTime  = CDateTimeInfo(forceDateTime(record.value('endDateTime')))
        self._capacity     = forceInt(record.value('capacity'))
        makeDependentActionIdList([self.id])
        actionIdList = CMapJobTicketsToActionsHelper.getActionIdList(self.id)
        self._actions = self.getInstance(CJobTicketsActionInfoList, tuple(actionIdList), presetActions=None)


    def _initByNull(self):
        self._jobType      = self.getInstance(CJobTypeInfo, None)
        self._jobPurpose      = self.getInstance(CJobPurposeInfo, None)
        self._orgStructure = self.getInstance(COrgStructureInfo, None)
        self._jobTicketOrgStructure = self.getInstance(COrgStructureInfo, None)
        self._datetime     = CDateTimeInfo()
        self._isExceeed    = False
        self._idx          = None
        self._status       = CJobTicketStatus.wait
        self._label        = ''
        self._note         = ''
        self._numberid         = ''
        self._jobDate  = CDateInfo()
        self._begJobTime  = CDateTimeInfo()
        self._endJobTime  = CDateTimeInfo()
        self._begDateTime  = CDateTimeInfo()
        self._endDateTime  = CDateTimeInfo()
        self._capacity     = 0
        self._actions = []


    def __str__(self):
        self.load()
        if self._ok:
            if self._isExceeed:
                return u'%s, %s, сверх плана, %s' % ( unicode(self._jobType),
                                             forceString(self._datetime.datetime.date()),
                                             unicode(self._orgStructure) )
            else:
                return u'%s, %s, %s' % ( unicode(self._jobType),
                                         unicode(self._datetime),
                                         unicode(self._orgStructure) )
        else:
            return ''


    jobType      = property(lambda self: self.load()._jobType)
    jobPurpose      = property(lambda self: self.load()._jobPurpose)
    orgStructure = property(lambda self: self.load()._orgStructure)
    jobTicketOrgStructure = property(lambda self: self.load()._jobTicketOrgStructure)
    datetime     = property(lambda self: self.load()._datetime)
    isExceeed    = property(lambda self: self.load()._isExceeed)
    idx          = property(lambda self: self.load()._idx)
    status       = property(lambda self: self.load()._status)
    label        = property(lambda self: self.load()._label)
    note         = property(lambda self: self.load()._note)
    numberid         = property(lambda self: self.load()._numberid)
    jobDate  = property(lambda self: self.load()._jobDate)
    begJobTime  = property(lambda self: self.load()._begJobTime)
    endJobTime  = property(lambda self: self.load()._endJobTime)
    begDateTime  = property(lambda self: self.load()._begDateTime)
    endDateTime  = property(lambda self: self.load()._endDateTime)
    capacity     = property(lambda self: self.load()._capacity)
    actions = property(lambda self: self.load()._actions)


class CJobTicketsActionInfo(CActionInfo):
    def __init__(self, context, actionId, action=None):
        db = QtGui.qApp.db
        if not action:
            record = db.getRecord('Action', '*', actionId)
            action = CAction(record=record)
        else:
            record = action.getRecord()
        CCookedActionInfo.__init__(self, context, record, action)

    def isVisible(self, propertyType):
        return propertyType.visibleInJobTicket

    def __getitem__(self, key):
        actionType = self._action.getType()
        if isinstance(key, (basestring, QString)):
            try:
                property = self._action.getProperty(unicode(key))
                propertyType = property.type()
                if self.isVisible(propertyType):
                    return self.getInstance(CPropertyInfo, property)
                else:
                    raise CException(u'У действия типа "%s" свойство "%s" не выводится в выполнении работ' % (
                                                        actionType.name, unicode(key))
                                    )
            except KeyError:
                raise CException(u'Действие типа "%s" не имеет свойства "%s"' % (actionType.name, unicode(key)))
        if isinstance(key, (int, long)):
            try:
                return self.getInstance(CPropertyInfo, self._action.getPropertyByIndex(key))
            except IndexError:
                raise CException(u'Действие типа "%s" не имеет свойства c индексом "%s"' % (actionType.name, unicode(key)))
        else:
            raise TypeError, u'Action property subscription must be string or integer'


    def __iter__(self):
        for property in self._action.getProperties():
            if self.isVisible(property.type()):
                yield self.getInstance(CPropertyInfo, property)



class CJobTicketsActionInfoList(CInfoList):
    def __init__(self, context, idList, **kwargs):
        CInfoList.__init__(self, context)
        self._idList = idList
        self._presetActions = kwargs.get('presetActions', None)

    def _load(self):
        if self._presetActions:
            self._items = [ self.getInstance(CJobTicketsActionInfo, None, action=action) for action in self._presetActions ]
        else:
            self._items = [ self.getInstance(CJobTicketsActionInfo, id) for id in self._idList ]
        return True

# расширенный вариант используется при печати из выполнения работ (список, редактор одного jobTicket)

class CJobTicketWithActionsInfo(CJobTicketInfo):
    def __init__(self, context, id, **kwargs):
        CJobTicketInfo.__init__(self, context, id)
        self._presetActions = kwargs.get('presetActions', None)

    def _initByRecord(self, record):
        CJobTicketInfo._initByRecord(self, record)
        if self._presetActions:
            actionIdList = []
        else:
            actionIdList = CMapJobTicketsToActionsHelper.getActionIdList(self.id)
        self._actions = self.getInstance(CJobTicketsActionInfoList, tuple(actionIdList), presetActions=self._presetActions)

    def _initByNull(self):
        CJobTicketInfo._initByNull(self)
        self._actions = []

    actions = property(lambda self: self.load()._actions)


class CJobTicketsWithActionsInfoList(CInfoList):
    def __init__(self, context, idList):
        CInfoList.__init__(self, context)
        self._idList = idList

    def _load(self):
        self._items = [ self.getInstance(CJobTicketWithActionsInfo, id) for id in self._idList ]
        return True


# ##############################################################################

class CMapJobTicketsToActionsHelper():
    mapJobTicketToActionIdList = {}

    @classmethod
    def getActionIdList(cls, jobTicketId):
        return cls.mapJobTicketToActionIdList.get(jobTicketId, [])

    @classmethod
    def setActionId(cls, jobTicketId, actionId):
        actionIdList = cls.mapJobTicketToActionIdList.setdefault(jobTicketId, [])
        if actionId not in actionIdList:
            actionIdList.append(actionId)

    @classmethod
    def invalidate(cls):
        cls.mapJobTicketToActionIdList.clear()


def makeDependentActionIdList(jobTicketIdList):
    db = QtGui.qApp.db

    table       = db.table('Job_Ticket')
    tableAPJT   = db.table('ActionProperty_Job_Ticket')
    tableAP     = db.table('ActionProperty')
    tableAction = db.table('Action')

    queryTable = table.leftJoin(tableAPJT,        tableAPJT['value'].eq(table['id']))
    queryTable = queryTable.leftJoin(tableAP,     tableAP['id'].eq(tableAPJT['id']))
    queryTable = queryTable.leftJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))

    cond = [table['id'].inlist(jobTicketIdList)]
    fields = [table['id'].alias('jobTicketId'), tableAction['id'].alias('actionId')]

    recordList = db.getRecordList(queryTable, fields, cond)

    CMapJobTicketsToActionsHelper.invalidate()

    for record in recordList:
        jobTicketId = forceRef(record.value('jobTicketId'))
        actionId    = forceRef(record.value('actionId'))
        CMapJobTicketsToActionsHelper.setActionId(jobTicketId, actionId)


class CJobInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('Job', '*', self.id) if self.id else None
        if record:
            self._initByRecord(record)
            return True
        else:
            self._initByNull()
            return False


    def _initByRecord(self, record):
        self._jobType      = self.getInstance(CJobTypeInfo, forceRef(record.value('jobType_id')))
        self._jobPurpose   = self.getInstance(CJobPurposeInfo, forceRef(record.value('jobPurpose_id')))
        self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
        self._date         = CDateInfo(forceDateTime(record.value('date')))
        self._begTime      = CTimeInfo(forceDateTime(record.value('begTime')))
        self._endTime      = CTimeInfo(forceDateTime(record.value('endTime')))
        self._quantity     = forceInt(record.value('quantity'))
        self._capacity     = forceInt(record.value('capacity'))


    def _initByNull(self):
        self._jobType      = self.getInstance(CJobTypeInfo, None)
        self._jobPurpose   = self.getInstance(CJobPurposeInfo, None)
        self._orgStructure = self.getInstance(COrgStructureInfo, None)
        self._date         = CDateInfo()
        self._begTime      = CTimeInfo()
        self._endTime      = CTimeInfo()
        self._quantity     = 0
        self._capacity     = 0


    def __str__(self):
        self.load()
        return ''


    jobType      = property(lambda self: self.load()._jobType)
    jobPurpose   = property(lambda self: self.load()._jobPurpose)
    orgStructure = property(lambda self: self.load()._orgStructure)
    date         = property(lambda self: self.load()._date)
    begTime      = property(lambda self: self.load()._begTime)
    endTime      = property(lambda self: self.load()._endTime)
    quantity     = property(lambda self: self.load()._quantity)
    capacity     = property(lambda self: self.load()._capacity)


class CJobInfoList(CInfoList):
    def __init__(self, context, idList):
        CInfoList.__init__(self, context)
        self.idList = idList


    def _load(self):
        self._items = [ self.getInstance(CJobInfo, id) for id in self.idList ]
        return True


