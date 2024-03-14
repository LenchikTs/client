# -*- coding: utf-8 -*-
#############################################################################cmbActivenessFilter
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
from PyQt4.QtCore import Qt, QDateTime, pyqtSignature, SIGNAL, QObject

from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog, CItemEditorDialog, CItemsListDialogEx
from library.TableModel      import CTextCol, CTableModel
from library.RBCheckTable    import CRBCheckTableModel
from library.Utils           import toVariant, forceString, forceRef, forceBool, forceStringEx
from library.DialogBase      import CDialogBase
from Reports.ReportBase      import CReportBase, createTable
from Reports.ReportView      import CReportViewDialog

from Users.Ui_UserRightListDialog import Ui_UserRightListDialog
from Users.Ui_RightsEdit import Ui_UserRightsEditDialog
from Users.Ui_UserRightsFilterDialog import Ui_UserRightsFilterDialog


class CUserRightListDialog(CItemsListDialog, Ui_UserRightListDialog):
    u'''Диалог со списоком всех возможных прав, которыми может обладать
        пользователь. Позволяет добавлять, изменять права (код и имя)'''
    setupUi       = Ui_UserRightListDialog.setupUi
    retranslateUi = Ui_UserRightListDialog.retranslateUi
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',       ['code'], 10),
            CTextCol(u'Название',  ['name'], 50)],
            'rbUserRight', ['name'])
        self.setWindowTitle(u'Список привилегий пользователей системы')


    def setup(self, cols, tableName, order, forSelect=False, filterClass=None):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.props = {}
        self.order = order
        self.addModels('', CTableModel(self, cols))
        self.addModels('UserRightListSort', CUserRightListSortModel(self, self.model))
        self.model = self.modelUserRightListSort.sourceModel()
        self.model.idFieldName = self.idFieldName
        self.model.setTable(tableName)
        self.setModels(self.tblItems, self.modelUserRightListSort, self.selectionModelUserRightListSort)
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
        QObject.connect(
            self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)


    def getItemEditor(self):
        editor = CItemEditorDialog(self, 'rbUserRight')
        editor.setWindowTitle(u'Привилегия пользователя')
        return editor


    @pyqtSignature('QString')
    def on_edtCodeFilter_textChanged(self, text):
        self.modelUserRightListSort.setCodeFilter(unicode(text))


    @pyqtSignature('QString')
    def on_edtNameFilter_textChanged(self, text):
        self.modelUserRightListSort.setNameFilter(unicode(text))


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        currRow = self.tblItems.currentRow()
        if currRow is not None or currRow >= 0:
            sortIndex = self.modelUserRightListSort.index(currRow, 0)
            if sortIndex.isValid():
                sortRow = self.modelUserRightListSort.mapToSource(sortIndex).row()
                if sortRow is not None or sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
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
        else:
            self.on_btnNew_clicked()


class CUserRightListSortModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent, sourceModel):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__codeFilter = ''
        self.__nameFilter = ''
        self.setSourceModel(sourceModel)


    def model(self):
        return  self.sourceModel()


    def __invalidateFilter(self):
        self.reset()


    def setCodeFilter(self, value):
        value = value.upper()
        if self.__codeFilter != value:
            self.__codeFilter = value
            self.__invalidateFilter()


    def setNameFilter(self, value):
        value = value.upper()
        if self.__nameFilter != value:
            self.__nameFilter = value
            self.__invalidateFilter()


    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceModel = self.sourceModel()
        if self.__codeFilter:
            sourceModel.getRecordByRow(sourceRow)
            code = forceString(sourceModel.getRecordByRow(sourceRow).value('code')).upper()
            if self.__codeFilter not in code:
                return False
        if self.__nameFilter:
            name = forceString(sourceModel.getRecordByRow(sourceRow).value('name')).upper()
            if self.__nameFilter not in name:
                return False
        return True


    def __getItemId(self, row):
        index = self.index(row, 0)
        sourceRow = self.mapToSource(index).row()
        return forceRef(self.sourceModel().getRecordByRow(sourceRow).value('id'))


