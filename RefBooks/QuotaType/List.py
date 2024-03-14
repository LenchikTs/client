# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QVariant, pyqtSignature, SIGNAL

from library.HierarchicalItemsListDialog import CHierarchicalItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemEditorBaseDialog
from library.interchange                 import getComboBoxValue, getLineEditValue, setComboBoxValue, setLineEditValue, setTextEditValue
from library.TableModel                  import CTableModel, CCol, CEnumCol, CRefBookCol, CTextCol, CDateCol
from library.TreeModel                   import CDBTreeItemWithClass, CDragDropDBTreeModelWithClassItems
from library.Utils                       import forceInt, forceRef, forceString, forceStringEx, formatRecordsCount, toVariant, forceDate

from .Ui_QuotaTypeEditor import Ui_QuotaTypeEditorDialog


class CQuotaTypeList(CHierarchicalItemsListDialog):
    def __init__(self, parent):
        CHierarchicalItemsListDialog.__init__(self, parent, [
            CEnumCol(u'Класс', ['class'], getQuotaTypeClassNameList(), 10),
            CQuotaTypeRefBookCol(u'Вид',   ['group_code'], 'QuotaType', 10),
            CTextCol(   u'Код',          ['code'], 20),
            CTextCol(   u'Региональный код',          ['regionalCode'], 20),
            CTextCol(   u'Наименование', ['name'], 40),
            CDateCol(   u'Действует с',          ['begDate'], 20),
            CDateCol(   u'Действует по',          ['endDate'], 20)
            ], 'QuotaType', ['class', 'group_code', 'code',  'regionalCode', 'name', 'id', 'begDate', 'endDate'])
        self.setWindowTitleEx(u'Виды квот')
        self.expandedItemsState = {}
        self.setSettingsTblItems()
        self.additionalPostSetupUi()


    def setSettingsTblItems(self):
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


    def preSetupUi(self):
        self.addModels('Tree', CQuotaTypeTreeModel(self, self.tableName, 'id', 'group_code', 'name', 'class', self.order))
        self.addModels('Table',CTableModel(self, self.cols, self.tableName))
        self.modelTree.setLeavesVisible(True)
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))


    def additionalPostSetupUi(self):
        self.treeItems.expand(self.modelTree.index(0, 0))
        #drag-n-drop support
        self.treeItems.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.connect(self.modelTree, SIGNAL('saveExpandedState()'),  self.saveExpandedState)
        self.connect(self.modelTree, SIGNAL('restoreExpandedState()'),  self.restoreExpandedState)


    def select(self, props=None):
        db = QtGui.qApp.db
        cond = []
        table = self.modelTable.table()
        groupId = self.currentGroupId()
        groupCond = db.translate(table, 'id', groupId, 'code')
        className = self.currentClass()
        cond = [ table['group_code'].eq(groupCond) ]
        cond.append(table['deleted'].eq(0))
        cond.append(table['class'].eq(className))
        list = QtGui.qApp.db.getIdList(table.name(),
                           'id',
                           cond,
                           self.order)
        self.lblCountRows.setText(formatRecordsCount(len(list)))
        return list


    def currentClass(self):
        return self.modelTree.itemClass(self.treeItems.currentIndex())


    def currentItem(self):
        return self.treeItems.currentIndex().internalPointer()


    def getItemEditor(self):
        return CQuotaTypeEditor(self)

    @pyqtSignature('')
    def on_btnNew_clicked(self):
        dialog = self.getItemEditor()
        try:
            dialog.setClass(self.currentClass())
            dialog.setGroupId(self.currentGroupId())
            dialog.setIsNew(True)
            dialog.setInputCodeSettings()
            if dialog.exec_():
                itemId = dialog.itemId()
                self.modelTree.update()
                self.renewListAndSetTo(itemId)
        finally:
            dialog.deleteLater()

# ###########################################################################


class CQuotaTypeRefBookCol(CRefBookCol):
    def format(self, values):
        parentCode = forceString(values[0])
        if parentCode:
            return QtGui.qApp.db.translate('QuotaType', 'code', parentCode, 'name')
        else:
            return CCol.invalid


