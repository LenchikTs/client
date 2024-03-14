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

u"""Экспорт реестра  в формате XML. Кировск Д1, Д4"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, Qt, QTextCodec

from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDate, formatSNILS)

from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
                             CAbstractExportPage1Xml, CAbstractExportPage2)
from Exchange.Order79Export import COrder79v3XmlStreamWriter
from Exchange.Utils import compressFileInZip
from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1

# выводит в консоль имена невыгруженных полей
DEBUG = False

def exportR47D1(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

def formatAccNumber(params, isFormatD3):
    u"""Номер счета состоит из следующих 15 симполов (буквы на русском в верхнем
            регистре):
        1. П -если Account.number начинаются на ЗП или ЗЛ
           Н -во всех остальных случаях
        2. Д - если используется формат экспорта Кировск Д3
           М - если используется формат экспорта Кировск Д1
        3. О - если этот счет выставляется впервые (нет постфикса /П в названии
                счета)
           И - счет перевыставлен (есть постфикс /П)
        4-6. 3 последние цифры Organisation.infisCode для ЛПУ в умолчаниях
        7-8. 2 последние цифры Account.payer_id->Organisation.infisCode
        9. разделитель "-"
        10-15. Account.id (дополнить слева нулями до 5 разрядов)"""
    accNum = params['accNumber']
    result = u'%s%s%s%s%s-%s' % (
        u'П' if params['isPerCapitaNorm'] else u'Н',
        u'Д' if isFormatD3 else u'М',
        u'И' if accNum[-2:] == u'/П' else u'О',
        params['lpuCode'][-3:],
        '99' if params['payerCode'] == '47' else params['payerCode'][-2:],
        '%06d' % (params['accId'] % 1000000),
    )

    return result

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта для Кировска"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Кировска'
        CAbstractExportWizard.__init__(self, parent, title)
        self.prefix = 'R47D1'
        self.page1 = CExportPage1(self, self.prefix)
        self.page2 = CExportPage2(self, self.prefix)

        self.addPage(self.page1)
        self.addPage(self.page2)

        self.__xmlBaseFileName = None
        self.note = None


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, self.prefix)


    def _getXmlBaseFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных"""

        def getPrefix(infisCode, isInsurer):
            u"""Возвращает префиксы по коду инфис и признаку страховой"""
            result = ''

            if infisCode == '47':
                result = 'T'
            else:
                result = 'S' if isInsurer else 'M'

            return result

        if self.__xmlBaseFileName:
            result = self.__xmlBaseFileName
        else:
            tableOrganisation = self.db.table('Organisation')
            tableContract = self.db.table('Contract')
            info = self.info

            payerCode = forceString(self.db.translate(
                tableOrganisation, 'id', info['payerId'], 'infisCode'))
            payerIsInsurer = forceString(self.db.translate(
                tableOrganisation, 'id', info['payerId'], 'isInsurer'))
            recipientId = forceString(self.db.translate(
                tableContract, 'id', info['contractId'], 'recipient_id'))
            recipientCode = forceString(self.db.translate(
                tableOrganisation, 'id', QtGui.qApp.currentOrgId(),
                'infisCode'))
            recipientIsInsurer = forceBool(self.db.translate(
                tableOrganisation, 'id', recipientId, 'isInsurer'))

            year = info['settleDate'].year() % 100
            month = info['settleDate'].month()
            packetNumber = info['accId']
            p_i = getPrefix(recipientCode, recipientIsInsurer)
            p_p = getPrefix(payerCode, payerIsInsurer)

            postfix = u'%02d%02d%d' % (
                year, month, packetNumber) if addPostfix else u''
            result = u'%s%s%s%s_%s.xml' % (
                p_i, recipientCode, p_p, payerCode, postfix)
            self.__xmlBaseFileName = result

        return result


    def getXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи данных."""
        return u'H%s' % self._getXmlBaseFileName(addPostfix)


    def getPersonalDataXmlFileName(self, addPostfix=True):
        u"""Возвращает имя файла для записи личных данных."""
        return u'L%s' % self._getXmlBaseFileName(addPostfix)


    def getFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getXmlFileName())


    def getPersonalDataFullXmlFileName(self):
        u"""Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getPersonalDataXmlFileName())


    def getZipFileName(self):
        u"""Возвращает имя архива"""
        return u'V%s.zip' % self._getXmlBaseFileName()[:-4]


    def getFullZipFileName(self):
        u"""Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу"""
        return os.path.join(self.getTmpDir(), self.getZipFileName())

