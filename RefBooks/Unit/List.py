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


from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel import CTextCol
from library.Utils import forceString, toVariant, forceStringEx

from RefBooks.Tables import rbCode, rbName, rbUnit
from RefBooks.Unit.Ui_RBUnitEditor import Ui_RBUnitEditor


class CRBUnitList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Латинское наименование', ['latinName'], 40),
            ], rbUnit, [rbCode, rbName])
        self.setWindowTitleEx(u'Единицы измерения')


    def getItemEditor(self):
        return CRBUnitEditor(self)


class CRBUnitEditor(Ui_RBUnitEditor, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbUnit)
        self.setWindowTitleEx(u'Единица измерения')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        self.edtLatinName.setText(forceString(record.value('latinName')))
        self.modelIdentification.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        record.setValue('latinName', toVariant(forceStringEx(self.edtLatinName.text())))
        return record
