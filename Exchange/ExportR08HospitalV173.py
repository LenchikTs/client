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

u'Экспорт реестра в формате XML. Республика Калмыкия, стационар (Д1,4) V173'

import json
import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QDate
from PyQt4.QtSql import QSqlRecord

from library.DbEntityCache import CDbEntityCache
from library.Utils import (forceString, forceInt, toVariant, forceRef,
                           forceBool, forceDate, forceDouble)

from Events.Action import CAction

from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin, CAbstractExportPage1Xml,
                             CMultiRecordInfo)
from Exchange.Order200Export import (
    COnkologyInfo as COrder200OnkologyInfo, CTfomsNomenclatureCache)
from Exchange.ExportR08Hospital import exportNomenclativeServices
from Exchange.ExportR08HospitalV59 import getXmlBaseFileName
from Exchange.ExportR60NativeAmbulance import (PersonalDataWriter, CExportPage1,
                                               CExportPage2)
from Exchange.Order79Export import (
    COrder79v3XmlStreamWriter as XmlStreamWriter,
    COrder79ExportWizard, COrder79ExportPage1)
from Exchange.Utils import compressFileInZip
from RefBooks.Service.ServiceModifier import applyModifier, parseModifier

DEBUG = False

def exportR08HospitalV173(widget, accountId, accountItemIdList, _):
    u'Создает диалог экспорта реестра счета'

    wizard = CR08ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CR08ExportWizard(COrder79ExportWizard):
    u'Мастер экспорта для Калмыкии'

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии, стационар'
        prefix = 'R08HospitalV173'
        COrder79ExportWizard.__init__(self, title, prefix, CR08ExportPage1,
                                      CR08ExportPage2, parent)
        self.setWindowTitle(title)
        self.page1.setXmlWriter((CR08XmlStreamWriter(self.page1),
                                 CR08PersonalDataWriter(self.page1),
                                 CR08XmlStreamWriterD4(self.page1),
                                 CD4PersonalDataWriter(self.page1)))
        self.__xmlBaseFileName = None
        self.__xmlBaseFileNameNoPostfix = None
        self.__tmpDirD4 = None
        self.anyOnklogy = False


    def _getXmlBaseFileName(self, addPostfix=True):
        u'Возвращает имя файла для записи данных'
        result = self.__xmlBaseFileName if addPostfix else self.__xmlBaseFileNameNoPostfix

        if not result:
            result = getXmlBaseFileName(self.db, self.info,
                                        self.page1.edtPacketNumber.value(),
                                        addPostfix)
            if addPostfix:
                self.__xmlBaseFileName = result
            else:
                self.__xmlBaseFileNameNoPostfix = result

        return result


    def getD4XmlFileName(self, addPostfix=True):
        u'Возвращает имя файла для записи личных данных.'
        return u'C{0}'.format(self._getXmlBaseFileName(addPostfix))


    def getCOVID19XmlFileName(self, addPostfix=True):
        u'Возвращает имя файла для записи личных данных.'
        return u'HW{0}'.format(self._getXmlBaseFileName(addPostfix))


    def getD4FullXmlFileName(self):
        u'''Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getD4XmlFileName())


    def getCOVID19FullXmlFileName(self):
        u'''Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getCOVID19XmlFileName())


    def getZipFileName(self):
        u'''Возвращает имя архива'''
        return u'{0}.zip'.format(self.getXmlFileName()[:-4])


    def getD4ZipFileName(self):
        u'''Возвращает имя архива'''
        return u'{0}.zip'.format(self.getD4XmlFileName()[:-4])


    def getCOVID19ZipFileName(self):
        u'''Возвращает имя архива'''
        return u'{0}.zip'.format(self.getCOVID19XmlFileName()[:-4])


    def getD4FullZipFileName(self):
        u'''Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getD4ZipFileName())


    def getCOVID19FullZipFileName(self):
        u'''Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getCOVID19ZipFileName())


    def getCOVID19PersonalDataXmlFileName(self, addPostfix=True):
        u'''Возвращает имя файла для записи личных данных.'''
        return u'LW{0}'.format(self._getXmlBaseFileName(addPostfix))


    def getD4PersonalDataXmlFileName(self, addPostfix=True):
        u'''Возвращает имя файла для записи личных данных.'''
        return u'LC{0}'.format(self._getXmlBaseFileName(addPostfix))


    def getCOVID19PersonalDataFullXmlFileName(self):
        u'''Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(),
                            self.getCOVID19PersonalDataXmlFileName())


    def getD4PersonalDataFullXmlFileName(self):
        u'''Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getD4TmpDir(),
                            self.getD4PersonalDataXmlFileName())


    def getD4TmpDir(self):
        u'''Возвращает строку с путем к временному каталогу'''
        if not self.__tmpDirD4:
            self.__tmpDirD4 = QtGui.qApp.getTmpDir('D4')
        return self.__tmpDirD4

# ******************************************************************************

