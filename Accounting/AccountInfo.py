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

from RefBooks.Service.Info import CServiceInfo
from RefBooks.AccountExportFormat.Info import CAccountExportFormatInfo


from Events.Utils          import CCSGInfo
from Orgs.Utils            import COrgInfo, COrgStructureInfo
from library.PrintInfo     import CInfo, CInfoList, CDateInfo, CRBInfo
from library.Utils         import forceString, forceDouble, forceRef, forceDate, forceInt

import json

__all__ = [ 'CAccountItemInfo',
            'CAccountInfo',
            'CAccountInfoList',
          ]

class CRBMedicalAidUnitInfo(CRBInfo):
    tableName = 'rbMedicalAidUnit'


class CRBPayRefuseTypeInfo(CRBInfo):
    tableName = 'rbPayRefuseType'


class CAccountItemInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self._preexposeItem = None

    def getPreexposeItem(self):
        if not self._preexposeItem:
            db = QtGui.qApp.db
            tableAI = db.table('Account_Item')
            cond = [tableAI['reexposeItem_id'].eq(self.id)]
            record = db.getRecordEx(tableAI, [tableAI['id']], cond)
            if record:
                self._preexposeItem = self.getInstance(CAccountItemInfo, forceRef(record.value('id')))
        return self._preexposeItem


    def _load(self):
        from Events.EventInfo  import CVisitInfo, CEmergencyEventInfo
        from Events.ActionInfo import CActionInfo

        db = QtGui.qApp.db
        record = db.getRecord('Account_Item', '*', self.id)
        if record:
            result = True
        else:
            record = db.table('Account_Item').newRecord()
            result = False

        self._serviceDate = CDateInfo(forceDate(record.value('serviceDate')))
        self._event       = self.getInstance(CEmergencyEventInfo, forceRef(record.value('event_id')))
        self._visit       = self.getInstance(CVisitInfo, forceRef(record.value('visit_id')))
        self._action      = self.getInstance(CActionInfo, forceRef(record.value('action_id')))
        self._price       = forceDouble(record.value('price'))
        self._unit        = self.getInstance(CRBMedicalAidUnitInfo, forceRef(record.value('unit_id')))
        self._amount      = forceDouble(record.value('amount'))
        self._uet         = forceDouble(record.value('uet'))
        self._sum         = forceDouble(record.value('sum'))
        self._date        = CDateInfo(forceDate(record.value('date')))
        self._number      = forceString(record.value('number'))
        self._refuseType  = self.getInstance(CRBPayRefuseTypeInfo, forceRef(record.value('refuseType_id')))
        self._reexposeItem = self.getInstance(CAccountItemInfo, forceRef(record.value('reexposeItem_id')))
        self._note        = forceString(record.value('note'))
        self._service     = self.getInstance(CServiceInfo, forceRef(record.value('service_id')))
        self._tariff = self.getInstance(CContractTariffInfo, forceRef(record.value('tariff_id')))
        self._vat           = forceDouble(record.value('VAT'))
        self._usedCoefficients  = self.getUsedCoefficientsList(forceString(record.value('usedCoefficients')))
        self._payedSum = forceDouble(record.value('payedSum'))
        self._csg = self.getInstance(CCSGInfo, forceInt(record.value('eventCSG_id')))
        return result

    def __str__(self):
        self.load()
        return u'%s %s %s' % (self._serviceDate, self.event.client, self._sum)

    serviceDate = property(lambda self: self.load()._serviceDate)
    event = property(lambda self: self.load()._event)
    visit = property(lambda self: self.load()._visit)
    action = property(lambda self: self.load()._action)
    price = property(lambda self: self.load()._price)
    unit = property(lambda self: self.load()._unit)
    amount = property(lambda self: self.load()._amount)
    uet = property(lambda self: self.load()._uet)
    sum = property(lambda self: self.load()._sum)
    date = property(lambda self: self.load()._date)
    number = property(lambda self: self.load()._number)
    refuseType = property(lambda self: self.load()._refuseType)
    reexposeItem = property(lambda self: self.load()._reexposeItem)
    note = property(lambda self: self.load()._note)
    service = property(lambda self: self.load()._service)
    tariff = property(lambda self: self.load()._tariff)
    vat = property(lambda self: self.load()._vat)
    usedCoefficients = property(lambda self: self.load()._usedCoefficients)
    payedSum = property(lambda self: self.load()._payedSum)
    csg = property(lambda self: self.load()._csg)
    preexposeItem = property(lambda self: self.getPreexposeItem())

    def getUsedCoefficientsList(self, usedCoefficients):
        usedCoefficientsList = []
        if usedCoefficients!=u'':
            coefficientList = json.loads(usedCoefficients)
            for group, list in coefficientList.iteritems():
                for name, value in list.iteritems():
                    usedCoefficientsList.append([group, name, value])
        return usedCoefficientsList


