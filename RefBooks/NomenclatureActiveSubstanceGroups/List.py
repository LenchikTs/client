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

from PyQt4.QtCore import Qt

from library.ItemsListDialog import CItemsListDialog , CItemEditorBaseDialog
from library.TableModel      import CTextCol
from library.interchange     import setLineEditValue, getLineEditValue
from library.Utils           import forceStringEx

from .Ui_RBNomenclatureActiveSubstanceGroupsEditor import Ui_RBNomenclatureActiveSubstanceGroupsEditor


class CRBNomenclatureActiveSubstanceGroupsList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          ['code'], 20),
            CTextCol(u'Наименование', ['name'], 40),
            ], 'rbNomenclatureActiveSubstanceGroups', ['code', 'name'])
        self.setWindowTitleEx(u'Группы действующих веществ')


    def getItemEditor(self):
        return CRBNomenclatureActiveSubstanceGroupsEditor(self)


class CRBNomenclatureActiveSubstanceGroupsEditor(CItemEditorBaseDialog, Ui_RBNomenclatureActiveSubstanceGroupsEditor):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbNomenclatureActiveSubstanceGroups')
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Группа действующего вещества')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, 'code')
        setLineEditValue(self.edtName, record, 'name')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, 'code')
        getLineEditValue(self.edtName, record, 'name')
        return record


    def checkDataEntered(self):
        result = True
        result = result and (forceStringEx(self.edtCode.text()) or self.checkInputMessage(u'код', False, self.edtCode))
        result = result and (forceStringEx(self.edtName.text()) or self.checkInputMessage(u'наименование', False, self.edtName))
        return result