class CR08ExportPage1(CExportPage1):
    u'Первая страница мастера экспорта'
    registryTypeD1 = 0
    registryTypeD4 = 1
    registryTypeCOVID19 = 2

    def __init__(self, parent, prefix):
        CExportPage1.__init__(self, parent, prefix)
        self.lblRegistryType.setVisible(True)
        #self.cmbRegistryType.setEnabled(True)
        self.cmbRegistryType.setVisible(True)
        self.cmbRegistryType.clear()
        self.cmbRegistryType.addItems([u'Д1', u'Д4', u'COVID-19'])
        self.registryType = self.registryTypeD1

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
        actionList = []
        actionCount = {}
        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            actionId = forceString(record.value('actionId'))

            if actionId and actionId != '0':
                actionList.append(actionId)
                actionCount[eventId] = 1 + actionCount.get(eventId, 0)

        params['actionList']  = actionList
        params['actionCount'] = actionCount
        params['ambulanceIncomplete'] = not self.chkAmbulancePlanComplete.isChecked()
        params['emergencyIncomplete'] = not self.chkEmergencyPlanComplete.isChecked()

        query.exec_()


    def nschet(self, registryType, params):
        settleDate = params['settleDate']

        return u'{p}{year:02d}{month:02d}{registryNumber:d}'.format(
            p=params['lpuMiacCode'][-2:],
            year=settleDate.year() % 100,
            month=settleDate.month(),
            registryNumber=params['accId']
        )


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
        params['completeEventSum'] = self.getCompleteEventSum()
        params['mapEventIdToKsgKpg'] = self.getKsgKpgInfo()
        params['onkologyInfo'] = self.getOnkologyInfo()
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
        params['USL_KODLPU'] = params['lpuCode']

        if self.registryType in (self.registryTypeD1, self.registryTypeCOVID19):
            for _class, name in ((CImplantsInfo, 'implantsInfo'),
                                 (CMedicalSuppliesInfo, 'medicalSuppliesInfo')):
                info = _class()
                params[name] = info.get(
                    self.db, self.tableAccountItem['id'].inlist(self.idList),
                    self)

        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['mapEventIdToFksgCode'] = self.getFksgCode()
            params['SLUCH_COUNT'] = params['accNumber']
            params['NSCHET'] = self.nschet(self.registryType, params)
            self._parent.note = u'[NSCHET:%s]' % params['NSCHET']

        self._recNum = 1
        params['isInsurerPayCode60'] = False
        params['fileName'] = (self._parent.getCOVID19XmlFileName()
            if self.registryType == self.registryTypeCOVID19
            else self._parent.getXmlFileName())
        params['shortFileName'] = (self._parent.getCOVID19XmlFileName()
            if self.registryType == self.registryTypeCOVID19
            else self._parent.getXmlFileName())
        params['d4shortFileName'] = self._parent.getD4XmlFileName(False)

        if self.registryType == self.registryTypeCOVID19:
            params['personalDataFileName'] = (
                self._parent.getCOVID19PersonalDataXmlFileName())
        elif self.registryType == self.registryTypeD4:
            params['personalDataFileName'] = (
                self._parent.getD4PersonalDataXmlFileName(False))
        else:
            params['personalDataFileName'] = (
                self._parent.getPersonalDataXmlFileName())
        params['visitExportedEventList'] = set()
        params['toggleFlag'] = 0
        params['doneVis'] = set()
        params['useNomenclativeServiceCode'] = (
            self.chkUseNomenclativeService.isChecked())
        self.setProcessParams(params)

        outFile = QFile(self._parent.getCOVID19FullXmlFileName()
            if self.registryType == self.registryTypeCOVID19
            else self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(
            self._parent.getCOVID19PersonalDataFullXmlFileName()
            if self.registryType == self.registryTypeCOVID19
            else self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        d4PersonalDataFile = QFile(
            self._parent.getD4PersonalDataFullXmlFileName())
        d4PersonalDataFile.open(QFile.WriteOnly|QFile.Text)

        d4File = QFile(self._parent.getD4FullXmlFileName())
        d4File.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, d4Writer,
         d4PersonalDataWriter) = self.xmlWriter()

        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        d4Writer.setDevice(d4File)
        d4PersonalDataWriter.setDevice(d4PersonalDataFile)

        CAbstractExportPage1Xml.exportInt(self)


    def prepareStmt(self, params):
        (_, _, where, _) = CExportPage1.prepareStmt(
            self, params)

        serviceCode = (u'''IF(VisitCount.amount > 1
            AND (SELECT AT.serviceType FROM ActionType AT
                 WHERE AT.id = Action.actionType_id) IN (1, 2)
            AND Action.person_id = Event.execPerson_id,
            (SELECT S.code FROM  ActionType AT
             LEFT JOIN rbService S ON S.id = AT.nomenclativeService_id
             WHERE Action.actionType_id = AT.id
             LIMIT 0,1),
            IF(Account_Item.visit_id IS NOT NULL,
                VisitService.infis, rbService.infis))''' if params[
                    'useNomenclativeServiceCode'] else
            u'''IF(Account_Item.visit_id IS NOT NULL,
                VisitService.infis, rbService.infis)''')

        policyNumber = (u""" IF(rbPolicyKind.regionalCode IN ('1','2'),
               ClientPolicy.number, '')"""
               if self.registryType in (
                    self.registryTypeD1, self.registryTypeCOVID19)
               else u'ClientPolicy.number')
        select = u'''FirstEvent.id AS eventId,
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
            rbSpeciality.code AS specialityCode,
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
            {policyNumber} AS PACIENT_NPOLIS,
            IF(rbPolicyKind.regionalCode = '3',
               ClientPolicy.number, '') AS PACIENT_ENP,
            Insurer.miacCode AS PACIENT_SMO,
            IF(Insurer.miacCode IS NULL OR Insurer.miacCode = '',
                        Insurer.OGRN,'') AS PACIENT_SMO_OGRN,
            IF(Insurer.miacCode IS NULL OR Insurer.miacCode = '',
                        Insurer.OKATO,'') AS PACIENT_SMO_OK,
            IF((Insurer.miacCode IS NULL OR Insurer.miacCode = '')
                    AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                    Insurer.shortName, '') AS PACIENT_SMO_NAM,
            IF(MES_ksg.code IN ('st17.001', 'st17.002', 'st17.003'),
               Client.birthWeight, '') AS PACIENT_VNOV_D,
            0 AS PACIENT_NOVOR,
            IF((
                SELECT MBE.code FROM ActionProperty AP
                INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
                INNER JOIN ActionProperty_rbMedicalBoardExpertiseCharacter APV ON AP.id = APV.id
                INNER JOIN rbMedicalBoardExpertiseCharacter MBE ON MBE.id = APV.value
                WHERE APT.name = 'Характеристика экспертизы'
                  AND AP.deleted = 0
                  AND AP.action_id = (
                    SELECT MAX(A.id) FROM Action A
                    LEFT JOIN Event E ON E.id = A.event_id
                    WHERE E.client_id = Client.id
                    AND A.deleted = 0
                    AND A.actionType_id = (
                        SELECT MAX(AT.id)
                        FROM ActionType AT
                        WHERE AT.flatCode ='inspection_case'
                    )
                  )
                LIMIT 1
            ) = '3.01', 1, '') AS PACIENT_MSE,
            InvStatus.regionalCode AS PACIENT_INV,

            Event.id AS Z_SL_IDCASE,
            rbMedicalAidType.regionalCode AS Z_SL_USL_OK,
            IFNULL(OrgStructure_Identification.value,
                rbMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            RelegateOrg.infisCode AS Z_SL_NPR_MO,
            DATE(Event.srcDate) AS Z_SL_NPR_DATE,
            PersonOrganisation.miacCode AS Z_SL_LPU,
            FirstEvent.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            rbMedicalAidUnit.federalCode AS Z_SL_IDSP,
            IF(MES_ksg.code IN ('st17.001', 'st17.002'),
             (SELECT GROUP_CONCAT(Child.birthWeight) FROM ClientRelation
              LEFT JOIN Client AS Child ON Child.id = ClientRelation.relative_id
              WHERE ClientRelation.client_id = Client.id
                AND ClientRelation.deleted = 0
                AND ClientRelation.relativeType_id IN (
                 SELECT id FROM rbRelationType
                 WHERE code IN ('01','02'))), -- сын, дочь
             '') AS Z_SL_VNOV_M,

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
            (IF(Diagnosis.MKB IN ('U07.1','U07.2'),
            (SELECT APD.value FROM ActionProperty AP
             INNER JOIN Action ON AP.action_id = Action.id
             INNER JOIN ActionType AT ON AT.id = Action.actionType_id
             INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
             INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
             WHERE APT.descr = 'weight' AND AT.flatCode = 'MedicalSupplie'
               AND AP.deleted = 0 AND Action.event_id = Account_Item.event_id
             LIMIT 1), '')) AS SL_WEI,
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
            CASE
                WHEN rbEventProfile.regionalCode = '1'
                    THEN HospitalAction.amount
                WHEN rbEventProfile.regionalCode = '3'
                    THEN CASE
                        WHEN rbMedicalAidUnit.federalCode IN (25, 29) THEN 777
                        WHEN rbMedicalAidUnit.federalCode = 28 THEN Account_Item.amount
                        ELSE HospitalAction.amount + IF(HospitalAction.cnt > 1, 1, 0)
                        END
                WHEN rbEventProfile.regionalCode = '6'
                    THEN UetInfo.uet
                ELSE Account_Item.amount
            END AS SL_ED_COL,
            Account_Item.price AS SL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35')
                AND rbEventProfile.regionalCode = '5', 0,
                    IF(rbEventProfile.regionalCode = '6',
                        UetInfo.`sum`, Account_Item.`sum`)) AS SL_SUM_M,

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
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.regionalCode AS MR_USL_N_PRVS,
            Person.federalCode AS USL_IDDOKT,
            IF(rbEventProfile.regionalCode = '2', VisitPerson.federalCode,
                Person.federalCode) AS USL_CODE_MD,
            IF(rbEventProfile.regionalCode = '2', VisitPerson.regionalCode,
                Person.regionalCode) AS MR_USL_N_CODE_MD,

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
            ClientDocument.date AS PERS_DOCDATE,
            ClientDocument.origin AS PERS_DOCORG,
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
            ) AS 'isAnyBirthDoc' '''.format(serviceCode=serviceCode,
                                            policyNumber=policyNumber)
        tables = u'''Account_Item
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
            LEFT JOIN rbSocStatusType AS InvStatus ON InvStatus.id= (
                SELECT CSS.socStatusType_id
                FROM ClientSocStatus AS CSS
                WHERE CSS.client_id = `Client`.id AND
                CSS.deleted = 0 AND CSS.socStatusClass_id = (
                    SELECT rbSSC.id
                    FROM rbSocStatusClass AS rbSSC
                    WHERE rbSSC.code = '2' AND rbSSC.group_id IS NULL
                    LIMIT 0,1
                )
                LIMIT 1
            )
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
        '''

        orderBy = u'Client.id, Event.id, FirstEvent.id'
        return (select, tables, where, orderBy)


    def getChildNumber(self, clientId, birthDate):
        u'''У новорожденного пациента должна быть указана представительская
            связь с матерью. Если у матери имеется несколько связей с разными
            пациентами, при этом дата рождения этих пациентов одинаковая,
            требуется этим пациентам "присвоить" порядковый номер. У ребенка,
            у которого самый маленький client.id, будет Н=1, у кого id больше,
            будет Н=2, у которого еще больше, будет Н=3.  Если у матери один
            новорожденный ребенок (нет других связанных пациентов с такой же
            psps датой рождения), то выгружаем Н=1, соответственно.'''

        result = 1
        stmt = '''SELECT DISTINCT Client.id
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
            ORDER BY Client.id'''.format(
                clientId=clientId, birthDate=birthDate.toString(Qt.ISODate))

        query = self._db.query(stmt)
        childIdList = []

        while query.next():
            record = query.record()
            childIdList.append(forceRef(record.value(0)))

        if clientId in childIdList:
            result = childIdList.index(clientId) + 1

        return result


    def getKsgKpgInfo(self):
        u'Получает информацию о КСГ, КПГ'
        fieldList = ('KSG_KPG_CRIT', 'KSG_KPG_DKK2', 'SL_P_CEL',
                     'bedProfileCode', 'SL_KD', 'Z_SL_VB_P',
                     'medicalAidTypeCode')
        stmt = u'''SELECT Event.id AS eventId,
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
            IF(HospitalAction.amount = 0, 1, -- несколько действий одним днём
                HospitalAction.amount) + IF(
                    rbEventProfile.regionalCode = '3' AND -- Дневной стационар
                    -- несколько действий разными днями
                    HospitalAction.cnt > 1 AND HospitalAction.amount > 0, 1, 0),
            '') AS SL_KD,
        IF(rbMedicalAidUnit.federalCode = 33 AND Event.order = 5,
            1, '') AS Z_SL_VB_P
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
                    WHEN TIMESTAMPDIFF(DAY, A.begDate, A.endDate) = 0 THEN 0
                    ELSE DATEDIFF(A.endDate, A.begDate) + IF(
                            rbEventProfile.regionalCode = '3', 1, 0)
                END) AS amount,
                COUNT(DISTINCT A.id) AS cnt, MAX(A.id) AS id
            FROM Action A
            LEFT JOIN Event ON Event.id = A.event_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbEventProfile ON
                rbEventProfile.id = EventType.eventProfile_id
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
        LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL
                   AND rbPayRefuseType.rerun != 0))
          AND {0}'''.format(self.tableAccountItem['id'].inlist(self.idList))

        query = self._db.query(stmt)
        result = {}
        completeEventSummary = {}
        processedEvents = set()

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

                if (completeEventSummary.has_key(_id)
                        and eventId not in processedEvents):
                    completeEventSummary[_id] += _kd
                elif eventId not in processedEvents:
                    completeEventSummary[_id] = _kd
                    processedEvents.add(eventId)

            if val.get('KSG_KPG_CRIT'):
                val['KSG_KPG_CRIT'] = val['KSG_KPG_CRIT'].split(',')

            result[eventId] = val

        for key in result:
            if completeEventSummary.has_key(key):
                result[key]['Z_SL_KD_Z'] = completeEventSummary[key]

        return result


    def _getCompleteEventCount(self, includeOnkology):
        u'Возвращает строкой количество событий в счете.'

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
                  AND (SUBSTR(ds.MKB,1,1) = 'C'
                       OR SUBSTR(ds.MKB,1,3) BETWEEN 'D01' AND 'D09'
                       OR SUBSTR(ds.MKB,1,3) BETWEEN 'D45' AND 'D47')
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
        u'Возвращает строкой количество событий без онкологии в счете.'
        (result, _) = self._getCompleteEventCount(False)
        return result


    def getD4CompleteEventCount(self):
        u'Возвращает строкой количество событий с онкологией в счете.'
        (result, _) = self._getCompleteEventCount(True)
        return result


    def getTotalSum(self):
        u'Возвращает сумму событий без онкологии в счете.'
        (_, result) = self._getCompleteEventCount(False)
        return result


    def getD4TotalSum(self):
        u'Возвращает сумму событий с онкологией в счете.'
        (_, result) = self._getCompleteEventCount(True)
        return result


class CR08ExportPage2(CExportPage2):
    u'Вторая страница мастера экспорта'

    def __init__(self, parent, prefix):
        CExportPage2.__init__(self, parent, prefix)


    def saveExportResults(self):
        if self._parent.page1.registryType == CR08ExportPage1.registryTypeD1:
            fileList = (self._parent.getFullXmlFileName(),
                        self._parent.getPersonalDataFullXmlFileName())
            zipFileName = self._parent.getFullZipFileName()
        elif (self._parent.page1.registryType ==
                CR08ExportPage1.registryTypeCOVID19):
            fileList = (self._parent.getCOVID19FullXmlFileName(),
                        self._parent.getCOVID19PersonalDataFullXmlFileName())
            zipFileName = self._parent.getCOVID19FullZipFileName()
        else:
            fileList = (self._parent.getD4FullXmlFileName(),
                        self._parent.getD4PersonalDataFullXmlFileName())
            zipFileName = self._parent.getD4FullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))

