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
from PyQt4.QtCore import Qt, QDate, QDateTime, QVariant, SIGNAL

# InputDialog.py уже не в library, а в Events.
# В library лежит InputDialog.pyc и все работает. Не убиваемая система
from Events.InputDialog        import COrgStructureInputDialog
from Users.Rights import urCanAddExceedJobTicket
from library.PreferencesMixin   import CPreferencesMixin
from library.TreeModel          import CTreeItem, CTreeModel
from library.TreeView           import CTreeView
from library.Utils              import forceDate, forceDateTime, forceInt, forceRef, forceString, getPref, setPref, toVariant

from Events.Action              import CActionType
from Events.ActionProperty      import CJobTicketActionPropertyValueType, CActionPropertyValueTypeRegistry
from Resources.JobTicketChooser import getJobTicketAsText, getJobTicketsQueryParts, CJobTicketChooserDialog
from Resources.JobTicketChooserHelper import CJobTicketChooserHelper, createExceedJobTicket


class CEventJobTicketsBaseItem(CTreeItem):
    def __init__(self, parent, model):
        self._model = model
        CTreeItem.__init__(self, parent, self._getName())


    def setCheckedValues(self):
        pass


    def changeCheckedValues(self):
        pass


    def loadChildren(self):
        return []


    def _getName(self):
        return ''


    def model(self):
        return self._model



class CEventJobTicketsItem(CEventJobTicketsBaseItem):
    nameColumn      = 0
    jobTicketColumn = 1
    def __init__(self, parent, model):
        self._checked = False
        self._jobTicketId = None
        CEventJobTicketsBaseItem.__init__(self, parent, model)


    def getJobTiketsItemList(self):
        return []


    def hasCheckedItems(self):
        if self._checked:
            return True
        for item in self.items():
            if item.hasCheckedItems():
                return True
        return False



    def setCheckedValues(self):
        for item in self.items():
            item.setCheckedValues()


    def changeCheckedValues(self):
        for item in self.items():
            item.changeCheckedValues()


    def jobTicketId(self):
        return self._jobTicketId


    def flags(self, column):
        flags = CEventJobTicketsBaseItem.flags(self)
        if column == CEventJobTicketsItem.nameColumn and self.model()._isCheckable:
            flags = flags | Qt.ItemIsUserCheckable
        elif column == CEventJobTicketsItem.jobTicketColumn:
            flags = flags | Qt.ItemIsEditable
        return flags


    def setChecked(self, value=None):
        if value is None:
            self._checked = not self._checked
        else:
            self._checked = value
        for item in self.items():
            item.setChecked(self._checked)


    def setJobTicketId(self, jobTicketId, force=True):
        self._jobTicketId = jobTicketId
        for item in self.items():
            item.setJobTicketId(self._jobTicketId, force=force)


    def checked(self):
        return self._checked


    def data(self, column):
        if column == 0:
            return toVariant(self._name)
        elif column == 1:
            return toVariant(getJobTicketAsText(self.jobTicketId()))
        else:
            return QVariant()

    def action(self):
        return None


class CEventJobTicketsJobTypeItem(CEventJobTicketsItem):
    def __init__(self, parent, jobTypeId, domain, model):
        self._jobTypeId = jobTypeId
        self._domain = domain
        CEventJobTicketsItem.__init__(self, parent, model)
        self._items = []


    def domain(self):
        return self._domain


    def _getName(self):
        result = forceString(QtGui.qApp.db.translate('rbJobType', 'id',
                                                     self._jobTypeId, 'CONCAT_WS(\' | \', code, name)'))
        if not result:
            result = u'----'

        return result


    def getActionItemList(self):
        return self._items


    def jobTicketIdActions(self, onlyChecked=False):
        result = {}
        for item in self.items():
            if item.checked() or not onlyChecked:
                value = result.setdefault((item.jobTicketId(), self.jobTypeId()), [])
                value.append(item.actionItem())
        return result


    def addItem(self, actionItem, jobTicketId=None):
        self._items.append(CEventJobTicketsActionItem(self, actionItem, jobTicketId, self.model()))


    def getCommonJobTicketId(self):
        jobTicketIdSet = set(
            item._jobTicketId for item in self._items if item._jobTicketId is not None
        )

        if len(jobTicketIdSet) == 1:
            return jobTicketIdSet.pop()

        return None


    def jobTypeId(self):
        return self._jobTypeId


    def loadChildren(self):
        return self._items


