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
import math

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QAbstractTableModel, QDate, QDateTime, QModelIndex, QVariant, pyqtSignature, SIGNAL

from Reports.ReportView import CReportViewDialog
from library.DialogBase import CDialogBase
from library.TableModel import CCol, CDateCol, CTimeCol
from library.Utils      import forceDateTime, forceInt, forceRef, forceString, toVariant, forceTime, forceDate, forceDouble
from library.crbcombobox import CRBModelDataCache
from Users.Rights       import urEditExecutionPlanAction
from Events.Action      import CActionTypeCache
from Events.ActionProperty import CJobTicketActionPropertyValueType
from Events.Utils       import calcQuantity
from Resources.JobTicketStatus import CJobTicketStatus

from Events.Ui_ExecutionPlanDialog import Ui_ExecutionPlanDialog
from Events.Ui_ExecutionPlanEditor import Ui_ExecutionPlanEditor


_RECIPE = 1
_DOSES  = 2


class CDateStringCol(CDateCol):
    def __init__(self, title, fields, defaultWidth, alignment='l', highlightRedDate=True):
        CDateCol.__init__(self, title, fields, defaultWidth, alignment)
        self.highlightRedDate = highlightRedDate and QtGui.qApp.highlightRedDate()
        self.isHasJobTicket = False


    def setHasJobTicket(self, isHasJobTicket):
        self.isHasJobTicket = isHasJobTicket


    def format(self, values):
        val = values[0]
        if self.isHasJobTicket:
            return QVariant(val)
        else:
            if val.type() == QVariant.Date:
                val = val.toDate()
                return QVariant(val.toString(Qt.LocaleDate))
            elif val.type() == QVariant.DateTime:
                val = val.toDateTime()
                return QVariant(val.toString(Qt.LocaleDate))
        return CCol.invalid


    def getValue(self, values):
        val = values[0]
        if self.isHasJobTicket:
            return forceString(val)
        else:
            if val.type() == QVariant.Date:
                return val.toDate()
            elif val.type() == QVariant.DateTime:
                return val.toDateTime()
            return QDateTime()


    def getForegroundColor(self, values):
        val = values[0]
        if self.isHasJobTicket:
            date = QDate.fromString(forceString(val), "dd.MM.yyyy")
        else:
            date = forceDate(val)
        if self.highlightRedDate and date and QtGui.qApp.calendarInfo.getDayOfWeek(date) in (6, 7):
            return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


class CExecutionPlanDialog(CDialogBase, Ui_ExecutionPlanDialog):
    def __init__(self, parent, cols, tableName, order, record, executionPlan, forSelect=False, filterClass=None, action=None, orgStructureIdList=[], scheduleWeekendDays=[6, 7]):
        CDialogBase.__init__(self, parent)
        self.setupBtnSchedule()
        self.setupUi(self)
        self.setup(cols, tableName, order, record, executionPlan, forSelect, filterClass, action, orgStructureIdList, scheduleWeekendDays=scheduleWeekendDays)


    def setup(self, cols, tableName, order, record, executionPlan, forSelect=False, filterClass=None, action=None, orgStructureIdList=[], scheduleWeekendDays=[6, 7]):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.btnSchedule.setMenu(self.mnuBtnSchedule)
        self.btnSave.setVisible(False)
        self.setVisibleBtn(True)
        self.isExecutionPlanByNoDate = False
        self.forSelect = forSelect
        self.executionPlan = executionPlan
        self.action = action
        self.isNomenclatureExpense = self.getNomenclatureExpense()
        self.orgStructureIdList = orgStructureIdList
        self.filterClass = filterClass
        self.isUpdateType = None
        self.props = {}
        self.order = order
        self.model = CExecutionPlanModel(self, cols, self.action.getType().isNomenclatureExpense)
        self.tblExecutionPlan.setModel(self.model)
        self.btnEdit.setDefault(not self.forSelect)
        self.tblExecutionPlan.setFocus(Qt.OtherFocusReason)
        self.scheduleWeekendDays = scheduleWeekendDays
        directionDateTime = forceDateTime(record.value('directionDate'))
        self.edtDirectionDate.setDate(directionDateTime.date())
        self.edtDirectionTime.setTime(directionDateTime.time())
        self.cmbSetPerson.setValue(forceRef(record.value('setPerson_id')))
        self.isEditor = False if forceDateTime(record.value('endDate')) else True
        self.specifiedName = forceString(record.value('specifiedName'))
        self.actionTypeId = forceRef(record.value('actionType_id'))
        self.jobTicketId = None
        self.jobId = None
        self.jobPurposeId = None
        self.jobTypeId = None
        self.jobTicketDate = None
        self.jobTicketOrgStructureId = None
        self.jobTypeIdList = []
        aliquoticity = forceInt(record.value('aliquoticity'))
        self.aliquoticity = aliquoticity if aliquoticity > 0 else 1
        self.quantity = self.executionPlan.quantity if self.executionPlan else forceInt(record.value('quantity'))
        self.getHasJobTicketPropertyType()
        begDateTime = forceDateTime(record.value('begDate'))
        self.begDate = begDateTime.date()
        self.edtBegDate.setDate(self.begDate)
        self.duration = forceInt(record.value('duration'))
        self.periodicity = forceInt(record.value('periodicity'))
        # periodicity - это интервал. Сколько полных дней между назначениями
        self.getQuantityExec()
        self.quantityExecAdd = 0
        plannedEndDateTime = forceDateTime(record.value('plannedEndDate'))
        if not plannedEndDateTime and self.quantityExec:
            plannedEndDateTime = begDateTime.addDays(self.quantityExec-1)
        plannedEndDate = plannedEndDateTime.date()
        self.edtEndDate.setDate(plannedEndDate)
        self.endDate = self.edtEndDate.date()
        self.edtQuantity.setValue(self.quantity)
        self.edtDuration.setValue(self.duration)
        self.edtPeriodicity.setValue(self.periodicity)
        self.edtAliquoticity.setValue(self.aliquoticity)
        self.actionId = forceRef(record.value('id'))
        self.model.loadData(self.executionPlan, self.quantityExec, self.aliquoticity, self.isExecutionPlanByNoDate)
        self.label.setText(u'всего: %d' % len(self.model.items))
