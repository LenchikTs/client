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
from library.TableModel import CTextCol

from RefBooks.Tables import rbCode, rbDocumentTypeGroup, rbName


class CRBDocumentTypeGroupList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbDocumentTypeGroup, [rbCode, rbName])
        self.setWindowTitleEx(u'Группы типов документов')

    def getItemEditor(self):
        return CRBDocumentTypeGroupEditor(self)


class CRBDocumentTypeGroupEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, rbDocumentTypeGroup)
        self.setWindowTitleEx(u'Группа типов документов')
