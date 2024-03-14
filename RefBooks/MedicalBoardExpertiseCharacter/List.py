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

from Registry.Utils          import expertiseClass
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol, CEnumCol
from library.interchange     import setComboBoxValue, getComboBoxValue
from RefBooks.Tables         import rbCode, rbName

from .Ui_RBMedicalBoardExpertiseCharacterEditor import Ui_ItemEditorDialog


class CRBMedicalBoardExpertiseCharacter(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CEnumCol(u'Класс',        ['class'], expertiseClass, 20),
            ], 'rbMedicalBoardExpertiseCharacter', [rbCode, rbName])
        self.setWindowTitleEx(u'Характеристики экспертизы')


    def getItemEditor(self):
        return CRBMedicalBoardExpertiseCharacterEditor(self)

#
# ##########################################################################
#

class CRBMedicalBoardExpertiseCharacterEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbMedicalBoardExpertiseCharacter')
        self.setWindowTitleEx(u'Характеристика экспертизы')
        items = []
        for item in expertiseClass:
            items.append(item[0])
        self.cmbClass.addItems(items)


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setComboBoxValue( self.cmbClass, record, 'class')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getComboBoxValue( self.cmbClass, record, 'class')
        return record