# ******************************************************************************

class CR08XmlStreamWriterCommon(XmlStreamWriter, CExportHelperMixin):
    u'Осуществляет запись данных экспорта в XML'

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'SMO',
                    'SMO_NAM', 'INV', 'MSE', 'NOVOR', 'VNOV_D')

    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD', 'NPR_DATE', 'NPR_MO')

    completeEventDateFields2 = ('NPR_DATE', )
    completeEventDateFields1 = ('DATE_Z_1', 'DATE_Z_2')
    completeEventDateFields = completeEventDateFields1 + completeEventDateFields2
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
    eventFields2 = ('REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
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
    mapCharacterCode = {'4': '1', '2': '2', '3': '3',  '1':  '1'}

    REABILITATION_SERVICES = {
        u'B05.070.001': u'B01.023.100', # неврология
        u'B05.070.002': u'B01.023.100',
        u'B05.070.003': u'B01.023.100',
        u'B05.071.001': u'B01.050.100', # травмотология-ортопедия
        u'B05.071.002': u'B01.050.100',
        u'B05.071.003': u'B01.050.100',
        u'B05.073.001': u'B01.027.100', # онкология
        u'B05.073.002': u'B01.027.100',
        u'B05.073.003': u'B01.027.100',
        u'B05.074.001': u'B01.047.100', # терапия
        u'B05.074.002': u'B01.047.100',
        u'B05.074.003': u'B01.047.100',
    }

    OTHER_REABILITATION_SERVICES = (
        u'B05.075.001', u'B05.075.002', u'B05.075.003')

    MAP_SPECIALITY_TO_REABILITATION_SERVICE_CODE = {
       (8, 207, 33, 34, 35, 36): u'B01.001.100', #"Посещение с профилактической целью - акушерство и гинекология"
       (112, 77, 255): u'B01.002.100', #"Посещение с профилактической целью - аллергология"
       (114, 79, 257): u'B01.004.100', #"Посещение с профилактической целью - гастроэнтерология"
       (115, 80, 258): u'B01.005.100', #"Посещение с профилактической целью - гематология"
       (10, 40): u'B01.008.100', #"Посещение с профилактической целью - дерматология"
       (32, 212, 53): u'B01.014.100', #"Посещение с профилактической целью - инфекционные болезни"
       (139, 43): u'B01.018.100', #"Посещение с профилактической целью - проктология"
       (140, 44): u'B01.024.100', #"Посещение с профилактической целью - нейрохирургия"
       (123, 89, 261): u'B01.025.100', #"Посещение с профилактической целью врача-нефролога"
       (18,171): u'B01.026.100', #"Посещение с профилактической целью - ВОП "
       (19, ): u'B01.028.100', #"Посещение с профилактической целью - оториноларнигология"
       (20, ): u'B01.029.100', #"Посещение с профилактической целью - офтальмология"
       (1, 22): u'B01.031.100', #"Посещение с профилактической целью - педиатрия"
       (138, 90, 125, 262): u'B01.037.100', #"Посещение с профилактической целью - пульмонология"
       (126, 91, 263): u'B01.040.100', #"Посещение с профилактической целью - ревматология"
       (141, 45): u'B01.043.100', #"Посещение с профилактической целью - сосудистая хирургия"
       (75, ): u'B01.046.100', #"Посещение-сурдология-отоларингология"
       (42, 145): u'B01.053.100', #"Посещение с профилактической целью - урология"
       (30, ): u'B01.057.100', #"Посещение с профилактической целью - хирургия"
       (83, 150, 31, 149): u'B01.058.100', #"Посещение с профилактической целью - эндокринология (в т.ч. диабетолог)"
       (216,215,217,230,206,232,228,221,214,210,207,223,211,213,212,231,235,224,222,205,225,219,208,209,233,234,218,227,226,204): u'B08.070.100', #"Посещение с профилактической целью - фельдшер, средний медперсонал "
    }

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
        self._servicesCacheKey = None
        self._servicesCacheValue = None
        self._visitsCacheKey = None
        self._visitsCacheValue = None
        self.__contractNumberToContractIdCache = {}

    def __contractNumber(self, _id):
        u'Возвращает номер договора по идентификатору'
        return forceString(self.getTableFieldById(_id, 'Contract',
                    'number', self.__contractNumberToContractIdCache))


    def writeHeader(self, params):
        u'Запись заголовка xml файла'
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')
        if self._parent.registryType == CR08ExportPage1.registryTypeCOVID19:
            self.writeAttribute('xmlns',
                                'urn:ffoms:dispa:schema:xsd:reestr:d1:1.1')

        self.writeStartElement('ZGLV')
        self.writeElement('VERSION', self.version)
        self.writeElement('DATA', date.toString(Qt.ISODate))
        self.writeElement('FILENAME', params['shortFileName'][:-4])
        self.writeElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '%d' % params['accId'])
        self.writeElement('CODE_MO', params['lpuMiacCode'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeElement('NSCHET', params['NSCHET'])
        self.writeElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeElement('PLAT', params['payerCode'])
        self.writeElement('SUMMAV',
                          u'{0:.2f}'.format(self._parent.getTotalSum()))
        self.writeEndElement() # SCHET

        self._recNum = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastCompleteEventId = None
        self._lastRecord = None
        self._exportedNomenclativeServices = set()
        self._exportedActions = set()
        self._exportedEvents = set()
        self._servicesCacheKey = None
        self._servicesCacheValue = None
        self._visitsCacheKey = None
        self._visitsCacheValue = None

        self.__newServiceCode = None


    def writeRecord(self, record, params):
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        lastEventId = forceRef(record.value('lastEventId'))

        if (   clientId != self._lastClientId
            or lastEventId != self._lastCompleteEventId
           ):
            if self._lastClientId:
                if self._lastRecord:
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
        serviceCode = forceString(record.value('USL_CODE_USL'))
        self.__newServiceCode = self.REABILITATION_SERVICES.get(serviceCode)
        if serviceCode in self.OTHER_REABILITATION_SERVICES:
            specialityCode = forceInt(record.value('specialityCode'))
            for key in self.MAP_SPECIALITY_TO_REABILITATION_SERVICE_CODE:
                if specialityCode in key:
                    self.__newServiceCode = (
                        self.MAP_SPECIALITY_TO_REABILITATION_SERVICE_CODE[key])
                    break

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
                    else u'BZTSZ_КС', params['contractId']))
            local_params['KSG_KPG_KOEF_U'] = (
                self._parent.contractAttributeByType(
                    u'KOEF_U_ДС' if local_params['medicalAidTypeCode'] == '7'
                    else u'KOEF_U_КС', params['contractId']))
            local_params.update(self.getCoefficients(record, params))

        local_params['SL_DS2'] = forceString(record.value('ds2List')).split(',')
        local_params.update(params.get('onkologyInfo', {}).get(eventId, {}))

        if local_params.get('isOnkology'):
            serviceType = local_params.get('ONK_USL_USL_TIP')
            mkb = forceString(record.value('SL_DS1'))[:5]
            if ((('C81' <= mkb <= 'C96') or ('D45' <= mkb <= 'D47'))
                    and serviceType > 4):
                local_params['LEK_PR_CODE_SH'] = [u'нет']*len(
                    local_params.get('LEK_PR_CODE_SH', []))
        local_params.update(params.get('medicalSuppliesInfo', {}).get(
            eventId, {}))
        _record = CExtendedRecord(record, local_params, DEBUG)
        if (    forceInt(self._lastRecord.value('Z_SL_USL_OK')) == 3
            and idsp == 28
           ): # см. #0011123:0037003
            _record.setValue('SL_ED_COL', toVariant(self.evalUSLCount(eventId, params)))
        self.writeGroup('SL', self.eventFields, _record, self.eventSubGroup,
                        closeGroup=False, dateFields=self.eventDateFields)
        self._lastEventId = eventId


    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))
        patrName = forceString(record.value('PERS_OT'))
        firstName = forceString(record.value('PERS_IM'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'
        noFirstName = not firstName or firstName.upper() == u'НЕТ'
        childWeights = forceString(record.value('Z_SL_VNOV_M'))

        local_params = {}
        local_params.update(params['mapEventIdToKsgKpg'].get(lastEventId, {}))
        if childWeights:
            local_params['Z_SL_VNOV_M'] = childWeights.split(u',')

        code = forceInt(record.value('eventProfileRegionalCode'))
        eventId = forceRef(record.value('eventId'))
        onkologyInfo = params.get('onkologyInfo', {}).get(eventId, {})
        isOnkology = onkologyInfo.get('isOnkology')
        isSuspicion = onkologyInfo.get('SL_DS_ONK')
        isSpecialContract = self.__contractNumber(
            params['contractId']) == u'08005-МУР'

        if not (code in (1, 3) or isOnkology or isSuspicion):
            if not isSpecialContract:
                record.setNull('Z_SL_NPR_MO')
                record.setNull('Z_SL_NPR_DATE')

        local_params['Z_SL_SUMV'] = params['completeEventSum'].get(lastEventId)
        local_params['Z_SL_FOR_POM'] = self.mapEventOrderToForPom.get(
            forceInt(record.value('eventOrder')), '')
        local_params['Z_SL_OS_SLUCH'] = ('2' if (
            not (noPatrName and noFirstName and params['isJustBorn'])
            and (noPatrName or (
             params['isJustBorn'] and not params['isAnyBirthDoc']))) else '')
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
        isHospital = eventProfileCode in (1, 3)
        isAmbulance = eventProfileCode == 2
        isStomatology = eventProfileCode == 6
        eventId = forceRef(record.value('eventId'))
        idsp = params['idsp']

        if idsp == 28:
            record.setValue('USL_VID_VME', record.value('USL_CODE_USL'))

        onkologyInfo = params.get('onkologyInfo', {}).get(eventId, {})
        if onkologyInfo.get('isOnkology'):
            serviceType = onkologyInfo.get('ONK_USL_USL_TIP')
            fieldName = ('USL_CODE_USL' if serviceType in (1, 4, 6)
                         else 'mesServiceCode')
            record.setValue('USL_VID_VME', record.value(fieldName))

        if forceInt(record.value('Z_SL_USL_OK')) == 3:
            serviceCode = forceString(record.value('USL_CODE_USL'))
            if serviceCode[:1] == u'A':
                record.setValue('USL_VID_VME', record.value('USL_CODE_USL'))

        if isHospital:
            actionServiceCodeList = []

            if (eventId and eventId not in self._exportedActions):
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

                    local_params = {}
                    local_params.update(params)
                    local_params.update(params.get('implantsInfo', {}).get(
                        eventId, {}))
                    _record = CExtendedRecord(record, local_params, DEBUG)
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

            local_params = {}
            local_params.update(params)
            local_params.update(params.get('implantsInfo', {}).get(eventId, {}))
            _record = CExtendedRecord(record, local_params, DEBUG)
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


    def getNomenclativeServices(self, eventId, params):
        u'Получает список услуг, с кешированием для исключения лишних запросов'
        if self._servicesCacheKey != eventId:
            self._servicesCacheValue = exportNomenclativeServices(self._parent.db,
                                                                  eventId,
                                                                  params['actionList'])
            self._servicesCacheKey = eventId
        return self._servicesCacheValue


    def writeNomenclativeServices(self, record, eventId, isStomatology, params):
        u'Записывает информацию о номенклатурных услугах'
        serviceList = self.getNomenclativeServices(eventId, params)
        for (code, begDate, endDate, childUetDoctor, adultUetDoctor) in serviceList:
            record.setValue('USL_CODE_USL', code)
            record.setValue('USL_DATE_IN', begDate)
            record.setValue('USL_DATE_OUT', endDate)
            record.setValue('USL_TARIF', toVariant(0))
            record.setValue('USL_SUMV_USL', toVariant(0))

            if isStomatology:
                amount = forceDouble(record.value('amount'))
                coeff = (childUetDoctor
                         if forceBool(record.value('SL_DET'))
                         else adultUetDoctor)
                record.setValue('USL_KOL_USL', toVariant(amount*coeff))

            params['USL_IDSERV'] += 1
            local_params = {}
            local_params.update(params)
            local_params.update(params.get('implantsInfo', {}).get(eventId, {}))
            _record = CExtendedRecord(record, local_params, DEBUG)
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
            visitRecords = self.getVisits(eventId, params)

            if isAmbulance or isStomatology:
                if visitRecords:
                    first = QSqlRecord(visitRecords[0])
                    first.setValue('USL_DATE_IN', record.value('SL_DATE_1'))
                    first.setValue('USL_DATE_OUT', record.value('SL_DATE_2'))
                    first.setValue('USL_TARIF', record.value('USL_TARIF'))
                    first.setValue('USL_SUMV_USL', record.value('USL_SUMV_USL'))
                    self.writeService(first, params)
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
                if self.__newServiceCode:
                    visit.setValue('USL_CODE_USL', self.__newServiceCode)
                elif isAmbulance or isStomatology:
                    code = forceString(visit.value('USL_CODE_USL'))
                    visit.setValue('USL_CODE_USL',
                                   applyModifier(code, modifier))
                self.writeService(visit, params)

            self._exportedEvents.add(eventId)


    def evalUSLCount(self, eventId, params):
        serviceList = self.getNomenclativeServices(eventId, params)
        visitsList  = self.getVisits(eventId, params)
        return (  len(serviceList)
                + len(visitsList)
                + params['actionCount'].get(eventId, 0)
               )


    def getVisits(self, eventId, params):
        u'Получает список визитов, с кешированием для исключения лишних запросов'
        if self._visitsCacheKey != eventId:
            self._visitsCacheValue = self.exportVisits(eventId, params)
            self._visitsCacheKey = eventId
        return self._visitsCacheValue


    def exportVisits(self, eventId, _):
        u'''Экспортирует данные для визитов с 0 стоимостью,
          при тарификации по посещениям'''
        stmt = u'''SELECT
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
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.regionalCode AS MR_USL_N_PRVS,
            rbSpeciality.federalCode AS USL_PRVS,
            Person.federalCode AS USL_IDDOKT,
            Person.regionalCode AS MR_USL_N_CODE_MD,
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
--            AND rbVisitType.code = ''
        ORDER BY Visit.date''' % eventId

        query = self._parent.db.query(stmt)
        result = []

        while query.next():
            result.append(query.record())

        return result


    def getActionServiceCodeList(self, eventId):
        u'Возвращает список действий по событию.'

        stmt = u'''SELECT RS.infis, A.amount, A.begDate, A.endDate
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
        '''.format(eventId=eventId)

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
        u'Если тег в списке обязательных, выгружаем его пустым'
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
        u'Пишет информацию о пациенте'
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

        _record = CExtendedRecord(record, params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def getCoefficients(self, record, _):
        u'Пишет блок SL_KOEF'
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

class CR08PersonalDataWriter(PersonalDataWriter, CExportHelperMixin):
    u'Осуществляет запись данных экспорта в XML'

    clientDateFields = ('DR_P', 'DOCDATE', 'DR')
    clientFields = ('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'DR', 'DOST', 'TEL',
                    'FAM_P', 'IM_P', 'OT_P', 'W_P', 'DR_P', 'DOST_P', 'MR',
                    'DOCTYPE', 'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS',
                    'OKATOG', 'OKATOP')


    def __init__(self, parent):
        PersonalDataWriter.__init__(self, parent)
        self.version = '3.2'
        CExportHelperMixin.__init__(self)


    def _writeClientInfo(self, record, params):
        u'Пишет информацию о пациенте'
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


    def writeClientInfo(self, record, params):
        eventId = forceRef(record.value('eventId'))
        onkInfo = params['onkologyInfo'].get(eventId, {})

        if not onkInfo.get('isOnkology'):
            self._writeClientInfo(record, params)


# ******************************************************************************

class CR08XmlStreamWriterD4(CR08XmlStreamWriterCommon):

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'INV', 'MSE', 'NOVOR',
                    'VNOV_D')

    onkuslSubGroup = {
        'LEK_PR': {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ')},
    }

    onkslSubGroup = {
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE', 'DIAG_RSLT',
                              'REC_RSLT')},
        'B_PROT': {'fields': ('PROT', 'D_PROT'),
                   'dateFields': ('D_PROT', )},
        'ONK_USL': {'fields': ('USL_TIP', 'HIR_TIP', 'LEK_TIP_L',
                               'LEK_TIP_V', 'LEK_PR', 'PPTR', 'LUCH_TIP'),
                    'subGroup': onkuslSubGroup},
    }

    eventSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL',
                            'NAPR_USL'),
                 'dateFields': ('NAPR_DATE', )},
        'CONS': {'fields': ('PR_CONS', 'DT_CONS', )},
        'ONK_SL' : {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                               'MTSTZ', 'SOD', 'K_FR', 'WEI', 'HEI', 'BSA',
                               'B_DIAG', 'B_PROT', 'ONK_USL'),
                    'subGroup': onkslSubGroup},
        'KSG_KPG': {'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG',
                               'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D',
                               'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                               'SL_KOEF'),
                    'subGroup': CR08XmlStreamWriterCommon.ksgSubGroup},
    }


    def __init__(self, parent):
        CR08XmlStreamWriterCommon.__init__(self, parent)


    def writeHeader(self, params):
        u'Запись заголовка xml файла'
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeElement('VERSION', '3.1')
        self.writeElement('DATA', date.toString(Qt.ISODate))
        self.writeElement('FILENAME', params['d4shortFileName'][:-4])
        self.writeElement('SD_Z', self._parent.getD4CompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '%d' % params['accId'])
        self.writeElement('CODE_MO', params['lpuMiacCode'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeElement('NSCHET', params['NSCHET'])
        self.writeElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeElement('PLAT', params['payerCode'])
        self.writeElement('SUMMAV',
                          u'{0:.2f}'.format(self._parent.getD4TotalSum()))
        self.writeEndElement() # SCHET

        self._recNum = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastCompleteEventId = None
        self._lastRecord = None


    def writeRecord(self, record, params):
        if self._parent.registryType == CR08ExportPage1.registryTypeD4:
            CR08XmlStreamWriterCommon.writeRecord(self, record, params)
            self._parent._parent.anyOnkology = True

# ******************************************************************************

class CR08XmlStreamWriter(CR08XmlStreamWriterCommon):

    conditionalFields = ('NPR_DATE', 'NPR_MO')
    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD')

    eventFields1 = (('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                     'P_CEL', 'NHISTORY', 'P_PER', 'DATE_1', 'DATE_2',
                     'KD', 'WEI', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB',
                     'DN', 'CODE_MES1', 'CODE_MES2', 'NAPR', 'CONS', 'ONK_SL',
                     'KSG_KPG'))
    eventFields2 = ('REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                    'SUM_M', 'LEK_PR')
    eventFields = eventFields1 + eventFields2

    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME',
                      'DET') + CR08XmlStreamWriterCommon.serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL',
                      'MED_DEV', 'MR_USL_N', 'NPL', 'COMENTU'))

    serviceSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_V', 'MET_ISSL', 'NAPR_USL'),
                 'dateFields': ('NAPR_DATE', )},
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED', ),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N':{
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'prefix': 'COVID_LEK_LEK_PR',
        },
    }

    eventSubGroup = {
        'KSG_KPG': {'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG',
                               'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D',
                               'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                               'SL_KOEF'),
                    'subGroup': CR08XmlStreamWriterCommon.ksgSubGroup},
        'LEK_PR': { 'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK',
                               'LEK_DOSE'),
                    'dateFields': ('DATA_INJ', ),
                    'requiredFields': ('DATA_INJ', 'CODE_SH'),
                    'prefix': 'COVID_LEK',
                    'subGroup': medicalSuppliesDoseGroup,  }
    }

    def __init__(self, parent):
        CR08XmlStreamWriterCommon.__init__(self, parent)
        self.__currentRecord =  None
        self.version = '3.2'


    def writeRecord(self, record, params):
        eventId = forceRef(record.value('eventId'))
        onkInfo = params['onkologyInfo'].get(eventId, {})
        isOnkology = onkInfo.get('isOnkology')
        isSuspicion = onkInfo.get('SL_DS_ONK')
        self.__currentRecord = record

        if (not (isOnkology or isSuspicion) and
                self._parent.registryType in (CR08ExportPage1.registryTypeD1,
                    CR08ExportPage1.registryTypeCOVID19)):
            CR08XmlStreamWriterCommon.writeRecord(self, record, params)


    def writeElement(self, elementName, value=None):
        u'Пишет элемент. Если элемент в списке обязательных, выгружаем его пустым'
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