#        QObject.connect(self.tblExecutionPlan.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)
        self.cmbOrgStructure.setExpandAll(True)
        self.setJobInfo()


    def getNomenclatureExpense(self):
        actionType = self.action.getType()
        return actionType.isNomenclatureExpense


    def getHasJobTicketPropertyType(self):
        self.hasJobTicketPropertyType = False
        actionType = self.action.getType()
        if not actionType.isNomenclatureExpense:
            db = QtGui.qApp.db
            tableJobTypeAT = db.table('rbJobType_ActionType')
            jobTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['master_id']], [tableJobTypeAT['actionType_id'].eq(self.actionTypeId)])
            self.hasJobTicketPropertyType = bool(jobTypeIdList or actionType._hasJobTicketPropertyType)
        return self.hasJobTicketPropertyType


    def setupBtnSchedule(self):
        self.addObject('mnuBtnSchedule', QtGui.QMenu(self))
        self.addObject('actBySchedule', QtGui.QAction(u'По расписанию подразделения', self))
        self.addObject('actFiveDayWeek', QtGui.QAction(u'Пятидневная неделя', self))
        self.addObject('actSixDayWeek', QtGui.QAction(u'Шестидневная неделя', self))
        self.addObject('actSevenDayWeek', QtGui.QAction(u'Семидневная неделя', self))
        self.mnuBtnSchedule.addAction(self.actBySchedule)
        self.mnuBtnSchedule.addAction(self.actFiveDayWeek)
        self.mnuBtnSchedule.addAction(self.actSixDayWeek)
        self.mnuBtnSchedule.addAction(self.actSevenDayWeek)


    def getOrgStructureId(self):
        return self.cmbOrgStructure.value()


    @pyqtSignature('')
    def on_mnuBtnSchedule_aboutToShow(self):
        quantity = forceInt(self.action.getRecord().value('quantity'))
        actionType = self.action.getType()
        db = QtGui.qApp.db
        tableJobTypeAT = db.table('rbJobType_ActionType')
        jobTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['master_id']], [tableJobTypeAT['actionType_id'].eq(self.actionTypeId)])
        enabled = not jobTypeIdList and not actionType._hasJobTicketPropertyType
        self.actBySchedule.setEnabled(bool(quantity) and not enabled)
        self.actFiveDayWeek.setEnabled(bool(quantity) and enabled)
        self.actSixDayWeek.setEnabled(bool(quantity) and enabled)
        self.actSevenDayWeek.setEnabled(bool(quantity) and enabled)


    @pyqtSignature('')
    def on_actBySchedule_triggered(self):
        self.scheduleWeekendDays = [6, 7]
        self.on_btnSchedule_clicked()


    @pyqtSignature('')
    def on_actFiveDayWeek_triggered(self):
        self.scheduleWeekendDays = [6, 7]
        self.on_btnSchedule_clicked()


    @pyqtSignature('')
    def on_actSixDayWeek_triggered(self):
        self.scheduleWeekendDays = [7]
        self.on_btnSchedule_clicked()


    @pyqtSignature('')
    def on_actSevenDayWeek_triggered(self):
        self.scheduleWeekendDays = []
        self.on_btnSchedule_clicked()


    def getQuantityExec(self):
        if (self.quantity <= self.duration):
            self.quantityExec = self.quantity
        else:
            actionType = CActionTypeCache.getById(self.actionTypeId) if self.actionTypeId else None
            if actionType and actionType.isNomenclatureExpense:
                durationPeriodicity = math.ceil(self.duration/float(1 if self.periodicity == 0 else (2 if self.periodicity == 1 else self.periodicity))) if (self.duration >= self.periodicity) else 1
                self.quantityExec = durationPeriodicity*self.aliquoticity
            else:
                if self.duration > 0:
                    durationPeriodicity = math.ceil(self.duration/float(1 if self.periodicity == 0 else (2 if self.periodicity == 1 else self.periodicity))) if (self.duration >= self.periodicity) else 1
                    quantityRes = durationPeriodicity*self.aliquoticity
                else:
                    quantityRes = self.quantity
                self.quantityExec = quantityRes if (quantityRes < self.quantity) else self.quantity
        return self.quantityExec


    def getJobTypeId(self, jobTypeCode):
        if jobTypeCode:
            data = CRBModelDataCache.getData('rbJobType')
            return data.getIdByCode(jobTypeCode)
        else:
            return None


    def setJobInfo(self):
        db = QtGui.qApp.db
        filter = db.table('OrgStructure')['id'].inlist(self.orgStructureIdList)
        if self.action:
            jobIdList = []
            actionType = self.action.getType()
            tableJobTypeAT = db.table('rbJobType_ActionType')
            self.jobTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['master_id']], [tableJobTypeAT['actionType_id'].eq(self.actionTypeId)])
            if not actionType.isNomenclatureExpense and (self.jobTypeIdList or actionType._hasJobTicketPropertyType):
                tableJob = db.table('Job')
                tableJobTicket = db.table('Job_Ticket')
                self.jobTicketId = None
                self.jobId = None
                self.jobPurposeId = None
                self.jobTypeId = None
                self.jobTicketDate = None
                self.jobTicketOrgStructureId = None
                for property in self.action._propertiesById.itervalues():
                    if property.type().isJobTicketValueType():
                        domain = CJobTicketActionPropertyValueType.parseDomain(property.type().valueDomain)
                        self.jobTypeId = self.getJobTypeId(domain['jobTypeCode'])
                        if self.jobTypeId or (self.jobTypeIdList and self.jobTypeId in self.jobTypeIdList):
                            jobTicketId = property.getValue()
                            if jobTicketId:
                                recordJT = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['id'].eq(jobTicketId), tableJobTicket['deleted'].eq(0)])
                                if recordJT:
                                    self.jobTicketId = forceRef(recordJT.value('id'))
                                    self.jobId = forceRef(recordJT.value('master_id'))
                                    if self.jobId and self.jobId not in jobIdList:
                                        jobIdList.append(self.jobId)
                                    if self.jobTicketId:
                                        break
                record = self.action.getRecord()
                begDateAction = forceDate(record.value('begDate')) if record else None
                if self.jobTicketId:
                    condJob = [tableJob['id'].eq(self.jobId), tableJob['deleted'].eq(0)]
                    recordJ = db.getRecordEx(tableJob, '*', condJob)
                    if recordJ:
                        self.jobTicketDate = forceDate(recordJ.value('date'))
                        self.jobTicketOrgStructureId = forceRef(recordJ.value('orgStructure_id'))
                        self.jobTypeId = forceRef(recordJ.value('jobType_id'))
                        self.jobPurposeId = forceRef(recordJ.value('jobPurpose_id'))
                        if begDateAction and self.jobTicketDate and self.jobTicketDate < begDateAction:
                            condJob = [tableJob['jobType_id'].eq(self.jobTypeId),
                                       tableJob['date'].dateGe(begDateAction),
                                       tableJob['orgStructure_id'].eq(self.jobTicketOrgStructureId),
                                       tableJob['deleted'].eq(0)
                                       ]
                            recordJ = db.getRecordEx(tableJob, '*', condJob, [tableJob['date'].name()])
                            if recordJ:
                                self.jobTicketDate = forceDate(recordJ.value('date'))
                                self.jobTicketOrgStructureId = forceRef(recordJ.value('orgStructure_id'))
                                self.jobTypeId = forceRef(recordJ.value('jobType_id'))
                            if not self.jobTicketDate or not self.jobTicketOrgStructureId or not self.jobTypeId:
                                return
                            self.jobPurposeId = forceRef(recordJ.value('jobPurpose_id'))
                        tableJob = db.table('Job')
                        cond = [tableJob['jobType_id'].eq(self.jobTypeId),
                                tableJob['date'].dateGe(self.jobTicketDate),
                                tableJob['deleted'].eq(0)
                                ]
                        if self.jobPurposeId:
                            cond.append(db.joinOr([tableJob['jobPurpose_id'].eq(self.jobPurposeId), tableJob['jobPurpose_id'].isNull()]))
                        self.orgStructureIdList = db.getDistinctIdList(tableJob, tableJob['orgStructure_id'].name(), cond)
                        if self.jobTicketOrgStructureId:
                            self.orgStructureIdList = list(set(self.orgStructureIdList)|set([self.jobTicketOrgStructureId]))
                        theseAndParentsOSIdList = db.getTheseAndParents('OrgStructure', 'parent_id', self.orgStructureIdList)
                        filter = db.table('OrgStructure')['id'].inlist(theseAndParentsOSIdList)
                elif (self.jobTypeId or self.jobTypeIdList) and begDateAction:
                    tableJob = db.table('Job')
                    cond = [tableJob['date'].dateGe(begDateAction),
                            tableJob['deleted'].eq(0)
                            ]
                    if self.jobTypeIdList and (self.jobTypeId in self.jobTypeIdList or not self.jobTypeId):
                        cond.append(tableJob['jobType_id'].inlist(self.jobTypeIdList))
                    else:
                        jobTypeIdList = []
                        for jobTypeId in jobTypeIdList:
                            jobTypeIdList.append(jobTypeId)
                        if self.jobTypeId:
                            jobTypeIdList.append(self.jobTypeId)
                        if jobTypeIdList:
                            cond.append(tableJob['jobType_id'].inlist(jobTypeIdList))
                    self.orgStructureIdList = db.getDistinctIdList(tableJob, tableJob['orgStructure_id'].name(), cond)
                    if self.jobTicketOrgStructureId:
                        self.orgStructureIdList = list(set(self.orgStructureIdList)|set([self.jobTicketOrgStructureId]))
                    theseAndParentsOSIdList = db.getTheseAndParents('OrgStructure', 'parent_id', self.orgStructureIdList)
                    filter = db.table('OrgStructure')['id'].inlist(theseAndParentsOSIdList)
        self.cmbOrgStructure.setFilter(filter)
        self.cmbOrgStructure.setOrgStructureIdList(self.orgStructureIdList)
        self.cmbOrgStructure.setValue(self.jobTicketOrgStructureId)


    def getDuration(self):
        return self.edtDuration.value()


    def getPeriodicity(self):
        return self.edtPeriodicity.value()


    def getAliquoticity(self):
        return self.edtAliquoticity.value()


    def getQuantity(self):
        return self.edtQuantity.value()


    @pyqtSignature('int')
    def on_edtDuration_valueChanged(self, value):
        record = self.action.getRecord()
        if record and forceInt(record.value('duration')) != value:
            self.action.getRecord().setValue('duration', toVariant(value))
            self.duration = forceInt(self.action.getRecord().value('duration'))
            self.edtQuantity.setValue(calcQuantity(self.action.getRecord()))


    @pyqtSignature('int')
    def on_edtPeriodicity_valueChanged(self, value):
        record = self.action.getRecord()
        if record and forceInt(record.value('periodicity')) != value:
            self.action.getRecord().setValue('periodicity', toVariant(value))
            self.periodicity = forceInt(self.action.getRecord().value('periodicity'))
            #if not self.edtQuantity.value():
            self.edtQuantity.setValue(calcQuantity(self.action.getRecord()))


    @pyqtSignature('int')
    def on_edtAliquoticity_valueChanged(self, value):
        record = self.action.getRecord()
        if record and forceInt(record.value('aliquoticity')) != value:
            self.action.getRecord().setValue('aliquoticity', toVariant(value))
            aliquoticity = forceInt(self.action.getRecord().value('aliquoticity'))
            self.aliquoticity = aliquoticity if aliquoticity > 0 else 1
            #if not self.edtQuantity.value():
            self.edtQuantity.setValue(calcQuantity(self.action.getRecord()))


    @pyqtSignature('int')
    def on_edtQuantity_valueChanged(self, value):
        record = self.action.getRecord()
        if record and forceInt(record.value('quantity')) != value:
            self.action.getRecord().setValue('quantity', toVariant(value))
            self.quantity = forceInt(self.action.getRecord().value('quantity'))
            self.on_cmbOrgStructure_currentIndexChanged(self.cmbOrgStructure.value())



    def select(self, props):
        table = self.model.table()
        return QtGui.qApp.db.getIdList(table.name(), 'id', '', self.order)


    def getItemEditor(self):
        return CExecutionPlanEditor(self, self.aliquoticity, self.quantityExec, self.quantityExecAdd)


    def selectItem(self):
        return self.exec_()


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        self.updateDataExecutionPlanModel()


    def updateDataExecutionPlanModel(self):
        domain = u''
        jobDates = []
        self.model.setMinimumDate(self.begDate)
        self.model.setMaximumDate(self.endDate)
        if not self.isNomenclatureExpense:
            orgStructureId = self.cmbOrgStructure.value()
            if orgStructureId and self.hasJobTicketPropertyType and self.jobTypeId and bool(self.jobTicketDate):
                db = QtGui.qApp.db
                tableJob = db.table('Job')
                cond = [tableJob['jobType_id'].eq(self.jobTypeId),
                        #tableJob['jobPurpose_id'].eq(self.jobPurposeId),
                        tableJob['date'].dateGe(self.jobTicketDate),
                        tableJob['deleted'].eq(0),
                        tableJob['orgStructure_id'].eq(orgStructureId)
                        ]
                records = db.getRecordList(tableJob, [tableJob['date']], cond, order=tableJob['date'].name())
                for record in records:
                    date = forceDate(record.value('date'))
                    if bool(date) and date not in jobDates:
                        jobDates.append(date)
                jobDates.sort()
                if jobDates:
                    domain = u','.join((u"'" + str(date.toString('dd.MM.yyyy')) + u"'") for date in jobDates if date)
            else:
                domain = self.initJobDatesWithoutJobTicket()
            self.model.setDomain(domain)
        self.model.setHasJobTicket(not self.isNomenclatureExpense and self.hasJobTicketPropertyType)


    @pyqtSignature('QModelIndex')
    def on_tblExecutionPlan_doubleClicked(self, index):
        if index.column() == 1:
            self.selected = True
            self.on_btnEdit_clicked()


    @pyqtSignature('')
    def on_btnDeleted_clicked(self):
        self.isExecutionPlanByNoDate = False
        self.getQuantityExec()
        self.action._executionPlanManager._clear()
        self.loadDataExecutionPlan()


    def loadDataExecutionPlan(self):
        self.executionPlan = self.action.getExecutionPlan()
        self.model.loadData(self.action.getExecutionPlan(), self.quantityExec, self.aliquoticity, self.isExecutionPlanByNoDate)


