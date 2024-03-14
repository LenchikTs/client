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
from library.TableModel      import CEnumCol, CTextCol

from .Ui_RBMesSpecificationEditor import Ui_ItemEditorDialog


class CRBMesSpecificationList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',              ['code'],         20),
            CTextCol(u'Наименование',     ['name'],         40),
            CTextCol(u'Региональный код', ['regionalCode'], 40),
            CEnumCol(u'Уровень испонения',['level'], [u'Прерван', u'Выполнен частично', u'Выполнен полностью'], 40),
            ], 'rbMesSpecification', ['code', 'name'])
        self.setWindowTitleEx(u'Особенности выполнения МЭС')


    def getItemEditor(self):
        return CRBMesSpecificationEditor(self)


class CRBMesSpecificationEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbMesSpecification')
        self.setupUi(self)
        self.setWindowTitleEx(u'Особенность выполнения МЭС')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,         record, 'code')
        setLineEditValue(   self.edtName,         record, 'name')
        setLineEditValue(   self.edtRegionalCode, record, 'regionalCode')
        setComboBoxValue(   self.cmbLevel,        record, 'level')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,         record, 'code')
        getLineEditValue(   self.edtName,         record, 'name')
        getLineEditValue(   self.edtRegionalCode, record, 'regionalCode')
        getComboBoxValue(   self.cmbLevel,        record, 'level')
        return record
