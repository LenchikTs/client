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

from PyQt4 import QtGui

from library.PrintInfo       import (
                                     CInfo,
                                     CInfoList,
                                     CDateTimeInfo,
                                     CRBInfo,
                                     CRBInfoWithIdentification,
                                    )
from library.Utils           import (
                                     forceBool,
                                     forceDateTime,
                                     forceDouble,
                                     forceInt,
                                     forceRef,
                                     forceString,
                                    )

from RefBooks.Test.Info      import CTestInfo
from RefBooks.Unit.Info      import CUnitInfo

from Registry.Utils          import CClientInfo
from Orgs.PersonInfo         import CPersonInfo

from TissueJournal.TissueJournalModels import probeStatuses


class CTissueTypeInfo(CRBInfoWithIdentification):
    tableName = 'rbTissueType'


class CTakenTissueJournalInfo(CInfo):
    def __init__(self, context, takenTissueJournalId):
        CInfo.__init__(self, context)
        self.id = takenTissueJournalId


    def _load(self):
        from Events.ActionInfo import CUnitInfo

        db = QtGui.qApp.db
        record = db.getRecord('TakenTissueJournal', '*', self.id) if self.id else None
        if record:
            self._client = self.getInstance(CClientInfo, forceRef(record.value('client_id')))
            self._tissueType = self.getInstance(CTissueTypeInfo, forceRef(record.value('tissueType_id')))
            self._externalId = forceString(record.value('externalId'))
            self._number = forceString(record.value('externalId'))
            self._amount = forceInt(record.value('amount'))
            self._unit = self.getInstance(CUnitInfo, forceRef(record.value('unit_id')))
            self._datetimeTaken = CDateTimeInfo(forceDateTime(record.value('datetimeTaken')))
            self._execPerson = self.getInstance(CPersonInfo, forceRef(record.value('execPerson_id')))
            self._note = forceString(record.value('note'))
            self._probes = self.getInstance(CProbeInfoList, forceRef(record.value('id')))
            return True
        else:
            self._client = self.getInstance(CClientInfo, None)
            self._tissueType = self.getInstance(CTissueTypeInfo, None)
            self._externalId = ''
            self._number = ''
            self._amount = 0
            self._unit = self.getInstance(CUnitInfo, None)
            self._datetimeTaken = CDateTimeInfo()
            self._execPerson = self.getInstance(CPersonInfo, None)
            self._note = ''
            self._probes = self.getInstance(CProbeInfoList, None)
            return False

    client        = property(lambda self: self.load()._client)
    tissueType    = property(lambda self: self.load()._tissueType)
    externalId    = property(lambda self: self.load()._externalId)
    number        = property(lambda self: self.load()._number)
    amount        = property(lambda self: self.load()._amount)
    unit          = property(lambda self: self.load()._unit)
    datetimeTaken = property(lambda self: self.load()._datetimeTaken)
    execPerson    = property(lambda self: self.load()._execPerson)
    note          = property(lambda self: self.load()._note)
    probes          = property(lambda self: self.load()._probes)

tissueJournalValuesCache = {}


class CEquipmentInfo(CRBInfo):
    tableName = 'rbEquipment'


class CSuiteReagentInfo(CRBInfo):
    tableName = 'SuiteReagent'


class CSpecimentTypeInfo(CRBInfoWithIdentification):
    tableName = 'rbSpecimenType'


class CContainerTypeInfo(CRBInfoWithIdentification):
    tableName = 'rbContainerType'

    def _initByRecord(self, record):
        self._amount = forceDouble(record.value('amount'))
        self._color = forceString(record.value('color'))
        self._unit = self.getInstance(CUnitInfo, forceRef(record.value('unit_id')))


    def _initByNull(self):
        self._amount = 0
        self._color = ''
        self._unit = self.getInstance(CUnitInfo, None)


    amount = property(lambda self: self.load()._amount)
    color = property(lambda self: self.load()._color)
    unit = property(lambda self: self.load()._unit)


class CProbeInfoList(CInfoList):
    def __init__(self, context, takenTissueJournalId):
        CInfoList.__init__(self, context)
        self.takenTissueJournalId = takenTissueJournalId
        self._recordList = []

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Probe')
        self._recordList = db.getRecordList(table, '*', table['takenTissueJournal_id'].eq(self.takenTissueJournalId), 'id')
        self._items = [ self.getInstance(CProbeInfo, record, None) for record in self._recordList ]
        return True


