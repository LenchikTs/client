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


from PyQt4        import QtGui
from PyQt4.QtCore import QVariant, pyqtSignature, SIGNAL

from Registry.RegistryTable import CSNILSCol
from library.AgeSelector                 import composeAgeSelector, parseAgeSelector
from library.database                    import CTableRecordCache
from library.interchange                 import getComboBoxValue, getLineEditValue, setComboBoxValue, setLineEditValue, setRBComboBoxValue, getRBComboBoxValue
from library.ItemsListDialog             import CItemEditorBaseDialog
from library.TableModel                  import CTableModel, CCol, CEnumCol, CRefBookCol, CTextCol
from library.TreeModel                   import CDragDropDBTreeModel
from library.Utils                       import forceInt, forceRef, forceString, forceStringEx, toVariant, formatNum1, trim
from Users.Rights import urAccessRefDeletedActionTemplate, urAccessRefDeletedAllActionTemplate, \
    urAccessRefUpdateOwnerActionTemplate

from Events.Action                       import CAction, CActionTypeCache
from Events.ActionPropertiesTable        import CActionPropertiesTableModel
from Events.Utils                        import setActionPropertiesColumnVisible

from .ActionTemplateListDialog           import CActionTemplateListDialog

from .Ui_ActionTemplateEditor    import Ui_ActionTemplateEditorDialog


SexList = ['', u'М', u'Ж']


