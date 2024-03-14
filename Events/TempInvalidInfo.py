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
from PyQt4.QtCore import QDate


from Events.MKBInfo    import CMKBInfo
from Orgs.PersonInfo   import CPersonInfo
from RefBooks.TypeEducationalInstitution.Info import CTypeEducationalInstitutionInfo
from Registry.Utils    import CClientInfo
from library.PrintInfo import (
                               CInfo,
                               CInfoList,
                               CDateInfo,
                               CDateTimeInfo,
                               CRBInfo,
                               CRBInfoWithIdentification,
                              )
from library.Utils     import (
                               forceBool,
                               forceDate,
                               forceDateTime,
                               forceInt,
                               forceRef,
                               forceString,
                               formatSex,
                               pyDate,
                              )

class CTempInvalidRegimeInfo(CRBInfo):
    tableName = 'rbTempInvalidRegime'


class CTempInvalidBreakInfo(CRBInfo):
    tableName = 'rbTempInvalidBreak'


class CTempInvalidResultInfo(CRBInfoWithIdentification):
    tableName = 'rbTempInvalidResult'

    def _initByRecord(self, record):
        self._type = forceInt(record.value('type'))
        self._able = forceInt(record.value('able'))
        self._state = forceInt(record.value('state'))
        self._decision = forceInt(record.value('decision'))

    def _initByNull(self):
        self._type = -1
        self._able = -1
        self._state = -1
        self._decision = -1

    type = property(lambda self: self.load()._type)
    able = property(lambda self: self.load()._able)
    state = property(lambda self: self.load()._state)
    decision = property(lambda self: self.load()._decision)


class CTempInvalidPeriodInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._begDate = CDateInfo()
        self._endDate = CDateInfo()
        self._endPerson = self.getInstance(CPersonInfo, None)
        self._chairPerson = self.getInstance(CPersonInfo, None)
        self._isExternal = None
        self._regime = None
        self._note = ''
        self._duration = 0
        self._isSigned = False
        self._signPerson = self.getInstance(CPersonInfo, None)
        self._signDatetime = CDateTimeInfo()
        self._signItem = self.getInstance(CTempInvalidDocumentItemInfo, None)
        self._signSubject = ''
        self._expert = None
        self._export = None
        self._result = None


    def _load(self):
        if self.id:
            db = QtGui.qApp.db
            tablePeriod = db.table('TempInvalid_Period')
            tableSignature = db.table('TempInvalidDocument_Signature')
            tableExport = db.table('TempInvalidDocument_Export')

            table = tablePeriod
            table = table.leftJoin(tableSignature, db.joinAnd([
                    tablePeriod['begDate'].eq(tableSignature['begDate']),
                    tablePeriod['endDate'].eq(tableSignature['endDate']),
                    'EXISTS(SELECT 1 FROM TempInvalidDocument WHERE TempInvalidDocument.master_id = TempInvalid_Period.master_id AND TempInvalidDocument_Signature.master_id = TempInvalidDocument.id)'
                ]))
            table = table.leftJoin(tableExport, tableExport['master_id'].eq(tableSignature['master_id']))
            cols = [ 'TempInvalid_Period.*',
                     '(TempInvalidDocument_Signature.id IS NOT NULL) AS isSigned',
                     tableSignature['signPerson_id'],
                     tableSignature['signDatetime'],
                     tableSignature['master_id'],
                     tableSignature['subject'],
                     'TempInvalidDocument_Export.note as export'
                   ]
            record = db.getRecordEx(table, cols, tablePeriod['id'].eq(self.id))
            if record:
                self.initByRecord(record)
                return True
        return False


    def initByRecord(self, record):
        self._begDate      = CDateInfo(forceDate(record.value('begDate')))
        self._endDate      = CDateInfo(forceDate(record.value('endDate')))
        self._endPerson    = self.getInstance(CPersonInfo, forceRef(record.value('endPerson_id')))
        self._chairPerson  = self.getInstance(CPersonInfo, forceRef(record.value('chairPerson_id')))
        self._isExternal   = forceBool(record.value('isExternal'))
        self._regime       = self.getInstance(CTempInvalidRegimeInfo, forceRef(record.value('regime_id')))
        self._duration     = forceInt(record.value('duration'))
        self._note         = forceString(record.value('note'))
        self._isSigned     = forceBool(record.value('isSigned'))
        self._signPerson   = self.getInstance(CPersonInfo, forceRef(record.value('signPerson_id')))
        self._signDatetime = CDateTimeInfo(forceDateTime(record.value('signDatetime')))
        self._signItem     = self.getInstance(CTempInvalidDocumentItemInfo, forceRef(record.value('master_id')))
        self._signSubject  = forceString(record.value('subject'))
        self._export = forceString(record.value('export'))
        self._expert = self.getInstance(CPersonInfo, forceRef(record.value('expert_id')))
        self._result = self.getInstance(CTempInvalidResultInfo, forceRef(record.value('result_id')))


    begDate      = property(lambda self: self.load()._begDate)
    endDate      = property(lambda self: self.load()._endDate)
    endPerson    = property(lambda self: self.load()._endPerson)
    chairPerson  = property(lambda self: self.load()._chairPerson)
    isExternal   = property(lambda self: self.load()._isExternal)
    regime       = property(lambda self: self.load()._regime)
    duration     = property(lambda self: self.load()._duration)
    note         = property(lambda self: self.load()._note)
    isSigned     = property(lambda self: self.load()._isSigned)
    signPerson   = property(lambda self: self.load()._signPerson)
    signDatetime = property(lambda self: self.load()._signDatetime)
    signItem     = property(lambda self: self.load()._signItem)
    signSubject  = property(lambda self: self.load()._signSubject)
    export = property(lambda self: self.load()._export)
    expert = property(lambda self: self.load()._expert)
    result = property(lambda self: self.load()._result)


