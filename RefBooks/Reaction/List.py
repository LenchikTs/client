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
from RefBooks.Reaction.Ui_RBReactionEditor import Ui_RBReactionEditor
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName


class CRBReactionList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbReaction', [rbCode, rbName])

        self.tblItems.addPopupDelRow()

        self.setWindowTitleEx(u'Реакции')

    def getItemEditor(self):
        return CRBReactionEditor(self)

#
# ##########################################################################
#

class CRBReactionEditor(Ui_RBReactionEditor, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbReaction')
        self.setWindowTitleEx(u'Реакция')
        self.setupDirtyCather()

    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        return record
