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

from PyQt4.QtCore import pyqtSignature

from library.interchange     import (
                                     getLineEditValue,
                                     getRBComboBoxValue,
                                     setLineEditValue,
                                     setRBComboBoxValue,
                                     setDateEditValue,
                                     getDateEditValue,
                                    )
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CRefBookCol, CTextCol, CDateCol

from RefBooks.Tables         import (
                                     rbCode,
                                     rbDiagnosticResult,
                                     rbEventTypePurpose,
                                     rbName,
                                     rbResult,
                                     rbBegDate,
                                     rbEndDate,
                                    )

from Ui_RBDiagnosticResultEditor import Ui_ItemEditorDialog


class CRBDiagnosticResultList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CRefBookCol(u'Назначение',      ['eventPurpose_id'], rbEventTypePurpose, 30),
            CTextCol(   u'Код',             [rbCode],        10),
            CTextCol(   u'Региональный код',['regionalCode'],10),
            CTextCol(   u'Наименование',    [rbName],        30),
            CTextCol(   u'Федеральный код', ['federalCode'], 10),
            CTextCol(   u'Код ЕГИСЗ',       ['usishCode'],   10),
            CRefBookCol(u'Результат обращения', ['result_id'], rbResult, 30),
            CDateCol(   u'Дата начала',     [rbBegDate],     20),
            CDateCol(   u'Дата окончания',  [rbEndDate],     20),
            ], rbDiagnosticResult, ['eventPurpose_id', rbCode, rbName, rbBegDate, rbEndDate])
        self.setWindowTitleEx(u'Результаты осмотра')

    def getItemEditor(self):
        return CRBDiagnosticResultEditor(self)
#
# ##########################################################################
#

class CRBDiagnosticResultEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbDiagnosticResult)
        self.setWindowTitleEx(u'Результат осмотра')
        self.cmbEventPurpose.setTable(rbEventTypePurpose, False)
        self.cmbResult.setTable(rbResult, True)


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setRBComboBoxValue( self.cmbEventPurpose, record, 'eventPurpose_id')
        setLineEditValue(   self.edtFederalCode,  record, 'federalCode')
        setLineEditValue(   self.edtUsishCode,    record, 'usishCode')
        setLineEditValue(   self.edtRegionalCode, record, 'regionalCode')
        setRBComboBoxValue( self.cmbResult,       record, 'result_id')
        setDateEditValue(   self.edtBegDate,      record, 'begDate')
        setDateEditValue(   self.edtEndDate,      record, 'endDate')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getRBComboBoxValue( self.cmbEventPurpose, record, 'eventPurpose_id')
        getLineEditValue(   self.edtFederalCode,  record, 'federalCode')
        getLineEditValue(   self.edtUsishCode,    record, 'usishCode')
        getLineEditValue(   self.edtRegionalCode, record, 'regionalCode')
        getRBComboBoxValue( self.cmbResult,       record, 'result_id')
        getDateEditValue(   self.edtBegDate,      record, 'begDate')
        getDateEditValue(   self.edtEndDate,      record, 'endDate')
        return record


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        filter = 'eventPurpose_id=%d' % self.cmbEventPurpose.value() if self.cmbEventPurpose.value() else ''
        id = self.cmbResult.value()
        if id:
            code = self.cmbResult.code()
        self.cmbResult.setFilter(filter)
        if id:
            self.cmbResult.setCode(code)
        else:
            self.cmbResult.setValue(id)

