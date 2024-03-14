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


from library.TableModel      import CTextCol
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog

from RefBooks.Tables         import rbCode, rbName

# Какое скверное имя таблицы :(
# rbLfForm - это «Формы выпуска лекарственных препаратов»
# должно быть rbDosageForm

class CRBLfFormList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbLfForm', [rbCode, rbName])
        self.setWindowTitleEx(u'Формы выпуска лекарственных препаратов')


    def getItemEditor(self):
        return CRBLfFormEditor(self)


class CRBLfFormEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbLfForm')
        self.setWindowTitleEx(u'Форма выпуска лекарственных препаратов')
