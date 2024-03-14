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

u'Экспорт реестра в формате XML. Забайкальский край, стационар (Д1,4) V173'

import json
import os

from decimal import Decimal, ROUND_HALF_UP

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QDate, pyqtSignature, SIGNAL

from library.Utils import (forceString, forceInt, toVariant, forceRef,
                           forceBool, forceDate, forceDouble)

from Events.Action import CAction
from Exchange.ExtendedRecord import CExtendedRecord
from Exchange.Export import (CExportHelperMixin, CMultiRecordInfo,
                             CAbstractExportPage1Xml)
from Exchange.Order200Export import COnkologyInfo
from Exchange.ExportR08Hospital import exportNomenclativeServices
from Exchange.ExportR08HospitalV59 import getXmlBaseFileName
from Exchange.ExportR60NativeAmbulance import (PersonalDataWriter,
                                               CExportPage2)
from Exchange.Order79Export import (
    COrder79v3XmlStreamWriter as XmlStreamWriter,
    COrder79ExportPage1 as CExportPage1,
    COrder79ExportWizard, COrder79ExportPage1)
from Exchange.Utils import compressFileInZip
from Registry.Utils import getClientPolicy

from Exchange.Ui_ExportPage1 import Ui_ExportPage1

DEBUG = False


def exportR80Hospital(widget, accountId, accountItemIdList, _=None):
    u'Создает диалог экспорта реестра счета'

    wizard = CR80ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()


def roundHalfUp(val):
    return forceDouble(Decimal(forceString(val)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP))


# ******************************************************************************