class CActionTemplateList(CActionTemplateListDialog):
    def __init__(self, parent, forSelect=False):
        CActionTemplateListDialog.__init__(self, parent, [
            CRefBookCol(u'Группа',       ['group_id'], 'ActionTemplate', 10),
            CTextCol(   u'Наименование', ['name'],   40),
            CEnumCol(   u'Пол',          ['sex'], SexList, 10),
            CTextCol(   u'Возраст',      ['age'], 10),
            CRefBookCol(u'Врач',         ['owner_id'],      'vrbPersonWithSpeciality', 10),
            CSNILSCol(u'СНИЛС', ['SNILS'], 4),
            CRefBookCol(u'Специальность', ['speciality_id'], 'rbSpeciality', 10),
            CRefBookCol(u'Подразделение', ['orgStructure_id'], 'OrgStructure', 10),
            CActionTypeCol(u'Действие',  ['action_id'], 10),
            ], 'ActionTemplate', ['ActionTemplate.name', 'ActionTemplate.id'], forSelect=forSelect)
        self.setWindowTitleEx(u'Шаблоны действий')
        self.expandedItemsState = {}
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.additionalPostSetupUi()
        self.renewListAndSetToWithoutUpdate()
        self.cmbActionType.setClassesPopupVisible(True)


    def preSetupUi(self):
        self.addModels('Tree', CDragDropDBTreeModel(self, self.tableName, 'id', 'group_id', 'name', self.order))
        self.addModels('Table', CTableModel(self, self.cols, self.tableName))
        self.modelTree.setLeavesVisible(True)
        self.modelTree.setOrder('name')
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))
        self.addObject('actDuplicate',    QtGui.QAction(u'Дублировать', self))
        self.addObject('actCopyCurrentItem', QtGui.QAction(u'Копировать', self))
        self.addObject('actPasteCurrentItem', QtGui.QAction(u'Вставить', self))
        self.addObject('actSelectAllRow', QtGui.QAction(u'Выделить все строки', self))
        self.addObject('actClearSelectionRow', QtGui.QAction(u'Снять выделение', self))
        self.addObject('actDelSelectedRows', QtGui.QAction(u'Удалить выделенные строки', self))


    def postSetupUi(self):
        CActionTemplateListDialog.postSetupUi(self)
        self.tblItems.createPopupMenu([self.actDelete])
        self.connect(self.tblItems.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)
        self.tblItems.addPopupAction(self.actDuplicate)
        self.connect(self.actDuplicate, SIGNAL('triggered()'), self.duplicateCurrentRow)

        self.tblItems.addPopupSeparator()
        self.tblItems.addPopupAction(self.actCopyCurrentItem)
        self.connect(self.actCopyCurrentItem, SIGNAL('triggered()'), self.copyCurrentItem)
        self.tblItems.addPopupAction(self.actPasteCurrentItem)
        self.actPasteCurrentItem.setEnabled(0)
        self.connect(self.actPasteCurrentItem, SIGNAL('triggered()'), self.pasteCurrentItem)

        self.tblItems.addPopupSeparator()
        self.tblItems.addPopupAction(self.actSelectAllRow)
        self.connect(self.actSelectAllRow, SIGNAL('triggered()'), self.selectAllRowTblItem)
        self.tblItems.addPopupAction(self.actClearSelectionRow)
        self.connect(self.actClearSelectionRow, SIGNAL('triggered()'), self.clearSelectionRow)
        self.tblItems.addPopupAction(self.actDelSelectedRows)
        self.connect(self.actDelSelectedRows, SIGNAL('triggered()'), self.delSelectedRows)
        self.tblItems.addPopupRecordProperies()


    def selectAllRowTblItem(self):
        self.tblItems.selectAll()


    def clearSelectionRow(self):
        self.tblItems.clearSelection()


    def delSelectedRows(self):
        db = QtGui.qApp.db
        selectedIdList = self.tblItems.selectedItemIdList()
        tableActionTemplate = db.table('ActionTemplate')
        if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить выделенные строки?(количество строк: %d)'% len(selectedIdList),
                                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No
                                    ) == QtGui.QMessageBox.Yes:
            for id in selectedIdList:
                record = db.getRecord(tableActionTemplate, ['id','deleted'], id)
                record.setValue('deleted', QVariant(1))
                db.updateRecord(tableActionTemplate, record)
        self.modelTree.update()
        self.renewListAndSetTo()


    def copyCurrentItem(self):
        selectedIdList = self.tblItems.selectedItemIdList()
        if selectedIdList:
            result = set(selectedIdList)
            self.copyList = list(result)
            self.statusBar.showMessage(u'Готово к копированию %i элементов.'%len(selectedIdList),  5000)
            self.actPasteCurrentItem.setEnabled(1)


    def insertGroupIdDescendants(self, id, firstGroupId):
        db = QtGui.qApp.db
        db.checkdb()
        table = db.forceTable('ActionTemplate')
        group = table['group_id']
        result = set([id])
        parents = [id]
        groupIdList = {id:firstGroupId}
        while parents:
            children = set(db.getIdList(table, where=group.inlist(parents)))
            records = db.getRecordList(table, '*', [table['group_id'].inlist(parents), table['deleted'].eq(0)])
            for record in records:
                actionTypeId = forceRef(record.value('id'))
                groupId = forceRef(record.value('group_id'))
                updateGroupId = groupIdList.get(groupId, firstGroupId)
                record.setNull('id')
                record.setValue('group_id', toVariant(updateGroupId))
                newId = db.insertRecord(table.name(), record)
                groupIdList[actionTypeId] = newId
            newChildren = children-result
            result |= newChildren
            parents = newChildren
        return list(result)


    def pasteCurrentItem(self):
        db = QtGui.qApp.db
        tableActionTemplate = db.table('ActionTemplate')
        currentGroup = self.treeItems.currentIndex().internalPointer()._id
        count = 0
        if self.copyList != []:
            self.statusBar.showMessage(u'Подождите, подготовка к копированию..',  5000)
            listLength = len(self.copyList)
            for id in self.copyList:
                db.transaction()
                try:
                    self.statusBar.showMessage(u'Подождите, идет копирование %i из %i элементов..'%(count,  listLength),  5000)
                    recordActionTemplate = db.getRecordEx(tableActionTemplate, '*', [tableActionTemplate['id'].eq(id), tableActionTemplate['deleted'].eq(0)])
                    recordActionTemplate.setNull('id')
                    recordActionTemplate.setValue('group_id', toVariant(currentGroup))
                    newItemId = db.insertRecord(tableActionTemplate, recordActionTemplate)
                    self.insertGroupIdDescendants(id, newItemId)
                    db.commit()
                    count += 1
                except:
                    db.rollback()
                    QtGui.qApp.logCurrentException()
                    raise
            self.renewListAndSetTo(newItemId)
            self.statusBar.showMessage(u'Скопировано %i элементов.'%count,  5000)
            self.renewListAndSetTo(newItemId)
            self.statusBar.showMessage(u'Перемещено %i элементов.'%count,  5000)


    def additionalPostSetupUi(self):
        self.treeItems.expand(self.modelTree.index(0, 0))
        #drag-n-drop support
        self.treeItems.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        # tree popup menu
        self.treeItems.createPopupMenu([self.actDelete])
        self.connect(self.treeItems.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)
        self.connect(self.modelTree, SIGNAL('saveExpandedState()'),  self.saveExpandedState)
        self.connect(self.modelTree, SIGNAL('restoreExpandedState()'),  self.restoreExpandedState)
        pref=QtGui.qApp.preferences
        props = pref.appPrefs
        expand = forceInt(props.get('actionTypeTreeExpand',  QVariant()))
        if not expand:
            self.treeItems.expandToDepth(0)
        elif expand == 1:
            self.treeItems.expandAll()
        else:
            expandLevel = forceInt(props.get('actionTypeTreeExpandLevel',  QVariant(1)))
            self.treeItems.expandToDepth(expandLevel)


    def getItemEditor(self):
        return CActionTemplateEditor(self)


    def popupMenuAboutToShow(self):
        actionEnabled = False
        app = QtGui.qApp
        currentUserId = app.userId
        if currentUserId:
            currentItemId = self.currentItemId()
            if currentItemId:
                isAdmin = app.isAdmin()
                db = QtGui.qApp.db
                table = db.table('ActionTemplate')
                record = db.getRecordEx(table, [table['createPerson_id'], table['owner_id']], [table['id'].eq(currentItemId), table['deleted'].eq(0)])
                createPersonId = forceRef(record.value('createPerson_id')) if record else None
                ownerId = forceRef(record.value('owner_id')) if record else None
                actionEnabled = bool(currentItemId) and (isAdmin or (app.userHasAnyRight([urAccessRefDeletedActionTemplate]) and createPersonId == currentUserId) or (app.userHasAnyRight([urAccessRefUpdateOwnerActionTemplate]) and ownerId == currentUserId))
        self.actDelete.setEnabled(actionEnabled)
        self.actCopyCurrentItem.setEnabled(actionEnabled)
        self.actPasteCurrentItem.setEnabled(actionEnabled)
        self.actSelectAllRow.setEnabled(actionEnabled)
        self.actClearSelectionRow.setEnabled(actionEnabled)
        self.actDelSelectedRows.setEnabled(actionEnabled)


    def copyInternals(self, newItemId, itemId):
        db = QtGui.qApp.db
        table = self.modelTable.table()
        record = db.getRecord(table, 'id, action_id', newItemId)
        oldActionId = forceRef(record.value('action_id'))
        if oldActionId:
            newAction = CAction.getActionById(oldActionId).clone()
            newActionId = newAction.save()
            record.setValue('action_id', newActionId)
            db.updateRecord(table, record)


    @pyqtSignature('')
    def on_actDelete_triggered(self):
        id = self.currentItemId()
        if id:
            row = self.tblItems.currentIndex().row()
            success, deleted = QtGui.qApp.call(self, deleteActionTemplateAndDescendants, (self, id))
            if deleted:
                self.renewListAndSetTo()
                self.tblItems.setCurrentRow(row)


