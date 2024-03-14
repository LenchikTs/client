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
#TODO: нужно более простое и ясное название таблицы чем rbDocumentTypeForTracking


from library.interchange     import getCheckBoxValue, getLineEditValue, setCheckBoxValue, setLineEditValue, setRBComboBoxValue, getRBComboBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CBoolCol, CTextCol

from RefBooks.Tables import rbCode, rbName

from .Ui_RBDocumentTypeForTracking import Ui_ItemEditorDialog


class CRBDocumentTypeForTrackingList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 20),
            CBoolCol(u'Отображение', ['showInClientInfo'], 10)
            ], 'rbDocumentTypeForTracking', [rbCode, rbName])
        self.setWindowTitleEx(u'Виды учётных документов')

    def getItemEditor(self):
        return CRBDocumentTypeForTrackingEditor(self)

#
# ##########################################################################
#

class CRBDocumentTypeForTrackingEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbDocumentTypeForTracking')
        self.setupUi(self)
        self.setWindowTitleEx(u'Вид учётного документа')
        self.setupDirtyCather()
        self.cmbCounter.setTable('rbCounter')
        self.cmbCounter.setCurrentIndex(0)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,  record, rbCode)
        setLineEditValue(   self.edtName,  record, rbName)
        setCheckBoxValue( self.chkShowInClientInfo, record, 'showInClientInfo')
        setRBComboBoxValue(self.cmbCounter, record, 'counter_id')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,  record, rbCode)
        getLineEditValue(   self.edtName,  record, rbName)
        getCheckBoxValue( self.chkShowInClientInfo, record, 'showInClientInfo')
        getRBComboBoxValue(self.cmbCounter, record, 'counter_id')
        return record
