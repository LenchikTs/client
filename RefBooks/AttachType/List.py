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

from library.interchange     import getCheckBoxValue, getLineEditValue, getRBComboBoxValue, setCheckBoxValue, setLineEditValue, setRBComboBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CBoolCol, CRefBookCol, CTextCol

from RefBooks.Tables         import rbAttachType, rbCode, rbFinance, rbName

from .Ui_RBAttachTypeEditor import Ui_ItemEditorDialog


class CRBAttachTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                     [rbCode], 10),
            CTextCol(u'Наименование',            [rbName], 30),
            CBoolCol(u'Временно',                ['temporary'], 10),
            CBoolCol(u'Выбытие',                 ['outcome'],   10),
            CRefBookCol(u'Источник финансирования', ['finance_id'], rbFinance, 30),
            CTextCol(u'Региональный код',  ['regionalCode'], 10)
            ], rbAttachType, [rbCode, rbName])
        self.setWindowTitleEx(u'Типы прикрепления')

    def getItemEditor(self):
        return CRBAttachTypeEditor(self)
#
# ##########################################################################
#

class CRBAttachTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbAttachType)
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип прикрепления')
        self.cmbFinance.setTable(rbFinance, False)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        setCheckBoxValue(   self.checkBox,         record, 'temporary')
        setCheckBoxValue(   self.chkOutcome,       record, 'outcome')
        setRBComboBoxValue( self.cmbFinance,       record, 'finance_id')
        setLineEditValue(   self.edtRegionalCode,  record, 'regionalCode')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        getCheckBoxValue(   self.checkBox,         record, 'temporary')
        getCheckBoxValue(   self.chkOutcome,       record, 'outcome')
        getRBComboBoxValue( self.cmbFinance,       record, 'finance_id')
        getLineEditValue(   self.edtRegionalCode,  record, 'regionalCode')
        return record


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
        result = result and (self.cmbFinance.value() or self.checkInputMessage(u'тип финансирования', False, self.cmbFinance))
        return result
