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

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName


class CRBLivingAreaList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 10),
            CTextCol(u'Наименование', [rbName], 40)
            ], 'rbLivingArea', [rbCode, rbName])
        self.setWindowTitleEx(u'Зоны проживания')


    def getItemEditor(self):
        return CRBLivingAreaEditor(self)


class CRBLivingAreaEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbLivingArea')
        self.setWindowTitleEx(u'Зона проживания')