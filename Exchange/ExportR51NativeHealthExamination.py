# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Экспорт счетов для Мурманска, Б6"""

import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile,  QDate
from library.Utils import (forceRef, forceString, forceDouble, forceBool,
                           toVariant, forceInt, formatSNILS, forceDate)

from Accounting.Utils import getIntContractAttribute
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CAbstractExportPage1Xml,
                             CExportHelperMixin, record2Dict)
from Exchange.ExportR60NativeAmbulance import PersonalDataWriter
from Exchange.ExportR60NativeHealthExamination import (
    getEventTypeCode, getEventTypeDDCode)
from Exchange.Order79Export import (COrder79ExportWizard, COrder79ExportPage1,
                                    COrder79ExportPage2,
                                    COrder79XmlStreamWriter)
from Exchange.Ui_ExportR60NativeAmbulancePage1 import Ui_ExportPage1
from Exchange.Utils import compressFileInZip, tbl

DEBUG = False


def exportR51HealthExamination(widget, accountId, accountItemIdList,
                               accountIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта Мурманск"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Мурманска, ДД Б4'
        prefix = 'R51HealthExamination'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.accountIdList = None
        self.__xmlBaseFileName = None


    def setAccountIdList(self, accountIdList):
        u"""Запоминает список идентификаторов счетов"""
        self.accountIdList = accountIdList


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""

        if self.__xmlBaseFileName:
            result = self.__xmlBaseFileName
        else:
            sysIdTfoms51F002 = self.page1._getAccSysIdByUrn('urn:tfoms51:F002')
            sysIdTfoms51F003 = self.page1._getAccSysIdByUrn('urn:tfoms51:F003')
            payerCode = self.page1._getOrgIdentification(
                self.info['payerId'], sysIdTfoms51F002)
            if not payerCode:
                payerCode = forceString(self.db.translate(
                    'Organisation', 'id', self.info['payerId'], 'infisCode'))
            record = self.db.getRecord('OrgStructure', 'infisCode,tfomsCode',
                                       self.info['accOrgStructureId'])
            orgStructCode = forceString(record.value(0)) if record else None
            tfomsCode = forceString(record.value(1)) if record else None
            currentOrgId = QtGui.qApp.currentOrgId()
            record = self.db.getRecord('Organisation', 'infisCode,tfomsExtCode',
                                       currentOrgId)
            lpuCode = self.page1._getOrgIdentification(currentOrgId,
                                                       sysIdTfoms51F003)
            if not lpuCode:
                lpuCode = forceString(record.value(0)) if record else None
            tfomsExtCode = forceString(
                record.value(1)) if record else None

            postfix = u'{year:02d}{month:02d}{packetNumber}'.format(
                year=self.info['settleDate'].year() % 100,
                month=self.info['settleDate'].month(),
                packetNumber=self.page1.edtPacketNumber.value()
                ) if addPostfix else u''

            result = (u'{prefix}M{lpuCode}{orgStructCode}{townCode}{rc}{payer}_'
                      u'{postfix}.xml'.format(
                          prefix=self.prefixX(self.info['accId']),
                          lpuCode=lpuCode,
                          orgStructCode=orgStructCode if orgStructCode else '00',
                          townCode=tfomsCode if tfomsCode else tfomsExtCode,
                          payer=payerCode, postfix=postfix,
                          rc='T' if payerCode == '01' else 'S'))
            self.__xmlBaseFileName = result

        return result


    def prefixX(self, accountId):
        u"""Вовзращает префикс имени файла"""
        code = getEventTypeCode(self.db, accountId, code='FILENAME')
        return code if code else '-'


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L{0}'.format(self._getXmlBaseFileName(addPostfix)[1:])


    def getRegistryXmlFileName(self):
        u"""Имя файла для формата Б3"""
        return u'T{0}'.format(self._getXmlBaseFileName()[1:])


    def getRegistryFullXmlFileName(self):
        u"""Имя файла для формата Б3"""
        return os.path.join(self.getTmpDir(), self.getRegistryXmlFileName())


    def getZipFileName(self):
        u"""Возвращает имя архива:"""
        return u'{0}.zip'.format(self._getXmlBaseFileName()[:-4])

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), PersonalDataWriter(self),
                     CRegistryWriter(self))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.cmbRegistryType.setVisible(False)
        self.lblRegistryType.setVisible(False)
        self.chkAmbulancePlanComplete.setVisible(False)
        self.chkEmergencyPlanComplete.setVisible(False)
        self.chkAdditionalSumOfPCF.setVisible(False)
        self.edtAdditionalSumOfPCF.setVisible(False)

        self._orgStructureIdentificationCache = {}
        self._orgStructureParentIdCache = {}

        self._tblOrgStructuteIdentification = tbl('OrgStructure_Identification')


    def setExportMode(self, flag):
        self.chkReexposed.setEnabled(not flag)
        COrder79ExportPage1.setExportMode(self, flag)


    def nschet(self, registryType, params):
        settleDate = params['settleDate']
        return u'{p}{x}{year:02d}{month:02d}{registryNumber:d}'.format(
            p=(params['lpuInfisCode'] if params['lpuInfisCode']
               else params['lpuCode'])[-3:],
            x=self._parent.prefixX(params['accId']),
            year=settleDate.year() % 100,
            month=settleDate.month(),
            registryNumber=self.edtPacketNumber.value())


    def _serviceCountByEvent(self):
        u"""Возвращает количество услуг в событии."""

        stmt = """SELECT Account_Item.event_id,
            COUNT(DISTINCT Action.id)
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id AND Action.deleted = 0
        INNER JOIN ActionType_Service ON ActionType_Service.master_id = Action.actionType_id
        WHERE {0}
        GROUP BY Account_Item.event_id""".format(
            self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            actionCount = forceInt(record.value(1))
            yield eventId, actionCount


    def prepareStmt(self, params):
        sysIdTfoms51F002 = self._getAccSysIdByUrn('urn:tfoms51:F002')
        sysIdOid635 = self._getAccSysIdByUrn('urn:oid:1.2.643.5.1.13.2.1.1.635')
        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            IF(ExposedAccountItem.id IS NULL AND rbPayRefuseType.id IS NULL, 0, 1)AS isExposedItem,
            IF(rbMesSpecification.level = '2', 1, 0) AS isMesComplete,
            Person.SNILS AS personSNILS,
            formatClientAddress(ClientRegAddress.id) AS personRegAddress,
            LastEvent.id AS lastEventId,
            rbDiagnosticResult.regionalCode AS diagRegCode,
            Relegate.id AS relegateOrgId,
            Relegate.infisCode AS relegateOrgCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            rbVisitType.regionalCode AS visitTypeRegionalCode,
            ClientAttach.begDate AS clientAttachBegDate,
            rbMedicalAidType.code AS medicalAidTypeCode,
            Action.org_id,
            Event.setDate,
            Account_Item.sum,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.regionalCode = '1', ClientPolicy.serial,
                '') AS PACIENT_SPOLIS,
            IF(rbPolicyKind.code IN (1, 2), ClientPolicy.number,
                '') AS PACIENT_NPOLIS,
            IF(rbPolicyKind.code IN (1, 2), '',
                ClientPolicy.number) AS PACIENT_ENP,
            Insurer.OKATO AS PACIENT_ST_OKATO,
            IFNULL(IFNULL((SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = '{payerId}'
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms51F002}'
               LIMIT 1)
            , (SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = '{payerId}'
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdOid635}'
               LIMIT 1)), '{payerInfis}') AS PACIENT_SMO,
            Insurer.OGRN AS PACIENT_SMO_OGRN,
            Insurer.OKATO AS PACIENT_SMO_OK,
            Insurer.shortName AS PACIENT_SMO_NAM,
            0 AS PACIENT_NOVOR,

            Account_Item.event_id AS Z_SL_IDCASE,
            rbMedicalAidKind.regionalCode AS Z_SL_VIDPOM,
            '{lpuCode}' AS Z_SL_LPU,
            IF(rbScene.code = '4', 1, 0)  AS Z_SL_VBR,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            IF(rbDiagnosticResult.regionalCode = '502', 1, 0) AS Z_SL_P_OTK,
            EventResult.regionalCode AS Z_SL_RSLT,
            EventResult.federalCode AS Z_SL_RSLT_D,
            rbDiagnosticResult.regionalCode AS Z_SL_ISHOD,
            IFNULL((SELECT value FROM rbMedicalAidUnit_Identification
                    WHERE master_id = Account_Item.unit_id
                      AND deleted = 0
                      AND system_id = IF(rbMesSpecification.level = '2',
                        '{sysIdIdsp}', '{sysIdIdspPos}')
                    LIMIT 1), rbMedicalAidUnit.regionalCode) AS Z_SL_IDSP,
            Account_Item.sum AS Z_SL_SUMV,
            IF(Client.patrName='', 1, '') AS Z_SL_OS_SLUCH,

            Account_Item.event_id AS SL_SL_ID,
            PersonOrgStructure.id AS SL_LPU_1,
            Event.id AS SL_NHISTORY,
            Event.setDate AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            Diagnosis.MKB AS SL_DS1,
            Account_Item.price AS SL_TARIF,
            IF(rbDiseaseCharacter.code IN (1, 2), 1, '') AS SL_DS1_PR,
            CASE
                WHEN rbDispanser.code = '1' THEN 1
                WHEN rbDispanser.code IN ('2', '6') THEN 2
                ELSE 3
            END AS SL_PR_D_N,
            Account_Item.sum AS SL_SUM_M,

            (SELECT GROUP_CONCAT(Diagnosis.MKB)
             FROM Diagnostic dc
             LEFT JOIN Diagnosis ON Diagnosis.id = dc.diagnosis_id
             WHERE dc.event_id = Account_Item.event_id
               AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
               AND dc.deleted = 0) AS DS2_N_DS2_,
            (SELECT GROUP_CONCAT(CASE
                WHEN rbDispanser.code = '1' THEN 1
                WHEN rbDispanser.code IN ('2', '6') THEN 2
                ELSE 3
             END)
             FROM Diagnostic dc
             LEFT JOIN Diagnosis ON Diagnosis.id = dc.diagnosis_id
             LEFT JOIN rbDispanser ON rbDispanser.id = Diagnosis.dispanser_id
             WHERE dc.event_id = Account_Item.event_id
               AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
               AND dc.deleted = 0) AS DS2_N_PR_DS2_N_,
            (SELECT GROUP_CONCAT(
                IF(rbDiseaseCharacter.code = 2, 1, 0))
             FROM Diagnostic dc
             LEFT JOIN Diagnosis ON Diagnosis.id = dc.diagnosis_id
             LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = dc.character_id
             WHERE dc.event_id = Account_Item.event_id
               AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
               AND dc.deleted = 0) AS DS2_N_DS2_PR_,

            '{lpuCode}' AS USL_LPU,
            PersonOrgStructure.id AS USL_LPU_1,
            IF(Action.status = 6, Event.setDate,
                IFNULL(Action.begDate, Visit.date)) AS USL_DATE_IN,
            IF(Action.status = 6, Event.setDate,
                IFNULL(Action.endDate, Visit.date)) AS USL_DATE_OUT,
            IF(rbDiagnosticResult.regionalCode = '502', 1, 0) AS USL_P_OTK,
            IF(rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL,
                MES_visit.altAdditionalServiceCode,
                    IF(rbService.infis IS NULL OR rbService.infis = '',
                        rbService.code, rbService.infis)) AS USL_CODE_USL,
            IF(rbMesSpecification.level = '2',Account_Item.price, 0) AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            1 AS MR_USL_N_MR_N,
            ActionSpeciality.federalCode AS MR_USL_N_PRVS,
            ActionPerson.SNILS AS MR_USL_N_CODE_MD,
            IFNULL((SELECT value FROM rbMedicalAidUnit_Identification
                    WHERE master_id = Account_Item.unit_id
                      AND deleted = 0
                      AND system_id = '{sysIdPayMode}'
                    LIMIT 1), rbMedicalAidUnit.regionalCode) AS USL_PAY_MODE,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            IFNULL((SELECT rSI.value FROM rbService_Identification rSI
             WHERE rSI.master_id = rbService.id
               AND rSI.deleted = 0
               AND rSI.system_id IN (SELECT id FROM rbAccountingSystem
                                    WHERE urn = "urn:tfoms51:V001")),
                rbService.infis) AS USL_VID_VME,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.lastName) AS PERS_FAM,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            rbDocumentType.regionalCode AS PERS_DOCTYPE,
            IF(rbDocumentType.code = '003',
                REPLACE(TRIM(ClientDocument.serial),' ', '-'),
                TRIM(ClientDocument.serial)) AS PERS_DOCSER,
            ClientDocument.number AS PERS_DOCNUM,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,
            IF(rbPolicyKind.regionalCode != 3, ClientDocument.date,'') AS PERS_DOCDATE,
            IF(rbPolicyKind.regionalCode != 3, ClientDocument.origin, '') AS PERS_DOCORG,
            (SELECT IF(MAX(ds.id) IS NOT NULL, 1, 0)
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code IN (1, 2, 9))
                  AND dc.event_id = Account_Item.event_id
                  AND rbDiseasePhases.code = 10
                  AND (SUBSTR(ds.MKB,1,1) = 'C' OR
                       (ds.MKB = 'Z03.1') OR
                       (SUBSTR(ds.MKB,1,3) BETWEEN 'D00' AND 'D09'
                        AND dc.diagnosisType_id IN (
                            SELECT id FROM rbDiagnosisType WHERE code IN (1, 2)
                      )))
            ) AS SL_DS_ONK,

            Account_Item.sum AS SUM_SUMV,
            Account_Item.event_id AS SLUCH_SL_ID,
            EXISTS (SELECT id FROM ClientWork
                    WHERE ClientWork.client_id = Event.client_id) AS  SLUCH_WORK,
            IFNULL((SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = AttachOrg.id
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms51F003}'
               LIMIT 1),
            AttachOrg.infisCode) AS SLUCH_MASTER,
            Person.SNILS AS SLUCH_SNILS_DOC,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = Person.orgStructure_id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
            ) AS SLUCH_ADDR_CODE,
            (SELECT infisCode FROM OrgStructure OS
             WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS SLUCH_SUB_HOSP,
            (SELECT Diagnosis.MKB FROM Diagnosis
             LEFT JOIN Diagnostic ON Diagnosis.id = Diagnostic.diagnosis_id
             LEFT JOIN rbDiseaseCharacter ON
                rbDiseaseCharacter.id = Diagnosis.character_id
             WHERE Diagnosis.deleted = 0
               AND rbDiseaseCharacter.code = 10
               AND Diagnostic.id = (
                   SELECT MAX(dc.id)
                   FROM Diagnostic dc
                   WHERE dc.event_id = Account_Item.event_id
                     AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType
                                                 WHERE code = '1')
                     AND dc.deleted = 0)) AS SLUCH_DS_PZ,
            (SELECT tfomsCode FROM OrgStructure OS
                WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS USL_TOWN_HOSP,
            IFNULL(IFNULL((SELECT `value` FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdTfoms51Purpose}'
             LIMIT 1), rbService.note),EventType.regionalCode) as SLUCH_PURPOSE,
            IFNULL(IFNULL((SELECT `value` FROM EventType_Identification ETI
             WHERE ETI.master_id = EventType.id
               AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdTfoms51Purpose}'
             LIMIT 1), rbService.note),EventType.regionalCode) as USL_PURPOSE,
            Person.SNILS AS USL_SNILS_DOC,
            (SELECT value FROM rbService_Identification RSI WHERE RSI.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = IFNULL(rbService.id, ActionType.nomenclativeService_id)
                  AND SId.system_id IN (SELECT id FROM rbAccountingSystem
                                        WHERE code = 'tfoms51.SERV3_METOD')
                  AND ((SId.checkDate = '2020-12-31' AND Action.endDate <= '2020-12-31') OR
                       (SId.checkDate = '2021-01-01' AND (
                        Action.endDate >= '2021-01-01' OR Action.endDate IS NULL)) OR
                       SId.checkDate IS NULL)
                  AND SId.deleted = 0)) AS USL_SERV_METOD,
            rbSpeciality.regionalCode AS SLUCH_PROFIL,
            IFNULL((SELECT rSI.value FROM rbSpeciality_Identification rSI
             WHERE rSI.master_id = Person.speciality_id
               AND rSI.deleted = 0
               AND rSI.system_id IN (SELECT id FROM rbAccountingSystem
                                    WHERE code = "tfoms51.V021")
             LIMIT 1), rbSpeciality.federalCode) AS SLUCH_PRVS,
            (CASE
             WHEN rbMedicalAidType.code = 6 -- амбулатория
                THEN IFNULL((SELECT `value` FROM EventType_Identification ETI
                       WHERE ETI.master_id = Event.eventType_id
                         AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
                         AND ETI.deleted = 0
                         AND ETI.system_id = '{sysIdTfoms51Purpose}'
                       LIMIT 1), rbService.note)
             WHEN rbMedicalAidType.code = 9 -- стоматология
                THEN (SELECT `value` FROM EventType_Identification ETI
                       WHERE ETI.master_id = Event.eventType_id
                         AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
                         AND ETI.deleted = 0
                         AND ETI.system_id = '{sysIdTfoms51Purpose}'
                       LIMIT 1)
             END) AS SLUCH_P_CEL,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS SLUCH_DET,
            rbEventTypePurpose.regionalCode AS SLUCH_USL_OK,
            Event.MES_id AS mesId""".format(
                payerId=self.wizard().info['payerId'],
                payerInfis=forceString(self.db.translate(
                    'Organisation', 'id', params['payerId'], 'infisCode')),
                sysIdTfoms51F002=sysIdTfoms51F002,
                sysIdTfoms51F003=self._getAccSysIdByUrn(u'urn:tfoms51:F003'),
                sysIdIdsp=self._getAccSysId('IDSP'),
                sysIdIdspPos=self._getAccSysId('IDSP_POS'),
                accOrgStructureId=params['accOrgStructureId'],
                lpuCode=params['lpuInfisCode'] if params[
                    'lpuInfisCode'] else params['lpuCode'],
                sysIdTfoms51Purpose=self._getAccSysId('tfoms51.PURPOSE'),
                sysIdPayMode=self._getAccSysId('PAY_MODE'),
                sysIdOid635=sysIdOid635)
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
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('1', '2'))
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDispanser ON Diagnosis.dispanser_id = rbDispanser.id
            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis AS DS9 ON DS9.id = AccDiagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDispanser AS DS9Dispanser ON DS9.dispanser_id = DS9Dispanser.id
            LEFT JOIN rbDiseaseCharacter AS AccCharacter ON AccDiagnostic.character_id = AccCharacter.id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
            LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            LEFT JOIN rbService ON rbService.id = Account_Item.service_id
            LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
                WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Event.client_id, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN rbDiseaseCharacter ON Diagnostic.character_id = rbDiseaseCharacter.id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN Visit ON Visit.id = (
                SELECT MAX(id)
                FROM Visit
                WHERE Visit.event_id = Account_Item.event_id
            )
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN Account_Item AS ExposedAccountItem ON
                ExposedAccountItem.reexposeItem_id = Account_Item.id
            LEFT JOIN mes.MES_visit ON mes.MES_visit.id = (
                SELECT MAX(id)
                FROM mes.MES_visit
                WHERE mes.MES_visit.serviceCode = rbService.code
                    AND mes.MES_visit.master_id = mes.MES.id
                    AND mes.MES_visit.deleted = 0
            )
            LEFT JOIN Action ON Account_Item.action_id = Action.id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
            LEFT JOIN rbSpeciality AS ActionSpeciality ON ActionPerson.speciality_id = ActionSpeciality.id
            LEFT JOIN rbSocStatusType ON rbSocStatusType.id = (
                SELECT MAX(rSST.id)
                FROM ClientSocStatus CSS
                LEFT JOIN rbSocStatusType rSST ON rSST.id = CSS.socStatusType_id
                WHERE CSS.client_id = Client.id AND CSS.deleted = 0
                  AND (CSS.begDate IS NULL OR CSS.begDate >= Event.setDate)
                  AND (CSS.endDate IS NULL OR CSS.endDate <= Event.execDate)
                  AND rSST.regionalCode IS NOT NULL
                  AND rSST.regionalCode != ''
                LIMIT 1
            )
            LEFT JOIN Event AS NextEvent ON NextEvent.prevEvent_id = Event.id
            LEFT JOIN Event AS LastEvent ON LastEvent.id = getLastEventId(Event.id)
            LEFT JOIN ClientAttach ON
                ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
            LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
            LEFT JOIN Organisation AS Relegate ON Event.relegateOrg_id = Relegate.id
            LEFT JOIN Person AS RelegatePerson ON RelegatePerson.id = Event.relegatePerson_id
            LEFT JOIN rbSpeciality AS RelegatePersonSpeciality ON
                RelegatePerson.speciality_id = RelegatePersonSpeciality.id
            LEFT JOIN rbVisitType ON Visit.visitType_id = rbVisitType.id"""
        where="""Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL
                     AND rbPayRefuseType.rerun != 0))
            AND {0}""".format(
                self.tableAccountItem['id'].inlist(self.idList))
        orderBy = u'Event.client_id, LastEvent.id, Event.id'

        return (select, tables, where, orderBy)


    def _visitList(self, params):
        u"""Формирует запрос о визитах события по его идентификатору"""

        stmt = u"""SELECT '{lpuCode}' AS USL_LPU,
            PersonOrgStructure.id AS USL_LPU_1,
            Visit.date AS USL_DATE_IN,
            Visit.date AS USL_DATE_OUT,
            0 AS USL_P_OTK,
            IF(rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL,
                MES_visit.altAdditionalServiceCode,
                    IF(rbService.infis IS NULL OR rbService.infis = '',
                        rbService.code, rbService.infis)) AS USL_CODE_USL,
            (SELECT price FROM Account_Item AI
             WHERE AI.visit_id = Visit.id AND AI.deleted = 0
             LIMIT 1) AS USL_TARIF,
            (SELECT IF(rbMesSpecification.level = '2', AI.sum, AI.price)
             FROM Account_Item AI
             WHERE AI.visit_id = Visit.id AND AI.deleted = 0
             LIMIT 1) AS USL_SUMV_USL,
            (SELECT rSI.value FROM rbSpeciality_Identification rSI
             WHERE rSI.master_id = Person.speciality_id
               AND rSI.deleted = 0
               AND rSI.system_id IN (SELECT id FROM rbAccountingSystem
                                    WHERE code = "tfoms51.V021")
             LIMIT 1) AS USL_PRVS,
            Person.regionalCode AS USL_CODE_MD,
            Event.id AS eventId,
            (SELECT tfomsCode FROM OrgStructure OS
                WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS USL_TOWN_HOSP,
            Relegate.infisCode AS relegateOrgCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            rbVisitType.regionalCode AS visitTypeRegionalCode,
            Person.SNILS AS USL_SNILS_DOC,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = ExecPerson.orgStructure_id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
            ) AS SLUCH_ADDR_CODE,
            (SELECT infisCode FROM OrgStructure OS
             WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS SLUCH_SUB_HOSP,
            rbMedicalAidProfile.regionalCode AS USL_PROFIL,
            (SELECT SUBSTR(Diagnosis.MKB,1,5) FROM Diagnosis
             LEFT JOIN Diagnostic ON Diagnosis.id = Diagnostic.diagnosis_id
             WHERE Diagnosis.deleted = 0
               AND Diagnostic.id = (
                   SELECT MAX(dc.id)
                   FROM Diagnostic dc
                   WHERE dc.event_id = Visit.event_id
                     AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType
                                                 WHERE code = '1')
                     AND dc.deleted = 0)) AS USL_DS,
            1 AS USL_KOL_USL,
            (SELECT `value` FROM EventType_Identification ETI
             WHERE ETI.master_id = Event.eventType_id
               AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdTfoms51Purpose}'
             LIMIT 1) as USL_PURPOSE,
            1 AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.SNILS AS MR_USL_N_CODE_MD,
            IFNULL((SELECT rSI.value FROM rbService_Identification rSI
             WHERE rSI.master_id = rbService.id
               AND rSI.deleted = 0
               AND rSI.system_id IN (SELECT MAX(id) FROM rbAccountingSystem
                                    WHERE urn = "urn:tfoms51:V001")
              LIMIT 1), rbService.infis) AS USL_VID_VME,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            rbMesSpecification.level = '2' AS isMesComplete
        FROM Visit
        LEFT JOIN Person ON Visit.person_id = Person.id
        LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
        LEFT JOIN Event ON Visit.event_id = Event.id
        LEFT JOIN Person AS ExecPerson ON ExecPerson.id = Event.execPerson_id
        LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
        LEFT JOIN mes.MES_visit ON mes.MES_visit.id = (
            SELECT MAX(id)
            FROM mes.MES_visit
            WHERE mes.MES_visit.serviceCode = rbService.code
                AND mes.MES_visit.master_id = mes.MES.id
                AND mes.MES_visit.deleted = 0
        )
        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
        LEFT JOIN Organisation AS Relegate ON Event.relegateOrg_id = Relegate.id
        LEFT JOIN ClientAttach ON
            ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
        LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
        LEFT JOIN Person AS RelegatePerson ON RelegatePerson.id = Event.relegatePerson_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = IFNULL(
            rbService_Profile.medicalAidProfile_id, rbService.medicalAidProfile_id)
        LEFT JOIN Client ON Event.client_id = Client.id
        WHERE Visit.event_id IN (
            SELECT event_id FROM Account_Item
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE Account_Item.reexposeItem_id IS NULL
              AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL
                     AND rbPayRefuseType.rerun != 0))
              AND {idList})
          AND Visit.deleted = '0'
          AND rbVisitType.code != 'ВУ'
        ORDER BY Visit.event_id, Visit.id
        """.format(lpuCode=params['lpuCode'],
                   accOrgStructureId=params['accOrgStructureId'],
                   sysIdTfoms51Purpose=self._getAccSysId('tfoms51.PURPOSE'),
                   idList=self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        result = {}
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result.setdefault(eventId, []).append(record)
        return result


    def _actionsByEvent(self, params, exportIncomplete=False):
        incompleteStmt = (u' AND (Action.status=6 OR (Action.status=2 AND '
            u'(Action.endDate NOT BETWEEN Event.setDate AND '
            u'Event.execDate)))') if exportIncomplete else (
            u' AND (Action.endDate BETWEEN Event.setDate AND Event.execDate)' )
        stmt = u"""SELECT '{lpuInfisCode}' AS USL_LPU,
            ExecPersonOrgStructure.id AS USL_LPU_1,
            IF(Action.status = 6, Event.setDate,
                IF(Action.status = 2 OR Action.begDate IS NULL,
                    Action.endDate, Action.begDate)) AS USL_DATE_IN,
            IF(Action.status = 6, Event.setDate,
                IFNULL(Action.endDate, Action.begDate)) AS USL_DATE_OUT,
            IF(Action.status = 2, 0, 1) AS USL_P_OTK,
            Event.setDate AS eventSetDate,
            rbMesSpecification.level AS mesSpecLevel,
            MES_visit.altAdditionalServiceCode AS altAdditionalServiceCode,
            rbService.infis AS USL_CODE_USL,
            1 AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.SNILS AS MR_USL_N_CODE_MD,
            Action.event_id AS eventId,
            Action.org_id AS org_id,
            (SELECT tfomsCode FROM OrgStructure OS
                WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS USL_TOWN_HOSP,
            Relegate.infisCode AS relegateOrgCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            rbVisitType.regionalCode AS visitTypeRegionalCode,
            Person.SNILS AS USL_SNILS_DOC,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = ExecPerson.orgStructure_id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
             LIMIT 1
            ) AS SLUCH_ADDR_CODE,
            (SELECT infisCode FROM OrgStructure OS
             WHERE OS.id = IFNULL(Person.orgStructure_id, '{accOrgStructureId}')
             LIMIT 1) AS SLUCH_SUB_HOSP,
            (SELECT value FROM rbService_Identification RSI WHERE RSI.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                  AND SId.system_id IN (SELECT id FROM rbAccountingSystem
                                        WHERE code = 'tfoms51.SERV3_METOD')
                  AND ((SId.checkDate = '2020-12-31' AND Action.endDate <= '2020-12-31') OR
                       (SId.checkDate = '2021-01-01' AND (
                        Action.endDate >= '2021-01-01' OR Action.endDate IS NULL)) OR
                       SId.checkDate IS NULL)
                  AND SId.deleted = 0)) AS USL_SERV_METOD,
            ExecPersonSpeciality.regionalCode AS SLUCH_PROFIL,
            rbMedicalAidProfile.regionalCode AS USL_PROFIL,
            (SELECT SUBSTR(Diagnosis.MKB,1,5) FROM Diagnosis
             LEFT JOIN Diagnostic ON Diagnosis.id = Diagnostic.diagnosis_id
             WHERE Diagnosis.deleted = 0
               AND Diagnostic.id = (
                   SELECT MAX(dc.id)
                   FROM Diagnostic dc
                   WHERE dc.event_id = Visit.event_id
                     AND dc.diagnosisType_id IN (SELECT MAX(id) FROM rbDiagnosisType
                                                 WHERE code = '1')
                     AND dc.deleted = 0)) AS USL_DS,
            Action.amount AS USL_KOL_USL,
            (SELECT `value` FROM EventType_Identification ETI
             WHERE ETI.master_id = Event.eventType_id
               AND (ETI.checkDate <= Event.execDate OR ETI.checkDate IS NULL)
               AND ETI.deleted = 0
               AND ETI.system_id = '{sysIdTfoms51Purpose}'
             LIMIT 1) as USL_PURPOSE,
            (SELECT AI.price FROM Account_Item AI
             WHERE AI.action_id = Action.id LIMIT 1) AS USL_TARIF,
            (SELECT AI.sum FROM Account_Item AI
             WHERE AI.action_id = Action.id LIMIT 1) AS USL_SUMV_USL,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            IFNULL((SELECT rSI.value FROM rbService_Identification rSI
             WHERE rSI.master_id = rbService.id
               AND rSI.deleted = 0
               AND rSI.system_id IN (SELECT MAX(id) FROM rbAccountingSystem
                                    WHERE urn = "urn:tfoms51:V001")
              LIMIT 1), rbService.infis) AS USL_VID_VME
        FROM Action
        LEFT JOIN Event ON Action.event_id = Event.id
        LEFT JOIN Person ON Person.id = Action.person_id
        LEFT JOIN Person AS ExecPerson ON ExecPerson.id = Event.execPerson_id
        LEFT JOIN OrgStructure AS ExecPersonOrgStructure
            ON ExecPerson.orgStructure_id = ExecPersonOrgStructure.id
        LEFT JOIN Organisation ON Organisation.id = IFNULL(Action.org_id, Person.org_id)
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbSpeciality AS ExecPersonSpeciality
            ON ExecPerson.speciality_id = ExecPersonSpeciality.id
        LEFT JOIN ActionType_Service ON ActionType_Service.master_id = Action.actionType_id
        LEFT JOIN rbService ON rbService.id = ActionType_Service.service_id
        LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
        LEFT JOIN mes.MES_visit ON mes.MES_visit.id = (
            SELECT MAX(id)
            FROM mes.MES_visit
            WHERE mes.MES_visit.serviceCode = rbService.code
                AND mes.MES_visit.master_id = mes.MES.id
                AND mes.MES_visit.deleted = 0
        )
        LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
        LEFT JOIN Organisation AS Relegate ON Event.relegateOrg_id = Relegate.id
        LEFT JOIN ClientAttach ON
            ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
        LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
        LEFT JOIN Visit ON Visit.id = (
            SELECT MAX(id)
            FROM Visit
            WHERE Visit.event_id = Action.event_id
        )
        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
        LEFT JOIN Person AS RelegatePerson ON RelegatePerson.id = Event.relegatePerson_id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = IFNULL(
            rbService_Profile.medicalAidProfile_id, rbService.medicalAidProfile_id)
        LEFT JOIN Client ON Event.client_id = Client.id
        WHERE Action.event_id IN (
                SELECT event_id FROM Account_Item
                WHERE {idList})
          AND Action.deleted = 0
          AND Action.status != 3
          AND ActionType_Service.id IS NOT NULL {incomplete}
        ORDER BY Action.event_id, Action.id
        """.format(
            idList=self.tableAccountItem['id'].inlist(self.idList),
            sysIdTfoms51Purpose=self._getAccSysId('tfoms51.PURPOSE'),
            lpuInfisCode=params['lpuInfisCode'],
            accOrgStructureId=params['accOrgStructureId'],
            incomplete=incompleteStmt)

        query = self._parent.db.query(stmt)
        result = {}
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result.setdefault(eventId, []).append(record)
        return result


    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = {
            'isReexposed': '1' if self.chkReexposed.isChecked() else '0',
            'contractFinanceType': getIntContractAttribute(
                self.wizard().accountId, u'VID_FIN')
        }
        lpuId = QtGui.qApp.currentOrgId()
        sysIdTfoms51F003 = self._getAccSysIdByUrn(u'urn:tfoms51:F003')
        params['lpuId'] = lpuId
        params['sysIdTfoms51F003'] = sysIdTfoms51F003
        params['sysIdTfoms51F003DEP'] = self._getAccSysIdByUrn(
            u'urn:tfoms51:F003_DEP')
        params['lpuCode'] = self.getOrgInfisCode(lpuId)
        params['lpuInfisCode'] = self._getOrgIdentification(
            lpuId, sysIdTfoms51F003)
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            sysIdTfoms51F002 = self._getAccSysIdByUrn(u'urn:tfoms51:F002')
            params['payerCode'] = self._getOrgIdentification(
                params['payerId'], sysIdTfoms51F002)
            if not params['payerCode']:
                sysIdOid635 = self._getAccSysIdByUrn(
                    u'urn:oid:1.2.643.5.1.13.2.1.1.635')
                params['payerCode'] = self._getOrgIdentification(
                    params['payerId'], sysIdOid635)
            if not params['payerCode']:
                params['payerCode'] = forceString(self.db.translate(
                    'Organisation', 'id', params['payerId'], 'infisCode'))
            params['eventCount'] = self.getEventCount()
            params['completeEventCount'] = self.getCompleteEventCount()
            params['completeEventSum'] = self.getCompleteEventSum()
            params['SL_COUNT'] = params['accNumber']
            params['mapEventIdToSum'] = self.getEventSum()
            params['mapEventIdToPrice'] = self.getEventPrice()
            params['serviceCount'] = dict(self._serviceCountByEvent())
            params['visitList'] = self._visitList(params)
            params['directions'] = self._directionsDict(params)
            params['actions'] = self._actionsByEvent(params)
            params['incompleteActions'] = self._actionsByEvent(params, True)

            registryType = self.cmbRegistryType.currentIndex()
            params['NSCHET'] = self.nschet(registryType, params)
            self._parent.note = u'[NSCHET:%s]' % params['NSCHET']

        params['rowNumber'] = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))
        params['invoice'] = {}
        params['clients'] = set()
        params['services'] = {}

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        regFile = QFile(self._parent.getRegistryFullXmlFileName())
        regFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, registryWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        registryWriter.setDevice(regFile)
        CAbstractExportPage1Xml.exportInt(self)


    def getEventPrice(self):
        u"""Возвращает общую цену услуг за событие"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.price) AS totalPrice
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
            _sum = forceDouble(record.value(1))
            result[eventId] = _sum

        return result

    def _directionsDict(self, params):
        u"""Генератор данных по назначениям для каждого события. Выгружаем
        столько блоков, сколько в событии есть назначений — действий
        с пл.кодами «%Direction», относящихся к классу диагностика
        (ActionType.class = 1)"""
        stmt = """SELECT Action.event_id,
            CASE
                WHEN ActionType.flatCode = 'consultationDirection'
                 AND Action.org_id IS NULL THEN 1
                WHEN ActionType.flatCode = 'consultationDirection'
                 AND Action.org_id IS NOT NULL
                 AND Action.org_id != '{lpuId}' THEN 2
                WHEN ActionType.flatCode = 'inspectionDirection' THEN 3
                ELSE ''
            END AS NAZ_NAZ_R,
            IF(ActionType.flatCode = 'inspectionDirection',
               DiagMethod.value, '') AS NAZ_NAZ_V,
            Person.SNILS AS NAZ_NAZ_IDDOKT,
            IF(ActionType.flatCode = 'inspectionDirection'
               OR (ActionType.flatCode = 'consultationDirection'
                   AND Action.org_id IS NOT NULL
                   AND Action.org_id != '{lpuId}'),
               Action.endDate, '') AS NAZ_NAPR_DATE,
            (SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = IFNULL(Action.org_id, '{lpuId}')
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms51F003}'
             LIMIT 1) AS NAZ_NAPR_MO
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFt JOIN Person ON Action.person_id = Person.id
        LEFT JOIN ActionProperty_Integer AS DiagMethod ON DiagMethod.id = (
            SELECT API.id
            FROM ActionProperty AS AP
            INNER JOIN ActionPropertyType AS APT ON AP.type_id = APT.id
            INNER JOIN ActionProperty_Integer AS API ON API.id = AP.id
            WHERE AP.deleted = 0 AND APT.`name` = 'NAZ_V' AND APT.actionType_id = ActionType.id
            LIMIT 0, 1
        )
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {0}
          AND ActionType.class IN (1, 2, 3) AND ActionType.flatCode LIKE '%Direction'
        GROUP BY Account_Item.event_id, Action.id
        """.format(self.tableAccountItem['id'].inlist(self.idList),
                   lpuId=params['lpuId'],
                   sysIdTfoms51F003=params['sysIdTfoms51F003'])
        query = self.db.query(stmt)
        result = {}
        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result.setdefault(eventId, []).append(record2Dict(record))

        return result


    def getOrgStructureParentId(self, _id):
        u"""Возвращает идентификатор родительского подразделения"""
        result = self._orgStructureParentIdCache.get(_id,  -1)

        if result == -1:
            result = forceRef(self.db.translate(
                'OrgStructure', 'id', _id, 'parent_id'))
            self._orgStructureParentIdCache[_id] = result
        return result


    def _getOrgStructureIdentification(self, _id, sysId):
        key = (_id,  sysId)
        result = self._orgStructureIdentificationCache.get(key, -1)
        if result == -1:
            _tbl = self._tblOrgStructuteIdentification
            cond = [_tbl['master_id'].eq(_id), _tbl['system_id'].eq(sysId),
                    _tbl['deleted'].eq(0)]
            record = self._db.getRecordEx(_tbl, 'value', where=cond)
            result = forceString(record.value(0)) if record else ''
            self._orgStructureIdentificationCache[key] = result
        return result


    def getLpu1Code(self, _id, params, recursionStep=0):
        code = self._getOrgStructureIdentification(
            _id, params['sysIdTfoms51F003DEP'])
        if not code and recursionStep < 100:
            parentId = self._getOrgStructureParentId(_id)
            code = self.getLpu1Code(parentId, params, recursionStep + 1)
        return code

# ******************************************************************************

class CExportPage2(COrder79ExportPage2):
    u"""Вторая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, prefix)

    def saveExportResults(self):
        wizard = self.wizard()
        fileList = (wizard.getFullXmlFileName(),
                    wizard.getPersonalDataFullXmlFileName(),
                    wizard.getRegistryFullXmlFileName())
        zipFileName = wizard.getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class XmlStreamWriter(COrder79XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR')
    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2')
    completeEventFields1 = (('IDCASE', 'VIDPOM', 'LPU', 'VBR')
                           + completeEventDateFields +
                           ('P_OTK', 'RSLT_D', 'RSLT', 'ISHOD', 'OS_SLUCH'))
    completeEventFields2 = ('IDSP', 'SUMV')
    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields = (('SL_ID', 'LPU_1', 'NHISTORY')
                   +  eventDateFields +
                   ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N', 'DN_DATE', 'DS2_N',
                    'NAZ', 'ED_COL', 'TARIF', 'SUM_M'))
    directionFields = ('NAZ_N', 'NAZ_R', 'NAZ_IDDOKT', 'NAZ_V', 'NAPR_DATE',
                       'NAPD_MO', 'NAZ_PMP')

    eventSubGroup = {
        'DS2_N': {'fields': ('DS2', 'DS2_PR', 'PR_DS2_N')},
        'NAZ': {'fields': directionFields,
                'dateFields': ('NAPR_DATE',)}
    }
    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1')
                     + serviceDateFields +
                     ('P_OTK', 'CODE_USL', 'TARIF', 'SUMV_USL', 'MR_USL_N'))
    serviceSubGroup = {
        'MR_USL_N': {'fields': ('MR_N', 'PRVS', 'CODE_MD')},
    }
    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP',  'SUMV', 'DS2', 'IDSERV', 'DATE_IN',
                      'DATE_OUT', 'CODE_USL', 'TARIF', 'SUMV_USL', 'MR_N',
                      'PRVS', 'CODE_MD')

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params.get('settleDate', QDate())
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.2')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', forceString(params['completeEventCount']))
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '{0}'.format(params['accId']))
        self.writeTextElement('CODE_MO', params['lpuInfisCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', params['NSCHET'])
        self.writeTextElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeTextElement('PLAT', params['payerCode'])
        self.writeTextElement('SUMMAV', u'{0:.2f}'.format(params['accSum']))
        self.writeTextElement('DISP', self.dispanserType(params))
        self.writeEndElement() # SCHET

    def dispanserType(self, params):
        u"""Возвращает код типа ДД"""
        return getEventTypeDDCode(self._parent.db, params['accId'])

    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            # выгрузка незавершенных действий
            self.exportActions(params['lastEventId'], params, True)

        if params.get('lastEventId'):
            self.writeEndElement() # SL
            self.writeGroup('Z_SL', self.completeEventFields2,
                            params['lastRecord'],
                            closeGroup=True,
                            openGroup=False)
            self.writeEndElement() # ZAP

        self.writeEndElement() # ZL_LIST


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('lastClientId'):
            if params.get('lastClientId'):
                # выгрузка незавершенных действий
                self.exportActions(params['lastEventId'], params, True)
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                params['lastRecord'],
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(clientId))
            self.writeTextElement('PR_NOV', params['isReexposed'])
            self.writeClientInfo(record, params)

            params['lastClientId'] = clientId
            params['lastEventId'] = None
            params['lastComleteEventId'] = None

        self.writeCompleteEvent(record, params)
        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))

        if lastEventId == params.get('lastComleteEventId'):
            return

        if params['lastEventId']:
            self.writeGroup('Z_SL', self.completeEventFields2,
                            params['lastRecord'],
                            closeGroup=True, openGroup=False)
            self.writeEndElement()

        lastEventId = forceRef(record.value('lastEventId'))
        record.setValue('Z_SL_SUMV', toVariant(
            params['completeEventSum'].get(lastEventId)))

        self.writeGroup('Z_SL', self.completeEventFields1, record,
                        closeGroup=False,
                        dateFields=self.completeEventDateFields)
        params['lastComleteEventId'] = forceRef(record.value('lastEventId'))
        params['lastEventId'] = None
        params['lastRecord'] = record


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""

        eventId = forceRef(record.value('eventId'))
        params['USL_PAY_MODE'] = forceString(
                record.value('USL_PAY_MODE'))
        if eventId not in params.setdefault('visitsExported', set()):
            visitList = params['visitList'].get(eventId, [])
            for visit in visitList:
                params['USL_IDSERV'] += 1

                _id = forceRef(visit.value('USL_LPU_1'))
                visit.setValue('USL_LPU_1', toVariant(
                    self._parent.getLpu1Code(_id, params)))
                visit.setValue('MR_USL_N_CODE_MD', formatSNILS(
                    visit.value('MR_USL_N_CODE_MD')))
                _record = CExtendedRecord(visit, params, DEBUG)
                self.writeGroup('USL', self.serviceFields, _record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields)
            params['visitsExported'].add(eventId)
        if params['isMesComplete']:
            self.exportActions(eventId, params)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        local_params = {
            'SL_ED_COL': params['serviceCount'].get(eventId, 1)
        }

        params['isMesComplete'] = forceBool(record.value('isMesComplete'))

        if not params['isMesComplete']:
            record.setValue('SL_SUMV', toVariant(
                params['mapEventIdToSum'].get(eventId, '0')))
        record.setValue('SL_SUM_M', toVariant(
            params['mapEventIdToSum'].get(eventId, '0')))
        record.setValue('SL_TARIF', record.value('SL_SUM_M'))

        sumv = u'{0:.2f}'.format(forceDouble(record.value('SL_SUMV')))
        record.setValue('SL_SUMV', toVariant(sumv))

        mkb = forceString(record.value('DS2_N_DS2'))
        isOnkology = forceInt(record.value('SL_DS_ONK')) == 1

        if mkb[:1] == 'C' and isOnkology:
            record.setNull('DS2_N_DS2')

        if forceString(record.value('DS2_N_DS2')) == u'':
            record.setNull('DS2_N_PR_DS2_N')

        if forceString(record.value('SL_PR_D_N')) != '1' and forceString(record.value('SL_PR_D_N')) != '2':
            record.setNull('SL_DN_DATE')

        local_params.update(params)

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0

            if params['lastEventId']:
                # выгрузка незавершенных действий
                params['USL_PAY_MODE'] = forceString(
                    record.value('USL_PAY_MODE'))
                self.exportActions(eventId, params, True)
                self.writeEndElement() # SL

            directions = params.get('directions', {}).get(eventId, [])
            n = 0
            for i in directions:
                n += 1
                i['NAZ_NAZ_N'] = n
                i['NAZ_NAZ_IDDOKT'] = formatSNILS(i['NAZ_NAZ_IDDOKT'])
                if not isOnkology:
                    i.pop('NAZ_NAPR_DATE')
                    i.pop('NAZ_NAPR_MO')
                for field in XmlStreamWriter.directionFields:
                    field = 'NAZ_{0}'.format(field)
                    local_params.setdefault(field, []).append(i.get(field))

            _id = forceRef(record.value('SL_LPU_1'))
            record.setValue('SL_LPU_1', toVariant(
                self._parent.getLpu1Code(_id, params)))

            for field in 'DS2_N_DS2_', 'DS2_N_PR_DS2_N_', 'DS2_N_DS2_PR_':
                val = forceString(record.value(field))
                if val:
                    local_params[field[:-1]] = val.split(',')
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('SL', self.eventFields, _record,
                            self.eventSubGroup if directions else None,
                            closeGroup=False, dateFields=self.eventDateFields)
            params['lastEventId'] = eventId


    def exportActions(self, eventId, params, exportIncomplete=False):
        u"""Выгружает все действия по указанному событию"""

        if (eventId, exportIncomplete) not in params.setdefault('exportedEvents', set()):
            params['exportedEvents'].add((eventId, exportIncomplete))

            actions = params['incompleteActions' if exportIncomplete
                             else 'actions'].get(eventId, [])
            for record in actions:
                params['USL_IDSERV'] += 1
                if not exportIncomplete:
                    params['USL_TARIF'] = 0
                    params['USL_SUMV_USL'] = 0
                _id = forceRef(record.value('USL_LPU_1'))
                record.setValue('USL_LPU_1', toVariant(
                    self._parent.getLpu1Code(_id, params)))
                record.setValue('MR_USL_N_CODE_MD', formatSNILS(
                    record.value('MR_USL_N_CODE_MD')))
                _record = CExtendedRecord(record, params, DEBUG)
                self.writeGroup('USL', self.serviceFields, _record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields)


    def writeTextElement(self, elementName, value=None):
        u"""Если тег в списке обязательных, выгружаем его пустым"""
        if value or elementName in self.requiredFields:
            COrder79XmlStreamWriter.writeTextElement(self, elementName, value)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        isInsurerNameNeeded = not forceString(record.value('PACIENT_SMO'))
        if not isInsurerNameNeeded:
            record.setNull('PACIENT_SMO_OK')
            record.setNull('PACIENT_SMO_NAM')
            record.setNull('PACIENT_SMO_OGRN')
        _record = CExtendedRecord(record, params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)

