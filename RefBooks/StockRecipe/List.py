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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QVariant

from library.crbcombobox                 import CRBComboBox
from library.HierarchicalItemsListDialog import CHierarchicalItemsListDialog
from library.InDocTable                  import CInDocTableModel, CFloatInDocTableCol, CRBInDocTableCol
from library.interchange                 import getLineEditValue, setLineEditValue
from library.ItemsListDialog             import CItemEditorBaseDialog
from library.TableModel                  import CTableModel, CTextCol
from library.TreeModel                   import CDragDropDBTreeModel
from library.Utils                       import forceRef, forceString, toVariant, forceInt

from Stock.NomenclatureComboBox          import CNomenclatureInDocTableCol
from RefBooks.Tables                     import rbCode, rbName

from .Ui_RBStockRecipeEditor import Ui_ItemEditorDialog


class CLocDragDropDBTreeModel(CDragDropDBTreeModel):
    def flags(self, index):
        defaultFlags = CDragDropDBTreeModel.flags(self, index)
        if index.isValid() and index.row() > 0:
            return Qt.ItemIsDragEnabled | \
                   Qt.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemIsDropEnabled | defaultFlags
            
            
    def isBtnNewEnabled(self, current):
        isBtnNewEnabled = self.isRootIndex(current)
        if current and current.isValid() and not isBtnNewEnabled:
            row = current.internalPointer().row()
            parent = current.internalPointer().parent()
            descendanLevel = [row]
            while parent:
                descendanLevel.append(row+1)
                parent = parent.parent()
            isBtnNewEnabled = len(descendanLevel) < 3 or (len(descendanLevel) == 3 and not current.internalPointer().isLeaf())
        return isBtnNewEnabled        


    def dropMimeData(self, data, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True
        if not self.isBtnNewEnabled(parentIndex):
            return False    
        if not data.hasText():
            return False
        dragId = forceRef(forceInt(data.text()))
        parentId = self.itemId(parentIndex)
        self.changeParent(dragId, parentId)
        self.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), parentIndex, parentIndex)
        return True
            

