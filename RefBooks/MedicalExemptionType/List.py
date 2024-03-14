# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from library.InDocTable      import CRBInDocTableCol, CInDocTableModel
from library.interchange     import getLineEditValue, setLineEditValue
from library.ItemsListDialog import CItemEditorBaseDialog, CItemsListDialog
from library.TableModel      import CRefBookCol, CTableModel, CTextCol
from library.Utils           import forceRef

from RefBooks.Tables         import rbCode, rbName

from .Ui_RBMedicalExemptionTypeItemList import Ui_RBMedicalExemptionTypeItemList
from .Ui_RBMedicalExemptionTypeEditor   import Ui_RBMedicalExemptionTypeEditor


class CRBMedicalExemptionTypeList(Ui_RBMedicalExemptionTypeItemList, CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbMedicalExemptionType', [rbCode, rbName])

        self.tblItems.addPopupDelRow()
        self.setWindowTitleEx(u'Типы медотводов')


    def getItemEditor(self):
        return CRBMedicalExemptionTypeEditor(self)


    def setup(self, *args, **kw):
        self.addModels('MedicalExemptionTypeInfections', 
                       CTableModel(self,
                                  [ CRefBookCol(u'Инфекция', ['infection_id'], 'rbInfection', 20) ],
                                    u'rbMedicalExemptionType_Infection')
                      )

        CItemsListDialog.setup(self, *args, **kw)


        self.setModels(self.tblMedicalExemptionTypeInfections,
                       self.modelMedicalExemptionTypeInfections,
                       self.selectionModelMedicalExemptionTypeInfections)

        self.connect(self.selectionModel,
                     SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
                     self.on_selectionModel_currentChanged)


    def getIdByRow(self, row):
        if 0 <= row < self.model.rowCount():
            return self.model.idList()[row]
        return None


    def on_selectionModel_currentChanged(self, current, previous):
        itemId = self.getIdByRow(current.row())
        if itemId:
            db = QtGui.qApp.db

            tableMedicalExemptionTypeInfection = db.table('rbMedicalExemptionType_Infection')
            idList = db.getIdList(tableMedicalExemptionTypeInfection, 'id',
                                  tableMedicalExemptionTypeInfection['master_id'].eq(itemId), 'id')
            self.modelMedicalExemptionTypeInfections.setIdList(idList)

#
# ##########################################################################
#

class CRBMedicalExemptionTypeEditor(CItemEditorBaseDialog, Ui_RBMedicalExemptionTypeEditor):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbMedicalExemptionType')
        self.addModels('MedicalExemptionTypeInfections', CMedicalExemptionTypeInfectionsModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип медотвода')
        self.setModels(self.tblMedicalExemptionTypeInfections,
                       self.modelMedicalExemptionTypeInfections,
                       self.selectionModelMedicalExemptionTypeInfections)
        self.tblMedicalExemptionTypeInfections.addPopupDelRow()
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,                record, 'code' )
        setLineEditValue(self.edtName,                record, 'name' )
        self.modelMedicalExemptionTypeInfections.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,                record, 'code' )
        getLineEditValue(self.edtName,                record, 'name' )
        return record


    def saveInternals(self, id):
        self.modelMedicalExemptionTypeInfections.saveItems(id)


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
        result = result and self.checkModelMedicalExemptionTypeInfections()
        return result


    def checkModelMedicalExemptionTypeInfections(self):
        for row, item in enumerate(self.modelMedicalExemptionTypeInfections.items()):
            infectionId = forceRef(item.value('infection_id'))
            if not infectionId:
                return self.checkInputMessage(u'инфекцию', False, self.tblMedicalExemptionTypeInfections, row, 0)
        return True



class CMedicalExemptionTypeInfectionsModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbMedicalExemptionType_Infection', 'id', 'master_id',   parent)
        self.addCol(CRBInDocTableCol(  u'Инфекция',     'infection_id',    20,   'rbInfection'))
