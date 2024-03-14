# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore            import QVariant

from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel      import CColorCol, CTextCol
from library.Utils           import forceString

from RefBooks.Tables         import rbCode, rbName

from .Ui_TreatmentTypeEditor import Ui_TreatmentTypeEditor


class CTreatmentTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            CColorCol(u'Цветовая маркировка', ['color'], 10, 'r'),
            ], 'TreatmentType', [rbCode, rbName])
        self.setWindowTitleEx(u'Циклы')


    def getItemEditor(self):
        return CTreatmentTypeEditor(self)

#
# ##########################################################################
#


class CTreatmentTypeEditor(Ui_TreatmentTypeEditor, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'TreatmentType')
        self.setWindowTitleEx(u'Цикл')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        self.cmbColor.setColor(forceString(record.value('color')))


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        record.setValue('color', QVariant(self.cmbColor.colorName()))
        return record