#    @pyqtSignature('')
#    def on_btnSave_clicked(self):
#        self.getQuantityExec()
#        if self.action.getExecutionPlan():
#            self.action._executionPlanManager.save()


#    @pyqtSignature('')
    def on_btnSchedule_clicked(self):
#        if self.cmbOrgStructure.value():
        self.isExecutionPlanByNoDate = False
        self.action._executionPlanManager._clear()
        self.updateExecutionPlanByRecord()
        self.getQuantityExec()
        self.loadDataExecutionPlan()
        self.isUpdateType = 0
        self.updateDataExecutionPlanModel()
        self.model.setUpdateType(self.isUpdateType)


    @pyqtSignature('')
    def on_btnPlan_clicked(self):
#        if self.cmbOrgStructure.value():
        self.isExecutionPlanByNoDate = True
        self.action._executionPlanManager._clear()
        self.updateExecutionPlanByRecordNoDate()
        self.getQuantityExec()
        self.loadDataExecutionPlan()
        self.isUpdateType = 1
        self.updateDataExecutionPlanModel()
        self.model.setUpdateType(self.isUpdateType)


    def initJobDatesWithoutJobTicket(self):
        domain = u''
        jobDates = []
        if not self.isNomenclatureExpense:
            orgStructureId = self.cmbOrgStructure.value()
            minimumDate = self.model.getMinimumDate()
            maximumDate = self.model.getMaximumDate()
            if orgStructureId and minimumDate and maximumDate and self.hasJobTicketPropertyType and self.jobTypeId and not bool(self.jobTicketDate):
                date = minimumDate.addDays(1)
                while date <= maximumDate:
                    if bool(date) and date not in jobDates:
                        jobDates.append(date)
                    date = date.addDays(1)
                jobDates.sort()
                if jobDates:
                    domain = u','.join((u"'" + str(date.toString('dd.MM.yyyy')) + u"'") for date in jobDates if date)
        return domain


    def setVisibleBtn(self, value):
        self.btnSchedule.setVisible(value)
        self.btnPlan.setVisible(value)
