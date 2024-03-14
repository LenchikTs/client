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

import json
import re

from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QDate, QDateTime, QEvent, QEventLoop, QModelIndex, QString, QVariant, QObject

from Reports.ReportBase import CReportBase, createTable

from library.ClientRecordProperties import CRecordProperties

from library.crbcombobox import CRBModelDataCache, CRBLikeEnumModel, CRBComboBox
from library.CRBSearchComboBox import CRBSearchComboBox

from library import database
from library.ICDUtils       import getMKBName
from library.Utils import CColsMovingFeature, copyFields, forceBool, forceDate, forceDateTime, forceInt, forceRef, forceString, forceStringEx, formatDate, formatDateTime, formatName, formatSex, formatTime, getDentitionActionTypeId, getPref, setPref, toVariant, trim, getExSubclassItemLastName


from library.DateEdit import CDateEdit
from library.DateTimeEdit import CDateTimeEdit
from library.PreferencesMixin import CPreferencesMixin


__all__ = ( 'CInDocTableCol',
            'CEnumInDocTableCol',
            'CSelectStrInDocTableCol',
            'CRBLikeEnumInDocTableCol',
            'CRBInDocTableCol',
            'CRBSearchInDocTableCol',
            'CClientInDocTableCol',
            'CCodeNameInDocTableCol',
            'CCodeRefInDocTableCol',
            'CDateInDocTableCol',
            'CTimeInDocTableCol',
            'CDateTimeInDocTableCol',
            'CDateTimeForEventInDocTableCol',
            'CBoolInDocTableCol',
            'CIntInDocTableCol',
            'CAgeInDocTableCol',
            'CFloatInDocTableCol',
            'CTextInDocTableCol',
            'CRecordListModel',
            'CInDocTableModel',
            'CLocItemDelegate',
            'CInDocTableView',
            'CMKBListInDocTableModel',
          )
#
# Отображение и редактирование таблицы БД в таблице Qt
# Модель - CInDocTableModel
# Представление - CInDocTableView.
#


def forcePyType(val):
    #Извлекает данные из QVariant
    #(обратная функция - toVariant)
    t = val.type()
    if t == QVariant.Bool:
        return val.toBool()
    elif t == QVariant.Date:
        return val.toDate()
    elif t == QVariant.DateTime:
        return val.toDateTime()
    elif t == QVariant.Double:
        return val.toDouble()[0]
    elif t == QVariant.Int:
        return val.toInt()[0]
    else:
        return unicode(val.toString())


class CInDocTableCol(object):
    # Столбец таблицы с возможностью редактирования
    def __init__(self, title, fieldName, width, **params):
        self._title     = toVariant(title)
        self._toolTip   = toVariant(params.get('toolTip', None))
        self._whatsThis = toVariant(params.get('whatThis', None))
        self._fieldName = fieldName
        self._width     = width
        self._external  = False
        self._valueType = None
        self._readOnly  = params.get('readOnly', False)
        self._maxLength = params.get('maxLength', None)
        self._inputMask = params.get('inputMask', None)
        self._validator = params.get('validator', None)
        self._sortable = False
        self._defaultWidth = width
        self._switchOff = params.get('switchOff', True)
        self._defaultHidden = params.get('defaultHidden', False)


    @property
    def defaultHidden(self):
        return self._defaultHidden


    def switchOff(self):
        return self._switchOff


    def setTitle(self, title):
        self._title = toVariant(title)


    def title(self):
        return self._title


    def setToolTip(self, toolTip):
        self._toolTip = toVariant(toolTip)
        return self


    def toolTip(self):
        return self._toolTip


    def setWhatsThis(self, whatsThis):
        self._whatsThis = toVariant(whatsThis)
        return self


    def whatsThis(self):
        return self._whatsThis


    def fieldName(self):
        return self._fieldName


    def width(self):
        return self._width


    def setInputMask(self, inputMask):
        self._inputMask = inputMask


    def setValidator(self, validator):
        self._validator = validator


    def setMaxLength(self, maxLength):
        self._maxLength = maxLength


    def setExternal(self, external):
        # Внешняя колонка есть в таблице БД, но не хранится в модели
        self._external  = external


    def external(self):
        # Внешняя колонка есть в таблице БД, но не хранится в модели
        return self._external


    def setValueType(self, valueType):
        self._valueType = valueType


    def valueType(self):
        return self._valueType


    def setReadOnly(self, readOnly=True):
        self._readOnly = readOnly
        return self


    def readOnly(self):
        return self._readOnly


    def setSortable(self, value=True):
        self._sortable = value
        return self


    def sortable(self):
        return self._sortable


    def flags(self, index=None):
        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if not self._readOnly:
            result |= Qt.ItemIsEditable
        return result


    def toString(self, val, record):
        # строковое представление (тип - QVariant!)
        return val


    def toSortString(self, val, record):
        return forcePyType(self.toString(val, record))


    def toStatusTip(self, val, record):
        return self.toString(val, record)


    def toCheckState(self, val, record):
        return QVariant()


    def getForegroundColor(self, val, record):
        return QVariant()


    def createEditor(self, parent):
        editor = QtGui.QLineEdit(parent)
        if self._maxLength:
            editor.setMaxLength(self._maxLength)
        if self._inputMask:
            editor.setInputMask(self._inputMask)
        if self._validator:
            editor.setValidator(self._validator)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setText(forceStringEx(value))


    def getEditorData(self, editor):
        text = trim(editor.text())
        if text:
            return toVariant(text)
        else:
            return QVariant()


    def alignment(self):
        return QVariant(Qt.AlignLeft + Qt.AlignVCenter)


