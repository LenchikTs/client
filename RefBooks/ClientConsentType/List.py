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

from library.interchange     import getCheckBoxValue, getComboBoxValue, getLineEditValue, getSpinBoxValue, setCheckBoxValue, setComboBoxValue, setLineEditValue, setSpinBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CBoolCol, CEnumCol, CNumCol, CTextCol

from RefBooks.Tables         import rbCode, rbName


from .Ui_RBClientConsentTypeEditor import Ui_RBClientConsentTypeEditor


class CRBClientConsentTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                     [rbCode],                                    20),
            CTextCol(u'Наименование',            [rbName],                                    40),
            CEnumCol(u'Срочность',               ['periodFlag'], [u'Бессрочное', u'Срочное'], 10),
            CNumCol(u'Срок действия',            ['defaultPeriod'],                           10),
            CBoolCol(u'Визуализация в блоке информации о пациенте', ['inClientInfoBrowser'],  15)
            ], 'rbClientConsentType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы согласия пациента')


    def getItemEditor(self):
        return CRBAgreementTypeEditor(self)


#
# ##########################################################################
#

class CRBAgreementTypeEditor(CItemEditorBaseDialog, Ui_RBClientConsentTypeEditor):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbClientConsentType')
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип согласия пациента')


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, 'code')
        setLineEditValue(self.edtName,                record, 'name')
        setComboBoxValue(self.cmbPeriodFlag,          record, 'periodFlag')
        setSpinBoxValue(self.edtDefaultPeriod,        record, 'defaultPeriod')
        setCheckBoxValue(self.chkInClientInfoBrowser, record, 'inClientInfoBrowser')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, 'code')
        getLineEditValue(self.edtName,                record, 'name')
        getComboBoxValue(self.cmbPeriodFlag,          record, 'periodFlag')
        getSpinBoxValue(self.edtDefaultPeriod,        record, 'defaultPeriod')
        getCheckBoxValue(self.chkInClientInfoBrowser, record, 'inClientInfoBrowser')
        return record