#        self.btnSave.setVisible(value)
        self.btnDeleted.setVisible(value)
        self.cmbOrgStructure.setEnabled(value)
        self.edtDuration.setEnabled(value)
        self.edtAliquoticity.setEnabled(value)
        self.edtPeriodicity.setEnabled(value)
        self.edtQuantity.setEnabled(value)


    def updateExecutionPlanByRecordNoDate(self):
        execOrgStructureId = self.cmbOrgStructure.value()
        record = self.action.getRecord()
        quantity = forceInt(record.value('quantity'))
        daysExecutionPlan = []
        daysDict = {}
        actionType = self.action.getType()
        if not actionType.isNomenclatureExpense and quantity:
            aliquoticity = forceInt(record.value('aliquoticity'))
            aliquoticity = aliquoticity if aliquoticity else 1
            quantityDay = math.ceil(quantity/float(aliquoticity if aliquoticity else 1))
            cnt = 0
            begDate = self.jobTicketDate if self.jobTicketDate else forceDate(record.value('begDate'))
            if not begDate:
                return
            nextDate = begDate
            if nextDate:
                daysLine = daysDict.get(execOrgStructureId, [])
                daysLine.append(nextDate)
                daysDict[execOrgStructureId] = daysLine
                cnt += 1
            days = quantityDay - cnt
            while cnt <= days:
                daysLine = daysDict.get(execOrgStructureId, [])
                daysLine.append(None)
                daysDict[execOrgStructureId] = daysLine
                cnt += 1
                if cnt >= quantityDay:
                    break
            for days in daysDict.values():
                for day in days:
                    daysExecutionPlan.append(day)
            if not daysExecutionPlan:
                return
            daysExecutionPlan.sort(reverse=True)
        daysExecutionPlanLen = len(daysExecutionPlan)
        if quantity > 0 and daysExecutionPlanLen > 0 and daysExecutionPlanLen < quantity:
            cnt = quantity - daysExecutionPlanLen
            while cnt > 0:
                daysExecutionPlan.append(None)
                cnt -= 1
        self.action.updateExecutionPlanByRecord(daysExecutionPlan=daysExecutionPlan)
        if actionType.isNomenclatureExpense:
            self.updateNomenclatureExpense()
        executionPlan = self.action.getExecutionPlan()
        if executionPlan:
            executionPlan.setScheduleWeekendDays(u','.join(str(scheduleWeekendDay)for scheduleWeekendDay in self.scheduleWeekendDays if scheduleWeekendDay))
#            if self.action and self.action.executionPlanManager:
#                self.action.executionPlanManager.setExecutionPlan(executionPlan)


    def updateExecutionPlanByRecord(self):
