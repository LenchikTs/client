# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import QVariant

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CColorCol, CTextCol
from library.Utils           import forceString, forceInt
from RefBooks.Tables         import rbCode, rbName

from Ui_RBStatusObservationClientEditor import Ui_ItemEditorDialog


class CRBStatusObservationClientTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CColorCol(u'Цветовая маркировка', ['color'], 10, 'r')
            ], 'rbStatusObservationClientType', [rbCode, rbName]) #WTF? rbClientOrservationStatus !!!
        self.setWindowTitleEx(u'Статусы наблюдения пациента')

    def getItemEditor(self):
        return CRBStatusObservationClientEditor(self)

#
# ##########################################################################
#

class CRBStatusObservationClientEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbStatusObservationClientType')
        self.setupUi(self)
        self.setWindowTitleEx(u'Статус наблюдения пациента')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, rbCode)
        setLineEditValue(self.edtName, record, rbName)
        self.cmbColor.setColor(forceString(record.value('color')))
        self.cmbRemoveStatus.setCurrentIndex(forceInt(record.value('removeStatus')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, rbCode)
        getLineEditValue(self.edtName, record, rbName)
        record.setValue('color', QVariant(self.cmbColor.colorName()))
        record.setValue('removeStatus', QVariant(self.cmbRemoveStatus.currentIndex()))
        return record
