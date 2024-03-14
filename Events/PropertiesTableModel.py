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
############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QModelIndex, QVariant

from Events.ActionPropertiesTable import CActionPropertiesTableView
from library.Utils                import foldText, toVariant, trim
from library.crbcombobox          import CRBModelDataCache


class CPropertiesTableModel(QAbstractTableModel):

    column = [u'Назначено', u'Значение',  u'Ед.изм.',  u'Норма', u'Оценка']
    visibleAll = 0
    visibleInJobTicket = 1
    ciIsAssigned   = 0
    ciValue      = 1
    ciUnit       = 2
    ciNorm       = 3
    ciEvaluation = 4


    def __init__(self, parent, visibilityFilter=0):
        QAbstractTableModel.__init__(self, parent)
        self.propertyList = []
        self.propertyTypeList = []
        self.unitData = CRBModelDataCache.getData('rbUnit', True)
        self.visibilityFilter = visibilityFilter
        self.readOnly = False
        self.updateActionStatusTip()
        self.action = None
        self.clientSex = None
        self.clientAge = None


    def getPropertyType(self, row):
        property = None
        if row >= 0 and row < len(self.propertyList):
            property = self.propertyList[row]
        return property.type() if property else None


    def getProperty(self, row):
        if row >= 0 and row < len(self.propertyList):
            return self.propertyList[row]
        return None


    def updateActionStatusTip(self):
        self.actionStatusTip = None


    def setReadOnly(self, value):
        self.readOnly = value


    def setProperties(self, action, propertyList, clientSex = None, clientAge = None):
        self.action = action
        self.clientSex = clientSex
        self.clientAge = clientAge
        if propertyList:
            propertyList.sort(key=lambda x: (x.type().idx, x.type().id))
            self.propertyList = [x for x in propertyList if x.type().applicable(self.clientSex, self.clientAge) and self.visible(x.type())]
            self.propertyTypeList = [x.type() for x in propertyList if x.type().applicable(self.clientSex, self.clientAge) and self.visible(x.type())]
        else:
            self.propertyList = []
            self.propertyTypeList = []
        self.reset()


    def visible(self, propertyType):
        return self.visibilityFilter == self.visibleAll or \
               self.visibilityFilter == self.visibleInJobTicket and propertyType.visibleInJobTicket


    def columnCount(self, index = None):
        return 5


    def rowCount(self, index = QModelIndex()):
        return len(self.propertyList)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        elif orientation == Qt.Vertical:
            property = self.propertyList[section]
            propertyType = property.type()
            if role == Qt.DisplayRole:
                return QVariant(foldText(propertyType.name, [CActionPropertiesTableView.titleWidth]))
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


    def hasCommonPropertyChangingRight(self, row):
        return False


    def flags(self, index):
        column = index.column()
        if column == self.ciValue:
            row = index.row()
            property = self.propertyList[row]
            propertyType = property.type()
            if propertyType.isBoolean():
                return Qt.ItemIsSelectable|Qt.ItemIsUserCheckable
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled



    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()
        property = self.propertyList[row]
        propertyType = property.type()
        if role == Qt.DisplayRole:
            if column == self.ciValue:
                if propertyType.isBoolean():
                    return QVariant()
                return toVariant(property.getText())
            elif column == self.ciUnit:
                return QVariant(self.unitData.getNameById(property.getUnitId()))
            elif column == self.ciNorm:
                return toVariant(property.getNorm())
            elif column == self.ciEvaluation:
                evaluation = property.getEvaluation()
                if evaluation is None:
                    s = self.getDefaultEvaluation(propertyType, property, index)
#                    s = ''
                else:
                    s = ('%+d'%evaluation) if evaluation else '0'
                return toVariant(s)
            else:
                return QVariant()
        elif role == Qt.CheckStateRole:
            if column == self.ciIsAssigned:
                if propertyType.isAssignable:
                    return toVariant(Qt.Checked if property.isAssigned() else Qt.Unchecked)
        elif role == Qt.EditRole:
            if column == self.ciIsAssigned:
                return toVariant(property.getStatus())
            elif column == self.ciValue:
                return toVariant(property.getValue())
            elif column == self.ciUnit:
                return toVariant(property.getUnitId())
            elif column == self.ciNorm:
                return toVariant(property.getNorm())
            elif column == self.ciEvaluation:
                return toVariant(property.getEvaluation())
            else:
                return QVariant()
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignLeft|Qt.AlignTop)
        elif role == Qt.DecorationRole:
            return QVariant()
        elif role == Qt.ForegroundRole:
            evaluation = property.getEvaluation()
            if evaluation:
                return QVariant(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        elif role == Qt.FontRole:
            evaluation = property.getEvaluation()
            if evaluation and abs(evaluation) == 2:
                font = QtGui.QFont()
                font.setBold(True)
                return QVariant(font)
        elif role == Qt.ToolTipRole:
            if column == self.ciIsAssigned:
                if propertyType.isAssignable:
                    return QVariant(u'Назначено' if property.isAssigned() else u'Не назначено')
        elif role == Qt.CheckStateRole:
            if column == self.ciValue:
                if propertyType.isBoolean():
                    return QVariant(Qt.Checked if property.getValue() else Qt.Unchecked)
        elif role == Qt.CheckStateRole:
            if column == self.ciValue:
                if propertyType.isBoolean():
                    return QVariant(Qt.Checked if property.getValue() else Qt.Unchecked)
        return QVariant()



    def emitDataChanged(self):
        leftTop = self.index(0, 0)
        rightBottom = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), leftTop, rightBottom)


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


    def sort(self, column, order):
        self.reset()


    def setLaboratoryCalculatorData(self, data):
        pass


    def setPlannedEndDateByJobTicket(self, jobTicketId):
        pass


    def plannedEndDateByJobTicket(self):
        pass

