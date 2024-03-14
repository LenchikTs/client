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
from library.ItemsListDialog import CItemsListDialog,  CItemEditorBaseDialog
from library.TableModel      import CEnumCol, CTextCol

from RefBooks.Tables         import rbCode, rbName, TempInvalidTypeList

from .Ui_RBTempInvalidRegimeEditor import Ui_RBTempInvalidRegimeEditorDialog


class CRBTempInvalidRegimeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CEnumCol(u'Класс',        ['type'], TempInvalidTypeList, 10),
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbTempInvalidRegime', ['type', rbCode, rbName])
        self.setWindowTitleEx(u'Режимы ВУТ, инвалидности или ограничения жизнедеятельности')

    def getItemEditor(self):
        return CRBTempInvalidRegimeEditor(self)

#
# ##########################################################################
#


class CRBTempInvalidRegimeEditor(Ui_RBTempInvalidRegimeEditorDialog, CItemEditorBaseDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbTempInvalidRegime')
        self.setupUi(self)
        self.setWindowTitleEx(u'Режим ВУТ, инвалидности или ограничения жизнедеятельности')
        self.cmbType.addItems(TempInvalidTypeList)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setComboBoxValue(self.cmbType, record, 'type')
        setLineEditValue(self.edtCode, record, 'code')
        setLineEditValue(self.edtName, record, 'name')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getComboBoxValue(self.cmbType, record, 'type')
        getLineEditValue(self.edtCode, record, 'code')
        getLineEditValue(self.edtName, record, 'name')
        return record
