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

u"""Экспорт реестра  в формате XML. Республика Калмыкия, СМП"""

from library.Utils import forceString, forceRef, forceInt, toVariant

from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.ExportR08Hospital import (
    getXmlBaseFileName, CR08ExportPage2, CR08ExportPage1 as CExportPage1,
    CR08XmlStreamWriter as XmlStreamWriter,
    CR08PersonalDataWriter as PersonalDataWriter)
from Exchange.Order79Export import (COrder79ExportWizard,
                                    COrder79v3XmlStreamWriter)

DEBUG = False

def exportR08Emergency(widget, accountId, accountItemIdList, _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CR08ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CR08ExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Калмыкии"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии, СМП'
        prefix = 'R08Emergency'
        COrder79ExportWizard.__init__(self, title, prefix, CR08ExportPage1,
                                      CR08ExportPage2, parent)
        self.setWindowTitle(title)
        self.page1.setXmlWriter((R08XmlStreamWriter(self.page1),
                                 PersonalDataWriter(self.page1)))
        self.__xmlBaseFileName = None


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""
        result = self.__xmlBaseFileName

        if not result:
            result = getXmlBaseFileName(self.db, self.info,
                                        self.page1.edtPacketNumber.value(),
                                        addPostfix)
            self.__xmlBaseFileName = result

        return result


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return u'{0}.zip'.format(self.getXmlFileName()[:-4])


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return u'T{0}'.format(self._getXmlBaseFileName(addPostfix))


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'LT{0}'.format(self._getXmlBaseFileName(addPostfix))

# ******************************************************************************

class CR08ExportPage1(CExportPage1):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CExportPage1.__init__(self, parent, prefix)


    def prepareStmt(self, params):
        (_, _, where, orderBy) = CExportPage1.prepareStmt(
            self, params)
        select = u"""FirstEvent.id AS eventId,
            LastEvent.id AS lastEventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            MesService.infis AS mesServiceInfis,
            MesAction.begDate AS mesActionBegDate,
            MesAction.endDate AS mesActionEndDate,
            Account_Item.`sum` AS `sum`,
            Account_Item.amount,
            Account_Item.usedCoefficients,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.regionalCode = '1', ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            Insurer.miacCode AS PACIENT_SMO,
            IF(Insurer.miacCode IS NULL OR Insurer.miacCode = '',
                        Insurer.OGRN,'') AS PACIENT_SMO_OGRN,
            IF(Insurer.miacCode IS NULL OR Insurer.miacCode = '',
                        Insurer.OKATO,'') AS PACIENT_SMO_OK,
            IF((Insurer.miacCode IS NULL OR Insurer.miacCode = '')
                    AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                    Insurer.shortName, '') AS PACIENT_SMO_NAM,
            Client.birthWeight AS PACIENT_VNOV_D,
            0 AS PACIENT_NOVOR,

            Event.id AS Z_SL_IDCASE,
            rbMedicalAidType.regionalCode AS Z_SL_USL_OK,
            IFNULL(OrgStructure_Identification.value,
                rbMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            RelegateOrg.infisCode AS Z_SL_NPR_MO,
            PersonOrganisation.miacCode AS Z_SL_LPU,
            FirstEvent.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            rbMedicalAidUnit.federalCode AS Z_SL_IDSP,

            Account_Item.event_id AS SL_SL_ID,
            mes.MES.code AS SL_VID_HMP,
            rbService.infis AS SL_METOD_HMP,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL(EventType_Identification.value,
                    PersonOrgStructure.tfomsCode)) AS SL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS SL_DET,
            Event.srcDate AS SL_TAL_D,
            FirstEvent.srcNumber AS SL_TAL_NUM,
            ReceivedAction.plannedEndDate AS SL_TAL_P,
            FirstEvent.id AS SL_NHISTORY,
            IF(EventType.form = '110',
                FirstEvent.execDate, FirstEvent.setDate) AS SL_DATE_1,
            FirstEvent.execDate AS SL_DATE_2,
            DS0.MKB AS SL_DS0,
            Diagnosis.MKB AS SL_DS1,
            DS9.MKB AS SL_DS2,
            DS3.MKB AS SL_DS3,
            rbSpeciality.regionalCode AS SL_PRVS,
            mes.MES_ksg.code AS SL_CODE_MES1,
            Person.federalCode AS SL_IDDOKT,
            Account_Item.price AS SL_TARIF,
            IF((rbMedicalAidUnit.federalCode IN ('26', '27') AND rbEventProfile.regionalCode = '2')
                OR (rbMedicalAidUnit.federalCode IN ('31', '35') AND rbEventProfile.regionalCode = '5'),
                0, IF(rbEventProfile.regionalCode = '6', UetInfo.`sum`, Account_Item.`sum`)) AS SL_SUM_M,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                IF(rbEventProfile.regionalCode = '6', UetInfo.uet, Account_Item.amount)) AS SL_ED_COL,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.lastName) AS PERS_FAM,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            rbDocumentType.regionalCode AS PERS_DOCTYPE,
            IF(rbDocumentType.regionalCode = '3',
                REPLACE(TRIM(ClientDocument.serial),' ', '-'),
                REPLACE(TRIM(ClientDocument.serial),'-', ' ')) AS PERS_DOCSER,
            TRIM(ClientDocument.number) AS PERS_DOCNUM,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,

            rbEventProfile.regionalCode AS eventProfileRegionalCode,
            BedProfile.value AS bedProfileCode,
            DeliveredBy.value AS delivered
        """

        tables = u"""Account_Item
            LEFT JOIN Event AS FirstEvent ON FirstEvent.id  = Account_Item.event_id
            LEFT JOIN Event ON Event.id = getLastEventId(Account_Item.event_id)
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
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbEventProfile ON rbEventProfile.id = EventType.eventProfile_id
            LEFT JOIN (
                    SELECT A.id, A.event_id, SUM(A.amount) AS amount, COUNT(DISTINCT A.id) AS cnt
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
            LEFT JOIN EventType_Identification ON  EventType_Identification.master_id = EventType.id
                AND EventType_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'НеотлПом'
            )
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
                    AND AT.`flatCode` = 'leaved'
                    AND APT.`typeName` = 'OrgStructure'
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
            LEFT JOIN Action AS ReceivedAction ON
                ReceivedAction.id = (
                    SELECT MAX(A.id)
                    FROM Action A
                    WHERE A.event_id = Event.id AND
                              A.deleted = 0 AND
                              A.actionType_id = (
                                    SELECT AT.id
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='received'
                              )
                )
            LEFT JOIN Event AS LastEvent ON LastEvent.id  = getLastEventId(Event.id)
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN ActionProperty_rbHospitalBedProfile AS BedProfile
                ON BedProfile.id = (
                    SELECT MAX(HBP.id)
                    FROM ActionProperty
                    LEFT JOIN ActionProperty_rbHospitalBedProfile AS HBP
                        ON HBP.id = ActionProperty.id
                    WHERE action_id = HospitalAction.id
                )
        """
        return (select, tables, where, orderBy)

# ******************************************************************************

class R08XmlStreamWriter(XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    ticketFields = ('TAL_D', 'TAL_P')
    eventDateFields = XmlStreamWriter.eventDateFields + ticketFields
    eventFields = (('SL_ID', 'VID_HMP', 'METOD_HMP', 'LPU_1', 'PODR',
                    'PROFIL', 'PROFIL_K', 'DET')
                   + ('TAL_D', 'TAL_NUM', 'TAL_P') +
                   ('NHISTORY', )
                   +  XmlStreamWriter.eventDateFields +
                   ('DS0', 'DS1', 'DS2', 'DS3', 'RSLT', 'CODE_MES1',
                    'CODE_MES2', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL',
                    'TARIF', 'SUM_M'))

    def __init__(self, parent):
        XmlStreamWriter.__init__(self, parent)


    def writeService(self, record, params):
        pass


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))

        if eventId == params.setdefault('lastEventId'):
            return

        patrName = forceString(record.value('PERS_OT'))
        params['eventProfileRegionalCode'] = forceInt(record.value(
            'eventProfileRegionalCode'))
        params['idsp'] = forceInt(record.value('SL_IDSP'))
        eventOrder = forceInt(record.value('eventOrder'))

        local_params = {
            'SL_OS_SLUCH': '2' if (not patrName or
                                      patrName.upper() == u'НЕТ') else '',
            'SL_VERS_SPEC': 'V021',
            'SL_FOR_POM': self.mapEventOrderToForPom.get(
                eventOrder, ''),
        }
        params['isHospital'] = params['eventProfileRegionalCode'] in (1, 3)

        if params['isHospital']:
            local_params['SL_EXTR'] = (forceString(
                eventOrder) if eventOrder in (1, 2)  else '')
            local_params['SL_P_PER'] = self.mapEventOrderToPPer.get(
                eventOrder)

            if not local_params['SL_P_PER']:
                delivered = forceString(record.value('delivered')) == u'СМП'
                local_params['S_P_PER'] = '2' if delivered else '1'

            bedProfileCode = forceString(record.value('bedProfileCode'))
            if bedProfileCode:
                local_params['SL_PROFIL_K'] = (
                    self.getHospitalBedProfileTfomsCode(bedProfileCode))

        elif params['eventProfileRegionalCode'] == 6: #стоматология
            record.setValue('SL_TARIF', toVariant(
                self._parent.contractAttributeByType(u'ует')))

        idsp = params['idsp']
        if params['emergencyIncomplete'] and idsp == 31:
            record.setValue('SL_SUM_M', toVariant(0))

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        params['USL_IDSERV'] = 0

        if params['lastEventId']:
            self.writeEndElement() # SLUCH

        self.writeGroup('SL', self.eventFields, _record,
                        closeGroup=False, dateFields=self.eventDateFields)
        params['lastEventId'] = eventId


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))
        patrName = forceString(record.value('PERS_OT'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'

        local_params = {}
        local_params['Z_SL_SUMV']= params['completeEventSum'].get(lastEventId)
        local_params['Z_SL_FOR_POM'] = self.mapEventOrderToForPom.get(
                forceInt(record.value('eventOrder')), '')
        local_params['Z_SL_OS_SLUCH'] = ('2' if (noPatrName or (
                params['isJustBorn'] and not params['isAnyBirthDoc'])) else '')
        local_params.update(params['mapEventIdToKsgKpg'].get(lastEventId))
        _record = CExtendedRecord(record, local_params, DEBUG)
        COrder79v3XmlStreamWriter.writeCompleteEvent(self, _record, params)

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR08Emergency, 234)
