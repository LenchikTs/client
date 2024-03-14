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

from library.TableModel import CTextCol
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog

from RefBooks.Tables import rbCashOperation, rbCode, rbName


class CRBCashOperationList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbCashOperation, [rbCode, rbName])
        self.setWindowTitleEx(u'Кассовые операции')

    def getItemEditor(self):
        return CRBCashOperationEditor(self)

#
# ##########################################################################
#

class CRBCashOperationEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, rbCashOperation)
        self.setWindowTitleEx(u'Кассовая операция')