class CTempInvalidPeriodInfoList(CInfoList):
    def __init__(self, context, tempInvalidId):
        CInfoList.__init__(self, context)
        self.tempInvalidId = tempInvalidId


    def addItem(self, id, record=None):
        item = self.getInstance(CTempInvalidPeriodInfo, id)
        if record:
            item.initByRecord(record)
            item.setOkLoaded()
        self._items.append(item)


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('TempInvalid_Period')
        stmt = db.selectStmt(table, fields='id', where=table['master_id'].eq(self.tempInvalidId), order='begDate, id')
        result = db.query(stmt)
        while result.next():
            record = result.record()
            id = forceRef(record.value('id'))
            self.addItem(id)
        return True


class CTempInvalidInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._type    = None
        self._doctype = context.getInstance(CTempInvalidDocTypeInfo, None)
        self._reason  = context.getInstance(CTempInvalidReasonInfo, None)
        self._changedReason  = context.getInstance(CTempInvalidReasonInfo, None)
        self._extraReason = context.getInstance(CTempInvalidExtraReasonInfo, None)
        self._busyness = 0
        self._placeWork = ''
        self._serial  = ''
        self._number  = ''
        self._sex     = ''
        self._age     = ''
        self._receiver= ''
        self._eventId = None
        self._duration = 0
        self._externalDuration = 0
        self._caseBegDate = CDateInfo()
        self._issueDate = CDateInfo()
        self._begDate = CDateInfo()
        self._endDate = CDateInfo()
        self._person = context.getInstance(CPersonInfo, None)
        self._state = None
        self._prev  = None
        self._accountPregnancyTo12Weeks = 0
        self._MKB   = self.getInstance(CMKBInfo, '')
        self._MKBEx = self.getInstance(CMKBInfo, '')
        self._periods = []
        self._visitsCount = 0
        self._insuranceOfficeMark = 0
        self._begDateStationary = CDateInfo()
        self._endDateStationary = CDateInfo()
        self._break = self.getInstance(CTempInvalidBreakInfo, None)
        self._breakDate = CDateInfo()
        self._result =  self.getInstance(CTempInvalidResultInfo, None)
        self._resultDate = CDateInfo()
        self._resultOtherwiseDate = CDateInfo()
        self._numberPermit = ''
        self._OGRN = ''
        self._begDatePermit = CDateInfo()
        self._endDatePermit = CDateInfo()
        self._regime     = self.getInstance(CTempInvalidRegimeInfo, None)
        self._items = []
        self._isSigned = False
        self._eventId = None
        self._institution = self.getInstance(CTypeEducationalInstitutionInfo, None)
        self._inf_contact = ''


    def _load(self):
        if self.id:
            db = QtGui.qApp.db
            table = db.table('TempInvalid')
            tableDoc = db.table('TempInvalidDocument')
            tableDocSign = db.table('TempInvalidDocument_Signature')
            tableEvent = db.table('Event')
            tableVisit = db.table('Visit')
            tableDiagnosis = db.table('Diagnosis')
            tableEx = table.leftJoin(tableDiagnosis, tableDiagnosis['id'].eq(table['diagnosis_id']))
            tableEx = tableEx.leftJoin(tableEvent, tableEvent['client_id'].eq(table['client_id']))
            tableEx = tableEx.leftJoin(tableVisit, [tableVisit['event_id'].eq(tableEvent['id']),
                                                                            tableVisit['date'].dateGe(table['begDate']),
                                                                            tableVisit['date'].dateLe(table['endDate']) ])

            subTable = table.innerJoin(tableDoc, table['id'].eq(tableDoc['master_id']))
            subTable = subTable.innerJoin(tableDocSign, tableDoc['id'].eq(tableDocSign['master_id']))

            cond = [table['id'].eq(self.id),
                    tableEvent['deleted'].eq(0),
                    tableVisit['deleted'].eq(0),
                   ]
            subCond = [table['id'].eq(self.id),
                       tableDocSign['subject'].eq('R'),
                       table['state'].eq(1)
                      ]
            cols = ['TempInvalid.*',
                    tableDiagnosis['MKB'],
                    tableDiagnosis['MKBEx'],
                    'COUNT(Visit.id) AS `visitsCount`',
                    'EXISTS(%s) AS `isSigned`' % db.selectStmt(subTable, tableDocSign['id'], subCond),
                   ]
            record = db.getRecordEx(tableEx, cols, cond)
            if record:
                self.initByRecord(record)
                return True
        return False


    def initByRecord(self, record):
        self._type    = forceInt(record.value('type'))
        self._doctype = self.getInstance(CTempInvalidDocTypeInfo, forceRef(record.value('doctype_id')))
        self._reason  = self.getInstance(CTempInvalidReasonInfo,  forceRef(record.value('tempInvalidReason_id')))
        self._changedReason  = self.getInstance(CTempInvalidReasonInfo,  forceRef(record.value('tempInvalidChangedReason_id')))
        self._extraReason  = self.getInstance(CTempInvalidExtraReasonInfo, forceRef(record.value('tempInvalidExtraReason_id')))
        self._busyness = forceInt(record.value('busyness'))
        self._placeWork = forceString(record.value('placeWork'))
        self._serial  = forceString(record.value('serial'))
        self._number  = forceString(record.value('number'))
        self._sex     = formatSex(forceInt(record.value('sex')))
        self._age     = forceInt(record.value('age'))
        self._receiver= self.getInstance(CClientInfo, forceRef(record.value('receiver_id')))
        self._duration= forceInt(record.value('duration'))
        self._externalDuration = 0
        self._caseBegDate = CDateInfo(forceDate(record.value('caseBegDate')))
        self._issueDate = CDateInfo(forceDate(record.value('issueDate')))
        self._begDate = CDateInfo(forceDate(record.value('begDate')))
        self._endDate = CDateInfo(forceDate(record.value('endDate')))
        self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
        self._state  = forceInt(record.value('state'))
        self._accountPregnancyTo12Weeks = forceInt(record.value('accountPregnancyTo12Weeks'))
        self._MKB = self.getInstance(CMKBInfo, forceString(record.value('MKB')))
        self._MKBEx = self.getInstance(CMKBInfo, forceString(record.value('MKBEx')))
        self._eventId = forceInt(record.value('eventId'))
        prev_id = forceRef(record.value('prev_id'))
        if prev_id:
            self._prev = self.getInstance(CTempInvalidInfo, prev_id)
        self._periods = self.getInstance(CTempInvalidPeriodInfoList, self.id)
        self._client = self.getInstance(CClientInfo, forceInt(record.value('client_id')))
        self._visitsCount = forceInt(record.value('visitsCount'))
        self._insuranceOfficeMark = forceInt(record.value('insuranceOfficeMark'))
        self._begDateStationary = CDateInfo(forceDate(record.value('begDateStationary')))
        self._endDateStationary = CDateInfo(forceDate(record.value('endDateStationary')))
        self._break = self.getInstance(CTempInvalidBreakInfo, forceRef(record.value('break_id')))
        self._breakDate = CDateInfo(forceDate(record.value('breakDate')))
        self._result =  self.getInstance(CTempInvalidResultInfo, forceRef(record.value('result_id')))
        self._resultDate = CDateInfo(forceDate(record.value('resultDate')))
        self._resultOtherwiseDate = CDateInfo(forceDate(record.value('resultOtherwiseDate')))
        self._numberPermit = forceString(record.value('numberPermit'))
        self._OGRN = forceString(record.value('OGRN'))
        self._begDatePermit = CDateInfo(forceDate(record.value('begDatePermit')))
        self._endDatePermit = CDateInfo(forceDate(record.value('endDatePermit')))
        self._regime     = self.getInstance(CTempInvalidRegimeInfo, forceRef(record.value('regime_id')))
        self._items = self.getInstance(CTempInvalidDocumentItemInfoList, self.id)
        self._isSigned = forceBool(record.value('isSigned'))
        self._institution = self.getInstance(CTypeEducationalInstitutionInfo, forceRef(record.value('institution_id')))
        self._inf_contact = forceString(record.value('inf_contact'))


    type        = property(lambda self: self.load()._type)
    doctype     = property(lambda self: self.load()._doctype)
    reason      = property(lambda self: self.load()._reason)
    changedReason = property(lambda self: self.load()._changedReason)
    extraReason = property(lambda self: self.load()._extraReason)
    busyness    = property(lambda self: self.load()._busyness)
    placeWork   = property(lambda self: self.load()._placeWork)
    serial      = property(lambda self: self.load()._serial)
    number      = property(lambda self: self.load()._number)
    sex         = property(lambda self: self.load()._sex)
    age         = property(lambda self: self.load()._age)
    receiver    = property(lambda self: self.load()._receiver)
    duration    = property(lambda self: self.load()._duration)
    externalDuration = property(lambda self: self.load()._externalDuration)
    caseBegDate = property(lambda self: self.load()._caseBegDate)
    issueDate   = property(lambda self: self.load()._issueDate)
    begDate     = property(lambda self: self.load()._begDate)
    endDate     = property(lambda self: self.load()._endDate)
    person      = property(lambda self: self.load()._person)
    MKB         = property(lambda self: self.load()._MKB)
    MKBEx       = property(lambda self: self.load()._MKBEx)
    eventId     = property(lambda self: self.load()._eventId)
    periods     = property(lambda self: self.load()._periods)
    state       = property(lambda self: self.load()._state)
    accountPregnancyTo12Weeks = property(lambda self: self.load()._accountPregnancyTo12Weeks)
    prev        = property(lambda self: self.load()._prev)
    client      = property(lambda self: self.load()._client)
    visitsCount = property(lambda self: self.load()._visitsCount)
    insuranceOfficeMark = property(lambda self: self.load()._insuranceOfficeMark)
    begDateStationary = property(lambda self: self.load()._begDateStationary)
    endDateStationary = property(lambda self: self.load()._endDateStationary)
    break_ = property(lambda self: self.load()._break)
    breakDate = property(lambda self: self.load()._breakDate)
    result = property(lambda self: self.load()._result)
    resultDate = property(lambda self: self.load()._resultDate)
    resultOtherwiseDate = property(lambda self: self.load()._resultOtherwiseDate)
    numberPermit = property(lambda self: self.load()._numberPermit)
    OGRN = property(lambda self: self.load()._OGRN)
    begDatePermit = property(lambda self: self.load()._begDatePermit)
    endDatePermit = property(lambda self: self.load()._endDatePermit)
    regime = property(lambda self: self.load()._regime)
    items = property(lambda self: self.load()._items)
    isSigned = property(lambda self: self.load()._isSigned)
    institution = property(lambda self: self.load()._institution)
    inf_contact = property(lambda self: self.load()._inf_contact)


