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

from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, pyqtSignature, QVariant

from library.InDocTable import CBoolInDocTableCol, CInDocTableCol, CInDocTableModel
from library.Utils      import forceRef, toVariant, forceBool

from Ui_ActionTypeListDialog import Ui_ActionTypeListDialog


class CActionTypeListDialog(QtGui.QDialog, Ui_ActionTypeListDialog):
    def __init__(self, parent, filter=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CActionTypeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.setWindowTitle(u'Выберите Типы Действий')
        self.tblActionTypeList.setModel(self.tableModel)
        self.tblActionTypeList.setSelectionModel(self.tableSelectionModel)
        self.tblActionTypeList.installEventFilter(self)
        self._parent = parent
        self.actionTypeIdList =  []
        self.filter = filter
        self.tblActionTypeList.model().clearItems()
        self.tblActionTypeList.model().setItems(self.getActionTypeItems())


    def getActionTypeItems(self):
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        cond = [tableActionType['deleted'].eq(0)]
        if self.filter:
            cond.append(self.filter)
        actionTypeItems = db.getRecordList(tableActionType, '*',
                              where=cond,
                              order=u'ActionType.code ASC, ActionType.name ASC')
        for row, record in enumerate(actionTypeItems):
            record.append(QtSql.QSqlField('include', QVariant.Int))
            record.setValue('include', toVariant(Qt.Checked))
            actionTypeItems[row] = record
        return actionTypeItems


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getCheckedIdList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getCheckedIdList(self):
        self.actionTypeIdList = self.tblActionTypeList.model().getCheckedIdList()


    def values(self):
        return self.actionTypeIdList


    def setValue(self, actionTypeIdList):
        self.actionTypeIdList = actionTypeIdList


class CActionTypeTableModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ActionType', 'id', 'master_id', parent)
        self.addExtCol(CBoolInDocTableCol(u'Включить', 'include', 10), QVariant.Int, idx=0)
        self.addCol(CInDocTableCol(       u'Код',          'code',  30))
        self.addCol(CInDocTableCol(       u'Наименование', 'name',  50))
        self.readOnly = False


    def setReadOnly(self, value):
        self.readOnly = value


    def rowCount(self, index = None):
        return len(self.items())


    def cellReadOnly(self, index):
        if index.column() == 0:
            return False
        return True


    def flags(self, index):
        if self.readOnly:
           return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def getEmptyRecord(self):
        result = CInDocTableModel.getEmptyRecord(self)
        result.append(QtSql.QSqlField('include', QVariant.Int))
        return result


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            row = index.row()
            column = index.column()
            if column == 0:
                if row >= 0 and row < len(self.items()):
                    self.setValue(row, 'include', QVariant(forceBool(value)))
                    self.emitCellChanged(row, column)
                    return True
        return False


    def loadItems(self, masterId=None):
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
        filter = []
        if self._filter:
            filter.append(self._filter)
        if table.hasField('deleted'):
            filter.append(table['deleted'].eq(0))
        order = [table['code'].name(), table['name'].name()]
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


    def on_checkedAllRow(self):
        items = self.items()
        for row, record in enumerate(items):
            record.setValue('include', toVariant(Qt.Checked))
            items[row] = record
        self.reset()


    def getCheckedIdList(self):
        checkedIdList = []
        items = self.items()
        for row, record in enumerate(items):
            include = record.value('include')
            if include == Qt.Checked:
                checkedIdList.append(forceRef(record.value('id')))
        return checkedIdList