# ******************************************************************************

class CExportPage1(CAbstractExportPage1Xml, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    registryTypeFlk = 0
    registryTypePayment = 1

    def __init__(self, parent, prefix):
        xmlWriter = (XmlStreamWriter(self), PersonalDataWriter(self))
        CAbstractExportPage1Xml.__init__(self, parent, xmlWriter)
        CExportHelperMixin.__init__(self)
        self.prefix = prefix

        self.exportedActionsList = None
        self.ignoreErrors = False

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(
            forceBool(prefs.get('Export%sVerboseLog' % prefix, False)))
        self.chkIgnoreErrors.setChecked(
            forceBool(prefs.get('Export%sIgnoreErrors' % prefix, False)))
        self.edtPacketNumber.setVisible(False)
        self.lblPacketNumber.setVisible(False)
        self.cmbRegistryType.setVisible(False)
        self.lblRegistryType.setVisible(False)
        self._orgStructInfoCache = {}

        self.chkIsPerCapitaNorm = QtGui.QCheckBox(self)
        self.chkIsPerCapitaNorm.setText(u'Оплата по подушевому нормативу')
        self.verticalLayout.addWidget(self.chkIsPerCapitaNorm)


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['Export%sIgnoreErrors' % self.prefix] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['Export%sVerboseLog' % self.prefix] = toVariant(
            self.chkVerboseLog.isChecked())
        return CAbstractExportPage1Xml.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)

        if hasattr(self, 'chkIsPerCapitaNorm'):
            self.chkIsPerCapitaNorm.setEnabled(not flag)

        if hasattr(self, 'lblPacketCounter'):
            self.lblPacketCounter.setEnabled(not flag)

        if hasattr(self, 'edtPacketNumber'):
            self.edtPacketNumber.setEnabled(not flag)

