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
u"""Экспорт счетов для Пскова, ДД (А3)"""

import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QIODevice, QTextStream, QDate
from library.Utils import (forceRef, forceString, forceDouble, forceBool,
                           toVariant, formatSNILS, formatName, formatDate,
                           formatSex, forceInt, forceDate)

from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import CAbstractExportPage1Xml
from Exchange.ExportR60NativeAmbulance import PersonalDataWriter
from Exchange.Order79Export import (COrder79ExportWizard, COrder79ExportPage1,
                                    COrder79ExportPage2,
                                    COrder79XmlStreamWriter)
from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1
from Exchange.Utils import compressFileInZip, tbl

DEBUG = False


def exportR60HealthExamination(widget, accountId, accountItemIdList,
                               accountIdList):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setAccountIdList(accountIdList)
    wizard.exec_()

# ******************************************************************************

def getEventTypeCode(_db, accountId, urn='tfoms60:FILENAME', code=None):
    u"""Вовзращает префикс имени файла"""
    cond = ('code = \'{0}\''.format(code) if code
            else 'urn = \'{0}\''.format(urn))
    stmt = u"""SELECT EventType_Identification.value
    FROM Account
    LEFT JOIN Account_Item ON Account.id = Account_Item.master_id
    LEFT JOIN Event ON Account_Item.event_id = Event.id
    LEFT JOIN EventType ON Event.eventType_id = EventType.id
    LEFT JOIN EventType_Identification ON  EventType_Identification.master_id = EventType.id
        AND EventType_Identification.system_id = (
        SELECT MAX(id) FROM rbAccountingSystem
        WHERE rbAccountingSystem.{cond}
    )
    WHERE Account.id = '{id}'
    LIMIT 0,1""".format(id=accountId, cond=cond)

    query = _db.query(stmt)
    result = u''

    if query.first():
        record = query.record()
        result = forceString(record.value(0))

    return result


# ******************************************************************************

def getEventTypeDDCode(_db, accountId):
    u"""Возвращает код типа ДД"""
    stmt = u"""SELECT EventType_Identification.value
    FROM Account
    LEFT JOIN Account_Item ON Account.id = Account_Item.master_id
    LEFT JOIN Event ON Account_Item.event_id = Event.id
    LEFT JOIN EventType ON Event.eventType_id = EventType.id
    LEFT JOIN EventType_Identification ON  EventType_Identification.master_id = EventType.id
        AND EventType_Identification.system_id = (
        SELECT MAX(id) FROM rbAccountingSystem
        WHERE rbAccountingSystem.urn = 'ptfoms.ru V016'
    )
    WHERE Account.id = %d
    LIMIT 0,1""" % accountId

    query = _db.query(stmt)
    result = u''

    if query.first():
        record = query.record()
        result = forceString(record.value(0))

    return result


# ******************************************************************************

class CExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта Республика Калмыкия"""

    mapPrefixToEventTypeCode = {u'ДВ1': 'DP', u'ДВ2': 'DV', u'ОПВ': 'DO',
                                u'ДС1': 'DS', u'ДС2': 'DU', u'ОН1': 'DF',
                                u'ОН2': 'DD', u'ОН3': 'DR', u'УД1': 'DA',
                                u'УД2': 'DB'}

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Псковской области, ДД'
        prefix = 'R60HealthExamination'
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
            tableOrganisation = self.db.table('Organisation')
            info = self.info

            payerCode = forceString(self.db.translate(
                tableOrganisation, 'id', info['payerId'], 'miacCode'))
            recipientCode = forceString(self.db.translate(
                tableOrganisation, 'id', QtGui.qApp.currentOrgId(), 'miacCode'))

            year = info['settleDate'].year() %100
            month = info['settleDate'].month()
            packetNumber = self.page1.edtPacketNumber.value()

            postfix = u'%02d%02d%d' % (
                year, month, packetNumber) if addPostfix else u''
            result = u'%2sM%sS%s_%s.xml' % (
                self.prefixX(info['accId']), recipientCode, payerCode, postfix)
            self.__xmlBaseFileName = result

        return result


    def prefixX(self, accountId):
        u"""Вовзращает префикс имени файла"""
        code = getEventTypeCode(self.db, accountId)
        return code


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L%s' % self._getXmlBaseFileName(addPostfix)[1:]


    def getZipFileName(self):
        u"""Возвращает имя архива:"""
        return u'%s.zip' % self._getXmlBaseFileName(True)[:-4]


    def getTxtFileName(self):
        u"""Возвращает имя файла счет-фактуры"""
        return u'sf%s.txt'% self._getXmlBaseFileName(True)


    def getRegistryFileName(self):
        u"""Возвращает имя файла счет-фактуры"""
        return u'pr%s.txt'% self._getXmlBaseFileName(True)


    def getFullTxtFileName(self):
        u"""Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getTxtFileName())


    def getRegistryFullFileName(self):
        u"""Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getRegistryFileName())

# ******************************************************************************

class CExportPage1(COrder79ExportPage1, Ui_ExportPage1):
    u"""Первая страница мастера экспорта"""

    mapReasonToEventTypeCode = {
        u'ДВ1': u'проведенной Диспансеризации I этап взрослого населения',
        u'ДВ2': u'проведенной Диспансеризации II этап взрослого населения',
        u'ДВ4': u'проведенной Диспансеризации I этап взрослого населения',
        u'ДС1': u'проведенной Диспансеризации пребывающих в стационарных'
                u' учреждениях детей-сирот и детей, находящихся в трудной '
                u'жизненной ситуации',
        u'ДС2': u'проведенной Диспансеризации детей-сирот и детей, оставшихся'
                u' без попечения родителей, в том числе усыновленных (удочеренн'
                u'ых), принятых под опеку (попечительство) в приемную или патро'
                u'натную семью',
        u'ОН1': u'проведенного Профилактического медицинского осмотра'
                u' несовершеннолетних',
        u'ОН2': u'проведенного Предварительного медицинского осмотра'
                u' несовершеннолетних',
        u'ОН3': u'проведенного Периодического медицинского осмотра '
                u'несовершеннолетних',
        u'ОПВ': u'проведенного Профилактического медицинского осмотра взрослого'
                u' населения',
        u'ПН1': u'проведенного Профилактического медицинского осмотра'
                u' несовершеннолетних',
        u'УД1': u'проведенной Углубленной Диспансеризации I этап взрослого '
                u'населения',
        u'УД2': u'проведенной Углубленной Диспансеризации II этап взрослого '
                u'населения',
    }

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), PersonalDataWriter(self))
        COrder79ExportPage1.__init__(self, parent, prefix, xmlWriter)
        self.cmbRegistryType.setVisible(False)
        self.lblRegistryType.setVisible(False)

        self.chkReexposed = QtGui.QCheckBox(self)
        self.chkReexposed.setText(u'Повторное выставление')
        self.verticalLayout.addWidget(self.chkReexposed)

        self._contractAttributeCache = {}
        self._contractAttributeTypeCache = {}
        self._serviceNameCache = {}
        self._mesServiceNameCache = {}

        self.invoiceFile = None
        self.invoiceStream = None

        self.registryFile = None
        self.registryStream = None
        self.tblMesVisit = tbl('mes.MES_visit')
        self.tblMrbService = tbl('mes.mrbService')


    def preprocessQuery(self, query, params):
        pass


    def nschet(self, registryType, params):
        settleDate = params['settleDate']
        return u'{p}{x}{year:02d}{month:02d}{registryNumber:d}'.format(
            p=params['lpuMiacCode'][-3:],
            x=self._parent.prefixX(params['accId']),
            year=settleDate.year() % 100,
            month=settleDate.month(),
            registryNumber=self.edtPacketNumber.value()
        )


    def getServiceCount(self):
        u"""Возвращает количество услуг в событии."""

        result = {}
        stmt = """SELECT Account_Item.event_id,
            COUNT(DISTINCT Action.id)
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id AND Action.deleted = 0
        WHERE {0}
        GROUP BY Account_Item.event_id""".format(
            self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            actionCount = forceInt(record.value(1))
            result[eventId] = actionCount

        return result


    def createQuery(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            IF(ExposedAccountItem.id IS NULL AND rbPayRefuseType.id IS NULL, 0, 1)AS isExposedItem,
            IF(rbMesSpecification.level = '2', 1, 0) AS isMesComplete,
            Person.SNILS AS personSNILS,
            formatClientAddress(ClientRegAddress.id) AS personRegAddress,
            LastEvent.id AS lastEventId,
            rbDiagnosticResult.regionalCode AS diagRegCode,

            rbService.infis AS invoiceCode,
            rbService.name AS invoiceName,
            Account_Item.price AS invoiceTariff,
            Account_Item.amount AS invoiceAmount,
            Account_Item.`sum` AS invoiceSum,
            IF(rbDiagnosticResult.regionalCode = '502', 1, 0) AS invoiceRefuse,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            IF(rbPolicyKind.regionalCode = '1', ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            Insurer.OKATO AS PACIENT_ST_OKATO,
            Insurer.miacCode AS PACIENT_SMO,
            IF(Insurer.miacCode IS NULL OR Insurer.miacCode = '',
                        Insurer.OGRN,'') AS PACIENT_SMO_OGRN,
            IF(Insurer.miacCode IS NOT NULL, '', Insurer.OKATO) AS PACIENT_SMO_OK,
            IF((Insurer.miacCode IS NULL OR Insurer.miacCode = '')
                    AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                    Insurer.shortName, '') AS PACIENT_SMO_NAM,
            0 AS PACIENT_NOVOR,

            Account_Item.event_id AS Z_SL_IDCASE,
            rbMedicalAidKind.regionalCode AS Z_SL_VIDPOM,
            PersonOrganisation.miacCode AS Z_SL_LPU,
            IF(rbScene.code = '4', 1, 0)  AS Z_SL_VBR,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            IF(rbDiagnosticResult.regionalCode = '502', 1, 0) AS Z_SL_P_OTK,
            EventResult.regionalCode AS Z_SL_RSLT_D,
            rbMedicalAidUnit.regionalCode AS Z_SL_IDSP,
            Account_Item.sum AS Z_SL_SUMV,

            Account_Item.event_id AS SL_SL_ID,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            Event.id AS SL_NHISTORY,
            IF(EventType.form = '110', Event.execDate, Event.setDate) AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            Diagnosis.MKB AS SL_DS1,
            CASE
                WHEN rbDispanser.code = '1' THEN 1
                WHEN rbDispanser.code IN ('2', '6') THEN 2
                ELSE 3
            END AS SL_PR_D_N,
            IF(Event.nextEventDate, DATE_FORMAT(Event.nextEventDate, '%m%y'), DATE_FORMAT(DATE_ADD(Event.execDate, INTERVAL 90 DAY), '%m%y')) AS SL_DN_DATE,
            Account_Item.sum AS SL_SUM_M,
            IFNULL(rbSocStatusType.regionalCode, '2') AS SL_COMENTSL,
            DS9.MKB AS DS2_N_DS2,
            CASE
                WHEN DS9Dispanser.code = '1' THEN 1
                WHEN DS9Dispanser.code IN ('2', '6') THEN 2
                ELSE 3
            END AS DS2_N_PR_DS2_N,

            IF(EventResult.regionalCode IN (3, 31, 32, 33, 34, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16), 1, '') AS NAZ_NAZ_N,
            IF(EventResult.regionalCode IN (3, 31, 32, 33, 34, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16),
                CASE
                    WHEN rbDiagnosticResult.regionalCode = '503' THEN 1
                    WHEN rbDiagnosticResult.regionalCode = '504' THEN 2
                    WHEN rbDiagnosticResult.regionalCode = '506' THEN 4
                    WHEN rbDiagnosticResult.regionalCode = '507' THEN 5
                    WHEN rbDiagnosticResult.regionalCode = '508' THEN 6
                    WHEN rbDiagnosticResult.regionalCode IN ('509', '510', '511', '501') THEN 3
                    ELSE ''
                END, '') AS NAZ_NAZ_R,
            IF (rbDiagnosticResult.regionalCode IN ('503', '504') AND
                 EventResult.regionalCode IN (3, 31, 32, 4, 5, 6, 7, 11, 12, 13, 14, 15),
                 rbSpeciality.federalCode, '') AS NAZ_NAZ_IDDOKT,
            IF(EventResult.regionalCode IN (3, 31, 32, 4, 5, 6, 7, 11, 12, 13, 14, 15),
                CASE
                    WHEN rbDiagnosticResult.regionalCode IN ('509', '501') THEN 1
                    WHEN rbDiagnosticResult.regionalCode = '510' THEN 2
                    WHEN rbDiagnosticResult.regionalCode = '511' THEN 3
                    ELSE ''
                END, '') AS NAZ_NAZ_V,
            IF (rbDiagnosticResult.regionalCode IN ('506', '507') AND
                 EventResult.regionalCode IN (3, 31, 32, 4, 5, 6, 7, 11, 12, 13, 14, 15),
                IFNULL(ServiceProfileMedicalAidProfile.code,
                    IFNULL(ServiceMedicalAidProfile.code, '')), '') AS NAZ_NAZ_PMP,

            PersonOrganisation.miacCode AS USL_LPU,
            PersonOrgStructure.infisCode AS USL_LPU_1,
            IFNULL(IF(Action.status = 2 OR Action.begDate IS NULL,
                Action.endDate, Action.begDate),Event.setDate) AS USL_DATE_IN,
            IFNULL(IFNULL(Action.endDate, Action.begDate),
                Event.execDate) AS USL_DATE_OUT,
            IF(rbDiagnosticResult.regionalCode = '502', 1, 0) AS USL_P_OTK,
            IF(rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL,
                MES_visit.altAdditionalServiceCode,
                    IF(rbService.infis IS NULL OR rbService.infis = '',
                        rbService.code, rbService.infis)) AS USL_CODE_USL,
            Account_Item.`sum` AS USL_SUMV_USL,
            (SELECT value FROM rbService_Identification RSI WHERE RSI.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                  AND SId.system_id IN (SELECT id FROM rbAccountingSystem
                                        WHERE code = 'tfomsVID_VME')
                  AND SId.deleted = 0)) AS USL_VID_VME,
            IF(ActionType.code IN ('630001', '631001'),
             (SELECT APO.value
              FROM ActionProperty AP
              LEFT JOIN ActionProperty_Integer AS APO ON APO.id = AP.id
              WHERE AP.deleted = 0
                AND AP.action_id = Action.id
                AND AP.type_id = (
                    SELECT id FROM ActionPropertyType APT
                    WHERE APT.name = 'Показатель сатурации'
                        AND APT.deleted = 0
                        AND APT.actionType_id = Action.actionType_id)),
            '') AS USL_COMENTU,

            1 AS MR_USL_N_MR_N,
            ActionSpeciality.federalCode AS MR_USL_N_PRVS,
            ActionPerson.federalCode AS MR_USL_N_CODE_MD,

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
            ClientContact.contact AS PERS_TEL,
            (SELECT IF(MAX(ds.id) IS NOT NULL, 1, 0)
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code IN (1, 2, 9))
                  AND dc.event_id = Account_Item.event_id
                  AND rbDiseasePhases.code = 10
                  AND (SUBSTR(ds.MKB,1,1) = 'C' OR
                       ((SUBSTR(ds.MKB,1,3) BETWEEN 'D00' AND 'D09')
                        AND dc.diagnosisType_id IN (
                            SELECT id FROM rbDiagnosisType WHERE code IN (1, 2))))
            ) AS SL_DS_ONK,
            Event.MES_id AS mesId
            FROM Account_Item
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
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
            LEFT JOIN Diagnosis AS DS9 ON DS9.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN rbDispanser AS DS9Dispanser ON DS9.dispanser_id = DS9Dispanser.id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id

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
            LEFT JOIN rbDiseaseCharacter ON Diagnosis.character_id = rbDiseaseCharacter.id
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
            LEFT JOIN ClientContact ON ClientContact.id = (
                SELECT MAX(id)
                FROM ClientContact
                WHERE ClientContact.deleted = 0 AND ClientContact.client_id = Client.id
                AND ClientContact.contactType_id = (
                    SELECT id FROM rbContactType WHERE code = '3'
                )
            )
            LEFT JOIN Action ON Account_Item.action_id = Action.id
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
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {0}
            ORDER BY Event.client_id, LastEvent.id, Event.id""".format(self.tableAccountItem['id'].inlist(self.idList))

        return self.db.query(stmt)


    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = {
            'isReexposed': '1' if self.chkReexposed.isChecked() else '0'
        }

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
        params['USL_KODLPU'] = params['lpuCode']
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['eventCount'] = self.getEventCount()
            params['completeEventCount'] = self.getCompleteEventCount()
            params['completeEventSum'] = self.getCompleteEventSum()
            params['SL_COUNT'] = params['accNumber']
            params['mapEventIdToSum'] = self.getEventSum()
            params['mapEventIdToPrice'] = self.getEventPrice()
            params['serviceCount'] = self.getServiceCount()
            eventTypeDDCode = getEventTypeDDCode(self.db, params['accId'])
            params['isDV1'] = eventTypeDDCode in (u'ДВ1', u'ОН1', u'ПН1')
            params['isDV12'] = eventTypeDDCode in (u'ДВ1', u'ДВ2')

            registryType = self.cmbRegistryType.currentIndex()
            params['NSCHET'] = self.nschet(registryType, params)
            self._parent.note = u'[NSCHET:%s]' % params['NSCHET']

            recipientId = forceRef(self.db.translate(
                'Contract', 'id', params['contractId'], 'recipient_id'))
            recipientRecord = self.db.getRecord(
                'Organisation', 'shortName, address, accountant',
                recipientId)
            params['recipientName'] = forceString(recipientRecord.value(0))
            params['recipientAddress'] = forceString(recipientRecord.value(1))
            params['accountant'] = forceString(recipientRecord.value(2))
            params['chief'] = self._getChiefName(recipientId)

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

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)

        self.invoiceFile = QFile(self.wizard().getFullTxtFileName())
        self.invoiceFile.open(QIODevice.WriteOnly | QIODevice.Text)
        self.invoiceStream = QTextStream(self.invoiceFile)
        self.invoiceStream.setCodec('UTF8')

        self.registryFile = QFile(
            self.wizard().getRegistryFullFileName())
        self.registryFile.open(QIODevice.WriteOnly | QIODevice.Text)
        self.registryStream = QTextStream(self.registryFile)
        self.registryStream.setCodec('UTF8')

        CAbstractExportPage1Xml.exportInt(self)


    def process(self, dest, record, params):
        CAbstractExportPage1Xml.process(self, dest, record, params)
        self.processInvoice(record, params)
        self.processRegistry(record, params)


    def processInvoice(self, record, params):
        u"""Пишет данные для счет-фактуры в словарь"""

        def updateData(invoice):
            key = (invoiceCode, mesId)
            if params[invoice].has_key(key):
                (name, tariff, amount, _sum) = params[invoice][key]
                params[invoice][key] = (
                    name, tariff, amount + invoiceAmount, _sum + invoiceSum)
            else:
                params[invoice][key] = (invoiceName, invoiceTariff,
                                        invoiceAmount, invoiceSum)

        invoiceCode = forceString(record.value('invoiceCode'))
        invoiceName = forceString(record.value('invoiceName'))
        invoiceTariff = forceDouble(record.value('invoiceTariff'))
        invoiceAmount = forceDouble(record.value('invoiceAmount'))
        invoiceSum = forceDouble(record.value('invoiceSum'))
        invoiceRefuse = forceBool(record.value('invoiceRefuse'))
        mesId = forceRef(record.value('mesId'))

        if not invoiceRefuse:
            updateData('invoice')


    def processRegistry(self, record, params):
        u"""Пишет данные для реестра пациентов в словарь"""

        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        if not params.has_key('skipClientInfo'):
            info = (formatName(record.value('PERS_FAM'),
                               record.value('PERS_IM'),
                               record.value('PERS_OT')),  #ФИО
                    formatSNILS(record.value('personSNILS')), #СНИЛС
                    formatDate(record.value('PERS_DR')), # ДР
                    formatSex(record.value('PERS_W')),  #Пол
                    (u'%s %s' % ( #Полис
                        forceString(record.value('PACIENT_SPOLIS')),
                        forceString(record.value('PACIENT_NPOLIS')))).strip(),
                    (u'%s %s' % ( #Документ
                        forceString(record.value('PERS_DOCSER')),
                        forceString(record.value('PERS_DOCNUM')))),
                    forceString(record.value('personRegAddress')),  #Адрес
                    forceString(record.value('SL_DS1')),
                    clientId)

            params['clients'].add(info)
        serviceRefused = forceBool(record.value('USL_P_OTK'))

        if not serviceRefused:
            serviceInfo = (
                forceString(record.value('USL_CODE_USL')),
                formatDate(record.value('USL_DATE_OUT')),
                forceDouble(record.value('USL_SUMV_USL')),
                forceRef(record.value('mesId')),
                forceString(record.value('invoiceName'))
            )
            params['services'].setdefault(clientId, []).append(serviceInfo)



    def postExport(self):
        self.writeInvoice(self._processParams['invoice'],
                          self.invoiceStream)
        self.writeRegistry(self._processParams['clients'],
                           self.registryStream)
        self.invoiceFile.close()
        self.registryFile.close()
        CAbstractExportPage1Xml.postExport(self)


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


    def writeInvoice(self, invoice, output):
        fmtStr = u'%10.10s│%10.10s│%40.40s│%10.10s│%10.10s│%12.12s\n'
        delimeter = u'-'*100 + '\n'
        params = self._processParams
        settleDate = params['settleDate']
        n = 1
        totalSum = 0
        totalAmount = 0

        output << u"""
Медицинское учреждение {recipientName}
 
СЧЕТ-ФАКТУРА № {number} от {currentDate} за оплату {reason}

за {settleDate}\n\n\n""".format(
    number=params['NSCHET'],
    recipientName=params['recipientName'],
    currentDate=QDate.currentDate().toString('dd.MM.yyyy'),
    settleDate=settleDate.toString('MMMM yyyy'),
    reason=self.mapReasonToEventTypeCode.get(
        getEventTypeDDCode(self.db, params['accId']), '?'))

        output << fmtStr % (u'№', u'Код услуги', u'Наименование услуги',
                            u'Цена', u'Количество', u'Сумма')
        output << delimeter

        _invoice = {}

        for key in sorted(invoice):
            (altName, tariff, amount, _sum) = invoice[key]
            code, mesId = key
            name = self.serviceName(code, mesId)
            if name == '-':
                name = altName
            key = code, name

            if _invoice.has_key(key):
                _, oldAmount, oldSum = _invoice[key]
                _invoice[key] = tariff, amount + oldAmount, _sum + oldSum
            else:
                _invoice[key] = tariff, amount, _sum


        for key in sorted(_invoice):
            tariff, amount, _sum = _invoice[key]
            code, name = key
            s = fmtStr % (u'%d' % n, code, name, u'%.2f' % tariff,
                          u'%.2f' % amount, u'%.2f' % _sum)
            totalSum += _sum
            totalAmount += amount
            output << s
            n += 1

        output << delimeter
        output << (u'Количество пациентов {clientCount} Количество услуг '
                   u'{totalAmount} Сумма {totalSum:.2f}\n'
                   u'Главный врач _______________ {chief}\n'
                   u'Главный бухгалтер ____________ {accountant}\n\n'.format(
                       clientCount=params['eventCount'],
                       totalAmount=totalAmount,
                       totalSum=totalSum,
                       chief=params['chief'],
                       accountant=params['accountant']))


    def writeRegistry(self, registry, output):
        params = self._processParams
        output << (u'\nРеестр счетов №{number} от {currentDate} за оплату '
                   u'{reason} за {settleDate}\nМО {shortName}, {address}'
                   u'\n\n'.format(
                       number=params['NSCHET'],
                       currentDate=QDate.currentDate().toString('dd.MM.yyyy'),
                       settleDate=params['settleDate'].toString('MMMM yyyy'),
                       reason=self.mapReasonToEventTypeCode.get(
                           getEventTypeDDCode(self.db, params['accId']), '?'),
                       shortName=params['recipientName'],
                       address=params['recipientAddress']))

        delimeter = u'-'*153 + '\n'
        fmtStr = (u'{number:4d}|{name:<40.40}|{sex:<3.3}|{birthDate:<13.13}|'
                  u'{address:<50.50}|{policy:<17.17}|{snils:<14.14}|'
                  u'{mkb:<10.10}\n')
        fmtService = u'{code:<10.10}|{name:<40.40}|{date:<10.10}|{sum:14.2f}\n'
        n = 0

        for client in sorted(list(registry)):
            n += 1
            output << delimeter
            output << (u'  № |                ФИО                     |Пол|'
                       u'Дата рождения|                          Адрес     '
                       u'              |      Полис      |     СНИЛС    | '
                       u'Диаг\n')
            output << delimeter
            (name, snils, birthDate, sex, policy, document, address, mkb,
             clientId) = client
            output << fmtStr.format(
                number=n, snils=snils, name=name, birthDate=birthDate, sex=sex,
                policy=policy, document=document, address=address, mkb=mkb)
            output << delimeter
            total = 0

            for service in params['services'].get(clientId, []):
                (code, date, _sum, mesId, altName) = service
                name = self.serviceName(code, mesId)
                if name == '-':
                    name = altName
                output << fmtService.format(code=code, name=name, date=date,
                                            sum=_sum)
                total += _sum

            output << delimeter
            output << u'Итого: {0:.2f}\n\n'.format(total)

        output << (u'Итого по счету {total:.2f}\n'
                   u'Главный врач _______________ {chief}\n'
                   u'Главный бухгалтер ____________ {accountant}\n\n'.format(
                       total=forceDouble(params['accSum']),
                       chief=params['chief'],
                       accountant=params['accountant']))


    def serviceName(self, code, mesId=None):
        u'Возвращает имя услуги'
        result = self._serviceNameCache.get(code, -1)

        if result == -1:
            cond = [self.tblMesVisit['deleted'].eq(0),
                    self.tblMesVisit['altAdditionalServiceCode'].eq(code)]

            if mesId:
                cond.append(self.tblMesVisit['master_id'].eq(mesId))

            record = self.db.getRecordEx(
                self.tblMesVisit, 'serviceCode', cond)
            serviceCode = forceString(record.value(0)) if record else None
            result = self.mesServiceName(serviceCode if serviceCode else code)
            self._serviceNameCache[code] = result

        return result


    def mesServiceName(self, code):
        u'Возвращает имя услуги МЭС'
        result = self._mesServiceNameCache.get(code, -1)

        if result == -1:
            cond = [self.tblMrbService['deleted'].eq(0),
                    self.tblMrbService['code'].eq(code)]
            record = self.db.getRecordEx(self.tblMrbService, 'name', cond)
            result = forceString(record.value(0)) if record else u'-'
            self._mesServiceNameCache[code] = result

        return result

