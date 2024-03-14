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

from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, pyqtSignature, QDateTime

from library.DialogBase    import CDialogBase
from library.InDocTable    import CDateTimeForEventInDocTableCol, CInDocTableModel
from library.Utils         import forceDateTime, forceRef, toVariant
from Orgs.PersonComboBoxEx import CPersonFindInDocTableCol
from Users.Rights          import urEditEventJournalOfPerson

from F003.Ui_ExecPersonListEditor import Ui_ExecPersonListEditor


class CExecPersonListEditorDialog(CDialogBase, Ui_ExecPersonListEditor):
    def __init__(self, parent, eventId):
        CDialogBase.__init__(self, parent)
        self.addModels('ExecPersonList', CExecPersonInDocTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblExecPersonList,  self.modelExecPersonList, self.selectionModelExecPersonList)
        self.eventId = eventId
        self.modelExecPersonList.loadItems(self.eventId)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(QtGui.qApp.userHasRight(urEditEventJournalOfPerson))


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            if self.eventId:
                self.modelExecPersonList.saveItems(self.eventId)
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def setExecPersonInfo(self, personId, endDate, currentUserId):
        if personId:
            if self.modelExecPersonList.items():
                item = self.modelExecPersonList.items()[-1]
                if item:
                    setDate = forceDateTime(item.value('setDate'))
                    db = QtGui.qApp.db
                    tableEJOP = db.table('Event_JournalOfPerson')
                    newItem = tableEJOP.newRecord()
                    newItem.setValue('execPerson_id', toVariant(personId))
                    newItem.setValue('setPerson_id', toVariant(currentUserId))
                    if endDate:
                        newItem.setValue('setDate', toVariant(endDate))
                    else:
                        newItem.setValue('setDate', toVariant(setDate.addSecs(60)))
                    self.modelExecPersonList.items().append(newItem)
            else:
                db = QtGui.qApp.db
                tableEJOP = db.table('Event_JournalOfPerson')
                newItem = tableEJOP.newRecord()
                newItem.setValue('execPerson_id', toVariant(personId))
                newItem.setValue('setPerson_id', toVariant(currentUserId))
                if endDate:
                    newItem.setValue('setDate', toVariant(endDate))
                else:
                    newItem.setValue('setDate', toVariant(QDateTime.currentDateTime()))
                self.modelExecPersonList.items().append(newItem)


    def getJournalOfPersonData(self):
        mapJournalOfPerson = []
        items = self.modelExecPersonList.items()
        for item in items:
            mapJournalOfPerson.append(item)
        return mapJournalOfPerson


    def setJournalOfPersonData(self, mapJournalOfPerson):
        modelItems = self.modelExecPersonList.items()
        items = []
        for item in mapJournalOfPerson:
            mapId = forceRef(item.value('id'))
            mapNoModel = True
            for modelItem in modelItems:
                if mapId and forceRef(modelItem.value('id')) == mapId:
                    mapNoModel = False
                    break
            if mapNoModel:
                items.append(item)
        for item in items:
            self.modelExecPersonList.items().append(item)


    def getExecPersonId(self):
        item = self.modelExecPersonList.items()[-1]
        if item:
            return forceRef(item.value('execPerson_id'))
        return None


class CLocInDocTableModel(CInDocTableModel):
    def __init__(self, tableName, idFieldName, masterIdFieldName, parent):
        CInDocTableModel.__init__(self, tableName, idFieldName, masterIdFieldName, parent)
        db = QtGui.qApp.db
        self._table = db.table(tableName)
        self._idFieldName = idFieldName
        self._masterIdFieldName = masterIdFieldName
        if self._table.hasField('idx'):
            self._idxFieldName = 'idx'
        else:
            self._idxFieldName = ''
        self._tableFields = None
        self._enableAppendLine = True
        self._extColsPresent = False
        self._filter = None
        self._orderFieldName = 'setDate'

    table = property(lambda self: self._table)
    idFieldName = property(lambda self: self._idFieldName)
    idxFieldName = property(lambda self: self._idxFieldName)
    orderFieldName = property(lambda self: self._orderFieldName)
    masterIdFieldName = property(lambda self: self._masterIdFieldName)
    filter = property(lambda self: self._filter)


    def getExecPersonId(self):
        item = self.modelExecPersonList.items()[-1]
        if item:
            return forceRef(item.value('execPerson_id'))
        return None


    def loadItems(self, masterId):
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
        filter = [table[self._masterIdFieldName].eq(masterId)]
        if self._filter:
            filter.append(self._filter)
        if table.hasField('deleted'):
            filter.append(table['deleted'].eq(0))
        order = [self._orderFieldName]
        self._items = db.getRecordList(table, cols, filter, order)
        if self._extColsPresent:
            extSqlFields = []
            for col in self._cols:
                if col.external():
                    fieldName = col.fieldName()
                    if fieldName not in cols:
                        extSqlFields.append(QtSql.QSqlField(fieldName, col.valueType()))
            if extSqlFields:
                for item in self._items:
                    for field in extSqlFields:
                        item.append(field)
        self.reset()


class CExecPersonInDocTableModel(CLocInDocTableModel):
    def __init__(self, parent):
        CLocInDocTableModel.__init__(self, 'Event_JournalOfPerson', 'id', 'master_id', parent)
        self.addCol(CPersonFindInDocTableCol(      u'Исполнитель',     'execPerson_id',20, 'vrbPersonWithSpecialityAndOrgStr', parent=parent))
        self.addCol(CDateTimeForEventInDocTableCol(u'Дата назначения', 'setDate',      20, canBeEmpty=True))
        self.addCol(CPersonFindInDocTableCol(      u'Назначивший',     'setPerson_id', 20, 'vrbPersonWithSpecialityAndOrgStr', parent=parent))
        self.readOnly = False

