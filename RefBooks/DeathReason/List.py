# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.interchange import getLineEditValue, setLineEditValue, setDateEditValue, getDateEditValue
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog
from library.TableModel import CTextCol, CDateCol
from RefBooks.Tables import rbCode, rbName, rbFederalCode, rbRegionalCode, rbBegDate, rbEndDate
from RefBooks.DeathReason.Ui_RBDeathReasonEditor import Ui_RBDeathReasonEditor


class CRBDeathReasonList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Региональный код', [rbRegionalCode], 20),
            CTextCol(u'Федеральный код', [rbFederalCode], 20),
            CDateCol(u'Дата начала действия', [rbBegDate], 20),
            CDateCol(u'Дата окончания действия', [rbEndDate], 20)
            ], 'rbDeathReason', [rbCode, rbName])
        self.setWindowTitleEx(u'Причины смерти')

    def getItemEditor(self):
        return CRBDeathReasonEditor(self)


class CRBDeathReasonEditor(CItemEditorBaseDialog, Ui_RBDeathReasonEditor):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbDeathReason')
        self.setupUi(self)
        self.setWindowTitleEx(u'Причина смерти')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, rbCode)
        setLineEditValue(self.edtName, record, rbName)
        setLineEditValue(self.edtRegionalCode, record, rbRegionalCode)
        setLineEditValue(self.edtFederalCode, record, rbFederalCode)
        setDateEditValue(self.edtBegDate, record, rbBegDate)
        setDateEditValue(self.edtEndDate, record, rbEndDate)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, rbCode)
        getLineEditValue(self.edtName, record, rbName)
        getLineEditValue(self.edtRegionalCode, record, rbRegionalCode)
        getLineEditValue(self.edtFederalCode, record, rbFederalCode)
        getDateEditValue(self.edtBegDate, record, rbBegDate)
        getDateEditValue(self.edtEndDate, record, rbEndDate)
        return record