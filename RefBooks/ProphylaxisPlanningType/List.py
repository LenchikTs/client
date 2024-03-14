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

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CTextCol
from library.interchange     import setSpinBoxValue, getSpinBoxValue
from RefBooks.Tables         import rbCode, rbName

from .Ui_RBProphylaxisPlanningTypeEditor import Ui_ItemEditorDialog


class CRBProphylaxisPlanningType(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                 [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CTextCol(u'Дни до',            ['daysBefore'], 4),
            CTextCol(u'Дни после',       ['daysAfter'], 4),
            ], 'rbProphylaxisPlanningType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы планирования профилактики')


    def getItemEditor(self):
        return CRBProphylaxisPlanningTypeEditor(self)


#
# ##########################################################################
#


class CRBProphylaxisPlanningTypeEditor(Ui_ItemEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbProphylaxisPlanningType')
        self.setWindowTitleEx(u'Тип планирования профилактики')


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setSpinBoxValue( self.edtDaysBefore, record, 'daysBefore')
        setSpinBoxValue( self.edtDaysAfter, record, 'daysAfter')


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getSpinBoxValue( self.edtDaysBefore, record, 'daysBefore')
        getSpinBoxValue( self.edtDaysAfter, record, 'daysAfter')
        return record

