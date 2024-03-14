# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import QVariant
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.Utils import forceInt
from library.interchange import setDateEditValue, getDateEditValue, setDoubleBoxValue
from library.ItemsListDialog import CItemsListDialog
from library.TableModel import CTextCol, CDateCol, CCol
from RefBooks.Tables import rbCode, rbHealthGroup, rbName, rbBegDate, rbEndDate

from .Ui_RBHealthGroupEditor import Ui_ItemEditorDialog


class CRBHealthGroupList(CItemsListDialog):
    class CLocAgeColumn(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            ageFrom = forceInt(values[0])
            ageTo = forceInt(values[1])
            if ageFrom or ageTo:
                return u'{0}-{1}'.format(u'%sг' % ageFrom if ageFrom else '', u'%sг' % ageTo if ageTo else '')
            return CCol.invalid


    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',            [rbCode],    20),
            CTextCol(u'Наименование',   [rbName],    40),
            CDateCol(u'Дата начала',    [rbBegDate], 20),
            CDateCol(u'Дата окончания', [rbEndDate], 20),
            CRBHealthGroupList.CLocAgeColumn(u'Возраст', ['ageFrom', 'ageTo'], 10)
        ], rbHealthGroup, [rbCode, rbName, rbBegDate, rbEndDate, 'ageFrom', 'ageTo'])
        self.setWindowTitleEx(u'Группы здоровья')


    def getItemEditor(self):
        return CRBHealthGroupEditor(self)


class CRBHealthGroupEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbHealthGroup)
        self.setWindowTitleEx(u'Группа здоровья')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setDateEditValue(self.edtBegDate, record, 'begDate')
        setDateEditValue(self.edtEndDate, record, 'endDate')
        setDoubleBoxValue(self.edtAgeFrom, record, 'ageFrom')
        setDoubleBoxValue(self.edtAgeTo, record, 'ageTo')
        

    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getDateEditValue(self.edtBegDate, record, 'begDate')
        getDateEditValue(self.edtEndDate, record, 'endDate')
        record.setValue('ageFrom', QVariant(self.edtAgeFrom.value() if self.edtAgeFrom.value() > 0 else None))
        record.setValue('ageTo', QVariant(self.edtAgeTo.value() if self.edtAgeTo.value() > 0 else None))
        return record
