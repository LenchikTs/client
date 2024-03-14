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

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol
from RefBooks.Tables         import rbCode, rbName, rbDeathCauseType


class CRBDeathCauseTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbDeathCauseType, [rbCode, rbName])
        self.setWindowTitleEx(u'Род причины смерти')

    def getItemEditor(self):
        dialog = CItemEditorDialog(self, rbDeathCauseType)
        dialog.setWindowTitle(u'Род причины смерти')
        return dialog
