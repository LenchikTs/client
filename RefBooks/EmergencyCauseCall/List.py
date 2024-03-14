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
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CEnumCol, CTextCol

from RefBooks.Tables         import rbCode, rbCodeRegional, rbEmergencyCauseCall, rbName, rbTypeCause

from .Ui_RBEmergencyCauseCall import Ui_ItemEditorDialog


class CRBEmergencyCauseCallList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Региональный код', [rbCodeRegional], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CEnumCol(u'Тип', [rbTypeCause], [u'вызов', u'обслуживание общ.мероприятия'], 20),
            ], rbEmergencyCauseCall, [rbCode, rbName, rbTypeCause])
        self.setWindowTitleEx(u'Поводы к вызову')

    def getItemEditor(self):
        return CRBEmergencyCauseCallEditor(self)

#
# ##########################################################################
#

class CRBEmergencyCauseCallEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbEmergencyCauseCall)
        self.setupUi(self)
        self.setWindowTitleEx(u'Повод к вызову')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,         record, rbCode)
        setLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        setLineEditValue(self.edtName,         record, rbName)
        setComboBoxValue(self.cmbType,         record, rbTypeCause)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,         record, rbCode)
        getLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        getLineEditValue(self.edtName,         record, rbName)
        getComboBoxValue(self.cmbType,         record, rbTypeCause)
        return record