class CTempInvalidDocumentItemInfoList(CInfoList):
    def __init__(self, context, tempInvalidtId):
        CInfoList.__init__(self, context)
        self.tempInvalidtId = tempInvalidtId


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('TempInvalidDocument')
        cond = [ table['master_id'].eq(self.tempInvalidtId),
                 table['deleted'].eq(0),
               ]
        stmt = db.selectStmt(table, fields='id', where=cond, order='id')
        result = db.query(stmt)
        while result.next():
            record = result.record()
            id = forceRef(record.value('id'))
            self.addItem(id)
        return True


    def addItem(self, id, record=None):
        item = self.getInstance(CTempInvalidDocumentItemInfo, id)
        if record:
            item.initByRecord(record)
            item.setOkLoaded()
        self._items.append(item)


class CTempInvalidDocumentItemInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._issueDate = CDateInfo()
        self._serial  = ''
        self._number  = ''
        self._duplicate  = 0
        self._duplicateReason = self.getInstance(CTempInvalidDuplicateReasonInfo, None)
        self._isExternal = None
        self._electronic  = 0
        self._busyness = 0
        self._placeWork = ''
        self._prevNumber = ''
        self._prev = None
        self._clientPrimum = self.getInstance(CClientInfo, None)
        self._clientSecond = self.getInstance(CClientInfo, None)
        self._last = None
        self._prevDuplicate = None
        self._person = self.getInstance(CPersonInfo, None)
        self._execPerson = self.getInstance(CPersonInfo, None)
        self._chairPerson = self.getInstance(CPersonInfo, None)
        self._annulmentReason = self.getInstance(CTempInvalidAnnulmentReasonInfo, None)
        self._note = ''
        self._fssStatus = ''
        self._cares = self.getInstance(CTempInvalidDocumentCareInfoList, None)


    def _load(self):
        if self.id:
            db = QtGui.qApp.db
            table = db.table('TempInvalidDocument')
            cond = [ table['id'].eq(self.id),
                     table['deleted'].eq(0),
                   ]
            record = db.getRecordEx(table, '*', cond)
            if record:
                self.initByRecord(record)
                return True
        return False


    def initByRecord(self, record):
        self._issueDate  = CDateInfo(forceDate(record.value('issueDate')))
        self._serial  = forceString(record.value('serial'))
        self._number  = forceString(record.value('number'))
        self._duplicate = forceInt(record.value('duplicate'))
        self._duplicateReason = self.getInstance(CTempInvalidDuplicateReasonInfo, forceRef(record.value('duplicateReason_id')))
        self._isExternal = forceBool(record.value('isExternal'))
        self._electronic = forceInt(record.value('electronic'))
        self._busyness = forceInt(record.value('busyness'))
        self._placeWork = forceString(record.value('placeWork'))
        self._prevNumber = forceString(record.value('prevNumber'))
        prev_id = forceRef(record.value('prev_id'))
        if prev_id:
            self._prev = self.getInstance(CTempInvalidDocumentItemInfo, prev_id)
        self._clientPrimum = self.getInstance(CClientInfo, forceInt(record.value('clientPrimum_id')))
        self._clientSecond = self.getInstance(CClientInfo, forceInt(record.value('clientSecond_id')))
        last_id = forceRef(record.value('last_id'))
        if last_id:
            self._last = self.getInstance(CTempInvalidDocumentItemInfo, last_id)
        prevDuplicate_id = forceRef(record.value('prevDuplicate_id'))
        if prevDuplicate_id:
            self._prevDuplicate = self.getInstance(CTempInvalidDocumentItemInfo, prevDuplicate_id)
        self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
        self._execPerson = self.getInstance(CPersonInfo, forceRef(record.value('execPerson_id')))
        self._chairPerson = self.getInstance(CPersonInfo, forceRef(record.value('chairPerson_id')))
        self._annulmentReason = self.getInstance(CTempInvalidAnnulmentReasonInfo, forceRef(record.value('annulmentReason_id')))
        self._note = forceString(record.value('note'))
        self._fssStatus = forceString(record.value('fssStatus'))
        self._cares = self.getInstance(CTempInvalidDocumentCareInfoList, self.id)


    issueDate       = property(lambda self: self.load()._issueDate)
    serial          = property(lambda self: self.load()._serial)
    number          = property(lambda self: self.load()._number)
    duplicate       = property(lambda self: self.load()._duplicate)
    duplicateReason = property(lambda self: self.load()._duplicateReason)
    isExternal      = property(lambda self: self.load()._isExternal)
    electronic      = property(lambda self: self.load()._electronic)
    busyness        = property(lambda self: self.load()._busyness)
    placeWork       = property(lambda self: self.load()._placeWork)
    prevNumber      = property(lambda self: self.load()._prevNumber)
    prev            = property(lambda self: self.load()._prev)
    clientPrimum    = property(lambda self: self.load()._clientPrimum)
    clientSecond    = property(lambda self: self.load()._clientSecond)
    last            = property(lambda self: self.load()._last)
    prevDuplicate   = property(lambda self: self.load()._prevDuplicate)
    person          = property(lambda self: self.load()._person)
    execPerson      = property(lambda self: self.load()._execPerson)
    chairPerson     = property(lambda self: self.load()._chairPerson)
    annulmentReason = property(lambda self: self.load()._annulmentReason)
    note            = property(lambda self: self.load()._note)
    fssStatus            = property(lambda self: self.load()._fssStatus)
    cares           = property(lambda self: self.load()._cares)



class CTempInvalidDocumentCareInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self._id = id
        self._idx = 0
        self._client = self.getInstance(CClientInfo, None)
        self._begDate = CDateInfo()
        self._endDate = CDateInfo()
        self._regime = self.getInstance(CTempInvalidRegimeInfo, None)
        self._MKB = ''
        self._reason = self.getInstance(CTempInvalidReasonInfo, None)


    def _load(self):
        if self._id:
            db = QtGui.qApp.db
            table = db.table('TempInvalidDocument_Care')
            record = db.getRecord(table, '*', self._id)
            self.initByRecord(record)
            return True
        return False


    def initByRecord(self, record):
        if not record:
            return
        self._id = forceInt(record.value('id'))
        self._idx = forceInt(record.value('idx'))
        self._client = self.getInstance(CClientInfo, forceRef(record.value('client_id')))
        self._begDate = CDateInfo(forceDate(record.value('begDate')))
        self._endDate = CDateInfo(forceDate(record.value('endDate')))
        self._regime = self.getInstance(CTempInvalidRegimeInfo, forceRef(record.value('tempInvalidRegime_id')))
        self._MKB = forceString(record.value('MKB'))
        self._reason = self.getInstance(CTempInvalidReasonInfo, forceRef(record.value('tempInvalidReason_id')))


    id      = property(lambda self: self.load()._id)
    idx     = property(lambda self: self.load()._idx)
    client  = property(lambda self: self.load()._client)
    begDate = property(lambda self: self.load()._begDate)
    endDate = property(lambda self: self.load()._endDate)
    regime  = property(lambda self: self.load()._regime)
    MKB     = property(lambda self: self.load()._MKB)
    reason  = property(lambda self: self.load()._reason)



