# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import itertools

from Events.ActionsModel import CActionRecordItem

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QVariant

from Events.Action import CAction
from Events.ExecutionPlan.Groups import CExecutionPlanProxyModelGroup
from Events.Utils        import calcQuantity, calcQuantityEx

from Stock.NomenclatureComboBox import CNomenclatureComboBox
from library.DateEdit import CDateEdit
from library.ROComboBox import CROEditableComboBox

from library.Utils import (forceDate, forceRef, forceString, forceDouble, forceInt, toVariant, forceStringEx,
                           trim
                           )

from Events.NomenclatureExpense.Utils import (
    DIREACTION_DATE_INDEX,
    BEG_DATE_INDEX,
    NOMENCLATURE_INDEX,
    PLAN_END_DATE,
    DOSES_INDEX,
    SIGNA_INDEX,
    DURATION_INDEX,
    ALIQUOTICITY_INDEX,
    PERIODICITY_INDEX,
    CCellsSettings
)
from library.crbcombobox import CRBComboBox

DONE_COLOR = QtGui.QColor(Qt.green)
NOT_DONE_COLOR = QtGui.QColor(Qt.yellow)
OVERDUE_COLOR = QtGui.QColor(Qt.red)

_mapColumnIndex2ValueConverter = {
    DOSES_INDEX: forceDouble,
    SIGNA_INDEX: forceString,
    NOMENCLATURE_INDEX: forceRef
}

_mapColumnIndex2FieldName = {
    DURATION_INDEX: 'duration',
    ALIQUOTICITY_INDEX: 'aliquoticity',
    PERIODICITY_INDEX: 'periodicity'
}


class CExpenseNomenclatureComboBox(CNomenclatureComboBox):
    def __init__(self, parent):
        CNomenclatureComboBox.__init__(self, parent)


    def setValue(self, value):
        itemId = forceRef(value)
        if itemId:
            self.setFilter('')
            rowIndex = self._model.searchId(itemId)
            if rowIndex >= 0:
                self.setCurrentIndex(rowIndex)
        else:
            CNomenclatureComboBox.setValue(self, forceRef(value))


    def setFinanceMedicalAidKind(self, var):
        if self._financeId != self._popup._financeId:
            self.setFinanceId(self._popup._financeId)
        if self._medicalAidKindId != self._popup._medicalAidKindId:
            self.setMedicalAidKindId(self._popup._medicalAidKindId)
        self.getFilterData()
        self._filier = self._filter
        self.reloadData()
        self.setValue(var)


class CSIGNANomenclatureComboBox(CROEditableComboBox):
    def __init__(self, parent = None):
        CROEditableComboBox.__init__(self, parent)
        self.values = []


    def toString(self, val, record):
        str = forceStringEx(val).lower()
        for item in self.values:
            if trim(item.lower()) == str:
                return toVariant(item)
        if str:
            self.values.append(forceString(val))
        return toVariant(val)


    def createEditor(self, parent):
        editor = CROEditableComboBox(parent)
        for val in self.values:
            editor.addItem(val)
        return editor


    def setValues(self, values):
        self.values = values


class Col(object):
    def __init__(self, key, width, title, switchOff=True):
        self.key = key
        self.width = width
        self._title = QVariant(title)
        self._switchOff = switchOff


    def switchOff(self):
        return self._switchOff


    def setTitle(self, title):
        self._title = toVariant(title)


    def title(self):
        return self._title


def _flagIteration(iterable, flag):
    for i in iterable:
        yield flag, i


