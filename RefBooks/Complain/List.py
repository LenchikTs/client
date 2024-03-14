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
from PyQt4.QtCore import SIGNAL, pyqtSignature

from library.HierarchicalItemsListDialog import CHierarchicalItemsListDialog
from library.interchange                 import getLineEditValue, getRBComboBoxValue, setLineEditValue, setRBComboBoxValue
from library.ItemsListDialog             import CItemEditorBaseDialog
from library.TableModel                  import CTextCol
from library.Utils                       import formatNum1, formatNum, toVariant, forceRef, agreeNumberAndWord
from Users.Rights                        import urAccessRefMedComplainDelete

from .Ui_RBComplainEditor        import Ui_ComplainEditorDialog


class CRBComplainList(CHierarchicalItemsListDialog):

    unitNameTuple = (u'строка', u'строки', u'строк')

    def __init__(self, parent):
        CHierarchicalItemsListDialog.__init__(self, parent, [
            CTextCol(   u'Код',          ['code'], 20),
            CTextCol(   u'Наименование', ['name'],   40),
            ], 'rbComplain', ['code', 'name', 'id'])
        self.setWindowTitleEx(u'Жалобы')
        self.modelTree.setLeavesVisible(True)
        self.copyList = []
        self.cutList = []


    def preSetupUi(self):
        CHierarchicalItemsListDialog.preSetupUi(self)
        self.modelTree.setLeavesVisible(True)
        self.modelTree.setOrder('code')
        self.addObject('actDelete',         QtGui.QAction(u'Удалить', self))
        self.addObject('actDuplicate',      QtGui.QAction(u'Дублировать', self))
        self.addObject('actCopy',           QtGui.QAction(u'Копировать', self))
        self.addObject('actCut',            QtGui.QAction(u'Вырезать', self))
        self.addObject('actPaste',          QtGui.QAction(u'Вставить', self))


    def postSetupUi(self):
        CHierarchicalItemsListDialog.postSetupUi(self)
        self.tblItems.createPopupMenu([self.actDelete,
                                       self.actDuplicate,
                                       '-',
                                       self.actCopy,
                                       self.actCut,
                                       self.actPaste,
                                       ]
                                     )
        self.connect(self.tblItems.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)
        self.connect(self.actDuplicate, SIGNAL('triggered()'), self.duplicateCurrentRow)


    def select(self, props):
        table = self.modelTable.table()
        groupId = self.currentGroupId()
        return QtGui.qApp.db.getIdList(table.name(),
                           'id',
                           QtGui.qApp.db.joinAnd([table['group_id'].eq(groupId), table['deleted'].eq(0)]),
                           self.order)


    def getItemEditor(self):
        return CComplainEditor(self)


    @pyqtSignature('')
    def on_actDelete_triggered(self):
        complainId = self.currentItemId()
        if not complainId:
            return

        db = QtGui.qApp.db
        tableComplain = db.table('rbComplain')
        complainIdList = db.getDescendants(tableComplain, 'group_id', complainId, 'deleted=0')
        if complainIdList == [complainId] :
            question = u'Вы действительно хотите удалить данную жалобу?'
        else:
            question = u'Вы действительно хотите удалить данную группу жалоб\nи %s?' %\
                formatNum1(len(complainIdList)-1,
                           (u'входящий в неё элемент',
                            u'входящих в неё элемента',
                            u'входящих в неё элементов',
                           )
                          )
        answer = QtGui.QMessageBox.question(self,
                                            u'Внимание!',
                                            question,
                                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.No
                                           )
        if answer == QtGui.QMessageBox.Yes:
            db.markRecordsDeleted(tableComplain, tableComplain['id'].inlist(complainIdList))
            self.renewListAndSetTo()


    @pyqtSignature('')
    def on_actCopy_triggered(self):
        selectedIdList = self.tblItems.selectedItemIdList()
        if selectedIdList:
            self.copyList = selectedIdList
            self.cutList = []
            self.statusBar.showMessage(u'Готово к копированию %s'% formatNum(len(selectedIdList), self.unitNameTuple),
                                       5000)


    @pyqtSignature('')
    def on_actCut_triggered(self):
        selectedIdList = self.tblItems.selectedItemIdList()
        if selectedIdList:
            self.copyList = []
            self.cutList = selectedIdList
            self.statusBar.showMessage(u'Готово к перемещению %s'% formatNum(len(selectedIdList), self.unitNameTuple),
                                       5000)
            self.actPaste.setEnabled(1)


    @pyqtSignature('')
    def on_actPaste_triggered(self):
        db = QtGui.qApp.db
        tableComplain = db.table('rbComplain')
        currentGroup = self.treeItems.currentIndex().internalPointer()._id
        if self.copyList:
            self.statusBar.showMessage(u'Подождите, подготовка к копированию',  5000)
            listLength = len(self.copyList)
            count = 0
            for id in self.copyList:
                db.transaction()
                try:
                    self.statusBar.showMessage(u'Подождите, идет копирование %d из %s'% \
                                                ( count+1,
                                                  formatNum(listLength, (u'строки', u'строк', u'строк')),
                                                ),
                                               5000)
                    recordComplain = db.getRecordEx(tableComplain, '*', [tableComplain['id'].eq(id), tableComplain['deleted'].eq(0)])
                    recordComplain.setNull('id')
                    recordComplain.setValue('group_id', toVariant(currentGroup))
                    newItemId = db.insertRecord(tableComplain, recordComplain)
                    self.insertGroupIdDescendants(id, newItemId)
                    db.commit()
                    count += 1
                except:
                    db.rollback()
                    QtGui.qApp.logCurrentException()
                    raise
            self.renewListAndSetTo(newItemId)
            self.statusBar.showMessage(agreeNumberAndWord(count,
                                                          (u'Скопирована %s',
                                                           u'Скопированo %s',
                                                           u'Скопированo %s',
                                                          )
                                                         ) % formatNum(count, self.unitNameTuple),
                                       5000)
        elif self.cutList:
            self.statusBar.showMessage(u'Подождите, подготовка к перемещению',  5000)
            listLength = len(self.cutList)
            count = 0
            for id in self.cutList:
                db.transaction()
                try:
                    self.statusBar.showMessage(u'Подождите, идет перемещение %d из %s'%\
                                                ( count+1,
                                                  formatNum(listLength, (u'строки', u'строк', u'строк')),
                                                ),
                                               5000)
                    recordComplain = db.getRecord(tableComplain, '*', id)
                    complainId = forceRef(recordComplain.value('id'))
                    recordComplain.setValue('group_id', toVariant(currentGroup))
                    newItemId = db.updateRecord(tableComplain, recordComplain)
                    self.updateGroupIdDescendants(complainId, newItemId)
                    db.commit()
                    count += 1
                except:
                    db.rollback()
                    QtGui.qApp.logCurrentException()
                    raise
            self.cutList = []
            self.renewListAndSetTo(newItemId)
            self.statusBar.showMessage(agreeNumberAndWord(count,
                                                          (u'Перемещена %s',
                                                           u'Перемещенo %s',
                                                           u'Перемещенo %s',
                                                          )
                                                         ) % formatNum(count, self.unitNameTuple),
                                       5000)


    def popupMenuAboutToShow(self):
        currentItemId = self.currentItemId()
        self.actDelete.setEnabled(bool(currentItemId) and QtGui.qApp.userHasAnyRight([urAccessRefMedComplainDelete]))
        self.actDuplicate.setEnabled(bool(currentItemId))
        self.actCopy.setEnabled(bool(currentItemId))
        self.actCut.setEnabled(bool(currentItemId))
        self.actPaste.setEnabled(bool(self.copyList or self.cutList))


    def insertGroupIdDescendants(self, id, firstGroupId):
        db = QtGui.qApp.db
        db.checkdb()
        table = db.forceTable('rbComplain')
        group = table['group_id']
        result = set([id])
        parents = [id]
        groupIdList = {id:firstGroupId}
        while parents:
            children = set(db.getIdList(table, where=group.inlist(parents)))
            records = db.getRecordList(table, '*', [table['group_id'].inlist(parents), table['deleted'].eq(0)])
            for record in records:
                complainId = forceRef(record.value('id'))
                groupId = forceRef(record.value('group_id'))
                updateGroupId = groupIdList.get(groupId, firstGroupId)
                record.setNull('id')
                record.setValue('group_id', toVariant(updateGroupId))
                newId = db.insertRecord(table.name(), record)
                groupIdList[complainId] = newId
            newChildren = children-result
            result |= newChildren
            parents = newChildren
        return list(result)


    def updateGroupIdDescendants(self, id, firstGroupId):
        db = QtGui.qApp.db
        db.checkdb()
        table = db.forceTable('rbComplain')
        group = table['group_id']
        result = set([id])
        parents = [id]
        groupIdList = {id:firstGroupId}
        while parents:
            children = set(db.getIdList(table, where=group.inlist(parents)))
            records = db.getRecordList(table, '*', [table['group_id'].inlist(parents), table['deleted'].eq(0)])
            for record in records:
                complainId = forceRef(record.value('id'))
                groupId = forceRef(record.value('group_id'))
                updateGroupId = groupIdList.get(groupId, firstGroupId)
                record.setValue('group_id', toVariant(updateGroupId))
                newId = db.updateRecord(table.name(), record)
                groupIdList[complainId] = newId
            newChildren = children-result
            result |= newChildren
            parents = newChildren
        return list(result)


#
# ##########################################################################
#

class CComplainEditor(CItemEditorBaseDialog, Ui_ComplainEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbComplain')
        self.setupUi(self)
        self.setWindowTitleEx(u'Жалоба')
        self.cmbGroup.setTable('rbComplain')
        self.setupDirtyCather()


    def setGroupId(self, id):
        self.cmbGroup.setValue(id)
        self.setIsDirty(False)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,           record, 'code')
        setLineEditValue(   self.edtName,           record, 'name')
        setRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,           record, 'code')
        getLineEditValue(   self.edtName,           record, 'name')
        getRBComboBoxValue( self.cmbGroup,          record, 'group_id')
        return record


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
#        result = result and (self.checkRecursion(self.cmbGroup.value()) or self.checkValueMessage(u'попытка создания циклической группировки', False, self.cmbGroup))
#        result = result and (self.cmbPurpose.value() or self.checkInputMessage(u'назначение', False, self.cmbPurpose))
        return result
