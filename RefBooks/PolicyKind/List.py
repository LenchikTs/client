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

from library.interchange     import setLineEditValue, getLineEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName
from .Ui_RBPolicyKindEditor  import Ui_ItemEditorDialog


class CRBPolicyKindList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 8),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Региональный код', ['regionalCode'], 8),
            CTextCol(u'Федеральный код',  ['federalCode'],  8),
            ], 'rbPolicyKind', [rbCode, rbName])
        self.setWindowTitleEx(u'Виды полиса')

    def getItemEditor(self):
        return CRBPolicyKindEditor(self)


class CRBPolicyKindEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbPolicyKind')
        self.setWindowTitleEx(u'Вид полиса')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setLineEditValue(self.edtFederalCode,  record, 'federalCode')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getLineEditValue(self.edtFederalCode, record,  'federalCode')
        return record
