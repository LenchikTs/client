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

from RefBooks.Tables         import rbCode, rbFinance, rbName, rbPayRefuseType

from .Ui_RBPayRefuseTypeEditor import Ui_ItemEditorDialog


class CRBPayRefuseTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CRefBookCol(u'Источник финансирования', ['finance_id'], rbFinance, 30),
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CBoolCol(u'Возможно перевыставление',   ['rerun'], 10),
            CTextCol(u'Основание',          ['reason'], 20),

            ], rbPayRefuseType, [rbCode, rbName])
        self.setWindowTitleEx(u'Причины отказа платежа')

    def getItemEditor(self):
        return CRBPayRefuseTypeEditor(self)

#
# ##########################################################################
#

class CRBPayRefuseTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbPayRefuseType)
        self.setupUi(self)
        self.setWindowTitleEx(u'Причина отказа платежа')
        self.cmbFinance.setTable(rbFinance, False)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setRBComboBoxValue( self.cmbFinance,       record, 'finance_id')
        setLineEditValue(   self.edtCode,          record, rbCode)
        setLineEditValue(   self.edtName,          record, rbName)
        setCheckBoxValue(   self.chkCanRerun,      record, 'rerun')
        setLineEditValue(   self.edtReason,        record, 'reason')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getRBComboBoxValue( self.cmbFinance,       record, 'finance_id')
        getLineEditValue(   self.edtCode,          record, rbCode)
        getLineEditValue(   self.edtName,          record, rbName)
        getCheckBoxValue(   self.chkCanRerun,      record, 'rerun')
        getLineEditValue(   self.edtReason,        record, 'reason')
        return record
