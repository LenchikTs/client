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

from PyQt4 import QtGui

from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CTextCol
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from RefBooks.Tables         import rbCode, rbContactType, rbName

from Ui_RBContactTypeEditor import Ui_ContactTypeEditorDialog

class CLocValidator(QtGui.QRegExpValidator):
    def __init__(self, parent):
        QtGui.QRegExpValidator.__init__(self, parent=parent)


class CRBContactTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], rbContactType, [rbCode, rbName])
        self.setWindowTitleEx(u'Способы связи с пациентом')

    def getItemEditor(self):
        return CRBContactTypeListEditor(self)

#
# ##########################################################################
#

class CRBContactTypeListEditor(Ui_ContactTypeEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbContactType)
        self.setWindowTitleEx(u'Способ связи с пациентом')
#        self.idValidator = CLocValidator(self)
#        self.edtRegExpValidator.setValidator(self.idValidator)


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtRegExpValidator, record, 'regExpValidator')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getLineEditValue(self.edtRegExpValidator, record, 'regExpValidator')
        return record

