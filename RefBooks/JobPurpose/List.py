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
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QVariant, SIGNAL, QModelIndex, QObject, pyqtSignature

from Events.ActionTypeComboBox import CActionTypeTableCol
from Events.Utils import getWorkEventTypeFilter
from library.AgeSelector     import parseAgeSelector, composeAgeSelector
from library.InDocTable      import CInDocTableModel, CEnumInDocTableCol, CRBInDocTableCol
from library.interchange     import (
                                        setLineEditValue, setComboBoxValue, setSpinBoxValue,
                                        getLineEditValue, getComboBoxValue, getSpinBoxValue
                                    )
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CTableModel
from library.Utils           import forceBool, forceInt, forceString, forceStringEx, toVariant, forceRef
from library.SortFilterProxyTableModel import CSortFilterProxyTableModel


from Orgs.OrgStructureCol    import COrgStructureInDocTableCol
from RefBooks.Tables         import rbCode, rbName, rbJobPurpose
from RefBooks.JobPurpose.Ui_RBJobPurposeListDialog import Ui_RBJobPurposeListDialog

from .Ui_RBJobPurposeEditor import Ui_RBJobPurposeEditorDialog
from .Ui_RBJobFilterDialog import Ui_RBJobFilterDialog


class CRBJobPurposeList(CItemsListDialog, Ui_RBJobPurposeListDialog):
    setupUi = Ui_RBJobPurposeListDialog.setupUi
    retranslateUi = Ui_RBJobPurposeListDialog.retranslateUi

    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 32),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbJobPurpose, [rbCode, rbName], filterClass=CRBJobFilterDialog)
        self.setWindowTitleEx(u'Назначения работы')
        self.setupMenu()


    def setup(self, cols, tableName, order, forSelect=False, filterClass=None):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.props = {}
        self.order = order
        self.addModels('', CTableModel(self, cols))
        self.addModels('RBJobPurpose', CSortFilterProxyTableModel(self, self.model))
        self.model = self.modelRBJobPurpose.sourceModel()
        self.model.idFieldName = self.idFieldName
        self.model.setTable(tableName)
        self.setModels(self.tblItems, self.modelRBJobPurpose, self.selectionModelRBJobPurpose)
        self.btnSelect.setEnabled(self.forSelect)
        self.btnSelect.setVisible(self.forSelect)
        self.btnSelect.setDefault(self.forSelect)
        self.btnFilter.setEnabled(self.forSelect and bool(self.filterClass))
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.btnNew.setShortcut('F9')
        self.btnEdit.setShortcut('F4')
        self.btnPrint.setShortcut('F6')

        QObject.connect(self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)


    def setupMenu(self):
        self.addObject('actDuplicate', QtGui.QAction(u'Дублировать', self))
        self.addObject('actRemove', QtGui.QAction(u'Удалить', self))

        self.tblItems.addPopupAction(self.actDuplicate)
        self.tblItems.addPopupAction(self.actRemove)

        self.connect(self.actDuplicate, SIGNAL('triggered()'), self.duplicateCurrentRow)
        self.connect(self.actRemove, SIGNAL('triggered()'), self.removeCurrentRow)


    def copyInternals(self, newItemId, oldItemId):
        db = QtGui.qApp.db
        tablePractice = db.table('rbJobPurpose_Practice')
        records = db.getRecordList(
            tablePractice, '*',
            tablePractice['master_id'].eq(oldItemId))
        for record in records:
            record.setNull('id')
            record.setValue('master_id', toVariant(newItemId))
            db.insertRecord(tablePractice, record)

    def duplicateCurrentRow(self):
        newItemIds = []
        for itemsIndex in self.tblItems.selectionModel().selectedRows():
            sortIndex = self.modelRBJobPurpose.index(itemsIndex.row(), 0)
            if sortIndex.isValid():
                sortRow = self.modelRBJobPurpose.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            newItemIds.append(self.duplicateRecord(itemId))
        for newItemId in newItemIds:
            self.renewListAndSetTo(newItemId)


    def removeCurrentRow(self):
        for itemsIndex in self.tblItems.selectionModel().selectedRows():
            sortIndex = self.modelRBJobPurpose.index(itemsIndex.row(), 0)
            if sortIndex.isValid():
                sortRow = self.modelRBJobPurpose.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            db = QtGui.qApp.db
                            table = db.table('rbJobPurpose')
                            db.deleteRecord(table, table['id'].eq(itemId))
        self.renewListAndSetTo(None, itemsIndex.row())


    def getItemEditor(self):
        return CRBJobPurposeEditor(self)

    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        currRow = self.tblItems.currentRow()
        if currRow is not None and currRow >= 0:
            sortIndex = self.modelRBJobPurpose.index(currRow, 0)
            if sortIndex.isValid():
                sortRow = self.modelRBJobPurpose.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            dialog = self.getItemEditor()
                            try:
                                dialog.load(itemId)
                                if dialog.exec_():
                                    itemId = dialog.itemId()
                                    self.renewListAndSetTo(itemId, sortIndex.row())
                            finally:
                                dialog.deleteLater()
                        else:
                            self.on_btnNew_clicked()
        else:
            self.on_btnNew_clicked()

    def renewListAndSetTo(self, itemId=None, index=-1):
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, itemId)
        self.label.setText(u'всего: %d' % len(idList))
        if index == -1 and itemId:
            index = self.tblItems.model().findItemIdIndex(itemId)
        if index >= 0:
            self.tblItems.selectRow(index)
        code = self.props.get('Код', '')
        if code:
            self.modelRBJobPurpose.setFilter('code', code, CSortFilterProxyTableModel.MatchStartsWith)
        else:
            self.modelRBJobPurpose.removeFilter('code')
        name = self.props.get('Наименование', '')
        if name:
            self.modelRBJobPurpose.setFilter('name', name, CSortFilterProxyTableModel.MatchContains)
        else:
            self.modelRBJobPurpose.removeFilter('name')