class CEventJobTicketsActionItem(CEventJobTicketsItem):
    def __init__(self, parent, actionItem, jobTicketId, model):
        self._actionItem  = actionItem
        CEventJobTicketsItem.__init__(self, parent, model)
        self.setJobTicketId(jobTicketId)


    def getActionItemList(self):
        return [self]


    def setCheckedValues(self):
        if self.checked() and self.jobTicketId():
            self.setCheckedValuesEx()


    def changeCheckedValues(self):
        if self.checked():
            self.setCheckedValuesEx()


    def setCheckedValuesEx(self):
        action           = self.action()
        actionType       = action.getType()
        propertyTypeList = actionType.getPropertiesById().values()
        jobTicketId = self.jobTicketId()
        for propertyType in propertyTypeList:
            property     = action.getPropertyById(propertyType.id)
            if property.type().isJobTicketValueType():
                property.setValue(jobTicketId)
                dateTimeJT = forceDateTime(QtGui.qApp.db.translate('Job_Ticket', 'id', jobTicketId, 'datetime'))
                dateJT = dateTimeJT.date()
                dateJT = dateJT.addDays(self.model().getTicketDuration(jobTicketId))
                action.getRecord().setValue('plannedEndDate', QVariant(dateJT))
                actionType = action._actionType
                if actionType:
                    if actionType.defaultBegDate == CActionType.dbdJobTicketTime:
                        action.getRecord().setValue('begDate', QVariant(dateTimeJT))


    def setJobTicketId(self, jobTicketId, force=True):
        if force or not self._jobTicketId:
            self._jobTicketId = jobTicketId


    def action(self):
        return self.actionItem()[1]


    def record(self):
        return self.actionItem()[0]


    def actionItem(self):
        return self._actionItem


    def _getName(self):
        return self.action().getType().name


    def domain(self):
        return self.parent().domain()


    def jobTypeId(self):
        return self.parent().jobTypeId()


    def jobTicketId(self):
        return self._jobTicketId


class CEventJobTicketsRootItem(CEventJobTicketsItem):
    def __init__(self, model):
        CEventJobTicketsItem.__init__(self, None, model)
        self._mapJobTypeIdToItem = {}


    def getCheckedJobTicketItemValues(self):
        return self.getAllJobTicketItemValues(onlyChecked=True)


    def setChecked(self, value=None):
        if self.model().rootItemVisible:
            CEventJobTicketsItem.setChecked(self, value)
        else:
            for item in self.items():
                item.setChecked(value)


    def getAllJobTicketItemValues(self, onlyChecked=False):
        result = {}
        for item in self._mapJobTypeIdToItem.values():
            tmpResult = item.jobTicketIdActions(onlyChecked=onlyChecked)
            for jobTicketValues, actionItemList in tmpResult.items():
                value = result.setdefault(jobTicketValues, [])
                value.extend(actionItemList)
        return result


    def getJobTypeItem(self, jobTypeId, domain):
        result = self._mapJobTypeIdToItem.get(jobTypeId, None)
        if not result:
            result = CEventJobTicketsJobTypeItem(self, jobTypeId, domain, self.model())
            self._mapJobTypeIdToItem[jobTypeId] = result
        return result


    def loadChildren(self):
        def getJobTypeId(domain):
            valType = CActionPropertyValueTypeRegistry.get('JobTicket', domain)
            return valType.getJobTypeId()

        modelItems = self.model().actionModelsItemList()
        for item in modelItems:
            record, action = item
            actionType = action.getType()
            propertyTypeList = actionType.getPropertiesById().items()
            for propertyTypeId, propertyType in propertyTypeList:
                if propertyType.isJobTicketValueType():
                    domain      = propertyType.valueDomain
                    jobTypeId   = getJobTypeId(domain)
                    jobTypeItem = self.getJobTypeItem(jobTypeId, domain)

                    property    = action.getPropertyById(propertyType.id)
                    jobTicketId = property.getValue()

                    jobTypeItem.addItem(item, jobTicketId)
                    break
        for jobTypeItem in self._mapJobTypeIdToItem.itervalues():
            jobTicketId = jobTypeItem.getCommonJobTicketId()
            if jobTicketId:
                jobTypeItem.setJobTicketId(jobTicketId, False)


        return self._mapJobTypeIdToItem.values()


