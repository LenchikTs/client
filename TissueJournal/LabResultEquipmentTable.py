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
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QVariant

from library.crbcombobox import CRBModelDataCache
from library.Utils       import forceInt, forceString

from TissueJournal.Utils import getEquipmentInterface


class CLabResultEquipmentTableView(QtGui.QTableView):
    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        h = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)



class CLabResultEquipmentModel(QAbstractTableModel):
    columnNames = (u'Включить', u'Оборудование', u'Директория', u'Статус')
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self._equipmentId2Checked = {}
        self._idList = []
        self._displayIndexList = (self.getColumnIndex(u'Оборудование'),
                                  self.getColumnIndex(u'Директория'),
                                  self.getColumnIndex(u'Статус'))
        self._mapData = {}
        self._parent = parent


    def checkedEquipmentIdList(self):
        return [equipmentId for equipmentId in self._idList if self.isEquipmentChecked(equipmentId)]


    def setIdList(self, idList, checkedId=None):
        self._idList = idList
        self.setEquipmentChecked(checkedId, Qt.Checked)
        self.reset()


    def rowCount(self, index=None):
        return len(self._idList)

    def columnCount(self, index=None):
        return len(CLabResultEquipmentModel.columnNames)

    def getColumnIndex(self, columnName):
        return CLabResultEquipmentModel.columnNames.index(columnName)


    def equipmentInfo(self, column, equipmentId):
        if (column, equipmentId) in self._mapData.keys():
            return self._mapData[(column, equipmentId)]
        else:
            if column == self.getColumnIndex(u'Оборудование'):
                data = CRBModelDataCache.getData('rbEquipment')
                result = QVariant(u' | '.join([unicode(data.getCodeById(equipmentId)),
                                               unicode(data.getNameById(equipmentId))]))
                self._mapData[(column, equipmentId)] = result
                return result
            elif column in (self.getColumnIndex(u'Директория'), self.getColumnIndex(u'Статус')):
                import json, os
                equipmentInterface = getEquipmentInterface(equipmentId)
                equipmentInterface = equipmentInterface if equipmentInterface else {}
                try:
                    opts = json.loads(equipmentInterface.address if equipmentInterface.address else '{}')
                except:
                    opts = {}
                    self._equipmentInterfaceAddressNotValid(equipmentId, equipmentInterface.address)
                inDir = os.path.expanduser(opts.get('inDir', opts.get('dir', '')))
                self._mapData[(self.getColumnIndex(u'Директория'), equipmentId)] = QVariant(inDir)
                self._mapData[(self.getColumnIndex(u'Статус'), equipmentId)] = QVariant(u'Директория существует' if os.path.exists(inDir) else u'Директория не существует')
                return self._mapData[(column, equipmentId)]
            else:
                self._mapData[(column, equipmentId)] = QVariant()
                return self._mapData[(column, equipmentId)]


    def _equipmentInterfaceAddressNotValid(self, equipmentId, equipmentInterfaceAddress):
        message = u'Адрес интерфейса оборудовния \'%s\' не корректен!\n\n%s' % (forceString(self.equipmentInfo(self.getColumnIndex(u'Оборудование'), equipmentId)), equipmentInterfaceAddress)
        QtGui.QMessageBox.information(self._parent, u'Внимание!', message, QtGui.QMessageBox.Ok)


    def isEquipmentChecked(self, equipmentId):
        return self._equipmentId2Checked.get(equipmentId, Qt.Unchecked)


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(CLabResultEquipmentModel.columnNames[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            column = index.column()
            row = index.row()
            equipmentId = self._idList[row]
            return QVariant(self.equipmentInfo(column, equipmentId))

        elif role == Qt.CheckStateRole:
            column = index.column()
            if column == self.getColumnIndex(u'Включить'):
                row = index.row()
                equipmentId = self._idList[row]
                return QVariant(self.isEquipmentChecked(equipmentId))

        elif role == Qt.BackgroundRole:
            row = index.row()
            equipmentId = self._idList[row]
            result = self._mapData.get((None, equipmentId), None)
            if not result:
                status = self.equipmentInfo(self.getColumnIndex(u'Статус'), equipmentId)
                if self._isStatusExist(status):
                    result = QVariant()
                else:
                    result = QVariant(QtGui.QColor(Qt.red))
                self._mapData[(None, equipmentId)] = result
            return result

        return QVariant()


    def _isStatusExist(self, status):
        return status == u'Директория существует'


    def setEquipmentChecked(self, equipmentId, value):
        self._equipmentId2Checked[equipmentId] = value


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole:
            column = index.column()
            if column == self.getColumnIndex(u'Включить'):
                row = index.row()
                equipmentId = self._idList[row]
                self.setEquipmentChecked(equipmentId, forceInt(value))
                self.emitCellChanged(row, column)
                return True

        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def flags(self, index=None):
        result = result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == self.getColumnIndex(u'Включить'):
            if self._isStatusExist(self.equipmentInfo(self.getColumnIndex(u'Статус'), self._idList[index.row()])):
                result = result | Qt.ItemIsUserCheckable
        return result