class CEnumInDocTableCol(CInDocTableCol):
    # В базе данных хранится номер,
    # а на экране рисуется комбо-бокс с соотв. значениями
    def __init__(self, title, fieldName, width, values, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.values = values


    def toString(self, val, record):
        return toVariant(self.values[forceInt(val)])


    def createEditor(self, parent):
        editor = QtGui.QComboBox(parent)
        for val in self.values:
            editor.addItem(val)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setCurrentIndex(forceInt(value))


    def getEditorData(self, editor):
        return toVariant(editor.currentIndex())


class CSelectStrInDocTableCol(CEnumInDocTableCol):
    # В базе данных хранится строка,
    # а на экране рисуется комбо-бокс с соотв. значениями

    def __init__(self, title, fieldName, width, values, **params):
        CEnumInDocTableCol.__init__(self, title, fieldName, width, values, **params)


    def toString(self, val, record):
        str = forceString(val).lower()
        for item in self.values:
            if item.lower() == str:
                return toVariant(item)
        return toVariant(u'{'+forceString(val)+u'}')


    def setEditorData(self, editor, value, record):
        index = editor.findText(forceString(value), Qt.MatchFixedString)
        if index<0:
            index=0
        editor.setCurrentIndex(index)


    def getEditorData(self, editor):
        return toVariant(editor.currentText())


class CRBLikeEnumInDocTableCol(CInDocTableCol):
    # Чем отличается от CEnumInDocTableCol
    def __init__(self, title, fieldName, width, values, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.values = values
        self.showFields = params.get('showFields', CRBComboBox.showName)
        self.preferredWidth = params.get('preferredWidth', None)
        self.model = CRBLikeEnumModel(None)
        self.model.setValues(self.values)


    def toString(self, val, record):
        text = self.model.d.getStringById(forceInt(val), self.showFields)
        return toVariant(text)


    def toStatusTip(self, val, record):
        text = self.model.d.getStringById(forceInt(val), CRBComboBox.showName)
        return toVariant(text)


    def createEditor(self, parent):
        editor = CRBComboBox(parent)
        editor.setShowFields(self.showFields)
        editor.setPreferredWidth(self.preferredWidth)
        model = CRBLikeEnumModel(editor)
        model.setValues(self.values)
        editor.setModel(model)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setCurrentIndex(forceInt(value))


    def getEditorData(self, editor):
        return toVariant(editor.currentIndex())


class CRBInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, tableName, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.tableName  = tableName
        self.filter     = params.get('filter', '')
        self.addNone    = params.get('addNone', True)
        self.showFields = params.get('showFields', CRBComboBox.showName)
        self.preferredWidth = params.get('preferredWidth', None)
        self.force = False


    def toString(self, val, record):
        cache = CRBModelDataCache.getData(self.tableName, True)
        text = cache.getStringById(forceInt(val), self.showFields)
        return toVariant(text)


    def toSortString(self, val, record):
        return forcePyType(self.getSortString(val, record))


    def getSortString(self, val, record):
        cache = CRBModelDataCache.getData(self.tableName, True)
        text = QString(forceString(cache.getStringById(forceInt(val), self.showFields)).lower())
        return toVariant(text)


    def toStatusTip(self, val, record):
        cache = CRBModelDataCache.getData(self.tableName, True)
        text = cache.getStringById(forceInt(val), CRBComboBox.showName)
        return toVariant(text)


    def createEditor(self, parent):
        editor = CRBComboBox(parent)
        editor.setTable(self.tableName, addNone=self.addNone, filter=self.filter, force=self.force)
        editor.setShowFields(self.showFields)
        editor.setPreferredWidth(self.preferredWidth)
        self.force = False
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(forceInt(value))


    def getEditorData(self, editor):
        return toVariant(editor.value())


    def setFilter(self, filter):
        self.filter = filter
        self.force = True



class CRBSearchInDocTableCol(CRBInDocTableCol):
    def createEditor(self, parent):
        editor = CRBSearchComboBox(parent)
        editor.setTable(self.tableName, addNone=self.addNone, filter=self.filter)
        editor.setShowFields(self.showFields)
        editor.setPreferredWidth(self.preferredWidth)
        return editor


# WFT?
# в libary этому классу не место!
class CClientInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)


    def toString(self, val, record):
        # строковое представление (тип - QVariant!)
        clientId = forceRef(val)
        if clientId:
            rec = QtGui.qApp.db.getRecord('Client', ['lastName', 'firstName', 'patrName', 'birthDate', 'sex', 'id'], clientId)
            name  = formatName(rec.value('lastName'),
                               rec.value('firstName'),
                               rec.value('patrName'))
            birthDate = forceString(rec.value('birthDate'))
            sex = formatSex(rec.value('sex'))
            id = u'(' + forceString(rec.value('id')) + u')'
            return toVariant(u', '.join(n for n in [name, birthDate, sex, id]))
        return val

# WFT?
# CRBInDocTableCol умеет немного не так, но и код и имя показывает!
class CCodeNameInDocTableCol(CRBInDocTableCol):
    #u"""Колонка, в которой отображается и код, и имя"""
    def toString(self, val, record):
        id = forceInt(val)
        if id:
            rec = QtGui.qApp.db.getRecord(self.tableName, ['code', 'name'], forceInt(val))
            return toVariant(rec.value('code').toString() + " - " + rec.value('name').toString())
        else:
            return toVariant(None)



class CCodeRefInDocTableCol(CRBInDocTableCol):
    #u"""Ссылка на справочник не по id, а по code"""
    def toString(self, val, record):
        code = forceString(val)
        if len(code):
            name = QtGui.qApp.db.translate(self.tableName, 'code', code, 'name')
            if name is not None:
                return toVariant(code + ' - ' + forceString(name))
        return QVariant()


    def setEditorData(self, editor, value, record):
        editor.setCode(forceString(value))


    def getEditorData(self, editor):
        return toVariant(editor.code())


class CDateInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.highlightRedDate = params.get('highlightRedDate', True) and QtGui.qApp.highlightRedDate()
        self.canBeEmpty = params.get('canBeEmpty', False)


    def toString(self, val, record):
        if not val.isNull():
           date = val.toDate()
           if date:
               return toVariant(formatDate(date))
        return QVariant()


    def toSortString(self, val, record):
        return forcePyType(val)


    def getForegroundColor(self, val, record):
        date = forceDate(val)
        if self.highlightRedDate and date and QtGui.qApp.calendarInfo.getDayOfWeek(date) in (6,7):
            return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


    def createEditor(self, parent):
        editor = CDateEdit(parent)
        editor.setHighlightRedDate(self.highlightRedDate)
        editor.canBeEmpty(self.canBeEmpty)
#        editor.selectAll()
#        editor.setCalendarPopup(True)
#        editor.setSelectedSection(QtGui.QDateTimeEdit.DaySection)
        return editor


    def setEditorData(self, editor, value, record):
        value = value.toDate()
        if not value.isValid() and not self.canBeEmpty:
            value = QDate.currentDate()
        editor.setDate(value)
#        editor.setDateIsChanged(False)


    def getEditorData(self, editor):
        value = editor.date()
        if value.isValid():
            return toVariant(value)
        elif self.canBeEmpty:
            return QVariant()
        else:
            return QVariant(QDate.currentDate())


class CTimeInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)


    def toString(self, val, record):
        if not val.isNull():
           time = val.toTime()
           if time.isValid():
               return toVariant(formatTime(time))
        return QVariant()


    def toSortString(self, val, record):
        return forcePyType(val)


    def createEditor(self, parent):
        editor = QtGui.QTimeEdit(parent)
        return editor


    def setEditorData(self, editor, value, record):
        time = value.toTime()
        editor.setTime(time.fromString('H:mm'))


    def getEditorData(self, editor):
        value = editor.time()
        if value.isValid():
            return toVariant(value)
        else:
            return QVariant()


class CNotCleanTimeInDocTableCol(CTimeInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CTimeInDocTableCol.__init__(self, title, fieldName, width, **params)


    def setEditorData(self, editor, value, record):
        time = value.toTime()
        editor.setTime(time.fromString(forceString(time), 'h:mm'))


class CDateTimeInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.highlightRedDate = params.get('highlightRedDate', True)


    def toString(self, val, record):
        if not val.isNull():
           datetime = val.toDateTime()
           if datetime:
               return toVariant(forceDateTime(datetime)) # WFT? чем QVariant(datetime) хуже? или имелся в виду formatDateTime?
        return QVariant()


    def toSortString(self, val, record):
        return forcePyType(val)


    def getForegroundColor(self, val, record):
        date = forceDate(val)
        if self.highlightRedDate and date and QtGui.qApp.calendarInfo.getDayOfWeek(date) in (6,7):
            return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()

# WTF? library не должно ничего знать об Event-ах...
class CDateTimeForEventInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.highlightRedDate = params.get('highlightRedDate', True) and QtGui.qApp.highlightRedDate()
        self.canBeEmpty = params.get('canBeEmpty', False)


    def toString(self, val, record):
        if not val.isNull():
           date = val.toDate()
           if date:
               datetime = val.toDateTime()
               return toVariant(formatDateTime(datetime))
        return QVariant()


    def toSortString(self, val, record):
        return forcePyType(val)


    def getForegroundColor(self, val, record):
        date = forceDate(val)
        if self.highlightRedDate and date and QtGui.qApp.calendarInfo.getDayOfWeek(date) in (6,7):
            return QVariant(QtGui.QColor(255, 0, 0))
        return QVariant()


    def createEditor(self, parent):
        editor = CDateTimeEdit(parent)
        editor.setHighlightRedDate(self.highlightRedDate)
        editor.canBeEmpty(self.canBeEmpty)
        return editor


    def setEditorData(self, editor, value, record):
        value = value.toDateTime()
        if not value.isValid() and not self.canBeEmpty:
            value = QDateTime.currentDateTime()
        editor.setDate(value)


    def getEditorData(self, editor):
        value = editor.date()
        if value.isValid():
            return toVariant(value)
        elif self.canBeEmpty:
            return QVariant()
        else:
            return QVariant(QDateTime.currentDateTime())


class CBoolInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)


    def flags(self, index=None):
        result = CInDocTableCol.flags(self)
