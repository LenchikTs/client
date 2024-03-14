# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from library.crbcombobox        import CRBModelDataCache
from library.Utils              import forceDate, forceDateTime, forceRef, trim
from Resources.JobTicketChooser import CJobTicketChooserComboBox, getJobTicketAsText
from Resources.JobTicketChooserHelper import CJobTicketChooserHelper, TODAY, ANYDAY, ANYNEXTDAY, TODAYTIME
from Users.Rights               import urEditJobTicket
from ActionPropertyValueType    import CActionPropertyValueType


class CJobTicketActionPropertyValueType(CActionPropertyValueType):
    name         = 'JobTicket'
    variantType  = QVariant.Int
    isCopyable   = False
    initPresetValue = True

    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)
        self.domain = self.parseDomain(domain)
        self._presetValueAllowed = self.domain['presetValueAllowed']
        self._forDays            = self.domain['forDays']
        self._jobTypeCode        = self.domain['jobTypeCode']
        self._chainLength        = self.domain['chainLength']
        self._countDays = self.domain['countDays']
        self._execOrgStructureId = None
        self._execJobPurposeId = None
        self._jobOrgStructureIdList = None
        self._isExceedJobTicket  = False
        self._isNearestJobTicket = False
        self._prematurelyClosingThreshold = 0
        self._isOrderDESC        = False
        self._dateTimeExecJob    = None


    @staticmethod
    def parseDomain(domain):
        # синтаксис:
        #   <код>[;A[0]],<длина цепочки>]]
        # <код> - код типа работы
        # A - возможность выбирать автоматом только на тек.дату
        # A0 - возможность выбирать автоматом на любую дату
        # <длина цепочки> - это длина цепочки талонов.

        presetValueAllowed = False
        forDays = TODAY
        countDays = 0
        chainLength = 1
        specialValues = presetSpecialValues = ''
        domain = domain.split(';')
        jobTypeCode = trim(domain[0])
        if len(domain) > 1:
            specialValuesStr = trim(domain[1]).lower()
            specialValuesList = specialValuesStr.split(',')

            if len(specialValuesList) == 1:
                specialValues = specialValuesList[0]
                if specialValues:
                    if specialValues[0] in ('a', u'а'):
                        presetSpecialValues = specialValues
                    else:
                        chainLength = specialValues
            elif len(specialValuesList) == 2:
                presetSpecialValues, chainLength = specialValuesList
            else:
                return {}

            if len(presetSpecialValues) == 1:
                presetValueAllowed = presetSpecialValues in ('a', u'а') # en & ru
            elif len(presetSpecialValues) == 2:
                presetValueAllowed = presetSpecialValues[0] in ('a', u'а') # en & ru
                if presetSpecialValues[1] == '0':
                    forDays = ANYDAY
                elif presetSpecialValues[1] == '1':
                    forDays = ANYNEXTDAY
                elif presetSpecialValues[1] == 't':
                    forDays = TODAYTIME
            elif len(presetSpecialValues) > 2:
                presetValueAllowed = presetSpecialValues[0] in ('a', u'а')  # en & ru
                presetSpecialValuesCountDays = presetSpecialValues.split(u':')
                if len(presetSpecialValuesCountDays) == 2:
                    if presetSpecialValues[1] == '1':
                        forDays = ANYNEXTDAY
                        countDays = presetSpecialValuesCountDays[1]
        return {'jobTypeCode'       : jobTypeCode,
                'presetValueAllowed': presetValueAllowed,
                'forDays'           : forDays,
                'chainLength'       : int(chainLength),
                'countDays'         : int(countDays)
               }


    def chainLength(self):
        return self._chainLength


    def getjobTypeCode(self):
        return self._jobTypeCode


    def getJobTypeId(self):
        if self._jobTypeCode:
            data = CRBModelDataCache.getData('rbJobType')
            return data.getIdByCode(self._jobTypeCode)
        else:
            return None


    @staticmethod
    def getParsedDomain(domain):
        return CJobTicketActionPropertyValueType.parseDomain(domain)


    class CPropEditor(CJobTicketChooserComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId, reservedJobTickets={}):
            CJobTicketChooserComboBox.__init__(self, parent)

            jobTypeCode = domain['jobTypeCode']
