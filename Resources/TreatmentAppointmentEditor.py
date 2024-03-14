# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                    import QtGui, QtSql
from PyQt4.QtCore             import Qt, QVariant, QModelIndex

from Events.ActionStatus      import CActionStatus
from Events.ActionProperty.JobTicketActionPropertyValueType import CJobTicketActionPropertyValueType
from library.DialogBase       import CDialogBase
from library.TableModel       import CCol
from library.PreferencesMixin import CDialogPreferencesMixin
from library.Utils            import forceRef, forceString, forceStringEx, forceInt, forceDate, formatShortNameInt, formatSex, toVariant
from Reports.Utils            import getDataOrgStructureNameMoving
from Resources.TreatmentAppointmentDialog import CRecordsTableModel

from Resources.Ui_TreatmentAppointmentEditor import Ui_TreatmentAppointmentEditor


class CTreatmentAppointmentEditor(CDialogBase, Ui_TreatmentAppointmentEditor, CDialogPreferencesMixin):
    def __init__(self, parent, filter=None, clientCache=None):
        CDialogBase.__init__(self, parent)
        self.tableModel = CTreatmentActionTableModel(self, clientCache)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(u'Состав группы')
        self.tblTreatmentAppointmentList.setModel(self.tableModel)
        self.tblTreatmentAppointmentList.setSelectionModel(self.tableSelectionModel)
        self.tblTreatmentAppointmentList.installEventFilter(self)
        self.tblTreatmentAppointmentList.addPopupDelRow()
        self.tblTreatmentAppointmentList.addPopupUpdateRow()
        self._parent = parent
        self.dateSchedule = None
        self.clientCache = clientCache
        self.filter = filter
        self.loadDialogPreferences()


    def loadData(self, datetime, actionTypeId, datetimePrev, datetimeLast, dateSchedule):
        self.dateSchedule = dateSchedule
        self.tblTreatmentAppointmentList.model().loadData(datetime, actionTypeId, datetimePrev, datetimeLast, self.dateSchedule)


    def saveData(self):
        return False


