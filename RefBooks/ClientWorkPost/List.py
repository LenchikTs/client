# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.ItemsListDialog                    import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel                         import CTextCol


class CRBClientWorkPostList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          ['code'], 20),
            CTextCol(u'Наименование', ['name'], 40),
            ], 'rbClientWorkPost', ['code', 'name'])
        self.setWindowTitleEx(u'Профессии рабочих и должностей служащих')


    def getItemEditor(self):
        return CRBClientWorkPostItemEditor(self)



class CRBClientWorkPostItemEditor(CItemEditorDialogWithIdentification):
    def __init__(self, parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbClientWorkPost')
        self.setWindowTitleEx(u'Профессии рабочих и должностей служащих')
