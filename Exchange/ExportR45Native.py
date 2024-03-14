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

u"""Экспорт реестра в формате XML. Курган Д1"""

import json

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QDate
from PyQt4.QtSql import QSqlRecord

from library.DbEntityCache import CDbEntityCache
from library.Utils import (forceString, forceInt, toVariant, forceRef,
                           forceBool, forceDate, forceDouble)

from Exchange.Export import CExportHelperMixin, CAbstractExportPage1Xml
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Order200Export import COnkologyInfo
from Exchange.ExportR08Hospital import exportNomenclativeServices
from Exchange.ExportR60NativeAmbulance import (PersonalDataWriter, CExportPage1,
                                               CExportPage2)
from Exchange.Order79Export import (
    COrder79v3XmlStreamWriter as XmlStreamWriter,
    COrder79XmlStreamWriter,
    COrder79ExportWizard, COrder79ExportPage1)
from Exchange.Utils import compressFileInZip
from RefBooks.Service.ServiceModifier import applyModifier, parseModifier

DEBUG = False

def exportR45Native(widget, accountId, accountItemIdList, _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CR45ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

def getXmlBaseFileName(_db, info, packetNumber, addPostfix=True, conditions=''):
    u"""Возвращает имя файла для записи данных
    Имя файла имеет вид HPiNiPpNp_YYMMN.XML
    где Pp – Параметр, определяющий организацию -получателя:
      S- если плательщиком по договору является страховая компания
        (Organisation.isInsurer=1)
      T - в остальных случаях (т.е. когда плательщиком является ТФОМС)
    Np – Номер получателя:
      если получатель страховая, то это Organisation.infisCode
      если ТФОМС, то 45
    """

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
    recipient = {'id': forceRef(_db.translate(tableContract, 'id',
                                              info['contractId'],
                                              'recipient_id'))}

    for org in (payer, recipient):
        record = _db.getRecord('Organisation',
                               'smoCode, isInsurer, isMedical', org['id'])

        if record:
            org['isMedical'] = forceBool(record.value(2))
            org['isInsurer'] = forceBool(record.value(1))
            org['code'] = forceString(record.value(0))

    p_i = getPrefix(recipient)
    p_p = 'S' if payer.get('isInsurer') else 'T'

    postfix = u'%02d%02d%s%02d' % (info['settleDate'].year() %100,
                                 info['settleDate'].month(),
                                 conditions,
                                 packetNumber) if addPostfix else u''
    result = u'%s%s%s%s_%s.xml' % (p_i, recipient.get('code', ''), p_p,
                                   (payer.get('code', '') if
                                    payer.get('isInsurer') else '45'), postfix)
    return result

# ******************************************************************************

class CR45ExportWizard(COrder79ExportWizard):
    u"""Мастер экспорта для Кургана"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Кургана'
        prefix = 'R45Native'
        COrder79ExportWizard.__init__(self, title, prefix, CR45ExportPage1,
                                      CR45ExportPage2, parent)
        self.setWindowTitle(title)
        self.page1.setXmlWriter((CR45XmlStreamWriter(self.page1),
                                 CR45PersonalDataWriter(self.page1),
                                 CR45RegistryXmlStreamWriter(self.page1)))
        self.__xmlBaseFileName = None
        self.anyOnklogy = False


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""
        result = self.__xmlBaseFileName

        if not result:
            result = getXmlBaseFileName(self.db, self.info,
                                        self.page1.edtPacketNumber.value(),
                                        addPostfix,
                                        self.page1.contractAttributeByType('U'))
            self.__xmlBaseFileName = result

        return result


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return u'{0}.zip'.format(self.getXmlFileName()[:-4])


# ******************************************************************************

class CR45ExportPage1(CExportPage1):
    u'Первая страница мастера экспорта'
    registryTypeId = 0
    registryTypeD1 = 1

    def __init__(self, parent, prefix):
        CExportPage1.__init__(self, parent, prefix)
        self.lblRegistryType.setVisible(True)
        self.cmbRegistryType.setVisible(True)
        self.cmbRegistryType.clear()
        self.cmbRegistryType.addItems([u'файл идентификации', u'реестр счета'])
        self.registryType = self.registryTypeId

        prefs = QtGui.qApp.preferences.appPrefs
        self.cmbRegistryType.setCurrentIndex(forceInt(prefs.get(
            'Export%sRegistryType' % prefix, 0)))

        self.chkUseNomenclativeService = QtGui.QCheckBox(self)
        self.chkUseNomenclativeService.setText(
            u'Использовать номенклатурные услуги')
        self.gridlayout.addWidget(self.chkUseNomenclativeService, 10, 0, 1, 5)

        self._recNum = 1


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['Export%sRegistryType' % self.prefix] = toVariant(
            self.cmbRegistryType.currentIndex())
        return CExportPage1.validatePage(self)


    def preprocessQuery(self, query, params):
        ambulanceIncomplete = not self.chkAmbulancePlanComplete.isChecked()
        emergencyIncomplete = not self.chkEmergencyPlanComplete.isChecked()
        params['ambulanceIncomplete'] = ambulanceIncomplete
        params['emergencyIncomplete'] = emergencyIncomplete
        params['actionList'] = []

        while query.next():
            record = query.record()
            actionId = forceString(record.value('actionId'))

            if actionId and actionId != '0':
                params['actionList'].append(actionId)

        query.exec_()


    def postExport(self):
        COrder79ExportPage1.postExport(self)


    def process(self, dest, record, params):
        COrder79ExportPage1.process(self, dest, record, params)


    def getOnkologyInfo(self):
        u'Получает информацию об онкологии в событиях'
        onkologyInfo = COnkologyInfo()
        return onkologyInfo.get(self.db,
                                self.tableAccountItem['id'].inlist(self.idList),
                                self)

    def exportInt(self):
        self._parent.anyOnkology = False
        self.registryType = self.cmbRegistryType.currentIndex()
        params = self.processParams()
        params['serviceModifier'] = forceString(self.db.translate(
            'rbVisitType', 'code', u'ПОС', 'serviceModifier'))
        params['isReexposed'] = '1' if self.chkReexposed.isChecked() else '0'
        params['mapEventIdToSum'] = self.getEventSum()
        params['tempInvalidMap'] = self.getTempInvalidInfo()
        params['completeEventSum'] = self.getCompleteEventSum()
        params['mapEventIdToKsgKpg'] = self.getKsgKpgInfo()
        params['onkologyInfo'] = self.getOnkologyInfo()
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuSmoCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'smoCode'))
        params['USL_KODLPU'] = params['lpuCode']
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'miacCode'))
            params['mapEventIdToFksgCode'] = self.getFksgCode()
            params['SLUCH_COUNT'] = params['accNumber']

        self._recNum = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))
        params['visitExportedEventList'] = set()
        params['toggleFlag'] = 0
        params['doneVis'] = set()
        params['useNomenclativeServiceCode'] = (
            self.chkUseNomenclativeService.isChecked())
        self.setProcessParams(params)

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, registryWriter) = self.xmlWriter()
        writer = (registryWriter if self.registryType == self.registryTypeId
                  else xmlWriter)

        self.setXmlWriter((writer, personalDataWriter))
        writer.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)

        CAbstractExportPage1Xml.exportInt(self)


    def prepareStmt(self, params):
        (_, _, where, _) = CExportPage1.prepareStmt(
            self, params)

        serviceCode = (u"""IF(VisitCount.amount > 1
            AND (SELECT AT.serviceType FROM ActionType AT
                 WHERE AT.id = Action.actionType_id) IN (1, 2)
            AND Action.person_id = Event.execPerson_id,
            (SELECT S.code FROM  ActionType AT
             LEFT JOIN rbService S ON S.id = AT.nomenclativeService_id
             WHERE Action.actionType_id = AT.id
             LIMIT 0,1),
            IF(Account_Item.visit_id IS NOT NULL,
                VisitService.infis, rbService.infis))""" if params[
                    'useNomenclativeServiceCode'] else
                       u"""IF(Account_Item.visit_id IS NOT NULL,
                VisitService.infis, rbService.infis)""")

        settleDate = params['settleDate']
        select = u"""FirstEvent.id AS eventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            MesService.code AS mesServiceCode,
            MesService.infis AS mesServiceInfis,
            MesAction.begDate AS mesActionBegDate,
            MesAction.endDate AS mesActionEndDate,
            Account_Item.`sum` AS `sum`,
            Account_Item.uet,
            Account_Item.amount,
            Account_Item.usedCoefficients,
            Event.id AS lastEventId,
            rbMedicalAidType.code AS medicalAidTypeCode,
            IF(rbMedicalAidType.regionalCode IN(1, 2, 3),
                Diagnostic.character_id, '') AS SL_C_ZAB,

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
            IF(rbPolicyKind.regionalCode = '1', ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            ClientPolicy.number AS PACIENT_ENP,
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
            IF(MseAction.id IS NOT NULL, 1, '') AS PACIENT_MSE,
            (SELECT AttachOrg.smoCode
             FROM ClientAttach
             LEFT JOIN Organisation AS AttachOrg ON
                AttachOrg.id = ClientAttach.LPU_id
             WHERE ClientAttach.id = getClientAttachIdForDate(Client.id, 0, Event.execDate)
            ) AS PACIENT_MCOD,

            Event.id AS Z_SL_IDCASE,
            rbMedicalAidType.regionalCode AS Z_SL_USL_OK,
            IFNULL(OrgStructure_Identification.value,
                rbMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            RelegateOrg.infisCode AS Z_SL_NPR_MO,
            DATE(Event.srcDate) AS Z_SL_NPR_DATE,
            PersonOrganisation.smoCode AS Z_SL_LPU,
            FirstEvent.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            rbMedicalAidUnit.federalCode AS Z_SL_IDSP,

            FirstEvent.setDate AS SLUCH_DATE_1,
            Event.execDate AS SLUCH_DATE_2,

            FirstEvent.id AS SL_SL_ID,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL(EventType_Identification.value,
                    PersonOrgStructure.tfomsCode)) AS SL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS SL_DET,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                Event.externalId, Client.id) AS SL_NHISTORY,
            IF(EventType.form = '110', FirstEvent.execDate,
                FirstEvent.setDate) AS SL_DATE_1,
            FirstEvent.execDate AS SL_DATE_2,
            DS0.MKB AS SL_DS0,
            Diagnosis.MKB AS SL_DS1,
            CONCAT_WS(',', Diagnosis.MKBEx, DS9.MKB) AS ds2List,
            DS3.MKB AS SL_DS3,
            CASE
                WHEN rbDispanser.observed = 1 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                WHEN rbDispanser.observed = 1 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                WHEN rbDispanser.observed = 0 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                WHEN rbDispanser.observed = 0 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                ELSE ''
            END AS SL_DN,
            mes.MES_ksg.code AS SL_CODE_MES1,
            rbSpeciality.federalCode AS SL_PRVS,
            Person.federalCode AS SL_IDDOKT,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                IF(rbEventProfile.regionalCode = '6', UetInfo.uet,
                    Account_Item.amount)) AS SL_ED_COL,
            Account_Item.price AS SL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35')
                AND rbEventProfile.regionalCode = '5', 0,
                    IF(rbEventProfile.regionalCode = '6',
                        UetInfo.`sum`, Account_Item.`sum`)) AS SL_SUM_M,
            0 AS SL_TELEMED,

            IF(rbMedicalAidType.regionalCode != '3', mes.MES_ksg.code, NULL) AS KSG_KPG_N_KSG,
            IF(rbMedicalAidType.regionalCode != '3', 0, NULL) AS KSG_KPG_KSG_PG,
            IF(rbMedicalAidType.regionalCode != '3', mes.MES_ksg.vk, NULL) AS KSG_KPG_KOEF_Z,
            IF(rbMedicalAidType.regionalCode != '3', 1, NULL) AS KSG_KPG_KOEF_UP,
            IF(rbMedicalAidType.regionalCode != '3', 1.049, NULL) AS KSG_KPG_KOEF_D,

            PersonOrganisation.miacCode AS USL_LPU,
            PersonOrgStructure.infisCode AS USL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL(EventType_Identification.value, PersonOrgStructure.tfomsCode)) AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS USL_PROFIL,
            '' AS USL_VID_VME,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            Event.setDate AS USL_DATE_IN,
            Event.execDate AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            {serviceCode} AS USL_CODE_USL,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                Account_Item.amount) AS USL_KOL_USL,
            Account_Item.price AS USL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35') AND rbEventProfile.regionalCode = '5',
                0, Account_Item.`sum`) AS USL_SUMV_USL,
            rbSpeciality.federalCode AS USL_PRVS,
            Person.federalCode AS USL_IDDOKT,
            IF(rbEventProfile.regionalCode = '2', VisitPerson.federalCode,
                Person.federalCode) AS USL_CODE_MD,

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
            TRIM(ClientDocument.number) AS PERS_DOCNUM,
            RegKLADR.OCATD AS PERS_OKATOG,
            LocKLADR.OCATD AS PERS_OKATOP,

            rbEventProfile.regionalCode AS eventProfileRegionalCode,
            DeliveredBy.value AS delivered,
            Account_Item.serviceDate AS serviceDate,
            Visit.id AS visitId,
            Account_Item.action_id AS actionId,
            Visit.date AS visitDate,
            rbDocumentType.code AS documentTypeCode,
            ClientDocument.date AS documentDate,
            Contract_Tariff.tariffType,
            Action.amount AS actionAmount,
            EXISTS(
                SELECT NULL FROM ClientDocument AS CD
                LEFT JOIN rbDocumentType ON CD.documentType_id = rbDocumentType.id
                WHERE CD.client_id= Client.id AND rbDocumentType.regionalCode = '3'
                    AND CD.deleted = 0
                LIMIT 1
            ) AS 'isAnyBirthDoc'""".format(serviceCode=serviceCode)
        tables = u"""Account_Item
            LEFT JOIN Event AS FirstEvent ON
                FirstEvent.id = Account_Item.event_id
            LEFT JOIN Event ON Event.id  = getLastEventId(FirstEvent.id)
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE rbDTG.code = '1'
                                           AND CD.client_id = Client.id
                                           AND CD.date <= Event.execDate
                                           AND CD.deleted=0)
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
            LEFT JOIN mes.MES ON FirstEvent.MES_id = mes.MES.id
            LEFT JOIN mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
            LEFT JOIN rbMedicalAidProfile AS ServiceProfileMedicalAidProfile ON ServiceProfileMedicalAidProfile.id = rbService_Profile.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbEventProfile ON rbEventProfile.id = EventType.eventProfile_id
            LEFT JOIN (
                    SELECT A.event_id, SUM(A.amount) AS amount, COUNT(DISTINCT A.id) AS cnt
                    FROM Action A
                    WHERE A.deleted = 0 AND
                              A.actionType_id IN (
                                    SELECT MAX(AT.id)
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='moving'
                              )
                      AND DATE(A.begDate) != DATE(A.endDate)
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
            LEFT JOIN mes.mrbService AS InvoiceMesService ON InvoiceMesService.id = (
                SELECT mes.mrbService.id
                FROM mes.MES_service MS
                LEFT JOIN mes.mrbService ON mes.mrbService.id = MS.service_id
                    AND mes.mrbService.deleted = 0
                WHERE MS.deleted = 0 AND MS.master_id = Event.MES_id
                LIMIT 0, 1
            )
            LEFT JOIN MKB AS MesMKB ON MesMKB.DiagId = (
                SELECT MM.mkb
                FROM mes.MES_mkb MM
                WHERE MM.master_id = Event.MES_id AND MM.deleted = 0
                LIMIT 0, 1
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
                LEFT JOIN Event E ON E.id = A.event_id
                WHERE E.client_id = Client.id
                  AND A.deleted = 0
                  AND MONTH(A.endDate) = '{month}'
                  AND YEAR(A.endDate) = '{year}'
                  AND A.status = 2
                  AND A.actionType_id = (
                    SELECT MAX(AT.id)
                    FROM ActionType AT
                    WHERE AT.flatCode ='inspection_mse'
                  )
            )
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
        """.format(month=settleDate.month(), year=settleDate.year())

        orderBy = u'Client.id, Event.id, FirstEvent.id'
        return (select, tables, where, orderBy)


    def getChildNumber(self, clientId, birthDate):
        u"""У новорожденного пациента должна быть указана представительская
            связь с матерью. Если у матери имеется несколько связей с разными
            пациентами, при этом дата рождения этих пациентов одинаковая,
            требуется этим пациентам "присвоить" порядковый номер. У ребенка,
            у которого самый маленький client.id, будет Н=1, у кого id больше,
            будет Н=2, у которого еще больше, будет Н=3.  Если у матери один
            новорожденный ребенок (нет других связанных пациентов с такой же
            psps датой рождения), то выгружаем Н=1, соответственно."""

        result = 1
        stmt = """SELECT DISTINCT Client.id
            FROM ClientRelation
            LEFT JOIN  Client ON Client.id = ClientRelation.relative_id
            WHERE ClientRelation.client_id = (
                    SELECT ClientRelation.client_id
                    FROM ClientRelation
                    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id = rbRelationType.id
                    WHERE ClientRelation.deleted = 0
                      AND ClientRelation.relative_id = {clientId}
                      AND rbRelationType.isDirectRepresentative
                    UNION
                    SELECT ClientRelation.relative_id
                    FROM ClientRelation
                    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id = rbRelationType.id
                    WHERE ClientRelation.deleted = 0
                      AND ClientRelation.client_id = {clientId}
                      AND rbRelationType.isBackwardRepresentative
                )
              AND Client.birthDate = '{birthDate}'
              AND ClientRelation.deleted = 0
            ORDER BY Client.id""".format(
                clientId=clientId, birthDate=birthDate.toString(Qt.ISODate))

        query = self._db.query(stmt)
        childIdList = []

        while query.next():
            record = query.record()
            childIdList.append(forceRef(record.value(0)))

        if clientId in childIdList:
            result = childIdList.index(clientId) + 1

        return result


    def getTempInvalidInfo(self):
        u'Получает информацию о больничных'
        stmt = """SELECT Event.client_id, rbTempInvalidRegime.code
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON
            rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN TempInvalid ON TempInvalid.id = (
                SELECT TI.id
                FROM TempInvalid TI
                LEFT JOIN rbTempInvalidResult ON
                    rbTempInvalidResult.id = TI.result_id
                WHERE TI.client_id = Event.client_id
                  AND TI.deleted = 0
                  AND TI.type = 1
                  AND rbTempInvalidResult.code = 1
                  AND (TI.begDate BETWEEN Event.setDate AND Event.execDate)
                LIMIT 1
            )
        LEFT JOIN rbTempInvalidRegime ON
            TempInvalid.disability_id = rbTempInvalidRegime.id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
              )
          AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))
        query = self._db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            clientId = forceRef(record.value(0))
            val = forceString(record.value(1))[1:]
            result[clientId] = val

        return result


    def getKsgKpgInfo(self):
        u'Получает информацию о КСГ, КПГ'
        fieldList = ('KSG_KPG_CRIT', 'KSG_KPG_DKK2', 'SL_P_CEL',
                     'bedProfileCode', 'SL_KD', 'Z_SL_VB_P',
                     'medicalAidTypeCode')
        stmt = """SELECT Event.id AS eventId,
        getLastEventId(Event.id) AS lastEventId,
        rbMedicalAidType.code AS medicalAidTypeCode,
        (SELECT GROUP_CONCAT(AT.code)
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.group_id IN (
                            SELECT id FROM ActionType AT1
                            WHERE AT1.flatCode IN ('codeSH', 'crit', 'DiapFR'))
                WHERE A.event_id = Event.id AND A.deleted = 0
        )  AS KSG_KPG_CRIT,
        IF(MesActionService.id != MesActionService2.id AND
            rbMedicalAidType.regionalCode != '3' AND
               SUBSTR(MesActionService2.infis, 1, 2) IN ('sh', 'it', 'rb'),
               MesActionService2.infis,
               NULL) AS KSG_KPG_DKK2,
        IF(rbMedicalAidType.regionalCode = '3',
            IF(rbMedicalAidType.code IN ('6', '9'),
                EventType_Identification.value, '1.3'), NULL) AS SL_P_CEL,
        BedProfile.value AS bedProfileCode,
        IF(rbMedicalAidType.code IN (1, 2, 3, 7),
            IF(HospitalAction.cnt = 1 AND HospitalAction.amount = 0, 1,
                HospitalAction.amount) + IF(
                    rbEventProfile.regionalCode = '3' AND
                    HospitalAction.cnt > 1, 1, 0),
            '') AS SL_KD,
        IF(rbMedicalAidType.code IN (1, 2, 3, 7),
            IF(NextEvent.id IS NOT NULL OR Event.prevEvent_id IS NOT NULL,
                1, ''), '') AS Z_SL_VB_P
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON
            rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbEventProfile ON
            rbEventProfile.id = EventType.eventProfile_id
        LEFT JOIN EventType_Identification ON
                EventType_Identification.master_id = EventType.id
                AND EventType_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'tfomsPCEL'
            )
        LEFT JOIN ActionType AS MesAT ON MesAT.id = (
            SELECT MAX(AT.id)
            FROM Action A
            LEFT JOIN ActionType AT ON A.actionType_id = AT.id
            LEFT JOIN rbService RS ON RS.id = AT.nomenclativeService_id
            LEFT JOIN mes.mrbService S ON S.code = RS.code
            WHERE A.deleted = 0 AND S.id IS NOT NULL
              AND A.event_id = Account_Item.event_id)
        LEFT JOIN rbService AS MesActionService ON MesActionService.id =
            MesAT.nomenclativeService_id
        LEFT JOIN ActionType AS MesAT2 ON MesAT2.id = (
            SELECT MIN(AT.id)
            FROM Action A
            LEFT JOIN ActionType AT ON A.actionType_id = AT.id
            LEFT JOIN rbService RS ON RS.id = AT.nomenclativeService_id
            LEFT JOIN mes.mrbService S ON S.code = RS.code
            WHERE A.deleted = 0 AND S.id IS NOT NULL
              AND A.event_id = Account_Item.event_id)
        LEFT JOIN rbService AS MesActionService2 ON MesActionService2.id =
            MesAT2.nomenclativeService_id
        LEFT JOIN (
            SELECT A.event_id,
                SUM(CASE
                    WHEN DATEDIFF(A.endDate, A.begDate) != 0 AND
                         TIMESTAMPDIFF(DAY, A.begDate, A.endDate) = 0 THEN 1
                    ELSE DATEDIFF(A.endDate, A.begDate)
                END) AS amount,
                COUNT(DISTINCT A.id) AS cnt, MAX(A.id) AS id
            FROM Action A
            WHERE A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='moving')
            GROUP BY A.event_id
        ) AS HospitalAction ON HospitalAction.event_id = Account_Item.event_id
        LEFT JOIN ActionProperty_rbHospitalBedProfile AS BedProfile
            ON BedProfile.id = (
                SELECT MAX(HBP.id)
                FROM ActionProperty
                LEFT JOIN ActionProperty_rbHospitalBedProfile AS HBP
                    ON HBP.id = ActionProperty.id
                WHERE action_id = HospitalAction.id
            )
        LEFT JOIN rbMedicalAidType ON
            rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN Event AS NextEvent ON NextEvent.prevEvent_id = Event.id
        LEFT JOIN Diagnostic ON Diagnostic.id = (
            SELECT MAX(dc.id)
                FROM Diagnostic dc
                WHERE dc.event_id = Account_Item.event_id
                AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                AND dc.deleted = 0
        )
        LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL
                   AND rbPayRefuseType.rerun != 0))
          AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))

        query = self._db.query(stmt)
        result = {}
        completeEventSummary = {}
        eventIdList = []

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            val = {}

            for field in fieldList:
                val[field] = None if record.isNull(field) else forceString(
                    record.value(field))

            if val['SL_KD']:
                _kd = forceInt(val['SL_KD'])
                _id = forceRef(record.value('lastEventId'))

                if completeEventSummary.has_key(_id) and _id not in eventIdList:
                    completeEventSummary[_id] += _kd
                elif _id not in completeEventSummary.keys():
                    completeEventSummary[_id] = _kd

                if _id not in eventIdList:
                    eventIdList.append(_id)

            if val.get('KSG_KPG_CRIT'):
                val['KSG_KPG_CRIT'] = val['KSG_KPG_CRIT'].split(',')

            result[eventId] = val

        for key in result:
            if completeEventSummary.has_key(key):
                result[key]['Z_SL_KD_Z'] = completeEventSummary[key]

        return result


    def _getCompleteEventCount(self, includeOnkology):
        u"""Возвращает строкой количество событий в счете."""

        result = tuple()
        stmt = """SELECT COUNT(DISTINCT eventId), SUM(`sum`)