class CUserRightProfileListDialog(CItemsListDialogEx):
    u'''Диалог со списоком всех возможных профилей прав, которые можно
        присваивать пользователям. Позволяет добавлять, изменять профили.'''

    def __init__(self, parent):
        CItemsListDialogEx.__init__(self, parent, [
            CTextCol(u'Название профиля',  ['name'], 10)],
            'rbUserProfile', order='name', filterClass=CUserRightProfileListFilterDialog)
        self.setWindowTitle(u'Список профилей прав пользователей системы')
        self.btnFilter.setText(u'Фильтр по праву')


    def getItemEditor(self):
        return CUserProfileEditDialog(self)


    def select(self, props={}):
        db = QtGui.qApp.db
        checkedIdList = props.get('checkedIdList')

        tableUserProfile = db.table('rbUserProfile')
        cond = [ tableUserProfile['deleted'].eq(0) ]

        if checkedIdList:
            tableUserRight = db.table('rbUserRight')
            tableUserProfileRight = db.table('rbUserProfile_Right')

            cols = [ tableUserProfile['id'],
                     'COUNT(%s) AS `cnt`' % tableUserProfile['id']
                   ]
            order = db.prepareOrder('rbUserProfile.' + self.order)
            cond.append(tableUserRight['id'].inlist(checkedIdList))

            queryTable = tableUserProfile
            queryTable = queryTable.leftJoin(tableUserProfileRight, tableUserProfileRight['master_id'].eq(tableUserProfile['id']))
            queryTable = queryTable.leftJoin(tableUserRight, tableUserProfileRight['userRight_id'].eq(tableUserRight['id']))
            stmt = db.selectStmtGroupBy(queryTable, cols, cond, group='1')
            query = db.query(stmt + " HAVING `cnt` = %d " % len(checkedIdList) + order)

            idList = []
            while query.next():
                idList.append(forceRef(query.value(0)))
            return idList
        else:
            return db.getIdList(tableUserProfile, 'id', cond, self.order)


    def copyInternals(self, newItemId, oldItemId):
        db = QtGui.qApp.db
        tableUserProfileRight = db.table('rbUserProfile_Right')
        records = db.getRecordList(tableUserProfileRight, '*', [tableUserProfileRight['master_id'].eq(oldItemId)])
        for record in records:
            record.setNull('id')
            record.setValue('master_id', toVariant(newItemId))
            db.insertRecord(tableUserProfileRight, record)


    def delSelectedRows(self):
        db = QtGui.qApp.db
        for row in self.tblItems.selectedRowList():
            record = self.model.getRecordByRow(row)
            isProfileUses = db.getCount('Person', '*', 'userProfile_id = %d' % forceRef(record.value('id'))) > 0
            if isProfileUses:
                QtGui.QMessageBox.critical(self, u'Внимание', u'Профиль прав используется, поэтому он не может быть удален')
                return
        CItemsListDialogEx.delSelectedRows(self)


