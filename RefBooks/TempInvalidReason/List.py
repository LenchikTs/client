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

from library.interchange     import getCheckBoxValue, getComboBoxValue, getSpinBoxValue, setCheckBoxValue, setComboBoxValue, setSpinBoxValue
from library.ItemsListDialog import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel      import CBoolCol, CEnumCol, CNumCol, CTextCol

from RefBooks.Tables import rbCode, rbName, rbTempInvalidReason, TempInvalidTypeList

from .Ui_RBTempInvalidReasonEditor import Ui_ItemEditorDialog


class CRBTempInvalidReasonList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CEnumCol(u'Класс',                   ['type'], TempInvalidTypeList, 10),
            CTextCol(u'Код',                     [rbCode], 10),
            CTextCol(u'Наименование',            [rbName], 30),
            CBoolCol(u'В Б/Л требуется диагноз', ['requiredDiagnosis'], 10),
            CEnumCol(u'Группа',                  ['grouping'], [u'заболевание', u'уход', u'беременность и роды'], 30),
            CNumCol(u'максимальная длительность первичного периода ВУТ в днях', ['primary'], 10),
            CNumCol(u'максимальная длительность продления ВУТ в днях', ['prolongate'], 10),
            CNumCol(u'ограничение периода ВУТ, после которого требуется КЭК', ['restriction'], 10),
            ], rbTempInvalidReason, ['type', rbCode, rbName])
        self.setWindowTitleEx(u'Причины ВУТ, инвалидности или ограничения жизнедеятельности')

    def getItemEditor(self):
        return CRBTempInvalidReasonEditor(self)
#
# ##########################################################################
#

class CRBTempInvalidReasonEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, rbTempInvalidReason)
        self.setWindowTitleEx(u'Причина ВУТ, инвалидности или ограничения жизнедеятельности')
        self.cmbType.addItems(TempInvalidTypeList)
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setComboBoxValue(self.cmbType, record, 'type')
        setCheckBoxValue(self.checkBox, record, 'requiredDiagnosis')
        setComboBoxValue(self.cmbGrouping, record, 'grouping')
        setSpinBoxValue(self.spinPrimary, record, 'primary')
        setSpinBoxValue(self.spinProlongate, record, 'prolongate')
        setSpinBoxValue(self.spinRestriction, record, 'restriction')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getComboBoxValue(self.cmbType, record, 'type')
        getCheckBoxValue(self.checkBox, record, 'requiredDiagnosis')
        getComboBoxValue(self.cmbGrouping, record, 'grouping')
        getSpinBoxValue(self.spinPrimary, record, 'primary')
        getSpinBoxValue(self.spinProlongate, record, 'prolongate')
        getSpinBoxValue(self.spinRestriction, record, 'restriction')
        return record