#        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        if result & Qt.ItemIsEditable:
            result = (result & ~Qt.ItemIsEditable) | Qt.ItemIsUserCheckable
        return result


    def toCheckState(self, val, record):
        if forceInt(val) == 0:
            return QVariant(Qt.Unchecked)
        else:
            return QVariant(Qt.Checked)


    def toString(self, val, record):
        return QVariant()


    def toSortString(self, val, record):
        return forcePyType(val)


    def createEditor(self, parent):
        editor = QtGui.QCheckBox(parent)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setChecked(forceInt(value)!=0)


    def getEditorData(self, editor):
        return toVariant(1 if editor.isChecked() else 0)


class CIntInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.low = params.get('low', 0)
        self.high = params.get('high', 100)


    def createEditor(self, parent):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(self.low)
        editor.setMaximum(self.high)
        return editor

    def setEditorData(self, editor, value, record):
        editor.setValue(forceInt(value))
        editor.selectAll()


    def toSortString(self, val, record):
        return forcePyType(val)


    def getEditorData(self, editor):
        return toVariant(editor.value())


class CAgeInDocTableCol(CIntInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CIntInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.low = params.get('low', 0)
        self.high = params.get('high', 160)


class CFloatInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.low = params.get('low', float('-inf'))
        self.high = params.get('high', float('inf'))
        self.precision = params.get('precision', 6)


    def _toString(self, value):
        if value.isNull():
            return None
        s = QString()
        if self.precision is None:
            s.setNum(value.toDouble()[0])
        else:
            s.setNum(value.toDouble()[0], 'f', self.precision)
        return s


    def toString(self, val, record):
        return toVariant(self._toString(val))


    def toSortString(self, val, record):
        return forcePyType(val)


    def createEditor(self, parent):
        editor = QtGui.QLineEdit(parent)
        validator = QtGui.QDoubleValidator(editor)
        validator.setRange(self.low, self.high, self.precision)
        editor.setValidator(validator)
        return editor


    def setEditorData(self, editor, value, record):
        s = self._toString(value)
        editor.setText('' if s is None else s)
        editor.selectAll()


    def getEditorData(self, editor):
        return toVariant(editor.text().toDouble()[0])


class CTextInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)


    def createEditor(self, parent):
        editor = QtGui.QTextEdit(parent)
        editor.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        editor.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setPlainText(forceStringEx(value))


    def getEditorData(self, editor):
        text = trim(editor.toPlainText())
        if text:
            return toVariant(text)
        else:
            return QVariant()


    def alignment(self):
        return QVariant(Qt.AlignLeft + Qt.AlignTop)


class CRecordListModel(QAbstractTableModel):
    # модель для взаимодействия со списком QSqlRecord; возможно редактирование
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self._cols = []
        self._hiddenCols = []
        self._items = []
        self._mapFieldNameToCol = None
        self._enableAppendLine = False
        self.readOnly = False


    def setReadOnly(self, value):
        self.readOnly = value


    def getReadOnly(self):
        return self.readOnly


    def setEnableAppendLine(self, enableAppendLine=True):
        self._enableAppendLine = enableAppendLine


    def addCol(self, col, idx=None):
        if idx is not None:
            self._cols.insert(idx, col)
        else:
            self._cols.append(col)
        self._mapFieldNameToCol = None
        return col



    def addHiddenCol(self, col):
        self._hiddenCols.append(col)
        return col


    def addExtCol(self, col, valType, idx=None):
        self._extColsPresent = True
        col.setExternal(True)
        col.setValueType(valType)
        return self.addCol(col, idx)


    def getColIndex(self, fieldName, default=-1):
        if self._mapFieldNameToCol is None:
            self._mapFieldNameToCol = {}
            for i, col in enumerate(self._cols):
                self._mapFieldNameToCol[col.fieldName()] = i
        return self._mapFieldNameToCol.get(fieldName, default)


    def setExtColsPresent(self, val = True):
        self._extColsPresent = val


    def cols(self):
        return self._cols


    def hiddenCols(self):
        return self._hiddenCols


    def clearItems(self):
        self._items = []
        self.reset()


    def setItems(self, items):
        if id(self._items) != id(items):
            self._items = items
            self.reset()


    def items(self):
        return self._items


    def columnCount(self, index=None):
        return len(self._cols)


    def flags(self, index):
        if self.readOnly:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        column = index.column()
        flags = self._cols[column].flags()
        if self.cellReadOnly(index):
            flags = flags & (~Qt.ItemIsEditable) & (~Qt.ItemIsUserCheckable)
        return flags


    def cellReadOnly(self, index):
        return False


    def rowCount(self, index=None):
        return len(self._items)+(1 if self._enableAppendLine else 0)


    def realRowCount(self):
        return len(self._items)


    def getEmptyRecord(self):
        record = QtSql.QSqlRecord()
        return record


    def insertRecord(self, row, record):
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.insert(row, record)
        self.endInsertRows()


    def addRecord(self, record):
        self.insertRecord(len(self._items), record)


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


    def removeRows(self, row, count, parentIndex=QModelIndex()):
        if 0 <= row and row+count <= len(self._items):
            self.beginRemoveRows(parentIndex, row, row+count-1)
            del self._items[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def removeRow(self, row, parentIndex=QModelIndex()):
        return self.removeRows(row, 1, parentIndex)

    
    def getRecordByRow(self, row):
        return self._items[row]
    

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self._items):
            if role == Qt.EditRole:
                col = self._cols[column]
                record = self._items[row]
                return record.value(col.fieldName())

            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self._items[row]
                return col.toString(record.value(col.fieldName()), record)

            if role == Qt.StatusTipRole:
                col = self._cols[column]
                record = self._items[row]
                return col.toStatusTip(record.value(col.fieldName()), record)

            if role == Qt.ToolTipRole and self.getColIndex('system_id') >= 0:
                db = QtGui.qApp.db
                record = db.getRecord('rbAccountingSystem', 'urn', forceString(self.items()[row].value('system_id')))
                if record:
                    result = forceString(record.value('urn'))
                else:
                    result = None
                return result
            elif role == Qt.ToolTipRole and column == self.getColIndex('MKB'):
                return getMKBName(forceString(self.items()[row].value('MKB')))
            elif role == Qt.ToolTipRole and column == self.getColIndex('exSubclassMKB'):
                return getExSubclassItemLastName(forceString(self.items()[row].value('exSubclassMKB')), forceString(self.items()[row].value('MKB')))
            
            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()

            if role == Qt.CheckStateRole:
                col = self._cols[column]
                record = self._items[row]
                return col.toCheckState(record.value(col.fieldName()), record)

            if role == Qt.ForegroundRole:
                col = self._cols[column]
                record = self._items[row]
                return col.getForegroundColor(record.value(col.fieldName()), record)
        else:
            if role == Qt.CheckStateRole:
                flags = self.flags(index)
                if (flags & Qt.ItemIsUserCheckable and flags & Qt.ItemIsEnabled):
                    col = self._cols[column]
                    return col.toCheckState(QVariant(False), None)

        return QVariant()

    def _addEmptyItem(self):
        self._items.append(self.getEmptyRecord())
        count = len(self._items)
        rootIndex = QModelIndex()
        self.beginInsertRows(rootIndex, count, count)
        self.insertRows(count, 1, rootIndex)
        self.endInsertRows()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if row == len(self._items):
                if value.isNull():
                    return False
                self._addEmptyItem()
            record = self._items[row]
            col = self._cols[column]
            record.setValue(col.fieldName(), value)
            self.emitCellChanged(row, column)
            return True
        if role == Qt.CheckStateRole:
            column = index.column()
            row = index.row()
            state = value.toInt()[0]
            if row == len(self._items):
                if state == Qt.Unchecked:
                    return False
                self._addEmptyItem()
            record = self._items[row]
            col = self._cols[column]
            record.setValue(col.fieldName(), QVariant(0 if state == Qt.Unchecked else 1))
            self.emitCellChanged(row, column)
            return True
        return False


    def setValue(self, row, fieldName, value):
        if 0<=row<len(self._items):
            item = self._items[row]
            valueAsVariant = toVariant(value)
            if item.value(fieldName) != valueAsVariant:
                item.setValue(fieldName, valueAsVariant)
                self.emitValueChanged(row, fieldName)


    def value(self, row, fieldName):
        if 0<=row<len(self._items):
            return self._items[row].value(fieldName)
        return None


    def sortData(self, column, ascending):
        col = self._cols[column]
        self._items.sort(key = lambda(item): col.toSortString(item.value(col.fieldName()), item), reverse = not ascending)
        self.emitRowsChanged(0, len(self._items)-1)


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitRowChanged(self, row):
        self.emitRowsChanged(row, row)


    def emitRowsChanged(self, begRow, endRow):
        index1 = self.index(begRow, 0)
        index2 = self.index(endRow, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(), column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitAllChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitValueChanged(self, row, fieldName):
        column = self.getColIndex(fieldName)
        if column>=0:
            self.emitCellChanged(row, column)


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._cols[section].title()
            if role == Qt.ToolTipRole:
                return self._cols[section].toolTip()
            if role == Qt.WhatsThisRole:
                return self._cols[section].whatsThis()

        return QVariant()


    def createEditor(self, index, parent):
        column = index.column()
        if hasattr(self._cols[column], 'setIndex'):
            self._cols[column].setIndex(index)
        return self._cols[column].createEditor(parent)


    def setEditorData(self, column, editor, value, record):
        return self._cols[column].setEditorData(editor, value, record)


    def getEditorData(self, column, editor):
        return self._cols[column].getEditorData(editor)


    def afterUpdateEditorGeometry(self, editor, index):
        pass


class CInDocTableModel(CRecordListModel):
    # модель для взаимодействия со списком QSqlRecord
    # основное назначение: табличная часть документа
    def __init__(self, tableName, idFieldName, masterIdFieldName, parent):
        CRecordListModel.__init__(self, parent)
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

    table = property(lambda self: self._table)
    idFieldName = property(lambda self: self._idFieldName)
    idxFieldName = property(lambda self: self._idxFieldName)
    masterIdFieldName = property(lambda self: self._masterIdFieldName)
    filter = property(lambda self: self._filter)


    def setFilter(self, filter):
        self._filter = filter


    def getTableFieldList(self):
        if self._tableFields is None:
            fields = []
            for col in self._cols:
                if col.external():
                    field = database.CSurrogateField(col.fieldName(), col.valueType())
                else:
                    field = self._table[col.fieldName()]

                fields.append(field)

            fields.append(self._table[self._idFieldName])
            fields.append(self._table[self._masterIdFieldName])
            if self._idxFieldName:
                fields.append(self._table[self._idxFieldName])
            for col in self._hiddenCols:
                field = self._table[col]
                fields.append(field)

            self._tableFields = fields
        return self._tableFields


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
        if self._idxFieldName:
            order = [self._idxFieldName, self._idFieldName]
        else:
            order = [self._idFieldName]
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


    def clearItemIds(self):
        if self._items is not None:
            for item in self._items:
                item.setValue(self._idFieldName, QVariant())


    def itemIdList(self):
        idList = []
        items = self.items()
        if items is not None:
            for item in items:
                idList.append(forceRef(item.value('id')))
        return idList


    def saveDependence(self, idx, id):
        pass


    def saveItems(self, masterId):
        if self._items is not None:
            db = QtGui.qApp.db
            table = self._table
            masterId = toVariant(masterId)
            masterIdFieldName = self._masterIdFieldName
            idFieldName = self._idFieldName
            idList = []
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
                idList.append(id)
                self.saveDependence(idx, id)

            filter = [table[masterIdFieldName].eq(masterId),
                      'NOT ('+table[idFieldName].inlist(idList)+')']
            if self._filter:
                filter.append(self._filter)
            db.deleteRecord(table, filter)


    def removeExtCols(self, srcRecord):
        record = self._table.newRecord()
        for i in xrange(record.count()):
            record.setValue(i, srcRecord.value(record.fieldName(i)))
        return record


    def getEmptyRecord(self):
        record = QtSql.QSqlRecord()
        fields = self.getTableFieldList()
        for field in fields:
            record.append( QtSql.QSqlField(field.field) )
        return record


class CLocItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.row = 0
        self.lastrow = 0
        self.column = 0
        self.editor = None


    def createEditor(self, parent, option, index):
        editor = index.model().createEditor(index, parent)
        self.connect(editor, SIGNAL('commit()'), self.emitCommitData)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
#        self.connect(editor, SIGNAL('activated(int)'), self.emitCommitData)
##        self.connect(self, SIGNAL('closeEditor(QWidget, QAbstractItemDelegate.EndEditHint)'), self.closeEditor)

        self.editor   = editor
        self.row = index.row()
        self.rowcount = index.model().rowCount(None)
        self.column   = index.column()
        return editor


    def setEditorData(self, editor, index):
        if editor is not None:
            column = index.column()
            row    = index.row()
            model  = index.model()
            if row < len(model.items()):
                record = model.items()[row]
            else:
                record = model.table.newRecord() #model.getEmptyRecord() иногда getEmptyRecord сразу сохраняет запись в бд
### БЛЯ! getEmptyRecord НИКОГДА НЕ ДОЛЖЕН СОХРАНЯТЬ ЗАПИСЬ В БД

            model.setEditorData(column, editor, model.data(index, Qt.EditRole), record)


    def setModelData(self, editor, model, index):
        if editor is not None:
            column = index.column()
            model.setData(index, index.model().getEditorData(column, editor))


    def emitCommitData(self):
        self.emit(SIGNAL('commitData(QWidget *)'), self.sender())


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)

