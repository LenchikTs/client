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

from library.interchange         import getDateEditValue, setDateEditValue
from library.ItemsListDialog     import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel          import CTextCol, CDateCol
from library.Utils               import forceString, forceStringEx, toVariant, trim

from RefBooks.Tables             import rbCode, rbName

from .Ui_RBTumorEditor           import Ui_RBTumorEditor


class CRBTumorList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Диагноз',      ['MKB'], 20),
            CDateCol(u'Дата начала', ['begDate'], 20),
            CDateCol(u'Дата окончания', ['endDate'], 20)
            ], 'rbTumor', [rbCode, rbName, 'MKB'])
        self.setWindowTitleEx(u'Размеры первичной опухоли')

    def getItemEditor(self):
        return CRBTumorEditor(self)


class CRBTumorEditor(Ui_RBTumorEditor, CItemEditorDialogWithIdentification):
    doCheckName = False

    def __init__(self, parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbTumor')
        self.setWindowTitleEx(u'Размер первичной опухоли')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        self.cmbMKB.setText(forceString(record.value('MKB')))
        setDateEditValue(self.edtBegDate, record, 'begDate')
        setDateEditValue(self.edtEndDate, record, 'endDate')
        self.modelIdentification.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        record.setValue('MKB', toVariant(forceStringEx(self.cmbMKB.text())))
        getDateEditValue(self.edtBegDate, record, 'begDate')
        getDateEditValue(self.edtEndDate, record, 'endDate')
        return record

    def checkDataEntered(self):
        result = CItemEditorDialogWithIdentification.checkDataEntered(self)
        result = result and (trim(forceStringEx(self.cmbMKB.text())) or self.checkInputMessage(u'диагноз', True, self.cmbMKB))
        return result
