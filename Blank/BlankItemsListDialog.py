#!/usr/bin/env python
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
from PyQt4.QtCore import Qt, QVariant, pyqtSignature

from library.DialogBase import CDialogBase
from library.TableModel import CTableModel
from library.TreeModel import CTreeItemWithId, CTreeModel, CDBTreeModel
from library.Utils import forceInt, forceRef, forceString, toVariant

from Ui_BlankItemsListDialog import Ui_BlankItemsListDialog


class CBlankTreeItem(CTreeItemWithId):
    def __init__(self, parent, id, code, name):
        CTreeItemWithId.__init__(self, parent, name, id)
        self._code = code
        self._items = []


    def flags(self):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def data(self, column):
        if column == 0:
            s = self._name
            return toVariant(s)
        else:
            return QVariant()


    def sortItems(self):
        pass


    def sortKey(self):
        return (2, self._code, self._name, self._id)


class CBlankTreeItems(CTreeItemWithId):
    def __init__(self, parent, name, id=None):
        CTreeItemWithId.__init__(self, parent, name, id)
        self._items = []

    def flags(self):
        return Qt.ItemIsEnabled

    def sortItems(self):
        self._items.sort(key=lambda item: item.sortKey())
        for item in self._items:
            item.sortItems()

    def sortKey(self):
        return (1, self._name)


class CBlankRootTreeItem(CTreeItemWithId):
    def __init__(self, filter = {}):
        CTreeItemWithId.__init__(self, None, '-', None)
        self._classesVisible = False


    def loadChildren(self):
        mapTypeToTreeItem = {}
        result = []
        tempInvalidTypeList = [u'ВУТ', u'Инвалидность', u'Ограничение жизнедеятельности']

        def getTempInvalidTypeTreeItem(type):
            if type in mapTypeToTreeItem:
                item = mapTypeToTreeItem[type]
            else:
                tempInvalidType = tempInvalidTypeList[type]
                parentItem = self
                item = CBlankTreeItems(parentItem, tempInvalidType)
                result.append(item)
                mapTypeToTreeItem[type] = item
            return item

        db = QtGui.qApp.db
        tableTempInvalid = db.table('rbTempInvalidDocument')
        table = tableTempInvalid
        cond = []
        query = db.query(db.selectStmt(table, '*', where=cond, order=tableTempInvalid['type'].name()))
        while query.next():
            record = query.record()
            id   = forceRef(record.value('id'))
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))
            type = forceInt(record.value('type'))
            tempInvalidTypeItem = getTempInvalidTypeTreeItem(type)
            tempInvalidTypeItem._items.append(CBlankTreeItem(tempInvalidTypeItem, id, code, name))

        result.sort(key=lambda item: item._name)
        for item in result:
            item.sortItems()
        return result


class CBlankModel(CTreeModel):
    def __init__(self, parent=None, filter={}):
        CTreeModel.__init__(self, parent, CBlankRootTreeItem(filter))


