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

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName


class CRBTempInvalidDuplicateReasonList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbTempInvalidDuplicateReason', [rbCode, rbName])
        self.setWindowTitleEx(u'Причины выдачи дубликатов документов ВУТ')


    def getItemEditor(self):
        return CRBTempInvalidDuplicateReasonEditor(self)


#
# ##########################################################################
#


class CRBTempInvalidDuplicateReasonEditor(CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbTempInvalidDuplicateReason')
        self.setWindowTitleEx(u'Причина выдачи дубликатов документов ВУТ')