class CR80ExportWizard(COrder79ExportWizard):
    u'Мастер экспорта для Забайкальского края'

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Забайкальского края, стационар'
        prefix = 'R80HospitalV173'
        COrder79ExportWizard.__init__(self, title, prefix, CR80ExportPage1,
                                      CR80ExportPage2, parent)
        self.setWindowTitle(title)
        self.page1.setXmlWriter((CR80XmlStreamWriter(self.page1),
                                 CR80PersonalDataWriter(self.page1),
                                 CR80XmlStreamWriterD4(self.page1),
                                 CD4PersonalDataWriter(self.page1)))
        self.__xmlBaseFileName = None
        self.__tmpDirD4 = None
        self.anyOnklogy = False

    def _getXmlBaseFileName(self, addPostfix=True):
        u'Возвращает имя файла для записи данных'
        result = self.__xmlBaseFileName

        if not result:
            result = getXmlBaseFileName(self.db, self.info,
                                        self.page1.edtPacketNumber.value(),
                                        addPostfix, tfomsCode='75')
            self.__xmlBaseFileName = result

        return result

    def getD4XmlFileName(self, addPostfix=True):
        u'Возвращает имя файла для записи личных данных.'
        return u'C{0}'.format(self._getXmlBaseFileName(addPostfix))

    def getD4FullXmlFileName(self):
        u'''Возвращает полное имя файла для записи данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getD4XmlFileName())

    def getZipFileName(self):
        u'''Возвращает имя архива'''
        return u'{0}.zip'.format(self.getXmlFileName()[:-4])

    def getD4ZipFileName(self):
        u'''Возвращает имя архива'''
        return u'{0}.zip'.format(self.getD4XmlFileName()[:-4])

    def getD4FullZipFileName(self):
        u'''Возвращает полное имя архива данных.
        Добавляется путь к временному каталогу'''
        return os.path.join(self.getTmpDir(), self.getD4ZipFileName())

    def getD4PersonalDataXmlFileName(self, addPostfix=True):
        u'''Возвращает имя файла для записи личных данных.'''
        return u'LC{0}'.format(self._getXmlBaseFileName(addPostfix))

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

class CR80ExportPage1(CExportPage1, Ui_ExportPage1):
    u'Первая страница мастера экспорта'
    registryTypeD1 = 0
    registryTypeD4 = 1  # онкология

    def __init__(self, parent, prefix):
        CExportPage1.__init__(self, parent, prefix, None)
        self.cmbRegistryType.addItems([u'Д1', u'Д4'])
        self.registryType = self.registryTypeD1

        prefs = QtGui.qApp.preferences.appPrefs
        self.cmbRegistryType.setCurrentIndex(forceInt(prefs.get(
            'Export%sRegistryType' % prefix, 0)))

        for name, title, value in (
                ('chkUseNomenclativeService',
                 u'Использовать номенклатурные услуги',
                 False),
                ('chkReexposed', u'Повторное выставление', False),
                ('chkCheckRegistry', u'Проверять реестр', True)):
            setattr(self, name, QtGui.QCheckBox(self))
            item = getattr(self, name)
            item.setText(title)
            item.setChecked(value)

        self.vlOptions.addWidget(self.chkReexposed)
        self.vlOptions.addWidget(self.chkUseNomenclativeService)
        self.vlOptions.insertWidget(0, self.chkCheckRegistry)

        self.lblCorrectedAccountNumber = QtGui.QLabel(self)
        self.edtCorrectedAccountNumber = QtGui.QLineEdit(self)
        self.vlCorrectedAccountNumber = QtGui.QHBoxLayout()
        self.vlCorrectedAccountNumber.addWidget(self.lblCorrectedAccountNumber)
        self.lblCorrectedAccountNumber.setText(u'Номер исправляемого счета')
        self.vlCorrectedAccountNumber.addWidget(self.edtCorrectedAccountNumber)
        self.vlOptions.addItem(self.vlCorrectedAccountNumber)
        for widget in (self.lblCorrectedAccountNumber,
                       self.edtCorrectedAccountNumber):
            widget.setEnabled(False)
        self.connect(self.chkReexposed, SIGNAL('toggled(bool)'),
                     self.on_chkReexposed_toggled)

        self._recNum = 1

    @pyqtSignature('bool')
    def on_chkReexposed_toggled(self, value):
        for widget in (self.lblCorrectedAccountNumber,
                       self.edtCorrectedAccountNumber):
            widget.setEnabled(value)

    def setExportMode(self, flag):
        for name in ('chkReexposed', 'chkUseNomenclativeService',
                     'chkCheckRegistry'):
            if hasattr(self, name):
                getattr(self, name).setEnabled(not flag)
        self.cmbRegistryType.setEnabled(not flag)
        COrder79ExportPage1.setExportMode(self, flag)

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

        params['actionList'] = actionList
        params['actionCount'] = actionCount

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

    def __getOnkologyInfo(self):
        u'Получает информацию об онкологии в событиях'
        onkologyInfo = CR80OnkologyInfo()
        return onkologyInfo.get(
            self.db, self.tableAccountItem['id'].inlist(self.idList), self)

    def __getMedicalSuppiesInfo(self):
        u'Получает информацию об мед. препаратах'
        medicalSuppliesInfo = CMedicalSuppliesInfo()
        return medicalSuppliesInfo.get(
            self.db, self.tableAccountItem['id'].inlist(self.idList), self)

    def __getImplantsInfo(self):
        u'Получает информацию об имплантантах'
        implantsInfo = CImplantsInfo()
        return implantsInfo.get(
            self.db, self.tableAccountItem['id'].inlist(self.idList), self)

    def exportInt(self):
        self._parent.anyOnkology = False
        self.registryType = self.cmbRegistryType.currentIndex()
        isOnkologyRegistry = self.registryType == self.registryTypeD4
        params = self.processParams()
        params['isReexposed'] = '1' if self.chkReexposed.isChecked() else '0'
        if params['isReexposed'] == '1':
            params['reexposedAccountNumber'] = forceString(
                self.edtCorrectedAccountNumber.text())
        params['mapEventIdToSum'] = self.getEventSum()
        params['tempInvalidMap'] = self.getTempInvalidInfo()
        params['completeEventSum'] = self.getCompleteEventSum(isOnkologyRegistry)
        params['accountSum'] = roundHalfUp(sum(
            val for val in params['completeEventSum'].values()))
        params['mapEventIdToKsgKpg'] = self.__getKsgKpgInfo()
        params['onkologyInfo'] = self.__getOnkologyInfo()
        params['medicalSuppliesInfo'] = self.__getMedicalSuppiesInfo()
        params['implantsInfo'] = self.__getImplantsInfo()
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuMiacCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'miacCode'))
        params['lpuCodeTfoms75MO'] = self._getOrgIdentification(
            lpuId, self._getAccSysId('tfoms75.MO'))

        params['USL_KODLPU'] = params['lpuCode']
        params['sysIdTfoms75SMO'] = self._getAccSysId('tfoms75.SMO')
        params['sysIdTfoms75CODE_USL'] = self._getAccSysId('tfoms75.CODE_USL')
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                self.aborted = True
                return

        if self.idList:
            params.update(self.accountInfo())
            params['BZTSZ_KS'] = self.contractAttributeByType(u'BZTSZ_КС', params['contractId'])
            params['BZTSZ_DS'] = self.contractAttributeByType(u'BZTSZ_ДС', params['contractId'])
            params['payerCode'] = self._getOrgIdentification(
                params['payerId'], params['sysIdTfoms75SMO'])
            params['mapEventIdToFksgCode'] = self.getFksgCode()
            params['SLUCH_COUNT'] = params['accNumber']
            params['NSCHET'] = self.nschet(self.registryType, params)
            self._parent.note = u'[NSCHET:%s]' % params['NSCHET']
        else:
            self.logError(u'Нечего выгружать.')
            self.aborted = True
            return

        params['checkRegistry'] = self.chkCheckRegistry.isChecked()
        if params['checkRegistry']:
            visitsOk = self.checkVisits()
            if not visitsOk and not self.ignoreErrors:
                self.aborted = True
                return

        self._recNum = 1
        params['fileName'] = self._parent.getXmlFileName()
        params['shortFileName'] = self._parent.getXmlFileName(False)
        params['d4shortFileName'] = self._parent.getD4XmlFileName(False)
        params['personalDataFileName'] = (
            self._parent.getD4PersonalDataXmlFileName(False)
            if self.registryType == self.registryTypeD4 else
            self._parent.getPersonalDataXmlFileName(False))
        params['visitExportedEventList'] = set()
        params['toggleFlag'] = 0
        params['doneVis'] = set()
        params['useNomenclativeServiceCode'] = (
            self.chkUseNomenclativeService.isChecked())
        self.setProcessParams(params)

        outFile = QFile(self._parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)
        self.logInfo(u'Формируем реестр `{0}`'.format(
            self._parent.getFullXmlFileName()))

        personalDataFile = QFile(self._parent.getPersonalDataFullXmlFileName())
        personalDataFile.open(QFile.WriteOnly | QFile.Text)

        d4PersonalDataFile = QFile(
            self._parent.getD4PersonalDataFullXmlFileName())
        d4PersonalDataFile.open(QFile.WriteOnly | QFile.Text)

        d4File = QFile(self._parent.getD4FullXmlFileName())
        d4File.open(QFile.WriteOnly | QFile.Text)

        self.setProcessParams(params)
        (xmlWriter, personalDataWriter, d4Writer,
         d4PersonalDataWriter) = self.xmlWriter()

        xmlWriter.setDevice(outFile)
        personalDataWriter.setDevice(personalDataFile)
        d4Writer.setDevice(d4File)
        d4PersonalDataWriter.setDevice(d4PersonalDataFile)

        CAbstractExportPage1Xml.exportInt(self)

    def prepareStmt(self, params):
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

        isOnkology = self.registryType == self.registryTypeD4
        policyFields = (u"""ClientPolicy.number AS PACIENT_NPOLIS,"""
                        if isOnkology else
                        u"""IF(rbPolicyKind.regionalCode != '3',
                               ClientPolicy.number, '') AS PACIENT_NPOLIS,
                            IF(rbPolicyKind.regionalCode = '3',
                               ClientPolicy.number, '') AS PACIENT_ENP,""")

        serviceDateFields = (u"""Action.begDate AS USL_DATE_IN,
                                 Action.endDate AS USL_DATE_OUT,""" if isOnkology else
                             u"""Event.setDate AS USL_DATE_IN,
                                 Event.execDate AS USL_DATE_OUT,""")

        settleDate = params.get('settleDate', QDate.currentDate())
        select = u'''FirstEvent.id AS eventId,
            Event.client_id AS clientId,
            Event.order AS eventOrder,
            MesService.code AS mesServiceCode,
            MesService.infis AS mesServiceInfis,
            MesAction.begDate AS mesActionBegDate,
            MesAction.endDate AS mesActionEndDate,
            rbMedicalAidType.code AS medicalAidTypeCode,
            Account_Item.`sum` AS `sum`,
            Account_Item.uet,
            Account_Item.amount,
            Account_Item.usedCoefficients,
            (SELECT E.CSGCode FROM Event_CSG E
             WHERE E.id = Account_Item.eventCSG_id
             LIMIT 1) AS eventCSGCode,
            Event.id AS lastEventId,
            (SELECT DCI.value FROM rbDiseaseCharacter_Identification DCI
             WHERE DCI.deleted = 0 AND DCI.master_id = Diagnostic.character_id
               AND DCI.system_id = '{sysIdTfoms75C_ZAB}'
            ) AS SL_C_ZAB,

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
            IF(rbPolicyKind.regionalCode != '3',
               ClientPolicy.serial, '') AS PACIENT_SPOLIS,
            {policyFields}
            Insurer.OKATO AS PACIENT_ST_OKATO,
            (SELECT OI.value FROM Organisation_Identification OI
                 WHERE OI.master_id = Insurer.id
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms75SMO}'
                   LIMIT 1) AS PACIENT_SMO,
            IF((Insurer.miacCode IS NULL OR Insurer.miacCode = '')
                    AND (Insurer.OGRN IS NULL OR Insurer.OGRN = ''),
                    Insurer.shortName, '') AS PACIENT_SMO_NAM,
            Client.birthWeight AS PACIENT_VNOV_D,
            0 AS PACIENT_NOVOR,
            IF(MseAction.id IS NOT NULL, 1, '') AS PACIENT_MSE,

            Event.id AS Z_SL_IDCASE,
            Event.id AS Z_SL_FIRST_IDCASE,
            (SELECT OI.value FROM rbMedicalAidType_Identification OI
                 WHERE OI.master_id = rbMedicalAidType.id
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms75USL_OK}'
                   LIMIT 1) AS Z_SL_USL_OK,
            IFNULL((SELECT ATI.value FROM Action A
              LEFT JOIN ActionType AT ON A.actionType_id = AT.id
              LEFT JOIN ActionType_Identification ATI ON ATI.master_id = AT.id
              WHERE AT.flatCode = 'moving' AND A.event_id = Event.id
                AND ATI.deleted = 0 AND AT.deleted = 0 AND A.deleted = 0
                AND ATI.system_id = '{sysIdVIDPOM}'
              LIMIT 1),
             rbMedicalAidKind.regionalCode) AS Z_SL_VIDPOM,
            IF(rbEventProfile.regionalCode = 2,
               (SELECT OI.value FROM Organisation_Identification OI
                 WHERE OI.master_id = RelegateOrg.id
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms75MO}'
                 LIMIT 1),
               RelegateOrg.infisCode) AS Z_SL_NPR_MO,
            DATE(Event.srcDate) AS Z_SL_NPR_DATE,
            (SELECT OI.value FROM Organisation_Identification OI
             WHERE OI.master_id = PersonOrganisation.id
               AND OI.deleted = 0
               AND OI.system_id = '{sysIdTfoms75MO}'
               LIMIT 1) AS Z_SL_LPU,
            FirstEvent.setDate AS Z_SL_DATE_Z_1,
            Event.execDate AS Z_SL_DATE_Z_2,
            EventResult.federalCode AS Z_SL_RSLT,
            rbDiagnosticResult.federalCode AS Z_SL_ISHOD,
            IFNULL((SELECT federalCode FROM Account_Item AI
             LEFT JOIN rbMedicalAidUnit MAU ON MAU.id = AI.unit_id
             WHERE AI.deleted = 0 AND AI.event_id = Event.id
               AND AI.visit_id IS NOT NULL
             LIMIT 1), rbMedicalAidUnit.federalCode) AS Z_SL_IDSP,

            FirstEvent.id AS SL_SL_ID,
            PersonOrgStructure.infisCode AS SL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL(EventType_Identification.value,
                    PersonOrgStructure.tfomsCode)) AS SL_PODR,
            IFNULL((SELECT MAP.regionalCode FROM ActionProperty
                    LEFT JOIN Action A ON A.id = ActionProperty.action_id
                    LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                    INNER JOIN ActionProperty_rbHospitalBedProfile AS HBP
                      ON HBP.id = ActionProperty.id
                    LEFT JOIN rbHospitalBedProfile BP ON BP.id = HBP.value
                    LEFT JOIN rbMedicalAidProfile MAP
                      ON BP.medicalAidProfile_id = MAP.id
                    WHERE A.event_id = Event.id AND A.deleted = 0
                      AND AT.flatCode = 'moving' LIMIT 1),
                   IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
                      ServiceProfileMedicalAidProfile.code,
                      ServiceMedicalAidProfile.code)) AS SL_PROFIL,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS SL_DET,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                Event.externalId, Client.id) AS SL_NHISTORY,
            FirstEvent.setDate AS SL_DATE_1,
            FirstEvent.execDate AS SL_DATE_2,
            IFNULL((SELECT APD.value
             FROM Action A
             INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
             INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
             INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
             INNER JOIN ActionProperty_Double AS APD ON APD.id = AP.id
             INNER JOIN ActionType_Identification ATI ON ATI.master_id = AT.id
             WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
               AND AP.deleted = 0
               AND APT.`name` = 'Вес'
               AND ATI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = 'tfoms75.ActionType')
               AND ATI.value = 'clientWeigh'
             LIMIT 0, 1),'') AS SL_WEI,
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
            (SELECT rSI.value FROM rbSpeciality_Identification rSI
             WHERE rSI.master_id = Person.speciality_id
               AND rSI.deleted = 0
               AND rSI.system_id = (SELECT id FROM rbAccountingSystem
                                    WHERE code = "tfoms75.Speciality")) AS SL_PRVS,
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
                    THEN (SELECT COUNT(*) FROM Account_Item
                          WHERE Account_Item.event_id = Event.id
                            AND Account_Item.deleted = 0)
                ELSE Account_Item.amount
            END AS SL_ED_COL,
            Account_Item.price AS SL_TARIF,
            IF(rbMedicalAidUnit.federalCode IN ('31', '35')
                AND rbEventProfile.regionalCode = '5', 0,
                    IF(rbEventProfile.regionalCode = '6',
                        Account_Item.`price`, Account_Item.`sum`)) AS SL_SUM_M,

            IF(rbMedicalAidType.regionalCode != '3', (
                SELECT E.CSGCode FROM Event_CSG E
                WHERE E.id = Account_Item.eventCSG_id
                LIMIT 1), NULL) AS KSG_KPG_N_KSG,
            IF(rbMedicalAidType.regionalCode != '3', 0, NULL) AS KSG_KPG_KSG_PG,
            IF(rbMedicalAidType.regionalCode != '3',
             Contract_Tariff.price * (
                SELECT percent FROM Contract_CompositionExpense CCE
                INNER JOIN rbExpenseServiceItem ESI ON ESI.id = CCE.rbTable_id
                WHERE CCE.master_id = Contract_Tariff.id
                  AND ESI.code = 'KOEF_Z'
                LIMIT 1), NULL) AS KSG_KPG_KOEF_Z,
            IF(rbMedicalAidType.regionalCode != '3', 1, NULL) AS KSG_KPG_KOEF_UP,

            PersonOrganisation.miacCode AS USL_LPU,
            PersonOrgStructure.infisCode AS USL_LPU_1,
            IFNULL(LeavedOrgStruct.tfomsCode,
                IFNULL(EventType_Identification.value, PersonOrgStructure.tfomsCode)) AS USL_PODR,
            IF(rbService_Profile.medicalAidProfile_id IS NOT NULL,
               ServiceProfileMedicalAidProfile.code,
               ServiceMedicalAidProfile.code) AS USL_PROFIL,
            '' AS USL_VID_VME,
            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS USL_DET,
            {serviceDateFields}
            Diagnosis.MKB AS USL_DS,
            {serviceCode} AS USL_CODE_USL,
            IF(rbEventProfile.regionalCode IN ('1', '3'),
                HospitalAction.amount + IF(rbEventProfile.regionalCode = '3' AND HospitalAction.cnt > 1, 1, 0),
                Account_Item.amount) AS USL_KOL_USL,
            IF(rbEventProfile.regionalCode != '6', Account_Item.price, 0) AS USL_TARIF,
            IF((rbMedicalAidUnit.federalCode IN ('31', '35')
                AND rbEventProfile.regionalCode  = '5')
               OR rbEventProfile.regionalCode = '6',
                0, Account_Item.`sum`) AS USL_SUMV_USL,
            (SELECT rSI.value FROM rbSpeciality_Identification rSI
             WHERE rSI.master_id = Person.speciality_id
               AND rSI.deleted = 0
               AND rSI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = "tfoms75.Speciality")) AS USL_PRVS,
            IF(rbEventProfile.regionalCode = '2', VisitPerson.federalCode,
                Person.federalCode) AS USL_CODE_MD,
            Person.federalCode AS USL_IDDOKT,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS MR_USL_N_CODE_MD,

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
                                            sysIdTfoms75SMO=params['sysIdTfoms75SMO'],
                                            sysIdTfoms75USL_OK=self._getAccSysId('tfoms75.USL_OK'),
                                            sysIdTfoms75MO=self._getAccSysId('tfoms75.MO'),
                                            sysIdTfoms75C_ZAB=self._getAccSysId('tfoms75.C_ZAB'),
                                            sysIdVIDPOM=self._getAccSysId('VIDPOM'),
                                            policyFields=policyFields,
                                            serviceDateFields=serviceDateFields)
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
                    SELECT A.event_id, SUM(A.amount) AS amount,
                           COUNT(DISTINCT A.id) AS cnt, MAX(A.id) AS id
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
                WHERE Account_Item.deleted = 0
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
        '''.format(month=settleDate.month(), year=settleDate.year())
        where = u"""Account_Item.reexposeItem_id IS NULL
            AND Account_Item.deleted = 0
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {0}""".format(self.tableAccountItem['id'].inlist(self.idList))
        orderBy = u'Client.id, Event.id, FirstEvent.id'
        return select, tables, where, orderBy

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

    def getTempInvalidInfo(self):
        u'Получает информацию о больничных'
        stmt = '''SELECT Event.client_id, rbTempInvalidRegime.code
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
          AND {0}'''.format(self.tableAccountItem['id'].inlist(self.idList))
        query = self._db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            clientId = forceRef(record.value(0))
            val = forceString(record.value(1))[1:]
            result[clientId] = val

        return result

    def __getKsgKpgInfo(self):
        u'Получает информацию о КСГ, КПГ'
        fieldList = ('KSG_KPG_CRIT', 'KSG_KPG_DKK2', 'SL_P_CEL',
                     'bedProfileCode', 'SL_KD', 'Z_SL_VB_P',
                     'medicalAidTypeCode')
        stmt = '''SELECT Event.id AS eventId,
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
            SELECT A.event_id, A.amount,
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
        LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL
                   AND rbPayRefuseType.rerun != 0))
          AND {0}'''.format(self.tableAccountItem['id'].inlist(self.idList))

        query = self._db.query(stmt)
        result = {}
        completeEventSummary = {}

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

                if completeEventSummary.has_key(_id):
                    completeEventSummary[_id] += _kd
                else:
                    completeEventSummary[_id] = _kd

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
        stmt = """SELECT COUNT(DISTINCT eventId),
    SUM(IF(`sum`*1000%10 > 5, CEIL(100*`sum`)/100, FLOOR(`sum`*100)/100))
FROM
    (SELECT getLastEventId(Account_Item.event_id) AS eventId,
            (SELECT MAX(ds.id) IS NOT NULL
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id
                    AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code IN ('1','2','9'))
                  AND dc.event_id = Account_Item.event_id
                  AND (SUBSTR(ds.MKB,1,1) = 'C' OR SUBSTR(ds.MKB,1,3) between 'D01' and 'D06')
            ) AS isOnkology,
            SUM(IF(rbMedicalAidType.code = 6, Account_Item.price,
               Account_Item.`sum`)) AS `sum`
    FROM Account_Item
    LEFT JOIN Event ON Event.id = Account_Item.event_id
    LEFT JOIN EventType ON EventType.id = Event.eventType_id
    LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
    WHERE {0}
    GROUP BY Account_Item.serviceDate, Account_Item.event_id) A
WHERE isOnkology {1} 0""".format(
            self.tableAccountItem['id'].inlist(self.idList),
            '!=' if includeOnkology else '=')

        query = self.db.query(stmt)

        if query.first():
            record = query.record()
            result = forceString(record.value(0)), roundHalfUp(record.value(1))

        return result

    def getCompleteEventCount(self):
        u'Возвращает строкой количество событий без онкологии в счете.'
        (result, _) = self._getCompleteEventCount(False)
        return result

    def getD4CompleteEventCount(self):
        u'Возвращает строкой количество событий с онкологией в счете.'
        (result, _) = self._getCompleteEventCount(True)
        return result

    def checkVisits(self):
        stmt = u"""SELECT Event.client_id AS clientId,
        Event.id AS eventId,
        (SELECT COUNT(DISTINCT Visit.service_id) AS serviceCount
         FROM Visit -- есть разные услуги
         WHERE Visit.event_id = Event.id
           AND Visit.deleted = 0
         HAVING serviceCount > 1 LIMIT 1) AS serviceError,
        IF(rbEventProfile.code = 2,
            (SELECT (COUNT(DISTINCT IF(rbVisitType.code != '', Visit.visitType_id, 0))
                     != COUNT(DISTINCT IF(rbVisitType.code != '',Visit.id,0))
                     OR SUM(IF(rbVisitType.code = '', 0, 1)) > 0) AS cnt
             FROM Visit -- тип визита разный или имеет код
             LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
             WHERE Visit.event_id = Event.id
               AND Visit.deleted = 0
             HAVING COUNT(DISTINCT Visit.id) > 1), 0) AS typeError,
        IF(rbEventProfile.code = 2,
            (SELECT COUNT(DISTINCT Visit.id) = 1
                    AND SUM(IF(rbVisitType.code = '', 1, 0)) > 0 AS cnt
             FROM Visit -- только один визит без кода
             LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
             WHERE Visit.event_id = Event.id
               AND Visit.deleted = 0), 0) AS codeError,
        (SELECT COUNT(DISTINCT Visit.date) < COUNT(DISTINCT Visit.id) AS flag
         FROM Visit -- несколько визитов с одинаковой датой
         WHERE Visit.event_id = Event.id
           AND Visit.deleted = 0) AS sameDateError,
        (SELECT SUM(Visit.date > Event.execDate) > 0
         FROM Visit -- визит вне дат события
         WHERE Visit.event_id = Event.id
           AND Visit.deleted = 0) AS dateIsOutOfEventError,
        (SELECT DATEDIFF(MAX(Visit.date), MIN(Visit.date)) > 30
         FROM Visit -- даты между двумя последними визитами.
         WHERE Visit.event_id = Event.id
           AND Visit.deleted = 0) AS dateIsTooLong,
        Client.sex = 0 AS clientSexError,
        CONCAT(Person.lastName, ' ',
               Person.firstName, ' ', Person.patrName) AS person
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON Event.eventType_id = EventType.id
        LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
        LEFT JOIN rbPayRefuseType ON
            rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Person ON Event.execPerson_id = Person.id
        LEFT JOIN Client ON Client.id = Event.client_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND Account_Item.visit_id IS NOT NULL
          AND Account_Item.deleted = 0
          AND rbEventProfile.regionalCode IN ('2', '6')
          AND (Account_Item.date IS NULL
               OR (Account_Item.date IS NOT NULL
                   AND rbPayRefuseType.rerun != 0))
          AND {0}
        GROUP BY Event.id
        HAVING serviceError > 0 OR typeError > 0 OR codeError > 0
            OR sameDateError > 0 OR dateIsOutOfEventError > 0 OR clientSexError > 0
            OR dateIsTooLong > 0
        """.format(self.tableAccountItem['id'].inlist(self.idList))

        query = self._db.query(stmt)
        result = True

        while query.next():
            record = query.record()
            serviceError = forceBool(record.value('serviceError'))
            typeError = forceBool(record.value(3)) or forceBool(record.value(4))
            sameDateError = forceBool(record.value('sameDateError'))
            dateIsOutOfEventError = forceBool(record.value('dateIsOutOfEventError'))
            clientSexError = forceBool(record.value('clientSexError'))
            dateIsTooLong = forceBool(record.value('dateIsTooLong'))
            if (serviceError or typeError or sameDateError
                    or dateIsOutOfEventError or clientSexError
                    or dateIsTooLong):
                clientId = forceRef(record.value('clientId'))
                eventId = forceRef(record.value('eventId'))
                person = forceString(record.value('person'))
                prefix = u'Пациент `{0}`, случай `{1}`, врач `{2}`'.format(
                    clientId, eventId, person)
                if serviceError:
                    message = u'визиты события имеют разные услуги'
                if typeError:
                    message = u'тип визита указан неверно'
                if sameDateError:
                    message = u'имеется несколько визитов в один день'
                if dateIsOutOfEventError:
                    message = u'дата визита не соответствует периоду события'
                if clientSexError:
                    message = u'не указан пол'
                if dateIsTooLong:
                    message = u'период между приемами обращений больше 1 месяца'
                self.logError(u'{0} - {1}.'.format(prefix, message))
                result = False

        return result

    def getEventSum(self):
        u"""Возвращает общую стоимость услуг за событие"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.price*Account_Item.amount) AS totalSum
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.serviceDate, Account_Item.event_id;""" \
               % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result[eventId] = result.setdefault(eventId, 0) + roundHalfUp(record.value(1))

        return result

    def getCompleteEventSum(self, includeOnkology):
        u"""Возвращает общую стоимость услуг за событие"""

        stmt = """SELECT getLastEventId(Account_Item.event_id) AS lastEventId,
             SUM(/*IF(rbMedicalAidType.code = 6,*/
                  Account_Item.price*Account_Item.amount/*, Account_Item.`sum`)*/) AS totalSum,
             (SELECT MAX(ds.id) IS NOT NULL
                FROM Diagnosis ds
                INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id
                    AND ds.deleted = 0 AND dc.deleted = 0)
                LEFT JOIN rbDiseasePhases ON rbDiseasePhases.id = dc.phase_id
                WHERE dc.diagnosisType_id IN (
                    SELECT id FROM rbDiagnosisType WHERE code IN ('1','2','9'))
                  AND dc.event_id = Account_Item.event_id
                  AND (SUBSTR(ds.MKB,1,1) = 'C'
                       OR SUBSTR(ds.MKB,1,3) BETWEEN 'D01' AND 'D09'
                       OR SUBSTR(ds.MKB,1,3) BETWEEN 'D45' AND 'D47'
                       OR ds.MKB IN ('D70', 'Z03.1'))
            ) AS isOnkology
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND {idList}
        GROUP BY Account_Item.serviceDate, lastEventId
        HAVING isOnkology {flag} 1;""".format(
            idList=self.tableAccountItem['id'].inlist(self.idList),
            flag=('=' if includeOnkology else '!='))

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            result[eventId] = result.setdefault(eventId, 0) + roundHalfUp(record.value(1))

        return result


class CR80ExportPage2(CExportPage2):
    u'Вторая страница мастера экспорта'

    def __init__(self, parent, prefix):
        CExportPage2.__init__(self, parent, prefix)

    def saveExportResults(self):
        if self._parent.page1.registryType == CR80ExportPage1.registryTypeD1:
            fileList = (self._parent.getFullXmlFileName(),
                        self._parent.getPersonalDataFullXmlFileName())
            zipFileName = self._parent.getFullZipFileName()
        else:
            fileList = (self._parent.getD4FullXmlFileName(),
                        self._parent.getD4PersonalDataFullXmlFileName())
            zipFileName = self._parent.getD4FullZipFileName()

        success, result = QtGui.qApp.call(self, compressFileInZip,
                                          (fileList, zipFileName))
        if not success or not result:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка экспорта данных!',
                                       u'Не удалось создать архив `{0}`'.format(zipFileName),
                                       QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False

        success, result = QtGui.qApp.call(self, self.moveFiles, ([zipFileName],))
        if not success or not result:
            QtGui.QMessageBox.critical(self,
                                       u'Ошибка экспорта данных!',
                                       u'Не удалось переместить архив `{0}`'.format(zipFileName),
                                       QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False

        return True


# ******************************************************************************

class CR80XmlStreamWriterCommon(XmlStreamWriter, CExportHelperMixin):
    u'Осуществляет запись данных экспорта в XML'

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'ST_OKATO',
                    'SMO', 'SMO_NAM', 'INV', 'MSE', 'NOVOR')

    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD')

    completeEventDateFields2 = ('NPR_DATE',)
    completeEventDateFields1 = ('DATE_Z_1', 'DATE_Z_2')
    completeEventDateFields = completeEventDateFields1 + completeEventDateFields2
    completeEventFields1 = (('IDCASE', 'FIRST_IDCASE', 'USL_OK', 'VIDPOM',
                             'FOR_POM', 'NPR_MO')
                            + completeEventDateFields2 + ('LPU',)
                            + completeEventDateFields1 +
                            ('KD_Z', 'VNOV_M', 'RSLT', 'ISHOD', 'OS_SLUCH',
                             'VB_P'))
    completeEventFields2 = ('IDSP', 'SUMV', 'OPLATA')
    completeEventFields = completeEventFields1 + completeEventFields2
    requiredCompleteEventFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM',
                                   'LPU', 'DATE_Z_1', 'DATE_Z_2', 'RSLT',
                                   'ISHOD', 'IDSP', 'SUMV')

    eventDateFields = ('DATE_1', 'DATE_2')
    eventFields1 = (('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                     'P_CEL', 'NHISTORY', 'P_PER')
                    + eventDateFields +
                    ('KD', 'WEI', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK', 'DN',
                     'CODE_MES1', 'CODE_MES2', 'NAPR', 'CONS', 'ONK_SL',
                     'KSG_KPG'))
    eventFields2 = ('REAB', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF',
                    'SUM_M', 'LEK_PR')
    eventFields = eventFields1 + eventFields2
    requiredEventFields = ('SL_ID', 'PROFIL', 'DET', 'NHISTORY', 'DATE_1',
                           'DATE_2', 'DS1', 'PRVS', 'VERS_SPEC', 'IDDOKT',
                           'SUM_M')

    ksgSubGroup = {
        'SL_KOEF': {'fields': ('IDSL', 'Z_SL'),
                    'requiredFields': ('IDSL', 'Z_SL')}
    }

    medicalSuppliesDoseGroup = {
        'LEK_DOSE': {
            'fields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
            'requiredFields': ('ED_IZM', 'DOSE_INJ', 'METHOD_INJ', 'COL_INJ'),
        },
    }

    medicalSuppliesGroup = {
        'fields': ('DATA_INJ', 'CODE_SH', 'REGNUM', 'COD_MARK', 'LEK_DOSE'),
        'dateFields': ('DATA_INJ',),
        'requiredFields': ('DATA_INJ', 'CODE_SH'),
        'subGroup': medicalSuppliesDoseGroup,
    }

    eventHospSubGroup = {
        'KSG_KPG': {'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG',
                               'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D',
                               'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                               'SL_KOEF'),
                    'requiredFields': ('VER_KSG', 'KSG_PG', 'KOEF_Z',
                                       'KOEF_UP', 'BZTSZ', 'KOEF_D', 'KOEF_U',
                                       'SL_K'),
                    'subGroup': ksgSubGroup},
        'LEK_PR': medicalSuppliesGroup,
    }

    eventSubGroup = {
        'LEK_PR': medicalSuppliesGroup,
    }

    serviceDateFields = ('DATE_IN', 'DATE_OUT')
    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME',
                      'DET') + serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL',
                      'MED_DEV', 'MR_USL_N', 'NPL', 'COMENTU'))
    requiredServiceFields = ('IDSERV', 'LPU', 'PROFIL', 'DET', 'DATE_IN',
                             'DATE_OUT', 'DS', 'CODE_USL', 'KOL_USL',
                             'SUMV_USL')

    serviceSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_V', 'MET_ISSL', 'NAPR_USL'),
                 'dateFields': ('NAPR_DATE',),
                 'requiredFields': ('NAPR_DATE', 'NAPR_V')},
        'MED_DEV': {
            'fields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'),
            'dateFields': ('DATE_MED',),
            'requiredFields': ('DATE_MED', 'CODE_MEDDEV', 'NUMBER_SER'), },
        'MR_USL_N': {
            'fields': ('MR_N', 'PRVS', 'CODE_MD'),
            'requiredFields': ('MR_N', 'PRVS', 'CODE_MD'), },
    }

    mapEventOrderToPPer = {5: '4', 7: '3'}
    mapEventOrderToForPom = {1: '3', 2: '1', 3: '1', 4: '3', 5: '3', 6: '2'}

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
        self.__serviceNumber = 0

    def writeHeader(self, params):
        u'Запись заголовка xml файла'
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeElement('VERSION', '3.2')
        self.writeElement('DATA', date.toString(Qt.ISODate))
        self.writeElement('FILENAME', params['shortFileName'][:-4])
        self.writeElement('SD_Z', self._parent.getCompleteEventCount())
        self.writeEndElement()  # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '{0}'.format(params['accId']))
        self.writeElement('CODE_MO', params['lpuCodeTfoms75MO'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeElement('NSCHET', params['NSCHET'])
        self.writeElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeElement('PLAT', params['payerCode'])
        self.writeElement('SUMMAV', forceString(params['accountSum']))
        if params['isReexposed'] == '1':
            self.writeStartElement('REF')
            record = self._db.getRecordEx('Account', 'id, settleDate',
                                          u'number=\'{0}\''.format(params['reexposedAccountNumber']))
            if record:
                self.writeElement('FIRST_CODE', forceString(record.value(0)))
                settleDate = forceDate(record.value(1))
                self.writeElement('FIRST_YEAR', settleDate.year())
                self.writeElement('FIRST_MONTH', settleDate.month())
            else:
                self._parent.logError(u'Счёт `{0}` не найден в БД'.format(
                    params['reexposedAccountNumber']))
            self.writeEndElement()  # REF
        self.writeEndElement()  # SCHET

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

    def handleEmptyRequiredField(self, field, prefix):
        self._parent.logError(
            u'Событие `{0}`: отсутствует обязательное поле {1}.{2}'
            .format(self._lastEventId if self._lastEventId
                    else self._lastCompleteEventId, prefix, field))

    def writeRecord(self, record, params):
        clientId = forceRef(record.value('PACIENT_ID_PAC'))
        lastEventId = forceRef(record.value('lastEventId'))

        if params['isReexposed'] != '1':
            record.setValue('Z_SL_FIRST_IDCASE', toVariant(''))

        if (clientId != self._lastClientId
                or lastEventId != self._lastCompleteEventId
        ):
            if self._lastClientId:
                if self._lastRecord:
                    self.writeEndElement()  # SL
                    self.writeGroup(
                        'Z_SL', self.completeEventFields2, self._lastRecord,
                        closeGroup=True, openGroup=False,
                        requiredFields=self.requiredCompleteEventFields)
                self.writeEndElement()  # ZAP

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
            record.setValue('SL_TARIF', toVariant(
                params['mapEventIdToSum'].get(eventId)))

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
                eventOrder) if eventOrder in (1, 2) else '')
            local_params['SL_P_PER'] = self.mapEventOrderToPPer.get(
                eventOrder)

            if not local_params['SL_P_PER']:
                delivered = forceString(record.value('delivered')) == u'СМП'
                local_params['SL_P_PER'] = '2' if delivered else '1'

        mkb = forceString(record.value('SL_DS1'))
        reab = forceInt(record.value('SL_REAB'))
        crit = forceString(record.value('KSG_KPG_CRIT')).split(',')
        isChild = forceBool(record.value('SL_DET'))
        uslOk = forceInt(record.value('Z_SL_USL_OK'))
        isCovidMedicalSuppliesUsed = (
                mkb in ('U07.1', 'U07.2') and reab != 1
                and (('STT5' not in crit and uslOk == 1) or uslOk == 3))
        if not isCovidMedicalSuppliesUsed:
            record.setValue('SL_WEI', '')

        if ((uslOk == 3 and mkb and (mkb[0] == 'Z' or
                                     (mkb >= 'U11' and mkb <= 'U11.9')))
                or uslOk not in (1, 2, 3)):
            record.setNull('SL_C_ZAB')

        local_params.update(params)
        self.__serviceNumber = 0

        if self._lastEventId:
            self.writeEndElement()  # SL

        if params['isHospital']:
            bedProfileCode = local_params['bedProfileCode']
            if bedProfileCode:
                local_params['SL_PROFIL_K'] = (
                    self.getHospitalBedProfileTfomsCode(bedProfileCode))

            local_params['KSG_KPG_VER_KSG'] = params['settleDate'].year()
            local_params['KSG_KPG_BZTSZ'] = (
                self.contractAttributeByType(
                    u'BZTSZ_ДС' if local_params['medicalAidTypeCode'] == '7'
                    else u'BZTSZ_КС', params['contractId']))
            local_params['KSG_KPG_KOEF_U'] = (
                self.contractAttributeByType(
                    u'KOEF_U_ДС' if local_params['medicalAidTypeCode'] == '7'
                    else u'KOEF_U_КС', params['contractId']))
            local_params['KSG_KPG_KOEF_D'] = (
                self.contractAttributeByType('KOEF_D', params['contractId']))
            local_params.update(self.getCoefficients(record, params))

        local_params['SL_DS2'] = forceString(record.value('ds2List')).split(',')
        local_params.update(params.get('onkologyInfo', {}).get(eventId, {}))
        if isCovidMedicalSuppliesUsed:
            isChild = forceBool(record.value('SL_DET'))
            mkb2 = forceString(record.value('SL_DS2'))[:3]
            if (mkb2 not in ('Z34', 'Z35')
                    and not (mkb2 and 'O00' >= mkb2 and mkb2 <= 'O99') and not isChild):
                local_params.update(params.get(
                    'medicalSuppliesInfo', {}).get(eventId, {}))

        if local_params.get('isOnkology'):
            fieldName = ('USL_CODE_USL' if local_params.get('ONK_USL_USL_TIP')
                                           in (1, 3, 4) else 'mesServiceCode')
            record.setValue('USL_VID_VME', record.value(fieldName))
            mkb = forceString(record.value('SL_DS1'))[:5]
            if 'C81' <= mkb <= 'C96':
                local_params['LEK_PR_CODE_SH'] = [u'нет'] * len(
                    local_params.get('LEK_PR_CODE_SH', []))

        _record = CExtendedRecord(record, local_params, DEBUG)
        idsp = params['idsp']

        if ((forceInt(self._lastRecord.value('Z_SL_USL_OK')) == 3
             and idsp == 28)
                or params['isHospital']):  # см. #0011123:0037003
            _record.setValue('SL_ED_COL', toVariant(
                self.evalUSLCount(eventId, params)))
        self.writeGroup('SL', self.eventFields, _record,
                        self.eventHospSubGroup if params[
                            'isHospital'] else self.eventSubGroup,
                        closeGroup=False, dateFields=self.eventDateFields,
                        requiredFields=self.requiredEventFields)
        self._lastEventId = eventId

    def writeCompleteEvent(self, record, params):
        lastEventId = forceRef(record.value('lastEventId'))
        patrName = forceString(record.value('PERS_OT'))
        firstName = forceString(record.value('PERS_IM'))
        noPatrName = not patrName or patrName.upper() == u'НЕТ'
        noFirstName = not firstName or firstName.upper() == u'НЕТ'

        local_params = {}
        local_params.update(params['mapEventIdToKsgKpg'].get(lastEventId, {}))

        code = forceInt(record.value('eventProfileRegionalCode'))
        eventId = forceRef(record.value('eventId'))
        onkologyInfo = params.get('onkologyInfo', {}).get(eventId, {})
        isOnkology = onkologyInfo.get('isOnkology')
        isSuspicion = onkologyInfo.get('SL_DS_ONK')

        if not (code in (1, 2, 3) or isOnkology or isSuspicion):
            record.setNull('Z_SL_NPR_DATE')
            record.setNull('Z_SL_NPR_MO')

        local_params['Z_SL_SUMV'] = params['completeEventSum'].get(lastEventId, '0')
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

        local_params = {}
        local_params.update(params.get('implantsInfo', {}).get(eventId, {}))
        local_params.update(params)

        if idsp == 28:
            record.setValue('USL_VID_VME', record.value('USL_CODE_USL'))

        if isHospital:
            actions = []

            if (eventId and eventId not in self._exportedActions):
                actions = self.actions(eventId, params)
                eventCSGCode = forceString(record.value('eventCSGCode'))
                actions.extend(self.csgs(eventId, eventCSGCode))

            for action in actions:
                params['USL_DET'] = record.value('SL_DET')
                self.__serviceNumber += 1
                local_params['USL_IDSERV'] = self.__serviceNumber
                local_params.update(params)
                _record = CExtendedRecord(action, local_params, DEBUG)
                _record.setValue('USL_CODE_USL',
                                 self.hospitalServiceCode(_record, params))

                self.writeGroup('USL', self.serviceFields, _record,
                                subGroup=self.serviceSubGroup,
                                dateFields=self.serviceDateFields,
                                requiredFields=self.requiredServiceFields)

            self._exportedActions.add(eventId)

            if not forceRef(record.value('actionId')):
                return

            record.setValue('USL_KOL_USL', record.value('actionAmount'))

        record.setValue('USL_DS',
                        toVariant(forceString(record.value('USL_DS'))[:5]))

        if not forceRef(record.value('visitId')):
            if isStomatology:
                self.writeVisits(record, params, eventId, isAmbulance,
                                 isStomatology)

            self.__serviceNumber += 1

            if isStomatology or isHospital:
                record.setValue('USL_DATE_IN', record.value('serviceDate'))
                record.setValue('USL_DATE_OUT', record.value('serviceDate'))

            local_params.update(params)
            local_params['USL_IDSERV'] = self.__serviceNumber
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            subGroup=self.serviceSubGroup,
                            dateFields=self.serviceDateFields,
                            requiredFields=self.requiredServiceFields)

        else:
            self.writeVisits(record, local_params, eventId, isAmbulance,
                             isStomatology)

        if (isStomatology and
                eventId not in self._exportedNomenclativeServices):
            self.writeNomenclativeServices(record, eventId, True, params)

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
                record.setValue('USL_KOL_USL', toVariant(amount * coeff))

            self.__serviceNumber += 1
            local_params = {'USL_IDSERV': self.__serviceNumber}
            local_params.update(params)
            _record = CExtendedRecord(record, local_params, DEBUG)
            self.writeGroup('USL', self.serviceFields, _record,
                            subGroup=self.serviceSubGroup,
                            dateFields=self.serviceDateFields,
                            requiredFields=self.requiredServiceFields)

        self._exportedNomenclativeServices.add(eventId)

    def writeVisits(self, record, params, eventId, isAmbulance, isStomatology):
        u'Выгружает визиты по заданному событию'
        if eventId and eventId not in self._exportedEvents:
            params['tarif'] = record.value('SL_TARIF')
            params['sum'] = record.value('SL_SUM_M')
            params['amount'] = record.value('SL_ED_COL')
            visitRecords = self.getVisits(eventId, params)

            if isStomatology or isAmbulance:
                if not visitRecords:
                    record.setValue('USL_DATE_IN', record.value('visitDate'))
                    record.setValue('USL_DATE_OUT', record.value('visitDate'))
                    self.__serviceNumber = +1
                    local_params = {'USL_IDSERV': self.__serviceNumber}
                    local_params.update(params)
                    _record = CExtendedRecord(record, local_params, DEBUG)
                    self.writeGroup('USL', self.serviceFields, _record,
                                    subGroup=self.serviceSubGroup,
                                    dateFields=self.serviceDateFields)

            for visit in visitRecords:
                if isAmbulance:
                    if visitRecords.index(visit):
                        code = forceString(visit.value('USL_CODE_USL'))
                        if code[-2:] == '.1':
                            visit.setValue('USL_CODE_USL', '{0}3'.format(code[:-1]))
                    else:
                        visit.setValue('USL_TARIF', record.value('USL_TARIF'))
                        visit.setValue('USL_SUMV_USL', record.value('USL_SUMV_USL'))
                if isStomatology:
                    _sum = forceDouble(visit.value('USL_SUMV_USL'))
                    amount = forceDouble(visit.value('USL_KOL_USL'))
                    visit.setValue('USL_SUMV_USL', roundHalfUp(_sum))
                    visit.setValue('USL_TARIF',
                                   roundHalfUp(_sum / amount) if amount else 0)

                self.writeService(visit, params)

            self._exportedEvents.add(eventId)

    def evalUSLCount(self, eventId, params):
        serviceList = self.getNomenclativeServices(eventId, params)
        visitsList = self.getVisits(eventId, params)
        return (len(serviceList)
                + len(visitsList)
                + params['actionCount'].get(eventId, 0)
                )

    def getVisits(self, eventId, params):
        u'Получает список визитов, с кешированием для исключения лишних запросов'
        if self._visitsCacheKey != eventId:
            self._visitsCacheValue = self.exportVisits(eventId, params)
            self._visitsCacheKey = eventId
        return self._visitsCacheValue

    def exportVisits(self, eventId, params):
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
            IF(rbEventProfile.regionalCode = '6',
                (SELECT SUM(AI.uet) FROM Account_Item AI
                 WHERE AI.event_id = Event.id
                   AND AI.master_id = '{accId}'
                   AND AI.deleted = 0
                   AND AI.serviceDate = Visit.date), 1) AS USL_KOL_USL,
            0 AS USL_TARIF,
            IF(rbEventProfile.regionalCode = '6',
                (SELECT SUM(AI.price*AI.amount) FROM Account_Item AI
                 WHERE AI.event_id = Event.id
                   AND AI.master_id = '{accId}'
                   AND AI.deleted = 0
                   AND AI.serviceDate = Visit.date), 0) AS USL_SUMV_USL,
            Person.federalCode AS USL_IDDOKT,
            (SELECT rSI.value FROM rbSpeciality_Identification rSI
             WHERE rSI.master_id = Person.speciality_id
               AND rSI.deleted = 0
               AND rSI.system_id = (
                SELECT id FROM rbAccountingSystem
                WHERE code = "tfoms75.Speciality")) AS USL_PRVS,
            Person.federalCode AS USL_CODE_MD,

            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS MR_USL_N_CODE_MD
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
        WHERE Visit.event_id = '{eventId}'
            AND Visit.deleted = '0'
            AND (rbVisitType.code = '' OR rbEventProfile.code = '6')
        ORDER BY Visit.date'''.format(eventId=eventId, accId=params['accId'])

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

    def actions(self, eventId, params):
        stmt = u'''SELECT
            Organisation.miacCode AS USL_LPU,
            OrgStructure.infisCode AS USL_LPU_1,
            OrgStructure.tfomsCode AS USL_PODR,
            rbMedicalAidProfile.regionalCode AS USL_PROFIL,
            '0' AS USL_DET,
            A.begDate AS USL_DATE_IN,
            A.endDate AS USL_DATE_OUT,
            A.MKB AS USL_DS,
            (SELECT OI.value FROM rbMedicalAidProfile_Identification OI
                 WHERE OI.master_id = rbMedicalAidProfile.id
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms75CODE_USL}'
                   LIMIT 1) AS USL_CODE_USL,
            1 AS USL_KOL_USL,
            CASE
                WHEN rbMedicalAidType.regionalCode IN (1,2,3) THEN '{BZTSZ_KS}'
                WHEN rbMedicalAidType.regionalCode = 7 THEN '{BZTSZ_DS}'
                ELSE ''
            END AS USL_TARIF,
            IF(A.eventCSG_id IS NOT NULL,
               (SELECT AI.sum FROM Account_Item AI
                WHERE AI.eventCSG_id = A.eventCSG_id
                LIMIT 1), 0) AS USL_SUMV_USL,
            rbSpeciality.federalCode AS USL_PRVS,
            Person.federalCode AS USL_CODE_MD,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS MR_USL_N_CODE_MD,

            IF(age(Client.birthDate,Event.setDate) < 18, 1, 0) AS SL_DET,
            AT.code AS movingCode,
            rbMedicalAidType.code AS medicalAidTypeCode
        FROM Action A
        LEFT JOIN ActionType AT ON A.actionType_id = AT.id
        LEFT JOIN Person ON A.person_id = Person.id
        LEFT JOIN Organisation ON Person.org_id = Organisation.id
        LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService RS ON RS.id = AT.nomenclativeService_id
        LEFT JOIN rbHospitalBedProfile AS BedProfile
            ON BedProfile.id = (
                SELECT HBP.value
                FROM ActionProperty
                LEFT JOIN ActionProperty_rbHospitalBedProfile AS HBP
                    ON HBP.id = ActionProperty.id
                WHERE action_id = A.id
                ORDER BY HBP.id DESC LIMIT 1
            )
        LEFT JOIN rbMedicalAidProfile ON
            BedProfile.medicalAidProfile_id = rbMedicalAidProfile.id
        LEFT JOIN Event ON A.event_id = Event.id
        LEFT JOIN EventType ON Event.eventType_id = EventType.id
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN Client ON Event.client_id = Client.id
        WHERE A.deleted = 0
          AND AT.flatCode = 'moving'
          AND A.event_id = {eventId}
        '''.format(eventId=eventId, **params)

        query = self._parent.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            if record:
                result.append(record)
        return result

    def csgs(self, eventId, eventCSGCode):
        stmt = u'''SELECT
            Organisation.miacCode AS USL_LPU,
            OrgStructure.infisCode AS USL_LPU_1,
            OrgStructure.tfomsCode AS USL_PODR,
            '97' AS USL_PROFIL,
            '0' AS USL_DET,
            A.begDate AS USL_DATE_IN,
            A.endDate AS USL_DATE_OUT,
            A.MKB AS USL_DS,
            rbService.infis AS USL_CODE_USL,
            A.amount AS USL_KOL_USL,
            '0' AS USL_TARIF,
            '0' AS USL_SUMV_USL,
            '1' AS MR_USL_N_MR_N,
            rbSpeciality.federalCode AS MR_USL_N_PRVS,
            Person.federalCode AS MR_USL_N_CODE_MD
        FROM Action A
        LEFT JOIN ActionType AT ON A.actionType_id = AT.id
        LEFT JOIN Person ON A.person_id = Person.id
        LEFT JOIN Organisation ON Person.org_id = Organisation.id
        LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN rbService ON rbService.id = AT.nomenclativeService_id
        WHERE A.deleted = 0 AND rbService.code IN (
            SELECT serviceCode FROM mes.CSG_Service
            INNER JOIN mes.CSG ON mes.CSG.id = mes.CSG_Service.master_id
            WHERE mes.CSG.code = '{csgCode}')
          AND A.status = 2
          AND A.event_id = {eventId}
        '''.format(eventId=eventId, csgCode=eventCSGCode)

        query = self._parent.db.query(stmt)
        result = []

        while query.next():
            record = query.record()
            if record:
                result.append(record)
        return result

    def getCoefficientRegionalCode(self, _code):
        u"""Возвращает региональный код коэффициента по его коду"""
        result = self._coefficientCache.get(_code, -1)

        if result == -1:
            result = forceString(self._parent.db.translate(
                'rbContractCoefficientType', 'code', _code, 'regionalCode'))
            self._coefficientCache[_code] = result

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
        clientId = forceRef(record.value('clientId'))

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
            representative = self.getClientRepresentativeInfo(clientId)
            representativeId = representative.get('id')
            if representativeId:
                policy = getClientPolicy(representativeId)
                if policy:
                    policyKind = forceString(self._db.translate(
                        'rbPolicyKind', 'id', policy.value('policyKind_id'),
                        'regionalCode'))
                    record.setValue('PACIENT_VPOLIS', policyKind)
                    record.setValue(
                        ('PACIENT_NPOLIS'
                         if policyKind != '3'
                            or self._parent.registryType ==
                            self._parent.registryTypeD4
                         else 'PACIENT_ENP'),
                        policy.value('number'))
                    if policyKind != '3':
                        record.setValue('PACIENT_SPOLIS',
                                        policy.value('serial'))

        local_params = {
            'PACIENT_INV': params['tempInvalidMap'].get(clientId, '')
        }
        local_params.update(params)
        _record = CExtendedRecord(record, local_params, DEBUG)
        self.writeGroup('PACIENT', self.clientFields, _record)

    def getCoefficients(self, record, _):
        u'Пишет блок SL_KOEF'

        def formatCoef(_val):
            u"""Обрезает значение коэффициента до 5 знаков без округления"""
            return str(Decimal(str(_val)).quantize(Decimal('.00001')))

        usedCoefficients = forceString(record.value('usedCoefficients'))
        result = {'KSG_KPG_SL_K': 0}
        isItSlNeq1 = False

        if usedCoefficients:
            coefficientList = json.loads(usedCoefficients)
            flag = False

            for _, i in coefficientList.iteritems():
                for key, val in i.iteritems():
                    if key == u'__all__':
                        continue

                    result['KSG_KPG_SL_K'] = 1 if val > 0 else 0
                    isItSlNeq1 = val != 1

                    if val > 0:
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

    def hospitalServiceCode(self, record, params):
        u'Формирует код услуги для стационара'
        prefix = 0
        isChild = forceBool(record.value('SL_DET'))
        isBUAction = forceString(record.value('movingCode')) == u'БУ'
        infix = 0
        medicalAidTypeCode = forceString(record.value('medicalAidTypeCode'))
        if medicalAidTypeCode in ('1', '2', '3'):
            prefix = 5 if isChild else 4
        elif medicalAidTypeCode == '7':
            prefix = 2 if isChild else 1
            if isBUAction:
                infix = 1
        bedProfileCode = forceString(record.value('USL_CODE_USL'))
        result = u'{0}98{1}{2}'.format(prefix, infix, bedProfileCode)
        return result


