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
from library.ItemsListDialog import CItemEditorDialog
from library.TableModel      import CTableModel, CTextCol
from library.Utils           import toVariant

from .Ui_MKBSubclassEditor import Ui_MKBSubclassEditorDialog

class CMKBSubclass(CDialogBase, Ui_MKBSubclassEditorDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.order = ['id']
        colsSubclass = [
            CTextCol(u'Код', ['code'], 5),
            CTextCol(u'Субклассификация', ['name'], 30),
            ]
        self.modelSubclass = CTableModel(self, colsSubclass, 'rbMKBSubclass')
        colsSubclass_Item = [
            CTextCol(u'пятый знак', ['code'], 5),
            CTextCol(u'Субклассификация', ['name'], 30),
            ]
        self.modelSubclass_Item = CTableModel(self, colsSubclass_Item, 'rbMKBSubclass_Item')
        self.select()
        self.tblSubclass.selectionModel().currentRowChanged.connect(self.select_Item)

    def select(self):
        table = self.modelSubclass.table()
        idList = QtGui.qApp.db.getIdList(table.name(), 'id', '', self.order)
        self.modelSubclass.setIdList(idList)
        self.tblSubclass.setModel(self.modelSubclass)

    def select_Item(self):
        id=self.tblSubclass.currentItemId()
        cond='master_id=%s' % (str(id) if id else 'null')
        idList=QtGui.qApp.db.getIdList('rbMKBSubclass_Item', 'id', cond, 'id')
        self.modelSubclass_Item.setIdList(idList)
        self.tblSubclass_Item.setModel(self.modelSubclass_Item)

    def editSubclass(self, itemId):
        dialog = CItemEditorDialog(self, 'rbMKBSubclass')
        try:
            if itemId:
                dialog.load(itemId)
            dialog.exec_()
        finally:
            dialog.deleteLater()

    def editSubclass_Item(self, master_id, itemId):
        dialog = CMKBSubclassItemEditorDialog(self, master_id)
        try:
            if itemId:
                dialog.load(itemId)
            dialog.exec_()
        finally:
            dialog.deleteLater()

    @QtCore.pyqtSignature('QModelIndex')
    def on_tblSubclass_activated(self, index):
        self.select_Item()

    @QtCore.pyqtSignature('QModelIndex')
    def on_tblSubclass_clicked(self, index):
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
        id=self.tblSubclass.currentItemId()
        self.editSubclass(id)
        self.select()
        self.select_Item()

    @QtCore.pyqtSignature('')
    def on_btnDel_clicked(self):
        self.select()
        self.select_Item()

    @QtCore.pyqtSignature('')
    def on_btnAdd_Item_clicked(self):
        master_id=self.tblSubclass.currentItemId()
        self.editSubclass_Item(master_id, None)
        self.select_Item()

    @QtCore.pyqtSignature('')
    def on_btnEdit_Item_clicked(self):
        master_id=self.tblSubclass.currentItemId()
        id=self.tblSubclass_Item.currentItemId()
        self.editSubclass_Item(master_id, id)
        self.select_Item()

    @QtCore.pyqtSignature('')
    def on_btnDel_Item_clicked(self):
        self.select_Item()

class CMKBSubclassItemEditorDialog(CItemEditorDialog):
    def __init__(self, parent, master_id):
        CItemEditorDialog.__init__(self, parent, 'rbMKBSubclass_Item')
        self.master_id=master_id

    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        record.setValue('master_id',  toVariant(self.master_id))
        return record