class CD4PersonalDataWriter(CR08PersonalDataWriter):
    u'Осуществляет запись данных экспорта в XML'


    def __init__(self, parent):
        CR08PersonalDataWriter.__init__(self, parent)
        self.version = '3.2'


    def writeClientInfo(self, record, params):
        if self._parent.registryType == CR08ExportPage1.registryTypeD4:
            CR08PersonalDataWriter._writeClientInfo(self, record, params)


    def writeHeader(self, params):
        u'Запись заголовка xml файла'
        date = params['accDate']
        self.writeStartElement('PERS_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', self.version)
        self.writeTextElement('DATA', date.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['personalDataFileName'][:-4])
        self.writeTextElement('FILENAME1',
                              self._parent._parent.getD4XmlFileName()[:-4])
        self.writeEndElement() # ZGLV

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


class COnkologyInfo(COrder200OnkologyInfo):
    def __init__(self):
        pass

    def _processMedicalSupplies(self, record, data):
        u'Заполняет поля для медикаментов'
        idList = forceString(record.value(
            'medicalSuppliesActionId')).split(',')
        nomenclatureDict = {}

        for i in idList:
            _id = forceRef(i)
            action = CAction.getActionById(_id) if _id else None

            if action:
                nomenclatureCode = None
                for prop in action.getProperties():
                    if prop.type().typeName == u'Номенклатура ЛСиИМН':
                        nomenclatureCode = (
                            CTfomsNomenclatureCache.getCode(
                                prop.getValue()))

                for prop in action.getProperties():
                    if prop.type().descr == 'DATE_INJ':
                        endDate = forceDate(action._record.value('endDate'))
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(endDate)
                else:
                    if nomenclatureCode:
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(None)

        codeSH = forceString(record.value('LEK_PR_CODE_SH'))

        for key, val in nomenclatureDict.iteritems():
            data.setdefault('LEK_PR_REGNUM', []).append(key if key else '-')
            data.setdefault('LEK_PR_DATE_INJ', []).append(val)
            data.setdefault('LEK_PR_CODE_SH', []).append(codeSH)

        return data

