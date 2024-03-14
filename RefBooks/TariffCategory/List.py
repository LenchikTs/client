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

from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName, rbTariffCategory

from .Ui_RBTariffCategoryEditor import Ui_ItemEditorDialog


class CRBTariffCategoryList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          ['code'], 20),
            CTextCol(u'Наименование', ['name'], 40),
            CTextCol(u'Федеральный код', ['federalCode'], 10),
            ], rbTariffCategory, [rbCode, rbName])
        self.setWindowTitleEx(u'Тарифные категории')

    def getItemEditor(self):
        return CRBTariffCategoryEditor(self)

#
# ##########################################################################
#

class CRBTariffCategoryEditor(Ui_ItemEditorDialog, CItemEditorBaseDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbTariffCategory)
        self.setupUi(self)
        self.setWindowTitleEx(u'Тарифная категория')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,         record, 'code')
        setLineEditValue(self.edtName,         record, 'name')
        setLineEditValue(self.edtFederalCode,  record, 'federalCode')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,         record, 'code')
        getLineEditValue(self.edtName,         record, 'name')
        getLineEditValue(self.edtFederalCode,  record, 'federalCode')
        return record