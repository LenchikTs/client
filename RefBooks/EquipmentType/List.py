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

from library.interchange     import getLineEditValue, setLineEditValue, getRBComboBoxValue, setRBComboBoxValue
from library.ItemsListDialog import CItemsListDialogEx, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CRefBookCol
from RefBooks.Tables         import rbCode, rbEquipmentType, rbName

from .Ui_RBEquipmentTypeEditor import Ui_RBEquipmentTypeEditorDialog


class CRBEquipmentTypeList(CItemsListDialogEx):
    def __init__(self, parent):
        CItemsListDialogEx.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CRefBookCol(u'Класс',   ['class_id'], 'rbEquipmentClass', 20),
            ], rbEquipmentType, [rbCode, rbName])
        self.setWindowTitleEx(u'Типы оборудования')
        self.actDuplicate.setVisible(False)


    def getItemEditor(self):
        return CRBEquipmentTypeEditor(self)


class CRBEquipmentTypeEditor(CItemEditorBaseDialog, Ui_RBEquipmentTypeEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbEquipmentType)
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип оборудования')
        self.cmbClass.setTable('rbEquipmentClass', True)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,         record, 'code')
        setLineEditValue(   self.edtName,         record, 'name')
        setRBComboBoxValue( self.cmbClass,        record, 'class_id')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,         record, 'code')
        getLineEditValue(   self.edtName,         record, 'name')
        getRBComboBoxValue( self.cmbClass,        record, 'class_id')
        return record
