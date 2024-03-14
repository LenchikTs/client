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

from library.interchange     import setCheckBoxValue, getCheckBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CBoolCol, CTextCol

from RefBooks.Tables         import rbPolicyType, rbCode, rbName
from .Ui_RBPolicyTypeEditor import Ui_RBPolicyTypeEditorDialog


class CRBPolicyTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CBoolCol(u'ОМС',          ['isCompulsory'], 10),
            ], rbPolicyType, [rbCode, rbName])
        self.setWindowTitleEx(u'Типы полиса')

    def getItemEditor(self):
        return CRBPolicyTypeEditor(self)


class CRBPolicyTypeEditor(Ui_RBPolicyTypeEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, rbPolicyType)
        self.setWindowTitleEx(u'Тип полиса')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setCheckBoxValue(self.chkIsCompulsory, record, 'isCompulsory')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getCheckBoxValue(self.chkIsCompulsory, record, 'isCompulsory')
        return record