#    def closeEditor(self, widget, hint):
#        self.editor = None

    def editorEvent(self, event, model, option, index):
        flags = model.flags(index)
        if not (flags & Qt.ItemIsEnabled and flags & Qt.ItemIsUserCheckable):
            return False

        value = index.data(Qt.CheckStateRole)
        if not value.isValid():
            return False

        if flags & Qt.ItemIsEnabled and flags & Qt.ItemIsEditable:
            return QtGui.QItemDelegate.editorEvent(self, event, model, option, index)

        state = QVariant(Qt.Unchecked if forceInt(value)==Qt.Checked else Qt.Checked)
        eventType = event.type()
#        if eventType == QEvent.MouseButtonDblClick:
#            return model.setData(index, state, Qt.CheckStateRole)

        if eventType == QEvent.MouseButtonRelease:
            if self.parent().hasFocus():
                return model.setData(index, state, Qt.CheckStateRole)
            else:
                return False

        if eventType == QEvent.KeyPress:
            if event.key() in (Qt.Key_Space, Qt.Key_Select):
                return model.setData(index, state, Qt.CheckStateRole)
        return QtGui.QItemDelegate.editorEvent(self, event, model, option, index)


    def eventFilter(self, object, event):
        def editorIsEmpty():
            if isinstance(self.editor, QtGui.QLineEdit):
                return self.editor.text() == ''
            if  isinstance(self.editor, QtGui.QComboBox):
                return self.editor.currentIndex() == 0
            if  isinstance(self.editor, CDateEdit):
                return not self.editor.dateIsChanged()
            if  isinstance(self.editor, QtGui.QDateEdit):
                return not self.editor.date().isValid()
            return False

        def editorCanEatTab():
            if  isinstance(self.editor, QtGui.QDateEdit):
                return self.editor.currentSection() != QtGui.QDateTimeEdit.YearSection
            return False

        def editorCanEatBacktab():
            if isinstance(self.editor, QtGui.QDateEdit):
                return self.editor.currentSection() != QtGui.QDateTimeEdit.DaySection
            return False