#
# ##########################################################################
#


class CRBJobPurposeEditor(Ui_RBJobPurposeEditorDialog, CItemEditorBaseDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbJobPurpose)
        self.addModels('Practices',  CPracticesModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Назначение работы')
        self.setModels(self.tblPractices, self.modelPractices, self.selectionModelPractices)

        self.setupDirtyCather()
        self.tblPractices.addMoveRow()
        self.tblPractices.popupMenu().addSeparator()
        self.tblPractices.addPopupDelRow()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,           record, 'code')
        setLineEditValue(   self.edtName,           record, 'name')
        setComboBoxValue(   self.cmbSex,            record, 'sex')
        setSpinBoxValue(self.edtPrematurelyClosingThreshold, record, 'prematurelyClosingThreshold')
        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(forceString(record.value('age')))
        self.cmbBegAgeUnit.setCurrentIndex(begUnit)
        self.edtBegAgeCount.setText(str(begCount))
        self.cmbEndAgeUnit.setCurrentIndex(endUnit)
        self.edtEndAgeCount.setText(str(endCount))
        self.modelPractices.loadItems(self.itemId())
#        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,           record, 'code')
        getLineEditValue(   self.edtName,           record, 'name')
        getComboBoxValue(   self.cmbSex,            record, 'sex')
        getSpinBoxValue(self.edtPrematurelyClosingThreshold, record, 'prematurelyClosingThreshold')
        record.setValue('age',        toVariant(composeAgeSelector(
                    self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
                    self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text())
                        )))
        return record


    def saveInternals(self, id):
        self.modelPractices.saveItems(id)