class CNomenclatureExpenseModel(QtCore.QAbstractTableModel):
    STATIC_HEADERS = {
        DIREACTION_DATE_INDEX: (u'Дата назначения', 10),
        BEG_DATE_INDEX: (u'Дата начала', 10),
        PLAN_END_DATE: (u'План', 10),
        NOMENCLATURE_INDEX: (u'ЛС', 10),
        DOSES_INDEX: (u'Доза', 3),
        SIGNA_INDEX: (u'СП', 3),
        DURATION_INDEX: (u'Д', 3),
        ALIQUOTICITY_INDEX: (u'К', 3),
        PERIODICITY_INDEX: (u'И', 3)
    }

    def cols(self):
        cols = []
        key = 0
        for key in sorted(self.STATIC_HEADERS.keys()):
            cols.append(Col(key, self.STATIC_HEADERS[key][1], self.STATIC_HEADERS[key][0]))

        for monthKey in range(31):
            cols.append(Col(key+monthKey+1, 3, str(monthKey+1)))

        return cols


    def __init__(self, parent=None, date=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._groups = []
        self._mapGroupToCopy = {}
        self._originGroups = []
        self._newGroups = []
        self._date = date or QtCore.QDate.currentDate()
        self._cellsSettings = CCellsSettings(self)
        self._actionTypeId = None
        self._nomenclatureId = None
        self._onlyActual = False
        self._ignoreTime = False
        self._considerPeriod = False
        self._begDate = None
        self._endDate = None
        self._eventEditor = None
        self._stockOrgStructureId = None


    def groups(self):
        return self._groups


    def groupsToSavePrepare(self):
        return [g for g in self._groups if g in self._mapGroupToCopy.values()]


    def groupsToAdd(self):
        return self._newGroups


    def discardChanges(self):
        pass


    def setOrgStructureId(self, orgStructureId):
        self._stockOrgStructureId = orgStructureId


    def setEventEditor(self, eventEditor):
        self._eventEditor = eventEditor


    def setBegDate(self, begDate):
        self._begDate = begDate
        self.setOriginGroups(self._originGroups)


    def setEndDate(self, endDate):
        self._endDate = endDate
        self.setOriginGroups(self._originGroups)


    def setActionTypeId(self, actionTypeId):
        self._actionTypeId = actionTypeId
        self.setOriginGroups(self._originGroups)


    def setNomenclatureId(self, nomenclatureId):
        self._nomenclatureId = nomenclatureId
        self.setOriginGroups(self._originGroups)


    def setDate(self, date):
        self._date = date
        self.setOriginGroups(self._originGroups)


    def setOnlyActual(self, onlyActual):
        self._onlyActual = onlyActual
        self.setOriginGroups(self._originGroups)


    def setIgnoreTime(self, ignoreTime):
        self._ignoreTime = ignoreTime
        self.setOriginGroups(self._originGroups)


    def considerPeriod(self, considerPeriod):
        self._considerPeriod = considerPeriod
        self.setOriginGroups(self._originGroups)


    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._groups) + 1


    def columnCount(self, parent=None, *args, **kwargs):
        return self._date.daysInMonth() + 1 + PERIODICITY_INDEX


    def setOriginGroups(self, groups):
        self._originGroups = groups
        groupsNoNew = []
        for g in groups:
            if g and g not in self._newGroups and g not in groupsNoNew:
                groupsNoNew.append(g)
        self._groups = []

        for isNew, group in itertools.chain(
                _flagIteration(groupsNoNew, False),
                _flagIteration(self._newGroups, True)):

            if not self._actionTypeId or self._actionTypeId != group.actionTypeId:
                continue

            canceled = False
            items = group.items
            for i in range(len(items)):
                if forceInt(group.items[i].action._record.value('status'))==3 and self._onlyActual:
                    canceled = True
                    break
            if canceled:
                continue

            if self._considerPeriod:
                if self._begDate and group.begDate() < self._begDate:
                    continue

                elif self._endDate and group.begDate() > self._endDate:
                    continue

            if self._date:
                begDate = group.begDate()
                begYM = (begDate.year(), begDate.month())
                planEndDate = group.planEndDate()
                planEndYM = (planEndDate.year(), planEndDate.month())
                YM = (self._date.year(), self._date.month())
                if not (begYM <= YM <= planEndYM):
                    continue

            if self._nomenclatureId and group.nomenclatureId and group.nomenclatureId != self._nomenclatureId:
                continue

            if group in self._mapGroupToCopy:
                self._groups.append(self._mapGroupToCopy[group])
            elif isNew:
                self._groups.append(group)
            else:
                copied = group.copy()
                self._mapGroupToCopy[group] = copied
                self._groups.append(copied)

        self.reset()


    def _addNewGroup(self, nomenclatureId):
        newGroup = CExecutionPlanProxyModelGroup(None)
        self._newGroups.append(newGroup)
        self._groups.append(newGroup)

        actionRecord = QtGui.qApp.db.table('Action').newRecord()
        action = CAction.getFilledAction(self._eventEditor, actionRecord, self._actionTypeId)
        action.updateExecutionPlanByRecord(forceDuration=True)
        item = CActionRecordItem(actionRecord, action)
        newGroup.addItem(None, item)
        self._cellsSettings.setGroupNomenclature(newGroup, nomenclatureId)
        self._cellsSettings.setGroupSigna(newGroup, self.getSignaToNomenclatureId(nomenclatureId))
        doses = self._cellsSettings.getNomenclatureDoses(nomenclatureId)
        self._cellsSettings.setGroupDoses(newGroup, doses)
        newGroup.setAliquoticity(newGroup.aliquoticity(), updateExecutionPlan=False)
        newGroup.setPeriodicity(newGroup.periodicity(), updateExecutionPlan=False)
        newGroup.setDuration(newGroup.duration(), updateExecutionPlan=False)
        self.calcQuantity(newGroup)
        self._setItemsDefaultDosesValueAndNomenclature(newGroup)
        for epItem in action.getExecutionPlan().items:
            if epItem.nomenclature:
                epItem.nomenclature.dosage = doses
                epItem.nomenclature.nomenclatureId = nomenclatureId
                nomenclatureItem = epItem.nomenclature
                nomenclatureItem.actionExecutionPlanItem = epItem
        action.updateSpecifiedName()

        index = QtCore.QModelIndex()
        cnt = len(self._groups)
        self.beginInsertRows(index, cnt, cnt)
        self.insertRows(cnt, 1, index)
        self.endInsertRows()
        self.emitItemsCountChanged()


    def _addNewGroupFromTemplate(self, newAction):
        newGroup = CExecutionPlanProxyModelGroup(None)
        self._newGroups.append(newGroup)
        self._groups.append(newGroup)
        newRecord = newAction.getRecord()
        item = CActionRecordItem(newRecord, newAction)
        newGroup.addItem(None, item)
        newGroup.setDuration(newGroup.duration(), updateExecutionPlan=False)
        newAction.updateSpecifiedName()
        index = QtCore.QModelIndex()
        cnt = len(self._groups)
        self.beginInsertRows(index, cnt, cnt)
        self.insertRows(cnt, 1, index)
        self.endInsertRows()
        self.emitItemsCountChanged()


    def calcQuantity(self, group):
        action = group.headItem.action
        if action:
            quantity = forceInt(calcQuantity(action.getRecord()))
            group.setQuantity(quantity if quantity else 1)


    def _setItemsDefaultDosesValueAndNomenclature(self, group):
        doses = self._cellsSettings.getGroupDoses(group)
        nomenclatureId = self._cellsSettings.getGroupNomenclature(group)
        action = group.headItem.action
        for epItem in action.getExecutionPlan().items:
            if epItem.nomenclature:
                epItem.nomenclature.dosage = doses
                epItem.nomenclature.nomenclatureId = nomenclatureId
                nomenclatureItem = epItem.nomenclature
                nomenclatureItem.actionExecutionPlanItem = epItem


    def itemsToOrigin(self, items):
        result = []
        for i in items:
            item = i.item
            if item.__origin__:
                item.mergeIntoOrigin()
            result.append(item.getOrigin())
        return result


    def updateDosageByIndex(self, index, dosage):
        if not index.isValid():
            return
        row = index.row()
        group = self._groups[row]
        if group:
            group.setDosageInExists(dosage)
            self.reset()


    def updateDosageNomenclatureByIndex(self, group):
        if group:
            dosage = self._cellsSettings.getGroupDoses(group)
            nomenclatureId = self._cellsSettings.getGroupNomenclature(group)
            group.setDosageNomenclatureInExists(dosage, nomenclatureId)
            self.reset()


    def updateDosageNomenclatureFromDate(self, group, date):
        if group:
            dosage = self._cellsSettings.getGroupDoses(group)
            nomenclatureId = self._cellsSettings.getGroupNomenclature(group)
            group.setDosageNomenclatureFromDate(dosage, nomenclatureId, date)
            self.reset()


    @property
    def lastMainIndex(self):
        return PERIODICITY_INDEX


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if (role != Qt.DisplayRole and role != Qt.ToolTipRole) or section < 0:
            return QtCore.QVariant()

        if orientation == Qt.Horizontal:
            if role == Qt.ToolTipRole:
                if section == NOMENCLATURE_INDEX:
                    return QVariant(u'Лекарственное средство')
                elif section == DOSES_INDEX:
                    return QVariant(u'Доза на один прием')
                elif section == SIGNA_INDEX:
                    return QVariant(u'Способ применения')
                elif section == DURATION_INDEX:
                    return QVariant(u'Длительность курса в днях')
                elif section == ALIQUOTICITY_INDEX:
                    return QVariant(u'Количество приемов в сутки (кратность)')
                elif section == PERIODICITY_INDEX:
                    return QVariant(u'''Интервал между днями приема: 
0 - каждый день,
1 - через 1 день,
2 - через 2 дня,
3 - через 3 дня,
и т.д.''')
                else:
                    return QtCore.QVariant()
            if section in self.STATIC_HEADERS:
                return QtCore.QVariant(self.STATIC_HEADERS[section][0])
            return QtCore.QVariant(section - PERIODICITY_INDEX)

        return QtCore.QVariant()


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        row = index.row()

        if not (0 <= row < len(self._groups)):
            return QtCore.QVariant()

        group = self._groups[row]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == DIREACTION_DATE_INDEX:
                return QtCore.QVariant(group.directionDate().date())
            elif column == BEG_DATE_INDEX:
                return QtCore.QVariant(group.begDate())
            elif column == PLAN_END_DATE:
                return QtCore.QVariant(group.planEndDate())
            elif column == NOMENCLATURE_INDEX:
                return QtCore.QVariant(self._cellsSettings.getGroupNomenclatureText(group))
            elif column == DOSES_INDEX:
                return QtCore.QVariant(self._cellsSettings.getGroupDosesText(group))
            elif column == SIGNA_INDEX:
                return QtCore.QVariant(self._cellsSettings.getGroupSignaText(group))
            elif column == DURATION_INDEX:
                return QtCore.QVariant(group.duration())
            elif column == ALIQUOTICITY_INDEX:
                return QtCore.QVariant(group.aliquoticity())
            elif column == PERIODICITY_INDEX:
                return QtCore.QVariant(group.periodicity())
            elif column > PERIODICITY_INDEX:
                return QtCore.QVariant(self._getDayDataValue(row, column, group))

        elif role == Qt.BackgroundColorRole:
            items = group.items
            enabled = True
            for i in range(len(items)):
                if group.items[i].action._record.value('status')==3:
                    enabled = False
                    break
            if not enabled:
                return QtCore.QVariant(QtGui.QColor(Qt.gray))
            else:
                if column > PERIODICITY_INDEX:
                    return QtCore.QVariant(self._getDayDataColor(row, column, group))

        return QtCore.QVariant()


    def _getDayDataValue(self, row, column, group):
        year = self._date.year()
        month = self._date.month()
        day = column - PERIODICITY_INDEX
        planItems = 0

        items = group.getItemsByDate(QtCore.QDate(year, month, day))
        if not items:
            return None
        planItems = len(items)

        not_done_items = []

        for item in items:
            executedDatetime = item.executedDatetime
            if executedDatetime is None:
                not_done_items.append(item)
            elif executedDatetime.isNull() or not executedDatetime.isValid():
                not_done_items.append(item)

        return u'%i/%i' % (planItems-len(not_done_items), planItems)


    def _getDayDataColor(self, row, column, group):
        year = self._date.year()
        month = self._date.month()
        day = column - PERIODICITY_INDEX

        items = group.getItemsByDate(QtCore.QDate(year, month, day))
        if not items:
            return None

        not_done_items = []
        overdue_items = []

        for item in items:
            executedDatetime = item.executedDatetime
            if executedDatetime is None:
                not_done_items.append(item)

            elif executedDatetime.isNull() or not executedDatetime.isValid():
                not_done_items.append(item)

            elif executedDatetime > QtCore.QDateTime(item.date, item.time) and not self._ignoreTime:
                overdue_items.append(item)
            elif forceDate(executedDatetime) > QtCore.QDateTime(item.date) and self._ignoreTime:
                overdue_items.append(item)

        if not_done_items:
            return NOT_DONE_COLOR

        elif overdue_items:
            return OVERDUE_COLOR

        return DONE_COLOR


    def flags(self, index):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        row = index.row()
        if row > len(self._groups):
            return flags

        editableFlags = flags | Qt.ItemIsEditable

        if row == len(self._groups):
            if self._actionTypeId and index.column() == NOMENCLATURE_INDEX:
                return editableFlags
            return flags

        column = index.column()
        group = self._groups[row]
        if column > PERIODICITY_INDEX:
            return flags

        elif column == DOSES_INDEX and not group.hasExecutedItems() and group.groupDataNotChanged():
            return editableFlags

        elif column == DURATION_INDEX and group.groupDataNotChanged() and not group.hasSavedItems() and not group.hasExecutedItems():
            return editableFlags

        if group.groupDataNotChanged():
            if column == DOSES_INDEX and group.hasExecutedItems():
                return flags
            elif column != DOSES_INDEX and (group.hasSavedItems() or group.hasExecutedItems()):
                return flags
            else:
                return editableFlags

        elif group.hasExecutedItems():
            return flags

        elif group.hasSavedItems():
            return flags

        return editableFlags


    def createEditor(self, index, parent):
        column = index.column()
        row = index.row()

        assert 0 <= row <= len(self._groups)
        assert 0 <= column <= PERIODICITY_INDEX

        if column == DIREACTION_DATE_INDEX:
            return CDateEdit(parent)

        elif column == BEG_DATE_INDEX:
            return CDateEdit(parent)

        elif column == NOMENCLATURE_INDEX:
            return self._createNomenclatureEditor(parent)

        elif column == PLAN_END_DATE:
            return CDateEdit(parent)

        elif column == DOSES_INDEX:
            editor = QtGui.QDoubleSpinBox(parent)
            editor.setMaximum(10000)
            editor.setMinimum(0)
            editor.setDecimals(2)
            return editor

        elif column == SIGNA_INDEX:
            return self._createSIGNAEditor(parent, row)
            # return QtGui.QLineEdit(parent)

        elif column in (DURATION_INDEX, ALIQUOTICITY_INDEX, PERIODICITY_INDEX):
            editor = QtGui.QSpinBox(parent)
            editor.setMaximum(365)
            editor.setMinimum(0)
            return editor

        else:
            return QtGui.QLineEdit(parent)


    def setEditorData(self, index, editor):
        row = index.row()
        column = index.column()
        if not (0 <= row < len(self._groups)):
            return False

        group = self._groups[row]

        if column == DIREACTION_DATE_INDEX:
            directionDate = group.directionDate()
            if directionDate is None:
                directionDate = QtCore.QDate()
            else:
                directionDate = directionDate.date()
            editor.setDate(directionDate)
            return True

        elif column == BEG_DATE_INDEX:
            editor.setDate(group.begDate() or QtCore.QDate())
            return True

        elif column == PLAN_END_DATE:
            editor.setDate(group.planEndDate() or QtCore.QDate())
            return True

        elif column == NOMENCLATURE_INDEX:
            editor.setValue(self._cellsSettings.getGroupNomenclature(group) or 1)
            return True

        elif column == DOSES_INDEX:
            editor.setValue(self._cellsSettings.getGroupDoses(group) or 1)
            return True
        elif column == SIGNA_INDEX:
            editor.setValue(self._cellsSettings.getGroupSigna(group))
            return True

        elif column == DURATION_INDEX:
            value = group.duration() or 1
            if group.hasExecutedItems():
                editor.setMinimum(value)
            editor.setValue(group.duration() or 1)
            return True

        elif column == ALIQUOTICITY_INDEX:
            editor.setValue(group.aliquoticity() or 1)
            return True

        elif column == PERIODICITY_INDEX:
            editor.setValue(group.periodicity() or 1)
            return True

        return False


    def getEditorData(self, index, editor):
        column = index.column()
        if column == DIREACTION_DATE_INDEX:
            return editor.date()
        elif column == BEG_DATE_INDEX:
            return editor.date()
        elif column == PLAN_END_DATE:
            return editor.date()
        elif column == NOMENCLATURE_INDEX:
            return editor.value()
        elif column == DOSES_INDEX:
            return editor.value()
        elif column == SIGNA_INDEX:
            return editor.value()
        elif column == DURATION_INDEX:
            return editor.value()
        elif column == ALIQUOTICITY_INDEX:
            return editor.value()
        elif column == PERIODICITY_INDEX:
            return editor.value()


    def _createSIGNAEditor(self, parent, row):
        editor = CRBComboBox(parent)
        group = self._groups[row]
        nomenclatureId = self._cellsSettings.getGroupNomenclature(group)
        usingTypeIdList = []
        if nomenclatureId:
            db = QtGui.qApp.db
            table = db.table('rbNomenclature_UsingType')
            usingTypeIdList = db.getDistinctIdList(table, table['usingType_id'].name(),
                                                   [table['master_id'].eq(nomenclatureId)],
                                                   order=table['idx'].name())
        if usingTypeIdList:
            filter = 'rbNomenclatureUsingType.id IN (%s)' % (
                u','.join(str(usingTypeId) for usingTypeId in usingTypeIdList if usingTypeId))
        else:
            filter = u''
        editor.setTable('rbNomenclatureUsingType', addNone=True, filter=filter)
        return editor


    def _createNomenclatureEditor(self, parent):
        editor = CExpenseNomenclatureComboBox(parent)
        cols = ['nomenclatureClass_id', 'nomenclatureKind_id', 'nomenclatureType_id']  # wtf
        record = QtGui.qApp.db.getRecord('ActionType', cols, self._actionTypeId)

        nomenclatureClassId = forceRef(record.value('nomenclatureClass_id'))
        nomenclatureKindId = forceRef(record.value('nomenclatureKind_id'))
        nomenclatureTypeId = forceRef(record.value('nomenclatureType_id'))
        editor.setOnlyNomenclature(True)
        editor.setDefaultIds(nomenclatureClassId, nomenclatureKindId, nomenclatureTypeId)
        if self._eventEditor:
            editor.setUseClientUnitId()
            editor.setFinanceId(self._eventEditor.eventFinanceId)
            editor.setMedicalAidKindId(self.getMedicalAidKindId(self._eventEditor.eventTypeId))

        editor.setOrgStructureId(self._stockOrgStructureId if self._stockOrgStructureId else QtGui.qApp.currentOrgStructureId())
        editor.setOnlyExists()
        editor.getFilterData()
        editor.setFilter(editor._filter)
        return editor


    def getMedicalAidKindId(self, eventTypeId):
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        cond = [tableEventType['id'].eq(eventTypeId)]
        queryTable = tableEvent
        queryTable = queryTable.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        record = db.getRecordEx(queryTable, tableEventType['medicalAidKind_id'], cond)
        if record:
            return forceInt(record.value('medicalAidKind_id'))
        return None


    def getSignaToNomenclatureId(self, nomenclatureId):
        if nomenclatureId:
            db = QtGui.qApp.db
            table = db.table('rbNomenclature')
            tableUsingType = db.table('rbNomenclature_UsingType')
            tableRBUsingType = db.table('rbNomenclatureUsingType')
            queryTable = table.innerJoin(tableUsingType, tableUsingType['master_id'].eq(table['id']))
            queryTable = queryTable.innerJoin(tableRBUsingType, tableRBUsingType['id'].eq(tableUsingType['usingType_id']))
            record = db.getRecordEx(queryTable, [tableRBUsingType['name'].alias('usingType')], [table['id'].eq(nomenclatureId)], order=tableUsingType['idx'].name())
            return forceString(record.value('usingType')) if record else u''
        return u''


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role != Qt.EditRole:
            return False

        column = index.column()

        row = index.row()
        if row == len(self._groups):
            if column != NOMENCLATURE_INDEX:
                return False

            if not value or (isinstance(value, QtCore.QVariant) and value.isNull()):
                return False

            self._addNewGroup(forceRef(value))

        isExistsDoneByIndex = self.existsDoneByIndex(index)
        group = self._groups[row]

        if column == DIREACTION_DATE_INDEX and not isExistsDoneByIndex:
            if not value.isValid():
                return False

            if value.isNull():
                return False

            group.setDirectionDate(forceDate(value))
            return True

        elif column == BEG_DATE_INDEX and not isExistsDoneByIndex:
            if not value.isValid():
                return False

            if value.isNull():
                return False

            begDate = forceDate(value)
            if begDate == group.begDate():
                return True

            duration = max(group.begDate().daysTo(group.planEndDate())+1, 1)
            group.setBegDate(begDate)
            group.setPlanEndDate(begDate.addDays(duration))
            group.setDuration(duration, updateExecutionPlan=False)
            self.calcQuantity(group)
            self._setItemsDefaultDosesValueAndNomenclature(group)
            return True

        elif column == PLAN_END_DATE and not isExistsDoneByIndex:
            plannEndDate = forceDate(value)
            if plannEndDate == group.planEndDate():
                return True

            group.setPlanEndDate(plannEndDate)
            duration = max(group.begDate().daysTo(plannEndDate)+1, 1)
            group.setDuration(duration, updateExecutionPlan=False)
            self.calcQuantity(group)
            self._setItemsDefaultDosesValueAndNomenclature(group)
            return True

        elif column == NOMENCLATURE_INDEX and not isExistsDoneByIndex:
            newNomenclatureId = forceRef(value)
            oldNomenclatureId = self._cellsSettings.getGroupNomenclature(group)
            self._cellsSettings.setGroupNomenclature(group, newNomenclatureId)
            if oldNomenclatureId != newNomenclatureId:
                if not (self._cellsSettings.getGroupSigna(group)):  # 0011445:0056953:пункт 1
                    self._cellsSettings.setGroupSigna(group, self.getSignaToNomenclatureId(newNomenclatureId))
            return True

        elif column == DOSES_INDEX:
            oldDosage = self._cellsSettings.getGroupDoses(group)
            self._cellsSettings.setGroupDoses(group, forceDouble(value))
            self._setItemsDefaultDosesValueAndNomenclature(group)
            newDosage = self._cellsSettings.getGroupDoses(group)
            if newDosage != oldDosage:
                self.updateDosageByIndex(index, newDosage)
                group.updateSpecifiedName()
            return True

        elif column == SIGNA_INDEX and not isExistsDoneByIndex:
            self._cellsSettings.setGroupSigna(group, forceRef(value))
            return True

        elif column == DURATION_INDEX and not isExistsDoneByIndex:
            currentDuration = group.duration()
            duration = forceInt(value)
            if duration == currentDuration:
                return True

            if group.hasExecutedItems():
                if duration < currentDuration:
                    return False
                doses = self._cellsSettings.getGroupDoses(group)
                nomenclatureId = self._cellsSettings.getGroupNomenclature(group)
                items = group.addDaysToEP(duration-currentDuration)
                for item in items:
                    if item.nomenclature:
                        item.nomenclature.dosage = doses
                        item.nomenclature.nomenclatureId = nomenclatureId
                return True

            group.setDuration(duration, updateExecutionPlan=False)
            self.calcQuantity(group)
            self.updateDosageNomenclatureByIndex(group)
            return True

        elif column == ALIQUOTICITY_INDEX and not isExistsDoneByIndex:
            aliquoticity = forceInt(value)
            if aliquoticity == group.aliquoticity():
                return True

            group.setAliquoticity(forceInt(value), updateExecutionPlan=False)
            self.calcQuantity(group)
            self.updateDosageNomenclatureByIndex(group)
            return True
        elif column == PERIODICITY_INDEX and not isExistsDoneByIndex:
            periodicity = forceInt(value)
            if periodicity == group.periodicity():
                return True

            group.setPeriodicity(forceInt(value), updateExecutionPlan=False)
            self.calcQuantity(group)
            self.updateDosageNomenclatureByIndex(group)
            return True

        self.emitRowDataChanged(row)
        self.emitAllDataChanged()


    def emitRowDataChanged(self, row):
        index1 = self.index(row, 0)
        index2 = self.index(row, self.columnCount())
        self.emit(QtCore.SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitAllDataChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(QtCore.SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitItemsCountChanged(self):
        self.emit(QtCore.SIGNAL('itemsCountChanged()'))


    def getItemsByIndex(self, index):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return []

        column = index.column()
        if column in self.STATIC_HEADERS:
            return []

        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]

        return group.getItemsByDate(date)


    def existsByIndex(self, index):
        return bool(self.getItemsByIndex(index))


    def existsDoneByIndex(self, index):
        items = self.getItemsByIndex(index)
        if not items:
            return False

        for item in items:
            if item.executedDatetime:
                return True
        return False


    def existsDoneActionItemExecToDateByIndex(self, index):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return False
        column = index.column()
        if column in self.STATIC_HEADERS:
            return False
        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]
        return group.existsDoneActionItemExecToDate(date)


    def existsDoneAfterIndex(self, index):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return False

        column = index.column()
        if column in self.STATIC_HEADERS:
            return False

        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]
        return group.existsDoneAfterDate(date)


    def existsDoneActionAfterIndex(self, index):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return False

        column = index.column()
        if column in self.STATIC_HEADERS:
            return False

        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]
        return group.existsDoneActionAfterDate(date)


    def isIndexAfterBegDate(self, index):
        row = index.row()

        if not (0 <= row < len(self._groups)):
            return False

        column = index.column()
        if column in self.STATIC_HEADERS:
            return False

        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]
        return group.begDate() <= date


    def getDosageUnitName(self, row):
        group = self._groups[row]
        return self._cellsSettings.getNomenclatureDosageUnitName(group.nomenclatureId)


    def setItemsForDayIndex(self, index, items, isApplyChangesCourseNextDays=False):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return

        column = index.column()
        if column in self.STATIC_HEADERS:
            return

        if isApplyChangesCourseNextDays:
            group = self._groups[row]
            cols = self.cols()
            for col in range(column, len(cols)):
                if col not in self.STATIC_HEADERS:
                    date = QtCore.QDate(self._date.year(), self._date.month(), col - PERIODICITY_INDEX)
                    itemsAlreadyExists = bool(group.getItemsByDate(date))
                    if itemsAlreadyExists:
                        group.setItemsByDate(date, items)
        else:
            date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
            group = self._groups[row]
            itemsAlreadyExists = bool(group.getItemsByDate(date))
            group.setItemsByDate(date, items)
            if not itemsAlreadyExists:
                maxDate = group.getMaxItemDate()
                group.setDuration(group.begDate().daysTo(maxDate) + 1, updateExecutionPlan=False)


    def setDurationForDayIndex(self, index, quantityDay, skipAfterLastDayCourse=0, isLastDayCourse=False):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return
        if quantityDay > 0:
            group = self._groups[row]
            maxDate = group.getMaxItemDate()
            quantity = forceInt(calcQuantityEx(group.aliquoticity(), group.periodicity(), quantityDay))
            quantityAdd = quantity if quantity else 1
            items = group.addDaysToEP(daysCount=quantityDay, quantityAdd=quantityAdd, skipAfterLastDayCourse=skipAfterLastDayCourse, isLastDayCourse=isLastDayCourse)
            if not isLastDayCourse:
                self.updateDosageNomenclatureFromDate(group, maxDate)
            newMaxDate = group.getMaxItemDate()
            group.setDuration(group.begDate().daysTo(newMaxDate) + 1, updateExecutionPlan=False)
        return items


    def deleteItemsByIndex(self, index):
        row = index.row()
        if not (0 <= row < len(self._groups)):
            return

        column = index.column()
        if column in self.STATIC_HEADERS:
            return

        date = QtCore.QDate(self._date.year(), self._date.month(), column - PERIODICITY_INDEX)
        group = self._groups[row]
        group.deleteItemsByDate(date)
