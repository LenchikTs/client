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
u"""Экспорт счетов для Мурманска, Б2,Б5,Б7"""

import json
import os

from PyQt4.QtCore import Qt, QFile
from PyQt4 import QtGui

from library.Utils import (forceDouble, forceInt, forceRef, forceString,
                           forceBool, toVariant, forceDate,
                           formatSNILS as _formatSNILS)

from Accounting.Tariff import CTariff
from Accounting.Utils import getDoubleContractAttribute, getIntContractAttribute

from Events.Action import CAction
from Exchange.Export import (
    CExportHelperMixin, CAbstractExportPage1Xml, record2Dict, CMultiRecordInfo)
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Order79Export import (
    COrder79ExportWizard, COrder79ExportPage1, COrder79ExportPage2,
    COrder79XmlStreamWriter)
from Exchange.ExportR60NativeAmbulance import (
    PersonalDataWriter as CR60PersonalDataWriter)
from Exchange.Utils import compressFileInZip, tbl

from Exchange.Ui_ExportR60NativeAmbulancePage1 import Ui_ExportPage1

DEBUG = False


def exportR51Ambulance(widget, accountId, accountItemIdList, accountIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
    wizard.exec_()


def formatSNILS(snils):
    return _formatSNILS(snils) if forceString(snils) else None

# ******************************************************************************


class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Мурманск"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Мурманска'
        prefix = 'R51NativeAmbulance'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.accountIdList = None
        self.__xmlBaseFileName = None
        self.__xmlFileName = None


    def setAccountIdList(self, accountIdList):
        u"""Запоминает список идентификаторов счетов"""
        self.accountIdList = accountIdList


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return u'%s.zip' % self.getXmlFileName()[:-4]


    def _getXmlBaseFileName(self, _=None):
        u"""Возвращает имя файла для записи данных"""
        result = self.__xmlBaseFileName

        if not result:
            sysIdoid635 = self.page1._getAccSysIdByUrn(
                u'urn:oid:1.2.643.5.1.13.2.1.1.635')
            sysIdTfoms51F003 = self.page1._getAccSysIdByUrn('urn:tfoms51:F003')
            payerCode = self.page1._getOrgIdentification(
                self.info['payerId'], sysIdoid635)
            if not payerCode:
                sysIdTfoms51F002 = self.page1._getAccSysIdByUrn(
                    'urn:tfoms51:F002')
                payerCode = self.page1._getOrgIdentification(
                    self.info['payerId'], sysIdTfoms51F002)
            sysIdTfoms = self.page1._getAccSysId('TFOMS')
            receiver = 'T' if self.page1._getOrgIdentification(
                self.info['payerId'], sysIdTfoms) else 'S'
            record = self.db.getRecord('OrgStructure', 'infisCode,tfomsCode',
                                       self.info['accOrgStructureId'])
            orgStructInfis = forceString(record.value(0)) if record else None
            orgStructTfoms = forceString(record.value(1)) if record else None
            currentOrgId = QtGui.qApp.currentOrgId()
            record = self.db.getRecord('Organisation', 'infisCode,tfomsExtCode',
                                       currentOrgId)
            currentOrgInfis = self.page1._getOrgIdentification(currentOrgId,
                                                       sysIdTfoms51F003)

            if not currentOrgInfis:
                currentOrgInfis = forceString(
                    record.value(0)) if record else None
            currentOrgTfomsExtCode = forceString(
                record.value(1)) if record else None

            result = (u'M{orgInfis}{orgStructInfis}{orgStructTfoms}{receiver}'
                      u'{payerInfis}_{settleYear:02d}{settleMonth:02d}'
                      u'{packetNumber:02d}.xml'.format(
                          orgInfis=currentOrgInfis,
                          orgStructInfis=(orgStructInfis
                                          if orgStructInfis else '00'),
                          orgStructTfoms=(orgStructTfoms
                                          if orgStructTfoms
                                          else currentOrgTfomsExtCode),
                          receiver=receiver, payerInfis=payerCode,
                          packetNumber=self.page1.edtPacketNumber.value(),
                          settleYear=self.info['settleDate'].year() % 100,
                          settleMonth=self.info['settleDate'].month()))
            self.__xmlBaseFileName = result

        return result


    def getXmlFileName(self, _=None):
        u"""Возвращает имя файла для записи данных."""
        result = self.__xmlFileName

        if not result:
            if self.page1.registryType == CExportPage1.REGISTRY_TYPE_B5:
                prefix = 'C'
            elif self.page1.registryType == CExportPage1.REGISTRY_TYPE_B7:
                prefix = 'HW'
            else: # B2
                prefix = 'H'
            result = u'{0}{1}'.format(prefix, self._getXmlBaseFileName())
            self.__xmlFileName = result

        return result


    def getPersonalDataXmlFileName(self, _=None):
        u"""Возвращает имя файла для записи личных данных."""
        prefix = ('W' if self.page1.registryType
                    == CExportPage1.REGISTRY_TYPE_B7 else '')
        return u'L{1}{0}'.format(self._getXmlBaseFileName(), prefix)


    def getRegistryXmlFileName(self):
        u"""Имя файла для формата Б3"""
        prefix = ('W' if self.page1.registryType
                    == CExportPage1.REGISTRY_TYPE_B7 else '')
        return u'T{1}{0}'.format(self._getXmlBaseFileName(), prefix)


    def getRegistryFullXmlFileName(self):
        u"""Имя файла для формата Б3"""
        return os.path.join(self.getTmpDir(), self.getRegistryXmlFileName())

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""
    REGISTRY_TYPE_B2 = 0
    REGISTRY_TYPE_B5 = 1
    REGISTRY_TYPE_B7 = 2

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self),
                     CPersonalDataWriter(self),
                     CRegistryWriter(self))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.chkAmbulancePlanComplete.setVisible(False)
        self.chkEmergencyPlanComplete.setVisible(False)
        self.chkAdditionalSumOfPCF.setVisible(False)
        self.edtAdditionalSumOfPCF.setVisible(False)
        self.cmbRegistryType.clear()
        self.cmbRegistryType.addItems([u'Б2', u'Б5', u'Б7'])
        self.registryType = self.REGISTRY_TYPE_B2
        self._recNum = 1

        self._tblAccountingSystem = tbl('rbAccountingSystem')
        self._tblOrgIdentification = tbl('Organisation_Identification')


    def setExportMode(self, flag):
        self.chkReexposed.setEnabled(not flag)
        self.cmbRegistryType.setEnabled(not flag)
        COrder79ExportPage1.setExportMode(self, flag)


    def prepareStmt(self, params):
        queryParams = {
            'sysIdReab': self._getAccSysId('REAB'),
            'sysIdTfoms51F002': self._getAccSysIdByUrn('urn:tfoms51:F002'),
            'sysIdTfoms51F003Dep': params['sysIdTfoms51F003Dep'],
            'sysIdTfoms51V027': self._getAccSysIdByUrn('urn:tfoms51:V027'),
            'sysIdTfoms51V021': self._getAccSysId('tfoms51.V021'),
            'sysIdTfoms51VIDPOM': self._getAccSysIdByUrn('urn:tfoms51:VIDPOM'),
            'sysIdTfoms51VIDPOM2': self._getAccSysIdByUrn('urn:tfoms51:VIDPOM2'),
            'sysIdTfoms51F003': params['sysIdTfoms51F003'],
            'sysIdTfoms51V001': self._getAccSysIdByUrn('urn:tfoms51:V001'),
            'sysIdTfoms51SubHosp': self._getAccSysIdByUrn('urn:tfoms51:sub_hosp'),
            'sysIdTfoms51DN': self._getAccSysIdByUrn('urn:tfoms51:dn'),
            'sysIdOid635': self._getAccSysIdByUrn(
                'urn:oid:1.2.643.5.1.13.2.1.1.635'),
            'sysIdEmergency': self._getAccSysId(u'НеотлПом'),
            'sysIdMedicalAidType': self._getAccSysId(u'ВидМП'),
            'sysIdTomsPcel': self._getAccSysId('tfomsPCEL'),
            'sysIdIdsp': self._getAccSysId('IDSP'),
            'sysIdIdspMo': self._getAccSysId('IDSP_MO'),
            'payerInfis': forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode')),
            'payerId': params['payerId'],
            'lpuCode': params['lpuCode'],
            'financeType': params['contractFinanceType'],
            'accOrgStructureId': params['accOrgStructureId'],
            'currentOrgId': params['currentOrgId'],
            'policyFields': (u'ClientPolicy.number AS PACIENT_NPOLIS,' if self.registryType == self.REGISTRY_TYPE_B5
                             else u"IF(rbPolicyKind.regionalCode IN ('1', '2'), "
                                  u"   ClientPolicy.number, '') AS PACIENT_NPOLIS,"),
        }

        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            MesService.infis AS mesServiceInfis,
            MesAction.begDate AS mesActionBegDate,
            MesAction.endDate AS mesActionEndDate,
            Account_Item.`sum` AS `sum`,
            Account_Item.amount,
            Account_Item.usedCoefficients,
            Account_Item.action_id AS actionId,
            LastEvent.id AS lastEventId,
            EventType.id AS eventTypeId,
            HospitalAction.id AS hospActionId,
            Diagnostic.dispanser_id AS dispanserId,
            Visit.id AS visitId,
            (EventType.form IN ('001','030')
             AND EventType.regionalCode != '001'
             AND (SELECT tariffType FROM Contract_Tariff
                  WHERE Account_Item.tariff_id = Contract_Tariff.id) = 2
             AND IFNULL(rbMedicalAidUnit.federalCode, 0) != 9
             AND Account_Item.visit_id IS NULL) AS isDiagnostics,
            (SELECT value IS NOT NULL FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdTfoms51DN}'
               LIMIT 1) as isDispensaryObservation,
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
            Event.execDate AS eventExecDate,
            Action.endDate AS actionEndDate,
            PersonOrgStructure.tfomsCode AS personOrgStructureTfomsCode,
            Action.MKB AS actionMkb,
            rbService.infis AS serviceInfis,
            rbMedicalAidType.code AS medicalAidTypeCode,
            Relegate.infisCode AS relegateOrgCode,
            Relegate.id AS relegateOrgId,
            Relegate.tfomsExtCode AS relegateOrgTfomsExtCode,
            IF(Event.nextEventDate, DATE_FORMAT(Event.nextEventDate, '%m%y'),
               DATE_FORMAT(DATE_ADD(Event.execDate, INTERVAL 90 DAY), '%m%y')) AS SL_DN_DATE,
            (SELECT tariffType FROM Contract_Tariff
                  WHERE Account_Item.tariff_id = Contract_Tariff.id) AS tariffType,
            rbSpeciality.federalCode AS specialityFederalCode,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id AND
                      A.deleted = 0 AND
                      A.actionType_id IN (
                            SELECT MAX(AT.id)
                            FROM ActionType AT
                            WHERE AT.flatCode ='moving'
            )) AS hospitalActionIdList,
            PersonOrgStructure.parent_id AS personOrgStructureParentId,
            IF(rbMedicalAidType.code IN (1,2,3,7), LeavedOrgStruct.id,
               VisitPerson.orgStructure_id) AS addrCodeOrgStructId,
            DeliveredBy.value AS deliveredBy,
            age(Client.birthDate, Event.execDate) as clientAge,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.regionalCode = '1', ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            {policyFields}
            IF(rbPolicyKind.regionalCode IN ('1', '2'),
               '', ClientPolicy.number) AS PACIENT_ENP,
            IFNULL((SELECT value FROM Organisation_Identification OID
             WHERE OID.master_id = Insurer.id
               AND OID.deleted = 0 AND OID.system_id = '{sysIdTfoms51F002}'
             LIMIT 1),(SELECT value FROM Organisation_Identification OID
             WHERE OID.master_id = Insurer.id
               AND OID.deleted = 0 AND OID.system_id = '{sysIdOid635}'
             LIMIT 1)) AS PACIENT_SMO,
            Insurer.OKATO AS PACIENT_ST_OKATO,
            Insurer.shortName AS PACIENT_SMO_NAM,
            (SELECT TID.code FROM TempInvalid TI
             LEFT JOIN rbTempInvalidDocument AS TID ON TID.id = TI.doctype
             LEFT JOIN rbTempInvalidResult AS TIR ON TIR.id = TI.result_id
             WHERE TI.client_id = Client.id
              AND TI.begDate BETWEEN Event.setDate AND Event.execDate
              AND TI.type = 1 AND TI.deleted = 0 AND TID.code = 1
             LIMIT 1) AS PACIENT_INV,
            IF(MseAction.id IS NOT NULL, 1, '') AS PACIENT_MSE,
            0 AS PACIENT_NOVOR,
            IF(DATEDIFF(Event.execDate,Client.birthDate) < 1 AND Client.birthWeight != 0,
                Client.birthWeight, '') AS PACIENT_VNOV_D,

            getLastEventId(Account_Item.event_id) AS Z_SL_IDCASE,
            rbEventTypePurpose.regionalCode AS Z_SL_USL_OK,
            (SELECT SI.value
             FROM rbSpeciality_Identification SI
             WHERE SI.master_id = Person.speciality_id
               AND SI.deleted = 0
               AND SI.system_id = IF(rbMedicalAidType.code IN (6, 9),
                  '{sysIdTfoms51VIDPOM}', '{sysIdTfoms51VIDPOM2}')
             LIMIT 0,1) AS Z_SL_VIDPOM,
            0 AS Z_SL_FOR_POM,
            IF(rbMedicalAidType.code IN (1,2,3,7) AND Event.order IN (1,5)
                    AND rbEventTypePurpose.regionalCode IN (1, 2),
                (SELECT OI.value FROM Organisation_Identification OI
                 WHERE OI.master_id = IFNULL(Relegate.id,'{currentOrgId}')
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms51F003}'
                   LIMIT 1), '') AS Z_SL_NPR_MO,
            IF(rbMedicalAidType.code IN (1,2,3,7) AND Event.order IN (1,5)
                    AND rbEventTypePurpose.regionalCode IN (1, 2),
                IFNULL(Event.srcDate, Event.setDate), '') AS Z_SL_NPR_DATE,
            '{lpuCode}' AS Z_SL_LPU,
            IFNULL(NextEvent.setDate, Event.setDate) AS Z_SL_DATE_Z_1,
            IFNULL(LastEvent.execDate, Event.execDate) AS Z_SL_DATE_Z_2,
            '' AS Z_SL_KD_Z,
            EventResult.regionalCode AS Z_SL_RSLT,
            rbDiagnosticResult.regionalCode AS Z_SL_ISHOD,
            IF(Client.patrName = '', 2, '') AS Z_SL_OS_SLUCH,
            IF(NextEvent.id IS NOT NULL, 1, '') AS Z_SL_VB_P,

            IF('{financeType}' != 2 AND rbMedicalAidType.code = 2, (
            SELECT value FROM rbMedicalAidUnit_Identification MAI
            WHERE master_id = Account_Item.unit_id
              AND deleted = 0
              AND system_id = IF((
                SELECT id FROM ClientAttach CA
                WHERE CA.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
                AND Event.execDate BETWEEN CA.begDate AND CA.endDate) IS NOT NULL,
              '{sysIdIdsp}', '{sysIdIdspMo}') LIMIT 1),
            IFNULL((SELECT value FROM rbMedicalAidUnit_Identification MAI
              WHERE master_id = Account_Item.unit_id
                AND deleted = 0
                AND system_id = '{sysIdIdsp}'
              LIMIT 1),
            rbMedicalAidUnit.regionalCode)) AS Z_SL_IDSP,
            Account_Item.`sum` AS Z_SL_SUMV,

            Account_Item.event_id AS SL_SL_ID,
            (SELECT OI.value FROM OrgStructure_Identification OI
             WHERE OI.master_id = Person.orgStructure_id
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms51F003Dep}'
               LIMIT 1) AS SL_LPU_1,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                IFNULL(LeavedOrgStruct.infisDepTypeCode,(
                    SELECT OS.infisDepTypeCode FROM Action A
                    INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                    INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                    INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
                    INNER JOIN ActionProperty_OrgStructure AS APO ON APO.id = AP.id
                    INNER JOIN OrgStructure AS OS ON OS.id = APO.value
                    WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                        AND AP.deleted = 0
                        AND AT.`flatCode` = 'moving'
                        AND APT.shortName = 'currentDep'
                    ORDER BY A.begDate DESC LIMIT 0, 1)),
                IF(PersonOrgStructure.infisDepTypeCode IS NULL OR PersonOrgStructure.infisDepTypeCode = '',
                    (SELECT infisDepTypeCode FROM OrgStructure OS
                        WHERE OS.id = (
                            SELECT Account.orgStructure_id FROM Account
                            WHERE Account.id = Account_Item.master_id)
                        LIMIT 1),
                   PersonOrgStructure.infisDepTypeCode)) AS SL_PODR,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                (SELECT APS.regionalCode
                FROM Action A
                INNER JOIN ActionType AS `AT` ON AT.id = A.actionType_id
                INNER JOIN Person AS AP ON A.person_id = AP.id
                INNER JOIN rbSpeciality AS APS ON AP.speciality_id = APS.id
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = IF(EventResult.code = 104, 'moving', 'leaved')
                ORDER BY A.begDate DESC
                LIMIT 1),
                rbSpeciality.regionalCode) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS SL_DET,
            CASE WHEN rbMedicalAidType.code = 9
                THEN IFNULL(EventType_Identification.value, EventType.regionalCode)
                WHEN rbMedicalAidType.code IN (1,2,3,7)
                THEN ''
                ELSE IFNULL(EventType_Identification.value, rbService.note)
            END AS SL_P_CEL,
            CASE wHEN rbMedicalAidType.code IN (1,2,3,7)
                 THEN IF(Event.externalId IS NULL
                         OR Event.externalId = '', Event.id, Event.externalId)
                 WHEN rbMedicalAidType.code = 4
                 THEN EmergencyCall.numberCardCall
                 ELSE Event.id
            END AS SL_NHISTORY,
            IF(EventType.form = '110', Event.execDate, Event.setDate) AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            DS0.MKB AS SL_DS0,
            Diagnosis.MKB AS SL_DS1,
            DS9.MKB AS SL_DS2,
            DS3.MKB AS SL_DS3,
            (SELECT DI.value FROM rbDiseaseCharacter_Identification DI
             WHERE DI.system_id = {sysIdTfoms51V027}
               AND DI.deleted = 0
               AND DI.master_id = Diagnostic.character_id
             LIMIT 1) AS SL_C_ZAB,
            CASE
                WHEN rbDispanser.id IS NULL
                  OR rbDispanser.name LIKE '%%нуждается%%' THEN ''
                WHEN rbDispanser.observed = 1
                 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                WHEN rbDispanser.observed = 1
                 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                WHEN rbDispanser.observed = 0
                 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                WHEN rbDispanser.observed = 0
                 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                ELSE ''
            END AS SL_DN,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                mes.MES_ksg.code,'') AS SL_CODE_MES1,
            (SELECT ETI.value FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdReab}'
               LIMIT 1) AS SL_REAB,
            IFNULL((SELECT value FROM rbSpeciality_Identification SI
                WHERE SI.master_id = rbSpeciality.id
                 AND SI.deleted = 0
                 AND SI.system_id = {sysIdTfoms51V021}
                LIMIT 1), rbSpeciality.federalCode) AS SL_PRVS,
            'V021' AS SL_VERS_SPEC,
            Person.regionalCode AS SL_IDDOKT,
            IF(rbMedicalAidType.code IN (1,2,3),
               DATEDIFF(Event.execDate, Event.setDate),
               IF(rbMedicalAidType.code = 7,
                  DATEDIFF(Event.execDate, Event.setDate) + 1, '')) AS SL_KD,
            Account_Item.price AS SL_TARIF,

            mes.MES_ksg.code AS KSG_KPG_N_KSG,
            0 AS KSG_KPG_KSG_PG,
            mes.MES_ksg.vk AS KSG_KPG_KOEF_Z,
            IFNULL(mes.MES_ksg.managementFactor, 1) AS KSG_KPG_KOEF_UP,
            IF(mes.MES_ksg.vk IS NOT NULL,
                Account_Item.price/mes.MES_ksg.vk/IFNULL(mes.MES_ksg.managementFactor, 1), 0) AS KSG_KPG_KOEF_U,
            (SELECT GROUP_CONCAT(AT.code)
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.flatCode = 'AddCriterion'
                WHERE A.event_id = Event.id AND A.deleted = 0
            )  AS critList,
            0 AS KSG_KPG_SL_K,
            1 AS KSG_KPG_KOEF_D,

            '{lpuCode}' AS USL_LPU,
            IFNULL(LeavedOrgStruct.infisDepTypeCode,
                IFNULL(EventType_Identification.value, PersonOrgStructure.infisDepTypeCode)) AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.regionalCode,
                    ServiceMedicalAidProfile.regionalCode) AS USL_PROFIL,
            IF(rbMedicalAidType.code IN (6,9),
               (SELECT SI.value FROM rbService_Identification SI
                WHERE SI.master_id = rbService.id
                AND SI.deleted = 0
                AND SI.system_id = '{sysIdTfoms51V001}'
                LIMIT 1)
                ,'') AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                Event.setDate, IFNULL(Visit.date, Action.begDate)) AS USL_DATE_IN,
            (CASE
                WHEN rbMedicalAidType.code IN (1,2,3,7) THEN Event.execDate
                WHEN rbMedicalAidType.code = 9 THEN Action.endDate
                ELSE IFNULL(Visit.date, Action.endDate)
            END) AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            IF(rbEventProfile.regionalCode IN (1,3),
                mes.MES_ksg.code,
                IF(Account_Item.visit_id IS NOT NULL,
                    VisitService.infis, rbService.infis)) AS USL_CODE_USL,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                Account_Item.amount) AS USL_KOL_USL,
            Account_Item.price AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            IFNULL((SELECT RSI.value FROM rbSpeciality_Identification RSI
             WHERE RSI.master_id = IFNULL((
                SELECT speciality_id FROM Person
                WHERE id = Action.person_id), Person.speciality_id)
               AND RSI.deleted = 0
               AND RSI.deleted = 0
               AND RSI.system_id = {sysIdTfoms51F002}
             LIMIT 1), IFNULL((
                    SELECT RS.federalCode FROM rbSpeciality RS
                    WHERE RS.id = IFNULL(
                        (SELECT speciality_id FROM Person P
                            WHERE P.id = Action.person_id),
                        VisitPerson.speciality_id)),
                rbSpeciality.federalCode)) AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            IFNULL(VisitPerson.SNILS,
                Person.SNILS) AS MR_USL_N_CODE_MD,
            '1' AS MR_USL_N_MR_N,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.lastName) AS PERS_FAM,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            IF(rbPolicyKind.regionalCode != 3, rbDocumentType.regionalCode,'') AS PERS_DOCTYPE,
            IF(rbPolicyKind.regionalCode != 3,
               IF(rbDocumentType.code = '003' OR rbDocumentType.regionalCode = '3',
                  REPLACE(TRIM(ClientDocument.serial),' ', '-'),
                  TRIM(ClientDocument.serial)), '') AS PERS_DOCSER,
            IF(rbPolicyKind.regionalCode != 3,
               TRIM(ClientDocument.number), '') AS PERS_DOCNUM,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,
            IF(rbPolicyKind.regionalCode != 3,
               ClientDocument.date,'') AS PERS_DOCDATE,
            IF(rbPolicyKind.regionalCode != 3,
               ClientDocument.origin, '') AS PERS_DOCORG,
            Client.SNILS AS PERS_SNILS,

            Event.id AS SLUCH_SL_ID,
            PersonOrgStructure.tfomsCode AS SLUCH_TOWN_HOSP,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               mes.MES_ksg.code,'') AS SLUCH_KSG,
            rbMesSpecification.level AS mesSpecificationLevel,
            Person.SNILS AS SLUCH_SNILS_DOC,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = Person.orgStructure_id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
             LIMIT 1) AS SLUCH_ADDR_CODE,
            EventResult.regionalCode AS SLUCH_RSLT,
            rbDiagnosticResult.regionalCode AS SLUCH_ISHOD,
            IF((SELECT code FROM rbDiseasePhases
                WHERE Diagnostic.phase_id = rbDiseasePhases.id
                LIMIT 1) = 10, Diagnosis.MKB, '') AS SLUCH_DS_PZ,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = IF(rbMedicalAidType.code IN (1,2,3,7),
                (SELECT OS.id
                 FROM Action A
                 INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                 INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                 INNER JOIN Person AP ON A.person_id = AP.id
                 INNER JOIN OrgStructure AS OS ON OS.id = AP.orgStructure_id
                 WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = IF(EventResult.code = 104, 'moving', 'leaved')
                 ORDER BY A.begDate DESC
                 LIMIT 0, 1), VisitPerson.orgStructure_id)
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
             LIMIT 1) AS USL_ADDR_CODE,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               rbMedicalAidUnit.federalCode,'') AS SUM_PAY_MODE,
            IF(rbMedicalAidType.code IN (1,2,3,7), rbSpeciality.federalCode, '') AS DEP_ADD_PROFIL,
            IF(rbMedicalAidType.code IN (1,2,3,7), Diagnosis.MKB, '') AS DEP_ADD_DS1,
            IF(rbMedicalAidType.code IN (1,2,3,7), Person.SNILS,'') AS DEP_ADD_IDDOKT,
            rbMedicalAidUnit.federalCode AS USL_PAY_MODE,
            IFNULL(Event.srcDate, Event.setDate) AS USL_NPR_DATE,
            IFNULL(VisitPerson.SNILS, Person.SNILS) AS USL_SNILS_DOC,
            Action.begDate,
            (CASE WHEN rbMedicalAidType.code IN (1,2,3,7,9,4,5)
                THEN (SELECT infisCode FROM OrgStructure OS
                      WHERE OS.id = IF(rbMedicalAidType.code IN (1,2,3,7),
                      '{accOrgStructureId}', Person.orgStructure_id)
                      LIMIT 1)
            WHEN rbMedicalAidType.code = 6 -- АПП
                THEN (SELECT value FROM rbService_Identification SI
                      WHERE SI.master_id = rbService.id
                        AND SI.deleted = 0
                        AND ((Event.execDate <= '2020-12-31' AND SI.checkDate <= '2020-12-31')
                             OR (Event.execDate >= '2021-01-01' AND SI.checkDate >= '2021-01-01'))
                        AND SI.system_id = '{sysIdTfoms51SubHosp}'
                      LIMIT 1)
            END) AS SLUCH_SUB_HOSP,
            (CASE
              WHEN rbMedicalAidType.code = 6 -- АПП
                THEN (SELECT value FROM rbService_Identification SI
                      WHERE SI.master_id = rbService.id
                        AND SI.deleted = 0
                        AND ((Event.execDate <= '2020-12-31' AND SI.checkDate <= '2020-12-31')
                             OR (Event.execDate >= '2021-01-01' AND SI.checkDate >= '2021-01-01'))
                        AND SI.system_id = '{sysIdTfoms51SubHosp}'
                      LIMIT 1)
              WHEN rbMedicalAidType.code IN (4,5,9) -- СМП, Стоматология
                THEN (SELECT infisCode FROM OrgStructure OS
                      WHERE OS.id = '{accOrgStructureId}' LIMIT 1)
              WHEN rbMedicalAidType.code IN (1,2,3,7) -- Стационар
                THEN (SELECT infisCode FROM OrgStructure OS
                      WHERE OS.id = Person.orgStructure_id LIMIT 1)
              ELSE NULL
            END) AS USL_SUB_HOSP,
            (SELECT IF(rbDiseaseCharacter.code IN (1, 2), 1, '')
             FROM rbDiseaseCharacter
             WHERE Diagnostic.character_id = rbDiseaseCharacter.id
            ) AS SLUCH_DS1_PR,
            (SELECT serviceType FROM ActionType AT
              WHERE AT.id = Action.actionType_id) AS serviceType,
            IF(rbMedicalAidType.code = 6,
             IF((Action.status IS NOT NULL AND Action.status != 2)
                OR rbDiagnosticResult.regionalCode = '502', 1, 0),
             '') AS USL_P_OTK
            """.format(**queryParams)
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
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
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
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbEventProfile ON rbEventProfile.id = EventType.eventProfile_id
            LEFT JOIN (
                    SELECT A.event_id, SUM(A.amount) AS amount, COUNT(DISTINCT A.id) AS cnt, MAX(A.id) AS id
                    FROM Action A
                    WHERE A.deleted = 0 AND
                              A.actionType_id IN (
                                    SELECT MAX(AT.id)
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='moving')
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
            LEFT JOIN EventType_Identification ON EventType_Identification.id = (
                SELECT EI.id FROM EventType_Identification EI
                WHERE EI.master_id = EventType.id
                  AND EI.deleted = 0
                  AND EI.system_id = '{sysIdEmergency}'
                LIMIT 0, 1)
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
            LEFT JOIN OrgStructure_Identification ON OrgStructure_Identification.id = (
                SELECT id FROM OrgStructure_Identification OSI
                WHERE OSI.master_id = IFNULL(LeavedOrgStruct.id, PersonOrgStructure.id)
                  AND OSI.deleted = 0
                  AND OSI.system_id = '{sysIdMedicalAidType}'
                LIMIT 0, 1)
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
            LEFT JOIN rbService AS AnotherMesService ON AnotherMesService.id = (
                SELECT S.id
                FROM rbService S
                WHERE mes.MES.code = S.code AND mes.MES.deleted = 0
                LIMIT 0, 1
            )
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN Action AS MseAction ON MseAction.id = (
                SELECT MAX(A.id)
                FROM Action A
                WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id = (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='inspection_mse'
                                LIMIT 0, 1
                          )
            )
            LEFT JOIN Event AS NextEvent ON NextEvent.id = (
                SELECT MAX(id) FROM Event E
                WHERE E.deleted = 0 AND E.prevEvent_id = Event.id)
            LEFT JOIN Event AS LastEvent ON LastEvent.id = getLastEventId(Event.id)
            LEFT JOIN Organisation AS Relegate ON Relegate.id = Event.relegateOrg_id
            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Account_Item.event_id
            LEFT JOIN rbService_Identification ON rbService_Identification.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                AND SId.system_id = {sysIdTomsPcel}
                AND SId.deleted = 0)""".format(**queryParams)
        where = u"""Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s""" % self.tableAccountItem['id'].inlist(self.idList)
        orderBy = u'Client.id, LastEvent.id, Event.id, Account_Item.id'

        return (select, tables, where, orderBy)


    def _getBedDaysByCompleteEvent(self):
        u"""Возвращает кол-во койкодней за законченный случай"""

        stmt = """SELECT getLastEventId(Account_Item.event_id) AS lastEventId,
            SUM(IF(rbMedicalAidType.code IN (1,2,3),
               DATEDIFF(Event.execDate, Event.setDate),
               IF(rbMedicalAidType.code = 7,
                  DATEDIFF(Event.execDate, Event.setDate) + 1, 0))) AS val
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY lastEventId;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            yield eventId, forceDouble(record.value(1))


    def _getVisitCount(self):
        stmt = """SELECT Account_Item.event_id, COUNT(DISTINCT Account_Item.id) AS amount
                FROM Account_Item
                LEFT JOIN rbPayRefuseType ON
                    rbPayRefuseType.id = Account_Item.refuseType_id
                WHERE Account_Item.reexposeItem_id IS NULL
                  AND (Account_Item.date IS NULL
                       OR (Account_Item.date IS NOT NULL
                           AND rbPayRefuseType.rerun != 0))
                  AND {0}
                GROUP BY Account_Item.event_id""".format(
                    self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            visitCount = forceInt(record.value(1))
            yield eventId, visitCount


    def _getOnkologyInfo(self, params):
        u"""Возвращает словарь с записями по онкологии и направлениям,
            ключ - идентификатор события"""

        stmt = """SELECT Event.id AS eventId,
            Event.setDate AS NAPR_NAPR_DATE,
            '{lpuCode}' AS NAPR_NAPR_MO,
            4 AS NAPR_NAPR_V,
            0 AS CONS_PR_CONS,
            6 AS ONK_SL_DS1_T,
            rbTNMphase_Identification.value AS ONK_SL_STAD,
            rbTumor_Identification.value AS ONK_SL_ONK_T,
            rbNodus_Identification.value AS ONK_SL_ONK_N,
            rbMetastasis_Identification.value AS ONK_SL_ONK_M,
            Sod.value AS ONK_SL_SOD,
            IF(GistologiaAction.id IS NOT NULL, 1,
                IF(ImmunohistochemistryAction.id IS NOT NULL, 2,
                    '')) AS B_DIAG_DIAG_TIP,
            GistologiaAction.id AS gistologiaActionId,
            ImmunohistochemistryAction.id AS immunohistochemistryActionId,
            ControlListOnkoAction.id AS controlListOnkoActionId,
            rbDiseasePhases.code AS diseasePhaseCode,
            DirectionAction.id AS directionActionId,
            Diagnosis.MKB,
            AccDiagnosis.MKB AS accMKB
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Diagnostic ON (Diagnostic.event_id = Account_Item.event_id
            AND Diagnostic.diagnosisType_id IN (
                SELECT id
                FROM rbDiagnosisType
                WHERE code IN ('1', '2'))
            AND Diagnostic.person_id = Event.execPerson_id
            AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = (
              SELECT MAX(ds.id)
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('9', '10', '11'))
                AND dc.event_id = Account_Item.event_id
        )
        LEFT JOIN rbDiseasePhases ON Diagnostic.phase_id = rbDiseasePhases.id
        LEFT JOIN rbTNMphase_Identification ON
            rbTNMphase_Identification.master_id = IFNULL(
                Diagnostic.cTNMphase_id, Diagnostic.pTNMphase_id)
            AND rbTNMphase_Identification.deleted = 0
            AND rbTNMphase_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'tfoms51.N002'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                Diagnostic.cTumor_id, Diagnostic.pTumor_id)
            AND rbTumor_Identification.deleted = 0
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'tfoms51.N003'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                Diagnostic.cNodus_id, Diagnostic.pNodus_id)
            AND rbNodus_Identification.deleted = 0
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'tfoms51.N004'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                Diagnostic.cMetastasis_id,Diagnostic.pMetastasis_id)
            AND rbMetastasis_Identification.deleted = 0
            AND rbMetastasis_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'tfoms51.N005'
            )
        LEFT JOIN ActionProperty_String AS Sod ON Sod.id = (
            SELECT APS.id
            FROM Action A
            INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
            INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
            INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
            INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
            WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                AND AP.deleted = 0
                AND AT.`flatCode` = 'ControlListOnko'
                AND APT.`shortName` = 'SOD'
            ORDER BY A.begDate DESC
            LIMIT 0, 1
        )
        LEFT JOIN Action AS GistologiaAction ON GistologiaAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            LEFT JOIN Event E ON E.id = A.event_id
            WHERE E.client_id = Event.client_id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='Gistologia'
              )
        )
        LEFT JOIN Action AS ImmunohistochemistryAction ON ImmunohistochemistryAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            LEFT JOIN Event E ON E.id = A.event_id
            WHERE E.client_id = Event.client_id
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
            LEFT JOIN Event E ON E.id = A.event_id
            WHERE E.client_id = Event.client_id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='ControlListOnko'
              )
        )
        LEFT JOIN Action AS DirectionAction ON DirectionAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            LEFT JOIN Event E ON E.id = A.event_id
            WHERE E.client_id = Event.client_id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode IN ('inspectionDirection',
                    'ConsultationDirection', 'hospitalDirection',
                    'recoveryDirection')
              )
        )
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
          AND (LEFT(Diagnosis.MKB, 1) = 'C'
               OR (LEFT(Diagnosis.MKB, 3) BETWEEN 'D00' AND 'D09')
               OR (LEFT(Diagnosis.MKB, 3) BETWEEN 'D45' AND 'D47')
               OR Diagnosis.MKB = 'Z03.1'
               OR (LEFT(AccDiagnosis.MKB, 3) = 'D70'
                   AND (LEFT(AccDiagnosis.MKB, 3) = 'C97'
                        OR (LEFT(AccDiagnosis.MKB, 3) BETWEEN 'C00' AND 'C80'))))
          """ .format(idList=self.tableAccountItem['id'].inlist(self.idList),
                      lpuCode=params['lpuCode'])
        query = self.db.query(stmt)

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            yield eventId, self._updateOnkologyInfo(record2Dict(record))


    def _updateOnkologyInfo(self, record):
        u"""Дополняет информацию по онкологии, которую не вытащить через SQL"""
        row = {}

        accMKB = forceString(record['accMKB'])
        mkb = forceString(record['MKB'])
        phaseCode = forceInt(record[
            'diseasePhaseCode']) if record['diseasePhaseCode'] else 0

        row['SL_DS_ONK'] = 1 if (phaseCode == 10 and (mkb[:1] == 'C' or (
            'D00' <= mkb[:3] <= 'D09') or ('D45' <= mkb[:3] <= 'D47')
            or mkb == 'Z03.1' or (
                mkb[:3] == 'D70' and (
                    ('C00' <= accMKB[:3] <= 'C80') or
                    accMKB[:3] == 'C97')))) else 0

        if row['SL_DS_ONK'] != 1:
            for field in ('NAPR_DATE', 'NAPR_MO', 'NAPR_V'):
                row[field] = ''

        row['ONK_USL_USL_TIP'] = 6
        row.update(record)
        return row


    def _getRegistryInfo(self):
        sysIdTfoms51Purpose = self._getAccSysId('tfoms51.PURPOSE')
        stmt = u"""SELECT Event.id AS eventId,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               IFNULL(Relegate.smoCode, AttachOrg.smoCode),
               '') AS SLUCH_DIR_SUBLPU,
            IFNULL((SELECT RSI.value FROM rbSpeciality_Identification RSI
             WHERE RSI.master_id = RelegatePerson.speciality_id AND RSI.deleted = 0
               AND RSI.system_id = {sysIdTfoms51DirSublpu}
             LIMIT 1), AttachOrg.smoCode) AS USL_DIR_SUBLPU,
            IFNULL((SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = AttachOrg.id
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms51F003}'
               LIMIT 1),
            AttachOrg.infisCode) AS SLUCH_MASTER,
            IFNULL(Relegate.tfomsExtCode, AttachOrg.tfomsExtCode) AS SLUCH_DIR_TOWN,
            EmergencyKLADR.infis AS emergencyTownInfis,
            TIME_FORMAT(EmergencyCall.arrivalDate, '%H:%i') AS SLUCH_SERV_TIME,
            CASE
                WHEN rbMedicalAidType.code = 6 THEN -- Амбулатория
                    IFNULL((SELECT `value` FROM rbService_Identification SI
                     WHERE SI.master_id = rbService.id
                       AND SI.deleted = 0
                       AND ((IFNULL(Visit.date, Action.endDate) <= '2020-12-31'
                             AND SI.checkDate <= '2020-12-31')
                            OR (IFNULL(Visit.date, Action.endDate) >= '2021-01-01'
                                AND SI.checkDate >= '2021-01-01')
                            OR SI.checkDate IS NULL)
                       AND SI.system_id = '{tfoms51Purpose}'
                     LIMIT 1), rbService.note)
                WHEN rbMedicalAidType.code = 9 THEN -- Стоматология
                    IFNULL((SELECT `value` FROM EventType_Identification ETI
                            WHERE ETI.master_id = EventType.id
                              AND ETI.checkDate <= Event.execDate
                              AND ETI.deleted = 0
                              AND ETI.system_id = '{tfoms51Purpose}'
                            LIMIT 1), EventType.regionalCode)
                ELSE ''
            END AS SLUCH_PURPOSE,
            IFNULL((SELECT `value` FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND ETI.checkDate <= Event.execDate
               AND ETI.deleted = 0
               AND ETI.system_id = '{tfoms51Purpose}'
             LIMIT 1), rbService.note) as USL_PURPOSE,
            IF(rbEmergencyPlaceCall.code = '6', (
                SELECT infisCode
                FROM Organisation O WHERE O.id = EmergencyCall.org_id
            ), '') AS SLUCH_LPU_PEREV,
            IF(rbEmergencyPlaceCall.code = '6', (
                SELECT tfomsExtCode
                FROM Organisation O WHERE O.id = EmergencyCall.org_id
            ), '') AS SLUCH_SUB_PEREV,
            ClientAttach.begDate AS clientAttachBegDate,
            IF(rbScene.code IN (2,3), 1, '') AS USL_PR_VISIT,
            rbService_Identification.value AS USL_SERV_METOD,
            AttachOrg.infisCode AS attachOrgCode,
            AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
            (SELECT RSI.value FROM rbSpeciality_Identification RSI
             WHERE RSI.master_id = RelegatePerson.speciality_id AND RSI.deleted = 0
               AND RSI.system_id = {sysIdTfoms51DirSpec}
             LIMIT 1) AS relegatePersonSpecialityCode,
            rbEmergencyResult.code AS emergencyResultCode,
            Action.org_id AS actionOrgId,
            rbVisitType.code AS visitTypeCode,
            (SELECT value FROM rbVisitType_Identification VTI
             WHERE VTI.master_id = Visit.visitType_id
               AND VTI.deleted = 0
               AND VTI.system_id = '{tmofs51pr_os}') AS SLUCH_PR_OS
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Visit ON Visit.id = Account_Item.visit_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN rbService ON Account_Item.service_id = rbService.id
        LEFT JOIN ClientAttach ON
            ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
        LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
        LEFT JOIN OrgStructure AS AttachOrgStruct ON AttachOrgStruct.id = ClientAttach.orgStructure_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN Organisation AS Relegate ON Relegate.id = Event.relegateOrg_id
        LEFT JOIN Person AS RelegatePerson ON RelegatePerson.id = Event.relegatePerson_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Account_Item.event_id
        LEFT JOIN Address AS EmergencyAddress ON EmergencyAddress.id = EmergencyCall.address_id
        LEFT JOIN rbEmergencyPlaceCall ON rbEmergencyPlaceCall.id = EmergencyCall.placeCall_id
        LEFT JOIN rbEmergencyResult ON rbEmergencyResult.id = EmergencyCall.resultCall_id
        LEFT JOIN AddressHouse AS EmergencyAddressHouse ON EmergencyAddressHouse.id = EmergencyAddress.house_id
        LEFT JOIN kladr.KLADR AS EmergencyKLADR ON EmergencyKLADR.CODE = EmergencyAddressHouse.KLADRCode
        LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
        LEFT JOIN rbService_Identification ON rbService_Identification.id = (
            SELECT MAX(SId.id)
            FROM rbService_Identification SId
            WHERE SId.master_id = rbService.id
            AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
            AND SId.deleted = 0
        )
        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL
                     AND rbPayRefuseType.rerun != 0))
            AND {0}
        ORDER BY Account_Item.event_id, Account_Item.action_id, Account_Item.id""".format(
            self.tableAccountItem['id'].inlist(self.idList),
            tfoms51Purpose=sysIdTfoms51Purpose,
            sysIdTfoms51F003=self._getAccSysIdByUrn(
                u'urn:tfoms51:F003'),
            sysIdTfoms51DirSpec=self._getAccSysIdByUrn(
                u'urn:tfoms51:dir_spec'),
            sysIdTfoms51DirSublpu=self._getAccSysIdByUrn(
                u'urn:tfoms51:dir_sublpu'),
            tmofs51pr_os=self._getAccSysIdByUrn('urn:tfoms51:pr_os'))
        query = self.db.query(stmt)
        prevEventId = None
        eventId = None
        val = []
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            if not prevEventId:
                prevEventId = eventId
            if prevEventId and prevEventId != eventId:
                yield prevEventId, val
                prevEventId = eventId
                val = []
            val.append(record2Dict(record))

        yield eventId, val

    def _operation(self, params):
        local_params = {
            'lpuCode': params['lpuCode'],
            'sysIdTfoms51F002': self._getAccSysIdByUrn('urn:tfoms51:F002'),
            'sysIdTfoms51V001': self._getAccSysIdByUrn('urn:tfoms51:V001'),
            'sysIdEmergency': self._getAccSysId(u'НеотлПом'),
        }
        stmt = u"""SELECT Event.id AS eventId,
            '{lpuCode}' AS USL_LPU,
            IFNULL(LeavedOrgStruct.infisDepTypeCode,
                IFNULL(EventType_Identification.value, PersonOrgStructure.infisDepTypeCode)) AS USL_PODR,
            IFNULL(IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.regionalCode,
                    ServiceMedicalAidProfile.regionalCode),
                    PersonOrgStructure.infisInternalCode) AS USL_PROFIL,
            (SELECT SI.value FROM rbService_Identification SI
             WHERE SI.master_id = rbService.id
              AND SI.deleted = 0
              AND SI.system_id = '{sysIdTfoms51V001}') AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            Event.setDate AS USL_DATE_IN,
            Event.execDate AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            rbService.infis AS USL_CODE_USL,
            Action.amount AS USL_KOL_USL,
            0 AS USL_TARIF,
            0 AS USL_SUMV_USL,
            IFNULL((SELECT RSI.value FROM rbSpeciality_Identification RSI
             WHERE RSI.master_id = Person.speciality_id AND RSI.deleted = 0
               AND RSI.system_id = {sysIdTfoms51F002}
             LIMIT 1), rbSpeciality.federalCode) AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.SNILS AS MR_USL_N_CODE_MD,
            '1' AS MR_USL_N_MR_N,
            '' AS USL_NPL -- FIXME: implement
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN Action ON Action.event_id = Event.id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN Person ON Person.id = Action.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
        LEFT JOIN OrgStructure AS PersonOrgStructure ON
            PersonOrgStructure.id = Person.orgStructure_id
        LEFT JOIN rbResult AS EventResult ON EventResult.id = Event.result_id
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
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (
            SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id
              AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON
            ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
            ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN rbPayRefuseType
            ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Diagnosis ON Diagnosis.id = (
              SELECT MAX(ds.id)
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (
                    ds.id = dc.diagnosis_id AND ds.deleted = 0
                    AND dc.deleted = 0)
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType
                    WHERE code IN ('1', '2'))
                AND dc.event_id = Account_Item.event_id
        )
        LEFT JOIN EventType_Identification ON EventType_Identification.id = (
            SELECT EI.id FROM EventType_Identification EI
            WHERE EI.master_id = Event.eventType_id
              AND EI.deleted = 0
              AND EI.system_id = '{sysIdEmergency}'
            LIMIT 0, 1)
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.serviceType = 4
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL
                AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id
        ORDER BY Account_Item.event_id, Account_Item.action_id
            """.format(idList=self.tableAccountItem['id'].inlist(self.idList),
                       **local_params)

        query = self.db.query(stmt)
        prevEventId = None
        eventId = None
        val = []
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            if not prevEventId:
                prevEventId = eventId
            if prevEventId and prevEventId != eventId:
                yield prevEventId, val
                prevEventId = eventId
                val = []
            val.append(record)

        yield eventId, val


    def getUetSum(self):
        u"""Возвращает генератор из номера события и количество УЕТ в событии"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.`uet`) AS totalUet
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

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            yield eventId, forceDouble(record.value(1))


    def __observationActions(self, params):
        local_params = {
            'lpuCode': params['lpuCode'],
            'sysIdTfoms51F002': self._getAccSysIdByUrn('urn:tfoms51:F002'),
            'sysIdTfoms51V001': self._getAccSysIdByUrn('urn:tfoms51:V001'),
            'sysIdEmergency': self._getAccSysId(u'НеотлПом'),
        }
        stmt = u"""SELECT Event.id AS eventId,
            '{lpuCode}' AS USL_LPU,
            IFNULL(LeavedOrgStruct.infisDepTypeCode,
                IFNULL(EventType_Identification.value, PersonOrgStructure.infisDepTypeCode)) AS USL_PODR,
            IFNULL(IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.regionalCode,
                    ServiceMedicalAidProfile.regionalCode),
                    PersonOrgStructure.infisInternalCode) AS USL_PROFIL,
            (SELECT SI.value FROM rbService_Identification SI
             WHERE SI.master_id = rbService.id
              AND SI.deleted = 0
              AND SI.system_id = '{sysIdTfoms51V001}') AS USL_VID_VME,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            Event.setDate AS USL_DATE_IN,
            Event.execDate AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            rbService.infis AS USL_CODE_USL,
            Action.amount AS USL_KOL_USL,
            0 AS USL_TARIF,
            0 AS USL_SUMV_USL,
            IFNULL((SELECT RSI.value FROM rbSpeciality_Identification RSI
             WHERE RSI.master_id = Person.speciality_id AND RSI.deleted = 0
               AND RSI.system_id = {sysIdTfoms51F002}
             LIMIT 1), rbSpeciality.federalCode) AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.SNILS AS MR_USL_N_CODE_MD,
            '1' AS MR_USL_N_MR_N,
            '' AS USL_NPL -- FIXME: implement
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN Action ON Action.event_id = Event.id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        INNER JOIN ActionType_Service ON ActionType.id = ActionType_Service.master_id
        LEFT JOIN Person ON Person.id = Action.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
        LEFT JOIN OrgStructure AS PersonOrgStructure ON
            PersonOrgStructure.id = Person.orgStructure_id
        LEFT JOIN rbResult AS EventResult ON EventResult.id = Event.result_id
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
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (
            SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id
              AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON
            ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
            ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN rbPayRefuseType
            ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Diagnosis ON Diagnosis.id = (
              SELECT MAX(ds.id)
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (
                    ds.id = dc.diagnosis_id AND ds.deleted = 0
                    AND dc.deleted = 0)
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType
                    WHERE code IN ('1', '2'))
                AND dc.event_id = Account_Item.event_id
        )
        LEFT JOIN EventType_Identification ON EventType_Identification.id = (
            SELECT EI.id FROM EventType_Identification EI
            WHERE EI.master_id = Event.eventType_id
              AND EI.deleted = 0
              AND EI.system_id = '{sysIdEmergency}'
            LIMIT 0, 1)
        WHERE Account_Item.reexposeItem_id IS NULL
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL
                AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id
        ORDER BY Account_Item.event_id, Account_Item.action_id
            """.format(idList=self.tableAccountItem['id'].inlist(self.idList),
                       **local_params)

        query = self.db.query(stmt)
        prevEventId = None
        eventId = None
        val = []
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            if not prevEventId:
                prevEventId = eventId
            if prevEventId and prevEventId != eventId:
                yield prevEventId, val
                prevEventId = eventId
                val = []
            val.append(record)

        yield eventId, val


    def exportInt(self):
        params = self.processParams()
        self.registryType = self.cmbRegistryType.currentIndex()
        params.update(self.accountInfo())
        params['recNum'] = 1
        params['isReexposed'] = '1' if self.chkReexposed.isChecked() else '0'
        params['completeEventSum'] = self.getCompleteEventSum()
        params['eventSum'] = self.getEventSum()
        params['uetSum'] = dict(self.getUetSum())
        params['contractAttrCS'] = getDoubleContractAttribute(
            self.wizard().accountId, u'КС')
        params['contractAttrDS'] = getDoubleContractAttribute(
            self.wizard().accountId, u'ДС')
        params['contractFinanceType'] = getIntContractAttribute(
            self.wizard().accountId, u'VID_FIN')
        if not params['contractFinanceType']:
            params['contractFinanceType'] = 1
        params['completeEventBedDays'] = dict(self._getBedDaysByCompleteEvent())
        params['visitCount'] = dict(self._getVisitCount())
        params['registryInfo'] = dict(self._getRegistryInfo())
        params['sysIdTfoms51F003'] = self._getAccSysIdByUrn(u'urn:tfoms51:F003')
        sysIdTfoms51F002 = self._getAccSysIdByUrn(u'urn:tfoms51:F002')
        currentOrgId = QtGui.qApp.currentOrgId()
        params['currentOrgId'] = currentOrgId
        params['lpuCode'] = self._getOrgIdentification(
            currentOrgId, params['sysIdTfoms51F003'])
        params['currentOrgInfis'] = forceString(self.db.translate(
                'Organisation', 'id', currentOrgId, 'infisCode'))
        if not params['lpuCode']:
            params['lpuCode'] = params['currentOrgInfis']

        params['payerCode'] = self._getOrgIdentification(
            params['payerId'], sysIdTfoms51F002)
        if not params['payerCode']:
            params['payerCode'] = self._getOrgIdentification(
                params['payerId'], self._getAccSysIdByUrn(
                    u'urn:oid:1.2.643.5.1.13.2.1.1.635'))
        if not params['payerCode']:
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
        params['payerInfisCode'] = self._getOrgIdentification(
            self.accountInfo()['payerId'], sysIdTfoms51F002)
        params['onkologyInfo'] = (
            dict(self._getOnkologyInfo(params))
            if self.registryType == self.REGISTRY_TYPE_B5
            else {})
        params['operation'] = dict(self._operation(params))
        params['observationActions'] = dict(self.__observationActions(params))
        params['personalDataFileName'] = (
            self.wizard().getPersonalDataXmlFileName(False))
        params['fileName'] = self.wizard().getXmlFileName()
        record = self.db.getRecord('OrgStructure',
            'infisCode, tfomsCode', params['accOrgStructureId'])
        if record:
            params['accOrgStructInfisCode'] = forceString(
                record.value('infisCode'))
            params['accOrgStructTfomsCode'] = forceString(
                record.value('tfomsCode'))

        tableActionType = self.db.table('ActionType')
        params['actionTypeIllegalActions'] = forceRef(self.db.translate(
            tableActionType, 'flatCode', 'IllegalActions', 'id'))
        params['actionTypeArrival'] = forceRef(self.db.translate(
            tableActionType, 'flatCode', 'received', 'id'))
        params['sysIdTfoms51F003Dep'] = self._getAccSysIdByUrn(
            'urn:tfoms51:F003_DEP')
        params['sysIdAddrCode'] = self._getAccSysId('addr_code')
        self.setProcessParams(params)

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        regFile = QFile(self._parent.getRegistryFullXmlFileName())
        regFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, regWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        regWriter.setDevice(regFile)
        self.setStatus(u'Запрос данных мед.препаратов...')
        items = self.tableAccountItem['id'].inlist(self.idList)
        medicalSuppliesInfo = CMedicalSuppliesInfo()
        params['medicalSuppliesInfo'] = medicalSuppliesInfo.get(
            self.db, items, self)
        CAbstractExportPage1Xml.exportInt(self)


    def setStatus(self, msg):
        self.log(msg)
        self.progressBar.setText(msg)
        QtGui.qApp.processEvents()


    def getParentCode(self, _id, sysId):
        u"""Возвращает идентификацию подразделения по идентификатору.
              Если таковая отсутствует, ищет в родительском подразделении"""
        if not _id:
            return None

        stmt = """SELECT parent_id,
           (SELECT OI.value FROM OrgStructure_Identification OI
             WHERE OI.master_id = OrgStructure.id
               AND OI.deleted = 0
               AND OI.system_id = '{sysId}'
               LIMIT 1)
        FROM OrgStructure
        WHERE OrgStructure.id='{id}'
        LIMIT 1""".format(id=_id, sysId=sysId)
        query = self.db.query(stmt)

        if query.first():
            record = query.record()
            code = forceString(record.value(0))
            if not code:
                code = self.getLpu1Code(forceRef(record.value(1)))

        return code

