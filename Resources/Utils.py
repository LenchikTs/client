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
from PyQt4.QtCore import QDate

from library.Utils import forceInt, forceRef, forceDate
from Resources.NextDateExecutionPlanDialog import CNextDateExecutionPlanDialog

TreatmentScheduleMinimumDuration = 300

def getNextDateExecutionPlan(widget, jobTicketId, prevActionDate, executionPlan, lastAction, nextExecutionPlanItem):
    jobData = [None, None, None]
    if not prevActionDate or not executionPlan or not lastAction:
        return None, jobData
    record = lastAction.getRecord()
    quantity = forceInt(record.value('quantity'))
    periodicity = forceInt(record.value('periodicity'))
    actionTypeId = forceRef(record.value('actionType_id'))
    actionType = lastAction.getType()
    db = QtGui.qApp.db
    tableJobTypeAT = db.table('rbJobType_ActionType')
    jobTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['master_id']], [tableJobTypeAT['actionType_id'].eq(actionTypeId)])
    isJobTicket = (jobTypeIdList or actionType._hasJobTicketPropertyType)
    if not actionType.isNomenclatureExpense:
        if (jobTypeIdList or actionType._hasJobTicketPropertyType) and quantity:
            db = QtGui.qApp.db
            tableJob = db.table('Job')
            tableJobTicket = db.table('Job_Ticket')
            for property in lastAction._propertiesById.itervalues():
                if property.type().isJobTicketValueType() and property.getValue():
                    jobTicketId = property.getValue()
                    if jobTicketId:
                        break
            if not jobTicketId:
                jobTicketId = lastAction.getFreeJobTicketCourseId()
            if not jobTicketId:
                return None, jobData
            recordJT = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['id'].eq(jobTicketId), tableJobTicket['deleted'].eq(0)])
            if recordJT:
                jobId = forceRef(recordJT.value('master_id'))
                if not jobId:
                    return None, jobData
            recordJ = db.getRecordEx(tableJob, '*', [tableJob['id'].eq(jobId), tableJob['deleted'].eq(0)])
            if recordJ:
                jobTicketDate = forceDate(recordJ.value('date'))
                jobTicketOrgStructureId = forceRef(recordJ.value('orgStructure_id'))
                jobTypeId = forceRef(recordJ.value('jobType_id'))
                if not jobTicketDate or not jobTicketOrgStructureId or not jobTypeId:
                    return None, jobData
                jobPurposeId = forceRef(recordJ.value('jobPurpose_id'))
                tableJob = db.table('Job')
                nextDate = prevActionDate.addDays(periodicity+1)
                cond = [tableJob['jobType_id'].eq(jobTypeId),
                        tableJob['jobPurpose_id'].eq(jobPurposeId),
                        tableJob['date'].dateGe(nextDate),
                        tableJob['deleted'].eq(0),
                        tableJob['orgStructure_id'].eq(jobTicketOrgStructureId)
                        ]
                recordNextJob = db.getRecordEx(tableJob, tableJob['date'].name(), cond, order = tableJob['date'].name())
                nextPlanDate = forceDate(recordNextJob.value('date')) if recordNextJob else QDate()
                jobData = [jobTypeId, jobPurposeId, jobTicketOrgStructureId]
                nextPlanDate = getNextDateExecutionPlanDialog(widget, jobTicketId, prevActionDate, executionPlan, lastAction, isJobTicket, nextPlanDate, jobData, nextExecutionPlanItem)
                if not nextPlanDate:
                    return None, jobData
                executionPlan, nextExecutionPlanItem = setExecutionPlanDate(executionPlan, nextExecutionPlanItem, nextPlanDate)
                return nextPlanDate, jobData
        elif (not jobTypeIdList and not actionType._hasJobTicketPropertyType) and quantity:
            begDate = forceDate(record.value('begDate'))
            if not begDate:
                return None, jobData
            nextDate = begDate.addDays(periodicity+1)
            scheduleWeekendDays = executionPlan.scheduleWeekendDays.split(',') if executionPlan else []
            if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is None or (scheduleWeekendDays and nextDate.dayOfWeek() not in scheduleWeekendDays)):
                nextDate = getNextDateExecutionPlanDialog(widget, jobTicketId, prevActionDate, executionPlan, lastAction, isJobTicket, nextDate, jobData, nextExecutionPlanItem)
                executionPlan, nextExecutionPlanItem = setExecutionPlanDate(executionPlan, nextExecutionPlanItem, nextDate)
                return nextDate, jobData
            while (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is not None or (scheduleWeekendDays and nextDate.dayOfWeek() in scheduleWeekendDays)):
                nextDate = nextDate.addDays(1)
            nextDate = getNextDateExecutionPlanDialog(widget, jobTicketId, prevActionDate, executionPlan, lastAction, isJobTicket, nextDate, jobData, nextExecutionPlanItem)
            executionPlan, nextExecutionPlanItem = setExecutionPlanDate(executionPlan, nextExecutionPlanItem, nextDate)
            return nextDate, jobData
    return None, jobData


def getNextDateExecutionPlanDialog(widget, jobTicketId, prevActionDate, executionPlan, lastAction, isJobTicket, planDate, jobData, nextExecutionPlanItem):
    nextPlanDate = QDate()
    if isJobTicket is not None:
        dialog = CNextDateExecutionPlanDialog(widget, [planDate], isJobTicket=isJobTicket)
        try:
            dialog.setJobData(jobTicketId, prevActionDate, executionPlan, lastAction, jobData, nextExecutionPlanItem)
            if dialog.exec_():
                nextPlanDate = dialog.getDate()
        finally:
                dialog.deleteLater()
    return nextPlanDate


def setExecutionPlanDate(executionPlan, nextExecutionPlanItem, newDate):
    if not newDate or not executionPlan:
        return None, None
    items = executionPlan.items
    sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
    aliquoticityIdx = -1
    for idx, item in enumerate(sortedItemsByDate):
        if not item.date:
            aliquoticityIdx = item.aliquoticityIdx
            break
    if aliquoticityIdx >= 0:
        for idx, item in enumerate(sortedItemsByDate):
            if item.aliquoticityIdx == aliquoticityIdx:
                item.date = newDate
    sortedItemsByDate = sorted(sortedItemsByDate, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
    executionPlan.items = sortedItemsByDate
    executionPlan.items._remapIdx()
    executionPlan.items._remap()
    nextExecutionPlanItem.executionPlan = executionPlan
    return executionPlan, nextExecutionPlanItem