# ******************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = {
            'isPerCapitaNorm': self.chkIsPerCapitaNorm.isChecked()
        }

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
        params['lpuTfomsCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'tfomsExtCode'))
        params['USL_KODLPU'] = params['lpuCode']
        params['completeEventSum'] = self.getCompleteEventSum()
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
            params['mapEventIdToSum'] = self.getEventSum()

        params['rowNumber'] = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getPersonalDataXmlFileName(False))

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly|QFile.Text)

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly|QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter) = self.xmlWriter()
        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        CAbstractExportPage1Xml.exportInt(self)


    def prepareStmt(self, params):
        select = u"""Account_Item.event_id AS eventId,
            Event.client_id AS clientId,
            Action.id AS actionId,
            Visit.id AS visitId,
            RelegateOrg.id AS relegateOrgId,
            LastEvent.id AS lastEventId,
            Diagnostic.dispanser_id AS dispanserId,

            Account_Item.event_id AS Z_SL_IDCASE,
            rbEventTypePurpose.federalCode AS Z_SL_USL_OK,
            IF(TotalAmount.accItemCount > 1,
                FirstVisitMedicalAidKind.regionalCode,
                ServiceMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            IFNULL(IF(rbMedicalAidType.code IN (1,2,3,7), RelegateOrg.infisCode, ''), '{lpuCode}') AS Z_SL_NPR_MO,
            IFNULL(IF(rbMedicalAidType.code IN (1,2,3,7), Event.srcDate, ''), Event.setDate) AS Z_SL_NPR_DATE,
            PersonOrganisation.infisCode AS Z_SL_LPU,
            Event.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            CASE
                WHEN rbMedicalAidType.code IN (1, 2, 3) THEN
                    DATEDIFF(Event.execDate, Event.setDate)
                WHEN rbMedicalAidType.code = 7 THEN
                    DATEDIFF(Event.execDate, Event.setDate) + 1
                ELSE
                    ''
            END AS Z_SL_KD_Z,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            IF(NextEvent.id IS NULL, '', 1) AS Z_SL_VB_P,
            rbMedicalAidUnit.code AS Z_SL_IDSP,
            0 AS Z_SL_SUMV,
            '' AS Z_SL_FOR_POM,
            '' AS Z_SL_OS_SLUCH,

            Event.id AS SL_SL_ID,
            PersonOrgStructure.tfomsCode AS SL_LPU_1,
            IF(TotalAmount.accItemCount > 1,
                FirstVisitMedicalAidProfile.regionalCode,
                ServiceMedicalAidProfile.regionalCode) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS SL_DET,
            rbService_Identification.value AS SL_P_CEL,
            Event.id AS SL_NHISTORY,
            IF(EventType.form = '110', Event.execDate, Event.setDate) AS SL_DATE_1,
            Event.execDate AS SL_DATE_2,
            DS0.MKB AS SL_DS0,
            IF(EventInfo.diagnosisCount>1,
                IFNULL(Diagnosis.MKB, BasicDiag.MKB),
                AnyDiagnosis.MKB) AS SL_DS1,
            DS2.MKB AS SL_DS2,
            DS3.MKB AS SL_DS3,
            CASE
                WHEN rbDispanser.observed = 1 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                WHEN rbDispanser.observed = 1 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                WHEN rbDispanser.observed = 0 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                WHEN rbDispanser.observed = 0 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                ELSE ''
            END AS SL_DN,
            IF(rbMedicalAidType.code IN (1,2,3,7), mes.MES.code, NULL) AS SL_CODE_MES1,
            0 AS SL_REAB,
            rbSpeciality.federalCode AS SL_PRVS,
            Person.regionalCode AS SL_IDDOKT,
            TotalAmount.amount AS SL_ED_COL,
            Account_Item.price AS SL_TARIF,

            IF (Action.id IS NOT NULL, ActionOrg.infisCode,
                IF (Visit.id IS NOT NULL, VisitPersonOrg.infisCode, PersonOrganisation.infisCode)) AS USL_LPU,
            IF (Action.id IS NOT NULL, ActionOrgSruct.tfomsCode,
                IF (Visit.id IS NOT NULL, VisitPersonOrgStruct.tfomsCode, PersonOrgStructure.tfomsCode)) AS USL_LPU_1,
            ServiceMedicalAidProfile.code AS USL_PROFIL,
            IF(age(Client.birthDate,Event.execDate) < 18, 1, 0) AS USL_DET,
            IFNULL(Visit.date, IFNULL(Action.begDate, Event.setDate)) AS USL_DATE_IN,
            IFNULL(Visit.date, IFNULL(Action.endDate, Event.execDate)) AS USL_DATE_OUT,
            IFNULL(BasicDiag.MKB, Diagnosis.MKB) AS USL_DS,
            rbService.code AS USL_CODE_USL,
            Account_Item.amount AS USL_KOL_USL,
            Account_Item.price AS USL_TARIF,
            Account_Item.`sum` AS USL_SUMV_USL,
            IFNULL(VisitPersonSpeciality.federalCode,
                IFNULL(ActionPersonSpeciality.federalCode, rbSpeciality.federalCode)) AS USL_PRVS,
            IFNULL(VisitPerson.regionalCode,
                IFNULL(ActionPerson.regionalCode, Person.regionalCode)) AS USL_CODE_MD,

            Event.client_id AS PACIENT_ID_PAC,
            rbPolicyKind.regionalCode AS PACIENT_VPOLIS,
            ClientPolicy.serial AS PACIENT_SPOLIS,
            ClientPolicy.number AS PACIENT_NPOLIS,
            Insurer.OKATO AS PACIENT_ST_OKATO,
            Insurer.smoCode AS PACIENT_SMO,
            IF(Insurer.smoCode IS NULL OR Insurer.smoCode = '',
                Insurer.OGRN,'') AS PACIENT_SMO_OGRN,
            IF((Insurer.smoCode IS NULL OR Insurer.smoCode = '') AND Insurer.OGRN IS NOT NULL,
                Insurer.OKATO, '') AS PACIENT_SMO_OK,
            IF((Insurer.smoCode IS NULL OR Insurer.smoCode = '')
                AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                Insurer.shortName,'') AS PACIENT_SMO_NAM,
            IF(MseAction.id IS NULL, NULL, '1') AS PACIENT_MSE,
            IF(rbTempInvalidDocument.code IN (1,2,3,4),
                rbTempInvalidDocument.code, NULL) AS PACIENT_INV,
            IF(age(Client.birthDate,Event.execDate) < 18, Client.birthWeight, '') AS PACIENT_VNOV_D,

            Event.client_id AS PERS_ID_PAC,
            UPPER(Client.firstName) AS PERS_IM,
            UPPER(Client.patrName) AS PERS_OT,
            UPPER(Client.lastName) AS PERS_FAM,
            Client.sex AS PERS_W,
            Client.birthDate AS PERS_DR,
            UPPER(Client.birthPlace) AS PERS_MR,
            rbDocumentType.federalCode AS PERS_DOCTYPE,
            ClientDocument.serial AS PERS_DOCSER,
            ClientDocument.number AS PERS_DOCNUM,
            Client.SNILS AS clientSnils,

            `Event`.order AS eventOrder,
            `Event`.execDate,
            Client.sex AS clientSex,
            Client.birthDate AS clientBirthDate,
            EXISTS(
                SELECT NULL FROM ClientDocument AS CD
                LEFT JOIN rbDocumentType ON CD.documentType_id = rbDocumentType.id
                WHERE CD.client_id= Client.id AND rbDocumentType.regionalCode = '3'
                    AND CD.deleted = 0
                LIMIT 1
            ) AS 'isAnyBirthDoc',
            PersonOrgStructure.parent_id AS personParentOrgStructureId,
            ActionOrgSruct.parent_id AS actionParentOrgStructureId,
            VisitPersonOrgStruct.parent_id AS visitParentOrgStructureId""".format(lpuCode=params['lpuCode'])
        tables = u"""Account_Item
            LEFT JOIN Event ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN Diagnostic AS AnyDiagnostic ON AnyDiagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis AS AnyDiagnosis ON AnyDiagnosis.id = AnyDiagnostic.diagnosis_id AND AnyDiagnosis.deleted = 0
            LEFT JOIN Diagnostic ON Diagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '1')
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnostic AS BasicDiagnostic ON BasicDiagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '2')
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN Diagnosis AS DS2 ON DS2.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN Diagnosis AS DS3 ON DS3.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '3')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN Diagnosis AS DS0 ON DS0.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '7')
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id = Diagnostic.result_id
            LEFT JOIN rbDiagnosticResult AS AnyDiagnosticResult ON AnyDiagnosticResult.id = AnyDiagnostic.result_id
            LEFT JOIN rbDiagnosticResult AS BasicDiagnosticResult ON BasicDiagnosticResult.id = BasicDiagnostic.result_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
            LEFT JOIN Organisation AS RelegateOrg
                ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN rbService ON rbService.id = Account_Item.service_id
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.`id`, 1, Event.execDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN Organisation AS PersonOrganisation ON PersonOrganisation.id = Person.org_id
            LEFT JOIN OrgStructure AS PersonOrgStructure ON PersonOrgStructure.id = Person.orgStructure_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN Visit ON Account_Item.visit_id = Visit.id
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
            LEFT JOIN Organisation AS VisitPersonOrg ON VisitPersonOrg.id = VisitPerson.org_id
            LEFT JOIN OrgStructure AS VisitPersonOrgStruct ON VisitPerson.orgStructure_id = VisitPersonOrgStruct.id
            LEFT JOIN rbSpeciality AS VisitPersonSpeciality ON VisitPersonSpeciality.id = VisitPerson.speciality_id
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
            LEFT JOIN Organisation AS ActionOrg ON ActionOrg.id = IFNULL(Action.org_id, ActionPerson.org_id)
            LEFT JOIN OrgStructure AS ActionOrgSruct ON ActionPerson.orgStructure_id = ActionOrgSruct.id
            LEFT JOIN rbSpeciality AS ActionPersonSpeciality ON ActionPersonSpeciality.id = ActionPerson.speciality_id
            LEFT JOIN Visit AS FirstVisit ON FirstVisit.id = (
                SELECT id FROM Visit AS V1
                WHERE V1.deleted = 0 AND V1.event_id = Account_Item.event_id
                     AND V1.person_id = Event.execPerson_id
                LIMIT 0,1)
            LEFT JOIN rbService AS FirstVisitService ON FirstVisit.service_id = FirstVisitService.id
            LEFT JOIN rbMedicalAidKind AS FirstVisitMedicalAidKind ON
                FirstVisitMedicalAidKind.id = FirstVisitService.medicalAidKind_id
            LEFT JOIN rbMedicalAidProfile AS FirstVisitMedicalAidProfile ON
                FirstVisitMedicalAidProfile.id = FirstVisitService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile
                ON rbService.medicalAidProfile_id = ServiceMedicalAidProfile.id
            LEFT JOIN Diagnosis AS BasicDiag ON BasicDiag.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '2')
                    AND dc.event_id = Account_Item.event_id
                    AND dc.person_id = IFNULL(ActionPerson.id, VisitPerson.id)
            )
            LEFT JOIN (
                SELECT A.event_id, SUM(A.amount) AS amount,
                    COUNT(DISTINCT A.id) AS accItemCount
                FROM Account_Item A
                WHERE A.deleted = 0
                GROUP BY A.event_id
            ) AS TotalAmount ON TotalAmount.event_id = Account_Item.event_id
            LEFT JOIN (
                SELECT E.id, COUNT(DISTINCT Diagnosis.id) AS diagnosisCount,
                    COUNT(DISTINCT Diagnostic.id) AS diagnosticCount
                FROM Event E
                LEFT JOIN Diagnostic ON Diagnostic.event_id = E.id AND Diagnostic.deleted = 0
                LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
                WHERE E.deleted = 0
                GROUP BY E.id
            ) AS EventInfo ON EventInfo.id = Account_Item.event_id
            LEFT JOIN rbMedicalAidKind AS ServiceMedicalAidKind ON rbService.medicalAidKind_id = ServiceMedicalAidKind.id
            LEFT JOIN Action AS MseAction ON MseAction.id = (
                SELECT MAX(A.id)
                FROM Action A
                WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id = (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='directionMSE'
                          ))
            LEFT JOIN Event AS LastEvent ON LastEvent.id = getLastEventId(Event.id)
            LEFT JOIN Event AS NextEvent ON NextEvent.prevEvent_id = Event.id
            LEFT JOIN TempInvalid ON TempInvalid.id = (
                SELECT  TI.id
                FROM    TempInvalid TI
                WHERE TI.client_id = Client.id
                  AND TI.deleted = 0
                  AND TI.type = 1
                  AND (TI.begDate IS NULL OR TI.begDate >= Event.setDate)
                  AND (TI.endDate IS NULL OR TI.endDate <= Event.execDate)
                LIMIT 1
            )
            LEFT JOIN rbTempInvalidDocument ON TempInvalid.doctype_id = rbTempInvalidDocument.id
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN rbService_Identification ON rbService_Identification.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfomsPCEL')
                AND SId.deleted = 0
            )
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id"""

        where = u"""Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))
        orderBy = u'Client.id, Event.id'
        return (select, tables, where, orderBy)


    def getOrgStructureInfo(self, _id):
        u"""Возвращает parent_id и tfomsCode для подразделения"""
        result = self._orgStructInfoCache.get(_id, -1)

        if result == -1:
            result = (None, None)
            record = self._db.getRecord(
                'OrgStructure', ['parent_id', 'tfomsCode'], _id)

            if record:
                result = (forceRef(record.value(0)),
                          forceString(record.value(1)))

            self._orgStructInfoCache[_id] = result

        return result

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent, prefix):
        CAbstractExportPage2.__init__(self, parent, 'Export%s' % prefix)


    def saveExportResults(self):
        fileList = (self._parent.getFullXmlFileName(),
                    self._parent.getPersonalDataFullXmlFileName())
        zipFileName = self._parent.getFullZipFileName()

        return (compressFileInZip(fileList, zipFileName) and
                self.moveFiles([zipFileName]))


    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs[
                '%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()
        return success

# ******************************************************************************

class XmlStreamWriter(COrder79v3XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'INV', 'MSE', 'NOVOR',
                    'VNOV_D')

    completeEventDateFields = ('DATE_Z_1', 'DATE_Z_2')
    completeEventFields1 = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO',
        'NPR_DATE', 'LPU') + completeEventDateFields + ('KD_Z', 'RSLT',
        'ISHOD', 'OS_SLUCH', 'VB_P')
    completeEventFields2 = ('IDSP', 'SUMV', 'OPLATA')
    completeEventFields = completeEventFields1 + completeEventFields2

    eventDateFields = ('DATE_1', 'DATE_2')

    eventFields = (('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                    'P_CEL', 'NHISTORY', 'P_PER')
                   + eventDateFields +
                   ('KD', 'DS0', 'DS1', 'DS2', 'DS3', 'DN',
                    'CODE_MES1', 'CODE_MES2', 'KSG_KPG', 'REAB',
                    'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF', 'SUM_M'))

    serviceDateFields = ('DATE_IN', 'DATE_OUT')

    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'DET')
                     + serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL', 'PRVS',
                      'CODE_MD',))

    requiredFields = ('N_ZAP', 'PR_NOV', 'ID_PAC', 'VPOLIS', 'NPOLIS', 'NOVOR',
                      'IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'LPU', 'PROFIL',
                      'DET', 'NHISTORY', 'DATE_1', 'DATE_2', 'DS1', 'RSLT',
                      'ISHOD', 'PRVS', 'IDDOKT', 'IDSP', 'SUMV', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'DS', 'CODE_USL', 'KOL_USL',
                      'SUMV_USL', 'CODE_MD')

    mapEventOrderToForPom = {1: '3', 3: '3', 4: '3', 5: '3', 6: '2', 2: '1'}

    def __init__(self, parent):
        COrder79v3XmlStreamWriter.__init__(self, parent)
        self.setCodec(QTextCodec.codecForName('cp1251'))


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        accDate = params['accDate'].toString(Qt.ISODate)
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.0')
        self.writeTextElement('DATA', accDate)
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', formatAccNumber(params, False))
        self.writeTextElement('DSCHET', accDate)
        self.writeTextElement('PLAT', params['payerCode'])
        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeEndElement() # SCHET


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('lastClientId'):
            if params.get('lastClientId'):
                # выгрузка незавершенных действий
                self.writeEndElement() # SL
                self.writeGroup('Z_SL', self.completeEventFields2,
                                params['lastRecord'],
                                closeGroup=True, openGroup=False)
                self.writeEndElement() # ZAP

            self.writeStartElement('ZAP')
            self.writeTextElement('N_ZAP', forceString(params['rowNumber']))
            self.writeTextElement('PR_NOV', '0')

            params['birthDate'] = forceDate(record.value('clientBirthDate'))
            execDate = forceDate(record.value('execDate'))
            params['isJustBorn'] = params['birthDate'].daysTo(execDate) < 28
            params['isAnyBirthDoc'] = forceBool(record.value('isAnyBirthDoc'))

            self.writeClientInfo(record, params)

            params['rowNumber'] += 1
            params['lastClientId'] = clientId
            params['lastEventId'] = None
            params['lastComleteEventId'] = None

        COrder79v3XmlStreamWriter.writeRecord(self, record, params)


    def writeService(self, record, params):
        u"""Выгружает информацию об услугах"""
        params['USL_IDSERV'] += 1

        local_params = {
            'USL_PKUR': '0',
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('USL', self.serviceFields, _record,
                        dateFields=self.serviceDateFields)


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        sex = forceString(record.value('clientSex'))

        local_params = {
            'PACIENT_NOVOR':  (('%s%s1' % (
                sex[:1], params['birthDate'].toString('ddMMyy')))
                               if (params['isJustBorn'] and
                                   not params['isAnyBirthDoc']) else '0'),
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)


    def writeEventInfo(self, record, params):
        u"""Пишет информацию о событии"""
        eventId = forceRef(record.value('eventId'))
        lpu1Code = forceString(record.value('SLUCH_LPU_1'))
        serviceLpu1Code = forceString(record.value('USL_LPU_1'))

        if not lpu1Code:
            parentId = forceRef(record.value('personParentOrgStructureId'))
            lpu1Code = self.getLpuCode(parentId)

            if lpu1Code:
                record.setValue('SL_LPU_1', toVariant(lpu1Code))


        if not serviceLpu1Code:
            parentId = forceRef(record.value('actionParentOrgStructureId'))

            if not parentId:
                parentId = forceRef(record.value('visitParentOrgStructureId'))

            serviceLpu1Code = self.getLpuCode(parentId)

            if serviceLpu1Code:
                record.setValue('USL_LPU_1', toVariant(serviceLpu1Code))

        local_params = {
            'SL_VERS_SPEC': 'V021',
            'SL_SUM_M': params['mapEventIdToSum'].get(eventId, '')
        }

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)

        if eventId != params.setdefault('lastEventId'):
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

        record.setValue('Z_SL_SUMV', toVariant(
            params['completeEventSum'].get(lastEventId)))
        record.setValue('Z_SL_FOR_POM', toVariant(
            self.mapEventOrderToForPom.get(
                forceInt(record.value('eventOrder')), '')
            ))
        record.setValue('Z_SL_OS_SLUCH',  toVariant ('2' if (noPatrName or (
                params['isJustBorn'] and not params['isAnyBirthDoc'])) else ''))
        COrder79v3XmlStreamWriter.writeCompleteEvent(self, record, params)


    def getLpuCode(self, parentId):
        u"""Возвращает tfomsCode родительского подразделения"""
        result = None
        i = 0 # защита от перекрестных ссылок

        while not result and parentId and i < 1000:
            parentId, result = self._parent.getOrgStructureInfo(parentId)
            i += 1

        return result


# ******************************************************************************

class PersonalDataWriter(CAbstractExportXmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    clientDateFields = ('DR', )
    representativeFields = ('FAM_P', 'IM_P', 'OT_P', 'W_P', 'DOST_P')
    clientFields1 = (('ID_PAC', 'FAM', 'IM', 'OT', 'W',)
                     + clientDateFields +
                     ('DOST',))
    clientFields2 = ('MR', 'DOCTYPE', 'DOCSER', 'DOCNUM', 'SNILS')
    requiredFields = ('ID_PAC', 'W', 'DR', )

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self.setCodec(QTextCodec.codecForName('cp1251'))


    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        self.writeStartElement('PERS_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', settleDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['personalDataFileName'][:-4])
        self.writeTextElement('FILENAME1', params['fileName'][:-4])
        self.writeEndElement() # ZGLV


    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('clientId'))

        if clientId != params.setdefault('persLastClientId'):
            local_params = {}
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeClientInfo(_record, params)
            params['persLastClientId'] = clientId


    def writeClientInfo(self, record, params):
        u"""Пишет информацию о пациенте"""

        def getNameProblems(firstName, patrName, lastName):
            u'''Возвращает определенный код при отсутствии частей ФИО'''
            result = None

            if not patrName or patrName.upper() == u'НЕТ':
                result = '1'

            if not lastName or lastName.upper() == u'НЕТ':
                result = '2'

            if not firstName or firstName.upper() == u'НЕТ':
                result = '3'

            return result

        birthDate = forceDate(record.value('PERS_DR'))
        execDate = forceDate(record.value('execDate'))
        isAnyBirthDoc = forceBool(record.value('isAnyBirthDoc'))
        isJustBorn = birthDate.daysTo(execDate) < 28 and not isAnyBirthDoc
        clientId = forceRef(record.value('clientId'))

        local_params = {
            'PERS_DOST' : getNameProblems(
                forceString(record.value('PERS_IM')),
                forceString(record.value('PERS_OT')),
                forceString(record.value('PERS_FAM'))),
            'PERS_SNILS': formatSNILS(forceString(record.value('clientSnils')))
        }

        if isJustBorn:
            info = self._parent.getClientRepresentativeInfo(clientId)
            local_params['PERS_FAM_P'] = info.get('firstName', '')
            local_params['PERS_IM_P'] = info.get('lastName', '')
            local_params['PERS_OT_P'] = info.get('patrName', '')
            local_params['PERS_W_P'] = info.get('sex', '')
            local_params['PERS_DOST_P'] = getNameProblems(
                info.get('firstName', ''), info.get('patrName', ''),
                info.get('lastName', ''))
            record.setValue('PERS_MR', toVariant(info.get('birthPlace', '')))
            record.setValue('PERS_DOCTYPE', toVariant(info.get(
                'documentTypeFederalCode', '')))
            record.setValue('PERS_DOCSER', toVariant(info.get('serial', '')))
            record.setValue('PERS_DOCNUM', toVariant(info.get('number', '')))
            local_params['PERS_SNILS'] = formatSNILS(info.get('SNILS', ''))

        documentType = forceString(record.value('PERS_DOCTYPE'))

        if documentType == '3': #св-во о рождении
            serial = forceString(record.value('PERS_DOCSER')).replace(' ', '-')
            record.setValue('PERS_DOCSER', toVariant(serial))

        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)

        # борьба с пустым OT_P при отсутствии представителя
        fields = (self.clientFields1 + self.representativeFields +
                  self.clientFields2 if isJustBorn else
                  self.clientFields1 + self.clientFields2)

        self.writeGroup('PERS', fields, _record,
                        dateFields=self.clientDateFields)


    def writeElement(self, elementName, value=None):
        if value or elementName in ('OT', 'OT_P') + self.requiredFields:
            self.writeTextElement(elementName, value)


    def writeFooter(self, params):
        u"""Закрывает теги в конце файла"""
        self.writeEndElement() # PERS_LIST

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR47D1, 415)
