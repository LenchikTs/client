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

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog
from library.TableModel      import CTextCol
from library.Utils           import forceStringEx, toVariant
from RefBooks.Tables         import rbCode, rbName

from .Ui_RBToxicSubstancesEditor import Ui_RBToxicSubstancesEditor

class CRBToxicSubstancesList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 8),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'МКБ',          ['MKB'], 8),
            ], 'rbToxicSubstances', [rbCode, rbName])
        self.setWindowTitleEx(u'Токсичные вещества')

    def getItemEditor(self):
        return CRBToxicSubstancesEditor(self)

#
# ##########################################################################
#

class CRBToxicSubstancesEditor(CItemEditorBaseDialog, Ui_RBToxicSubstancesEditor):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbToxicSubstances')
        self.setupUi(self)
        self.setWindowTitleEx(u'Токсичные вещества')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, rbCode )
        setLineEditValue(self.edtName,                record, rbName )
        self.cmbMKB.setText(forceStringEx(record.value('MKB')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, rbCode )
        getLineEditValue(self.edtName,                record, rbName )
        record.setValue('MKB', toVariant(forceStringEx(self.cmbMKB.text())))
        return record


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
        result = result and (forceStringEx(self.cmbMKB.text()) or self.checkValueMessage(u'Не указан диагноз', False, self.cmbMKB))
        return result


