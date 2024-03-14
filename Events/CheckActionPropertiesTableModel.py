# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4               import QtGui
from PyQt4.QtCore        import Qt, QVariant, QAbstractTableModel, SIGNAL, QModelIndex

from library.Utils       import forceInt, trim, toVariant, foldText
from library.crbcombobox import CRBModelDataCache


class CCheckActionPropertiesTableModel(QAbstractTableModel):
    column = [u'Х', u'Значение']
    ciIsChecked = 0
    ciValue     = 1

    def __init__(self, parent, visibilityFilter=0):
        QAbstractTableModel.__init__(self, parent)
        self.action = None
        self.clientId = None
        self.propertyTypeList = []
        self.unitData = CRBModelDataCache.getData('rbUnit', True)
        self.visibilityFilter = visibilityFilter
        self.readOnly = False
        self.actionStatusTip = None
        self.includeRows = {}
        self.eventTypeId = None


    def setActionTypeProperty(self, action):
        self.propertyTypeList = []
        self.action = action
        if self.action:
            propertyTypeList = []
            actionType = self.action.getType()
            propertiesById = actionType.getPropertiesById()
            for id, propType in propertiesById.items():
                propertyTypeList.append((id, propType))
            propertyTypeList.sort(key=lambda x: x[1].name)
            for row, x in enumerate(propertyTypeList):
                if x[1]:
                    self.propertyTypeList.append(x[1])
                    self.includeRows[row] = Qt.Unchecked
        self.updateActionStatusTip()
        self.reset()


    def updateActionStatusTip(self):
        if self.action:
            actionType = self.action.getType()
            self.actionStatusTip = actionType.code + ': ' + actionType.name
        else:
            self.actionStatusTip = None


    def columnCount(self, index = None):
        return len(self.column)


    def rowCount(self, index = QModelIndex()):
        return len(self.propertyTypeList)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        elif orientation == Qt.Vertical:
            propertyType = self.propertyTypeList[section]
            property = self.action.getPropertyById(propertyType.id)
            if role == Qt.DisplayRole:
                return QVariant(foldText(propertyType.name, [20]))
            elif role == Qt.ToolTipRole:
                result = propertyType.descr if trim(propertyType.descr) else propertyType.name
                return QVariant(result)
            elif role == Qt.TextAlignmentRole:
                return QVariant(Qt.AlignLeft|Qt.AlignTop)
            elif role == Qt.ForegroundRole:
                evaluation = property.getEvaluation()
                if evaluation:
                    return QVariant(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            elif role == Qt.FontRole:
                evaluation = property.getEvaluation()
                if (evaluation and abs(evaluation) == 2):
                    font = QtGui.QFont()
                    font.setBold(True)
                    return QVariant(font)
        return QVariant()


    def getPropertyType(self, row):
        return self.propertyTypeList[row]


    def getProperty(self, row):
        propertyType = self.propertyTypeList[row]
        return self.action.getPropertyById(propertyType.id)


    def flags(self, index):
        if index.column() == self.ciIsChecked:
            return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        elif index.column() == self.ciValue:
            propertyType = self.propertyTypeList[index.row()]
            if propertyType.isBoolean():
                return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsUserCheckable
            return Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()
        propertyType = self.propertyTypeList[row]
        property = self.action.getPropertyById(propertyType.id)
        if role == Qt.DisplayRole:
            if column == self.ciValue:
                if propertyType.isBoolean():
                    return QVariant()
                return toVariant(property.getText())
        elif role == Qt.CheckStateRole:
            if column == self.ciValue:
                if propertyType.isBoolean():
                    return toVariant(Qt.Checked if property.getValue() else Qt.Unchecked)
            if column == self.ciIsChecked:
                return toVariant(Qt.Checked if self.includeRows.get(row, 0) else Qt.Unchecked)
        elif role == Qt.EditRole:
            if column == self.ciValue:
                return toVariant(property.getValue())
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignLeft|Qt.AlignTop)
        elif role == Qt.StatusTipRole:
            if self.actionStatusTip:
                return toVariant(self.actionStatusTip)
        return QVariant()


    def getDefaultEvaluation(self, propertyType, property, index):
        if propertyType.defaultEvaluation in (1, 2):
            if propertyType.defaultEvaluation == 2:
                if property.getEvaluation() is not None:
                    return ('%+d'%property.getEvaluation())
            value = unicode(property.getText())
            if bool(value):
                try:
                    value = float(value)
                except ValueError:
                    return ''
                norm = property.getNorm()
                parts = norm.split('-')
                if len(parts) == 2:
                    try:
                        bottom = float(parts[0].replace(',', '.'))
                        top    = float(parts[1].replace(',', '.'))
                    except ValueError:
                        return ''
                    if bottom > top:
                        return ''
                    if value < bottom:
                        evaluation = -1
                    elif value > top:
                        evaluation = 1
                    else:
                        evaluation = 0
                    index = self.index(index.row(), self.ciEvaluation)
                    self.setData(index, QVariant(evaluation))
                    return '%+d'%evaluation
        return ''


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        propertyType = self.propertyTypeList[row]
        property = self.action.getPropertyById(propertyType.id)
        if role == Qt.EditRole:
            if column == self.ciValue:
                if not propertyType.isVector:
                    property.preApplyDependents(self.action)
                    property.setValue(propertyType.convertQVariantToPyValue(value))
                    self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
                    self.getDefaultEvaluation(propertyType, property, index)
                    if property.isActionNameSpecifier():
                        self.action.updateSpecifiedName()
                        self.emit(SIGNAL('actionNameChanged()'))
                    property.applyDependents(self.action)
                    if propertyType.isJobTicketValueType():
                        self.action.setPlannedEndDateOnJobTicketChanged(property.getValue())
                    if propertyType.whatDepends:
                        self.updateDependedProperties(propertyType.whatDepends)
                    return True
        elif role == Qt.CheckStateRole:
            if column == self.ciIsChecked:
                self.includeRows[row] = Qt.Checked if forceInt(value) else Qt.Unchecked
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
                return True
            elif column == self.ciValue:
                if propertyType.isBoolean():
                    property.setValue(forceInt(value) == Qt.Checked)
                    self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
                    self.getDefaultEvaluation(propertyType, property, index)
                    if propertyType.whatDepends:
                        self.updateDependedProperties(propertyType.whatDepends)
                    return True
        return False


    def updateDependedProperties(self, vars):
        values = {}
        propertiesByVar = self.action.getPropertiesByVar()
        for var, property in propertiesByVar.iteritems():
            values[var] = property.getValue()
        for var in vars:
            property = propertiesByVar[var]
            propertyType = property.type()
            val = propertyType.evalValue(values)
            values[var] = val
            property.setValue(val)
            row = self.propertyTypeList.index(propertyType)
            index = self.index(row, self.ciValue)
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitDataChanged(self):
        leftTop = self.index(0, 0)
        rightBottom = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), leftTop, rightBottom)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(), column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)