class CActionTypeCol(CCol):
    def __init__(self, title, fields, defaultWidth, alignment='l'):
        CCol.__init__(self, title, fields, defaultWidth, alignment)
        db = QtGui.qApp.db
        self._cache = CTableRecordCache(db, 'Action', 'actionType_id')


    def getActionTypeId(self, actionId):
        if actionId:
            record = self._cache.get(actionId)
            if record:
                return forceRef(record.value(0))
        return None


    def format(self, values):
        val = values[0]
        actionTypeId = self.getActionTypeId(forceRef(val))
        if actionTypeId:
            actionType = CActionTypeCache.getById(actionTypeId)
            if actionType:
                return QVariant(actionType.code+' | '+actionType.name)
        return QVariant()


    def invalidateRecordsCache(self):
        self._cache.invalidate()


class CActionTemplateEditor(CItemEditorBaseDialog, Ui_ActionTemplateEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'ActionTemplate')
        self.addModels('ActionProperties', CActionPropertiesTableModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Шаблон действия')
        self.cmbGroup.setTable('ActionTemplate')
        self.cmbActionType.setClasses([0, 1, 2, 3])
        self.cmbActionType.setClassesVisible(True)
        self.cmbSpeciality.setTable('rbSpeciality')
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.setModels(self.tblProps, self.modelActionProperties, self.selectionModelActionProperties)
        self.groupId = None
        self.action = None
        self.actionId = None
        self.cmbGroup.setEnabled(False)
        self.setupDirtyCather()


    def setGroupId(self, id):
        self.groupId = id
        self.cmbGroup.setValue(self.groupId)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.setGroupId(forceRef(record.value('group_id')))
#        getLineEditValue(   self.edtCode,           record, 'code')
        setLineEditValue(   self.edtName,           record, 'name')
        setComboBoxValue(   self.cmbSex,            record, 'sex')
        setRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(forceString(record.value('age')))
        self.cmbBegAgeUnit.setCurrentIndex(begUnit)
        self.edtBegAgeCount.setText(str(begCount))
        self.cmbEndAgeUnit.setCurrentIndex(endUnit)
        self.edtEndAgeCount.setText(str(endCount))

        ownerId = forceRef(record.value('owner_id'))
        specialityId = forceRef(record.value('speciality_id'))
        orgStructureId = forceRef(record.value('orgStructure_id'))
        SNILS = forceRef(record.value('SNILS'))
        if ownerId:
            self.rbVisibleToOwner.setChecked(True)
            self.cmbOwner.setValue(ownerId)
        elif orgStructureId:
            self.rbVisibleToOrgStructure.setChecked(True)
            self.cmbOrgStructure.setValue(orgStructureId)
        elif specialityId:
            self.rbVisibleToSpeciality.setChecked(True)
            self.cmbSpeciality.setValue(specialityId)
        elif SNILS:
            self.rbVisibleToSNILS.setChecked(True)
        else:
            self.rbVisibleToAll.setChecked(True)
        if not SNILS and ownerId:
            SNILS = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('Person'), 'id', ownerId, 'SNILS'))
            if SNILS:
                record.setValue('SNILS',  toVariant(SNILS))
        self.setActionId(forceRef(record.value('action_id')))
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('group_id', toVariant(self.groupId))
#        getLineEditValue(   self.edtCode,           record, 'code')
        getLineEditValue(   self.edtName,           record, 'name')
        getComboBoxValue(   self.cmbSex,            record, 'sex')
        getRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        record.setValue('age',        toVariant(composeAgeSelector(
                    self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
                    self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text())
                        )))
        record.setValue('owner_id', toVariant(self.cmbOwner.value() if self.rbVisibleToOwner.isChecked() else None))
        record.setValue('speciality_id', toVariant(self.cmbSpeciality.value() if self.rbVisibleToSpeciality.isChecked() else None))
        record.setValue('orgStructure_id', toVariant(self.cmbOrgStructure.value() if self.rbVisibleToOrgStructure.isChecked() else None))
        db = QtGui.qApp.db
        if self.rbVisibleToSNILS.isChecked():
            SNILS = forceString(db.translate(db.table('Person'), 'id', QtGui.qApp.userId, 'SNILS'))
            record.setValue('SNILS',  toVariant(SNILS))  # if self.rbVisibleToSNILS.isChecked() else None)
        else:
            ownerId = forceRef(record.value('owner_id'))
            if ownerId and not self.rbVisibleToAll.isChecked() and not self.cmbGroup.value():
                SNILS = forceString(db.translate(db.table('Person'), 'id', ownerId, 'SNILS'))
                record.setValue('SNILS',  toVariant(SNILS))
            else:
                record.setValue('SNILS',  toVariant(None))
        record.setValue('action_id', toVariant(self.saveAction()))
        return record


    def checkDataEntered(self):
