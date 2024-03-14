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

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName, rbTraumaType

from .Ui_RBTraumaTypeEditor  import Ui_ItemEditorDialog


class CRBTraumaTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 10),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Код ЕГИСЗ',    ['usishCode'], 10),
            ], rbTraumaType, [rbCode, rbName])
        self.setWindowTitleEx(u'Типы травмы')

    def getItemEditor(self):
        return CRBTraumaTypeEditor(self)

#
# ##########################################################################
#

class CRBTraumaTypeEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):

    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbTraumaType)
        self.setWindowTitleEx(u'Тип травмы')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtUsishCode,    record, 'usishCode')

    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(self.edtUsishCode,    record, 'usishCode')
        return record