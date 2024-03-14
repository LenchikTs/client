# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant, pyqtSignature, SIGNAL

from library.HierarchicalItemsListDialog import CHierarchicalItemsListDialog
from library.InDocTable        import CRBInDocTableCol, CInDocTableModel, CIntInDocTableCol
from library.interchange       import setCheckBoxValue, getCheckBoxValue, getComboBoxValue, getLineEditValue, getRBComboBoxValue, getSpinBoxValue, getTextEditValue, setComboBoxValue, setLineEditValue, setRBComboBoxValue, setSpinBoxValue, setTextEditValue
from library.ItemsListDialog   import CItemEditorBaseDialog
from library.TableModel        import CEnumCol, CTextCol
from library.Utils             import forceRef, forceString, toVariant, forceInt

from Events.ActionStatus       import CActionStatus
from Events.ActionTypeComboBox import CActionTypeComboBox

from RefBooks.Tables           import rbCode, rbName

from .Ui_RBJobTypeEditor import Ui_ItemEditorDialog


actionPersonChangerValues = [u'Не меняется',
                             u'Пользователь',
                             u'Назначивший действие',
                             u'Ответственный за событие']


actionDateChagerValues = [u'Не меняется',
                          u'Дата окончания']


class CRBJobTypeList(CHierarchicalItemsListDialog):
    class CStatusChangerCol(CEnumCol):
        def format(self, values):
            val = values[0]
            i = forceRef(val)
            if i is None:
                return u'Не меняется'
            return CEnumCol.format(self, values)


    def __init__(self, parent):
        CHierarchicalItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Региональный код',  ['regionalCode'], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CRBJobTypeList.CStatusChangerCol(u'Модификатор статуса действия', ['actionStatusChanger'], CActionStatus.names, 30),
            CEnumCol(u'Модификатор исполнителя действия', ['actionPersonChanger'], actionPersonChangerValues, 30),
            CEnumCol(u'Модификатор даты действия', ['actionDateChanger'], actionDateChagerValues, 30)
            ], 'rbJobType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы работ')


    def preSetupUi(self):
        CHierarchicalItemsListDialog.preSetupUi(self)
        self.modelTree.setLeavesVisible(True)
        self.modelTree.setOrder('code')
        self.addObject('actDuplicate', QtGui.QAction(u'Дублировать', self))
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))


    def postSetupUi(self):
        CHierarchicalItemsListDialog.postSetupUi(self)
        self.tblItems.createPopupMenu([self.actDuplicate, '-', self.actDelete])
        self.connect(self.tblItems.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)
        self.treeItems.expand(self.modelTree.index(0, 0))
        self.treeItems.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.connect(self.modelTree, SIGNAL('saveExpandedState()'), self.saveExpandedState)
        self.connect(self.modelTree, SIGNAL('restoreExpandedState()'), self.restoreExpandedState)
        pref = QtGui.qApp.preferences
        props = pref.appPrefs
        expand = forceInt(props.get('actionTypeTreeExpand', QVariant()))
        if not expand:
            self.treeItems.expandToDepth(0)
        elif expand == 1:
            self.treeItems.expandAll()
        else:
            expandLevel = forceInt(props.get('actionTypeTreeExpandLevel', QVariant(1)))
            self.treeItems.expandToDepth(expandLevel)


    def getItemEditor(self):
        return CRBJobTypeEditor(self)


    def popupMenuAboutToShow(self):
        currentItemId = self.currentItemId()
        self.actDuplicate.setEnabled(bool(currentItemId))
        self.actDelete.setEnabled(bool(currentItemId))


    @pyqtSignature('')
    def on_actDuplicate_triggered(self):
        def duplicateGroup(currentGroupId, newGroupId):
            db = QtGui.qApp.db
            table = db.table('rbJobType')
            records = db.getRecordList(table, '*', table['group_id'].eq(currentGroupId))
            for record in records:
                currentItemId = record.value('id')
                record.setValue('group_id', toVariant(newGroupId))
                record.setNull('id')
                newItemId = db.insertRecord(table, record)
                db.copyDepended(db.table('rbJobType_ActionType'), 'master_id', currentItemId, newItemId)
                duplicateGroup(currentItemId, newItemId)

        def duplicateCurrentInternal():
            currentItemId = self.currentItemId()
            if currentItemId:
                db = QtGui.qApp.db
                table = db.table('rbJobType')
                db.transaction()
                try:
                    record = db.getRecord(table, '*', currentItemId)
                    record.setValue('code', toVariant(forceString(record.value('code'))+'_1'))
                    record.setNull('id')
                    newItemId = db.insertRecord(table, record)
                    db.copyDepended(db.table('rbJobType_ActionType'), 'master_id', currentItemId, newItemId)
                    duplicateGroup(currentItemId, newItemId)
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
                table = db.table('rbJobType')
                db.deleteRecord(table, table['id'].eq(currentItemId))
                self.renewListAndSetTo()
                self.tblItems.setCurrentRow(row)
        QtGui.qApp.call(self, deleteCurrentInternal)


