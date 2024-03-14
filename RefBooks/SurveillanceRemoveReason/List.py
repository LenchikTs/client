# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019-2021 SAMSON Group. All rights reserved.
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
from library.interchange     import getLineEditValue, setLineEditValue, setRBComboBoxValue, getRBComboBoxValue
from RefBooks.Tables         import rbCode, rbName

from Ui_RBSurveillanceRemoveReasonEditor import Ui_RBSurveillanceRemoveReasonEditor


class CRBSurveillanceRemoveReasonList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            # CRefBookCol(u'Отметка ДН',['dispanser_id'], 'rbDispanser', 10),
            ], 'rbSurveillanceRemoveReason', [rbCode, rbName])
        self.setWindowTitleEx(u'Причины снятия с Диспансерного наблюдения')


    def getItemEditor(self):
        return CRBSurveillanceRemoveReasonEditor(self)

#
# ##########################################################################
#

class CRBSurveillanceRemoveReasonEditor(Ui_RBSurveillanceRemoveReasonEditor, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbSurveillanceRemoveReason')
        self.setWindowTitleEx(u'Причина снятия с Диспансерного наблюдения')
        self.cmbDispanser.setTable('rbDispanser')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setLineEditValue(  self.edtCode,      record, 'code')
        setLineEditValue(  self.edtName,      record, 'name')
        setRBComboBoxValue(self.cmbDispanser, record, 'dispanser_id')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getLineEditValue(  self.edtCode,      record, 'code')
        getLineEditValue(  self.edtName,      record, 'name')
        getRBComboBoxValue(self.cmbDispanser, record, 'dispanser_id')
        return record

