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

from library.interchange     import getLineEditValue, setLineEditValue, setDateEditValue, getDateEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CDateCol
from library.AgeSelector     import composeAgeSelector, parseAgeSelector
from library.Utils           import forceString, forceStringEx, toVariant

from RefBooks.Tables import rbCode, rbName, rbBegDate, rbEndDate, rbAge

from Ui_RBDiet import Ui_RBDiet


class CRBDiet(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',            [rbCode],    20),
            CTextCol(u'Наименование',   [rbName],    40),
            CDateCol(u'Дата начала',    [rbBegDate], 20),
            CDateCol(u'Дата окончания', [rbEndDate], 20),
            CTextCol(u'Возраст',        ['age'],     10)
            ], 'rbDiet', [rbCode, rbName, rbBegDate, rbEndDate, rbAge])
        self.setWindowTitleEx(u'Столы питания')

    def getItemEditor(self):
        return CRBDietEditor(self)

#
# ##########################################################################
#

class CRBDietEditor(CItemEditorBaseDialog, Ui_RBDiet):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbDiet')
        self.setupUi(self)
        self.setWindowTitleEx(u'Стол питания')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, rbCode)
        setLineEditValue(self.edtName, record, rbName)
        setDateEditValue(self.edtBegDate, record, rbBegDate)
        setDateEditValue(self.edtEndDate, record, rbEndDate)
        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(forceString(record.value('age')))
        self.cmbBegAgeUnit.setCurrentIndex(begUnit)
        self.edtBegAgeCount.setText(str(begCount))
        self.cmbEndAgeUnit.setCurrentIndex(endUnit)
        self.edtEndAgeCount.setText(str(endCount))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, rbCode)
        getLineEditValue(self.edtName, record, rbName)
        getDateEditValue(self.edtBegDate, record, rbBegDate)
        getDateEditValue(self.edtEndDate, record, rbEndDate)
        record.setValue('age',        toVariant(composeAgeSelector(
                    self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
                    self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text())
                        )))
        return record

