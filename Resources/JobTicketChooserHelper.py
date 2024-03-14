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

import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import QDateTime, QDate

from library.Utils import forceInt, forceDate, forceDateTime, forceRef

from Orgs.Utils import getSolitaryOrgStructureId, getOrgStructureDescendants

from JobTicketStatus import CJobTicketStatus


TODAY      = 0  # только сегодня
ANYDAY     = 1  # любая дата
ANYNEXTDAY = 2  # любая дата начиная с завтра
TODAYTIME  = 3  # только сегодня с учетом времени


class CJobTicketChooserHelper(object):
    def __init__(self, jobTypeId, clientId, eventTypeId, chainLength, forDays,
                 courseDate=None, courseTime=None, **kwargs):
        self.jobTypeId = jobTypeId
        self.forDays = forDays
        self.chainLength = chainLength
        self.clientId = clientId
        self.eventTypeId = eventTypeId
        self.courseDate = courseDate
        self.courseTime = courseTime
        self.jobOrgStructureIdList = kwargs.get('jobOrgStructureIdList', None)
        self.actionDate = kwargs.get('actionDate', None)
        self.actionTypeId = kwargs.get('actionTypeId', None)
        self.ticketDuration = kwargs.get('ticketDuration', None)
        self.actionEndDate = kwargs.get('actionEndDate', None)
        self.isExceedJobTicket = False
        self.isNearestJobTicket = kwargs.get('isNearestJobTicket', False)
        self.execOrgStructureId = kwargs.get('execOrgStructureId', None)
        self.execJobPurposeId = kwargs.get('execJobPurposeId', None)
        self.isFreeJobTicket = kwargs.get('isFreeJobTicket', False)
        self.countDays = kwargs.get('countDays', 0)
        self.prematurelyClosingThreshold = kwargs.get('prematurelyClosingThreshold', 0)
        self.isJobTicketLe = False
        self.isOrderDESC = False
        self.kwargs = kwargs

        self.__initTables()


    def __initTables(self):
        db = QtGui.qApp.db

        self.tableEvent = db.table('Event')
        self.tableAction = db.table('Action')
        self.tableActionProperty = db.table('ActionProperty')
        self.tableActionPropertyJobTicket = db.table('ActionProperty_Job_Ticket')
        self.tableJobTicket = db.table('Job_Ticket')
        self.tableJob = db.table('Job')
        self.tableJobPurpose = db.table('rbJobPurpose')
        self.tableJobPurposePractice = db.table('rbJobPurpose_Practice')


    def setActionTypeId(self, actionTypeId):
        self.actionTypeId = actionTypeId


    def get(self, isExceedJobTicket = False, isOrderDESC = False):
        self.isExceedJobTicket = isExceedJobTicket
        self.isJobTicketLe = False
        self.isOrderDESC = isOrderDESC
        if self.isNearestJobTicket:
            if bool(self.courseDate):
                result = self.selectCourseJobTicket()
            else:
                result = None
                if self.clientId:
                    self.isJobTicketLe = True
                    self.isOrderDESC = True
                    actionEndDate = self.actionEndDate
                    if self.prematurelyClosingThreshold > 0 and self.prematurelyClosingThreshold <= 24 and isinstance(
                            self.actionEndDate, QDateTime):
                        actionEndDate = self.actionEndDate.addSecs(self.prematurelyClosingThreshold * 3600)
                    result = self.selectUsedJobTicket(actionEndDate)
                    self.isJobTicketLe = False
                    self.isOrderDESC = False
                    if not result and not (self.prematurelyClosingThreshold > 0 and self.prematurelyClosingThreshold <= 24 and isinstance(self.actionEndDate, QDateTime)):
                        result = self.selectUsedJobTicket(self.actionEndDate)
                if not result:
                    self.isJobTicketLe = True
                    self.isOrderDESC = True
                    result = self.selectFreeJobTicket(date=self.actionEndDate)
                    self.isJobTicketLe = False
                    self.isOrderDESC = False
                    if not result:
                        result = self.selectFreeJobTicket(date=self.actionEndDate)
                if not result and self.isExceedJobTicket:
                    result = self.selectExceedJobTicket(self.actionEndDate)
                self.isJobTicketLe = False
                self.isOrderDESC = False
        else:
            if self.courseDate is not None:
                result = self.selectCourseJobTicket()
            else:
                result = None
            if self.clientId and not QtGui.qApp.checkGlobalPreference(u'23:uniqJobTickets', u'да'):
                result = self.selectUsedJobTicket(self.actionEndDate)
            if not result:
                result = self.selectFreeJobTicket(date=self.actionEndDate)
            if not result and self.isExceedJobTicket:
                result = self.selectExceedJobTicket(self.actionEndDate)
        return result


    def selectCourseJobTicket(self):
        jobId = self.getJobIdForSelect()
        if jobId:
            if self.courseTime is not None and not self.courseTime.isNull() and self.courseTime.isValid():
                # Так как у нас в курсовом плане назначений время задается с точностью только до минуты,
                # а номерки бывает по секндам то, наверное, следовало бы искать в диапазона этой минуты.
                # Но по обсуждениям, мы ищем свободные номерки +5 минут в перед.
                beg, end = QDateTime(self.courseDate), QDateTime(self.courseDate)
                beg.setTime(self.courseTime)
                end.setTime(self.courseTime.addSecs(5*60 - 1))
                date = (beg, end)
            else:
                date = self.courseDate
            result = self.selectUsedJobTicket(date)
            if not result:
                result = self.selectFreeJobTicket(date=date)
            if not result:
                result = self.createExceedJobTicket(jobId)
            return result

        elif self.kwargs.get('firstInCourse', False):
            return None

        return self.selectFreeJobTicket()


    def selectExceedJobTicket(self, date):
        result = None
        orgStructureIdList = []
        orgStructureId = self.execOrgStructureId if self.execOrgStructureId else QtGui.qApp.currentOrgStructureId()
        if orgStructureId:
            if not self.execOrgStructureId:
                orgStructureId = getSolitaryOrgStructureId(orgStructureId)
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
        jobId = self.getJobId(orgStructureId=orgStructureId, date=date)
        if not jobId:
            jobId = self.getJobId(orgStructureId=None, date=date, orgStructureIdList=orgStructureIdList)
        if jobId:
            result = self.createExceedJobTicket(jobId)
        return result


    def getJobId(self, orgStructureId, date, orgStructureIdList=[]):
        if date:
            db = QtGui.qApp.db
            table = db.table('Job')
            cond = [table['deleted'].eq(0),
                    table['jobType_id'].eq(self.jobTypeId),
                    table['date'].eq(date),
                    ]
            if orgStructureId:
                cond.append(table['orgStructure_id'].eq(orgStructureId))
            if orgStructureIdList:
                cond.append(table['orgStructure_id'].inlist(orgStructureIdList))
            record = db.getRecordEx(table, 'id', cond)
            if record:
                return forceRef(record.value('id'))
        return None


    def getJobIdForSelect(self, date=None):
        return getJobId(self.jobTypeId, date or self.courseDate, additionalCond=self.getJobPurposeConditions())


    def getJobPurposeConditions(self):
        cond = []
        db = QtGui.qApp.db
        orgStructureId = self.execOrgStructureId if self.execOrgStructureId else QtGui.qApp.currentOrgStructureId()
        jobPurposeIdList = self.selectJobPurposeIdList(self.clientId, self.eventTypeId, orgStructureId, True, self.actionTypeId, isFreeJobTicket=self.isFreeJobTicket)
        cond.append(db.joinOr([self.tableJob['jobPurpose_id'].isNull(),
                               self.tableJob['jobPurpose_id'].inlist(jobPurposeIdList)]))
        if orgStructureId:
            if not self.execOrgStructureId:
                orgStructureId = getSolitaryOrgStructureId(orgStructureId)
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            cond.append(db.joinOr([self.tableJob['orgStructure_id'].inlist(orgStructureIdList),
                                   self.tableJob['jobPurpose_id'].isNotNull(),
                                   ]
                                  )
                        )
        return cond


    @staticmethod
    def selectJobPurposeIdList(clientId, eventTypeId, orgStructureId, forAuto, actionTypeId=None, isFreeJobTicket=False):
        db = QtGui.qApp.db
        tableJobPurposePractice = db.table('rbJobPurpose_Practice')

        if clientId:
            clientRecord = db.getRecord('Client', ('sex', 'birthDate'), clientId)
            clientSex = forceInt(clientRecord.value('sex'))
            clientBirthDate = forceDate(clientRecord.value('birthDate'))
            cond = 'isSexAndAgeSuitable(%d, %s, rbJobPurpose.sex, rbJobPurpose.age, CURRENT_DATE())' \
                   % (
                       clientSex,
                       db.formatDate(clientBirthDate)
                   )
        else:
            cond = db.joinAnd(['rbJobPurpose.sex=0', 'rbJobPurpose.age=\'\''])

        if actionTypeId:
            actionTypeGroupIdList = db.getTheseAndParents('ActionType', 'group_id', [actionTypeId])
            if actionTypeGroupIdList:
                actionTypeSubCond = db.joinOr([tableJobPurposePractice['actionType_id'].isNull(),
                                               tableJobPurposePractice['actionType_id'].inlist(actionTypeGroupIdList)])
            else:
                actionTypeSubCond = tableJobPurposePractice['actionType_id'].isNull()
        else:
            actionTypeSubCond = tableJobPurposePractice['actionType_id'].isNull()
        actionTypeSubCond = db.joinXor([actionTypeSubCond, tableJobPurposePractice['excludeActionType'].ne(0)])

        if orgStructureId:
            orgStructureIdList = db.getTheseAndParents('OrgStructure', 'parent_id', [orgStructureId])
            orgStructureSubCond = db.joinOr([tableJobPurposePractice['orgStructure_id'].isNull(),
                                             tableJobPurposePractice['orgStructure_id'].inlist(orgStructureIdList),
                                             ]
                                            )
        else:
            orgStructureSubCond = '1'
        orgStructureSubCond = db.joinXor([orgStructureSubCond,
                                          tableJobPurposePractice['excludeOrgStructure'].ne(0)
                                          ]
                                         )
        if eventTypeId:
            eventTypeSubCond = db.joinOr([tableJobPurposePractice['eventType_id'].isNull(),
                                          tableJobPurposePractice['eventType_id'].eq(eventTypeId)
                                          ]
                                         )
        else:
            eventTypeSubCond = tableJobPurposePractice['eventType_id'].isNull()
        eventTypeSubCond = db.joinXor([eventTypeSubCond,
                                       tableJobPurposePractice['excludeEventType'].ne(0)
                                       ]
                                      )
        if forAuto and not isFreeJobTicket:
            availSubCond = tableJobPurposePractice['avail'].eq(2)
        else:
            availSubCond = tableJobPurposePractice['avail'].ne(0)

        practiceCond = db.joinAnd([actionTypeSubCond,
                                   orgStructureSubCond,
                                   eventTypeSubCond,
                                   availSubCond,
                                   ]
                                  )

        stmt = u'SELECT DISTINCT rbJobPurpose.id' \
               u' FROM rbJobPurpose' \
               u' LEFT JOIN rbJobPurpose_Practice ON rbJobPurpose_Practice.master_id = rbJobPurpose.id' \
               u' WHERE %(cond)s' \
               u' GROUP BY rbJobPurpose.id, rbJobPurpose_Practice.grouping' \
               u' HAVING SUM(%(practiceCond)s OR rbJobPurpose_Practice.id IS NULL) = COUNT(rbJobPurpose.id)' \
               % {'cond': cond,
                  'practiceCond': practiceCond
                  }

        query = db.query(stmt)
        result = []
        while query.next():
            result.append(query.value(0).toInt()[0])
        return result


    def getJobTciketCondByDate(self, date):
        if isinstance(date, (tuple, list)):
            def condGetter(datesRange):
                beg, end = datesRange
                return QtGui.qApp.db.joinAnd([self.tableJobTicket['datetime'].ge(beg),
                                              self.tableJobTicket['datetime'].le(end)])
        elif isinstance(date, (QDate, datetime.date)):
            condGetter = self.tableJobTicket['datetime'].dateEq
        elif self.isNearestJobTicket:
            if self.isJobTicketLe:
                return QtGui.qApp.db.joinAnd([self.tableJobTicket['datetime'].le(date),
                                              self.tableJobTicket['datetime'].dateEq(date)])
            else:
                return QtGui.qApp.db.joinAnd([self.tableJobTicket['datetime'].ge(date),
                                              self.tableJobTicket['datetime'].dateEq(date)])
        else:
            condGetter = self.tableJobTicket['datetime'].eq
        return condGetter(date)


    def _getMainQueryTable(self, joinType):
        def join(queryTable, table, cond):
            return getattr(queryTable, joinType)(table, cond)

        queryTable = self.tableJobTicket
        queryTable = join(queryTable, self.tableActionPropertyJobTicket,
                          self.tableActionPropertyJobTicket['value'].eq(self.tableJobTicket['id']))
        queryTable = join(queryTable, self.tableActionProperty,
                          [self.tableActionProperty['id'].eq(self.tableActionPropertyJobTicket['id']),
                           self.tableActionProperty['deleted'].eq(0)])
        queryTable = join(queryTable, self.tableAction,
                          [self.tableAction['id'].eq(self.tableActionProperty['action_id']),
                           self.tableAction['deleted'].eq(0)])
        queryTable = join(queryTable, self.tableEvent,
                          [self.tableEvent['id'].eq(self.tableAction['event_id']),
                           self.tableEvent['deleted'].eq(0)])
        queryTable = join(queryTable, self.tableJob, self.tableJob['id'].eq(self.tableJobTicket['master_id']))

        return queryTable


    def _orderByJobOrgStructure(self, orderBy):
        jobOrgStructureIdList = self.jobOrgStructureIdList
        if not jobOrgStructureIdList:
            jobOrgStructureIdList = [self.execOrgStructureId if self.execOrgStructureId else QtGui.qApp.currentOrgStructureId()]
        if not jobOrgStructureIdList:
            return orderBy

        # Here it is important list order because the first value has the most big weight in select
        caseList = ['CASE'] \
            + [' WHEN %s THEN %s ' % (self.tableJob['orgStructure_id'].eq(orgStructure_id), weight)
               for weight, orgStructure_id in enumerate(jobOrgStructureIdList)] \
            + ['ELSE %s END' % len(jobOrgStructureIdList)]

        orderBy.insert(0, ''.join(caseList))

        return orderBy


    def tryReservePartByPart(self, queryTable, cond, order):
        # Я считаю, что вытягивать в данном случае все-все свободные номерки - это излишество.
        # Если паралельно кто-то еще назначет номерок по схожим условиям, выборка из 10 номерков это достаточно,
        # не думаю что нагрузка очень уж большая. В случае чего сделаем еще один запрос.
        # Предполагаю, что так будет быстрее.

        db = QtGui.qApp.db

        todo = True
        invalidIds = []
        while todo:
            cond = list(cond) if isinstance(cond, (list, tuple)) else [cond]
            if invalidIds:
                cond.append(self.tableJobTicket['id'].notInlist(invalidIds))
            jobTicketIdList = db.getIdList(queryTable, self.tableJobTicket['id'].name(),
                                           cond, order=order, limit=10)
            for jobTicketId in jobTicketIdList:
                if QtGui.qApp.addJobTicketReservation(jobTicketId):
                    return jobTicketId
                else:
                    invalidIds.append(jobTicketId)
            # Будем пытаться делать запросы, пока выборка не окажется пустой.
            todo = bool(jobTicketIdList)
        return None


    def selectUsedJobTicket(self, date=None):
        db = QtGui.qApp.db

        queryTable = self._getMainQueryTable('innerJoin')

        cond = [self.tableJob['jobType_id'].eq(self.jobTypeId),
                self.tableJobTicket['deleted'].eq(0),
                self.tableJobTicket['endDateTime'].isNull(),
                self.tableEvent['client_id'].eq(self.clientId),
                self.tableJobTicket['status'].inlist([CJobTicketStatus.wait,
                                                      CJobTicketStatus.enqueued,
                                                      CJobTicketStatus.doing]),
                self.tableJobTicket['masterJobTicket_id'].isNull()]

        order = self._orderByJobOrgStructure([self.tableJobTicket['datetime'].name() + u' DESC'] if self.isOrderDESC else [self.tableJobTicket['datetime'].name()])

        if date:
            dateTimeCond = self.getJobTciketCondByDate(date)
        elif self.actionDate:
            if self.ticketDuration > 1:
                dateTimeCond = db.joinOr(
                    [db.joinAnd(['DATE(' + self.tableJobTicket['datetime'].name() + ') < CURRENT_DATE()',
                                 'DATE(' + self.tableJobTicket['datetime'].dateAddDay(self.ticketDuration).name() + ') >= CURRENT_DATE()']),
                     'DATE(' + self.tableJobTicket['datetime'].name() + ') > CURRENT_DATE()'
                ])
            else:
                dateTimeCond = 'DATE(' + self.tableJobTicket['datetime'].name() + ') >= CURRENT_DATE()'
        else:
            duration = forceInt(db.translate('rbJobType', 'id', self.jobTypeId, 'ticketDuration'))
            if duration > 1:
                dateTimeCond = db.joinOr(
                    [db.joinAnd(['DATE(' + self.tableJobTicket['datetime'].name() + ') < CURRENT_DATE()',
                                 'DATE(' + self.tableJobTicket['datetime'].dateAddDay(duration).name() + ') >= CURRENT_DATE()']),
                     'DATE(' + self.tableJobTicket['datetime'].name() + ') > CURRENT_DATE()'
                ])

            else:
                dateTimeCond = 'DATE(' + self.tableJobTicket['datetime'].name() + ') >= CURRENT_DATE()'

        cond.append(dateTimeCond)

        return self.tryReservePartByPart(queryTable, cond, order)

        # jobTicketIdList = db.getDistinctIdList(
        #     queryTable, self.tableJobTicket['id'].name(), cond, order=order
        # )
        # return self.getReservedJobTicketId(jobTicketIdList)


    def selectFreeJobTicket(self, jobId=None, date=None):
        # ищем среди свободных
        forDays = date or self.forDays

        db = QtGui.qApp.db

        queryTable = self._getMainQueryTable('leftJoin')

        if jobId:
            dateTimeCond = db.joinAnd(['Job_Ticket.`datetime` >= NOW()', self.tableJob['id'].eq(jobId)])

        # datetime.datetime наследник от datetime.date.
        # tuple, list - это для назначений, там возможно планирвоание времени номерка до минут, без секунд.
        # В таком случае будем сюда присылать диапозон нужной минуты.
        elif isinstance(forDays, (QDate, QDateTime, datetime.date, tuple, list)):
            dateTimeCond = self.getJobTciketCondByDate(forDays)
        elif forDays == TODAY:
            dateTimeCond = 'DATE(' + self.tableJobTicket['datetime'].name() + ') = CURRENT_DATE()'
        elif forDays == TODAYTIME:
            dateTimeCond = db.joinAnd(['DATE(' + self.tableJobTicket['datetime'].name() + ') = CURRENT_DATE()',
                                       self.tableJobTicket['datetime'].name() + ' >= NOW()'])
        elif forDays == ANYDAY:
            dateTimeCond = self.tableJobTicket['datetime'].name() + ' > NOW()'
        elif forDays == ANYNEXTDAY:
            countDays = self.countDays if self.countDays else 1
            dateTimeCond = 'DATE(' + self.tableJobTicket['datetime'].name() + ') > (CURRENT_DATE() + INTERVAL %d DAY)'%(countDays)
        else:
            dateTimeCond = '0'

        cond = [self.tableJob['deleted'].eq(0),
                self.tableJobTicket['deleted'].eq(0),
                self.tableJob['jobType_id'].eq(self.jobTypeId),
                self.tableJobTicket['status'].eq(CJobTicketStatus.wait),
                dateTimeCond,
                self.tableAction['id'].isNull(),
                self.tableActionPropertyJobTicket['id'].isNull(),
                'NOT isReservedJobTicket(Job_Ticket.id)',
                self.tableJobTicket['isExceedQuantity'].eq(0)
                ]
        if QtGui.qApp.checkGlobalPreference(u'23:uniqJobTickets', u'да'):
            cond.append(self.tableJobTicket['id'].notInlist(QtGui.qApp.getReservedJobTickets()))

        order = self._orderByJobOrgStructure([self.tableJobTicket['datetime'].name() + u' DESC'] if self.isOrderDESC else [self.tableJobTicket['datetime'].name()])

        if jobId is None:
            if self.isFreeJobTicket:
                orgStructureId = self.execOrgStructureId if self.execOrgStructureId else QtGui.qApp.currentOrgStructureId()
                if self.execJobPurposeId:
                    cond.append(self.tableJob['jobPurpose_id'].eq(self.execJobPurposeId))
                else:
                    cond.append(self.tableJob['jobPurpose_id'].isNull())
                if orgStructureId:
                    cond.append(db.joinOr([self.tableJob['orgStructure_id'].eq(orgStructureId),
                                           self.tableJob['jobPurpose_id'].isNotNull()]))
                else:
                    cond.append(db.joinOr([self.tableJob['orgStructure_id'].isNull(),
                                           self.tableJob['jobPurpose_id'].isNotNull()]))
            else:
                cond.extend(self.getJobPurposeConditions())

        return self.tryReservePartByPart(queryTable, cond, order)

        # jobTicketIdList = db.getIdList(queryTable,
        #                                self.tableJobTicket['id'].name(),
        #                                cond,
        #                                order=order
        #                                )
        # return self.getReservedJobTicketId(jobTicketIdList)


    def createExceedJobTicket(self, jobId):
        return createExceedJobTicket(jobId, self.tableJobTicket)


    def getReservedJobTicketId(self, jobTicketIdList):
        for jobTicketId in jobTicketIdList:
            if QtGui.qApp.addJobTicketReservation(jobTicketId):
                return jobTicketId
        return None

