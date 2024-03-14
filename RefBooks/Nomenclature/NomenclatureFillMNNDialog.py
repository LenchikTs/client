# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignature, QModelIndex, SIGNAL

from library.Utils       import forceString, forceBool, forceRef, forceInt, forceStringEx, toVariant
from library.DialogBase  import CDialogBase

from .Ui_NomenclatureFillMNNDialog import Ui_NomenclatureFillMNNDialog


class CNomenclatureFillMNNDialog(CDialogBase, Ui_NomenclatureFillMNNDialog):
    def __init__(self, parent, compositionItems):
        CDialogBase.__init__(self, parent)
        self.addModels('SelectedValueMNN', CSelectedValueMNNModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Выберите значение МНН')
        self.setModels(self.tblSelectedValueMNN, self.modelSelectedValueMNN, self.selectionModelSelectedValueMNN)
#        self.modelNomenclatureExpense.setEnableAppendLine(False)
        self.MnnRussianStr = u''
        self.MnnRussian = False
        self.MnnLatinStr = u''
        self.MnnLatin = False
        self.isCancelDone = False
        self.compositionItems = compositionItems
        self.modelSelectedValueMNN.loadItems(self.compositionItems)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.on_buttonBox_ok()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.MnnRussianStr = u''
            self.MnnRussian = False
            self.MnnLatinStr = u''
            self.MnnLatin = False
            QtGui.QDialog.reject(self)


    def on_buttonBox_ok(self):
        self.isCancelDone = False
        self.MnnRussianStr = u''
        self.MnnRussian = False
        self.MnnLatinStr = u''
        self.MnnLatin = False
        include = False
        for row, item in enumerate(self.modelSelectedValueMNN._items):
            if forceBool(item[1]):
                if row == 0:
                    self.MnnRussianStr = forceString(item[2])
                    self.MnnRussian = True
                elif row == 1:
                    self.MnnLatinStr = forceString(item[2])
                    self.MnnLatin = True
                include = True
        if not include:
            self.checkInputMessage(u'значение для заполнения', False, self.tblSelectedValueMNN, 0, 1)
            self.isCancelDone = True
        else:
            QtGui.QDialog.accept(self)


    def on_buttonBox_reset(self):
        self.isCancelDone = False
        self.MnnRussianStr = u''
        self.MnnRussian = False
        self.MnnLatinStr = u''
        self.MnnLatin = False
        for item in self.modelSelectedValueMNN._items:
            if forceBool(item[1]):
                item.setValue('include', QVariant(False))
        self.modelSelectedValueMNN.reset()


    def getMNNValue(self):
        return (self.MnnRussianStr, self.MnnRussian, self.MnnLatinStr, self.MnnLatin)


    def saveData(self):
        return (not self.isCancelDone)


class CSelectedValueMNNModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self._items = []
        self.caches = {}
        self._cols = [u'МНН', u'Заполнить', u'Значение']


    def addCol(self, col):
        self._cols.append(col)
        return col


    def items(self):
        return self._items


    def columnCount(self, index=None):
        return len(self._cols)


    def rowCount(self, index=None):
        return len(self._items)


    def flags(self, index = QModelIndex()):
        column = index.column()
        row = index.row()
        if column == 1 and row >= 0 and row < len(self._items):
            if self._items[row][2]:
                return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsUserCheckable
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self._cols[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if column != 1:
                item = self._items[row]
                return toVariant(item[column])
        elif role == Qt.ToolTipRole:
            if column == 2:
                item = self._items[row]
                return QVariant(item[column])
        elif role == Qt.CheckStateRole:
            if column == 1:
                item = self._items[row]
                if forceInt(item[column]) == 0:
                    return QVariant(Qt.Unchecked)
                else:
                    return QVariant(Qt.Checked)
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            row = index.row()
            column = index.column()
            if column == 1:
                if row >= 0 and row < len(self._items):
                    state = value.toInt()[0]
                    self._items[row][1] = 0 if state == Qt.Unchecked else 1
                    self.emitCellChanged(row, column)
                    return True
        return False


    def loadItems(self, compositionItems):
        self._items = [[u'На русском', 0, u''],
                       [u'На латинском', 0, u'']
                      ]
        activeRussianType = []
        activeAdditionalRussianType = []
#        additionalRussianType = []
        activeLatinType = []
        activeAdditionalLatinType = []
#        additionalLatinType = []
        russianName = u''
        latinName = u''
        isRussian = True
        isLatin = True
        for record in compositionItems:
            activeSubstanceRussianName = u''
            activeSubstanceLatinName = u''
            activeSubstanceId = forceRef(record.value('activeSubstance_id'))
            type = forceInt(record.value('type'))
            if activeSubstanceId:
                recordCache = self.caches.get(activeSubstanceId, None)
                if not recordCache:
                    db = QtGui.qApp.db
                    table = db.table('rbNomenclatureActiveSubstance')
                    recordCache = db.getRecordEx(table, [table['name'], table['mnnLatin']], [table['id'].eq(activeSubstanceId)])
                if recordCache:
                    activeSubstanceRussianName = forceStringEx(recordCache.value('name'))
                    activeSubstanceLatinName = forceStringEx(recordCache.value('mnnLatin'))
                    if isRussian:
                        isRussian = bool(activeSubstanceRussianName) or (bool(activeSubstanceLatinName) and type == 2)
                    if isLatin:
                        isLatin = bool(activeSubstanceLatinName) or (bool(activeSubstanceRussianName) and type == 2)
                    if type == 0:
                        if isRussian and activeSubstanceRussianName:
                            activeRussianType.append(activeSubstanceRussianName)
                        if isLatin and activeSubstanceLatinName:
                            activeLatinType.append(activeSubstanceLatinName)
                    elif type == 1:
                        if isRussian and activeSubstanceRussianName:
                            activeAdditionalRussianType.append(activeSubstanceRussianName)
                        if isLatin and activeSubstanceLatinName:
                            activeAdditionalLatinType.append(activeSubstanceLatinName)
#                    elif type == 2:
#                        if isRussian and activeSubstanceRussianName:
#                            additionalRussianType.append(activeSubstanceRussianName)
#                        if isLatin and activeSubstanceLatinName:
#                            additionalLatinType.append(activeSubstanceLatinName)
                    self.caches[activeSubstanceId] = recordCache
        if isRussian:
            activeRussianType.sort(key=lambda x: x.lower())
            activeAdditionalRussianType.sort(key=lambda x: x.lower())
    #        additionalRussianType.sort(key=lambda x: x.lower())
            activeRussianTypeStr = u'+'.join(name for name in activeRussianType if name)
            russianName = activeRussianTypeStr
            activeAdditionalRussianTypeStr = u'+'.join(name for name in activeAdditionalRussianType if name)
            if activeAdditionalRussianTypeStr:
                russianName += (u'+[' if russianName else u'[') + activeAdditionalRussianTypeStr + u']'
    #        additionalRussianTypeStr = u'+'.join(name for name in additionalRussianType if name)
    #        if additionalRussianTypeStr:
    #            russianName += (u'+[' if russianName else u'[') + additionalRussianTypeStr + u']'
        self._items[0][2] = russianName
        self._items[0][1] = 1 if self._items[0][2] else 0
        if isLatin:
            activeLatinType.sort(key=lambda x: x.lower())
            activeAdditionalLatinType.sort(key=lambda x: x.lower())
    #        additionalLatinType.sort(key=lambda x: x.lower())
            activeLatinTypeStr = u'+'.join(name for name in activeLatinType if name)
            latinName = activeLatinTypeStr
            activeAdditionalLatinTypeStr = u'+'.join(name for name in activeAdditionalLatinType if name)
            if activeAdditionalLatinTypeStr:
                latinName += (u'+[' if latinName else u'[') + activeAdditionalLatinTypeStr + u']'
    #        additionalLatinTypeStr = u'+'.join(name for name in additionalLatinType if name)
    #        if additionalLatinTypeStr:
    #            latinName += (u'+[' if latinName else u'[') + additionalLatinTypeStr + u']'
        self._items[1][2] = latinName
        self._items[1][1] = 1 if self._items[1][2] else 0
        self.reset()


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)

