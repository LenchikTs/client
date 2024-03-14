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

from RefBooks.Tables         import rbCode, rbCodeRegional, rbEmergencyEbriety, rbName

from .Ui_RBEmergency import Ui_ItemEditorDialog


class CRBEmergencyEbrietyList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Региональный код', [rbCodeRegional], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbEmergencyEbriety, [rbCode, rbName])
        self.setWindowTitleEx(u'Состояния опьянение')


    def getItemEditor(self):
        return CRBEmergencyEbrietyEditor(self)

#
# ##########################################################################
#

class CRBEmergencyEbrietyEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbEmergencyEbriety)
        self.setupUi(self)
        self.setWindowTitleEx(u'состояние опьянения')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,         record, rbCode)
        setLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        setLineEditValue(self.edtName,         record, rbName)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,         record, rbCode)
        getLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        getLineEditValue(self.edtName,         record, rbName)
        return record