class CUserRightProfileListFilterDialog(CDialogBase, Ui_UserRightsFilterDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Фильтр списка профилей прав пользователей')
        self.addObject('modelProfiles', CRBCheckTableModel(self, 'rbUserRight', u'Наименование'))
        self.addModels('Rights', CRightsModel(self, self.modelProfiles))
        self.setModels(self.tblRights, self.modelRights, self.selectionModelRights)


    def setProps(self, props):
        self.modelProfiles.setCheckedIdList(props.get('checkedIdList', []))


    def props(self):
        return {'checkedIdList': self.modelProfiles.getCheckedIdList()}


    @pyqtSignature('int')
    def on_cmbActivenessFilter_currentIndexChanged(self, index):
        self.modelRights.setActivenessFilter(index)


    @pyqtSignature('QString')
    def on_edtCodeFilter_textChanged(self, text):
        self.modelRights.setCodeFilter(unicode(text))


    @pyqtSignature('QString')
    def on_edtNameFilter_textChanged(self, text):
        self.modelRights.setNameFilter(unicode(text))




class CUserProfileEditDialog(CItemEditorBaseDialog, Ui_UserRightsEditDialog):
    u'''Диалог для редактирования профиля - позволяет изменить имя профиля,
        а так же добавить в него различные права'''
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent,  'rbUserProfile')
        self.addObject('modelProfiles', CRBCheckTableModel(self, 'rbUserRight', u'Наименование'))
        self.addModels('Rights', CRightsModel(self, self.modelProfiles))
        self.addObject('btnPrint', QtGui.QPushButton(u'Печать', self))
        self.setupUi(self)
        self.buttonBox.addButton(self.btnPrint,  QtGui.QDialogButtonBox.ActionRole)
        self.setModels(self.tblRights, self.modelRights, self.selectionModelRights)
        self.modelProfiles.updateList()
        self.setupDirtyCather()


    def destoy(self):
        self.tblRights.setModel(None)
        del self.modelRights
        del self.modelProfiles


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.edtName.setText(forceString(record.value('name')))
#        self.modelRights.setActivenessFilter(self.cmbActivenessFilter.currentIndex())
        self.modelRights.loadItems(self.itemId())
        self.setIsDirty(False)


    def checkDataEntered(self):
        result = True
        name = forceStringEx(self.edtName.text())
        result = result and (name or self.checkInputMessage(u'наименование', False, self.edtName))
        return result


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        name   = forceStringEx(self.edtName.text())
        record.setValue('name', toVariant(name))
        return record


    def saveInternals(self, id):
        self.modelRights.saveItems(id)


    def dumpParams(self, cursor):
        description = []
        description.append(u'Название ' + self.edtName.text())
        description.append(u'Права ' + [u'Все', u'Выбранные', u'Не выбранные'][self.cmbActivenessFilter.currentIndex()])
        codeFilter = forceString(self.edtCodeFilter.text())
        if codeFilter:
            description.append(u'С фильтром по коду ' + codeFilter)
        nameFilter = forceString(self.edtNameFilter.text())
        if nameFilter:
            description.append(u'С фильтром по названию ' + nameFilter)
        description.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def printRights(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Права')
        cursor.insertBlock()
        self.dumpParams(cursor)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('5%',[u'№'], CReportBase.AlignRight),
                ('10%', [u'Включено'], CReportBase.AlignLeft),
                ('35%', [u'Код'], CReportBase.AlignLeft),
                ('50%', [u'Наименование'], CReportBase.AlignLeft)
               ]
        table = createTable(cursor, cols)
        modelRights = self.modelRights
        for row in xrange(modelRights.rowCount()):
            check = forceBool(modelRights.data(self.modelRights.index(row, 0), Qt.CheckStateRole))
            code  = forceString(modelRights.data(self.modelRights.index(row, 0)))
            name  = forceString(modelRights.data(self.modelRights.index(row, 1)))
            i = table.addRow()
            table.setText(i, 0, row+1)
            table.setText(i, 1, u'да' if check else u'нет')
            table.setText(i, 2, code)
            table.setText(i, 3, name)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportBody)
        reportView = CReportViewDialog(self)
        reportView.setWindowTitle(u'Профиль прав')
        reportView.setOrientation(QtGui.QPrinter.Landscape)
        reportView.setText(doc)
        reportView.exec_()


    @pyqtSignature('int')
    def on_cmbActivenessFilter_currentIndexChanged(self, index):
        self.modelRights.setActivenessFilter(index)


    @pyqtSignature('QString')
    def on_edtCodeFilter_textChanged(self, text):
#        text = unicode(self.edtCodeFilter.text())
        self.modelRights.setCodeFilter(unicode(text))


    @pyqtSignature('QString')
    def on_edtNameFilter_textChanged(self, text):