#        if not self.jobTypeId and not self.jobTypeIdList:
#            return
        execOrgStructureId = self.cmbOrgStructure.value()
        record = self.action.getRecord()
        db = QtGui.qApp.db
        if self.jobTypeId and self.jobTypeIdList:
            if not self.jobTicketId or self.jobTicketOrgStructureId != execOrgStructureId:
                actionType = self.action.getType()
                if not actionType.isNomenclatureExpense and (self.jobTypeIdList or actionType._hasJobTicketPropertyType):
                    tableJob = db.table('Job')
                    begDateAction = forceDate(record.value('begDate')) if record else None
                    condJob = [tableJob['date'].dateGe(begDateAction),
                               tableJob['orgStructure_id'].eq(execOrgStructureId),
                               tableJob['deleted'].eq(0)
                               ]
                    if self.jobTypeId:
                        condJob.append(tableJob['jobType_id'].eq(self.jobTypeId))
                    elif self.jobTypeIdList:
                        condJob.append(tableJob['jobType_id'].inlist(self.jobTypeIdList))
                    recordJ = db.getRecordEx(tableJob, '*', condJob, [tableJob['date'].name()])
                    if recordJ:
                        self.jobId = forceRef(recordJ.value('id'))
                        self.jobTicketDate = forceDate(recordJ.value('date'))
                        self.jobTicketOrgStructureId = forceRef(recordJ.value('orgStructure_id'))
                        self.jobTypeId = forceRef(recordJ.value('jobType_id'))
                    if not self.jobTicketDate or not self.jobTicketOrgStructureId or not self.jobTypeId:
                        return
                    self.jobPurposeId = forceRef(recordJ.value('jobPurpose_id'))
                    tableJobTicket = db.table('Job_Ticket')
                    for property in self.action._propertiesById.itervalues():
                        propertyType = property.type()
                        if propertyType.isJobTicketValueType():
                            domain = CJobTicketActionPropertyValueType.parseDomain(property.type().valueDomain)
                            jobTypeId = self.getJobTypeId(domain['jobTypeCode'])
                            if jobTypeId == self.jobTypeId:
                                propertyType.valueType.setIsNearestJobTicket(True)
                                if self.jobTicketOrgStructureId:
                                    propertyType.valueType.setExecOrgStructureId(self.jobTicketOrgStructureId)
                                if self.jobPurposeId:
                                    propertyType.valueType.setExecJobPurposeId(self.jobPurposeId)
                                propertyType.valueType.setDateTimeExecJob(begDateAction)
                                QtGui.qApp.setJTR(self)
                                try:
                                    property._value = property._type.valueType.getPresetValueWithoutAutomatic(self.action, isFreeJobTicket=True)
                                    property._type.valueType.resetParams()
                                    property._changed = True
                                    self.action.setJobTicketChange(True)
                                finally:
                                    QtGui.qApp.unsetJTR(self)
                                self.jobTicketId = property.getValue()
                                if self.jobTicketId:
                                    recordJT = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['id'].eq(self.jobTicketId), tableJobTicket['deleted'].eq(0)])
                                    if recordJT:
                                        self.jobTicketId = forceRef(recordJT.value('id'))
                                        self.jobTicketDate = forceDate(recordJT.value('datetime'))
                                        break
                    if self.jobTicketDate and not self.jobTicketId:
                        recordJT = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['master_id'].eq(self.jobId),tableJobTicket['datetime'].dateEq(self.jobTicketDate), tableJobTicket['status'].eq(CJobTicketStatus.wait), tableJobTicket['deleted'].eq(0)], tableJobTicket['idx'].name())
                        if recordJT:
                            self.jobTicketId = forceRef(recordJT.value('id'))
                            self.jobTicketDate = forceDate(recordJT.value('datetime'))
        quantity = forceInt(record.value('quantity'))
        daysExecutionPlan = []
        daysDict = {}
        jobIdList = []
        actionType = self.action.getType()
        if not actionType.isNomenclatureExpense:
            tableJobTypeAT = db.table('rbJobType_ActionType')
            jobTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['master_id']], [tableJobTypeAT['actionType_id'].eq(self.actionTypeId)])
            if (jobTypeIdList or actionType._hasJobTicketPropertyType) and quantity:
                if not execOrgStructureId:
                    return
                db = QtGui.qApp.db
                tableJob = db.table('Job')
                if self.jobTicketId and self.jobId:
                    aliquoticity = forceInt(record.value('aliquoticity'))
                    aliquoticity = aliquoticity if aliquoticity else 1
                    periodicity = forceInt(record.value('periodicity'))
                    quantityDay = math.ceil(quantity/float(aliquoticity if aliquoticity else 1))
                    cnt = 0
                    isWeekend = False
                    if not self.jobTicketDate:
                        return
                    prevDate = self.jobTicketDate if bool(self.jobTicketDate) else forceDate(record.value('begDate'))
                    nextDate = prevDate
                    if bool(self.jobTicketDate) and bool(nextDate) and self.jobTicketOrgStructureId == execOrgStructureId:
                        daysLine = daysDict.get(self.jobTicketOrgStructureId, [])
                        daysLine.append(nextDate)
                        daysDict[self.jobTicketOrgStructureId] = daysLine
                        nextDate = nextDate.addDays(periodicity+1)
                        cnt += 1
                        if self.jobId not in jobIdList:
                            jobIdList.append(self.jobId)
                    if nextDate > self.jobTicketDate or self.jobTicketOrgStructureId != execOrgStructureId:
                        days = quantityDay - cnt
                        while cnt <= days:
                            isJob = False
                            cond = [tableJob['jobType_id'].eq(self.jobTypeId),
                                    #tableJob['jobPurpose_id'].eq(self.jobPurposeId),
                                    tableJob['id'].notInlist(jobIdList),
                                    tableJob['date'].eq(nextDate),
                                    tableJob['deleted'].eq(0),
                                    tableJob['orgStructure_id'].eq(execOrgStructureId)
                                    ]
                            recordJob = db.getRecordEx(tableJob, '*', cond, order = [tableJob['orgStructure_id'].name()])
                            if recordJob:
                                isJob = True
                                isWeekend = False
                                jobId = forceRef(recordJob.value('id'))
                                if jobId and jobId not in jobIdList:
                                    jobIdList.append(jobId)
                                orgStructureId = forceRef(recordJob.value('orgStructure_id'))
                                daysLine = daysDict.get(orgStructureId, [])
                                daysLine.append(nextDate)
                                daysDict[orgStructureId] = daysLine
                            elif nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is not None or nextDate.dayOfWeek() in [6, 7]):
                                isWeekend = True
                            else:
                                isWeekend = False
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
                if not daysExecutionPlan:
                    return
                daysExecutionPlan.sort()
            elif (not jobTypeIdList and not actionType._hasJobTicketPropertyType) and quantity:
                aliquoticity = forceInt(record.value('aliquoticity'))
                aliquoticity = aliquoticity if aliquoticity else 1
                periodicity = forceInt(record.value('periodicity'))
                quantityDay = math.ceil(quantity/float(aliquoticity if aliquoticity else 1))
                cnt = 0
                isWeekend = False
                begDate = forceDate(record.value('begDate'))
                if not begDate:
                    return
                prevDate = begDate
                nextDate = prevDate
                if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) != 7 and (not self.scheduleWeekendDays or nextDate.dayOfWeek() not in self.scheduleWeekendDays)):
                    daysLine = daysDict.get(execOrgStructureId, [])
                    daysLine.append(nextDate)
                    daysDict[execOrgStructureId] = daysLine
                    nextDate = nextDate.addDays(periodicity+1)
                    cnt += 1
                if nextDate >= begDate:
                    days = quantityDay - cnt
                    while cnt <= days:
                        if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) != 7 and (not self.scheduleWeekendDays or nextDate.dayOfWeek() not in self.scheduleWeekendDays)):
                            daysLine = daysDict.get(execOrgStructureId, [])
                            daysLine.append(nextDate)
                            daysDict[execOrgStructureId] = daysLine
                            #nextDate = nextDate.addDays(periodicity+1)
                            isWeekend = False
                        elif nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is not None or (self.scheduleWeekendDays and nextDate.dayOfWeek() in self.scheduleWeekendDays)):
                            isWeekend = True
                        else:
                            isWeekend = False
                        if isWeekend:
                            nextDate = nextDate.addDays(1)
                        else:
                            nextDate = nextDate.addDays(periodicity+1)
                            cnt += 1
                        if cnt >= quantityDay:
                            break
                for days in daysDict.values():
                    for day in days:
                        if day and day not in daysExecutionPlan:
                            daysExecutionPlan.append(day)
                if not daysExecutionPlan:
                    return
                daysExecutionPlan.sort()
        else:
            aliquoticity = forceInt(record.value('aliquoticity'))
            aliquoticity = aliquoticity if aliquoticity else 1
            periodicity = forceInt(record.value('periodicity'))
            quantityDay = math.ceil(quantity/float(aliquoticity if aliquoticity else 1))
            cnt = 0
            isWeekend = False
            begDate = forceDate(record.value('begDate'))
            if not begDate:
                return
            prevDate = begDate
            nextDate = prevDate
            if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) != 7 and (not self.scheduleWeekendDays or nextDate.dayOfWeek() not in self.scheduleWeekendDays)):
                daysLine = daysDict.get(execOrgStructureId, [])
                daysLine.append(nextDate)
                daysDict[execOrgStructureId] = daysLine
                nextDate = nextDate.addDays(periodicity+1)
                cnt += 1
            if nextDate >= begDate:
                days = quantityDay - cnt
                while cnt <= days:
                    if nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) != 7 and (not self.scheduleWeekendDays or nextDate.dayOfWeek() not in self.scheduleWeekendDays)):
                        daysLine = daysDict.get(execOrgStructureId, [])
                        daysLine.append(nextDate)
                        daysDict[execOrgStructureId] = daysLine
                        isWeekend = False
                    elif nextDate and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*nextDate.getDate()) is not None or (self.scheduleWeekendDays and nextDate.dayOfWeek() in self.scheduleWeekendDays)):
                        isWeekend = True
                    else:
                        isWeekend = False
                    if isWeekend:
                        nextDate = nextDate.addDays(1)
                    else:
                        nextDate = nextDate.addDays(periodicity+1)
                        cnt += 1
                    if cnt >= quantityDay:
                        break
            for days in daysDict.values():
                for day in days:
                    if day and day not in daysExecutionPlan:
                        daysExecutionPlan.append(day)
            if not daysExecutionPlan:
                return
            daysExecutionPlan.sort()
        daysExecutionPlanLen = len(daysExecutionPlan)
        if quantity > 0 and daysExecutionPlanLen > 0 and daysExecutionPlanLen < quantity:
            cnt = quantity - daysExecutionPlanLen
            while cnt > 0:
                daysExecutionPlan.append(None)
                cnt -= 1
        self.action.updateExecutionPlanByRecord(daysExecutionPlan=daysExecutionPlan)
        if actionType.isNomenclatureExpense:
            self.updateNomenclatureExpense()
        executionPlan = self.action.getExecutionPlan()
        if executionPlan:
            executionPlan.setScheduleWeekendDays(u','.join(str(scheduleWeekendDay)for scheduleWeekendDay in self.scheduleWeekendDays if scheduleWeekendDay))
