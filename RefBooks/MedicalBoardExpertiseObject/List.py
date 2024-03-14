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

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol, CRefBookCol
from library.interchange     import setRBComboBoxValue, getRBComboBoxValue
from RefBooks.Tables         import rbCode, rbName

from .Ui_RBMedicalBoardExpertiseKindEditor import Ui_ItemEditorDialog


class CRBMedicalBoardExpertiseObject(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CRefBookCol(u'Характеристика экспертизы', ['expertiseCharacter_id'], 'rbMedicalBoardExpertiseCharacter', 30),
            ], 'rbMedicalBoardExpertiseObject', [rbCode, rbName])
        self.setWindowTitleEx(u'Предметы экспертизы')


    def getItemEditor(self):
        return CRBMedicalBoardExpertiseObjectEditor(self)

#
# ##########################################################################
#

class CRBMedicalBoardExpertiseObjectEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbMedicalBoardExpertiseObject')
        self.setWindowTitleEx(u'Предмет экспертизы')
        self.cmbExpertiseCharacter.setTable('rbMedicalBoardExpertiseCharacter', False)


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setRBComboBoxValue( self.cmbExpertiseCharacter, record, 'expertiseCharacter_id')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getRBComboBoxValue( self.cmbExpertiseCharacter, record, 'expertiseCharacter_id')
        return record
