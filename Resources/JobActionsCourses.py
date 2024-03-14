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
import datetime

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QDate

from Events.Action          import CAction
from Resources.CourseStatus import CCourseStatus
from library.Utils          import forceRef, forceInt, forceDate, forceDateTime, toVariant
from Resources.Utils        import getNextDateExecutionPlan


class AddingInfo(object):
    def __init__(self, addingDate, duration, amount, financeId, contractId, directionDate, quantity, nextExecutionPlanItem=None, jobTicketOrgStructureId=None):
        self.addingDate = addingDate
        self.duration = duration
        self.amount = amount
        self.financeId = financeId
        self.contractId = contractId
        self.directionDate = directionDate
        self.quantity = quantity
        self.nextExecutionPlanItem = nextExecutionPlanItem
        self.jobTicketOrgStructureId = jobTicketOrgStructureId


class CJobActionsCoursesMixin(object):
    """
    Класс наследник должен обладать интерфейсом:
    getClientId() - возвращает идентификатор клиента, чьи курсовые назначения мы анализируем

    Иметь свойство _jobTypeActionsAddingHelper <CJobTypeActionsAddingHelper>
    """


    def getClientId(self):
        """
        Обязательно переопределим в наследнике
        """
        raise NotImplementedError


    def _getLoadedActions(self):
        """
        Переопределим в наследнике по необходимости
        :return list<CAction>
        """
        return []


    def _getLoadedEventIdList(self):
        """
        Переопределим в наследнике по необходимости
        :return list<int>
        """
        return []
    #
    #
    # def _checkJobActionsExecutionPlan2(self, jobTicketId):
    #     """
    #     В рамках одного события могут проходить несколько курсов. Теоретически.
    #     Или с одной работой могут быть связаны обычные действия и действие из курса
    #     и они будут из разных событий.
    #     И только один курс по типу действия в событии
    #     """
    #
    #     db = QtGui.qApp.db
    #
    #     loadedActionList = self._getLoadedActions()
    #     eventIdList = self._getLoadedEventIdList()
    #     actionIdList = []
    #     # courses - dict[(courseMasterId, actionTypeId)] -> dict[actionBegDate] -> actionList<CAction>
    #     courses = {}
    #
    #     # Теперь соберем все основываясь на планах
    #     tableAction = db.table('Action')
    #     tableEvent = db.table('Event')
    #     tableActionExecutionPlan = db.table('Action_ExecutionPlan')
    #     queryTable = tableActionExecutionPlan.innerJoin(tableAction,
    #                                                     tableAction['id'].eq(tableActionExecutionPlan['action_id']))
    #     queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
    #
    #     cond = [tableAction['deleted'].eq(0),
    #             tableEvent['deleted'].eq(0),
    #             tableActionExecutionPlan['action_id'].inlist([forceRef(action.getRecord().value('id'))
    #                                                           for action in loadedActionList])]
    #
    #     # Отсортируем по типу действия, при этом первая запись среди одинаковых типов действий будет началом курса.
    #     # Дальше все сортируется по времени
    #     order = [tableAction['actionType_id'].name(),
    #              '%s DESC' % tableActionExecutionPlan['master_id'].eq(tableActionExecutionPlan['action_id']),
    #              tableActionExecutionPlan['execDate'].name()]


    def _checkJobActionsExecutionPlan(self, jobTicketId, execCourse=CCourseStatus.proceed):
        """
        В рамках одного события могут проходить несколько курсов. Теоретически.
        Или с одной работой могут быть связаны обычные действия и действие из курса
        и они будут из разных событий.
        Но один курс проходит в рамках одного события
        И только один курс по типу действия в событии
        """

        db = QtGui.qApp.db

        loadedActionList = self._getLoadedActions()
        eventIdList = self._getLoadedEventIdList()
        actionIdList = []
        # courses - dict[(eventId, actionTypeId)] -> dict[actionBegDate] -> actionList<CAction>
        courses = {}

        # Сгруппируем курсовые назначения
        for action in loadedActionList:
            self._groupActions(courses, actionIdList, eventIdList, action=action, execCourse=execCourse)

        # Теперь соберем все остальные действия связанные с курсами
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableEvent = db.table('Event')
        queryTable, cond = self._getMainQueryTableAndCond()
        cond.extend([#tableAPJT['value'].isNotNull(),
                     db.joinOr([tableAPJT['value'].ne(jobTicketId), tableAPJT['value'].isNull()]),
                     tableAction['event_id'].inlist(eventIdList),
                     tableAction['id'].notInlist(actionIdList),
                     tableActionType['deleted'].eq(0),
                     tableEvent['client_id'].eq(self.getClientId())])
        cond.append(db.joinOr([db.joinAnd([tableActionType['isNomenclatureExpense'].eq(1), tableAction['duration'].gt(0)]),
                    db.joinAnd([tableActionType['isNomenclatureExpense'].eq(0), tableAction['quantity'].gt(0)])]))
        query = db.query(db.selectStmt(queryTable, 'Action.*', cond, order=tableAction['id'].name()))
        # Сгруппируем курсовые назначения
        while query.next():
            self._groupActions(courses, actionIdList, eventIdList, record=query.record(), execCourse=execCourse)

        for (eventId, actionTypeId), courseData in courses.items():
            addingInfo = self._getNewCourseActionInfo(eventId, actionTypeId, courseData, jobTicketId=jobTicketId)
            if addingInfo is None:
                continue
            self.addNewCourseAction(addingInfo, eventId, actionTypeId, courseData=courseData)


    def _getNewCourseActionInfo(self, eventId, actionTypeId, courseData, jobTicketId=None):
        result = None
        nextExecutionPlanItem = None
        jobTicketOrgStructureId = None
        currentDate = QtCore.QDate.currentDate()
        sortedDates = sorted(courseData.keys())
        startDate = sortedDates[0]
        startDayData = courseData[startDate]
        startAction = self._getStartAction(startDayData, idx=0)
        startRecord = startAction.getRecord()
        aliquoticity = forceInt(startRecord.value('aliquoticity'))
        duration = forceInt(startRecord.value('duration')) or 1
        amount = forceInt(startRecord.value('amount'))
        financeId = forceRef(startRecord.value('finance_id'))
        contractId = forceRef(startRecord.value('contract_d'))
        directionDate = forceDateTime(startRecord.value('directionDate'))
        executionPlan = startAction.getExecutionPlan()
        if not executionPlan:
            return QtCore.QDate()
        executionPlanKeys = executionPlan.items._mapDateToItems.keys()
        executionPlanKeys.sort()
        executionPlanDateList = []
        for executionPlanKey in executionPlanKeys:
            if len(executionPlanKey) > 0 and bool(QDate(executionPlanKey[0],executionPlanKey[1],executionPlanKey[2])):
                executionPlanDateList.append(executionPlanKey)
