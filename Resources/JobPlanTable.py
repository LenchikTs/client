# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtCore
from PyQt4.QtCore import *

from library.Utils import *
from library.TableView import *
from library.TimeEdit import *
from Timeline.Schedule import invertGapList, calcTimePlanForCapacity


def formatTimeRange(range):
    if range:
        start, finish = range
        return start.toString('HH:mm')+' - ' +finish.toString('HH:mm')
    else:
        return ''


def convertTimeRangeToVariant(range):
    if range:
        start, finish = range
        return QVariant.fromList([QVariant(start), QVariant(finish)])
    else:
        return QVariant()


def convertVariantToTimeRange(value):
    list = value.toList()
    if len(list) == 2:
        start = list[0].toTime()
        finish = list[1].toTime()
        if start.isNull() and finish.isNull():
            return None
        return start, finish
    else:
        return None


class CJobPlanItem(object):
    def __init__(self):
        self.record = None
        self.timeRange = None
        self.oldTimeRange = None
        self.quantity = 0
        self.oldQuantity = 0
        self.reserved = 0
        self.busy = 0
        self.executed = 0
        self.tickets = []
        self.ticketIsDirty = []
        self.forceChange = False


    def countUsed(self):
        return self.reserved + self.busy + self.executed


    def changed(self):
        return self.timeRange != self.oldTimeRange or self.quantity != self.oldQuantity or self.forceChange


    def setRecord(self, record):
        self.record = record
        self.timeRange = forceTime(record.value('begTime')), forceTime(record.value('endTime'))
        self.oldTimeRange = self.timeRange
        self.quantity = forceInt(record.value('quantity'))
        self.oldQuantity = self.quantity
        self.reserved = 0
        self.busy     = 0
        self.executed = 0
        db = QtGui.qApp.db
        tableTicket = db.table('Job_Ticket')
        cols = [tableTicket['id'],
                tableTicket['master_id'],
                tableTicket['idx'],
                tableTicket['datetime'],
#                tableTicket['resTimestamp'],
#                tableTicket['resConnectionId'],
                tableTicket['status'],
                tableTicket['begDateTime'],
                tableTicket['endDateTime'],
                tableTicket['label'],
                tableTicket['note'],
                '''EXISTS(SELECT ActionProperty_Job_Ticket.value
FROM Job_Ticket AS JT
LEFT JOIN ActionProperty_Job_Ticket ON ActionProperty_Job_Ticket.value=JT.id
LEFT JOIN ActionProperty ON ActionProperty.id=ActionProperty_Job_Ticket.id
LEFT JOIN Action ON Action.id=ActionProperty.action_id
LEFT JOIN ActionType ON ActionType.id=Action.actionType_id
WHERE JT.id=Job_Ticket.id AND Action.deleted=0
ORDER BY JT.id) AS usedInActionProperty ''']
        self.tickets = db.getRecordList(tableTicket, cols, tableTicket['master_id'].eq(record.value('id')), 'Job_Ticket.id')
        for ticket in self.tickets:
            status = forceInt(ticket.value('status'))
            usedInActionProperty = forceBool(ticket.value('usedInActionProperty'))
            if usedInActionProperty:
                if status == 0:
                    self.reserved += 1
                elif status == 1:
                    self.busy += 1
                elif status == 2:
                    self.executed += 1
        self.ticketIsDirty = [False]*len(self.tickets)


    def updateRecord(self, orgStructureId, jobTypeId, date):
        db = QtGui.qApp.db
        if not self.record:
            if self.timeRange or self.quantity:
                tableJob = db.table('Job')
                self.record = tableJob.newRecord()
                self.record.setValue('orgStructure_id', toVariant(orgStructureId))
                self.record.setValue('jobType_id', toVariant(jobTypeId))
                self.record.setValue('date',            toVariant(date))
        if self.record:
            self.quantity = max(self.quantity, self.countUsed())
            begTime, endTime = self.timeRange if self.timeRange else (None, None)
            self.record.setValue('begTime', toVariant(begTime))
            self.record.setValue('endTime', toVariant(endTime))
            self.record.setValue('quantity',toVariant(self.quantity))

            tableTicket = db.table('Job_Ticket')
            if len(self.tickets) > self.quantity:
                i = len(self.tickets)
                while i>0 and len(self.tickets)>self.quantity:
                    i -= 1
                    ticket = self.tickets[i]
                    if not forceBool(ticket.value('usedInActionProperty')):
                        del self.tickets[i]
                        del self.ticketIsDirty[i]

            else:
                while len(self.tickets)<self.quantity:
                    self.tickets.append(tableTicket.newRecord(['id', 'master_id', 'datetime', 'idx']))
                    self.ticketIsDirty.append(True)

            timePlan = getTimePlan(self.timeRange, self.quantity, orgStructureId)
            for i, ticket in enumerate(self.tickets):
                datetime = forceDateTime(QDateTime(date, timePlan[i]) if i < len(timePlan) else None)
                oldDatetime = forceDateTime(ticket.value('datetime'))
                oldIdx = forceInt(ticket.value('idx'))
                if oldDatetime != datetime or oldIdx != i:
                    ticket.setValue('datetime', toVariant(datetime))
                    ticket.setValue('idx', toVariant(i))
                    self.ticketIsDirty[i] = True


    def saveRecord(self):
        jobTicketIdList = []
        db = QtGui.qApp.db
        tableJob = db.table('Job')
        tableTicket = db.table('Job_Ticket')
        id = db.insertOrUpdate(tableJob, self.record)
        for i, ticket in enumerate(self.tickets):
            jobTicketId = forceRef(ticket.value('id'))
            if self.ticketIsDirty[i] or forceInt(ticket.value('master_id')) != id:
                record = tableTicket.newRecord(['id', 'master_id', 'datetime', 'idx'])
                record.setValue('id',        ticket.value('id'))
                record.setValue('master_id', toVariant(id))
                record.setValue('datetime',  ticket.value('datetime'))
                record.setValue('idx',       ticket.value('idx'))
                jobTicketId = db.insertOrUpdate(tableTicket, record)
            if jobTicketId:
                jobTicketIdList.append(jobTicketId)
        if jobTicketIdList:
            db.deleteRecord(tableTicket,
                             [ tableTicket['master_id'].eq(id),
                               tableTicket['id'].notInlist(jobTicketIdList)])
        else:
            db.deleteRecord(tableTicket,
                             [ tableTicket['master_id'].eq(id) ])


