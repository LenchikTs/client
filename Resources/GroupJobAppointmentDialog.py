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
from PyQt4.QtCore                           import (
                                                    Qt,
                                                    pyqtSignature,
                                                    SIGNAL,
                                                    QDate,
                                                    QDateTime,
                                                    QModelIndex,
                                                    QVariant,
                                                    QAbstractTableModel,
                                                   )

from Events.ActionStatus                    import CActionStatus
from Events.Action                          import CAction, CActionTypeCache
from Events.ActionEditDialog                import CActionEditDialog
from Events.ActionInfo                      import CActionInfoListEx
from Events.EventInfo                       import CEventInfoList
from library.DialogBase                     import CDialogBase
from Reports.ReportBase                     import CReportBase, createTable
from Reports.ReportView                     import CReportViewDialog
from Reports.Utils                          import dateRangeAsStr
from library.PrintInfo                      import CInfoContext
from library.InDocTable                     import (
                                                    CInDocTableModel,
                                                    CEnumInDocTableCol,
                                                    CInDocTableCol,
                                                    forcePyType,
                                                   )
from library.TableModel                     import (
                                                    CTableModel,
                                                    CCol,
                                                    CDateTimeCol,
                                                    CRefBookCol,
                                                    CTextCol,
                                                    CEnumCol,
                                                    CBoolCol,
                                                   )
from library.Utils                          import (
                                                    forceBool,
                                                    forceDateTime,
                                                    forceInt,
                                                    forceRef,
                                                    forceString,
                                                    toVariant,
                                                    formatSex,
                                                    formatShortNameInt,
                                                    copyFields,
                                                      )
from library.PrintTemplates                 import applyTemplate, getPrintButton, getPrintAction
from Resources.JobTicketStatus              import CJobTicketStatus
from Resources.JobTicketInfo                import makeDependentActionIdList, CJobTicketsWithActionsInfoList, CJobInfoList

from Resources.Ui_GroupJobAppointmentDialog import Ui_GroupJobAppointmentDialog