# ******************************************************************************

class CExportPage2(COrder79ExportPage2):
    u"""Вторая страница мастера экспорта"""
    def __init__(self, parent, prefix):
        COrder79ExportPage2.__init__(self, parent, prefix)

    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(),
                    self._parent.getPersonalDataFullXmlFileName(),
                    self._parent.getFullTxtFileName(),
                    self._parent.getRegistryFullFileName())
        zipFileName = self._parent.getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class XmlStreamWriter(COrder79XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR')
    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2')
    completeEventFields1 = (('IDCASE', 'VIDPOM', 'LPU', 'VBR')
                           + completeEventDateFields +
                           ('P_OTK', 'RSLT_D', 'OS_SLUCH'))
    completeEventFields2 = ('IDSP', 'SUMV')
    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields = (('SL_ID', 'LPU_1', 'NHISTORY')
                   +  eventDateFields +
                   ('DS1', 'DS1_PR', 'DS_ONK', 'PR_D_N', 'DN_DATE', 'DS2_N', 'NAZ', 'ED_COL',
                    'SUM_M'))
    eventSubGroup = {
        'DS2_N': {'fields': ('DS2', 'DS2_PR', 'PR_DS2_N')},
        'NAZ': {'fields': ('NAZ_N', 'NAZ_R', 'NAZ_IDDOKT', 'NAZ_V', 'NAZ_PMP')}
    }
    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1')
                     + serviceDateFields +
                     ('P_OTK', 'VID_VME', 'CODE_USL', 'SUMV_USL', 'MR_USL_N',
                      'COMENTU'))
    serviceSubGroup = {
        'MR_USL_N': {'fields': ('MR_N', 'PRVS', 'CODE_MD')},
    }
    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP',  'SUMV', 'DS2', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'MR_N')

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params.get('settleDate', QDate())
        payerMiacCode = forceString(self._parent.db.translate(
            'Organisation', 'id', params['payerId'], 'miacCode'))
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.1.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', forceString(params['completeEventCount']))
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuMiacCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', params['NSCHET'])
        self.writeTextElement('DSCHET', settleDate.toString(Qt.ISODate))
        self.writeTextElement('PLAT', payerMiacCode)
        self.writeTextElement('SUMMAV', u'{0:.2f}'.format(params['accSum']))
        self.writeTextElement('DISP', self.dispanserType(params))
        self.writeEndElement() # SCHET


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        if params.get('lastEventId'):
            # выгрузка незавершенных действий
            self.exportActions(params['lastEventId'], params, True)
            self.writeTextElement('COMENTSL', params['lastCOMENTSL'])

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
                self.writeTextElement(
                    'COMENTSL', forceString(record.value('SL_COMENTSL')))
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
            params['lastCOMENTSL'] = forceString(
                record.value('SL_COMENTSL')) if params['isDV12'] else ''

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

        if params['isMesComplete']:
            eventId = forceRef(record.value('eventId'))
            self.exportActions(eventId, params)
        else:
            params['USL_IDSERV'] += 1

            _record = CExtendedRecord(record, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            subGroup=self.serviceSubGroup,
                            dateFields=self.serviceDateFields)


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
        _record = CExtendedRecord(record, local_params, DEBUG)

        if eventId != params.setdefault('lastEventId'):
            params['USL_IDSERV'] = 0

            if params['lastEventId']:
                # выгрузка незавершенных действий
                self.exportActions(eventId, params, True)
                self.writeEndElement() # SL

            self.writeGroup('SL', self.eventFields, _record, self.eventSubGroup if forceString(record.value('NAZ_NAZ_N')) else None,
                            closeGroup=False, dateFields=self.eventDateFields)
            params['lastEventId'] = eventId


    def exportActions(self, eventId, params, exportUncomplete=False):
        u"""Выгружает  все действия по указанному событию"""

        if eventId not in params.setdefault('exportedEvents', set()):
            params['exportedEvents'].add(eventId)
            dv1Cond = (u'OR Action.status = 6 OR (Action.endDate NOT BETWEEN '
                       u'Event.setDate AND Event.execDate)' if params['isDV1']
                       else u'')
            stmt = u"""SELECT Organisation.miacCode AS USL_LPU,
                ExecPersonOrgStructure.infisCode AS USL_LPU_1,
                IF(Action.status = 2 OR Action.begDate IS NULL,
                    Action.endDate, Action.begDate) AS USL_DATE_IN,
                IFNULL(Action.endDate, Action.begDate) AS USL_DATE_OUT,
                IF(Action.status = 2, 0, 1) AS USL_P_OTK,
                Event.setDate AS eventSetDate,
                rbMesSpecification.level AS mesSpecLevel,
                MES_visit.altAdditionalServiceCode AS altAdditionalServiceCode,
                IF((rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL)  %s,
                    MES_visit.altAdditionalServiceCode,
                        IF(rbService.infis IS NULL OR rbService.infis = '',
                            rbService.code, rbService.infis)) AS USL_CODE_USL,
                IF(IF((rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL) %s,
                    MES_visit.altAdditionalServiceCode,
                        IF(rbService.infis IS NULL OR rbService.infis = '',
                            rbService.code, rbService.infis)) = mes.MES.code, '%.2f', 0) AS USL_TARIF,
                IF(IF((rbMesSpecification.level = '2' AND MES_visit.id IS NOT NULL) %s,
                    MES_visit.altAdditionalServiceCode,
                        IF(rbService.infis IS NULL OR rbService.infis = '',
                            rbService.code, rbService.infis)) = mes.MES.code, '%.2f', 0) AS USL_SUMV_USL,
                Person.federalCode AS USL_IDDOKT,
                IF(ActionType.code IN ('630001', '631001'),
                 (SELECT APO.value
                  FROM ActionProperty AP
                  LEFT JOIN ActionProperty_Integer AS APO ON APO.id = AP.id
                  WHERE AP.deleted = 0
                    AND AP.action_id = Action.id
                    AND AP.type_id = (
                        SELECT id FROM ActionPropertyType APT
                        WHERE APT.name = 'Показатель сатурации'
                            AND APT.deleted = 0
                            AND APT.actionType_id = Action.actionType_id)),
                '') AS USL_COMENTU,
                1 AS MR_USL_N_MR_N,
                rbSpeciality.federalCode AS MR_USL_N_PRVS,
                Person.federalCode AS MR_USL_N_CODE_MD,
                Event.client_id AS PACIENT_ID_PAC, -- for registry
                Event.MES_id AS mesId -- for registry
            FROM Action
            LEFT JOIN Event ON Action.event_id = Event.id
            LEFT JOIN Person ON Person.id = Action.person_id
            LEFT JOIN Person AS ExecPerson ON ExecPerson.id = Event.execPerson_id
            LEFT JOIN OrgStructure AS ExecPersonOrgStructure ON ExecPerson.orgStructure_id = ExecPersonOrgStructure.id
            LEFT JOIN Organisation ON Organisation.id = IFNULL(Action.org_id, Person.org_id)
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            LEFT JOIN rbService ON ActionType.nomenclativeService_id = rbService.id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN mes.MES_visit ON mes.MES_visit.id = (
                SELECT MAX(id)
                FROM mes.MES_visit
                WHERE mes.MES_visit.serviceCode = rbService.code
                    AND mes.MES_visit.master_id = mes.MES.id
                    AND mes.MES_visit.deleted = 0
            )
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            WHERE Action.event_id = %d AND Action.deleted = 0""" % (
                dv1Cond, dv1Cond,
                params['mapEventIdToPrice'].get(eventId, 0), dv1Cond,
                params['mapEventIdToSum'].get(eventId, 0), eventId)

            if exportUncomplete:
                stmt += (u' AND (Action.status=6 OR (Action.status=2 AND '
                         u'(Action.endDate NOT BETWEEN Event.setDate AND '
                         u'Event.execDate)))')

            query = self._parent.db.query(stmt)

            while query.next():
                params['USL_IDSERV'] += 1
                record = query.record()
                local_params = {
                    'invoiceAmount': 1,
                    'invoiceCode' : forceString(record.value('USL_CODE_USL')),
                    'invoiceSum': forceDouble(record.value('USL_SUMV_USL')),
                    'invoiceTariff': forceDouble(record.value('USL_TARIF')),
                    'invoiceRefuse': forceBool(record.value('USL_P_OTK')),
                    'skipClientInfo': True
                }
                if (((forceInt(record.value('USL_P_OTK')) == 1 and forceInt(record.value('USL_P_OTK')) !=2) or
                    (forceDate(record.value('eventSetDate')) > forceDate(record.value('USL_DATE_OUT'))))) and params['isDV1']:
                        record.setValue('USL_CODE_USL', toVariant(forceString(record.value('altAdditionalServiceCode'))))
                        local_params['invoiceCode'] = forceString(record.value('altAdditionalServiceCode'))
                local_params.update(params)
                record = CExtendedRecord(record, local_params, DEBUG)
                if not local_params['invoiceSum']: # только с 0 суммами
                    self._parent.processInvoice(record, params)
                    self._parent.processRegistry(record, local_params)
                self.writeGroup('USL', self.serviceFields, record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields)


    def dispanserType(self, params):
        u"""Возвращает код типа ДД"""
        return getEventTypeDDCode(self._parent.db, params['accId'])


    def writeTextElement(self, elementName, value=None):
        u"""Если тег в списке обязательных, выгружаем его пустым"""
        if value or elementName in self.requiredFields:
            COrder79XmlStreamWriter.writeTextElement(self, elementName, value)


# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR60HealthExamination,
                      accNum=u'Углубленная диспансеризация I этап-1',
                      configFileName='75_13_s11.ini',
                      #eventIdList=[907916]
                      )
