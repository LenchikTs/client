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
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QLocale, QVariant

from decimal import Decimal, Context

from library.PreferencesMixin import CPreferencesMixin
from library.Utils import forceDouble, forceInt, forceString, forceStringEx, smartDict, trim

FiledType = smartDict()
FiledType.PercentType = '%'
FiledType.GlobalType  = 'A'

groupList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D']

class CLaboratoryCalculatorTableModel(QAbstractTableModel):
    horizontalHeaders = [u'Имя свойства(А)', u'K', u'Сумма', u'А', u'%', u'Имя свойства(%)', u'Группа']
    fields        = [('name(A)', QVariant.String),
                     ('K', QVariant.Int),
                     ('Sum', QVariant.Int),
                     ('A', QVariant.Double),
                     ('%', QVariant.Double),
                     ('name(%)', QVariant.String),
                     ('group', QVariant.String)]

    ciPropNameGlobal  = 0
    ciGlobalCount     = 1
    ciGroupSumm       = 2
    ciAL     = 3
    ciPercentCount    = 4
    ciPropNamePercent = 5

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._parent = parent
        self.clear()
        self.resetAdditional(False)
        self._inputData = None
        self._maxGroupValue = 100
        self._rounding = 0
        self._locale = QLocale()


        self._historyPointer = 0
        self._history = []
        self._needToSave = False
        self._onHistoryPointer = True
        self.leukocytesPropId = None
        self.ggPropId = None
        self.eePropId = None
        self.ciPropId = None

        self._emptyItem = smartDict(
                                    items=[],
                                    mapKeyToRow={},
                                    mapGroupToRows={},
                                    mapNameToRow={},
                                    mapRowToGroup={},
                                    mapRowToButtonKey={},
                                    mapPropertyTypeIdToCoords={}
                                   )
        self._history.append(self._emptyItem)

    def setRounding(self, rounding):
        self._rounding = rounding

    def load(self, data):
        if data:
            self._inputData = data
            self.clear()
            for value in data.split(';'):
                value = trim(value).strip('()').split(',')
                itemValues = int(value[0]), value[1], value[2]
                if itemValues[1][:3] == 'LL*':
                    self.addLL(itemValues[1][3:], itemValues[0])
                    continue
                if itemValues[1][:3] == 'GG*':
                    self.addGG(itemValues[1][3:], itemValues[0])
                    continue
                if itemValues[1][:3] == 'EE*':
                    self.addEE(itemValues[1][3:], itemValues[0])
                    continue
                if itemValues[1][:3] == 'CI*':
                    self.addCI(itemValues[1][3:], itemValues[0])
                    continue
                self._fullStruct.append(itemValues)
            self._fullStruct.sort(key=lambda item: item[1][2]) # сортирует по группам
        self.addItems()
        if self._additionalItems:
            for item in self._additionalItems:
                item.setValue('A', QVariant())
                item.setValue('Sum', QVariant())
                item.setValue('%', QVariant())
        self.reset()

    def acceptKeys(self):
        self._parent.enabledKeys(self._mapKeyToRow.keys())


    def hasOuterItems(self):
        return bool(len(self._items))

    def addLL(self, value, proptypeId):
        try:
            value = float(value)
        except:
            value = 0
        self.leukocytesPropId = proptypeId
        if value:
            self._parent.edtLeukocytes.setValue(value)
            self._parent.edtLeukocytes.setEnabled(False)
            self._parent.lblLeukocytes.setEnabled(False)

    def addGG(self, value, proptypeId):
        try:
            value = float(value)
        except:
            value = 0
        self.ggPropId = proptypeId
        if value:
            self._parent.edtGG.setValue(value)
            self._parent.edtGG.setEnabled(False)
            self._parent.lblGG.setEnabled(False)

    def addEE(self, value, proptypeId):
        try:
            value = float(value)
        except:
            value = 0
        self.eePropId = proptypeId
        if value:
            self._parent.edtEE.setValue(value)
            self._parent.edtEE.setEnabled(False)
            self._parent.lblEE.setEnabled(False)

    def addCI(self, value, proptypeId):
        self.ciPropId = proptypeId

    def addItems(self):
        for itemValues in self._fullStruct:
            self.addItem(itemValues)
        self.acceptKeys()

    def addItem(self, values):
        propertyTypeId, settings, propertyTypeName = values
        buttonKey = settings[0]
        fieldNameType = settings[1]
        group = settings[2]
        column = 3 if fieldNameType == 'A' else 4
        #if propertyTypeName in self._mapNameToRow.keys():
        if buttonKey in self._mapKeyToRow.keys():
            #row = self._mapNameToRow[propertyTypeName]
            row = self._mapKeyToRow[buttonKey][0][0]
            item = self._items[row]
        else:
            item = self.getNewRecord()
            self._items.append(item)
            row = len(self._items)-1
            self._mapNameToRow[propertyTypeName] = row
            result = self._mapGroupToRows.setdefault(group, [row])
            self._mapRowToGroup[row] = group
            if row not in result:
                result.append(row)

        self.mapKeyToRow(buttonKey, row, fieldNameType)

        valueCords = (row, column)
        self._mapPropertyTypeIdToCoords[propertyTypeId] = valueCords

        buttonKeyList = self._mapRowToButtonKey.setdefault(row, [buttonKey])
        if buttonKey not in buttonKeyList:
            buttonKeyList.append(buttonKey)

        existsGroupValue = forceStringEx(item.value('group'))
        if existsGroupValue and existsGroupValue != group:
            newGroupValue = existsGroupValue+'|'+group
        else:
            newGroupValue = group

        item.setValue('group', QVariant(newGroupValue))
        item.setValue('name('+fieldNameType+')', propertyTypeName)

    def addAdditionalRow(self, key, group, name):
        if not name:
            name = '-----'
        self._mapAdditionalKeyToGroup[key] = group
        item = self.getNewRecord()
        item.setValue('name(A)', QVariant(name))
        item.setValue('name(%)', QVariant(name))
        item.setValue('group', QVariant(group))
        self._additionalItems.append(item)
        row = len(self._items) + len(self._additionalItems)-1

        self.mapKeyToRow(key, row, 'A')
        self.mapKeyToRow(key, row, '%')

        result = self._mapGroupToRows.setdefault(group, [row])
        self._mapRowToGroup[row] = group
        if row not in result:
            result.append(row)

        buttonKeyList = self._mapRowToButtonKey.setdefault(row, [key])
        if key not in buttonKeyList:
            buttonKeyList.append(key)

        self.updateDataForGroup(row)

        self.reset()

    def resetAdditional(self, sentData=True):
        for key in self._mapAdditionalKeyToGroup.keys():
            del self._mapKeyToRow[key]
        realItemsCount = len(self._items)
        for row in range(realItemsCount, len(self._additionalItems)+realItemsCount):
            del self._mapRowToButtonKey[row]
            group = self._mapRowToGroup[row]
            del self._mapRowToGroup[row]
            rows = self._mapGroupToRows[group]
            if row in rows:
                del rows[rows.index(row)]

        self._mapAdditionalKeyToGroup = {}
        self._additionalItems = []

        self.reset()

        for row in range(realItemsCount):
            self.updateDataForGroup(row)
            self.countPercentValueForGroup(row)

        if sentData:
            self._parent.sentData()

    def mapKeyToRow(self, buttonKey, row, fieldNameType):
        if buttonKey in self._mapKeyToRow.keys():
            self._mapKeyToRow[buttonKey].append((row, fieldNameType))
        else:
            self._mapKeyToRow[buttonKey] = [(row, fieldNameType)]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        row    = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            realItemsCount = len(self._items)
            additionalItemsCount = len(self._additionalItems)
            item = None
            if 0 <= row and row < realItemsCount:
                item = self._items[row]
            elif  realItemsCount <= row and row < additionalItemsCount+realItemsCount:
                item = self._additionalItems[row-realItemsCount]
            if item:
                value = item.value(CLaboratoryCalculatorTableModel.fields[column][0])
                if column == CLaboratoryCalculatorTableModel.ciPercentCount:
                    value = forceDouble(value)
                    value = QVariant(self._locale.toString(value, 'f', self._rounding))
                return value
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            realItemsCount = len(self._items)
            additionalItemsCount = len(self._additionalItems)
            row = index.row()
            item = None
            if 0 <= row and row < realItemsCount:
                item = self._items[row]
            elif  realItemsCount <= row and row < additionalItemsCount+realItemsCount:
                item = self._additionalItems[row-realItemsCount]
            if item:
                column = index.column()
                fieldName = CLaboratoryCalculatorTableModel.fields[column][0]
                item.setValue(fieldName, value)
                self.emitRowDataChanged(row)
                if column == CLaboratoryCalculatorTableModel.ciGlobalCount:
                    self.updateDataForGroup(row)
                return True
        return False

    def emitRowDataChanged(self, row):
        begIndex = self.index(row, 0)
        endIndex = self.index(row, self.columnCount()-1)
        self.emitDataChanged(begIndex, endIndex)

    def emitDataChanged(self, begIndex, endIndex):
        self.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), begIndex, endIndex)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QVariant(CLaboratoryCalculatorTableModel.horizontalHeaders[section])
            elif orientation == Qt.Vertical:
                bittonKeyList = self._mapRowToButtonKey[section]
                return QVariant('|'.join(bittonKeyList))
        return QVariant()


    def columnCount(self, index=None):
        return len(CLaboratoryCalculatorTableModel.horizontalHeaders)

    def rowCount(self, index=None):
        return len(self._items) + len(self._additionalItems)

    def availableGroupList(self):
        return groupList

    def clear(self):
        self._origStruct = []
        self._fullStruct = []
        self._items = []
        self._additionalItems = []
        self._mapAdditionalKeyToGroup = {}
        self._mapKeyToRow  = {}
        self._mapGroupToRows = {}
        self._mapNameToRow = {}
        self._mapRowToGroup = {}
        self._mapRowToButtonKey = {}
        self._mapPropertyTypeIdToCoords = {}

    def additionalKeyList(self):
        return self._mapAdditionalKeyToGroup.keys()

    def copyItems(self, items=[]):
        newItems = []
        for item in items:
            newItems.append(QtSql.QSqlRecord(item))
        return newItems

    def saveSetData(self):
        if self._needToSave:

            itemToSave = smartDict()
            itemToSave.items = self.copyItems(self._items)
            itemToSave.additionalItems = self.copyItems(self._additionalItems)
            itemToSave.mapAdditionalKeyToGroup = dict(self._mapAdditionalKeyToGroup)
            itemToSave.mapKeyToRow = dict(self._mapKeyToRow)
            itemToSave.mapGroupToRows = dict(self._mapGroupToRows)
            itemToSave.mapNameToRow = dict(self._mapNameToRow)
            itemToSave.mapRowToGroup = dict(self._mapRowToGroup)
            itemToSave.mapRowToButtonKey = dict(self._mapRowToButtonKey)
            itemToSave.mapPropertyTypeIdToCoords = dict(self._mapPropertyTypeIdToCoords)
            self._history.append(itemToSave)

            self._historyPointer += 1
            self._onHistoryPointer = True
            self._needToSave = False

    def loadLastSetData(self):
        if self._onHistoryPointer:
            self.downHistoryPointer()
        if self._historyPointer > 0:
            itemToLoad = self._history[self._historyPointer]

            self._items = self.copyItems(itemToLoad.items)
            self._additionalItems = self.copyItems(itemToLoad.additionalItems)
            self._mapAdditionalKeyToGroup = itemToLoad.mapAdditionalKeyToGroup
            self._mapKeyToRow  = itemToLoad.mapKeyToRow
            self._mapGroupToRows = itemToLoad.mapGroupToRows
            self._mapNameToRow = itemToLoad.mapNameToRow
            self._mapRowToGroup = itemToLoad.mapRowToGroup
            self._mapRowToButtonKey = itemToLoad.mapRowToButtonKey
            self._mapPropertyTypeIdToCoords = itemToLoad.mapPropertyTypeIdToCoords

            self._onHistoryPointer = True
            self._needToSave = False
        else:
            self.clear()
            self._history = [self._emptyItem]
            self._historyPointer = 0
            self.resetData()

        self.reset()

    def downHistoryPointer(self):
        self._historyPointer -= 1
        del self._history[-1]

    def reset(self):
        QAbstractTableModel.reset(self)

    def resetData(self):
        self.load(self._inputData)


    def commands(self, keyList=[]):
        for key in keyList:
            self.command(key)


    def command(self, key):
        CLaboratoryCalculatorTableModel.__dict__.get(key, lambda val: val)(self)

    def done(self, key, rounding=0):
        result = False
        for cellDescription in self._mapKeyToRow.get(key, []):
            result = True
            row, fieldType = cellDescription
            if forceInt(self.data(self.index(row, CLaboratoryCalculatorTableModel.ciGroupSumm))) < self._maxGroupValue:
                if self.needDoneGlobalRowValue(key, fieldType):
                    self._needToSave = True
                    self._onHistoryPointer = False
                    self.doneGlobalRowValue(row)
                    self.countPercentValueForGroup(row, rounding)
