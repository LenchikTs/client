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
##
## Назначение мероприятий по циклам
##
#############################################################################
import math

from PyQt4 import QtGui
from PyQt4.QtCore                           import (
                                                    Qt,
                                                    pyqtSignature,
                                                    SIGNAL,
                                                    QDate,
                                                    QDateTime,
                                                    QTime,
                                                    QModelIndex,
                                                    QVariant,
                                                    QAbstractTableModel,
                                                   )

from Events.ActionStatus                    import CActionStatus
from Events.Action                          import CAction, CActionTypeCache
from Events.ActionEditDialog                import CActionEditDialog
from Events.ActionInfo                      import CActionInfoListEx
from Events.EventInfo                       import CEventInfoList
from Events.ActionProperty.JobTicketActionPropertyValueType import CJobTicketActionPropertyValueType
from Events.Utils                           import checkTissueJournalStatusByActions
from library.DialogBase                     import CDialogBase
from Reports.ReportBase                     import CReportBase, createTable
from Reports.ReportView                     import CReportViewDialog
from Orgs.Utils                             import getOrgStructureFullName
from library.database                       import CTableRecordCache
from library.PrintInfo                      import CInfoContext
from library.TableModel                     import (
                                                    CTableModel,
                                                    CCol,
                                                    CTextCol,
                                                    CEnumCol,
                                                    CBoolCol,
                                                   )
from library.Utils                          import (
                                                    forceBool,
                                                    forceDate,
                                                    forceTime,
                                                    forceDateTime,
                                                    pyDate,
                                                    pyTime,
                                                    pyDateTime,
                                                    forceInt,
                                                    forceRef,
                                                    forceString,
                                                    forceStringEx,
                                                    toVariant,
                                                    formatSex,
                                                    formatShortNameInt,
                                                    exceptionToUnicode,
                                                    getPref,
                                                    setPref,
                                                      )
from library.PrintTemplates                 import applyTemplate, getPrintButton, getPrintAction
from library.PreferencesMixin               import CDialogPreferencesMixin
from Resources.JobTicketInfo                import makeDependentActionIdList, CJobTicketsWithActionsInfoList, CJobInfoList
from Resources.JobTicketStatus              import CJobTicketStatus
from Resources.Utils                        import TreatmentScheduleMinimumDuration

from Resources.Ui_TreatmentAppointmentDialog import Ui_TreatmentAppointmentDialog


