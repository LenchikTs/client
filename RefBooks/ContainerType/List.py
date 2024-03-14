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

from PyQt4.QtCore            import QVariant

from library.interchange     import getDoubleBoxValue, getRBComboBoxValue, setDoubleBoxValue, setRBComboBoxValue

from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CColorCol, CRefBookCol, CSumCol, CTextCol
from library.Utils           import forceString

from RefBooks.Tables         import rbCode, rbName


from .Ui_RBContainerTypeEditor import Ui_RBContainerTypeEditor

CAmountCol = CSumCol

class CRBContainerTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CColorCol(u'Цветовая маркировка', ['color'], 10, 'r'),
            CAmountCol(u'Объем', ['amount'], 10),
            CRefBookCol(u'Ед.изм.', ['unit_id'], 'rbUnit', 10, showFields=2)
            ], 'rbContainerType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы контейнеров')

    def getItemEditor(self):
        return CRBContainerTypeEditor(self)

#
# ##########################################################################
#

class CRBContainerTypeEditor(Ui_RBContainerTypeEditor, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbContainerType')
        self.setWindowTitleEx(u'Тип контейнера')
        self.cmbUnit.setTable('rbUnit', addNone=True)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        self.cmbColor.setColor(forceString(record.value('color'))) #WFT?
        setDoubleBoxValue(self.edtAmount, record, 'amount')
        setRBComboBoxValue(self.cmbUnit,  record, 'unit_id')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        record.setValue('color', QVariant(self.cmbColor.colorName()))
        getDoubleBoxValue(self.edtAmount, record, 'amount')
        getRBComboBoxValue(self.cmbUnit,  record, 'unit_id')
        return record