class CTempInvalidDocumentCareInfoList(CInfoList):
    def __init__(self, context, tempInvalidDocumentId):
        CInfoList.__init__(self, context)
        self._idList = []
        self._masterId = tempInvalidDocumentId


    def addItem(self, id, record=None):
        item = self.getInstance(CTempInvalidDocumentCareInfo, id)
        if record:
            item.initByRecord(record)
            item.setOkLoaded()
        self._items.append(item)


    def _load(self):
        if not self._idList and self._masterId:
            db = QtGui.qApp.db
            table = db.table('TempInvalidDocument_Care')
            self._idList = db.getIdList(table, 'id', [table['master_id'].eq(self._masterId)], order='idx')
            self._items = [ self.getInstance(CTempInvalidDocumentCareInfo, id) for id in self._idList ]
            return True
        return False



class CTempInvalidDocTypeInfo(CRBInfo):
    tableName = 'rbTempInvalidDocument'


class CTempInvalidReasonInfo(CRBInfoWithIdentification):
    tableName = 'rbTempInvalidReason'

    def _initByRecord(self, record):
        self._grouping = forceInt(record.value('grouping'))


    def _initByNull(self):
        self._grouping = None

    grouping = property(lambda self: self.load()._grouping)


class CTempInvalidExtraReasonInfo(CRBInfo):
    tableName = 'rbTempInvalidExtraReason'