FROM
    (SELECT getLastEventId(Account_Item.event_id) AS eventId,
            (SELECT MAX(ds.id) IS NOT NULL
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code IN ('1','2','9'))
                  AND dc.event_id = Account_Item.event_id
                  AND (SUBSTR(ds.MKB,1,1) = 'C' OR SUBSTR(ds.MKB,1,3) between 'D01' and 'D06')
            ) AS isOnkology,
            Account_Item.sum
    FROM Account_Item
    WHERE {0}) A
WHERE isOnkology {1} 0""".format(
    self.tableAccountItem['id'].inlist(self.idList),
    '!=' if includeOnkology else '=')

        query = self.db.query(stmt)

        if query.first():
            record = query.record()
            result = forceString(record.value(0)), forceDouble(record.value(1))

        return result


    def getCompleteEventCount(self):
        u"""Возвращает строкой количество событий без онкологии в счете."""
        (result, _) = self._getCompleteEventCount(False)
        return result


    def getTotalSum(self):
        u"""Возвращает сумму событий без онкологии в счете."""
        (_, result) = self._getCompleteEventCount(False)
        return result


class CR45ExportPage2(CExportPage2):
    u'Вторая страница мастера экспорта'

    def __init__(self, parent, prefix):
        CExportPage2.__init__(self, parent, prefix)


    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(),
                    self._parent.getPersonalDataFullXmlFileName())
        zipFileName = self._parent.getFullZipFileName()
        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class CR45XmlStreamWriterCommon(XmlStreamWriter, CExportHelperMixin):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'MCOD', 'SMO_NAM', 'INV', 'MSE', 'NOVOR')

    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD', 'NPR_DATE', 'NPR_MO')

    completeEventDateFields2 = ('NPR_DATE', )
    completeEventDateFields1 = ('DATE_Z_1', 'DATE_Z_2')
    completeEventDateFields = (completeEventDateFields1 +
                               completeEventDateFields2)
    completeEventFields1 = (('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO')
                            + completeEventDateFields2 + ('LPU', )
                            + completeEventDateFields1 +
                            ('KD_Z', 'VNOV_M', 'RSLT', 'ISHOD', 'OS_SLUCH',
                             'VB_P'))
    completeEventFields2 = ('IDSP', 'SUMV', 'OPLATA')
    completeEventFields = completeEventFields1 + completeEventFields2

    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields1 = (('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                     'P_CEL', 'NHISTORY', 'P_PER')
                    + eventDateFields +
                    ('KD', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK', 'DN',
                     'CODE_MES1', 'CODE_MES2', 'NAPR', 'CONS', 'ONK_SL',
                     'KSG_KPG'))
    eventFields2 = ('TELEMED', 'REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                    'SUM_M')
    eventFields = eventFields1 + eventFields2

    ksgSubGroup = {
        'SL_KOEF' : {'fields': ('IDSL', 'Z_SL')}
    }

    eventSubGroup = {
        'KSG_KPG': {'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG',
                               'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D',
                               'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                               'SL_KOEF'),
                    'subGroup': ksgSubGroup},
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME',
                      'DET') + serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL', 'PRVS',
                      'CODE_MD', 'NPL', 'COMENTU'))

    serviceSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_V', 'MET_ISSL', 'NAPR_USL'),
                 'dateFields': ('NAPR_DATE', )},
    }

    mapEventOrderToPPer = {5: '4', 7: '3'}
    mapEventOrderToForPom = {1: '3', 2: '1', 3: '1', 4: '3', 5: '3', 6: '2'}
    mapCharacterCode = {'4': '1', '2': '2', '3': '3', '1': '1'}

    def __init__(self, parent):
        XmlStreamWriter.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self._coefficientCache = {}
        self._recNum = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastCompleteEventId = None
        self._exportedNomenclativeServices = set()
        self._exportedActions = set()
        self._exportedEvents = set()


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeElement('VERSION', '3.1')
        self.writeElement('DATA', date.toString(Qt.ISODate))
        self.writeElement('FILENAME', params['shortFileName'][:-4])
        self.writeElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '%d' % params['accId'])
        self.writeElement('CODE_MO', params['lpuSmoCode'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeElement('NSCHET', params['accNumber'])
        self.writeElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeElement('PLAT', params['payerCode'])
        self.writeElement('SUMMAPR', '0')
        self.writeElement('SUMMAV', forceString(self._parent.getTotalSum()))
        self.writeEndElement() # SCHET

        self._recNum = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastCompleteEventId = None
        self._lastRecord = None
        self._exportedNomenclativeServices = set()
        self._exportedActions = set()
        self._exportedEvents = set()


    def writeRecord(self, record, params):
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        lastEventId = forceRef(record.value('lastEventId'))

        if (clientId != self._lastClientId or
                lastEventId != self._lastCompleteEventId):
            if self._lastClientId:
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                self._lastRecord,
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self._recNum += 1
            self.writeTextElement('N_ZAP', forceString(self._recNum))
            self.writeTextElement('PR_NOV', params['isReexposed'])
            self.writeClientInfo(record, params)

            self._lastClientId = clientId
            self._lastEventId = None
            params['birthDate'] = forceDate(record.value('PERS_DR'))
            execDate = forceDate(record.value('USL_DATE_OUT'))
            params['isJustBorn'] = params['birthDate'].daysTo(execDate) < 28
            params['isAnyBirthDoc'] = forceBool(record.value('isAnyBirthDoc'))
            self._lastCompleteEventId = None

        XmlStreamWriter.writeRecord(self, record, params)


    def writeEventInfo(self, record, params):
        eventId = forceRef(record.value('eventId'))

        if eventId == self._lastEventId:
            return

        eventProfileCode = forceInt(record.value('eventProfileRegionalCode'))

        if eventProfileCode not in (1, 3):
            record.setNull('SL_CODE_MES1')

        if forceInt(record.value('tariffType')) != 9:
            record.setValue('SL_TARIF',
                            toVariant(params['mapEventIdToSum'].get(eventId)))

        record.setValue('SL_SUM_M',
                        toVariant(params['mapEventIdToSum'].get(eventId)))
        record.setValue('SL_NHISTORY', toVariant(eventId))

        for field in ('SL_DS0', 'SL_DS1', 'SL_DS3'):
            record.setValue(field,
                            toVariant(forceString(record.value(field))[:5]))

        params['eventProfileRegionalCode'] = forceInt(record.value(
            'eventProfileRegionalCode'))
        params['idsp'] = forceInt(record.value('Z_SL_IDSP'))
        eventOrder = forceInt(record.value('eventOrder'))

        local_params = {
            'SL_VERS_SPEC': 'V021',
        }
        local_params.update(params['mapEventIdToKsgKpg'].get(eventId, {}))
        params['isHospital'] = local_params['medicalAidTypeCode'] in (
            '1', '2', '3', '7')

        if params['isHospital']:
            local_params['SL_EXTR'] = (forceString(
                eventOrder) if eventOrder in (1, 2)  else '')
            local_params['SL_P_PER'] = self.mapEventOrderToPPer.get(
                eventOrder)

            if not local_params['SL_P_PER']:
                delivered = forceString(record.value('delivered')) == u'СМП'
                local_params['SL_P_PER'] = '2' if delivered else '1'

        idsp = params['idsp']
        if params['emergencyIncomplete'] and idsp == 31:
            record.setValue('SL_SUM_M', toVariant(0))

        if forceInt(record.value('Z_SL_USL_OK')) in (1, 2, 3):
            characterId = forceRef(record.value('SL_C_ZAB'))
            record.setValue('SL_C_ZAB', toVariant(self.mapCharacterCode.get(
                CDiseaseCharacterCodeCache.getCode(characterId))))

        local_params.update(params)
        params['USL_IDSERV'] = 0

        if self._lastEventId:
            self.writeEndElement() # SL

        if params['isHospital']:
            bedProfileCode = local_params['bedProfileCode']
            if bedProfileCode:
                local_params['SL_PROFIL_K'] = (
                    self.getHospitalBedProfileTfomsCode(bedProfileCode))

            local_params['KSG_KPG_VER_KSG'] = params['settleDate'].year()
            local_params['KSG_KPG_BZTSZ'] = (
                self._parent.contractAttributeByType(
                    u'BZTSZ_ДС' if local_params['medicalAidTypeCode'] == '7'
                    else u'BZTSZ_КС'))
            local_params['KSG_KPG_KOEF_U'] = (
                self._parent.contractAttributeByType(
                    u'KOEF_U_ДС' if local_params['medicalAidTypeCode'] == '7'
                    else u'KOEF_U_КС'))
            local_params.update(self.getCoefficients(record, params))

        local_params['SL_DS2'] = forceString(record.value('ds2List')).split(',')
        local_params.update(params.get('onkologyInfo', {}).get(eventId, {}))

        if local_params.get('isOnkology'):
            fieldName = ('USL_CODE_USL' if local_params.get('ONK_USL_USL_TIP')
                         in (1, 3, 4) else 'mesServiceCode')
            record.setValue('USL_VID_VME', record.value(fieldName))
            mkb = forceString(record.value('SL_DS1'))[:3]

            if mkb == 'C73' or (mkb >= 'C81' and mkb <= 'C96'):
                local_params['LEK_PR_CODE_SH'] = [u'нет']*len(
                    local_params.get('LEK_PR_CODE_SH', []))

        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('SL', self.eventFields, _record, self.eventSubGroup,
                        closeGroup=False, dateFields=self.eventDateFields)
        self._lastEventId = eventId


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))
        patrName = forceString(record.value('PERS_OT'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'

        local_params = {}
        local_params.update(params['mapEventIdToKsgKpg'].get(lastEventId, {}))

        code = forceInt(record.value('eventProfileRegionalCode'))
        eventId = forceRef(record.value('eventId'))
        onkologyInfo = params.get('onkologyInfo', {}).get(eventId, {})
        isOnkology = onkologyInfo.get('isOnkology')
        isSuspicion = onkologyInfo.get('SL_DS_ONK')

        if not (code in (1, 3) or isOnkology or isSuspicion):
            record.setNull('Z_SL_NPR_DATE')
            record.setNull('Z_SL_NPR_MO')

        local_params['Z_SL_SUMV'] = params['completeEventSum'].get(lastEventId)
        local_params['Z_SL_FOR_POM'] = self.mapEventOrderToForPom.get(
            forceInt(record.value('eventOrder')), '')
        local_params['Z_SL_OS_SLUCH'] = ('2' if (noPatrName or (
            params['isJustBorn'] and not params['isAnyBirthDoc'])) else '')
        _record = CExtendedRecord(record, local_params, DEBUG)
        XmlStreamWriter.writeCompleteEvent(self, _record, params)


    def writeService(self, record, params):
        # Если профиль события Стационар или Дневной стационар
        # (т.е. Account_Item.event_id -> Event.eventType_id->
        # EventType.eventProfile_id -> rbEventProfile.regionalCode = 1 или 3)
        # блок <USL> выгружается только в случае, если в событии присутствует
        # мероприятие, у которого Action.actionType_id ->
        # ActionType.service_id -> rbService. code = mes.mrbService.code
        # (какой-либо услуге из mrbService), при этом CODE_USL =
        # ActionType.service_id-> rbService.infis (TARIF и SUMV_USL при этом
        # принимают значение 0).
        eventProfileCode = forceInt(record.value('eventProfileRegionalCode'))
        medicalAidTypeCode = forceInt(record.value('medicalAidTypeCode'))
        isHospital = eventProfileCode in (1, 3)
        isAmbulance = medicalAidTypeCode == 3
        isStomatology = eventProfileCode == 6
        eventId = forceRef(record.value('eventId'))
        idsp = params['idsp']

        if idsp == 28:
            record.setValue('USL_VID_VME', record.value('USL_CODE_USL'))

        if isHospital:
            actionServiceCodeList = []

            if (eventId and
                    eventId not in self._exportedActions):
                actionServiceCodeList = self.getActionServiceCodeList(eventId)

            if actionServiceCodeList:
                for code, amount, begDate, endDate in actionServiceCodeList:
                    if forceString(code)[:2] in ('it', 'sh', 'rb', ''):
                        continue

                    record.setValue('USL_CODE_USL', code)
                    record.setValue('USL_KOL_USL', amount)
                    record.setValue('USL_DATE_IN', begDate)
                    record.setValue('USL_DATE_OUT', endDate)
                    record.setValue('USL_TARIF', toVariant(0))
                    record.setValue('USL_SUMV_USL', toVariant(0))

                    if (params.get('onkologyInfo', {}).get(eventId, {}).get(
                            'ONK_USL_USL_TIP') in (1, 3, 4)):
                        record.setValue('USL_VID_VME', code)

                    _record = CExtendedRecord(record, params, DEBUG)
                    params['USL_IDSERV'] += 1
                    self.writeGroup('USL', self.serviceFields, _record,
                                    subGroup=self.serviceSubGroup,
                                    dateFields=self.serviceDateFields)

            self._exportedActions.add(eventId)

            if not forceRef(record.value('actionId')):
                return

            record.setValue('USL_KOL_USL', record.value('actionAmount'))

        if ((params['ambulanceIncomplete'] and idsp in (26, 27))
                or (params['emergencyIncomplete'] and idsp == 31)):
            record.setValue('USL_SUMV_USL', toVariant(0))

        record.setValue('USL_DS',
                        toVariant(forceString(record.value('USL_DS'))[:5]))

        if not forceRef(record.value('visitId')):
            params['USL_IDSERV'] += 1

            if isAmbulance or isStomatology or isHospital:
                record.setValue('USL_DATE_IN', record.value('serviceDate'))
                record.setValue('USL_DATE_OUT', record.value('serviceDate'))

            _record = CExtendedRecord(record, params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            subGroup=self.serviceSubGroup,
                            dateFields=self.serviceDateFields)
        else:
            self.writeVisits(record, params, eventId, isAmbulance,
                             isStomatology)

        if ((isStomatology or isAmbulance) and
                eventId not in self._exportedNomenclativeServices):
            self.writeNomenclativeServices(record, eventId, isStomatology,
                                           params)


    def writeNomenclativeServices(self, record, eventId, isStomatology, params):
        u'Записывает информацию о номенклатурных услугах'
        serviceList = exportNomenclativeServices(self._parent.db, eventId,
                                                 params['actionList'])

        for (code, begDate, endDate, childUetDoctor,
             adultUetDoctor) in serviceList:
            record.setValue('USL_CODE_USL', code)
            record.setValue('USL_DATE_IN', begDate)
            record.setValue('USL_DATE_OUT', endDate)
            record.setValue('USL_TARIF', toVariant(0))
            record.setValue('USL_SUMV_USL', toVariant(0))

            if isStomatology:
                amount = forceDouble(record.value('amount'))
                coeff = (childUetDoctor if forceBool(record.value(
                    'SL_DET')) else adultUetDoctor)
                record.setValue('USL_KOL_USL', toVariant(amount*coeff))

            _record = CExtendedRecord(record, params, DEBUG)
            params['USL_IDSERV'] += 1
            self.writeGroup('USL', self.serviceFields, _record,
                            subGroup=self.serviceSubGroup,
                            dateFields=self.serviceDateFields)

        self._exportedNomenclativeServices.add(eventId)


    def writeVisits(self, record, params, eventId, isAmbulance, isStomatology):
        u'Выгружает визиты по заданному событию'
        if eventId and eventId not in self._exportedEvents:
            params['tarif'] = record.value('SL_TARIF')
            params['sum'] = record.value('SL_SUM_M')
            params['amount'] = record.value('SL_ED_COL')
            visitRecords = self.exportVisits(eventId, params)

            if isAmbulance or isStomatology:
                if visitRecords:
                    first = QSqlRecord(visitRecords[0])
                    first.setValue('USL_DATE_IN', record.value('SL_DATE_1'))
                    first.setValue('USL_DATE_OUT', record.value('SL_DATE_2'))
                    first.setValue('USL_TARIF', record.value('USL_TARIF'))
                    first.setValue('USL_SUMV_USL', record.value('USL_SUMV_USL'))
                    self.writeService(first, params)
                    visitRecords.pop(0)
                else:
                    record.setValue('USL_DATE_IN', record.value('visitDate'))
                    record.setValue('USL_DATE_OUT', record.value('visitDate'))
                    _record = CExtendedRecord(record, params, DEBUG)
                    params['USL_IDSERV'] += 1
                    self.writeGroup('USL', self.serviceFields, _record,
                                    subGroup=self.serviceSubGroup,
                                    dateFields=self.serviceDateFields)

            modifier = parseModifier(params['serviceModifier'])
            for visit in visitRecords:
                if isAmbulance or isStomatology:
                    code = forceString(visit.value('USL_CODE_USL'))
                    visit.setValue('USL_CODE_USL',
                                   applyModifier(code, modifier))
                self.writeService(visit, params)

            self._exportedEvents.add(eventId)


    def exportVisits(self, eventId, _):
        u"""Экспортирует данные для визитов с 0 стоимостью,
            при тарификации по посещениям"""
        stmt = u"""SELECT
            PersonOrganisation.miacCode AS USL_LPU,
            ExecPersonOrgStructure.infisCode AS USL_LPU_1,
            PersonOrgStructure.tfomsCode AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                ServiceProfileMedicalAidProfile.code,
                    ServiceMedicalAidProfile.code) AS USL_PROFIL,
            '' AS USL_VID_VME,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            Visit.date AS USL_DATE_IN,
            Visit.date AS USL_DATE_OUT,
            Diagnosis.MKB AS USL_DS,
            IF(rbService.infis IS NULL OR rbService.infis = '',
                rbService.code, rbService.infis) AS USL_CODE_USL,
            1 AS USL_KOL_USL,
            0 AS USL_TARIF,
            0 AS USL_SUMV_USL,
            rbSpeciality.federalCode AS USL_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.federalCode AS USL_CODE_MD
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
        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
        WHERE Visit.event_id = %d
            AND Visit.deleted = '0'
        ORDER BY Visit.date""" % eventId

        query = self._parent.db.query(stmt)
        result = []

        while query.next():
            result.append(query.record())

        return result


    def getActionServiceCodeList(self, eventId):
        u'Возвращает список действий по событию.'

        stmt = u"""SELECT RS.infis, A.amount, A.begDate, A.endDate
            FROM Action A
            LEFT JOIN ActionType AT ON A.actionType_id = AT.id
            LEFT JOIN rbService RS ON RS.id = AT.nomenclativeService_id
            LEFT JOIN mes.mrbService S ON S.id = (
                SELECT MAX(id)
                FROM mes.mrbService
                WHERE mes.mrbService.code = RS.code
            )
            WHERE A.deleted = 0 AND S.id IS NOT NULL
              AND A.event_id = {eventId}
        """.format(eventId=eventId)

        query = self._parent.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            if record:
                result.append((record.value(0), record.value(1),
                               record.value(2), record.value(3)))

        return result


    def getCoefficientRegionalCode(self, name):
        u'Возвращает региональный код коэффициента по его имени'
        result = self._coefficientCache.get(name, -1)

        if result == -1:
            result = forceString(self._parent.db.translate(
                'rbContractCoefficientType', 'name', name, 'regionalCode'))
            self._coefficientCache[name] = result

        return result


    def writeElement(self, elementName, value=None):
        u"""Если тег в списке обязательных, выгружаем его пустым"""
        if value or (elementName in self.requiredFields):
            if isinstance(value, QDate):
                XmlStreamWriter.writeTextElement(self, elementName,
                                                 value.toString(Qt.ISODate))
            elif isinstance(value, int):
                XmlStreamWriter.writeTextElement(self, elementName,
                                                 forceString(value))
            else:
                XmlStreamWriter.writeTextElement(self, elementName, value)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        birthDate = forceDate(record.value('PERS_DR'))
        execDate = forceDate(record.value('SL_DATE_2'))
        documentTypeCode = forceString(record.value('documentTypeCode'))
        documentDate = forceDate(record.value('documentDate'))

        if (birthDate.isValid() and execDate.isValid() and
                (documentTypeCode != '3' or
                 (documentTypeCode == '3' and documentDate > execDate)) and
                (birthDate.daysTo(execDate) <= 28)):
            # ЕСЛИ возраст пациента <=28 дней на момент окончания события
            # (Event.execDate) И в ClientDocument отсутствует свидетельство о
            # рождении (documentType_id->rbDocumentType.code=3) в период
            # действия которого попадает дата окончания события. (отсутствует
            # ClientDocument, где ClientDocument.date<=Event.execDate)

            # ТО тег заполняется следующим образом: ПДДММГГН, где П - пол
            # ребенка (Client.sex) ДД - день рождения; ММ - месяц рождения;ГГ -
            # последние две цифры года рождения; (из Client.birthDate)

            childNumber = self._parent.getChildNumber(forceRef(record.value(
                'clientId')), birthDate)

            record.setValue('PACIENT_NOVOR', toVariant(u'{sex}{date}{n}'.format(
                sex=forceString(record.value('PERS_W')),
                date=birthDate.toString('ddMMyy'),
                n=childNumber)))
            params['isNewBorn'] = True

        clientId = forceRef(record.value('clientId'))
        local_params = {
            'PACIENT_INV': params['tempInvalidMap'].get(clientId, '')
        }
        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def getCoefficients(self, record, _):
        u"""Пишет блок SL_KOEF"""
        def formatCoef(val):
            u'Обрезает значение коэффициента до 5 знаков без округления'
            _rc = '%.50f' % val
            return _rc[:_rc.index('.')+6]

        usedCoefficients = forceString(record.value('usedCoefficients'))
        result = {'KSG_KPG_SL_K' : 0}
        isItSlNeq1 = False

        if usedCoefficients:
            coefficientList = json.loads(usedCoefficients)
            flag = False

            for _, i in coefficientList.iteritems():
                for key, val in i.iteritems():
                    if key == u'__all__':
                        continue

                    result['KSG_KPG_SL_K'] = 1 if val > 1 else 0
                    isItSlNeq1 = val != 1

                    if val > 1:
                        result['KSG_KPG_IT_SL'] = formatCoef(val)
                        flag = True
                        break

                if flag:
                    break

            if isItSlNeq1:
                for _, i in coefficientList.iteritems():
                    for key, val in i.iteritems():
                        if key == u'__all__':
                            continue

                        code = self.getCoefficientRegionalCode(key)

                        if code:
                            result.setdefault('SL_KOEF_IDSL', []).append(code)
                            result.setdefault(
                                'SL_KOEF_Z_SL', []).append(formatCoef(val))

        return result

# ******************************************************************************

class CR45PersonalDataWriter(PersonalDataWriter, CExportHelperMixin):
    u"""Осуществляет запись данных экспорта в XML"""

    representativeDateFields = ('DR_P', )
    clientDateFields = (PersonalDataWriter.clientDateFields +
                        representativeDateFields)
    clientFields = (('ID_PAC', 'FAM', 'IM', 'OT', 'W',) +
                    PersonalDataWriter.clientDateFields +
                    ('DOST', 'TEL', 'FAM_P', 'IM_P', 'OT_P', 'W_P', ) +
                    representativeDateFields +
                    ('DOST_P', 'MR', 'DOCTYPE', 'DOCSER', 'DOCNUM', 'SNILS',
                     'OKATOG', 'OKATOP'))


    def __init__(self, parent):
        PersonalDataWriter.__init__(self, parent)
        self.version = '3.1'
        CExportHelperMixin.__init__(self)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""
        local_params = {}

        # ЕСЛИ возраст пациента <60 дней И в ClientDocument отсутствует
        # свидетельство о рождении (documentType_id->rbDocumentType.code=3)
        # ТО выгружаем данные представителя
        if params.get('isNewBorn'):
            clientId = forceRef(record.value('clientId'))
            representative = self.getClientRepresentativeInfo(clientId)

            if representative:
                local_params['PERS_FAM_P'] = representative['lastName']
                local_params['PERS_IM_P'] = representative['firstName']
                local_params['PERS_OT_P'] = representative['patrName']
                local_params['PERS_W_P'] = representative['sex']
                local_params['PERS_DR_P'] = representative['birthDate']
                record.setValue('PERS_MR',
                                toVariant(representative['birthPlace']))
                nameProblems = []

                for (field, code) in (
                        (representative['patrName'], '1'),
                        (representative['lastName'], '2'),
                        (representative['firstName'], '3'),):
                    if not field or field.upper() == u'НЕТ':
                        nameProblems.append(code)

                local_params['PERS_DOST_P'] = nameProblems

        if forceString(record.value('PERS_DOCTYPE')) == '3':
            serial = forceString(record.value('PERS_DOCSER')).replace(' ', '-')
            record.setValue('PERS_DOCSER', toVariant(serial))

        local_params.update(params)
        PersonalDataWriter.writeClientInfo(self, record, local_params)

# ******************************************************************************

class CR45RegistryXmlStreamWriter(COrder79XmlStreamWriter):

    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields = ('IDCASE',) + eventDateFields
    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR')

    def __init__(self, parent):
        COrder79XmlStreamWriter.__init__(self, parent)


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeElement('VERSION', '2.2')
        self.writeElement('DATA', date.toString(Qt.ISODate))
        self.writeElement('FILENAME', params['shortFileName'][:-4])
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '%d' % params['accId'])
        self.writeElement('CODE_MO', params['lpuSmoCode'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('lastClientId'):
            if params.get('lastClientId'):
                # выгрузка незавершенных действий
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(clientId))
            self.writeTextElement('PR_NOV', params['isReexposed'])
            self.writeClientInfo(record, params)

            params['lastClientId'] = clientId
            params['lastEventId'] = None

        self.writeEventInfo(record, params)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        params['lastEventId'] = forceRef(record.value('eventId'))
        self.writeGroup('SLUCH', self.eventFields, record,
                        dateFields=self.eventDateFields)

# ******************************************************************************

class CR45XmlStreamWriter(CR45XmlStreamWriterCommon):

    conditionalFields = ('NPR_DATE', 'NPR_MO')
    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD')

    def __init__(self, parent):
        CR45XmlStreamWriterCommon.__init__(self, parent)
        self.__currentRecord = None


    def writeRecord(self, record, params):
        eventId = forceRef(record.value('eventId'))
        onkInfo = params['onkologyInfo'].get(eventId, {})
        self.__currentRecord = record

        if ((not onkInfo or not onkInfo.get('isOnkology')) and
                self._parent.registryType == CR45ExportPage1.registryTypeD1):
            CR45XmlStreamWriterCommon.writeRecord(self, record, params)


    def writeElement(self, elementName, value=None):
        u"""Если тег в списке обязательных, выгружаем его пустым"""
        if value or self.isRequired(elementName):
            if isinstance(value, QDate):
                XmlStreamWriter.writeTextElement(self, elementName,
                                                 value.toString(Qt.ISODate))
            elif isinstance(value, int):
                XmlStreamWriter.writeTextElement(self, elementName,
                                                 forceString(value))
            else:
                XmlStreamWriter.writeTextElement(self, elementName, value)


    def isRequired(self, fieldName):
        u'Проверяет нужно ли писать пустое поле'
        result = False

        if fieldName in self.requiredFields:
            result = True
        elif fieldName in self.conditionalFields:
            regionalCode = forceString(self.__currentRecord.value(
                'eventProfileRegionalCode'))
            result = regionalCode != '2'

        return result


# ******************************************************************************

class CDiseaseCharacterCodeCache(CDbEntityCache):
    mapIdToCode = {}

    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def getCode(cls, _id):
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            result = forceString(QtGui.qApp.db.translate(
                'rbDiseaseCharacter', 'id', _id, 'code'))
            cls.mapIdToCode[_id] = result
        return result

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR45Native,
                      u'A-9-3160',
                      '51_s11_20190716.ini')