class CJobPlanModel(QAbstractTableModel):
    headerText = [u'Время', u'План', u'Назначено', u'Выполняется', u'Выполнено']

    actionsTypesChecked = False

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.orgStructureId = None
        self.jobTypeId = None
        self.year = None
        self.month = None
        self.begDate = None
        self.daysInMonth = 0
        self.items = []
        self.redDays = []
        self.redBrush = QtGui.QBrush(QtGui.QColor(255, 0, 0))


    def columnCount(self, index = None):
        return 5


    def rowCount(self, index = None):
        return self.daysInMonth


    def flags(self, index):
        column = index.column()
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|(Qt.ItemIsEditable if column <=1 else Qt.NoItemFlags)


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.EditRole:
            if row < self.daysInMonth:
                item = self.items[row]
                if column == 0:
                    return convertTimeRangeToVariant(item.timeRange)
                elif column == 1:
                    return toVariant(item.quantity)
        elif role == Qt.DisplayRole:
            if row < self.daysInMonth:
                item = self.items[row]
                if column == 0:
                    return toVariant(formatTimeRange(item.timeRange))
                elif column == 1:
                    return toVariant(item.quantity)
                elif column == 2:
                    return toVariant(item.reserved)
                elif column == 3:
                    return toVariant(item.busy)
                elif column == 4:
                    return toVariant(item.executed)