#                    self.countAL(row)
            else:
                QtGui.QApplication.beep()
                return result
        if result:
            self.saveSetData()
        return result

    def setMaxGroupValue(self, val):
        self._maxGroupValue = val

    def needDoneGlobalRowValue(self, key, fieldType):
        if fieldType == FiledType.GlobalType:
            return True
        result = True
        for row, fieldType in self._mapKeyToRow.get(key, []):
            if fieldType == FiledType.GlobalType:
                result = False
        return result

    def doneGlobalRowValue(self, row):
        column = CLaboratoryCalculatorTableModel.ciGlobalCount
        fieldName = CLaboratoryCalculatorTableModel.fields[column][0]

        realItemsCount = len(self._items)
        additionalItemsCount = len(self._additionalItems)
        item = None
        if 0 <= row and row < realItemsCount:
            item = self._items[row]
        elif  realItemsCount <= row and row < additionalItemsCount+realItemsCount:
            item = self._additionalItems[row-realItemsCount]
        if item:
            value = forceInt(item.value(fieldName))+1
            self.setData(self.index(row, column), QVariant(value))

    def updateDataForGroup(self, row):
        rows = self.getGroupRows(row)
        rowGroupData = 0
        countedButtons = []
        for row in rows:
            button = self._mapRowToButtonKey.get(row, None)[0]
            if button not in countedButtons:
                rowGroupData += forceInt(self.data(self.index(row, CLaboratoryCalculatorTableModel.ciGlobalCount)))
                countedButtons.append(button)
        for row in rows:
            self.setData(self.index(row, CLaboratoryCalculatorTableModel.ciGroupSumm), QVariant(rowGroupData))

