# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from library.Utils import *

class CHeaderViewWithWordWrap(QtGui.QHeaderView):
    def __init__(self, orientation):
        QtGui.QHeaderView.__init__(self, orientation)
        if orientation == Qt.Horizontal:
            self.textAlignment = Qt.AlignVCenter | Qt.AlignHCenter | Qt.TextWordWrap
        else:
            self.textAlignment = Qt.AlignVCenter | Qt.TextWordWrap
        self.margin = 4

    def sectionSizeFromContents(self, logicalIndex):
        if self.model():
            headerText = self.model().headerData(logicalIndex,
                                                 self.orientation(),
                                                 Qt.DisplayRole)
            options = self.viewOptions()
            metrics = QtGui.QFontMetrics(options.font)
            sectionSize = self.sectionSize(logicalIndex)
            if self.orientation() == Qt.Horizontal:
                rect = QRect(0, 0, sectionSize - self.margin * 2, 5000)
            else:
                rect = QRect(0, 0, self.width() - self.margin * 2, 5000)
            boundingRect = metrics.boundingRect(rect, self.textAlignment, headerText)
            return boundingRect.adjusted(0, 0, self.margin * 2, self.margin * 2).size()
        else:
            return QtGui.QHeaderView.sectionSizeFromContents(self, logicalIndex)

    def paintSection(self, painter, rect, logicalIndex):
        if self.model():
            painter.save()
            self.model().hideHeaders()
            QtGui.QHeaderView.paintSection(self, painter, rect, logicalIndex)
            self.model().unhideHeaders()
            painter.restore()
            headerText = self.model().headerData(logicalIndex,
                                                 self.orientation(),
                                                 Qt.DisplayRole)
            textRect = rect.adjusted(self.margin, self.margin, -self.margin, -self.margin)
            painter.drawText(textRect, self.textAlignment, headerText)
        else:
            QtGui.QHeaderView.paintSection(self, painter, rect, logicalIndex)

class CReportTableView(QtGui.QTableView):
    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        self.setHorizontalHeader(CHeaderViewWithWordWrap(Qt.Horizontal))
        self.setVerticalHeader(CHeaderViewWithWordWrap(Qt.Vertical))
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.verticalHeader().setFixedWidth(300)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        self.horizontalHeader().setDefaultSectionSize(150)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)

    def verticalResizeToContents(self):
        totalHeight = 0
        if not self.horizontalHeader().isHidden():
            totalHeight += self.horizontalHeader().height()
        self.horizontalHeader().height()
        count = self.verticalHeader().count()
        for i in xrange(0, count):
            if not self.verticalHeader().isSectionHidden(i):
                totalHeight += self.verticalHeader().sectionSize(i)
        if not self.horizontalScrollBar().isHidden():
            totalHeight += self.horizontalScrollBar().height()
        self.setMinimumHeight(totalHeight)

class CReportTableColumn:
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name

class CReportTableRow:
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name

class CReportTableIndex:
    def __init__(self, id, code, value):
        self.id = id
        self.code = code
        self.value = value
    
    def formatValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
        return self.value
    
    def isNull(self):
        return self.value.isNull()
    
class CReportTableIndexString(CReportTableIndex):
    def setValue(self, value):
        db = QtGui.qApp.db
        formattedValue = db.formatValueEx(QVariant.String, value)
        stmt = u'UPDATE SvodIndex SET valueString = %s WHERE id = %d' % (formattedValue, self.id)
        db.query(stmt)
        return CReportTableIndex.setValue(self, value)
    
class CReportTableIndexNumeric(CReportTableIndex):
    def setValue(self, value):
        db = QtGui.qApp.db
        formattedValue = db.formatValueEx(QVariant.Double, value)
        stmt = u'UPDATE SvodIndex SET valueNumeric = %s WHERE id = %d' % (formattedValue, self.id)
        db.query(stmt)
        return CReportTableIndex.setValue(self, value)
    
