# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel import CTextCol

from RefBooks.Tables import rbCode, rbName


class CRBTypeEducationalInstitutionList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbTypeEducationalInstitution', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы учебного заведения')

    def getItemEditor(self):
        return CRBTypeEducationalInstitutionEditor(self)


class CRBTypeEducationalInstitutionEditor(CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbTypeEducationalInstitution')
        self.setWindowTitleEx(u'Тип учебного заведения')
