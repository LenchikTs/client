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

from PyQt4.QtCore               import pyqtSignature
from library.ItemsListDialog    import CItemsListDialog, CItemEditorDialog
from library.TableModel         import CTextCol
from library.Utils              import forceInt, toVariant
from RefBooks.Tables            import rbCode, rbName, rbFinanceSource, rbFinance
from Ui_FinanceSourceItemEditor import Ui_FinanceSourceItemEditor


class CRBFinanceSourceList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbFinanceSource, [rbCode, rbName])
        self.setWindowTitleEx(u'Источники финансирования')


    def getItemEditor(self):
        return CRBFinanceSourceEditor(self)



class CRBFinanceSourceEditor(Ui_FinanceSourceItemEditor, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, rbFinanceSource)
        self.cmbFinance.setTable(rbFinance, addNone=False)
        self.setWindowTitleEx(u'Источник финансирования')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        self.cmbFinance.setValue(forceInt(record.value('master_id')))


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        record.setValue('master_id', toVariant(self.cmbFinance.value()))
        return record


    def checkDataEntered(self):
        return bool(self.cmbFinance.value())


    @pyqtSignature('int')
    def on_cmbFinance_currentIndexChanged(self, index):
        self.setIsDirty()
