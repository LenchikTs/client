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

from library.interchange     import getCheckBoxValue, getComboBoxValue, getRBComboBoxValue, setCheckBoxValue, setComboBoxValue, setRBComboBoxValue
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.ItemsListDialog import CItemsListDialog
from library.TableModel      import CBoolCol, CEnumCol, CTextCol

from .Ui_RBTissueTypeEditor import Ui_TissueTypeEditorDialog


class CRBTissueTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',            ['code'],   10),
            CTextCol(u'Наименование',   ['name'],   30),
            CEnumCol(u'Пол',            ['sex'], [u'Любой', u'М', u'Ж'], 5),
            CBoolCol(u'Ручной ввод идентификатора',    ['counterManualInput'], 15),
            CEnumCol(u'Период уникальности идентификатора', ['counterResetType'], [u'День', u'Неделя',
                                                               u'Месяц', u'Полгода', u'Год', u'Постоянно'], 15)
            ], 'rbTissueType', ['code', 'name'])
        self.setWindowTitleEx(u'Типы биоматериалов')

    def getItemEditor(self):
        return CRBTissueTypeListEditor(self)

# ###################################################


class CRBTissueTypeListEditor(Ui_TissueTypeEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbTissueType')
        self.setWindowTitleEx(u'Тип биоматериала')
        self.cmbCounter.setTable('rbCounter')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setComboBoxValue(self.cmbSex,                  record, 'sex')
        setCheckBoxValue(self.chkCounterManualInput,   record, 'counterManualInput')
        setComboBoxValue(self.cmbCounterResetType,     record, 'counterResetType')
        setCheckBoxValue(self.chkIsRealTimeProcessing, record, 'isRealTimeProcessing')
        setRBComboBoxValue(self.cmbCounter,            record, 'counter_id')


    def getRecord(self):
        record = CItemEditorDialogWithIdentification.getRecord(self)
        getComboBoxValue(self.cmbSex,                  record, 'sex')
        getCheckBoxValue(self.chkCounterManualInput,   record, 'counterManualInput')
        getComboBoxValue(self.cmbCounterResetType,     record, 'counterResetType')
        getCheckBoxValue(self.chkIsRealTimeProcessing, record, 'isRealTimeProcessing')
        if self.cmbCounter.isEnabled():
            getRBComboBoxValue(self.cmbCounter,        record, 'counter_id')
        else:
            record.setValue('counter_id',  None)
        return record

