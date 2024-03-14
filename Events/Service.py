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
from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from Accounting.Tariff import CTariff
from library.PrintInfo import CDateInfo, CRBInfo, CInfo, CRBInfoWithIdentification

from library.AgeSelector import parseAgeSelector, checkAgeSelector
from library.PrintInfo import CInfo, CRBInfo, CDateInfo
from library.Utils import (
    forceString,
    forceDouble,
    forceInt,
    forceDate,
    calcAgeTuple, forceRef, forceBool,
)


class CServiceGroupInfo(CRBInfo):
    tableName = 'rbServiceGroup'

    def _initByRecord(self, record):
        self._regionalCode = forceString(record.value('regionalCode'))


    def _initByNull(self):
        self._regionalCode = None

    regionalCode  = property(lambda self: self.load()._regionalCode)


class CServiceInfo(CRBInfoWithIdentification):
    tableName = 'rbService'

    def _initByRecord(self, record):
        self._groupId = forceRef(record.value('group_id'))
        self._eisLegacy = forceBool(record.value('eisLegacy'))
        self._license = forceBool(record.value('license'))
        self._infis = forceString(record.value('infis'))
        self._begDate = CDateInfo(record.value('begDate'))
        self._endDate = CDateInfo(record.value('endDate'))
        self._adultUetDoctor = forceDouble(record.value('adultUetDoctor'))
        self._adultUetAverageMedWorker = forceDouble(record.value('adultUetAverageMedWorker'))
        self._childUetDoctor = forceDouble(record.value('childUetDoctor'))
        self._childUetAverageMedWorker = forceDouble(record.value('childUetAverageMedWorker'))


    def _initByNull(self):
        self._groupId = None
        self._eisLegacy = False
        self._eisLegacy = False
        self._license = False
        self._infis = ''
        self._begDate = CDateInfo()
        self._endDate = CDateInfo()
        self._adultUetDoctor = 0
        self._adultUetAverageMedWorker = 0
        self._childUetDoctor = 0
        self._childUetAverageMedWorker = 0


    def prepareTariff(self, contractId, clientId = None):
        self.tariff = self.getInstance(CTariffInfo, self.id)
        self.tariff.setContractId(contractId)
        if clientId:
            self.tariff.setClientId(clientId)

    group       = property(lambda self: self.getInstance(CServiceGroupInfo, self.load()._groupId))
    eisLegacy   = property(lambda self: self.load()._eisLegacy)
    license     = property(lambda self: self.load()._license)
    infis       = property(lambda self: self.load()._infis)
    begDate     = property(lambda self: self.load()._begDate)
    endDate     = property(lambda self: self.load()._endDate)
    adultUetDoctor = property(lambda self: self.load()._adultUetDoctor)
    adultUetAverageMedWorker = property(lambda self: self.load()._adultUetAverageMedWorker)
    childUetDoctor = property(lambda self: self.load()._childUetDoctor)
    childUetAverageMedWorker = property(lambda self: self.load()._childUetAverageMedWorker)
    serviceIdent = property(lambda self: self.identify(u'urn:oid:131o'))