class CTreatmentAppointmentDialog(CDialogBase, Ui_TreatmentAppointmentDialog, CDialogPreferencesMixin):
    def __init__(self, parent, orgStructureId, eventIdList, actionCache, clientCache):
        CDialogBase.__init__(self, parent)
        self.__id = None
        self.addModels('Events',   CEventsModel(self, actionCache, clientCache))
        self.addModels('Schedule', CScheduleModel(self))
        self.addModels('Resources',CResourcesModel(self, clientCache))
        self.addModels('Actions',  CActionsModel(self, clientCache))
        self.addObject('btnPrint', getPrintButton(self, ''))
        self.addObject('actEventsPrint', QtGui.QAction(u'Список Список проживающих', self))
        self.addObject('actSchedulePrint', QtGui.QAction(u'Список Календарь назначений', self))
        self.addObject('actResourcesPrint', QtGui.QAction(u'Список Доступные ресурсы', self))
        self.addObject('actActionsPrint', QtGui.QAction(u'Список Состав группы', self))
        self.addObject('actJobTicketListPrint', getPrintAction(self, getTreatmentAppointmentContext()[0], u'По контексту', False))
        self.addObject('mnuBtnPrint', QtGui.QMenu(self))
        self.mnuBtnPrint.addAction(self.actEventsPrint)
        self.mnuBtnPrint.addAction(self.actSchedulePrint)
        self.mnuBtnPrint.addAction(self.actResourcesPrint)
        self.mnuBtnPrint.addAction(self.actActionsPrint)
        self.mnuBtnPrint.addSeparator()
        self.mnuBtnPrint.addAction(self.actJobTicketListPrint)
        self.btnPrint.setMenu(self.mnuBtnPrint)
        self.setupEventsMenu()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setObjectName('CTreatmentAppointmentDialog')
        self.setModels(self.tblEvents, self.modelEvents, self.selectionModelEvents)
        self.setModels(self.tblSchedule, self.modelSchedule, self.selectionModelSchedule)
        self.setModels(self.tblResources, self.modelResources, self.selectionModelResources)
        self.setModels(self.tblActions, self.modelActions, self.selectionModelActions)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.tblResources.addAppointmentToDate()
        self.tblResources.addAppointmentToTreatment()
        self.tblEvents.setPopupMenu(self.mnuEvents)
        self.tblActions.addPopupDelRow()
        self.tblActions.addPopupTreatmentDelRow()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.setActionTypeCache()
        self.orgStructureId = orgStructureId
        self.eventIdList = eventIdList
        self.actionCache = actionCache
        self.clientCache = clientCache
        self.jobTicketCache = {}
        self.actionJobTicketCache = {}
        self.clientAddCache = {}
        self.jobCurrentRow = None
        self.isAddToResources = False
        self.isRemoveFromQueue = False
        self.isFirst = True
        self.modelEvents.setActionCache(self.actionCache)
        self.modelEvents.setIdList(self.eventIdList)
        self.isFirst = False
        self.setLblCountEvents()
        self.btnPrint.setEnabled(True)
        self.modelSchedule.setOrgStructureId(self.orgStructureId)
        self.modelResources.setOrgStructureId(self.orgStructureId)
        self.modelSchedule.loadHeader()
        self.modelResources.setEventEditor(self)
        self.tblEvents.setCurrentRow(0)
        self.preferencesResources = getPref(QtGui.qApp.preferences.windowPrefs, 'tblTreatmentAppointmentResources', {})


    def setActionTypeCache(self):
        db = QtGui.qApp.db
        self.actionTypeCache = CTableRecordCache(db, db.forceTable('ActionType'), u'*', capacity=None)
        self.modelSchedule.setActionTypeCache(self.actionTypeCache)
        self.modelResources.setActionTypeCache(self.actionTypeCache)


    @pyqtSignature('int, int')
    def on_calendar_currentPageChanged(self, year, month):
        selectedDate = self.calendar.selectedDate()
        currYear = selectedDate.year()
        currMonth = selectedDate.month()
        newDate = selectedDate.addMonths((year-currYear)*12+(month-currMonth))
        self.calendar.setSelectedDate(newDate)


    @pyqtSignature('')
    def on_calendar_selectionChanged(self):
        if self.modelResources.items:
            self.preferencesResources = self.tblResources.savePreferences()
            setPref(QtGui.qApp.preferences.windowPrefs, 'tblTreatmentAppointmentResources', self.preferencesResources)
        actionCountDict, jobTicketIdList = self.getActionCountBusy()
        self.modelResources.setActionCountBusy(actionCountDict)
        self.modelResources.setJobTicketIdBusy(jobTicketIdList)
        self.modelResources.loadItems(self.modelEvents.getCheckedEventIdList(), self.getCurrentClientId(), self.calendar.selectedDate(), self.modelSchedule.dates, self.modelSchedule.dateHeader)
        self.setSpanResources()
        self.updateModelActions()
        self.tblResources.loadPreferences(self.preferencesResources)


    def dumpParams(self, cursor, params={}):
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
        orgStructureId = params.get('orgStructureId', None)
        if orgStructureId:
            rows.append(u'Подразделение: ' + getOrgStructureFullName(orgStructureId))
        actionTypeId = params.get('actionTypeId', None)
        if actionTypeId:
            rows.append(u'Мероприятие: ' + forceString(db.translate('ActionType', 'id', actionTypeId, 'name')))
        selectedDate = params.get('selectedDate', None)
        if selectedDate:
            rows.append(u'На дату: ' + forceString(selectedDate))
        clientId = params.get('clientId', None)
        if clientId:
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                   forceString(clientRecord.value('firstName')),
                   forceString(clientRecord.value('patrName'))) + u', ' + forceString(clientRecord.value('birthDate')) + u', ' + formatSex(clientRecord.value('sex')) + u', ' + forceString(clientId)
                rows.append(u'Пациент: ' + name)
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    @pyqtSignature('int')
    def on_actJobTicketListPrint_printByTemplate(self, templateId):
        jobTicketsIdList = self.modelResources.itemIdList()
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
        params = {}
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Список проживающих')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        params['orgStructureId'] = self.orgStructureId
        self.dumpParams(cursor, params)
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
        params = {}
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Календарь назначений')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        params['orgStructureId'] = self.orgStructureId
        params['clientId'] = self.getCurrentClientId()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        colWidths  = [ self.tblSchedule.columnWidth(i) for i in xrange(self.modelSchedule.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(self.modelSchedule.headers[iCol])], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for col, dateHeader in enumerate(self.modelSchedule.headers):
            if col > 0:
                record = self.modelSchedule.dateHeader.get(pyDate(dateHeader), None)
                if record:
                    brushColor = QtGui.QColor(forceString(record.value('color')))
                    cursorTable = table.cursorAt(0, col)
                    tableFormat = QtGui.QTextCharFormat()
                    tableFormat.setBackground(QtGui.QBrush(brushColor))
                    cursorTable.setBlockCharFormat(tableFormat)
        iModelRowTotal = 1
        for iModelRow in xrange(self.modelSchedule.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelSchedule.columnCount()):
                index = self.modelSchedule.createIndex(iModelRow, iModelCol)
                text = forceString(self.modelSchedule.data(index))
                brushColor = None
                column = index.column()
                if column > 0:
                    row = index.row()
                    if row >= 0 and row < len(self.modelSchedule.dates):
                        datetimePrev, datetimeLast = self.modelSchedule.dates[row]
                        header = pyDate(self.modelSchedule.headers[column])
                        if datetimePrev and datetimeLast and header:
                            if header and (((pyTime(datetimePrev), pyTime(datetimeLast)), header) in self.modelSchedule.items.keys()):
                                keyScheme = ((pyTime(datetimePrev), pyTime(datetimeLast)), header)
                                actionTypeId, item, quantity, duration = self.modelSchedule.items.get(keyScheme, None)
                                if item:
                                    status = forceInt(item.value('status'))
                                    if status in (CActionStatus.started, CActionStatus.wait, CActionStatus.withoutResult, CActionStatus.appointed):
                                        brushColor = QtGui.QColor(Qt.yellow)
                                    elif status in (CActionStatus.finished, ):
                                        brushColor = QtGui.QColor(Qt.green)
                table.setText(iTableRow, iModelCol, text, brushColor = brushColor)
            iModelRowTotal += 1
        if iModelRowTotal > 1:
            headers = self.modelSchedule.headers
            dates = self.modelSchedule.dates
            items = self.modelSchedule.items
            for column, header in enumerate(headers):
                if column > 0:
                    for row, (datetimePrev, datetimeLast) in enumerate(dates):
                        if header and (((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(header)) in items.keys()):
                            item = items.get(((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(header)), None)
                            if item and item[3]:
                                duration = item[3]
                                rowSpanCount = math.ceil(float(duration/self.modelSchedule.minimumDuration))
                                table.mergeCells(row+1, column, rowSpanCount, 1)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_actResourcesPrint_triggered(self):
        params = {}
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Доступные ресурсы')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        params['orgStructureId'] = self.orgStructureId
        params['selectedDate'] = self.calendar.selectedDate()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        colWidths  = [ self.tblResources.columnWidth(i) for i in xrange(self.modelResources.columnCount()) ]
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            tableColumns.append((widthInPercents, [forceString(u'')], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        iModelRowTotal = 1
        for iModelRow in xrange(self.modelResources.rowCount()):
            iTableRow = table.addRow()
            for iModelCol in xrange(self.modelResources.columnCount()):
                index = self.modelResources.createIndex(iModelRow, iModelCol)
                text = forceString(self.modelResources.data(index))
                table.setText(iTableRow, iModelCol, text)
            iModelRowTotal += 1
        if iModelRowTotal > 1:
            headers = self.modelResources.headers
            dates = self.modelResources.dates
            items = self.modelResources.items
            for column, header in enumerate(headers):
                if column > 0:
                    for row, (datetimePrev, datetimeLast) in enumerate(dates):
                        if header and (((datetimePrev, datetimeLast), header) in items.keys()):
                            item = items.get(((datetimePrev, datetimeLast), header), None)
                            if item and item[3]:
                                duration = item[3]
                                rowSpanCount = math.ceil(float(duration/self.modelSchedule.minimumDuration))
                                table.mergeCells(row+1, column, rowSpanCount, 1)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('')
    def on_actActionsPrint_triggered(self):
        params = {}
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Список Состав группы')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        row, column, datetime, actionTypeId, datetimePrev, datetimeLast = self.getCurrentActionTypeData()
        params['orgStructureId'] = self.orgStructureId
        params['actionTypeId'] = actionTypeId
        params['selectedDate'] = datetime
        self.dumpParams(cursor, params)
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
        self.lblCountEvents.setText(u'Контингент всего: %d.'%(len(self.modelEvents.idList())))


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


    def eventId(self, index):
        return self.tblEvents.itemId(index)


    def currentEventId(self):
        return self.tblEvents.currentItemId()


    def getCurrentClientId(self):
        record = None
        rowCount = self.modelEvents.rowCount()
        row = self.tblEvents.currentRow()
        if row >= 0 and row < rowCount:
            record = self.modelEvents.getRecordByRow(row)
        return forceRef(record.value('client_id')) if record else None


    def currentResourcesId(self):
        return self.tblResources.currentItemId()


    def actionId(self, index):
        return self.tblActions.itemId(index)


    def currentActionId(self):
        return self.tblActions.currentItemId()


    def setSpanSchedule(self):
        headers = self.modelSchedule.headers
        dates = self.modelSchedule.dates
        items = self.modelSchedule.items
        for column, header in enumerate(headers):
            if column > 0:
                for row, (datetimePrev, datetimeLast) in enumerate(dates):
                    self.tblSchedule.setSpan(row, column, 1, 1)
        for column, header in enumerate(headers):
            if column > 0:
                for row, (datetimePrev, datetimeLast) in enumerate(dates):
                    if header and (((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(header)) in items.keys()):
                        item = items.get(((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(header)), None)
                        if item and item[3]:
                            duration = item[3]
                            rowSpanCount = math.ceil(float(duration/self.modelSchedule.minimumDuration))
                            self.tblSchedule.setSpan(row, column, rowSpanCount, 1)


    def setSpanResources(self):
        headers = self.modelResources.headers
        dates = self.modelResources.dates
        items = self.modelResources.items
        for column, header in enumerate(headers):
            if column > 0:
                for row, (datetimePrev, datetimeLast) in enumerate(dates):
                    self.tblResources.setSpan(row, column, 1, 1)
        for column, header in enumerate(headers):
            if column > 0:
                for row, (datetimePrev, datetimeLast) in enumerate(dates):
                    if header and (((datetimePrev, datetimeLast), header) in items.keys()):
                        item = items.get(((datetimePrev, datetimeLast), header), None)
                        if item and item[3]:
                            duration = item[3]
                            rowSpanCount = math.ceil(float(duration/self.modelSchedule.minimumDuration))
                            self.tblResources.setSpan(row, column, rowSpanCount, 1)


    def getActionCountBusy(self):
        actionCountDict = {}
        jobTicketIdList = []
        clientIdList = self.modelEvents.getClientIdList()
        if not clientIdList or len(self.modelSchedule.headers) <= 1:
            return actionCountDict
        db = QtGui.qApp.db
        tableRBJobType = db.table('rbJobType')
        tableActionType = db.table('ActionType')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableEvent = db.table('Event')
        tableAction = db.table('Action')
        tableAP = db.table('ActionProperty')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableJobTicket = db.table('Job_Ticket')
        tableJob = db.table('Job')
        cond = [#tableEvent['client_id'].inlist(clientIdList),
                tableEvent['deleted'].eq(0),
                tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                tableJobTicket['datetime'].dateGe(self.modelSchedule.headers[1]),
                tableJobTicket['datetime'].dateLe(self.modelSchedule.headers[len(self.modelSchedule.headers)-1]),
                tableActionPropertyType['id'].eq(tableAP['type_id']),
                tableJobTicket['id'].isNotNull(),
                tableAction['status'].notInlist([CActionStatus.canceled, CActionStatus.refused]),
                tableAPJT['value'].eq(tableJobTicket['id'])
                ]
        if self.modelResources.actionTypeIdResources:
            cond.append(tableActionType['id'].inlist(self.modelResources.actionTypeIdResources))
        cols = [u'COUNT(Action.id) AS actionCount',
                tableAction['actionType_id'],
                tableJobTicket['datetime'],
                tableJobTicket['id'].alias('jobTicketId')
                ]
        queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
        LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
        queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
        queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
        queryTable = queryTable.innerJoin(tableAction, tableAction['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        queryTable = queryTable.innerJoin(tableAPJT, tableAP['id'].eq(tableAPJT['id']))
        groupBy = u'Action.actionType_id, Job_Ticket.datetime, Job_Ticket.id'
        records = db.getRecordListGroupBy(queryTable, cols, cond, groupBy)
        for record in records:
            actionTypeId = forceRef(record.value('actionType_id'))
            datetime = forceDateTime(record.value('datetime'))
            actionCount = actionCountDict.get((pyDateTime(datetime), actionTypeId), 0)
            actionCount += forceInt(record.value('actionCount'))
            actionCountDict[(pyDateTime(datetime), actionTypeId)] = actionCount
            jobTicketId = forceRef(record.value('jobTicketId'))
            if jobTicketId and jobTicketId not in jobTicketIdList:
                jobTicketIdList.append(jobTicketId)
        return actionCountDict, jobTicketIdList


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Close:
            self.close()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelEvents_currentRowChanged(self, current, previous):
        self.updateData()


    def updateData(self):
        self.modelSchedule.loadItems(self.getCurrentClientId())
        self.modelResources.setMinimumDuration(self.modelSchedule.minimumDuration)
        self.setSpanSchedule()
        self.updateCalendar()
        self.modelResources.getResources()
        actionCountDict, jobTicketIdList = self.getActionCountBusy()
        self.modelResources.setActionCountBusy(actionCountDict)
        self.modelResources.setJobTicketIdBusy(jobTicketIdList)
        self.modelResources.loadItems(self.modelEvents.getCheckedEventIdList(), self.getCurrentClientId(), self.calendar.selectedDate(), self.modelSchedule.dates, self.modelSchedule.dateHeader)
        self.setSpanResources()
        self.setLblCountEvents()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelEvents_dataChanged(self, topLeft, bottomRight):
        self.modelResources.setEventIdList(self.modelEvents.getCheckedEventIdList())
        self.modelResources.setClientIdDict(self.modelEvents.getCheckedClientIdDict())


    def updateCalendar(self):
        dateHeader = self.modelSchedule.dateHeader
        minDate = QDate.currentDate()
        maxDate = QDate.currentDate()
        for date, record in dateHeader.items():
            isStart = forceInt(record.value('isStart'))
            isEnd = forceInt(record.value('isEnd'))
            if isStart:
                minDate = date
            if isEnd:
                maxDate = date
            if isStart or isEnd:
                pass
            else:
                color = QtGui.QColor(forceString(record.value('color')))
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QBrush(color))
                self.calendar.setDateTextFormat(forceDate(date), format)
        self.calendar.setMinimumDate(minDate)
        self.calendar.setMaximumDate(maxDate)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelResources_currentChanged(self, current, previous):
        self.updateModelActions()


    def getCurrentActionTypeData(self):
        datetime = None
        actionTypeId = None
        datetimePrev = None
        datetimeLast = None
        index = self.tblResources.currentIndex()
        row = index.row()
        column = index.column()
        if column > 0 and row >= 0 and row < len(self.modelResources.dates):
                datetimePrev, datetimeLast = self.modelResources.dates[row]
                if self.modelResources.headers[column] and (((datetimePrev, datetimeLast), self.modelResources.headers[column]) in self.modelResources.items.keys()):
                    keyScheme = ((datetimePrev, datetimeLast), self.modelResources.headers[column])
                    actionTypeId, record, quantity, duration, actionTypeCount = self.modelResources.items.get(keyScheme, None)
                    if record:
                        datetime = QDateTime(forceDate(record.value('date')), forceTime(record.value('datetime')))
                        datetimePrev = QDateTime(forceDate(record.value('date')), forceTime(datetimePrev))
                        datetimeLast = QDateTime(forceDate(record.value('date')), forceTime(datetimeLast))
        return row, column, datetime, actionTypeId, datetimePrev, datetimeLast


    def updateModelActions(self):
        row, column, datetime, actionTypeId, datetimePrev, datetimeLast = self.getCurrentActionTypeData()
        self.modelActions.loadData(self.modelEvents.getClientIdList(), datetime, actionTypeId, datetimePrev, datetimeLast, self.modelSchedule.dateHeader)
        self.getClientIdBusyList()
        self.modelEvents.reset()
        return row, column


    def getClientIdBusyList(self):
        clientIdBusyList = []
        items = self.modelActions.items
        for item in items:
            clientId = forceRef(item.value('client_id'))
            if clientId and clientId not in clientIdBusyList:
                clientIdBusyList.append(clientId)
        self.modelEvents.setClientIdBusyList(clientIdBusyList)


    @pyqtSignature('QModelIndex')
    def on_tblActions_doubleClicked(self, index):
        self.editAction(self.modelActions.getItemId(self.tblActions.currentIndex()))


    @pyqtSignature('int')
    def on_modelActions_itemsCountChanged(self, count):
        currentRow = self.tblEvents.currentRow()
        rowResources, columnResources = self.updateModelActions()
        self.tblEvents.setCurrentRow(currentRow)
        self.tblResources.setCurrentIndex(self.modelResources.index(rowResources, columnResources))


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
        self.clientIdBusyList = []
        self.setTable('Event')


    def getItemIdCheckedRow(self):
        includeCaches = self._cols[0].getIncludeCaches()
        for eventId, include in includeCaches.items():
            if include and eventId:
                index = self.findItemIdIndex(eventId)
                if index and index >= 0:
                    return index
        return 0


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
            clientId = forceRef(record.value('client_id')) if record else None
            if clientId not in self.clientIdBusyList:
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


    def setClientIdBusyList(self, clientIdBusyList):
        self.clientIdBusyList = clientIdBusyList


    def getCheckedEventIdList(self):
        checkedEventIdList = []
        includeCaches = self._cols[0].getIncludeCaches()
        for eventId, include in includeCaches.items():
            if include and eventId and eventId not in checkedEventIdList:
                checkedEventIdList.append(eventId)
        return checkedEventIdList


    def getClientIdList(self):
        clientIdList = []
        rowCount = self.rowCount()
        for row in range(0, rowCount):
            record = self.getRecordByRow(row)
            clientId = forceRef(record.value('client_id')) if record else None
            if clientId and clientId not in clientIdList:
                clientIdList.append(clientId)
        return clientIdList


    def getCheckedClientIdList(self):
        clientIdList = []
        includeCaches = self._cols[0].getIncludeCaches()
        for eventId, include in includeCaches.items():
            if include and eventId:
                record = self.getRecordById(eventId)
                clientId = forceRef(record.value('client_id')) if record else None
                if clientId and clientId not in clientIdList:
                    clientIdList.append(clientId)
        return clientIdList


    def getCheckedClientIdDict(self):
        clientIdDict = {}
        includeCaches = self._cols[0].getIncludeCaches()
        for eventId, include in includeCaches.items():
            if include and eventId:
                record = self.getRecordById(eventId)
                clientId = forceRef(record.value('client_id')) if record else None
                if clientId:
                    clientIdDict[eventId] = clientId
        return clientIdDict


    def emitDataChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


class CScheduleModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.headers = []
        self.items = {}
        self.sourceItems = {}
        self.dates = []
        self.readOnly = False
        self.quantityMax = 0
        self.minimumDuration = TreatmentScheduleMinimumDuration
        self.actionTypeCache = {}
        self.orgStructureId = None
        self.currentDate = QDate.currentDate()
        self.dateHeader = {}


    def items(self):
        return self.items


    def setReadOnly(self, value):
        self.readOnly = value


    def columnCount(self, index = None):
        return len(self.headers)


    def rowCount(self, index = None):
        return len(self.dates)


    def flags(self, index = QModelIndex()):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                header = self.headers[section]
                if header:
                    if section == 0:
                        return QVariant(header)
                    else:
                        return QVariant(header.toString('dd.MM.yyyy'))
            elif role == Qt.BackgroundRole and section > 0:
                header = self.headers[section]
                if header:
                    record = self.dateHeader.get(pyDate(header), None)
                    color = forceString(record.value('color')) if record else u''
                    return QVariant(QtGui.QColor(color))
        return QVariant()


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def setActionTypeCache(self, actionTypeCache):
        self.actionTypeCache = actionTypeCache


    def loadHeader(self):
        self.headers = [u'Сеансы']
        if self.orgStructureId:
            db = QtGui.qApp.db
            tableTreatmentSchedule = db.table('TreatmentSchedule')
            tableTreatmentType = db.table('TreatmentType')
            cond = [tableTreatmentSchedule['orgStructure_id'].eq(self.orgStructureId),
                    u'''TreatmentSchedule.date >= (SELECT MAX(TSStart.date)
                                                   FROM TreatmentSchedule AS TSStart
                                                   WHERE TSStart.orgStructure_id = %d
                                                   AND TSStart.date <= %s
                                                   AND TSStart.isStart = 1)'''%(self.orgStructureId, db.formatDate(self.currentDate)),
                    u'''TreatmentSchedule.date <= (SELECT MIN(TSEnd.date)
                                                   FROM TreatmentSchedule AS TSEnd
                                                   WHERE TSEnd.orgStructure_id = %d
                                                   AND TSEnd.date >= %s
                                                   AND TSEnd.isEnd = 1)'''%(self.orgStructureId, db.formatDate(self.currentDate))
                    ]
            queryTable = tableTreatmentSchedule.leftJoin(tableTreatmentType, tableTreatmentType['id'].eq(tableTreatmentSchedule['treatmentType_id']))
            records = db.getRecordList(queryTable, 'TreatmentSchedule.*, TreatmentType.*', cond, order='TreatmentSchedule.date')
            for record in records:
                date = forceDate(record.value('date'))
                self.dateHeader[pyDate(date)] = record
                if forceInt(record.value('isStart')) or forceInt(record.value('isEnd')):
                    pass
                else:
                    self.headers.append(date)
        self.reset()


    def getActionTypeShowNameList(self, actionTypeId):
        if actionTypeId:
            record = self.actionTypeCache.get(actionTypeId)
            if record:
                return forceStringEx(record.value('name'))
        return u''


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row < len(self.dates):
                datetimePrev, datetimeLast = self.dates[row]
                if column == 0:
                    if datetimePrev and datetimeLast:
                        timePrev = datetimePrev
                        timeLast = datetimeLast
                        return QVariant(timePrev.toString('hh:mm') + u' - ' + timeLast.toString('hh:mm'))
                else:
                    if self.headers[column] and (((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(self.headers[column])) in self.items.keys()):
                        keyScheme = ((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(self.headers[column]))
                        actionTypeId, item, quantity, duration = self.items.get(keyScheme, None)
                        return toVariant(self.getActionTypeShowNameList(actionTypeId))
        elif role == Qt.EditRole:
            if row < len(self.dates):
                datetimePrev, datetimeLast = self.dates[row]
                if column == 0:
                    if datetimePrev and datetimeLast:
                        timePrev = datetimePrev
                        timeLast = datetimeLast
                        return QVariant(timePrev.toString('hh:mm') + u' - ' + timeLast.toString('hh:mm'))
                else:
                    if self.headers[column] and (((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(self.headers[column])) in self.items.keys()):
                        keyScheme = ((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(self.headers[column]))
                        actionTypeId, item, quantity, duration = self.items.get(keyScheme, None)
                        return toVariant(self.getActionTypeShowNameList(actionTypeId))
        elif role == Qt.BackgroundRole:
            if row >= 0 and row < len(self.dates):
                if column == 0:
                    return QVariant(QtGui.QColor(Qt.white))
                else:
                    datetimePrev, datetimeLast = self.dates[row]
                    header = pyDate(self.headers[column])
                    if datetimePrev and datetimeLast and header:
                        if header and (((pyTime(datetimePrev), pyTime(datetimeLast)), header) in self.items.keys()):
                            keyScheme = ((pyTime(datetimePrev), pyTime(datetimeLast)), header)
                            actionTypeId, item, quantity, duration = self.items.get(keyScheme, None)
                            if item:
                                status = forceInt(item.value('status'))
                                if status in (CActionStatus.started, CActionStatus.wait, CActionStatus.withoutResult, CActionStatus.appointed):
                                    return QVariant(QtGui.QColor(Qt.yellow))
                                elif status in (CActionStatus.finished, ):
                                    return QVariant(QtGui.QColor(Qt.green))
        return QVariant()


    def loadItems(self, currentClientId = None):
        self.currentClientId = currentClientId
        self.items = {}
        self.dates = []
        self.quantityMax = 0
        self.sourceItems = {}
        self.minimumDuration = TreatmentScheduleMinimumDuration
        treatmentTypeIdList = []
        treatmentSchemeIdList = []
        datetimeMin = None
        datetimeMax = None
        if len(self.headers) > 1:
            db = QtGui.qApp.db
            tableTreatmentScheme = db.table('TreatmentScheme')
            tableTreatmentSchemeSource = db.table('TreatmentScheme_Source')
            tableJobTicket = db.table('Job_Ticket')
            tableJob = db.table('Job')
            queryTable = tableTreatmentScheme.innerJoin(tableTreatmentSchemeSource, tableTreatmentSchemeSource['treatmentScheme_id'].eq(tableTreatmentScheme['id']))
            queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['id'].eq(tableTreatmentScheme['jobTicket_id']))
            queryTable = queryTable.innerJoin(tableJob, tableJob['id'].eq(tableJobTicket['master_id']))
            condSource = []
            for date, record in self.dateHeader.items():
                if forceInt(record.value('isStart')) or forceInt(record.value('isEnd')):
                    pass
                else:
                    treatmentTypeId = forceRef(record.value('treatmentType_id'))
                    if treatmentTypeId and (date, treatmentTypeId) not in treatmentTypeIdList:
                        treatmentTypeIdList.append((date, treatmentTypeId))
                        condSource.append(db.joinAnd([tableTreatmentScheme['treatmentType_id'].eq(treatmentTypeId),
                                                      tableTreatmentScheme['endDate'].dateGe(date),
                                                      tableJobTicket['datetime'].dateLe(date),
                                                     ]))
            if condSource and self.orgStructureId:
                cond = [tableTreatmentSchemeSource['orgStructure_id'].eq(self.orgStructureId),
                        tableJobTicket['deleted'].eq(0),
                        tableJob['deleted'].eq(0),
                        ]
                cond.append(db.joinOr(condSource))
                cols = [u'DISTINCT Job.id AS jobId',
                        tableJob['date'],
                        tableJob['begTime'],
                        tableJob['endTime'],
                        tableJob['quantity'],
                        tableTreatmentScheme['id'].alias('treatmentSchemeId')
                        ]
                order = [tableJob['begTime'].name(), tableJob['endTime'].name()]
                records = db.getRecordList(queryTable, cols, cond, order)
                for record in records:
                    quantity = forceInt(record.value('quantity'))
                    if quantity > self.quantityMax:
                        self.quantityMax = quantity
                    begTime = forceTime(record.value('begTime'))
                    endTime = forceTime(record.value('endTime'))
                    if not datetimeMin or datetimeMin > begTime:
                        datetimeMin = begTime
                    if not datetimeMax or datetimeMax < endTime:
                        datetimeMax = endTime
                    treatmentSchemeId = forceRef(record.value('treatmentSchemeId'))
                    if treatmentSchemeId and treatmentSchemeId not in treatmentSchemeIdList:
                        treatmentSchemeIdList.append(treatmentSchemeId)

                if self.minimumDuration and datetimeMin and datetimeMax:
                    datetimePrev = datetimeMin
                    while datetimePrev <= datetimeMax:
                        datetimeLast = datetimePrev.addSecs(self.minimumDuration)
                        self.dates.append((datetimePrev, datetimeLast))
                        datetimePrev = datetimeLast

                if self.dates and self.currentClientId and treatmentSchemeIdList and self.dateHeader:
                    tableRBJobType = db.table('rbJobType')
                    tableActionType = db.table('ActionType')
                    tableActionPropertyType = db.table('ActionPropertyType')
                    tableEvent = db.table('Event')
                    tableAction = db.table('Action')
                    tableAP = db.table('ActionProperty')
                    tableAPJT = db.table('ActionProperty_Job_Ticket')

                    cond = [tableEvent['client_id'].eq(self.currentClientId),
                            tableEvent['deleted'].eq(0),
                            tableAction['deleted'].eq(0),
                            tableActionType['deleted'].eq(0),
                            tableActionPropertyType['deleted'].eq(0),
                            tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                            tableActionPropertyType['valueDomain'].isNotNull(),
                            tableActionType['isUsesCycles'].eq(1),
                            tableJob['deleted'].eq(0),
                            tableJobTicket['deleted'].eq(0),
                            tableJobTicket['datetime'].dateGe(self.headers[1]),
                            tableJobTicket['datetime'].dateLe(self.headers[len(self.headers)-1]),
                            tableJobTicket['id'].isNotNull(),
                            tableAPJT['value'].eq(tableJobTicket['id']),
                            tableAP['action_id'].eq(tableAction['id']),
                            tableAP['deleted'].eq(0),
                            tableAction['status'].notInlist([CActionStatus.canceled, CActionStatus.refused])
                            ]

                    cols = [tableJobTicket['id'].alias('jobTicketId'),
                            tableJobTicket['datetime'],
                            tableAction['status'],
                            tableActionPropertyType['actionType_id'].alias('actionTypeId'),
                            tableJob['jobType_id'],
                            tableJob['date'],
                            tableJob['begTime'],
                            tableJob['endTime'],
                            tableJob['quantity']
                            ]
                    queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
                    queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
                    LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
                    queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
                    queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
                    queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableActionPropertyType['id']))
                    queryTable = queryTable.innerJoin(tableAPJT, tableAP['id'].eq(tableAPJT['id']))
                    queryTable = queryTable.innerJoin(tableAction, tableAction['actionType_id'].eq(tableActionType['id']))
                    queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
                    order = [tableJobTicket['id'].name(), tableJobTicket['datetime'].name(), tableJobTicket['idx'].name()]
                    records = db.getRecordList(queryTable, cols, cond, order)
                    for record in records:
                        actionTypeId = forceRef(record.value('actionTypeId'))
                        datetime = forceDateTime(record.value('datetime'))
                        date = forceDate(record.value('date'))
                        begTime = forceTime(record.value('begTime'))
                        endTime = forceTime(record.value('endTime'))
                        timeToSecs = begTime.secsTo(endTime)
                        quantity = forceInt(record.value('quantity'))
                        duration = math.floor(float(timeToSecs)/quantity)
                        for datetimePrev, datetimeLast in self.dates:
                            if datetime.time() >= datetimePrev and datetime.time() < datetimeLast:
                                self.items[((pyTime(datetimePrev), pyTime(datetimeLast)), pyDate(datetime.date()))] = (actionTypeId, record, quantity, duration)
                                break
        self.dates.sort()
        self.reset()


class CResourcesModel(QAbstractTableModel):
    def __init__(self, parent, clientCache):
        QAbstractTableModel.__init__(self, parent)
        self.clientCache = clientCache
        self.headers = []
        self.items = {}
        self.dates = []
        self.readOnly = False
        self.minimumDuration = TreatmentScheduleMinimumDuration
        self.actionTypeCache = {}
        self.orgStructureId = None
        self.eventEditor = None
        self.eventIdList = []
        self.clientIdDict = {}
        self.currentDate = QDate.currentDate()
        self.selectedDate = self.currentDate
        self.scheduleDates = []
        self.dateResources = {}
        self.actionCountBusyDict = {}
        self.scheduleDateHeader = {}
        self.busyJobTicketId = []
        self.actionTypeIdResources = []
        self.datesSpan = []


    def items(self):
        return self.items


    def setReadOnly(self, value):
        self.readOnly = value


    def columnCount(self, index = None):
        return len(self.headers)


    def rowCount(self, index = None):
        return len(self.dates)


    def flags(self, index = QModelIndex()):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        return QVariant()


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def setOrgStructureId(self, value):
        self.orgStructureId = value


    def setMinimumDuration(self, value):
        self.minimumDuration = value


    def setActionTypeCache(self, actionTypeCache):
        self.actionTypeCache = actionTypeCache


    def setEventIdList(self, eventIdList):
        self.eventIdList = eventIdList


    def setClientIdDict(self, clientIdDict):
        self.clientIdDict = clientIdDict


    def setActionCountBusy(self, actionCountBusyDict):
        self.actionCountBusyDict = actionCountBusyDict


    def setJobTicketIdBusy(self, jobTicketIdList):
        self.busyJobTicketId = jobTicketIdList


    def getActionBusy(self, clientId, scheduleDatePrev, scheduleDateLast):
        if not clientId or not scheduleDatePrev or not scheduleDateLast:
            return None
        db = QtGui.qApp.db
        tableRBJobType = db.table('rbJobType')
        tableActionType = db.table('ActionType')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableEvent = db.table('Event')
        tableAction = db.table('Action')
        tableAP = db.table('ActionProperty')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableJobTicket = db.table('Job_Ticket')
        tableJob = db.table('Job')
        cols = [tableAction['id'],
                tableJobTicket['datetime'],
                tableActionType['name'].alias(u'actionTypeName')
               ]
        cond = [tableEvent['client_id'].eq(clientId),
                tableEvent['deleted'].eq(0),
                tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                tableJobTicket['datetime'].ge(scheduleDatePrev),
                tableJobTicket['datetime'].lt(scheduleDateLast),
                tableActionPropertyType['id'].eq(tableAP['type_id']),
                tableJobTicket['id'].isNotNull(),
                tableAction['status'].notInlist([CActionStatus.canceled, CActionStatus.refused]),
                tableAPJT['value'].eq(tableJobTicket['id'])
                ]
        queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
        LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
        queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
        queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
        queryTable = queryTable.innerJoin(tableAction, tableAction['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        queryTable = queryTable.innerJoin(tableAPJT, tableAP['id'].eq(tableAPJT['id']))
        record = db.getRecordEx(queryTable, cols, cond, order = u'Job_Ticket.datetime DESC')
        return record


    def on_appointmentToDate(self, row, column):
        if not self.eventIdList or not self.selectedDate:
            return
        self.saveNewAction(row, column, [self.selectedDate])


    def saveNewAction(self, row, column, dateList):
        if not dateList:
            return
        if row >= 0 and row < len(self.dates):
            dateList.sort()
            for idx, selectedDate in enumerate(dateList):
                datetimePrev, datetimeLast = self.dates[row]
                if self.headers[column] and (((datetimePrev, datetimeLast), self.headers[column]) in self.items.keys()):
                    keyScheme = ((datetimePrev, datetimeLast), self.headers[column])
                    actionTypeId, recordResources, quantity, duration, actionTypeCount = self.items.get(keyScheme, None)
                    if quantity > actionTypeCount:
                        newActionTypeCount = actionTypeCount
                        for eventId in self.eventIdList:
                            jobTicketId = forceRef(recordResources.value('jobTicket_id')) if recordResources else None
                            if not jobTicketId:
                                return
                            datetime = forceDateTime(recordResources.value('datetime')) if recordResources else None
                            if not datetime:
                                return
                            orgStructureId = forceRef(recordResources.value('orgStructure_id')) if recordResources else None
                            if not orgStructureId:
                                return
                            db = QtGui.qApp.db
                            findDateTime = QDateTime(selectedDate, datetime.time())
                            if jobTicketId in self.busyJobTicketId:
                                jobTicketId = None
                            if not jobTicketId or (datetime != findDateTime and recordResources):
                                quantity         = forceInt(recordResources.value('capacity'))
                                jobTypeId        = forceRef(recordResources.value('jobType_id'))
                                jobPurposeId     = forceRef(recordResources.value('jobPurpose_id'))
                                tableJob = db.table('Job')
                                tableJobTicket = db.table('Job_Ticket')
                                cols = [tableJobTicket['id'].alias('jobTicketId'),
                                        tableJobTicket['datetime']
                                       ]
                                cond = [tableJob['deleted'].eq(0),
                                        tableJobTicket['deleted'].eq(0),
                                        db.joinOr([tableJobTicket['datetime'].eq(findDateTime),
                                        db.joinAnd([tableJobTicket['datetime'].ge(QDateTime(selectedDate, QTime(datetimePrev))),
                                        tableJobTicket['datetime'].lt(QDateTime(selectedDate, QTime(datetimeLast)))])]),
                                        tableJob['date'].eq(selectedDate),
                                        tableJob['jobType_id'].eq(jobTypeId),
                                        tableJob['jobPurpose_id'].eq(jobPurposeId),
                                        tableJob['orgStructure_id'].eq(orgStructureId),
                                        tableJob['quantity'].eq(forceInt(recordResources.value('quantity'))),
                                        db.joinOr([tableJob['capacity'].eq(quantity), tableJob['capacity'].gt(1)]),
                                        tableJobTicket['status'].eq(CJobTicketStatus.wait)
                                       ]
                                if self.busyJobTicketId:
                                    cond.append(tableJobTicket['id'].notInlist(self.busyJobTicketId))
                                queryTable = tableJob.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
                                recordJT = db.getRecordEx(queryTable, cols, cond, u'Job_Ticket.idx, Job_Ticket.id')
                                jobTicketId = forceRef(recordJT.value('jobTicketId')) if recordJT else None
                                datetime = forceDateTime(recordJT.value('datetime')) if recordJT else None
                            if jobTicketId and datetime:
                                currentDateTime = QDateTime.currentDateTime()
                                tableAction = db.table('Action')
                                tableActionType = db.table('ActionType')
                                tableEvent = db.table('Event')
                                actionType = CActionTypeCache.getById(actionTypeId)
                                defaultStatus = actionType.defaultStatus
                                defaultOrgId = actionType.defaultOrgId
                                try:
                                    try:
                                        db.transaction()
                                        clientId = self.clientIdDict.get(eventId, None)
                                        if quantity > newActionTypeCount and clientId and actionTypeId and datetime:
                                            recordActionBusy = None
                                            for (scheduleTimePrev, scheduleTimeLast) in self.datesSpan:
                                                scheduleDatePrev = QDateTime(selectedDate, scheduleTimePrev)
                                                scheduleDateLast = QDateTime(selectedDate, scheduleTimeLast)
                                                if datetime >= scheduleDatePrev and datetime < scheduleDateLast:
                                                    recordActionBusy = self.getActionBusy(clientId, scheduleDatePrev, scheduleDateLast)
                                                    if recordActionBusy and forceRef(recordActionBusy.value('id')):
                                                        name = u''
                                                        if clientId:
                                                            clientRecord = self.clientCache.get(clientId)
                                                            if clientRecord:
                                                                name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                                                                   forceString(clientRecord.value('firstName')),
                                                                   forceString(clientRecord.value('patrName'))) + u', ' + forceString(clientRecord.value('birthDate')) + u', ' + formatSex(clientRecord.value('sex')) + u', ' + forceString(clientId)
                                                        message = u'''У пациента %s уже есть назначение на %s %s!'''%(name, forceString(recordActionBusy.value('datetime')), forceString(recordActionBusy.value('actionTypeName')))
                                                        QtGui.QMessageBox.warning(self.eventEditor,
                                                                u'Внимание!',
                                                                message,
                                                                QtGui.QMessageBox.Ok)
                                                        break
                                            if not recordActionBusy:
                                                newRecord = tableAction.newRecord()
                                                newRecord.setValue('createDatetime',  toVariant(currentDateTime))
                                                newRecord.setValue('createPerson_id', toVariant(QtGui.qApp.userId))
                                                newRecord.setValue('modifyDatetime',  toVariant(currentDateTime))
                                                newRecord.setValue('modifyPerson_id', toVariant(QtGui.qApp.userId))
                                                newRecord.setValue('id',              toVariant(None))
                                                newRecord.setValue('event_id',        toVariant(eventId))
                                                newRecord.setValue('actionType_id',   toVariant(actionTypeId))
                                                newRecord.setValue('status',          toVariant(defaultStatus))
                                                newRecord.setValue('begDate',         toVariant(datetime))
                                                newRecord.setValue('directionDate',   toVariant(datetime if datetime < currentDateTime else currentDateTime))
                                                newRecord.setValue('org_id',          toVariant(defaultOrgId if defaultOrgId else QtGui.qApp.currentOrgId()))
                                                newRecord.setValue('setPerson_id',    toVariant(QtGui.qApp.userId))
                                                newRecord.setValue('plannedEndDate',  toVariant(datetime))
                                                newAction = CAction(record=newRecord)
                                                if newAction:
                                                    isBusyJobTicketId = False
                                                    newActionType = newAction.getType()
                                                    propertyTypeList = newActionType.getPropertiesById().values()
                                                    for propertyType in propertyTypeList:
                                                        if propertyType.isJobTicketValueType():
                                                            property = newAction.getPropertyById(propertyType.id)
                                                            if property.type().isJobTicketValueType():
                                                                property.setValue(jobTicketId)
                                                                isBusyJobTicketId = True
                                                    recordAction = db.getRecordEx(tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id'])), 'MAX(Action.idx) AS idxLast', [tableAction['event_id'].eq(eventId), tableAction['deleted'].eq(0), tableActionType['deleted'].eq(0), tableActionType['class'].eq(actionType.class_)])
                                                    idxLast = (forceInt(recordAction.value('idxLast')) + 1) if recordAction else 0
                                                    id = newAction.save(eventId, idx = idxLast, checkModifyDate = False)
                                                    if id:
                                                        if isBusyJobTicketId:
                                                            self.busyJobTicketId.append(jobTicketId)
                                                        newAction.getRecord().setValue('id', toVariant(id))
                                                        checkTissueJournalStatusByActions([(newAction.getRecord(), newAction)])
                                                        recordEvent = db.getRecordEx(tableEvent, 'Event.*', [tableEvent['id'].eq(eventId), tableEvent['deleted'].eq(0)])
                                                        if newAction.getType().closeEvent and recordEvent:
                                                            eventExecDate = forceDate(recordEvent.value('execDate'))
                                                            actionEndDate = forceDateTime(newAction.getRecord().value('endDate'))
                                                            if not eventExecDate and actionEndDate:
                                                                recordEvent.setValue('execDate', QVariant(actionEndDate))
                                                                recordEvent.setValue('isClosed', QVariant(1))
                                                                db.updateRecord('Event', recordEvent)
                                                    newActionTypeCount += 1
                                        db.commit()
                                    except:
                                        db.rollback()
                                        raise
                                except Exception, e:
                                    QtGui.qApp.logCurrentException()
                                    QtGui.QMessageBox.critical( self,
                                                                u'',
                                                                exceptionToUnicode(e),
                                                                QtGui.QMessageBox.Close)
                            else:
                                name = u''
                                if eventId:
                                    clientId = self.clientIdDict.get(eventId, None)
                                    if clientId:
                                        clientRecord = self.clientCache.get(clientId)
                                        if clientRecord:
                                            name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                                               forceString(clientRecord.value('firstName')),
                                               forceString(clientRecord.value('patrName'))) + u', ' + forceString(clientRecord.value('birthDate')) + u', ' + formatSex(clientRecord.value('sex')) + u', ' + forceString(clientId)
                                message = u'''Невозможно сделать назначение пациенту %s: план работ не соответствует плану циклов!'''%(name)
                                QtGui.QMessageBox.warning(self.eventEditor,
                                        u'Внимание!',
                                        message,
                                        QtGui.QMessageBox.Ok)


    def on_appointmentToTreatment(self, row, column):
        if not self.scheduleDateHeader or not self.selectedDate:
            return
        currentRecord = self.scheduleDateHeader.get(pyDate(self.selectedDate), None)
        currentTreatmentTypeId = forceRef(currentRecord.value('treatmentType_id')) if currentRecord else None
        if not currentTreatmentTypeId:
            return
        dateList = []
        for date, record in self.scheduleDateHeader.items():
            treatmentTypeId = forceRef(record.value('treatmentType_id'))
            if currentTreatmentTypeId == treatmentTypeId and date and date not in dateList:
                dateList.append(date)
        self.saveNewAction(row, column, dateList)


    def getActionTypeShowNameList(self, actionTypeId, quantity, actionTypeCount):
        if actionTypeId:
            record = self.actionTypeCache.get(actionTypeId)
            if record:
                return forceStringEx(record.value('name')) + u'(%d/%d)'%(quantity, actionTypeCount)
        return u''


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row < len(self.dates):
                datetimePrev, datetimeLast = self.dates[row]
                if column == 0:
                    if datetimePrev and datetimeLast:
                        timePrev = forceTime(datetimePrev)
                        timeLast = forceTime(datetimeLast)
                        return QVariant(timePrev.toString('hh:mm') + u' - ' + timeLast.toString('hh:mm'))
                else:
                    if self.headers[column] and (((datetimePrev, datetimeLast), self.headers[column]) in self.items.keys()):
                        keyScheme = ((datetimePrev, datetimeLast), self.headers[column])
                        actionTypeId, record, quantity, duration, actionTypeCount = self.items.get(keyScheme, None)
                        return toVariant(self.getActionTypeShowNameList(actionTypeId, quantity, actionTypeCount))
        elif role == Qt.EditRole:
            if row < len(self.dates):
                datetimePrev, datetimeLast = self.dates[row]
                if column == 0:
                    if datetimePrev and datetimeLast:
                        timePrev = forceTime(datetimePrev)
                        timeLast = forceTime(datetimeLast)
                        return QVariant(timePrev.toString('hh:mm') + u' - ' + timeLast.toString('hh:mm'))
                else:
                    if self.headers[column] and (((datetimePrev, datetimeLast), self.headers[column]) in self.items.keys()):
                        keyScheme = ((datetimePrev, datetimeLast), self.headers[column])
                        actionTypeId, record, quantity, duration, actionTypeCount = self.items.get(keyScheme, None)
                        return toVariant(self.getActionTypeShowNameList(actionTypeId, quantity, actionTypeCount))
        return QVariant()


    def getResources(self):
        self.busyJobTicketId = []
        self.actionTypeIdResources = []
        self.dateResources = {}
        if self.orgStructureId:
            db = QtGui.qApp.db
            tableTreatmentType = db.table('TreatmentType')
            tableTreatmentSchedule = db.table('TreatmentSchedule')
            tableTreatmentScheme = db.table('TreatmentScheme')
            tableTreatmentSchemeSource = db.table('TreatmentScheme_Source')
            tableJobTicket = db.table('Job_Ticket')
            tableJob = db.table('Job')
            cond = [tableTreatmentSchedule['orgStructure_id'].eq(self.orgStructureId),
                    u'''TreatmentSchedule.date > (SELECT MAX(TSStart.date)
                                                   FROM TreatmentSchedule AS TSStart
                                                   WHERE TSStart.orgStructure_id = %d
                                                   AND TSStart.date <= %s
                                                   AND TSStart.isStart = 1)'''%(self.orgStructureId, db.formatDate(self.currentDate)),
                    u'''TreatmentSchedule.date < (SELECT MIN(TSEnd.date)
                                                   FROM TreatmentSchedule AS TSEnd
                                                   WHERE TSEnd.orgStructure_id = %d
                                                   AND TSEnd.date >= %s
                                                   AND TSEnd.isEnd = 1)'''%(self.orgStructureId, db.formatDate(self.currentDate)),
                    tableTreatmentScheme['treatmentType_id'].eq(tableTreatmentSchedule['treatmentType_id']),
                    tableTreatmentScheme['endDate'].dateGe(tableTreatmentSchedule['date']),
                    tableJobTicket['datetime'].dateLe(tableTreatmentSchedule['date']),
                    tableJobTicket['deleted'].eq(0),
                    tableJob['deleted'].eq(0)
                    ]
            queryTable = tableTreatmentSchedule.innerJoin(tableTreatmentType, tableTreatmentType['id'].eq(tableTreatmentSchedule['treatmentType_id']))
            queryTable = queryTable.innerJoin(tableTreatmentSchemeSource, tableTreatmentSchemeSource['orgStructure_id'].eq(tableTreatmentSchedule['orgStructure_id']))
            queryTable = queryTable.innerJoin(tableTreatmentScheme, tableTreatmentScheme['id'].eq(tableTreatmentSchemeSource['treatmentScheme_id']))
            queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['id'].eq(tableTreatmentScheme['jobTicket_id']))
            queryTable = queryTable.innerJoin(tableJob, tableJob['id'].eq(tableJobTicket['master_id']))
            cols = [u'DISTINCT TreatmentSchedule.date',
                    tableTreatmentScheme['actionType_id'],
                    tableTreatmentScheme['treatmentType_id'],
                    tableTreatmentScheme['jobTicket_id'],
                    tableJobTicket['datetime'],
                    tableJob['quantity'],
                    tableJob['begTime'],
                    tableJob['endTime'],
                    tableJob['jobType_id'],
                    tableJob['jobPurpose_id'],
                    tableJob['orgStructure_id'],
                    tableJob['capacity'],
                    tableJobTicket['orgStructure_id'].alias('orgStructureIdJT'),
                    tableTreatmentSchedule['isStart'],
                    tableTreatmentSchedule['isEnd']
                    ]
            records = db.getRecordList(queryTable, cols, cond, order='TreatmentSchedule.date, Job_Ticket.datetime, Job_Ticket.idx')
            for record in records:
                date = forceDate(record.value('date'))
                dateResourcesLine = self.dateResources.get(pyDate(date), [])
                dateResourcesLine.append(record)
                self.dateResources[pyDate(date)] = dateResourcesLine
                actionTypeId = forceRef(record.value('actionType_id'))
                if actionTypeId and actionTypeId not in self.actionTypeIdResources:
                    self.actionTypeIdResources.append(actionTypeId)
        self.reset()


    def loadItems(self, eventIdList, currentClientId, selectedDate, scheduleDates, dateHeader):
        self.eventIdList = eventIdList
        self.selectedDate = selectedDate
        self.scheduleDateHeader = dateHeader
        self.scheduleDates = scheduleDates
        self.currentClientId = currentClientId
        self.headers = []
        self.items = {}
        self.dates = []
        self.datesSpan = []
        actionCountBusyItems = {}
        self.scheduleDates.sort()
        if self.selectedDate and self.scheduleDates:
            dateResourcesLine = self.dateResources.get(pyDate(self.selectedDate), [])
            for record in dateResourcesLine:
                date = forceDate(record.value('date'))
                if date == self.selectedDate:
                    actionTypeId = forceRef(record.value('actionType_id'))
                    datetimeJT = forceDateTime(record.value('datetime'))
                    datetime = pyTime(datetimeJT.time())
                    begTime = forceTime(record.value('begTime'))
                    endTime = forceTime(record.value('endTime'))
                    timeToSecs = begTime.secsTo(endTime)
                    capacity = forceInt(record.value('capacity'))
                    quantity = forceInt(record.value('quantity'))
                    duration = math.floor(float(timeToSecs)/quantity)
                    for scheduleDateRow, (scheduleDatePrev, scheduleDateLast) in enumerate(self.scheduleDates):
                        scheduleDatetimePrev = pyTime(scheduleDatePrev)
                        scheduleDatetimeLast = pyTime(scheduleDateLast)
                        if datetime >= scheduleDatetimePrev and datetime < scheduleDatetimeLast:
                            busyDatePrev = pyDateTime(QDateTime(date, scheduleDatePrev))
                            busyDateLast = pyDateTime(QDateTime(date, scheduleDateLast))
                            for i, busyKey in enumerate(self.actionCountBusyDict.keys()):
                                busyDate, busyActionTypeId = busyKey
                                if actionTypeId == busyActionTypeId and busyDate >= busyDatePrev and ((i == (len(self.actionCountBusyDict.keys()) - 1) and (busyDate <= busyDateLast)) or (i < (len(self.actionCountBusyDict.keys()) - 1) and (busyDate < busyDateLast))):
                                    actionCountBusyItems[((scheduleDatetimePrev, scheduleDatetimeLast), actionTypeId)] = self.actionCountBusyDict.get(busyKey, 0) + actionCountBusyItems.get(((scheduleDatetimePrev, scheduleDatetimeLast), actionTypeId), 0)
                            actionCountBusy = actionCountBusyItems.get(((scheduleDatetimePrev, scheduleDatetimeLast), actionTypeId), 0)
                            self.items[((scheduleDatetimePrev, scheduleDatetimeLast), actionTypeId)] = (actionTypeId, record, capacity, duration, actionCountBusy)
                            if (scheduleDatetimePrev, scheduleDatetimeLast) not in self.dates:
                                self.dates.append((scheduleDatetimePrev, scheduleDatetimeLast))
                                self.datesSpan.append((scheduleDatetimePrev, scheduleDatetimeLast))
                            rowSpanCount = int(math.ceil(float(duration/self.minimumDuration)))
                            if rowSpanCount > 0:
                                scheduleDateRow +=1
                                if scheduleDateRow < len(self.scheduleDates):
                                    rowSpanCount += scheduleDateRow - 1
                                    if rowSpanCount < len(self.scheduleDates):
                                        for row in range(scheduleDateRow, rowSpanCount):
                                            scheduleDatePrev, scheduleDateLast = self.scheduleDates[row]
                                            scheduleDatetimePrev = pyTime(scheduleDatePrev)
                                            scheduleDatetimeLast = pyTime(scheduleDateLast)
                                            if (scheduleDatetimePrev, scheduleDatetimeLast) not in self.dates:
                                                self.dates.append((scheduleDatetimePrev, scheduleDatetimeLast))
                                                datetimePrevSpan, datetimeLastSpan = self.datesSpan[len(self.datesSpan)-1]
                                                self.datesSpan[len(self.datesSpan)-1] = (datetimePrevSpan, scheduleDatetimeLast)
                            if actionTypeId and actionTypeId not in self.headers:
                                self.headers.append(actionTypeId)
                            break
            if len(self.headers) > 0:
                self.headers.sort(key=lambda h:CActionTypeCache.getById(h).code)
                self.headers.insert(0, u'')
        self.dates.sort()
        self.reset()


class CRecordsTableModel(QAbstractTableModel):
    __pyqtSignals__ = ('itemsCountChanged(int)',
                      )

    def __init__(self, parent, cols=[], tableName=''):
        QAbstractTableModel.__init__(self, parent)
        self._cols = []
        self.items = []
        self.clientIdList = []
        self.scheduleDateHeader = {}
        self.datetimePrev = None
        self.datetimeLast = None
        self.actionTypeId = None
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


    def beforeRemoveItem(self, itemId):
        jobTicketIdList = []
        if itemId:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            record = db.getRecordEx(tableAction, '*', [tableAction['id'].eq(itemId), tableAction['deleted'].eq(0)])
            if record:
                action = CAction(record=record)
                if action:
                    for property in action.getType()._propertiesById.itervalues():
                        if property.isJobTicketValueType():
                            jobTicketId = action[property.name]
                            if jobTicketId and jobTicketId not in jobTicketIdList:
                                jobTicketIdList.append(jobTicketId)
        return jobTicketIdList


    def afterRemoveItem(self, jobTicketIdList):
        if jobTicketIdList:
            db = QtGui.qApp.db
            tableJobTicket = db.table('Job_Ticket')
            records = db.getRecordList(tableJobTicket, '*', [tableJobTicket['id'].inlist(jobTicketIdList), tableJobTicket['deleted'].eq(0)])
            for record in records:
                record.setValue('status', toVariant(CJobTicketStatus.wait))
                record.setValue('orgStructure_id', toVariant(None))
                db.updateRecord(tableJobTicket, record)


    def removeRow(self, row, parent = QModelIndex()):
        if self.items and 0 <= row < len(self.items):
            itemId = forceRef(self.items[row].value('id'))
            if itemId and self.canRemoveItem(itemId):
                QtGui.qApp.setWaitCursor()
                try:
                    db = QtGui.qApp.db
                    table = db.table('Action')
                    db.transaction()
                    try:
                        jobTicketIdList = self.beforeRemoveItem(itemId)
                        db.deleteRecord(table, table['id'].eq(itemId))
                        self.afterRemoveItem(jobTicketIdList)
                        db.commit()
                    except:
                        db.rollback()
                        raise
                    self.beginRemoveRows(parent, row, row)
                    del self.items[row]
                    self.endRemoveRows()
                    self.emitItemsCountChanged()
                    return True
                finally:
                    QtGui.qApp.restoreOverrideCursor()
        return False


    def beforeRemoveTreatmentItem(self, itemId, clientId):
        totalActionIdList = []
        totalJobTicketIdList = []
        actionJobTicketIdList = []
        dateList = []
        if itemId and clientId:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            record = db.getRecordEx(tableAction, '*', [tableAction['id'].eq(itemId), tableAction['deleted'].eq(0)])
            if record:
                action = CAction(record=record)
                if action:
                    for property in action.getType()._propertiesById.itervalues():
                        if property.isJobTicketValueType():
                            jobTicketId = action[property.name]
                            if jobTicketId and jobTicketId not in actionJobTicketIdList:
                                actionJobTicketIdList.append(jobTicketId)
                            if actionJobTicketIdList:
                                tableJobTicket = db.table('Job_Ticket')
                                records = db.getRecordList(tableJobTicket, [tableJobTicket['datetime']], [tableJobTicket['id'].inlist(actionJobTicketIdList), tableJobTicket['deleted'].eq(0)])
                                for record in records:
                                    date = forceDate(record.value('datetime'))
                                    if date and date not in (dateList):
                                        dateList.append(date)
                                for selectedDate in dateList:
                                    actionIdList, jobTicketIdList = self.getTreatmentDate(selectedDate, clientId)
                                    if actionIdList:
                                        totalActionIdList = list(set(totalActionIdList)|set(actionIdList))
                                    if jobTicketIdList:
                                        totalJobTicketIdList = list(set(totalJobTicketIdList)|set(jobTicketIdList))
        return totalActionIdList, totalJobTicketIdList


    def removeTreatmentRow(self, row, parent = QModelIndex()):
        if self.items and 0 <= row < len(self.items):
            itemId = forceRef(self.items[row].value('id'))
            clientId = forceRef(self.items[row].value('client_id'))
            if itemId and self.canRemoveItem(itemId) and clientId:
                QtGui.qApp.setWaitCursor()
                try:
                    db = QtGui.qApp.db
                    table = db.table('Action')
                    db.transaction()
                    try:
                        actionIdList, jobTicketIdList = self.beforeRemoveTreatmentItem(itemId, clientId)
                        db.deleteRecord(table, table['id'].inlist(actionIdList))
                        self.afterRemoveItem(jobTicketIdList)
                        db.commit()
                    except:
                        db.rollback()
                        raise
                    self.beginRemoveRows(parent, row, row)
                    del self.items[row]
                    self.endRemoveRows()
                    self.emitItemsCountChanged()
                    return True
                finally:
                    QtGui.qApp.restoreOverrideCursor()
        return False


    def getTreatmentDate(self, selectedDate, clientId):
        if not self.scheduleDateHeader or not selectedDate or not self.actionTypeId or not self.datetimePrev or not self.datetimeLast or not clientId:
            return [], []
        currentRecord = self.scheduleDateHeader.get(pyDate(selectedDate), None)
        currentTreatmentTypeId = forceRef(currentRecord.value('treatmentType_id')) if currentRecord else None
        if not currentTreatmentTypeId:
            return [], []
        totalActionIdList = []
        totalJobTicketIdList = []
        dateList = []
        for date, record in self.scheduleDateHeader.items():
            treatmentTypeId = forceRef(record.value('treatmentType_id'))
            if not forceInt(record.value('isStart')) and not forceInt(record.value('isEnd')):
                if currentTreatmentTypeId == treatmentTypeId and date and date not in dateList:
                    actionIdList, jobTicketIdList = self.getTreatmentActions(clientId, self.actionTypeId, QDateTime(date, self.datetimePrev.time()), QDateTime(date, self.datetimeLast.time()))
                    if actionIdList:
                        totalActionIdList = list(set(totalActionIdList)|set(actionIdList))
                    if jobTicketIdList:
                        totalJobTicketIdList = list(set(totalJobTicketIdList)|set(jobTicketIdList))
        return totalActionIdList, totalJobTicketIdList


    def getTreatmentActions(self, clientId, actionTypeId, datetimePrev, datetimeLast):
        if not clientId or not actionTypeId or not datetimePrev or not datetimeLast:
            return [], []
        actionIdList = []
        jobTicketIdList = []
        db = QtGui.qApp.db
        tableRBJobType = db.table('rbJobType')
        tableActionType = db.table('ActionType')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableEvent = db.table('Event')
        tableAction = db.table('Action')
        tableAP = db.table('ActionProperty')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableJobTicket = db.table('Job_Ticket')
        tableJob = db.table('Job')
        cond = [tableEvent['deleted'].eq(0),
                tableEvent['client_id'].eq(clientId),
                tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableActionType['id'].eq(actionTypeId),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                db.joinAnd([tableJobTicket['datetime'].ge(datetimePrev), tableJobTicket['datetime'].lt(datetimeLast)]),
                tableActionPropertyType['id'].eq(tableAP['type_id']),
                tableJobTicket['id'].isNotNull(),
                tableAction['status'].eq(CActionStatus.appointed),
                tableAPJT['value'].eq(tableJobTicket['id'])
                ]
        queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
        LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
        queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
        queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
        queryTable = queryTable.innerJoin(tableAction, tableAction['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        queryTable = queryTable.innerJoin(tableAPJT, tableAP['id'].eq(tableAPJT['id']))
        records = db.getRecordList(queryTable, u'DISTINCT Action.*, Event.client_id, Job_Ticket.idx AS jobTicketIdx, Job_Ticket.id AS jobTicketId', cond, [tableJobTicket['idx'].name(), tableAction['begDate'].name()])
        for record in records:
            actionId = forceRef(record.value('id'))
            if actionId and actionId not in actionIdList:
                actionIdList.append(actionId)
            jobTicketId = forceRef(record.value('jobTicketId'))
            if jobTicketId and jobTicketId not in jobTicketIdList:
                jobTicketIdList.append(jobTicketId)
        return actionIdList, jobTicketIdList


    def canRemoveRow(self, row):
        return self.canRemoveItem(forceRef(self.items[row].value('id')))


    def canRemoveItem(self, itemId):
        return True


    def confirmRemoveRow(self, view, row, multiple=False):
        return self.confirmRemoveItem(view, forceRef(self.items[row].value('id')), multiple)


    def confirmRemoveItem(self, view, itemId, multiple=False):
        buttons = QtGui.QMessageBox.Yes|QtGui.QMessageBox.No
        if multiple:
            buttons |= QtGui.QMessageBox.Cancel
        mbResult = QtGui.QMessageBox.question(view, u'Внимание!', u'Действительно удалить?', buttons, QtGui.QMessageBox.No)
        return {QtGui.QMessageBox.Yes: True,
                QtGui.QMessageBox.No: False}.get(mbResult, None)


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self.items):
            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self.items[row]
                if column == 0:
                    return col.format([row+1, record])
                else:
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
            elif role == Qt.FontRole:
                record = self.items[row]
                clientId = forceRef(record.value('client_id')) if record else None
                if clientId not in self.clientIdList:
                    result = QtGui.QFont()
                    result.setBold(True)
                    return QVariant(result)
        return QVariant()


    def getActionsData(self, clientIdList, datetime, actionTypeId, datetimePrev, datetimeLast):
        if not clientIdList or not datetime or not actionTypeId or not datetimePrev or not datetimeLast:
            return []
        db = QtGui.qApp.db
        tableRBJobType = db.table('rbJobType')
        tableActionType = db.table('ActionType')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableEvent = db.table('Event')
        tableAction = db.table('Action')
        tableAP = db.table('ActionProperty')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableJobTicket = db.table('Job_Ticket')
        tableJob = db.table('Job')
        cond = [tableEvent['deleted'].eq(0),
                tableAction['deleted'].eq(0),
                tableActionType['deleted'].eq(0),
                tableActionType['id'].eq(actionTypeId),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                db.joinOr([tableJobTicket['datetime'].eq(datetime),
                db.joinAnd([tableJobTicket['datetime'].ge(datetimePrev), tableJobTicket['datetime'].lt(datetimeLast)])]),
                tableActionPropertyType['id'].eq(tableAP['type_id']),
                tableJobTicket['id'].isNotNull(),
                tableAction['status'].notInlist([CActionStatus.canceled, CActionStatus.refused]),
                tableAPJT['value'].eq(tableJobTicket['id'])
                ]
        queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
        LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
        queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
        queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
        queryTable = queryTable.innerJoin(tableAction, tableAction['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        queryTable = queryTable.innerJoin(tableAPJT, tableAP['id'].eq(tableAPJT['id']))
        return db.getRecordList(queryTable, u'DISTINCT Action.*, Event.client_id, Job_Ticket.idx AS jobTicketIdx, Job_Ticket.id AS jobTicketId', cond, [tableJobTicket['idx'].name(), tableAction['begDate'].name()])


    def loadData(self, clientIdList, datetime, actionTypeId, datetimePrev, datetimeLast, dateHeader):
        self.items = []
        self.scheduleDateHeader = dateHeader
        self.clientIdList = clientIdList
        self.datetimePrev = datetimePrev
        self.datetimeLast = datetimeLast
        self.actionTypeId = actionTypeId
        if not self.clientIdList or not datetime or not actionTypeId or not datetimePrev or not datetimeLast:
            self.reset()
            return
        self.items = self.getActionsData(self.clientIdList, datetime, actionTypeId, datetimePrev, datetimeLast)
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


    def getClientIdList(self):
        idList = []
        for item in self.items:
            clientId = forceRef(item.value('client_id'))
            if clientId and clientId not in idList:
                idList.append(clientId)
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


    def emitItemsCountChanged(self):
        self.emit(SIGNAL('itemsCountChanged(int)'), len(self.items) if self.items else 0)


class CActionsModel(CRecordsTableModel):
    class CLocNumberColumn(CCol):
        def __init__(self, title, fields, defaultWidth, alignment='l'):
            CCol.__init__(self, title, fields, defaultWidth, alignment)

        def format(self, values):
            return toVariant(forceInt(values[0]))

        def getValue(self, values):
            return forceInt(values[0])

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
                   forceString(clientRecord.value('patrName'))) + u',' + forceString(clientRecord.value('birthDate')) + u',' + formatSex(clientRecord.value('sex')) + u',' + forceString(clientId)
                return toVariant(name)
            return CCol.invalid

    def __init__(self, parent, clientCache):
        CRecordsTableModel.__init__(self, parent)
        self.addColumn(CActionsModel.CLocNumberColumn(u'№', ['id'], 5))
        self.addColumn(CActionsModel.CLocClientColumn( u'Ф.И.О.', ['client_id'], 60, clientCache))
        self.addColumn(CEnumCol(u'Состояние', ['status'], CActionStatus.names, 10))
        self.setTable('Action')


def getTreatmentAppointmentContext():
    return ['treatmentAppointment']