#        def editIfTableView():
#            focused = self.parent().focusWidget()
#            if isinstance(focused, CInDocTableView):
#                index = focused.currentIndex()
#                if index.isValid():
#                    focused.edit(index)

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Tab:
                if editorCanEatTab():
                    self.editor.keyPressEvent(event)
                    return True
                if self.editor is not None and hasattr(self.parent(), 'commitData'):
                    self.parent().commitData(self.editor)
                self.parent().keyPressEvent(event)
                return True
            elif event.key() == Qt.Key_Backtab:
                if editorCanEatBacktab():
                    self.editor.keyPressEvent(event)
                    return True
                if self.editor is not None:
                    self.parent().commitData(self.editor)
                self.parent().keyPressEvent(event)
                return True
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
##                event.accept()
                return True
        return QtGui.QItemDelegate.eventFilter(self, object, event)

    def updateEditorGeometry(self, editor, option, index):
        QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index)
        index.model().afterUpdateEditorGeometry(editor, index)


class CInDocTableView(QtGui.QTableView, CPreferencesMixin, CColsMovingFeature):

    __pyqtSignals__ = ('popupMenuAboutToShow()',
                      )

    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        self._popupMenu = None

        h = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.verticalHeader().hide()

        self.setShowGrid(True)
#        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setItemDelegate(CLocItemDelegate(self))
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.setTabKeyNavigation(True)
#        self.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed | QtGui.QAbstractItemView.EditKeyPressed | QtGui.QAbstractItemView.SelectedClicked | QtGui.QAbstractItemView.DoubleClicked)
        self.setFocusPolicy(Qt.StrongFocus)
        self.__actUpRow = None
        self.__actDownRow = None
        self.__actDeleteRows = None
        self.__actSelectAllRow = None
        self.__actSelectRowsByData = None
        self.__actCheckedAllRow = None
        self.__actClearCheckedAllRow = None
        self.__actDuplicateCurrentRow = None
        self.__actAddFromReportRow = None
        self.__actDuplicateSelectRows = None
        self.__actClearSelectionRow = None
        self.__actRecordProperties = None
        self.__sortColumn = None
        self.__sortAscending = False
        self.__delRowsChecker = None
        self.__delRowsIsExposed = None
        self.__actionsWithCheckers = []
        self.__dropColsPreferences = False
        self.rbTable = None
        self.connect( self.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.on_sortByColumn)

        # Это для обхода ошибки в Qt/PyQt/sip в AltLinux6.
        # Она проявляется в том, что вертикальный заголовок при изменении
        # (уменьшении) числа строк перестаёт обновляться.
        self.connect( self.verticalHeader(), SIGNAL('sectionCountChanged(int,int)'), self.on_rowsCountChanged)


    def setSelectionModel(self, selectionModel):
        currSelectionModel = self.selectionModel()
        if currSelectionModel:
            self.disconnect(currSelectionModel, SIGNAL('currentChanged(QModelIndex,QModelIndex))'), self.currentChanged)
        QtGui.QTableView.setSelectionModel(self, selectionModel)
        if selectionModel:
            self.connect(selectionModel, SIGNAL('currentChanged(QModelIndex,QModelIndex))'), self.currentChanged)


    def setActionsWithCheckers(self, actionsWithCheckers):
        self.__actionsWithCheckers = actionsWithCheckers


    def createPopupMenu(self, actions=[]):
        menu = QtGui.QMenu(self)
        menu.setObjectName('popupMenu')
        self.setPopupMenu(menu)
        if actions:
            self.addPopupActions(actions)
        return self._popupMenu


    def setPopupMenu(self, menu):
        if self._popupMenu:
            self.disconnect(self._popupMenu, SIGNAL('aboutToShow()'), self.on_popupMenu_aboutToShow)
        self._popupMenu = menu
        if menu:
            self.connect(menu, SIGNAL('aboutToShow()'), self.on_popupMenu_aboutToShow)


    def popupMenu(self):
        return self._popupMenu if self._popupMenu else self.createPopupMenu()


    def addPopupSeparator(self):
        self.popupMenu().addSeparator()


    def addPopupAction(self, action):
        self.popupMenu().addAction(action)


    def addPopupActions(self, actions):
        menu = self.popupMenu()
        for action in actions:
            if isinstance(action, QtGui.QAction):
                menu.addAction(action)
            elif action == '-':
                menu.addSeparator()


    def addMoveRow(self):