class CBlanksItemsListDialog(CDialogBase, Ui_BlankItemsListDialog):
    def __init__(self, parent, cols, tableName, tableName2, tableName3, tableName4, order, forSelect=False, filterClass=None, findClass=None):
        CDialogBase.__init__(self, parent)
        self.cols = cols
        self.tableNameTI = tableName
        self.tableNameTI2 = tableName2
        self.tableNameAction = tableName3
        self.tableNameAction2 = tableName4
        self.order = order
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.findClass = findClass
        self.props = {}
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.btnNew.setShortcut(Qt.Key_F9)
        self.btnEdit.setShortcut(Qt.Key_F4)


    def preSetupUi(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.addModels('Tree', CBlankModel(self))
        self.addModels('Table',CTableModel(self, self.cols, self.tableNameTI2))
        filter = u'''(ActionType.id IN (SELECT DISTINCT AT.id
                FROM ActionType AS AT INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                WHERE AT.deleted = 0 AND APT.deleted = 0 AND APT.typeName = 'BlankSerialNumber')
                OR ActionType.id IN (SELECT DISTINCT AT.group_id
                FROM ActionType AS AT INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                WHERE AT.deleted = 0 AND APT.deleted = 0 AND APT.typeName = 'BlankSerialNumber')
                )'''
        self.addModels('Tree2', CDBTreeModel(self, self.tableNameAction, 'id', 'group_id', 'name', self.order, filter))
        self.addModels('Table2',CTableModel(self, self.cols, self.tableNameAction2))
        self.modelTree2.setLeavesVisible(True)


    def postSetupUi(self):
        self.setModels(self.treeItemsTempInvalid,  self.modelTree,  self.selectionModelTree)
        self.setModels(self.tblItemsTempInvalid,   self.modelTable, self.selectionModelTable)
        self.setModels(self.treeItemsOthers,  self.modelTree2,  self.selectionModelTree2)
        self.setModels(self.tblItemsOthers,   self.modelTable2, self.selectionModelTable2)
        self.treeItemsTempInvalid.header().hide()
        self.treeItemsOthers.header().hide()
        idList = self.select(self.props)
        self.modelTable.setIdList(idList)
        self.tblItemsTempInvalid.selectRow(0)
        self.btnSelect.setEnabled(self.forSelect)
        self.btnSelect.setVisible(self.forSelect)
        self.btnSelect.setDefault(self.forSelect)
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnFind.setEnabled(bool(self.findClass))
        self.btnFind.setVisible(bool(self.findClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItemsTempInvalid.setFocus(Qt.OtherFocusReason)


    def select(self, props):
        db = QtGui.qApp.db
        groupId = self.currentGroupId()
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            table = self.modelTable.table()
            return db.getIdList(table.name(),
                               'id',
                               table['doctype_id'].eq(groupId),
                               self.order)
        else:
            table = self.modelTable2.table()
            groupIdList = db.getDescendants('ActionType', 'group_id', groupId)
            if not groupIdList:
                return None
            return db.getIdList(table.name(),
                               'id',
                               table['doctype_id'].inlist(groupIdList),
                               self.order)


    def selectItem(self):
        return self.exec_()


    def setCurrentItemId(self, itemId):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            self.tblItemsTempInvalid.setCurrentItemId(itemId)
        else:
            self.tblItemsOthers.setCurrentItemId(itemId)


    def currentItemId(self):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            return self.tblItemsTempInvalid.currentItemId()
        else:
            return self.tblItemsOthers.currentItemId()


    def currentGroupId(self):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            return self.modelTree.itemId(self.treeItemsTempInvalid.currentIndex())
        else:
            return self.modelTree2.itemId(self.treeItemsOthers.currentIndex())


    def findById(self, id):
        widgetIndex = self.tabWidget.currentIndex()
        if widgetIndex == 0:
            index = self.modelTree.findItemId(id)
            parentIndex = self.modelTree.parent(index)
            self.treeItemsTempInvalid.expand(parentIndex)
            self.treeItemsTempInvalid.setCurrentIndex(parentIndex)
        else:
            index = self.modelTree2.findItemId(id)
            parentIndex = self.modelTree2.parent(index)
            self.treeItemsOthers.expand(parentIndex)
            self.treeItemsOthers.setCurrentIndex(parentIndex)
        self.renewListAndSetTo(id)


    def renewListAndSetTo(self, itemId=None):
        widgetIndex = self.tabWidget.currentIndex()
        idList = self.select(self.props)
        if not itemId:
            if widgetIndex == 0:
                itemId = self.tblItemsTempInvalid.currentItemId()
            else:
                itemId = self.tblItemsOthers.currentItemId()
        if widgetIndex == 0:
            self.tblItemsTempInvalid.setIdList(idList, itemId)
        else:
            self.tblItemsOthers.setIdList(idList, itemId)
        #groupId = self.currentGroupId()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelTree2_currentChanged(self, current, previous):
        self.renewListAndSetTo(None)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelTree_currentChanged(self, current, previous):
        self.renewListAndSetTo(None)


    @pyqtSignature('QModelIndex')
    def on_tblItemsOthers_doubleClicked(self, index):
        self.on_btnEdit_clicked()


    @pyqtSignature('')
    def on_btnNew_clicked(self):
        dialog = self.getItemEditor()
        try:
            dialog.setGroupId(self.currentGroupId())
            if dialog.exec_():
                itemId = dialog.itemId()
                self.renewListAndSetTo(itemId)
        finally:
            dialog.deleteLater()


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        itemId = self.currentItemId()
        if itemId:
            dialog = self.getItemEditor()
            try:
                dialog.load(itemId)
                if dialog.exec_():
                    itemId = dialog.itemId()
                    self.renewListAndSetTo(itemId)
            finally:
                dialog.deleteLater()
        else:
            self.on_btnNew_clicked()

