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

from library.interchange     import getComboBoxValue, getLineEditValue, setComboBoxValue, setLineEditValue

from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol

from RefBooks.Tables         import rbCode, rbName, rbOKFS

from .Ui_RBOKFSEditor import Ui_ItemEditorDialog


class CRBOKFSList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbOKFS, [rbCode, rbName])
        self.setWindowTitleEx(u'ОКФС')

    def getItemEditor(self):
        return CRBOKFSEditor(self)

#
# ##########################################################################
#

class CRBOKFSEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbOKFS)
        self.setupUi(self)
        self.setWindowTitleEx(u'Элемент справочника ОКФС')


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,               record, rbCode)
        setLineEditValue(   self.edtName,               record, rbName)
        setComboBoxValue(   self.cmbOwnership,          record, 'ownership')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,               record, rbCode)
        getLineEditValue(   self.edtName,               record, rbName)
        getComboBoxValue(   self.cmbOwnership,          record, 'ownership')
        return record