class CQuotaTypeEditor(Ui_QuotaTypeEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'QuotaType')
        # self.setupUi(self)
        self._applyQuotaTypeClassComboBox()
        self.setWindowTitleEx(u'Вид квоты')
        self.isNew   = False
        self.oldCode = None
        self.cmbGroup.setTable('QuotaType')
        self.setupDirtyCather()


    def _applyQuotaTypeClassComboBox(self):
        self.cmbClass.blockSignals(True)
        for className, value in quotaTypeClassItems:
            self.cmbClass.addItem(className)
        self.cmbClass.blockSignals(False)


    def setIsNew(self, val):
        self.isNew = val

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setTextEditValue(   self.edtName,           record, 'name')
        setComboBoxValue(   self.cmbClass,          record, 'class')
        self.cmbGroup.setCode(forceString(record.value('group_code')))
        self.setInputCodeSettings()
        setLineEditValue(   self.edtCode,           record, 'code')
        setLineEditValue(   self.edtRegionalCode,           record, 'regionalCode')
        self.edtBegDate.setDate(forceDate(record.value('begDate')))
        self.edtEndDate.setDate(forceDate(record.value('endDate')))
        self.oldCode = self.edtCode.text()
        self.modelIdentification.loadItems(self.itemId())
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,           record, 'code')
        getLineEditValue(   self.edtRegionalCode,           record, 'regionalCode')
        record.setValue('begDate', toVariant(self.edtBegDate.date()))
        record.setValue('endDate', toVariant(self.edtEndDate.date()))
        record.setValue('name', QVariant(self.edtName.toPlainText().replace('\n', ' ')))
        group_code = self.cmbGroup.code()
        if group_code != '0':
            record.setValue('group_code', QVariant(group_code))
        else:
            record.setValue('group_code', QVariant())
        getComboBoxValue(   self.cmbClass,          record, 'class')
        return record

    def setInputCodeSettings(self):
        parentCode = self.cmbGroup.code()
        if parentCode:
            if parentCode != '0':
                inputMask = parentCode+'.'+'9'*(15-len(parentCode))
            else:
                inputMask = '9'*16
        else:
            inputMask = ''
        self.edtCode.setInputMask(inputMask)

    def setClass(self, _class):
        self.cmbClass.setCurrentIndex(_class)

    def setGroupId(self, groupId):
        self.cmbGroup.setValue(groupId)


    def checkDataEntered(self):
        result = True
        code    = forceStringEx(self.edtCode.text())
        name    = forceStringEx(self.edtName.toPlainText())
        result = result and (code or self.checkInputMessage(u'код', False, self.edtCode))
        result = result and (name or self.checkInputMessage(u'наименование', False, self.edtName))
        if self.isNew or code != self.oldCode:
            result = result and self.checkUniqueCode(code)
        return result

    def checkUniqueCode(self, code):
        db = QtGui.qApp.db
        parentCode = self.cmbGroup.code()
        if parentCode == '0':
            stmt = db.selectStmt(self._tableName, 'code', 'group_code IS NULL')
        else:
            stmt = db.selectStmt(self._tableName, 'code', 'group_code=%s'%parentCode)
        query = db.query(stmt)
        result = []
        while query.next():
            result.append(query.value(0).toString())
        if code in result:
            QtGui.QMessageBox().warning(self,
                                        u'Внимание!',
                                        u'Данный код уже существует',
                                        QtGui.QMessageBox.Ok,
                                        QtGui.QMessageBox.Ok)
            return False
        return True

    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, classCode):
        fiter = 'class=%d and deleted = 0' % classCode
        self.cmbGroup.setFilter(fiter)
#        self.cmbPrescribedType.setFilter(fiter)

# ############################

quotaTypeClassItems =  (
                        (u'ВТМП', 0),
                        (u'СМП', 1),
                        (u'Родовой сертификат', 2),
                        (u'Платные', 3),
                        (u'ОМС', 4),
                        (u'СКЛ', 5)
                       )
quotaTypeClassItemsByExists = None

def getQuotaTypeClassItemsByExists():
    global quotaTypeClassItemsByExists
    if quotaTypeClassItemsByExists is None:
        quotaTypeClassItemsByExists = []
        db = QtGui.qApp.db
        table = db.table('QuotaType')
        for name, _class in quotaTypeClassItems:
            if bool(db.getCount(table, table['id'].name(), table['class'].eq(_class))):
                quotaTypeClassItemsByExists.append((name, _class))
        quotaTypeClassItemsByExists = tuple(quotaTypeClassItemsByExists)
    return quotaTypeClassItemsByExists


def getQuotaTypeClassNameList():
    return [name for name, _class in quotaTypeClassItems]


