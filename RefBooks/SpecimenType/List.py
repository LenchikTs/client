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

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBSpecimenTypeEditor import Ui_SpecimenTypeEditorDialog


class CRBSpecimenTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Латинское наименование', ['latinName'], 40),
            ], 'rbSpecimenType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы образцов')

    def getItemEditor(self):
        return CRBSpecimenTypeEditor(self)


# #####################################################################################


class CRBSpecimenTypeEditor(Ui_SpecimenTypeEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbSpecimenType')
        self.setWindowTitleEx(u'Тип образца')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue( self.edtLatinName, record, 'latinName')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue( self.edtLatinName, record, 'latinName')
        return record
