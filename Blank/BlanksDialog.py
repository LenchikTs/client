#!/usr/bin/env python
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
from PyQt4.QtCore import Qt, QDate, QModelIndex, QObject, pyqtSignature

from library.crbcombobox import CRBComboBox
from library.database import CSurrogateField
from library.DialogBase import CDialogBase
from library.InDocTable import CInDocTableModel, CDateInDocTableCol, CInDocTableCol, CIntInDocTableCol, CRBInDocTableCol
from library.TreeModel import CDBTreeModel
from library.Utils  import forceInt, forceRef, forceString, toVariant, variantEq, formatRecordsCount

from Blank.BlankItemsListDialog import CBlankModel
from Orgs.OrgStructureCol  import COrgStructureInDocTableCol
from Orgs.PersonComboBoxEx import CPersonFindInDocTableCol

from Blank.Ui_BlanksDialog  import Ui_BlanksDialog


class CBlanksDialog(CDialogBase, Ui_BlanksDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('BlankTypeTempInvalid', CBlankModel(self))
        self.addModels('BlankTypeTempInvalidEl', CBlankModel(self))
        filter = u'''(ActionType.id IN (SELECT DISTINCT AT.id
                FROM ActionType AS AT INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                WHERE AT.deleted = 0 AND APT.deleted = 0 AND APT.typeName = 'BlankSerialNumber')
                OR ActionType.id IN (SELECT DISTINCT AT.group_id
                FROM ActionType AS AT INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                WHERE AT.deleted = 0 AND APT.deleted = 0 AND APT.typeName = 'BlankSerialNumber')
                )'''
        self.addModels('BlankTypeActions', CDBTreeModel(self, 'ActionType', 'id', 'group_id', 'name', 'name', filter))
        self.modelBlankTypeActions.setLeavesVisible(True)
        self.addModels('BlankTempInvalidParty', CBlankTempInvalidPartyModel(self))
        self.addModels('BlankTempInvalidMoving', CBlankTempInvalidMovingModel(self))
        self.addModels('BlankTempInvalidPartyEl', CBlankTempInvalidPartyModelEl(self))
        self.addModels('BlankActionsParty', CBlankActionsPartyModel(self))
        self.addModels('BlankActionsMoving', CBlankActionsMovingModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.treeBlankTypeTempInvalid, self.modelBlankTypeTempInvalid, self.selectionModelBlankTypeTempInvalid)
        self.setModels(self.treeBlankTypeTempInvalidEl, self.modelBlankTypeTempInvalidEl, self.selectionModelBlankTypeTempInvalidEl)
        self.setModels(self.treeBlankTypeActions, self.modelBlankTypeActions, self.selectionModelBlankTypeActions)
        self.setModels(self.tblBlankTempInvalidParty,  self.modelBlankTempInvalidParty, self.selectionModelBlankTempInvalidParty)
        self.setModels(self.tblBlankTempInvalidPartyEl,  self.modelBlankTempInvalidPartyEl, self.selectionModelBlankTempInvalidPartyEl)
        self.setModels(self.tblBlankTempInvalidMoving,  self.modelBlankTempInvalidMoving, self.selectionModelBlankTempInvalidMoving)
        self.setModels(self.tblBlankActionsParty,  self.modelBlankActionsParty, self.selectionModelBlankActionsParty)
        self.setModels(self.tblBlankActionsMoving,  self.modelBlankActionsMoving, self.selectionModelBlankActionsMoving)
        self.tblBlankTempInvalidParty.addPopupDelRow()
        self.tblBlankTempInvalidMoving.addPopupDelRow()
        self.tblBlankActionsParty.addPopupDelRow()
        self.tblBlankActionsMoving.addPopupDelRow()
        self.treeBlankTypeTempInvalid.header().hide()
        self.treeBlankTypeTempInvalidEl.header().hide()
        self.treeBlankTypeActions.header().hide()
        self.resetFilterTempInvalidEl()
        self.resetFilterTempInvalid()
        self.resetFilterActions()
        self.treeBlankTypeTempInvalid.expand(self.modelBlankTypeTempInvalid.index(0, 0))
        self.treeBlankTypeTempInvalid.setCurrentIndex(self.modelBlankTypeTempInvalid.index(0, 0))
        self.treeBlankTypeTempInvalidEl.expand(self.modelBlankTypeTempInvalidEl.index(0, 0))
        self.treeBlankTypeTempInvalidEl.setCurrentIndex(self.modelBlankTypeTempInvalidEl.index(0, 0))


    @pyqtSignature('int')
    def on_tabTempInvalidTypeELN_currentChanged(self, widgetIndex):
        if widgetIndex == 0:
            self.treeBlankTypeTempInvalid.expand(self.modelBlankTypeTempInvalid.index(0, 0))
            self.treeBlankTypeTempInvalid.setCurrentIndex(self.modelBlankTypeTempInvalid.index(0, 0))
        else:
            self.treeBlankTypeTempInvalidEl.expand(self.modelBlankTypeTempInvalidEl.index(0, 0))
            self.treeBlankTypeTempInvalidEl.setCurrentIndex(self.modelBlankTypeTempInvalidEl.index(0, 0))


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, widgetIndex):
        if widgetIndex == 0:
            tempInvalidTypeIndex = self.tabTempInvalidTypeELN.currentIndex()
            if tempInvalidTypeIndex:
                self.treeBlankTypeTempInvalid.expand(self.modelBlankTypeTempInvalid.index(0, 0))
                self.treeBlankTypeTempInvalid.setCurrentIndex(self.modelBlankTypeTempInvalid.index(0, 0))
            else:
                self.treeBlankTypeTempInvalidEl.expand(self.modelBlankTypeTempInvalidEl.index(0, 0))
                self.treeBlankTypeTempInvalidEl.setCurrentIndex(self.modelBlankTypeTempInvalidEl.index(0, 0))
        else:
            self.treeBlankTypeActions.expand(self.modelBlankTypeActions.index(0, 0))
            self.treeBlankTypeActions.setCurrentIndex(self.modelBlankTypeActions.index(0, 0))


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelBlankTypeTempInvalidEl_currentChanged(self, current, previous):
        treeDocTypeIdList = self.getTempInvalidDocTypeIdEl()
        if treeDocTypeIdList:
            self.modelBlankTempInvalidPartyEl.cols()[0].setFilter(treeDocTypeIdList)
        db = QtGui.qApp.db
        tableRBBlankTempInvalids = db.table('rbBlankTempInvalids')
        tableBlankTempInvalidParty = db.table('BlankTempInvalid_Party')
        table = tableBlankTempInvalidParty.innerJoin(tableRBBlankTempInvalids, tableBlankTempInvalidParty['doctype_id'].eq(tableRBBlankTempInvalids['id']))
        doctypeIdList = db.getDistinctIdList(table, [tableBlankTempInvalidParty['id']], [tableRBBlankTempInvalids['doctype_id'].inlist(treeDocTypeIdList), tableBlankTempInvalidParty['deleted'].eq(0), tableBlankTempInvalidParty['isElectronic'].eq(1)])
        filterParty = self.getFilterTempInvalidParamsEl()
        self.modelBlankTempInvalidPartyEl.loadPartyItems(doctypeIdList, filterParty)
        self.tblBlankTempInvalidPartyEl.setFocus(Qt.TabFocusReason)
        self.lblCountRecordsEl.setText(formatRecordsCount(self.modelBlankTempInvalidPartyEl.rowCount()-1))


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelBlankTypeTempInvalid_currentChanged(self, current, previous):
        QtGui.qApp.callWithWaitCursor(self, self.saveItemsPrevious, self.tblBlankTempInvalidParty.currentIndex(), self.modelBlankTempInvalidParty, self.modelBlankTempInvalidMoving)
        treeDocTypeIdList = self.getTempInvalidDocTypeId()
        if treeDocTypeIdList:
            self.modelBlankTempInvalidParty.cols()[0].setFilter(treeDocTypeIdList)
        db = QtGui.qApp.db
        tableRBBlankTempInvalids = db.table('rbBlankTempInvalids')
        tableBlankTempInvalidParty = db.table('BlankTempInvalid_Party')
        table = tableBlankTempInvalidParty.innerJoin(tableRBBlankTempInvalids, tableBlankTempInvalidParty['doctype_id'].eq(tableRBBlankTempInvalids['id']))
        doctypeIdList = db.getDistinctIdList(table, [tableBlankTempInvalidParty['id']], [tableRBBlankTempInvalids['doctype_id'].inlist(treeDocTypeIdList), tableBlankTempInvalidParty['deleted'].eq(0), tableBlankTempInvalidParty['isElectronic'].eq(0)])
        filterParty, filterMoving = self.getFilterTempInvalidParams()
        self.modelBlankTempInvalidParty.loadPartyItems(doctypeIdList, filterParty)
        self.tblBlankTempInvalidParty.setFocus(Qt.TabFocusReason)
        self.setItemsBlankTempInvalidMoving(filterMoving)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelBlankTempInvalidParty_currentChanged(self, current, previous):
        QtGui.qApp.callWithWaitCursor(self, self.saveItemsPrevious, previous, self.modelBlankTempInvalidParty, self.modelBlankTempInvalidMoving)
        filterParty, filterMoving = self.getFilterTempInvalidParams()
        QtGui.qApp.callWithWaitCursor(self, self.setItemsBlankTempInvalidMoving, filterMoving)


    def setItemsBlankTempInvalidMoving(self, filterMoving):
        blankPartyId = self.getBlankPartyId(self.tblBlankTempInvalidParty, self.modelBlankTempInvalidParty)
        self.modelBlankTempInvalidMoving.loadSubPartyItems(blankPartyId, filterMoving)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelBlankTypeActions_currentChanged(self, current, previous):
        QtGui.qApp.callWithWaitCursor(self, self.saveItemsPrevious, self.tblBlankActionsParty.currentIndex(), self.modelBlankActionsParty, self.modelBlankActionsMoving)
        treeDocTypeIdList = self.getActionsDocTypeId()
        if treeDocTypeIdList:
            self.modelBlankActionsParty.cols()[0].setFilter(treeDocTypeIdList)
        db = QtGui.qApp.db
        tableRBBlankActions = db.table('rbBlankActions')
        tableBlankActionsParty = db.table('BlankActions_Party')
        table = tableBlankActionsParty.innerJoin(tableRBBlankActions, tableBlankActionsParty['doctype_id'].eq(tableRBBlankActions['id']))
        doctypeIdList = db.getDistinctIdList(table, [tableBlankActionsParty['id']], [tableRBBlankActions['doctype_id'].inlist(treeDocTypeIdList), tableBlankActionsParty['deleted'].eq(0)])
        filterParty, filterMoving = self.getFilterActionsParams()
        self.modelBlankActionsParty.loadPartyItems(doctypeIdList, filterParty)
        self.tblBlankActionsParty.setFocus(Qt.TabFocusReason)
        self.setItemsBlankActionsMoving(filterMoving)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelBlankActionsParty_currentChanged(self, current, previous):
        QtGui.qApp.callWithWaitCursor(self, self.saveItemsPrevious, previous, self.modelBlankActionsParty, self.modelBlankActionsMoving)
        filterParty, filterMoving = self.getFilterActionsParams()
        self.setItemsBlankActionsMoving(filterMoving)


    def setItemsBlankActionsMoving(self, filterMoving):
        blankPartyId = self.getBlankPartyId(self.tblBlankActionsParty, self.modelBlankActionsParty)
        self.modelBlankActionsMoving.loadSubPartyItems(blankPartyId, filterMoving)


    def saveItemsPrevious(self, previous, modelParty, modelMoving):
        if previous.isValid():
            modelParty.savePartyItems()
            previousRow = previous.row()
            items = modelParty.items()
            if len(items) > previousRow:
                record = items[previousRow]
                previousBlankPartyId = forceRef(record.value('id'))
                if previousBlankPartyId:
                    modelMoving.saveItems(previousBlankPartyId)


    def updateTempInvalidBlankParty(self):
        received = 0
        used = 0
        returnAmount = 0
        for item in self.modelBlankTempInvalidMoving.items():
            received += forceInt(item.value('received'))
            used += forceInt(item.value('used'))
            returnAmount += forceInt(item.value('returnAmount'))
        currentIndex = self.tblBlankTempInvalidParty.currentIndex()
        if currentIndex.isValid():
            currentRow = currentIndex.row()
            itemsParty = self.modelBlankTempInvalidParty.items()
            record = itemsParty[currentRow]
            amountBlank = forceInt(record.value('amount'))
            writingBlank = forceInt(record.value('writing'))
            record.setValue('extradited', toVariant(received))
            record.setValue('used', toVariant(used))
            record.setValue('returnBlank', toVariant(returnAmount))
            record.setValue('balance', toVariant(amountBlank - received - writingBlank + returnAmount))
            itemsParty[currentRow] = record
            self.modelBlankTempInvalidParty.setItems(itemsParty)
            self.modelBlankTempInvalidParty.emitRowChanged(currentRow)


    def updateActionsBlankParty(self):
        received = 0
        used = 0
        returnAmount = 0
        for item in self.modelBlankActionsMoving.items():
            received += forceInt(item.value('received'))
            used += forceInt(item.value('used'))
            returnAmount += forceInt(item.value('returnAmount'))
        currentIndex = self.tblBlankActionsParty.currentIndex()
        if currentIndex.isValid():
            currentRow = currentIndex.row()
            itemsParty = self.modelBlankActionsParty.items()
            record = itemsParty[currentRow]
            amountBlank = forceInt(record.value('amount'))
            writingBlank = forceInt(record.value('writing'))
            record.setValue('extradited', toVariant(received))
            record.setValue('used', toVariant(used))
            record.setValue('returnBlank', toVariant(returnAmount))
            record.setValue('balance', toVariant(amountBlank - received -writingBlank + returnAmount))
            itemsParty[currentRow] = record
            self.modelBlankActionsParty.setItems(itemsParty)
            self.modelBlankActionsParty.emitRowChanged(currentRow)


    def getTempInvalidDocTypeId(self):
        return self.modelBlankTypeTempInvalid.getItemIdList(self.treeBlankTypeTempInvalid.currentIndex())


    def getTempInvalidDocTypeIdEl(self):
        return self.modelBlankTypeTempInvalidEl.getItemIdList(self.treeBlankTypeTempInvalidEl.currentIndex())


    def getActionsDocTypeId(self):
        return self.modelBlankTypeActions.getItemIdList(self.treeBlankTypeActions.currentIndex())


    def getBlankPartyId(self, table, model):
        currentIndex = table.currentIndex()
        if currentIndex.isValid():
            currentRow = currentIndex.row()
            items = model.items()
            if len(items) > currentRow:
                record = items[currentRow]
                blankPartyId = forceRef(record.value('id'))
                return blankPartyId
        return None


    def saveData(self):
        if not self.checkIntervalNumbers(self.tblBlankTempInvalidParty, self.tblBlankTempInvalidMoving, self.modelBlankTempInvalidParty, self.modelBlankTempInvalidMoving):
            return False
        if not self.checkIntervalNumbers(self.tblBlankActionsParty, self.tblBlankActionsMoving, self.modelBlankActionsParty, self.modelBlankActionsMoving):
            return False
        QtGui.qApp.callWithWaitCursor(self, self.saveBlankTempInvalid)
        QtGui.qApp.callWithWaitCursor(self, self.saveBlankActions)
        return True


    def saveBlankTempInvalid(self):
        self.modelBlankTempInvalidParty.savePartyItems()
        blankPartyId = self.getBlankPartyId(self.tblBlankTempInvalidParty, self.modelBlankTempInvalidParty)
        if blankPartyId:
            self.modelBlankTempInvalidMoving.saveItems(blankPartyId)


    def saveBlankActions(self):
        self.modelBlankActionsParty.savePartyItems()
        blankPartyId = self.getBlankPartyId(self.tblBlankActionsParty, self.modelBlankActionsParty)
        if blankPartyId:
            self.modelBlankActionsMoving.saveItems(blankPartyId)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxFilterEl_clicked(self, button):
        buttonCode = self.buttonBoxFilterEl.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.applyFilterTempInvalidEl()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilterTempInvalidEl()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxFilter_clicked(self, button):
        buttonCode = self.buttonBoxFilter.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.applyFilterTempInvalid()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilterTempInvalid()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxFilterActions_clicked(self, button):
        buttonCode = self.buttonBoxFilterActions.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.applyFilterActions()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilterActions()


    def getFilterTempInvalidParamsEl(self):
        filterParty = []
        db = QtGui.qApp.db
        table = db.table('BlankTempInvalid_Party')
        # tableMoving = db.table('BlankTempInvalid_Moving')
        personId = self.cmbPersonPartyEl.value()
        if personId:
            filterParty.append(table['person_id'].eq(personId))
        begDate = self.edtBegDatePartyEl.date()
        if begDate:
            filterParty.append(table['date'].ge(begDate))
        endDate = self.edtEndDatePartyEl.date()
        if endDate:
            filterParty.append(table['date'].le(endDate))
        serial = self.edtSerialPartyEl.text()
        if serial:
            filterParty.append(table['serial'].eq(serial))
        numberTo = self.edtNumberToEl.value()
        if numberTo:
            numberFrom = self.edtNumberFromEl.value()
            filterParty.append(db.joinAnd([table['numberFrom'].ge(numberFrom), table['numberTo'].le(numberTo)]))
        if self.chkFreeEl.isChecked() and not self.chkExtraditedEl.isChecked():
            filterParty.append(table['extradited'].eq(0))
        if self.chkExtraditedEl.isChecked() and not self.chkFreeEl.isChecked():
            filterParty.append(table['extradited'].eq(1))
        return filterParty


    def getFilterTempInvalidParams(self):
        filterParty = []
        filterMoving = []
        db = QtGui.qApp.db
        table = db.table('BlankTempInvalid_Party')
        tableMoving = db.table('BlankTempInvalid_Moving')
        personId = self.cmbPersonParty.value()
        if personId:
            filterParty.append(table['person_id'].eq(personId))
        begDate = self.edtBegDateParty.date()
        if begDate:
            filterParty.append(table['date'].ge(begDate))
        endDate = self.edtEndDateParty.date()
        if endDate:
            filterParty.append(table['date'].le(endDate))
        serial = self.edtSerialParty.text()
        if serial:
            filterParty.append(table['serial'].eq(serial))
        numberTo = self.edtNumberTo.value()
        if numberTo:
            numberFrom = self.edtNumberFrom.value()
            filterParty.append(db.joinAnd([table['numberFrom'].ge(numberFrom), table['numberTo'].le(numberTo)]))
        orgStructureId = self.cmbOrgStructureSubParty.value()
        if orgStructureId:
            filterMoving.append(tableMoving['orgStructure_id'].eq(orgStructureId))
        personId = self.cmbPersonSubParty.value()
        if personId:
            filterMoving.append(tableMoving['person_id'].eq(personId))
        begDate = self.edtBegDateSubParty.date()
        if begDate:
            filterMoving.append(tableMoving['date'].ge(begDate))
        endDate = self.edtEndDateSubParty.date()
        if endDate:
            filterMoving.append(tableMoving['date'].le(endDate))
        return filterParty, filterMoving


    def getFilterActionsParams(self):
        filterParty = []
        filterMoving = []
        db = QtGui.qApp.db
        table = db.table('BlankActions_Party')
        tableMoving = db.table('BlankActions_Moving')
        personId = self.cmbPersonPartyActions.value()
        if personId:
            filterParty.append(table['person_id'].eq(personId))
        begDate = self.edtBegDatePartyActions.date()
        if begDate:
            filterParty.append(table['date'].ge(begDate))
        endDate = self.edtEndDatePartyActions.date()
        if endDate:
            filterParty.append(table['date'].le(endDate))
        serial = self.edtSerialPartyActions.text()
        if serial:
            filterParty.append(table['serial'].eq(serial))
        numberTo = self.edtNumberToActions.value()
        if numberTo:
            numberFrom = self.edtNumberFromActions.value()
            filterParty.append(db.joinAnd([table['numberFrom'].ge(numberFrom), table['numberTo'].le(numberTo)]))
        orgStructureId = self.cmbOrgStructureSubPartyActions.value()
        if orgStructureId:
            filterMoving.append(tableMoving['orgStructure_id'].eq(orgStructureId))
        personId = self.cmbPersonSubPartyActions.value()
        if personId:
            filterMoving.append(tableMoving['person_id'].eq(personId))
        begDate = self.edtBegDateSubPartyActions.date()
        if begDate:
            filterMoving.append(tableMoving['date'].ge(begDate))
        endDate = self.edtEndDateSubPartyActions.date()
        if endDate:
            filterMoving.append(tableMoving['date'].le(endDate))
        return filterParty, filterMoving


    def applyFilterTempInvalidEl(self):
        self.on_selectionModelBlankTypeTempInvalidEl_currentChanged(QModelIndex(), QModelIndex())


    def applyFilterTempInvalid(self):
        self.on_selectionModelBlankTypeTempInvalid_currentChanged(QModelIndex(), QModelIndex())


    def applyFilterActions(self):
        self.on_selectionModelBlankTypeActions_currentChanged(QModelIndex(), QModelIndex())


    def resetFilterTempInvalidEl(self):
        self.cmbPersonPartyEl.setValue(None)
        currentDate = QDate.currentDate()
        self.edtBegDatePartyEl.setDate(QDate(currentDate.year(), 1, 1))
        self.edtEndDatePartyEl.setDate(currentDate)
        self.edtSerialPartyEl.setText(u'')
        self.edtNumberToEl.setValue(0)
        self.edtNumberFromEl.setValue(0)
        self.chkFreeEl.setChecked(True)
        self.chkExtraditedEl.setChecked(False)
        self.applyFilterTempInvalidEl()


    def resetFilterTempInvalid(self):
        self.cmbPersonParty.setValue(None)
        currentDate = QDate.currentDate()
        self.edtBegDateParty.setDate(QDate(currentDate.year(), 1, 1))
        self.edtEndDateParty.setDate(currentDate)
        self.edtSerialParty.setText(u'')
        self.edtNumberTo.setValue(0)
        self.edtNumberFrom.setValue(0)
        self.cmbOrgStructureSubParty.setValue(None)
        self.cmbPersonSubParty.setValue(None)
        self.edtBegDateSubParty.setDate(QDate(currentDate.year(), 1, 1))
        self.edtEndDateSubParty.setDate(currentDate)
        self.applyFilterTempInvalid()


    def resetFilterActions(self):
        self.cmbPersonPartyActions.setValue(None)
        currentDate = QDate.currentDate()
        self.edtBegDatePartyActions.setDate(QDate(currentDate.year(), 1, 1))
        self.edtEndDatePartyActions.setDate(currentDate)
        self.edtSerialPartyActions.setText(u'')
        self.edtNumberToActions.setValue(0)
        self.edtNumberFromActions.setValue(0)
        self.cmbOrgStructureSubPartyActions.setValue(None)
        self.cmbPersonSubPartyActions.setValue(None)
        self.edtBegDateSubPartyActions.setDate(QDate(currentDate.year(), 1, 1))
        self.edtEndDateSubPartyActions.setDate(currentDate)
        self.applyFilterActions()


    def checkIntervalNumbers(self, table, tableMoving, model, modelMoving):
        for rowItem, record in enumerate(modelMoving.items()):
            if record:
                numberFrom = forceInt(record.value('numberFrom'))
                numberTo = forceInt(record.value('numberTo'))
                if not self.checkIntervalNumber(numberFrom, rowItem, record.indexOf('numberFrom'), table, tableMoving, model):
                    return False
                if not self.checkIntervalNumber(numberTo, rowItem, record.indexOf('numberTo'), table, tableMoving, model):
                    return False
        return True


    def checkIntervalNumber(self, number, rowItem, column, table, tableMoving, model):
        currentIndex = table.currentIndex()
        if currentIndex.isValid():
            currentRow = currentIndex.row()
            itemsParty = model.items()
            if itemsParty and len(itemsParty) < currentRow:
                record = itemsParty[currentRow]
                if record:
                    numberFrom = forceInt(record.value('numberFrom'))
                    numberTo = forceInt(record.value('numberTo'))
                    if not number or number < numberFrom or number > numberTo:
                        return self.checkValueMessage(u'Номер %s не попадает в диапазон %s-%s'% (forceString(number), forceString(numberFrom), forceString(numberTo)), False, tableMoving, rowItem, column)
        return True


    def checkDoubleNumber(self, number, row, column, table, model):
        if number:
            for rowItem, record in enumerate(model.items()):
                if rowItem != row and record:
                    numberFrom = forceInt(record.value('numberFrom'))
                    numberTo = forceInt(record.value('numberTo'))
                    if not number or number == numberFrom or number == numberTo:
                        return self.checkValueMessage(u'Номер %s дублируется'% (forceString(number)), False, table, row, column)
        return True


    def checkReturnBlank(self, row, column, table, model):
        items = model.items()
        record = items[row]
        if record:
            returnAmount = forceInt(record.value('returnAmount'))
            if returnAmount:
                self.checkValueMessage(u'Из подпартии был возврат', False, table, row, column)


