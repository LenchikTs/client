# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, SIGNAL
from Events.ActionRelations.Groups import CRelationsProxyModelGroup

from library.InDocTable import CRBInDocTableCol
from library.Utils import (
    forceDate, forceDouble, forceInt, forceRef, forceString, toVariant, getDentitionActionTypeId,
    forceDateTime)

from Events.Action import CAction, CActionType, CActionTypeCache, getActionDefaultAmountEx, getActionDuration
from Events.ActionStatus                import CActionStatus
from Events.ExecutionPlan.Groups        import CActionExecutionPlanGroup, CExecutionPlanProxyModelGroup
from Events.ExecutionPlan.ExecutionPlan import CActionExecutionPlan, CActionExecutionPlanItem
from Events.Utils import getActionTypeIdListByClass
from Resources.JobTicketStatus          import CJobTicketStatus
from library.blmodel.Query              import CQuery


__all__ = [
            'CActionsModel',
            'getActionDefaultAmountEx',
            'CGroupActionsProxyModel'
          ]


class CActionRecordItem(object):
    def __init__(self, record, action):
        self._data = (record, action)

    @property
    def id(self):
        return self.action.getId()

    @property
    def record(self):
        return self._data[0]

    @property
    def action(self):
        return self._data[1]

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, index):
        return self._data[index]


class CActionsModel(QAbstractTableModel):

    __pyqtSignals__ = ('amountChanged(int)',
                      )

    def __init__(self, parent, actionTypeClass=None):
        QAbstractTableModel.__init__(self, parent)
        self.actionTypeClass = None
        self.actionTypeIdList = []
        self.disabledActionTypeIdList = []
        self.col = CRBInDocTableCol(u'',  'actionType_id', 10, 'ActionType', addNone=True, preferredWidth=300)
        self._items = []   # each item is pair (record, action)
        self._loadedActionIdListWithEndDate = []
        self.eventEditor = None
        if actionTypeClass is not None:
            self.setActionTypeClass(actionTypeClass)
        self.idxFieldName = 'idx'  # :( для обеспечения возможности перемещения строк.
        self.table = QtGui.qApp.db.table('Action')
        self.readOnly = False
        self.ttjForDeleteIdList = []
        self.cachedFreeJobTicket = []
        self.cachedFreeJobTicketActionProperty = []
        self.actionIdForMarkDeleted = []


    def setReadOnly(self, value):
        self.readOnly = value


    def getReadOnly(self):
        return self.readOnly


    def setActionTypeClass(self, actionTypeClass):
        self.actionTypeClass = actionTypeClass
        self.actionTypeIdList = getActionTypeIdListByClass(actionTypeClass)
        self.col.filter = 'class=%d' % actionTypeClass

    def items(self):
        return self._items


    def updatePersonId(self, oldPersonId, newPersonId):
        pass
#        def replacePerson(record, field):
#            if forceRef(record.value(field)) == oldPersonId:
#                record.setValue(field, toVariant(newPersonId))
#
#        if oldPersonId and newPersonId and oldPersonId != newPersonId:
#            for item in self._items:
#                record = item[0]
##                replacePerson(record, 'setPerson_id')
#                replacePerson(record, 'person_id')


    def emitAmountChanged(self, row):
        self.emit(SIGNAL('amountChanged(int)'), row)


    def updateActionsAmount(self):  # по изменению в событии
        for row, item in enumerate(self._items):
            record, action = item
            actionTypeId = forceRef(record.value('actionType_id'))
            if actionTypeId:
                actionType = CActionTypeCache.getById(actionTypeId)
                if actionType.amountEvaluation in (CActionType.eventVisitCount,
                                                   CActionType.eventDurationWithFiveDayWorking,
                                                   CActionType.eventDurationWithSixDayWorking,
                                                   CActionType.eventDurationWithSevenDayWorking):
                    prevValue = forceDouble(record.value('amount'))
                    value = float(self.getDefaultAmountEx(actionType, record, action))
                    if prevValue != value:
                        record.setValue('amount', toVariant(value))
                        self.emitRowsChanged(row, row)
                        self.emitAmountChanged(row)

                # TT 1012 "Синхронизировать даты действия с датами события"
                if actionType.defaultDirectionDate == CActionType.dddSyncEventBegDate:
                    prevDirectionDate = forceDateTime(record.value('directionDate'))
                    directionDate = forceDateTime(self.eventEditor.eventSetDateTime)
                    if prevDirectionDate != directionDate:
                        record.setValue('directionDate', toVariant(directionDate))
                        self.emitRowsChanged(row, row)
                elif actionType.defaultDirectionDate == CActionType.dddSyncEventEndDate:
                    prevDirectionDate = forceDateTime(record.value('directionDate'))
                    directionDate = forceDateTime(self.eventEditor.getExecDateTime())
                    if prevDirectionDate != directionDate:
                        record.setValue('directionDate', toVariant(directionDate))
                        self.emitRowsChanged(row, row)

                if actionType.defaultBegDate == CActionType.dbdSyncEventBegDate:
                    prevBegDate = forceDateTime(record.value('begDate'))
                    begDate = forceDateTime(self.eventEditor.eventSetDateTime)
                    if prevBegDate != begDate:
                        record.setValue('begDate', toVariant(begDate))
                        self.emitRowsChanged(row, row)
                elif actionType.defaultBegDate == CActionType.dbdSyncEventEndDate:
                    prevBegDate = forceDateTime(record.value('begDate'))
                    begDate = forceDateTime(self.eventEditor.getExecDateTime())
                    if prevBegDate != begDate:
                        record.setValue('begDate', toVariant(begDate))
                        self.emitRowsChanged(row, row)

                if actionType.defaultEndDate == CActionType.dedSyncEventBegDate:
                    prevEndDate = forceDateTime(record.value('endDate'))
                    endDate = forceDateTime(self.eventEditor.eventSetDateTime)
                    if prevEndDate != endDate:
                        record.setValue('endDate', toVariant(endDate))
                        record.setValue('status', toVariant(CActionStatus.finished if not endDate.isNull() else CActionStatus.started))
                        self.emitRowsChanged(row, row)
                elif actionType.defaultEndDate == CActionType.dedSyncEventEndDate:
                    prevEndDate = forceDateTime(record.value('endDate'))
                    endDate = forceDateTime(self.eventEditor.getExecDateTime())
                    if prevEndDate != endDate:
                        record.setValue('endDate', toVariant(endDate))
                        record.setValue('status', toVariant(CActionStatus.finished if not endDate.isNull() else CActionStatus.started))
                        self.emitRowsChanged(row, row)


    def updateActionAmount(self, row):  # по изменению в самом действии
        record, action = self._items[row]
        actionTypeId = forceRef(record.value('actionType_id'))
        if actionTypeId:
            actionType = CActionTypeCache.getById(actionTypeId)
            if actionType.amountEvaluation in (CActionType.eventVisitCount,
                                               CActionType.eventDurationWithFiveDayWorking,
                                               CActionType.eventDurationWithSixDayWorking,
                                               CActionType.eventDurationWithSevenDayWorking,
                                               CActionType.actionDurationWithFiveDayWorking,
                                               CActionType.actionDurationWithSixDayWorking,
                                               CActionType.actionDurationWithSevenDayWorking,
                                               CActionType.actionFilledPropsCount,
                                               CActionType.actionAssignedPropsCount,
                                               CActionType.actionDurationFact):
                prevValue = forceDouble(record.value('amount'))
                value = float(self.getDefaultAmountEx(actionType, record, action))
                if prevValue != value:
                    record.setValue('amount', toVariant(value))
                    self.emitRowsChanged(row, row)
                    self.emitAmountChanged(row)


    def disableActionType(self, actionTypeId):
        self.disabledActionTypeIdList.append(actionTypeId)


    def getActionDuration(self, record, weekProfile):
        return getActionDuration(self.eventEditor.eventTypeId, record, weekProfile)


    def getDefaultAmountEx(self, actionType, record, action):
        return getActionDefaultAmountEx(self.eventEditor, actionType, record, action)


    def getDefaultAmount(self, actionTypeId, record, action):
        if actionTypeId:
            actionType = CActionTypeCache.getById(actionTypeId)
            result = self.getDefaultAmountEx(actionType, record, action)
        else:
            result = 0
        return result


    def columnCount(self, index=None, *args, **kwargs):
        return 1


    def rowCount(self, index=None, *args, **kwargs):
        return len(self._items)+1


    def flags(self, index):
        if self.readOnly:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        row = index.row()