# ******************************************************************************

class CR80PersonalDataWriter(PersonalDataWriter, CExportHelperMixin):
    u'Осуществляет запись данных экспорта в XML'

    clientDateFields = ('DR_P', 'DOCDATE', 'DR')
    clientFields = ('ID_PAC', 'FAM', 'IM', 'OT', 'W', 'DR', 'DOST', 'TEL',
                    'FAM_P', 'IM_P', 'OT_P', 'W_P', 'DR_P', 'DOST_P', 'MR',
                    'DOCTYPE', 'DOCSER', 'DOCNUM', 'DOCDATE', 'DOCORG', 'SNILS',
                    'OKATOG', 'OKATOP')
    EVENT_EXEC_DATE_FIELD_NAME = 'SL_DATE_2'

    def __init__(self, parent):
        PersonalDataWriter.__init__(self, parent)
        self.version = '3.2'
        CExportHelperMixin.__init__(self)
        self.__exportedClientIds = set()

    def writeHeader(self, params):
        self.__exportedClientIds = set()
        PersonalDataWriter.writeHeader(self, params)

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
            return True
        return False

    def writeRecord(self, record, params):
        u"""Пишет sql запись в файл"""
        clientId = forceRef(record.value('PACIENT_ID_PAC'))

        if (clientId != self._lastClientId
                and clientId not in self.__exportedClientIds):
            self.__exportedClientIds.add(clientId)
            local_params = {}
            local_params.update(params)
            _record = CExtendedRecord(record, local_params, DEBUG)
            if self.writeClientInfo(_record, params):
                self._lastClientId = clientId


