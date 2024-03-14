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
from PyQt4.QtCore import Qt, pyqtSignature
from PyQt4 import QtGui

from library.interchange     import ( setLineEditValue,
                                      setDateEditValue,
                                      getLineEditValue,
                                      getDateEditValue,
                                      setRBComboBoxValue, 
                                      getRBComboBoxValue
                                    )
from library.ItemsListDialog import CItemEditorBaseDialog
from library.Utils           import forceDate, forceStringEx
from library.crbcombobox import CRBComboBox

from Accounting.Ui_AccountEditDialog import Ui_AccountEditDialog


class CAccountEditDialog(CItemEditorBaseDialog, Ui_AccountEditDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'Account')
        self.setupUi(self)
        self.setupDirtyCather()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Счет')
        self.finance_id = parent.currentFinanceId
        self.cmbAccountType.setShowFields(CRBComboBox.showCodeAndName)
        self.cmbAccountType.setTable('rbAccountType')
       

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtNumber,      record, 'number')
        setRBComboBoxValue(self.cmbAccountType, record, 'type_id')
        setDateEditValue(self.edtDate,        record, 'date')
        setDateEditValue(self.edtExposeDate,  record, 'exposeDate')
        setLineEditValue(self.edtNote,        record, 'note')
        setDateEditValue(self.edtPrivateDate, record, 'personalDate')
        self.applyFinanceFilter()
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtNumber,      record, 'number')
        getDateEditValue(self.edtDate,        record, 'date')
        getRBComboBoxValue(self.cmbAccountType, record, 'type_id')
        getDateEditValue(self.edtExposeDate,  record, 'exposeDate')
        getLineEditValue(self.edtNote,        record, 'note')
        getDateEditValue(self.edtPrivateDate, record, 'personalDate')
        return record


    def checkDataEntered(self):
        result = True
        number = forceStringEx(self.edtNumber.text())
        result = result and (number or self.checkInputMessage(u'Номер', False, self.edtNumber))
        return result
        
        
    def applyFinanceFilter(self):
        db = QtGui.qApp.db
        tableRbAccountType = db.table('rbAccountType')
        cond = []
        if self.finance_id:
            cond.append(tableRbAccountType['finance_id'].eq(self.finance_id))
        if self.edtDate.date():
            cond.append('begDate<= {0:s} and endDate >= {0:s}'.format(db.formatDate(forceDate(self.edtDate.date()))))
        filter = db.joinAnd(cond)
        tmp = self.cmbAccountType.getValue()
        self.cmbAccountType.setFilter(filter, order='code asc')
        self.cmbAccountType.setValue(tmp)
        
        
    @pyqtSignature('QDate')
    def on_edtDate_dateChanged(self, date):
        self.applyFinanceFilter()
