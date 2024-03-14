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

from PyQt4        import QtGui
from PyQt4.QtCore import QDateTime, QVariant, SIGNAL


from library.DialogBase                import CDialogBase
# InputDialog.py уже не в library, а в Events.
# В library лежит InputDialog.pyc и все работает. Не убиваемая система
from Events.InputDialog                import CJobTiketDoneDateTimeInputWithPresetDialog
from library.RecordLock                import  CRecordLockMixin
from library.Utils                     import forceBool, forceDate, forceInt, forceRef

from Events.ActionStatus               import CActionStatus
from Events.EventJobTicketsEditorTable import CEventJobTicketsModel
from Resources.JobTicketStatus         import CJobTicketStatus

from Events.Ui_EventJobTicketsEditorDialog    import Ui_EventJobTicketsEditor


class CEventJobTicketsEditor(CDialogBase, Ui_EventJobTicketsEditor):
    def __init__(self, parent, emptyActionModelsItemList, fullActionModelsItemList, clientId, eventEditor):
        CDialogBase.__init__(self, parent)

        self._parent = parent
        self._eventEditor = eventEditor or parent
        self._clientId = clientId
        self.addModels('SetEventJobTickets',    CEventJobTicketsModel(self, emptyActionModelsItemList, clientId))
        self.addModels('ChangeEventJobTickets', CEventJobTicketsModel(self, fullActionModelsItemList,  clientId))

        self.setupUi(self)

        self.setModels(self.tblSetEventJobTickets, self.modelSetEventJobTickets,
                       self.selectionModelSetEventJobTickets)
        self.setModels(self.tblChangeEventJobTickets, self.modelChangeEventJobTickets,
                       self.selectionModelChangeEventJobTickets)
        self.tblSetEventJobTickets.expandAll()
        self.tblChangeEventJobTickets.expandAll()
        self.connect(self.btnCloseJobTickets, SIGNAL('clicked()'), self.on_btnCloseJobTickets)
        self.connect(self.modelSetEventJobTickets,    SIGNAL('itemChecked()'), self.on_itemChecked)
        self.connect(self.modelChangeEventJobTickets, SIGNAL('itemChecked()'), self.on_itemChecked)
        self.setWindowTitle(u'Назначение работ')
        self._jobTicketRecordsMap2PostUpdate = {}
        self._actions2Update = {}
        self.checkActualTab()
        self.checkAll()
        self.on_itemChecked()


    def setBtnCloseJobTicketsVisible(self, value):
        self.btnCloseJobTickets.setVisible(value)
        self.modelChangeEventJobTickets.setCheckable(False)
        self.modelSetEventJobTickets.setCheckable(False)


    def checkAll(self):
        self.checkEmpty()
        self.checkFull()


    def checkEmpty(self):
        self.modelSetEventJobTickets.checkAll()


    def checkFull(self):
        self.modelChangeEventJobTickets.checkAll()


    def checkActualTab(self):
        if not self.existsEmpty() and self.existsFull():
           self.tabWidget.setCurrentIndex(1)


    def existsEmpty(self):
        return len(self.modelSetEventJobTickets.actionModelsItemList())


    def existsFull(self):
        return len(self.modelChangeEventJobTickets.actionModelsItemList())


    def on_itemChecked(self):
        self.btnCloseJobTickets.setEnabled(self.existsCheckedItems())


    def existsCheckedItems(self):
        return self.modelChangeEventJobTickets.hasCheckedItems() or self.modelSetEventJobTickets.hasCheckedItems()


    def mapActions2Update(self, actionItemList, dateTime, actionStatusChanger, actionPersonChanger, actionDateChanger):
        for actionItem in actionItemList:

            actionRecord, action = actionItem

            changes = self._actions2Update.setdefault(actionItem, {})

            if actionStatusChanger is not None:
                changes['status'] = actionStatusChanger
            if actionPersonChanger:
                if actionPersonChanger == 1:
                    changes['person_id'] = QtGui.qApp.userId
                elif actionPersonChanger == 2:
                    changes['person_id'] = forceRef(actionRecord.value('setPerson_id'))
                elif actionPersonChanger == 3:
                    changes['person_id'] = self.getEventExecPersonId()
            if actionDateChanger == 1:
                if dateTime and not forceDate(actionRecord.value('endDate')).isValid():
                    changes['endDate'] = dateTime
                    if not actionStatusChanger:
                        changes['status'] = CActionStatus.finished



    def getEventExecPersonId(self):
        return self._eventEditor.getExecPersonId()


    def getEventId(self):
        return self._eventEditor.getEventId()


    def getEventTypeId(self):
        return self._eventEditor.getEventTypeId()


    def applyJobTypeModifier(self):
        for (actionRecord, action), changes in self._actions2Update.items():
            for field in changes.keys():
                actionRecord.setValue(field, QVariant(changes[field]))


    def getCondForDateTimeSearching(self):
        checkedResult   = self.getCheckedJobTicketItemValues()
        jobTicketIdList = [item[0] for item in checkedResult.keys()]
        jobTypeIdList   = [item[1] for item in checkedResult.keys()]
        return jobTicketIdList, jobTypeIdList


    def on_btnCloseJobTickets(self):
        checkedResult = self.getCheckedJobTicketItemValues()
        allResult     = self.getAllJobTicketItemValues()

        prefs = QtGui.qApp.preferences.appPrefs

        jobTicketEndDateAskingIsRequired = forceBool(prefs.get('jobTicketEndDateAskingIsRequired', QVariant(True)))

        if jobTicketEndDateAskingIsRequired:
            dlg = CJobTiketDoneDateTimeInputWithPresetDialog(self, clientId=self._clientId)
            if dlg.exec_():
                dateTime = dlg.dateTime()
            else:
                dateTime = QDateTime()
        else:
            dateTime = QDateTime.currentDateTime()

        if not dateTime:
            return

        jobTypeIdChangerValuesMap = {}
        db = QtGui.qApp.db

        for (jobTicketId, jobTypeId),  actionItemList in checkedResult.items():
            jobTypeIdChangerValues = jobTypeIdChangerValuesMap.get(jobTypeId, None)
            if jobTypeIdChangerValues is None:
                jobTypeIdChangerValues = (
                                          forceRef(db.translate('rbJobType', 'id', jobTypeId, 'actionStatusChanger')),
                                          forceInt(db.translate('rbJobType', 'id', jobTypeId, 'actionPersonChanger')),
                                          forceInt(db.translate('rbJobType', 'id', jobTypeId, 'actionDateChanger'))
                                         )
                jobTypeIdChangerValuesMap[jobTypeId] = jobTypeIdChangerValues
            actionStatusChanger, actionPersonChanger, actionDateChanger = jobTypeIdChangerValues
            self.mapActions2Update(actionItemList,
                                   dateTime,
                                   actionStatusChanger,
                                   actionPersonChanger,
                                   actionDateChanger)
            setJobEnded = True
            allActionItemList = allResult[(jobTicketId, jobTypeId)]
            for allActionItem in allActionItemList:
                if allActionItem in self._actions2Update:
                    status = self._actions2Update[allActionItem].get('status', None)
                else:
                    actionRecord, action = allActionItem
                    status = forceInt(actionRecord.value('status'))

                if status != CActionStatus.finished:
                    setJobEnded = False
                    break

            jobTicketRecord = db.getRecord('Job_Ticket', '*', jobTicketId)
            jobTicketRecord.setValue('endDateTime', QVariant(dateTime))
            if setJobEnded:
                jobTicketRecord.setValue('status', QVariant(CJobTicketStatus.done))
            else:
                jobTicketRecord.setValue('status', QVariant(CJobTicketStatus.doing))
            self._jobTicketRecordsMap2PostUpdate[jobTicketId] = jobTicketRecord
        self.accept()


    def getJobTicketRecordsMap2PostUpdate(self):
        return self._jobTicketRecordsMap2PostUpdate


    def getCheckedJobTicketItemValues(self):
        result = {}
        tmpResult = self.modelSetEventJobTickets.getCheckedJobTicketItemValues()
        for jobTicketValues, actionItemList in tmpResult.items():
            value = result.setdefault(jobTicketValues, [])
            value.extend(actionItemList)
        tmpResult = self.modelChangeEventJobTickets.getCheckedJobTicketItemValues()
        for jobTicketValues, actionItemList in tmpResult.items():
            value = result.setdefault(jobTicketValues, [])
            value.extend(actionItemList)
        return result


    def getAllJobTicketItemValues(self):
        result = {}
        tmpResult = self.modelSetEventJobTickets.getAllJobTicketItemValues()
        for jobTicketValues, actionItemList in tmpResult.items():
            value = result.setdefault(jobTicketValues, [])
            value.extend(actionItemList)
        tmpResult = self.modelChangeEventJobTickets.getAllJobTicketItemValues()
        for jobTicketValues, actionItemList in tmpResult.items():
            value = result.setdefault(jobTicketValues, [])
            value.extend(actionItemList)
        return result


    def exec_(self):
        result = CDialogBase.exec_(self)
        if result:
            self.modelSetEventJobTickets.setCheckedValues()
            self.modelChangeEventJobTickets.changeCheckedValues()
            self.modelSetEventJobTickets.setPlannedEndDate()
            self.modelChangeEventJobTickets.setPlannedEndDate()
            self.applyJobTypeModifier()
        else:
            self._jobTicketRecordsMap2PostUpdate.clear()
        return result