class CTempInvalidAnnulmentReasonInfo(CRBInfo):
    tableName = 'rbTempInvalidAnnulmentReason'


class CTempInvalidInfoList(CInfoList):
    def __init__(self, context, clientId = None, begDate = None, endDate = None, types=(0, )):
        CInfoList.__init__(self, context)
        self.clientId = clientId
        self.begDate  = QDate(begDate) if begDate else None
        self.endDate  = QDate(endDate) if endDate else None
        self.types    = types
        self._idList = []

    def setIdList(self, idList):
        self._idList = idList


    def _load(self):
        if not self._idList and self.clientId:
            db = QtGui.qApp.db
            table = db.table('TempInvalid')
            cond = [ table['client_id'].eq(self.clientId),
                     table['deleted'].eq(0),
                     table['type'].inlist(self.types)]
            if self.begDate:
                cond.append(table['begDate'].ge(self.begDate))
            if self.endDate:
                cond.append(table['endDate'].le(self.endDate))
            self._idList = db.getIdList(table, 'id', cond, 'begDate')
        self._items = [ self.getInstance(CTempInvalidInfo, id) for id in self._idList ]
        return True


    @staticmethod
    def _get(context, clientId, begDate, endDate, types=None):
        if isinstance(endDate, CDateInfo):
            endDate = endDate.date
        if isinstance(begDate, CDateInfo):
            begDate = begDate.date
        if isinstance(types, (set, frozenset, list, tuple)):
            types = tuple(types)
        elif isinstance(types, (int, long, basestring)):
            types = (types, )
        elif types is None:
            types = (0, )
        else:
            raise ValueError('parameter "types" must be list, tuple, set or int')
        # потребность в pyDate обусловлена использованием дат в ключе кеша объектов.
        return context.getInstance(CTempInvalidInfoList, clientId, pyDate(begDate), pyDate(endDate), types)