class CQuotaTypeTreeModel(CDragDropDBTreeModelWithClassItems):
    def __init__(self, parent, tableName, idColName, groupColName, nameColName, classColName, order=None):
        CDragDropDBTreeModelWithClassItems.__init__(self, parent, tableName, idColName, groupColName, nameColName, classColName, order)
        self.setClassItems(quotaTypeClassItems)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(u'Вид квоты')
        return QVariant()

    def loadChildrenItems(self, group):
        result = []
        if group == self.getRootItem():
            result = self.classItems
        else:
            db = QtGui.qApp.db
            table = db.table(self.tableName)
            groupCond = db.translate(table, 'id', group._id, 'code')
            cond = [ table[self.groupColName].eq(groupCond) ]
            cond.append(table[self.classColName].eq(group.className))
            if table.hasField('deleted'):
                cond.append(table['deleted'].eq(0))
            if not self.leavesVisible:
                alias = table.alias(self.tableName+'2')
                cond.append(db.existsStmt(alias, alias[self.groupColName].eq(table['code'])))
            for record in db.getRecordList(table, [self.idColName, self.nameColName], cond, self.order):
                id   = forceRef(record.value(0))
                name = forceString(record.value(1))
                result.append(CDBTreeItemWithClass(group, name, id, group.className, self))
        return result


    def dropMimeData(self, data, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        if not data.hasText():
            return False

        dragId = forceRef(forceInt(data.text()))
        parentId = self.itemId(parentIndex)
        parentClass = self.itemClass(parentIndex)

        self.changeParent(dragId, parentId, parentClass)
        self.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), parentIndex, parentIndex)
        return True


    def changeParent(self, id, parentId, parentClass):
        # if parentId not in self.getItemIdList(self.findItemId(id)):
            db = QtGui.qApp.db
            table = db.table(self.tableName)
            parentCode  = forceString(db.translate(table, 'id', parentId, 'code'))
            oldCode     = forceString(db.translate(table, 'id', id, 'code'))
            newCode = self.getNewCode(oldCode, parentCode)
            record = db.getRecord(table, [self.idColName, self.groupColName, self.classColName, 'code'], id)
            if record:
                self.emit(SIGNAL('saveExpandedState()'))
                childIdList = db.getIdList(table, 'id', table['group_code'].eq(oldCode))
                variantParentCode =  toVariant(parentCode) if parentCode else QVariant()
                record.setValue(self.groupColName, variantParentCode)
                record.setValue(self.classColName, toVariant(parentClass))
                record.setValue('code', toVariant(newCode))
                db.updateRecord(table, record)
                for childId in childIdList:
                    self.changeChildren(childId, id, parentClass)
                self.reset()
                self.update()
                self.emit(SIGNAL('restoreExpandedState()'))


    def changeChildren(self, id,  parentId, parentClass):
        db = QtGui.qApp.db
        table = db.table(self.tableName)
        parentCode  = forceString(db.translate(table, 'id', parentId, 'code'))
        oldCode     = forceString(db.translate(table, 'id', id, 'code'))
        newCode = self.getNewCode(oldCode, parentCode)
        record = db.getRecord(table, [self.idColName, self.groupColName, self.classColName, 'code'], id)
        if record:
            variantParentCode =  toVariant(parentCode) if parentCode else QVariant()
            record.setValue(self.groupColName, variantParentCode)
            record.setValue(self.classColName, toVariant(parentClass))
            record.setValue('code', toVariant(newCode))
            db.updateRecord(table, record)
            self.reset()
            self.update()
            childIdList = db.getIdList(table, 'id', table['group_code'].eq(oldCode))
            for childId in childIdList:
                self.changeChildren(childId, id, parentClass)

    def getNewCode(self, oldCode, parentCode):
        db = QtGui.qApp.db
        table = db.table(self.tableName)
        codeList = db.getRecordList(table, 'code', table['group_code'].eq(parentCode))
        oldCodeParts = oldCode.split('.')
        lastPartOldCode = oldCodeParts[len(oldCodeParts)-1]
        max = 0
        exists = False
        for code in codeList:
            codeParts = forceString(code.value('code')).split('.')
            lastCodePart = codeParts[len(codeParts)-1]
            if lastPartOldCode == lastCodePart:
                exists = True
            if max < int(lastCodePart):
                max = int(lastCodePart)
        if exists:
            newCode = parentCode+'.'+str(max+1) if parentCode else str(max+1)
        else:
            newCode = parentCode+'.'+lastPartOldCode if parentCode else lastPartOldCode
        return newCode

# #########################################################
