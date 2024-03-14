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
from PyQt4.QtCore import SIGNAL

from library.interchange        import getLineEditValue, setLineEditValue, setTextEditValue, getTextEditValue


from library.ItemsListDialog    import CItemsListDialog, CItemEditorDialog
from library.TableModel         import CTextCol

from RefBooks.Tables            import rbActivity, rbCode, rbName


from .Ui_RBActivityEditor import Ui_ItemEditorDialog


class CRBActivityList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 8),
            CTextCol(u'Региональный код', ['regionalCode'], 8),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbActivity, [rbCode, rbName])
        self.setWindowTitleEx(u'Виды(типы) деятельности врача')
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.actSelectAllRow = QtGui.QAction(u'Выделить все строки', self)
        self.tblItems.addPopupAction(self.actSelectAllRow)
        self.connect(self.actSelectAllRow, SIGNAL('triggered()'), self.selectAllRowTblItem)
        self.actClearSelectionRow = QtGui.QAction(u'Снять выделение', self)
        self.tblItems.addPopupAction(self.actClearSelectionRow)
        self.connect(self.actClearSelectionRow, SIGNAL('triggered()'), self.clearSelectionRow)
        self.actDelete = QtGui.QAction(u'Удалить', self)
        self.tblItems.addPopupAction(self.actDelete)
        self.connect(self.actDelete, SIGNAL('triggered()'), self.deleteSelected)


    def getItemEditor(self):
        return CRBActivityEditor(self)


    def selectAllRowTblItem(self):
        self.tblItems.selectAll()


    def clearSelectionRow(self):
        self.tblItems.clearSelection()


    def deleteSelected(self):
        db = QtGui.qApp.db
        selectedIdList = self.tblItems.selectedItemIdList()
        if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить выделенные строки?(количество строк: %d)'% len(selectedIdList),
                                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No
                                    ) == QtGui.QMessageBox.Yes:
            for id in selectedIdList:
                tableActivity = db.table('rbActivity')
                tablePersonActivity = db.table('Person_Activity')
                db.deleteRecord(tableActivity, tableActivity['id'].eq(id))
                db.deleteRecord(tablePersonActivity, tablePersonActivity['activity_id'].eq(id))
                self.renewListAndSetTo(None)

#
# ##########################################################################
#

class CRBActivityEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, rbActivity)
        self.setWindowTitleEx(u'Вид(тип) деятельности врача')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setTextEditValue(self.edtNote,         record, 'note')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getTextEditValue(self.edtNote,         record, 'note')
        return record
