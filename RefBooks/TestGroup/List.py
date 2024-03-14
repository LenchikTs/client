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

from PyQt4.QtCore import Qt

from library.TableModel      import CTextCol
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBTestGroupEditor   import Ui_RBTestGroupEditor


class CRBTestGroupList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbTestGroup', [rbCode, rbName])
        self.setWindowTitleEx(u'Группы показателей исследований')

    def getItemEditor(self):
        return CRBTestGroupEditor(self)


class CRBTestGroupEditor(Ui_RBTestGroupEditor, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbTestGroup')
        self.setWindowTitleEx(u'Группа показателей исследований')
        self.edtCode.setFocus(Qt.OtherFocusReason)


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        return record
