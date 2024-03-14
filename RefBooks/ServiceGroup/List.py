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

from RefBooks.Tables import rbCode, rbName, rbServiceGroup

from Ui_RBServiceGroupEditor import Ui_ItemEditorDialog


class CRBServiceGroupList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(   u'Код',         [rbCode], 10),
            CTextCol(   u'Региональный код', ['regionalCode'], 10),
            CTextCol(   u'Наименование',[rbName], 30),
            ], rbServiceGroup, [rbCode, rbName])
        self.setWindowTitleEx(u'Группы услуг')


    def getItemEditor(self):
        return CRBServiceGroupEditor(self)

#
# ##########################################################################
#

class CRBServiceGroupEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbServiceGroup)
        self.setupUi(self)
        self.setWindowTitleEx(u'Группа услуг')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, 'code' )
        setLineEditValue(self.edtName,                record, 'name' )
        setLineEditValue(self.edtRegionalCode,        record, 'regionalCode' )


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, 'code' )
        getLineEditValue(self.edtName,                record, 'name' )
        getLineEditValue(self.edtRegionalCode,        record, 'regionalCode' )
        return record
