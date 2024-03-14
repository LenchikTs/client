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
import json

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, pyqtSignature, QModelIndex

from library.DialogBase import CDialogBase
from Events.NomenclatureExpense.NomenclatureExpenseModel import CNomenclatureExpenseModel
from Events.NomenclatureExpense.QueriesStatements        import getNomenclatureActionTypesIds
from Events.NomenclatureExpense.NomenclatureExpenseLoadTemplate import CNomenclatureExpenseLoadTemplate
from Events.NomenclatureExpense.Utils import (DIREACTION_DATE_INDEX,
                                             BEG_DATE_INDEX,
                                             NOMENCLATURE_INDEX,
                                             DOSES_INDEX,
                                             DURATION_INDEX,
                                             ALIQUOTICITY_INDEX,
                                             #CCellsSettings
                                             )
from Events.ActionStatus                                 import CActionStatus
from Events.ActionsSelector                              import CTemplateEditor
#from Events.Utils                                        import calcQuantityEx
from library.Utils                                       import forceString, forceInt, forceDate, forceBool, toVariant

from Events.NomenclatureExpense.Ui_NomenclatureExpenseDialog import Ui_NomenclatureExpenseDialog
from Events.NomenclatureExpense.Ui_ExtendAppointmentNomenclatureDialog import Ui_ExtendAppointmentNomenclatureDialog


_RECIPE = 1
_DOSES  = 2
_SIGNA  = 3
_ACTIVESUBSTANCE = 4

def _getDefaultValues():
    result = {}
    data = forceString(
        QtGui.qApp.preferences.appPrefs.get('NomenclatureExpenseDialogDefaultValues', '')
    )
    try:
        data = json.loads(data) if data else {}
    except:
        data = {}

    result['actionTypeId'] = data.get('actionTypeId', None)
    result['nomenclatureId'] = data.get('nomenclatureId', None)
    result['begDate'] = QtCore.QDate.fromString(data.get('begDate', QtCore.QDate.currentDate().toString('yyyy.MM.dd')), 'yyyy.MM.dd')
    result['endDate'] = QtCore.QDate.fromString(data.get('endDate', QtCore.QDate.currentDate().toString('yyyy.MM.dd')), 'yyyy.MM.dd')
    result['year'] = data.get('year', QtCore.QDate.currentDate().year())
    result['month'] = data.get('month', QtCore.QDate.currentDate().month() - 1)
    result['period'] = data.get('period', False)
    result['actual'] = data.get('actual', True)
    result['ignoreTime'] = data.get('ignoreTime', False)
    result['currentEvent'] = data.get('currentEvent', True)
    result['orgStructureId'] = data.get('orgStructureId', None)

    return result