class CAmountIntInDocTableCol(CIntInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CIntInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.low = params.get('low', 0)
        self.high = params.get('high', 10000)


class CRBInvalDocTypeInDocTableCol(CRBInDocTableCol):
    def setFilter(self, doctypeIdList):
        self.filter = u'rbBlankTempInvalids.doctype_id IN (%s)'%(','.join(str(doctypeId) for doctypeId in doctypeIdList))


class CRBActionDocTypeInDocTableCol(CRBInDocTableCol):
    def setFilter(self, doctypeIdList):
        self.filter = u'rbBlankActions.doctype_id IN (%s)'%(','.join(str(doctypeId) for doctypeId in doctypeIdList))


class CBlankPartyInDocTableModel(CInDocTableModel):
    def removeRows(self, row, count, parentIndex = QModelIndex()):
        if 0<=row and row+count<=len(self._items):
            self.beginRemoveRows(parentIndex, row, row+count-1)
            item = self._items[row]
            self.deletedIdList.append(forceRef(item.value('id')))
            del self._items[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def savePartyItems(self):
        if self._items is not None:
            db = QtGui.qApp.db
            table = self._table
            idFieldName = self._idFieldName
            for idx, record in enumerate(self._items):
                if self._idxFieldName:
                    record.setValue(self._idxFieldName, toVariant(idx))
                if self._extColsPresent:
                    outRecord = self.removeExtCols(record)
                else:
                    outRecord = record
                id = db.insertOrUpdate(table, outRecord)
                record.setValue(idFieldName, toVariant(id))
            if self.deletedIdList:
                filter = [table[idFieldName].inlist(self.deletedIdList)]
                if self._filter:
                    filter.append(self._filter)
                    db.markRecordsDeleted(table, filter)


    def loadPartyItems(self, masterIdList, filter = []):
        db = QtGui.qApp.db
        cols = []
        for col in self._cols:
            if not col.external():
                cols.append(col.fieldName())
        cols.append(self._idFieldName)
        if self._idxFieldName:
            cols.append(self._idxFieldName)
        for col in self._hiddenCols:
            cols.append(col)
        table = self._table
        filter.append(table[self._idFieldName].inlist(masterIdList))
        if self._filter:
            filter.append(self._filter)
        if table.hasField('deleted'):
            filter.append(table['deleted'].eq(0))
        if self._idxFieldName:
            order = [self._idxFieldName, self._idFieldName]
        else:
            order = [self._idFieldName]
        self._items = db.getRecordList(table, cols, filter, order)
        self.reset()


    def getTableFieldList(self):
        if self._tableFields is None:
            fields = []
            for col in self._cols:
                if col.external():
                    field = CSurrogateField(col.fieldName(), col.valueType())
                else:
                    field = self._table[col.fieldName()]

                fields.append(field)

            fields.append(self._table[self._idFieldName])
            if self._idxFieldName:
                fields.append(self._table[self._idxFieldName])
            for col in self._hiddenCols:
                field = self._table[col]
                fields.append(field)

            self._tableFields = fields
        return self._tableFields


class CBlankMovingInDocTableModel(CInDocTableModel):
    def removeRows(self, row, count, parentIndex = QModelIndex()):
        if 0<=row and row+count<=len(self._items):
            self.beginRemoveRows(parentIndex, row, row+count-1)
            item = self._items[row]
            self.deletedIdList.append(forceRef(item.value('id')))
            del self._items[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def saveItems(self, masterId):
        if self._items is not None:
            db = QtGui.qApp.db
            table = self._table
            masterId = toVariant(masterId)
            masterIdFieldName = self._masterIdFieldName
            idFieldName = self._idFieldName
            for idx, record in enumerate(self._items):
                record.setValue(masterIdFieldName, masterId)
                if self._idxFieldName:
                    record.setValue(self._idxFieldName, toVariant(idx))
                if self._extColsPresent:
                    outRecord = self.removeExtCols(record)
                else:
                    outRecord = record
                id = db.insertOrUpdate(table, outRecord)
                record.setValue(idFieldName, toVariant(id))
            if self.deletedIdList:
                filter = [table[masterIdFieldName].eq(masterId),
                          table[idFieldName].inlist(self.deletedIdList)]
                if self._filter:
                    filter.append(self._filter)
                    db.markRecordsDeleted(table, filter)


    def loadSubPartyItems(self, masterId, filter = []):
        db = QtGui.qApp.db
        cols = []
        for col in self._cols:
            if not col.external():
                cols.append(col.fieldName())
        cols.append(self._idFieldName)
        cols.append(self._masterIdFieldName)
        if self._idxFieldName:
            cols.append(self._idxFieldName)
        for col in self._hiddenCols:
            cols.append(col)
        table = self._table
        filter.append(table[self._masterIdFieldName].eq(masterId))
        if self._filter:
            filter.append(self._filter)
        if table.hasField('deleted'):
            filter.append(table['deleted'].eq(0))
        if self._idxFieldName:
            order = [self._idxFieldName, self._idFieldName]
        else:
            order = [self._idFieldName]
        self._items = db.getRecordList(table, cols, filter, order)
        self.reset()


class CBlankTempInvalidPartyModelEl(CBlankPartyInDocTableModel):
    def __init__(self, parent):
        CBlankPartyInDocTableModel.__init__(self, 'BlankTempInvalid_Party', 'id', 'doctype_id', parent)
        self.addCol(CRBInvalDocTypeInDocTableCol(u'Тип', 'doctype_id', 10, 'rbBlankTempInvalids', addNone=False, showFields=CRBComboBox.showCodeAndName))
        self.addCol(CDateInDocTableCol(u'Дата', 'date', 20))
        self.addCol(CPersonFindInDocTableCol(u'Получатель', 'person_id', 20, 'vrbPersonWithSpeciality', parent=parent))
        self.addCol(CInDocTableCol(u'Серия', 'serial', 10))
        self.addCol(CInDocTableCol(u'Номер с', 'numberFrom', 10))
        self.addCol(CInDocTableCol(u'Номер по', 'numberTo', 10))
        self.addCol(CAmountIntInDocTableCol(u'Исходное количество', 'amount', 10))
        self.addCol(CAmountIntInDocTableCol(u'Выдано', 'extradited', 10)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Списано', 'writing', 10))
        self.addCol(CAmountIntInDocTableCol(u'Возврат', 'returnBlank', 10)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Остаток', 'balance', 10)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Использовано', 'used', 10)).setReadOnly(True)
        self.deletedIdList = []


    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def savePartyItems(self):
        pass


class CBlankTempInvalidPartyModel(CBlankPartyInDocTableModel):
    def __init__(self, parent):
        CBlankPartyInDocTableModel.__init__(self, 'BlankTempInvalid_Party', 'id', 'doctype_id', parent)
        self.addCol(CRBInvalDocTypeInDocTableCol(u'Тип', 'doctype_id', 10, 'rbBlankTempInvalids', addNone=False, showFields=CRBComboBox.showCodeAndName))
        self.addCol(CDateInDocTableCol(u'Дата', 'date', 20))
        self.addCol(CPersonFindInDocTableCol(u'Получатель', 'person_id',  20, 'vrbPersonWithSpeciality', parent=parent))
        self.addCol(CInDocTableCol(u'Серия', 'serial', 10))
        self.addCol(CInDocTableCol(u'Номер с', 'numberFrom', 10))
        self.addCol(CInDocTableCol(u'Номер по', 'numberTo', 10))
        self.addCol(CAmountIntInDocTableCol(u'Исходное количество', 'amount', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Выдано', 'extradited', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Списано', 'writing', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Возврат', 'returnBlank', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Остаток', 'balance', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Использовано', 'used', 10, high=100000)).setReadOnly(True)
        self.deletedIdList = []


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
#        row = index.row()
        if not variantEq(self.data(index, role), value):
            if column == 6:
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateTempInvalidBlankParty()
                return result
            elif column == 8:
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateTempInvalidBlankParty()
                return result
            return CInDocTableModel.setData(self, index, value, role)
        else:
            return True


class CBlankTempInvalidMovingModel(CBlankMovingInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'BlankTempInvalid_Moving', 'id', 'blankParty_id', parent)
        self.addCol(CDateInDocTableCol(u'Дата', 'date', 20))
        self.addCol(CInDocTableCol(u'Номер с', 'numberFrom', 10))
        self.addCol(CInDocTableCol(u'Номер по', 'numberTo', 10))
        self.addCol(COrgStructureInDocTableCol(u'Подразделение',  'orgStructure_id',  15))
        self.addCol(CPersonFindInDocTableCol(u'Получил', 'person_id',  20, 'vrbPersonWithSpeciality', parent=parent))
        self.addCol(CAmountIntInDocTableCol(u'Получено', 'received', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Использовано', 'used', 10, high=100000))
        self.addCol(CDateInDocTableCol(u'Дата возврата', 'returnDate', 20, canBeEmpty=True))
        self.addCol(CAmountIntInDocTableCol(u'Возвращено', 'returnAmount', 10, high=100000))
        self.deletedIdList = []


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        row = index.row()
        if not variantEq(self.data(index, role), value):
            if column == 1:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                QObject.parent(self).checkDoubleNumber(forceInt(value), row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 2:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                QObject.parent(self).checkDoubleNumber(forceInt(value), row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 3:
                self._cols[4].orgStructureId = forceRef(value)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 5:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateTempInvalidBlankParty()
                return result
            elif column == 6:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateTempInvalidBlankParty()
                return result
            elif column == 8:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankTempInvalidMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateTempInvalidBlankParty()
                return result
            return CInDocTableModel.setData(self, index, value, role)
        else:
            return True


class CBlankActionsPartyModel(CBlankPartyInDocTableModel):
    def __init__(self, parent):
        CBlankPartyInDocTableModel.__init__(self, 'BlankActions_Party', 'id', 'doctype_id', parent)
        self.addCol(CRBActionDocTypeInDocTableCol(u'Тип', 'doctype_id', 10, 'rbBlankActions', addNone=False, showFields=CRBComboBox.showCodeAndName))
        self.addCol(CDateInDocTableCol(u'Дата', 'date', 20))
        self.addCol(CPersonFindInDocTableCol(u'Получатель', 'person_id',  20, 'vrbPersonWithSpeciality', parent=parent))
        self.addCol(CInDocTableCol(u'Серия', 'serial', 10))
        self.addCol(CInDocTableCol(u'Номер с', 'numberFrom', 10))
        self.addCol(CInDocTableCol(u'Номер по', 'numberTo', 10))
        self.addCol(CAmountIntInDocTableCol(u'Исходное количество', 'amount', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Выдано', 'extradited', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Списано', 'writing', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Возврат', 'returnBlank', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Остаток', 'balance', 10, high=100000)).setReadOnly(True)
        self.addCol(CAmountIntInDocTableCol(u'Использовано', 'used', 10, high=100000)).setReadOnly(True)
        self.deletedIdList = []


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
#        row = index.row()
        if not variantEq(self.data(index, role), value):
            if column == 6:
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateActionsBlankParty()
                return result
            elif column == 8:
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateActionsBlankParty()
                return result
            return CInDocTableModel.setData(self, index, value, role)
        else:
            return True


class CBlankActionsMovingModel(CBlankMovingInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'BlankActions_Moving', 'id', 'blankParty_id', parent)
        self.addCol(CDateInDocTableCol(u'Дата', 'date', 20))
        self.addCol(CInDocTableCol(u'Номер с', 'numberFrom', 10))
        self.addCol(CInDocTableCol(u'Номер по', 'numberTo', 10))
        self.addCol(COrgStructureInDocTableCol(u'Получатель подразделение',  'orgStructure_id',  15))
        self.addCol(CPersonFindInDocTableCol(u'Получатель персона', 'person_id',  20, 'vrbPersonWithSpeciality', parent=parent))
        self.addCol(CAmountIntInDocTableCol(u'Получено', 'received', 10, high=100000))
        self.addCol(CAmountIntInDocTableCol(u'Использовано', 'used', 10, high=100000))
        self.addCol(CDateInDocTableCol(u'Возврат дата', 'returnDate', 20))
        self.addCol(CAmountIntInDocTableCol(u'Возврат количество', 'returnAmount', 10, high=100000))
        self.deletedIdList = []


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        row = index.row()
        if not variantEq(self.data(index, role), value):
            if column == 1:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankActionsMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                QObject.parent(self).checkDoubleNumber(forceInt(value), row, column, QObject.parent(self).tblBlankActionsMoving, self)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 2:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankActionsMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                QObject.parent(self).checkDoubleNumber(forceInt(value), row, column, QObject.parent(self).tblBlankActionsMoving, self)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 3:
                self._cols[4].orgStructureId = forceRef(value)
                return CInDocTableModel.setData(self, index, value, role)
            elif column == 5:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankActionsMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateActionsBlankParty()
                return result
            elif column == 6:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankActionsMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateActionsBlankParty()
                return result
            elif column == 8:
                QObject.parent(self).checkReturnBlank(row, column, QObject.parent(self).tblBlankActionsMoving, self)
                result = CInDocTableModel.setData(self, index, value, role)
                if result:
                    QObject.parent(self).updateActionsBlankParty()
                return result
            return CInDocTableModel.setData(self, index, value, role)
        else:
            return True
