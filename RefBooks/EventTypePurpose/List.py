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

from library.interchange     import getComboBoxValue, getLineEditValue, setComboBoxValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbEventTypePurpose, rbName

from .Ui_RBEventTypePurposeEditor   import Ui_ItemEditorDialog


class CRBEventTypePurposeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              [rbCode], 10),
            CTextCol(u'Наименование',     [rbName], 40),
            CTextCol(u'Федеральный код',  ['federalCode'], 10),
            CTextCol(u'Код ЕГИСЗ',        ['usishCode'],   10),
            CTextCol(u'Региональный код', ['regionalCode'], 10),
            CTextCol(u'Цель',             ['purpose'], 10)
            ], rbEventTypePurpose, [rbCode, rbName])
        self.setWindowTitleEx(u'Назначение типов событий')


    def getItemEditor(self):
        return CRBEventTypePurposeEditor(self)


class CRBEventTypePurposeEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbEventTypePurpose)
        self.setWindowTitleEx(u'Назначение типа событий')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setLineEditValue(self.edtFederalCode,  record, 'federalCode')
        setLineEditValue(self.edtUsishCode,    record, 'usishCode')
        setComboBoxValue(self.cmbPurpose,      record, 'purpose')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getLineEditValue(self.edtFederalCode,  record, 'federalCode')
        getLineEditValue(self.edtUsishCode,    record, 'usishCode')
        getComboBoxValue(self.cmbPurpose,      record, 'purpose')
        return record