# ******************************************************************************

class CR80XmlStreamWriterD4(CR80XmlStreamWriterCommon):
    onkuslSubGroup = {
        'LEK_PR': {'fields': ('REGNUM', 'CODE_SH', 'DATE_INJ'),
                   'requiredFields': ('REGNUM', 'CODE_SH')},
    }

    onkslSubGroup = {
        'B_DIAG': {'fields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE', 'DIAG_RSLT',
                              'REC_RSLT'),
                   'requiredFields': ('DIAG_DATE', 'DIAG_TIP', 'DIAG_CODE')},
        'B_PROT': {'fields': ('PROT', 'D_PROT'),
                   'requiredFields': ('PROT', 'D_PROT'),
                   'dateFields': ('D_PROT',)},
        'ONK_USL': {'fields': ('USL_TIP', 'HIR_TIP', 'LEK_TIP_L',
                               'LEK_TIP_V', 'LEK_PR', 'PPTR', 'LUCH_TIP'),
                    'requiredFields': ('USL_TIP',),
                    'subGroup': onkuslSubGroup},
    }

    consGroup = {'fields': ('PR_CONS', 'DT_CONS'),
                 'requiredFields': ('PR_CONS'), }
    # 'dateFields': ('DT_CONS', )}
    onkSlGroup = {'fields': ('DS1_T', 'STAD', 'ONK_T', 'ONK_N', 'ONK_M',
                             'MTSTZ', 'SOD', 'K_FR', 'WEI', 'HEI', 'BSA',
                             'B_DIAG', 'B_PROT', 'ONK_USL'),
                  'requiredFields': ('DS1_T',),
                  'subGroup': onkslSubGroup}

    eventSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL',
                            'NAPR_USL'),
                 'dateFields': ('NAPR_DATE',)},
        'CONS': consGroup,
        'ONK_SL': onkSlGroup,
    }

    eventHospSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL',
                            'NAPR_USL'),
                 'dateFields': ('NAPR_DATE',)},
        'CONS': consGroup,
        'ONK_SL': onkSlGroup,
        'KSG_KPG': {'fields': ('N_KSG', 'VER_KSG', 'KSG_PG', 'N_KPG',
                               'KOEF_Z', 'KOEF_UP', 'BZTSZ', 'KOEF_D',
                               'KOEF_U', 'CRIT', 'SL_K', 'IT_SL',
                               'SL_KOEF'),
                    'requiredFields': ('VER_KSG', 'KSG_PG', 'KOEF_Z', 'KOEF_UP',
                                       'BZTSZ', 'KOEF_D', 'KOEF_U', 'SL_K',),
                    'subGroup': CR80XmlStreamWriterCommon.ksgSubGroup},
    }

    eventFields1 = (('SL_ID', 'LPU_1', 'PODR', 'PROFIL', 'PROFIL_K', 'DET',
                     'P_CEL', 'NHISTORY', 'P_PER')
                    + CR80XmlStreamWriterCommon.eventDateFields +
                    ('KD', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK', 'DN',
                     'CODE_MES1', 'CODE_MES2', 'NAPR', 'CONS', 'ONK_SL',
                     'KSG_KPG'))

    serviceFields = (('IDSERV', 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME',
                      'DET') + CR80XmlStreamWriterCommon.serviceDateFields +
                     ('DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL', 'PRVS',
                      'CODE_MD', 'NPL', 'COMENTU'))

    serviceSubGroup = {
        'NAPR': {'fields': ('NAPR_DATE', 'NAPR_V', 'MET_ISSL', 'NAPR_USL'),
                 'dateFields': ('NAPR_DATE',),
                 'requiredFields': ('NAPR_DATE', 'NAPR_V')},
    }

    clientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO',
                    'SMO_NAM', 'INV', 'MSE', 'NOVOR')

    def __init__(self, parent):
        CR80XmlStreamWriterCommon.__init__(self, parent)

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
        self.writeEndElement()  # ZGLV

        self.writeStartElement('SCHET')
        self.writeElement('CODE', '{0}'.format(params['accId']))
        self.writeElement('CODE_MO', params['lpuCodeTfoms75MO'])
        self.writeElement('YEAR', forceString(settleDate.year()))
        self.writeElement('MONTH', forceString(settleDate.month()))
        self.writeElement('NSCHET', params['NSCHET'])
        self.writeElement('DSCHET', params['accDate'].toString(Qt.ISODate))
        self.writeElement('PLAT', params['payerCode'])
        self.writeElement('SUMMAV', forceString(params['accountSum']))
        self.writeEndElement()  # SCHET

        self._recNum = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastCompleteEventId = None
        self._lastRecord = None

    def writeRecord(self, record, params):
        if self._parent.registryType == CR80ExportPage1.registryTypeD4:
            CR80XmlStreamWriterCommon.writeRecord(self, record, params)
            self._parent._parent.anyOnkology = True