#        result = CItemEditorBaseDialog.checkDataEntered(self)
        result = True
        result = result and (forceStringEx(self.edtName.text()) or self.checkInputMessage(u'наименование', False, self.edtName))
        result = result and (not self.rbVisibleToOwner.isChecked() or self.cmbOwner.value() or self.checkInputMessage(u'врача', False, self.cmbOwner))
        result = result and (not self.rbVisibleToSpeciality.isChecked() or self.cmbSpeciality.value() or self.checkInputMessage(u'специальность', False, self.cmbSpeciality))
        result = result and (not self.rbVisibleToOrgStructure.isChecked() or self.cmbOrgStructure.value() or self.checkInputMessage(u'подразделение', False, self.cmbOrgStructure))
        if forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('Person'), 'id', QtGui.qApp.userId, 'SNILS')) == u'' and self.rbVisibleToSNILS.isChecked():
            res = QtGui.QMessageBox.warning( self,
                                         u'Внимание!',
                                         u'У Вас не указан СНИЛС. Выберите другой параметр для сохранения шаблона.',
                                         QtGui.QMessageBox.Ok,
                                         QtGui.QMessageBox.Ok)
            if res:
                result = False
        begAgeUnit = self.cmbBegAgeUnit.currentIndex()
        begAgeCount = forceInt(QVariant(self.edtBegAgeCount.text())) if bool(trim(self.edtBegAgeCount.text())) else -1
        endAgeUnit = self.cmbEndAgeUnit.currentIndex()
        endAgeCount = forceInt(QVariant(self.edtEndAgeCount.text())) if bool(trim(self.edtEndAgeCount.text())) else -1
        if result and begAgeUnit > 0 and begAgeCount < 0:
            result = result and self.checkInputMessage(u' возраст: начало периода', False, self.edtBegAgeCount)
        if result and begAgeUnit <= 0 and begAgeCount > 0:
            result = result and self.checkInputMessage(u' возраст: начало периода', False, self.cmbBegAgeUnit)
        if result and endAgeUnit > 0 and endAgeCount < 0:
            result = result and self.checkInputMessage(u' возраст: конец периода', False, self.edtEndAgeCount)
        if result and endAgeUnit <= 0 and endAgeCount > 0:
            result = result and self.checkInputMessage(u' возраст: конец периода', False, self.cmbEndAgeUnit)
        return result


    def setActionId(self, actionId):
        self.actionId = actionId
        self.setAction(CAction.getActionById(actionId))


    def setAction(self, action):
        self.action = action
        if action:
            actionTypeId = action.getType().id
        else:
            actionTypeId = None
        self.setActionTypeId(actionTypeId)
        if self.action:
            self.tblProps.model().setAction(self.action, None, 0, None, None)
            self.tblProps.resizeRowsToContents()
            actionType = self.action.getType()
            setActionPropertiesColumnVisible(actionType, self.tblProps)


    def setActionTypeId(self, actionTypeId):
        self.cmbActionType.setValue(actionTypeId)
        self.tabWidget.setTabEnabled(1, bool(actionTypeId))
        if actionTypeId:
            if (not self.action or self.action.getType().id != actionTypeId):
                self.action = CAction.createByTypeId(actionTypeId)
                self.tblProps.model().setAction(self.action, None, 0, None, None)
                self.tblProps.resizeRowsToContents()
        else:
            self.action = None
            self.tblProps.model().setAction(self.action, None, 0, None, None)
            self.tblProps.resizeRowsToContents()


    def saveAction(self):
        if self.action:
            actionId = self.action.save()
        else:
            actionId = None
        if self.actionId and self.actionId != actionId:
            db = QtGui.qApp.db
            table = db.table('Action')
            db.deleteRecord(table, table['id'].eq(self.actionId))
            self.actionId = actionId
        return actionId


    @pyqtSignature('int')
    def on_cmbActionType_currentIndexChanged(self, index):
        self.setActionTypeId(self.cmbActionType.value())


def deleteActionTemplateAndDescendants(parentWidget, id):
    db = QtGui.qApp.db
    table = db.table('ActionTemplate')
    actionTemplateIdList = db.getDescendants(table, 'group_id', id, 'deleted=0')
    if actionTemplateIdList == [id] :
        question = u'Удалить данную группу шаблонов?'
    else:
        question = u'Удалить группу со всеми вложенными шаблонами\nи %s?' %\
            formatNum1(len(actionTemplateIdList)-1,
                        (u'входящий в неё элемент',
                            u'входящего в неё элемента',
                            u'входящих в неё элементов',
                        )
                        )
    res = QtGui.QMessageBox.question(parentWidget,
                                        u'Подтверждение удаления',
                                        question,
                                        QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                        QtGui.QMessageBox.No
                                        )
    if res == QtGui.QMessageBox.Yes:
        db.markRecordsDeleted(table, table['id'].inlist(actionTemplateIdList))
        return True
    else:
        return False
