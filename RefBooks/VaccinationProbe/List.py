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

from library.AgeSelector     import composeAgeSelector, parseAgeSelector
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.interchange     import getLineEditValue, getRBMultivalueComboBoxValue, setLineEditValue, setRBMultivalueComboBoxValue
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog
from library.TableModel      import CTextCol
from library.Utils           import forceString, forceStringEx, toVariant

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBVaccinationProbeEditor import Ui_RBVaccinationProbeEditor


class CRBVaccinationProbeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                  [rbCode], 20),
            CTextCol(u'Наименование',         [rbName], 40),
            CTextCol(u'Возраст',              ['age'], 20), 
            CTextCol(u'Минимальный срок',     ['minimumTerm'], 20), 
            CTextCol(u'Срок действия',        ['duration'], 20), 
            CTextCol(u'Инфекции',             ['infections'], 20), 
            CTextCol(u'Тип прививки',         ['vaccinationType'], 20)
            ], 'rbVaccinationProbe', [rbCode, rbName])

        self.tblItems.addPopupDelRow()
        self.setWindowTitleEx(u'Пробы')


    def getItemEditor(self):
        return CRBVaccinationProbeEditor(self)


#
# ##########################################################################
#

class CRBVaccinationProbeEditor(Ui_RBVaccinationProbeEditor, CItemEditorDialogWithIdentification):
    def __init__(self, parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'rbVaccinationProbe')
        # self.setupUi(self)
        self.cmbInfections.setTable(u'rbInfection')
        self.setWindowTitleEx(u'Проба')


    def setRecord(self, record):
        CItemEditorDialogWithIdentification.setRecord(self, record)
        setLineEditValue(self.edtCode,                   record, 'code' )
        setLineEditValue(self.edtName,                   record, 'name' )

        (begAgeUnit, begAgeCount, endAgeUnit, endAgeCount) = parseAgeSelector(forceString(record.value('age')))
        self.cmbBegAgeUnit.setCurrentIndex(begAgeUnit)
        self.edtBegAgeCount.setText(str(begAgeCount))
        self.cmbEndAgeUnit.setCurrentIndex(endAgeUnit)
        self.edtEndAgeCount.setText(str(endAgeCount))

        minimumTermValues = parseAgeSelector(forceString(record.value('minimumTerm')))
        (begMinimumTermUnit, begMinimumTermCount, endMinimumTermUnit, endMinimumTermCount) = minimumTermValues
        self.cmbMinimumTermUnit.setCurrentIndex(begMinimumTermUnit)
        self.edtMinimumTermCount.setText(str(begMinimumTermCount))

        durationValues = parseAgeSelector(forceString(record.value('duration')))
        (begDurationUnit, begDurationCount, endDurationUnit, endDurationCount) = durationValues
        self.cmbDurationUnit.setCurrentIndex(endDurationUnit)
        self.edtDurationCount.setText(str(endDurationCount))

        setRBMultivalueComboBoxValue(self.cmbInfections, record, 'infections' )
        setLineEditValue(self.edtVaccinationType,        record, 'vaccinationType' )



    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                   record, 'code' )
        getLineEditValue(self.edtName,                   record, 'name' )

        record.setValue('age',         toVariant(composeAgeSelector(
                    self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
                    self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text())
                        )))

        record.setValue('minimumTerm', toVariant(composeAgeSelector(
                    self.cmbMinimumTermUnit.currentIndex(),  forceStringEx(self.edtMinimumTermCount.text()),
                    0,  0
                        )))

        record.setValue('duration',    toVariant(composeAgeSelector(
                    0,  0, 
                    self.cmbDurationUnit.currentIndex(),  forceStringEx(self.edtDurationCount.text())
                        )))


        getRBMultivalueComboBoxValue(self.cmbInfections, record, 'infections' )
        getLineEditValue(self.edtVaccinationType,        record, 'vaccinationType' )
        return record