#        for row, executionPlanKey in enumerate(executionPlanKeys):
#            if len(executionPlanKey) > 0 and not bool(QDate(executionPlanKey[0],executionPlanKey[1],executionPlanKey[2])):
#                executionPlanDateList.append(executionPlanKey)
        for item in executionPlan.items:
            if not bool(item.date):
                year = item.date.year()
                month = item.date.month()
                day = item.date.day()
                executionPlanDateList.insert(item.aliquoticityIdx, (year, month, day))
        lastDate = sortedDates[-1]
        tempDate = QDate(lastDate)
        findDate = (tempDate.year(), tempDate.month(), tempDate.day())
        if findDate in executionPlan.items._mapDateToItems.keys():
            planDayTimes = []
            executionPlanItems = executionPlan.items.getItemsByDate(QDate(findDate[0],findDate[1],findDate[2]))
            lastDayData = courseData[lastDate]
            lastAction = self._getStartAction(lastDayData, idx=(len(lastDayData)-1))
            if lastAction:
                lastAction.executionPlanManager.setCurrentItemIndex(lastAction.executionPlanManager.executionPlan.items.index(lastAction.executionPlanManager._currentItem))
                nextExecutionPlanItem = lastAction.executionPlanManager.getNextItem()
                lastAction.executionPlanManager.setCurrentItemExecuted()
                quantity = forceInt(lastAction.getRecord().value('quantity'))
            for planItem in executionPlanItems:
                planDayTimes.append(planItem.time)
            planDayTimes = sorted(planDayTimes)
            planDayCount = self._getPlanDayCount(planDayTimes, aliquoticity)
            doneDayCount = len(courseData[lastDate])
            if doneDayCount < planDayCount:
                # У нас на день lastDate еще есть запланированные направления
                if doneDayCount < len(planDayTimes) and self._checkPlanTime(planDayTimes[doneDayCount]):
                    # У нас есть запланированное конкретное время
                    result = QtCore.QDateTime(lastDate)
                    result.setTime(planDayTimes[doneDayCount])
                else:
                    # У нас не запланировано конкретное время
                    result = QtCore.QDate(lastDate)
            else:
                # У нас на день lastDate больше нет запланированных направлений
                # Ищем последующий запланированный день
                for row, executionPlanDate in enumerate(executionPlanDateList):
                    if not QDate(executionPlanDate[0],executionPlanDate[1],executionPlanDate[2]) and not lastAction.getType().isNomenclatureExpense:
                        nextPlanDate, jobData = getNextDateExecutionPlan(self, jobTicketId, tempDate, executionPlan, lastAction, nextExecutionPlanItem)
                        jobTicketOrgStructureId = jobData[2] if len(jobData) >= 3 else None
                        if not nextPlanDate:
                            return nextPlanDate and AddingInfo(nextPlanDate, duration, amount, financeId, contractId, directionDate, quantity=quantity, nextExecutionPlanItem=None, jobTicketOrgStructureId=jobTicketOrgStructureId)
                        executionDate = datetime.date(nextPlanDate.year(), nextPlanDate.month(), nextPlanDate.day())
                        result = QtCore.QDate(executionDate)
                        for prevActions in courseData.values():
                            for prevAction in prevActions:
                                if prevAction and prevAction.executionPlanManager:
                                    prevAction.executionPlanManager.setExecutionPlan(executionPlan)
                    else:
                        executionDate = datetime.date(executionPlanDate[0],executionPlanDate[1],executionPlanDate[2])
                        if not lastAction.getType().isNomenclatureExpense:
                            if not jobTicketId:
                                jobTicketId = lastAction.getFreeJobTicketCourseId()
                                if jobTicketId:
                                    db = QtGui.qApp.db
                                    tableJob = db.table('Job')
                                    tableJobTicket = db.table('Job_Ticket')
                                    recordJT = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['id'].eq(jobTicketId), tableJobTicket['deleted'].eq(0)])
                                    jobId = forceRef(recordJT.value('master_id')) if recordJT else None
                                    if jobId:
                                        recordJ = db.getRecordEx(tableJob, '*', [tableJob['id'].eq(jobId), tableJob['deleted'].eq(0)])
                                        jobTicketOrgStructureId = forceRef(recordJ.value('orgStructure_id')) if recordJ else None
                    # Так же мы проверим не просрочили ли мы день.
                    if executionDate > lastDate and QtCore.QDate(executionDate) >= currentDate:
                        planDayTimes = []
                        executionPlanItems = executionPlan.items.getItemsByDate(QDate(executionDate))
                        for planItem in executionPlanItems:
                            planDayTimes.append(planItem.time)
                        if len(planDayTimes) and self._checkPlanTime(planDayTimes[0]):
                            # У нас есть запланированное конкретное время
                            result = QtCore.QDateTime(executionDate)
                            result.setTime(planDayTimes[0])
                        else:
                            # У нас не запланировано конкретное время
                            result = QtCore.QDate(executionDate)
                        break

        return result and AddingInfo(result, duration, amount, financeId, contractId, directionDate, quantity=quantity-(1 if quantity > 0 else 0), nextExecutionPlanItem=nextExecutionPlanItem, jobTicketOrgStructureId=jobTicketOrgStructureId)


    def _getStartAction(self, actionList, idx=0):
        return sorted(actionList, key=lambda action: action.getRecord().value('id').toInt()[0])[idx]


    def _getPlanDayCount(self, timesList, aliquoticity):
        # По хорошому, для корректной работы по такому алгоритму,
        # в таблице Action_ExecutionPlan Дату и время бы разделить в разные поля.
        # Так как в случае когда у нас не указаны в F2 из F9 конкретные времена назначений,
        # у нас получается одна запись со временем QTime(0, 0). А это для нас опасно,
        # Хорошо что хоть номерков на это время не планируют.

        timesListLen = len(timesList)
        if timesListLen == 1:
            if not self._checkPlanTime(timesList[0]):
                return aliquoticity or 1
        return timesListLen or 1


    def _checkPlanTime(self, time, zeroTime=QtCore.QTime(0, 0)):
        # По хорошому, для корректной работы по такому алгоритму,
        # в таблице Action_ExecutionPlan Дату и время бы разделить в разные поля.
        # Но пока предположим что время QTime(0, 0) - не валидное,
        # в полночь работы не выполняем

        return time and time.isValid() and time != zeroTime


    def addNewCourseAction(self, addingInfo, eventId, actionTypeId, courseData=None):
        # Ввиду того, что у нас связанность действий и событий,
        # нам никаких дополнительных блокировок брать не нужно.
        # По крайней мере в единственном сейчас случае использования в редакторе работы.

        # Чтобы выполнение ниже следующего когда не поламало случайно что-нибудь сохраним
        # созданное ранее helper-ом, а потом обязательно возвернем назад
        oldEventEditor = getattr(self, 'eventEditor', None)
        oldActionTemplateCache = getattr(self, 'actionTemplateCache', None)
        QtGui.qApp.setJTR(self)
        try:
            self._jobTypeActionsAddingHelper.creatEventPossibilities(eventId)
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            record = tableAction.newRecord()
            newAction = CAction.getFilledAction(self.eventEditor, record, actionTypeId, addingInfo.amount,
                                                addingInfo.financeId, addingInfo.contractId, initPresetValues=False)
            if addingInfo.nextExecutionPlanItem:
                newAction.setExecutionPlanItem(addingInfo.nextExecutionPlanItem)
                newAction.executionPlanManager.bindAction(newAction)
            record.setValue('duration', addingInfo.duration)
            record.setValue('quantity', addingInfo.quantity)
            record.setValue('event_id', eventId)
            record.setValue('directionDate', toVariant(addingInfo.directionDate))

            addingDate = addingInfo.addingDate
            record.setValue('begDate', forceDateTime(addingDate))
            if isinstance(addingInfo.addingDate, QtCore.QDate):
                presetValueDate, presetValueTime = addingDate, None
            elif isinstance(addingInfo.addingDate, QtCore.QDateTime):
                presetValueDate, presetValueTime = addingDate.date(), addingDate.time()
            else:
                presetValueDate, presetValueTime = None, None

            newAction.updatePresetValuesConditions({'courseDate': presetValueDate,
                                                    'courseTime': presetValueTime})
            execOrgStructureId = addingInfo.jobTicketOrgStructureId
            if addingDate and execOrgStructureId:
                for property in newAction.getType()._propertiesById.itervalues():
                    if property.isJobTicketValueType() and property.valueType.initPresetValue:
                        prop = newAction.getPropertyById(property.id)
                        if prop._type:
                            prop._type.valueType.setIsExceedJobTicket(True)
                            prop._type.valueType.setIsNearestJobTicket(True)
                            prop._type.valueType.setDateTimeExecJob(addingDate)