#            if self.action and self.action.executionPlanManager:
#                self.action.executionPlanManager.setExecutionPlan(executionPlan)


    def updateNomenclatureExpense(self):
        record = self.action.getRecord() if self.action else None
        if record and self.action:
            nomenclatureId = forceRef(record.value('recipe'))
            doses = forceDouble(record.value('doses'))
            if nomenclatureId and self.action.getExecutionPlan():
                for epItem in self.action.getExecutionPlan().items:
                    if epItem.nomenclature:
                        epItem.nomenclature.nomenclatureId = nomenclatureId
                        epItem.nomenclature.dosage = doses
                        nomenclatureItem = epItem.nomenclature
                        nomenclatureItem.actionExecutionPlanItem = epItem


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        if self.action and self.action.executionPlanManager:
            executionPlan = self.action.getExecutionPlan()
            if executionPlan and executionPlan.items and len(executionPlan.items) > 0:
                self.action._executionPlanManager.setCurrentItem(executionPlan.items[0])
        self.close()


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        if self.isEditor:
            if QtGui.qApp.userHasRight(urEditExecutionPlanAction):
                row = self.tblExecutionPlan.currentRow()
                if row >= 0:
                    items = self.tblExecutionPlan.model().items
                    item = items[row]
                    if item and item.date:
                        dialog = self.getItemEditor()
                        try:
                            dialog.load(item)
                            if dialog.exec_():
                                item.merge()
                                self.quantityExecAdd = dialog.quantityExecAdd
                            else:
                                item.clear()
                        finally:
                            dialog.deleteLater()
            else:
                QtGui.QMessageBox.information(
                    self,
                    u'Внимание!',
                    u'У вас нет прав на редактирование календаря выполнения назначений!')
        else:
            QtGui.QMessageBox.information(
                self,
                u'Внимание!',
                u'Вы не можете редактировать календарь выполнения назначений, так как действие выполнено!')


    def getReportHeader(self):
        return self.objectName()


    def getFilterAsText(self):
        return u''


    def contentToHTML(self):
        actionTypeName = ''
        if self.actionTypeId:
            db = QtGui.qApp.db
            table = db.table('ActionType')
            record = db.getRecordEx(table, [table['name']], [table['id'].eq(self.actionTypeId), table['deleted'].eq(0)])
            if record:
                actionTypeName = forceString(record.value('name'))
        reportHeader = self.getReportHeader() + u'\n'+ u'Действие: ' + actionTypeName + ((u'(' + self.specifiedName + u')') if self.specifiedName else u'')
        self.tblExecutionPlan.setReportHeader(reportHeader)
        reportDescription=self.getFilterAsText()
        self.tblExecutionPlan.setReportDescription(reportDescription)
        return self.tblExecutionPlan.contentToHTML()


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        html = self.contentToHTML()
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    def setSort(self, col):
        name=self.model.cols()[col].fields()[0]
        self.order = name
        header=self.tblExecutionPlan.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(col, Qt.AscendingOrder)


class CExecutionPlanEditor(CDialogBase, Ui_ExecutionPlanEditor):
    def __init__(self,  parent, aliquoticity, quantityExec, quantityExecAdd):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.tblPlanEditor.setModel(CExecutionPlanEditorModel(self))
        self.item = None
        self.aliquoticity = max(aliquoticity, 1)
        self.quantityExec = quantityExec
        self.quantityExecAdd = quantityExecAdd
        self.tblPlanEditor.model().setAliquoticity(self.aliquoticity)
        self.tblPlanEditor.model().setQuantityExec(self.quantityExec)


    def load(self, item):
        self.item = item
        if self.item:
            self.tblPlanEditor.model().setQuantityExecAdd(self.quantityExecAdd)
            self.tblPlanEditor.model().loadData(self.item)


    def getInfoDict(self):
        return self.tblPlanEditor.model().saveData()


    def saveData(self):
        modelItems = self.tblPlanEditor.model().items
        if modelItems and len(modelItems) != self.aliquoticity:
            return self.checkValueMessage(u'Запланированное время должно либо '
                                          u'отсутствовать либо иметь %d элемента' % self.aliquoticity,
                                          skipable=False,
                                          widget=self)
        self.quantityExecAdd = self.tblPlanEditor.model().quantityExecAdd
        return True