# ######################################################
# Функции используемые отдельно

def createExceedJobTicket(jobId, tableJobTicket=None):
    return forceRef(createNewExceedJobTicketRecord(jobId, tableJobTicket).value('id'))


def createNewExceedJobTicketRecord(jobId, tableJobTicket=None, storeIdx=True):
    db = QtGui.qApp.db

    tableJobTicket = tableJobTicket or db.table('Job_Ticket')

    date = forceDateTime(QtGui.qApp.db.translate('Job', 'id', jobId, 'date'))
    newRecord = tableJobTicket.newRecord()
    newRecord.setValue('master_id', jobId)
    newRecord.setValue('datetime', date)
    newRecord.setValue('status', CJobTicketStatus.wait)
    newRecord.setValue('isExceedQuantity', 1)
    result = db.insertRecord(tableJobTicket, newRecord)

    minId = forceRef(db.translate(tableJobTicket, 'master_id', jobId, 'min(id)'))
    if storeIdx:
        newRecord = tableJobTicket.newRecord(['id', 'idx'])
    newRecord.setValue('id', result)
    newRecord.setValue('idx', result - minId)
    if storeIdx:
        db.updateRecord(tableJobTicket, newRecord)
    return newRecord


def getJobId(jobTypeId, date, orgStructureId=None, additionalCond=None, clientId=None):
    db = QtGui.qApp.db
    table = db.table('Job')
    cond = [table['deleted'].eq(0),
            table['jobType_id'].eq(jobTypeId),
            table['date'].dateEq(date),
            ]
    queryTable = table
    if orgStructureId:
        cond.append(table['orgStructure_id'].eq(orgStructureId))
    if clientId:
        clientRecord = db.getRecord('Client', ('sex', 'birthDate'), clientId)
        clientSex = forceInt(clientRecord.value('sex'))
        clientBirthDate = forceDate(clientRecord.value('birthDate'))
        tableRBJobPurpose = db.table('rbJobPurpose')
        cond.append(u'isSexAndAgeSuitable(%d, %s, rbJobPurpose.sex, rbJobPurpose.age, CURRENT_DATE())' % (clientSex, db.formatDate(clientBirthDate)))
        queryTable = queryTable.leftJoin(tableRBJobPurpose, tableRBJobPurpose['id'].eq(table['jobPurpose_id']))
    if additionalCond:
        cond.extend(additionalCond)
    record = db.getRecordEx(queryTable, [table['id']], cond)
    if record:
        return forceRef(record.value('id'))
    return None

