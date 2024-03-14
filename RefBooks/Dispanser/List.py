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

from library.interchange     import getCheckBoxValue, getLineEditValue, setCheckBoxValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.TableModel      import CBoolCol, CTextCol

from RefBooks.Tables import rbCode, rbDispanser, rbName

from .Ui_RBDispanserEditor import Ui_ItemEditorDialog


class CRBDispanserList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CBoolCol(u'Наблюдается',  ['observed'], 10),
            ], rbDispanser, [rbCode, rbName])
        self.setWindowTitleEx(u'Отметки диспансерного наблюдения')

    def getItemEditor(self):
        return CRBDispanserEditor(self)


#
# ##########################################################################
#

class CRBDispanserEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbDispanser)
        self.setWindowTitleEx(u'Отметка диспансерного наблюдения')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        setCheckBoxValue(   self.chkObserved,      record, 'observed')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        getCheckBoxValue(   self.chkObserved,      record, 'observed')
        return record
