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


from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog  import CItemsListDialog
from library.TableModel       import  CTextCol
from RefBooks.Tables          import rbCode, rbName
from .Ui_RBReactionTypeEditor import Ui_RBReactionTypeEditor


class CRBReactionTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbReactionType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы реакции')

    def getItemEditor(self):
        return CRBReactionTypeEditor(self)

#
# ##########################################################################
#

class CRBReactionTypeEditor(Ui_RBReactionTypeEditor, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbReactionType')
        self.setWindowTitleEx(u'Тип реакции')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        return record