# ******************************************************************************

class CRegistryWriter(COrder79XmlStreamWriter, CExportHelperMixin):
    eventDateFields = tuple()
    eventFields1 = ('SL_ID', 'COUNT', 'CODE_COUNT', 'CARD', 'WORK', 'MASTER',
                    'SUM')
    eventFields2 = ('PURPOSE', 'SNILS_DOC', 'ADDR_CODE', 'SUB_HOSP', 'PROFIL',
                    'P_CEL', 'PRVS', 'DS_PZ', 'USL_OK', 'DET')
    eventFields = eventFields1 + eventFields2
    sumFields = ('SUMV', 'VID_FIN', 'PAY_MODE')
    depAddFields = ('DATE_1', 'DATE_2', 'PVRS', 'PROFIL', 'DS1', 'IDDOKT')
    serviceDateFields = tuple()
    serviceFields = ('IDSERV', 'ID_USL', 'TOWN_HOSP', 'DIR_SUBLPU', 'DIR_TOWN',
                     'PURPOSE', 'REASON', 'DIRECT_SPEC', 'SERV_METOD',
                     'VID_FIN', 'PAY_MODE', 'AIM', 'SNILS_DOC', 'ADDR_CODE',
                     'SUB_HOSP', 'PROFIL', 'DS', 'KOL_USL', 'VID_VME', 'DET')
    eventRequiredFields = ('SL_ID', 'COUNT', 'MASTER', 'SUM', 'SNILS_DOC',
                           'ADDR_CODE', 'SUB_HOSP', 'PROFIL', 'P_CEL', 'PRVS')
    serviceRequiredFields = ('IDSERV', 'VID_FIN', 'SNILS_DOC', 'ADDR_CODE',
                             'SUB_HOSP', 'PROFIL', 'DS', 'KOL_USL', 'VID_VME',
                             'DET')
    eventSubGroup = {'SUM': {'fields': sumFields }}
    mapPCel = {'101':u'3.1', '102':u'2.2', '103':u'2.1', '104':u'2.5',
               '106':u'3.1', '107':u'2.3', '201':u'1.1', '301':u'3.0',
               '302':u'3.0', '401':u'1.0', '402':u'2.6', '403':u'2.6',
               '404':u'2.6', '405':u'2.6', '406':u'1.3', '407':u'2.6',
               '408':u'2.5', '409':u'1.3', '109':u'1.3', '501':u'2.2',
               '502':u'2.1', '303':u'2.6', '304':u'2.6', '601':u'1.3',
               '602':u'2.2', '504':u'3.1'}

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self._lastEventId = None
        self._serviceNumber = 0
        self._actionsExported = set()


    def handleEmptyRequiredField(self, field, prefix):
        self._parent.logError(u'Региональный файл, событие `{2}` услуга `{3}`: '
                              u'отсутствует обязательное поле `{0}.{1}`.'
                              .format(prefix, field, self._lastEventId,
                                      self._serviceNumber))

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
        self.__lastRecord = None
        self._serviceNumber = 0


    def writeFooter(self, params):
        if self._lastEventId:
            # выгрузка незавершенных действий
            self._exportActions(self._lastEventId, params, True)

            self.writeGroup('SLUCH', self.eventFields2,
                        self.__lastRecord,
                        dateFields=self.eventDateFields, closeGroup=False,
                        openGroup=False,
                        requiredFields=self.eventRequiredFields)
        COrder79XmlStreamWriter.writeFooter(self, params)


    def writeRecord(self, record, params):
        lastEventId = forceRef(record.value('eventId'))

        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
        params['eventId'] = lastEventId
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)
        params['isStomatology'] = medicalAidTypeCode == 9
        params['isEmergency'] = medicalAidTypeCode in (4, 5)
        record.setValue('SLUCH_SNILS_DOC', formatSNILS(
            record.value('SLUCH_SNILS_DOC')))

        if lastEventId != self._lastEventId:
            if self._lastEventId:
                # выгрузка незавершенных действий
                self._exportActions(self._lastEventId, params, True)

                self.writeGroup('SLUCH', self.eventFields2,
                            self.__lastRecord,
                            dateFields=self.eventDateFields, closeGroup=False,
                            openGroup=False,
                            requiredFields=self.eventRequiredFields)
                self.writeEndElement() # SLUCH

            self.writeEventInfo(record, params)
            self._lastEventId = lastEventId
            self._serviceNumber = 1

        if lastEventId not in self._actionsExported:
            self._actionsExported.add(lastEventId)
            self._exportVisits(lastEventId, params)
            if params['isMesComplete']:
                self._exportActions(lastEventId, params)


    def writeEventInfo(self, record, params):
        local_params = {
            'SLUCH_COUNT': params['accNumber'][-10:],
            'SLUCH_R_MP': '1' if params['isStomatology'] else '0',
            'SLUCH_MASTER': '',
            'SUM_VID_FIN': '1',
        }
        record.setValue('SLUCH_P_CEL', self.mapPCel.get(
            forceString(record.value('SLUCH_P_CEL'))))
        _record = CExtendedRecord(record, local_params, DEBUG)
        subGroup = (self.hospitalEventSubGroup if params['isHospital']
                    else self.eventSubGroup)
        self.__lastRecord = _record
        if not forceBool(record.value('isMesComplete')):
            record.setValue('SUM_SUMV', toVariant(
                params['mapEventIdToSum'].get(params['eventId'], 0)))
        self.writeGroup('SLUCH', self.eventFields1, _record, subGroup,
                            dateFields=self.eventDateFields, closeGroup=False,
                            requiredFields=self.eventRequiredFields)


    def writeService(self, record, params):
        local_params = {
            'USL_IDSERV': self._serviceNumber,
            'USL_VID_FIN': forceString(params['contractFinanceType']),
            'USL_PAY_MODE': params['USL_PAY_MODE'],
            'USL_REASON': 4
        }
        relegateOrgId = forceRef(record.value('relegateOrgId'))

        local_params['USL_DIRECT_LPU'] = forceString(record.value(
                    'relegateOrgCode' if relegateOrgId
                             else 'attachOrgInfisCode'))

        record.setValue('USL_SNILS_DOC', formatSNILS(
            record.value('USL_SNILS_DOC')))

        orgId = forceRef(record.value('org_id'))
        servDate = forceDate(record.value('USL_DATE_IN'))
        begDate = forceDate(record.value('Z_SL_DATE_Z_1'))
        endDate = forceDate(record.value('Z_SL_DATE_Z_2'))
        local_params['USL_AIM'] = '1' if ((orgId and orgId != params['lpuId'])
                                     or not ((servDate >= begDate)
                                             and (servDate <= endDate))
                                    ) else '0'
        local_params['USL_ADDR_CODE'] = forceString(record.value('SLUCH_ADDR_CODE'))
        local_params['USL_SUB_HOSP'] = forceString(record.value('SLUCH_SUB_HOSP'))

        record.setValue('MR_USL_N_CODE_MD', formatSNILS(
            record.value('MR_USL_N_CODE_MD')))
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('USL', self.serviceFields, _record, None,
                            dateFields=self.serviceDateFields,
                            requiredFields=self.serviceRequiredFields)
        self._serviceNumber += 1


    def _exportActions(self, eventId, params, exportIncomplete=False):
        actions = params['incompleteActions' if exportIncomplete
                         else 'actions'].get(eventId, [])
        for record in actions:
            self.writeService(record, params)


    def _exportVisits(self, eventId, params):
        visits = params['visitList'].get(eventId, [])
        for record in visits:
            self.writeService(record, params)

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51HealthExamination,
    #accNum=u'ДВН14-100/ДВН2эт',
                      configFileName='75_18_s11.ini',
                      #eventIdList=[495456]
                      accNum=u'ДВН14-131/ДВН1эт'
                      )