# WTF? что это? почему это здесь?
class CTariffInfo(CInfo):
    def __init__(self, context, serviceId):
        CInfo.__init__(self, context)
        self._serviceId = serviceId
        self._masterId = None
        self._price = None
        self._uet = 0
        self._maxAmount = 0
        self._contractDescr = None
        self._clientId = None
        self._clientBirthDate = None


    def setContractId(self, contractId):
        self._masterId = contractId

    def setClientId(self, clientId):
        self._clientId = clientId


    def _load(self, isVisit,  execDate):
        if self._masterId and self._serviceId:
            db = QtGui.qApp.db
            table = db.table('Contract_Tariff')
            cond = [table['deleted'].eq(0),
                    table['service_id'].eq(self._serviceId),
                    table['master_id'].eq(self._masterId), 
                    table['begDate'].le(execDate), 
                   "Contract_Tariff.endDate is null or Contract_Tariff.endDate >= '%s'" % execDate.toString("yyyy-MM-dd")
                   ]
            if isVisit:
                cond.append(table['tariffType'].eq(0))
                       
            recordList = db.getRecordList(table, '*', cond)
            tariffRecord = None
            for record in recordList:
                age = forceString(record.value('age'))
                ageSelector = None
                if age and self._clientId:
                    ageSelector = parseAgeSelector(age)
                    if not self._clientBirthDate:
                        self._clientBirthDate = forceDate(db.translate('Client', 'id', self._clientId, 'birthDate'))
                    clientAge = calcAgeTuple(self._clientBirthDate, QDate.currentDate())
                    if not clientAge:
                        clientAge = (0, 0, 0, 0)
                    if checkAgeSelector(ageSelector, clientAge):
                        tariffRecord = record
                        break
                else:
                    tariffRecord = record
                    break
            if tariffRecord:
                self._price            = forceDouble(tariffRecord.value('price'))
                self._uet = forceDouble(tariffRecord.value('uet'))
                frags = [(0.0, 0.0, self._price)]

                if forceDouble(tariffRecord.value('frag1Start')):
                    frags.append(( forceDouble(tariffRecord.value('frag1Start')),
                                   forceDouble(tariffRecord.value('frag1Sum')),
                                   forceDouble(tariffRecord.value('frag1Price')),
                                ))

                if forceDouble(tariffRecord.value('frag2Start')):
                    frags.append(( forceDouble(tariffRecord.value('frag2Start')),
                                   forceDouble(tariffRecord.value('frag2Sum')),
                                   forceDouble(tariffRecord.value('frag2Price'))/2,
                                ))
                frags.reverse()
                self._frags            = frags

                self._tariffType = forceInt(tariffRecord.value('tariffType'))
                self._maxAmount = forceDouble(tariffRecord.value('amount'))
                self._tariff = CTariff(tariffRecord, 2)
                return True
        return False



    def getPrice(self, amount, execDate, isVisit=False, eventInfo=None, actionInfo=None):
        from Accounting.Utils import getContractDescr
        from Accounting.Utils import unpackExposeDiscipline
        from Accounting.AccountBuilder import evalPriceForKrasnodarA13, evalPriceForMurmansk2015Hospital
        db = QtGui.qApp.db

        if self._load(isVisit,  execDate):
            if self._maxAmount and amount > self._maxAmount:
                amount = self._maxAmount
            if self._price:
                if self._tariffType == CTariff.ttEventByMESLen:
                    sum = 0
                    for fragStart, fragSum, fragPrice in self._frags:
                        if amount>=fragStart:
                            sum = fragSum + (amount-fragStart)*fragPrice
                            break
                    price = sum/amount if amount else self._price
                    return sum
                elif self._tariffType == CTariff.ttVisitsByMES: #визиты по МЭС
                    return self._price
                elif  self._tariffType == CTariff.ttKrasnodarA13 and eventInfo is not None and eventInfo._loaded:
                    if not self._contractDescr:
                        self._contractDescr = getContractDescr(self._masterId)
                    amount = 1.0
                    clientId = eventInfo._clientId
                    eventId = eventInfo.id
                    eventTypeId = eventInfo.getEventTypeId()
                    eventBegDate = eventInfo._setDate.date
                    eventEndDate = eventInfo._execDate.date
                    relativeId = eventInfo._relative._id
                    infis = forceString(db.translate('rbService', 'id', self._serviceId, 'infis'))
                    price, coeff, usedCoeffDict = evalPriceForKrasnodarA13(self._contractDescr, self._tariff, clientId, eventId, eventTypeId, eventBegDate, eventEndDate, relativeId, infis)
                    sum    = round(price, 2)
                    return sum
                elif self._tariffType == CTariff.ttMurmansk2015Hospital and eventInfo is not None and eventInfo._loaded:
                    if not self._contractDescr:
                        self._contractDescr = getContractDescr(self._masterId)
                    amount = 1.0
                    clientId = eventInfo._clientId
                    eventId = eventInfo.id
                    eventTypeId = eventInfo.getEventTypeId()
                    eventBegDate = eventInfo._setDate.date
                    eventEndDate = eventInfo._execDate.date
                    shortHospitalisation = eventBegDate.addDays(1) > eventEndDate
                    level = eventInfo.mesSpecification.level
                    mesId = eventInfo.mes.id
                    price  = evalPriceForMurmansk2015Hospital(self._contractDescr, self._tariff, eventId, eventTypeId, eventBegDate, eventEndDate, mesId, shortHospitalisation, level)
                    sum    = round(price, 2)
                    return sum
                elif self._tariffType in [CTariff.ttActionAmount, CTariff.ttActionUET] and eventInfo is not None and actionInfo is not None and eventInfo._loaded:
                    action = db.getRecord("vAction LEFT JOIN Person ON Person.id = vAction.person_id LEFT JOIN Event ON Event.id = vAction.event_id \
                            left join Client on Client.id = Event.client_id left join Account_Item ON Account_Item.event_id = Event.id and Account_Item.action_id = vAction.id \
                            and Account_Item.refuseType_id is not null and Account_Item.reexposeItem_id is null and Account_Item.deleted = 0 \
                            left join EventType on EventType.id = Event.eventType_id \
                            left join rbMedicalAidType on EventType.medicalAidType_id = rbMedicalAidType.id \
                            left join rbEventProfile ep on ep.id = EventType.eventProfile_id",
                          """Event.id as eventId, Event.setDate, Event.result_id, Event.eventType_id, Event.client_id, vAction.id, vAction.actionType_id, Event.eventType_id, 
                          vAction.event_id, vAction.exposeDate, vAction.amount, vAction.MKB, Person.tariffCategory_id, Event.execDate, 
                          Account_Item.id as oldAccId, Client.birthDate, vAction.org_id, rbMedicalAidType.regionalCode as matCode, ep.regionalCode as eventProfile""", actionInfo.id)
                    orgId = forceRef(action.value('org_id'))
                    exposeDate = forceDate(action.value('exposeDate'))
                    execDate = forceDate(action.value('execDate'))
                    # birthDate = forceDate(action.value('birthDate'))
                    setDate = forceDate(action.value('setDate'))
                    # MKB = forceString(action.value('MKB'))
                    # tariffCategoryId = forceRef(action.value('tariffCategory_id'))
                    # eventTypeId = forceRef(action.value('eventType_id'))
                    eventId = forceRef(action.value('eventId'))
                    serviceRecord = db.getRecord('rbService', ['infis', u"name like 'Обращен%' AS isObr"], self._serviceId)
                    serviceInfis = forceString(serviceRecord.value('infis'))
                    isObr = forceInt(serviceRecord.value('isObr'))
                    uet = amount * self._uet if self._tariffType == CTariff.ttActionUET else 0
                    medicalAidTypeCode = forceString(action.value('matCode'))
                    eventProfileRegionalCode = forceString(action.value('eventProfile'))
                    price = self._price
                    if not self._contractDescr:
                        self._contractDescr = getContractDescr(self._masterId)
                        self.exposeBySourceOrg, self.exposeByOncology, self.exposeByBatch, self.exposeByEvent, self.exposeByMonth, self.exposeByClient, self.exposeByInsurer = unpackExposeDiscipline(self._contractDescr.exposeDiscipline)

                    def getPayer(clientId, date, eventId=None):
                        from Registry.Utils import getClientCompulsoryPolicy

                        def getPayerId(insurerId):
                            result = None
                            if insurerId:
                                tmpInsurerId = insurerId
                                db = QtGui.qApp.db
                                table = db.table('Organisation')
                                if self.exposeByInsurer == 1:
                                    if forceString(db.translate(table, 'id', tmpInsurerId, 'area'))[:2] == QtGui.qApp.defaultKLADR()[:2]:
                                        while True:
                                            headId = forceRef(db.translate(table, 'id', tmpInsurerId, 'head_id'))
                                            if headId:
                                                tmpInsurerId = headId
                                            else:
                                                break
                                    else:
                                        tmpInsurerId = self._contractDescr.payerId
                                result = tmpInsurerId
                            return result

                        if clientId:
                            if QtGui.qApp.defaultKLADR()[:2] == u'23':
                                record = getClientCompulsoryPolicy(clientId, date, eventId)
                            else:
                                record = getClientCompulsoryPolicy(clientId)
                            if record:
                                insurerId = forceRef(record.value('insurer_id'))
                                insurerArea = forceString(record.value('area'))
                                return getPayerId(insurerId), insurerArea
                        return None, None

                    (payerId, insurerArea) = getPayer(eventInfo._clientId, execDate, eventId) if self.exposeByInsurer else (self._contractDescr.payerId, '00')

                    if orgId:
                        orgCode = forceString(db.translate('Organisation', 'id', orgId, 'infisCode'))
                        internalOrg = db.getCount("OrgStructure", "bookkeeperCode", "TRIM(bookkeeperCode) = '{0}'".format(orgCode))

                    if QtGui.qApp.defaultKLADR()[:2] == u'23':
                        isTwoYears = db.getCount(
                            "Action a left join ActionType at on at.id = a.actionType_id left join rbService s on s.id = at.nomenclativeService_id",
                            'a.id',
                            "a.event_id = %d and a.deleted = 0 and s.infis in ('B04.047.001.092', 'B04.026.001.093')" % eventId)
                        # с 2017-09-01 для инокраевых пациентов в пол-ках с прикрепленным населением меняем УОМП
                        if execDate >= QDate(2017, 9, 1) and medicalAidTypeCode in ['271', '272'] and payerId == self._contractDescr.payerId:
                            medicalAidTypeCode = '21' if medicalAidTypeCode == '271' else '22'
                        # тарификация услуг обращения/посещения для поликлиники
                        if execDate >= QDate(2019, 3, 1) and medicalAidTypeCode in ['21', '22'] and serviceInfis[:3] in ['B01', 'B02', 'B04', 'B05'] \
                                and not isObr and db.getCount(u"""Event e
                                    LEFT JOIN soc_obr u ON u.spec = '{codeSpec}'
                                    left join rbService rs on rs.infis in (u.kusl, u.kusl2)
                                    left join ActionType at on at.nomenclativeService_id = rs.id
                                    left join Action a on a.event_id = e.id and a.actionType_id = at.id""".format(codeSpec=serviceInfis[4:7]),
                                    "a.id",
                                    "e.id = {aEvent_id} and e.deleted = 0 and a.deleted = 0".format(aEvent_id=eventId)):
                            price = 0
                        # для ранее оказанных и внешних услуг  - цена равна 0
                        elif setDate > exposeDate and not isTwoYears or orgId and medicalAidTypeCode != '211' or orgId and not internalOrg:
                            price = 0
                        # обнуление простых услуг для детских профосмотров
                        elif medicalAidTypeCode in ['232', '252', '262'] and execDate >= QDate(2019, 3, 1) and serviceInfis[:7] not in ['B04.031', 'B04.026']:
                            price = 0
                        elif medicalAidTypeCode in ['232', '252', '262'] and execDate < QDate(2019, 3, 1) and serviceInfis[:3] not in ['B01', 'B04'] and uet == 0:
                            price = 0
                        # обнуление простых услуг для дисп. взрослых
                        elif medicalAidTypeCode == '261' and execDate >= QDate(2019, 3, 1) and serviceInfis[:7] not in ['B04.047', 'B04.026']:
                            price = 0
                        elif medicalAidTypeCode == '261' and execDate < QDate(2019, 3, 1) and serviceInfis[:3] not in ['B01', 'B04']:
                            price = 0
                        # обнуление стоимости услуг для выполненного этапа взрослой дисп.
                        elif medicalAidTypeCode == '211' and eventProfileRegionalCode in ['8008', '8014']:
                            isCompleted = not db.getCount("Action a left join ActionType at on at.id = a.actionType_id left join rbService s on s.id = at.nomenclativeService_id",
                                'a.id',
                                "a.event_id = %d and a.deleted = 0 and s.infis in ('B04.026.001.062', 'B04.047.001.061', 'B04.047.001.092', 'B04.026.001.093')" % eventId)
                            if isCompleted:
                                if serviceInfis[:7] not in ['B04.026', 'B04.047']:
                                    price, sum = 0, 0
                        # обнуление стоимости у краевых застрахованных участковой службы
                        elif medicalAidTypeCode in ['271', '272'] and exposeDate >= QDate(2017, 1, 1) and payerId != self._contractDescr.payerId:
                            price = 0
                        # обнуление стоимости для ковидной диспансеризации
                        elif medicalAidTypeCode == '233' and serviceInfis in ['B04.047.002', 'B04.047.004', 'B04.026.002']:
                            price = 0
                    return price * amount
                else:
                    return self._price * amount
        return 0