class CProbeInfo(CInfo):
    def __init__(self, context, record, probe):
        CInfo.__init__(self, context)
        self._record = record
        self._probe = probe

    def _load(self):
        if self._record:
            self.initByRecord(self._record)
            return True
        else:
            self.initByRecord(QtGui.qApp.db.dummyRecord())
            return False

    def getTissueJournalValues(self, tissueJournalId):
        record = QtGui.qApp.db.getRecord(QtGui.qApp.db.table('TakenTissueJournal'), 'tissueType_id, externalId, datetimeTaken', tissueJournalId)
        return forceRef(record.value('tissueType_id')), forceString(record.value('externalId')), forceDateTime(record.value('datetimeTaken'))


    def initByRecord(self, record):
        self._externalId = forceString(record.value('externalId'))
        self._isUrgent = forceBool(record.value('isUrgent'))
        self._status = probeStatuses[forceInt(record.value('status'))]
        self._workTest = self.getInstance(CTestInfo, forceInt(record.value('workTest_id')))
        self._specimenType = self.getInstance(CSpecimentTypeInfo, forceInt(record.value('specimenType_id')))
        self._norm = forceString(record.value('norm'))
        self._externalEvaluation = forceString(record.value('norm'))
        self._id = forceInt(record.value('id'))
        self._person = self.getInstance(CPersonInfo, forceInt(record.value('person_id')))
        self._result1 = forceString(record.value('result1'))
        self._result2 = forceString(record.value('result2'))
        self._result3 = forceString(record.value('result3'))
        self._suiteReagent = self.getInstance(CSuiteReagentInfo, forceInt(record.value('suiteReagent_id')))
        self._equipment = self.getInstance(CEquipmentInfo, forceInt(record.value('equipment_id')))
        self._unit = self.getInstance(CUnitInfo, forceRef(record.value('unit_id')))
        self._tripodNumber = forceString(record.value('tripodNumber'))
        self._placeInTripod = forceString(record.value('placeInTripod'))
        self._typeName = forceString(record.value('typeName'))
        self._date = ''
        tissueJournalId = forceRef(record.value('takenTissueJournal_id'))
        containerTypeId = forceRef(record.value('containerType_id'))
        self._ibm = ''
        self._tissueType = ''
        self._colorMark = ''
        self._containerCount = 0
        self._containerType = self.getInstance(CContainerTypeInfo, containerTypeId)
        self._takenTissueJournal = self.getInstance(CTakenTissueJournalInfo, tissueJournalId)
        if self._probe:
            self._colorMark = self._probe[7].name() if self._probe[7] else ''
            self._containerCount = forceInt(self._probe[8])
            self._date = self._probe[3] if self._probe[3] else ''
        if tissueJournalId:
            values = tissueJournalValuesCache.get(tissueJournalId, None)
            if not values:
                tissueTypeId, ibm, datetimeTaken = self.getTissueJournalValues(tissueJournalId)
                values = tissueTypeId, ibm, datetimeTaken
                tissueJournalValuesCache[tissueJournalId] = values
            self._tissueType = self.getInstance(CTissueTypeInfo, values[0])
            self._ibm = values[1]


    ibm   = property(lambda self: self.load()._ibm)
    externalId   = property(lambda self: self.load()._externalId)
    isUrgent = property(lambda self: self.load()._isUrgent)
    status = property(lambda self: self.load()._status)
    workTest = property(lambda self: self.load()._workTest)
    specimenType = property(lambda self: self.load()._specimenType)
    norm = property(lambda self: self.load()._norm)
    externalEvaluation = property(lambda self: self.load()._externalEvaluation)
    id = property(lambda self: self.load()._id)
    person = property(lambda self: self.load()._person)
    result1 = property(lambda self: self.load()._result1)
    result2 = property(lambda self: self.load()._result2)
    result3 = property(lambda self: self.load()._result3)
    suiteReagent = property(lambda self: self.load()._suiteReagent)
    equipment = property(lambda self: self.load()._equipment)
    unit = property(lambda self: self.load()._unit)
    tripodNumber = property(lambda self: self.load()._tripodNumber)
    placeInTripod = property(lambda self: self.load()._placeInTripod)
    typeName = property(lambda self: self.load()._typeName)
    tissueType = property(lambda self: self.load()._tissueType)
    date = property(lambda self: self.load()._date)
    colorMark = property(lambda self: self.load()._colorMark)
    containerCount = property(lambda self: self.load()._containerCount)
    containerType = property(lambda self: self.load()._containerType)
    takenTissueJournal = property(lambda self: self.load()._takenTissueJournal)


class CWorkListInfo(CInfoList):
    def __init__(self, context, recordList, probes):
        CInfoList.__init__(self, context)
        self.recordList = recordList
        self.probes = {}
        self._items = []
        for probe in probes:
            for id in probes[probe][0]:
                self.probes[id] = [probe[1]]
                self.probes[id].extend(probes[probe])


    def _load(self):
        for record in self.recordList:
            self._items.append(CProbeInfo(self.context, record, self.probes.get( forceRef(record.value('id')), None )))

        #self._items = [ self.getInstance(CProbeInfo, record) for record in self.recordList ]
        return True
