# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Экспорт счетов для Пскова"""

import json
import os
import copy

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QIODevice, QTextStream, QDate

from library.AmountToWords import amountToWords
from library.Utils import (forceDouble, forceInt, forceRef, forceString,
                           forceBool, toVariant, forceDate)

from Accounting.Utils import getDoubleContractAttribute
from Events.Action import CAction
from Exchange.Export import CExportHelperMixin, CMultiRecordInfo
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Order79Export import (
    COrder79ExportWizard, COrder79ExportPage1, COrder79ExportPage2,
    COrder79PersonalDataWriter, COrder79XmlStreamWriter)
from Exchange.Order200Export import (COnkologyInfo, mapDiagRslt, mapPptr,
                                     mapMetIssl, COrganisationMiacCodeCache)
from Exchange.Utils import compressFileInZip


from Exchange.Ui_ExportR60NativeAmbulancePage1 import Ui_ExportPage1

DEBUG = False

def exportR60Ambulance(widget, accountId, accountItemIdList, accountIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
    wizard.exec_()


def getXmlBaseFileName(_db, info, packetNumber, addPostfix=True):
    u"""Возвращает имя файла для записи данных"""

    def getPrefix(org):
        u"""Возвращает префиксы по коду инфис и признаку страховой"""
        result = ''

        if not org['isMedical'] and not org['isInsurer']:
            result = 'T'
        else:
            result = 'S' if org['isInsurer'] else 'M'

        return result

    tableContract = _db.table('Contract')
    payer = {'id': info['payerId']}
    recipient = {'id': forceRef(_db.translate(
        tableContract, 'id', info['contractId'], 'recipient_id'))}

    for org in (payer, recipient):
        record = _db.getRecord('Organisation',
                               'infisCode, isInsurer, isMedical', org['id'])

        if record:
            org['code'] = forceString(record.value(0))
            org['isInsurer'] = forceBool(record.value(1))
            org['isMedical'] = forceBool(record.value(2))

    p_i = getPrefix(recipient)
    p_p = getPrefix(payer)

    postfix = u'%02d%02d%d' % (
        info['settleDate'].year() %100,
        info['settleDate'].month(), packetNumber) if addPostfix else u''
    result = u'%s%s%s%s_%s.xml' % (
        p_i, recipient['code'], p_p, payer['code'], postfix)
    return result

# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта Псковской области"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Псковской области'
        prefix = 'R60NativeAmbulance'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.accountIdList = None
        self.__xmlBaseFileName = None
        self.__xmlFileName = None


    def setAccountId(self, accountId):
        COrder79ExportWizard.setAccountId(self, accountId)
        self.page1.accountIdChanged()


    def setAccountIdList(self, accountIdList):
        u"""Запоминает список идентификаторов счетов"""
        self.accountIdList = accountIdList


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return u'%s.zip' % self.getXmlFileName()[:-4]


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""
        result = self.__xmlBaseFileName

        if not result:
            result = getXmlBaseFileName(
                self.db, self.info, self.page1.edtPacketNumber.value(),
                addPostfix)
            self.__xmlBaseFileName = result

        return result


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        result = self.__xmlFileName

        if not result:
            payerCode = forceString(self.db.translate(
                'Organisation', 'id', self.info['payerId'], 'infisCode'))

            if payerCode == '60':
                prefix = 'C' if self.page1.registryType else 'R'
            else:
                prefix = 'C' if self.page1.registryType else 'H'

            result = u'{0}{1}'.format(
                prefix, self._getXmlBaseFileName(addPostfix))
            self.__xmlFileName = result

        return result

    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        if self.page1.registryType:
            return u'LC%s' % self._getXmlBaseFileName(addPostfix)

        return u'L%s' % self._getXmlBaseFileName(addPostfix)

    def getTxtFileName(self):
        u"""Возвращает имя файла счет-фактуры"""
        return u'sf%s.txt'% self._getXmlBaseFileName(True)


    def getFullTxtFileName(self):
        u"""Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getTxtFileName())

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""
    registryTypeA1 = 0
    registryTypeA4 = 1

    mapMesLevelToInvoice = {2: 0, 1: 1, 0: 1}
    ambulanceCodes = (26, 27, 30)  # Поликлиника
    emergencyCodes = (31, 24)  # СМП
    urgentCodes = (39, 41)  # Неотложная
    stomatologyCodes = (9, )
    fapCodes = (44, )
    DD_CODES = (29, )  # Диспансеризация

    TABLE_NUM_DIAGNOSTIC = 7
    TABLE_NUM_FAP = 8
    TABLE_NUM_ADDITIONAL_SUM = 9
    TABLE_NUM_DD = 10
    TABLE_NUM_LAST = 10

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self),
                     PersonalDataWriter(self))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.cmbRegistryType.setVisible(True)
        self.lblRegistryType.setVisible(True)
        self.cmbRegistryType.clear()
        self.cmbRegistryType.addItems([u'A1', u'A4'])
        self.registryType = self.registryTypeA1

        prefs = QtGui.qApp.preferences.appPrefs
        self.cmbRegistryType.setCurrentIndex(forceInt(prefs.get(
            'Export%sRegistryType' % prefix, 0)))
        self._recNum = 1


    def accountIdChanged(self):
        additionalSumOfPCF = getDoubleContractAttribute(
            self.wizard().accountId, u'подуш_доп')
        self.edtAdditionalSumOfPCF.setValue(additionalSumOfPCF)


    def preprocessQuery(self, query, params):
        ambulanceIncomplete = not self.chkAmbulancePlanComplete.isChecked()
        emergencyIncomplete = not self.chkEmergencyPlanComplete.isChecked()
        if self.chkAdditionalSumOfPCF.isChecked():
            additionalSumOfPCF = self.edtAdditionalSumOfPCF.value()
        else:
            additionalSumOfPCF = 0.0

        params['ambulanceIncomplete'] = ambulanceIncomplete
        params['emergencyIncomplete'] = emergencyIncomplete

        if params['registryType'] == CExportPage1.registryTypeA1:
            params['SUM_POD'] = round(getDoubleContractAttribute(
                self.wizard().accountId, u'подуш_амб'), 2)
            params['SUM_FAP'] = round(getDoubleContractAttribute(
                self.wizard().accountId, u'подуш_фап'), 2)
            params['SUM_POD_DOP'] = additionalSumOfPCF
        else:
            params['SUM_POD'] = 0
            params['SUM_FAP'] = 0
            params['SUM_POD_DOP'] = 0

        params['SUM_U'] = 0.0
        while query.next():
            record = query.record()
            idsp = forceInt(record.value('Z_SL_IDSP'))
            val = round(forceDouble(record.value('sum')), 2)
            if idsp not in (25, 31):
                params['SUM_U'] += val

        params['SUMMAV'] = (params['SUM_POD'] + params['SUM_FAP'] +
                            params['SUM_POD_DOP'] + params['SUM_U'])
        query.exec_()


    def nschet(self, registryType, params):
        settleDate = params['settleDate']
        if self.registryType:
            nschet = u'{p}C{year:02d}{month:02d}{registryNumber:d}'
        else:
            nschet = u'{p}H{year:02d}{month:02d}{registryNumber:d}'

        return nschet.format(
            p=params['lpuMiacCode'][-3:],
            year=settleDate.year() % 100,
            month=settleDate.month(),
            registryNumber=self.edtPacketNumber.value()
        )


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
        stmt = u"""SELECT COUNT(DISTINCT IF(EventType.form IN ('001','030')
             AND EventType.regionalCode != '001'
             AND (SELECT tariffType FROM Contract_Tariff
                  WHERE Account_Item.tariff_id = Contract_Tariff.id) = 2
             AND rbMedicalAidUnit.federalCode != 9
             AND Account_Item.visit_id IS NULL, NULL, event_id)) +
            COUNT(IF(EventType.form IN ('001','030')
             AND EventType.regionalCode != '001'
             AND (SELECT tariffType FROM Contract_Tariff
                  WHERE Account_Item.tariff_id = Contract_Tariff.id) = 2
             AND rbMedicalAidUnit.federalCode != 9
             AND Account_Item.visit_id IS NULL, event_id, NULL))
            FROM Account_Item
            LEFT JOIN Event ON Event.id = Account_Item.event_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            WHERE {0}""".format(
            self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        result = 0

        if query.first():
            record = query.record()
            result = forceInt(record.value(0))

        return result


    def getBedDaysCount(self):
        days = {}
        completeDays = {}
        stmt = """SELECT  Action.event_id,
                getLastEventId(Action.event_id),
                DATEDIFF(MAX(Action.endDate), MIN(Action.begDate)),
                rbMedicalAidType.code
            FROM Account_Item
            LEFT JOIN Event ON Account_Item.event_id = Event.id
            LEFT JOIN Action ON Action.event_id = Event.id AND
                      Action.deleted = 0 AND
                      Action.actionType_id = (
                            SELECT AT.id
                            FROM ActionType AT
                            WHERE AT.flatCode ='moving'
                      )
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidType ON
                EventType.medicalAidType_id = rbMedicalAidType.id
            WHERE {0}
            GROUP BY Action.event_id""".format(
                self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            lastEventId = forceRef(record.value(1))
            val = forceInt(record.value(2))
            medicalAidTypeCode = forceInt(record.value(3))

            if medicalAidTypeCode == 7:
                val += 1

            if val <= 0:
                val = 1

            days[eventId] = val

            if completeDays.has_key(lastEventId):
                completeDays[lastEventId] += val
            else:
                completeDays[lastEventId] = val

        return (days, completeDays)


    def getMedicalAidType(self):
        stmt = """SELECT Event.id, rbMedicalAidType.code
        FROM Account_Item
        LEFT JOIN Event ON Account_Item.event_id = Event.id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON
            EventType.medicalAidType_id = rbMedicalAidType.id
        WHERE {0}
        GROUP BY Account_Item.event_id""".format(
            self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            code = forceInt(record.value(1))
            result[eventId] = code

        return result


    def prepareStmt(self, params):
        diagnosticFlag = u"""(EventType.form IN ('001','030')
             AND EventType.regionalCode != '001'
             AND (SELECT tariffType FROM Contract_Tariff
                  WHERE Account_Item.tariff_id = Contract_Tariff.id) = 2
             AND IFNULL(rbMedicalAidUnit.federalCode, 0) != 9
             AND Account_Item.visit_id IS NULL)"""

        policyKindCodes = ("'1', '2'" if params.get('isInsurerPayCode60')
                           else "'1', '2', '3'")

        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            MesService.infis AS mesServiceInfis,
            MesAction.begDate AS mesActionBegDate,
            MesAction.endDate AS mesActionEndDate,
            Account_Item.`sum` AS `sum`,
            Account_Item.uet,
            Account_Item.amount,
            Account_Item.usedCoefficients,
            LastEvent.id AS lastEventId,
            EventType.id AS eventTypeId,
            HospitalAction.id AS hospActionId,
            Diagnostic.dispanser_id AS dispanserId,
            {diagnosticFlag} AS isDiagnostics,
            (SELECT MAX(id) FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND ETI.deleted = 0
               AND ETI.system_id = (
                    SELECT id FROM rbAccountingSystem
                    WHERE code = 'diag20')) as isDiag20,
            Action.directionDate AS actionDirectionDate,
            (SELECT federalCode FROM Person
             WHERE Person.id = Action.person_id
             LIMIT 1) AS actionPersonFederalCode,
            (SELECT OS.infisCode FROM Person
             LEFT JOIN OrgStructure AS OS ON OS.id = Person.orgStructure_id
             WHERE Person.id = Action.person_id
             LIMIT 1) AS actionPersonOrgStructureInfisCode,
            (SELECT OS.tfomsCode FROM Person
             LEFT JOIN OrgStructure AS OS ON OS.id = Person.orgStructure_id
             WHERE Person.id = Action.person_id
             LIMIT 1) AS actionPersonOrgStructureTfomsCode,
            (SELECT rbSpeciality.federalCode FROM Person
             LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
             WHERE Person.id = Action.person_id
             LIMIT 1) AS actionPersonSpecialityFederalCode,
            Event.execDate AS eventExecDate,
            Action.endDate AS actionEndDate,
            PersonOrgStructure.tfomsCode AS personOrgStructureTfomsCode,
            Action.MKB AS actionMkb,
            rbService.infis AS serviceInfis,
            IF(Event.nextEventDate, DATE_FORMAT(Event.nextEventDate, '%m%y'), DATE_FORMAT(DATE_ADD(Event.execDate, INTERVAL 90 DAY), '%m%y')) AS SL_DN_DATE,
            IF((SELECT SI.id FROM rbService_Identification SI
                WHERE SI.master_id = Account_Item.service_id
                  AND SI.deleted = 0
                  AND SI.system_id IN (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE urn = 'urn:covid'
                      AND domain = 'rbService')
                LIMIT 1) IS NULL, '0', '1') AS isCovid,

            rbService.name AS invoiceName, -- поля для печатной формы
            rbService.code AS invoiceCode,
            1 AS invoiceAmount,
            Account_Item.price AS invoicePrice,
            HospitalAction.amount AS invoiceHospitalAmount,
            VisitCount.amount AS invoiceVisitCount,

            LeavedOrgStruct.tfomsCode AS invoiceOrgStructCode,
            LeavedOrgStruct.name AS invoiceOrgStructName,
            AnotherMesService.infis AS invoiceServiceCode,
            IFNULL(CONCAT(InvoiceMesService.code, ' ', InvoiceMesService.name),
                CONCAT(MesMKB.DiagId, ' ', MesMKB.DiagName)) AS invoiceServiceName,
            rbMesSpecification.level AS invoiceMesLevel,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.regionalCode = '1',
                ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            IF(rbPolicyKind.regionalCode IN ({policyKindCodes}),
                ClientPolicy.number, '') AS PACIENT_NPOLIS,
            IF(rbPolicyKind.regionalCode = '3',
                ClientPolicy.number, '') AS PACIENT_ENP,
            Insurer.miacCode AS PACIENT_SMO,
            IF((Insurer.miacCode IS NULL OR Insurer.miacCode = '')
                    AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                    Insurer.shortName, '') AS PACIENT_SMO_NAM,
            Client.birthWeight AS PACIENT_VNOV_D,
            0 AS PACIENT_NOVOR,
            IF(MseAction.id IS NOT NULL, 1, '') AS PACIENT_MSE,
            IF(Insurer.miacCode != '60001',
               Insurer.OKATO, '') AS PACIENT_ST_OKATO,

            getLastEventId(Account_Item.event_id) AS Z_SL_IDCASE,
            rbEventTypePurpose.regionalCode AS Z_SL_USL_OK,
            IFNULL(OrgStructure_Identification.value, rbMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            0 AS Z_SL_FOR_POM,
            PersonOrganisation.miacCode AS Z_SL_LPU,
            IFNULL(NextEvent.setDate, Event.setDate) AS Z_SL_DATE_Z_1,
            IFNULL(LastEvent.execDate, Event.execDate) AS Z_SL_DATE_Z_2,
            0 AS Z_SL_KD_Z,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            IF(NextEvent.id IS NOT NULL, 1, '') AS Z_SL_VB_P,
            rbMedicalAidUnit.regionalCode AS Z_SL_IDSP,
            rbMedicalAidUnit.federalCode AS Z_SL_IDSPFEDERAL,
            IF(rbMedicalAidUnit.federalCode IN ('35') AND rbEventProfile.regionalCode = '5',
                0, IF(rbEventProfile.regionalCode = '6', UetInfo.`sum`, Account_Item.`sum`)) AS Z_SL_SUMV,
            Relegate.miacCode AS Z_SL_NPR_MO,
            IFNULL(Event.srcDate, Event.setDate) AS Z_SL_NPR_DATE,

            Account_Item.event_id AS SL_SL_ID,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL((SELECT EI.value FROM EventType_Identification EI
                    WHERE EI.master_id = EventType.id
                      AND EI.deleted = 0
                      AND EI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'НеотлПом')
                LIMIT 1
                ), PersonOrgStructure.tfomsCode)) AS SL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS SL_DET,
            IF(rbEventTypePurpose.regionalCode = 3, rbService_Identification.value, '') AS SL_P_CEL,
            IF(rbEventProfile.regionalCode IN ('1', '3'), Event.externalId, Client.id) AS SL_NHISTORY,
            IF(EventType.form = '110', Event.execDate, Event.setDate) AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            IF(Diagnosis.MKB IN ('U07.1', 'U07.2'),
             (SELECT APD.value FROM ActionProperty AP
              INNER JOIN Action ON AP.action_id = Action.id
              INNER JOIN ActionType AT ON AT.id = Action.actionType_id
              INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
              INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
              WHERE APT.descr = 'weight' AND AT.flatCode = 'MedicalSupplies'
                AND AP.deleted = 0 AND Action.event_id = Account_Item.event_id
              LIMIT 1),'') AS SL_WEI,
            DS0.MKB AS SL_DS0,
            Diagnosis.MKB AS SL_DS1,
            DS9.MKB AS SL_DS2,
            DS3.MKB AS SL_DS3,
            (SELECT
                    rbDiseaseCharacter_Identification.value
                FROM
                    rbDiseaseCharacter_Identification
                        LEFT JOIN
                    rbAccountingSystem ON rbAccountingSystem.id = rbDiseaseCharacter_Identification.system_id
                WHERE
                    rbAccountingSystem.urn = 'tfoms60:V027'
                        AND rbDiseaseCharacter_Identification.master_id = Diagnosis.character_id
                LIMIT 1) AS SL_C_ZAB,
            mes.MES_ksg.code AS SL_CODE_MES1,
            EventResult.federalCode AS SL_RSLT,
            Person.federalCode AS SL_IDDOKT,
            IF(   rbMedicalAidUnit.federalCode IN ('9', '24', '31')
               OR rbMedicalAidUnit.regionalCode IN ('25', '31'),
               Account_Item.price,
               '') AS SL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35') AND rbEventProfile.regionalCode = '5',
                0, IF(rbEventProfile.regionalCode = '6', UetInfo.`sum`, Account_Item.`sum`)) AS SL_SUM_M,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                IF(rbMedicalAidUnit.federalCode = '9', UetInfo.uet, VisitCount.amount)) AS SL_ED_COL,
            rbSpeciality.federalCode AS SL_PRVS,

            mes.MES_ksg.code AS KSG_KPG_N_KSG,
            mes.MES_ksg.vk AS KSG_KPG_KOEF_Z,
            IF(mes.MES_ksg.vk IS NOT NULL, Account_Item.price/mes.MES_ksg.vk, 0) AS KSG_KPG_KOEF_U,
            (SELECT GROUP_CONCAT(AT.code)
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND (SUBSTR(AT.code, 1, 2) IN
                                ('it', 'fr', 'rb', 'sh', 'mt')
                             OR SUBSTR(AT.code, 1, 3) IN ('stt', 'flt', 'ivf', 'amt')
                             OR SUBSTR(AT.code, 1, 4) IN ('gibp', 'derm')
                             OR SUBSTR(AT.code, 1, 5) = 'gemop')
                WHERE A.event_id = Event.id AND A.deleted = 0
            )  AS critList,
            0 AS KSG_KPG_SL_K,

            PersonOrganisation.miacCode AS USL_LPU,
            PersonOrgStructure.infisCode AS USL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL((SELECT EI.value FROM EventType_Identification EI
                    WHERE EI.master_id = EventType.id
                      AND EI.deleted = 0
                      AND EI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'НеотлПом')
                LIMIT 1
                ), PersonOrgStructure.tfomsCode)) AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS USL_PROFIL,
            (SELECT NS.infis FROM ActionType NSAT
             LEFt JOIN rbService NS ON NS.id = NSAT.nomenclativeService_id
             WHERE NSAT.id = Action.actionType_id
             LIMIT 1) AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            Event.setDate AS USL_DATE_IN,
            Event.execDate AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            IF(rbEventProfile.regionalCode IN (1,3),
                mes.MES_ksg.code,
                IF(Account_Item.visit_id IS NOT NULL,
                    VisitService.infis, rbService.infis)) AS USL_CODE_USL,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                Account_Item.amount) AS USL_KOL_USL,
            IF(   rbMedicalAidUnit.federalCode IN ('9', '24', '31')
               OR rbMedicalAidUnit.regionalCode IN ('25', '31'),
               Account_Item.price,
               '') AS USL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35') AND rbEventProfile.regionalCode = '5',
                0, Account_Item.`sum`) AS USL_SUMV_USL,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            IF(rbEventProfile.regionalCode = '2', VisitPerson.federalCode,
                Person.federalCode) AS MR_USL_N_CODE_MD,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.lastName) AS PERS_FAM,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            IF(rbPolicyKind.regionalCode != '3',
                rbDocumentType.regionalCode, '') AS PERS_DOCTYPE,
            IF(rbPolicyKind.regionalCode != '3',
             IF(rbDocumentType.code = '003',
                 REPLACE(TRIM(ClientDocument.serial),' ', '-'),
                 TRIM(ClientDocument.serial)),'') AS PERS_DOCSER,
            IF(rbPolicyKind.regionalCode != '3',
                TRIM(ClientDocument.number), '') AS PERS_DOCNUM,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,
            DATE(IF(rbPolicyKind.regionalCode != 3, ClientDocument.date,'')) AS PERS_DOCDATE,
            IF(rbPolicyKind.regionalCode != 3, ClientDocument.origin, '') AS PERS_DOCORG,

            rbEventProfile.regionalCode AS eventProfileRegionalCode,
            DeliveredBy.value AS delivered,
            (SELECT EI.value FROM EventType_Identification EI
                WHERE EI.master_id = Event.eventType_id
                  AND EI.deleted = 0
                  AND EI.system_id IN (
                    SELECT id FROM rbAccountingSystem
                    WHERE code = 'UziKtFgds' AND domain = 'EventType')
            ) AS uziKtFgdsCode,
            IFNULL((SELECT SId.value FROM rbService_Identification SId
                WHERE SId.master_id = Account_Item.service_id
                  AND SId.deleted = 0
                  AND SId.system_id IN (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'diagISHOD'
                      AND domain = 'rbService')
                LIMIT 1), 306) AS diagnosticResult""".format(
            diagnosticFlag=diagnosticFlag, policyKindCodes=policyKindCodes)
        tables = u"""Account_Item
            LEFT JOIN Event ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.id  = getClientRegAddressId(Client.id)
            LEFT JOIN ClientAddress ClientLocAddress ON ClientLocAddress.id = getClientLocAddressId(Client.id)
            LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN kladr.KLADR AS RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN Address   LocAddress ON LocAddress.id = ClientLocAddress.address_id
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR AS LocKLADR ON LocKLADR.CODE = LocAddressHouse.KLADRCode
            LEFT JOIN Diagnostic ON Diagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN Diagnosis AS DS3 ON DS3.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '3')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN Diagnosis AS DS9 ON DS9.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN Diagnosis AS DS0 ON DS0.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '7')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbService ON rbService.id = Account_Item.service_id
            LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
                WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = IFNULL(rbService_Profile.medicalAidKind_id,
                IFNULL(rbService.medicalAidKind_id,EventType.medicalAidKind_id))
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(
                Client.`id`, 1, IF(
                    {diagnosticFlag}, Account_Item.serviceDate, Event.execDate))
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbEventProfile ON rbEventProfile.id = EventType.eventProfile_id
            LEFT JOIN (
                    SELECT A.event_id, SUM(A.amount) AS amount, COUNT(DISTINCT A.id) AS cnt, MAX(A.id) AS id
                    FROM Action A
                    WHERE A.deleted = 0 AND
                              A.actionType_id IN (
                                    SELECT AT.id
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='moving'
                              )
                    GROUP BY A.event_id
                ) AS HospitalAction ON HospitalAction.event_id = Account_Item.event_id
            LEFT JOIN Visit ON Account_Item.visit_id = Visit.id
            LEFT JOIN Action ON Account_Item.action_id = Action.id
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = IFNULL(Visit.person_id, Action.person_id)
            LEFT JOIN rbService AS VisitService ON VisitService.id = Visit.service_id
            LEFT JOIN Action AS MesAction ON MesAction.id = (
                    SELECT MAX(A.id)
                    FROM mes.MES_service MS
                    LEFT JOIN mes.mrbService AS S ON S.id = MS.service_id
                        AND S.deleted = 0
                    LEFT JOIN ActionType AS AType ON S.code = AType.code
                        AND AType.deleted = 0
                    LEFT JOIN Action AS A ON A.actionType_id = AType.id
                        AND A.deleted = 0
                    WHERE MS.deleted = 0 AND MS.master_id = Event.MES_id
                        AND A.event_id = Event.id
                )
            LEFT JOIN rbService AS MesService ON MesService.id = (
                    SELECT AType.nomenclativeService_id
                    FROM ActionType AS AType
                    WHERE AType.id = MesAction.actionType_id
                    LIMIT 1
                )
            LEFT JOIN ActionProperty_String AS DeliveredBy ON DeliveredBy.id = (
                SELECT APS.id
                FROM Action A
                INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
                INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = 'received'
                    AND APT.`name` = 'Кем доставлен'
                ORDER BY A.begDate DESC
                LIMIT 0, 1
            )
            LEFT JOIN (
                SELECT Account_Item.event_id,
                    SUM(Account_Item.uet) AS uet,
                    SUM(Account_Item.`sum`) AS `sum`
                FROM Account_Item
                GROUP BY Account_Item.event_id
            ) AS UetInfo ON UetInfo.event_id = Account_Item.event_id
            LEFT JOIN OrgStructure AS LeavedOrgStruct ON LeavedOrgStruct.id = (
                SELECT OS.id
                FROM Action A
                INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
                INNER JOIN ActionProperty_OrgStructure AS APO ON APO.id = AP.id
                INNER JOIN OrgStructure AS OS ON OS.id = APO.value
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = IF(EventResult.code = 104, 'moving', 'leaved')
                    AND IF(EventResult.code = 104, APT.shortName = 'currentDep', APT.`typeName` = 'OrgStructure')
                ORDER BY A.begDate DESC
                LIMIT 0, 1
            )
            LEFT JOIN OrgStructure_Identification
                ON OrgStructure_Identification.master_id = IFNULL(LeavedOrgStruct.id, PersonOrgStructure.id)
                AND OrgStructure_Identification.deleted = 0
                AND OrgStructure_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'ВидМП'
            )
            LEFT JOIN mes.mrbService AS InvoiceMesService ON InvoiceMesService.id = (
                SELECT mes.mrbService.id
                FROM mes.MES_service MS
                LEFT JOIN mes.mrbService ON mes.mrbService.id = MS.service_id
                    AND mes.mrbService.deleted = 0
                LEFT JOIN ActionType ATMS ON ATMS.code = mes.mrbService.code
                LEFT JOIN Action AMS ON AMS.actionType_id = ATMS.id
                WHERE MS.deleted = 0 AND MS.master_id = Event.MES_id AND AMS.event_id = Event.id
                LIMIT 0, 1
            )
            LEFT JOIN MKB AS MesMKB ON MesMKB.id = (
                SELECT MAX(id) FROM MKB
                WHERE DiagId = Diagnosis.MKB
            )
            LEFT JOIN rbService AS AnotherMesService ON AnotherMesService.id = (
                SELECT S.id
                FROM rbService S
                WHERE mes.MES.code = S.code AND mes.MES.deleted = 0
                LIMIT 0, 1
            )
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN (
                SELECT V.event_id, V.service_id, COUNT(*) AS amount
                FROM Visit V
                WHERE V.deleted = 0
                GROUP BY V.event_id, V.service_id
            ) AS VisitCount ON VisitCount.event_id = Event.id
                AND VisitCount.service_id = Account_Item.service_id
            LEFT JOIN Action AS MseAction ON MseAction.id = (
                SELECT MAX(A.id)
                FROM Action A
                WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id = (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='inspection_mse'
                          )
            )
            LEFT JOIN Event AS NextEvent ON NextEvent.prevEvent_id = Event.id
            LEFT JOIN Event AS LastEvent ON LastEvent.id = getLastEventId(Event.id)
            LEFT JOIN Organisation AS Relegate ON Relegate.id = Event.relegateOrg_id
            LEFT JOIN rbService_Identification ON rbService_Identification.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfomsPCEL')
                AND SId.deleted = 0
            )
            """.format(diagnosticFlag=diagnosticFlag)
        where = u"""Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s""" % self.tableAccountItem['id'].inlist(self.idList)
        orderBy = u'Client.id, LastEvent.id, Event.id'

        return (select, tables, where, orderBy)


    def setExportMode(self, flag):
        COrder79ExportPage1.setExportMode(self, flag)
        self.chkAmbulancePlanComplete.setEnabled(not flag)
        self.chkEmergencyPlanComplete.setEnabled(not flag)
        self.chkReexposed.setEnabled(not flag)
        self.chkAdditionalSumOfPCF.setEnabled(not flag)
        self.cmbRegistryType.setEnabled(not flag)
        self.lblRegistryType.setEnabled(not flag)
        self.lblPacketNumber.setEnabled(not flag)


    def process(self, dest, record, params):
        COrder79ExportPage1.process(self, dest, record, params)
        self.processInvoice(record, params)


    def exportInt(self):
        self.invoiceFile = QFile(self.wizard().getFullTxtFileName())
        self.invoiceFile.open(QIODevice.WriteOnly | QIODevice.Text)
        self.invoiceStream = QTextStream(self.invoiceFile)
        self.invoiceStream.setCodec('UTF8')

        params = self.processParams()
        self.registryType = self.cmbRegistryType.currentIndex() # 0-A1, 1-A4
        payerCode = forceString(self.db.translate(
                'Organisation', 'id', self.accountInfo()['payerId'], 'infisCode'))
        params['isInsurerPayCode60'] = payerCode == '60'
        params['recNum'] = 1
        params['isReexposed'] = '1' if self.chkReexposed.isChecked() else '0'
        params['completeEventSum'] = self.getCompleteEventSum()
        params['medicalAidType'] = self.getMedicalAidType()
        params['bedDays'],  params['completeBedDays'] = self.getBedDaysCount()

        for name, _class in (('onkologyInfo', CR60OnkologyInfo),
                             ('medicalSuppliesInfo', CMedicalSuppliesInfo),
                             ('implantsInfo', CImplantsInfo)):
            val = _class()
            params[name] = val.get(
                self.db, self.tableAccountItem['id'].inlist(self.idList),
                self)

        params['registryType'] = self.registryType
        self.setProcessParams(params)

        COrder79ExportPage1.exportInt(self)


    def processInvoice(self, record, params):
        u"""Пишет данные для счет-фактуры в словарь"""

        def addToInvoice(code, name, amount, inSum, price, uet):
            if params.setdefault('invoice', {}).setdefault(
                    tableNum, {}).has_key(code):
                (_name, _amount, _sum, _price, _uet) = params[
                    'invoice'][tableNum][code]
                params['invoice'][tableNum][code] = (
                    _name, _amount + amount, _sum, _price, _uet + uet)
            else:
                params['invoice'][tableNum][code] = (
                    name, amount, inSum, price, uet)

            if params.setdefault('ambInfo', {}).setdefault(
                    tableNum, {}).has_key('totalAmount'):
                params['ambInfo'][tableNum]['totalAmount'] += amount
            else:
                params['ambInfo'][tableNum]['totalAmount'] = amount

        invoiceCode = forceString(record.value('invoiceCode'))
        invoiceName = forceString(record.value('invoiceName'))
        invoiceAmount = forceDouble(record.value('invoiceAmount'))
        invoiceSum = forceDouble(record.value('sum'))
        invoiceUet = forceDouble(record.value('uet'))
        invoicePrice = forceDouble(record.value('invoicePrice'))
        idsp = forceInt(record.value('Z_SL_IDSPFEDERAL'))
        clientId = forceRef(record.value('clientId'))
        params.setdefault('clients', set()).add(clientId)
        isHospital = forceInt(record.value('Z_SL_USL_OK')) in (1, 2)
        eventOrder = forceInt(record.value('eventOrder'))
        isDiagnostics = forceBool(record.value('isDiagnostics'))
        isHealthExamination = idsp in self.DD_CODES and forceString(record.value('USL_CODE_USL'))[:1] == u'0'

        if isDiagnostics:
            tableNum = self.TABLE_NUM_DIAGNOSTIC
        elif idsp in self.fapCodes:
            tableNum = self.TABLE_NUM_FAP
        elif idsp in self.ambulanceCodes:
            tableNum = 5 if invoiceCode in ('101025',
                '101125', '101034', '101134', '101099') else 1
        elif idsp in self.emergencyCodes:
            tableNum = 2
        elif idsp in self.urgentCodes:
            tableNum = 3
        elif idsp in self.stomatologyCodes:
            tableNum = 4 if eventOrder != 6 else 6
        elif isHealthExamination:
            tableNum = self.TABLE_NUM_DD
        else:
            tableNum = 0


        if tableNum in (1, 5):
            addToInvoice(invoiceCode[2:] if tableNum == 1 else invoiceCode, invoiceName, invoiceAmount,
                invoiceSum, invoicePrice, invoiceUet)

            if invoiceCode[3] == '1':
                addToInvoice(u'{beg}3{end}'.format(beg=invoiceCode[:2] if tableNum == 5 else '',
                    end=invoiceCode[3:]),
                    u'Первичн. прием в рамках услуги {0}'.format(invoiceName),
                    invoiceAmount, 0, 0, 0)
                amount = forceInt(record.value('invoiceVisitCount')) - 2*invoiceAmount
                addToInvoice(u'{beg}4{end}'.format(beg=invoiceCode[:2] if tableNum == 5 else '',
                    end=invoiceCode[3:]),
                    u'Повторн. прием в рамках услуги {0}'.format(invoiceName),
                    amount if amount > 0 else 1,
                    0, 0, 0)
        else:
            addToInvoice(invoiceCode, invoiceName, invoiceAmount, invoiceSum,
                invoicePrice, invoiceUet)


        for (key, val) in (('totalSum', invoiceSum),
                           ('totalUet', invoiceUet),
                           ('uetSum', invoiceSum if invoiceUet else 0)):
            if params.setdefault('ambInfo', {}).setdefault(
                    tableNum, {}).has_key(key):
                params['ambInfo'][tableNum][key] += val
            else:
                params['ambInfo'][tableNum][key] = val

        params['ambInfo'][tableNum].setdefault('hospClientCount' if isHospital
            else 'clientCount', set()).add(clientId)

        self.processHospitalInvoice(record, params)
        self.processTotal(record, params)


    def processHospitalInvoice(self, record, params):
        u"""Еще одна СФ для Стационара и ДС"""

        eventProfile = forceInt(record.value('eventProfileRegionalCode'))

        if eventProfile not in (1, 3): # Стационар, ДС
            return

        invoiceOrgStructCode = forceString(record.value('invoiceOrgStructCode'))

        if not invoiceOrgStructCode:
            return

        invoiceServiceCode = forceString(record.value('invoiceServiceCode'))
        level = forceInt(record.value('invoiceMesLevel'))
        _sum = forceDouble(record.value('sum'))
        amount = forceDouble(record.value('amount'))
        uet = forceDouble(record.value('uet'))
        hospAmount = forceDouble(record.value('invoiceHospitalAmount'))
        key = (invoiceServiceCode, level, _sum)

        if params.setdefault('hospInvoice', {}
                ).setdefault(invoiceOrgStructCode, {}).has_key(key):
            params['hospInvoice'][invoiceOrgStructCode][key] += amount
        else:
            params['hospInvoice'][invoiceOrgStructCode][key] = amount

        if params.setdefault('hospInvoiceInfo', {}).setdefault(
                invoiceOrgStructCode, {}).has_key('amount'):
            params['hospInvoiceInfo'][invoiceOrgStructCode]['amount'] += amount
        else:
            params['hospInvoiceInfo'][invoiceOrgStructCode]['amount'] = amount

        if params['hospInvoiceInfo'][invoiceOrgStructCode].has_key('bedDays'):
            params['hospInvoiceInfo'][invoiceOrgStructCode][
                'bedDays'] += hospAmount
        else:
            params['hospInvoiceInfo'][invoiceOrgStructCode][
                'bedDays'] = hospAmount

        for (key, val) in (('totalSum', _sum),
                           ('totalUet', uet),
                           ('uetSum', _sum if uet > 0 else 0)):
            if params['hospInvoiceInfo'][invoiceOrgStructCode].has_key(key):
                params['hospInvoiceInfo'][invoiceOrgStructCode][key] += val
            else:
                params['hospInvoiceInfo'][invoiceOrgStructCode][key] = val

        clientId = forceRef(record.value('clientId'))
        params['hospInvoiceInfo'][invoiceOrgStructCode].setdefault(
            'clients', set()).add(clientId)

        params.setdefault('orgStructMap', {})[invoiceOrgStructCode
            ] = forceString(record.value('invoiceOrgStructName'))
        params.setdefault('serviceMap', {})[invoiceServiceCode
            ] = forceString(record.value('invoiceServiceName'))


    def processTotal(self, record, params):
        u"""Собирает данные для сводки по условиям оказания помощи."""

        def initData(name, params):
            params['total'].setdefault(name, {'clients': set(),
                'ambClients': set(), 'hospClients': set(), 'amount':0, 'sum': 0,
                'uet': 0, 'mesAmount': 0, 'mesSum': 0, 'bedDays': 0,
                'totalSum': 0,  'uetSum': 0, 'totalUet': 0,
            })

        idsp = forceInt(record.value('Z_SL_IDSPFEDERAL'))
        eventOrder = forceInt(record.value('eventOrder'))
        params.setdefault('total', {})
        clientId = forceRef(record.value('clientId'))
        name = None
        isHospital = False
        isDiagnostics = forceBool(record.value('isDiagnostics'))
        serviceCode = forceString(record.value('USL_CODE_USL'))

        if isDiagnostics:
            name = u'Диагн. услуги'
        elif idsp in self.ambulanceCodes:  # Поликлиника
            name = u'Поликлиника'
        elif idsp in self.emergencyCodes:  # СМП
            name = u'СМП'
        elif idsp in self.urgentCodes:  # Неотложная помощь
            name = u'Неотложная помощь'
        elif idsp in self.stomatologyCodes:
            name = u'Стоматология' if eventOrder != 6 else u'Стоматология неотл'
        elif idsp in self.fapCodes:
            name = u'ФАПы'
        elif idsp in self.DD_CODES and serviceCode[:1] == u'0':
            name = u'Диспансерное наблюдение'
        else:
            profile = forceInt(record.value('eventProfileRegionalCode'))
            isHospital = True
            if profile == 1:  # Стационар
                name = u'Стационар'
            elif profile == 3:  # ДС
                name = u'Дневной стационар'

        if name:
            initData(name, params)
            _sum = forceDouble(record.value('sum'))
            amount = forceDouble(record.value('invoiceAmount'))
            uet = forceDouble(record.value('uet'))
            params['total'][name]['totalUet'] += uet
            params['total'][name]['totalSum'] += _sum
            params['total'][name]['clients'].add(clientId)
            params['total'][name]['hospClients' if isHospital else 'ambClients'
                ].add(clientId)

            if uet:
                params['total'][name]['uetSum'] += _sum

            if isHospital:
                params['total'][name]['mesAmount'] += amount
                params['total'][name]['mesSum'] += _sum
                params['total'][name]['bedDays'] += forceDouble(
                    record.value('invoiceHospitalAmount'))
            else:
                params['total'][name]['amount'] += amount
                params['total'][name]['sum'] += _sum


    def postExport(self):
        self.writeInvoice(self._processParams)
        self.invoiceFile.close()
        COrder79ExportPage1.postExport(self)


    def writeInvoice(self, params):
        orgStructName = [
            u'0001 Поликлиническое отделение для взрослых (Поликлиническое отделение для взрослых)',
            u'0241 Скорая помощь (Скорая помощь)',
            u'0731 Приемное отделение (Хирургические услуги)',
            u'0351 Стоматологические услуги (Стоматологические услуги)',
            u'1001 Поликлиническое отделение для детей (Поликлиническое отделение для детей)',
            u'0351 Стоматология неотложная помощь',
            u'     Диагностические услуги',
            u'0001 ФАПы',
            u'     Доп.сумма с учетом',
            u'     Диспансерное наблюдение',
        ]

        fmtStr = (u'{invoiceCode: <17.15}│{invoiceName: <49.60}│{level: <3.3}│'
                  u'{price: <11.11}│{invoiceAmount:9.2f}│{sum:11.2f}\n')
        splitter = (u'─────────────────┼────────────────────────────────────'
                    u'─────────────┼───┼───────────┼─────────┼───────────\n')

        settleDate = params['settleDate']
        output = self.invoiceStream

        tableHeader = u"""\nОтделение: {orgStructName}
Количество пролеченных пациентов {totalClientCount:10d} на сумму {totalSum:11.2f}
             из них амбулаторных {ambClients:10d} на сумму {ambSum:11.2f}
                    стационарных {hospClients:10d} на сумму {hospSum:11.2f}
                                      Средства ФФОМС        0.00
                                               Итого {total:11.2f}
Выполнено услуг (УЕТ)       {uetCount:15.2f} на сумму {uetSum:11.2f}
Выполнено услуг (операций)  {servCount:15.2f} на сумму {servSum:11.2f}
Выполнено МЭСов             {mesCount:15.2f} на сумму {mesSum:11.2f}
Всего реализовано койко-дней{bedDays:15.2f} на сумму {bedDaysSum:11.2f}
─────────────────┬─────────────────────────────────────────────────┬───┬───────────┬─────────┬───────────
 Код             │             Наименование                        │Тип│ Стоимость │ Кол-во  │   Итого
услуги           │                                                 │МЭС│ стандарта │         │
(МЭС)            │                                                 │   │           │         │
(К/Д)            │                                                 │   │           │         │
(П/П)            │                                                 │   │           │         │
"""

        output << u"""
Медицинское учреждение {lpuShortName}

СЧЕТ-ФАКТУРА № {invoiceNumber} от {accountDate}
за оказанные медицинские услуги по стандартам оказания мед.помощи в рамках региональной программы модернизации здравоохранения
пациентам своей территории
за {settleDate}
--------------------------------------------------
Основная информация\n1. РАБОТА ПРОФИЛЬНЫХ ОТДЕЛЕНИЙ\n""".format(
        accountDate=params['accDate'].toString('dd.MM.yyyy'),
        lpuShortName=params['lpuShortName'],
        settleDate=settleDate.toString('MMMM yyyy'),
        invoiceNumber=params['NSCHET'])

        for i in (1, self.TABLE_NUM_FAP, self.TABLE_NUM_DIAGNOSTIC, 2, 3, 4, 6,
                  5, self.TABLE_NUM_DD):
            if not params.get('invoice', {}).has_key(i):
                continue

            invoice = params['invoice'][i]
            info = params['ambInfo'][i]
            clientCount = len(info.get('clientCount', set()))
            totalClientCount = len(
                info.get('hospClientCount', set())) + clientCount
            totalSum = info['totalSum'] if clientCount else 0
            _sum = params['emergency'] if clientCount else 0
            totalAmount = info['totalAmount']

            if i == 1:
                totalSum = params['SUM_POD']
            if i == 2:
                totalSum = params['emergency']
            if i == 5:
                totalSum = 0
            if i == self.TABLE_NUM_FAP:
                totalSum = params['SUM_FAP']

            output << tableHeader.format(orgStructName=orgStructName[i-1],
                totalClientCount=totalClientCount, ambClients=clientCount,
                totalSum=totalSum, ambSum=totalSum, total=totalSum,
                servCount=(0 if i == self.TABLE_NUM_DD else totalAmount),
                servSum=(0 if i == self.TABLE_NUM_DD else totalSum),
                mesCount=0, mesSum=0, bedDays=0, bedDaysSum=0,
                hospClients=0, hospSum=0, uetCount=info['totalUet'],
                uetSum=info['uetSum'])

            output << splitter

            for code in sorted(invoice):
                (name, amount, _sum, price, _) = invoice[code]

                if i in (3, 4, 6, self.TABLE_NUM_DIAGNOSTIC):
                    priceStr = '%11.2f' % price
                elif i == self.TABLE_NUM_DD:
                    priceStr = ''
                else:
                    priceStr = ''
                    price = 0

                output << fmtStr.format(invoiceCode=code, invoiceName=name[:49],
                    invoiceAmount=amount, sum=price*amount, price=priceStr, level='')

            if i == 1: #подушевой только для таблиц 1 и 2 и ФАП
                output << fmtStr.format(invoiceCode='201001',
                    invoiceName=u'Подушевой норматив по амбулат.полик.пом.',
                    invoiceAmount=1, sum=params['SUM_POD'], level='',
                    price=('%11.2f' % params['SUM_POD']))
            elif i == 2:
                output << fmtStr.format(invoiceCode='201002',
                    invoiceName=u'Подушевой норматив по скорой помощи',
                    invoiceAmount=1, sum=params['emergency'], level='',
                    price=('%11.2f' % params['emergency']))
            elif i == self.TABLE_NUM_FAP:
                output << fmtStr.format(invoiceCode='0001',
                    invoiceName=u'Подушевой норматив по ФАП',
                    invoiceAmount=1, sum=params['SUM_FAP'], level='',
                    price=('%11.2f' % params['SUM_FAP']))

            output << splitter
            output << fmtStr.format(invoiceCode=u'ИТОГО', invoiceName='',
                invoiceAmount=totalAmount, price='', level='',
                sum=totalSum)

        # СФ для ДС и Стационара
        if params.has_key('hospInvoice'):
            self._writeHospitalInvoice(output, params, tableHeader, splitter,
                                        fmtStr)

        self._writeInvoiceResultTable(output, params, orgStructName)

    ADDITIONAL_SUM = u'Доп.сумма с учетом'

    def _writeInvoiceResultTable(self, output, params, orgStructName):
        u"""Пишет сводную таблицу по отделениям"""
        resultTableHeader = u"""\n2. СВОДНАЯ СПРАВКА ПО ПРОФИЛЬНЫМ ОТДЕЛЕНИЯМ
Всего обратившихся пациентов {totalClientCount:10d}
+-------------------+------+------+------+---------+-----------+---------+------+-----------+------+-----------+
|Наименование       | Пролечено пациентов|       Выполнено услуг         |    Реализовано МЭСов    | Стоимость |
|отделения          |                    |                               |                         |           |
|                   +------+------+------+---------+-----------+---------+------+-----------+------+           |
|                   |Всего | Амб. | Стац.| Кол-во  | Стоимость |   УЕТ   |Кол-во| Стоимость | К/д  |           |
"""
        splitter = (u'+-------------------+------+------+------+---------'
         u'+-----------+---------+------+-----------+------+-----------+\n')
        output << resultTableHeader.format(
            totalClientCount=len(params['clients']))
        fmtStr = (u'|{name: <19.19}|{clients:6d}|{ambClients:6d}|'
            u'{hospClients:6d}|{amount:9.2f}|{sum:11.2f}|{uet:9.2f}|'
            u'{mesAmount:6.0f}|{mesSum:11.2f}|{bedDays:6.0f}|{totalSum:11.2f}|\n')

        if params['ambInfo'].has_key(1) and params['ambInfo'].has_key(5):
            params['ambInfo'][1]['totalSum'] = params['SUM_POD']
            params['ambInfo'][1]['totalAmount'] += params['ambInfo'][5][
                'totalAmount']
            params['ambInfo'][1]['clientCount'].update(params['ambInfo'][5][
                'clientCount'])

        if params['ambInfo'].has_key(2): #СМП
            params['ambInfo'][2]['totalSum'] = params['emergency']

        if params['total'].has_key(u'СМП'):
            params['total'][u'СМП']['sum'] = params['emergency']
            params['total'][u'СМП']['totalSum'] = params['emergency']

        if params['total'].has_key(u'Поликлиника'):
            params['total'][u'Поликлиника']['sum'] = params['SUM_POD']
            params['total'][u'Поликлиника']['totalSum'] = params['SUM_POD']

        if params['ambInfo'].has_key(self.TABLE_NUM_FAP):
            params['ambInfo'][self.TABLE_NUM_FAP]['totalSum'] = params['SUM_FAP']

        if params['total'].has_key(u'ФАПы'):
            params['total'][u'ФАПы']['sum'] = params['SUM_FAP']
            params['total'][u'ФАПы']['totalSum'] = params['SUM_FAP']

        if params.has_key('SUM_POD_DOP'):
            additionalSum = {
                'clients': [],
                'ambClients': [],
                'hospClients': [],
                'amount': 0,
                'uet': 0,
                'mesAmount': 0,
                'mesSum': 0,
                'bedDays': 0,
                'sum': params['SUM_POD_DOP'],
                'totalSum': params['SUM_POD_DOP'],
                'totalUet': 0,
                'totalAmount': 0,
            }
            params['total'][self.ADDITIONAL_SUM] = additionalSum
            params['invoice'][self.TABLE_NUM_ADDITIONAL_SUM] = 0
            params['ambInfo'][self.TABLE_NUM_ADDITIONAL_SUM] = additionalSum

        totalAmount = 0
        totalClients = 0
        totalDays = 0
        totalSum = 0
        totalUet = 0
        totalHospClients = 0
        totalAmbClients = 0
        totalHospAmount = 0
        totalAmbAmount = 0
        totalAmbSum = 0
        totalHospSum = 0
        hospClients = 0

        for i in range(1, self.TABLE_NUM_LAST + 1):
            if i == 5 or not params['invoice'].has_key(i):
                continue

            info = params['ambInfo'][i]
            ambClients = len(info.get('clientCount', set()))
            hospClients = len(
                info.get('hospClientCount', set()))

            output << splitter
            output << fmtStr.format(
                name=orgStructName[i-1][5:],
                clients=(ambClients + hospClients),
                ambClients=ambClients, hospClients=hospClients,
                amount=info['totalAmount'], sum=info['totalSum'], uet=info['totalUet'],
                mesAmount=0,  mesSum=0, bedDays=0, totalSum=info['totalSum'])

            totalSum += info['totalSum']
            totalAmbSum += info['totalSum']
            totalHospClients += hospClients
            totalClients += ambClients + hospClients
            totalAmbClients += ambClients
            totalAmbAmount += info['totalAmount']
            totalAmount += info['totalAmount']
            totalUet += info['totalUet']

        if params.has_key('hospInvoice'):
            for code, services in params['hospInvoice'].iteritems():
                info = params['hospInvoiceInfo'][code]
                output << splitter
                clients = len(info['clients'])
                output << fmtStr.format(
                    name=params['orgStructMap'].get(code, ''),
                    clients=clients, ambClients=0, hospClients=clients,
                    amount=0, sum=0, uet=info['totalUet'],
                    mesAmount=info['amount'], mesSum=info['totalSum'],
                    bedDays=info['bedDays'], totalSum=info['totalSum'])
                totalSum += info['totalSum']
                totalHospSum += info['totalSum']
                totalClients += clients
                hospClients += clients
                totalHospAmount += info['amount']
                totalAmount += info['amount']
                totalDays += info['bedDays']
                totalUet += info['totalUet']

        output << splitter
        output << fmtStr.format(
            name=u'Итого', clients=totalClients, ambClients=totalAmbClients,
            hospClients=totalHospClients, amount=totalAmbAmount, sum=totalAmbSum,
            uet=totalUet, mesAmount=totalHospAmount, mesSum=totalHospSum,
            bedDays=totalDays, totalSum=totalSum)

        output << splitter
        output << (u'|В том числе:       |      |      |      |         '
         u'|           |         |      |           |      |           |\n')

        for name, val in sorted(params['total'].iteritems()):
            for key in ('clients', 'ambClients', 'hospClients'):
                val[key] = len(val[key])

            val['uet'] = val['totalUet']
            output << fmtStr.format(name=name, **val)

        output << splitter
        output << u"""\nВСЕГО ПРЕДСТАВЛЕНО К ОПЛАТЕ: {totalSum:.2f}
      ({words})\n
Руководитель мед.учреждения ____________________ {lpuChief}\n
Гл.бухгалтер мед.учреждения ____________________ {lpuAccountant}
""".format(totalSum=params['SUMMAV'],
           words=amountToWords(params['SUMMAV']),
           lpuChief = params['lpuChief'],
           lpuAccountant=params['lpuAccountant'])


    def _writeHospitalInvoice(self, output, params,
                               tableHeader, splitter, fmtStr):
        u"""Пишет с\ф для стационара."""
        for code, services in params['hospInvoice'].iteritems():
            info = params['hospInvoiceInfo'][code]
            output << tableHeader.format(
                orgStructName=('%s %s' % (code,
                    params['orgStructMap'].get(code, ''))),
                    totalClientCount=len(info['clients']),
                    totalSum=info['totalSum'], ambClients=0, ambSum=0,
                    hospClients=len(info['clients']), hospSum=info['totalSum'] ,
                    total=info['totalSum'], servCount=0, servSum=0,
                    mesCount=info['amount'], mesSum=info['totalSum'],
                    bedDays=info['bedDays'], bedDaysSum=info['totalSum'],
                    uetCount=info['totalUet'], uetSum=info['uetSum']
                )
            output << splitter
            totalAmount = 0

            for key, amount in services.iteritems():
                (serviceCode, level, _sum) = key
                name = ('C' if serviceCode and serviceCode[0] == u'C' else
                    params['serviceMap'].get(serviceCode, ''))
                output << fmtStr.format(invoiceCode=serviceCode,
                    invoiceName=name[:49],
                    invoiceAmount=amount, price=('%11.2f' % _sum),
                    sum=(_sum*amount),
                    level=('%3d' % self.mapMesLevelToInvoice.get(level, 1)))
                totalAmount += amount

            output << splitter
            output << fmtStr.format(invoiceCode=u'ИТОГО',invoiceName='',
                invoiceAmount=totalAmount, price='', sum=info['totalSum'],
                    level='')

# ******************************************************************************

class CExportPage2(COrder79ExportPage2):
    u"""Первая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, prefix)


    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(),
                    self._parent.getPersonalDataFullXmlFileName(),
                    self._parent.getFullTxtFileName())
        zipFileName = self._parent.getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                        self.moveFiles([zipFileName]))

# ******************************************************************************

class XmlStreamWriter(COrder79XmlStreamWriter, CExportHelperMixin):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_NAM', 'INV', 'MSE', 'NOVOR')

    completeEventDateFields1 = ('DATE_Z_1', 'DATE_Z_2')
    completeEventDateFields2 = ('NPR_DATE',  )
    completeEventDateFields = completeEventDateFields1 + completeEventDateFields2
    completeEventFields1 = (('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO')
                            + completeEventDateFields2 +
                            ('LPU',  )
                           + completeEventDateFields1 +
                           ('KD_Z', 'VNOV_M', 'RSLT', 'ISHOD', 'OS_SLUCH',
                            'VB_P'))
    completeEventFields2 = ('IDSP', 'SUMV')
    completeEventFields = completeEventFields1 + completeEventFields2

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFieldsA1 = ('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                   'P_CEL', 'NHISTORY', 'P_PER') +  eventDateFields + ('KD',
                   'WEI', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DN', 'DN_DATE',
                   'CODE_MES1', 'NAPR', 'CONS', 'ONK_SL', 'KSG_KPG',  'REAB',
                   'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF', 'SUM_M',
                   'LEK_PR')

    eventFieldsA4 = ('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                   'P_CEL', 'NHISTORY', 'P_PER') +  eventDateFields + ('KD',
                   'WEI', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB','DS_ONK', 'DN',
                   'DN_DATE', 'CODE_MES1', 'NAPR', 'CONS', 'ONK_SL', 'KSG_KPG',
                   'REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                   'SUM_M', 'LEK_PR')

    ksgSubGroup = {
        'SL_KOEF' : {'fields': ('IDSL', 'Z_SL')}
    }

    onkLekPrSubGroup = {
        'LEK_PR' : {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ')}
    }

    onkSlSubGroup = {
        'ONK_USL': {'fields': ('USL_TIP', 'HIR_TIP', 'LEK_TIP_L',
                               'LEK_TIP_V', 'LEK_PR', 'PPTR', 'LUCH_TIP'),
                               'subGroup': onkLekPrSubGroup},
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE', 'DIAG_RSLT', 'REC_RSLT')},
        'B_PROT': {'fields': ('PROT', 'D_PROT')}
    }

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
        },
    }

    eventSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'ONK_SL': {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                              'MTSTZ', 'B_DIAG', 'B_PROT', 'SOD'),
                   'subGroup': onkSlSubGroup},
        'LEK_PR': { 'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK',
                               'LEK_DOSE'),
                    'dateFields': ('DATA_INJ', ),
                    'requiredFields': ('DATA_INJ', 'CODE_SH'),
                    'subGroup': medicalSuppliesDoseGroup,  }
    }

    eventHospSubGroupA1 = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'KSG_KPG': { 'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG', 'KOEF_Z',
                                'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U', 'CRIT',
                                'SL_K', 'IT_SL', 'SL_KOEF'),
                               'subGroup': ksgSubGroup },
        'LEK_PR': { 'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK',
                               'LEK_DOSE'),
                    'dateFields': ('DATA_INJ', ),
                    'requiredFields': ('DATA_INJ', 'CODE_SH'),
                    'subGroup': medicalSuppliesDoseGroup,  }
    }

    eventHospSubGroupA4 = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'KSG_KPG': { 'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG', 'KOEF_Z',
                                'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U',
                                'SL_K', 'IT_SL', 'SL_KOEF'),
                               'subGroup': ksgSubGroup },
        'ONK_SL': {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                              'MTSTZ', 'B_DIAG', 'B_PROT', 'SOD', 'K_FR', 'WEI', 'HEI', 'BSA', 'ONK_USL'),
                   'subGroup': onkSlSubGroup}
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME', 'VID_VME2',
            'DET') + serviceDateFields + ('DS', 'CODE_USL', 'KOL_USL', 'TARIF',
            'SUMV_USL', 'MED_DEV', 'MR_USL_N', 'NPL', 'COMENTU'))

    serviceSubGroupA1 = {
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED', ),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    serviceSubGroupA4 = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL', 'NAPR_USL')},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED', ),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    mapEventOrderToForPom = {1: '3', 2: '1', 3: '1', 4: '3', 5: '3', 6: '2'}
    mapEventOrderToPPer = {5: '4', 7: '3'}

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)
        CExportHelperMixin.__init__(self)

        self._coefficientCache = {}
        self._reasonCache = {}
        self._dispanserCache = {}
        self._vidVmeCodeCache = {}


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        population = self.contractAttributeByType(
            u'населениесмп', params['contractId'])
        population = forceDouble(population) if population else 0.0
        emergency = self.contractAttributeByType(u'смп', params['contractId'])
        emergency = forceDouble(emergency) if emergency else 0.0

        payerMiacCode = forceString(self._parent.db.translate(
                'Organisation', 'id', params['payerId'], 'miacCode'))
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.1.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', forceString(
            self._parent.getCompleteEventCount()))
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE',    str(params['accId']))
        self.writeTextElement('CODE_MO', params['lpuMiacCode'])
        self.writeTextElement('YEAR',    str(settleDate.year()))
        self.writeTextElement('MONTH',   str(settleDate.month()))
        self.writeTextElement('NSCHET',  params['NSCHET'])
        self.writeTextElement('DSCHET',  settleDate.toString(Qt.ISODate))

        if payerMiacCode:
            self.writeTextElement('PLAT', payerMiacCode)

        self.writeTextElement('SUMMAV', str(params['SUMMAV']))
        if params['registryType'] == CExportPage1.registryTypeA1:
            if params['SUM_POD_DOP']:
                self.writeTextElement('SUM_POD_DOP', str(params['SUM_POD_DOP']))
            if params['SUM_POD']:
                self.writeTextElement('SUM_POD', str(params['SUM_POD']))
            if params['SUM_FAP']:
                self.writeTextElement('SUM_FAP', str(params['SUM_FAP']))
            self.writeTextElement('SUM_U',   str(params['SUM_U']))
        params['emergency'] = emergency*population
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        lastEventId = forceRef(record.value('lastEventId'))
        params['isDiagnostics'] = forceBool(record.value('isDiagnostics'))

        if (clientId != params.setdefault('lastClientId')
                or lastEventId != params.setdefault('lastComleteEventId')
                or params['isDiagnostics']
                or params['isDiagnostics'] != params.setdefault(
                    'lastWasDiagnostic')):
            if params['lastClientId']:
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                params['lastRecord'],
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['recNum']))
            self.writeTextElement('PR_NOV', params['isReexposed'])
            self.writeClientInfo(record, params)

            if (params['isDiagnostics'] and
                    lastEventId != params.setdefault('lastComleteEventId')):
                params['diagnosticNumber'] = 1

            params['lastClientId'] = clientId
            params['lastEventId'] = None
            params['lastComleteEventId'] = None
            params['lastWasDiagnostic'] = params['isDiagnostics']
            params['recNum'] += 1

        self.writeCompleteEvent(record, params)
        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))

        if lastEventId == params.get('lastComleteEventId'):
            return

        if params['lastEventId']:
            self.writeEndElement()
            self.writeGroup('Z_SL', self.completeEventFields2,
                            params['lastRecord'],
                            closeGroup=True,
                            openGroup=False)

        eventOrder = forceInt(record.value('eventOrder'))
        record.setValue('Z_SL_FOR_POM', self.mapEventOrderToForPom.get(
            eventOrder, ''))

        params['idsp'] = forceInt(record.value('Z_SL_IDSP'))

        if params['idsp'] in (25, 31):
            record.setValue('Z_SL_SUMV', toVariant(0))
            record.setValue('SL_SUM_M',  toVariant(0))
            record.setValue('USL_SUMV_USL', toVariant(0))
        else:
            record.setValue('Z_SL_SUMV', toVariant(
                params['completeEventSum'].get(lastEventId)))

        if record.isNull('Z_SL_NPR_MO'):
            record.setValue('Z_SL_NPR_MO',  toVariant(params['lpuMiacCode']))

        record.setValue('Z_SL_KD_Z', toVariant(params['completeBedDays'].get(lastEventId)))

        if params['isDiagnostics']:
            self._prepareDiagnosticsCompleteEventFields(record, params)

        self.writeGroup('Z_SL', self.completeEventFields1, record,
                        closeGroup=False,
                        dateFields=self.completeEventDateFields)
        params['lastComleteEventId'] = forceRef(record.value('lastEventId'))
        params['lastEventId'] = None
        params['lastRecord'] = record


    def prepareCoefficients(self, coefficients):
        u"""Готовит блок SL_KOEF"""
        result = {}

        for _, i in coefficients.iteritems():
            for key, val in i.iteritems():
                if key == u'__all__':
                    continue

                code = self.getCoefficientRegionalCode(key)

                if code:
                    result.setdefault('SL_KOEF_IDSL', []).append(code[:4])
                    result.setdefault('SL_KOEF_Z_SL', []).append('%1.5f' % (val + 1))

        return result


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        if eventId == params.setdefault('lastEventId'):
            return

        patrName = forceString(record.value('PERS_OT'))
        params['eventProfileRegionalCode'] = forceInt(record.value(
            'eventProfileRegionalCode'))
        eventOrder = forceInt(record.value('eventOrder'))
        medicalAidTypeCode = params['medicalAidType'].get(eventId, 0)

        local_params = {
            'SL_OS_SLUCH': '2' if (not patrName or
                                      patrName.upper() == u'НЕТ') else '',
            'SL_VERS_SPEC': 'V021',
            'SL_KD': params['bedDays'].get(eventId)
        }
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)

        local_params['SL_DN'], isObserved = self.getDispanserCode(forceRef(
            record.value('dispanserId')))

        if forceString(local_params['SL_DN']) != '1' and forceString(local_params['SL_DN']) != '2':
            record.setNull('SL_DN_DATE')

        if forceInt(record.value('Z_SL_USL_OK')) == 3:
            if isObserved:
                record.setValue('SL_P_CEL', toVariant('1.3'))
            elif not forceString(record.value('SL_P_CEL')):
                eventTypeId = forceRef(record.value('eventTypeId'))
                record.setValue('SL_P_CEL', toVariant(
                    self.getReason(eventTypeId)))

        mkb = forceString(record.value('SL_DS1'))
        if ((mkb[:1] == 'Z'
                and medicalAidTypeCode not in self._parent.stomatologyCodes)
             or (medicalAidTypeCode in self._parent.stomatologyCodes
                    and mkb == 'Z01.2')):
            record.setValue('SL_P_CEL', toVariant('2.6'))

        if params['isHospital']:
            local_params['SL_EXTR'] = (forceString(
                eventOrder) if eventOrder in (1, 2)  else '')
            local_params['SL_P_PER'] = self.mapEventOrderToPPer.get(
                eventOrder)
            record.setValue('SL_ED_COL', toVariant(params['bedDays'].get(eventId)))

            hospActionId = forceRef(record.value('hospActionId'))
            if hospActionId:
                action = CAction.getActionById(hospActionId)
                bedCode = self.getHospitalBedProfileTfomsCode(
                    self.getHospitalBedProfileId(forceRef(action[u'койка'])))
                local_params['SL_PROFIL_K'] = bedCode

            if not local_params['SL_P_PER']:
                delivered = forceString(record.value('delivered')) == u'СМП'
                local_params['SL_P_PER'] = '2' if delivered else '1'
        elif params['eventProfileRegionalCode'] == 6: #стоматология
            record.setValue('SL_TARIF', toVariant(
                self.contractAttributeByType(u'ует', params['contractId'])))

        local_params.update(params)
        params['USL_IDSERV'] = 0

        if params['lastEventId']:
            self.writeEndElement() # SL

        self.eventHospSubGroup = self.eventHospSubGroupA4 if forceInt(params['registryType']) else self.eventHospSubGroupA1
        subGroup = copy.deepcopy(self.eventHospSubGroup if params['isHospital']
                                 else self.eventSubGroup)
        if params['isHospital']:
            local_params['KSG_KPG_VER_KSG'] = forceString(params['settleDate'].year())
            local_params['KSG_KPG_KSG_PG'] = '0'
            local_params['KSG_KPG_SL_K'] = '0'
            local_params['KSG_KPG_KOEF_D'] = '1.00000'
            mesLevel = forceInt(record.value('invoiceMesLevel'))

            if mesLevel == 2:
                contractAttr = (u'КС' if medicalAidTypeCode in (1, 2, 3)
                                else u'ДС')
            else:
                contractAttr = (u'КС_пр' if medicalAidTypeCode in (1, 2, 3)
                                else u'ДС_пр')

            local_params['KSG_KPG_BZTSZ'] = self.contractAttributeByType(
                contractAttr, params['contractId'])
            local_params['KSG_KPG_KOEF_UP']  = '1.00000'


            usedCoefficients = forceString(record.value('usedCoefficients'))

            if usedCoefficients:
                coefficients = json.loads(usedCoefficients)

                for _, i in coefficients.iteritems():
                    flag = False

                    for key, val in i.iteritems():
                        if key[:5] == 'DS_uk':
                            local_params['KSG_KPG_KOEF_UP'] = u'%.1f' % val
                            flag = True

                    if flag:
                        continue

                    if i['__all__'] > 1:
                        local_params['KSG_KPG_IT_SL'] = u'%.5f' %  i['__all__']

                if local_params.has_key('KSG_KPG_IT_SL'):
                    local_params.update(self.prepareCoefficients(
                        coefficients))
            else:
                subGroup['KSG_KPG']['subGroup'] = None

            coef = (forceDouble(local_params['KSG_KPG_BZTSZ']
                    if local_params['KSG_KPG_BZTSZ'] else 0.0))

            if coef != 0:
                record.setValue('KSG_KPG_KOEF_U', u'%.5f' % (forceDouble(
                    record.value('KSG_KPG_KOEF_U')) / coef))
            else:
                record.setNull('KSG_KPG_KOEF_U')
        record.setValue('KSG_KPG_KOEF_Z', '%.5f' % forceDouble(record.value('KSG_KPG_KOEF_Z')))

        if local_params.has_key('KSG_KPG_IT_SL'):
            if forceDouble(local_params['KSG_KPG_IT_SL']) > 1:
                local_params['KSG_KPG_SL_K'] =  '1'
                record.setValue('KSG_KPG_SL_K',  '1')
        else:
            local_params['KSG_KPG_SL_K'] =  '0'
            record.setValue('KSG_KPG_SL_K',  '0')

        local_params['KSG_KPG_CRIT'] = forceString(
            record.value('critList')).split(',')

        if medicalAidTypeCode == 4:
            if forceInt(record.value('SL_ED_COL')) == 0:
                record.setValue('SL_ED_COL', toVariant(1))

        local_params.update(params['onkologyInfo'].get(eventId, {}))
        local_params.update(params['medicalSuppliesInfo'].get(eventId, {}))

        if forceString(record.value('CONS_PR_CONS')) == u'':
            record.setValue('CONS_PR_CONS', toVariant('0'))
        if params['isDiagnostics']:
            self._prepareDiagnosticsEventFields(record, local_params)
        if params['isHospital'] and forceBool(record.value('isCovid')):
            record.setValue('SL_PODR', toVariant('010028'))
            local_params['SL_PROFIL_K'] = '24'
            record.setValue('SL_PROFIL', toVariant('28'))
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.eventFields = self.eventFieldsA4 if forceInt(params['registryType']) else self.eventFieldsA1
        self.writeGroup('SL', self.eventFields, _record, subGroup,
            closeGroup=False, dateFields=self.eventDateFields)
        params['lastEventId'] = eventId


    def exportVisits(self, eventId, params):
        u"""Экспортирует данные для визитов с 0 стоимостью,
            при тарификации по посещениям"""
        stmt = u"""SELECT
            PersonOrganisation.miacCode AS USL_LPU,
            ExecPersonOrgStructure.infisCode AS USL_LPU_1,
            PersonOrgStructure.tfomsCode AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS USL_PROFIL,
            IF(SUBSTR(rbService.code, 1, 3) = 'A16', rbService.code, '') AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            Visit.date AS USL_DATE_IN,
            Visit.date AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            IF(rbService.infis IS NULL OR rbService.infis = '',
                rbService.code, rbService.infis) AS USL_CODE_USL,
            1 AS USL_KOL_USL,
            0 AS USL_TARIF,
            0 AS USL_SUMV_USL,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.federalCode AS MR_USL_N_CODE_MD,
            Event.id AS eventId
        FROM Visit
        LEFT JOIN Event ON Event.id = Visit.event_id
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Event.id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                  AND Diagnostic.deleted = 0 )
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN Person ON Person.id = Visit.person_id
        LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
        LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
        LEFT JOIN Person AS ExecPerson ON ExecPerson.id = Event.execPerson_id
        LEFT JOIN OrgStructure AS ExecPersonOrgStructure ON ExecPerson.orgStructure_id = ExecPersonOrgStructure.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbEventProfile ON rbEventProfile.id = EventType.eventProfile_id
        WHERE Visit.event_id = {eventId}
            AND Visit.deleted = '0'
            AND rbEventProfile.regionalCode != '6' -- исключаем стоматологию
        ORDER BY Visit.date""".format(
            eventId=eventId, unit=params['medicalAidUnit'])

        query = self._parent.db.query(stmt)
        result = False

        if query.size() > 1:
            curPos = 1
            querySize = query.size()

            while query.next():
                record = query.record()
                params['isLastVisit'] = curPos == querySize

                self.writeService(record, params)
                curPos += 1

            result = True

        return result


    def exportUziServices(self, eventId, params):
        u"""Выгружает в блоки USL действия из вкладки Диагностика(ActionType.class = 2),
        со всеми возможными тегами, в том числе VID_VME, с нулевой стоимостью
        (SUMV_USL = 0), если код профиля мед.помощи ном. услуги услуг
         - 106(УЗИ), 78(Рентгенология) или 123(Эндоскопия)"""

        stmt = """SELECT
            PersonOrganisation.miacCode AS USL_LPU,
            PersonOrgStructure.infisCode AS USL_LPU_1,
            PersonOrgStructure.tfomsCode AS USL_PODR,
            rbMedicalAidProfile.code AS USL_PROFIL,
            rbService_Identification.value AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            Action.begDate AS USL_DATE_IN,
            Action.endDate AS USL_DATE_OUT,
            Action.MKB AS USL_DS,
            NomenclativeService.infis AS USL_CODE_USL,
            Action.amount AS USL_KOL_USL,
            0 AS USL_TARIF,
            0 AS USL_SUMV_USL,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.federalCode AS MR_USL_N_CODE_MD,
            Event.id AS eventId
        FROM Action
        LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
        LEFT JOIN Person ON Action.person_id = Person.id
        LEFT JOIN Organisation AS PersonOrganisation ON
            Person.org_id = PersonOrganisation.id
        LEFT JOIN OrgStructure AS PersonOrgStructure ON
            Person.orgStructure_id = PersonOrgStructure.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService AS NomenclativeService ON
            ActionType.nomenclativeService_id = NomenclativeService.id
        LEFT JOIN rbMedicalAidProfile ON
            NomenclativeService.medicalAidProfile_id = rbMedicalAidProfile.id
        LEFT JOIN rbService_Identification ON
            rbService_Identification.master_id = NomenclativeService.id AND
            rbService_Identification.deleted = 0 AND
            rbService_Identification.system_id IN (
                SELECT id FROM rbAccountingSystem WHERE urn = 'tfoms60:V001')
        LEFT JOIN Event ON Action.event_id = Event.id
        LEFT JOIN Client ON Client.id = Event.client_id
        WHERE Action.event_id = {eventId}
            AND Action.deleted = 0
            AND ActionType.class = 1
            AND rbMedicalAidProfile.code IN (78, 106, 123)
        """.format(eventId=eventId)
        query = self._parent.db.query(stmt)

        while query.next():
            record = query.record()

            self.writeService(record, params)


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""

        if params['isDiagnostics']:
            params['USL_IDSERV'] = 1
            self._prepareDiagnosticsServiceFields(record, params)
            _record = CExtendedRecord(record, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroupA1)
            return

        eventId = forceRef(record.value('eventId'))
        isVisitExported = False

        idsp = params['idsp']
        if idsp == 25:
            record.setValue('USL_SUMV_USL', toVariant(0))

        medicalAidTypeCode = params['medicalAidType'].get(eventId, 0)

        if medicalAidTypeCode == 9:
            record.setNull('USL_TARIF')

        if (eventId and
             eventId not in params.setdefault('exportedEvents', set())):
            params['tarif'] = record.value('SL_TARIF')
            params['sum'] = record.value('Z_SL_SUMV')
            params['amount'] = record.value('SL_ED_COL')
            params['medicalAidUnit'] = forceString(record.value('Z_SL_IDSPFEDERAL'))
            params['exportedEvents'].add(eventId)
            isVisitExported = self.exportVisits(eventId, params)

        uziKtFgdsCode = forceInt(record.value('uziKtFgdsCode'))
        if uziKtFgdsCode in (1, 2):
            serviceCode = forceString(record.value('USL_CODE_USL'))
            record.setValue('USL_VID_VME', toVariant(self.getVidVmeCode(
                eventId, serviceCode, 'VID_VME')))
            if uziKtFgdsCode == 2:
                params['USL_VID_VME2'] = self.getVidVmeCode(
                    eventId, serviceCode, 'VID_VME2')

        if not isVisitExported and (not params['isHospital'] or params.get('force')):
            if (forceString(record.value('KSG_KPG_N_KSG')) ==
                        forceString(record.value('USL_CODE_USL'))) and not params.get('isOnkservice'):
                return

            params['USL_IDSERV'] += 1

            if params.get('isLastVisit'):
                record.setValue('USL_TARIF', params['tarif'])
                record.setValue('USL_SUMV_USL', params['sum'])

                if params['isHospital']:
                    record.setValue('USL_KOL_USL', params['amount'])

                params['isLastVisit'] = False

            if (params['eventProfileRegionalCode'] in (1, 3)
                    and not params.get('isMesServiceExported')):
                usedCoefficients = forceString(record.value('usedCoefficients'))
                if usedCoefficients:
                    coefficientList = json.loads(usedCoefficients)
                    for _, list in coefficientList.iteritems():
                        for _, value in list.iteritems():
                            if value > 1.0:
                                params['USL_COMENTU'] = value
                                break

                        if params.has_key('USL_COMENTU'):
                            break

            local_params = dict(params)
            local_params.update(params['onkologyInfo'].get(eventId, {}))
            local_params.update(params['implantsInfo'].get(eventId, {}))
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroupA1)

            if params.has_key('USL_COMENTU'):
                params.pop('USL_COMENTU')

        # выгрузка номенклатурных услуг
        mesService = forceString(record.value('mesServiceInfis'))

        if (params['eventProfileRegionalCode'] in (1, 3)
                and mesService
                and not params.setdefault('isMesServiceExported', False)):
            params['isMesServiceExported'] = True
            record.setValue('USL_CODE_USL', toVariant(mesService))
            record.setValue('USL_SUMV_USL', toVariant(0))
            record.setNull('USL_TARIF')
            record.setValue('USL_DATE_IN', record.value('mesActionBegDate'))
            record.setValue('USL_DATE_OUT', record.value('mesActionEndDate'))
            record.setValue('USL_KOL_USL', record.value('amount'))
            params['force'] = True
            self.writeService(record, params)
            params['isMesServiceExported'] = False
            params['force'] = False

        onkDiag = (forceString(record.value('SL_DS1'))[:1] == 'C' or
                   forceString(record.value('SL_DS2'))[:1] == 'C' or
                   forceString(record.value('SL_DS3'))[:1] == 'C')

        if (params['isHospital'] and not mesService and onkDiag and
                not params.setdefault('isOnkServiceExported', False)):
            params['isOnkServiceExported'] = True
            params['force'] = True
            record.setValue('USL_CODE_USL', record.value('SL_CODE_MES1'))
            record.setValue('USL_KOL_USL', toVariant(1))
            record.setValue('USL_SUMV_USL', toVariant(0))
            record.setValue('USL_DATE_IN', record.value('SL_DATE_1'))
            record.setValue('USL_DATE_OUT', record.value('SL_DATE_1'))
            record.setNull('USL_TARIF')
            self.writeService(record, params)
            params['isOnkServiceExported'] = False
            params['force'] = False


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        _record = CExtendedRecord(record, params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            self.writeEndElement() # SL
            self.writeGroup('Z_SL', self.completeEventFields2,
                            params['lastRecord'],
                            closeGroup=True,
                            openGroup=False)
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def getCoefficientRegionalCode(self, code):
        u'Возвращает региональный код коэффициента по его имени'
        result = self._coefficientCache.get(code, -1)

        if result == -1:
            result = forceString(self._parent.db.translate(
                     'rbContractCoefficientType', 'code', code, 'regionalCode'))
            self._coefficientCache[code] = result

        return result


    def getReason(self, eventTypeId):
        result = self._reasonCache.get(eventTypeId, -1)

        if result == -1:
            stmt = """SELECT value
            FROM EventType_Identification
            WHERE EventType_Identification.master_id = '{eventTypeId}'
                AND EventType_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE code = 'tfomsPCEL'
                  AND domain = 'EventType'
            )""".format(eventTypeId=eventTypeId)

            query = self._parent.db.query(stmt)
            result = ''

            if query.first():
                record = query.record()
                result = forceString(record.value(0))

            self._reasonCache[eventTypeId] = result

        return result


    def getDispanserCode(self, dispanserId):
        result = self._dispanserCache.get(dispanserId, -1)

        if result == -1:
            result = ('', False)

            if dispanserId:
                stmt = u"""SELECT
                    CASE
                        WHEN rbDispanser.observed = 1 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                        WHEN rbDispanser.observed = 1 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                        WHEN rbDispanser.observed = 0 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                        WHEN rbDispanser.observed = 0 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                        ELSE NULL
                    END AS dispanserObserved,
                    rbDispanser.observed
                FROM rbDispanser
                WHERE rbDispanser.id = {0}""".format(dispanserId)
                query = self._parent.db.query(stmt)

                if query and query.first():
                    record = query.record()
                    result = (forceString(record.value(0)),
                              forceInt(record.value(1)))
                    self._dispanserCache[dispanserId] = result

        return result


    def getVidVmeCode(self, eventId, serviceCode, identificationCode):
        u"""Возвращает Action.actionType_id->ActionType.nomenclativeService_id
            ->rbService.infis - по действию (первому найденному) из раздела
            "Диагностика" (ActionType.class = 1), если услуга
            nomenclativeService_id действия содержит в идентификации кодом
            code код услуги данного обращения-<CODE_USL> данного блока <USL>"""
        key = (eventId, serviceCode, identificationCode)
        result = self._vidVmeCodeCache.get(key, -1)

        if result == -1:
            result = None
            stmt = """SELECT rbService.infis
                      FROM Action
                      INNER JOIN ActionType ON ActionType.id = Action.actionType_id
                      INNER JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
                      INNER JOIN rbService_Identification ON rbService_Identification.master_id = rbService.id
                      INNER JOIN rbAccountingSystem ON rbAccountingSystem.id = rbService_Identification.system_id
                      WHERE Action.deleted=0
                        AND Action.event_id = {eventId}
                        AND Action.status IN (2, 4)
                        AND ActionType.class = 1
                        AND rbAccountingSystem.code = '{code}'
                        AND rbService_Identification.deleted=0
                        AND rbService_Identification.value = '{serviceCode}'
                      ORDER BY Action.id asc, rbService_Identification.id desc
                      LIMIT 1""".format(eventId=eventId,
                                        code=identificationCode,
                                        serviceCode=serviceCode)
            query = self._parent.db.query(stmt)

            if query and query.first():
                record = query.record()
                result = forceString(record.value(0))

            self._vidVmeCodeCache[key] = result
        return result


    def _prepareDiagnosticsCompleteEventFields(self, record, params):
        if not forceBool(record.value('isDiag20')):
            idCase = '{0}999{1}'.format(
                forceInt(record.value('eventId')),
                params.setdefault('diagnosticNumber', 1))
            params['diagnosticNumber'] += 1
        else:
            idCase = record.value('eventId')

        for field, val in (('IDCASE', idCase),
                ('USL_OK', '3'),
                ('VIDPOM', '13'),
                ('FOR_POM', '3'),
                ('RSLT', '314'),
                ('ISHOD', record.value('diagnosticResult')),
                ('IDSP', '28'),
                ('SUMV', record.value('sum')),
                ('NPR_DATE', record.value('actionDirectionDate')),
                ('DATE_Z_1', record.value('actionEndDate')),
                ('DATE_Z_2', record.value('actionEndDate'))):
            record.setValue('Z_SL_{0}'.format(field), toVariant(val))


    mapServiceCodeToMkb = {'022001': 'K29.9',
                           '022003': 'K64.9',
                           '021001': 'I11.9',
                           '021003': 'I11.9'}


    def _prepareDiagnosticsEventFields(self, record, params):
        profile = forceString(record.value('SL_PROFIL'))
        if not profile:
            serviceCode = forceString(record.value('USL_CODE_USL'))[:3]
            if serviceCode == '022':
                profile = '123'
            elif serviceCode == '021':
                profile = '106'
        mkb = forceString(record.value('SL_DS1'))
        if not forceBool(record.value('isDiag20')):
            if not mkb:
                mkb = forceString(record.value('actionMkb'))
            if not mkb:
                serviceCode = forceString(record.value('USL_CODE_USL'))[:6]
                mkb = ('I11.9' if serviceCode[:3] == '021' else
                       self.mapServiceCodeToMkb.get(serviceCode))

        for field, val in (('SL_ID', record.value('Z_SL_IDCASE')),
                ('PROFIL', profile),
                ('P_CEL', '2.6'),
                ('DATE_1', record.value('actionEndDate')),
                ('DATE_2', record.value('actionEndDate')),
                ('C_ZAB', '3'),
                ('ED_COL', '1'),
                ('SUM_M', record.value('sum')),
                ('IDDOKT', record.value('actionPersonFederalCode')),
                ('LPU_1', record.value('actionPersonOrgStructureInfisCode')),
                ('PODR', record.value('actionPersonOrgStructureTfomsCode')),
                ('PRVS', record.value('actionPersonSpecialityFederalCode')),
                ('DS1', mkb)):
            record.setValue('SL_{0}'.format(field), toVariant(val))



    def _prepareDiagnosticsServiceFields(self, record, params):
        for field, val in (('DATE_IN', record.value('actionEndDate')),
                ('DATE_OUT', record.value('actionEndDate')),
                ('LPU_1', record.value('SL_LPU_1')),
                ('PODR', record.value('SL_PODR')),
                ('PRVS', record.value('SL_PRVS')),
                ('PROFIL', record.value('SL_PROFIL')),
                ('KOL_USL', 1),
                ('DS', record.value('SL_DS1')),
                ('SUMV_USL', record.value('sum')),
                ('CODE_USL', record.value('serviceInfis'))):
            record.setValue('USL_{0}'.format(field), toVariant(val))

        for field, val in (('PRVS', record.value('SL_PRVS')),
                ('CODE_MD', record.value('SL_IDDOKT'))):
            record.setValue('MR_USL_N_{0}'.format(field), toVariant(val))


# ******************************************************************************


class CR60OnkologyInfo(COnkologyInfo):
    mapProtName = {
        u'Противопоказания к проведению хирургического лечения': '1',
        u'Противопоказания к проведению химиотерапевтического лечения': '2',
        u'Отказ от проведения хирургического лечения': '4',
        u'Отказ от проведения химиотерапевтического лечения': '5',
    }

    def __init__(self):
        COnkologyInfo.__init__(self)

    def get(self, _db, idList, parent):
        u"""Возвращает словарь с записями по онкологии и направлениям,
            ключ - идентификатор события"""

        stmt = u"""SELECT Event.id AS eventId,
            rbEventTypePurpose.regionalCode AS uslOk,
            rbMedicalAidUnit.federalCode as medicalFederalCode,
            rbDiseasePhases.code AS diseasePhaseCode,
            Diagnosis.MKB,
            IF(GistologiaAction.id IS NOT NULL, 1,
                IF(ImmunohistochemistryAction.id IS NOT NULL, 2,
                    0)) AS DIAG_TIP,
            rbTNMphase_Identification.value AS STAD,
            rbTumor_Identification.value AS ONK_T,
            rbNodus_Identification.value AS ONK_N,
            rbMetastasis_Identification.value AS ONK_M,
            GistologiaAction.id AS gistologiaActionId,
            ImmunohistochemistryAction.id AS immunohistochemistryActionId,
            ControlListOnkoAction.id AS controlListOnkoActionId,
            ConsiliumAction.id AS consiliumActionId,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE (AT.flatCode = 'inspectionDirection' or AT.flatCode = 'ConsultationDirection' or
                                    AT.flatCode = 'hospitalDirection' or AT.flatCode ='recoveryDirection')
            )) AS directionActionId,
            IF(rbMedicalAidType.code = '6',
                IF(rbDispanser.observed = 1, '1.3',
                    EventType_Identification.value), '') AS pCel,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'MedicalSupplies'
            )) AS medicalSuppliesActionId,
            (SELECT AT.code
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.group_id IN (
                            SELECT id FROM ActionType AT1
                            WHERE AT1.flatCode = 'codeSH')
                WHERE A.event_id = Event.id AND A.deleted = 0
                LIMIT 0,1
            ) AS LEK_PR_CODE_SH,
            KFrAction.id AS kFrActionId
        FROM Account_Item
        LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN Diagnostic ON (Diagnostic.event_id = Account_Item.event_id
            AND Diagnostic.diagnosisType_id IN (
                SELECT id
                FROM rbDiagnosisType
                WHERE code IN ('1', '2', '9'))
            AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
            AND Diagnosis.deleted = 0 AND (Diagnosis.MKB LIKE 'C%' OR Diagnosis.MKB LIKE 'D0%')
        LEFT JOIN rbDiseasePhases ON Diagnostic.phase_id = rbDiseasePhases.id
        LEFT JOIN rbTNMphase ON rbTNMphase.id = IFNULL(Diagnostic.pTNMphase_id, Diagnostic.cTNMphase_id)
        LEFT JOIN rbTumor ON rbTumor.id = IFNULL(Diagnostic.pTumor_id, Diagnostic.cTumor_id)
        LEFT JOIN rbNodus ON rbNodus.id = IFNULL(Diagnostic.pNodus_id, Diagnostic.cNodus_id)
        LEFT JOIN rbMetastasis ON rbMetastasis.id = IFNULL(Diagnostic.pMetastasis_id, Diagnostic.cMetastasis_id)
        LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
        LEFT JOIN Action AS GistologiaAction ON GistologiaAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id = (
                SELECT MAX(AT.id)
                FROM ActionType AT
                WHERE AT.flatCode ='Gistologia'
              )
        )
        LEFT JOIN Action AS ImmunohistochemistryAction ON ImmunohistochemistryAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='Immunohistochemistry'
              )
        )
        LEFT JOIN Action AS ControlListOnkoAction ON ControlListOnkoAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='ControlListOnko'
              )
        )
        LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
        LEFT JOIN EventType_Identification ON
            EventType_Identification.master_id = EventType.id
            AND EventType_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfomsPCEL'
        )
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN Action AS ConsiliumAction ON ConsiliumAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='Consilium'
              )
        )
        LEFT JOIN rbTNMphase_Identification ON
            rbTNMphase_Identification.master_id = IFNULL(
                Diagnostic.cTNMphase_id, Diagnostic.pTNMphase_id)
            AND rbTNMphase_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'TNMphase'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                Diagnostic.cTumor_id, Diagnostic.pTumor_id)
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Tumor'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                Diagnostic.cNodus_id, Diagnostic.pNodus_id)
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Nodus'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                Diagnostic.cMetastasis_id, Diagnostic.pMetastasis_id)
            AND rbMetastasis_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Metastasis'
            )
        LEFT JOIN Action AS KFrAction ON KFrAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.group_id IN (
                    SELECT AT1.id FROM ActionType AT1
                    WHERE AT1.flatCode ='DiapFR')
              )
        )
        WHERE Account_Item.reexposeItem_id IS NULL
          AND Diagnosis.MKB IS NOT NULL
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""" .format(idList=idList)

        query = _db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result[eventId] = self._processOnkRecord(record, parent)

        return result


    def _processOnkRecord(self, record, parent):
        data = COnkologyInfo._processOnkRecord(self, record, parent)
        if data['SL_DS_ONK'] == 0:
            data['SL_DS_ONK'] = '0' # обязательно выгружаем 0
        if data.has_key('ONK_SL_DS1_T') and data['ONK_SL_DS1_T'] not in (1, 2):
            data['ONK_SL_MTSTZ'] = None
        if (data.has_key('ONK_SL_DS1_T') and data['ONK_SL_DS1_T'] not in (0, 1, 2)) or (data.has_key('uslOk') and data['uslOk'] not in (1, 2)):
            data['ONK_USL_USL_TIP'] = None
        if data.has_key('ONK_SL_DS1_T') and data['ONK_SL_DS1_T'] not in (0, 1, 2, 3, 4):
            data['ONK_SL_STAD'] = None
            data['ONK_SL_ONK_T'] = None
            data['ONK_SL_ONK_N'] = None
            data['ONK_SL_ONK_M'] = None
        return data


    def _removeUnnessesaryFields(self, data):
        u'Убирает ненужные поля для разных типов услуг'

        if data.get('ONK_USL_USL_TIP') != '1':
            data['ONK_USL_HIR_TIP'] = None

        if data.get('ONK_USL_USL_TIP') not in ('3', '4'):
            data['ONK_SL_SOD'] = None
            data['ONK_USL_LUCH_TIP'] = None

        if data.get('ONK_USL_USL_TIP') != '2':
            data['ONK_USL_LEK_TIP_L'] = None
            data['ONK_USL_LEK_TIP_V'] = None

        if data.get('ONK_USL_USL_TIP') not in ('2', '4'):
            data['ONK_USL_PPTR'] = None

        if not data.get('ONK_USL_USL_TIP'):
            data['ONK_USL_USL_TIP'] = '5'


    def _processDiagnostics(self, record, data):
        u'Заполняет поля для диагностик'
        for field, diagType in (('gistologiaActionId', 1),
                                ('immunohistochemistryActionId', 2)):
            _id = forceRef(record.value(field))
            action = CAction.getActionById(_id) if _id else None

            if not (action and action.getProperties()):
                continue

            diagDate = forceDate(action.getRecord().value('endDate')).toString(
                Qt.ISODate)

            for prop in action.getProperties():
                if forceString(prop.type().shortName) == 'DIAG_DATE':
                    val = prop.getValue()

                    if val.isValid():
                        diagDate = val.toString(Qt.ISODate)

                    continue

                text = prop.getTextScalar().strip()
                descr = forceString(prop.type().descr).strip()

                if not text and not descr:
                    continue

                data.setdefault('B_DIAG_DIAG_DATE', []).append(diagDate)
                data.setdefault('B_DIAG_DIAG_TIP', []).append(diagType)
                data.setdefault('B_DIAG_DIAG_CODE1', []).append(descr)
                rslt = mapDiagRslt.get(text, 0)
                data.setdefault('B_DIAG_DIAG_RSLT1', []).append(rslt)
                data.setdefault('B_DIAG_REC_RSLT', []).append(
                    1 if rslt else None)


    def _processControlList(self, record, data):
        u'Заполняет поля из контрольного листка'
        _id = forceRef(record.value('controlListOnkoActionId'))
        action = CAction.getActionById(_id) if _id else None

        if action:
            for prop in action.getProperties():
                shortName = prop.type().shortName
                name = prop.type().name
                descr = prop.type().descr

                if shortName == 'PROT':
                    date = prop.getValueScalar()

                    if (date is not None and isinstance(date,  QDate)
                            and date.isValid() and name):
                        data.setdefault('B_PROT_PROT', []).append(
                            self.mapProtName.get(name))
                        data.setdefault('B_PROT_D_PROT', []).append(
                            date.toString(Qt.ISODate))
                if descr == 'SOD':
                    data['ONK_SL_SOD'] = prop.getValueScalar()
                elif self.__mapPropDescr__.has_key(prop.type().descr):
                    data[self.__mapPropDescr__[prop.type().descr]] = prop.getValue()
                elif prop.type().descr == 'PPTR':
                    val = prop.getValue()
                    if val:
                        data['ONK_USL_PPTR'] = mapPptr.get(val.lower())

        if forceInt(record.value('diseasePhaseCode')) == 3:
            data['ONK_SL_DS1_T'] = 1
        elif forceInt(record.value('diseasePhaseCode')) == 1:
            data['ONK_SL_DS1_T'] = 2
        elif forceInt(record.value('diseasePhaseCode')) == 2:
            data['ONK_SL_DS1_T'] = 4
        else:
            if forceInt(record.value('medicalFederalCode')) != 31:
                data['ONK_SL_DS1_T'] = 6
            else:
                data['ONK_SL_DS1_T'] = None


    def _processConsilium(self, record, data):
        COnkologyInfo._processConsilium(self, record, data)

        if 'CONS_PR_CONS' not in data.keys():
            data['CONS_PR_CONS'] = '0'


    def _processDirection(self, record, data, parent):
        u'Заполняет поля для направлений'
        actionIdList = forceString(record.value(
            'directionActionId'))
        actionIdList = actionIdList.split(',') if actionIdList else []

        for actionId in actionIdList:
            action = CAction.getActionById(forceRef(actionId))
            directionDate = forceDate(action.getRecord().value('endDate'))
            directionOrgId = forceRef(action.getProperty(
                u'Куда направляется').getValue()) if action.hasProperty(
                    u'Куда направляется') else None
            data.setdefault('NAPR_NAPR_MO', []).append(
                COrganisationMiacCodeCache.getCode(
                    directionOrgId if directionOrgId !=
                    QtGui.qApp.currentOrgId() else None))
            naprDate = forceString(directionDate.toString('yyyy-MM-dd'))
            if directionDate.isValid():
                data.setdefault('NAPR_NAPR_DATE', []).append(naprDate)
            else:
                data.setdefault('NAPR_NAPR_DATE', []).append(None)

            if action:
                if action.hasProperty(u'Профиль'):
                    bedProfileId = action.getProperty(u'Профиль').getValue()
                    code = parent.getHospitalBedProfileUsishCode(
                        bedProfileId)
                    if code == '43':
                        data.setdefault('NAPR_NAPR_V', []).append(1)
                        if data['NAPR_NAPR_MO'] == [u'']:
                            data['NAPR_NAPR_MO'][0] = '600002'
                elif action.hasProperty(u'Вид направления'):
                    val = action.getProperty(
                        u'Вид направления').getTextScalar()
                    data.setdefault('NAPR_NAPR_V', []).append(
                        self.__mapDirection__.get(val, 3))
                else:
                    data.setdefault('NAPR_NAPR_V', []).append(None)

                if (data.get('NAPR_NAPR_V', [0])[-1] == 3 and
                        action.hasProperty(
                            u'Метод диагностического исследования')):
                    val = action.getProperty(
                        u'Метод диагностического исследования').getValue()
                    data.setdefault('NAPR_MET_ISSL', []).append(
                        mapMetIssl.get(val))
                else:
                    data.setdefault('NAPR_MET_ISSL', []).append(None)

                if (data.get('NAPR_NAPR_V', [0])[-1] == 3 and data.get(
                        'NAPR_MET_ISSL', [0])[-1] in (1, 2, 3, 4) and
                        action.hasProperty(u'Код услуги')):
                    prop = action.getProperty(u'Код услуги')
                    data.setdefault('NAPR_NAPR_USL', []).append(
                        prop.getValue())
                else:
                    data.setdefault('NAPR_NAPR_USL', []).append(None)



# ******************************************************************************

class PersonalDataWriter(COrder79PersonalDataWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientDateFields = ( 'DR', 'DOCDATE', )
    clientFields = (('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'DR',
                    'DOST', 'TEL', 'FAM_P', 'IM_P', 'OT_P', 'W_P', 'MR',
                    'DOCTYPE', 'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS',
                    'OKATOG', 'OKATOP'))


    def __init__(self, parent):
        COrder79PersonalDataWriter.__init__(self, parent, version='3.2')


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        if record.contains('PERS_TEL'):
            phoneNumber = forceString(record.value('PERS_TEL'))
            record.setValue('PERS_TEL', toVariant(
                    filter(lambda ch: ch not in '+()- ', phoneNumber)[-10:]))

        COrder79PersonalDataWriter.writeClientInfo(self, record, params)

# ******************************************************************************

class CMedicalSuppliesInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        Action.endDate AS LEK_PR_DATA_INJ,
        (SELECT NC.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature N ON N.id = APN.value
         INNER JOIN rbNomenclatureType NT ON N.type_id = NT.id
         INNER JOIN rbNomenclatureKind NK ON NK.id = NT.kind_id
         INNER JOIN rbNomenclatureClass NC ON NC.id = NK.class_id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
          AND APT.descr = 'V032'
         LIMIT 1) AS LEK_PR_CODE_SH,
        (SELECT rbNomenclature.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature ON rbNomenclature.id = APN.value
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.descr = 'N20'
           AND APT.typeName = 'Номенклатура ЛСиИМН'
         LIMIT 1) AS LEK_PR_REGNUM,
        (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_String APS ON APS.id = AP.id
         WHERE APT.descr = 'COD_MARK'
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1) AS LEK_PR_COD_MARK,
        (SELECT UI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature ON rbNomenclature.id = APN.value
         INNER JOIN rbUnit U ON U.id = rbNomenclature.unit_id
         INNER JOIN rbUnit_Identification UI ON UI.master_id = U.id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.descr = 'V034'
           AND UI.system_id = '{sysIdUnit}'
         LIMIT 1) AS LEK_DOSE_ED_IZM,
        (SELECT APD.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
         WHERE APT.descr = 'Доза'
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1) AS LEK_DOSE_DOSE_INJ,
        (SELECT NUT.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureUsingType APN ON APN.id = AP.id
         INNER JOIN rbNomenclatureUsingType NUT ON NUT.id = APN.value
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.descr = 'OID:1.2.643.5.1.13.13.11.1468'
         LIMIT 1) AS LEK_DOSE_METHOD_INJ,
        Action.amount AS LEK_DOSE_COL_INJ
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.code = 'MedicalSupplies'
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""" .format(
            idList=self._idList,
            sysIdUnit=self._parent._getAccSysIdByUrn('urn:oid:V034'))
        return stmt


class CImplantsInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        Action.endDate AS MED_DEV_DATE_MED,
        ActionType.code AS MED_DEV_CODE_MEDDEV,
        (SELECT APS.value FROM ActionProperty AP
          INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
          INNER JOIN ActionProperty_String APS ON APS.id = AP.id
          WHERE APT.descr = 'NUMBER_SER'
            AND AP.deleted = 0 AND AP.action_id = Action.id
          LIMIT 1) AS MED_DEV_NUMBER_SER
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'MED_DEV'
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""" .format(idList=self._idList)
        return stmt

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR60Ambulance,
                      configFileName='75_13_s11.ini',
                      #accNum=u'МАКС (Основной реестр)-118'
                      eventIdList=[1181410]
                      )