class CReportTableIndexDate(CReportTableIndex):
    def setValue(self, value):
        db = QtGui.qApp.db
        formattedValue = db.formatValueEx(QVariant.Date, value)
        stmt = u'UPDATE SvodIndex SET valueDate = %s WHERE id = %d' % (formattedValue, self.id)
        db.query(stmt)
        return CReportTableIndex.setValue(self, value)

class CReportTableModel(QAbstractTableModel):
    def __init__(self, parent, sectionId, tableId):
        QAbstractTableModel.__init__(self, parent)
        self.sectionId = sectionId
        self.tableId = tableId
        self.columns = []
        self.rows = []
        self.indexesByCode = {}
        self.indexesByRowAndColumn = {}
        self.load()
        self.headersHidden = False
    
    def load(self):
        db = QtGui.qApp.db
        columnRecords = db.getRecordList('SvodTableColumn', cols='id, externalCode, name', where='table_id = %d' % self.tableId, order='externalCode')
        for columnRecord in columnRecords:
            id = forceRef(columnRecord.value('id'))
            code = forceString(columnRecord.value('externalCode'))
            name = forceString(columnRecord.value('name'))
            column = CReportTableColumn(id, code, name)
            self.columns.append(column)
        rowRecords = db.getRecordList('SvodTableRow', cols='id, externalCode, name', where='table_id = %d' % self.tableId, order='externalCode')
        for rowRecord in rowRecords:
            id = forceRef(rowRecord.value('id'))
            code = forceString(rowRecord.value('externalCode'))
            name = forceString(rowRecord.value('name'))
            row = CReportTableRow(id, code, name)
            self.rows.append(row)
        indexRecords = db.getRecordList('SvodIndex', cols='id, column_id, row_id, externalCode, valueType, valueString, valueNumeric, valueDate', where='reportSection_id = %d and table_id = %d' % (self.sectionId, self.tableId))
        for indexRecord in indexRecords:
            id = forceRef(indexRecord.value('id'))
            column_id = forceRef(indexRecord.value('column_id'))
            row_id = forceRef(indexRecord.value('row_id'))
            code = forceString(indexRecord.value('externalCode'))
            valueType = forceString(indexRecord.value('valueType'))
            if valueType.startswith(u'Строка'):
                index = CReportTableIndexString(id, code, indexRecord.value('valueString'))
            elif valueType.startswith(u'Число'):
                index = CReportTableIndexNumeric(id, code, indexRecord.value('valueNumeric'))
            elif valueType.startswith(u'Дата'):
                index = CReportTableIndexDate(id, code, indexRecord.value('valueDate'))
            else:
                raise Exception(u"Неизвестный тип показателя: %s" % valueType)
            self.indexesByCode[code] = index
            self.indexesByRowAndColumn[(row_id, column_id)] = index

    def totalIndexes(self):
        return len(self.indexesByCode)

    def filledIndexes(self):
        return sum(1 for index in self.indexesByCode.itervalues() if not index.isNull())

    def columnCount(self, index = None):
        return len(self.columns)

    def rowCount(self, index = None):
        return len(self.rows)
    
    def hideHeaders(self):
        self.headersHidden = True
    
    def unhideHeaders(self):
        self.headersHidden = False

    def data(self, index, role=Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.EditRole):
            column = self.columns[index.column()]
            row = self.rows[index.row()]
            cellIndex = self.indexesByRowAndColumn.get((row.id, column.id))
            if cellIndex:
                return cellIndex.formatValue()
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self.headersHidden:
                return QVariant()
            if orientation == Qt.Horizontal and section < len(self.columns):
                return self.columns[section].name
            if orientation == Qt.Vertical and section < len(self.rows):
                return self.rows[section].name
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = self.columns[index.column()]
            row = self.rows[index.row()]
            cellIndex = self.indexesByRowAndColumn.get((row.id, column.id))
            cellIndex.setValue(value)
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def emitDataChanged(self):
        leftTop = self.index(0, 0)
        rightBottom = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), leftTop, rightBottom)
