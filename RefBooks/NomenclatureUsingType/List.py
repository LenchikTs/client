# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel import CTextCol
from RefBooks.Tables    import rbCode, rbName

from Ui_RBNomenclatureUsingTypeEditor import Ui_ItemEditorDialog


class CRBNomenclatureUsingTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              [rbCode],      10),
            CTextCol(u'Наименование',     [rbName],      40),
            ], 'rbNomenclatureUsingType', [rbCode, rbName])
        self.setWindowTitleEx(u'Способы применения')


    def getItemEditor(self):
        return CRBNomenclatureUsingTypeEditor(self)


class CRBNomenclatureUsingTypeEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbNomenclatureUsingType')
        self.setWindowTitleEx(u'Способ применения')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        return record