class CRBStockRecipeList(CHierarchicalItemsListDialog):
    def __init__(self, parent):
        CHierarchicalItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbStockRecipe', [rbCode, rbName])
        self.setWindowTitleEx(u'Рецепты производства ЛСиИМН')
        self.expandedItemsState = {}
        self.additionalPostSetupUi()


    def preSetupUi(self):
        CHierarchicalItemsListDialog.preSetupUi(self)
        self.addModels('Tree', CLocDragDropDBTreeModel(self, self.tableName, 'id', 'group_id', 'name', self.order))
        self.addModels('Table',CTableModel(self, self.cols, self.tableName))
        self.modelTree.setLeavesVisible(True)
        self.modelTree.setOrder('code')
        self.addObject('actDuplicate', QtGui.QAction(u'Дублировать', self))
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))
        self.addObject('actMakeMainOne',    QtGui.QAction(u'Сделать основным', self))


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
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnFind.setEnabled(bool(self.findClass))
        self.btnFind.setVisible(bool(self.findClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.tblItems.createPopupMenu([self.actDuplicate, '-', self.actDelete, '-', self.actMakeMainOne])
        self.connect(self.tblItems.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)


    def getItemEditor(self):
        return CRBStockRecipeEditor(self)


    def additionalPostSetupUi(self):
        self.treeItems.expand(self.modelTree.index(0, 0))
        self.treeItems.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.connect(self.modelTree, SIGNAL('saveExpandedState()'),  self.saveExpandedState)
        self.connect(self.modelTree, SIGNAL('restoreExpandedState()'),  self.restoreExpandedState)
        self.connect(self.selectionModelTree, SIGNAL('currentChanged(QModelIndex,QModelIndex)'), self.on_selectionModelTree_currentChanged)
        pref = QtGui.qApp.preferences
        props = pref.appPrefs
        expand = forceInt(props.get('actionTypeTreeExpand',  QVariant()))
        if not expand:
            self.treeItems.expandToDepth(0)
        elif expand == 1:
            self.treeItems.expandAll()
        else:
            expandLevel = forceInt(props.get('actionTypeTreeExpandLevel',  QVariant(1)))
            self.treeItems.expandToDepth(expandLevel)


    def popupMenuAboutToShow(self):
        currentItemId = self.currentItemId()
        self.actDuplicate.setEnabled(bool(currentItemId))
        self.actDelete.setEnabled(bool(currentItemId))
        isEnable = False
        if currentItemId:
            indexId = self.modelTree.findItemId(currentItemId)
            isEnable = bool(currentItemId) and self.modelTree.isLeaf(indexId)
        self.actMakeMainOne.setEnabled(isEnable)


    @pyqtSignature('')
    def on_btnNew_clicked(self):
        indexId = self.treeItems.currentIndex()
        if self.isBtnNewEnabled(indexId):
            dialog = self.getItemEditor()
            try:
                dialog.setGroupId(self.currentGroupId())
                if dialog.exec_():
                    itemId = dialog.itemId()
                    self.modelTree.update()
                    self.renewListAndSetTo(itemId)
            finally:
                dialog.deleteLater()


    def on_selectionModelTree_currentChanged(self, current, previous):
        self.btnNew.setEnabled(self.isBtnNewEnabled(current))
        self.renewListAndSetToWithoutUpdate(None)


    def isBtnNewEnabled(self, current):
        isBtnNewEnabled = self.modelTree.isRootIndex(current)
        if current and current.isValid() and not isBtnNewEnabled:
            row = current.internalPointer().row()
            parent = current.internalPointer().parent()
            descendanLevel = [row]
            while parent:
                descendanLevel.append(row+1)
                parent = parent.parent()
            isBtnNewEnabled = len(descendanLevel) < 3 or (len(descendanLevel) == 3 and not current.internalPointer().isLeaf())
        return isBtnNewEnabled

    @pyqtSignature('')
    def on_actDuplicate_triggered(self): #WTF? свой Duplicate?
        def duplicateContent(currentId, newId):
            db = QtGui.qApp.db
            table = db.table('rbStockRecipe_Item')
            records = db.getRecordList(table, '*', table['master_id'].eq(currentId))
            for record in records:
                record.setValue('master_id', toVariant(newId))
                record.setNull('id')
                db.insertRecord(table, record)

        def duplicateGroup(currentGroupId, newGroupId):
            db = QtGui.qApp.db
            table = db.table('rbStockRecipe')
            records = db.getRecordList(table, '*', table['group_id'].eq(currentGroupId))
            for record in records:
                currentItemId = record.value('id')
                record.setValue('group_id', toVariant(newGroupId))
                record.setNull('id')
                newItemId = db.insertRecord(table, record)
                duplicateGroup(currentItemId, newItemId)
                duplicateContent(currentItemId, newItemId)

        def duplicateCurrentInternal():
            currentItemId = self.currentItemId()
            if currentItemId:
                db = QtGui.qApp.db
                table = db.table('rbStockRecipe')
                db.transaction()
                try:
                    record = db.getRecord(table, '*', currentItemId)
                    record.setValue('code', toVariant(forceString(record.value('code'))+'_1'))
                    record.setNull('id')
                    newItemId = db.insertRecord(table, record)
                    duplicateGroup(currentItemId, newItemId)
                    duplicateContent(currentItemId, newItemId)
                    db.commit()
                except:
                    db.rollback()
                    QtGui.qApp.logCurrentException()
                    raise
                self.renewListAndSetTo(newItemId)
        QtGui.qApp.call(self, duplicateCurrentInternal)


    @pyqtSignature('')
    def on_actDelete_triggered(self):
        def deleteCurrentInternal():
            currentItemId = self.currentItemId()
            if currentItemId:
                row = self.tblItems.currentIndex().row()
                db = QtGui.qApp.db
                table = db.table('rbStockRecipe')
                db.deleteRecord(table, table['id'].eq(currentItemId))
                self.renewListAndSetTo()
                self.tblItems.setCurrentRow(row)
        QtGui.qApp.call(self, deleteCurrentInternal)


    @pyqtSignature('')
    def on_actMakeMainOne_triggered(self):
        currentItemId = self.currentItemId()
        if currentItemId:
            indexId = self.modelTree.findItemId(currentItemId)
            if self.modelTree.isLeaf(indexId):
                item = self.modelTree.getItemByIdEx(currentItemId)
                if not item:
                    item = self.modelTree.getItemById(currentItemId)
                if item:
                    parentIndex = self.modelTree.parentByItem(item)
                    parentId = self.modelTree.itemId(parentIndex)
                    if parentId:
                        leafIdList = self.modelTree.getItemIdListById(parentId)
                        if leafIdList:
                            db = QtGui.qApp.db
                            table = db.table('rbStockRecipe')
                            recordPrev = db.getRecordEx(table, '*', [table['id'].eq(parentId), table['deleted'].eq(0)])
                            if recordPrev:
                                groupId = forceRef(recordPrev.value('group_id'))
                                records = db.getRecordList(table, '*', [table['id'].inlist(leafIdList), table['deleted'].eq(0)])
                                for record in records:
                                    if currentItemId != forceRef(record.value('id')):
                                        record.setValue('group_id', toVariant(currentItemId))
                                    else:
                                        recordPrev.setValue('group_id', toVariant(currentItemId))
                                        record.setValue('group_id', toVariant(groupId))
                                    db.updateRecord(table, record)
                                db.updateRecord(table, recordPrev)
                    self.treeItems.expand(parentIndex)
                    self.treeItems.setCurrentIndex(parentIndex)
                    self.renewListAndSetTo(currentItemId)


#
# ##########################################################################
#

class CRBStockRecipeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbStockRecipe')
        self.addModels('InItems', CItemsModel(self, False))
        self.addModels('OutItems', CItemsModel(self, True))
        self.setupUi(self)
        self.setWindowTitleEx(u'Рецепт производства ЛСиИМН')
        self.prepareTable(self.tblInItems, self.modelInItems)
        self.prepareTable(self.tblOutItems, self.modelOutItems)
        self.setupDirtyCather()
        self.groupId = None


    def prepareTable(self, tblWidget, model):
        tblWidget.setModel(model)
        tblWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        tblWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tblWidget.addPopupDuplicateCurrentRow()
        tblWidget.addPopupSeparator()
        tblWidget.addMoveRow()
        tblWidget.addPopupDelRow()


    def setGroupId(self, id):
        self.groupId = id


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        self.groupId = forceRef(record.value('group_id'))
        self.modelInItems.loadItems(self.itemId())
        self.modelOutItems.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('group_id', toVariant(self.groupId))
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        return record


    def saveInternals(self, id):
        self.modelInItems.saveItems(id)
        self.modelOutItems.saveItems(id)


class CItemsModel(CInDocTableModel):
    def __init__(self, parent, isOut):
        CInDocTableModel.__init__(self, 'rbStockRecipe_Item', 'id', 'master_id', parent)
        self.isOut = isOut
        self._unitColumn = CRBInDocTableCol(u'Ед.Учета', 'unit_id', 12, 'rbUnit', addNone=False)
        self.addCol(CNomenclatureInDocTableCol(u'ЛСиИМН', 'nomenclature_id', 50, showFields = CRBComboBox.showName))
        self.addCol(CFloatInDocTableCol( u'Кол-во', 'qnt', 12, precision=QtGui.qApp.numberDecimalPlacesQnt()))
        self.addCol(self._unitColumn)
        self.addHiddenCol('isOut')
        self.setFilter('isOut!=0' if isOut else 'isOut=0')


    def createEditor(self, index, parent):
        editor = CInDocTableModel.createEditor(self, index, parent)
        column = index.column()
        if column == self.getColIndex('nomenclature_id'):
            filterSetter = getattr(editor, 'setOrgStructureId', None)
            if not filterSetter:
                return editor
            if not editor._stockOrgStructureId:
                filterSetter(getattr(self, '_supplierId', None))
            editor.getFilterData()
            editor.setFilter(editor._filter)
            editor.reloadData()
        elif column == self.getColIndex('unit_id'):
            self._setUnitEditorFilter(index.row(), editor)
        return editor


    def getEmptyRecord(self):
        record = CInDocTableModel.getEmptyRecord(self)
        record.setValue('isOut', toVariant(self.isOut))
        return record


    def _setUnitEditorFilter(self, row, editor):
        if 0 <= row < len(self._items):
            item = self._items[row]
            nomenclatureId = forceRef(item.value('nomenclature_id'))
            if not nomenclatureId:
                return
            editor.setFilter(self._getNomenclatureUnitFilter(nomenclatureId))


    @staticmethod
    def _getNomenclatureUnitFilter(nomenclatureId):
        if not nomenclatureId:
            return None

        result = set()
        records = QtGui.qApp.db.getRecordList('rbNomenclature_UnitRatio', where='master_id=%d AND deleted=0' % nomenclatureId)
        for record in records:
            targetUnitId = forceRef(record.value('targetUnit_id'))
            sourceUnitId = forceRef(record.value('sourceUnit_id'))
            if targetUnitId:
                result.add(targetUnitId)
            if sourceUnitId:
                result.add(sourceUnitId)
        return QtGui.qApp.db.table('rbUnit')['id'].inlist(result)