#            chainLength = domain['chainLength']
#            self.setchainLengthValue(chainLength)
            self.setEventTypeId(eventTypeId)
            self.setClientId(clientId)
            self.setReservedJobTickets(reservedJobTickets)
            self.setDefaultJobTypeCode(jobTypeCode)
            date = forceDate(action._record.value('begDate')) if action else None
            if date:
                self.setDefaultDate(date)
            actionTypeId = forceRef(action._record.value('actionType_id')) if action else None
            if actionTypeId:
                self.setActionTypeId(actionTypeId)

            enabled = QtGui.qApp.userHasRight(urEditJobTicket)
            if jobTypeCode:
                enabled = enabled and QtGui.qApp.isUserAvailableJobType(jobTypeCode)
            self.setEnabled(enabled)


        def setValue(self, value):
            CJobTicketChooserComboBox.setValue(self, forceRef(value))


    def setExecOrgStructureId(self, execOrgStructureId):
        self._execOrgStructureId = execOrgStructureId


    def setJobOrgStructureIdList(self, jobOrgStructureIdList):
        self._jobOrgStructureIdList = jobOrgStructureIdList


    def setExecJobPurposeId(self, execJobPurposeId):
        self._execJobPurposeId = execJobPurposeId


    def setIsExceedJobTicket(self, isExceedJobTicket):
        self._isExceedJobTicket = isExceedJobTicket


    def setIsNearestJobTicket(self, isNearestJobTicket):
        self._isNearestJobTicket = isNearestJobTicket


    def setPrematurelyClosingThreshold(self, prematurelyClosingThreshold):
        self._prematurelyClosingThreshold = prematurelyClosingThreshold


    def setIsOrderDESC(self, isOrderDESC):
        self._isOrderDESC = isOrderDESC


    def setDateTimeExecJob(self, dateTimeExecJob):
        self._dateTimeExecJob = dateTimeExecJob


    def resetParams(self):
        self._execOrgStructureId = None
        self._isExceedJobTicket  = False
        self._isNearestJobTicket = False
        self._prematurelyClosingThreshold = 0
        self._isOrderDESC        = False
        self._dateTimeExecJob    = None


    def getPresetValue(self, action):
        jobTicketId = None
        if self._presetValueAllowed:
            jobTicketId = self.getPresetValueWithoutAutomatic(action)
        self.resetParams()
        return jobTicketId


    def getPresetValueWithoutAutomatic(self, action, isFreeJobTicket=False):
        jobTypeId = self.getJobTypeId()
        if jobTypeId:
            db = QtGui.qApp.db
            jobTypeIdList = db.getDescendants('rbJobType', 'group_id', jobTypeId)
            if len(jobTypeIdList) == 1 and jobTypeIdList[0] == jobTypeId:
                conditions = action.presetValuesConditions
                clientId = conditions.get('clientId')
                eventTypeId = conditions.get('eventTypeId')
                courseDate = conditions.get('courseDate')
                courseTime = conditions.get('courseTime')
                firstInCourse = conditions.get('firstInCourse', False)
                if not conditions:
                    record = action.getRecord()
                    if record:
                        eventId = forceRef(record.value('event_id'))
                        if eventId:
                            tableEvent = db.table('Event')
                            recordEvent = db.getRecordEx(tableEvent, [tableEvent['client_id'], tableEvent['eventType_id']], [tableEvent['id'].eq(eventId), tableEvent['deleted'].eq(0)])
                            if recordEvent:
                                clientId = forceRef(recordEvent.value('client_id'))
                                eventTypeId = forceRef(recordEvent.value('eventType_id'))
                date = (forceDateTime(action._record.value('begDate')) if action._actionType.showTime else forceDate(action._record.value('begDate'))) if action else None
                if self._dateTimeExecJob:
                    actionEndDate = self._dateTimeExecJob
                else:
                    actionEndDate = (forceDateTime(action._record.value('endDate')) if action._actionType.showTime else forceDate(action._record.value('endDate'))) if action else None
                ticketDuration = action._actionType.ticketDuration if action._actionType else None
                actionTypeId = forceRef(action._record.value('actionType_id')) if action else None
                return CJobTicketChooserHelper(jobTypeId, clientId, eventTypeId, self._chainLength, self._forDays,
                                               courseDate=courseDate, courseTime=courseTime,
                                               firstInCourse=firstInCourse, actionDate=date,
                                               ticketDuration=ticketDuration, actionTypeId=actionTypeId,
                                               actionEndDate=actionEndDate, isNearestJobTicket=self._isNearestJobTicket,
                                               execOrgStructureId=self._execOrgStructureId,
                                               isFreeJobTicket=isFreeJobTicket,
                                               execJobPurposeId=self._execJobPurposeId,
                                               jobOrgStructureIdList=self._jobOrgStructureIdList,
                                               countDays=self._countDays,
                                               prematurelyClosingThreshold=self._prematurelyClosingThreshold
                                               ).get(isExceedJobTicket=self._isExceedJobTicket, isOrderDESC=self._isOrderDESC)
        return None


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue

    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'Job_Ticket'


    def toText(self, v):
        return getJobTicketAsText(forceRef(v))


    def toInfo(self, context, v):
        from Resources.JobTicketInfo import CJobTicketInfo
        return CJobTicketInfo(context, forceRef(v))
