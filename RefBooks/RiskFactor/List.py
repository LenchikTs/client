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

from library.ItemsListDialog                    import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel                         import CTextCol
from library.Utils                              import forceString, toVariant
from Ui_RiskFactorEditor                        import Ui_RiskFactorEditor


class CRBRiskFactor(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              ['code'], 20),
            CTextCol(u'Региональный код', ['regionalCode'], 20),
            CTextCol(u'Наименование',     ['name'], 40),
        ], 'rbRiskFactor', ['code', 'name'])
        self.setWindowTitleEx(u'Факторы риска')


    def getItemEditor(self):
        return CRBRiskFactorItemEditor(self)


class CRBRiskFactorItemEditor(Ui_RiskFactorEditor, CItemEditorDialogWithIdentification):
    def __init__(self, parent=None):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbRiskFactor')
        self.setWindowTitleEx(u'Фактор риска')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        self.edtRegionalCode.setText(forceString(record.value('regionalCode')))


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        record.setValue('regionalCode', toVariant(self.edtRegionalCode.text()))
        return record
