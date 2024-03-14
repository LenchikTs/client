# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019-2020 SAMSON Group. All rights reserved.
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


class CRBTempInvalidAnnulmentReasonList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbTempInvalidAnnulmentReason', [rbCode, rbName])
        self.setWindowTitleEx(u'Причины аннулирования документов ВУТ')


    def getItemEditor(self):
        return CRBTempInvalidAnnulmentReasonEditor(self)

#
# ##########################################################################
#

class CRBTempInvalidAnnulmentReasonEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbTempInvalidAnnulmentReason')
        self.setWindowTitleEx(u'Причина аннулирования документов ВУТ')