class CExecutionPlanEditorModel(QAbstractTableModel):
    column = [u'Выбранное время']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.items = []
        self.dateItem = None
        self.aliquoticity = 1
        self.quantityExec = 0
        self.quantityExecAdd = 0


    def setAliquoticity(self, aliquoticity):
        self.aliquoticity = aliquoticity


    def setQuantityExec(self, quantityExec):
        self.quantityExec = quantityExec


    def setQuantityExecAdd(self, quantityExecAdd):
        self.quantityExecAdd = quantityExecAdd


    def columnCount(self, index = None):
        return 1


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index = None):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def loadData(self, dateItem):
        self.dateItem = dateItem
        self.items = dateItem.items
        self.reset()


    def saveData(self):
        return self.dateItem.merge()


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == Qt.DisplayRole:
            if 0 <= row < len(self.items):
                return toVariant(self.dateItem.getItemTime(self.items[row]))

        if role == Qt.EditRole:
            if 0 <= row < len(self.items):
                return toVariant(self.dateItem.getItemTime(self.items[row]))

        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if self.aliquoticity == row:
                return False
            if self.quantityExecAdd >= self.quantityExec:
                return False
            if row == len(self.items):
                if value.isNull():
                    return False
                self.dateItem.addNewTime(forceTime(value))
                self.items = self.dateItem.items
                vCnt = len(self.items)
                vIndex = QModelIndex()
                self.beginInsertRows(vIndex, vCnt, vCnt)
                self.insertRows(vCnt, 1, vIndex)
                self.endInsertRows()
                self.quantityExecAdd += 1
                self.emitCellChanged(row, column)
                return True
            if 0 <= row < len(self.items):
                newTime = value.toTime()
                if newTime.isNull():
                    newTime = None
                oldTime = forceTime(self.dateItem.getItemTime(self.items[row]))
                oldTime = oldTime if not oldTime.isNull() else None
                if not oldTime and newTime:
                    self.quantityExecAdd += 1
                elif oldTime and not newTime:
                    self.quantityExecAdd -= 1
                self.dateItem.setItemTime(self.items[row], newTime)
            self.emitCellChanged(row, column)
            return True
        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def confirmRemoveRow(self, view, row, multiple=False):
        return True


    def canRemoveRow(self, row):
        return 0 <= row < len(self.items)


    def removeRow(self, row, parentIndex=QModelIndex()):
        if not 0 <= row < len(self.items):
            return False

        self.beginRemoveRows(parentIndex, row, row)
        item = self.items[row]
        self.dateItem.removeItem(item)
        self.endRemoveRows()
        self.items = self.dateItem.items
        self.quantityExecAdd -= 1
        self.reset()


class CGetExecutionPlan(CExecutionPlanDialog):
    def __init__(self, parent, record, executionPlan, action=None, orgStructureIdList=[], scheduleWeekendDays=[6, 7]):
        CExecutionPlanDialog.__init__(self, parent, [
            CDateStringCol(u'Дата',  ['date'], 20),
            CTimeCol(u'Время', ['time'], 40),
            ], 'ActionExecutionPlan_item', ['date'], record, executionPlan, action=action, orgStructureIdList=orgStructureIdList, scheduleWeekendDays=scheduleWeekendDays)
        self.setWindowTitleEx(u'План выполнения назначений')
        self.selected = False
        self.executionPlan = executionPlan


class CDateItems(object):
    def __init__(self, executionPlan, date, executionPlanItem):
        self._executionPlan = executionPlan
        self._executionPlanItem = executionPlanItem
        self._date = date
        self._items = []
        self._times = None
        self._newItems = []
        self._timesCache = {}


    def addNewTime(self, time):
        item = self._executionPlan.createNewDateTimeItem(self._date, time)
        self._timesCache[item] = time
        self._newItems.append(item)
        self._times = None


    def setItemTime(self, item, time):
        self._timesCache[item] = time
        self._times = None


    def getItemTime(self, item):
        return self._timesCache.get(item, None)


    def removeItem(self, item):
        if item is self._executionPlan.items[0]:
            raise ValueError("Could not delete initial item")
        if item in self._timesCache:
            del self._timesCache[item]

        if item in self._items:
            #self._items.remove(item)
            item.time = None
            item.setIsDirty()
        elif item in self._newItems:
            self._newItems.remove(item)
        else:
            raise ValueError()


    @property
    def items(self):
        return self._items + self._newItems


    def merge(self):
        for item in self._newItems:
            self._executionPlan.addItem(item)
            self._items.append(item)
        self._newItems = []

        for i in self._items:
            if i in self._timesCache:
                i.time = self._timesCache[i]
                i.setIsDirty()

        return self._items


    def clear(self):
        for i in self._items:
            if i in self._timesCache:
                i.setIsDirty()
        self._times = None
        self._newItems = []
        self._timesCache = {}


    def setDate(self, date):
        self._date = date
        self._executionPlanItem.date = self._date
        items = self._executionPlan.items
        for idx, item in enumerate(items):
            if self._executionPlanItem.aliquoticityIdx == item.aliquoticityIdx:
                self._executionPlan.items[idx].date = self._date
        sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
        self._executionPlan.items = sortedItemsByDate
        self._executionPlan.items._remapIdx()
        items = self._executionPlanItem.executionPlan.items
        for idx, item in enumerate(items):
            if self._executionPlanItem.aliquoticityIdx == item.aliquoticityIdx:
                self._executionPlanItem.executionPlan.items[idx].date = self._date
        sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
        self._executionPlanItem.executionPlan.items = sortedItemsByDate
        self._executionPlanItem.executionPlan.items._remapIdx()
        self._executionPlanItem.executionPlan.items._remap()
        self._executionPlan.items._remap()


    @property
    def date(self):
        return self._date


    @property
    def time(self):
        if self._times is None:
            times = []
            for i in self.items:
                if i not in self._timesCache:
                    continue
                time = self._timesCache[i]
                if not (time and time.isValid()):
                    continue
                times.append(unicode(time.toString('hh:mm')))

            self._times = ';'.join(times)

        return self._times


    def addItem(self, item):
        self._items.append(item)


