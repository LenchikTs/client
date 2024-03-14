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
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel import CTextCol
from library.ItemsListDialog import CItemsListDialog

from RefBooks.Tables import rbCode, rbHurtFactorType, rbName


class CRBHurtFactorTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbHurtFactorType, [rbCode, rbName])
        self.setWindowTitleEx(u'Факторы вредности')

    def getItemEditor(self):
        return CRBHurtFactorTypeEditor(self)


class CRBHurtFactorTypeEditor(CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbHurtFactorType)
        self.setWindowTitleEx(u'Фактор вредности')
