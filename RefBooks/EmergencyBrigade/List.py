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

from library.InDocTable      import CInDocTableModel, CRBInDocTableCol
from library.interchange     import getLineEditValue, setLineEditValue, setDateEditValue, getDateEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CDateCol

from RefBooks.Tables import rbCode, rbCodeRegional, rbEmergencyBrigade, rbName

from .Ui_RBEmergencyBrigade import Ui_ItemEditorDialog


class CRBEmergencyBrigadeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                [rbCode], 20),
            CTextCol(u'Региональный код',   [rbCodeRegional], 20),
            CTextCol(u'Наименование',       [rbName], 40),
            CDateCol(u'Начало действия',    ['begDate'], 20),
            CDateCol(u'Окончание действия', ['endDate'], 20),
            ], rbEmergencyBrigade, [rbCode, rbName])
        self.setWindowTitleEx(u'Бригады')


    def getItemEditor(self):
        return CRBEmergencyBrigadeEditor(self)

#
# ##########################################################################
#

class CRBEmergencyBrigadeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbEmergencyBrigade)
        self.setupUi(self)
        self.setWindowTitleEx(u'Бригада')
        self.setupDirtyCather()
        self.addModels('PersonnelBrigade',  CPersonnelBrigadeModel(self))
        self.setModels(self.tblPersonnelBrigade, self.modelPersonnelBrigade, self.selectionModelPersonnelBrigade)
        self.tblPersonnelBrigade.addMoveRow()
        self.tblPersonnelBrigade.popupMenu().addSeparator()
        self.tblPersonnelBrigade.addPopupDelRow()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,         record, rbCode)
        setLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        setLineEditValue(self.edtName,         record, rbName)
        setDateEditValue(self.edtBegDate,      record, 'begDate')
        setDateEditValue(self.edtEndDate,      record, 'endDate')
        self.modelPersonnelBrigade.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,         record, rbCode)
        getLineEditValue(self.edtRegionalCode, record, rbCodeRegional)
        getLineEditValue(self.edtName,         record, rbName)
        getDateEditValue(self.edtBegDate,      record, 'begDate')
        getDateEditValue(self.edtEndDate,      record, 'endDate')
        return record


    def saveInternals(self, id):
        self.modelPersonnelBrigade.saveItems(id)


class CPersonnelBrigadeModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'EmergencyBrigade_Personnel', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'ФИО', 'person_id', 10, 'vrbPersonWithSpeciality', preferredWidth=150))