class CGroupJobAppointmentDialog(CDialogBase, Ui_GroupJobAppointmentDialog):
    def __init__(self, parent, eventIdList, actionCache, clientCache):
        CDialogBase.__init__(self, parent)
        self.__id = None
        self.addModels('Events',   CEventsModel(self, actionCache, clientCache))
        self.addModels('Schedule', CScheduleModel(self))
        self.addModels('Group',    CGroupModel(self, clientCache))
        self.addModels('Actions',  CActionsModel(self))
        self.addObject('btnPrint', getPrintButton(self, ''))
        self.addObject('btnAdd',   QtGui.QPushButton(u'Добавить в группу', self))
        self.addObject('btnSave',  QtGui.QPushButton(u'Сохранить', self))
        self.addObject('actEventsPrint', QtGui.QAction(u'Список Контингент', self))
        self.addObject('actSchedulePrint', QtGui.QAction(u'Список Расписание', self))
        self.addObject('actGroupPrint', QtGui.QAction(u'Список Группа', self))
        self.addObject('actActionsPrint', QtGui.QAction(u'Список Назначение', self))
        self.addObject('actJobTicketListPrint', getPrintAction(self, 'groupJobAppointment', u'По контексту', False))
        self.addObject('mnuBtnPrint', QtGui.QMenu(self))
        self.mnuBtnPrint.addAction(self.actEventsPrint)
        self.mnuBtnPrint.addAction(self.actSchedulePrint)
        self.mnuBtnPrint.addAction(self.actGroupPrint)
        self.mnuBtnPrint.addAction(self.actActionsPrint)
        self.mnuBtnPrint.addSeparator()
        self.mnuBtnPrint.addAction(self.actJobTicketListPrint)
        self.btnPrint.setMenu(self.mnuBtnPrint)
        self.setupEventsMenu()
        self.setupGroupMenu()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setObjectName('CGroupJobAppointmentDialog')
        self.setModels(self.tblEvents, self.modelEvents, self.selectionModelEvents)
        self.setModels(self.tblSchedule, self.modelSchedule, self.selectionModelSchedule)
        self.setModels(self.tblGroup, self.modelGroup, self.selectionModelGroup)
        self.setModels(self.tblActions, self.modelActions, self.selectionModelActions)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnAdd, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnSave, QtGui.QDialogButtonBox.ActionRole)
        self.tblEvents.setPopupMenu(self.mnuEvents)
        self.tblGroup.setPopupMenu(self.mnuGroup)
        self.eventIdList = eventIdList
        self.actionCache = actionCache
        self.clientCache = clientCache
        self.jobTicketCache = {}
        self.actionJobTicketCache = {}
        self.clientAddCache = {}
        self.jobCurrentRow = None
        self.isAddToGroup = False
        self.isRemoveFromQueue = False
        self.isFirst = True
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbJobType.setTable('rbJobType', True, filter=u'capacity > 1')
        self.on_cmbJobType_currentIndexChanged(0)
        self.modelEvents.setActionCache(self.actionCache)
        self.tblGroup.addPopupSelectAllRow()
        self.tblGroup.addPopupClearSelectionRow()
        self.modelEvents.setIdList(self.eventIdList)
        self.loadData()
        self.isFirst = False
        self.btnSave.setEnabled(False)
        self.setLblCountEvents()
        self.btnPrint.setEnabled(True)


    def dumpParams(self, cursor, params):
        description = self.getDescription(params)
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getDescription(self, params):
        db = QtGui.qApp.db
        rows = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'За период', begDate, endDate))
        jobTypeId = params.get('jobTypeId', None)
        if jobTypeId:
            rows.append(u'Назначение: ' + forceString(db.translate('rbJobType', 'id', jobTypeId, 'name')))
        orgStructureId = params.get('orgStructureId', None)
        if orgStructureId:
            rows.append(u'\n' + u'Подразделение: ' + forceString(QtGui.qApp.db.translate('OrgStructure', 'id', orgStructureId, 'name')))
        else:
            rows.append(u'\n' + u'ЛПУ')
        actionTypeId = params.get('actionTypeId', None)
        if actionTypeId:
            rows.append(u'Назначение: ' + forceString(db.translate('ActionType', 'id', actionTypeId, 'name')))
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    @pyqtSignature('int')
    def on_actJobTicketListPrint_printByTemplate(self, templateId):
        jobTicketsIdList = self.modelGroup.itemIdList()
        makeDependentActionIdList(jobTicketsIdList)
        context = CInfoContext()
        eventList = context.getInstance(CEventInfoList, self.modelEvents.idList())
        scheduleList = context.getInstance(CJobInfoList, self.modelSchedule.itemIdList())
        jobTicketsInfoList = context.getInstance(CJobTicketsWithActionsInfoList, tuple(jobTicketsIdList))
        actionList = context.getInstance(CActionInfoListEx, self.modelActions.itemIdList())
        data = { 'events'     : eventList,
                 'schedule'   : scheduleList,
                 'jobTickets' : jobTicketsInfoList,
                 'actions'    : actionList
                }
        applyTemplate(self, templateId, data)


    @pyqtSignature('')
    def on_actEventsPrint_triggered(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Контингент')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, self.filter)
        cursor.insertBlock()
        colWidths  = [ self.tblEvents.columnWidth(i) for i in xrange(self.modelEvents.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(self.modelEvents._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(self.modelEvents.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelEvents.columnCount()):
                if iModelCol == 0:
                    text = u''
                    (col, values) = self.modelEvents.getRecordValues(iModelCol, iModelRow)
                    if len(values) > 0:
                        eventId  = forceRef(values[0])
                        if eventId:
                            if self.modelEvents._cols[0].includeCaches.get(eventId, 0):
                                text = u'X'
                else:
                    index = self.modelEvents.createIndex(iModelRow, iModelCol)
                    text = forceString(self.modelEvents.data(index))
                table.setText(iTableRow, iModelCol, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_actSchedulePrint_triggered(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Расписание')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, self.filter)
        cursor.insertBlock()
        colWidths  = [ self.tblSchedule.columnWidth(i) for i in xrange(self.modelSchedule.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(self.modelSchedule.cols()[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(self.modelSchedule.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelSchedule.columnCount()):
                index = self.modelSchedule.createIndex(iModelRow, iModelCol)
                text = forceString(self.modelSchedule.data(index))
                table.setText(iTableRow, iModelCol, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_actGroupPrint_triggered(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Группа')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, self.filter)
        cursor.insertBlock()
        colWidths  = [ self.tblGroup.columnWidth(i) for i in xrange(self.modelGroup.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(self.modelGroup._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(self.modelGroup.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelGroup.columnCount()):
                index = self.modelGroup.createIndex(iModelRow, iModelCol)
                text = forceString(self.modelGroup.data(index))
                table.setText(iTableRow, iModelCol, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_actActionsPrint_triggered(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Назначение')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, self.filter)
        cursor.insertBlock()
        colWidths  = [ self.tblActions.columnWidth(i) for i in xrange(self.modelActions.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(self.modelActions._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(self.modelActions.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelActions.columnCount()):
                index = self.modelActions.createIndex(iModelRow, iModelCol)
                text = forceString(self.modelActions.data(index))
                table.setText(iTableRow, iModelCol, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    def getEventBusy(self):
        count = 0
        for eventId, (clientId, actionId) in self.actionCache.items():
            if clientId and self.clientAddCache.get(clientId, 0):
                count += 1
        return count


    def setLblCountEvents(self):
        self.lblCountEvents.setText(u'Контингент всего: %d.  Контингент в группе: %d'%(len(self.modelEvents.idList()), self.getEventBusy()))


    def setupGroupMenu(self):
        self.addObject('mnuGroup', QtGui.QMenu(self))
        self.addObject('actRemoveFromQueue', QtGui.QAction(u'Удалить из очереди', self))
        self.mnuGroup.addAction(self.actRemoveFromQueue)


    @pyqtSignature('')
    def on_mnuGroup_aboutToShow(self):
        self.actRemoveFromQueue.setEnabled(len(self.modelGroup.items()))


    def setupEventsMenu(self):
        self.addObject('mnuEvents', QtGui.QMenu(self))
        self.addObject('actSelectAllRow', QtGui.QAction(u'Выделить все строки', self))
        self.addObject('actClearSelectionRow', QtGui.QAction(u'Снять выделение', self))
        self.mnuEvents.addAction(self.actSelectAllRow)
        self.mnuEvents.addAction(self.actClearSelectionRow)


    @pyqtSignature('')
    def on_mnuEvents_aboutToShow(self):
        self.actSelectAllRow.setEnabled(len(self.modelEvents.idList()))
        self.actClearSelectionRow.setEnabled(len(self.modelEvents.idList()))


    @pyqtSignature('')
    def on_actSelectAllRow_triggered(self):
        rowCount = self.modelEvents.rowCount()
        for row in xrange(0, rowCount):
            record = self.modelEvents.getRecordByRow(row)
            eventId = forceRef(record.value('id')) if record else None
            if eventId:
                self.modelEvents._cols[0].includeCaches[eventId] = forceBool(Qt.Checked)
        self.modelEvents.reset()


    @pyqtSignature('')
    def on_actClearSelectionRow_triggered(self):
        rowCount = self.modelEvents.rowCount()
        for row in xrange(0, rowCount):
            record = self.modelEvents.getRecordByRow(row)
            eventId = forceRef(record.value('id')) if record else None
            if eventId:
                self.modelEvents._cols[0].includeCaches[eventId] = forceBool(Qt.Unchecked)
        self.modelEvents.reset()


    @pyqtSignature('')
    def on_actRemoveFromQueue_triggered(self):
        self.jobCurrentRow = self.tblSchedule.currentRow()
        rows = self.tblGroup.getSelectedRows()
        self.isRemoveFromQueue = bool(len(rows))
        items = self.modelGroup.items()
        for row in rows:
            if 0 <= row < len(items):
                item = items[row]
                jobTicketId = forceRef(item.value('id'))
                jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                action = jobTicketLine.get('action', None)
                if jobTicketLine.get('clientId', None):
                    if action:
                        action.getRecord().setValue('status', toVariant(CActionStatus.canceled))
                        for property in action.getType()._propertiesById.itervalues():
                            if property.isJobTicketValueType():
                                action[property.name] = None
                        jobTicketLine['action'] = action
                    jobTicketLine['isRemoveFromQueue'] = 1
                    jobTicketLine['isAdd'] = 0
                    clientId = jobTicketLine.get('clientId', None)
                    if clientId:
                        clientCount = self.clientAddCache.get(clientId, 0)
                        self.clientAddCache[clientId] = (clientCount - 1) if clientCount else 0
                    jobTicketLine['clientId'] = None
                    jobTicketLine['eventIdAdd'] = None
                    self.modelGroup.items()[row].setValue('status', toVariant(CJobTicketStatus.wait))
                    self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
                    jobRow = self.tblSchedule.currentRow()
                    jobItems = self.modelSchedule.items
                    if 0 <= jobRow < len(jobItems):
                        self.modelSchedule.items[jobRow][2] += 1
                        self.modelSchedule.items[jobRow][3] -= 1
        self.modelSchedule.reset()
        self.modelGroup.reset()
        self.modelActions.reset()
        self.btnSave.setEnabled((self.isRemoveFromQueue or self.isAddToGroup) and len(self.jobTicketCache) > 0)
        self.tblSchedule.setCurrentRow(self.jobCurrentRow)
        self.modelEvents.setClientAddCache(self.clientAddCache)
        self.modelEvents.reset()


    def eventId(self, index):
        return self.tblEvents.itemId(index)


    def currentEventId(self):
        return self.tblEvents.currentItemId()


    def scheduleId(self, index):
        row = index.row()
        items = self.modelSchedule.items
        if 0 <= row < len(items):
            return items[row][4]
        return None


    def scheduleDateTime(self, index):
        row = index.row()
        items = self.modelSchedule.items
        if 0 <= row < len(items):
            return items[row][0]
        return None


    def currentScheduleId(self):
        return self.tblSchedule.currentItemId()


    def groupId(self, index):
        return forceRef(self.modelGroup.value(index.row(), 'id'))


    def currentGroupId(self):
        return self.tblGroup.currentItemId()


    def actionId(self, index):
        return self.tblActions.itemId(index)


    def currentActionId(self):
        return self.tblActions.currentItemId()


    def setFilter(self):
        self.filter = {}
        self.filter['jobTypeId'] = self.cmbJobType.value()
        self.filter['actionTypeId'] = self.cmbActionType.value()
        self.filter['orgStructureId'] = self.cmbOrgStructure.value()
        self.filter['begDate'] = self.edtBegDate.date()
        self.filter['endDate'] = self.edtEndDate.date()


    def loadData(self):
        jobCurrentRow = self.tblSchedule.currentRow()
        self.setFilter()
        jobIdList = []
        jobTicketIdList = []
        jobCapacityCache = {}
        self.clientAddCache = {}
        if self.cmbJobType.value():
            jobTypeId = self.filter.get('jobTypeId', None)
            actionTypeId = self.filter.get('actionTypeId', None)
            orgStructureId = self.filter.get('orgStructureId', None)
            begDate = self.filter.get('begDate', None)
            endDate = self.filter.get('endDate', None)
            curOrgStructureId = QtGui.qApp.currentOrgStructureId()
            db = QtGui.qApp.db
            tableJob = db.table('Job')
            tableJobTicket = db.table('Job_Ticket')
            tableJobType = db.table('rbJobType')
            tableJobTypeAT = db.table('rbJobType_ActionType')
            tableAPJobTicket = db.table('ActionProperty_Job_Ticket')
            tableActionProperty = db.table('ActionProperty')
            tableAction = db.table('Action')
            tableEvent = db.table('Event')
            tableJobPurpose = db.table('rbJobPurpose')
            tableJobPurposePractice = db.table('rbJobPurpose_Practice')
            queryTable = tableJob.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
            queryTable = queryTable.innerJoin(tableJobType, tableJobType['id'].eq(tableJob['jobType_id']))
            queryTable = queryTable.innerJoin(tableJobTypeAT, tableJobTypeAT['master_id'].eq(tableJobType['id']))
            queryTable = queryTable.leftJoin(tableAPJobTicket, tableAPJobTicket['value'].eq(tableJobTicket['id']))
            queryTable = queryTable.leftJoin(tableActionProperty, db.joinAnd([tableActionProperty['id'].eq(tableAPJobTicket['id']), tableActionProperty['deleted'].eq(0)]))
            queryTable = queryTable.leftJoin(tableAction, db.joinAnd([tableAction['id'].eq(tableActionProperty['action_id']), tableAction['deleted'].eq(0)]))
            queryTable = queryTable.leftJoin(tableEvent, db.joinAnd([tableEvent['id'].eq(tableAction['event_id']), tableEvent['deleted'].eq(0)]))
            queryTable = queryTable.leftJoin(tableJobPurpose, tableJobPurpose['id'].eq(tableJob['jobPurpose_id']))
            queryTable = queryTable.leftJoin(tableJobPurposePractice, tableJobPurposePractice['master_id'].eq(tableJobPurpose['id']))
            cols = [tableJob['id'].alias('jobId'),
                    tableJobTicket['id'].alias('jobTicketId'),
                    tableJob['capacity'],
                    tableJobTicket['status'],
                    tableJobTicket['datetime'],
                    tableAction['id'].alias('actionId')
                    ]
            cond = [tableJob['capacity'].gt(1),
                    tableJob['deleted'].eq(0),
                    tableJobTicket['deleted'].eq(0),
                    ]
            if jobTypeId:
                cond.append(tableJob['jobType_id'].eq(jobTypeId))
            if orgStructureId:
                cond.append(tableJob['orgStructure_id'].eq(orgStructureId))
            if begDate:
                cond.append(tableJob['date'].dateGe(begDate))
            if endDate:
                cond.append(tableJob['date'].dateLe(endDate))
            if actionTypeId:
                cond.append(tableJobTypeAT['actionType_id'].eq(actionTypeId))
                actionTypeGroupIdList = db.getTheseAndParents('ActionType', 'group_id', [actionTypeId])
                if actionTypeGroupIdList:
                    actionTypeSubCond = db.joinOr([tableJobPurposePractice['actionType_id'].isNull(),
                                                   tableJobPurposePractice['actionType_id'].inlist(actionTypeGroupIdList)])
                else:
                    actionTypeSubCond = tableJobPurposePractice['actionType_id'].isNull()
            else:
                actionTypeSubCond = tableJobPurposePractice['actionType_id'].isNull()
            actionTypeSubCond = db.joinXor([actionTypeSubCond, tableJobPurposePractice['excludeActionType'].ne(0)])
            cond.append(db.joinOr([tableJob['jobPurpose_id'].isNull(), actionTypeSubCond]))
            if curOrgStructureId:
                curOrgStructureIdList = db.getTheseAndParents('OrgStructure', 'parent_id', [curOrgStructureId])
                orgStructureSubCond = db.joinOr([tableJobPurposePractice['orgStructure_id'].isNull(),
                                                 tableJobPurposePractice['orgStructure_id'].inlist(curOrgStructureIdList)])
                orgStructureSubCond = db.joinXor([orgStructureSubCond, tableJobPurposePractice['excludeOrgStructure'].ne(0)])
            else:
                orgStructureSubCond = db.joinOr([tableJob['jobPurpose_id'].isNull(), db.joinXor(['1', tableJobPurposePractice['excludeOrgStructure'].ne(0)])])
            cond.append(orgStructureSubCond)
            eventTypeSubCond = db.joinOr([tableEvent['eventType_id'].isNull(),
                                          tableJobPurposePractice['eventType_id'].isNull(),
                                          tableJobPurposePractice['eventType_id'].eq(tableEvent['eventType_id'])])
            eventTypeSubCond = db.joinXor([eventTypeSubCond, tableJobPurposePractice['excludeEventType'].ne(0)])
            cond.append(db.joinOr([tableJob['jobPurpose_id'].isNull(), eventTypeSubCond]))
            cond.append(db.joinOr([tableJob['jobPurpose_id'].isNull(), tableJobPurposePractice['avail'].ne(0)]))
            records = db.getRecordList(queryTable, cols, cond, [tableJob['date'].name(), tableJobTicket['datetime'].name()])
            for record in records:
                jobId = forceRef(record.value('jobId'))
                if jobId and jobId not in jobIdList:
                    jobIdList.append(jobId)
                jobTicketId = forceRef(record.value('jobTicketId'))
                if jobTicketId and jobTicketId not in jobTicketIdList:
                    jobTicketIdList.append(jobTicketId)
                    datetime = forceDateTime(record.value('datetime'))
                    jobCapacityLine = jobCapacityCache.get((jobId, datetime.toString(Qt.LocaleDate)), [None, 0, 0, 0, None])
                    jobCapacityLine[4] = jobId
                    jobCapacityLine[0] = datetime
                    jobCapacityLine[1] = forceInt(record.value('capacity'))
                    #status = forceInt(record.value('status'))
                    jobCapacityLine[2] += (1 if not forceRef(record.value('actionId')) else 0) #(1 if status == CJobTicketStatus.wait else 0)
                    jobCapacityLine[3] += (1 if forceRef(record.value('actionId')) else 0) #(1 if status != CJobTicketStatus.wait else 0)
                    jobCapacityCache[(jobId, datetime.toString(Qt.LocaleDate))] = jobCapacityLine
            jobCapacityItems = jobCapacityCache.values()
            jobCapacityItems.sort(key=lambda x: x[0])
            self.modelSchedule.setItems(jobCapacityItems)
            self.tblSchedule.setCurrentRow(jobCurrentRow)
            self.on_selectionModelGroup_currentRowChanged(self.modelGroup.index(0, 0), self.modelGroup.index(0, 0))
        else:
            self.jobTicketCache = {}
            self.actionJobTicketCache = {}
            self.jobCurrentRow = None
            self.isAddToGroup = False
            self.isRemoveFromQueue = False
            self.btnSave.setEnabled((self.isRemoveFromQueue or self.isAddToGroup) and len(self.jobTicketCache) > 0)
            self.modelSchedule.setItems([])
            self.modelGroup.clearItems()
            self.modelActions.setItems([])


    @pyqtSignature('')
    def on_btnAdd_clicked(self):
        jobId = self.scheduleId(self.tblSchedule.currentIndex())
        self.jobCurrentRow = self.tblSchedule.currentRow()
        actionTypeId = self.cmbActionType.value()
        eventIdList = self.modelEvents.getCheckedEventIdList()
        if jobId and actionTypeId and eventIdList:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            tableJobTicket = db.table('Job_Ticket')
            self.isAddToGroup = True
            self.btnPrint.setEnabled(False)
            jobTicketIdList = self.jobTicketCache.keys()
            jobTicketIdList.sort()
            notAddJobTicketIdList = []
            for jobTicketIdKey in jobTicketIdList:
                jobTicketLine = self.jobTicketCache.get(jobTicketIdKey, {})
                jobTicketId, row = jobTicketIdKey
                if not jobTicketLine.get('isAdd', 0) and not jobTicketLine.get('clientId', None) and jobTicketId and jobTicketId not in notAddJobTicketIdList:
                    notAddJobTicketIdList.append(jobTicketId)
            countJobTicketId = len(notAddJobTicketIdList)
            countEventId = len(eventIdList)
            if countJobTicketId < countEventId and self.checkAddValueMessage():
                joibId = self.scheduleId(self.tblSchedule.currentIndex())
                if joibId:
                    jobTicketId = jobTicketIdList[len(jobTicketIdList)-1][0]
                    if jobTicketId:
                        record = db.getRecordEx(tableJobTicket, '*', [tableJobTicket['id'].eq(jobTicketId), tableJobTicket['deleted'].eq(0)])
                        if record:
                            count = countEventId - countJobTicketId
                            newItems = []
                            for i in xrange(0, count):
                                newRecord = tableJobTicket.newRecord()
                                copyFields(newRecord, record)
                                newRecord.setValue('id', toVariant(None))
                                newRecord.setValue('idx', toVariant(forceInt(record.value('idx'))+1))
                                newItems.append(newRecord)
                                jTKey = (None, (len(self.modelGroup.items())+i))
                                jobTicketLine = self.jobTicketCache.get(jTKey, {})
                                jobTicketLine['clientId'] = None
                                jobTicketLine['datetime'] = forceDateTime(record.value('datetime'))
                                jobTicketLine['isAdd'] = 0
                                jobTicketLine['isRemoveFromQueue'] = 0
                                self.jobTicketCache[jTKey] = jobTicketLine
                            self.modelGroup._items.extend(newItems)
            items = self.modelGroup.items()
            for row, eventId in enumerate(eventIdList):
                for i, item in enumerate(items):
                    jobTicketId = forceRef(item.value('id'))
                    jobTicketLine = self.jobTicketCache.get((jobTicketId, i), {})
                    if not jobTicketLine.get('isAdd', 0) and not jobTicketLine.get('clientId', None):
                        clientId, actionId = self.actionCache.get(eventId, (None, None))
                        jobTicketLine['clientId'] = clientId
                        jobTicketLine['isAdd'] = 1
                        datetime = jobTicketLine.get('datetime', None)
                        self.modelGroup.items()[i].setValue('status', toVariant(CJobTicketStatus.wait))
                        newRecord = tableAction.newRecord()
                        newRecord.setValue('id', toVariant(None))
                        newRecord.setValue('idx', toVariant(0))
                        newRecord.setValue('createDatetime',  toVariant(QDateTime.currentDateTime()))
                        newRecord.setValue('createPerson_id', toVariant(QtGui.qApp.userId))
                        newRecord.setValue('modifyDatetime',  toVariant(QDateTime.currentDateTime()))
                        newRecord.setValue('modifyPerson_id', toVariant(QtGui.qApp.userId))
                        newRecord.setValue('actionType_id',   toVariant(actionTypeId))
                        newRecord.setValue('event_id',        toVariant(eventId))
                        newRecord.setValue('setPerson_id',    toVariant(QtGui.qApp.userId))
                        newRecord.setValue('directionDate',   toVariant(QDateTime.currentDateTime()))
                        newRecord.setValue('plannedEndDate',  toVariant(datetime))
                        newRecord.setValue('org_id',          toVariant(QtGui.qApp.currentOrgId()))
                        newRecord.setValue('status',          toVariant(CActionStatus.appointed))
                        newRecord.setValue('begDate',         toVariant(datetime))
                        actionType = CActionTypeCache.getById(actionTypeId)
                        newAction = CAction(actionType=actionType, record=newRecord)
                        if jobTicketId:
                            for property in newAction.getType()._propertiesById.itervalues():
                                if property.isJobTicketValueType():
                                    newAction[property.name] = jobTicketId
                        jobTicketLine['action'] = newAction
                        jobTicketLine['eventIdAdd'] = eventId
                        if clientId:
                            self.clientAddCache[clientId] = 1 + self.clientAddCache.get(clientId, 0)
                        self.jobTicketCache[(jobTicketId, i)] = jobTicketLine
                        newRecords = self.actionJobTicketCache.get((jobTicketId, i), [])
                        newRecords.append(newRecord)
                        self.actionJobTicketCache[(jobTicketId, i)] = newRecords
                        jobRow = self.tblSchedule.currentRow()
                        jobItems = self.modelSchedule.items
                        if 0 <= jobRow < len(jobItems):
                            self.modelSchedule.items[jobRow][2] -= 1
                            self.modelSchedule.items[jobRow][3] += 1
                        break
            self.modelSchedule.reset()
            self.modelGroup.reset()
            self.modelActions.reset()
            self.btnSave.setEnabled((self.isRemoveFromQueue or self.isAddToGroup) and len(self.jobTicketCache) > 0)
            self.tblSchedule.setCurrentRow(self.jobCurrentRow)
            self.modelEvents.setClientAddCache(self.clientAddCache)
            self.modelEvents.reset()


    def checkAddValueMessage(self):
        message = u'Свободные номерки на работу заканчились! Создать сверхплановые номерки на работу?'
        buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        res = QtGui.QMessageBox.warning( self,
                                         u'Внимание!',
                                         message,
                                         buttons,
                                         QtGui.QMessageBox.Yes)
        if res == QtGui.QMessageBox.Yes:
            return True
        elif res == QtGui.QMessageBox.No:
            return False


    @pyqtSignature('')
    def on_btnSave_clicked(self):
        if (self.isRemoveFromQueue or self.isAddToGroup) and len(self.jobTicketCache) > 0:
            items = self.modelGroup.items()
            db = QtGui.qApp.db
            tableJobTicket = db.table('Job_Ticket')
            if self.isAddToGroup:
                for row, item in enumerate(items):
                    jobTicketId = forceRef(item.value('id'))
                    jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                    action = jobTicketLine.get('action', None)
                    if not jobTicketLine.get('isRemoveFromQueue', 0) and jobTicketLine.get('isAdd', 0) and jobTicketLine.get('clientId', None) and action:
                        if jobTicketId:
                            action.save(idx=-1)
                            db.updateRecord(tableJobTicket, item)
                        else:
                            jobTicketId = db.insertOrUpdate(tableJobTicket, item)
                            if jobTicketId:
                                for property in action.getType()._propertiesById.itervalues():
                                    if property.isJobTicketValueType():
                                        action[property.name] = jobTicketId
                                action.save(idx=-1)
                        jobTicketLine['action'] = action
                        jobTicketLine['isAdd'] = 0
                        self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
            if self.isRemoveFromQueue:
                for row, item in enumerate(items):
                    jobTicketId = forceRef(item.value('id'))
                    jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                    if jobTicketLine.get('isRemoveFromQueue', 0):
                        action = jobTicketLine.get('action', None)
                        if action:
                            action.getRecord().setValue('status', toVariant(CActionStatus.canceled))
                            for property in action.getType()._propertiesById.itervalues():
                                if property.isJobTicketValueType():
                                    action[property.name] = None
                            action.save(idx=-1)
                        actionIdList = jobTicketLine.get('actionIdList', [])
                        if actionIdList:
                            tableAction = db.table('Action')
                            records = db.getRecordList(tableAction, '*', [tableAction['id'].inlist(actionIdList), tableAction['deleted'].eq(0)])
                            for record in records:
                                record.setValue('status', toVariant(CActionStatus.canceled))
                                action = CAction(record=record)
                                if action:
                                    for property in action.getType()._propertiesById.itervalues():
                                        if property.isJobTicketValueType():
                                            action[property.name] = None
                                    action.save(idx=-1)
                        if jobTicketId:
                            db.updateRecord(tableJobTicket, item)
                        jobTicketLine['action'] = action if jobTicketId else None
                        jobTicketLine['isRemoveFromQueue'] = 0
                        jobTicketLine['isAdd'] = 0
                        jobTicketLine['clientId'] = None
                        self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
        self.isAddToGroup = False
        self.isRemoveFromQueue = False
        self.actionJobTicketCache = {}
        self.btnSave.setEnabled(False)
        self.jobCurrentRow = None
        self.loadData()
        self.btnPrint.setEnabled(True)


    def checkAddValue(self, previous=None):
        if (self.isRemoveFromQueue or self.isAddToGroup) and len(self.jobTicketCache) > 0:
            message = u'В группу были внесены изменения! Сохранить?'
            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
            res = QtGui.QMessageBox.warning( self,
                                             u'Внимание!',
                                             message,
                                             buttons,
                                             QtGui.QMessageBox.Yes)
            if res == QtGui.QMessageBox.Yes:
                self.on_btnSave_clicked()
                return True
            elif res == QtGui.QMessageBox.No:
                items = self.modelGroup.items()
                if self.isAddToGroup:
                    for row, item in enumerate(items):
                        jobTicketId = forceRef(item.value('id'))
                        jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                        action = jobTicketLine.get('action', None)
                        if not jobTicketLine.get('isRemoveFromQueue', 0) and jobTicketLine.get('isAdd', 0) and jobTicketLine.get('clientId', None) and action:
                            self.modelGroup.items()[row].setValue('status', toVariant(CJobTicketStatus.wait))
                            jobTicketLine['action'] = None
                            jobTicketLine['isAdd'] = 0
                            clientId = jobTicketLine.get('clientId', None)
                            if clientId:
                                clientAddCount = self.clientAddCache.get(clientId, 0)
                                self.clientAddCache[clientId] = (clientAddCount - 1) if clientAddCount else 0
                            jobTicketLine['eventIdAdd'] = None
                            jobTicketLine['clientId'] = None
                            self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
                            if previous and previous.isValid():
                                jobRow = previous.row()
                            else:
                                jobRow = self.tblSchedule.currentRow()
                            jobItems = self.modelSchedule.items
                            if 0 <= jobRow < len(jobItems):
                                self.modelSchedule.items[jobRow][2] += 1
                                self.modelSchedule.items[jobRow][3] -= 1
                if self.isRemoveFromQueue:
                    for row, item in enumerate(items):
                        jobTicketId = forceRef(item.value('id'))
                        jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                        if jobTicketLine.get('isRemoveFromQueue', 0):
                            self.modelGroup.items()[row].setValue('status', toVariant(CJobTicketStatus.wait))
                            jobTicketLine['isRemoveFromQueue'] = 0
                            jobTicketLine['isAdd'] = 0
                            eventId = jobTicketLine.get('eventId', None)
                            if eventId:
                                db = QtGui.qApp.db
                                tableEvent = db.table('Event')
                                recordEvent = db.getRecordEx(tableEvent, [tableEvent['client_id']], [tableEvent['id'].eq(eventId), tableEvent['deleted'].eq(0)])
                                clientId = forceRef(recordEvent.value('client_id')) if recordEvent else None
                                jobTicketLine['clientId'] = clientId
                                if clientId:
                                    clientAddCount = self.clientAddCache.get(clientId, 0)
                                    self.clientAddCache[clientId] = clientAddCount + 1
                            self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
                            if previous and previous.isValid():
                                jobRow = previous.row()
                            else:
                                jobRow = self.tblSchedule.currentRow()
                            jobItems = self.modelSchedule.items
                            if 0 <= jobRow < len(jobItems):
                                self.modelSchedule.items[jobRow][2] -= 1
                                self.modelSchedule.items[jobRow][3] += 1
                self.isAddToGroup = False
                self.isRemoveFromQueue = False
                self.actionJobTicketCache = {}
                self.btnSave.setEnabled(False)
                self.jobCurrentRow = None
                self.modelEvents.setClientAddCache(self.clientAddCache)
                self.modelEvents.reset()
                return False
        return True


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Close:
            self.checkAddValue()
            self.close()


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        if not self.isFirst:
            self.checkAddValue()
            self.loadData()


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        if not self.isFirst:
            self.checkAddValue()
            self.loadData()


    @pyqtSignature('int')
    def on_cmbJobType_currentIndexChanged(self, index):
        if not self.isFirst:
            self.checkAddValue()
        orgStructureFilter = u'0'
        orgStructureIdList = []
        db = QtGui.qApp.db
        tableJobTypeAT = db.table('rbJobType_ActionType')
        jobTypeId = forceRef(self.cmbJobType.value())
        if jobTypeId:
            actionTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['actionType_id']], [tableJobTypeAT['master_id'].eq(jobTypeId)], tableJobTypeAT['id'].name())
            begDate = self.edtBegDate.date()
            endDate = self.edtEndDate.date()
            actionTypeId = self.cmbActionType.value()
            tableJob = db.table('Job')
            tableJobTicket = db.table('Job_Ticket')
            tableJobType = db.table('rbJobType')
            tableJobTypeAT = db.table('rbJobType_ActionType')
            tableOS = db.table('OrgStructure')
            queryTable = tableJob.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
            queryTable = queryTable.innerJoin(tableJobType, tableJobType['id'].eq(tableJob['jobType_id']))
            queryTable = queryTable.innerJoin(tableJobTypeAT, tableJobTypeAT['master_id'].eq(tableJobType['id']))
            queryTable = queryTable.innerJoin(tableOS, tableOS['id'].eq(tableJob['orgStructure_id']))
            cond = [tableJob['capacity'].gt(1),
                    tableJob['deleted'].eq(0),
                    tableJobTicket['deleted'].eq(0),
                    tableJob['orgStructure_id'].isNotNull(),
                    tableOS['deleted'].eq(0),
                    ]
            if jobTypeId:
                cond.append(tableJob['jobType_id'].eq(jobTypeId))
            if begDate:
                cond.append(tableJob['date'].dateGe(begDate))
            if endDate:
                cond.append(tableJob['date'].dateLe(endDate))
            if actionTypeId:
                cond.append(tableJobTypeAT['actionType_id'].eq(actionTypeId))
            orgStructureIdList = db.getDistinctIdList(queryTable, [tableJob['orgStructure_id']], cond, [tableJob['date'].name(), tableOS['name'].name()])
            if orgStructureIdList:
                orgStructureFilter = u'id IN (%s)'%(u','.join(forceString(orgStructureId) for orgStructureId in orgStructureIdList if orgStructureId))
            self.cmbActionType.setActionTypeIdList(actionTypeIdList)
            actionTypeId = actionTypeIdList[0] if len(actionTypeIdList) > 0 else None
            self.cmbActionType.setValue(actionTypeId)
        else:
            actionTypeIdList = db.getDistinctIdList(tableJobTypeAT, [tableJobTypeAT['actionType_id']], [tableJobTypeAT['actionType_id'].isNotNull()], tableJobTypeAT['id'].name())
            self.cmbActionType.setActionTypeIdList(actionTypeIdList)
        self.cmbOrgStructure.setFilter(orgStructureFilter)
        self.cmbOrgStructure.setValue(orgStructureIdList[0] if len(orgStructureIdList) else None)
        if not self.isFirst:
            self.loadData()


    @pyqtSignature('int')
    def on_cmbActionType_currentIndexChanged(self, index):
        if not self.isFirst:
            self.checkAddValue()
            self.loadData()


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        if not self.isFirst:
            self.checkAddValue()
#        self.cmbActionType.setOrgStructure(self.cmbOrgStructure.value())
#        self.cmbActionType.setValue(None)
        if not self.isFirst:
            self.loadData()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelSchedule_currentRowChanged(self, current, previous):
        if self.jobCurrentRow is None or (current.isValid() and current.row() != self.jobCurrentRow):
            self.checkAddValue(previous)
            scheduleId = self.scheduleId(current)
            scheduleDateTime = self.scheduleDateTime(current)
            self.jobTicketCache = {}
            self.clientAddCache = {}
            if scheduleId:
                jobTicketIdList = []
                db = QtGui.qApp.db
                tableJob = db.table('Job')
                tableJobTicket = db.table('Job_Ticket')
                tableAPJobTicket = db.table('ActionProperty_Job_Ticket')
                tableActionProperty = db.table('ActionProperty')
                tableEvent = db.table('Event')
                tableAction = db.table('Action')
                queryTable = tableJob.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
                queryTable = queryTable.leftJoin(tableAPJobTicket, tableAPJobTicket['value'].eq(tableJobTicket['id']))
                queryTable = queryTable.leftJoin(tableActionProperty, db.joinAnd([tableActionProperty['id'].eq(tableAPJobTicket['id']), tableActionProperty['deleted'].eq(0)]))
                queryTable = queryTable.leftJoin(tableAction, db.joinAnd([tableAction['id'].eq(tableActionProperty['action_id']), tableAction['deleted'].eq(0)]))
                queryTable = queryTable.leftJoin(tableEvent, db.joinAnd([tableEvent['id'].eq(tableAction['event_id']), tableEvent['deleted'].eq(0)]))
                cols = [tableJob['id'].alias('jobId'),
                        tableJobTicket['id'].alias('jobTicketId'),
                        tableJob['capacity'],
                        tableJobTicket['status'],
                        tableJobTicket['datetime'],
                        tableEvent['client_id'],
                        tableEvent['id'].alias('eventId'),
                        tableAction['id'].alias('actionId')
                        ]
                cond = [tableJob['id'].eq(scheduleId),
                        tableJobTicket['datetime'].eq(scheduleDateTime),
                        tableJob['capacity'].gt(1),
                        tableJob['deleted'].eq(0),
                        tableJobTicket['deleted'].eq(0),
                        ]
                records = db.getRecordList(queryTable, cols, cond, tableJobTicket['datetime'].name())
                for row, record in enumerate(records):
                    jobTicketId = forceRef(record.value('jobTicketId'))
                    if jobTicketId and jobTicketId not in jobTicketIdList:
                        jobTicketIdList.append(jobTicketId)
                        jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                        clientId = forceRef(record.value('client_id'))
                        jobTicketLine['clientId'] = clientId
                        jobTicketLine['datetime'] = forceDateTime(record.value('datetime'))
                        actionId = forceRef(record.value('actionId'))
                        actionIdList = jobTicketLine.get('actionIdList', [])
                        if actionId and actionId not in actionIdList:
                            actionIdList.append(actionId)
                            jobTicketLine['actionIdList'] = actionIdList
                        jobTicketLine['isAdd'] = 0
                        jobTicketLine['isRemoveFromQueue'] = 0
                        eventId = forceRef(record.value('eventId'))
                        jobTicketLine['eventId'] = eventId
                        if clientId:
                            self.clientAddCache[clientId] = 1 + self.clientAddCache.get(clientId, 0)
                        self.jobTicketCache[(jobTicketId, row)] = jobTicketLine
                if jobTicketIdList:
                    self.modelGroup.setFilter(u'id IN (%s)'%(u','.join(forceString(jobTicketId) for jobTicketId in jobTicketIdList if jobTicketId)))
                else:
                    self.modelGroup.setFilter(u'0')
                self.modelGroup.setJobTicketCache(self.jobTicketCache)
                self.modelGroup.loadItems(scheduleId)
                self.on_selectionModelGroup_currentRowChanged(self.modelGroup.index(0, 0), self.modelGroup.index(0, 0))
                self.modelEvents.setClientAddCache(self.clientAddCache)
                self.modelEvents.reset()
        self.setLblCountEvents()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelGroup_currentRowChanged(self, current, previous):
        groupId = self.groupId(current)
        jobTicketLine = self.jobTicketCache.get((groupId, current.row()), {})
        actionIdList = jobTicketLine.get('actionIdList', [])
        self.modelActions.loadData(actionIdList)
        newRecords = self.actionJobTicketCache.get((groupId, current.row()), [])
        if newRecords:
            self.modelActions.items.extend(newRecords)
            self.modelActions.reset()


    @pyqtSignature('QModelIndex')
    def on_tblActions_doubleClicked(self, index):
        self.editAction(self.modelActions.getItemId(self.tblActions.currentIndex()))


    def editAction(self, actionId):
        if actionId:
            dialog = CActionEditDialog(self)
            try:
                dialog.load(actionId)
                if dialog.exec_():
                    return dialog.itemId()
            finally:
                dialog.deleteLater()


class CEventsModel(CTableModel):
    class CLocClientColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                   forceString(clientRecord.value('firstName')),
                   forceString(clientRecord.value('patrName')))
                return toVariant(name)
            return CCol.invalid

    class CLocClientBirthDateColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache, extraFields=[]):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.extraFields = extraFields
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                return toVariant(forceString(clientRecord.value('birthDate')))
            return CCol.invalid

    class CLocClientSexColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache, extraFields=[]):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.extraFields = extraFields
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                return toVariant(formatSex(clientRecord.value('sex')))
            return CCol.invalid

    class CLocIncludeColumn(CBoolCol):
        def __init__(self, title, fields, defaultWidth, extraFields=[]):
            CBoolCol.__init__(self, title, fields, defaultWidth, 'l')
            self.extraFields = extraFields
            self.includeCaches = {}

        def format(self, values):
            return CCol.invalid

        def getIncludeCaches(self):
            return self.includeCaches

        def checked(self, values):
            val = values[0]
            eventId  = forceRef(val)
            if eventId:
                include = self.includeCaches.get(eventId, 0)
                val = CBoolCol.valChecked if forceBool(include) else CBoolCol.valUnchecked
                self.includeCaches[eventId] = forceBool(val)
                return val
            else:
                return CCol.invalid

    def __init__(self, parent, actionCache, clientCache):
        CTableModel.__init__(self, parent)
        includeCol = CEventsModel.CLocIncludeColumn(u'Включить', ['id'], 5, ['include'])
        clientCol   = CEventsModel.CLocClientColumn( u'Ф.И.О.', ['client_id'], 60, clientCache)
        clientBirthDateCol = CEventsModel.CLocClientBirthDateColumn(u'Дата рожд.', ['client_id'], 20, clientCache, ['birthDate'])
        clientSexCol = CEventsModel.CLocClientSexColumn(u'Пол', ['client_id'], 5, clientCache, ['sex'])
        self.addColumn(includeCol)
        self.addColumn(clientCol)
        self.addColumn(CTextCol(u'Код пациента', ['client_id'], 30))
        self.addColumn(clientBirthDateCol)
        self.addColumn(clientSexCol)
        self.clientAddCache = {}
        #self.addColumn(CEventsModel.CLocOrgStructureColumn(u'Подразделение прибывания', ['id'], 7, ['orgStructure_id'], actionCache))
        self.setTable('Event')


    def setClientAddCache(self, clientAddCache):
        self.clientAddCache = clientAddCache


    def setActionCache(self, actionCache):
        self.actionCache = actionCache


    def flags(self, index=None):
        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        column = index.column()
        row    = index.row()
        if role == Qt.DisplayRole:
            (col, values) = self.getRecordValues(column, row)
            return col.format(values)
        elif role == Qt.TextAlignmentRole:
           col = self._cols[column]
           return col.alignment()
        elif role == Qt.CheckStateRole:
            (col, values) = self.getRecordValues(column, row)
            return col.checked(values)
        elif role == Qt.ForegroundRole:
            (col, values) = self.getRecordValues(column, row)
            return col.getForegroundColor(values)
        elif role == Qt.BackgroundRole:
            (col, values) = self.getRecordValues(column, row)
            return col.getBackgroundColor(values)
        elif role == Qt.FontRole:
            record = self.getRecordByRow(row)
            eventId = forceRef(record.value('id')) if record else None
            clientId, actionId = self.actionCache.get(eventId, (None, None))
            if clientId and self.clientAddCache.get(clientId, 0):
                result = QtGui.QFont()
                result.setBold(True)
                return QVariant(result)
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole:
            if column == 0:
                record = self.getRecordByRow(row)
                eventId = forceRef(record.value('id')) if record else None
                if eventId:
                    self._cols[column].includeCaches[eventId] = forceInt(value) == Qt.Checked
            self.emitDataChanged(row, column)
            return True
        return False


    def getCheckedEventIdList(self):
        checkedEventIdList = []
        includeCaches = self._cols[0].getIncludeCaches()
        for eventId, include in includeCaches.items():
            if include and eventId and eventId not in checkedEventIdList:
                checkedEventIdList.append(eventId)
        return checkedEventIdList


    def emitDataChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


class CScheduleModel(QAbstractTableModel):
    __pyqtSignals__ = ('itemsCountChanged(int)',
                      )
    column = [u'Дата', u'План', u'Свободно', u'Занято']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self._cols = []
        self.items = []


    def columnCount(self, index = None):
        return 4


    def rowCount(self, index = None):
        return len(self.items)


    def addColumn(self, col):
        self._cols.append(col)
        return col


    def cols(self):
        self._cols = self.column
        return self._cols


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def setItems(self, items):
        self.items = items
        self.reset()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            return toVariant(self.items[row][column])
        return QVariant()


    def itemIdList(self):
        idList = []
        for item in self.items:
            idList.append(item[4])
        return idList


class CGroupModel(CInDocTableModel):
    Col_Number     = 0
    Col_Client     = 1
    Col_Date       = 2
    Col_Status     = 3


    class CLocClientColumn(CInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CInDocTableCol.__init__(self, title, fieldName, width, **params)
            self.clientCache  = params.get('clientCaches', [])
            self.jobTicketCache = {}

        def setJobTicketCache(self, jobTicketCache):
            self.jobTicketCache = jobTicketCache

        def toString(self, val, record, row):
            jobTicketId  = forceRef(val)
            jobTicketCache = self.jobTicketCache.get((jobTicketId, row), {})
            clientId = jobTicketCache.get('clientId', None)
            if clientId:
                clientRecord = self.clientCache.get(clientId) if clientId else None
                if clientRecord:
                    birthDate = forceString(clientRecord.value('birthDate'))
                    sex = formatSex(clientRecord.value('sex'))
                    id = forceString(clientRecord.value('id'))
                    name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                       forceString(clientRecord.value('firstName')),
                       forceString(clientRecord.value('patrName'))) + u', '.join(n for n in [birthDate, sex, id] if n)
                    return toVariant(name)
            return QVariant()

        def toSortString(self, val, record, row):
            return forcePyType(self.toString(val, record, row))

        def toStatusTip(self, val, record, row):
            return self.toString(val, record, row)

        def setEditorData(self, editor, value, record):
            editor.setValue(forceRef(value))

        def getEditorData(self, editor):
            return toVariant(editor.value())

        def alignment(self):
            return QVariant(Qt.AlignLeft + Qt.AlignTop)


    def __init__(self, parent, clientCache):
        CInDocTableModel.__init__(self, 'Job_Ticket', 'id', 'master_id', parent)
        self.addCol(CInDocTableCol(u'№', 'id', 5)).setReadOnly(True)
        self.addCol(CGroupModel.CLocClientColumn(u'Ф.И.О.', 'id', 30, clientCaches=clientCache)).setReadOnly(True)
        #self.addCol(CDateTimeInDocTableCol(u'Дата', 'datetime',  10)).setReadOnly()
        self.addCol(CEnumInDocTableCol(u'Состояние', 'status', 10, CJobTicketStatus.names)).setReadOnly()
        self.setEnableAppendLine(False)
        self.jobTicketCache = {}


    def setJobTicketCache(self, jobTicketCache):
        self.jobTicketCache = jobTicketCache
        self._cols[CGroupModel.Col_Client].setJobTicketCache(self.jobTicketCache)


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self._items):
            if role == Qt.EditRole:
                col = self._cols[column]
                record = self._items[row]
                return record.value(col.fieldName())
            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self._items[row]
                if column == CGroupModel.Col_Number:
                    return col.toString(row+1, record)
                elif column == CGroupModel.Col_Client:
                    return col.toString(record.value(col.fieldName()), record, row)
                else:
                    return col.toString(record.value(col.fieldName()), record)
            if role == Qt.StatusTipRole:
                col = self._cols[column]
                record = self._items[row]
                if column == CGroupModel.Col_Client:
                    return col.toStatusTip(record.value(col.fieldName()), record, row)
                else:
                    return col.toStatusTip(record.value(col.fieldName()), record)
            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()
            if role == Qt.CheckStateRole:
                col = self._cols[column]
                record = self._items[row]
                return col.toCheckState(record.value(col.fieldName()), record)
            if role == Qt.ForegroundRole:
                col = self._cols[column]
                record = self._items[row]
                return col.getForegroundColor(record.value(col.fieldName()), record)
            if role == Qt.FontRole:
                if column == CGroupModel.Col_Client:
                    jobTicketId = forceRef(self._items[row].value('id'))
                    jobTicketLine = self.jobTicketCache.get((jobTicketId, row), {})
                    if jobTicketLine.get('isAdd', 0):
                        result = QtGui.QFont()
                        result.setBold(True)
                        return QVariant(result)
        return QVariant()


class CItemsTableModel(QAbstractTableModel):
    __pyqtSignals__ = ('itemsCountChanged(int)',
                      )

    def __init__(self, parent, cols=[], tableName=''):
        QAbstractTableModel.__init__(self, parent)
        self._cols = []
        self.items = []
        self._table = None
        self._cols.extend(cols)
        if tableName:
            self.setTable(tableName)


    def columnCount(self, index = None):
        return len(self._cols)


    def rowCount(self, index = None):
        return len(self.items)


    def addColumn(self, col):
        self._cols.append(col)
        return col


    def cols(self):
        return self._cols


    def setItems(self, items):
        self.items = items
        self.reset()


    def setTable(self, table):
        db = QtGui.qApp.db
        self._table = db.forceTable(table)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._cols):
                    return self._cols[section].title()
            if role == Qt.ToolTipRole:
                return self._cols[section].toolTip()
            if role == Qt.WhatsThisRole:
                return self._cols[section].whatsThis()
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self.items):
            if role == Qt.DisplayRole:
                col = self._cols[column]
                val = self.items[row][column]
                return col.format(val, None)
            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()
            if role == Qt.CheckStateRole:
                col = self._cols[column]
                val = self.items[row][column]
                return col.checked(val, None)
            elif role == Qt.ForegroundRole:
                col = self._cols[column]
                val = self.items[row][column]
                return col.getForegroundColor(val, None)
            if role == Qt.ForegroundRole:
                col = self._cols[column]
                val = self.items[row][column]
                return col.getForegroundColor(val, None)
        return QVariant()


class CRecordsTableModel(QAbstractTableModel):
    __pyqtSignals__ = ('itemsCountChanged(int)',
                      )

    def __init__(self, parent, cols=[], tableName=''):
        QAbstractTableModel.__init__(self, parent)
        self._cols = []
        self.items = []
        self._table = None
        self._cols.extend(cols)
        if tableName:
            self.setTable(tableName)


    def columnCount(self, index = None):
        return len(self._cols)


    def rowCount(self, index = None):
        return len(self.items)


    def addColumn(self, col):
        self._cols.append(col)
        return col


    def cols(self):
        return self._cols


    def items(self):
        return self.items


    def setItems(self, items):
        self.items = items
        self.reset()


    def setTable(self, table):
        db = QtGui.qApp.db
        self._table = db.forceTable(table)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._cols):
                    return self._cols[section].title()
            if role == Qt.ToolTipRole:
                return self._cols[section].toolTip()
            if role == Qt.WhatsThisRole:
                return self._cols[section].whatsThis()
        return QVariant()


    def insertRecord(self, row, record):
        self.beginInsertRows(QModelIndex(), row, row)
        self.items.insert(row, record)
        self.endInsertRows()


    def addRecord(self, record):
        self.insertRecord(len(self.items), record)


    def removeRows(self, row, count, parentIndex = QModelIndex()):
        if 0 <= row and row+count <= len(self.items):
            self.beginRemoveRows(parentIndex, row, row+count-1)
            del self.items[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self.items):
            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self.items[row]
                return col.format([record.value(col.fields()[0]), record])
            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()
            if role == Qt.CheckStateRole:
                col = self._cols[column]
                record = self.items[row]
                return col.checked([record.value(col.fields()[0]), record])
            elif role == Qt.ForegroundRole:
                col = self._cols[column]
                record = self.items[row]
                return col.getForegroundColor([record.value(col.fields()[0]), record])
            if role == Qt.ForegroundRole:
                col = self._cols[column]
                record = self.items[row]
                return col.getForegroundColor([record.value(col.fields()[0]), record])
        return QVariant()


    def loadData(self, actionIdList):
        self.items = []
        if actionIdList:
            db = QtGui.qApp.db
            table = self._table
            tableActionType = db.table('ActionType')
            queryTable = table.innerJoin(tableActionType, tableActionType['id'].eq(table['actionType_id']))
            cond = [table['id'].inlist(actionIdList),
                    table['deleted'].eq(0)
                   ]
            self.items = db.getRecordList(queryTable, 'Action.*', cond, [tableActionType['name'].name(), table['directionDate'].name()])
        self.reset()


    def getItemId(self, index):
        if index and index.isValid():
            row = index.row()
            if 0 <= row < len(self.items):
                return forceRef(self.items[row].value('id'))
        return None


    def itemIdList(self):
        idList = []
        for item in self.items:
            idList.append(forceRef(item.value('id')))
        return idList


    def getActionTypeId(self, index):
        if index and index.isValid():
            row = index.row()
            if 0 <= row < len(self.items):
                return forceRef(self.items[row].value('actionType_id'))
        return None


    def getRecord(self, index):
        if index and index.isValid():
            row = index.row()
            if 0 <= row < len(self.items):
                return self.items[row]
        return None


class CActionsModel(CRecordsTableModel):
    def __init__(self, parent):
        CRecordsTableModel.__init__(self, parent)
        self.addColumn(CRefBookCol(u'Тип',  ['actionType_id'], 'ActionType', 15))
        self.addColumn(CEnumCol(u'Статус выполнения', ['status'], CActionStatus.names, 10))
        self.addColumn(CRefBookCol(u'Назначивший',  ['setPerson_id'], 'vrbPersonWithSpeciality', 15))
        self.addColumn(CDateTimeCol(u'Назначено',  ['directionDate'], 15))
        self.setTable('Action')


def getGroupJobAppointmentContext():
    return ['groupJobAppointment']