# ******************************************************************************

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
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Action.id""" .format(idList=self._idList)
        return stmt


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
        Action.endDate AS COVID_LEK_LEK_PR_DATA_INJ,
        (SELECT NC.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureClass APNC ON APNC.id = AP.id
         INNER JOIN rbNomenclatureClass NC ON APNC.value = NC.id
         WHERE APT.descr = 'V032' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_CODE_SH,
        {regnum} AS COVID_LEK_LEK_PR_REGNUM,
        (SELECT APS.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_String APS ON APS.id = AP.id
         WHERE APT.descr = 'COD_MARK' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1) AS COVID_LEK_LEK_PR_COD_MARK,
        IF({regnum} IS NOT NULL,
        (SELECT U.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbUnit APU ON APU.id = AP.id
         INNER JOIN rbUnit U ON U.id = APU.value
         WHERE APT.descr = 'V034' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1), NULL) AS COVID_LEK_LEK_PR_LEK_DOSE_ED_IZM,
        IF({regnum} IS NOT NULL,
        (SELECT APD.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
         WHERE APT.descr = 'Доза' AND AP.action_id = Action.id
           AND AP.deleted = 0
         LIMIT 1), NULL) COVID_LEK_LEK_PR_LEK_DOSE_DOSE_INJ,
        IF({regnum} IS NOT NULL,
        (SELECT N.code FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureUsingType APNU ON APNU.id = AP.id
         INNER JOIN rbNomenclatureUsingType N ON APNU.value = N.id
         WHERE APT.descr = 'OID:1.2.643.5.1.13.13.11.1468'
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1), NULL)  AS COVID_LEK_LEK_PR_LEK_DOSE_METHOD_INJ,
        IF({regnum} IS NOT NULL, Action.amount, '') AS COVID_LEK_LEK_PR_LEK_DOSE_COL_INJ
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.flatCode = 'MedicalSupplie'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""" .format(idList=self._idList, regnum=regnum)
        return stmt

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR08HospitalV173,
                      configFileName=u'75_79_s11.ini',
                      #accNum='5-12'
                      eventIdList=[465562]
                      )