class CNomenclatureExpenseDialog(CDialogBase, Ui_NomenclatureExpenseDialog):
    def __init__(self, parent=None, eventEditor=None, groups=None, fromEventEditor=True):
        CDialogBase.__init__(self, parent)

        self.modelNomenclatureExpense = None
        self.selectionModelNomenclatureExpense = None

        self.addModels('NomenclatureExpense', CNomenclatureExpenseModel(self))
        self.selectionModelNomenclatureExpenseDays = QtGui.QItemSelectionModel(self.modelNomenclatureExpense, self)
        self.selectionModelNomenclatureExpenseDays.setObjectName('selectionModelNomenclatureExpenseDays')
        self.addObject('btnSaveTemplate', QtGui.QPushButton(u'Сохранить шаблон', self))
        self.addObject('btnLoadTemplate', QtGui.QPushButton(u'Загрузить шаблон', self))

        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)
        self.buttonBox.addButton(self.btnSaveTemplate, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnLoadTemplate, QtGui.QDialogButtonBox.ActionRole)

        self.cmbActionType.setClass(None)
        self.cmbActionType.setClassesVisible(True)
        self.setCmbActionTypeFilter()
        self.cmbNomenclature.setOnlyExists(True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())

        defaults = _getDefaultValues()

        self.cmbActionType.setValue(defaults['actionTypeId'])
        orgStructureId = defaults['orgStructureId']
        self.cmbOrgStructure.setValue(orgStructureId if orgStructureId else QtGui.qApp.currentOrgStructureId())
        self.cmbNomenclature.setValue(defaults['nomenclatureId'])
        self.cmbNomenclature.getFilterData()
        self.cmbNomenclature.setFilter(self.cmbNomenclature._filter)
        self.edtBegDate.setDate(defaults['begDate'])
        self.edtEndDate.setDate(defaults['endDate'])
        self.edtYear.setValue(defaults['year'])
        self.cmbMonth.setCurrentIndex(defaults['month'])
        self.chkPeriod.setChecked(defaults['period'])
        self.chkActual.setChecked(defaults['actual'])
        self.chkIgnoreTime.setChecked(defaults['ignoreTime'])
        self.chkCurrentEvent.setChecked(defaults['currentEvent'])

        self._eventEditor = eventEditor
        self._fromEventEditor = fromEventEditor

        self.setWindowTitle(u'Назначение ЛС')

        self.setModels(
            self.tblNomenclatureExpense,
            self.modelNomenclatureExpense,
            self.selectionModelNomenclatureExpense
        )
        self.setModels(
            self.tblNomenclatureExpenseDays,
            self.modelNomenclatureExpense,
            self.selectionModelNomenclatureExpenseDays
        )
        self.tblNomenclatureExpenseDays.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblNomenclatureExpenseDays.addEditDay()
        self.tblNomenclatureExpenseDays.addCopyDay()
        self.tblNomenclatureExpenseDays.addPasteDay()
        self.tblNomenclatureExpenseDays.addDeleteDays()
        self.modelNomenclatureExpense.setIgnoreTime(self.chkIgnoreTime.isChecked())

        self._hideDaysColumns(self.tblNomenclatureExpense)
        self._hideMainColumns(self.tblNomenclatureExpenseDays)

        self._cmbActionTypeWidgetsDependets = [
            self.cmbNomenclature, self.chkPeriod, self.chkActual, self.chkIgnoreTime, self.chkCurrentEvent, self.edtYear, self.cmbMonth,
            self.lblNomenclature, self.lblYear, self.lblMonth
        ]

        self.chkCurrentEvent.setVisible(False)

        self.addObject('mnuNomenclatureExpense', QtGui.QMenu(self))
        self.addObject('actDeleteRows', QtGui.QAction(u'Удалить назначение', self))
        self.connect(self.actDeleteRows, SIGNAL('triggered()'), self.on_actDeleteRows_triggered)
        self.addObject('actExtendAppointmentNomenclature', QtGui.QAction(u'Продлить назначение', self))
        self.connect(self.actExtendAppointmentNomenclature, SIGNAL('triggered()'), self.on_extendAppointmentNomenclature)

        self.tblNomenclatureExpense.setNomenclatureExpensePopupMenu(self.mnuNomenclatureExpense)
        self.mnuNomenclatureExpense.addActions([self.actDeleteRows, self.actExtendAppointmentNomenclature])

        self.connect(self.cmbActionType, SIGNAL('currentIndexChanged(int)'), self.on_cmbActionTypeIndexChanged)
        self.connect(self.cmbNomenclature, SIGNAL('currentIndexChanged(int)'), self.on_cmbNomenclatureIndexChanged)
        self.connect(self.cmbMonth, SIGNAL('currentIndexChanged(int)'), self.on_cmbMonthIndexChanged)
        self.connect(self.edtYear, SIGNAL('valueChanged(int)'), self.on_edtYearValueChanged)
        self.connect(self.chkActual, SIGNAL('clicked(bool)'), self.on_chkActualClicked)
        self.connect(self.chkIgnoreTime, SIGNAL('clicked(bool)'), self.on_chkIgnoreTimeClicked)
        self.connect(self.chkPeriod, SIGNAL('clicked(bool)'), self.on_chkPeriodClicked)

        self.connect(
            self.selectionModelNomenclatureExpense,
            SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
            self.on_nomenclatureExpenseSelectionChanged
        )

        self.connect(
            self.selectionModelNomenclatureExpenseDays,
            SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
            self.on_nomenclatureExpenseDaysSelectionChanged
        )

        self.on_cmbActionTypeIndexChanged()
        self.on_cmbNomenclatureIndexChanged()
        self.on_cmbMonthIndexChanged(self.cmbMonth.currentIndex())
        self.on_edtYearValueChanged(self.edtYear.value())
        self.on_chkActualClicked(self.chkActual.isChecked())
        self.on_chkIgnoreTimeClicked(self.chkIgnoreTime.isChecked())
        self.on_chkPeriodClicked()
        self.on_edtBegDate_dateChanged(self.edtBegDate.date())
        self.on_edtEndDate_dateChanged(self.edtEndDate.date())

        self.groups = groups
        self.groupsDeleted = []
        self.modelNomenclatureExpense.setOriginGroups(self.groups)

        self.tblNomenclatureExpense.enableColsHide()
        self.tblNomenclatureExpense.enableColsMove()
        self.tblNomenclatureExpenseDays.enableColsHide()
        self.tblNomenclatureExpenseDays.enableColsMove()


    def on_actDeleteRows_triggered(self):
        for index in self.tblNomenclatureExpense.selectedIndexes():
            if index.row() <= len(self.modelNomenclatureExpense.groups()):
                headAciton = self.modelNomenclatureExpense.groups()[index.row()].headItem.action
                if forceInt(headAciton._record.value('id')):
                    res = QtGui.QMessageBox.warning( self,
                        u'Внимание!',
                        u'Данное назначение можно только отменить. Отменить назначение?',
                        QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                        QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Ok:
                        items = self.modelNomenclatureExpense.groups()[index.row()].items
                        for i in range(len(items)):
                            if forceInt(items[i].action._record.value('status')) !=2:
                                items[i].action._record.setValue('status', toVariant(CActionStatus.canceled))
                                items[i].action.cancel()
                        self.modelNomenclatureExpense.setOriginGroups(self.modelNomenclatureExpense._originGroups)
                        self.modelNomenclatureExpense.emitAllDataChanged()
                    else:
                        return False
                else:
                    group = self.modelNomenclatureExpense.groups()[index.row()]
                    self.removeNewGroupRows(index.row(), self.modelNomenclatureExpense.rowCount()-1,  group)
                    self.modelNomenclatureExpense.emitAllDataChanged()


    def on_extendAppointmentNomenclature(self):
        dialog = CExtendAppointmentNomenclatureDialog(self)
        try:
            if dialog.exec_():
                extendParametrs = dialog.getExtendParametrs()
                quantityDay = forceInt(extendParametrs.get('quantityDay', 0))
                skipAfterLastDayCourse = forceInt(extendParametrs.get('skipAfterLastDayCourse', 0))
                isLastDayCourse = forceBool(extendParametrs.get('isLastDayCourse', False))
                index = self.tblNomenclatureExpense.currentIndex()
                if index.isValid() and quantityDay > 0:
                    self.tblNomenclatureExpense.model().setDurationForDayIndex(index, quantityDay, skipAfterLastDayCourse=skipAfterLastDayCourse, isLastDayCourse=isLastDayCourse)
                    self.tblNomenclatureExpense.model().reset()
        finally:
            dialog.deleteLater()


    def removeNewGroupRows(self, row, count, group, parentIndex = QModelIndex()):
        self.modelNomenclatureExpense.beginRemoveRows(parentIndex, row, count)
        if group in self.modelNomenclatureExpense._newGroups:
            groupRow = self.modelNomenclatureExpense._newGroups.index(group)
            if groupRow >= 0 and groupRow < len(self.modelNomenclatureExpense._newGroups):
                del self.modelNomenclatureExpense._newGroups[groupRow]
                if group not in self.groupsDeleted:
                    self.groupsDeleted.append(group)
        if group in self.modelNomenclatureExpense._groups:
            groupRow = self.modelNomenclatureExpense._groups.index(group)
            if groupRow >= 0 and groupRow < len(self.modelNomenclatureExpense.groups()):
                del self.modelNomenclatureExpense._groups[groupRow]
                if group not in self.groupsDeleted:
                    self.groupsDeleted.append(group)
        if group in self.modelNomenclatureExpense._originGroups:
            groupRow = self.modelNomenclatureExpense._originGroups.index(group)
            if groupRow >= 0 and groupRow < len(self.modelNomenclatureExpense._originGroups):
                del self.modelNomenclatureExpense._originGroups[groupRow]
                if group not in self.groupsDeleted:
                    self.groupsDeleted.append(group)
        self.modelNomenclatureExpense.endRemoveRows()
        self.modelNomenclatureExpense.setOriginGroups(self.modelNomenclatureExpense._groups)


    def getOrgStructureId(self):
        return self.cmbOrgStructure.value()


    def on_chkPeriodClicked(self, v=None):
        self.modelNomenclatureExpense.considerPeriod(self.chkPeriod.isChecked())


    @pyqtSignature('')
    def on_btnReset_pressed(self):
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbNomenclature.setValue(None)
        self.chkPeriod.setChecked(False)
        self.chkActual.setChecked(True)
        self.chkIgnoreTime.setChecked(True)
        currentDate = QtCore.QDate.currentDate()
        self.edtYear.setValue(currentDate.year())
        self.cmbMonth.setCurrentIndex(currentDate.month()-1)


    @pyqtSignature('')
    def on_btnSaveTemplate_pressed(self):
        actionTypeId = self.cmbActionType.value()
        if actionTypeId:
            db = QtGui.qApp.db
            tableAT = db.table('ActionType')
            recordAT = db.getRecordEx(tableAT, [tableAT['class']], [tableAT['id'].eq(actionTypeId), tableAT['deleted'].eq(0)])
            if recordAT:
                dlg = CTemplateEditor(self, forceInt(recordAT.value('class')), isOffset=True)
                if dlg.exec_():
                    db.transaction()
                    try:
                        groupsList = []
                        actionTypeGroupId = dlg.itemId()
                        table = db.table('ActionTypeGroup_Item')
                        model = self.tblNomenclatureExpense.model()
                        for index in self.tblNomenclatureExpense.selectedIndexes():
                            row = index.row()
                            if 0 <= row < len(model._groups):
                                groupsList.append(model._groups[row])
                        groupsList.sort(key=lambda x: forceDate(x.headItem.action.getRecord().value('begDate')))
                        offsetDate = forceDate(groupsList[0].headItem.action.getRecord().value('begDate')) if len(groupsList) > 0 else None
                        isOffset = dlg.chkOffset.isChecked()
                        for groups in groupsList:
                            action = groups.headItem.action
                            record = action.getRecord()
                            if action:
                                nomenclatureId = self.modelNomenclatureExpense._cellsSettings.getGroupNomenclature(groups)
                                if nomenclatureId:
                                    begDate = forceDate(record.value('begDate'))
                                    offset = offsetDate.daysTo(begDate) if (isOffset and offsetDate) else 0
                                    newRecord = table.newRecord()
                                    newRecord.setValue('master_id', actionTypeGroupId)
                                    newRecord.setValue('actionType_id', actionTypeId)
                                    newRecord.setValue('orgStructure_id', toVariant(self.cmbOrgStructure.value()))
                                    propertyType = self.modelNomenclatureExpense._cellsSettings.getGroupNomenclaturePT(groups)
                                    if propertyType and propertyType.inActionsSelectionTable == _RECIPE:
                                        newRecord.setValue('nomenclature_id', toVariant(nomenclatureId))
                                    propertyType = self.modelNomenclatureExpense._cellsSettings.getGroupDosesPT(groups)
                                    if propertyType and propertyType.inActionsSelectionTable == _DOSES:
                                        newRecord.setValue('doses', toVariant(self.modelNomenclatureExpense._cellsSettings.getGroupDoses(groups)))
                                    propertyType = self.modelNomenclatureExpense._cellsSettings.getGroupSignaPT(groups)
                                    if propertyType and propertyType.inActionsSelectionTable == _SIGNA:
                                        newRecord.setValue('signa', toVariant(self.modelNomenclatureExpense._cellsSettings.getGroupSigna(groups)))
                                    newRecord.setValue('duration', toVariant(groups.duration()))
                                    newRecord.setValue('periodicity', toVariant(groups.periodicity()))
                                    newRecord.setValue('aliquoticity', toVariant(groups.aliquoticity()))
                                    newRecord.setValue('offset', toVariant(offset))
                                    actionTypeGroupItemId = db.insertRecord(table, newRecord)
                                    if actionTypeGroupItemId:
                                        items = groups._epGroup._executionPlan.items
                                        if items:
                                            tablePI = db.table('ActionTypeGroup_Plan_Item')
                                            tablePINomenclature = db.table('ActionTypeGroup_Plan_Item_Nomenclature')
                                            #for i in items: print i.id, i.idx, i.time, i.date, i.nomenclature.id, i.executedDatetime, i.nomenclature.dosage, i.nomenclature.actionExecutionPlanItemId
                                            for item in items:
                                                idx = item.idx
                                                time = item.time
                                                date = item.date
                                                dateIdx = (begDate.daysTo(item.date) + 1) if begDate != date else 1
                                                newRecordPI = tablePI.newRecord()
                                                newRecordPI.setValue('master_id', toVariant(actionTypeGroupItemId))
                                                newRecordPI.setValue('idx', toVariant(idx))
                                                newRecordPI.setValue('date_idx', toVariant(dateIdx))
                                                newRecordPI.setValue('time', toVariant(time))
                                                planItemId = db.insertRecord(tablePI, newRecordPI)
                                                if planItemId and item.nomenclature:
                                                    doses = item.nomenclature.dosage
                                                    nomenclatureId = item.nomenclature.nomenclatureId
                                                    newRecordPIN = tablePINomenclature.newRecord()
                                                    newRecordPIN.setValue('master_id', toVariant(planItemId))
                                                    newRecordPIN.setValue('nomenclature_id', toVariant(nomenclatureId))
                                                    newRecordPIN.setValue('dosage', toVariant(doses))
                                                    db.insertRecord(tablePINomenclature, newRecordPIN)
                    except:
                        db.rollback()
                        raise
                    else:
                        db.commit()
                dlg.deleteLater()


    @pyqtSignature('')
    def on_btnLoadTemplate_pressed(self):
        actionTypeId = self.cmbActionType.value()
        if actionTypeId:
            db = QtGui.qApp.db
            tableAT = db.table('ActionType')
            record = db.getRecordEx(tableAT, [tableAT['class']], [tableAT['id'].eq(actionTypeId), tableAT['deleted'].eq(0)])
            if record:
                dlg = CNomenclatureExpenseLoadTemplate(self, self._eventEditor, self._eventEditor.eventTypeId, forceInt(record.value('class')))
                dlg.setOrgStructureId(self.cmbOrgStructure.value())
                if dlg.exec_():
                    db.transaction()
                    try:
                        actions = dlg.getSelectedList()
                        for action in actions:
                            self.modelNomenclatureExpense._addNewGroupFromTemplate(action)
                    except:
                        db.rollback()
                        raise
                    else:
                        db.commit()
                dlg.deleteLater()


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.modelNomenclatureExpense.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.modelNomenclatureExpense.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbNomenclature.setOrgStructureId(orgStructureId)
        self.modelNomenclatureExpense.setOrgStructureId(orgStructureId)


    def on_nomenclatureExpenseSelectionChanged(self, i1, i2):
        self.selectionModelNomenclatureExpenseDays.clearSelection()


    def on_nomenclatureExpenseDaysSelectionChanged(self, i1, i2):
        self.selectionModelNomenclatureExpense.clearSelection()


    def _hideDaysColumns(self, tbl):
        header = tbl.horizontalHeader()
        start = tbl.model().lastMainIndex + 1
        self._hideHeaderColumns(header, start, header.count())


    def _hideMainColumns(self, tbl):
        header = tbl.horizontalHeader()
        stop = tbl.model().lastMainIndex + 1
        self._hideHeaderColumns(header, 0, stop)


    @staticmethod
    def _hideHeaderColumns(header, start, stop):
        for i in range(start, stop):
            header.setSectionHidden(i, True)


    @property
    def eventEditor(self):
        return self._eventEditor


    def setEventEditor(self, eventEditor):
        self._eventEditor = eventEditor
        self.modelNomenclatureExpense.setEventEditor(eventEditor)


    def on_chkActualClicked(self, value):
        self.modelNomenclatureExpense.setOnlyActual(value)


    def on_chkIgnoreTimeClicked(self, value):
        self.modelNomenclatureExpense.setIgnoreTime(value)


    def on_cmbMonthIndexChanged(self, monthIndex):
        month = monthIndex + 1
        year = self.edtYear.value()
        self._updateModelDate(year, month)
        self._hideDaysColumns(self.tblNomenclatureExpense)


    def on_edtYearValueChanged(self, year):
        month = self.cmbMonth.currentIndex()+1
        self._updateModelDate(year, month)
        self._hideDaysColumns(self.tblNomenclatureExpense)


    def _updateModelDate(self, year, month):
        date = QtCore.QDate(year, month, 1)
        date = QtCore.QDate(year, month, date.daysInMonth())
        self.modelNomenclatureExpense.setDate(date)


    def setCmbActionTypeFilter(self):
        db = QtGui.qApp.db
        table = db.table('ActionType')
        idList = getNomenclatureActionTypesIds()
        descendants = []
        for id in idList:
            descendants.extend(db.getDescendants(table, 'group_id', id))

        idList = db.getTheseAndParents(table, 'group_id', descendants)

        self.cmbActionType.setEnabledActionTypeIdList(idList)


    def exec_(self):
        return CDialogBase.exec_(self)


    def on_cmbNomenclatureIndexChanged(self, index=None):
        nomenclatureId = self.cmbNomenclature.value()
        self.modelNomenclatureExpense.setNomenclatureId(nomenclatureId)


    def on_cmbActionTypeIndexChanged(self, index=None):
        actionTypeId = self.cmbActionType.value()

        for wgt in self._cmbActionTypeWidgetsDependets:
            wgt.setEnabled(bool(actionTypeId))

        self.modelNomenclatureExpense.setActionTypeId(actionTypeId)

        self.chkPeriod.emit(SIGNAL('clicked(bool)'), self.chkPeriod.isChecked() and bool(actionTypeId))


    def done(self, result):
        defaults = {
            'actionTypeId': self.cmbActionType.value(),
            'nomenclatureId': self.cmbNomenclature.value(),
            'begDate': str(self.edtBegDate.date().toString('yyyy.MM.dd')),
            'endDate': str(self.edtEndDate.date().toString('yyyy.MM.dd')),
            'year': self.edtYear.value(),
            'month': self.cmbMonth.currentIndex(),
            'period': self.chkPeriod.isChecked(),
            'actual': self.chkActual.isChecked(),
            'ignoreTime': self.chkIgnoreTime.isChecked(),
            'currentEvent': self.chkCurrentEvent.isChecked(),
            'orgStructureId': self.cmbOrgStructure.value()
        }

        defaults = json.dumps(defaults)

        QtGui.qApp.preferences.appPrefs['NomenclatureExpenseDialogDefaultValues'] = defaults

        return CDialogBase.done(self, result)


    def checkDataEntered(self):
        result = True
        if QtGui.qApp.controlFillingFieldsNomenclatureExpense():
            for row, group in enumerate(self.modelNomenclatureExpense._groups):
                begDate = forceDate(group.begDate())
                directionDate = forceDate(group.directionDate())
                nomenclatureId = self.modelNomenclatureExpense._cellsSettings.getGroupNomenclature(group)
                doses = self.modelNomenclatureExpense._cellsSettings.getGroupDoses(group)
                duration = group.duration()
                aliquoticity = group.aliquoticity()
                result = result and (nomenclatureId or self.checkInputMessage(u'ЛС', False, self.tblNomenclatureExpense, row, NOMENCLATURE_INDEX))
                result = result and (doses or self.checkInputMessage(u'Дозу', False, self.tblNomenclatureExpense, row, DOSES_INDEX))
                result = result and (duration or self.checkInputMessage(u'Длительность', False, self.tblNomenclatureExpense, row, DURATION_INDEX))
                result = result and (aliquoticity or self.checkInputMessage(u'Кратность', False, self.tblNomenclatureExpense, row, ALIQUOTICITY_INDEX))
                result = result and (directionDate or self.checkInputMessage(u'Дату назначения', False, self.tblNomenclatureExpense, row, DIREACTION_DATE_INDEX))
                result = result and (begDate or self.checkInputMessage(u'Дату начала', False, self.tblNomenclatureExpense, row, BEG_DATE_INDEX))
                result = result and (begDate >= directionDate or self.checkValueMessage(u'"Дата начала" не может быть меньше "Даты назначения"!', False, self.tblNomenclatureExpense, row, BEG_DATE_INDEX))
        return result


    def saveData(self):
        if not self.checkDataEntered():
            return False
        if self._fromEventEditor:
            self._prepareGoupsToSave()
            self._addNewGroups()
            tabs = self._eventEditor.getActionsTabsList()
            for tab in tabs:
                for groupRemove in self.groupsDeleted:
                    mapItem2RowsGroupRemove = groupRemove._mapItem2Row
                    for actionRemove, rowRemove in mapItem2RowsGroupRemove.items():
                        groups = tab.modelAPActions._items._groups
                        for group in groups:
                            mapItem2Row = group._mapItem2Row
                            for action, row in mapItem2Row.items():
                                if actionRemove == action and rowRemove == row:
                                    if action.action and action.action.nomenclatureClientReservation:
                                        action.action.cancel()
                                    tab.modelAPActions.removeRows(row, 1)
            return True


    def discardData(self):
        if self._fromEventEditor:
            self.modelNomenclatureExpense.discardChanges()


    def getExecutionPlanIsDirty(self, action):
        if action:
            executionPlan = action.getExecutionPlan()
            if executionPlan:
                items = executionPlan.items
                for item in items:
                    if item.getIsDirty():
                        return True
        return False


    def _prepareGoupsToSave(self):
        for group in self.modelNomenclatureExpense.groupsToSavePrepare():
            group.prepareToSave()
            isDirty = False
            for row, item in enumerate(group.items):
                executionPlan = group._epGroup.getExecutionPlan()
                item.action.executionPlanManager.setExecutionPlan(executionPlan, force=True)
                item.action.executionPlanManager.setCurrentItemIndex(row)
                if item.action.executionPlanManager.hasItemsToDo():
                    item.action.updateDosageFromExecutionPlan()
                    item.action.updateSpecifiedName()
                    if self.getExecutionPlanIsDirty(item.action):
                        isDirty = True
                        executionPlan.updateQuantity()
                        #currentItemIndex = item.action.executionPlanManager.getCurrentItemIndex()
                        action = item.action.executionPlanManager.executionPlan.items[row].action
                        if action:
                            record = action.getRecord()
                            duration = forceInt(record.value('duration'))
                            item.action.setDuration(duration)
                            aliquoticity = forceInt(record.value('aliquoticity'))
                            item.action.setAliquoticity(aliquoticity)
                            quantity = forceInt(record.value('quantity'))
                            item.action.setQuantity(quantity)
                    financeId = item.action.getFinanceId()
                    medicalAidKindId = item.action.getMedicalAidKindId() if item.action.getMedicalAidKindId() else self.getMedicalAidKindId()
                    supplierId = self.cmbOrgStructure.value()
                    if item.action.nomenclatureClientReservation is not None and self.getExecutionPlanIsDirty(item.action):
                        item.action.cancel()
                        item.action.initNomenclatureReservation(self._eventEditor.clientId, financeId=financeId, medicalAidKindId=medicalAidKindId, supplierId=supplierId, markToUpdate=True)
            if isDirty:
                for row, item in enumerate(group.items):
                    item.action.executionPlanManager.setCurrentItemIndex(row)
                    currentItemIndex = item.action.executionPlanManager.getCurrentItemIndex()
                    action = item.action.executionPlanManager.executionPlan.items[currentItemIndex].action
                    if action:
                        record = action.getRecord()
                        duration = forceInt(record.value('duration'))
                        item.action.setDuration(duration)
                        aliquoticity = forceInt(record.value('aliquoticity'))
                        item.action.setAliquoticity(aliquoticity)
                        quantity = forceInt(record.value('quantity'))
                        item.action.setQuantity(quantity)


    def closeEvent(self, event):
        self.saveDialogPreferences()
        CDialogBase.closeEvent(self, event)


    def getMedicalAidKindId(self):
        return self.eventEditor.eventMedicalAidKindId


    def _addNewGroups(self):
        if self._fromEventEditor:
            tabs = self._eventEditor.getActionsTabsList()
            differClasses = len(tabs) > 1
            for group in self.modelNomenclatureExpense.groupsToAdd():
                action = group.headItem.action
                action.setOrgStructureId(self.cmbOrgStructure.value())
                action.executionPlanManager.setCurrentItemIndex(0)
                action.executionPlanManager.setCurrentItem(action.executionPlanManager.currentItem)
                if QtGui.qApp.controlSMFinance() == 0:
                    action.setFinanceId(None)
                financeId = action.getFinanceId()
                medicalAidKindId = action.getMedicalAidKindId() if action.getMedicalAidKindId() else self.getMedicalAidKindId()
                supplierId = self.cmbOrgStructure.value()
                if action.nomenclatureClientReservation is not None and self.getExecutionPlanIsDirty(action):
                    action.cancel()
                action.initNomenclatureReservation(self._eventEditor.clientId, financeId=financeId, medicalAidKindId=medicalAidKindId, supplierId=supplierId)
                if differClasses:
                    model = tabs[action.actionType().class_].modelAPActions
                else:
                    model = tabs[0].modelAPActions
                action.updateSpecifiedName()
                group.bindModel(model)
                model.addRow(action.actionType().id, presetAction=action)
                modelRow = len(model.items()) - 1
                group.bindFirstItemModelRow(modelRow)

            for tab in tabs:
                tab.onActionCurrentChanged()


class CExtendAppointmentNomenclatureDialog(CDialogBase, Ui_ExtendAppointmentNomenclatureDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setupDirtyCather()


    def getExtendParametrs(self):
        params = {}
        params['quantityDay'] = self.edtQuantityDay.value()
        params['skipAfterLastDayCourse'] = self.edtSkipAfterLastDayCourse.value()
        params['isLastDayCourse'] = self.chkLastDayCourse.isChecked()
        return params
