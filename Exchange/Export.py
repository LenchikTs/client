# -*- coding: utf-8 -*-
#pylint: disable=R0921
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Абстрактные классы экспорта реестров счетов,
    примесевый класс экспорта данных с кэшированием."""

import os
import shutil

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, QTime, pyqtSignature, SIGNAL

from library.Utils import (
    forceDate, forceDouble, forceRef, forceString, forceStringEx, toVariant,
    trim, forceInt, formatShortName)

from Registry.Utils import getAttachRecord
from Events.Action import CAction
from Exchange.Utils import getClientRepresentativeInfo
from Exchange.Ui_ExportPage2 import Ui_ExportPage2

# ******************************************************************************

def record2Dict(record):
    result = {}
    for i in range(record.count()):
        result[forceString(record.fieldName(i))] = record.value(i)
    return result

# ******************************************************************************

class CExportHelperMixin(object):
    u'Класс часто используемых функций экспорта'
    sexMap = {1: u'М', 2: u'Ж'}

    def __init__(self):
        self._accSysIdToUrnCache = {}
        self._accSysIdToCodeCache = {}
        self._actionPropertyCache = {}
        self._actionPropertyTypeCache = {}
        self._actionPropertyValueCache = {}
        self._clientAttachCache = {}
        self._contractAttributeCache = {}
        self._contractAttributeTypeCache = {}
        self._hospitalBedProfileRegionalCodeCache = {}
        self._hospitalBedProfileTfomsCodeCache = {}
        self._hospitalBedProfileUsishCodeCache = {}
        self._hospitalBedProfileCodeCache = {}
        self._rbSpecialityFederalCodeCache = {}
        self._hospitalBedProfileMedicalAidProfileCache = {}
        self._hospitalBedProfileId = {}
        self._hospitalBedTypeCodeCache = {}
        self._hospitalBedTypeId = {}
        self._medicalAidProfileFederalCodeCache = {}
        self._medicalAidProfileRegionalCodeCache = {}
        self._medicalAidTypeRegionalCodeCache = {}
        self._okatoCache = {}
        self._orgCodesCache = {}
        self._orgInfisCodeCache = {}
        self._orgStructBookkeeperCodeCache = {}
        self._orgStructureInfisCodeCache = {}
        self._orgStructureTfomsCodeCache = {}
        self._orgStructureInfisDepTypeCodeCache = {}
        self._orgStructureInfisInternalCodeCache = {}
        self._personNameCache = {}
        self._personSpecialityRegionalCodeCache = {}
        self._personSpecialityFederalCodeCache = {}
        self._personRegionalCodeCache = {}
        self._personFederalCodeCache = {}
        self._personOrgStructureInfisCache = {}
        self._personOrgStructureInfisDepTypeCache = {}
        self._personOrgStructureIdCache = {}
        self._representativeInfoCache = {}
        self._regionCenterNameCache = {}
        self._regionNameCache = {}
        self._specialityRegionalCodeCache = {}
        self._specialityFederalCodeCache = {}
        self._serviceCodeCache = {}
        self._serviceInfisCache = {}
        self._specialityCache = {}
        self._serviceToMedicalAidTypeIdCache = {}
        self._serviceToMedicalAidProfileIdCache = {}
        self._toothNumberCache = {}
        self._KRITCode = {}
        self._db = QtGui.qApp.db
        self._tblAccountingSystem = self._db.table('rbAccountingSystem')
        self._tblOrgIdentification = self._db.table(
            'Organisation_Identification')


    def getTableFieldById(self, _id, tableName, fieldName, cacheDict,
                          idFieldName='id'):
        u'''Получает поле из таблицы по имени и идентификатору.
            Результат кэшируется.'''
        result = cacheDict.get(_id, -1)

        if result == -1:
            result = self._db.translate(tableName, idFieldName, _id, fieldName)
            cacheDict[_id] = result

        return result


    def getClientRepresentativeInfo(self, clientId):
        u'''Возвращает информацию о представителе клиента.'''

        key = clientId
        result = self._representativeInfoCache.get(key)

        if not result:
            result = getClientRepresentativeInfo(clientId)
            self._representativeInfoCache[key] = result

        return result


    def getAttachRecord(self, clientId, isTemporary):
        u'''Возвращает словарь с иноформацией о прикреплении пациента
        или None, если прикрепление не найдено'''

        key = (clientId, isTemporary)
        result = self._clientAttachCache.get(key)

        if not result:
            result = getAttachRecord(clientId, isTemporary)
            self._clientAttachCache[key] = result

        return result


    def _getAccSysId(self, code, domain=None):
        key = (code, domain)
        result = self._accSysIdToUrnCache.get(key, -1)
        if result == -1:
            cond = [self._tblAccountingSystem['code'].eq(code)]
            if domain:
                cond.append(self._tblAccountingSystem['domain'].eq(domain))
            record = self._db.getRecordEx(
                self._tblAccountingSystem, 'id', where=cond)
            result = forceRef(record.value(0)) if record else 0
            self._accSysIdToUrnCache[key] = result
        return result


    def _getAccSysIdByUrn(self, urn):
        result = self._accSysIdToUrnCache.get(urn, -1)
        if result == -1:
            record = self._db.getRecordEx(
                self._tblAccountingSystem, 'id',
                where=self._tblAccountingSystem['urn'].like(urn))
            result = forceRef(record.value(0)) if record else 0
            self._accSysIdToUrnCache[urn] = result
        return result


    def _getIdentification(self, tablePrefix, _id, sysId):
        _tbl = self._db.table('{0}_Identification'.format(tablePrefix))
        cond = [_tbl['master_id'].eq(_id), _tbl['system_id'].eq(sysId),
                _tbl['deleted'].eq(0)]
        record = self._db.getRecordEx(_tbl, 'value', where=cond)
        result = forceString(record.value(0)) if record else ''
        return result


    def _getOrgIdentification(self, orgId, sysId):
        _tbl = self._tblOrgIdentification
        cond = [_tbl['master_id'].eq(orgId), _tbl['system_id'].eq(sysId),
                _tbl['deleted'].eq(0)]
        record = self._db.getRecordEx(_tbl, 'value', where=cond)
        result = forceString(record.value(0)) if record else ''
        return result


    def getRegionCenterName(self, code):
        u'Возвращает название регионального центра.'

        result = self._regionCenterNameCache.get(code)

        if not result:
            result = ''

            stmt = '''SELECT `NAME` FROM kladr.KLADR
            WHERE `CODE` LIKE '%s%%' AND `STATUS` IN ('2','3')
            ''' % code[:2]

            query = self._db.query(stmt)

            while query.next():
                record = query.record()

                if record:
                    result = forceString(record.value(0))

            self._regionCenterNameCache[code] = result

        return result


    def getRegionName(self, code):
        u'Возвращает название района. Области отфильтровываются.'

        result = self._regionNameCache.get(code)

        if not result:
            if code != '':
                regionCode = code[:5].ljust(13, '0')
                result = (forceString(self._db.translate('kladr.KLADR', 'CODE',
                    regionCode, 'NAME')) if regionCode[2:5] != '000' else
                        self.getRegionCenterName(code))
            else:
                result = ''

            self._regionNameCache[code] = result

        return result


    def getRegionOKATO(self, subRegionOKATO):
        u'Определяем ОКАТО региона по ОКАТО района через КЛАДР.'
        result = self._okatoCache.get(subRegionOKATO, -1)

        if result == -1:
            result = ''
            kladrCode = forceString(self._db.translate(
                'kladr.KLADR', 'OCATD', subRegionOKATO, 'CODE'))

            if kladrCode:
                result = forceString(self._db.translate(
                    'kladr.KLADR', 'CODE', kladrCode[:2].ljust(13, '0'),
                    'OCATD')).ljust(5, '0') if kladrCode else ''

            self._okatoCache[subRegionOKATO] = result

        return result


    def getServiceMedicalAidTypeId(self, serviceId):
        u'''Получает идентификатор типа медицинской помощи по
        идентификатору услуги.'''
        return forceRef(self.getTableFieldById(serviceId, 'rbService',
                    'medicalAidType_id', self._serviceToMedicalAidTypeIdCache))


    def getServiceMedicalAidProfileId(self, serviceId):
        u'''Получает идентификатор профиля медицинской помощи по
        идентификатору услуги.'''
        return forceRef(self.getTableFieldById(serviceId, 'rbService',
                    'medicalAidProfile_id', self._serviceToMedicalAidProfileIdCache))


    def getMedicalAidTypeRegionalCode(self, _id):
        u"""Возвращает региональный код типа медицинской помощи
        по идентификатору типа."""
        return forceString(self.getTableFieldById(_id, 'rbMedicalAidType',
                        'regionalCode', self._medicalAidTypeRegionalCodeCache))


    def getHospitalBedProfileId(self, _id):
        u"""Получает по id койки id ее профиля"""
        return forceRef(self.getTableFieldById(_id, 'OrgStructure_HospitalBed',
                        'profile_id', self._hospitalBedProfileId))


    def getKRITCode(self, _id):
        u"""Получает по id койки id ее профиля"""
        return forceString(self.getTableFieldById(_id, 'soc_spr80', 'code', self._KRITCode))


    def getHospitalBedTypeId(self, _id):
        u"""Получает по id койки id ее типа"""
        return forceRef(self.getTableFieldById(_id, 'OrgStructure_HospitalBed',
                        'type_id', self._hospitalBedTypeId))


    def getHospitalBedProfileRegionalCode(self, _id):
        u"""Получает по id профиля койки его региональный код"""
        return forceString(self.getTableFieldById(_id, 'rbHospitalBedProfile',
                    'regionalCode', self._hospitalBedProfileRegionalCodeCache))


    def getHospitalBedProfileTfomsCode(self, _id):
        u"""Получает по id профиля койки его региональный код"""
        return forceString(self.getTableFieldById(_id, 'rbHospitalBedProfile',
                    'tfomsCode', self._hospitalBedProfileTfomsCodeCache))


    def getHospitalBedProfileUsishCode(self, _id):
        u"""Получает по id профиля койки его региональный код"""
        return forceString(self.getTableFieldById(_id, 'rbHospitalBedProfile',
                    'usishCode', self._hospitalBedProfileUsishCodeCache))


    def getHospitalBedProfileCode(self, _id):
        u"""Получает по id профиля койки его код"""
        return forceString(self.getTableFieldById(_id, 'rbHospitalBedProfile',
                        'code', self._hospitalBedProfileCodeCache))


    def getSpecialityFederalCode(self, _id):
        u"""Получает по id специальности ее федеральный код"""
        return forceString(
            self.getTableFieldById(_id, 'rbSpeciality', 'federalCode', self._rbSpecialityFederalCodeCache))


    def getHospitalBedProfileMedicalAidProfileId(self, _id):
        u"""Получает по id профиля койки его код"""
        return forceString(self.getTableFieldById(
            _id, 'rbHospitalBedProfile', 'medicalAidProfile_id',
            self._hospitalBedProfileMedicalAidProfileCache))


    def getHospitalBedTypeCode(self, _id):
        u"""Получает по id типа койки его код"""
        return forceString(self.getTableFieldById(_id, 'rbHospitalBedType',
                        'code', self._hospitalBedTypeCodeCache))


    def getPersonSpecialityId(self, personId):
        u"""Определяем id специальности врача по его id"""
        return forceRef(self.getTableFieldById(personId, 'Person',
                        'speciality_id', self._specialityCache))


    def getPersonName(self, _id):
        u"""Получает ФИО сотрудника по его id"""
        return forceString(self.getTableFieldById(_id, 'vrbPerson',
                        'name', self._personNameCache))


    def getOrgInfisCode(self, _id):
        u"""Получает инфис код организации по его id"""
        return forceString(self.getTableFieldById(_id, 'Organisation',
                        'infisCode', self._orgInfisCodeCache))


    def getOrgStructureBookkeeperCode(self, _id):
        u"""Получает код для бухгалтерии по id отделения"""
        result = self._orgStructBookkeeperCodeCache.get(_id, -1)

        if result == -1:
            stmt = u"""select IF(length(trim(os.bookkeeperCode))=5, os.bookkeeperCode,
                        IF(length(trim(destParent1.bookkeeperCode))=5, destParent1.bookkeeperCode,
                          IF(length(trim(destParent2.bookkeeperCode))=5, destParent2.bookkeeperCode,
                            IF(length(trim(destParent3.bookkeeperCode))=5, destParent3.bookkeeperCode,
                              IF(length(trim(destParent4.bookkeeperCode))=5, destParent4.bookkeeperCode, destParent5.bookkeeperCode)))))
                        FROM OrgStructure as os
                        left join OrgStructure as destParent1 on destParent1.id = os.parent_id
                        left join OrgStructure as destParent2 on destParent2.id = destParent1.parent_id
                        left join OrgStructure as destParent3 on destParent3.id = destParent2.parent_id
                        left join OrgStructure as destParent4 on destParent4.id = destParent3.parent_id
                        left join OrgStructure as destParent5 on destParent5.id = destParent4.parent_id
                        where os.id = {0}""".format(_id)
            query = self._db.query(stmt)
            if query.first():
                record = query.record()
                if record:
                    result = record.value(0)
            self._orgStructBookkeeperCodeCache[_id] = result
        return forceString(result)


    def getOrgStructureInfisCode(self, _id):
        u"""Получает инфис код отделения по его id"""
        return forceString(self.getTableFieldById(_id, 'OrgStructure',
                        'infisCode', self._orgStructureInfisCodeCache))


    def getOrgStructureTfomsCode(self, _id):
        u"""Получает инфис код отделения по его id"""
        return forceString(self.getTableFieldById(_id, 'OrgStructure',
                        'tfomsCode', self._orgStructureTfomsCodeCache))


    def getOrgStructureInfisInternalCode(self, _id):
        u"""Получает инфис код отделения по его id"""
        return forceString(self.getTableFieldById(_id, 'OrgStructure',
                'infisInternalCode', self._orgStructureInfisInternalCodeCache))


    def getOrgStructureInfisDepTypeCode(self, _id):
        u"""Получает инфис код отделения по его id"""
        return forceString(self.getTableFieldById(_id, 'OrgStructure',
                'infisDepTypeCode', self._orgStructureInfisDepTypeCodeCache))


    def getPersonSpecialityRegionalCode(self, personId):
        u"""Определяем региональный код специальности врача по его id"""
        result = self._personSpecialityRegionalCodeCache.get(personId, -1)

        if result == -1:
            result = None
            specialityId = self.getPersonSpecialityId(personId)

            if specialityId:
                result = forceString(self._db.translate('rbSpeciality', 'id',
                                                specialityId, 'regionalCode'))

            self._personSpecialityRegionalCodeCache[personId] = result

        return result


    def getSpecialityRegionalCode(self, _id):
        u"""Получает федеральный код специальности по его id"""
        return forceString(
            self.getTableFieldById(_id, 'rbSpeciality', 'regionalCode', self._specialityRegionalCodeCache))


    def getPersonSpecialityFederalCode(self, personId):
        u"""Определяем федеральный код специальности врача по его id"""
        result = self._personSpecialityFederalCodeCache.get(personId, -1)

        if result == -1:
            result = None
            specialityId = self.getPersonSpecialityId(personId)

            if specialityId:
                result = forceString(self._db.translate('rbSpeciality', 'id',
                                                specialityId, 'federalCode'))

            self._personSpecialityFederalCodeCache[personId] = result

        return result


    def getPersonRegionalCode(self, personId):
        u"""Определяем региональный код врача по его id"""
        return forceString(self.getTableFieldById(personId, 'Person',
                'regionalCode', self._personRegionalCodeCache))


    def getPersonFederalCode(self, personId):
        u"""Определяем федеральный код врача по его id"""
        return forceString(self.getTableFieldById(personId, 'Person',
                'federalCode', self._personFederalCodeCache))


    def getServiceCode(self, _id):
        u"""Определяем код профиля оплаты по его id"""
        result = self._serviceCodeCache.get(_id, -1)

        if result == -1:
            result = forceString(self._db.translate('rbService', 'id', _id,
                'code'))
            self._serviceCodeCache[_id] = result

        return result


    def getServiceInfis(self, _id):
        u"""Определяем инфис код профиля оплаты по его id"""
        result = self._serviceInfisCache.get(_id, -1)

        if result == -1:
            result = forceString(self._db.translate('rbService', 'id', _id,
                'infis'))
            self._serviceInfisCache[_id] = result

        return result


    def getMedicalAidProfileFederalCode(self, _id):
        u"""Определяем федеральный код профиля мед. помощи по его id"""
        result = self._medicalAidProfileFederalCodeCache.get(_id, -1)

        if result == -1:
            result = forceString(self._db.translate('rbMedicalAidProfile',
                'id', _id, 'federalCode'))
            self._medicalAidProfileFederalCodeCache[_id] = result

        return result


    def getMedicalAidProfileRegionalCode(self, _id):
        u"""Определяем региональный код профиля мед. помощи по его id"""
        result = self._medicalAidProfileRegionalCodeCache.get(_id, -1)

        if result == -1:
            result = forceString(self._db.translate('rbMedicalAidProfile',
                'id', _id, 'regionalCode'))
            self._medicalAidProfileRegionalCodeCache[_id] = result

        return result


    def getActionPropertyText(self, eventId, actionTypeId, name):
        u"""Возвращает строку, содержащую текствое свойство действия
        по идентификатору события, типа действия и имени свойства"""
        key = (eventId, actionTypeId, name)
        result = self._actionPropertyCache.get(key, -1)

        if result == -1:
            result = ''

            if actionTypeId and eventId and name:
                table = self._db.table('Action')
                record = self._db.getRecordEx(table, '*', [
                    table['event_id'].eq(eventId),
                    table['actionType_id'].eq(actionTypeId)])

                if record:
                    action = CAction(record=record)
                    prop = action.getProperty(name)

                    if prop:
                        val = prop.getTextScalar()
                        result = val if val else ''

            self._actionPropertyCache[key] = result

        return result


    def getActionPropertyValue(self, eventId, actionTypeId, name):
        u"""Возвращает значение свойства действия по идентификатору
            события, типа действия и имени свойства"""
        key = (eventId, actionTypeId, name)
        result = self._actionPropertyValueCache.get(key, -1)

        if result == -1:
            result = None

            if actionTypeId and eventId and name:
                table = self._db.table('Action')
                record = self._db.getRecordEx(table, '*', [
                    table['event_id'].eq(eventId),
                    table['actionType_id'].eq(actionTypeId)])

                if record:
                    action = CAction(record=record)
                    prop = action.getProperty(name)

                    if prop:
                        result = prop.getValueScalar()

            self._actionPropertyValueCache[key] = result

        return result


    def getActionPropertyTypeIdByName(self, actionTypeId, name):
        u"""Получаем id типа свойства действия по id типа действия
        и имени свойства"""

        key = (actionTypeId, name)
        result = self._actionPropertyTypeCache.get(key, -1)

        if result == -1:
            result = None
            tableActionPropertyType = self._db.table('ActionPropertyType')
            cond = []

            cond.append(tableActionPropertyType['name'].eq(name))
            cond.append(tableActionPropertyType['deleted'].eq(0))
            cond.append(tableActionPropertyType['actionType_id'].eq(
                                                                actionTypeId))

            record = self._db.getRecordEx(tableActionPropertyType, 'id', cond)

            if record:
                result = forceRef(record.value(0))

            self._actionPropertyTypeCache[key] = result

        return result


    def getPersonOrgStructreId(self, personId):
        u"""Возвращет id подразделения сотрудника"""
        result = self._personOrgStructureIdCache.get(personId, -1)

        if result == -1:
            result = forceRef(self._db.translate(
                'Person', 'id', personId, 'orgStructure_id'))
            self._personOrgStructureIdCache[personId] = result

        return result


    def getPersonOrgStructreInfis(self, personId):
        u"""Возвращет код подразделения сотрудника"""
        result = self._personOrgStructureInfisCache.get(personId, -1)

        if result == -1:
            result = None
            orgStructureId = self.getPersonOrgStructreId(personId)

            if orgStructureId:
                result = self.getOrgStructureInfisCode(orgStructureId)

            self._personOrgStructureInfisCache[personId] = result

        return result


    def getPersonOrgStructreInfisDepType(self, personId):
        u"""Возвращет код типа подразделения сотрудника"""
        result = self._personOrgStructureInfisDepTypeCache.get(personId, -1)

        if result == -1:
            result = None
            orgStructureId = self.getPersonOrgStructreId(personId)

            if orgStructureId:
                result = self.getOrgStructureInfisDepTypeCode(orgStructureId)

            self._personOrgStructureInfisCache[personId] = result

        return result


    def _getAttachOrgCodes(self, orgId):
        u"""Возвращает словарь с тремя кодами: инфис, смо, тфомс"""
        result = self._orgCodesCache.get(orgId)

        if not result:
            record = self._db.getRecord('Organisation',
                'infisCode,smoCode,tfomsExtCode', orgId)
            result = {
                'attachOrgCode': forceString(record.value('infisCode')),
                'attachOrgSmoCode': forceString(record.value('smoCode')),
                'attachOrgTfomsExtCode': forceString(record.value(
                    'tfomsExtCode'))
            } if record else {}
            self._orgCodesCache[orgId] = result

        return result


    def toothNumber(self, actionId):
        u"""Возвращает номер зуба по идентификатору действия"""

        result = self._toothNumberCache.get(actionId, -1)

        if result == -1:
            result = ''
            action = CAction.getActionById(actionId)
            if action:
                try:
                    result = action[u'№ зуба']

                    if not result:
                        result = ''

                except KeyError:
                    self.logWarning(u'Для действия id=%d отсутствует свойство'
                        u' "№ зуба"' % actionId)
            self._toothNumberCache[actionId] = result
        return result

    def contractAttributeTypeId(self, code):
        u"""Получает идентификатор типа параметра договора по его коду"""
        result = self._contractAttributeTypeCache.get(code, -1)

        if result == -1:
            result = forceRef(self._db.translate(
                    'rbContractAttributeType', 'code', code, 'id'))
            self._contractAttributeTypeCache[code] = result

        return result


    def contractAttribute(self, contractId, attributeId):
        u"""Получает значение параметра договора по идентификатору типа"""
        result = self._contractAttributeCache.get(attributeId, -1)

        if result == -1:
            result = None
            table = self._db.table('Contract_Attribute')
            cond = [table['master_id'].eq(contractId),
                table['deleted'].eq(0),
                table['attributeType_id'].eq(attributeId)]

            record = self._db.getRecordEx(table, 'value', cond)

            if record:
                result = forceString(record.value(0)).replace(',','.')

            self._contractAttributeCache[attributeId] = result

        return result


    def contractAttributeByType(self, code, contractId):
        u"""Возвращает параметр договора по коду типа"""
        return self.contractAttribute(contractId,
                                      self.contractAttributeTypeId(code))


    def _getChiefName(self, orgId):
        u"""Возвращает Ф.И.О руководителя организации"""
        result = None
        personId = forceRef(self._db.translate(
            'Organisation', 'id', orgId, 'chief_id'))
        if personId:
            record = self._db.getRecord('Person',
                'firstName,patrName,lastName', personId)
            if record:
                result = formatShortName(record.value('lastName'),
                                         record.value('firstName'),
                                         record.value('patrName'))
        if not result:
            result = forceString(self._db.translate(
                'Organisation', 'id', orgId, 'chiefFreeInput'))
        return result

# ******************************************************************************

class LoggerMixin(object):
    u'Примесевый класс для вывода сообщений в журнал QTextbrowser logBrowser'

    def log(self, _str, forceLog=False):
        if not hasattr(self, 'logBrowser'):
            return

        if hasattr(self, 'chkVerboseLog'):
            verboseLog = self.chkVerboseLog.isChecked()
        else:
            verboseLog = True

        if verboseLog or forceLog:
            timeStr = forceString(QTime.currentTime().toString('hh:mm:ss'))
            self.logBrowser.append('[%s] %s' % (timeStr, _str))
            self.logBrowser.update()


    def logWarning(self, _str):
        self.log(u'<font color=orange><b>Предупреждение</b></font>: %s' % _str,
            forceLog=True)


    def logError(self, _str):
        self.log(u'<font color=red><b>ОШИБКА</b></font>: %s' % _str,
            forceLog=True)


    def logInfo(self, _str, forceLog=False):
        self.log(u'<font color=green><b>ИНФО</b></font>: %s' % _str, forceLog)

# ******************************************************************************

class CAbstractExportWizard(QtGui.QWizard):
    u"""Родительский класс мастера экспорта счетов."""

    def __init__(self, parent=None, title=''):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowTitle(title)
        self.dbfFileName = ''
        self.tmpDir = ''
        self.db = QtGui.qApp.db
        self.info = {}
        self.accountId = None


    def setAccountId(self, accountId):
        u"""Устанавливает счета для экспорта по его идентификатору"""
        if hasattr(self, 'page1'):
            self.accountId = accountId

            self.info = self.getAccountInfo(accountId)
            date = self.info.get('accDate', QDate())
            number = self.info.get('accNumber', '')

            strNumber = number if trim(number) else u'б/н'
            strDate = forceString(date) if date else u'б/д'
            self.page1.setTitle(u'Экспорт данных реестра по счёту'
                u' №%s от %s' % (strNumber, strDate))

        if hasattr(self, 'page2'):
            self.page2.setTitle(u'Укажите директорий для сохранения '
                u'обменных файлов "*.dbf"')


    def setAccountExposeDate(self):
        u"""Меняет дату выставления счета на текущую"""
        accountRecord = self.db.table('Account').newRecord(['id', 'exposeDate'])
        accountRecord.setValue('id', toVariant(self.accountId))
        accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
        self.db.updateRecord('Account', accountRecord)


    def getTmpDir(self):
        u"""Возвращает строку с путем к временному каталогу"""
        return self.getTmpDirEx('EXPORT')


    def getTmpDirEx(self, prefix):
        u"""Возвращает строку с путем к временному каталогу с учетом префикса"""
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir(prefix)
        return self.tmpDir


    def getFullDbfFileName(self):
        u"""Возвращает полный путь к DBF файлу"""
        return os.path.join(self.getTmpDir(), self.dbfFileName + '.dbf')


    def setAccountItemsIdList(self, accountItemIdList):
        u"""Устанавливает список элементов реестра счета"""
        self.page1.setAccountItemsIdList(accountItemIdList)


    def cleanup(self):
        u"""Удаляет временный каталог при его наличии"""
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def exec_(self):
        u"""Запускает диалог мастера экспорта, по окончании работы
        вызывает метод cleanup()"""
        QtGui.QWizard.exec_(self)
        self.cleanup()


    def getAccountInfo(self, accountId):
        u"""Возвращает словарь с данными о счете по его идентификатору"""
        result = {}
        record = self.db.getRecord('Account', 'id, date, number, exposeDate, '
            'contract_id, payer_id, settleDate, personalDate, note, sum, '
            'orgStructure_id, amount, type_id', accountId)

        if record:
            result['accDate'] = forceDate(record.value('date'))
            result['exposeDate'] = forceDate(record.value('exposeDate'))
            result['accNumber'] = forceString(record.value('number'))
            result['contractId'] = forceRef(record.value('contract_id'))
            result['payerId'] = forceRef(record.value('payer_id'))
            result['settleDate'] = forceDate(record.value('settleDate'))
            result['personalDate'] = forceDate(record.value('personalDate'))
            result['note'] = forceString(record.value('note'))
            result['accSum'] = forceDouble(record.value('sum'))
            result['accId'] = forceRef(record.value('id'))
            result['typeId'] = forceRef(record.value('type_id'))
            result['accOrgStructureId'] = forceRef(record.value('orgStructure_id'))
            result['accAmount'] = forceInt(record.value('amount'))

        return result

# ******************************************************************************

class CAbstractExportPage1Common(QtGui.QWizardPage, LoggerMixin):
    u"""Абстрактная страница 1 мастера экспорта счетов.
        Для работы необходимо реализовать следующие функции:
            setExportMode(flag)
            createDbf()
            createQuery()
            process()
        Имя для индикатора прогресса: progressBar
        Имя журнала ошибок: logBrowser
        Имя checkbox'a включающего подробный журнал ошибок: chkVerboseLog
        """
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        LoggerMixin.__init__(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "экспорт"')
        self.setupUi(self)

        if hasattr(self, 'progressBar'):
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(1)
            self.progressBar.setText('')

        self.setExportMode(False)
        self.aborted = False
        self.done = False
        self.idList = []
        self._parent = parent
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.db = QtGui.qApp.db
        self.tableAccountItem = self.db.table('Account_Item')
        self._processParams = {}
        self._processFuncList = []

        if hasattr(self, 'lblRevision'):
            try:
                from s11main import gLastChangedRev
                self.lblRevision.setText(u'рев. %s' % gLastChangedRev)
            except:
                pass


    def setExportMode(self, flag):
        """Выключаем элементы управления, если flag == True,
        иначе -- включаем. Абстрактный метод."""
        raise NotImplementedError


    def validatePage(self):
        return self.done


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        dest = self.createExportDest()

        try:
            from s11main import (gTitle, gVersion,
                 gLastChangedRev, gLastChangedDate)
            self.log(u'<font color=blue>%s, вер. %s (рев. <b>%s</b> от '
                u'<b>%s</b>)</font>' % (gTitle, gVersion, gLastChangedRev,
                    gLastChangedDate))
        except:
            pass

        self.log(u'Запрос в БД...')
        if hasattr(self, 'progressBar'):
            self.progressBar.reset()
            self.progressBar.setMaximum(1)
            self.progressBar.setValue(0)
            self.progressBar.setText(u'Запрос в БД...')

        QtGui.qApp.processEvents()
        query = QtGui.qApp.callWithWaitCursor(self, self.createQuery)

        if hasattr(self, 'progressBar'):
            querySize = 0

            if isinstance(query, list) or isinstance(query, tuple):
                for item in query:
                    if callable(item):
                        continue

                    querySize += item.size()
            else:
                querySize = query.size()

            self.log(u'Получено {0} записей из БД'.format(querySize))
            self.progressBar.setMaximum(max(querySize, 1))
            self.progressBar.reset()
            self.progressBar.setValue(0)

        return dest, query


    def export(self):
        self._processParams = {}
        (result, _) = QtGui.qApp.call(self, self.exportInt)
        self.setExportMode(False)

        if self.aborted or not result:
            if hasattr(self, 'progressBar'):
                self.progressBar.setText(u'прервано')
            self.log(u'Прервано')
        else:
            if hasattr(self, 'progressBar'):
                self.progressBar.setText(u'готово')
            self.log(u'Успешно завершено')
            self.done = True
            self.emit(SIGNAL('completeChanged()'))


    def _processQuery(self, dest, query, func, time, startPos):
        while query.next():
            QtGui.qApp.processEvents()

            if self.aborted:
                break

            if hasattr(self, 'progressBar'):
                self.progressBar.step()

            func(dest, query.record(), self._processParams)

            if hasattr(self, 'progressBar') and hasattr(self, 'lblElapsed'):
                elapsed = time.elapsed()

                if elapsed != 0 and (self.progressBar.value()-startPos > 100):
                    startPos = self.progressBar.value()
                    oldSpeed = 100*1000/elapsed
                    newSpeed = (oldSpeed+100*1000/elapsed)/2
                    if newSpeed != 0:
                        finishTime = QTime.currentTime().addSecs(
                             self.progressBar.maximum()/newSpeed)
                        self.lblElapsed.setText(u'Текущая операция: %03.f '
                            u'зап/с, окончание в %s' % (
                              newSpeed, finishTime.toString('hh:mm:ss')))
                        time.restart()


    def preprocessQuery(self, query, params):
        pass


    def postExport(self):
        pass


    def preExport(self):
        pass


    def exportInt(self):
        dest, query = self.prepareToExport()
        time = QTime()
        startPos = 0
        self.log(u'Обработка результатов...')
        self.preprocessQuery(query, self._processParams)

        if (hasattr(self, 'lblElapsed') and hasattr(self, 'progressBar')
                and (self.progressBar.maximum() > 100)):
            self.lblElapsed.setText(
                u'Текущая операция: ??? зап/с, окончание в ??:??:??')
            time.start()

        self.preExport()

        if self.idList:
            if ((isinstance(query, list) or isinstance(query, tuple)) and
                    self._processFuncList != []):
                for (q, f) in zip(query, self._processFuncList):
                    if callable(q):
                        q = q()
                    self._processQuery(dest, q, f, time, startPos)
            else:
                self._processQuery(dest, query, self.process, time, startPos)

        else:
            self.log(u'Нечего выгружать.')

            if hasattr(self, 'progressBar'):
                self.progressBar.step()

        self.postExport()

        if isinstance(dest, (list, tuple)):
            for item in dest:
                if item is not None:
                    item.close()
        else:
            dest.close()


    def setProcessParams(self, params):
        self._processParams = params


    def processParams(self):
        return self._processParams


    def setProcessFuncList(self, funcList):
        self._processFuncList = list(funcList)


    def process(self, dest, record, params):
        raise NotImplementedError


    def prepareStmt(self, params):
        u'Возращает tuple из строк select, таблицы, where, orderBy'
        raise NotImplementedError


    def createQuery(self):
        (select, tables, where, orderBy) = self.prepareStmt(self._processParams)
        stmt = (u'SELECT {select} FROM {table}\n'
            u'WHERE {where} ORDER BY {orderBy}').format(
            select=select, table=tables, where=where, orderBy=orderBy)
        return self.db.query(stmt)


    def createExportDest(self):
        raise NotImplementedError


    def isComplete(self):
        return self.done


    def abort(self):
        self.aborted = True


    def getTmpDir(self):
        return self._parent.getTmpDir()


    def accountInfo(self):
        return self._parent.info


    def accountId(self):
        return self._parent.accountId


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        self.export()


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.abort()


    def getEventSum(self):
        u"""Возвращает общую стоимость услуг за событие"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.`sum`) AS totalSum
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result[eventId] = forceDouble(record.value(1))

        return result


    def getEventCount(self):
        u"""Возвращает строкой количество событий в счете."""

        result = u''
        stmt = """SELECT COUNT(DISTINCT Account_Item.event_id)
        FROM Account_Item
        WHERE %s""" % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)

        if query.first():
            record = query.record()
            result = forceString(record.value(0))

        return result


    def getCompleteEventSum(self):
        u"""Возвращает общую стоимость услуг за событие"""

        stmt = """SELECT getLastEventId(Account_Item.event_id) AS lastEventId,
            SUM(Account_Item.`sum`) AS totalSum
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY lastEventId;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result[eventId] = forceDouble(record.value(1))

        return result


    def getCompleteEventCount(self):
        u"""Возвращает строкой количество событий в счете."""

        result = u''
        stmt = """SELECT COUNT(DISTINCT getLastEventId(Account_Item.event_id))
        FROM Account_Item
        WHERE %s""" % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)

        if query.first():
            record = query.record()
            result = forceString(record.value(0))

        return result

# ******************************************************************************

class CAbstractExportPage1(CAbstractExportPage1Common):
    def __init__(self, parent):
        CAbstractExportPage1Common.__init__(self, parent)


    def createExportDest(self):
        return self.createDbf()


    def createDbf(self):
        raise NotImplementedError

# ******************************************************************************

class CAbstractExportPage1Xml(CAbstractExportPage1Common):
    def __init__(self, parent,  xmlWriter=None):
        CAbstractExportPage1Common.__init__(self, parent)

        self._xmlWriter = xmlWriter


    def setXmlWriter(self, xmlWriter):
        self._xmlWriter = xmlWriter


    def xmlWriter(self):
        return self._xmlWriter


    def createExportDest(self):
        return self.xmlWriter()


    def process(self, dest, record, params):
        if isinstance(dest, (tuple, set, list)):
            for i in dest:
                i.writeRecord(record, params)

                if hasattr(i, 'hasError') and i.hasError():
                    raise IOError(u'Ошибка записи данных')
        else:
            dest.writeRecord(record, params)

            if hasattr(dest, 'hasError') and dest.hasError():
                raise IOError(u'Ошибка записи данных')


    def postExport(self):
        if isinstance(self._xmlWriter, (tuple, set, list)):
            for i in self._xmlWriter:
                i.writeFooter(self._processParams)
        else:
            self._xmlWriter.writeFooter(self._processParams)


    def preExport(self):
        if isinstance(self._xmlWriter, (tuple, set, list)):
            for i in self._xmlWriter:
                i.writeStartDocument()
                i.writeHeader(self._processParams)
        else:
            self._xmlWriter.writeStartDocument()
            self._xmlWriter.writeHeader(self._processParams)

# ******************************************************************************

class CAbstractExportPage2(QtGui.QWizardPage, Ui_ExportPage2):
    def __init__(self, parent, prefix=''):
        QtGui.QWizardPage.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "финиш"')

        self.pathIsValid = True
        homePath = QDir.toNativeSeparators(QDir.homePath())
        self.prefix = prefix
        self.exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('%sExportDir' % prefix, homePath))
        self.edtDir.setText(self.exportDir)


    def isComplete(self):
        return self.pathIsValid


    def saveExportResults(self):
        u"""Абстрактный метод, используется для сохранения результатов экспорта
        в указанный пользователем каталог. Должен вернуть true в случае успеха,
        иначе false."""
        raise NotImplementedError


    def moveFiles(self, fileList):
        u"""Переносит файлы из списка в каталог, выбранный пользователем"""

        for src in fileList:
            srcFullName = os.path.join(forceStringEx(self.getTmpDir()),
                                                    os.path.basename(src))
            dst = os.path.join(forceStringEx(self.edtDir.text()),
                                                    os.path.basename(src))
            success, _ = QtGui.qApp.call(self, shutil.move,
                                              (srcFullName, dst))

            if not success:
                break

        return success


    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs[
                '%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()
        return success


    def getTmpDir(self):
        return self._parent.getTmpDir()


    @pyqtSignature('QString')
    def on_edtDir_textChanged(self):
        path = forceStringEx(self.edtDir.text())
        pathIsValid = os.path.isdir(path)
        if self.pathIsValid != pathIsValid:
            self.pathIsValid = pathIsValid
            self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectDir_clicked(self):
        path = QtGui.QFileDialog.getExistingDirectory(self,
                u'Выберите директорий для сохранения файла выгрузки',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(path):
            self.edtDir.setText(QDir.toNativeSeparators(path))
# ******************************************************************************

def record2DictOfLists(record):
    u'Создает из записи словарь, каждый элемент которого - список'
    result = {}
    for i in range(record.count()):
        result[forceString(record.fieldName(i))] = [record.value(i)]
    return result


def updateDictOfListsItem(_dict, record):
    u'Добавляет записи в словарь, каждый элемент которого - список'
    for key in _dict.keys():
        _dict[key].append(record.value(key))

# ******************************************************************************

class CMultiRecordInfo():
    def __init__(self):
        self._parent = None
        self._idList = None


    def _stmt(self):
        raise NotImplementedError


    def get(self, _db, _idList, parent):
        self._parent = parent
        self._idList = _idList
        query = _db.query(self._stmt())
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            if eventId in result:
                updateDictOfListsItem(result[eventId], record)
            else:
                result[eventId] = record2DictOfLists(record)

        return result
