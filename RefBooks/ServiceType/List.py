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


from library.interchange     import getComboBoxValue, getLineEditValue, getRBComboBoxValue, getTextEditValue, setComboBoxValue, setLineEditValue, setRBComboBoxValue, setTextEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CEnumCol, CRefBookCol, CTextCol
from library.Utils           import forceString

from RefBooks.Tables         import rbCode, rbName, rbServiceGroup, rbServiceType

from Ui_RBServiceTypeEditor  import Ui_ItemEditorDialog



class CRBServiceTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(   u'Раздел', ['section'], 4),
            CTextCol(   u'Код',         [rbCode], 4),
            CTextCol(   u'Наименование',[rbName], 50),
            CTextCol(   u'Описание', ['description'], 50),
            CEnumCol(   u'Класс', ['class'], [u'статус', u'диагностика', u'лечение', u'прочие'], 10),
            CRefBookCol(u'Группа', ['group_id'], rbServiceGroup, 20)
            ], rbServiceType, ['section', 'code'])
        self.setWindowTitleEx(u'Типы номенклатурных услуг')


    def getItemEditor(self):
        return CRBServiceTypeEditor(self)

#
# ##########################################################################
#

class CRBServiceTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):

    mapSectionToIndex = { u'A': 0, # lat A
                          u'B': 1, # lat B
                          u'D': 2,
                          u'F': 3,
                          u'А': 0, # rus A
                          u'В': 1, # rus V
                          u'Д': 2,
                          u'Ф': 3,
                        }

    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbServiceType)
        self.setupUi(self)
        self.cmbGroup.setTable(rbServiceGroup)
        self.setWindowTitleEx(u'Тип номенклатурной услуги')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        section = forceString(record.value('section'))
        sectionIndex = self.mapSectionToIndex.get(section, 0)
        self.cmbSection.setCurrentIndex(sectionIndex)
        setLineEditValue(self.edtCode,                record, rbCode)
        setLineEditValue(self.edtName,                record, rbName)
        setTextEditValue(self.txtDescription,         record, 'description')
        setComboBoxValue(self.cmbClass,               record, 'class')
        setRBComboBoxValue(self.cmbGroup,             record, 'group_id')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('section', self.cmbSection.currentText()[0])
        getLineEditValue(self.edtCode,                record, rbCode)
        getLineEditValue(self.edtName,                record, rbName)
        getTextEditValue(self.txtDescription,         record, 'description')
        getComboBoxValue(self.cmbClass,               record, 'class')
        getRBComboBoxValue(self.cmbGroup,             record, 'group_id')
        return record