# ******************************************************************************

class CR80XmlStreamWriter(CR80XmlStreamWriterCommon):
    conditionalFields = ('NPR_DATE', 'NPR_MO')
    requiredFields = ('PR_NOV', 'ID_PAC', 'VPOLIS', 'VIDPOM', 'LPU',
                      'VBR', 'NHISTORY', 'P_OTK', 'DATE_1', 'DATE_2', 'DS1',
                      'RSLT_D', 'IDSP', 'TARIF', 'SUMV', 'IDDOKT', 'IDSERV',
                      'DATE_IN', 'DATE_OUT', 'CODE_USL', 'SUMV_USL', 'PRVS',
                      'CODE_MD')

    def __init__(self, parent):
        CR80XmlStreamWriterCommon.__init__(self, parent)
        self.__currentRecord = None

    def writeRecord(self, record, params):
        eventId = forceRef(record.value('eventId'))
        onkInfo = params['onkologyInfo'].get(eventId, {})
        isOnkology = onkInfo.get('isOnkology')
        isSuspicion = onkInfo.get('SL_DS_ONK')
        self.__currentRecord = record

        if (not (isOnkology or isSuspicion) and
                self._parent.registryType == CR80ExportPage1.registryTypeD1):
            CR80XmlStreamWriterCommon.writeRecord(self, record, params)

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