#        if self.model().idxFieldName:
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actUpRow = QtGui.QAction(u'Поднять строку', self)
        self.__actUpRow.setObjectName('actUpRow')
        self.__actUpRow.setShortcut('Ctrl+Shift+Up')
        self.__actUpRow.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actUpRow)
        self.addAction(self.__actUpRow)
        self.connect(self.__actUpRow, SIGNAL('triggered()'), self.on_upRow)
        self.__actDownRow = QtGui.QAction(u'Опустить строку', self)
        self.__actDownRow.setObjectName('actDownRow')
        self.__actDownRow.setShortcut('Ctrl+Shift+Down')
        self.__actDownRow.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actDownRow)
        self.addAction(self.__actDownRow)
        self.connect(self.__actDownRow, SIGNAL('triggered()'), self.on_downRow)


    def addPopupDelRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actDeleteRows = QtGui.QAction(u'Удалить строку', self)
        self.__actDeleteRows.setObjectName('actDeleteRows')
        self._popupMenu.addAction(self.__actDeleteRows)
        self.connect(self.__actDeleteRows, SIGNAL('triggered()'), self.on_deleteRows)


    def addPopupSelectAllRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actSelectAllRow = QtGui.QAction(u'Выделить все строки', self)
        self.__actSelectAllRow.setObjectName('actSelectAllRow')
        self._popupMenu.addAction(self.__actSelectAllRow)
        self.connect(self.__actSelectAllRow, SIGNAL('triggered()'), self.on_selectAllRow)


    def addPopupSelectRowsByData(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actSelectRowsByData = QtGui.QAction(u'Выделить строки соответствующие текущему столбцу', self)
        self.__actSelectRowsByData.setObjectName('actSelectRowsByDate')
        self._popupMenu.addAction(self.__actSelectRowsByData)
        self.connect(self.__actSelectRowsByData, SIGNAL('triggered()'), self.on_selectRowsByData)


    def addPopupClearSelectionRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actClearSelectionRow = QtGui.QAction(u'Снять выделение', self)
        self.__actClearSelectionRow.setObjectName('actClearSelectionRow')
        self._popupMenu.addAction(self.__actClearSelectionRow)
        self.connect(self.__actClearSelectionRow, SIGNAL('triggered()'), self.on_clearSelectionRow)


    def addPopupCheckedAllRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actCheckedAllRow = QtGui.QAction(u'Выбрать всё', self)
        self.__actCheckedAllRow.setObjectName('actCheckedAllRow')
        self._popupMenu.addAction(self.__actCheckedAllRow)
        self.connect(self.__actCheckedAllRow, SIGNAL('triggered()'), self.on_checkedAllRow)


    def addPopupClearCheckedAllRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actClearCheckedAllRow = QtGui.QAction(u'Отменить выбор', self)
        self.__actClearCheckedAllRow.setObjectName('actClearCheckedAllRow')
        self._popupMenu.addAction(self.__actClearCheckedAllRow)
        self.connect(self.__actClearCheckedAllRow, SIGNAL('triggered()'), self.on_clearCheckedAllRow)


    def addPopupRecordProperies(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actRecordProperties = QtGui.QAction(u'Свойства записи', self)
        self.__actRecordProperties.setObjectName('actRecordProperties')
        self._popupMenu.addAction(self.__actRecordProperties)
        self.connect(self.__actRecordProperties, SIGNAL('triggered()'), self.showRecordProperties)


    def addPopupDuplicateCurrentRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actDuplicateCurrentRow = QtGui.QAction(u'Дублировать строку', self)
        self.__actDuplicateCurrentRow.setObjectName('actDuplicateCurrentRow')
        self._popupMenu.addAction(self.__actDuplicateCurrentRow)
        self.connect(self.__actDuplicateCurrentRow, SIGNAL('triggered()'), self.on_duplicateCurrentRow)


    def addPopupDuplicateSelectRows(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actDuplicateSelectRows = QtGui.QAction(u'Дублировать выделенные строки', self)
        self.__actDuplicateSelectRows.setObjectName('actDuplicateSelectRows')
        self._popupMenu.addAction(self.__actDuplicateSelectRows)
        self.connect(self.__actDuplicateSelectRows, SIGNAL('triggered()'), self.on_duplicateSelectRows)


#    def setPopupMenu(self, menu):
#        self._popupMenu = menu
#
#
#    def popupMenu(self):
#        if self._popupMenu is None:
#            self.createPopupMenu()
#        return self._popupMenu


    def setDelRowsChecker(self, func):
        self.__delRowsChecker = func


    def setDelRowsIsExposed(self, func):
        self.__delRowsIsExposed = func


    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Escape, Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
#        elif key == Qt.Key_Return or key == Qt.Key_Enter:
#            event.ignore()
        elif event.key() == Qt.Key_Tab:
            if event.modifiers() & Qt.ControlModifier:
                event.ignore()
            else:
                index = self.currentIndex()
                model = self.model()
                if index.row() == model.rowCount()-1 and index.column() == model.columnCount()-1:
                    self.parent().focusNextChild()
                    event.accept()
                else:
                    QtGui.QTableView.keyPressEvent(self, event)
        elif event.key() == Qt.Key_Backtab:
            if event.modifiers() & Qt.ControlModifier:
                event.ignore()
            else:
                index = self.currentIndex()
                if index.row() == 0 and index.column() == 0:
                    self.parent().focusPreviousChild()
                    event.accept()
                else:
                    QtGui.QTableView.keyPressEvent(self, event)
        else:
            QtGui.QTableView.keyPressEvent(self, event)


    def focusInEvent(self, event):
        reason = event.reason()
        model = self.model()
        if reason in (Qt.TabFocusReason, Qt.ShortcutFocusReason, Qt.OtherFocusReason):
            if not self.hasFocus():
                self.setCurrentIndex(model.index(0, 0))
        elif reason == Qt.BacktabFocusReason:
            if not self.hasFocus():
                self.setCurrentIndex(model.index(model.rowCount()-1, model.columnCount()-1))
        QtGui.QTableView.focusInEvent(self, event)
        self.updateStatusTip(self.currentIndex())


    def focusOutEvent(self, event):
        self.updateStatusTip(None)
        QtGui.QTableView.focusOutEvent(self, event)


    def closeEditor(self, editor, hint):
        if hasattr(editor, 'deletePopup'):
            editor.deletePopup()
        QtGui.QTableView.closeEditor(self, editor, hint)


    def removeCurrentRow(self):
        index = self.currentIndex()
        if index.isValid():
            row = index.row()
            self.model().removeRow(row)


    def contextMenuEvent(self, event): # event: QContextMenuEvent
        if self._popupMenu:
            self._popupMenu.exec_(event.globalPos())
            event.accept()
        else:
            event.ignore()


    def colKey(self, col):
        return unicode('width '+forceString(col.title()))


    def getSelectedRows(self):
#        model = self.model()
#        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
        rowCount = len(self.model().items())
        selectionBehavior = self.selectionBehavior()
        if selectionBehavior == self.SelectRows:
            rowSet = set(index.row() for index in self.selectionModel().selectedRows() if 0<=index.row()<rowCount)
        else:
            rowSet = set(index.row() for index in self.selectionModel().selectedIndexes() if 0<=index.row()<rowCount)
        result = list(rowSet)
        result.sort()
        return result


    def getSelectedItems(self):
        items = self.model().items()
        return [items[row] for row in self.getSelectedRows()]


    def on_popupMenu_aboutToShow(self):
        model = self.model()
        isReadOnly = model.getReadOnly()
        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
        row = self.currentIndex().row()
        if self.__actUpRow:
            self.__actUpRow.setEnabled(0<row<rowCount and not isReadOnly)
        if self.__actDownRow:
            self.__actDownRow.setEnabled(0<=row<rowCount-1 and not isReadOnly)
        if self.__actDuplicateCurrentRow:
            self.__actDuplicateCurrentRow.setEnabled(0<=row<rowCount and not isReadOnly)
        if self.__actAddFromReportRow:
            self.__actAddFromReportRow.setEnabled(rowCount <= 0 and not isReadOnly)
        if self.__actDeleteRows:
            rows = self.getSelectedRows()
            canDeleteRow = bool(rows)
            if canDeleteRow and self.__delRowsChecker:
                canDeleteRow = self.__delRowsChecker(rows)
            if len(rows) == 1 and rows[0] == row:
                self.__actDeleteRows.setText(u'Удалить текущую строку')
            elif len(rows) == 1:
                self.__actDeleteRows.setText(u'Удалить выделенную строку')
            else:
                self.__actDeleteRows.setText(u'Удалить выделенные строки')
            if canDeleteRow and self.__delRowsIsExposed:
                canDeleteRow = self.__delRowsIsExposed(rows)
            self.__actDeleteRows.setEnabled(canDeleteRow and not isReadOnly)
            if self.__actDuplicateSelectRows:
                self.__actDuplicateSelectRows.setEnabled(canDeleteRow and not isReadOnly)
        if self.__actSelectAllRow:
            self.__actSelectAllRow.setEnabled(0<=row<rowCount and not isReadOnly)
        if self.__actSelectRowsByData:
            column = self.currentIndex().column()
            items = self.model().items()
            value = items[row].value(column) if row < len(items) else None
            self.__actSelectRowsByData.setEnabled(forceBool(0<=row<rowCount and (value and value.isValid())) and not isReadOnly)
        if self.__actClearSelectionRow:
            self.__actClearSelectionRow.setEnabled(0<=row<rowCount and not isReadOnly)
        if self.__actCheckedAllRow:
            self.__actCheckedAllRow.setEnabled(0<=row<rowCount and not isReadOnly)
        if self.__actClearCheckedAllRow:
            self.__actClearCheckedAllRow.setEnabled(0<=row<rowCount and not isReadOnly)
        if self.__actRecordProperties:
            self.__actRecordProperties.setEnabled(0<=row<rowCount and not isReadOnly)
        for act, checker in self.__actionsWithCheckers:
            act.setEnabled(checker() and not isReadOnly)
        self.emit(SIGNAL('popupMenuAboutToShow()'))


    def on_upRow(self):
        index = self.currentIndex()
        if index.isValid():
            row = index.row()
            if self.model().upRow(row):
                self.setCurrentIndex(self.model().index(row-1, index.column()))
                self.resetSorting()


    def on_downRow(self):
        index = self.currentIndex()
        if index.isValid():
            row = index.row()
            if self.model().downRow(row):
                self.setCurrentIndex(self.model().index(row+1, index.column()))
                self.resetSorting()


    def on_deleteRows(self):
        rows = self.getSelectedRows()
        for row in reversed(rows): # getSelectedRows уже отсортирован!
            self.model().removeRow(row)
#        self.removeCurrentRow()
        model = self.model()
        isReadOnly = model.getReadOnly()
        if self.__actUpRow:
            self.__actUpRow.setEnabled(not isReadOnly)
        if self.__actDownRow:
            self.__actDownRow.setEnabled(not isReadOnly)


    def on_selectAllRow(self):
        self.selectAll()


    def on_selectRowsByData(self):
        items = self.model().items()
        currentRow = self.currentIndex().row()
        if currentRow < len(items):
            currentColumn = self.currentIndex().column()
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            currentRecord = items[currentRow]
            data = currentRecord.value(currentColumn)
            if data.isValid():
                for row, item in enumerate(items):
                    if (item.value(currentColumn) == data) and (row not in selectRowList):
                        self.selectRow(row)


    def on_duplicateCurrentRow(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            newRecord = self.model().getEmptyRecord()
            copyFields(newRecord, items[currentRow])
            newRecord.setValue(self.model()._idFieldName, toVariant(None))
            self.model().insertRecord(currentRow+1, newRecord)


    def on_duplicateSelectRows(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            selectRowList.sort()
            for row in selectRowList:
                newRecord = self.model().getEmptyRecord()
                copyFields(newRecord, items[row])
                newRecord.setValue(self.model()._idFieldName, toVariant(None))
                items.append(newRecord)
            self.model().reset()


    def on_clearSelectionRow(self):
        self.clearSelection()


    def on_checkedAllRow(self):
        items = self.model().items()
        for row, record in items.items():
            record.setValue('include', toVariant(2))
            items[row] = record


    def on_selectCheckedRows(self):
        items = self.model().items()
        for row, record in enumerate(items):
            if forceBool(record.value('include')):
                self.selectRow(row)


    def on_clearSelectionCheckedRow(self):
        selectRowList = []
        items = self.model().items()
        selectIndexes = self.selectedIndexes()
        for selectIndex in selectIndexes:
            selectRow = selectIndex.row()
            record = items[selectRow]
            if selectRow not in selectRowList and not forceBool(record.value('include')):
                selectRowList.append(selectRow)
        self.clearSelection()
        for row in selectRowList:
            self.selectRow(row)


    def on_clearCheckedAllRow(self):
        items = self.model().items()
        for row, record in items.items():
            record.setValue('include', toVariant(0))
            items[row] = record


    def showRecordProperties(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            itemId = forceRef(items[currentRow].value('id'))
        else:
            return
        table = self.model().table
        CRecordProperties(self, table, itemId).exec_()


    def setCurrentRow(self, row):
        currentIndex = self.currentIndex()
        self.setCurrentIndex(self.model().index(row, currentIndex.column() if currentIndex.isValid() else 0))


    def setSortColumn(self, sortColumn):
        self.__sortColumn = sortColumn


    def setSortAscending(self, sortAscending):
        self.__sortAscending = sortAscending


    def getSortColumn(self):
        return self.__sortColumn


    def getSortAscending(self):
        return self.__sortAscending


    def resetSorting(self):
        self.horizontalHeader().setSortIndicatorShown(False)
        self.__sortColumn = None

# мне не хочется возиться с proxy model - я принял решение сортировать в модели.
# возможны побочные эффекты, но я думаю забить на это...
    def on_sortByColumn(self, logicalIndex):
        currentIndex = self.currentIndex()
        currentItem = self.currentItem()
        model = self.model()
        if isinstance(model, CRecordListModel):
            header=self.horizontalHeader()
            if model.cols()[logicalIndex].sortable():
                if self.__sortColumn == logicalIndex:
                    self.__sortAscending = not self.__sortAscending
                else:
                    self.__sortColumn = logicalIndex
                    self.__sortAscending = True
                header.setSortIndicatorShown(True)
                header.setSortIndicator(self.__sortColumn, Qt.AscendingOrder if self.__sortAscending else Qt.DescendingOrder)
                model.sortData(logicalIndex, self.__sortAscending)
            elif self.__sortColumn is not None:
                header.setSortIndicator(self.__sortColumn, Qt.AscendingOrder if self.__sortAscending else Qt.DescendingOrder)
            else:
                header.setSortIndicatorShown(False)
            if currentItem:
                newRow = model.items().index(currentItem)
                self.setCurrentIndex(model.index(newRow, currentIndex.column()))
            else:
                self.setCurrentIndex(model.index(0, 0))
        else: # для QSortFilterProxyModel и др.
            header=self.horizontalHeader()
            if self.__sortColumn == logicalIndex:
                self.__sortAscending = not self.__sortAscending
            else:
                self.__sortColumn = logicalIndex
                self.__sortAscending = True
            sortOrder = Qt.AscendingOrder if self.__sortAscending else Qt.DescendingOrder
            header.setSortIndicatorShown(True)
            header.setSortIndicator(self.__sortColumn, sortOrder)
            model.sort(logicalIndex, sortOrder)


    # Это для обхода ошибки в Qt/PyQt/sip в AltLinux6.
    # Она проявляется в том, что вертикальный заголовок при изменении
    # (уменьшении) числа строк перестаёт обновляться.

    def on_rowsCountChanged(self, oldCount, newCount):
        vh = self.verticalHeader()
        if vh.isVisible() and oldCount>newCount:
            vh.setUpdatesEnabled(True)
            #vh.update()


    def resizeTableHorizontalHeaderLoc(self):
        for column in range(self.horizontalHeader().count()):
            text = self.model().headerData(column, orientation=Qt.Horizontal, role=Qt.DisplayRole).toString()
            fm = QtGui.QFontMetrics(QtGui.QFont(text))
            width = fm.width(text)
            self.horizontalHeader().resizeSection(column, width)


    def loadPreferences(self, preferences):
        model = self.model()
        if hasattr(model, 'sourceModel'):
            model = model.sourceModel()
        if isinstance(model, (CInDocTableModel, CRecordListModel)):
            charWidth = self.fontMetrics().width('A0')/2
            cols = model.cols()
            i = 0
            for column, col in enumerate(cols):
                widthField = col.width() * charWidth
                text = model.headerData(column, orientation=Qt.Horizontal, role=Qt.DisplayRole).toString()
                if text:
                    fm = QtGui.QFontMetrics(QtGui.QFont(text))
                    widthCol = fm.width(text)
                    if widthCol:
                        widthField = widthCol
                width = forceInt(getPref(preferences, self.colKey(col), widthField))
                if width:
                    self.setColumnWidth(i, width)
                i += 1
        self.horizontalHeader().setStretchLastSection(True)
        state = getPref(preferences, 'headerState', QVariant()).toByteArray()
        if state:
            header = self.horizontalHeader()
            try:
                state = json.loads(forceString(state))
            except:
                header.restoreState(state)
                return
            maxVIndex = 0
            colsLen = len(model.cols())
            for i, col in enumerate(model.cols()):
                name = forceString(col.title())
                curVIndex = header.visualIndex(i)
                if name in state:
                    vIndex = state[name][0]
                    isHidden = state[name][1]
                    if vIndex > maxVIndex:
                        maxVIndex = vIndex
                    if vIndex != curVIndex:
                        header.moveSection(curVIndex, vIndex)
                    if isHidden:
                        header.setSectionHidden(i, True)
                else:
                    header.moveSection(curVIndex, colsLen-1)

    def savePreferences(self):
        preferences = {}
        model = self.model()
        if hasattr(model, 'sourceModel'):
            model = model.sourceModel()
        if isinstance(model, (CInDocTableModel, CRecordListModel)):
            cols = model.cols()
            i = 0
            for col in cols:
                width = self.columnWidth(i)
                setPref(preferences, self.colKey(col), QVariant(width))
                i += 1
        header = self.horizontalHeader()
        if header.isMovable() or self.headerColsHidingAvailable():
            params = {}
            needSave = False
            for i, col in enumerate(model.cols()):
                if i != header.visualIndex(i)  or header.isSectionHidden(i):
                    needSave = True
                    break
            if needSave:
                for i, col in enumerate(model.cols()):
                    name = forceString(col.title())
                    params[name] = (header.visualIndex(i), header.isSectionHidden(i))
            setPref(preferences, 'headerState', QVariant(json.dumps(params)))
        return preferences


    def updateStatusTip(self, index):
        tip = forceString(index.data(Qt.StatusTipRole)) if index else ''
        event = QtGui.QStatusTipEvent(tip)
        QtGui.qApp.sendEvent(self, event)


    def currentChanged(self, current, previous):
        QtGui.QTableView.currentChanged(self, current, previous)
        self.updateStatusTip(current)


    def currentItem(self):
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            if isinstance(model, (CInDocTableModel, CRecordListModel)):
                row = index.row()
                if 0 <= row < len(model.items()):
                   return model.items()[row]
        return None


    def addContentToTextCursor(self, cursor):
        model = self.model()
        cols = model.cols()
#        cursor.movePosition(QtGui.QTextCursor.End)
        colWidths  = [ self.columnWidth(i) for i in xrange(len(cols)) ]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        alignRight = CReportBase.AlignRight
        alignLeft = CReportBase.AlignLeft
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iCol == 0:
                tableColumns.append((widthInPercents, [u'№'], alignRight))
            else:
                col = cols[iCol-1]
#                format = QtGui.QTextBlockFormat()
#                format.setAlignment(alignLeft)
                tableColumns.append((widthInPercents, [forceString(col.title())], alignLeft))

        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(model.rowCount()):
            QtGui.qApp.processEvents(QEventLoop.ExcludeUserInputEvents)
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            iTableCol = 1
            for iModelCol in xrange(len(cols)):
                index = model.createIndex(iModelRow, iModelCol)
                text = forceString(model.data(index))
                table.setText(iTableRow, iTableCol, text)
                iTableCol += 1


# WTF? модель не должна зависеть от типа столбцов!
# это какая-то ошибка!
# обоснование: если таких специфических столбцов будет 10, то нужно будет 1024 моделей, да?
class CMKBListInDocTableModel(CInDocTableModel):
    def __init__(self, tableName, idFieldName, masterIdFieldName, parent):
        CInDocTableModel.__init__(self, tableName, idFieldName, masterIdFieldName, parent)


    def createEditor(self, index, parent):
        column = index.column()
        row = index.row()
        editor = self._cols[column].createEditor(parent)
        colMKB = self.getColIndex('MKB')
        colMKBEx = self.getColIndex('MKBEx')
        colTNMS = self.getColIndex('TNMS',  None)
        colExSubclassMKB = self.getColIndex('exSubclassMKB',  None)
        eventEditor = None
        if column>=0 and  (colMKB == column or colMKBEx == column):
            if hasattr(self, '_parent'):
                eventEditor = self._parent
            elif hasattr(self, 'eventEditor'):
                eventEditor = self.eventEditor
            if eventEditor:
                filter = []
                if self.eventEditor.__class__.__name__ == 'CF131Dialog':
                    diagFilter = self.eventEditor.getDiagFilter(self.specialityId(row))
                else:
                    diagFilter = self.eventEditor.getDiagFilter()
                if diagFilter:
                    filter.append("INSTR('{0}', substr(MKB.DiagId, 1, 1)) = 0".format(diagFilter))
                if hasattr(eventEditor, 'edtBegDate'):
                    begDate = eventEditor.edtBegDate.date()
                    filter.append('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(begDate)))
                elif hasattr(eventEditor, 'edtAPBegDate'):
                    begDate = eventEditor.edtAPBegDate.date()
                    filter.append('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(begDate)))
                elif hasattr(eventEditor, 'modelPeriods'):
                    items = eventEditor.modelPeriods.items()
                    if len(items) > 0:
                        begDate = forceDate(items[0].value('begDate'))
                        filter.append('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(begDate)))
                editor.setFilter(QtGui.qApp.db.joinAnd(filter))
                if hasattr(eventEditor, 'isLUDSelected') and hasattr(eventEditor, 'clientId'):
                    editor.setLUDEnabled(bool(eventEditor.clientId))
                    editor.setLUDChecked(eventEditor.isLUDSelected, eventEditor.clientId)
        elif QtGui.qApp.isTNMSVisible() and column >= 0 and column == colTNMS:
            row = index.row()
            if 0 <= row < len(self.items()):
                editor.setMKB(forceString(self.items()[row].value('MKB')))
                if hasattr(self, 'eventEditor'):
                    date = None
                    if hasattr(self.eventEditor, 'edtEndDate'):
                        endDate = self.eventEditor.edtEndDate.date()
                        if endDate:
                            date = endDate
                        elif hasattr(self.eventEditor, 'edtBegDate'):
                            begDate = self.eventEditor.edtBegDate.date()
                            if begDate:
                                date = begDate
                    elif hasattr(self.eventEditor, 'edtBegDate'):
                        begDate = self.eventEditor.edtBegDate.date()
                        if begDate:
                            date = begDate
                    if date:
                        editor.setEndDate(date)
        elif QtGui.qApp.isExSubclassMKBVisible() and (colExSubclassMKB is not None and column == colExSubclassMKB):
            row = index.row()
            if 0 <= row < len(self.items()):
                editor.setMKB(forceString(self.items()[row].value('MKB')))
        elif QtGui.qApp.isTNMSVisible() and (colTNMS is not None and column == colTNMS):
            row = index.row()
            if 0 <= row < len(self.items()):
                editor.setMKB(forceString(self.items()[row].value('MKB')))
                if hasattr(self, '_parent'):
                    eventEditor = self._parent
                elif hasattr(self, 'eventEditor'):
                    eventEditor = self.eventEditor
                else:
                    eventEditor = QObject.parent(self) # для 131 формы
                if eventEditor:
                    date = None
                    if hasattr(eventEditor, 'edtEndDate'):
                        endDate = eventEditor.edtEndDate.date()
                        if endDate:
                            date = endDate
                        elif hasattr(eventEditor, 'edtBegDate'):
                            begDate = eventEditor.edtBegDate.date()
                            if begDate:
                                date = begDate
                    elif hasattr(eventEditor, 'edtBegDate'):
                        begDate = eventEditor.edtBegDate.date()
                        if begDate:
                            date = begDate
                    if date:
                        editor.setEndDate(date)
        elif QtGui.qApp.isExSubclassMKBVisible() and column>=0 and column == colExSubclassMKB:
            row = index.row()
            if 0 <= row < len(self.items()):
                editor.setMKB(forceString(self.items()[row].value('MKB')))
        return editor

# WTF?
class CDentitionInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.eventEditor = None


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def on_deleteRows(self):
        rows = self.getSelectedRows()
        rows.sort(reverse=True)
        items = self.model().items()
        for row in rows:
            if items and row >= 0 and len(items) > row:
                item = items[row]
                if item:
                    personId = forceRef(item.value('person_id'))
                    date = forceDateTime(item.value('date'))
                    eventId = forceRef(item.value('event_id'))
                    if not eventId:
                        eventId = self.eventEditor.itemId()
                    visitId = forceRef(item.value('id'))
                    dentitionHistoryRow = self.eventEditor.modelClientDentitionHistory.getDentitionHistoryRow(eventId, visitId, personId, date)
                    if dentitionHistoryRow is not None:
                        self.eventEditor.modelClientDentitionHistory._dentitionHistoryItems.pop(dentitionHistoryRow)
                        self.eventEditor.modelClientDentitionHistory._resultDentitionHistoryItems.pop(dentitionHistoryRow)
                        resDent = self.eventEditor.actionDentitionList.pop((date.toPyDateTime(), personId, eventId), None)
                        resParodent = self.eventEditor.actionParodentiumList.pop((date.toPyDateTime(), personId, eventId), None)
                        if resDent is not None and resParodent is not None:
                            for row in rows:
                                self.model().removeRow(row)
                        dentActionTypeId, parodentActionTypeId = getDentitionActionTypeId()
                        actionTypeDentIdList = []
                        if dentActionTypeId:
                            actionTypeDentIdList.append(dentActionTypeId)
                        if parodentActionTypeId:
                            actionTypeDentIdList.append(parodentActionTypeId)
                        for model in (self.eventEditor.tabStatus.modelAPActions,
                                      self.eventEditor.tabDiagnostic.modelAPActions,
                                      self.eventEditor.tabCure.modelAPActions,
                                      self.eventEditor.tabMisc.modelAPActions):
                            if dentActionTypeId in model.actionTypeIdList or parodentActionTypeId in model.actionTypeIdList:
                                actionItems = model.items()
                                for actionRow, (record, action) in enumerate(actionItems):
                                    actionTypeId = forceRef(record.value('actionType_id'))
                                    if actionTypeId in actionTypeDentIdList:
                                        actionPersonId = forceRef(record.value('person_id'))
                                        actionBegDate  = forceDateTime(record.value('begDate'))
                                        actionEventId  = forceRef(record.value('event_id'))
                                        if not actionEventId:
                                            actionEventId = self.eventEditor.itemId()
                                        actionVisitId  = forceRef(record.value('visit_id'))
                                        if eventId == actionEventId and visitId == actionVisitId and personId == actionPersonId and date == actionBegDate:
                                            model.removeRows(actionRow, 1)
                        self.eventEditor.modelClientDentitionHistory.reset()