# ******************************************************************************

class CExportPage2(COrder79ExportPage2):
    u"""Вторая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, prefix)


    def saveExportResults(self):
        fileList = (self.wizard().getFullXmlFileName(),
                    self.wizard().getRegistryFullXmlFileName(),
                    self.wizard().getPersonalDataFullXmlFileName())
        zipFileName = self.wizard().getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class XmlStreamWriter(COrder79XmlStreamWriter, CExportHelperMixin):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'INV', 'MSE',
                    'NOVOR', 'VNOV_D')
    clientOnkFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO',
                       'SMO', 'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'INV', 'MSE',
                       'NOVOR', 'VNOV_D')

    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2', 'NPR_DATE')
    completeEventFields1 = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO',
                            'NPR_DATE', 'LPU', 'DATE_Z_1', 'DATE_Z_2', 'KD_Z',
                            'VNOV_M', 'RSLT', 'ISHOD', 'OS_SLUCH', 'VB_P')
    completeEventFields2 = ('IDSP', 'SUMV')
    completeEventFields = completeEventFields1 + completeEventFields2

    ksgSubGroup = {
        'SL_KOEF' : {'fields': ('IDSL', 'Z_SL')}
    }
    ksgFields = ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG', 'KOEF_Z', 'KOEF_UP',
                 'BZTSZ', 'KOEF_D', 'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                 'SL_KOEF')

    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields = ('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                   'P_CEL', 'NHISTORY', 'P_PER') +  eventDateFields + (
                       'KD', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK',
                       'DN', 'CODE_MES1',  'NAPR', 'CONS', 'ONK_SL',  'KSG_KPG',
                       'REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                       'SUM_M',  'LEK_PR')
    eventOnkFields = ('SL_ID', 'LPU_1', 'PROFIL', 'PROFIL_K', 'DET',
                   'P_CEL', 'NHISTORY', 'P_PER') +  eventDateFields + (
                       'KD', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK',
                       'DN', 'CODE_MES1',  'NAPR', 'CONS', 'ONK_SL',  'KSG_KPG',
                       'REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                       'SUM_M',  'LEK_PR')

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'prefix': 'COVID_LEK_LEK_PR',
        },
    }
    medicalSuppliesGroup = { 'fields': ('ID_LEK_PR', 'DATA_INJ', 'CODE_SH',
                                        'REGNUM', 'COD_MARK', 'LEK_DOSE'),
                    'dateFields': ('DATA_INJ', ),
                    'requiredFields': ('DATA_INJ', 'CODE_SH'),
                    'prefix': 'COVID_LEK',
                    'subGroup': medicalSuppliesDoseGroup,  }
    eventCovidSubGroup = {
        'LEK_PR': medicalSuppliesGroup
    }

    eventSubGroup = {
        'KSG_KPG': {'fields': ksgFields, 'subGroup': ksgSubGroup},
        'LEK_PR': medicalSuppliesGroup
    }

    onkLekPrSubGroup = {
        'LEK_PR' : {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ')}
    }

    onkSlSubGroup = {
        'ONK_USL': {'fields': ('USL_TIP', 'HIR_TIP', 'LEK_TIP_L',
                               'LEK_TIP_V', 'LEK_PR', 'PPTR', 'LUCH_TIP'),
                    'subGroup': onkLekPrSubGroup},
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE', 'DIAG_RSLT',
                              'REC_RSLT')},
        'B_PROT': {'fields': ('PROT', 'D_PROT')}
    }
    eventOnkSubGroup = {
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V'),
                 'dateFields': ('NAPR_DATE', )},
        'ONK_SL': {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                              'B_DIAG', 'B_PROT', 'SOD'),
                   'subGroup': onkSlSubGroup},
    }
    eventOnkHospSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V'),
                 'dateFields': ('NAPR_DATE', )},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'ONK_SL': {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                              'B_DIAG', 'B_PROT', 'SOD'),
                   'subGroup': onkSlSubGroup},
        'KSG_KPG': {'fields': ksgFields, 'subGroup': ksgSubGroup}
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = ('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME',
                     'DET', 'DATE_IN', 'DATE_OUT', 'DS', 'CODE_USL', 'KOL_USL',
                     'TARIF', 'SUMV_USL', 'MR_USL_N', 'NPL')
    serviceOnkFields = ('IDSERV', 'LPU', 'LPU_1', 'PROFIL', 'VID_VME',
                     'DET', 'DATE_IN', 'DATE_OUT', 'DS', 'CODE_USL', 'KOL_USL',
                     'TARIF', 'SUMV_USL', 'NPL')
    serviceSubGroup = {
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    mapEventOrderToForPom = {1: '3', 2: '1', 3: '1', 4: '3', 5: '3', 6: '2'}
    mapEventOrderToPPer = {5: '4', 7: '3'}
    mapPCel = {'101': '3.1', '102': '2.2',
               '103': '2.1', '104': '2.5', '106': '3.1', '107': '2.3',
               '201': '1.1', '301': '3.0', '302': '3.0', '401': '1.0',
               '402': '2.6', '403': '2.6', '404': '2.6', '405': '2.6',
               '406': '1.3', '407': '2.6', '408': '2.5', '409': '1.3',
               '109': '1.3', '501': '2.2', '502': '2.1', '503': '2.2',
               '303': '2.6', '304': '3.0', '601': '1.3', '602': '2.2',
               '603': '3.1', '604': '2.3', '605': '2.5', '606': '2.6',
               '607': '1.0', '610': '3.1', '620': '2.6', '621': '2.5',
               '330': '3.0', '309': '3.0', '700': '3.0', '701': '3.0',
               '340': '3.0', '341': '3.0', '342': '3.0', '504': '3.1'}

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self._coefficientCache = {}
        self.__serviceNumber = 0


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""

        if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5:
            self.eventSubGroup = self.eventOnkSubGroup
            self.eventFields = self.eventOnkFields
            self.serviceFields = self.serviceOnkFields
            self.serviceSubGroup = None
            self.clientFields = self.clientOnkFields

        settleDate = params['settleDate']

        self.writeStartElement('ZL_LIST')
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.2')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME',
            self._parent.wizard().getXmlFileName(False)[:-4])
        self.writeTextElement('SD_Z', forceString(
            self._parent.getCompleteEventCount()))
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', str(params['accId']))
        codeMo = params['lpuCode']
        self.writeTextElement('CODE_MO', codeMo)
        year = str(settleDate.year())
        month = str(settleDate.month())
        self.writeTextElement('YEAR', year)
        self.writeTextElement('MONTH', month)
        self.writeTextElement('NSCHET', u'{prefix}H{year}{month}'.format(
            prefix=codeMo[:3], year=year[:2], month=month[:2]))
        self.writeTextElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeTextElement('SUMMAV', str(params['accSum']))
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        lastEventId = forceRef(record.value('lastEventId'))
        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
        params['isDiagnostics'] = forceBool( # Выключаем диагностику для ДС.
            record.value('isDiagnostics')) and medicalAidTypeCode != 7
        params['eventId'] = lastEventId
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)
        params['isStomatology'] = medicalAidTypeCode == 9
        params['isEmergency'] = medicalAidTypeCode in (4, 5)
        params['isAmbulance'] = medicalAidTypeCode == 6

        record.setValue(
            'Z_SL_SUMV', params['completeEventSum'].get(lastEventId, 0))

        if (clientId != params.setdefault('lastClientId') or
                lastEventId != params.setdefault('lastComleteEventId')):
            if params['lastClientId']:
                if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5:
                    self.writeTextElement('COMENTSL', '')
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                params['lastRecord'],
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['recNum']))
            self.writeTextElement('PR_NOV', params['isReexposed'])
            self.writeClientInfo(record, params)

            params['lastClientId'] = clientId
            params['lastEventId'] = None
            params['lastComleteEventId'] = None
            params['recNum'] += 1

        self.writeCompleteEvent(record, params)
        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeCompleteEvent(self, record, params):
        u"""Пишет информацию о законченном случае, группа Z_SL"""
        lastEventId = forceRef(record.value('lastEventId'))

        if lastEventId == params.get('lastComleteEventId'):
            return

        if params['lastEventId']:
            self.writeEndElement()
            self.writeGroup(
                'Z_SL', self.completeEventFields2, params['lastRecord'],
                closeGroup=True, openGroup=False)

        eventOrder = forceInt(record.value('eventOrder'))
        record.setValue('Z_SL_FOR_POM', self.mapEventOrderToForPom.get(
            eventOrder, ''))
        if params['isHospital']:
            record.setValue('Z_SL_KD_Z', params['completeEventBedDays'].get(
                lastEventId, ''))
        self.writeGroup('Z_SL', self.completeEventFields1, record,
                        closeGroup=False,
                        dateFields=self.completeEventDateFields)
        params['lastComleteEventId'] = forceRef(record.value('lastEventId'))
        params['lastEventId'] = None
        params['lastRecord'] = record

    MAP_IDSL_CODE = {
        u'КСЛП001': 1, u'КСЛП002': 2, u'КСЛП003': 3, u'КСЛП004': 4,
        u'КСЛП005': 5, u'КСЛП006': 6, u'КСЛП6.1': 6, u'КСЛП007': 7,
        u'КСЛП7.1': 7, u'КСЛП008': 8, u'КСЛП8.1': 8, u'КСЛП009': 9,
        u'КСЛП9.1': 9, u'КСЛП010': 10 }

    def prepareCoefficients(self, coefficients):
        u"""Готовит блок SL_KOEF"""
        result = {}
        total = 0

        for _, i in coefficients.iteritems():
            for key, val in i.iteritems():
                code_ = self.MAP_IDSL_CODE.get(key)

                if code_:
                    result.setdefault('SL_KOEF_IDSL', []).append(code_)
                    result.setdefault('SL_KOEF_Z_SL', []).append('%1.5f' % val)
                    total += val

        if total:
            result['KSG_KPG_IT_SL'] = '%1.5f' % total
        return result


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        if eventId == params.setdefault('lastEventId'):
            return

        params['eventProfileRegionalCode'] = forceInt(record.value(
            'eventProfileRegionalCode'))
        eventOrder = forceInt(record.value('eventOrder'))
        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))

        local_params = {
            'SL_SUM_M': params['eventSum'].get(eventId, 0.0),
            'SL_DS_ONK': params['onkologyInfo'].get(
                eventId, {}).get('SL_DS_ONK')
        }
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)
        params['isStomatology'] = medicalAidTypeCode == 9

        if not forceString(record.value('SL_LPU_1')):
            code = self._parent.getParentCode(forceRef(record.value(
                'personOrgStructureParentId')), params['sysIdTfoms51F003Dep'])
            record.setValue('SL_LPU_1',  code)

        if params['isHospital']:
            local_params['SL_EXTR'] = (forceString(
                eventOrder) if eventOrder in (1, 2)  else '')
            local_params['SL_P_PER'] = self.mapEventOrderToPPer.get(
                eventOrder)
            if not local_params['SL_P_PER']:
                deliveredBy = forceString(record.value('deliveredBy'))
                local_params['SL_P_PER'] = 2 if deliveredBy == u'СМП' else 1

            hospActionId = forceRef(record.value('hospActionId'))
            if hospActionId:
                action = CAction.getActionById(hospActionId)
                bedCode = self.getHospitalBedProfileRegionalCode(
                    self.getHospitalBedProfileId(forceRef(action[u'койка'])))
                local_params['SL_PROFIL_K'] = bedCode

        elif params['isStomatology']:
            local_params['SL_ED_COL'] = params['uetSum'].get(eventId, .0)
        else:
            local_params['SL_ED_COL'] = params['visitCount'].get(
                eventId, record.value('amount'))

        pcel = forceString(record.value('SL_P_CEL'))
        pcel = ('2.6' if pcel == '610' and forceRef(record.value('actionId'))
                else self.mapPCel.get(pcel, ''))
        record.setValue('SL_P_CEL', toVariant(pcel))
        ds1 = forceString(record.value('SL_DS1'))
        eventOrder = forceInt(record.value('eventOrder'))
        isCovidSupples = eventOrder in (1, 4, 5) and ds1 in (
            'U07.1', 'U07.2')
        if isCovidSupples:
            local_params.update(params['medicalSuppliesInfo'].get(
                eventId, {}))

        local_params.update(params)
        self.__serviceNumber = 0

        if params['lastEventId']:
            if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5:
                self.writeTextElement('COMENTSL', '')
            self.writeEndElement() # SL

        if params['isHospital']:
            local_params['KSG_KPG_VER_KSG'] = forceString(
                params['settleDate'].year())
            local_params['KSG_KPG_BZTSZ'] = params.get(
                'contractAttrCS' if medicalAidTypeCode in (1, 2, 3) else
                'contractAttrDS', 0)
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

                    #local_params['KSG_KPG_IT_SL'] = u'%.5f' %  i['__all__']

                record.setValue('KSG_KPG_SL_K', 1)
                local_params.update(self.prepareCoefficients(
                    coefficients))

            coef = (forceDouble(local_params['KSG_KPG_BZTSZ']
                                if local_params['KSG_KPG_BZTSZ'] else 0.0))

            if coef != 0:
                record.setValue('KSG_KPG_KOEF_U', u'%.5f' % (forceDouble(
                    record.value('KSG_KPG_KOEF_U')) / coef))
            else:
                record.setNull('KSG_KPG_KOEF_U')
        else: # not Hospital
            record.setValue('SL_TARIF', toVariant(
                params['eventSum'].get(eventId)))

        record.setValue('KSG_KPG_KOEF_Z', '%.5f' % forceDouble(
            record.value('KSG_KPG_KOEF_Z')))
        local_params['KSG_KPG_CRIT'] = forceString(
            record.value('critList')).split(',')

        _record = CExtendedRecord(record, local_params, DEBUG)

        isOnkExport = self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5
        if params['isHospital']:
            subGroup = (self.eventOnkHospSubGroup if isOnkExport
                        else self.eventSubGroup)
        else:
            subGroup = (self.eventOnkSubGroup if isOnkExport
                        else self.eventCovidSubGroup)

        if isOnkExport:
            local_params.update(params['onkologyInfo'].get(eventId, {}))
        self.writeGroup('SL', self.eventFields, _record, subGroup=subGroup,
                        closeGroup=False, dateFields=self.eventDateFields)
        params['lastEventId'] = eventId


    def exportVisits(self, eventId, params):
        u"""Экспортирует данные для визитов с 0 стоимостью,
            при тарификации по посещениям"""
        stmt = u"""SELECT
            PersonOrganisation.miacCode AS USL_LPU,
            IFNULL(EventType_Identification.value,
                   PersonOrgStructure.infisDepTypeCode) AS USL_PODR,
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
            IF('{unit}' IN ('9', '24', '31'), 0, '') AS USL_TARIF,
            0 AS USL_SUMV_USL,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.SNILS AS MR_USL_N_CODE_MD,
            '1' AS MR_USL_N_MR_N,
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
        LEFT JOIN EventType_Identification ON EventType_Identification.id = (
            SELECT EI.id FROM EventType_Identification EI
            WHERE EI.master_id = Event.eventType_id
              AND EI.deleted = 0
              AND EI.system_id = '{sysIdEmergency}'
            LIMIT 0, 1)
        WHERE Visit.event_id = {eventId}
            AND Visit.deleted = '0'
            AND (rbEventProfile.regionalCode IS NULL OR rbEventProfile.regionalCode != '6') -- исключаем стоматологию
        ORDER BY Visit.date""".format(
            eventId=eventId, unit=params['medicalAidUnit'],
            sysIdEmergency=self._getAccSysId(u'НеотлПом'),)

        query = self._parent.db.query(stmt)
        result = False

        if query.size() > 1:
            curPos = 1
            querySize = query.size()
            self.__serviceNumber -= 1

            while query.next():
                record = query.record()
                params['isLastVisit'] = curPos == querySize

                self.writeService(record, params)
                curPos += 1

            result = True

        return result


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        if not forceString(record.value('USL_PODR')):
            record.setValue('USL_PODR', record.value('SL_PODR'))

        if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B7:
            age = forceInt(record.value('clientAge'))
            record.setValue('USL_DIR_SUBLPU', '112' if age < 18 else '111')

        self.__serviceNumber += 1
        params['USL_IDSERV'] = self.__serviceNumber
        record.setValue('MR_USL_N_CODE_MD',
            toVariant(formatSNILS(record.value('MR_USL_N_CODE_MD'))))

        if params['isDiagnostics']:
            _record = CExtendedRecord(record, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroup)
            return

        eventId = forceRef(record.value('eventId'))
        params['USL_LPU_1'] = forceString(record.value('SL_LPU_1'))
        isVisitExported = False

        if (eventId and
                eventId not in params.setdefault('exportedEvents', set())):
            params['tarif'] = record.value('SL_TARIF')
            params['sum'] = record.value('Z_SL_SUMV')
            params['amount'] = record.value('SL_ED_COL')
            params['medicalAidUnit'] = forceString(
                record.value('Z_SL_IDSPFEDERAL'))
            params['exportedEvents'].add(eventId)
            isVisitExported = self.exportVisits(eventId, params)

        isDispensaryObservation = forceBool(record.value('isDispensaryObservation'))
        if isDispensaryObservation and eventId and eventId not in params.setdefault('exportedObservations', set()):
            self.__exportObservationActions(eventId, params)
            params['exportedObservations'].add(eventId)

        if not isVisitExported and (not params['isHospital']
                                    or params.get('force')):
            if (forceString(record.value('KSG_KPG_N_KSG')) ==
                    forceString(record.value('USL_CODE_USL'))
                    and not params.get('isOnkservice')):
                return

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
                    for _, _list in coefficientList.iteritems():
                        for _, value in _list.iteritems():
                            if value > 1.0:
                                params['USL_COMENTU'] = value
                                break

                        if params.has_key('USL_COMENTU'):
                            break

            local_params = dict(params)
            if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5:
                local_params.update(params['onkologyInfo'].get(eventId, {}))
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroup)

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

        if params['isHospital'] and eventId not in params.setdefault(
                'isOperationExported', set()):
            params['isOperationExported'].add(eventId)
            for operation in params['operation'].get(eventId, []):
                _record = CExtendedRecord(operation, params, DEBUG)
                self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroup)
                params['USL_IDSERV'] += 1


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        isInsurerNameNeeded = not forceString(record.value('PACIENT_SMO'))
        isFreshBorn = forceString(record.value('PACIENT_NOVOR'))
        if not isFreshBorn:
            record.setNull('PACIENT_VNOV_D')
        if not isInsurerNameNeeded:
            record.setNull('PACIENT_SMO_NAM')
        _record = CExtendedRecord(record, params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            if self._parent.registryType == CExportPage1.REGISTRY_TYPE_B5:
                self.writeTextElement('COMENTSL', '')
            self.writeEndElement() # SL
            self.writeGroup('Z_SL', self.completeEventFields2,
                            params['lastRecord'],
                            closeGroup=True,
                            openGroup=False)
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def __exportObservationActions(self, eventId, params):
        u"""Выгрузка действий для ДН"""
        actions = params.get('observationActions', dict()).get(eventId, list())
        for action in actions:
            _record = CExtendedRecord(action, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                        dateFields=self.serviceDateFields,
                        subGroup=self.serviceSubGroup)
            params['USL_IDSERV'] += 1



# ******************************************************************************

class CRegistryWriter(COrder79XmlStreamWriter, CExportHelperMixin):
    eventDateFields = tuple()
    eventFields1 = ('SL_ID', 'COUNT', 'CODE_COUNT', 'CARD', 'R_MP', 'KRIM',
                   'MASTER', 'DIR_SUBLPU', 'DIR_TOWN', 'TOWN_HOSP', 'DOP_PR',
                   'STOIM_D', 'SUM', 'TALON', 'BED_PROF', 'KSG', 'DEP_ADD',
                   'PR_OS', 'ZS', 'USL')
    eventFields2 = ('CNASP_V', 'LPU_DOST', 'TOWN_DOST', 'LPU_PEREV',
                    'SUB_PEREV', 'TOWN_PEREV', 'MOTHER', 'SERV_TIME', 'PURPOSE',
                    'DS_P', 'DS1_PR', 'SNILS_DOC', 'ADDR_CODE', 'SUB_HOSP',
                    'RSLT', 'ISHOD', 'DS_PZ')
    eventFields = eventFields1 + eventFields2
    sumFields = ('SUMV', 'VID_FIN', 'PAY_MODE')
    depAddFields = ('DATE_1', 'DATE_2', 'PRVS', 'PROFIL', 'DS1', 'IDDOKT')
    serviceDateFields = ('NPR_DATE', )
    serviceFields = ('IDSERV', 'ID_USL', 'TOOTH', 'DIRECT_LPU', 'TOWN_HOSP',
                     'DIR_SUBLPU', 'DIR_TOWN', 'PURPOSE', 'REASON', 'PR_VISIT',
                     'DIRECT_SPEC', 'SERV_METOD', 'VID_FIN', 'PAY_MODE',
                     'PR_OPER', 'NPR_DATE', 'SNILS_DOC', 'ADDR_CODE',
                     'SUB_HOSP', 'AIM', 'P_OTK')
    eventSubGroup = {'SUM': {'fields': sumFields }}
    hospitalEventSubGroup = { 'SUM': {'fields': sumFields },
                              'DEP_ADD': {'fields': depAddFields}}

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self._lastEventId = None
        self._serviceNumber = 0
        self.__lastRecord = None
        self.__lastSubGroup = None


    def logWarning(self, _str):
        self._parent.logWarning(_str)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']

        self.writeStartElement('REG_LIST')
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.2')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement(
            'FILENAME', self._parent.wizard().getRegistryXmlFileName()[:-4])
        self.writeTextElement(
            'FILENAME1',  self._parent.wizard().getXmlFileName()[:-4])

        self.writeStartElement('SUMMA')
        self.writeTextElement('SUMMAV', str(params['accSum']))
        self.writeTextElement('VID_FIN', str(params['contractFinanceType']))
        self.writeEndElement() # SUMMA
        self.writeEndElement() # ZGLV

        self._lastEventId = None
        self._serviceNumber = 0


    def writeRecord(self, record, params):
        lastEventId = forceRef(record.value('eventId'))

        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
        params['eventId'] = lastEventId
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)
        params['isDayHospital'] = medicalAidTypeCode == 7
        params['isStomatology'] = medicalAidTypeCode == 9
        params['isEmergency'] = medicalAidTypeCode in (4, 5)
        params['isAmbulance'] = medicalAidTypeCode == 6

        if lastEventId != self._lastEventId:
            if self._lastEventId:
                self.writeGroup('SLUCH', self.eventFields2, self.__lastRecord,
                                openGroup=False,
                                dateFields=self.eventDateFields)

            self.writeEventInfo(record, params)
            self._lastEventId = lastEventId
            self._serviceNumber = 1

        if not (params['isEmergency'] or
                (params['isHospital'] and
                 forceInt(record.value('serviceType')) != 4)):
            self.writeService(record, params)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if self._lastEventId:
            self.writeGroup('SLUCH', self.eventFields2, self.__lastRecord,
                            openGroup=False,
                            dateFields=self.eventDateFields)
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def writeEventInfo(self, record, params):
        local_params = {
            'SLUCH_COUNT': params['accNumber'][-10:],
            'SLUCH_R_MP': '1' if params['isStomatology'] else '0',
            'SLUCH_MASTER': '',
            'SUM_SUMV': params['eventSum'].get(params['eventId'], 0),
            'SUM_VID_FIN': forceString(params['contractFinanceType']),
        }
        registryInfo = params['registryInfo'].get(params['eventId'], [])
        if registryInfo:
            local_params.update(registryInfo[0])

        if params['isHospital']:
            criminalSign = forceBool(self.getActionPropertyText(
                params['eventId'], params['actionTypeIllegalActions'],
                u'Признак')) if params[
                    'actionTypeIllegalActions'] else False
            local_params['SLUCH_KRIM'] = '1' if criminalSign else '0'
            if not params['isDayHospital']:
                local_params['SLUCH_TALON'] = self.getActionPropertyText(
                    params['eventId'], params['actionTypeArrival'],
                    u'№ направления на госпитализацию')

            hospitalActionList = forceString(record.value(
                'hospitalActionIdList')).split(',')
            bedProfileId  = None

            for x in hospitalActionList:
                hospitalActionId = forceRef(x)
                local_params['bedProfileId'] = None
                local_params['isIntensive'] = False
                if hospitalActionId:
                    action = CAction.getActionById(hospitalActionId)
                    bedId = forceRef(action[u'койка'])
                    if bedId:
                        bedProfileId = self.getHospitalBedProfileId(bedId)
                        bedTypeCode = (self.getHospitalBedTypeCode(
                            self.getHospitalBedTypeId(bedId)))
                        actRecord = action.getRecord()
                        personId = forceRef(actRecord.value('person_id'))
                        if bedTypeCode in ('2', '3'):
                            local_params['DEP_ADD_PRVS'] = self.getPersonSpecialityFederalCode(personId)
                            local_params['DEP_ADD_DATE_1'] = forceDate(
                                actRecord.value('begDate'))
                            local_params['DEP_ADD_DATE_2'] = forceDate(
                                actRecord.value('endDate'))
                        else:
                            record.setNull('DEP_ADD_DS1')
                            record.setNull('DEP_ADD_IDDOKT')
                            record.setNull('DEP_ADD_PROFIL')

            local_params['SLUCH_BED_PROF'] =  self.getHospitalBedProfileRegionalCode(
                bedProfileId)
            local_params['SLUCH_PR_OS'] = '0'
            local_params['SLUCH_ZS'] = '1' if forceInt(record.value(
                'mesSpecificationLevel')) == 2 else '0'
            local_params['SLUHC_MOTHER'] = '0'

        if params['isEmergency']:
            local_params['SLUCH_DOP_PR'] = 0
            local_params['SLUCH_CNASP_V'] = local_params.get(
                'emergencyTownInfis')
            if forceString(local_params.get('emergencyResultCode')) == '4':
                local_params['SLUCH_LPU_DOST'] = params['currentOrgInfis']
                local_params['SLUCH_TOWN_DOST'] = forceString(
                    self._db.translate('kladr.KLADR', 'CODE',
                                       QtGui.qApp.defaultKLADR(), 'infis'))

        if forceRef(record.value('visitId')) and 'SLUCH_DIR_TOWN' in local_params:
            local_params.pop('SLUCH_DIR_TOWN')

        record.setValue('SLUCH_SNILS_DOC', formatSNILS(
            record.value('SLUCH_SNILS_DOC')))
        _record = CExtendedRecord(record, local_params, DEBUG)
        subGroup = (self.hospitalEventSubGroup if params['isHospital']
                    else self.eventSubGroup)
        self.writeGroup('SLUCH', self.eventFields1, _record, subGroup,
                            dateFields=self.eventDateFields, closeGroup=False)
        self.__lastRecord = _record
        self.__lastSubGroup = subGroup


    def writeService(self, record, params):
        local_params = {
            'USL_IDSERV': self._serviceNumber,
        }
        registryInfo = params['registryInfo'].get(params['eventId'], [])
        if registryInfo:
            local_params.update(registryInfo.pop(0))
        if params['isStomatology']:
            actionId = forceRef(record.value('actionId'))
            local_params['USL_TOOTH'] = self.toothNumber(actionId)
        relegateOrgId = forceRef(record.value('relegateOrgId'))
        tariffType = forceInt(record.value('tariffType'))
        eventTypeCode = forceString(record.value('eventTypeCode'))

        if eventTypeCode == '19-cz':
            if tariffType == CTariff.ttActionAmount:
                local_params['USL_DIRECT_LPU'] = self.getOrgStructureInfisCode(
                    QtGui.qApp.currentOrgStructureId())
            elif tariffType == CTariff.ttVisit:
                local_params['USL_DIRECT_LPU'] = forceString(record.value(
                    'relegateOrgCode')) if relegateOrgId else ''
        else:
            local_params['USL_DIRECT_LPU'] = forceString(local_params.get(
                'attachOrgCode') if not relegateOrgId else record.value(
                    'relegateOrgCode'))
        local_params['USL_TOWN_HOSP'] = params.get('accOrgStructTfomsCode', '')
        local_params['USL_DIR_TOWN'] = (forceString(
                record.value('relegateOrgTfomsExtCode')) if relegateOrgId else
                             local_params.get('attachOrgTfomsExtCode'))

        if (params['isStomatology']
                and forceString(local_params.get('USL_PURPOSE')) in ('301', '302')):
            serviceDate = forceDate(record.value('USL_DATE_OUT'))
            eventDate = forceDate(record.value('SL_DATE_1'))
            local_params['USL_PURPOSE'] = '302' if serviceDate > eventDate else '301'

        age = forceInt(record.value('clientAge'))
        local_params['USL_DIRECT_SPEC'] = forceString(local_params.get(
            'relegatePersonSpecialityCode'))
        if not local_params['USL_DIRECT_SPEC']:
            local_params['USL_DIRECT_SPEC'] = '49' if age < 18 else '76'

        if not params['isHospital']:
            local_params['USL_VID_FIN'] = forceString(
                params['contractFinanceType'])
        else:
            local_params['USL_PR_OPER'] = (1 if forceString(
                record.value('serviceCode')) == u'A16.20.037' else 0)

        record.setValue('USL_SNILS_DOC', formatSNILS(
            record.value('USL_SNILS_DOC')))

        if not forceString(record.value('USL_ADDR_CODE')):
            _id = forceRef(record.value('addrCodeOrgStructId'))
            code = self._parent.getParentCode(_id, params['sysIdAddrCode'])
            record.setValue('USL_ADDR_CODE', toVariant(code))

        if forceRef(record.value('visitId')) and not relegateOrgId:
            for field in ('USL_DIRECT_LPU', 'USL_DIR_SUBLPU', 'USL_DIRECT_SPEC',
                          'USL_NPR_DATE', 'USL_DIR_TOWN'):
                if field in local_params:
                    local_params.pop(field)
                else:
                    record.setNull(field)
        if (not record.contains('USL_DIRECT_LPU')
                and not local_params.has_key('USL_DIRECT_LPU')):
            local_params['USL_REASON'] = 1 if forceInt(
                record.value('eventOrder')) == 6 else 4

        orgId = forceRef(local_params.get('actionOrgId'))
        servDate = forceDate(record.value('USL_DATE_IN'))
        begDate = forceDate(record.value('Z_SL_DATE_Z_1'))
        endDate = forceDate(record.value('Z_SL_DATE_Z_2'))
        if '6' == forceString(record.value('medicalAidTypeCode')):
            local_params['USL_AIM'] = '1' if (
                (orgId and orgId != params['currentOrgId'])
                or not ((servDate >= begDate) and (servDate <= endDate))
                or local_params.get('visitTypeCode') == u'ВУ') else '0'

        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('USL', self.serviceFields, _record,
                            dateFields=self.serviceDateFields,
                            subGroup=self.serviceSubGroup)
        self._serviceNumber += 1


class CPersonalDataWriter(CR60PersonalDataWriter):
    EVENT_EXEC_DATE_FIELD_NAME = 'SL_DATE_2'


    def __init__(self, parent):
        CR60PersonalDataWriter.__init__(self, parent)


    def writeClientInfo(self, record, params):
        record.setValue('PERS_SNILS', formatSNILS(record.value('PERS_SNILS')))
        CR60PersonalDataWriter.writeClientInfo(self, record, params)

# ******************************************************************************

class CMedicalSuppliesInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)


    def _stmt(self):
        regnum = u"""(SELECT N.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature N ON APN.value = N.id
         WHERE APT.descr = 'N20' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1)"""
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        1 AS COVID_LEK_LEK_PR_ID_LEK_PR,
        Action.endDate AS COVID_LEK_LEK_PR_DATA_INJ,
        (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_String APS ON APS.id = AP.id
         WHERE APT.descr = 'V032' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_CODE_SH,
        (SELECT IF(N.code != '', LPAD(N.code, 6, '0'), '') FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature N ON APN.value = N.id
         WHERE APT.descr = 'N20' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_REGNUM,
        (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_String APS ON APS.id = AP.id
         WHERE APT.descr = 'COD_MARK' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_COD_MARK,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT UI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbUnit APU ON APU.id = AP.id
         INNER JOIN rbUnit_Identification UI ON UI.master_id = APU.value
         WHERE APT.descr = 'V034' AND AP.action_id = Action.id
           AND AP.deleted = 0
           AND UI.system_id = '{unitSysId}'
         LIMIT 1), NULL) AS COVID_LEK_LEK_PR_LEK_DOSE_ED_IZM,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT GROUP_CONCAT(APD.value) FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
         WHERE APT.descr = 'Доза' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1), NULL) COVID_LEK_LEK_PR_LEK_DOSE_DOSE_INJ,
        IF({regnum} IS NOT NULL AND {regnum} != '',
        (SELECT GROUP_CONCAT(N.value) FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureUsingType APNU ON APNU.id = AP.id
         INNER JOIN rbNomenclatureUsingType_Identification N ON APNU.value = N.master_id
         WHERE APT.descr = 'V035'
           AND N.system_id = '{nomenclatureUsingTypeId}' AND N.deleted = 0
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1), NULL)  AS COVID_LEK_LEK_PR_LEK_DOSE_METHOD_INJ,
        IF({regnum} IS NOT NULL AND {regnum} != '',
         Action.amount, '') AS COVID_LEK_LEK_PR_LEK_DOSE_COL_INJ
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'MedicalSupplies'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id""" .format(
            idList=self._idList,
            regnum=regnum,
            unitSysId=self._parent._getAccSysIdByUrn(
                'urn:tfoms51:V034'),
            nomenclatureUsingTypeId=self._parent._getAccSysIdByUrn(
                'urn:tfoms51:V035'))
        return stmt


    def get(self, _db, _idList, parent):
        result = CMultiRecordInfo.get(self, _db, _idList, parent)
        for key, val in result.items():
            val['COVID_LEK_LEK_PR_ID_LEK_PR'] = range(
                1, 1 + len(val['eventId']))
        return result

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51Ambulance,
                      configFileName='75_18_s11.ini',
                      eventIdList=[6215925])