class CD4PersonalDataWriter(CR80PersonalDataWriter):
    u'Осуществляет запись данных экспорта в XML'

    def __init__(self, parent):
        CR80PersonalDataWriter.__init__(self, parent)
        self.version = '3.2'

    def writeClientInfo(self, record, params):
        if self._parent.registryType == CR80ExportPage1.registryTypeD4:
            CR80PersonalDataWriter._writeClientInfo(self, record, params)

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
        self.writeEndElement()  # ZGLV


# ******************************************************************************

class CR80OnkologyInfo(COnkologyInfo):
    def __init__(self):
        COnkologyInfo.__init__(self)

    def _onkologyMkbStmt(self):
        return u"""DS.MKB LIKE 'C%' OR DS.MKB BETWEEN 'D01' AND 'D09'
                                    OR DS.MKB BETWEEN 'D45' AND 'D47'
                                    OR DS.MKB IN ('D70', 'Z03.1')"""

    def get(self, _db, idList, parent):
        u"""Возвращает словарь с записями по онкологии и направлениям,
            ключ - идентификатор события"""
        stmt = u"""SELECT Event.id AS eventId,
            rbDiseasePhases.code AS diseasePhaseCode,
            rbEventTypePurpose.regionalCode AS uslOk,
            Diagnosis.MKB,
            AccDiagnosis.MKB AS accMKB,
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
            (SELECT GROUP_CONCAT(A.id)
                FROM Action A
                WHERE A.event_id = Event.id
                  AND A.deleted = 0
                  AND A.actionType_id IN (
                    SELECT AT.id
                    FROM ActionType AT
                    WHERE AT.flatCode ='Consilium'
            )) AS consiliumActionId,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'directionCancer'
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
                 WHERE AT.flatCode = 'MedicalSupplies')
             ORDER BY A.begDate
            ) AS medicalSuppliesActionId,
            (SELECT AT.code
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.group_id IN (
                            SELECT id FROM ActionType AT1
                            WHERE AT1.flatCode IN ('codeSH', 'МНН ЛП в сочетании с ЛТ'))
                WHERE A.event_id = Event.id AND A.deleted = 0
                LIMIT 0,1
            ) AS LEK_PR_CODE_SH,
            KFrAction.id AS kFrActionId,
            (SELECT OI.value FROM rbMedicalAidType_Identification OI
                 WHERE OI.master_id = rbMedicalAidType.id
                   AND OI.deleted = 0
                   AND OI.system_id = '{sysIdTfoms75USL_OK}'
                   LIMIT 1) AS medicalAidTypeCode
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN Diagnostic ON Diagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND ({mkbStmt})
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
        LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            LEFT JOIN rbDiagnosisType DT ON DT.id = D.diagnosisType_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND DT.code = '9' AND DS.MKB LIKE 'C%'
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = AccDiagnostic.diagnosis_id
            AND AccDiagnosis.deleted = 0 AND (AccDiagnosis.MKB LIKE 'C%')
        LEFT JOIN Diagnostic AnyDiagnostic ON AnyDiagnostic.id = IFNULL(Diagnostic.id, AccDiagnostic.id)
        LEFT JOIN rbDiseasePhases ON AnyDiagnostic.phase_id = rbDiseasePhases.id
        LEFT JOIN rbTNMphase ON rbTNMphase.id = IFNULL(AnyDiagnostic.pTNMphase_id, AnyDiagnostic.cTNMphase_id)
        LEFT JOIN rbTumor ON rbTumor.id = IFNULL(AnyDiagnostic.pTumor_id, AnyDiagnostic.cTumor_id)
        LEFT JOIN rbNodus ON rbNodus.id = IFNULL(AnyDiagnostic.pNodus_id, AnyDiagnostic.cNodus_id)
        LEFT JOIN rbMetastasis ON rbMetastasis.id = IFNULL(AnyDiagnostic.pMetastasis_id, AnyDiagnostic.cMetastasis_id)
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
        LEFT JOIN rbDispanser ON AnyDiagnostic.dispanser_id = rbDispanser.id
        LEFT JOIN EventType_Identification ON
            EventType_Identification.master_id = EventType.id
            AND EventType_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfomsPCEL'
        )
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN rbTNMphase_Identification ON
            rbTNMphase_Identification.master_id = IFNULL(
                AnyDiagnostic.cTNMphase_id, AnyDiagnostic.pTNMphase_id)
            AND rbTNMphase_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'TNMphase'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                AnyDiagnostic.cTumor_id, AnyDiagnostic.pTumor_id)
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Tumor'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                AnyDiagnostic.cNodus_id, AnyDiagnostic.pNodus_id)
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Nodus'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                AnyDiagnostic.cMetastasis_id, AnyDiagnostic.pMetastasis_id)
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
          AND (Diagnosis.MKB IS NOT NULL OR AccDiagnosis.MKB IS NOT NULL)
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Account_Item.event_id""".format(
            idList=idList, mkbStmt=self._onkologyMkbStmt(),
            sysIdTfoms75USL_OK=parent._getAccSysId('tfoms75.USL_OK'))

        query = _db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result[eventId] = self._processOnkRecord(record, parent)

        return result

    def _isOnkology(self, record):
        mkb = forceString(record.value('MKB'))[:3]
        accMkb = forceString(record.value('accMKB'))[:3]
        phase = forceInt(record.value('diseasePhaseCode'))
        medicalAidTypeCode = forceString(record.value('medicalAidTypeCode'))

        isNeutropenic = (mkb == 'D70' and (
                (accMkb >= 'C00' and accMkb <= 'C80') or accMkb == 'C97'))
        dsOnk = (1 if (phase == 10 and (
                mkb[:1] == 'C' or isNeutropenic or
                (mkb[:3] >= 'D01' and mkb[:3] <= 'D09') or
                (mkb[:3] >= 'D45' and mkb[:3] <= 'D47'))) else 0)
        isOnkology = (mkb[:1] == 'C' or (
                (mkb[:3] >= 'D01' and mkb[:3] <= 'D09') or
                (mkb[:3] >= 'D45' and mkb[:3] <= 'D47') or isNeutropenic)
                      ) and dsOnk == 0 and medicalAidTypeCode != '4'
        return dsOnk, isOnkology

    def _processConsilium(self, record, data):
        COnkologyInfo._processConsilium(self, record, data)
        mkb = forceString(record.value('MKB'))[:3]
        if (mkb[:1] == 'C' or (
                (mkb[:3] >= 'D01' and mkb[:3] <= 'D09') or
                (mkb[:3] >= 'D45' and mkb[:3] <= 'D47'))) and forceString(
            record.value('medicalAidTypeCode')) == '4':
            data['CONS_PR_CONS'] = 0

    def _processDiagnostics(self, record, data):
        u'Заполняет поля для диагностик'
        for field, diagType in (('gistologiaActionId', 1),
                                ('immunohistochemistryActionId', 2)):
            _id = forceRef(record.value(field))
            action = CAction.getActionById(_id) if _id else None

            if not (action and action.getProperties()):
                continue

            diagDate = None

            for prop in action.getProperties():
                if forceString(prop.type().descr) == 'DIAG_DATE':
                    val = prop.getValue()

                    if val and val.isValid():
                        diagDate = val.toString(Qt.ISODate)

                    continue

                text = prop.getTextScalar().strip()
                descr = forceString(prop.type().descr).strip()

                if not text or not descr:
                    continue

                data.setdefault('B_DIAG_DIAG_DATE', []).append(diagDate)
                data.setdefault('B_DIAG_DIAG_TIP', []).append(diagType)
                data.setdefault('B_DIAG_DIAG_CODE', []).append(descr)
                rslt = text.split('.')[0]
                data.setdefault('B_DIAG_DIAG_RSLT', []).append(rslt)
                data.setdefault('B_DIAG_REC_RSLT', []).append(
                    1 if rslt else None)


class CMedicalSuppliesInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)

    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        Action.endDate AS LEK_PR_DATA_INJ,
        CONCAT(
         (SELECT APS.value FROM ActionProperty AP
          INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
          INNER JOIN ActionProperty_String APS ON APS.id = AP.id
          WHERE APT.descr = 'CODE_SH'
            AND AP.deleted = 0 AND AP.action_id = Action.id
          LIMIT 1),
         '-',
         (SELECT NT.code FROM ActionProperty AP
          INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
          INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
          INNER JOIN rbNomenclature ON rbNomenclature.id = APN.value
          INNER JOIN rbNomenclatureType NT ON NT.id = rbNomenclature.type_id
          WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.inActionsSelectionTable = 1
           AND APT.typeName = 'Номенклатура ЛСиИМН'
          LIMIT 1)
        ) AS LEK_PR_CODE_SH,
        (SELECT NI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature ON rbNomenclature.id = APN.value
         INNER JOIN rbNomenclatureType ON
            rbNomenclature.type_id = rbNomenclatureType.id
         INNER JOIN rbNomenclature_Identification NI ON
            NI.master_id = rbNomenclature.id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.inActionsSelectionTable = 1
           AND APT.typeName = 'Номенклатура ЛСиИМН'
           AND NI.system_id = '{sysIdTfoms75N020}'
           AND NI.deleted = 0
           AND rbNomenclatureType.code IN (1, 2)
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
         INNER JOIN rbUnit_Identification UI ON
            UI.master_id = rbNomenclature.unit_id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.inActionsSelectionTable = 1
           AND APT.typeName = 'Номенклатура ЛСиИМН'
           AND UI.system_id = '{sysIdMzUnit}'
           AND UI.deleted = 0
         LIMIT 1) AS LEK_DOSE_ED_IZM,
        (SELECT APD.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Double APD ON APD.id = AP.id
         WHERE APT.inActionsSelectionTable = 2
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1) AS LEK_DOSE_DOSE_INJ,
        (SELECT UI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclatureUsingType APN ON APN.id = AP.id
         INNER JOIN rbNomenclatureUsingType_Identification UI ON
            APN.value = UI.master_id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.inActionsSelectionTable = 3
           AND UI.system_id = '{sysIdNomenclatureUsingType}'
           AND UI.deleted = 0
         LIMIT 1) AS LEK_DOSE_METHOD_INJ,
        (SELECT API.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_Integer API ON API.id = AP.id
         WHERE APT.descr = 'COL_INJ'
           AND AP.deleted = 0 AND AP.action_id = Action.id
         LIMIT 1) AS LEK_DOSE_COL_INJ
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN ActionType_Identification ATI ON ATI.master_id = ActionType.id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ATI.value = 'MedicalSupplies'
          AND ATI.system_id = '{sysIdTfoms75ActionType}'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""".format(
            idList=self._idList,
            sysIdTfoms75ActionType=self._parent._getAccSysId('tfoms75.ActionType'),
            sysIdTfoms75N020=self._parent._getAccSysId('tfoms75.N020'),
            sysIdMzUnit=self._parent._getAccSysId('mz.unit'),
            sysIdNomenclatureUsingType=self._parent._getAccSysId(
                'tfoms75.NomenclatureUsingType'))
        return stmt


class CImplantsInfo(CMultiRecordInfo):
    def __init__(self):
        CMultiRecordInfo.__init__(self)

    def _stmt(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
        Action.endDate AS MED_DEV_DATE_MED,
        (SELECT NI.value FROM ActionProperty AP
         INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
         INNER JOIN ActionProperty_rbNomenclature APN ON APN.id = AP.id
         INNER JOIN rbNomenclature ON rbNomenclature.id = APN.value
         INNER JOIN rbNomenclature_Identification NI ON
            NI.master_id = rbNomenclature.id
         WHERE AP.deleted = 0 AND AP.action_id = Action.id
           AND APT.descr = 'CODE_MEDDEV'
           AND NI.system_id = '{sysIdTfoms75MEDDEV}'
           AND NI.deleted = 0
         LIMIT 1) AS MED_DEV_CODE_MEDDEV,
        (SELECT APS.value FROM ActionProperty AP
          INNER JOIN ActionPropertyType APT ON AP.type_id = APT.id
          INNER JOIN ActionProperty_String APS ON APS.id = AP.id
          WHERE APT.descr = 'NUMBER_SER'
            AND AP.deleted = 0 AND AP.action_id = Action.id
          LIMIT 1) AS MED_DEV_NUMBER_SER
        FROM Account_Item
        LEFT JOIN Action ON Action.event_id = Account_Item.event_id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN ActionType_Identification ATI ON ATI.master_id = ActionType.id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ATI.value = 'Implantation'
          AND ATI.system_id = '{sysIdTfoms75ActionType}'
          AND Action.deleted = 0
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}""".format(
            idList=self._idList,
            sysIdTfoms75ActionType=self._parent._getAccSysId('tfoms75.ActionType'),
            sysIdTfoms75MEDDEV=self._parent._getAccSysId('tfoms75.MEDDEV'))
        return stmt


# ******************************************************************************

if __name__ == '__main__':
    # pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport

    # pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR80Hospital,
                      configFileName=u'lokosova_gkb2_13022023.ini',
                      eventIdList=[222926]
                      # accNum=u'3-11'
                      )