class CTempInvalidPatronageInfoList(CTempInvalidInfoList):
    def __init__(self, context, clientId = None, begDate = None, endDate = None, types=(0, )):
        CTempInvalidInfoList.__init__(self, context, clientId, begDate, endDate, types)

    def _load(self):
        if not self._idList and self.clientId:
            db = QtGui.qApp.db
            table = db.table('TempInvalid')
            tableDocument = db.table('TempInvalidDocument')
            cond = [ tableDocument['clientPrimum_id'].eq(self.clientId),
                     table['deleted'].eq(0)]
            if self.begDate:
                cond.append(table['begDate'].ge(self.begDate))
            if self.endDate:
                cond.append(table['endDate'].le(self.endDate))
            queryTable = table
            queryTable = table.leftJoin(tableDocument, tableDocument['master_id'].eq(table['id']))
            self._idList = db.getIdList(queryTable, table['id'], cond, 'begDate')
        self._items = [ self.getInstance(CTempInvalidInfo, id) for id in self._idList ]
        return True


    @staticmethod
    def _get(context, clientId, begDate, endDate, types=None):
        if isinstance(endDate, CDateInfo):
            endDate = endDate.date
        if isinstance(begDate, CDateInfo):
            begDate = begDate.date
        if isinstance(types, (set, frozenset, list, tuple)):
            types = tuple(types)
        elif isinstance(types, (int, long, basestring)):
            types = (types, )
        elif types is None:
            types = (0, )
        else:
            raise ValueError('parameter "types" must be list, tuple, set or int')
        return context.getInstance(CTempInvalidPatronageInfoList, clientId, pyDate(begDate), pyDate(endDate), types)