class CEventJobTicketsModel(CTreeModel):
    names = [u'Наименование', u'Номерок']
    def __init__(self, parent, actionModelsItemList, clientId):
        self._actionModelsItemList = actionModelsItemList
        self._clientId = clientId
        self._parent   = parent
        CTreeModel.__init__(self, parent, CEventJobTicketsRootItem(self))
        self.rootItemVisible = False
        self._jobIdToTicketDuration = {}
        self._isCheckable = True
        self._mapJobTicketId2PlannedEndDate = {}
        self._actionItemListToSetEndPlannedDate = {}


    def setCheckable(self, value):
        self._isCheckable = value
#        self.reset()


    def getTicketDuration(self, jobTicketId):
        db = QtGui.qApp.db
        jobId = forceRef(db.translate('Job_Ticket', 'id', jobTicketId, 'master_id'))
        result = self._jobIdToTicketDuration.get(jobId, None)
        if result is None:
            jobTypeId = forceRef(db.translate('Job', 'id', jobId, 'jobType_id'))
            result = forceInt(db.translate('rbJobType', 'id', jobTypeId, 'ticketDuration'))
            self._jobIdToTicketDuration[jobId] = result
        return result


    def isIndexItemHasJobTicket(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return isinstance(item, CEventJobTicketsActionItem)


    def checkAll(self):
        self.getRootItem().setChecked(True)


    def getEventId(self):
        return self._parent.getEventId()


    def getEventTypeId(self):
        return self._parent.getEventTypeId()


    def setCheckedValues(self):
        self.getRootItem().setCheckedValues()


    def changeCheckedValues(self):
        self.getRootItem().changeCheckedValues()


    def actionModelsItemList(self):
        return self._actionModelsItemList


    def hasCheckedItems(self):
        return self.getRootItem().hasCheckedItems()


    def getCheckedJobTicketItemValues(self):
        return self.getRootItem().getCheckedJobTicketItemValues()


    def getAllJobTicketItemValues(self):
        return self.getRootItem().getAllJobTicketItemValues()


    def columnCount(self, parent=None):
        return 2


    def clientId(self):
        return self._clientId


    def getEditorInitValues(self, index):
        item = index.internalPointer()
        return self.getEditorInitValuesByItem(item)

    def getEditorInitValuesByItem(self, item):
        clientId = self.clientId()
        if item:
            action = item.action()
            domain = item.domain()
            return action, domain, clientId
        return None, None, clientId


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and section in (0, 1) and role == Qt.DisplayRole:
            return QVariant(CEventJobTicketsModel.names[section])
        return QVariant()


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        item = index.internalPointer()
        if not item:
            return Qt.NoItemFlags
        return item.flags(index.column())


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        column = index.column()
        if role == Qt.CheckStateRole and self._isCheckable and column == CEventJobTicketsItem.nameColumn:
            item = index.internalPointer()
            if item:
                return QVariant(item.checked())
        elif role == Qt.EditRole and column == CEventJobTicketsItem.jobTicketColumn:
            item = index.internalPointer()
            if item:
                return QVariant(item.jobTicketId())
        elif role == Qt.FontRole:
            if self.isIndexItemHasJobTicket(index):
                item = index.internalPointer()
                if item:
                    rec = item.record()
                    if rec and self.getEventId() != forceRef(rec.value('event_id')):
                        result = QtGui.QFont()
                        result.setBold(True)
                        return QVariant(result)
        else:
            return CTreeModel.data(self, index, role)


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole:
            item = index.internalPointer()
            if item:
                item.setChecked()
                self.emitColumnChanged(index.column())
                self.emit(SIGNAL('itemChecked()'))
                return True

        elif role == Qt.EditRole:
            item = index.internalPointer()
            if item:
                jobTicketId = forceRef(value)
                item.setJobTicketId(jobTicketId)
                self._applayPlannedEndDate(item, jobTicketId)
                self.emitColumnChanged(index.column())
                return True
        return False


    def getPlannedEndDateByJobTicketId(self, jobTicketId):
        if jobTicketId is None:
            return QDateTime()
        elif jobTicketId in self._mapJobTicketId2PlannedEndDate:
            plannedEndDate = self._mapJobTicketId2PlannedEndDate[jobTicketId]
        else:
            date = forceDate(QtGui.qApp.db.translate('Job_Ticket', 'id', jobTicketId, 'datetime'))
            plannedEndDate = date.addDays(self.getTicketDuration(jobTicketId))
            self._mapJobTicketId2PlannedEndDate[jobTicketId] = plannedEndDate
        return plannedEndDate


    def _applayPlannedEndDate(self, item, jobTicketId):
        plannedEndDate = self.getPlannedEndDateByJobTicketId(jobTicketId)

        actionItemList = item.getActionItemList()
        for modelItem in actionItemList:
            actionRecord, action = modelItem.actionItem()
            actionType = action.getType()
            if actionType.defaultPlannedEndDate == actionType.dpedJobTicketDate:
                self._actionItemListToSetEndPlannedDate[actionRecord] = (action, plannedEndDate)


    def setPlannedEndDate(self):
        for actionRecord, (action, plannedEndDate) in self._actionItemListToSetEndPlannedDate.items():
            actionRecord.setValue('plannedEndDate', QVariant(plannedEndDate))


    def _getExceedQuantityJobTicketId(self, jobTypeId, date):
        def _getJobId(jobTypeId, date):
            db = QtGui.qApp.db
            table = db.table('Job')
            cond = [table['date'].eq(date),
                    table['jobType_id'].eq(jobTypeId),
                    table['deleted'].eq(0)]
            record = db.getRecordEx(table, 'id', cond)
            if record:
                return forceRef(record.value('id'))
            return None

        jobId = _getJobId(jobTypeId, date)
        if jobId:
            return createExceedJobTicket(jobId)
        return None


    def _getForceJobTicketOnCurrentDay(self, tbl, index):

        def _getJobTicketIdList(editor, ticketId, jobTypeId, date, exceed, orgStructureId, eventTypeId, clientId):
            if jobTypeId and date:
                db = QtGui.qApp.db
                tableEx, cond = getJobTicketsQueryParts(ticketId, jobTypeId, date, False, orgStructureId, eventTypeId, clientId)
                if exceed:
                    cond.append(db.table('Job_Ticket')['isExceedQuantity'].eq(1))
                else:
                    cond.append(db.table('Job_Ticket')['isExceedQuantity'].eq(0))
                idList = db.getIdList(tableEx, idCol='Job_Ticket.id', where=cond, order='OrgStructure.code, datetime')
            else:
                idList = []
            return idList

        def _getJobTypeId(jobTypeCode):
            return forceRef(QtGui.qApp.db.translate('rbJobType', 'code', jobTypeCode, 'id'))

        action, domain, clientId = self.getEditorInitValues(index)
        date = QDate.currentDate()
        eventTypeId = self.getEventTypeId()
        actionTypeId = forceRef(action._record.value('actionType_id')) if action else None

        valType = CActionPropertyValueTypeRegistry.get('JobTicket', domain)
        editor = CJobTicketActionPropertyValueType.CPropEditor(action, valType.domain, tbl, clientId, eventTypeId)
        jobTypeId = _getJobTypeId(editor.defaultJobTypeCode())
        if jobTypeId:
            orgStructureId = self._getOrgStructureId(jobTypeId)
            if orgStructureId == -1:
                return 0
            jobTicketIdList = _getJobTicketIdList(editor, None, jobTypeId, date, False, orgStructureId, eventTypeId, clientId)
            if jobTicketIdList:
                for jobTicketId in jobTicketIdList:
                    if QtGui.qApp.addJobTicketReservation(jobTicketId):
                        return jobTicketId

            if QtGui.qApp.userHasRight(urCanAddExceedJobTicket):
                if QtGui.QMessageBox.question(self._parent,
                                              u'Внимание!',
                                              u'Свободных талонов на сегодня нет.\nДобавить превышающий выделенное количество?',
                                              QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                              QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                    jobTicketIdList = _getJobTicketIdList(editor, None, jobTypeId, date, True, orgStructureId, eventTypeId, clientId)
                    if jobTicketIdList:
                        for jobTicketId in jobTicketIdList:
                            if QtGui.qApp.addJobTicketReservation(jobTicketId):
                                return jobTicketId
                    else:
                        jobTicketId = self._getExceedQuantityJobTicketId(jobTypeId, date)
                        if jobTicketId:
                            if QtGui.qApp.addJobTicketReservation(jobTicketId):
                                return jobTicketId
                        else:
                            QtGui.QMessageBox.information(self._parent,
                                              u'Внимание!',
                                              u'Работ данного типа на сегодня не запланировано.',
                                              QtGui.QMessageBox.Ok)
                else:
                    if QtGui.QMessageBox.question(self._parent,
                                                  u'Внимание!',
                                                  u'Назначить первый свободный в ближайший день?',
                                                  QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                                  QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                        CJobTicketChooserHelper(jobTypeId, clientId,
                                                eventTypeId,
                                                valType.chainLength(),
                                                True, actionTypeId=actionTypeId).get()
            else:
                if QtGui.QMessageBox.question(self._parent,
                                              u'Внимание!',
                                              u'Свободных талонов на сегодня нет.\nНазначить первый свободный в ближайший день?',
                                              QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                              QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                    CJobTicketChooserHelper(jobTypeId, clientId,
                                            eventTypeId,
                                            valType.chainLength(),
                                            True, actionTypeId=actionTypeId).get()

            return None

        return None

    def _getOrgStructureId(self, jobTypeId):
        def _getOrgStructureByJobTypeId(jobTypeId):
            db = QtGui.qApp.db
            table = db.table('Job')
            cond = [table['jobType_id'].eq(jobTypeId),
                    table['deleted'].eq(0),
                    table['date'].ge(QDate.currentDate()),
                    table['date'].le(QDate.currentDate().addYears(1))
                   ]
            idList = db.getDistinctIdList(table, table['orgStructure_id'].name(), cond)
            return idList
        orgStructureIdList = _getOrgStructureByJobTypeId(jobTypeId)
        if orgStructureIdList:
            if len(orgStructureIdList) == 1:
                return orgStructureIdList[0]

            filterOrgStructureIdList = QtGui.qApp.db.getTheseAndParents('OrgStructure', 'parent_id', orgStructureIdList)
            orgStructureChooser = COrgStructureInputDialog()
            orgStructureChooser.setFilter(
                            QtGui.qApp.db.table('OrgStructure')['id'].inlist(filterOrgStructureIdList))
            if orgStructureChooser.exec_():
                return orgStructureChooser.orgStructure()

            return -1

        return None

    def forceSetJobTicketOnCurrentDay(self, tbl, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                jobTicketId = self._getForceJobTicketOnCurrentDay(tbl, index)
                if jobTicketId:
                    item.setJobTicketId(jobTicketId, force=True)



    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emitIndexChanged(index)


    def emitRowChanged(self, row):
        self.emitRowsChanged(row, row)


    def emitRowsChanged(self, begRow, endRow):
        index1 = self.index(begRow, 0)
        index2 = self.index(endRow, self.columnCount())
        self.emitIndexChanged(index1, index2)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(None), column)
        self.emitIndexChanged(index1, index2)

    def emitIndexChanged(self, index1, index2=None):
        index2 = index1 if index2 is None else index2
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


# ######################################################################################

class CEventJobTicketsDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def commit(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)


    def createEditor(self, parent, option, index):
        model = index.model()
        action, domain, clientId = model.getEditorInitValues(index)
        domain = CJobTicketActionPropertyValueType.parseDomain(domain)
        editor = CJobTicketActionPropertyValueType.CPropEditor(action, domain,
                                                               parent, clientId, model.getEventTypeId())
        self.connect(editor, SIGNAL('commit()'), self.commit)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        return editor


    def setEditorData(self, editor, index):
        model = index.model()
        value = model.data(index, Qt.EditRole)
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        model = index.model()
        value = editor.value()
        model.setData(index, toVariant(value))


class CEventJobTicketsView(CTreeView, CPreferencesMixin):
    jobTicketColumn = 1
    def __init__(self, parent):
        CTreeView.__init__(self, parent)
        self.actEditMultiTickets = None
        self.setItemDelegateForColumn(CEventJobTicketsView.jobTicketColumn, CEventJobTicketsDelegate(self))
        self.actForceSetJobTicketOnCurrentDay = QtGui.QAction(u'Назначить сегодня', self)
        self.connect(self.actForceSetJobTicketOnCurrentDay, SIGNAL('triggered()'),
                     self.on_actForceSetJobTicketOnCurrentDay)
        self.createPopupMenu([self.actForceSetJobTicketOnCurrentDay])
        self.connect(self.popupMenu(), SIGNAL('aboutToShow()'), self._popupMenuAboutToShow)


    def addActEditMultiTickets(self):
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.ExtendedSelection)
        self.actEditMultiTickets = QtGui.QAction(u'Редактировать выделенные записи', self)
        self.connect(
            self.actEditMultiTickets, SIGNAL('triggered()'), self.on_actEditMultiTickets
        )
        self.popupMenu().addAction(self.actEditMultiTickets)

    def selectedItems(self):
        items = []
        for index in self.selectedIndexes():
            item = index.internalPointer()
            if item not in items:
                items.append(item)
        return items

    def on_actEditMultiTickets(self):
        model = self.model()

        items = self.selectedItems()
        item = items[0]
        action, domain, clientId = model.getEditorInitValuesByItem(item)
        domain = CJobTicketActionPropertyValueType.parseDomain(domain)

        jobTypeCode = domain['jobTypeCode']
        date = forceDate(action._record.value('begDate')) if action else None
        actionTypeId = forceRef(action._record.value('actionType_id')) if action else None
        dlg = CJobTicketChooserDialog(self, model.getEventTypeId(), clientId, actionTypeId)
        if item.jobTicketId():
            dlg.setTicketId(jobTypeCode, item.jobTicketId())
        else:
            dlg.setDefaults(jobTypeCode, date)

        if dlg.exec_():
            jobTicketId = dlg.getTicketId()
            for item in items:
                item.setJobTicketId(jobTicketId)

            model.emitRowsChanged(0, model.rowCount(None))


    def _popupMenuAboutToShow(self):
        index = self.currentIndex()
#        self.actForceSetJobTicketOnCurrentDay.setEnabled(self.model().isIndexItemHasJobTicket(index))
        self.actForceSetJobTicketOnCurrentDay.setEnabled(index.isValid())
        if self.actEditMultiTickets is not None:
            self.actEditMultiTickets.setEnabled(self._selectedHasSameJobType())

    def _selectedHasSameJobType(self):
        return len(set(item.jobTypeId() for item in self.selectedItems() if item)) == 1


    def on_actForceSetJobTicketOnCurrentDay(self):
        index = self.currentIndex()
        self.model().forceSetJobTicketOnCurrentDay(self, index)


    def loadPreferences(self, preferences):
        model = self.model()
        for i in xrange(model.columnCount()):
            width = forceInt(getPref(preferences, 'col_'+str(i), None))
            if width:
                self.setColumnWidth(i, width)


    def savePreferences(self):
        preferences = {}
        model = self.model()
        if model:
            for i in xrange(model.columnCount()):
                width = self.columnWidth(i)
                setPref(preferences, 'col_%d'%i, QVariant(width))
        return preferences


# ######################################