class CPracticesModel(CInDocTableModel):
    # В этой модели есть такое "украшение".
    # Записи rbJobPurpose_Practice используются
    # "по ИЛИ" если они находятся в разных группах
    # и по "И" если они находятся в одной группе.
    # Найдена возможность реализовать более привычную запись - с И и ИЛИ
    # этому посвящены поля junction и "волшебство" в flags/data/loadItems/...
    #
    # логика группировки скопирована в RefBooks/RBContractCoefficientType.py
    # будет использовата третий раз - нужно будет выносить в отдельный класс (миксин?)

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbJobPurpose_Practice', 'id', 'master_id', parent)
        self.addExtCol(CEnumInDocTableCol(u'Связка', 'junction', 5, (u'или', u'и')),
                       QVariant.Int)
        self.addCol(CEnumInDocTableCol(u'Условие', 'excludeOrgStructure', 10,
                                       (u'∈', u'∉')
                                      ))
        self.addCol(COrgStructureInDocTableCol(u'Подразделение',  'orgStructure_id',  15))
        self.addCol(CEnumInDocTableCol(u'Условие', 'excludeEventType', 10,
                                       (u'=', u'≠')
                                      ))
        self.addCol(CRBInDocTableCol(u'Тип события', 'eventType_id', 20, 'EventType', filter=getWorkEventTypeFilter()))
        self.addCol(CEnumInDocTableCol(u'Условие', 'excludeActionType', 10,
                                       (u'=', u'≠')
                                      ))
        self.addCol(CActionTypeTableCol(u'Тип действия', 'actionType_id', 20, None, classesVisible=True))
        self.addCol(CEnumInDocTableCol(u'Доступность', 'avail', 35,
                                       (u'недоступно', u'доступно для ручного выбора', u'доступно для автоматического выбора')
                                      ))
        self.addHiddenCol('grouping')


    def _cellIsDisabled(self, index):
        row = index.row()
        column = index.column()
        if column == 0:
            if row == 0:
                return True
        elif column == 5:  # avail
            if row+1 < len(self._items) and \
               forceBool(self._items[row+1].value('junction')):  # True == «И»
                return True
        return False


    def flags(self, index):
        if self._cellIsDisabled(index):
            return Qt.ItemIsSelectable
        return CInDocTableModel.flags(self, index)


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self._cellIsDisabled(index):
                return QVariant()
        return CInDocTableModel.data(self, index, role)


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        if role == Qt.EditRole and column == self.getColIndex('actionType_id'):
            noWriteList = True
            row = index.row()
            if row == len(self._items):
                if value.isNull():
                    return False
                outWriteList, noWriteList = self.writeActionTypeIdList(forceRef(value), row, column)
                if outWriteList:
                    return True
                self._addEmptyItem()
            record = self._items[row]
            col = self._cols[column]
            record.setValue(col.fieldName(), value)
            self.emitCellChanged(row, column)
            if noWriteList:
                outWriteList, noWriteList = self.writeActionTypeIdList(forceRef(value), row, column, True)
                if outWriteList:
                    return True
            return True
        result = CInDocTableModel.setData(self, index, value, role)
        if result:
            column = index.column()
            if column == 0:  # junction
                self.emitColumnChanged(5)  # avail
            elif column == 5:  # avail
                row = index.row()
                while row > 0:
                    if self._items[row].value('junction'):  # True == «И»
                        self._items[row-1].setValue('avail', value)
                    row -= 1
        return result


    def loadItems(self, masterId):
        CInDocTableModel.loadItems(self, masterId)
        prevGrouping = -1
        for item in self._items:
            grouping = forceInt(item.value('grouping'))
            item.setValue('junction', grouping == prevGrouping)  # True == «И»
            prevGrouping = grouping


    def saveItems(self, masterId):
        if self._items:
            grouping = -1
            for item in self._items:
                junction = forceBool(item.value('junction'))  # True == «И»
                if grouping == -1 or not junction:
                    grouping = grouping+1
                item.setValue('grouping', grouping)

            grouping = -1
            avail = None
            for item in reversed(self._items):
                currGrouping = forceInt(item.value('grouping'))
                if grouping != currGrouping:
                    avail = forceInt(item.value('avail'))
                    grouping = currGrouping
                else:
                    item.setValue('avail', avail)

        CInDocTableModel.saveItems(self, masterId)


    def getActionTypeCluster(self, actionTypeId):
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        result = db.getLeafes(tableActionType,
                              'group_id',
                              actionTypeId,
                              tableActionType['deleted'].eq(0))
        return sorted(result) if result else [actionTypeId]


    def writeActionTypeIdList(self, actionTypeId, row, column, these=False):
        if actionTypeId:
            actionTypeIdList = self.getActionTypeCluster(actionTypeId)
            if these:
                actionTypeIdList = list(set(actionTypeIdList)-set([actionTypeId]))
            else:
                if actionTypeId not in actionTypeIdList:
                    actionTypeIdList.insert(0, actionTypeId)
            if len(actionTypeIdList) > 1:
                if QtGui.QMessageBox.warning(None,
                        u'Внимание!',
                        u'Добавить группу действий?',
                        QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                        QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok:
                    for atId in actionTypeIdList:
                        self._items.append(self.getEmptyRecord())
                        count = len(self._items)
                        rootIndex = QModelIndex()
                        self.beginInsertRows(rootIndex, count, count)
                        self.insertRows(count, 1, rootIndex)
                        self.endInsertRows()
                        currentRecord = self._items[row]
                        record = self._items[count-1]
                        for col in self._cols:
                            if col == self._cols[column]:
                                record.setValue(col.fieldName(), toVariant(atId))
                            else:
                                record.setValue(col.fieldName(), currentRecord.value(col.fieldName()))
                        self.emitCellChanged(count-1, column)
                    return True, False
                else:
                    return False, False
            else:
                return False, False
        return False, False
#
# ##########################################################################
#

class CRBJobFilterDialog(QtGui.QDialog, Ui_RBJobFilterDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edtName.setFocus(Qt.ShortcutFocusReason)
    
    def setProps(self, props):
        self.edtCode.setText(props.get('Код', ''))
        self.edtName.setText(props.get('Наименование', ''))
        
    def props(self):
        result = {}
        result['Код'] = forceStringEx(self.edtCode.text())
        result['Наименование'] = forceStringEx(self.edtName.text())
        return result