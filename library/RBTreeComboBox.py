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

from library.crbcombobox  import CRBComboBox, CRBModelDataCache
from library.TreeModel    import CTreeItemWithId, CTreeModel
from library.TreeComboBox import CTreeComboBox

from library.InDocTable   import CInDocTableCol
from library.Utils        import forceInt, forceString, toVariant


class CRBTreeItem(CTreeItemWithId):
    def __init__(self, rootItem, parent, id, name):
        CTreeItemWithId.__init__(self, parent, name, id)
        self.rootItem = rootItem


    def loadChildren(self):
        result = []
        db = QtGui.qApp.db
        table = self.rootItem.table
        rootItem = self.rootItem
        cond = [table[rootItem.groupField].eq(self._id)]
        if rootItem.filter:
            cond.append(rootItem.filter)
        order = rootItem.order if rootItem.order else rootItem.nameField
        query = db.query(db.selectStmt(table, ['id', rootItem.nameField], where=cond, order=order))
        while query.next():
            record = query.record()
            id   = forceInt(record.value(0))
            name = forceString(record.value(1))
            result.append(CRBTreeItem(rootItem, self, id, name))
        return result


class CRBRootTreeItem(CRBTreeItem):
    nameField = 'name'
    groupField = 'group_id'

    def __init__(self, tableName, filter, order, id):
        CRBTreeItem.__init__(self, self, None, '-', id)
        db = QtGui.qApp.db
        self.table  = db.table(tableName)
        self.filter = filter
        self.order = order
        self.setId(id)

    def setId(self, id=None):
        if self._id != id:
            self._id = id
            self._items = None
            if self._id:
                self._name = forceString(QtGui.qApp.db.translate(self.table, 'id', self._id, 'name'))
            else:
                self._name = u'-'


    def isObsolete(self):
        return False



class CRBRootTreeItemCache(object):
    _mapTableToData = {}

    @classmethod
    def getData(cls, tableName, filter='', order=None, rootId=None):
        key = '|'.join([unicode(tableName), filter, unicode(order), unicode(rootId)])
        result = cls._mapTableToData.get(key, None)
        if result is None or result.isObsolete():
            result = CRBRootTreeItem(tableName, filter, order, rootId)
            cls._mapTableToData[key] = result
        return result


    @classmethod
    def reset(cls):
        cls._mapTableToData.clear()



class CRBTreeModel(CTreeModel):
    def __init__(self, id, parent=None):
        CTreeModel.__init__(self, parent, None)
        self.resetRequired = False


    def setTable(self, tableName, filter='', order=None, rootId=None, showRoot=True):
        rootItem = self._rootItem
        self._rootItem = CRBRootTreeItemCache.getData(tableName, filter, order, rootId)
        if rootItem and rootItem.isLoaded() or self.resetRequired:
            self.reset()
            self.resetRequired = False


    def setId(self, id=None):
        self.getRootItem().setId(id)
        self.reset()


class CRBTreeComboBox(CTreeComboBox):
    def __init__(self, parent):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self._model = CRBTreeModel(None, self)
        self.setModel(self._model)
        self._expandAll = False


    def setTable(self, tableName, filter='', order=None, rootId=None, showRoot=True):
        self._tableName = tableName
        self._rootId    = rootId
        self._showRoot  = showRoot
        self._filier    = filter
        self._order     = order
        self._model.setTable(tableName, filter, order, rootId, showRoot)


    def setFilter(self, filter=''):
        self._filier = filter
        self._model.setTable(self._tableName, self._filter, self._order, self._rootId, self._showRoot)


    def setRoot(self, rootId):
        self._rootId = rootId
        self._model.setTable(self._tableName, self._addNone, filter, self._order, self._rootId, self._showRoot)


    def setValue(self, id):
#        id = None
        index = self._model.findItemId(id)
        if index:
            self.setCurrentModelIndex(index)


    def value(self):
        modelIndex = self.currentModelIndex()
        if modelIndex.isValid():
            return self._model.itemId(modelIndex)
        return None


class CRBTreeInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, tableName, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.tableName  = tableName
        self.filter     = params.get('filter', '')
        self.order      = params.get('order', '')
        self.rootId     = params.get('rootId', None)
        self.showRoot   = params.get('showRoot', True)

#        self.addNone    = params.get('addNone', True)
        self.showFields = params.get('showFields', CRBComboBox.showName)
        self.preferredWidth = params.get('preferredWidth', None)


    def toString(self, val, record):
        cache = CRBModelDataCache.getData(self.tableName, True)
        text = cache.getStringById(forceInt(val), self.showFields)
        return toVariant(text)

    def toStatusTip(self, val, record):
        cache = CRBModelDataCache.getData(self.tableName, True)
        text = cache.getStringById(forceInt(val), CRBComboBox.showName)
        return toVariant(text)


    def createEditor(self, parent):
        editor = CRBTreeComboBox(parent)
        editor.setTable(self.tableName, filter=self.filter, order=self.order, rootId=self.rootId, showRoot=self.showRoot)
#        editor.setShowFields(self.showFields)
#        editor.setPreferredWidth(self.preferredWidth)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(forceInt(value))


    def getEditorData(self, editor):
        return toVariant(editor.value())
