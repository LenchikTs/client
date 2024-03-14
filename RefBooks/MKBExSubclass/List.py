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


from PyQt4 import QtCore, QtGui

from library.DialogBase      import CDialogBase
from library.ItemsListDialog import CItemEditorDialog, CItemEditorBaseDialog
from library.TableModel      import CTableModel, CTextCol, CIntCol
from library.Utils           import toVariant
from library.interchange     import getLineEditValue, getSpinBoxValue, setLineEditValue, setSpinBoxValue
from RefBooks.Tables         import rbCode, rbName

from .Ui_MKBExSubclassDialog import Ui_MKBExSubclassDialog
from .Ui_MKBExSubclassEditor import Ui_MKBExSubclassEditor


class CMKBExSubclass(CDialogBase, Ui_MKBExSubclassDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.order = ['id']
        colsExSubclass = [
            CTextCol(u'Код',     ['code'], 5),
            CIntCol( u'Позиция', ['position'], 5),
            CTextCol(u'Название субклассификации', ['name'], 30),
            ]
        self.modelExSubclass = CTableModel(self, colsExSubclass, 'rbMKBExSubclass')
        colsExSubclass_Item = [
            CTextCol(u'Код',      ['code'], 5),
            CTextCol(u'Название', ['name'], 30),
            ]
        self.modelExSubclass_Item = CTableModel(self, colsExSubclass_Item, 'rbMKBExSubclass_Item')
        self.btnAdd.setShortcut('F9')
        self.btnEdit.setShortcut('F4')
        self.btnAdd_Item.setShortcut('F9')
        self.btnEdit_Item.setShortcut('F4')
        self.select()


    def select(self):
        table = self.modelExSubclass.table()
        idList = QtGui.qApp.db.getIdList(table.name(), 'id', '', self.order)
        self.modelExSubclass.setIdList(idList)
        self.tblExSubclass.setModel(self.modelExSubclass)


    def select_Item(self):
        id=self.tblExSubclass.currentItemId()
        cond='master_id=%s' % (str(id) if id else 'null')
        idList=QtGui.qApp.db.getIdList('rbMKBExSubclass_Item', 'id', cond, 'id')
        self.modelExSubclass_Item.setIdList(idList)
        self.tblExSubclass_Item.setModel(self.modelExSubclass_Item)


    def editSubclass(self, itemId):
        dialog = CMKBExSubclassEditor(self)
        try:
            if itemId:
                dialog.load(itemId)
            dialog.exec_()
        finally:
            dialog.deleteLater()


    def editSubclass_Item(self, master_id, itemId):
        dialog = CMKBExSubclassItemEditor(self, master_id)
        try:
            if itemId:
                dialog.load(itemId)
            dialog.exec_()
        finally:
            dialog.deleteLater()


    @QtCore.pyqtSignature('QModelIndex')
    def on_tblExSubclass_doubleClicked(self, index):
        self.on_btnEdit_clicked()


    @QtCore.pyqtSignature('QModelIndex')
    def on_tblExSubclass_Item_doubleClicked(self, index):
        self.on_btnEdit_Item_clicked()


    @QtCore.pyqtSignature('QModelIndex')
    def on_tblExSubclass_activated(self, index):
        self.select_Item()


    @QtCore.pyqtSignature('QModelIndex')
    def on_tblExSubclass_clicked(self, index):
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()


    @QtCore.pyqtSignature('')
    def on_btnAdd_clicked(self):
        self.editSubclass(None)
        self.select()
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnEdit_clicked(self):
        id=self.tblExSubclass.currentItemId()
        self.editSubclass(id)
        self.select()
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnDel_clicked(self):
        self.tblExSubclass.removeCurrentRow()
        self.select()
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnAdd_Item_clicked(self):
        master_id=self.tblExSubclass.currentItemId()
        self.editSubclass_Item(master_id, None)
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnEdit_Item_clicked(self):
        master_id=self.tblExSubclass.currentItemId()
        id=self.tblExSubclass_Item.currentItemId()
        self.editSubclass_Item(master_id, id)
        self.select_Item()


    @QtCore.pyqtSignature('')
    def on_btnDel_Item_clicked(self):
        self.tblExSubclass_Item.removeCurrentRow()
        self.select_Item()

#
# ##########################################################################
#


class CMKBExSubclassItemEditor(CItemEditorDialog):
    def __init__(self, parent, master_id):
        CItemEditorDialog.__init__(self, parent, 'rbMKBExSubclass_Item')
        self.setWindowTitle(u'Элемент расширенной субклассификации МКБ')
        self.master_id=master_id


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        record.setValue('master_id',  toVariant(self.master_id))
        return record


class CMKBExSubclassEditor(CItemEditorBaseDialog, Ui_MKBExSubclassEditor):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbMKBExSubclass')
        self.setupUi(self)
        self.setWindowTitleEx(u'Расширенная субклассификация МКБ')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue( self.edtCode,     record, rbCode)
        setSpinBoxValue(  self.edtPosition, record, u'position')
        setLineEditValue( self.edtName,     record, rbName)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue( self.edtCode,     record, rbCode)
        getSpinBoxValue(  self.edtPosition, record, u'position')
        getLineEditValue( self.edtName,     record, rbName)
        return record


