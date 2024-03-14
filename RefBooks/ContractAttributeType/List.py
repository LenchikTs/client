# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2020 SAMSON Group. All rights reserved.
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

from RefBooks.Tables import rbCode, rbName


class CRBContractAttributeTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbContractAttributeType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы атрибутов договоров')

    def getItemEditor(self):
        return CRBContractAttributeTypeEditor(self)

#
# ##########################################################################
#

class CRBContractAttributeTypeEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbContractAttributeType')
        self.setWindowTitleEx(u'Тип атрибута договоров')