#                            prop._type.valueType.setExecOrgStructureId(execOrgStructureId)
            newAction.initPresetValues()
            newAction.finalFillingPlannedEndDate()
            newAction.save()
        finally:
            self.eventEditor = oldEventEditor
            self.actionTemplateCache = oldActionTemplateCache
            if newAction and not newAction.getType().isNomenclatureExpense:
                for prevActions in courseData.values():
                    for prevAction in prevActions:
                        actionType = prevAction.getType()
                        if not actionType.isNomenclatureExpense:
                            oldExecutionPlan = prevAction.getExecutionPlan()
                            if oldExecutionPlan and prevAction._executionPlanManager:
                                prevAction._executionPlanManager.save()
            QtGui.qApp.unsetJTR(self)


    @staticmethod
    def _groupActions(courses, actionIdList, eventIdList, action=None, record=None, execCourse=CCourseStatus.proceed):
        """
        Курсовые назначения имеют общее событие и один и тот же тип действия
        Группируем по датам для дальнейшего анализа курса.
        """

        action = action or CAction(record=record)
        record = record or action.getRecord()
        duration = forceInt(record.value('duration'))
        quantity = forceInt(record.value('quantity'))
        if duration < 1 and action.getType().isNomenclatureExpense:
            return
        elif not action.getType().isNomenclatureExpense and (quantity < 1 or execCourse in [CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]):
            return
        actionTypeId = forceRef(record.value('actionType_id'))
        eventId = forceRef(record.value('event_id'))
        actionId = forceRef(record.value('id'))
        eventId not in eventIdList and eventIdList.append(eventId)
        actionId not in actionIdList and actionIdList.append(actionId)
        dateKey = forceDate(record.value('begDate')).toPyDate()
        courseData = courses.setdefault((eventId, actionTypeId), {})
        courseData.setdefault(dateKey, []).append(action)


    def _getMainQueryTableAndCond(self):
        db = QtGui.qApp.db
        table = db.table('Job_Ticket')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableAP = db.table('ActionProperty')
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tablePerson = db.table('vrbPersonWithSpeciality')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')

        queryTable = table
        queryTable = queryTable.leftJoin(tableAPJT, tableAPJT['value'].eq(table['id']))
        queryTable = queryTable.leftJoin(tableAP, tableAP['id'].eq(tableAPJT['id']))
        queryTable = queryTable.leftJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
        queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
        queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))

        cond = [tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableClient['deleted'].eq(0)]

        return queryTable, cond

