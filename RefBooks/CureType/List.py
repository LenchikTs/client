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

from library.interchange     import getLineEditValue, getDateEditValue, setLineEditValue, setDateEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CDateCol

from RefBooks.Tables import rbCode, rbCureType, rbName, rbRegionalCode

from .Ui_RBCureTypeEditor import Ui_ItemEditorDialog


class CRBCureType(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Региональный код', [rbRegionalCode], 20),
            CDateCol(u'Дата окончания действия', ['endDate'],  10),
            ], rbCureType, [rbCode, rbName])
        self.setWindowTitleEx(u'Виды лечения')

    def getItemEditor(self):
        return CRBCureTypeEditor(self)

#
# ##########################################################################
#

class CRBCureTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbCureType)
        self.setupUi(self)
        self.setWindowTitleEx(u'Вид лечения')
        self.setupDirtyCather()
        self.edtEndDate.canBeEmpty()



    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue( self.edtCode,              record, rbCode)
        setLineEditValue( self.edtName,              record, rbName)
        setLineEditValue( self.edtRegionalCode,      record, rbRegionalCode)
        setDateEditValue( self.edtEndDate,           record, 'endDate')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue( self.edtCode,              record, rbCode)
        getLineEditValue( self.edtName,              record, rbName)
        getLineEditValue( self.edtRegionalCode,      record, rbRegionalCode)
        getDateEditValue( self.edtEndDate,           record, 'endDate')
        return record
