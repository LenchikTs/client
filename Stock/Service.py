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

from PyQt4 import QtGui, QtCore

from library.Counter import CCounterController
from library.blmodel.Query import CQuery
from library.Utils import forceDouble, forceRef, forceDate, forceString

from Stock.StockModel import CStockMotion, CStockMotionItem
from Stock.Utils import (
    findFinanceBatchShelfTime, UTILIZATION, getBatchShelfTimeFinance,
    INTERNAL_CONSUMPTION, getExistsNomenclatureAmount, getStockMotionItemQntEx, getNomenclatureUnitRatio, #getRatio
)

from Stock.Utils import CStockCache


def _getSockMotionItemUniqueValues(stockMotionItem, fieldName, cond=None):
    queryTable = stockMotionItem.getTable()

    _cond = [
        CStockMotionItem.master_id == stockMotionItem.master_id,
    ]

    if cond:
        if isinstance(cond, list):
            _cond.extend(cond)
        else:
            _cond.append(cond)

    fields = [fieldName]

    return [
        getattr(CStockMotionItem, fieldName).attributeType.fromQVariantValue(getattr(r, fieldName))
        for r in CStockMotionItem
            .query(queryTable, fields=fields, cond=_cond)
            .getDistinctList()
        ]


class CStockService(object):
    def __init__(self, stockMotion):
        self._stockMotion = stockMotion
        self.stockCache = CStockCache()
        self._mapNomenclatureIdToUnitId = {}


    def _getNomenclatureDefaultUnits(self, nomenclatureId):
        if not nomenclatureId:
            return {}
        result = self._mapNomenclatureIdToUnitId.get(nomenclatureId)
        if result is None:
            record = QtGui.qApp.db.getRecord('rbNomenclature',
                                             ('defaultStockUnit_id', 'defaultClientUnit_id'),
                                             nomenclatureId
                                            )
            if record:
                defaultStockUnitId = forceRef(record.value('defaultStockUnit_id'))
                defaultClientUnitId = forceRef(record.value('defaultClientUnit_id'))
            else:
                defaultStockUnitId = defaultClientUnitId = None
            result = {
                       'defaultStockUnitId' : defaultStockUnitId,
                       'defaultClientUnitId': defaultClientUnitId
                     }
            self._mapNomenclatureIdToUnitId[nomenclatureId] = result
        return result


    def getDefaultStockUnitId(self, nomenclatureId):
        return self._getNomenclatureDefaultUnits(nomenclatureId).get('defaultStockUnitId')


    def getRatio(self, nomenclatureId, oldUnitId, newUnitId):
        if oldUnitId is None:
            oldUnitId = self.getDefaultStockUnitId(nomenclatureId)
        if newUnitId is None:
            newUnitId = self.getDefaultStockUnitId(nomenclatureId)
        if oldUnitId == newUnitId:
            return 1
        ratio = getNomenclatureUnitRatio(nomenclatureId, oldUnitId, newUnitId)
        return ratio


    @staticmethod
    def getStockMotionByRecord(stockMotionRecord):
        return CStockMotion(stockMotionRecord)


    def getStockMotionItemByRecord(self, stockMotionItemRecord):
        result = CStockMotionItem(stockMotionItemRecord)
        result.stockMotion = self._stockMotion
        return result


    @staticmethod
    def setFinanceBatchShelfTime(stockMotionItem, financeId=None, medicalAidKindId=None, setShelfTimeCond=False, isInternalConsumption=False):
        stockMotion = stockMotionItem.stockMotion

        if setShelfTimeCond and not isInternalConsumption:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,
                stockMotionItem=stockMotionItem, financeId=financeId,  first=False, medicalAidKind = medicalAidKindId
                )
        elif setShelfTimeCond and isInternalConsumption:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,
                stockMotionItem=stockMotionItem, filterFor=INTERNAL_CONSUMPTION, first=False, medicalAidKind = medicalAidKindId
                )
        elif QtGui.qApp.controlSMFinance() == 0 or not setShelfTimeCond:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,
                stockMotionItem=stockMotionItem, filterFor=UTILIZATION, first=False, medicalAidKind = medicalAidKindId
                )
        else:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,
                stockMotionItem=stockMotionItem, financeId=financeId,  first=False, medicalAidKind = medicalAidKindId
                )

        infinity = []
        withShelfTime = []
        withMedicalAidKind = []
        withoutMedicalAidKind = []

        for v in result:
            _, _, shelfTime, medicalAidKind, price, reservationClient = v
            if shelfTime.isNull():
                infinity.append(v)
            else:
                withShelfTime.append(v)
            if medicalAidKindId:
                if medicalAidKind:
                    withMedicalAidKind.append(v)
                else:
                    withoutMedicalAidKind.append(v)

        vw = None
        vwo = None

        if withShelfTime:
            v = sorted(result, key=lambda v: v[2])[0]
            if len(withMedicalAidKind):
                vw = sorted(withMedicalAidKind, key=lambda v: v[2])[0]
            if len(withoutMedicalAidKind):
                vwo = sorted(withoutMedicalAidKind, key=lambda v: v[2])[0]
        else:
            v = infinity[0] if infinity else (None, None, None, None)
            if len(withMedicalAidKind):
                vw = sorted(withMedicalAidKind, key=lambda v: v[3])[0]
            if len(withoutMedicalAidKind):
                vwo = sorted(withoutMedicalAidKind, key=lambda v: v[3])[0]

        if vw:
            financeId, batch, shelfTime, medicalAidKindId, price, reservationClient = vw
        elif vwo:
            financeId, batch, shelfTime, medicalAidKindId, price, reservationClient = vwo
        else:
            financeId, batch, shelfTime, medicalAidKindId, price, reservationClient = v

        stockMotionItem.finance_id = financeId
        stockMotionItem.batch = batch
        stockMotionItem.shelfTime = shelfTime
        stockMotionItem.price = price
        stockMotionItem.medicalAidKind_id = medicalAidKindId


    @staticmethod
    def setFinanceAndShelfTimeByBatch(stockMotionItem, setShelfTimeCond=False, isStockUtilization = False):
        if setShelfTimeCond:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id,
            batch = stockMotionItem.batch,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        else:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id,
            batch = stockMotionItem.batch, setShelfTimeCond=False, isStockUtilization = isStockUtilization
            )
        stockMotionItem.finance_id = financeId
        stockMotionItem.medicalAidKind_id = medicalAidKind
        stockMotionItem.shelfTime = shelfTime
        stockMotionItem.price = price

    @staticmethod
    def setFinanceAndBatchByShelfTime(stockMotionItem, setShelfTimeCond=False):
        if setShelfTimeCond:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        else:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id, setShelfTimeCond=False,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        stockMotionItem.finance_id = financeId
        stockMotionItem.medicalAidKind_id = medicalAidKind
        stockMotionItem.batch = batch
        stockMotionItem.price = price

    @staticmethod
    def setBatchAndShelfTimeAndFinanceByMedicalAidMind(stockMotionItem, setShelfTimeCond=False):
        if setShelfTimeCond:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        else:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id, setShelfTimeCond=False,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        stockMotionItem.shelfTime = shelfTime
        stockMotionItem.batch = batch
        stockMotionItem.financeId = financeId
        stockMotionItem.price = price

    @staticmethod
    def setBatchAndShelfTimeByFinance(stockMotionItem, setShelfTimeCond=False):
        if setShelfTimeCond:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        else:
            batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(stockMotionItem.nomenclature_id, setShelfTimeCond=False,
            medicalAidKind = stockMotionItem.medicalAidKind_id,
            financeId = stockMotionItem.finance_id)
        stockMotionItem.shelfTime = shelfTime
        stockMotionItem.medicalAidKind_id = medicalAidKind
        stockMotionItem.batch = batch
        stockMotionItem.price = price

    @staticmethod
    def getBatchListDependOnFinanceAndShelfTime(stockMotionItem):
        stockMotion = stockMotionItem.stockMotion
        if stockMotion.supplier_id:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,#FILTER_FOR_BATCH_AND_SHELF_TIME_FOR_UTILIZATION
                stockMotionItem=stockMotionItem, filterFor=UTILIZATION, first=False
            )
            return [r[1] for r in result]

        cond = [
            CStockMotionItem.finance_id == stockMotionItem.finance_id,
            CStockMotionItem.shelfTime == stockMotionItem.shelfTime
        ]
        return _getSockMotionItemUniqueValues(stockMotionItem, CStockMotionItem.batch.name, cond)


    @staticmethod
    def getShelfTimeListDependOnFinanceAndBatch(stockMotionItem, orgStructureId=None):
        stockMotion = stockMotionItem.stockMotion
        if stockMotion.supplier_id:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,#FILTER_FOR_BATCH_AND_FINANCE_FOR_UTILIZATION
                stockMotionItem=stockMotionItem, filterFor=UTILIZATION, first=False
            )
            return [r[2] for r in result]

        cond = [
            CStockMotionItem.finance_id == stockMotionItem.finance_id,
            CStockMotionItem.batch == stockMotionItem.batch
        ]
        return _getSockMotionItemUniqueValues(stockMotionItem, CStockMotionItem.shelfTime.name, cond)

    @staticmethod
    def getFinanceIdListDependOnBatchAndShelfTime(stockMotionItem, orgStructureId):
        stockMotion = stockMotionItem.stockMotion
        if stockMotion.supplier_id:
            result = findFinanceBatchShelfTime(
                stockMotion.supplier_id, stockMotionItem.nomenclature_id,#FILTER_FOR_FINANCE_AND_SHELF_TIME_FOR_UTILIZATION
                stockMotionItem=stockMotionItem, filterFor=UTILIZATION, first=False
            )
            return [r[0] for r in result]

        cond = [
            CStockMotionItem.shelfTime == stockMotionItem.shelfTime,
            CStockMotionItem.batch == stockMotionItem.batch
        ]

        return _getSockMotionItemUniqueValues(stockMotionItem, CStockMotionItem.finance_id.name, cond)

    @classmethod
    def doClientInvoice(cls, action, supplierId, date=None, clientId=None):
        """
        :param action: Events.Action.CAction
        :param supplierId: supplier org structure id
        :return: bool
        """
        messageExecWriteOffNomenclatureExpense = u''
        nomenclatureExpense = action.nomenclatureExpense
        if not nomenclatureExpense:
            return False, messageExecWriteOffNomenclatureExpense

        event = action.event
        if not event:
            return False, messageExecWriteOffNomenclatureExpense

        QtGui.qApp.setCounterController(CCounterController())

        executionPlanItem = action.executionPlanManager.currentItem
        if executionPlanItem and executionPlanItem.nomenclature and executionPlanItem.nomenclature.nomenclatureId:
            if executionPlanItem.nomenclature.nomenclatureId:
                if not action.nomenclatureExpense.stockMotionItems() or not action.nomenclatureExpense.getNomenclatureIdItem(executionPlanItem.nomenclature.nomenclatureId):
                    nomenclatureIdDict = {}
                    nomenclatureIdDict[executionPlanItem.nomenclature.nomenclatureId] = (action.getRecord(), executionPlanItem.nomenclature.dosage)
                    action.nomenclatureExpense.updateNomenclatureIdListToAction(nomenclatureIdDict)
                if executionPlanItem.nomenclature.dosage:
                    nomenclatureExpense.updateNomenclatureDosageValue(
                        executionPlanItem.nomenclature.nomenclatureId,
                        executionPlanItem.nomenclature.dosage,
                        force=True
                    )

        stockMotionRecord = nomenclatureExpense.stockMotionRecord()
        stockMotionItemRecords = nomenclatureExpense.stockMotionItems()

        stockMotion = CStockMotion(stockMotionRecord)
        stockMotion.supplier_id = supplierId
        stockMotion.stockDocumentType = 4
        stockMotion.date = QtCore.QDateTime.currentDateTime()
        stockMotion.generateStockMotionNumber()
        stockMotion.client_id = event.client_id

        service = cls(stockMotion)
        for stockMotionItemRecord in stockMotionItemRecords:
            service.getStockMotionItemByRecord(stockMotionItemRecord)

        isControlExecWriteOffNomenclatureExpense = QtGui.qApp.controlExecutionWriteOffNomenclatureExpense()
        if isControlExecWriteOffNomenclatureExpense:
            db = QtGui.qApp.db
            message = u''
            nomenclatureLine = []
            tableNomenclature = db.table('rbNomenclature')
            if action.nomenclatureExpense:
                stockMotionItems = action.nomenclatureExpense.stockMotionItems()
                for stockMotionItem in stockMotionItems:
                    price = forceDouble(stockMotionItem.value('price'))
                    nomenclatureId = forceRef(stockMotionItem.value('nomenclature_id'))
                    if nomenclatureId and nomenclatureId not in nomenclatureLine:
                        qnt = round(forceDouble(stockMotionItem.value('qnt')), QtGui.qApp.numberDecimalPlacesQnt())
                        unitId = forceRef(stockMotionItem.value('unit_id'))
                        stockUnitId = service.getDefaultStockUnitId(nomenclatureId)
                        ratio = service.getRatio(nomenclatureId, stockUnitId, unitId)
                        if ratio is not None:
                            price = price*ratio
                            qnt = qnt / ratio
                        financeId = forceRef(stockMotionItem.value('finance_id'))
                        batch = forceString(stockMotionItem.value('batch'))
                        shelfTime = forceDate(stockMotionItem.value('shelfTime'))
                        shelfTime = shelfTime.toPyDate() if bool(shelfTime) else None
                        medicalAidKindId = forceRef(stockMotionItem.value('medicalAidKind_id'))
                        if date:
                            otherHaving=[u'(shelfTime>=%s) OR shelfTime is NULL'%(db.formatDate(date))]
                        else:
                            otherHaving=[u'(shelfTime>=curDate()) OR shelfTime is NULL']
                        stockMotionId = forceRef(stockMotionItem.value('master_id'))
                        existsQnt = getExistsNomenclatureAmount(nomenclatureId, financeId, batch, unitId=stockUnitId, medicalAidKindId = medicalAidKindId, shelfTime=shelfTime, otherHaving=otherHaving, exact=True, price=price, isStockUtilization=False, precision=QtGui.qApp.numberDecimalPlacesQnt())
                        prevQnt = round(getStockMotionItemQntEx(nomenclatureId, stockMotionId=stockMotionId, batch=batch, financeId=financeId, clientId=clientId, medicalAidKindId=medicalAidKindId, price=None, oldPrice=price, oldUnitId=stockUnitId), QtGui.qApp.numberDecimalPlacesQnt()) if stockMotionId else 0
                        if clientId:
                            reservationQnt = round(getStockMotionItemQntEx(nomenclatureId, stockMotionId=None, batch=batch, financeId=financeId, clientId=clientId, medicalAidKindId=medicalAidKindId, price=None, oldPrice=price, oldUnitId=stockUnitId), QtGui.qApp.numberDecimalPlacesQnt())
                            resQnt = (round(existsQnt, 2) + round(reservationQnt, 2) + prevQnt) - qnt
                        else:
                            resQnt = (existsQnt + prevQnt) - qnt
                        if resQnt < 0:
                            nomenclatureLine.append(nomenclatureId)
                if nomenclatureLine:
                    nomenclatureName = u''
                    records = db.getRecordList(tableNomenclature, [tableNomenclature['name']], [tableNomenclature['id'].inlist(nomenclatureLine)], order = tableNomenclature['name'].name())
                    for recordNomenclature in records:
                        nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                    message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n'''%(action._actionType.name, nomenclatureName)
                if message:
                    messageExecWriteOffNomenclatureExpense = u'Списываемое ЛСиИМН отсутствует на остатке подразделения.\n'
                    if isControlExecWriteOffNomenclatureExpense == 1:
                        button = QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel
                        message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Выполнить списание?'
                    else:
                        button = QtGui.QMessageBox.Cancel
                        message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Списание невозможно!'
                    res = QtGui.QMessageBox.warning(None,
                                              u'Внимание!',
                                              message2,
                                              button,
                                              QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Cancel:
                        return False, messageExecWriteOffNomenclatureExpense

        db = QtGui.qApp.db
        db.transaction()
        try:
            nextAction = action.finishAction(event.client_id, date)
            action.save(idx=-1)

            if action.executionPlanManager.currentItem:
                CQuery.save(action.executionPlanManager.currentItem)


            if nextAction:
                idx = nextAction.countIdx(event.id)
                nextAction.save(eventId=event.id, idx=idx)
                if nextAction.executionPlanManager.currentItem:
                    epi = nextAction.executionPlanManager.currentItem
                    epi.actionId = nextAction.getId()
                    CQuery.save(epi)
                    if epi.nomenclature:
                        CQuery.save(epi.nomenclature)

        except:
            db.rollback()
            QtGui.qApp.resetAllCounterValueIdReservation()
            raise

        db.commit()

        QtGui.qApp.delAllCounterValueIdReservation()

        QtGui.qApp.setCounterController(None)

        if not nextAction:
            if action.nomenclatureClientReservation:
                action.nomenclatureClientReservation.cancel()

        return True, messageExecWriteOffNomenclatureExpense

