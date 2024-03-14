# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Поддержка таблицы клиентов сервиса самозаписи: квоты и типы финансирования
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature


from library.interchange     import ( getCheckBoxValue,
                                      getLineEditValue,
                                      getSpinBoxValue,
                                      setCheckBoxValue,
                                      setLineEditValue,
                                      setSpinBoxValue,
                                    )
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol, CBoolCol, CIntCol
from library.InDocTable      import ( CInDocTableModel,
#                                      CInDocTableCol,
#                                      CEnumInDocTableCol,
                                      CRBInDocTableCol,
                                    )
from library.crbcombobox     import CRBComboBox


from Ui_SRSUserEditor import Ui_ItemEditorDialog


class CSRSUserList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          ['code'],     40),
            CTextCol(u'Роль',         ['position'], 40),
            CTextCol(u'Наименование', ['name'],     40),
            CBoolCol(u'Локальный',    ['isLocal'],  6),
            CIntCol(u'Квота',         ['quota'],  6),

            ], 'SRSUser', ['name'])
        self.setWindowTitleEx(u'Ограничения пользователей сервиса самозаписи N3.СЗнПВ')
        self.tblItems.createPopupMenu([self.actDuplicate, '-', self.actDelete])


    def preSetupUi(self):
        CItemsListDialog.preSetupUi(self)
        self.addObject('actDuplicate', QtGui.QAction(u'Дублировать', self))
        self.addObject('actDelete',    QtGui.QAction(u'Удалить', self))


    def copyInternals(self, newItemId, oldItemId):
        for tableName in ( 'SRSUser_AvailableFinance',
                         ):
            self.copyDependedTableData(tableName,
                                       'master_id',
                                       newItemId,
                                       oldItemId
                                      )


    def getItemEditor(self):
        return CSRSUserEditor(self)


    @pyqtSignature('')
    def on_tblItems_popupMenuAboutToShow(self):
        currentItemId = self.currentItemId()
        self.actDuplicate.setEnabled(bool(currentItemId))
        self.actDelete.setEnabled(bool(currentItemId))


    @pyqtSignature('')
    def on_actDuplicate_triggered(self):
        self.duplicateCurrentRow()


    @pyqtSignature('')
    def on_actDelete_triggered(self):
        def deleteCurrentInternal():
            currentItemId = self.currentItemId()
            if currentItemId:
                row = self.tblItems.currentIndex().row()
                db = QtGui.qApp.db
                table = db.table('SRSUser')
                db.deleteRecord(table, table['id'].eq(currentItemId))
                self.renewListAndSetTo()
                self.tblItems.setCurrentRow(row)
        QtGui.qApp.call(self, deleteCurrentInternal)


#
# ##########################################################################
#

class CSRSUserEditor(Ui_ItemEditorDialog, CItemEditorBaseDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'SRSUser')
        self.addModels('AvailableFinances', CAvailableFinancesModel(self))

        self.setupUi(self)
        self.setWindowTitleEx(u'Ограничения пользователя сервиса самозаписи N3.СЗнПВ')

        self.setModels(self.tblAvailableFinances, self.modelAvailableFinances, self.selectionModelAvailableFinances)
        self.tblAvailableFinances.addPopupDelRow()
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue( self.edtCode,              record, 'code')
        setLineEditValue( self.edtPosition,          record, 'position')
        setLineEditValue( self.edtName,              record, 'name')
        setCheckBoxValue( self.chkIsLocal,           record, 'isLocal')
        setSpinBoxValue(self.edtQuota,               record, 'quota')

        self.modelAvailableFinances.loadItems(self.itemId())
        pass


    def checkDataEntered(self):
        return True


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue( self.edtCode,              record, 'code')
        getLineEditValue( self.edtPosition,          record, 'position')
        getLineEditValue( self.edtName,              record, 'name')
        getCheckBoxValue( self.chkIsLocal,           record, 'isLocal')
        getSpinBoxValue(self.edtQuota,               record, 'quota')
        return record


    def saveInternals(self, id):
        self.modelAvailableFinances.saveItems(id)


class CAvailableFinancesModel(CInDocTableModel):

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'SRSUser_AvailableFinance', 'id', 'master_id', parent)
#        self.setEnableAppendLine(True)
        self.addCol(CRBInDocTableCol(u'Тип финансирования', 'finance_id', 20, 'rbFinance', showFields = CRBComboBox.showName))