#        nameFind = forceString(self.edtNameFilter.text())
        self.modelRights.setNameFilter(unicode(text))


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        self.printRights()


class CRightsModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent, sourceModel):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__activenessFilter = 0
        self.__codeFilter = ''
        self.__nameFilter = ''
        self.setSourceModel(sourceModel)


    def loadItems(self, masterId):
        db = QtGui.qApp.db
        table = db.table('rbUserProfile_Right')
        rightIdList = db.getIdList(table, 'userRight_id', table['master_id'].eq(masterId))
        self.sourceModel().setCheckedIdList(rightIdList)


    def saveItems(self, masterId):
        db = QtGui.qApp.db
        table = db.table('rbUserProfile_Right')
        masterCond = table['master_id'].eq(masterId)
        presentRightIdSet = set(db.getIdList(table, 'userRight_id', masterCond))
        newRightIdSet = self.sourceModel().getCheckedIdSet()
        addRightIdSet = newRightIdSet - presentRightIdSet
        delRightIdSet = presentRightIdSet - newRightIdSet
        db.deleteRecord(table, db.joinAnd([masterCond,
                                           table['userRight_id'].inlist(delRightIdSet)
                                          ]
                                         )
                       )
        record = table.newRecord()
        record.setValue('master_id', masterId)
        for rightId in addRightIdSet:
            record.setNull('id')
            record.setValue('userRight_id', rightId)
            db.insertRecord(table, record)


    def __invalidateFilter(self):
        self.reset()


    def setActivenessFilter(self, value):
        if self.__activenessFilter != value:
            self.__activenessFilter = value
            self.__invalidateFilter()


    def setCodeFilter(self, value):
        value = value.upper()
        if self.__codeFilter != value:
            self.__codeFilter = value
            self.__invalidateFilter()


    def setNameFilter(self, value):
        value = value.upper()
        if self.__nameFilter != value:
            self.__nameFilter = value
            self.__invalidateFilter()


    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceModel = self.sourceModel()
        if self.__activenessFilter == 1: # только вкл.
            itemId = forceRef(sourceModel.value(sourceRow, 'id'))
            if itemId not in sourceModel.getCheckedIdSet():
                return False
        elif self.__activenessFilter == 2: # только выкл.
            itemId = forceRef(sourceModel.value(sourceRow, 'id'))
            if itemId in sourceModel.getCheckedIdSet():
                return False
        if self.__codeFilter:
            code = forceString(sourceModel.value(sourceRow, 'code')).upper()
            if self.__codeFilter not in code:
                return False
        if self.__nameFilter:
            name = forceString(sourceModel.value(sourceRow, 'name')).upper()
            if self.__nameFilter not in name:
                return False
        return True


    def __getItemId(self, row):
        index = self.index(row, 0)
        sourceRow = self.mapToSource(index).row()
        return forceRef(self.sourceModel().value(sourceRow, 'id'))


    def getCheckedIdList(self):
        result = []
        sourceModel = self.sourceModel()
        checkedIdSet = sourceModel.getCheckedIdSet()
        for row in xrange(self.rowCount()):
            itemId = self.__getItemId(row)
            if itemId in checkedIdSet:
                result.append(itemId)
        return result


    def checkAll(self):
        sourceModel = self.sourceModel()
        checkedIdSet = sourceModel.getCheckedIdSet()
        for row in xrange(self.rowCount()):
            checkedIdSet.add(self.__getItemId(row))
        sourceModel.setCheckedIdList(checkedIdSet)


    def uncheckAll(self):
        sourceModel = self.sourceModel()
        checkedIdSet = sourceModel.getCheckedIdSet()
        for row in xrange(self.rowCount()):
            checkedIdSet.discard(self.__getItemId(row))
        sourceModel.setCheckedIdList(checkedIdSet)
