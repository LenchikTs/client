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
#WTF? rbDocumentTypeLocation == 'справочник мест типов документов'
#     RBLocationCardType == 'справочник типов карт мест'
#     а нужно - 'справочник (типов) мест документов'

from PyQt4.QtCore import QVariant

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CColorCol, CTextCol

from library.Utils           import forceString

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBLocationCardEditor import Ui_ItemEditorDialog


class CRBLocationCardTypeList(CItemsListDialog):
    def __init__(self, parent):
            CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CColorCol(u'Цветовая маркировка', ['color'], 10, 'r')
            ], 'rbDocumentTypeLocation', [rbCode, rbName])
            self.setWindowTitleEx(u'Место нахождения учетного документа')

    def getItemEditor(self):
        return CRBLocationCardTypeEditor(self)


class CRBLocationCardTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbDocumentTypeLocation')
        self.setupUi(self)
        self.setWindowTitleEx(u'Место нахождения учетного документа')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, rbCode )
        setLineEditValue(self.edtName,                record, rbName )
        self.cmbColor.setColor(forceString(record.value('color')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, rbCode )
        getLineEditValue(self.edtName,                record, rbName )
        record.setValue('color',      QVariant(self.cmbColor.colorName()))
        return record
