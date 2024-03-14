# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.interchange import setLineEditValue, getLineEditValue, setCheckBoxValue, getCheckBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel import CTextCol, CBoolCol

from RefBooks.Tables import rbCode, rbName

from RefBooks.DiagnosticService.Ui_RBDiagnosticServiceEditor import Ui_ItemEditorDialog


class CRBDiagnosticServiceList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Полное наименование', ['fullName'], 60),
            CTextCol(u'Метод', ['method'], 20),
            CTextCol(u'Область', ['area'], 20),
            CTextCol(u'Локализация', ['localization'], 20),
            CTextCol(u'Компоненты', ['components'], 20),
            CBoolCol(u'Применяемость', ['applicability'], 20),
            ], 'rbDiagnosticService', [rbCode, rbName])
        self.setWindowTitleEx(u'Виды инструментальных исследований')

    def getItemEditor(self):
        return CRBDiagnosticServiceEditor(self)


class CRBDiagnosticServiceEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbDiagnosticService')
        self.setupUi(self)
        self.setWindowTitleEx(u'Вид инструментального исследования')
        self.setupDirtyCather()

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, 'code')
        setLineEditValue(self.edtName, record, 'name')
        setLineEditValue(self.edtFullName, record, 'fullName')
        setLineEditValue(self.edtMethod, record, 'method')
        setLineEditValue(self.edtArea, record, 'area')
        setLineEditValue(self.edtLocalization, record, 'localization')
        setLineEditValue(self.edtComponents, record, 'components')
        setCheckBoxValue(self.chkApplicability, record, 'applicability')

    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, 'code')
        getLineEditValue(self.edtName, record, 'name')
        getLineEditValue(self.edtFullName, record, 'fullName')
        getLineEditValue(self.edtMethod, record, 'method')
        getLineEditValue(self.edtArea, record, 'area')
        getLineEditValue(self.edtLocalization, record, 'localization')
        getLineEditValue(self.edtComponents, record, 'components')
        getCheckBoxValue(self.chkApplicability, record, 'applicability')
        return record