class CEventJobTicketsListEditor(CEventJobTicketsEditor, CRecordLockMixin):
    def __init__(self, parent, emptyActionModelsItemList, fullActionModelsItemList, clientId, eventEditor):
        CEventJobTicketsEditor.__init__(self, parent, emptyActionModelsItemList, fullActionModelsItemList, clientId, eventEditor)
        CRecordLockMixin.__init__(self)
        self.isJobTicketId = False
        self.edtJobTicketIdList = []


    def exec_(self):
        result = CDialogBase.exec_(self)
        if result:
            db = QtGui.qApp.db
            lockAction = True
            modelItems = self.modelSetEventJobTickets.actionModelsItemList() + self.modelChangeEventJobTickets.actionModelsItemList()
            for item in modelItems:
                record, action = item
                actionType = action.getType()
                actionId = action.getId()
                propertyTypeList = actionType.getPropertiesById().items()
                for propertyTypeId, propertyType in propertyTypeList:
                    if propertyType.isJobTicketValueType():
                        property    = action.getPropertyById(propertyType.id)
                        jobTicketId = property.getValue()
                        break
                if jobTicketId and actionId:
                    if not self.lock('Action', actionId):
                        try:
                            lockAction = False
                        finally:
                            self.releaseLock()
                        return result
            if not lockAction:
                return result
            try:
                db.transaction()
                try:
                    self.modelSetEventJobTickets.setCheckedValues()
                    self.modelChangeEventJobTickets.changeCheckedValues()
                    self.modelSetEventJobTickets.setPlannedEndDate()
                    self.modelChangeEventJobTickets.setPlannedEndDate()
                    self.applyJobTypeModifier()
                    for actionRecord, action in self.modelSetEventJobTickets.actionModelsItemList() + self.modelChangeEventJobTickets.actionModelsItemList():
                        action.save(idx=-1)
                    ticketList = self.getCheckedJobTicketItemValues()
                    idList = ','.join(str(id) for (id, tmp) in ticketList.keys())
                    self.isJobTicketId = True
                    self.edtJobTicketIdList = idList
                    db.commit()
                except:
                    db.rollback()
                    self.isJobTicketId = False
                    self.edtJobTicketIdList = []
                    QtGui.qApp.logCurrentException()
                    raise
            finally:
                self.releaseLock()
        else:
            self._jobTicketRecordsMap2PostUpdate.clear()
        return result


