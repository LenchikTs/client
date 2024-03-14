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
##
## Импорт тарифа из ЕИС-ОМС
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from Accounting.Tariff import CTariff
from library.Utils import forceDate, forceDouble, forceInt, forceRef, forceString, toVariant

from Exchange.Cimport import CEISimport, Cimport
from Exchange.Utils import EIS_close, setEIS_db, tbl


from Exchange.Ui_ImportTariffs import Ui_Dialog


def ImportTariffs(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
    try:
        setEIS_db()
        dlg=CImportTariffs(widget, QtGui.qApp.EIS_db, contractId, begDate, endDate, tariffList)
        dlg.exec_()
        return dlg.ok, dlg.tariffList, tariffExpenseItems, []
    except:
        EIS_close()


class CImportTariffs(CEISimport, QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent, EIS_db, contractId, begDate, endDate, tariffList):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.progressBar.setFormat(u'%v из %m')
        self.EIS_db=EIS_db
        self.contractId=contractId
        self.begDate = begDate
        self.endDate = endDate
        self.tariffList = map(None, tariffList)
        self.tariffDict = {}
        for i, tariff in enumerate(self.tariffList):
            key = ( forceInt(tariff.value('tariffType')),
                    forceRef(tariff.value('service_id')),
                    forceString(tariff.value('age')),
                    forceRef(tariff.value('unit_id')) )
            tariffIndexList = self.tariffDict.setdefault(key, [])
            tariffIndexList.append(i)
        self.tblContract_Tariff=tbl('Contract_Tariff')
        self.tblContract=tbl('Contract')
        self.ok = False
        self._mapAmountAndINFIS_CODE2Exists = {}


    def startImport(self):
        self._mapAmountAndINFIS_CODE2Exists.clear()
        self.ok = False
        db=QtGui.qApp.db
        EIS_db=self.EIS_db
        if not EIS_db:
            return
        loadChildren=self.chkLoadChildren.isChecked()
        loadAdult=self.chkLoadAdult.isChecked()
        if not (loadChildren or loadAdult):
            self.log.append(u'нечего загружать')
            return
        amb=self.chkAmb.isChecked()
        stom=self.chkStom.isChecked()
        completeCase = self.chkCompleteCase.isChecked()
        eisProfileTypeIdList=[]
        if amb:
            eisProfileTypeIdList.append(3)
        if stom:
            eisProfileTypeIdList.append(4)
        if completeCase:
            eisProfileTypeIdList.extend((7,  8,  9,  10))
        if not eisProfileTypeIdList:
            self.log.append(u'нечего загружать')
            return
        n=0

        begDateStr='\''+unicode(self.begDate.toString('dd.MM.yyyy'))+'\''
        endDateStr='\''+unicode(self.endDate.toString('dd.MM.yyyy'))+'\''
        eisTariffGroupIdList = EIS_db.getIdList('VMU_TARIFF_PLAN',
                         'ID_TARIFF_GROUP',
                         'TP_BEGIN_DATE<=%s AND TP_END_DATE>=%s' % (endDateStr, begDateStr)
                        )

        eisTableTariff  = EIS_db.table('VMU_TARIFF')
        eisTableProfile = EIS_db.table('VMU_PROFILE')
        eisTable = eisTableTariff.leftJoin(eisTableProfile, eisTableProfile['ID_PROFILE'].eq(eisTableTariff['ID_PROFILE']))
        cond = [ eisTableTariff['ID_LPU'].inlist(eisTariffGroupIdList),
                 eisTableTariff['TARIFF_BEGIN_DATE'].le(self.endDate),
                 eisTableTariff['TARIFF_END_DATE'].ge(self.begDate),
                 eisTableProfile['ID_PROFILE_TYPE'].inlist(eisProfileTypeIdList),
                 eisTableProfile['PROFILE_BEGIN_DATE'].le(self.endDate),
                 eisTableProfile['PROFILE_END_DATE'].ge(self.begDate),
               ]
        if loadChildren and not loadAdult:
            cond.append(eisTableTariff['ID_ZONE_TYPE'].eq(3))
        if loadAdult and not loadChildren:
            cond.append(eisTableTariff['ID_ZONE_TYPE'].eq(1))

        eisTariffKeys = EIS_db.getRecordList(eisTable,
                                             'DISTINCT VMU_TARIFF.ID_PROFILE, VMU_TARIFF.ID_ZONE_TYPE, VMU_PROFILE.PROFILE_INFIS_CODE, VMU_PROFILE.ID_PROFILE_TYPE',
                                             cond,
                                             'PROFILE_INFIS_CODE, ID_PROFILE_TYPE, ID_ZONE_TYPE'
                                            )
        num = len(eisTariffKeys)
        self.progressBar.setMaximum(max(num, 0))
        updatedTariffs = set()
        n_add=0
        n_edit=0
        self.tariffListAdult = []
        self.tariffListChild = []

        self.maxFragList = []
        self.maxFragListValues = []

        for eisTariffKeyRecord in eisTariffKeys:
            QtGui.qApp.processEvents()
            if self.abort:
                break
            PROFILE_INFIS_CODE=forceString(eisTariffKeyRecord.value('PROFILE_INFIS_CODE'))
            ID_ZONE_TYPE=forceInt(eisTariffKeyRecord.value('ID_ZONE_TYPE'))
            ID_PROFILE_TYPE=forceInt(eisTariffKeyRecord.value('ID_PROFILE_TYPE'))
            self.progressBar.setValue(n)
            n+=1
            self.n=n
            age=u''
            if ID_ZONE_TYPE==1:
                age=u'18г-'
            if ID_ZONE_TYPE==3:
                age=u'-17г'
            serviceId=forceInt(db.translate('rbService', 'infis', PROFILE_INFIS_CODE, 'id'))
            if not serviceId:
                self.err2log(PROFILE_INFIS_CODE, u'услуга не найдена')
                continue

            tariffType = CTariff.ttVisit
            unitId = 1
            if ID_PROFILE_TYPE == 4:
                tariffType = CTariff.ttActionUET
                unitId = 3
            if ID_PROFILE_TYPE == 7:
                tariffType = CTariff.ttVisitsByMES
                unitId = 4

            key = (tariffType, serviceId, age, unitId)
            tariffIndexList = self.tariffDict.get(key, None)
            tariffDescr = self.calculateTariffData(PROFILE_INFIS_CODE, ID_ZONE_TYPE, ID_PROFILE_TYPE, eisTariffGroupIdList)

            if tariffIndexList is not None and tariffDescr is not None:
#                localEdit = False
                for i in tariffIndexList:
                    tariff = self.tariffList[i]
                    updatedTariffs.add(i)

                    if self.updateTariff(PROFILE_INFIS_CODE, tariff, tariffDescr):
                        n_edit+=1
                    else:
                        self.err2log(PROFILE_INFIS_CODE, u'не изменён')
            else:
                tariff=self.tblContract_Tariff.newRecord()

                tariff.setValue('master_id', toVariant(self.contractId))
                tariff.setValue('tariffType', toVariant(tariffType))
                tariff.setValue('service_id', toVariant(serviceId))
                tariff.setValue('age', toVariant(age))
                tariff.setValue('unit_id', toVariant(unitId))
                self.setTariff(tariff, tariffDescr)

                if ID_PROFILE_TYPE==7:
                    eventTypeId = self.toKnowEventTypeId(PROFILE_INFIS_CODE)
                    tariff.setValue('eventType_id', toVariant(eventTypeId))

                i = len(self.tariffList)
                self.tariffDict[key] = [i]
                self.tariffList.append(tariff)
                updatedTariffs.add(i)
                n_add+=1
                self.err2log(PROFILE_INFIS_CODE, u'добавлен')

        for i, tariff in enumerate(self.tariffList):
            if i in updatedTariffs:
                continue
            serviceId=forceRef(tariff.value('service_id'))
            PROFILE_INFIS_CODE=forceString(db.translate('rbService', 'id', serviceId, 'infis'))
            self.tariffList[i] = None
            self.err2log(PROFILE_INFIS_CODE, u'удалён')

        self.tariffList = filter(None, self.tariffList)

        zone=''
        if loadChildren and not loadAdult:
            zone=' AND VMU_TARIFF.ID_ZONE_TYPE=3'
        if loadAdult and not loadChildren:
            zone=' AND VMU_TARIFF.ID_ZONE_TYPE=1'

        prevContract=db.getRecordEx(
            self.tblContract,
            'MAX(begDate)',
            'begDate<\''+unicode(self.begDate.toString('yyyy-MM-dd'))+u'\' and grouping=\'ГТС\'')
        if prevContract:
            prevContractDate=forceDate(prevContract.value(0))
            if prevContractDate:
                prevContractDateStr='\''+unicode(prevContractDate.toString('dd.MM.yyyy'))+'\''
                stmt=u'''
                    SELECT *
                    FROM VMU_TARIFF
                    JOIN VMU_PROFILE ON VMU_PROFILE.ID_PROFILE=VMU_TARIFF.ID_PROFILE
                    WHERE
                        VMU_TARIFF.TARIFF_BEGIN_DATE<'''+begDateStr+'''
                        AND VMU_TARIFF.TARIFF_BEGIN_DATE>'''+prevContractDateStr+'''
                        AND VMU_PROFILE.ID_PROFILE_TYPE=3
                        AND VMU_PROFILE.PROFILE_END_DATE>=VMU_TARIFF.TARIFF_BEGIN_DATE
                        AND VMU_PROFILE.PROFILE_BEGIN_DATE<=VMU_TARIFF.TARIFF_BEGIN_DATE'''+zone
                query = EIS_db.query(stmt)
                query.setForwardOnly(True)
                while query.next():
                    QtGui.qApp.processEvents()
                    if self.abort:
                        break
                    record = query.record()
                    PROFILE_INFIS_CODE=forceString(record.value('PROFILE_INFIS_CODE'))
                    self.err2log(PROFILE_INFIS_CODE, u'между этим контрактом и предыдущим')

        nextContract=db.getRecordEx(
            self.tblContract, '*',
            'begDate>\''+unicode(self.begDate.toString('yyyy-MM-dd'))+u'\' and grouping=\'ГТС\'')
        if not nextContract:
            stmt=u'''
                SELECT *
                FROM VMU_TARIFF
                JOIN VMU_PROFILE on VMU_PROFILE.ID_PROFILE=VMU_TARIFF.ID_PROFILE
                WHERE
                    VMU_TARIFF.TARIFF_BEGIN_DATE>'''+begDateStr+'''
                    AND VMU_PROFILE.ID_PROFILE_TYPE=3
                    AND VMU_PROFILE.PROFILE_END_DATE>=VMU_TARIFF.TARIFF_BEGIN_DATE
                    AND VMU_PROFILE.PROFILE_BEGIN_DATE<=VMU_TARIFF.TARIFF_BEGIN_DATE'''+zone
            query = EIS_db.query(stmt)
            query.setForwardOnly(True)
            while query.next():
                QtGui.qApp.processEvents()
                if self.abort:
                    break
                record = query.record()
                PROFILE_INFIS_CODE=forceString(record.value('PROFILE_INFIS_CODE'))
                self.err2log(PROFILE_INFIS_CODE, u'позже этого контракта')

        self.log.append(u'добавлено: %d; изменено: %d' % (n_add, n_edit))
        self.log.append(u'готово')
        self.progressBar.setValue(n-1)
        self.ok = not self.abort


    def calculateTariffData(self, PROFILE_INFIS_CODE, ID_ZONE_TYPE, ID_PROFILE_TYPE, eisTariffGroupIdList):
        # возвращаемое значение - тройка amount, fragmets, uet
        EIS_db = self.EIS_db
        eisTableTariff  = EIS_db.table('VMU_TARIFF')
        eisTableProfile = EIS_db.table('VMU_PROFILE')
        eisTable = eisTableTariff.leftJoin(eisTableProfile, eisTableProfile['ID_PROFILE'].eq(eisTableTariff['ID_PROFILE']))
        records = EIS_db.getRecordList(eisTable,
                                         'TARIFF_BEGIN_DATE, TARIFF_END_DATE, AMOUNT, PRICE, SUMM_DAY, UET, START_DAY, END_DAY',
                                         [ eisTableTariff['ID_LPU'].inlist(eisTariffGroupIdList),
                                           eisTableTariff['ID_ZONE_TYPE'].eq(ID_ZONE_TYPE),
                                           eisTableTariff['TARIFF_BEGIN_DATE'].le(self.endDate),
                                           eisTableTariff['TARIFF_END_DATE'].ge(self.begDate),
                                           eisTableProfile['ID_PROFILE_TYPE'].eq(ID_PROFILE_TYPE),
                                           eisTableProfile['PROFILE_INFIS_CODE'].eq(PROFILE_INFIS_CODE),
                                         ],
                                         ['TARIFF_BEGIN_DATE, ID_TARIFF']
                                      )
        values = {}
        uets   = {}
        prevDate = QDate()
        maxAmount = 0
        for record in records:
            begDate = forceDate(record.value('TARIFF_BEGIN_DATE'))
            if record.isNull('AMOUNT'):
                startDay = forceInt(record.value('START_DAY'))
                endDay = forceInt(record.value('END_DAY'))
                if not startDay or startDay > endDay:
                    continue
                if endDay == 1000:
                    endDay = startDay + 2
                uet = forceDouble(record.value('UET'))
                base = forceDouble(record.value('PRICE'))
                price = forceDouble(record.value('SUMM_DAY'))
                if abs(price) <= 0.001:
                    maxAmount = max(maxAmount, startDay)
                else:
                    maxAmount = max(maxAmount, endDay)
                for day in range(startDay, endDay+1):
                    locValue = base + price*(day-startDay)
                    if prevDate > begDate:
                        pass # нам не интересно
                    elif prevDate == begDate:
                        values[day] = locValue
                        uets[day]   = uet
                    else:
                        prevDate = begDate
                        values = {day: locValue}
                        uets   = {day: uet}
            else:
                amount  = forceInt(record.value('AMOUNT')) # да, оно округляет
                maxAmount = max(maxAmount, amount)
                value   = forceDouble(record.value('PRICE'))
                uet     = forceDouble(record.value('UET'))
                if prevDate > begDate:
                    pass # нам не интересно
                elif prevDate == begDate:
                    values[amount] = value
                    uets[amount]   = uet
                else:
                    prevDate = begDate
                    values = {amount: value}
                    uets   = {amount: uet}

        amounts = values.keys()
        amounts.sort()

        if len(values) == 1:
            return maxAmount, [(0, 0, values.values()[0])], uets.values()[0] # один только нулевой фрагмент

        if None in values: # 0
            return None # что-то непонятное с форматом

        fragList = []

        fragStart = 0
        fragSum = 0.0

        prevValue = 0
        prevAmount = 0

        for i, amount in enumerate(amounts):
            value = values[amount]
            if i == 0:
                price = value/amount
                fragList.append((fragStart, fragSum, price))
            else:
                if amount>maxAmount:
                    break
                # делаем оценку предыдущей суммы из предположения продолжения фрагмента
                estimatedPrevValue = (value-fragSum)/(amount-fragStart)*(prevAmount-fragStart) + fragSum
                if abs(estimatedPrevValue-prevValue)<0.01:
                    # гипотеза линии подтверждена
                    # обновляем цену в fragList
                    price = (value-fragSum)/(amount-fragStart)
                    fragList[-1] = (fragStart, fragSum, price)
                else:
                    # гипотеза линии отброшена
                    # добавляем фрагмент, базирующийся на текущем значении
                    fragStart = amount
                    fragSum = value
                    price = (value-prevValue)/(amount-prevAmount)
                    fragList.append((fragStart, fragSum, price))
            prevAmount = amount
            prevValue  = value
        return maxAmount, fragList, uets.get(1, 0) or uets.values()[0] or 0


    def updateTariff(self, PROFILE_INFIS_CODE, tariff, tariffDescr):
        tariffChanged = False

        amount, fragList, uet = tariffDescr
        price = fragList[0][2]

        oldPrice=forceDouble(tariff.value('price'))
        oldUet = forceDouble(tariff.value('uet'))
        oldAmount = forceDouble(tariff.value('amount'))

        if abs(price-oldPrice)>0.001:
            tariffChanged = True
            tariff.setValue('price', toVariant(price))
            self.err2log(PROFILE_INFIS_CODE, u'стоимость изменёна с %f на %f' % (oldPrice, price))
        if abs(uet-oldUet)>0.001:
            tariffChanged = True
            tariff.setValue('uet', toVariant(uet))
            self.err2log(PROFILE_INFIS_CODE, u'УЕТ изменён с %f на %f' % (oldUet, uet))
        if abs(amount-oldAmount)>0.001:
            tariffChanged = True
            tariff.setValue('amount', toVariant(amount))
            self.err2log(PROFILE_INFIS_CODE, u'количество изменено с %f на %f' % (oldAmount, amount))

        f1 = fragList[1] if len(fragList)>1 else (0, 0, 0)
        oldF1Start = forceDouble(tariff.value('frag1Start'))
        oldF1Sum   = forceDouble(tariff.value('frag1Sum'))
        oldF1Price = forceDouble(tariff.value('frag1Price'))

        if abs(f1[0]-oldF1Start) > 0.001:
            tariffChanged = True
            tariff.setValue('frag1Start', toVariant(f1[0]))
            self.err2log(PROFILE_INFIS_CODE, u'Начало Ф1 изменено c %f на %f' % (oldF1Start, f1[0]))

        if abs(f1[1]-oldF1Sum) > 0.001:
            tariffChanged = True
            tariff.setValue('frag1Sum', toVariant(f1[1]))
            self.err2log(PROFILE_INFIS_CODE, u'Начальная сумма Ф1 изменена с %f на %f' % (oldF1Sum, f1[1]))

        if abs(f1[2]-oldF1Price) > 0.001:
            tariffChanged = True
            tariff.setValue('frag1Price', toVariant(f1[2]))
            self.err2log(PROFILE_INFIS_CODE, u'Цена в Ф1 изменена с %f на %f' % (oldF1Price, f1[2]))

        f2 = fragList[2] if len(fragList)>2 else (0, 0, 0)
        oldF2Start = forceDouble(tariff.value('frag2Start'))
        oldF2Sum   = forceDouble(tariff.value('frag2Sum'))
        oldF2Price = forceDouble(tariff.value('frag2Price'))

        if abs(f2[0]-oldF2Start) > 0.001:
            tariffChanged = True
            tariff.setValue('frag2Start', toVariant(f2[0]))
            self.err2log(PROFILE_INFIS_CODE, u'Начало Ф2 изменено c %f на %f' % (oldF2Start, f2[0]))

        if abs(f2[1]-oldF2Sum) > 0.001:
            tariffChanged = True
            tariff.setValue('frag2Sum', toVariant(f2[1]))
            self.err2log(PROFILE_INFIS_CODE, u'Начальная сумма Ф2 изменена с %f на %f' % (oldF2Sum, f2[1]))

        if abs(f2[2]-oldF2Price) > 0.001:
            tariffChanged = True
            tariff.setValue('frag2Price', toVariant(f2[2]))
            self.err2log(PROFILE_INFIS_CODE, u'Цена в Ф2 изменена с %f на %f' % (oldF2Price, f2[2]))

        return tariffChanged


    def setTariff(self, tariff, tariffDescr):
        amount, fragList, uet = tariffDescr
        price = fragList[0][2]
        f1 = fragList[1] if len(fragList)>1 else (0, 0, 0)
        f2 = fragList[2]if len(fragList)>2 else (0, 0, 0)

        tariff.setValue('price', toVariant(price))
        tariff.setValue('uet', toVariant(uet))
        tariff.setValue('amount', toVariant(amount))
        tariff.setValue('frag1Start', toVariant(f1[0]))
        tariff.setValue('frag1Sum',   toVariant(f1[1]))
        tariff.setValue('frag1Price', toVariant(f1[2]))
        tariff.setValue('frag2Start', toVariant(f2[0]))
        tariff.setValue('frag2Sum',   toVariant(f2[1]))
        tariff.setValue('frag2Price', toVariant(f2[2]))


    def toKnowEventTypeId(self, PROFILE_INFIS_CODE):
        eisProfileName = forceString(self.EIS_db.translate('VMU_PROFILE', 'PROFILE_INFIS_CODE', PROFILE_INFIS_CODE, 'PROFILE_NAME'))
        eisKsgGroupId  = forceInt(self.EIS_db.translate('VMU_PROFILE', 'PROFILE_INFIS_CODE', PROFILE_INFIS_CODE, 'ID_KSG_GROUP'))
        eisKsgGroupName= forceString(self.EIS_db.translate('VMU_KSG_GROUP', 'ID_KSG_GROUP', eisKsgGroupId, 'KSG_GROUP_NAME'))

        db = QtGui.qApp.db
        tableEventType = db.table('EventType')
        tableEventProfile = db.table('rbEventProfile')
        table = tableEventType.leftJoin(tableEventProfile, tableEventProfile['id'].eq(tableEventType['eventProfile_id']))
        record = db.getRecordEx(table,
                                tableEventType['id'],
                                [ tableEventType['name'].like(eisProfileName[:3]+'%'),
                                  tableEventProfile['name'].eq(eisKsgGroupName),
                                ]
                               )
        return forceRef(record.value('id')) if record else None


    def err2log(self, infisServiceCode, message):
        note=u''
        begDate=forceDate(QtGui.qApp.db.translate('rbService', 'infis', infisServiceCode, 'begDate'))
        endDate=forceDate(QtGui.qApp.db.translate('rbService', 'infis', infisServiceCode, 'endDate'))
        if begDate:
            note=u' (с '+forceString(begDate)
            if endDate:
                note+=u' по '+forceString(endDate)
            note+=u')'
        self.log.append(u'тариф '+infisServiceCode+note+u' '+message)
