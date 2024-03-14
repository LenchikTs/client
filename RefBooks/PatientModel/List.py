# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

from library.InDocTable      import CInDocTableModel
from library.interchange     import getLineEditValue, getRBComboBoxValue, getDateEditValue, setLineEditValue, setRBComboBoxValue, setDateEditValue
from library.ItemsListDialog import CItemEditorBaseDialog, CRBItemsSplitListDialogEx
from library.TableModel      import CRefBookCol, CTextCol, CDateCol

from RefBooks.Tables         import rbCode, rbName, rbPatientModel
from Ui_RBPatientModelEditor import Ui_ItemEditorDialog
from PatientsModelComboBox   import CPatientsModelTableCol


class CRBPatientModel(CRBItemsSplitListDialogEx):
    def __init__(self, parent):
        CRBItemsSplitListDialogEx.__init__(self, parent, rbPatientModel, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 20),
            CTextCol(u'Диагноз', ['MKB'], 20),
            CRefBookCol(u'Вид ВТМП', ['quotaType_id'], 'QuotaType', 40),
            CDateCol(u'Дата окончания действия', ['endDate'],  10),
            ],
            [rbCode, rbName],
            'rbPatientModel_Item',
            [
            CRefBookCol(u'Вид лечения', ['cureType_id'], 'rbCureType', 40),
            CRefBookCol(u'Метод лечения', ['cureMethod_id'], 'rbCureMethod', 40)
            ],
            'master_id', 'id'
            )
        self.setWindowTitleEx(u'Модели пациента')


    def getItemEditor(self):
        return CRBPatientModelEditor(self)


    def select(self, props={}):
        table = self.model.table()
        return QtGui.qApp.db.getIdList(table.name(), 'id')

#
# ##########################################################################
#

class CRBPatientModelEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbPatientModel)
        self.addModels('TypeMetodCure', CTypeMetodCureModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Модель пациента')
        self.setModels(self.tblItems, self.modelTypeMetodCure, self.selectionModelTypeMetodCure)
        self.tblItems.addMoveRow()
        self.tblItems.addPopupDelRow()
        self.setupDirtyCather()
        self.edtEndDate.canBeEmpty()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,        record, 'code')
        setLineEditValue(self.edtName,        record, 'name')
        setLineEditValue(self.edtMKB,         record, 'MKB')
        setRBComboBoxValue(self.cmbQuotaType, record, 'quotaType_id')
        setDateEditValue(self.edtEndDate,     record, 'endDate')
        self.modelTypeMetodCure.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,        record, 'code')
        getLineEditValue(self.edtName,        record, 'name')
        getLineEditValue(self.edtMKB,         record, 'MKB')
        getRBComboBoxValue(self.cmbQuotaType, record, 'quotaType_id')
        getDateEditValue(self.edtEndDate,     record, 'endDate')
        return record


    def saveInternals(self, id):
        self.modelTypeMetodCure.saveItems(id)


class CTypeMetodCureModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbPatientModel_Item', 'id', 'master_id', parent)
        self.addCol(CPatientsModelTableCol(u'Вид лечения',   'cureType_id',   20, 'rbCureType'))
        self.addCol(CPatientsModelTableCol(u'Метод лечения', 'cureMethod_id', 20, 'rbCureMethod'))
