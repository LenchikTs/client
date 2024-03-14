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

from library.interchange     import getCheckBoxValue, getLineEditValue, setCheckBoxValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CBoolCol, CTextCol

from RefBooks.Tables        import rbCode, rbExpenseServiceItem, rbName

from Ui_RBExpenseServiceItem import Ui_RBExpenseServiceItem


class CRBExpenseServiceItemList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CBoolCol(u'Является базовой', ['isBase'], 10),
            ], rbExpenseServiceItem, [rbCode, rbName])
        self.setWindowTitleEx(u'Статьи затрат услуг')

    def getItemEditor(self):
        return CRBExpenseServiceItemEditor(self)

#
# ##########################################################################
#

class CRBExpenseServiceItemEditor(CItemEditorBaseDialog, Ui_RBExpenseServiceItem):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbExpenseServiceItem)
        self.setupUi(self)
        self.setWindowTitleEx(u'Статья затрат услуг')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,   record, rbCode )
        setLineEditValue(self.edtName,   record, rbName )
        setCheckBoxValue(self.chkIsBase, record, 'isBase')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,   record, rbCode )
        getLineEditValue(self.edtName,   record, rbName )
        getCheckBoxValue(self.chkIsBase, record, 'isBase')
        return record
