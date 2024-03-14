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
from PyQt4.QtCore import SIGNAL

from library.interchange import getLineEditValue,  setLineEditValue, getDateEditValue, setDateEditValue, getRBComboBoxValue, setRBComboBoxValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel import CTextCol, CDateCol, CRefBookCol
from library.Utils import forceInt

from RefBooks.Tables import rbAccountType, rbFinance

from RefBooks.AccountType.Ui_RBAccountTypeEditor import Ui_ItemEditorDialog


class CRBAccountTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код', ['code'], 1),
            CTextCol(u'Региональный код', ['regionalCode'], 1),
            CTextCol(u'Наименование', ['name'], 60),
            CRefBookCol(u'Источник финансирования', ['finance_id'], rbFinance, 20),
            CDateCol(u'Дата начала действия', ['begDate'], 10),
            CDateCol(u'Дата окончания действия', ['endDate'], 10)
            ], rbAccountType, 'code')
        self.setWindowTitleEx(u'Типы реестров счетов')
        self.actDelete = QtGui.QAction(u'Удалить', self)
        self.tblItems.addPopupAction(self.actDelete)
        self.connect(self.actDelete, SIGNAL('triggered()'), self.deleteSelected)
        
    def getItemEditor(self):
        return CRBAccountTypeEditor(self)
        
    def deleteSelected(self):
        db = QtGui.qApp.db
        selectedIdList = self.tblItems.selectedItemIdList()
        for id in selectedIdList:
            query = db.query(u'select count(id) as cnt from Account where type_id = {0:d}'.format(id))
            query.first()
            if forceInt(query.record().value('cnt')):
                QtGui.QMessageBox.warning(self, u'Удаление невозможно!',
                                    u'Тип используется в реестрах счетов.',
                                    QtGui.QMessageBox.Ok,
                                    QtGui.QMessageBox.Ok)
            else:
                if QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                                    u'Вы уверены что хотите удалить тип реестра счетов?',
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                    tableRbAccountType = db.table('rbAccountType')
                    db.deleteRecord(tableRbAccountType, tableRbAccountType['id'].eq(id))
                    self.renewListAndSetTo(None)


class CRBAccountTypeEditor(CItemEditorBaseDialog, Ui_ItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, rbAccountType)
        self.setupUi(self)
        self.setupDirtyCather()
        self.setWindowTitleEx(u'Тип реестра счетов')
        self.cmbFinance.setTable('rbFinance')


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, 'code')
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setLineEditValue(self.edtName, record, 'name')
        setRBComboBoxValue(self.cmbFinance, record, 'finance_id')
        setDateEditValue(self.edtBegDate, record, 'begDate')
        setDateEditValue(self.edtEndDate, record, 'endDate')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode, record, 'code')
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getLineEditValue(self.edtName, record, 'name')
        getRBComboBoxValue(self.cmbFinance, record, 'finance_id')
        getDateEditValue(self.edtBegDate, record, 'begDate')
        getDateEditValue(self.edtEndDate, record, 'endDate')
        return record