class CContractTariffInfo(CInfo):
    def __init__(self, context, tariffId):
        CInfo.__init__(self, context)
        self._tariffId = tariffId
        self._sex = 0
        self._age = ''
        self._compositionExpenses = []

    def _load(self):
        db = QtGui.qApp.db
        tableContractTariff = db.table('Contract_Tariff')
        cond = [tableContractTariff['deleted'].eq(0),
                tableContractTariff['id'].eq(self._tariffId),
                ]
        record = db.getRecordEx(tableContractTariff, '*', cond)
        if record:
            self._age = forceString(record.value('age'))
            self._sex = forceInt(record.value('sex'))
            id = forceInt(record.value('id'))
            self._compositionExpenses = self.getInstance(CContractCompositionExpenseInfoList, id)
            return True
        return False

    sex     = property(lambda self: self.load()._sex)
    age     = property(lambda self: self.load()._age)
    compositionExpenses = property(lambda self: self.load()._compositionExpenses)


class CContractCompositionExpenseInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id

    def _load(self):
        db = QtGui.qApp.db
        tableCCE = db.table('Contract_CompositionExpense')
        tableESI = db.table('rbExpenseServiceItem')
        table = tableCCE.leftJoin(tableESI, tableCCE['rbTable_id'].eq(tableESI['id']))
        cond = [ tableCCE['id'].eq(self.id) ]
        record = db.getRecordEx(table, '*', cond)
        if record:
            self._percent = forceDouble(record.value('percent'))
            self._sum = forceDouble(record.value('sum'))
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._isBase = forceInt(record.value('isBase'))
            return True
        else:
            self._percent = None
            self._sum = None
            self._code = ''
            self._name = ''
            self._isBase = None
            return False

    percent = property(lambda self: self.load()._percent)
    sum     = property(lambda self: self.load()._sum)
    code    = property(lambda self: self.load()._code)
    name    = property(lambda self: self.load()._name)
    isBase  = property(lambda self: self.load()._isBase)


class CContractCompositionExpenseInfoList(CInfoList):
    def __init__(self, context, contractTariffId):
        CInfoList.__init__(self, context)
        self.contractTariffId = contractTariffId

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Contract_CompositionExpense')
        idList = db.getIdList(table, 'id', table['master_id'].eq(self.contractTariffId), 'id')
        self._items = [ self.getInstance(CContractCompositionExpenseInfo, id) for id in idList ]
        return True


class CAccountItemInfoList(CInfoList):
    def __init__(self, context, accountId):
        CInfoList.__init__(self, context)
        self.accountId = accountId


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Account_Item')
        idList = db.getIdList(table, 'id', table['master_id'].eq(self.accountId), 'id')
        self._items = [ self.getInstance(CAccountItemInfo, id) for id in idList ]
        return True


class CAccountInfoList(CInfoList):
    def __init__(self, context, accountIdList):
        CInfoList.__init__(self, context)
        self.idList = accountIdList


    def _load(self):
        self._items = [ self.getInstance(CAccountInfo, id) for id in self.idList ]
        return True


class CAccountInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
        self.selectedItemIdList = []


    def _load(self):
        from Events.EventInfo  import CContractInfo

        db = QtGui.qApp.db
        record = db.getRecord('Account', '*', self.id)
        if record:
            result = True
        else:
            record = db.table('Account').newRecord()
            result = False
        self._contract = self.getInstance(CContractInfo, forceRef(record.value('contract_id')))
        self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
        self._payer = self.getInstance(COrgInfo, forceRef(record.value('payer_id')))
        self._settleDate = CDateInfo(forceDate(record.value('settleDate')))
        self._number = forceString(record.value('number'))
        self._date = CDateInfo(forceDate(record.value('date')))
        self._amount = forceDouble(record.value('amount'))
        self._uet = forceDouble(record.value('uet'))
        self._sum = forceDouble(record.value('sum'))
        self._exposeDate = CDateInfo(forceDate(record.value('exposeDate')))
        self._payedAmount = forceDouble(record.value('payedAmount'))
        self._payedSum = forceDouble(record.value('payedSum'))
        self._refusedAmount = forceDouble(record.value('refusedAmount'))
        self._refusedSum = forceDouble(record.value('refusedSum'))
        self._format = self.getInstance(CAccountExportFormatInfo, forceRef(record.value('format_id')))
        self._items = self.getInstance(CAccountItemInfoList, self.id)
        self._selectedItems = [ self.getInstance(CAccountItemInfo, id) for id in self.selectedItemIdList ]
        return result


    def __str__(self):
        self.load()
        return u'%s от %s' % (self._number, self._date)

    contract = property(lambda self: self.load()._contract)
    orgStructure = property(lambda self: self.load()._orgStructure)
    payer = property(lambda self: self.load()._payer)
    settleDate = property(lambda self: self.load()._settleDate)
    number = property(lambda self: self.load()._number)
    date = property(lambda self: self.load()._date)
    uet = property(lambda self: self.load()._uet)
    sum = property(lambda self: self.load()._sum)
    exposeDate = property(lambda self: self.load()._exposeDate)
    payedAmount = property(lambda self: self.load()._payedAmount)
    payedSum = property(lambda self: self.load()._payedSum)
    refusedAmount = property(lambda self: self.load()._refusedAmount)
    refusedSum = property(lambda self: self.load()._refusedSum)
    format = property(lambda self: self.load()._format)
    items = property(lambda self: self.load()._items)
    selectedItems = property(lambda self: self.load()._selectedItems)