#    def countAL(self, row):
#        column = CLaboratoryCalculatorTableModel.ciAL
#        fieldName = CLaboratoryCalculatorTableModel.fields[column][0]
#
#        realItemsCount = len(self._items)
#        additionalItemsCount = len(self._additionalItems)
#        item = None
#        if 0 <= row and row < realItemsCount:
#            item = self._items[row]
#        elif  realItemsCount <= row and row < additionalItemsCount+realItemsCount:
#            item = self._additionalItems[row-realItemsCount]
#        if item:
#            value = forceDouble(item.value(fieldName))+1
#            self.setData(self.index(row, column), QVariant(value))

    def countPercentValueForGroup(self, row, rounding=0):
        column = CLaboratoryCalculatorTableModel.ciPercentCount
        columnAL = CLaboratoryCalculatorTableModel.ciAL
        rows = self.getGroupRows(row)
        for row in rows:
            rowGroupData = forceInt(self.data(self.index(row, CLaboratoryCalculatorTableModel.ciGroupSumm)))
            if rowGroupData:
                rowData = forceInt(self.data(self.index(row, CLaboratoryCalculatorTableModel.ciGlobalCount)))
                value = (100.0*rowData)/rowGroupData

                decimalValue = Decimal(unicode(value))
                context = Context(prec=rounding+len(str(int(value))))
                value = float(decimalValue.normalize(context)/1)

                self.setData(self.index(row, column), QVariant(value))
                valueAL = self._parent.edtLeukocytes.value() * value / 100
                self.setData(self.index(row, columnAL), QVariant(valueAL))

    def recountPercentValueForGroup(self, rounding=0):
        for row in xrange(self.rowCount()):
            self.countPercentValueForGroup(row, rounding)

    def getGroupRows(self, row):
        group = self._mapRowToGroup[row]
        return self._mapGroupToRows.get(group, [])

    def formatData(self):
        self.saveSetData()
        valueList = []
        for propertyTypeId in self._mapPropertyTypeIdToCoords.keys():
            valueCoords = self._mapPropertyTypeIdToCoords[propertyTypeId]
            value = forceString(self.data(self.index(*valueCoords)))
            valueList.append(u'('+unicode(propertyTypeId)+', '+unicode(value)+')')
        if self.leukocytesPropId:
            valueList.append(u'%i,%f'%(self.leukocytesPropId, self._parent.edtLeukocytes.value()))
        if self.ggPropId:
            valueList.append(u'%i,%f'%(self.ggPropId, self._parent.edtGG.value()))
        if self.eePropId:
            valueList.append(u'%i,%f'%(self.eePropId, self._parent.edtEE.value()))
        if self.ciPropId:
            valueList.append(u'%i,%f'%(self.ciPropId, self._parent.edtCI.value()))
        return ';'.join(valueList)

    @classmethod
    def getNewRecord(cls):
        record = QtSql.QSqlRecord()
        for fieldName, fieldType in cls.fields:
            record.append(QtSql.QSqlField(fieldName, fieldType))
        return record


# ###############################################


class CLaboratoryCalculatorTableView(QtGui.QTableView, CPreferencesMixin):
    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        self._popupMenu = None

        h = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(3*h/2)
#        self.verticalHeader().hide()
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)



