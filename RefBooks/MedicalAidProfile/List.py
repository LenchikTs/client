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

from RefBooks.Tables         import rbCode, rbName

from Ui_RBMedicalAidProfileEditor import Ui_ItemEditorDialog



class CRBMedicalAidProfileList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              [rbCode],         20),
            CTextCol(u'Наименование',     [rbName],         40),
            CTextCol(u'Федеральный код',  ['federalCode'],  40),
            CTextCol(u'Региональный код', ['regionalCode'], 40),
            ], 'rbMedicalAidProfile', [rbCode, rbName])
        self.setWindowTitleEx(u'Профили медицинской помощи')

    def getItemEditor(self):
        return CRBMedicalAidProfileEditor(self)


class CRBMedicalAidProfileEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbMedicalAidProfile')
        self.setWindowTitleEx(u'Профиль медицинской помощи')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(   self.edtCode,         record, 'code')
        setLineEditValue(   self.edtName,         record, 'name')
        setLineEditValue(   self.edtFederalCode,  record, 'federalCode')
        setLineEditValue(   self.edtRegionalCode, record, 'regionalCode')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(   self.edtCode,         record, 'code')
        getLineEditValue(   self.edtName,         record, 'name')
        getLineEditValue(   self.edtFederalCode,  record, 'federalCode')
        getLineEditValue(   self.edtRegionalCode, record, 'regionalCode')
        return record