#
#            return toVariant(self.items[row][column])
        elif role == Qt.TextAlignmentRole:
            if row < self.daysInMonth:
                if column!=1:
                    return QVariant(Qt.AlignLeft|Qt.AlignVCenter)
            return QVariant(Qt.AlignRight|Qt.AlignVCenter)
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if row < self.daysInMonth:
                item = self.items[row]
                valueChanged = False
                if column == 0:
                    newValue = convertVariantToTimeRange(value)
                    valueChanged = item.timeRange != newValue
                    item.timeRange = newValue
                elif column  == 1:
                    newValue = forceInt(value)
                    valueChanged = item.quantity != newValue
                    item.quantity = max(newValue, item.countUsed())
                if valueChanged:
                    self.emitCellChanged(row, column)
            return True
        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(QtCore.SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return QVariant(self.headerText[section])
        if orientation == Qt.Vertical and self.daysInMonth:
            if role == QtCore.Qt.DisplayRole:
                if section<self.daysInMonth:
                    return QVariant(section+1)
                else:
                    return QVariant(u'Всего')
            if role == Qt.ToolTipRole:
                if section<self.daysInMonth:
                    return QVariant(self.begDate.addDays(section))
                else:
                    return QVariant(u'Всего')
            if role == Qt.ForegroundRole:
                if section<self.daysInMonth and self.redDays[section]:
                    return QVariant(self.redBrush)
                else:
                    return QVariant()
        return QVariant()


    def setJobAndMonth(self, orgStructureId, jobTypeId, year, month):
        if self.orgStructureId != orgStructureId or self.jobTypeId != jobTypeId or self.year != year or self.month != month:
            self.saveData()
            self.loadData(orgStructureId, jobTypeId, year, month)


    def saveData(self):
        if self.orgStructureId and self.jobTypeId and self.year and self.month:
            db = QtGui.qApp.db
            db.transaction()
            try:
                for day in xrange(self.daysInMonth):
                    item = self.items[day]
                    if item.changed():
                        item.updateRecord(self.orgStructureId, self.jobTypeId, QDate(self.year, self.month, day+1))
                        item.saveRecord()
                db.commit()
            except:
                db.rollback()
                QtGui.qApp.logCurrentException()
                raise


    def loadData(self, orgStructureId, jobTypeId, year, month):
        self.orgStructureId = orgStructureId
        self.jobTypeId = jobTypeId
        self.year = year
        self.month = month
        self.begDate = QDate(year, month, 1)
        self.daysInMonth = self.begDate.daysInMonth()
        calendarInfo = QtGui.qApp.calendarInfo
        self.redDays = []
        for day in xrange(self.daysInMonth):
            date = QDate(year, month, day+1)
            self.redDays.append(calendarInfo.getDayOfWeek(date) in (Qt.Saturday, Qt.Sunday))

        self.items = [ CJobPlanItem() for day in xrange(self.daysInMonth) ]
        db = QtGui.qApp.db
        tableJob = db.table('Job')

        records = db.getRecordList(tableJob, '*',
                                   [tableJob['orgStructure_id'].eq(orgStructureId),
                                    tableJob['jobType_id'].eq(jobTypeId),
                                    tableJob['deleted'].eq(0),
                                    tableJob['date'].ge(self.begDate),
                                    tableJob['date'].lt(self.begDate.addMonths(1)),
                                   ])

        for record in records:
            day = self.begDate.daysTo(forceDate(record.value('date')))
            self.items[day].setRecord(record)
        self.reset()


    def setWorkPlan(self, plan, dateRange):
        (begDate, endDate) = dateRange
        if not begDate:
            begDate = self.begDate
        if not endDate:
            endDate = self.begDate.addDays(self.daysInMonth-1)

        (daysPlan, setRedDays) = plan
        daysPlanLen = len(daysPlan)
        if daysPlanLen<=2:
            for day in xrange(self.begDate.daysTo(begDate), self.begDate.daysTo(endDate)+1):
                if setRedDays or not self.redDays[day]:
                    dayPlan = daysPlan[day%daysPlanLen]
                    self.setDayPlan(day, dayPlan)
        elif daysPlanLen==7:
            for day in xrange(self.begDate.daysTo(begDate), self.begDate.daysTo(endDate)+1):
                dow = self.begDate.addDays(day).dayOfWeek()
                dayPlan = daysPlan[dow-1]
                self.setDayPlan(day, dayPlan)


    def setDayPlan(self, day, dayPlan):
        timeRange, quantity = dayPlan
        dayInfo = self.items[day]
        dayInfo.timeRange = timeRange
        dayInfo.quantity = max(quantity, dayInfo.countUsed())

        self.emitCellChanged(day, 0)
        self.emitCellChanged(day, 1)


    def copyDayFromDate(self, day, sourceDate):
        db = QtGui.qApp.db
        tableJob = db.table('Job')

        record = db.getRecordEx(tableJob, ('begTime', 'endTime','quantity'),
                                [tableJob['orgStructure_id'].eq(self.orgStructureId),
                                 tableJob['jobType_id'].eq(self.jobTypeId),
                                 tableJob['deleted'].eq(0),
                                 tableJob['date'].eq(sourceDate),
                                ])
        if record:
            timeRange = forceTime(record.value('begTime')), forceTime(record.value('endTime'))
            quantity = forceInt(record.value('quantity'))
        else:
            timeRange = None
            quantity = 0
        self.setDayPlan(day, (timeRange, quantity))


    def copyDataFromPrevDate(self, startDate, mode, fillRedDays):
        startDateDow = startDate.dayOfWeek()
        if mode == 0: # один день
            fixedStartDate = startDate.addDays(0 if fillRedDays or startDateDow not in (6, 7)  else 2)
            for day in range(self.daysInMonth):
                if fillRedDays or not self.redDays[day]:
                    self.copyDayFromDate(day, fixedStartDate)
                else:
                    self.setDayPlan(day, (None, 0))

        elif mode == 1: # два дня
            fixedStartDates = [startDate.addDays(0 if fillRedDays or startDateDow not in (6, 7) else 2),
                               startDate.addDays(1 if fillRedDays or startDateDow not in (5, 6) else 3)]
            for day in range(self.daysInMonth):
                if fillRedDays or not self.redDays[day]:
                    self.copyDayFromDate(day, fixedStartDates[day%2])
                else:
                    self.setDayPlan(day, (None, 0))
        else: # mode == 2: # неделя
            for day in range(self.daysInMonth):
                offset = (self.begDate.addDays(day).dayOfWeek() - startDateDow)%7 # yes, it is python '%'
                self.copyDayFromDate(day, startDate.addDays(offset))


    def updateSums(self, column, emitChanges=True):
        pass


    def updateAttrs(self):
        pass


class CTimeRangeItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = CTimeRangeEdit(parent)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setTimeRange(convertVariantToTimeRange(data))


    def setModelData(self, editor, model, index):
        model.setData(index, convertTimeRangeToVariant(editor.timeRange()))



class CJobPlanTable(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)

        self.verticalHeader().show()
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.setTabKeyNavigation(True)
#        self.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed | QtGui.QAbstractItemView.EditKeyPressed | QtGui.QAbstractItemView.SelectedClicked | QtGui.QAbstractItemView.DoubleClicked)
        self.setFocusPolicy(Qt.StrongFocus)
        self.timeRangeDelegate = CTimeRangeItemDelegate(self)
        self.setItemDelegateForColumn(0, self.timeRangeDelegate)

    def setSelectionModel(self, selectionModel):
        currSelectionModel = self.selectionModel()
        if currSelectionModel:
            self.disconnect(currSelectionModel, QtCore.SIGNAL('currentChanged(QModelIndex,QModelIndex))'), self.currentChanged)
        QtGui.QTableView.setSelectionModel(self, selectionModel)
        if selectionModel:
            self.connect(selectionModel, QtCore.SIGNAL('currentChanged(QModelIndex,QModelIndex))'), self.currentChanged)

#    def focusInEvent(self, event):
#        reason = event.reason()
#        model = self.model()
#        if reason in (Qt.TabFocusReason, Qt.ShortcutFocusReason, Qt.OtherFocusReason):
#            if not self.hasFocus():
#                self.setCurrentIndex(model.index(0, 0))
#            self.updateStatusLine(self.currentIndex())
#        elif reason == Qt.BacktabFocusReason:
#            if not self.hasFocus():
#                self.setCurrentIndex(model.index(model.rowCount()-1, model.columnCount()-1))
#            self.updateStatusLine(self.currentIndex())
#        QtGui.QTableView.focusInEvent(self, event)


#    def focusOutEvent(self, event):
#        self.clearStatusLine()
#        QtGui.QTableView.focusOutEvent(self, event)


#    def updateStatusLine(self, index):
#        tipString = forceString(self.model().data(index, Qt.StatusTipRole))
#        self.updateStatusLineStr(tipString)


#    def clearStatusLine(self):
#        self.updateStatusLineStr('')


#    def updateStatusLineStr(self, tipString):
#        self.setStatusTip(tipString)
#        tip = QtGui.QStatusTipEvent(tipString)
#        QtGui.qApp.sendEvent(self.parent(), tip)


#    def currentChanged(self, current, previous):
#        QtGui.QTableView.currentChanged(self, current, previous)
#        self.updateStatusLine(current)


#def getTimePlan(date, begTime, endTime, quantity):
#    if begTime and endTime and quantity>0:
#        begDateTime = QDateTime(date, begTime)
#        t = begTime.secsTo(endTime)
#        if t < 0:
#            t += 84600
#        dt = float(t)/quantity
#        result = [begDateTime.addSecs(dt*i) for i in xrange(quantity)]
#    else:
#        result = []
#    return result


def getTimePlan(timeRange, plan, orgStructureId, allowGaps = True):
    result = []
    if timeRange and plan>0:
        if allowGaps:
            gapList = getGapList(orgStructureId)
        else:
            gapList = []
        fullWorkList = invertGapList(gapList)
        begTime, endTime = timeRange
        result = calcTimePlanForCapacity(begTime, endTime, plan, fullWorkList)
    return result


def getGapList(orgStructureId):
    def addGap(gapList, record):
        bTime = forceTime(record.value('begTime'))
        eTime = forceTime(record.value('endTime'))
        if bTime < eTime:
            gapList.append((bTime, eTime))
        elif bTime > eTime:
            gapList.append((bTime, QTime(23, 59, 59, 999)))
            gapList.append((QTime(0, 0), eTime))

    db = QtGui.qApp.db
    orgStructureBaseId = orgStructureId
    result = []
    orgStructureId = orgStructureBaseId
    while orgStructureId:
        gapRecordList = db.getRecordList('OrgStructure_Gap', 'begTime, endTime',  'master_id=%d' %(orgStructureId), 'begTime, endTime')
        for record in gapRecordList:
            addGap(result, record)
        inheritGaps = forceBool(db.translate('OrgStructure', 'id', orgStructureId, 'inheritGaps'))
#        inheritGaps = forceBool(recordInheritGaps.value(0)) if recordInheritGaps else (False if gapRecordList else True)
        if not inheritGaps:
            break
        orgStructureId = forceRef(db.translate('OrgStructure', 'id', orgStructureId, 'parent_id'))
    result.sort()
    return result