class CTempInvalidAllInfoList(CInfoList):
    def __init__(self, context, idList):
        CInfoList.__init__(self, context)
        self._idList = idList

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('TempInvalid')
        records = db.getRecordList(table, [table['id'], table['id']], table['id'].inlist(self._idList))
        self._items = []
        dup = {}
        for record in records:
            id = forceInt(record.value(1))
            if id in dup:
                dup[id].append(record.value(0))
            else:
                dup[id] = [forceInt(record.value(0))]
        for id in self._idList:
            self._items.append( self.getInstance(CTempInvalidInfo, id) )
        return True

class CTempInvalidDuplicateReasonInfo(CRBInfo):
    tableName = 'rbTempInvalidDuplicateReason'


class CTempInvalidDuplicateInfo(CTempInvalidInfo):
    def __init__(self, context, tempInvalid_id, id):
        CTempInvalidInfo.__init__(self, context, tempInvalid_id)
        self.duplicate_id = id
        self._person = context.getInstance(CPersonInfo, None)
        self._date = CDateInfo()
        self._duplicateSerial = ''
        self._duplicateNumber = ''
        self._destination = ''
        self._duplicateReason = context.getInstance(CTempInvalidDuplicateReasonInfo, None)
        self._insuranceOfficeMark = -1
        self._duplicatePlaceWork = ''
        self._note = ''

    def _load(self):
        if CTempInvalidInfo._load(self) and self.duplicate_id:
            db = QtGui.qApp.db
            table = db.table('TempInvalidDuplicate')
            record = db.getRecordEx(table, '*', table['id'].eq(self.duplicate_id))
            if record:
                self.initDuplicateByRecord(record)
                return True
        return False


    def initDuplicateByRecord(self, record):
        self._person = self.getInstance(CPersonInfo, forceRef(record.value('person_id')))
        self._date = CDateInfo(forceDate(record.value('date')))
        self._duplicateSerial = forceString(record.value('serial'))
        self._duplicateNumber = forceString(record.value('number'))
        self._destination = forceString(record.value('destination'))
        self._duplicateReason = self.getInstance(CTempInvalidDuplicateReasonInfo, forceRef(record.value('reason_id')))
        self._insuranceOfficeMark = forceInt(record.value('insuranceOfficeMark'))
        self._duplicatePlaceWork = forceString(record.value('placeWork'))
        self._note = forceString(record.value('note'))


    person      = property(lambda self: self.load()._person)
    date        = property(lambda self: self.load()._date)
    duplicateSerial  = property(lambda self: self.load()._duplicateSerial)
    duplicateNumber  = property(lambda self: self.load()._duplicateNumber)
    destination = property(lambda self: self.load()._destination)
    duplicateReason      = property(lambda self: self.load()._duplicateReason)
    insuranceOfficeMark  = property(lambda self: self.load()._insuranceOfficeMark)
    duplicatePlaceWork   = property(lambda self: self.load()._duplicatePlaceWork)
