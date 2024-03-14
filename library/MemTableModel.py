# -*- coding: utf-8 -*-
from PyQt4 import QtSql, QtGui
from PyQt4.QtCore           import *

from library.TableModel		import *

class CMemTableModel(QAbstractTableModel):
    class CRecordIndex():
        def __init__(self, fields):
            self.fields = fields if isinstance(fields, tuple) else (fields, )
            self.dict = {}
            
        def add(self, record):
            key = tuple([record.value(field).toPyObject() for field in self.fields])
            if key not in self.dict:
                self.dict[key] = []
            self.dict[key].append(record)
            
        def remove(self, record):
            key = tuple([record.value(field).toPyObject() for field in self.fields])
            if key not in self.dict or record not in self.dict[key]:
                return False
            else:
                self.dict[key].remove(record)
                if self.dict[key] == []:
                    del self.dict[key]
                return True
                    
        def select(self, values):
            if not isinstance(values, tuple):
                values = (values,)
            key = tuple([value.toPyObject() if isinstance(value, QVariant) else value for value in values])
            return list(self.dict.get(key, []))
            
        def clear(self):
            self.dict.clear()

    
    def __init__(self, parent, columns = [], addFields = []):
        QAbstractTableModel.__init__(self, parent)
        self._columns = columns
        self._records = []
        self._indexes = []
        self._addFields = addFields

    def cols(self):
        return self._columns

    def recordList(self):
        return self._records

    def invalidateRecordsCache(self):
        for column in self._columns:
            column.invalidateRecordsCache()

    def getRecordByRow(self, row):
        return self._records[row]

    def getRecordValues(self, columnIndex, rowIndex):
        column = self._columns[columnIndex]
        record = self._records[rowIndex]
        data = column.extractValuesFromRecord(record)
        return (column, data)

    def setRecordValue(self, columnIndex, rowIndex, value):
        record = self._records[rowIndex]
        record.setValue(columnIndex, value)

    def columnCount(self, index = None):
        return len(self._columns)

    def rowCount(self, index = None):
        return len(self._records)
        
    def appendRecord(self, otherRecord = None, **fieldValues):
        newRowIndex = len(self._records)
        self.beginInsertRows(QModelIndex(), newRowIndex, newRowIndex)
        newRecord = QtSql.QSqlRecord()
        newRecord.row = newRowIndex
        for column in self._columns:
            for fieldName in column.fields():
                newRecord.append(QtSql.QSqlField(fieldName))
        for fieldName in self._addFields:
            newRecord.append(QtSql.QSqlField(fieldName))
        
        if isinstance(otherRecord, QtSql.QSqlRecord):
            for index in range(0, otherRecord.count()):
                newRecord.setValue(otherRecord.fieldName(index), otherRecord.field(index).value())
        for fieldName, value in fieldValues.iteritems():
            newRecord.setValue(fieldName, value)
        self._records.append(newRecord)
        for index in self._indexes:
            index.add(newRecord)
        self.endInsertRows()
        

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        columnIndex = index.column()
        rowIndex    = index.row()
        if role == Qt.DisplayRole:
            (column, values) = self.getRecordValues(columnIndex, rowIndex)
            return column.format(values)
        elif role == Qt.TextAlignmentRole:
            column = self._columns[columnIndex]
            return column.alignment()
        elif role == Qt.CheckStateRole:
            (column, values) = self.getRecordValues(columnIndex, rowIndex)
            return column.checked(values)
        elif role == Qt.ForegroundRole:
            (column, values) = self.getRecordValues(columnIndex, rowIndex)
            return column.getForegroundColor(values)
        elif role == Qt.BackgroundRole:
            (column, values) = self.getRecordValues(columnIndex, rowIndex)
            return column.getBackgroundColor(values)
        return QVariant()
        
        
    def setData(self, index, value, role):
        columnIndex = index.column()
        rowIndex    = index.row()
        column = self._columns[columnIndex]
        if role == Qt.CheckStateRole and isinstance(column, CBoolCol):
            if value == Qt.Checked:
                self.setRecordValue(columnIndex, rowIndex, True)
            else:
                self.setRecordValue(columnIndex, rowIndex, False)
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def flags(self, index):
        columnIndex = index.column()
        rowIndex    = index.row()
        column = self._columns[columnIndex]
        if hasattr(column, 'checkable') and column.checkable == True:
            return QAbstractTableModel.flags(self, index) | Qt.ItemIsUserCheckable
        else:
            return QAbstractTableModel.flags(self, index)
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._columns):
                    return self._columns[section].title()
            if role == Qt.ToolTipRole:
                return self._columns[section].toolTip()
            if role == Qt.WhatsThisRole:
                return self._columns[section].whatsThis()
        return QVariant()


    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, row, row)
        record = self._records[row]
        for index in self._indexes:
            index.remove(record)
        del self._records[row]
        self.endRemoveRows()
        return True


    def clear(self):
        self._records = []
        for index in self._indexes:
            index.clear()
        self.reset()


    def makeIndex(self, fields):
        newIndex = CMemTableModel.CRecordIndex(fields)
        for record in self._records:
            newIndex.add(record)
        self._indexes.append(newIndex)
        return newIndex


    def loadFromSql(self, sql, acceptIf = None):
        query = QtGui.qApp.db.query(sql)
        self.clear()
        while query.next():
            record = query.record()
            if not acceptIf or not callable(acceptIf) or acceptIf(record):
                self.appendRecord(record)
        
        
    def assignRecord(self, record, newRecord):
        for index in self._indexes:
            index.remove(record)
        for i in range(0, newRecord.count()):
            record.setValue(newRecord.fieldName(i), newRecord.field(i).value())
        self.dataChanged.emit(self.index(record.row, 0), self.index(record.row, len(self._columns) - 1))
        for index in self._indexes:
            index.add(record)