class CTreatmentActionTableModel(CRecordsTableModel):
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

    class CLocOrgStructurePresenceColumn(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.caches = {}

        def format(self, values):
            eventId  = forceRef(values[0])
            if eventId:
                orgStructureName = self.caches.get(eventId, None)
                if orgStructureName:
                    return toVariant(orgStructureName)
                record = values[1]
                if record:
                    clientId = forceRef(record.value('client_id'))
                    if not clientId:
                        return CCol.invalid
                    actionDate = forceDate(record.value('begDate'))
                    if not actionDate:
                        actionDate = forceDate(record.value('directionDate'))
                    if actionDate:
                        query = QtGui.qApp.db.query(getDataOrgStructureNameMoving(u'Отделение пребывания', actionDate, clientId, u'moving%%'))
                        if query.first():
                            recordOS = query.record()
                            orgStructureName = forceStringEx(recordOS.value('nameOrgStructure'))
                            self.caches[eventId] = orgStructureName
                            return toVariant(orgStructureName)
            return CCol.invalid

    class CLocActionStatusColumn(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            status = forceInt(values[0])
            if status:
                return toVariant(CActionStatus.names[status])
            record = values[1]
            if record:
                actionId = forceRef(record.value('id'))
                if actionId:
                    return toVariant(CActionStatus.names[forceInt(record.value('status'))])
            return CCol.invalid

    def __init__(self, parent, clientCache):
        CRecordsTableModel.__init__(self, parent)
        self.addColumn(CTreatmentActionTableModel.CLocNumberColumn(u'№', ['id'], 5))
        self.addColumn(CTreatmentActionTableModel.CLocClientColumn( u'Ф.И.О.', ['client_id'], 60, clientCache))
        self.addColumn(CTreatmentActionTableModel.CLocOrgStructurePresenceColumn(u'Отделение пребывания', ['event_id'], 25))
        self.addColumn(CTreatmentActionTableModel.CLocActionStatusColumn(u'Состояние', ['status'], 10))
        self.setTable('Action')
        self.dateSchedule = None
        self.actionTypeId = None
        self.datetime = None
        self.datetimePrev = None
        self.datetimeLast = None


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self.items):
            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self.items[row]
                if column == 0:
                    jobTicketIdx = forceInt(record.value('jobTicketIdx'))
                    return col.format([jobTicketIdx+1, record])
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
        return QVariant()


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
                    oldRecord = self.items[row]
                    jobTicketIdx = forceInt(oldRecord.value('jobTicketIdx'))
                    jobTicketId = forceRef(oldRecord.value('jobTicketId'))
                    datetime = forceRef(oldRecord.value('datetime'))
                    newRecord = self.getRecordAfterRemove()
                    newRecord.setValue('jobTicketIdx', toVariant(jobTicketIdx))
                    newRecord.setValue('jobTicketId', toVariant(jobTicketId))
                    newRecord.setValue('datetime', toVariant(datetime))
                    self.items[row] = newRecord
                    self.emitItemsCountChanged()
                    return True
                finally:
                    QtGui.qApp.restoreOverrideCursor()
        return False


    def getRecordAfterRemove(self):
        tableJobTicket = QtGui.qApp.db.table('Job_Ticket')
        record = tableJobTicket.newRecord()
        for i in range(0, record.count()):
            record.remove(i)
        record.append(QtSql.QSqlField('jobTicketIdx', QVariant.Int))
        record.append(QtSql.QSqlField('jobTicketId', QVariant.Int))
        record.append(QtSql.QSqlField('datetime', QVariant.DateTime))
        return record


    def loadData(self, datetime, actionTypeId, datetimePrev, datetimeLast, dateSchedule):
        self.dateSchedule = dateSchedule
        self.actionTypeId = actionTypeId
        self.datetime = datetime
        self.datetimePrev = datetimePrev
        self.datetimeLast = datetimeLast
        self.items = []
        jobTickedData = {}
        busyJobTicketIdList = []
        if not datetime or not self.actionTypeId or not datetimePrev or not datetimeLast:
            self.reset()
            return
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
        cond = [tableActionType['deleted'].eq(0),
                tableActionType['id'].eq(self.actionTypeId),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                db.joinOr([tableJobTicket['datetime'].eq(datetime),
                db.joinAnd([tableJobTicket['datetime'].ge(datetimePrev), tableJobTicket['datetime'].lt(datetimeLast)])]),
                tableJobTicket['id'].isNotNull(),
                tableAPJT['value'].eq(tableJobTicket['id']),
                tableAP['action_id'].eq(tableAction['id']),
                tableAP['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableAction['deleted'].eq(0),
                tableAction['status'].notInlist([CActionStatus.canceled, CActionStatus.refused])
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
        records = db.getRecordList(queryTable, u'DISTINCT Action.*, Event.client_id, Job_Ticket.idx AS jobTicketIdx, Job_Ticket.id AS jobTicketId, Job_Ticket.datetime', cond, [tableJobTicket['idx'].name(), tableAction['begDate'].name(), tableJobTicket['datetime'].name()])
        for record in records:
            jobTicketIdx = forceInt(record.value('jobTicketIdx'))
            jobTicketId = forceRef(record.value('jobTicketId'))
            clientId = forceRef(record.value('client_id'))
            jobTickedData[(jobTicketIdx, jobTicketId, clientId)] = record
            if jobTicketId and jobTicketId not in busyJobTicketIdList:
                busyJobTicketIdList.append(jobTicketId)

        cond = [tableActionType['id'].eq(self.actionTypeId),
                tableActionPropertyType['deleted'].eq(0),
                tableActionPropertyType['typeName'].like(CJobTicketActionPropertyValueType.name),
                tableActionPropertyType['valueDomain'].isNotNull(),
                tableActionType['isUsesCycles'].eq(1),
                tableJob['deleted'].eq(0),
                tableJobTicket['deleted'].eq(0),
                db.joinOr([tableJobTicket['datetime'].eq(datetime),
                db.joinAnd([tableJobTicket['datetime'].ge(datetimePrev), tableJobTicket['datetime'].lt(datetimeLast)])]),
                tableJobTicket['id'].isNotNull()
                ]
        if busyJobTicketIdList:
            cond.append(tableJobTicket['id'].notInlist(busyJobTicketIdList))
        queryTable = tableActionType.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBJobType, u'''rbJobType.code = IF(INSTR(ActionPropertyType.valueDomain, ';') > 0,
        LEFT(ActionPropertyType.valueDomain, INSTR(ActionPropertyType.valueDomain, ';')-1), ActionPropertyType.valueDomain)''')
        queryTable = queryTable.innerJoin(tableJob, tableJob['jobType_id'].eq(tableRBJobType['id']))
        queryTable = queryTable.innerJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
        records = db.getRecordList(queryTable, u'DISTINCT Job_Ticket.idx AS jobTicketIdx, Job_Ticket.id AS jobTicketId, Job_Ticket.datetime', cond, [tableJobTicket['idx'].name(), tableJobTicket['datetime'].name()])
        for record in records:
            jobTicketIdx = forceInt(record.value('jobTicketIdx'))
            jobTicketId = forceRef(record.value('jobTicketId'))
            jobTickedData[(jobTicketIdx, jobTicketId, None)] = record

        jobTickedDataKeys = jobTickedData.keys()
        jobTickedDataKeys.sort(key=lambda x: (x[0], x[1]))
        for jobTickedKey in jobTickedDataKeys:
            self.items.append(jobTickedData[jobTickedKey])

        self.reset()


