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

u"""Д.ФМО Информационное взаимодействие между Федеральным фондом обязательного
медицинского страхования (далее – ФОМС) имедицинскими организациями, функции и
полномочия учредителей в отношении которых осуществляют Правительство Российской
Федерации или федеральные органы исполнительной власти (далее - ФМО), при
направления информации об оказании медицинской помощи, финансовое обеспечение
которой осуществляется в соответствии с пунктом 11 статьи 5 Федерального закона
от 29 ноября 2010 г. № 326-ФЗ «Об обязательном медицинском страховании в
Российской Федерации». Мурманск"""

import json
import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile #, QDate
from library.Utils import (forceDouble, forceInt, forceRef, forceString,
                           forceBool, toVariant)

from Exchange.Export import CAbstractExportPage1Xml
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Order79Export import (
    COrder79ExportWizard, COrder79ExportPage1, COrder79ExportPage2,
    COrder79XmlStreamWriter)
from Exchange.Utils import compressFileInZip#, tbl

from Exchange.Ui_ExportPage1 import Ui_ExportPage1

DEBUG = False

def exportR51FMO(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта в ОМС Мурманской области Д.ФМО"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Мурманска'
        prefix = 'R51FMO'
        COrder79ExportWizard.__init__(self, title, prefix, CExportPage1,
                                      CExportPage2, parent)

        self.__xmlBaseFileName = None
        self.__xmlFileName = None


    def getXmlFileName(self):
        u"""Имя файла реестра"""
        if not self.__xmlFileName:
            sysIdTfoms51F003 = self.page(0)._getAccSysIdByUrn(
                u'urn:tfoms51:F003')
            currentOrgId = QtGui.qApp.currentOrgId()
            lpuCode = self.page(0)._getOrgIdentification(
                currentOrgId, sysIdTfoms51F003)
            settleDate = self.info['settleDate']
            self.__xmlFileName = u'{year:04}_{month:02}_{lpuCode}_1000.xml'.format(
                year=settleDate.year(),
                month=settleDate.month(),
                lpuCode=lpuCode
            )
        return self.__xmlFileName


    def getFullXmlFileName(self):
        u"""Путь к файлу реестра"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return  '{0}zip'.format(self.getXmlFileName()[:-3])

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        xmlWriter = XmlStreamWriter(self)
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.cmbRegistryType.setVisible(False)
        self.lblRegistryType.setVisible(False)
        self.edtPacketNumber.setVisible(False)
        self.lblPacketNumber.setVisible(False)

        self._recNum = 1


    def prepareStmt(self, params):
        queryParams = {
            'sysIdTfoms51V027': self._getAccSysIdByUrn('urn:tfoms51:V027'),
            'sysIdAdrGar': self._getAccSysIdByUrn('urn:gisoms:ADR_GAR'),
            'sysIdAdrName': self._getAccSysIdByUrn('urn:gisoms:ADR_NAME'),
            'sysIdTfoms51F003': params['sysIdTfoms51F003'],
            'lpuCode': params['lpuCode'],
            'payerSmoCode': forceString(self._db.translate(
                'Organisation', 'id', params['payerId'], 'smoCode')),
            'sysIdTfoms51F002': self._getAccSysIdByUrn('urn:tfoms51:F002'),
            'urn635': self._getAccSysIdByUrn('oid:1.2.643.5.1.13.2.1.1.635')
        }

        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            rbMedicalAidType.code AS medicalAidTypeCode,

            ClientPolicy.number AS PACIENT_ENP,
            IF(rbPolicyKind.regionalCode = 1,
               ClientPolicy.serial, '') AS PACIENT_SNPOLIS,
            Insurer.OKATO AS PACIENT_SMO_OK,
            IFNULL((SELECT value FROM OrgStructure_Identification
              WHERE master_id = Event.relegateOrg_id
                AND deleted = 0
                AND system_id IN ('{sysIdTfoms51F002}', '{urn635}')
             LIMIT 1),'{payerSmoCode}') AS PACIENT_SMO,
            Client.sex AS PACIENT_W,
            Client.birthDate AS PACIENT_DR,
            0 AS PACIENT_NOVOR, -- FIXME:
            Client.lastName AS PACIENT_FAM,
            Client.firstName AS PACIENT_IM,
            Client.patrName AS PACIENT_OT,
            '' AS PACIENT_TEL,
            '' AS PACIENT_MR,
            '' AS PACIENT_DOCTYPE,
            '' AS PACIENT_DOCSER,
            '' AS PACIENT_DOCNUM,
            '' AS PACIENT_DOCDATE,
            '' AS PACIENT_DOCORG,
            '' AS PACIENT_DOCSNILS,
            '' AS PACIENT_DOCOKATOG,
            '' AS PACIENT_DOCOKATOP,
            '' AS PACIENT_COMENTP,

            Event.id AS NPR_IDNPR,
            Event.id AS NPR_IDNPR_MIS,
            IFNULL(Event.srcDate, Event.setDate) AS NPR_TAL_D,
            (SELECT APS.value FROM Action A
             INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
             INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
             INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
             INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
             WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
               AND AP.deleted = 0
               AND AT.`flatCode` = 'received'
               AND APT.name = '№ направления на госпитализацию'
             ORDER BY A.begDate DESC LIMIT 0, 1) AS NPR_TAL_NUM,
            IFNULL((SELECT value FROM OrgStructure_Identification
              WHERE master_id = Event.relegateOrg_id
                AND deleted = 0 AND system_id = '{sysIdTfoms51F003}'),
             '{lpuCode}') AS NPR_NPR_MO,
            2 AS NPR_POVOD,
            SUBSTR(Diagnosis.MKB, 1, 5) AS NPR_DS1,
            SUBSTR(DS9.MKB, 1, 5) AS NPR_DS2,
            SUBSTR(DS3.MKB, 1, 5) AS NPR_DS3,
            rbEventTypePurpose.regionalCode AS NPR_USL_OK,
            rbMedicalAidKind.federalCode AS NPR_VIDPOM,
            Event.order AS NPR_FOR_POM,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               (SELECT APS.regionalCode
                FROM Action A
                INNER JOIN ActionType AS `AT` ON AT.id = A.actionType_id
                INNER JOIN Person AS AP ON A.person_id = AP.id
                INNER JOIN rbSpeciality AS APS ON AP.speciality_id = APS.id
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = IF(EventResult.code = 4, 'moving', 'leaved')
                ORDER BY A.begDate DESC LIMIT 1), '')  AS NPR_PROFIL,
            '6' AS NPR_RESH,
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
                ORDER BY A.begDate DESC LIMIT 0, 1)), '') AS NPR_PODR,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               IFNULL(LeavedOrgStruct.name,(
                SELECT OS.name FROM Action A
                INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
                INNER JOIN ActionProperty_OrgStructure AS APO ON APO.id = AP.id
                INNER JOIN OrgStructure AS OS ON OS.id = APO.value
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = 'moving'
                    AND APT.shortName = 'currentDep'
                ORDER BY A.begDate DESC LIMIT 1)), '') AS NPR_PODR_NAME,
            Event.setDate AS NPR_TAL_P,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               (SELECT rbHospitalBedProfile.tfomsCode
                FROM ActionProperty AP
                INNER JOIN ActionProperty_rbHospitalBedProfile AS HBP ON HBP.id = AP.id
                INNER JOIN rbHospitalBedProfile ON HBP.value = rbHospitalBedProfile.id
                WHERE AP.action_id = HospitalAction.id
                  AND AP.deleted = 0
                  LIMIT 1), '')  AS NPR_PROFIL_K,

            Event.id AS Z_SL_IDCASE,
            Event.order AS Z_SL_FOR_POM,
            IF(Event.id = getLastEventId(Event.id), '', 1) AS Z_SL_IDCASE_LINK,
            (SELECT value FROM Organisation_Identification
              WHERE master_id = Person.org_id
                AND deleted = 0
                AND system_id = '{sysIdAdrGar}') AS Z_SL_ADR_GAR,
            (SELECT value FROM Organisation_Identification
              WHERE master_id = Person.org_id
                AND deleted = 0
                AND system_id = '{sysIdAdrName}') AS Z_SL_ADR_NAME,
            rbEventTypePurpose.regionalCode AS Z_SL_USL_OK,
            rbMedicalAidKind.federalCode AS Z_SL_VIDPOM,
            IFNULL(NextEvent.setDate, Event.setDate) AS Z_SL_DATE_Z_1,
            IFNULL(LastEvent.execDate, Event.execDate) AS Z_SL_DATE_Z_2,
            '' AS Z_SL_KD_Z,
            EventResult.regionalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            IF(rbMesSpecification.level = 2, 0, 1) AS Z_SL_IS_PRERV,
            1 AS Z_SL_KOEF_D,

            Event.id AS SL_SL_ID,
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
                ORDER BY A.begDate DESC LIMIT 0, 1)), '') AS SL_PODR,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               IFNULL(LeavedOrgStruct.name,(
                SELECT OS.name FROM Action A
                INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
                INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
                INNER JOIN ActionProperty_OrgStructure AS APO ON APO.id = AP.id
                INNER JOIN OrgStructure AS OS ON OS.id = APO.value
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = 'moving'
                    AND APT.shortName = 'currentDep'
                ORDER BY A.begDate DESC LIMIT 1)), '') AS SL_PODR_NAME,
            IF(rbMedicalAidType.code IN (1,2,3,7),
                (SELECT APS.regionalCode
                FROM Action A
                INNER JOIN ActionType AS `AT` ON AT.id = A.actionType_id
                INNER JOIN Person AS AP ON A.person_id = AP.id
                INNER JOIN rbSpeciality AS APS ON AP.speciality_id = APS.id
                WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
                    AND AP.deleted = 0
                    AND AT.`flatCode` = IF(EventResult.code = 4, 'moving', 'leaved')
                ORDER BY A.begDate DESC LIMIT 1), '') AS SL_PROFIL,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               (SELECT rbHospitalBedProfile.tfomsCode
                FROM ActionProperty
                INNER JOIN ActionProperty_rbHospitalBedProfile AS HBP
                    ON HBP.id = ActionProperty.id
                INNER JOIN rbHospitalBedProfile
                    ON HBP.value = rbHospitalBedProfile.id
                WHERE action_id = HospitalAction.id
                  AND ActionProperty.deleted = 0
                  LIMIT 1), '') AS SL_PROFIL_K,
            IF(rbMedicalAidType.code IN (1,2,3,7),
               CONCAT('#', Event.externalId),
               Event.id) AS SL_NHISTORY,
            SUBSTR(Diagnosis.MKB, 1, 5) AS SL_DS_GR,
            SUBSTR(Diagnosis.MKB, 1, 5) AS SL_DS1,
            SUBSTR(DS9.MKB, 1, 5) AS SL_DS2,
            SUBSTR(DS3.MKB, 1, 5) AS SL_DS3,
            (SELECT DI.value FROM rbDiseaseCharacter_Identification DI
             WHERE DI.system_id = {sysIdTfoms51V027}
               AND DI.deleted = 0
               AND DI.master_id = Diagnosis.character_id
             LIMIT 1) AS SL_C_ZAB,
            Account_Item.price AS SL_TARIF,

            mes.MES.patientModel AS KSG_KPG_GR,
            YEAR((SELECT settleDate FROM Account
                  WHERE id = Account_Item.master_id)) AS KSG_KPG_VER_KSG,
            IFNULL(mes.MES_ksg.vk,1) AS KSG_KPG_KOEF_Z,
            (SELECT GROUP_CONCAT(AT.code)
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.flatCode = 'AddCriterion'
                WHERE A.event_id = Event.id AND A.deleted = 0
            )  AS critList,
            IFNULL(mes.MES_ksg.code, mes.MES.code) AS KSG_KPG_N_KSG,
            0 AS KSG_KPG_SL_K,
            0 AS KSG_KPG_IT_SL,

            '' AS CONS_PR_CONS,

            6 AS ONK_SL_DS1_T,
            6 AS ONK_USL_USL_TIP
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
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN Event AS NextEvent ON NextEvent.prevEvent_id = Event.id
            LEFT JOIN Event AS LastEvent ON LastEvent.id = getLastEventId(Event.id)
        """.format(**queryParams)
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

    def _operation(self, params):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            (SELECT SI.value FROM rbService_Identification SI
             WHERE SI.master_id = rbService.id
              AND SI.deleted = 0
              AND SI.system_id = '{sysIdTfoms51V001}') AS USL_VID_VME
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN Person ON Person.id = Action.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id
        LEFT JOIN rbPayRefuseType
            ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.serviceType = 4
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL
                AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id
        ORDER BY Account_Item.event_id, Account_Item.action_id
            """.format(idList=self.tableAccountItem['id'].inlist(self.idList),
                       sysIdTfoms51V001=self._getAccSysIdByUrn(
                        'urn:tfoms51:V001'))

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
        params['completeEventSum'] = self.getCompleteEventSum()
        params['eventSum'] = self.getEventSum()
        params['sysIdTfoms51F003'] = self._getAccSysIdByUrn(u'urn:tfoms51:F003')
        currentOrgId = QtGui.qApp.currentOrgId()
        params['currentOrgId'] = currentOrgId
        params['lpuCode'] = self._getOrgIdentification(
            currentOrgId, params['sysIdTfoms51F003'])
        params['completeEventBedDays'] = dict(self._getBedDaysByCompleteEvent())
        params['operation'] = dict(self._operation(params))
        self.setProcessParams(params)

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        xmlWriter = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        CAbstractExportPage1Xml.exportInt(self)

# ******************************************************************************

class CExportPage2(COrder79ExportPage2):
    u"""Вторая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, prefix)


    def saveExportResults(self):
        fileList = (self.wizard().getFullXmlFileName(), )
        zipFileName = self.wizard().getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class XmlStreamWriter(COrder79XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientDateFields = ('DR', )
    clientFields = ('ENP', 'SNPOLIS', 'SMO_OK','SMO', 'W', 'DR', 'NOVOR', 'FAM',
                    'IM', 'OT', 'TEL', 'MR', 'DOCTYPE', 'DOCSER', 'DOCNUM',
                    'DOCDATE', 'DOCORG', 'SNILS', 'OKATOG', 'OKATOP', 'COMENTP')
    clientRequiredFields = ('W', 'DR', 'NOVOR')

    directionDateFields = ('TAL_D', 'TAL_P')
    directionFields = ('IDNPR', 'IDNPR_MIS','TAL_D', 'TAL_NUM', 'NPR_MO',
                       'POVOD', 'DS1', 'DS2', 'DS3', 'USL_OK', 'VIDPOM',
                       'FOR_POM', 'PROFIL', 'RESH', 'PODR', 'PODR_NAME',
                       'PROFIL_K', 'TAL_P')
    directionRequiredFields = ('IDNPR', 'TAL_D', 'TAL_NUM',
                               'NPR_MO', 'POVOD', 'DS1', 'USL_OK', 'VIDPOM',
                               'FOR_POM', 'PROFIL')

    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2')
    completeEventFields1 = ('IDCASE', 'IDCASE_LINK', 'ADR_GAR', 'ADR_NAME',
                            'USL_OK', 'VIDPOM', 'FOR_POM', 'DATE_Z_1',
                            'DATE_Z_2', 'KD_Z', 'RSLT', 'ISHOD', 'IS_PRERV',
                            'KOEF_PRERV', 'KOEF_PRIV', 'KOEF_SPEC', 'SRED_NFZ',
                            'KOEF_D')
    completeEventFields2 = ('SUMV', )
    completeEventFields = completeEventFields1 + completeEventFields2
    completeEventRequiredFields = ('IDCASE', 'ADR_GAR', 'ADR_NAME',
                            'USL_OK', 'VIDPOM', 'FOR_POM', 'DATE_Z_1', )


    eventFields = ('SL_ID', 'PODR', 'PODR_NAME', 'PROFIL', 'PROFIL_K',
                   'NHISTORY', 'DS_GR', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'CONS',
                   'ONK_SL',  'KSG_KPG', 'TARIF')
    eventRequiredFields = ('SL_ID', 'PODR', 'PODR_NAME', 'PROFIL', 'PROFIL_K',
                   'NHISTORY', 'DS1')

    ksgFields = ('N_KSG', 'GR', 'VER_KSG', 'KOEF_Z', 'CRIT', 'SL_K', 'IT_SL',
                 'SL_KOEF')
    ksgReqiredFields = ('N_KSG', 'GR', 'VER_KSG', 'SL_K')
    ksgSubGroup = {
        'SL_KOEF' : {'fields': ('IDSL', 'Z_SL'),
                     'requiredFields': ('IDSL', 'Z_SL')}
    }

    eventSubGroup = {
        'KSG_KPG': {'fields': ksgFields,
                    'subGroup': ksgSubGroup,
                    'requiredFields': ksgReqiredFields},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS'),
                 'requiredFields': ('PR_CONS', ) },
        'ONK_SL': {}
    }

    serviceFields = ('IDSERV', 'VID_VME')
    serviceRequiredFields = ('IDSERV', 'VID_VME')

    onkSlFields = ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M')
    onkUslFields = ('USL_TIP', )

    onkSlSubGroup = {
        'ONK_USL': {'fields': ('USL_TIP', )},
    }
    eventOnkSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL',
                            'NAPR_USL'),
                 'dateFields': ('NAPR_DATE', )},
        'ONK_SL': {'fields': onkSlFields,
                   'subGroup': onkSlSubGroup},
    }
    eventOnkHospSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL',
                            'NAPR_USL'),
                 'dateFields': ('NAPR_DATE', )},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS')},
        'ONK_SL': {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                              'B_DIAG', 'B_PROT', 'SOD'),
                   'subGroup': onkSlSubGroup},
        'KSG_KPG': {'fields': ksgFields, 'subGroup': ksgSubGroup}
    }

    mapEventOrderToForPom = {1: 3, 2: 1, 3: 1, 4: 3, 5: 3,  6: 2}

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)
        self._coefficientCache = {}
        self.__eventId = None


    def handleEmptyRequiredField(self, field, prefix):
        self._parent.logError(
            u'Событие `{0}`: отсутствует обязательное поле {1}.{2}'
            .format(self.__eventId, prefix, field))


    def writeElement(self, elementName, value=None):
        self.writeTextElement(elementName, value)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""

        settleDate = params['settleDate']

        self.writeStartElement('ZL_LIST')
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '1.0')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME',
            self._parent.wizard().getXmlFileName()[:-4])
        self.writeTextElement('SD_Z', forceString(
            self._parent.getCompleteEventCount()))
        self.writeEndElement() # ZGLV

        self.writeStartElement('OTPR')
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', str(settleDate.year()))
        self.writeTextElement('MONTH', str(settleDate.month()))
        self.writeTextElement('DAY', str(settleDate.day()))
        self.writeEndElement() # OTPR

        self.writeStartElement('SIGNATURE')
        for field in ('CANONMETALG', 'SIGNMETALG', 'REFERENCE', 'KEYINFO',
                      'SIGN'):
            self.writeTextElement(field, '')
        self.writeEndElement() # SIGNATURE


    def writeRecord(self, record, params):
        clientId = forceRef(record.value('clientId'))
        lastEventId = forceRef(record.value('eventId'))
        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
        params['isDiagnostics'] = forceBool( # Выключаем диагностику для ДС.
            record.value('isDiagnostics')) and medicalAidTypeCode != 3
        params['eventId'] = lastEventId
        self.__eventId = lastEventId
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)
        params['isStomatology'] = medicalAidTypeCode == 9
        params['isEmergency'] = medicalAidTypeCode in (4, 5)
        params['isAmbulance'] = medicalAidTypeCode == 6

        record.setValue(
            'Z_SL_SUMV', params['completeEventSum'].get(lastEventId, 0))

        if (clientId != params.setdefault('lastClientId') or
                lastEventId != params.setdefault('lastComleteEventId') or
                params['isDiagnostics']):
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
            self.writeTextElement('TYPE', 'PRIL4')
            self.writeClientInfo(record, params)
            eventOrder = forceInt(record.value('eventOrder'))
            if self.mapEventOrderToForPom.get(eventOrder) != 1:
                self.writeDirectionInfo(record, params)

            if (params['isDiagnostics'] and
                    lastEventId != params.setdefault('lastComleteEventId')):
                params['diagnosticNumber'] = 1

            params['lastClientId'] = clientId
            params['lastEventId'] = None
            params['lastComleteEventId'] = None
            params['recNum'] += 1

        self.writeCompleteEvent(record, params)
        self.writeEventInfo(record, params)
        self.writeService(record, params)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        _record = CExtendedRecord(record, params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record,
                        dateFields=self.clientDateFields,
                        requiredFields=self.clientRequiredFields)


    def writeDirectionInfo(self, record, params):
        record.setValue('NPR_FOR_POM', toVariant(
            self.mapEventOrderToForPom.get(
                forceInt(record.value('NPR_FOR_POM')), '')))
        self.writeGroup('NPR', self.directionFields, record,
                        dateFields=self.directionDateFields,
                        requiredFields=self.directionRequiredFields)


    def writeCompleteEvent(self, record, params):
        u"""Пишет информацию о законченном случае, группа Z_SL"""
        lastEventId = forceRef(record.value('eventId'))

        if lastEventId == params.get('lastComleteEventId'):
            return

        if params['lastEventId']:
            self.writeEndElement()
            self.writeGroup(
                'Z_SL', self.completeEventFields2, params['lastRecord'],
                closeGroup=True, openGroup=False)

        record.setValue('Z_SL_FOR_POM', self.mapEventOrderToForPom.get(
            forceInt(record.value('Z_SL_FOR_POM')), ''))
        if params['isHospital']:
            record.setValue('Z_SL_KD_Z', params['completeEventBedDays'].get(
                lastEventId, ''))
        self.writeGroup('Z_SL', self.completeEventFields1, record,
                        closeGroup=False,
                        dateFields=self.completeEventDateFields)
        params['lastComleteEventId'] = forceRef(record.value('eventId'))
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
                    result.setdefault('SL_KOEF_Z_SL', []).append(
                        '%1.5f' % (val + 1))

        return result


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        if eventId == params.setdefault('lastEventId'):
            return

        params['eventProfileRegionalCode'] = forceInt(record.value(
            'eventProfileRegionalCode'))
        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))

        local_params = {
            'SL_SUM_M': params['eventSum'].get(eventId, 0.0),
#            'SL_DS_ONK': params['onkologyInfo'].get(
                #eventId, {}).get('SL_DS_ONK')
        }
        params['isHospital'] = medicalAidTypeCode in (1, 2, 3, 7)

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

                    if i['__all__'] > 1:
                        local_params['KSG_KPG_IT_SL'] = u'%.5f' %  i['__all__']

                if local_params.has_key('KSG_KPG_IT_SL'):
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

        self.writeGroup('SL', self.eventFields, _record,
                        subGroup=self.eventSubGroup,
                        closeGroup=False, dateFields=self.eventDateFields)
        params['lastEventId'] = eventId


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""

        if params['isDiagnostics']:
            params['USL_IDSERV'] = 1
            _record = CExtendedRecord(record, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record, None,
                            dateFields=self.serviceDateFields)
            return

        eventId = forceRef(record.value('eventId'))
        params['USL_LPU_1'] = forceString(record.value('SL_LPU_1'))


        if not params['isHospital'] or params.get('force'):
            if (forceString(record.value('KSG_KPG_N_KSG')) ==
                    forceString(record.value('USL_CODE_USL'))
                    and not params.get('isOnkservice')):
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
            self.writeGroup('USL', self.serviceFields, _record, None,
                            dateFields=self.serviceDateFields)

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
                params['USL_IDSERV'] += 1
                _record = CExtendedRecord(operation, params, DEBUG)
                self.writeGroup('USL', self.serviceFields, _record, None,
                            dateFields=self.serviceDateFields)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            self.writeEndElement() # SL
            self.writeEndElement() # Z_SL
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

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51FMO,
                      configFileName='75_38_s11.ini',
                      accNum=u'14_субвенция-246',
                      #eventIdList=[1623239]
                      )
