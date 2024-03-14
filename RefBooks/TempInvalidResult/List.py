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

from library.interchange                        import getComboBoxValue, setComboBoxValue
from library.ItemsListDialog                    import CItemsListDialog
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification

from library.TableModel                         import CEnumCol, CTextCol

from RefBooks.Tables                            import rbCode, rbName, TempInvalidTypeList
from RefBooks.TempInvalidState                  import CTempInvalidState


from Ui_RBTempInvalidResultEditor import Ui_ItemEditorDialog


class CRBTempInvalidResultList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CEnumCol(u'Класс',                   ['type'], TempInvalidTypeList, 10),
            CTextCol(u'Код',                     [rbCode], 10),
            CTextCol(u'Наименование',            [rbName], 30),
            CEnumCol(u'Состояние',               ['state'], CTempInvalidState.names, 4),
            CEnumCol(u'Решение',                 ['decision'], [u'', u'Направление на КЭК', u'Решение КЭК', u'Направление на МСЭ', u'Решение МСЭ', u'Госпитализация', u'Сан.кур.лечение'], 30),
            ], 'rbTempInvalidResult', ['type', rbCode, rbName])
        self.setWindowTitleEx(u'Результаты периода ВУТ, инвалидности или ограничения жизнедеятельности')

    def getItemEditor(self):
        return CRBTempInvalidResultEditor(self)
#
# ##########################################################################
#

class CRBTempInvalidResultEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbTempInvalidResult')
        self.setWindowTitleEx(u'Результат периода ВУТ, инвалидности или ограничения жизнедеятельности')
        self.cmbType.addItems(TempInvalidTypeList)


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setComboBoxValue(self.cmbType, record, 'type')
        setComboBoxValue(self.cmbState, record, 'state')
        setComboBoxValue(self.cmbDecision, record, 'decision')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getComboBoxValue(self.cmbType, record, 'type')
        getComboBoxValue(self.cmbState, record, 'state')
        getComboBoxValue(self.cmbDecision, record, 'decision')
        return record
