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
from PyQt4.QtCore import Qt, pyqtSignature, QModelIndex

from library.DialogBase import CDialogBase
from library.Utils import forceString, toVariant
from library.TableModel import CTableModel
from library.TreeModel import CDragDropDBTreeModel

from Ui_HierarchicalItemsListDialog import Ui_HierarchicalItemsListDialog

class CHierarchicalItemsListDialog(CDialogBase, Ui_HierarchicalItemsListDialog):
    def __init__(self, parent, cols, tableName, order, forSelect=False, filterClass=None, findClass=None):
        CDialogBase.__init__(self, parent)
        self.cols = cols
        self.tableName = tableName
        self.order = order
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.findClass = findClass
        self.props = {}
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
#        self.setup(cols, tableName, order, forSelect, filterClass)
        self.btnNew.setShortcut(Qt.Key_F9)
        self.btnEdit.setShortcut(Qt.Key_F4)


    def preSetupUi(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.addModels('Tree', CDragDropDBTreeModel(self, self.tableName, 'id', 'group_id', 'name', self.order))
        self.addModels('Table',CTableModel(self, self.cols, self.tableName))


    def postSetupUi(self):
        self.setModels(self.treeItems,  self.modelTree,  self.selectionModelTree)
        self.setModels(self.tblItems,   self.modelTable, self.selectionModelTable)
        self.treeItems.header().hide()
        idList = self.select(self.props)
        self.modelTable.setIdList(idList)
        self.tblItems.selectRow(0)
        self.btnSelect.setEnabled(self.forSelect)
        self.btnSelect.setVisible(self.forSelect)
        self.btnSelect.setDefault(self.forSelect)
#        self.btnFilter.setEnabled(self.forSelect and bool(self.filterClass))
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnFind.setEnabled(bool(self.findClass))
        self.btnFind.setVisible(bool(self.findClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)

    def select(self, props):
        table = self.modelTable.table()
        groupId = self.currentGroupId()
        return QtGui.qApp.db.getIdList(table.name(),
                           'id',
                           table['group_id'].eq(groupId),
                           self.order)

    def selectItem(self):
#        if self.filterClass is not None: etc.
        return self.exec_()


#    def createPopupMenu(self, widget):
#        menu = QtGui.QMenu(widget)
#        menu.addAction( const QIcon & icon, const QString & text )
#        menu.addAction(u'Выбрать',         self, 'selectStatTalon')
#        menu.addAction(u'Новая запись',    self, 'newStatTalon')
#        menu.addAction(u'Изменить запись', self, 'editStatTalon')
##        widget.setPopup(menu)

    def setCurrentItemId(self, itemId):
        self.tblItems.setCurrentItemId(itemId)


    def currentItemId(self):
        return self.tblItems.currentItemId()

    def currentGroupId(self):
        return self.modelTree.itemId(self.treeItems.currentIndex())

    def findById(self, id):
        item = self.modelTree.getItemByIdEx(id)
        if not item:
            item = self.modelTree.getItemById(id)
        parentIndex = self.modelTree.parentByItem(item)
        self.treeItems.expand(parentIndex)
        self.treeItems.setCurrentIndex(parentIndex)
        self.renewListAndSetToWithoutUpdate(id)

    def renewListAndSetTo(self, itemId=None):
        self.renewListAndSetToWithoutUpdate(itemId)
        self.modelTree.update()

    def renewListAndSetToWithoutUpdate(self, itemId=None):
        if not itemId:
            itemId = self.tblItems.currentItemId()
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, itemId)
#        groupId = self.currentGroupId()

    def copyDependedTableData(self, tableName, refFieldName, newItemId, oldItemId):
        db = QtGui.qApp.db
        table = db.table(tableName)
        records = db.getRecordList(table, '*', table[refFieldName].eq(oldItemId))
        for record in records:
            record.setNull('id')
            record.setValue(refFieldName, toVariant(newItemId))
            db.insertRecord(table, record)


    def copyInternals(self, newItemId, itemId):
        pass


    def duplicateRecord(self, itemId):
        def duplicateRecordInternal():
            db = QtGui.qApp.db
            record = db.getRecord(self.modelTable.table(), '*', itemId)
            code = forceString(record.value('code'))
            name = forceString(record.value('name'))

            record.setNull('id') # чтобы не дублировался id
            record.setValue('code', code + '*')
            record.setValue('name', name + u'(копия)')
            try:
                db.transaction()
                newItemId = db.insertRecord(self.modelTable.table(), record)
                self.copyInternals(newItemId, itemId)
                db.commit()
                return newItemId
            except:
                db.rollback()
                raise
        ok, result = QtGui.qApp.call(self, duplicateRecordInternal)
        return result


    def duplicateCurrentRow(self):
        itemId = self.tblItems.currentItemId()
        newItemId = self.duplicateRecord(itemId)
        self.renewListAndSetTo(newItemId)


    def saveExpandedState(self):
        def saveStateInternal(model,  parent=QModelIndex(),  prefix=''):
            for column in xrange(model.columnCount(parent)):
                for row in xrange(model.rowCount(parent)):
                    index = model.index(row, column,  parent)
                    if index.isValid():
                        prefix += index.internalPointer().name() + '_'
                        isExpanded = self.treeItems.isExpanded(index)
                        if isExpanded:
                            self.expandedItemsState[prefix] = isExpanded
                            saveStateInternal(model,  index, prefix)
        self.expandedItemsState = {}
        saveStateInternal(self.modelTree)


    def restoreExpandedState(self):
        def restoreStateInternal(model,  parent=QModelIndex(),  prefix=''):
            for column in xrange(model.columnCount(parent)):
                for row in xrange(model.rowCount(parent)):
                    index = model.index(row, column,  parent)
                    if index.isValid():
                        prefix += index.internalPointer().name() + '_'
                        isExpanded = self.expandedItemsState.get(prefix,  False)
                        if isExpanded:
                            self.treeItems.setExpanded(index, isExpanded)
                            restoreStateInternal(model,  index, prefix)
        restoreStateInternal(self.modelTree)
        self.expandedItemsState.clear()

#    @pyqtSignature('int, int')
#    def on_splitterTree_splitterMoved(self, pos, index):
#        print pos, index


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelTree_currentChanged(self, current, previous):
        self.renewListAndSetToWithoutUpdate(None)


    @pyqtSignature('QModelIndex')
    def on_tblItems_doubleClicked(self, index):
        if self.forSelect:
            self.on_btnSelect_clicked()
        else:
            self.on_btnEdit_clicked()


    @pyqtSignature('')
    def on_btnFind_clicked(self):
        if self.findClass:
            dialog = self.findClass(self)
            try:
                dialog.setProps(self.props)
                if dialog.exec_():
                    self.props = dialog.getProps()
                    id = dialog.id()
                    self.findById(id)
            finally:
                dialog.deleteLater()


    @pyqtSignature('')
    def on_btnFilter_clicked(self):
        if self.filterClass:
            dialog = self.filterClass(self)
            try:
                dialog.setProps(self.props)
                if dialog.exec_():
                    self.props = dialog.props()
                    self.renewListAndSetTo(None)
            finally:
                dialog.deleteLater()


    @pyqtSignature('')
    def on_btnSelect_clicked(self):
        self.accept()



    @pyqtSignature('')
    def on_btnNew_clicked(self):
        dialog = self.getItemEditor()
        try:
            dialog.setGroupId(self.currentGroupId())
            if dialog.exec_():
                itemId = dialog.itemId()
                self.modelTree.update()
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
                    self.modelTree.update()
                    self.renewListAndSetTo(itemId)
            finally:
                dialog.deleteLater()
        else:
            self.on_btnNew_clicked()


#
# #######################################################################
#

#class CItemEditorBaseDialog(CDialogBase):
#class CItemEditorDialog(CItemEditorBaseDialog, Ui_ItemEditorDialog):