class CExecutionPlanModel(QAbstractTableModel):
    column = [u'Дата', u'Время']

    def __init__(self, parent, cols, isNomenclatureExpense=False):
        QAbstractTableModel.__init__(self, parent)
        self.items = []
        self._cols = cols
        self.isNomenclatureExpense = isNomenclatureExpense
        self.executionPlan = None
        self.isExecutionPlanByNoDate = False
        self.quantityExec = 0
        self.aliquoticity = 0
        self.setDomain(u'')
        self.isHasJobTicket = False
        self.minimumDate = None
        self.maximumDate = None
        self.isUpdateType = None


    def setUpdateType(self, isUpdateType):
        self.isUpdateType = isUpdateType


    def cols(self):
        return self._cols


    def setDomain(self, domain):
        self.domain = domain


    def getDomain(self):
        return self.domain


    def setHasJobTicket(self, isHasJobTicket):
        self.isHasJobTicket = isHasJobTicket
        self._cols[0].setHasJobTicket(isHasJobTicket)
        self.reset()


    def setMinimumDate(self, date):
        self.minimumDate = date


    def setMaximumDate(self, date):
        self.maximumDate = date


    def getMinimumDate(self):
        return self.minimumDate


    def getMaximumDate(self):
        return self.maximumDate


    def columnCount(self, index = None):
        return 2


    def rowCount(self, index = None):
        return len(self.items)


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            if column == 0:
                return toVariant(item.date)
            elif column == 1:
                return toVariant(item.time)
        if role == Qt.EditRole:
            if 0 <= row < len(self.items):
                if column == 0:
                    return toVariant(self.items[row].date)
        if role == Qt.ForegroundRole:
            item = self.items[row]
            if column == 0:
                date = item.date
                if bool(date) and (QtGui.qApp.calendarInfo.getDayOfWeekInt(*date.getDate()) is not None or date.dayOfWeek() in (6, 7)):
                    return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


    def loadData(self, executionPlan, quantityExec, aliquoticity, isExecutionPlanByNoDate = False):
        self.items = []
        self.isExecutionPlanByNoDate = isExecutionPlanByNoDate
        self.quantityExec = quantityExec
        self.aliquoticity = aliquoticity
        quantityDay = math.ceil(self.quantityExec/float(self.aliquoticity if self.aliquoticity else 1))
        self.executionPlan = executionPlan
        aliquoticityIdx = -1
        aliquoticityTimeIdx = 0
        if self.executionPlan and self.executionPlan.items:
            dateItems = {}
            items = self.executionPlan.items
            sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
            if not self.isExecutionPlanByNoDate:
                for idx, item in enumerate(sortedItemsByDate):
                    if not item.date:
                        self.isExecutionPlanByNoDate = True
                        break
            isUpdateItems = False
            dataKey = None
            for idx, item in enumerate(sortedItemsByDate):
                dk = item.date.toPyDate()
                isUpdateItems = False
                if self.isExecutionPlanByNoDate:
                    if self.isNomenclatureExpense:
                        if len(dateItems.keys()) < quantityDay:
                            dataKey = (dk, idx)
                            isUpdateItems = True
                            if item.date:
                                dkKeys = dateItems.keys()
                                dkKeys.sort(key=lambda x: (x[1], x[0]))
                                for (dkKey, idxKey) in dkKeys:
                                    if dkKey == dk:
                                        dataKey = (dkKey, idxKey)
                                        break
                    else:
                        if item.aliquoticityIdx != aliquoticityIdx and len(dateItems.keys()) < quantityDay:
                            aliquoticityTimeIdx = 0
                            dataKey = (dk, idx)
                            isUpdateItems = False
                            aliquoticityIdx = item.aliquoticityIdx
                            if item.date:
                                dkKeys = dateItems.keys()
                                dkKeys.sort(key=lambda x: (x[1], x[0]))
                                for (dkKey, idxKey) in dkKeys:
                                    if dkKey == dk:
                                        dataKey = (dkKey, idxKey)
                                        break
                else:
                    dataKey = dk
                    isUpdateItems = True
#                if (self.isNomenclatureExpense and isUpdateItems) or (aliquoticityTimeIdx < aliquoticity and not self.isNomenclatureExpense):
                if isUpdateItems or (aliquoticityTimeIdx < aliquoticity and not self.isNomenclatureExpense):
                    if not dataKey:
                        dataKey = dk
                    dateItem = dateItems.get(dataKey, CDateItems(self.executionPlan, item.date, item))
                    if dateItem:
                        dateItem.setItemTime(item, item.time)
                        dateItems[dataKey] = dateItem
                    dateItems[dataKey].addItem(item)
                    aliquoticityTimeIdx += 1
            self.items = [dateItems[k] for k in sorted(dateItems.keys())]
        self.reset()


    def loadDataItem(self, executionPlan, execDate, row):
        execTimeDict = executionPlan.get(execDate, {})
        execTimeKeys = execTimeDict.keys()
        execTimeKeys.sort()
        execTimeStr = u', '.join(str(execTime.toString('hh:mm')) for execTime in execTimeKeys if execTime)
        item = [QDate(execDate).toString('dd-MM-yyyy'),
                execTimeStr,
                executionPlan
                ]
        self.executionPlan[execDate] = executionPlan.get(execDate, {})
        self.items[row] = item
        self.reset()


    def flags(self, index):
        column = index.column()
        if column == 0:
            if self.isNomenclatureExpense:
                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
            row = index.row()
            if 0 <= row < len(self.items):
                item = self.items[row]
                if bool(item._executionPlanItem.executedDatetime):
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                date = item.date
                if bool(date) and row == 0 and not self.isUpdateType:
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                elif bool(date):
                    times = item.getItemTime(item)
                    if times:
                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                    if row == 0 and (row+1) == len(self.items):
                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                    if (row+1) <= len(self.items):
                        rowLast = row + (1 if (row < len(self.items)-1) else 0)
                        itemLast = self.items[rowLast]
                        if row > 0:
                            itemPrev = self.items[row-1]
                            if not itemPrev.date:
                                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                            elif itemPrev.date >= date:
                                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                            elif itemLast.date == date.addDays(1) and itemPrev.date == date.addDays(-1):
                                return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                            else:
                                return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                        if row == rowLast:
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                        if itemLast and bool(itemLast.date) and date.addDays(1) >= itemLast.date:
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                        elif itemLast and not itemLast.date:
                            for rowLast, iLast in enumerate(self.items):
                                if rowLast > row and iLast and bool(iLast.date):
                                    if iLast.date <= date.addDays(1):
                                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                                    else:
                                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                elif row == 0:
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                elif row > 0:
                    itemPrev = self.items[row-1]
                    if not itemPrev:
                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                    if (row+1) <= len(self.items):
                        rowLast = row + (1 if (row < len(self.items)-1) else 0)
                        if row == rowLast:
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                        itemLast = self.items[rowLast]
                        if itemLast and bool(itemLast.date) and itemPrev.date.addDays(-1) < itemLast.date:
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                        elif itemLast and not itemLast.date:
                            for rowLast, iLast in enumerate(self.items):
                                if rowLast > row and iLast and bool(iLast.date):
                                    if iLast.date <= itemPrev.addDays(1):
                                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
                                    else:
                                        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
                            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if 0 <= row < len(self.items):
                if column == 0:
                    item = self.items[row]
                    if self.isHasJobTicket:
                        date = QDate.fromString(forceString(value), "dd.MM.yyyy")
                    else:
                        date = forceDate(value)
                    if row > 0:
                        itemPrev = self.items[row-1]
                        if bool(itemPrev.date) and bool(date) and itemPrev.date >= date:
                            return False
                        if row < (len(self.items)-1):
                            itemLast = self.items[row+1]
                            if bool(itemLast.date) and bool(date) and itemLast.date <= date:
                                return False
                    if item: #and date:
                        item.setDate(date)
                    self.emitCellChanged(row, column)
                    items = self.executionPlan.items
                    sortedItemsByDate = sorted(items, key=lambda x: (x.date.toPyDate(), x.idx, x.aliquoticityIdx), reverse=False)
                    self.executionPlan.items = sortedItemsByDate
                    self.executionPlan.items._remapIdx()
                    self.executionPlan.items._remap()
                    return True
        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