#
# ##########################################################################
#

class CRBJobTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbJobType')
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип работы')
        self.cmbActionStatusChanger.insertSpecialValue(u'Не меняется', None)
        self.setupDirtyCather()
        self.groupId = None
        self.addModels('JobTypeActions', CJobTypeActionsModel(self))
        self.setModels(self.tblJobTypeActions, self.modelJobTypeActions, self.selectionModelJobTypeActions)
        self.tblJobTypeActions.addPopupDelRow()


    def setGroupId(self, id):
        self.groupId = id


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.groupId = forceRef(record.value('group_id'))
        setLineEditValue(   self.edtCode,                record, 'code')
        setLineEditValue(   self.edtName,                record, 'name')
        setLineEditValue(   self.edtRegionalCode,        record, 'regionalCode')
        setSpinBoxValue(    self.edtCapacity,            record, 'capacity')
        setRBComboBoxValue( self.cmbActionStatusChanger, record, 'actionStatusChanger')
        setComboBoxValue(   self.cmbActionPersonChanger, record, 'actionPersonChanger')
        setComboBoxValue(   self.cmbActionDateChanger,   record, 'actionDateChanger')
        setSpinBoxValue(    self.edtTicketDuration,      record, 'ticketDuration')
        setLineEditValue(   self.edtListContext,         record, 'listContext')
        setTextEditValue(   self.edtNote,                record, 'notes')
        setCheckBoxValue(   self.chkManualExecutionAssignments, record, 'manualExecutionAssignments')
        self.modelJobTypeActions.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('group_id', toVariant(self.groupId))
        getLineEditValue(   self.edtCode,                record, 'code')
        getLineEditValue(   self.edtName,                record, 'name')
        getLineEditValue(   self.edtRegionalCode,        record, 'regionalCode')
        getSpinBoxValue(    self.edtCapacity,            record, 'capacity')
        getRBComboBoxValue( self.cmbActionStatusChanger, record, 'actionStatusChanger')
        getComboBoxValue(   self.cmbActionPersonChanger, record, 'actionPersonChanger')
        getComboBoxValue(   self.cmbActionDateChanger,   record, 'actionDateChanger')
        getSpinBoxValue(    self.edtTicketDuration,      record, 'ticketDuration')
        getLineEditValue(   self.edtListContext,         record, 'listContext')
        getTextEditValue(   self.edtNote,                record, 'notes')
        getCheckBoxValue(   self.chkManualExecutionAssignments, record, 'manualExecutionAssignments')
        return record


    def saveInternals(self, id):
        self.modelJobTypeActions.saveItems(id)


    @pyqtSignature('int')
    def on_cmbActionStatusChanger_currentIndexChanged(self, index):
        finished = self.cmbActionStatusChanger.value() == CActionStatus.finished
        if finished:
            if self.chkManualExecutionAssignments.isChecked():
                self.chkManualExecutionAssignments.setChecked(False)
        self.chkManualExecutionAssignments.setEnabled(not finished)


# ############################################################################


class CJobTypeActionsCol(CRBInDocTableCol):
    def __init__(self):
        CRBInDocTableCol.__init__(self, u'Тип действия',  'actionType_id', 10, 'ActionType', preferredWidth=300)


    def createEditor(self, parent):
        editor = CActionTypeComboBox(parent)
        editor.setPreferredWidth(self.preferredWidth)
        return editor


class CJobTypeActionsModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbJobType_ActionType', 'id', 'master_id', parent)
        self.addCol(CJobTypeActionsCol())
        self.addCol(CIntInDocTableCol(u'Группа выбора', 'selectionGroup', 12))

    def getEmptyRecord(self):
        result = CInDocTableModel.getEmptyRecord(self)
        result.setValue('selectionGroup', QVariant(0))
        return result
