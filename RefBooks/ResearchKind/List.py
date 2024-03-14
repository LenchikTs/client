# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
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

from RefBooks.Tables         import rbCode, rbName, rbClientResearchKind

from RefBooks.ResearchKind.Ui_RBResearchKindEditor import Ui_ItemEditorDialog


class CRBResearchKindList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CBoolCol(u'Визуализация в шильдике',   ['inClientInfoBrowser'], 10),
            ], rbClientResearchKind, [rbCode, rbName])
        self.setWindowTitleEx(u'Виды обследований')


    def getItemEditor(self):
        return CRBResearchKindEditor(self)


class CRBResearchKindEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbClientResearchKind)
        self.setupUi(self)
        self.setWindowTitleEx(u'Вид обследования')
        self.setupDirtyCather()

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, rbCode)
        setLineEditValue(self.edtName, record, rbName)
        setCheckBoxValue(self.chkInClientInfoBrowser, record, 'inClientInfoBrowser')

    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, rbCode)
        getLineEditValue(self.edtName, record, rbName)
        getCheckBoxValue(self.chkInClientInfoBrowser, record, 'inClientInfoBrowser')
        return record