#        if self.isLocked(row):
#            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if row < len(self._items):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self.isExposed(row):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(u'Наименование')
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if row < len(self._items):
            if role == Qt.EditRole:
                record = self._items[row][0]
                return record.value('actionType_id')
            if role == Qt.DisplayRole:
                record = self._items[row][0]
                outName = forceString(record.value('specifiedName'))
                actionTypeId = forceRef(record.value('actionType_id'))
                actionBegDate = forceString(forceDate(record.value('begDate')))
                if actionTypeId:
                    actionType = CActionTypeCache.getById(actionTypeId)
                    if actionType:
                        outName = actionType.name + ' '+outName if outName else actionType.name
                        # showBegDate = self.showBegDate(actionTypeId)
                        if actionType.showBegDate:
                            outName = outName + ', ' + actionBegDate
                return QVariant(outName)
            if role == Qt.StatusTipRole or role == Qt.ToolTipRole:
                record, action = self._items[row]
                specifiedName = forceString(record.value('specifiedName'))
                actionTypeId = forceRef(record.value('actionType_id'))
                actionType = CActionTypeCache.getById(actionTypeId) if actionTypeId else None
                actionName = (actionType.code + ': ' + actionType.name) if actionType else ''
                actionBegDate = forceString(forceDate(record.value('begDate')))
                if actionTypeId and actionType:
                    showBegDate = actionType.showBegDate  # self.showBegDate(actionTypeId)
                    if role == Qt.StatusTipRole:
                        actionName = actionName + u' ' + specifiedName
                    if showBegDate:
                        actionName = actionName + u', ' + actionBegDate

                prevActionId = forceRef(record.value('prevAction_id'))
                if action and ((action.trailerIdx > 0 and not bool(action.trailerIdx & 1)) or prevActionId):
                    if not prevActionId:
                        actionName += u' связано с действием ...'
                    else:
                        prevAction = CAction.getActionById(prevActionId)
                        if prevAction:
                            prevActionType = prevAction.getType()
                            actionName += u' связано с действием ' + (prevActionType.code + ': ' + prevActionType.name) if prevActionType else ''
                return QVariant(actionName)
            if role == Qt.ForegroundRole:
                record, action = self._items[row]
                if action and action.getType().isRequiredCoordination and record.isNull('coordDate'):
                    return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole, presetAction=None):  # presetAction - это ошибка!
        if role == Qt.EditRole:
            row = index.row()
            actionTypeId = forceRef(value)
            if actionTypeId and not (self.checkMaxOccursLimit(actionTypeId) and
                                     self.checkMovingNoLeaved(actionTypeId) and
                                     self.checkMovingAfterReceived(actionTypeId) and
                                     self.checkLeavedAfterMoving(actionTypeId) and
                                     self.checkLeavedAfterMovingDate(actionTypeId)):
                return False
            if row == len(self._items):  # Это ошибка!
                if actionTypeId is None:
                    return False

                self.addRow(presetAction=presetAction)
            if not presetAction:
                record = self._items[row][0]
                action = self.getFilledAction(record, actionTypeId)
            else:
                record = presetAction.getRecord()
                action = presetAction
            self._items[row] = CActionRecordItem(record, action)
            if not presetAction:
                record.setValue('amount', toVariant(self.getDefaultAmount(actionTypeId, record, action)))
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            self.emitItemsCountChanged()
            actionsSummaryRowRow = self.eventEditor.translate2ActionsSummaryRow(self, row)
            if actionsSummaryRowRow is not None:
                self.eventEditor.onActionChanged(actionsSummaryRowRow)
            return True


    def appendOuterAction(self, action):
        item = (action.getRecord(), action)
        self._items.append(item)
        index = QModelIndex()
        cnt = len(self._items)
        self.beginInsertRows(index, cnt, cnt)
        self.insertRows(cnt, 1, index)
        self.endInsertRows()
        self.emitItemsCountChanged()



    def emitItemsCountChanged(self):
        self.emit(SIGNAL('itemsCountChanged()'))


    def addRow(self, actionTypeId=None, amount=None, financeId=None, contractId=None, presetAction=None):
        if not presetAction:
            record = QtGui.qApp.db.table('Action').newRecord()
            action = self.getFilledAction(record, actionTypeId, amount, financeId, contractId)
            item = CActionRecordItem(record, action)
        else:
            item = CActionRecordItem(presetAction.getRecord(), presetAction)
        self._items.append(item)
        index = QModelIndex()
        cnt = len(self._items)
        self.beginInsertRows(index, cnt, cnt)
        self.insertRows(cnt, 1, index)
        self.endInsertRows()
        self.emitItemsCountChanged()
        return cnt-1


    def getFilledAction(self, record, actionTypeId, amount=None, financeId=None, contractId=None, **kwargs):
        return CAction.getFilledAction(self.eventEditor, record, actionTypeId, amount, financeId, contractId)


    def delVisit(self, record):
        eventEditor = self.eventEditor
        if not hasattr(eventEditor, 'tblVisits'):
            return
        visitId = forceRef(record.value('visit_id'))
        visitList = eventEditor.modelActionsSummary.visitList
        visitRecord = visitList.get(record)
        visitsModel = eventEditor.modelVisits
        visitList   = visitsModel.items()
        visitRow = None

        if visitRecord:
            visitRow = visitList.index(visitRecord)

        if visitId and not visitRow:
            for i, record in enumerate(visitList):
                id = forceInt(record.value('id'))
                if id == visitId:
                    visitRow = i
        if visitRow is not None:
            visitsModel.removeRows(visitRow, 1)


    def removeRows(self, row, count, parentIndex=QModelIndex(), *args, **kwargs):
        if 0 <= row and row + count <= len(self._items):
            if not self.checkDirectionDeleted(row, count):
                return False
            for i in xrange(count):
                if self.isLocked(row+i):
                    return False
                record, action = self._items[row]
                actionTypeId = forceRef(record.value('actionType_id'))
                if actionTypeId and not (self.checkReceivedDeleted(actionTypeId) and
                                         self.checkMovingDeleted(actionTypeId, row)):
                    return False
                self.delVisit(record)
                ttjId = forceRef(record.value('takenTissueJournal_id'))
                if ttjId:
                    self.ttjForDeleteIdList.append(ttjId)
                if action:
                    for property in action._propertiesById.itervalues():
                        propertyType = property.type()
                        if propertyType.isJobTicketValueType():
                            jobTicketId = action[propertyType.name]
                            if jobTicketId:
                                if jobTicketId not in self.cachedFreeJobTicket:
                                    self.cachedFreeJobTicket.append(jobTicketId)
                                propertyRecord = property.getRecord()
                                propertyId = forceRef(propertyRecord.value('id')) if propertyRecord else None
                                if propertyId and propertyId not in self.cachedFreeJobTicketActionProperty:
                                    self.cachedFreeJobTicketActionProperty.append(propertyId)
                    actionId = forceRef(record.value('id'))
                    if action.nomenclatureClientReservation is not None and not actionId:
                        action.cancel()
                if action.getId():
                    self.actionIdForMarkDeleted.append(action.getId())
            self.beginRemoveRows(parentIndex, row, row+count-1)
            del self._items[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def loadItems(self, items):
        items.sort(key=lambda x: forceInt(x.record.value('idx')))
        self._items = items

        for item in self._items:
            record = item.record
            if forceDate(record.value('endDate')):
                self._loadedActionIdListWithEndDate.append(forceRef(record.value('id')))
        self.reset()

    def loadedActionIdListWithEndDate(self):
        return self._loadedActionIdListWithEndDate


    def saveItems(self, eventId):
        db = QtGui.qApp.db
        table = db.table('Action')
        idList = []
        dentActionTypeId, parodentActionTypeId = getDentitionActionTypeId()
        actionTypeDentIdList = []
        if dentActionTypeId:
            actionTypeDentIdList.append(dentActionTypeId)
        if parodentActionTypeId:
            actionTypeDentIdList.append(parodentActionTypeId)
        for row, item in enumerate(self._items):
            record, action = item
            if action:
                if self.table.newRecord().count() != record.count():
                    action._record = self.removeExtCols(record)
                self.eventEditor.getMKBValueForActionDuringSaving(record, action)
                if hasattr(self.eventEditor, 'modelActionsSummary'):
                    visitList = self.eventEditor.modelActionsSummary.visitList
                    visitRecord = visitList.get(record)
                    if visitRecord:
                        visitId = forceRef(visitRecord.value('id'))
                        if visitId:
                            action._record.setValue('visit_id', visitId)
                            record.setValue('visit_id', toVariant(visitId))
                if not actionTypeDentIdList or forceRef(record.value('actionType_id')) not in actionTypeDentIdList:
                    if action.trailerIdx > 0:
                        if bool(action.trailerIdx & 1):  # нечет
                            _id = action.save(eventId, len(idList))
                            # для обновления данных в модели при нажатии кнопки "применить"
                            for fieldName in ['id', 'createDatetime', 'createPerson_id', 'modifyDatetime',
                                              'modifyPerson_id', 'expose']:
                                record.setValue(fieldName, toVariant(action._record.value(fieldName)))
                            idList.append(_id)
                        else:  # чет
                            prevActionId = self.eventEditor.trailerIdList.get(action.trailerIdx-1, None)
                            if prevActionId:
                                action._record.setValue('prevAction_id', toVariant(prevActionId))
                                _id = action.save(eventId, len(idList))
                                # для обновления данных в модели при нажатии кнопки "применить"
                                for fieldName in ['id', 'createDatetime', 'createPerson_id', 'modifyDatetime',
                                                  'modifyPerson_id', 'expose']:
                                    record.setValue(fieldName, toVariant(action._record.value(fieldName)))
                                idList.append(_id)
                            else:
                                self.eventEditor.trailerActions.append(action)
                    else:
                        _id = action.save(eventId, len(idList))
                        # для обновления данных в модели при нажатии кнопки "применить"
                        for fieldName in ['id', 'createDatetime', 'createPerson_id', 'modifyDatetime', 'modifyPerson_id', 'expose']:
                            record.setValue(fieldName, toVariant(action._record.value(fieldName)))
                        idList.append(_id)
        if QtGui.qApp.controlNomenclatureExpense():
            message = u''
            tableNomenclature = db.table('rbNomenclature')
            actionTypeIdExpense = []
            for recordExpense, actionExpense in self._items:
                status = forceInt(actionExpense.getRecord().value('status'))
                if actionExpense.nomenclatureExpense:
                    if not actionExpense._actionType.generateAfterEventExecDate or bool(actionExpense._actionType.generateAfterEventExecDate and actionExpense.event.execDate):
                        if actionExpense.nomenclatureExpense and status == CActionStatus.finished and (
                                actionExpense.nomenclatureExpense.getStockMotionId() or actionExpense.nomenclatureExpense.stockMotionItems()):
                            if actionExpense.nomenclatureExpense._noAvialableQnt and actionExpense._actionType.getNomenclatureRecordList():
                                actionTypeId = actionExpense._actionType.id
                                if actionTypeId and actionTypeId not in actionTypeIdExpense:
                                    actionTypeIdExpense.append(actionTypeId)
                                    nomenclatureLine = actionExpense.nomenclatureExpense._noAvialableQnt.get(actionTypeId, [])
                                    if nomenclatureLine:
                                        if actionExpense.nomenclatureExpense.selectNomenclatureIdList:
                                            nomenclatureLine = list(set(nomenclatureLine) & set(actionExpense.nomenclatureExpense.selectNomenclatureIdList))
                                        nomenclatureName = u''
                                        records = db.getRecordList(tableNomenclature, [tableNomenclature['name']], [tableNomenclature['id'].inlist(nomenclatureLine)], order = tableNomenclature['name'].name())
                                        for recordNomenclature in records:
                                            nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                                        message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n''' % (actionExpense._actionType.name, nomenclatureName)
            if message:
                QtGui.QMessageBox().warning(None,
                                            u'Внимание!',
                                            message,
                                            QtGui.QMessageBox.Ok,
                                            QtGui.QMessageBox.Ok)
        cond = [table['event_id'].eq(eventId), table['deleted'].eq(0), 'NOT ('+table['id'].inlist(idList)+')']
        if self.actionTypeClass is not None:
            cond.append('EXISTS(SELECT NULL FROM ActionType WHERE ActionType.id = Action.actionType_id AND ActionType.`class` = {0})'.format(self.actionTypeClass))

        if self.actionIdForMarkDeleted:
            tableActionProperty = db.table('ActionProperty')
            filter = [tableActionProperty['action_id'].inlist(self.actionIdForMarkDeleted), tableActionProperty['deleted'].eq(0)]
            db.markRecordsDeleted(tableActionProperty, filter)

            tableActionExecutionPlan = db.table('Action_ExecutionPlan')
            filter = [tableActionExecutionPlan['master_id'].inlist(self.actionIdForMarkDeleted), tableActionExecutionPlan['deleted'].eq(0)]
            db.markRecordsDeleted(tableActionExecutionPlan, filter)

            tableStockMotion = db.table('StockMotion')
            tableStockMotionItem = db.table('StockMotion_Item')
            tableActionNR = db.table('Action_NomenclatureReservation')
            filterActionNR = [tableActionNR['action_id'].inlist(self.actionIdForMarkDeleted)]
            if idList:
                filterActionNR.append(tableActionNR['action_id'].notInlist(idList))
            reservationIdList = db.getDistinctIdList(tableActionNR, [tableActionNR['reservation_id']], filterActionNR)
            if reservationIdList:
                filterSINR = [tableStockMotionItem['master_id'].inlist(reservationIdList),
                              tableStockMotionItem['deleted'].eq(0)]
                db.deleteRecord(tableStockMotionItem, filterSINR)
                filterSNR = [tableStockMotion['id'].inlist(reservationIdList), tableStockMotion['deleted'].eq(0)]
                db.deleteRecord(tableStockMotion, filterSNR)
                db.deleteRecord(tableActionNR, filterActionNR)

            filter = [table['id'].inlist(self.actionIdForMarkDeleted), table['deleted'].eq(0)]
            stockMotionIdList = db.getDistinctIdList(table, [table['stockMotion_id']], filter)
            if stockMotionIdList:
                filter = [tableStockMotionItem['master_id'].inlist(stockMotionIdList), tableStockMotionItem['deleted'].eq(0)]
                db.deleteRecord(tableStockMotionItem, filter)
                filter = [tableStockMotion['id'].inlist(stockMotionIdList), tableStockMotion['deleted'].eq(0)]
                db.deleteRecord(tableStockMotion, filter)

            filter = [table['id'].inlist(self.actionIdForMarkDeleted), table['deleted'].eq(0)]
            db.markRecordsDeleted(table, filter)
        if self.ttjForDeleteIdList:
            tableTTJ = db.table('TakenTissueJournal')
            filter = [tableTTJ['id'].inlist(self.ttjForDeleteIdList), tableTTJ['deleted'].eq(0)]
            db.deleteRecord(tableTTJ, filter)
        if self.cachedFreeJobTicketActionProperty:
            tableAPJT = db.table('ActionProperty_Job_Ticket')
            filter = [tableAPJT['id'].inlist(self.cachedFreeJobTicketActionProperty)]
            db.deleteRecord(tableAPJT, filter)
        if self.cachedFreeJobTicket:
            tableJobTicket = db.table('Job_Ticket')
            records = db.getRecordList(tableJobTicket, '*', [tableJobTicket['id'].inlist(self.cachedFreeJobTicket), tableJobTicket['deleted'].eq(0)])
            for recordJobTicket in records:
                recordJobTicket.setValue('status', toVariant(CJobTicketStatus.wait))
                recordJobTicket.setValue('begDateTime', toVariant(None))
                recordJobTicket.setValue('endDateTime', toVariant(None))
                recordJobTicket.setValue('orgStructure_id', toVariant(None))
                db.updateRecord(tableJobTicket, recordJobTicket)


    def removeExtCols(self, srcRecord):
        record = self.table.newRecord()
        for i in xrange(record.count()):
            record.setValue(i, srcRecord.value(record.fieldName(i)))
        return record


    def isLocked(self, row):
        if 0 <= row < len(self._items):
            action = self._items[row][1]
            if action:
                return action.isLocked()
        return False


    def isCanDeletedByUser(self, row):
        if 0 <= row < len(self._items):
            action = self._items[row][1]
            if action:
                return action.isCanDeletedByUser()
        return True


    def isLockedOrExposed(self, row):
        db = QtGui.qApp.db
        if 0 <= row < len(self._items):
            recod, action = self._items[row]
            if action.getId():
                table = db.table('Account_Item')
                cond  = [table['deleted'].eq(0)]
                cond.append(table['action_id'].eq(action.getId()))
                cond.append(table['refuseType_id'].isNotNull())
                cond.append(table['reexposeItem_id'].isNull())
                if db.getRecordList(table, 'id', cond):
                    return action and action.isLocked()
            return forceInt(recod.value('payStatus')) != 0 or (action and action.isLocked())
        return False


    def isExposed(self, row):
        if 0 <= row < len(self._items):
            record, action = self._items[row]
            if action:
                return action.isExposed()
        return False


    def actionTypeId(self, row):
        if 0 <= row < len(self._items):
            return forceInt(self._items[row][0].value('actionType_id'))
        else:
            return None


    def payStatus(self, row):
        if 0 <= row < len(self._items):
            return forceInt(self._items[row][0].value('payStatus'))
        else:
            return 0


#    def changeActionType(self, row, newActionTypeId):
#        self._items[row].setValue('actionType_id', QVariant(newActionTypeId))
#        self.emitCellChanged(row, 0)


    def removeRowEx(self, row):
        self.removeRows(row, 1)


    def upRow(self, row):
        if 0 < row < len(self._items):
            self._items[row-1], self._items[row] = self._items[row], self._items[row-1]
            self.emitRowsChanged(row-1, row)
            return True
        else:
            return False


    def downRow(self, row):
        if 0 <= row < len(self._items)-1:
            self._items[row+1], self._items[row] = self._items[row], self._items[row+1]
            self.emitRowsChanged(row, row+1)
            return True
        else:
            return False


    def checkMaxOccursLimit(self, actionTypeId):
        actionType = CActionTypeCache.getById(actionTypeId)
        count = 0
        for record, action in self._items:
            if action and action.getType() == actionType:
                count += 1
        result = actionType.checkMaxOccursLimit(count, True)
        return result


    def checkReceivedDeleted(self, actionTypeId):
        result = True
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'received' in actionType.flatCode.lower():
            for record, action in self._items:
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'moving' in actionTypeItem.flatCode.lower()):
                        return actionType.checkReceivedMovingLeaved(u'Нельзя удалить действие "Поступление" если есть "Движение"')
                    if actionTypeItem and (u'leaved' in actionTypeItem.flatCode.lower()):
                        return actionType.checkReceivedMovingLeaved(u'Нельзя удалить действие "Поступление" если есть "Выписка"')
        return result


    def checkMovingDeleted(self, actionTypeId, rowCurrent):
        result = True
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'moving' in actionType.flatCode.lower():
            for row, item in enumerate(self.items()):
                record, action = item
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'leaved' in actionTypeItem.flatCode.lower()):
                        return actionType.checkReceivedMovingLeaved(u'Нельзя удалить действие "Движение" если есть "Выписка"')
                    elif row > rowCurrent and actionTypeItem and (u'moving' in actionTypeItem.flatCode.lower()):
                       return actionType.checkReceivedMovingLeaved(u'Нельзя удалить действие "Движение" если после него есть "Движение"')
        return result


    def checkMovingNoLeaved(self, actionTypeId):
        result = True
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'moving' in actionType.flatCode.lower():
            for record, action in self._items:
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'leaved' in actionTypeItem.flatCode.lower()):
                        return actionType.checkReceivedMovingLeaved(u'Действие "Движение" не должно применяться после действия "Выписка"')
                    elif actionTypeItem and (u'moving' in actionTypeItem.flatCode.lower()):
                        if not forceDate(record.value('endDate')):
                            return actionType.checkReceivedMovingLeaved(u'Действие "Движение" не может появится при наличии не законченного "Движение"')
        return result


    def checkMovingAfterReceived(self, actionTypeId):
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'moving' in actionType.flatCode.lower():
            for record, action in self._items:
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'received' in actionTypeItem.flatCode.lower()):
                        if not forceDate(record.value('endDate')):
                            return actionType.checkReceivedMovingLeaved(u'Действие "Движение" не может появится при наличии не законченного действия "Поступление"')
                        return True
            return actionType.checkReceivedMovingLeaved(u'Действие "Движение" не должно применяться пока нет действия действия "Поступление"')
        return True


    def checkLeavedAfterMoving(self, actionTypeId):
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'leaved' in actionType.flatCode.lower():
            for record, action in self._items:
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'moving' in actionTypeItem.flatCode.lower()):
                        return True
            return actionType.checkReceivedMovingLeaved(u'Действие "Выписка" не должно применяться пока нет действия "Движение"')
        return True


    def checkLeavedAfterMovingDate(self, actionTypeId):
        actionType = CActionTypeCache.getById(actionTypeId)
        if u'leaved' in actionType.flatCode.lower():
            for record, action in self._items:
                if action:
                    actionTypeItem = action.getType()
                    if actionTypeItem and (u'moving' in actionTypeItem.flatCode.lower()):
                        if not forceDate(record.value('endDate')):
                            return actionType.checkReceivedMovingLeaved(u'Действие "Выписка" не может появится при наличии не законченного действия "Движение"')
        return True


    def emitRowsChanged(self, row1, row2):
        index1 = self.index(row1, 0)
        index2 = self.index(row2, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def reloadItem(self, row):
        db = QtGui.qApp.db
        table = db.table('Action')
        if 0 <= row < len(self._items):
            item = self._items[row]
            action = item.action
            actionId = action.getId()
            newRecord = db.getRecord(table, '*', actionId)
            action.setRecord(newRecord)
            item._data = (newRecord, action)
            self.emitRowsChanged(row, row)
    

    def checkDirectionDeleted(self, row, count):
        for record, action in self._items[row:row+count]:
            actionTypeId = forceRef(record.value('actionType_id'))
            actionType = CActionTypeCache.getById(actionTypeId)
            if (actionType.flatCode.lower() == u'consultationDirection'.lower()
                and u'Идентификатор направления' in actionType._propertiesByName
                and u'Причина аннулирования' in actionType._propertiesByName
                and action[u'Идентификатор направления'] is not None
                and action[u'Причина аннулирования'] is None
            ):
                QtGui.QMessageBox.critical(
                    self.eventEditor,
                    u'Произошла ошибка',
                    u'Перед удалением направления необходимо его аннулировать!',
                    QtGui.QMessageBox.Close
                )
                return False
        return True


_emptyValue = object()
_nomenclatureIndex = 1


class CGroups(object):
    def __init__(self, model):
        self._mapProxyRow2Group = {}
        self._groups = []
        self.idx = None
        self._model = model
        self.proxyRow = 0

    def upGroup(self, proxyRow, group):
        if group not in self._groups:
            return False

        index = self._groups.index(group)
        if index == 0:
            return False

        upperGroup = self._groups[index-1]
        upperGroup.proxyRow = proxyRow
        upperGroup.increaseItemsIdx(group.itemsCount(), upperGroup)
        group.idx = upperGroup.idx
        group.decreaseItemsIdx(upperGroup.itemsCount(), upperGroup)

        self._groups[index], self._groups[index - 1] = upperGroup, group

        self._resetModelNewItemsOrder()

        return True

    def getGroupProxyRow(self, group):
        result = 0
        for targetGroup in self._groups:
            if group is targetGroup:
                return result
            result += len(group)
        return -1

    def downGroup(self, proxyRow, group):
        if group not in self._groups:
            return False

        index = self._groups.index(group)
        if index == len(self._groups) - 1:
            return False

        downerGroup = self._groups[index + 1]
        downerGroup.proxyRow = proxyRow
        downerGroup.decreaseItemsIdx(group.itemsCount(), downerGroup)
        group.idx = downerGroup.idx

        group.increaseItemsIdx(downerGroup.itemsCount(), downerGroup)

        self._groups[index], self._groups[index + 1] = downerGroup, group

        self._resetModelNewItemsOrder()

        return True


    def _setNewOrder(self, sortKey):
        self._groups.sort(key=lambda x: x.getSortValue(sortKey))
        for idx, group in enumerate(self._groups):
            group.idx = idx
            for item in group.items:
                record = item.record
                record.setValue('idx', toVariant(idx))


    def _resetModelNewItemsOrder(self):
        model = self._model.model()

        items = {}
        for group in self._groups:
            for item in group:
                record = item[0]
                items.setdefault(forceInt(record.value('idx')), []).append(item)

        newItemsList = []
        for idx in sorted(items.keys()):
            newItemsList.extend(items[idx])

        model.items()[:] = newItemsList

    def clear(self):
        self._mapProxyRow2Group.clear()
        self._groups = []

    @property
    def groupsIterator(self):
        return iter(self._groups)

    def __iter__(self):
        return iter(self._model.model().items())

    def __len__(self):
        return self.rowsCount()

    def __getitem__(self, proxyRow):
        if proxyRow < 0:
            modelRowsCount = self._model.rowCount() - 1
            proxyRow += modelRowsCount
        return self.getItem(proxyRow)

    def delete(self, group):
        for proxyRow in group.proxyRows:
            group.deleteProxyRow(proxyRow, self._model.model())
            del self._mapProxyRow2Group[proxyRow]
        self._groups.remove(group)

    def newGroup(self, actionTypeId = None):
        group = CRelationsProxyModelGroup(self._model) if bool(CActionTypeCache.getById(actionTypeId).getRelatedActionTypes()) else CExecutionPlanProxyModelGroup(self._model)
        self._groups.append(group)
        return group

    def addGroup(self, group):
        self._groups.append(group)

    def mapGroup(self, proxyRow, group):
        self._mapProxyRow2Group[proxyRow] = group

    def getItem(self, proxyRow):
        return self._mapProxyRow2Group[proxyRow].getItem(proxyRow)

    @property
    def groupsCount(self):
        return len(self._groups)

    def rowsCount(self):
        return sum([len(g) for g in self._groups])


class CGroupActionsProxyModel(QtGui.QProxyModel):
    __groupingAllowed__ = True

    __pyqtSignals__ = (
        'amountChanged(int)',
        'itemsCountChanged()'
    )

    def __init__(self, parent):
        actionModel = CActionsModel(parent)

        QtGui.QProxyModel.__init__(self, parent)
        QtGui.QProxyModel.setModel(self, actionModel)

        self._parent = parent
        self._actionModel = actionModel

        self._groups = CGroups(self)
        self._mapProxyRow2Group = {}
        self._mapModelRow2ProxyRow = {}

        boldFont = QtGui.QFont()
        boldFont.setWeight(QtGui.QFont.Bold)

        self._qBoldFont = QVariant(boldFont)

        boldFont.setItalic(QtGui.QFont.StyleItalic)
        self._qBoldItalicFont = QVariant(boldFont)

        italicFont = QtGui.QFont()
        italicFont.setItalic(QtGui.QFont.StyleItalic)
        self._qItalicFont = QVariant(italicFont)

        self._groupItemsShift = u' ' * 3

        self.connect(self._actionModel, SIGNAL('dataChanged(QModelIndex, QModelIndex)'), self._emitDataChanged)
        self.connect(self._actionModel, SIGNAL('amountChanged(int)'), self._emitAmountChanged)
        self.connect(self._actionModel, SIGNAL('itemsCountChanged()'), self._emitItemsCountChanged)

    @property
    def eventEditor(self):
        return self._actionModel.eventEditor

    @eventEditor.setter
    def eventEditor(self, eventEditor):
        self._actionModel.eventEditor = eventEditor

    def _emitDataChanged(self, index1, index2):
        mr1, mr2 = index1.row(), index2.row()
        if mr1 not in self._mapModelRow2ProxyRow or mr2 not in self._mapModelRow2ProxyRow:
            return
        r1, r2 = self._mapModelRow2ProxyRow[mr1], self._mapModelRow2ProxyRow[mr2]
        i1, i2 = self.index(r1, 0), self.index(r2, 0)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), i1, i2)

    def _emitAmountChanged(self, row):
        row = self._mapModelRow2ProxyRow[row]
        self.emit(SIGNAL('amountChanged(int)'), row)

    def _emitItemsCountChanged(self):
        self.emit(SIGNAL('itemsCountChanged()'))

    def setModel(self, model):
        # Это довольно специфическое решение. Запретим задавать целевую модель. Она задается в конструкторе.
        raise AttributeError()

    def __getattr__(self, attributeName):
        return getattr(self._actionModel, attributeName)

    def setData(self, index, value, group=None, *args, **kwargs):
        proxyRow = index.row()
        if 'related' in kwargs.keys():
            ifRelated = kwargs.pop('related')
        else:
            ifRelated = True

        if proxyRow not in self._mapProxyRow2Group and (proxyRow == len(self._mapModelRow2ProxyRow) or proxyRow == len(self._mapProxyRow2Group)):
            modelRow = len(self._actionModel.items())

        elif proxyRow not in self._mapProxyRow2Group:
            return False

        else:
            group = self._mapProxyRow2Group[proxyRow]
            modelRow = group.getModelRow(proxyRow, self._actionModel)

        index = self._actionModel.index(modelRow, 0)

        self._actionModel.blockSignals(True)

        result = self._actionModel.setData(index, value, *args, **kwargs)

        self._actionModel.blockSignals(False)

        if result:
            self._addNewItem(group)
            index = self.index(proxyRow, 0)
            self.emit(SIGNAL('rowsInserted(QModelIndex, int, int)'), index, proxyRow, proxyRow+1)
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            self.emitRowIndexActivated(proxyRow)
            if ifRelated:
                self.addRelatedActions(forceRef(value), index)

        return result


    def addRelatedActions(self, actionType_id, index=None):
        actionTypes = CActionTypeCache.getById(actionType_id).getRelatedActionTypes()
        if not index:
            index = self.index(self.rowCount()-2, 0)
        for actionType, isRequired in actionTypes.items():
            if isRequired:
                self.setData(self.index(index.row()+1, 0), actionType, self._mapProxyRow2Group[index.row()])
   
    
    def loadItems(self, eventId):
        self._actionModel._items = []
        self._items.clear()
        self._groups.clear()
        self._remapRows()
        self._actionModel.loadItems(eventId)
        self._group()

    def addGroup(self, actionTypeId, modelRow, item, mapActionTypeGroups=None):
        group = self._groups.newGroup(actionTypeId)
        self._mapProxyRow2Group[self._groups.groupsCount - 1] = group

        group.addItem(modelRow, item)

        if mapActionTypeGroups is not None:
            mapActionTypeGroups.setdefault(actionTypeId, []).append(group)

        return group

    def _group(self):
        actionTypeGroups = {}
        unadded = []
        for modelRow, item in enumerate(self._actionModel.items()):
            record, action = item

            actionTypeId = action.getType().id

            if action.getMasterId():
                unadded.append((modelRow, item, False))
                continue
            
            if actionTypeId not in actionTypeGroups:
                self.addGroup(actionTypeId, modelRow, item, actionTypeGroups)
                continue

            added = False

            for group in actionTypeGroups[actionTypeId]:
                if isinstance(group, CRelationsProxyModelGroup):
                    continue
                if group.addItem(modelRow, item):
                    added = True
                    break
            if added:
                continue

            self.addGroup(actionTypeId, modelRow, item, actionTypeGroups)      
        for modelRow, item, added in unadded:
            for key, groups in actionTypeGroups.items():
                for group in groups:
                    if isinstance(group, CRelationsProxyModelGroup): 
                        record, action = item 
                        if group.firstItem.id == action.getMasterId() or (not group.firstItem.id and id(group.firstItem) == action.getMasterId()):
                            group.addItem(modelRow, item)
                            added = True
                    if not group.expanded:
                        self.touchGrouping(group._mapItem2Row[group.firstItem])
                    if added:
                        continue
            if not added:
                self.addGroup(actionTypeId, modelRow, item, actionTypeGroups)  
        self._remapRows()

    def _remapRows(self):
        self._mapProxyRow2Group.clear()
        self._mapModelRow2ProxyRow.clear()

        modelItems = self._actionModel.items()

        proxyRow = 0
        for group in self._groups.groupsIterator:
            group.resetMapping(self._actionModel)
            for item in group.items:
                group.mapRows(proxyRow, item)
                self._mapProxyRow2Group[proxyRow] = group
                self._groups.mapGroup(proxyRow, group)
                self._mapModelRow2ProxyRow[modelItems.index(item)] = proxyRow
                if group.expanded:
                    proxyRow += 1
            if not group.expanded:
                proxyRow += 1


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if row not in self._mapProxyRow2Group:
            return QVariant()

        group = self._mapProxyRow2Group[row]
        modelRow = group.getModelRow(row, self._actionModel)

        modelIndex = self._actionModel.index(modelRow, 0)

        isHeadItem = group.isHeadItem(row, self._actionModel)

        if role == Qt.DisplayRole and not isHeadItem:
            value = forceString(self._actionModel.data(modelIndex, role))
            return QVariant(self._groupItemsShift+value)

        elif role == Qt.FontRole:
            items = self._actionModel.items()
            if 0 <= row < len(items):
                record, action = items[row]
                if isHeadItem and group.canBeGrouped():
                    if action and ((action.trailerIdx > 0 and not bool(action.trailerIdx & 1)) or forceRef(record.value('prevAction_id'))):
                        return self._qBoldItalicFont
                    return self._qBoldFont
                if action and ((action.trailerIdx > 0 and not bool(action.trailerIdx & 1)) or forceRef(record.value('prevAction_id'))):
                    return self._qItalicFont

        return self._actionModel.data(modelIndex, role)

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        return QtGui.QProxyModel.index(self, row, column, parent)

    def columnCount(self, index=None, *args, **kwargs):
        return 1

    def rowCount(self, index=None, *args, **kwargs):
        count = 1
        for group in self._groups.groupsIterator:
            count += len(group) if group.expanded else 1
        return count

    def canRowBeGrouped(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            return False

        group = self._mapProxyRow2Group[proxyRow]
        return group.canBeGrouped()


    def removeRows(self, row, count, parentIndex=QModelIndex(), *args, **kwargs):
        if not (0 <=row and row+count <= self.rowCount()):
            return False

        for proxyRow in xrange(row, row+count):
            self._removeRow(proxyRow)

        return True

    def afterRowsDeleting(self):
        self._emitItemsCountChanged()

    def _removeRow(self, proxyRow, removeRelated = False, unbind = False):
        if hasattr(self.eventEditor, 'tabStatus'):
            tabs = {
                0: self.eventEditor.tabStatus,
                1: self.eventEditor.tabDiagnostic,
                2: self.eventEditor.tabCure,
                3: self.eventEditor.tabMisc
            }
        else:
            tabs = {
                0: self.eventEditor.tabActions,
                1: self.eventEditor.tabActions,
                2: self.eventEditor.tabActions,
                3: self.eventEditor.tabActions
            }
        if proxyRow not in self._mapProxyRow2Group:
            return
        group = self._mapProxyRow2Group[proxyRow]
        if not group.expanded:
            self.touchGrouping(proxyRow)
        parentActionType = group.firstItem.action.getType()
        relatedActionTypes = CActionTypeCache.getById(parentActionType.id).getRelatedActionTypes()
        required = []
        for item in relatedActionTypes:
            relatedActionType = CActionTypeCache.getById(item)
            if parentActionType.class_ != relatedActionType.class_:
                required.append(relatedActionType.class_)
        required = set(required)
        if (len(group.items) > 1 or required) and group.getItem(proxyRow) == group.firstItem and not removeRelated and not unbind:
            res = QtGui.QMessageBox().warning(
                                            None,
                                            u'Внимание!',
                                            u"При удалении родительского действия удалятся и все подчиненные. Продолжить?",
                                            QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Cancel)
            if res == QtGui.QMessageBox.Ok:
                for itemClass in required:
                    for item in tabs[itemClass].modelAPActions._groups.groupsIterator:
                        if item.firstItem.action.getMasterId() == group.firstItem.id:
                            tabs[itemClass].modelAPActions._removeRow(item._mapItem2Row[item.firstItem], removeRelated = True)
                for item in reversed(sorted(group.proxyRows[1:])):
                    self._removeRow(item, removeRelated = True) 
            else:
                return False
        modelRow = group.getModelRow(proxyRow, self._actionModel)    
        removed = self._actionModel.removeRow(modelRow)
        if removed:
            del self._mapModelRow2ProxyRow[modelRow]
            group.deleteProxyRow(proxyRow, self._actionModel)
            if not len(group):
                self._groups.delete(group)
            del self._mapProxyRow2Group[proxyRow]
            self._remapRows()
            self.reset()

    
    def _unbindRow(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            return
        group = self._mapProxyRow2Group[proxyRow]
        if not group.expanded:
            self.touchGrouping(proxyRow)
        for item in reversed(sorted(group.proxyRows)):
            self._removeRow(item, removeRelated = True, unbind = True) 

    

    def touchGrouping(self, proxyRow):
        if self._mapProxyRow2Group and proxyRow < len(self._mapProxyRow2Group):
            group = self._mapProxyRow2Group[proxyRow]
            group.setExpanded(not group.expanded)
            self._resetData()

    def getExpandedByRow(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            return None
        group = self._mapProxyRow2Group[proxyRow]
        return group.expanded

    @property
    def _items(self):
        return self._groups

    def items(self):
        return self._groups

    def _resetData(self, remap=True):
        if hasattr(self, 'beginResetModel'):
            self.beginResetModel()
        if remap:
            self._remapRows()
        # self.reset()
        if hasattr(self, 'endResetModel'):
            self.endResetModel()
        else:
            self.reset()


    def _addNewItem(self, group = None):
        newItem = self._actionModel.items()[-1]
        modelRow = len(self._actionModel.items()) - 1
        newRecord, newAction = newItem
        if not newAction:
            return None, None

        begDateTime = forceDateTime(newRecord.value('begDate'))
        if not begDateTime or not begDateTime.isValid():
            newRecord.setValue('begDate', toVariant(QtCore.QDateTime().currentDateTime()))

        actionTypeId = newItem[1].getType().id

        added = False

        if group:
            if isinstance(group, CRelationsProxyModelGroup) and not newAction.getMasterId():
                newAction.setMasterId(id(group.firstItem))
            group.addItem(modelRow, newItem)
        else:
            for group in self._groups.groupsIterator:
                if group.actionTypeId != actionTypeId or isinstance(group, CRelationsProxyModelGroup):
                    continue

                if group.addItem(modelRow, newItem):
                    added = True
                    break

            if not added:
                group = self.addGroup(actionTypeId, modelRow, newItem)
        self._resetData()

        return group, newItem

    def addRow(self, *args, **kwargs):
        if 'related' in kwargs.keys():
            ifRelated = kwargs.pop('related')
        else:
            ifRelated = True
        result = self._actionModel.addRow(*args, **kwargs)
        group, _ = self._addNewItem()
        self.emitRowIndexActivated(self._groups.getGroupProxyRow(group))
        if ifRelated: 
            self.addRelatedActions(args[0], index = None)
        return result


    def addNewGroup(self, group):
        result = self._actionModel.addRow(presetAction=group.isHeadItem.action)
        self._groups.addGroup(group)
        return result


    def emitRowIndexActivated(self, row):
        self.emit(SIGNAL("rowIndexActivated(int)"), row)

    def flags(self, index):
        proxyRow = index.row()

        if proxyRow not in self._mapProxyRow2Group and proxyRow == len(self._groups):
            modelRow = len(self._actionModel.items())

        elif proxyRow not in self._mapProxyRow2Group:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            group = self._mapProxyRow2Group[proxyRow]
            modelRow = group.getModelRow(proxyRow, self._actionModel)

        return self._actionModel.flags(self._actionModel.index(modelRow, 0))

    def upRow(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            result = False

        else:
            group = self._mapProxyRow2Group[proxyRow]

            if group.canUpInGroup(proxyRow):
                result = group.upProxyRow(proxyRow)

            else:
                result = self._groups.upGroup(proxyRow, group)

        if result:
            self._remapRows()
            self.emitAllChanged()

        return result

    def downRow(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            result = False

        else:
            group = self._mapProxyRow2Group[proxyRow]

            if group.canDownInGroup(proxyRow):
                result = group.downProxyRow(proxyRow)

            else:
                result = self._groups.downGroup(proxyRow, group)

        if result:
            self._remapRows()
            self.emitAllChanged()

        return result

    def emitAllChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)

    def updateActionAmount(self, proxyRow):
        if proxyRow not in self._mapProxyRow2Group:
            return

        group = self._mapProxyRow2Group[proxyRow]
        modelRow = group.getModelRow(proxyRow, self._actionModel)
        self._actionModel.updateActionAmount(modelRow)

    def getFilledAction(self, newRecord, *args, **kwargs):
        plannedEndDate = directionDate = None
        saveDirectionDate = kwargs.pop('saveDirectionDates', False) and newRecord
        if saveDirectionDate:
            directionDate = forceDateTime(newRecord.value('directionDate'))
            plannedEndDate = forceDateTime(newRecord.value('plannedEndDate'))

        action = self._actionModel.getFilledAction(newRecord, *args, **kwargs)

        if saveDirectionDate:
            action.getRecord().setValue('directionDate', directionDate)
            action.getRecord().setValue('plannedEndDate', plannedEndDate)

        return action
    
    
    def addMasterIds(self):
        db = QtGui.qApp.db
        table = db.table('Action')
        for group in self._groups.groupsIterator:
            if isinstance(group, CRelationsProxyModelGroup):  
                ids = []   
                for item in group.items:
                    if item != group.firstItem:
                        ids.append(item.id)
                if ids:
                    db.updateRecords(table, 'master_id = {}'.format(group.firstItem.id), table['id'].inlist(ids))
        

    def saveItems(self, eventId):
        def _getEpItemsMap():
            epItems = {}
            for item in self._actionModel.items():
                action = item.action
                ep = action.getExecutionPlan()
                if not ep or not ep.id:
                    continue

                epItems.setdefault(ep.id, set()).update([i.id for i in ep.items if i.id])
            return epItems

        self._actionModel.saveItems(eventId)
        self.addMasterIds()

        newEpItemsMap = _getEpItemsMap()

        for epId, itemsIds in newEpItemsMap.items():
            itemsCond = [
                CActionExecutionPlanItem.masterId == epId
            ]
            if not itemsIds:
                CQuery.delete(CActionExecutionPlan, CActionExecutionPlan.id == epId)
            else:
                itemsCond.append(CActionExecutionPlanItem.id.notInlist(itemsIds))

            CQuery.delete(
                CActionExecutionPlanItem, itemsCond
            )
