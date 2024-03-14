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

from PyQt4              import QtGui
from PyQt4.QtCore       import pyqtSignature, QDate

from library.DialogBase import CDialogBase
from library.Utils      import forceString, forceDate, forceRef, forceInt

from Ui_NextDateExecutionPlanDialog     import Ui_NextDateExecutionPlanDialog


class CNextDateExecutionPlanDialog(CDialogBase, Ui_NextDateExecutionPlanDialog):
    def __init__(self, parent, jobDates=[], isJobTicket=False):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Выберите дату следующего шага курса')
        self.jobDates = jobDates
        self.isJobTicket = isJobTicket
        self.jobTicketId = None
        self.jobTypeId = None
        self.jobPurposeId = None
        self.jobTicketOrgStructureId = None
        self.prevActionDate = None
        self.executionPlan = None
        self.orgStructureIdList = []
        self.lastAction = None
        self.nextExecutionPlanItem = None
        self.jobData = [None, None, None]
        self.setOrgStructureVisible(False)
        self.setDateVisible(self.isJobTicket)


    def setOrgStructureIdList(self):
        currentOrgStructureId = QtGui.qApp.currentOrgStructureId()
        userOrgStructureId = QtGui.qApp.userOrgStructureId
        currentOrgStructureIdList = []
        userOrgStructureIdList = []
        db = QtGui.qApp.db
        tableOrgStructure = db.table('OrgStructure')
        if currentOrgStructureId:
            recordOS = db.getRecordEx(tableOrgStructure, [tableOrgStructure['parent_id']], [tableOrgStructure['id'].eq(currentOrgStructureId), tableOrgStructure['deleted'].eq(0)])
            parentOSId = forceRef(recordOS.value('parent_id')) if recordOS else None
            currentOrgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', parentOSId if parentOSId else currentOrgStructureId)
        if userOrgStructureId:
            recordOS = db.getRecordEx(tableOrgStructure, [tableOrgStructure['parent_id']], [tableOrgStructure['id'].eq(userOrgStructureId), tableOrgStructure['deleted'].eq(0)])
            parentOSId = forceRef(recordOS.value('parent_id')) if recordOS else None
            userOrgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', parentOSId if parentOSId else userOrgStructureId)
        self.orgStructureIdList = list(set(currentOrgStructureIdList)|set(userOrgStructureIdList))
        if self.orgStructureIdList:
            if self.jobTypeId and len(self.jobDates) > 0 and self.jobDates[0]:
                tableJob = db.table('Job')
                cond = [tableJob['jobType_id'].eq(self.jobTypeId),
                        #tableJob['jobPurpose_id'].eq(self.jobPurposeId),
                        tableJob['date'].dateGe(self.jobDates[0]),
                        tableJob['deleted'].eq(0),
                        tableJob['orgStructure_id'].inlist(self.orgStructureIdList)
                        ]
                self.orgStructureIdList = db.getDistinctIdList(tableJob, tableJob['orgStructure_id'].name(), cond)
            else:
                self.orgStructureIdList = []
        elif self.jobTicketOrgStructureId:
            self.orgStructureIdList = [self.jobTicketOrgStructureId]
        if self.orgStructureIdList:
            filter = db.table('OrgStructure')['id'].inlist(self.orgStructureIdList)
            self.cmbOrgStructureJobTicket.setFilter(filter)
        self.cmbOrgStructureJobTicket.setValue(self.jobTicketOrgStructureId)


    def setOrgStructureVisible(self, value):
        self._orgStructureVisible = value
        self.cmbOrgStructureNotJobTicket.setVisible(value)
        self.lblOrgStructureNotJobTicket.setVisible(value)


    def setDateJobTicket(self, jobDates):
        self.cmbDateJobTicket._model.clear()
        domain = u','.join((u"'" + str(date.toString('dd.MM.yyyy')) + u"'") for date in jobDates if date)
        self.cmbDateJobTicket.setDomain(domain)


    def setJobData(self, jobTicketId, prevActionDate, executionPlan, lastAction, jobData, nextExecutionPlanItem):
        self.jobTicketId = jobTicketId
        self.prevActionDate = prevActionDate
        self.executionPlan = executionPlan
        self.lastAction = lastAction
        self.jobData = jobData
        self.nextExecutionPlanItem = nextExecutionPlanItem
        if self.jobData:
            self.jobTypeId = self.jobData[0]
            self.jobPurposeId = self.jobData[1]
            self.jobTicketOrgStructureId = self.jobData[2]
        if self.isJobTicket:
            self.setOrgStructureIdList()
            self.setDateJobTicket(self.jobDates)
        else:
            self.getJobDates()


    def setDateVisible(self, value):
        self.stwFilter.setCurrentWidget(self.tabJobTicketFilter if value else self.tabNotJobTicketFilter)


    def setDate(self, date):
        if self.isJobTicket:
            self.cmbDateJobTicket.setCurrentIndex(0)
        else:
            self.edtDateNotJobTicket.setDate(date)


    def getDate(self):
        if self.isJobTicket:
            return QDate.fromString(forceString(self.cmbDateJobTicket.text()), "dd.MM.yyyy")
        else:
            return self.edtDateNotJobTicket.date()


    def getCountDays(self):
        if self.isJobTicket:
            return self.edtJobTicketDays.value()
        else:
            return self.edtNotJobTicketDays.value()


    def getOrgStructure(self):
        if self.isJobTicket:
            return self.cmbOrgStructureJobTicket.value()
        else:
            return self.cmbOrgStructureNotJobTicket.value()


    @pyqtSignature('int')
    def on_cmbOrgStructureJobTicket_currentIndexChanged(self, index):
        if self.jobTypeId and len(self.jobDates) > 0 and self.jobDates[0] and self.cmbOrgStructureJobTicket.value() and self.lastAction:
            self.getJobDates()
        elif index > -1:
            self.jobDates = []
            self.setDateJobTicket(self.jobDates)


    def getJobDates(self):
        execOrgStructureId = None
        prevDate = None
        quantityDay = self.getCountDays()
        daysDict = {}
        jobIdList = []
        daysExecutionPlan = []
        record = self.lastAction.getRecord()
        aliquoticity = forceInt(record.value('aliquoticity'))
        aliquoticity = aliquoticity if aliquoticity else 1
        periodicity = forceInt(record.value('periodicity'))
        if not self.nextExecutionPlanItem:
            self.jobDates = []
            self.setDateJobTicket(self.jobDates)
            return
        prevIdx = self.nextExecutionPlanItem.idx
        #prevAliquoticityIdx = self.nextExecutionPlanItem.aliquoticityIdx
        lastDate = None
        items = self.executionPlan.items
        sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
        for idx, item in enumerate(sortedItemsByDate):
            if idx > prevIdx and item.date:
                lastDate = item.date
                break
        if self.isJobTicket:
            execOrgStructureId = self.cmbOrgStructureJobTicket.value()
            if not execOrgStructureId:
                self.jobDates = []
                self.setDateJobTicket(self.jobDates)
                return
            db = QtGui.qApp.db
            tableJob = db.table('Job')
            if self.jobTicketId:
                cnt = 0
                isWeekend = False
                prevDate = self.jobDates[0]
                if not prevDate:
                    self.jobDates = []
                    self.setDateJobTicket(self.jobDates)
                    return
                nextDate = prevDate
                days = quantityDay - cnt
                while cnt <= days:
                    isJob = False
                    if lastDate and lastDate <= nextDate:
                        break
                    cond = [tableJob['jobType_id'].eq(self.jobTypeId),
                            #tableJob['jobPurpose_id'].eq(self.jobPurposeId),
                            tableJob['date'].eq(nextDate),
                            tableJob['deleted'].eq(0),
                            tableJob['orgStructure_id'].eq(execOrgStructureId)
                            ]
                    if jobIdList:
                        cond.append(tableJob['id'].notInlist(jobIdList))
                    recordJob = db.getRecordEx(tableJob, '*', cond, order = [tableJob['orgStructure_id'].name()])
                    if recordJob:
                        isWeekend = False
                        isJob = True
                        jobId = forceRef(recordJob.value('id'))
                        if jobId and jobId not in jobIdList:
                            jobIdList.append(jobId)
                        orgStructureId = forceRef(recordJob.value('orgStructure_id'))
                        daysLine = daysDict.get(orgStructureId, [])
                        daysLine.append(nextDate)
                        daysDict[orgStructureId] = daysLine
                    else:
                        isWeekend = True
                    if isWeekend:
                        nextDate = nextDate.addDays(1)
                    else:
                        nextDate = nextDate.addDays(periodicity+1)
                        if isJob:
                            cnt += 1
                    if cnt >= quantityDay:
                        break
                    if prevDate.addYears(1) < nextDate:
                        break
            for days in daysDict.values():
                for day in days:
                    if day and day not in daysExecutionPlan:
                        daysExecutionPlan.append(day)
            daysExecutionPlan.sort()
        else:
            cnt = 0
            isWeekend = False
            begDate = forceDate(record.value('begDate'))
            prevDate = begDate
            if not begDate:
                self.jobDates = []
                return
            nextDate = begDate
            if lastDate and lastDate <= nextDate:
                self.jobDates = []
                return
            scheduleWeekendDays = self.executionPlan.scheduleWeekendDays.split(',') if self.executionPlan else []
            if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is None and (not scheduleWeekendDays or nextDate.dayOfWeek() not in scheduleWeekendDays)):
                daysLine = daysDict.get(execOrgStructureId, [])
                daysLine.append(nextDate)
                daysDict[execOrgStructureId] = daysLine
                nextDate = nextDate.addDays(periodicity+1)
                cnt += 1
            if nextDate > begDate:
                days = quantityDay - cnt
                while cnt <= days:
                    if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is None and (not scheduleWeekendDays or nextDate.dayOfWeek() not in scheduleWeekendDays)):
                        daysLine = daysDict.get(execOrgStructureId, [])
                        daysLine.append(nextDate)
                        daysDict[execOrgStructureId] = daysLine
                        nextDate = nextDate.addDays(periodicity+1)
                    elif nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is not None or (scheduleWeekendDays and nextDate.dayOfWeek() in scheduleWeekendDays)):
                        isWeekend = True
                    if isWeekend:
                        nextDate = nextDate.addDays(1)
                    else:
                        nextDate = nextDate.addDays(periodicity+1)
                        cnt += 1
                    if cnt >= quantityDay:
                        break
                    if prevDate.addYears(1) < nextDate:
                        break
            for days in daysDict.values():
                for day in days:
                    if day and day not in daysExecutionPlan:
                        daysExecutionPlan.append(day)
            daysExecutionPlan.sort()
        self.jobDates = daysExecutionPlan
        if self.isJobTicket:
            self.setDateJobTicket(self.jobDates)
        else:
            self.edtDateNotJobTicket.setMinimumDate(prevDate)
        self.setDate(prevDate)