class CEventJobTicketsLockEditor(CEventJobTicketsEditor, CRecordLockMixin):
    def __init__(self, parent, emptyActionModelsItemList, fullActionModelsItemList, clientId, eventEditor):
        CEventJobTicketsEditor.__init__(self, parent, emptyActionModelsItemList, fullActionModelsItemList, clientId, eventEditor)
        CRecordLockMixin.__init__(self)
        self.tblChangeEventJobTickets.addActEditMultiTickets()


    def exec_(self):
        result = CDialogBase.exec_(self)
        if result:
            db = QtGui.qApp.db
            lockAction = True
            modelItems = self.modelChangeEventJobTickets.actionModelsItemList()
            for item in modelItems:
                record, action = item
                actionType = action.getType()
                actionId = action.getId()
                propertyTypeList = actionType.getPropertiesById().items()
                for propertyTypeId, propertyType in propertyTypeList:
                    if propertyType.isJobTicketValueType():
                        property    = action.getPropertyById(propertyType.id)
                        jobTicketId = property.getValue()
                        break
                if jobTicketId and actionId:
                    if not self.lock('Action', actionId):
                        try:
                            lockAction = False
                        finally:
                            self.releaseLock()
                        return result
            if not lockAction:
                return result
            try:
                db.transaction()
                try:
                    self.modelSetEventJobTickets.setCheckedValues()
                    self.modelChangeEventJobTickets.changeCheckedValues()
                    self.modelSetEventJobTickets.setPlannedEndDate()
                    self.modelChangeEventJobTickets.setPlannedEndDate()
                    self.applyJobTypeModifier()
                    db.commit()
                except:
                    db.rollback()
                    QtGui.qApp.logCurrentException()
                    raise
            finally:
                self.releaseLock()
        else:
            self._jobTicketRecordsMap2PostUpdate.clear()
        return result

# ###################################################################

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    w = CEventJobTicketsEditor(None)
    w.show()
    app.exec_()

