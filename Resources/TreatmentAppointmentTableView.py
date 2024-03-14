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
from PyQt4.QtCore import SIGNAL, QDateTime, QVariant

from Events.Action     import CAction, CActionTypeCache
from Events.Utils      import checkTissueJournalStatusByActions
from library.database  import CTableRecordCache
from library.TableView import CTableView
from library.Utils     import forceRef, forceInt, forceDate, forceDateTime, exceptionToUnicode, toVariant
from Resources.TreatmentAppointmentClientsEditor import CTreatmentAppointmentClientsEditor


class CTreatmentAppointmentTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)
        self._actUpdateRow = None


    def addPopupUpdateRow(self):
        self._actUpdateRow = QtGui.QAction(u'Добавить пациента', self)
        self._actUpdateRow.setObjectName('actUpdateRow')
        self.connect(self._actUpdateRow, SIGNAL('triggered()'), self.updateCurrentRow)
        self.addPopupAction(self._actUpdateRow)


    def updateCurrentRow(self):
        def updateCurrentRowInternal():
            currentIndex = self.currentIndex()
            if currentIndex.isValid():
                dateSchedule = self.model().dateSchedule
                actionTypeId = self.model().actionTypeId
                if dateSchedule and actionTypeId:
                    row = currentIndex.row()
                    items = self.model().items
                    if row >= 0 and row < len(items):
                        item = items[row]
                        jobTicketId = forceRef(item.value('jobTicketId'))
                        if jobTicketId:
#                            jobTicketIdx = forceInt(item.value('jobTicketIdx'))
                            datetime = forceDateTime(item.value('datetime'))
                            clientId = forceRef(item.value('client_id')) if item else None
                            actionId = forceRef(item.value('id')) if item else None
                            if not clientId and not actionId:
                                db = QtGui.qApp.db
                                clientCache = CTableRecordCache(db, db.forceTable('Client'), u'*', capacity=None)
                                dialog = CTreatmentAppointmentClientsEditor(self, clientCache=clientCache)
                                try:
                                    dialog.loadData(dateSchedule)
                                    dialog.setBusyClientIdList(self.model().getClientIdList())
                                    if dialog.exec_():
                                        eventId, newClientId = dialog.getValue()
                                        if newClientId and eventId:
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
                                                        newActionType = newAction.getType()
                                                        propertyTypeList = newActionType.getPropertiesById().values()
                                                        for propertyType in propertyTypeList:
                                                            if propertyType.isJobTicketValueType():
                                                                property = newAction.getPropertyById(propertyType.id)
                                                                if property.type().isJobTicketValueType():
                                                                    property.setValue(jobTicketId)
                                                        recordAction = db.getRecordEx(tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id'])), 'MAX(Action.idx) AS idxLast', [tableAction['event_id'].eq(eventId), tableAction['deleted'].eq(0), tableActionType['deleted'].eq(0), tableActionType['class'].eq(actionType.class_)])
                                                        idx = (forceInt(recordAction.value('idxLast')) + 1) if recordAction else 0
                                                        id = newAction.save(eventId, idx = idx, checkModifyDate = False)
                                                        if id:
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
                                finally:
                                    dialog.deleteLater()
                                model = self.model()
                                self.model().loadData(model.datetime, model.actionTypeId, model.datetimePrev, model.datetimeLast, model.dateSchedule)
                                self.model().reset()
                                self.setCurrentRow(row)
        QtGui.qApp.call(self, updateCurrentRowInternal)


    def on_popupMenu_aboutToShow(self):
        enable = False
        currentIndex = self.currentIndex()
        curentIndexIsValid = currentIndex.isValid()
        row = currentIndex.row()
        items = self.model().items
        if row >= 0 and row < len(items):
            item = items[row]
            clientId = forceRef(item.value('client_id')) if item else None
            actionId = forceRef(item.value('id')) if item else None
            enable = curentIndexIsValid and not clientId and not actionId
        self._actUpdateRow.setEnabled(enable)
        CTableView.on_popupMenu_aboutToShow(self)

