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
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialogEx
from library.TableModel      import CTextCol
from RefBooks.Tables         import rbCode, rbEquipmentClass, rbName

from .Ui_RBEquipmentClassEditor import Ui_RBEquipmentClassEditorDialog


class CRBEquipmentClassList(CItemsListDialogEx):
    def __init__(self, parent):
        CItemsListDialogEx.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbEquipmentClass, [rbCode, rbName])
        self.setWindowTitleEx(u'Классы оборудования')
        self.actDuplicate.setVisible(False)


    def getItemEditor(self):
        return CRBEquipmentClassEditor(self)


class CRBEquipmentClassEditor(CItemEditorBaseDialog, Ui_RBEquipmentClassEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbEquipmentClass)
        self.setupUi(self)
        self.setWindowTitleEx(u'Класс оборудования')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,         record, 'code')
        setLineEditValue(   self.edtName,         record, 'name')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,         record, 'code')
        getLineEditValue(   self.edtName,         record, 'name')
        return record
